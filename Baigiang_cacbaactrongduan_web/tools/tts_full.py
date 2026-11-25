# -*- coding: utf-8 -*-
"""TTS full 44 cue theo shard: python tts_full.py --i 0 --n 4
Biến thể CHỈ đổi dấu câu; miss thì giãn cách rồi thử tiếp; ghi tts_state.json."""
import json, msvcrt, os, re, subprocess, sys, time

ROOT = "D:/Edit/Baigiang_cacbaactrongduan_web"
FULL = ROOT + "/mau"
AUD = FULL + "/audio"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"
SHARDS = {
    "0": ["S01", "S02", "S03", "S04", "S05"],
    "1": ["S06", "S07", "S08", "S09"],
    "2": ["S10", "S11", "S12", "S13"],
    "3": ["S14", "S15", "S16", "S17"],
}

def dur(p):
    r = subprocess.run([FF, "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)

def try_text(text, rate, out):
    text = text.replace("…", ",")
    try:
        subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE, f"--rate={rate}",
                        "--text", text, "--write-media", out], capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None
    if os.path.exists(out) and os.path.getsize(out) > 1200:
        d = dur(out)
        if d and d > 0.4:
            return d
    if os.path.exists(out):
        os.remove(out)
    return None

def variants(t):
    out = [t]
    for v in (t.rstrip(".") + ".", t.replace(":", ","), t.replace(", ", " — "),
              t.rstrip("."), t + " ", t.replace("? ", ". ").rstrip("?") + "."):
        if v not in out:
            out.append(v)
    return out

def state_add(sp, cid, rec):
    with open(sp + ".lock", "a") as lk:
        msvcrt.locking(lk.fileno(), msvcrt.LK_LOCK, 1)
        try:
            st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
            st[cid] = rec
            json.dump(st, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        finally:
            msvcrt.locking(lk.fileno(), msvcrt.LK_UNLCK, 1)

def main():
    i = sys.argv[sys.argv.index("--i") + 1] if "--i" in sys.argv else "0"
    man = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    sp = FULL + "/tts_state.json"
    state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    mine = [c for c in man if c["scene"] in SHARDS[i]
            and (c["id"] not in state or not os.path.exists(f"{AUD}/{c['id']}.mp3"))]
    print(f"SHARD{i} START {len(mine)}/{len(SHARDS[i])} scenes", flush=True)
    for c in mine:
        out = f"{AUD}/{c['id']}.mp3"
        vs = variants(c["say"])
        ok = False
        for rnd in range(4):
            if rnd:
                time.sleep(25)
            d = try_text(vs[rnd % len(vs)], c["rate"], out)
            if d:
                state_add(sp, c["id"], {"dur": round(d, 3), "variant": rnd,
                                        "bytes": os.path.getsize(out)})
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} ok {d:.2f}s r{rnd}", flush=True)
                ok = True
                break
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} miss r{rnd}", flush=True)
        if not ok:
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} GIVEUP", flush=True)
    left = [c["id"] for c in man if c["id"] not in state or not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print(f"SHARD{i} DONE missing {left}", flush=True)

if __name__ == "__main__":
    main()
