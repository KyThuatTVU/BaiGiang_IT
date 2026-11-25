# -*- coding: utf-8 -*-
"""Trộn 87 cue voice + SFX theo timeline, chuẩn hóa 2 pass -> mix_norm.wav."""
import json, os, re, subprocess, sys, wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import full_common as C

RATE = 48000
SFX = C.PROJ + "/mau/sfx"
MIX = C.FULL + "/mix.wav"
NORM = C.FULL + "/mix_norm.wav"

EVENTS = {
    "S01": [("chime", 0.15), ("pop", 3.9)],
    "S02": [("whoosh", 0.25), ("buzz", 2.6)],
    "S03": [("pop", 0.2), ("click", 4.0)],
    "S04": [("whoosh", 0.2)],
    "S05": [("pop", 0.2), ("pen", 3.9)],
    "S06": [("pop", 0.2), ("whoosh", 3.9)],
    "S07": [("click", 1.0), ("pop", 4.1)],
    "S08": [("whoosh", 0.2)],
    "S09": [("pop", 0.25), ("click", 4.0)],
    "S10": [("chime", 3.9)],
    "S11": [("pop", 0.2), ("pop", 4.0), ("pop", 7.8), ("pop", 11.7), ("chime", 15.5)],
    "S12": [("whoosh", 0.2), ("buzz", 3.9)],
    "S13": [("pop", 0.25)],
    "S14": [("click", 3.9)],
    "S15": [("pop", 0.2), ("pop", 4.0), ("pop", 7.8), ("pop", 11.7), ("chime", 15.5)],
    "S16": [("chime", 0.25)],
    "S17": [("pop", 0.25)],
    "S18": [("buzz", 0.9), ("click", 4.2)],
    "S19": [("key", 3.0), ("click", 7.8), ("pop", 11.7), ("chime", 15.5)],
    "S20": [("pop", 0.25), ("whoosh", 3.9)],
    "S21": [("pop", 0.25), ("click", 4.0), ("chime", 7.8)],
    "S22": [("pop", 0.25), ("click", 4.0), ("key", 7.8), ("chime", 11.7)],
    "S23": [("pop", 0.25), ("key", 4.0), ("click", 7.8)],
    "S24": [("pop", 0.25), ("click", 4.0)],
    "S25": [("chime", 3.9)],
    "S26": [("key", 0.9), ("pop", 4.0), ("click", 7.8)],
    "S27": [("click", 0.6), ("pop", 4.0), ("chime", 7.8)],
    "S28": [("pop", 0.25), ("whoosh", 4.0), ("click", 7.8), ("chime", 11.7)],
    "S29": [("pop", 0.25), ("click", 4.0), ("whoosh", 7.8)],
    "S30": [("buzz", 0.9), ("pop", 4.0), ("click", 7.8), ("whoosh", 11.7)],
    "S31": [("pop", 0.25), ("click", 4.0), ("chime", 11.7)],
    "S32": [("pop", 0.25), ("buzz", 4.0), ("click", 7.8), ("whoosh", 11.7)],
    "S33": [("pop", 0.25), ("chime", 3.9)],
    "S34": [("chime", 0.35), ("whoosh", 7.8)],
}


def decode_mp3(path):
    r = subprocess.run([C.FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(RATE), "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("decode fail " + path + "\n" + r.stderr.decode("utf-8", "ignore")[-800:])
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getframerate() == RATE, path
        assert w.getnchannels() == 1, path
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    return x


def write_wav(path, x):
    y = np.clip(x, -1.0, 1.0)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes((y * 32767.0).astype(np.int16).tobytes())


def dur(path):
    r = subprocess.run([C.FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return 0.0
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def main():
    total = C.TOTAL
    n = int(round(total * RATE)) + RATE
    voice = np.zeros(n)
    last = 0
    for sid in C.SIDS:
        s = C.SC[sid]
        for c, st, du in zip(s["cues"], s["starts"], s["durs"]):
            x = decode_mp3(f"{C.AUD}/{c['id']}.mp3")
            i = int(round((C.GSTART[sid] + st) * RATE))
            voice[i:i + len(x)] += x
            last = max(last, i + len(x))
    sfx = np.zeros(n)
    for sid, evs in EVENTS.items():
        prev = -9.0
        for name, local in evs:
            assert local - prev >= 1.5 - 1e-6, (sid, name, local, prev)
            prev = local
            x = read_wav(f"{SFX}/{name}.wav")
            i = int(round((C.GSTART[sid] + local) * RATE))
            j = min(n, i + len(x))
            sfx[i:j] += x[:j - i]
    mix = voice + sfx
    peak = float(np.max(np.abs(mix)))
    lim = 10 ** (-1.5 / 20)
    scaled = peak > lim
    if scaled:
        mix *= lim / peak
    write_wav(MIX, mix)
    print(f"MIX total={total:.2f}s voice_end={last / RATE:.2f}s peak={peak:.3f} scaled={scaled}", flush=True)

    r = subprocess.run([C.FF, "-hide_banner", "-i", MIX, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        print(r.stderr[-1500:]); raise SystemExit("loudnorm measure fail")
    print("LOUDNORM_IN", {k: json.loads(m[-1])[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh")}, flush=True)
    r = subprocess.run([C.FF, "-y", "-v", "error", "-i", MIX, "-af",
                        "loudnorm=I=-14:TP=-1.2:LRA=11",
                        "-ar", str(RATE), "-c:a", "pcm_s16le", NORM], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); raise SystemExit("normalize fail")
    r = subprocess.run([C.FF, "-hide_banner", "-i", NORM, "-af",
                        "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if m:
        j = json.loads(m[-1])
        print("LOUDNORM_OUT", {k: j[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
    print(f"AUDIO_DONE norm={dur(NORM):.2f}s target={total:.2f}s", flush=True)


if __name__ == "__main__":
    main()
