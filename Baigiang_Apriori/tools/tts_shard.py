# -*- coding: utf-8 -*-
"""Sinh TTS song song: mỗi tiến trình nhận một shard cue, ghi state riêng."""
import json, os, re, subprocess, sys, time

ROOT = "D:/Edit/Baigiang_Apriori"
FULL = ROOT + "/mau/full"
AUD = FULL + "/audio"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"
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
    k = int(sys.argv[sys.argv.index("--shard") + 1])
    n = int(sys.argv[sys.argv.index("--of") + 1])
    manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    sp = FULL + "/tts_state.json"
    state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    todo = [c for c in manifest if c["id"] not in state or not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    mine = [c for i, c in enumerate(todo) if i % n == k]
    outp = FULL + f"/tts_state_s{k}.json"
    own = json.load(open(outp, encoding="utf-8")) if os.path.exists(outp) else {}
    print(f"SHARD {k}/{n}: {len(mine)} cues", flush=True)
    for c in mine:
        out = f"{AUD}/{c['id']}.mp3"
        ok = False
        for rnd, text in enumerate(variants(c.get("say") or c["text"])):
            try:
                subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE,
                                f"--rate={c.get('rate', '+18%')}", "--text", text,
                                "--write-media", out],
                               capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                pass
            if os.path.exists(out) and os.path.getsize(out) > 1200:
                d = dur(out)
                if d and d > 0.4:
                    own[c["id"]] = {"dur": round(d, 3), "variant": rnd, "bytes": os.path.getsize(out)}
                    json.dump(own, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                    print(f"[{time.strftime('%H:%M:%S')}] s{k} {c['id']} ok {d:.2f}s v{rnd}", flush=True)
                    ok = True
                    break
            if os.path.exists(out):
                os.remove(out)
            time.sleep(1.5)
        if not ok:
            print(f"[{time.strftime('%H:%M:%S')}] s{k} {c['id']} FAIL", flush=True)
    print(f"SHARD_DONE {k} {len(own)}", flush=True)


if __name__ == "__main__":
    main()
