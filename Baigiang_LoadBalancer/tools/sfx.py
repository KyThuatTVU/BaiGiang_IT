# -*- coding: utf-8 -*-
"""SFX + nhạc nền tự tổng hợp bằng numpy (không bản quyền). 24kHz mono."""
import math, os, wave
import numpy as np

SR = 24000
ROOT = "D:/Edit/Baigiang_LoadBalancer"
CACHE = ROOT + "/mau/sfx"
os.makedirs(CACHE, exist_ok=True)

def _env(n, a=0.005, d=None, shape="exp"):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / a)
    if shape == "exp":
        e *= np.exp(-t / (d if d else n / SR / 3))
    elif shape == "pad":
        e *= np.minimum(1.0, (n / SR - t) / 0.4)
    return e

def _noise(n, seed=7):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n)

def _band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip((f - lo) / 120, 0, 1) * np.clip((hi - f) / 120, 0, 1)
    return np.fft.irfft(X * m, len(x))

def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    f = 620 + 320 * np.exp(-t / 0.03)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.035)
    return x * 0.5

def click():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 2100 * t) * np.exp(-t / 0.006)
    x += _band(_noise(n, 3), 1500, 4000) * np.exp(-t / 0.004) * 0.6
    return x * 0.45

def whoosh():
    n = int(0.26 * SR)
    t = np.arange(n) / SR
    q = t / (n / SR)
    lo = _band(_noise(n, 11), 250, 800)
    mid = _band(_noise(n, 12), 800, 1800)
    hi = _band(_noise(n, 13), 1800, 3600)
    w = np.sin(np.pi * q)
    x = lo * (1 - q) * w + mid * w + hi * q * w
    e = np.sin(np.pi * q) ** 1.5
    return x * e * 0.55

def marker(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = _band(_noise(n, 21), 900, 2600)
    wob = 0.6 + 0.4 * np.sin(2 * np.pi * 13 * t) * np.sin(2 * np.pi * 3.1 * t)
    e = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.06)
    return x * wob * e * 0.30

def tick():
    n = int(0.045 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1050 * t) * np.exp(-t / 0.012)
    return x * 0.4

def chime(notes=(659.25, 880.0), dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for i, f in enumerate(notes):
        st = int(i * 0.07 * SR)
        m = n - st
        tt = np.arange(m) / SR
        x[st:] += (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2 * tt)) * \
                  np.exp(-tt / 0.16) * np.minimum(1, tt / 0.008) * 0.3
    return x

def success():
    return chime((523.25, 659.25, 783.99), 0.6)


def deny():
    n = int(0.34 * SR)
    t = np.arange(n) / SR
    f1, f2 = 420, 240
    f = np.where(t < 0.14, f1, f2)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    e = np.minimum(1, t / 0.008) * np.exp(-np.maximum(0, t - 0.14) / 0.09)
    return x * e * 0.32

def thud():
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    f = 150 - 60 * (t / (n / SR))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    x += _band(_noise(n, 31), 60, 300) * np.exp(-t / 0.03) * 0.4
    return x * 0.5

GEN = {"pop": pop, "click": click, "whoosh": whoosh, "tick": tick,
       "chime": chime, "success": success, "deny": deny, "thud": thud}

def sfx(name, dur=None):
    key = f"{name}_{dur:.2f}" if dur else name
    p = f"{CACHE}/{key}.npy"
    if os.path.exists(p):
        return np.load(p)
    x = marker(dur) if name == "marker" else GEN[name]()
    np.save(p, x)
    return x

def music_loop(bars=4, bpm=84):
    """Pad ấm + pluck arpeggio, vòng 4 hợp âm Am F C G. Mức thấp, không lời."""
    spb = 60 / bpm
    dur = bars * 4 * spb
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63],
              [130.81, 196.0, 261.63], [196.0, 246.94, 293.66]]
    bar_n = int(4 * spb * SR)
    for b in range(bars):
        ch = chords[b % 4]
        seg = slice(b * bar_n, (b + 1) * bar_n)
        tt = np.arange(bar_n) / SR
        e = np.minimum(1, tt / 0.5) * np.minimum(1, (4 * spb - tt) / 0.6)
        pad = np.zeros(bar_n)
        for f in ch:
            pad += np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2 * tt)
        x[seg] += pad * e * 0.045
        arp = [ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[1] * 2] * 2
        for i, f in enumerate(arp):
            st = int(i * spb / 2 * SR)
            m = min(bar_n - st, int(0.5 * SR))
            if m <= 0:
                continue
            tt2 = np.arange(m) / SR
            x[b * bar_n + st: b * bar_n + st + m] += \
                np.sin(2 * np.pi * f * tt2) * np.exp(-tt2 / 0.14) * 0.035
    return x

def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32767