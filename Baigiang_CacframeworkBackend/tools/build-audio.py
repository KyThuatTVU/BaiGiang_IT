"""Dựng nhạc nền tech tươi sáng, SFX và trộn với giọng đọc theo timeline.

Xuất build/audio/mix.wav (48k stereo) và build/audio/mix.m4a.
"""
import json, os, subprocess, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(20261111)
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
for sc in tl['scenes']:
    p = f"build/voice/scenes/{sc['id']}.wav"
    if not os.path.exists(p):
        raise SystemExit('missing voice: ' + p)
    a = read_wav(p).astype(np.float32) / 32768.0
    off = int(round(sc['start'] * SR))
    end = min(N, off + len(a))
    seg = a[:end - off].copy()
    f = min(len(seg), int(0.006 * SR))
    if f:
        seg[:f] *= np.linspace(0, 1, f)[:, None]
        seg[-f:] *= np.linspace(1, 0, f)[:, None]
    nar[off:end] += seg
print('narration built')

# ---------- music ----------
# Cmaj7 - G - Am7 - Fmaj7, bright tech bed, 8 s per chord
chords = [
    [130.81, 164.81, 196.00, 246.94],
    [98.00, 123.47, 146.83, 196.00],
    [110.00, 130.81, 164.81, 196.00],
    [87.31, 110.00, 130.81, 164.81],
]
CH = 8.0
seg_n = int(CH * SR)
music = np.zeros(N, dtype=np.float32)
pos, ci = 0, 0
while pos < N:
    t = np.arange(min(seg_n, N - pos), dtype=np.float32) / SR
    root, third, fifth, sev = chords[ci % 4]
    e = env_adsr(len(t), a=1.2, r=1.5)
    pad = (0.46 * np.sin(2 * np.pi * root * t)
           + 0.20 * np.sin(2 * np.pi * third * t + 0.2)
           + 0.16 * np.sin(2 * np.pi * fifth * t + 0.6)
           + 0.08 * np.sin(2 * np.pi * sev * t + 1.0)
           + 0.05 * np.sin(2 * np.pi * root * 2 * t + 0.3))
    pad *= (0.84 + 0.16 * np.sin(2 * np.pi * 0.06 * t + ci))
    music[pos:pos + len(t)] += (pad * e * 0.045).astype(np.float32)
    pos += len(t)
    ci += 1

# light arpeggio every 0.5 s, pentatonic C
arp = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50]
for i, p0 in enumerate(range(int(0.5 * SR), N, int(0.5 * SR))):
    if rng.random() > 0.42:
        continue
    n = min(int(0.75 * SR), N - p0)
    t = np.arange(n, dtype=np.float32) / SR
    f = arp[(i * 3 + int(rng.integers(0, 2))) % len(arp)]
    pl = np.sin(2 * np.pi * f * t) * np.exp(-7 * t) * 0.010
    pl += np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-11 * t) * 0.003
    music[p0:p0 + n] += pl.astype(np.float32)

# soft pulse every 2 s
for p0 in range(0, N, int(2.0 * SR)):
    n = min(int(0.5 * SR), N - p0)
    t = np.arange(n, dtype=np.float32) / SR
    music[p0:p0 + n] += (np.sin(2 * np.pi * 58 * t) * np.exp(-9 * t) * 0.022).astype(np.float32)

fi, fo = int(3 * SR), int(5 * SR)
music[:fi] *= np.linspace(0, 1, fi) ** 2
music[-fo:] *= np.linspace(1, 0, fo) ** 2
print('music built')

# ---------- ducking ----------
B = 2400
nb = max(1, N // B)
seg = nar[:nb * B]
rms = np.sqrt((seg[:, 0] ** 2 + seg[:, 1] ** 2).reshape(nb, B).mean(axis=1) / 2).astype(np.float32)
act = np.clip((rms - 0.004) / 0.02, 0, 1)
rate = SR / B
ca, cr = np.exp(-1 / (0.10 * rate)), np.exp(-1 / (0.75 * rate))
duck_b = np.empty(nb, dtype=np.float32)
g = 0.0
for i in range(nb):
    v = float(act[i])
    g = v + (g - v) * (ca if v > g else cr)
    duck_b[i] = g
duck = np.repeat(duck_b, B)
if len(duck) < N:
    duck = np.pad(duck, (0, N - len(duck)), mode='edge')
music *= (1.0 - 0.80 * duck[:N])
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


def tone_bell(f, dur=1.2, amp=0.4):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = (np.sin(2 * np.pi * f * t) * np.exp(-2.6 * t)
         + 0.42 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-3.8 * t)
         + 0.18 * np.sin(2 * np.pi * f * 3.02 * t) * np.exp(-5.5 * t))
    return (y * amp).astype(np.float32)


