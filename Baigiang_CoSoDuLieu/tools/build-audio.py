"""Dựng nhạc nền, hiệu ứng và trộn với giọng đọc theo timeline.

- Nhạc nền ambient/tech sinh bằng numpy, tự duck theo giọng đọc.
- SFX: whoosh, chime, sparkle, success, error, riser, boot, keyboard.
- Xuất build/audio/mix.wav (48k stereo) và mix.m4a.
"""
import json, os, subprocess, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(20241110)
FF = subprocess.run(['node', '-e', "console.log(require('ffmpeg-static'))"],
                    capture_output=True, text=True).stdout.strip()
OUT = 'build/audio'
os.makedirs(OUT, exist_ok=True)
tl = json.load(open('build/timeline.json', encoding='utf-8'))
DUR = tl['duration']
N = int(np.ceil(DUR * SR))
print(f'timeline {DUR:.1f}s = {N} samples')


def read_wav(path):
    with wave.open(path, 'rb') as w:
        assert w.getframerate() == SR and w.getnchannels() == 2 and w.getsampwidth() == 2, path
        a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2')
    return a.reshape(-1, 2)


def write_wav(path, stereo):
    x = np.clip(stereo, -32768, 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(x.tobytes())


def env_adsr(n, a=0.01, r=0.3):
    e = np.ones(n, dtype=np.float32)
    na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na: e[:na] = np.linspace(0, 1, na) ** 2
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


# ---------- narration ----------
nar = np.zeros((N, 2), dtype=np.float32)
missing = []
for sc in tl['scenes']:
    p = f"build/voice/scenes/{sc['id']}.wav"
    if not os.path.exists(p):
        missing.append(sc['id']); continue
    a = read_wav(p).astype(np.float32) / 32768.0
    off = int(round((sc['start'] + sc['lead']) * SR))
    end = min(N, off + len(a))
    seg = a[:end - off].copy()
    f = min(len(seg), int(0.006 * SR))
    if f:
        seg[:f] *= np.linspace(0, 1, f)[:, None]
        seg[-f:] *= np.linspace(1, 0, f)[:, None]
    nar[off:end] += seg
if missing:
    raise SystemExit('missing voice: ' + ', '.join(missing))
print('narration built')

# ---------- music ----------
# A minor ambient progression, 8 s per chord
bpm_pulse = 0.5  # 120 bpm eighth
chords = [
    [110.00, 164.81, 220.00, 261.63],   # Am
    [87.31, 130.81, 174.61, 220.00],    # F
    [130.81, 196.00, 261.63, 329.63],   # C
    [98.00, 146.83, 196.00, 246.94],    # G
]
CH = 8.0
seg_n = int(CH * SR)
music = np.zeros(N, dtype=np.float32)
pos = 0
ci = 0
while pos < N:
    t = np.arange(min(seg_n, N - pos), dtype=np.float32) / SR
    root, fifth, octv, third = chords[ci % 4]
    e = env_adsr(len(t), a=1.4, r=1.6)
    wave_ = (0.50 * np.sin(2 * np.pi * root * t)
             + 0.26 * np.sin(2 * np.pi * fifth * t + 0.3)
             + 0.16 * np.sin(2 * np.pi * octv * t + 0.7)
             + 0.10 * np.sin(2 * np.pi * third * t * 1.003 + 1.1)
             + 0.06 * np.sin(2 * np.pi * root * 2 * t + 0.2))
    # slow breathing filter via amplitude LFO
    wave_ *= (0.82 + 0.18 * np.sin(2 * np.pi * 0.055 * t + ci))
    music[pos:pos + len(t)] += (wave_ * e * 0.055).astype(np.float32)
    pos += len(t)
    ci += 1

# soft pulse every 2 s
step = int(2.0 * SR)
for p0 in range(0, N, step):
    n = min(int(0.7 * SR), N - p0)
    t = np.arange(n, dtype=np.float32) / SR
    thump = np.sin(2 * np.pi * 52 * t) * np.exp(-7 * t) * 0.035
    music[p0:p0 + n] += thump

# airy plucks (pentatonic) every 1 s, quiet
notes = [523.25, 587.33, 659.25, 783.99, 880.00]
for i, p0 in enumerate(range(int(1.0 * SR), N, int(1.0 * SR))):
    if rng.random() > 0.55:
        continue
    n = min(int(1.4 * SR), N - p0)
    t = np.arange(n, dtype=np.float32) / SR
    f = notes[int(rng.integers(0, len(notes)))]
    pl = np.sin(2 * np.pi * f * t) * np.exp(-4.5 * t) * 0.012
    pl += np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-7 * t) * 0.004
    music[p0:p0 + n] += pl.astype(np.float32)

# fade bed in/out
fi, fo = int(4 * SR), int(6 * SR)
music[:fi] *= np.linspace(0, 1, fi) ** 2
music[-fo:] *= np.linspace(1, 0, fo) ** 2
print('music built')

