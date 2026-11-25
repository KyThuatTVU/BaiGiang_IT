# -*- coding: utf-8 -*-
"""TTS cho video mẫu Cổng B (S01, S02, S06). Chạy lại an toàn theo state."""
import json, os, re, subprocess, sys, time

ROOT = "D:/Edit/Baigiang_dongbodulieu"
OUT = ROOT + "/mau"
AUD = OUT + "/audio"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"
RATE = "+18%"
SAMPLE = {"S01", "S02", "S06"}
os.makedirs(AUD, exist_ok=True)

def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)

def variants(text):
    yield text
    yield text if text.endswith(".") else text + "."
    yield text.replace(", ", " — ")
    yield text + " "

def main():
    manifest = json.load(open(ROOT + "/manifest.json", encoding="utf-8"))
    cues = [c for c in manifest if c["scene"] in SAMPLE]
    sp = OUT + "/tts_state.json"
    state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    todo = [c for c in cues if c["id"] not in state or not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print(f"SAMPLE_TTS start: {len(cues)} cues, {len(todo)} cần tạo", flush=True)
    for c in todo:
        out = f"{AUD}/{c['id']}.mp3"
        ok = False
        for rnd, text in enumerate(variants(c.get("say") or c["text"])):
            try:
                r = subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE,
                                    f"--rate={c.get('rate', RATE)}", "--text", text,
                                    "--write-media", out],
                                   capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                r = None
            if os.path.exists(out) and os.path.getsize(out) > 1200:
                d = dur(out)
                if d and d > 0.4:
                    state[c["id"]] = {"dur": round(d, 3), "variant": rnd, "bytes": os.path.getsize(out)}
                    json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    print(f"[{time.strftime('%H:%M:%S')}] {c['id']} ok {d:.2f}s v{rnd}", flush=True)
                    ok = True
                    break
            if os.path.exists(out):
                os.remove(out)
            time.sleep(2.5)
        if not ok:
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} FAIL", flush=True)
    miss = [c["id"] for c in cues if c["id"] not in state]
    print("SAMPLE_TTS_DONE total", len(state), "missing", len(miss), miss, flush=True)

if __name__ == "__main__":
    main()
