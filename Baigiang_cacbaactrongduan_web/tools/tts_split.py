# -*- coding: utf-8 -*-
"""Cứu các cue TTS lỗi dịch vụ: tách cue thành cụm ngắn, tổng hợp từng cụm rồi ghép.
python tts_split.py S05c3 S11c1 S15c2 S17c1
Giữ nguyên giọng/rate; chỉ miếng ghép thay đổi. Ghi tts_state.json như tts_full."""
import json, os, re, subprocess, sys, time
import numpy as np

ROOT = "D:/Edit/Baigiang_cacbaactrongduan_web"
FULL = ROOT + "/mau"
AUD = FULL + "/audio"
TMP = FULL + "/tts_split_tmp"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"
SR = 24000
JOIN = 0.18


def decode(path, sr=SR):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(sr), "-"], capture_output=True)
    if r.returncode != 0:
        return None
    return np.frombuffer(r.stdout, dtype="<f4")


def synth(text, rate, out, rounds=3, gap=8.0):
    vs = [text, text.rstrip(".") + ".", text.replace(", ", " — ")]
    for r in range(rounds):
        if r:
            time.sleep(gap)
        t = vs[r % len(vs)]
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE, f"--rate={rate}",
                            "--text", t, "--write-media", out],
                           capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if os.path.exists(out) and os.path.getsize(out) > 1200:
            x = decode(out)
            if x is not None and len(x) > 0.4 * SR:
                return x
        if os.path.exists(out):
            os.remove(out)
    return None


def halve(text):
    ws = text.split()
    if len(ws) < 4:
        return None
    m = len(ws) // 2
    return " ".join(ws[:m]).rstrip(",") + ",", " ".join(ws[m:])


def synth_any(text, rate, tag):
    x = synth(text, rate, f"{TMP}/{tag}.mp3")
    if x is not None:
        return x
    hs = halve(text)
    if not hs:
        return None
    print(f"  halve {tag} -> {len(hs[0])}+{len(hs[1])}", flush=True)
    a = synth(hs[0], rate, f"{TMP}/{tag}_a.mp3")
    b = synth(hs[1], rate, f"{TMP}/{tag}_b.mp3") if a is not None else None
    if a is None or b is None:
        return None
    return np.concatenate([a, np.zeros(int(0.12 * SR), dtype="<f4"), b])


def chunks(say, target=3):
    parts = [p.strip() for p in re.split(r"(?<=[;:.])\s+|(?<=,)\s+", say) if p.strip()]
    if len(parts) <= 1:
        return [say]
    n = max(1, min(target, len(say) // 55))
    size = len(say) / n
    out, cur = [], ""
    for p in parts:
        trial = (cur + " " + p).strip()
        if cur and len(cur) >= size * 0.9 and len(out) < n - 1:
            out.append(cur)
            cur = p
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


def main():
    ids = sys.argv[1:]
    man = {c["id"]: c for c in json.load(open(FULL + "/manifest.json", encoding="utf-8"))}
    sp = FULL + "/tts_state.json"
    os.makedirs(TMP, exist_ok=True)
    for cid in ids:
        c = man[cid]
        cs = chunks(c["say"])
        print(f"SPLIT {cid} n={len(cs)}", [len(x) for x in cs], flush=True)
        pcs, fail = [], False
        for i, ch in enumerate(cs):
            x = synth_any(ch, c["rate"], f"{cid}_{i}")
            if x is None:
                print(f"[{time.strftime('%H:%M:%S')}] {cid} part{i} FAIL", flush=True)
                fail = True
                break
            print(f"[{time.strftime('%H:%M:%S')}] {cid} part{i} ok {len(x)/SR:.2f}s", flush=True)
            pcs.append(x)
        if fail:
            continue
        sil = np.zeros(int(JOIN * SR), dtype="<f4")
        mix = np.concatenate([v for p in pcs for v in (p, sil)][:-1])
        raw = f"{TMP}/{cid}_full.f32"
        mix.tofile(raw)
        out = f"{AUD}/{cid}.mp3"
        r = subprocess.run([FF, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                            "-i", raw, "-c:a", "libmp3lame", "-b:a", "64k", "-ar", str(SR),
                            "-ac", "1", out], capture_output=True, text=True)
        if r.returncode != 0:
            print(cid, "ENCODE FAIL", r.stderr[-300:], flush=True)
            continue
        d = len(mix) / SR
        st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
        st[cid] = {"dur": round(d, 3), "variant": -1, "split": len(cs),
                   "bytes": os.path.getsize(out)}
        json.dump(st, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[{time.strftime('%H:%M:%S')}] {cid} DONE dur={d:.2f}s", flush=True)
    man2 = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    state = json.load(open(sp, encoding="utf-8"))
    left = [c["id"] for c in man2 if c["id"] not in state or not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print("SPLIT_DONE missing", left, flush=True)


if __name__ == "__main__":
    main()