# ---------- ducking envelope (block-rate, vectorized) ----------
B = 2400  # 50 ms blocks
nb = max(1, N // B)
seg = nar[:nb * B]
rms = np.sqrt((seg[:, 0] ** 2 + seg[:, 1] ** 2).reshape(nb, B).mean(axis=1) / 2).astype(np.float32)
act = np.clip((rms - 0.004) / 0.02, 0, 1)
# one-pole attack/release at 20 Hz
rate = SR / B
ca, cr = np.exp(-1 / (0.12 * rate)), np.exp(-1 / (0.8 * rate))
duck_b = np.empty(nb, dtype=np.float32)
g = 0.0
for i in range(nb):
    v = float(act[i])
    g = v + (g - v) * (ca if v > g else cr)
    duck_b[i] = g
duck = np.repeat(duck_b, B)
if len(duck) < N:
    duck = np.pad(duck, (0, N - len(duck)), mode='edge')
music *= (1.0 - 0.82 * duck[:N])
del duck
print('ducked')

# ---------- sfx ----------
sfx = np.zeros((N, 2), dtype=np.float32)

def add(buf, at, pan=0.0, gain=1.0):
    p0 = int(at * SR)
    if p0 >= N: return
    n = min(len(buf), N - p0)
    l = np.sqrt(0.5 * (1 - pan)); r = np.sqrt(0.5 * (1 + pan))
    sfx[p0:p0 + n, 0] += buf[:n] * gain * l
    sfx[p0:p0 + n, 1] += buf[:n] * gain * r


def key(g=1.0):
    n = int(0.05 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    noise = np.diff(noise, prepend=0)  # highpass-ish
    click = np.sin(2 * np.pi * 2400 * t) * np.exp(-70 * t) * 0.5
    return (noise * np.exp(-45 * t) * 0.5 + click) * 0.5 * g


def whoosh():
    n = int(0.55 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    # simple time-varying lowpass: cumulative smoothing
    k = np.linspace(0.02, 0.35, n).astype(np.float32)
    out = np.empty_like(noise); acc = 0.0
    for i in range(n):
        acc += k[i] * (noise[i] - acc); out[i] = acc
    return out * np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 1.5 * 0.9


def tone_bell(f, dur=1.3, amp=0.5):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = (np.sin(2 * np.pi * f * t) * np.exp(-2.4 * t)
         + 0.45 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-3.5 * t)
         + 0.22 * np.sin(2 * np.pi * f * 3.02 * t) * np.exp(-5 * t))
    return (y * amp).astype(np.float32)


def chime():
    n = int(1.5 * SR); y = np.zeros(n, dtype=np.float32)
    for f, g in [(880, 0.5), (1318.5, 0.28), (1760, 0.18)]:
        b = tone_bell(f, 1.4, g)
        y[:len(b)] += b
    return y * 0.5


def sparkle():
    n = int(1.0 * SR); y = np.zeros(n, dtype=np.float32)
    for i, f in enumerate([1568, 1976, 2349, 3136]):
        p0 = int(i * 0.07 * SR)
        b = tone_bell(f, 0.8, 0.22)
        y[p0:p0 + len(b)] += b[:len(y) - p0]
    return y


def success():
    n = int(0.75 * SR); t = np.arange(n, dtype=np.float32) / SR
    f = np.where(t < 0.22, 659.25, 987.77)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-2.2 * t) * 0.5).astype(np.float32)


def error():
    n = int(0.6 * SR); t = np.arange(n, dtype=np.float32) / SR
    y = (np.sin(2 * np.pi * 128 * t) + 0.6 * np.sin(2 * np.pi * 181 * t)) * np.exp(-4 * t)
    return (np.sign(y) * 0.35 * np.exp(-4 * t)).astype(np.float32)


def riser():
    n = int(1.1 * SR); t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    k = np.linspace(0.01, 0.25, n).astype(np.float32)
    out = np.empty_like(noise); acc = 0.0
    for i in range(n):
        acc += k[i] * (noise[i] - acc); out[i] = acc
    return (out * (t / 1.1) ** 2 * 1.1).astype(np.float32)


def boot():
    n = int(1.3 * SR); t = np.arange(n, dtype=np.float32) / SR
    f = 42 + 320 * (t / 1.3) ** 2
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-1.6 * t) * 0.6
    y += np.sin(2 * np.pi * 36 * t) * np.exp(-3.5 * t) * 0.5
    return y.astype(np.float32)


gens = {'key': key, 'whoosh': whoosh, 'chime': chime, 'sparkle': sparkle,
        'success': success, 'error': error, 'riser': riser, 'boot': boot}
cache = {}
for ev in tl['sfx']:
    typ = ev['type']
    if typ not in gens:
        continue
    if typ not in cache:
        cache[typ] = gens[typ]()
    pan = float(np.clip(rng.normal(0, 0.45), -0.8, 0.8)) if typ in ('key', 'whoosh') else 0.0
    g = 0.32 if typ == 'key' else (0.7 if typ in ('whoosh', 'success', 'error') else 0.55)
    add(cache[typ], ev['t'], pan, g * ev.get('gain', 1.0))
print(f"sfx built: {len(tl['sfx'])} events")

# ---------- mix ----------
nar += music[:, None]
nar += sfx
del music, sfx
mix = nar
peak = float(np.max(np.abs(mix)))
if peak > 0:
    mix *= min(1.0, 0.89 / peak)
np.multiply(mix, 1.02, out=mix)
np.tanh(mix, out=mix)
mix *= 0.94
mix *= 32767
write_wav(f'{OUT}/mix.wav', mix)
print('mix written', f'{OUT}/mix.wav', f'{DUR/60:.2f} min')

subprocess.run([FF, '-y', '-v', 'error', '-i', f'{OUT}/mix.wav',
                '-c:a', 'aac', '-b:a', '192k', f'{OUT}/mix.m4a'], check=True)
print('mix.m4a written')
