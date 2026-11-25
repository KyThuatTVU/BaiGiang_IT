# -*- coding: utf-8 -*-
"""Tổng hợp SFX bằng numpy -> WAV 48 kHz (04_ArtDirection §9)."""
import os, wave
import numpy as np

SR = 48000
OUT = "D:/Edit/Baigiang_dongbodulieu/mau/sfx"
os.makedirs(OUT, exist_ok=True)

def wav(path, x, peak_db):
    x = x.astype(np.float64)
    x = x / max(1e-9, np.max(np.abs(x))) * (10 ** (peak_db / 20))
    n = int(0.008 * SR)
    if len(x) > 2 * n:
        x[:n] *= np.linspace(0, 1, n)
        x[-n:] *= np.linspace(1, 0, n)
    pcm = np.clip(x * 32767, -32768, 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

def t_axis(dur):
    return np.arange(int(dur * SR)) / SR

def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

rng = np.random.default_rng(7)

def pen():
    t = t_axis(0.18)
    x = band(rng.normal(0, 1, len(t)), 1200, 3500)
    env = np.minimum(t / 0.012, 1) * np.exp(-(t - 0.012).clip(0) / 0.05)
    return x * env

def pop():
    t = t_axis(0.12)
    f = 660 - 220 * (t / 0.12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.045)

def click():
    t = t_axis(0.06)
    x = rng.normal(0, 1, len(t)) * np.exp(-t / 0.003)
    x += 0.6 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.005)
    return x

def chime():
    t = t_axis(0.5)
    x = (1.0 * np.sin(2 * np.pi * 523.25 * t) +
         0.7 * np.sin(2 * np.pi * 659.25 * t) +
         0.5 * np.sin(2 * np.pi * 783.99 * t))
    return x * np.minimum(t / 0.006, 1) * np.exp(-t / 0.16)

def whoosh():
    t = t_axis(0.35)
    n = rng.normal(0, 1, len(t))
    n = band(n, 400, 4200)
    env = np.sin(np.pi * np.clip(t / 0.35, 0, 1)) ** 1.6
    sweep = 0.18 * np.sin(2 * np.pi * np.cumsum(180 + 540 * (t / 0.35)) / SR)
    return (n * 0.8 + sweep) * env

def buzz():
    t = t_axis(0.18)
    x = np.zeros_like(t)
    for k in range(1, 13):
        x += np.sin(2 * np.pi * 140 * k * t) / k
    x *= 1 + 0.18 * np.sin(2 * np.pi * 28 * t)
    return x * np.minimum(t / 0.005, 1) * np.exp(-t / 0.09)

def key():
    t = t_axis(0.04)
    x = rng.normal(0, 1, len(t)) * np.exp(-t / 0.002)
    x += 0.5 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.004)
    return x

if __name__ == "__main__":
    table = [("pen", pen, -26), ("pop", pop, -26), ("click", click, -24),
             ("chime", chime, -28), ("whoosh", whoosh, -28), ("buzz", buzz, -30),
             ("key", key, -30)]
    for name, fn, db in table:
        wav(f"{OUT}/{name}.wav", fn(), db)
        print("sfx", name, db, "dBFS", flush=True)
    print("SFX_DONE", flush=True)