def whoosh(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    k = np.linspace(0.02, 0.30, n).astype(np.float32)
    out = np.empty_like(noise); acc = 0.0
    for i in range(n):
        acc += k[i] * (noise[i] - acc); out[i] = acc
    return (out * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.4 * 0.8).astype(np.float32)


def pop():
    n = int(0.22 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    f = 620 * np.exp(-9 * t) + 150
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-16 * t) * 0.7
    y[:int(0.004 * SR)] += rng.standard_normal(int(0.004 * SR)) * 0.25
    return y.astype(np.float32)


def click():
    n = int(0.07 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = np.sin(2 * np.pi * 2300 * t) * np.exp(-90 * t) * 0.55
    y += rng.standard_normal(n).astype(np.float32) * np.exp(-120 * t) * 0.2
    return y.astype(np.float32)


def marker():
    n = int(0.24 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    k = np.linspace(0.05, 0.22, n).astype(np.float32)
    out = np.empty_like(noise); acc = 0.0
    for i in range(n):
        acc += k[i] * (noise[i] - acc); out[i] = acc
    env = np.sin(np.pi * np.clip(t / 0.24, 0, 1)) ** 2
    y = out * env * 0.55
    y += np.sin(2 * np.pi * 170 * t) * np.exp(-22 * t) * 0.18
    return y.astype(np.float32)


def hover():
    n = int(0.16 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    f = 880 + 260 * (t / 0.16)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.sin(np.pi * t / 0.16) * 0.24).astype(np.float32)


def data():
    # packet blip: two quick digital chirps, dùng cho request/response
    n = int(0.20 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = np.zeros(n, dtype=np.float32)
    for p0, f0, f1 in [(0.0, 1500, 2100), (0.075, 1900, 2500)]:
        a, b = int(p0 * SR), int((p0 + 0.075) * SR)
        tt = np.arange(b - a, dtype=np.float32) / SR
        f = f0 + (f1 - f0) * (tt / 0.075)
        ph = 2 * np.pi * np.cumsum(f) / SR
        y[a:b] += (np.sin(ph) * np.exp(-34 * tt) * 0.30).astype(np.float32)
    return y


def tick():
    n = int(0.09 * SR)
    t = np.arange(n, dtype=np.float32) / SR
    y = np.sin(2 * np.pi * 1600 * t) * np.exp(-55 * t) * 0.42
    y += np.sin(2 * np.pi * 820 * t) * np.exp(-40 * t) * 0.22
    return y.astype(np.float32)


def chime():
    n = int(1.4 * SR); y = np.zeros(n, dtype=np.float32)
    for f, g in [(880, 0.5), (1318.5, 0.28), (1760, 0.16)]:
        b = tone_bell(f, 1.3, g)
        y[:len(b)] += b
    return (y * 0.45).astype(np.float32)


def sparkle():
    n = int(0.9 * SR); y = np.zeros(n, dtype=np.float32)
    for i, f in enumerate([1568, 1976, 2349, 3136]):
        p0 = int(i * 0.06 * SR)
        b = tone_bell(f, 0.7, 0.20)
        y[p0:p0 + len(b)] += b[:len(y) - p0]
    return y.astype(np.float32)


def success():
    n = int(0.7 * SR); t = np.arange(n, dtype=np.float32) / SR
    f = np.where(t < 0.20, 659.25, 987.77)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-2.4 * t) * 0.45).astype(np.float32)


def error():
    n = int(0.55 * SR); t = np.arange(n, dtype=np.float32) / SR
    y = (np.sin(2 * np.pi * 132 * t) + 0.6 * np.sin(2 * np.pi * 185 * t)) * np.exp(-5 * t)
    return (np.tanh(y * 2.2) * 0.30).astype(np.float32)


def riser():
    n = int(1.0 * SR); t = np.arange(n, dtype=np.float32) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    k = np.linspace(0.01, 0.24, n).astype(np.float32)
    out = np.empty_like(noise); acc = 0.0
    for i in range(n):
        acc += k[i] * (noise[i] - acc); out[i] = acc
    return (out * (t / 1.0) ** 2 * 1.0).astype(np.float32)


gens = {'pop': pop, 'click': click, 'marker': marker, 'hover': hover, 'tick': tick,
        'data': data, 'whoosh': whoosh, 'chime': chime, 'sparkle': sparkle, 'success': success,
        'error': error, 'riser': riser}
cache = {}
GAIN = {'click': 0.26, 'tick': 0.30, 'hover': 0.26, 'pop': 0.30, 'marker': 0.22,
        'data': 0.34, 'whoosh': 0.40, 'chime': 0.36, 'sparkle': 0.26, 'success': 0.40,
        'error': 0.30, 'riser': 0.34}
for ev in tl['sfx']:
    typ = ev['type']
    if typ not in gens:
        continue
    if typ not in cache:
        cache[typ] = gens[typ]()
    pan = float(np.clip(rng.normal(0, 0.35), -0.7, 0.7)) if typ in ('click', 'whoosh', 'marker') else 0.0
    add(cache[typ], ev['t'], pan, GAIN.get(typ, 0.3) * ev.get('gain', 1.0))
print(f"sfx built: {len(tl['sfx'])} events")

# ---------- mix ----------
mix = nar + music[:, None] + sfx
del music, sfx
peak = float(np.max(np.abs(mix)))
if peak > 0:
    mix *= min(1.0, 0.88 / peak)
mix = np.tanh(mix * 1.05) * 0.94
mix *= 32767
write_wav(f'{OUT}/mix.wav', mix)
print('mix written', f'{OUT}/mix.wav', f'{DUR/60:.2f} min')

subprocess.run([FF, '-y', '-v', 'error', '-i', f'{OUT}/mix.wav',
                '-c:a', 'aac', '-b:a', '192k', f'{OUT}/mix.m4a'], check=True)
print('mix.m4a written')
