# -*- coding: utf-8 -*-
"""Hậu kỳ bản thu người: cắt im lặng, EQ/nén/limiter nhẹ, cân loudness từng cue.

Đầu vào : mau/voice_human/raw/{cid}.wav|.m4a|.mp3|...
Đầu ra  : mau/audio/{cid}.mp3 + cập nhật mau/tts_state.json
Kiểm tra: python tools/voice_human_prep.py --check
"""
import json, os, re, subprocess, sys, tempfile, wave
import numpy as np

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
FULL = ROOT + "/mau"
RAW = FULL + "/voice_human/raw"
AUD = FULL + "/audio"
STATE = FULL + "/tts_state.json"
REF = FULL + "/tts_state_namminh.json"
MAN = FULL + "/manifest.json"
REPORT = FULL + "/voice_human/prep_report.json"
FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
SR = 48000
EXTS = (".wav", ".m4a", ".mp3", ".flac", ".ogg", ".aac", ".wma")
TARGET_I = -18.0
CHAIN = ("highpass=f=70,acompressor=threshold=-18dB:ratio=2:attack=10:release=150")


def find_raw(cid, raw_dir):
    for ext in EXTS:
        p = f"{raw_dir}/{cid}{ext}"
        if os.path.exists(p):
            return p
    if os.path.isdir(raw_dir):
        for f in os.listdir(raw_dir):
            stem, ext = os.path.splitext(f)
            if stem.lower() == cid.lower() and ext.lower() in EXTS:
                return os.path.join(raw_dir, f)
    return None


def decode(path):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("decode fail: " + path)
    return np.frombuffer(r.stdout, dtype="<f4").astype(np.float64)


def trim(x, thresh_db=-45.0, pad=0.12):
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x, 0.0, 0.0
    env = np.max(np.abs(x[:n * win].reshape(n, win)), axis=1)
    idx = np.where(env > 10 ** (thresh_db / 20))[0]
    if len(idx) == 0:
        return np.zeros(0), len(x) / SR, 0.0
    a = max(0, int(idx[0] * win - pad * SR))
    b = min(len(x), int((idx[-1] + 1) * win + pad * SR))
    return x[a:b], a / SR, (len(x) - b) / SR


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def target(c, ref):
    if c["id"] in ref:
        return ref[c["id"]]["dur"]
    return max(0.8, len(c["say"]) / 17.5)


def measure_i(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path, "-af",
                        CHAIN + ",loudnorm=I=-18:TP=-1.5:LRA=7:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    ms = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not ms:
        return None
    try:
        return float(json.loads(ms[-1])["input_i"])
    except (ValueError, KeyError):
        return None


def main():
    check = "--check" in sys.argv
    force = "--force" in sys.argv
    raw_dir = (sys.argv[sys.argv.index("--raw") + 1]
               if "--raw" in sys.argv else RAW)
    out_dir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else AUD
    no_state = "--no-state" in sys.argv
    ids = (sys.argv[sys.argv.index("--ids") + 1].split(",")
           if "--ids" in sys.argv else None)
    man = json.load(open(MAN, encoding="utf-8"))
    ref = json.load(open(REF, encoding="utf-8")) if os.path.exists(REF) else {}
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    todo = [c for c in man if ids is None or c["id"] in ids]
    missing, rows = [], []
    os.makedirs(out_dir, exist_ok=True)

    for c in todo:
        cid = c["id"]
        raw = find_raw(cid, raw_dir)
        if not raw:
            missing.append(cid)
            continue
        out = f"{out_dir}/{cid}.mp3"
        if check:
            d = dur(raw) or 0.0
            rows.append({"id": cid, "raw": raw, "dur_raw": round(d, 2),
                         "target": round(target(c, ref), 2)})
            print(f"{cid} OK raw={d:.2f}s target~{target(c, ref):.1f}s")
            continue
        if (not force and os.path.exists(out)
                and os.path.getmtime(out) >= os.path.getmtime(raw)):
            print(f"{cid} skip (up to date)", flush=True)
            continue
        x = decode(raw)
        peak_raw = float(np.max(np.abs(x))) if len(x) else 0.0
        x, lead, tail = trim(x)
        if len(x) < SR * 0.35:
            print(f"{cid} FAIL too_short_or_silent", flush=True)
            continue
        x = x - np.mean(x)
        f = int(0.008 * SR)
        if f * 2 < len(x):
            x[:f] *= np.linspace(0, 1, f)
            x[-f:] *= np.linspace(1, 0, f)
        with tempfile.TemporaryDirectory() as td:
            tmp = td + "/trim.wav"
            with wave.open(tmp, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(SR)
                w.writeframes(np.clip(x * 32767, -32768, 32767).astype("<i2").tobytes())
            li = measure_i(tmp)
            if li is None:
                print(f"{cid} FAIL loudness_measure", flush=True)
                continue
            gain = TARGET_I - li
            r = subprocess.run(
                [FF, "-y", "-v", "error", "-i", tmp, "-af",
                 CHAIN + f",volume={gain:.2f}dB,alimiter=limit=0.95:level=false",
                 "-ar", str(SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "160k", out],
                capture_output=True, text=True)
            if r.returncode != 0:
                print(f"{cid} FAIL encode {r.stderr[:120]}", flush=True)
                continue
        d = dur(out) or 0.0
        if d < 0.35:
            print(f"{cid} FAIL bad_dur {d:.2f}", flush=True)
            continue
        want = target(c, ref)
        ratio = d / want if want else 0
        warns = []
        if peak_raw >= 0.999:
            warns.append("clipping_raw")
        if ratio > 1.35:
            warns.append(f"slow_x{ratio:.2f}")
        elif ratio < 0.65:
            warns.append(f"fast_x{ratio:.2f}")
        if lead > 2.0 or tail > 2.0:
            warns.append(f"long_silence_{lead:.1f}/{tail:.1f}")
        if not no_state:
            st[cid] = {"dur": round(d, 3), "variant": 0, "bytes": os.path.getsize(out),
                       "voice": "human", "speed": 1.0, "mode": "human"}
            json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rows.append({"id": cid, "raw": raw, "dur": round(d, 2), "target": round(want, 2),
                     "gain_db": round(gain, 1), "peak_raw": round(peak_raw, 3),
                     "lead_s": round(lead, 2), "tail_s": round(tail, 2),
                     "warnings": warns})
        print(f"{cid} ok {d:.2f}s target~{want:.1f}s gain{gain:+.1f}dB "
              f"{' '.join(warns)}".rstrip(), flush=True)

    if not check and not no_state and out_dir == AUD:
        json.dump(rows, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"HUMAN_DONE {len(rows)}/{len(todo)} missing={len(missing)}")
    if missing:
        print("MISSING " + ",".join(missing))


if __name__ == "__main__":
    main()
