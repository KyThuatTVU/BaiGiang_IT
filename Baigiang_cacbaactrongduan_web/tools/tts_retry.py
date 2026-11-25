# -*- coding: utf-8 -*-
"""Thử lại các cue còn thiếu (1 tiến trình, giãn cách, xoay biến thể dấu câu).
python tts_retry.py [--passes 3] [--gap 30]"""
import json, os, sys, time
sys.path.insert(0, "D:/Edit/Baigiang_cacbaactrongduan_web/tools")
from tts_full import FULL, AUD, variants, try_text, state_add

PASSES = int(sys.argv[sys.argv.index("--passes") + 1]) if "--passes" in sys.argv else 3
GAP = float(sys.argv[sys.argv.index("--gap") + 1]) if "--gap" in sys.argv else 30.0

man = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
sp = FULL + "/tts_state.json"

def missing():
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    return [c for c in man if c["id"] not in st or not os.path.exists(f"{AUD}/{c['id']}.mp3")]

for p in range(PASSES):
    miss = missing()
    print(f"RETRY pass {p + 1}/{PASSES} missing={len(miss)}", flush=True)
    if not miss:
        break
    for k, c in enumerate(miss):
        vs = variants(c["say"])
        out = f"{AUD}/{c['id']}.mp3"
        d = try_text(vs[(p + k) % len(vs)], c["rate"], out)
        if d:
            state_add(sp, c["id"], {"dur": round(d, 3), "variant": (p + k) % len(vs),
                                    "bytes": os.path.getsize(out)})
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} ok {d:.2f}s p{p + 1}", flush=True)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} miss p{p + 1}", flush=True)
        time.sleep(GAP)

miss = [c["id"] for c in missing()]
print("RETRY_DONE missing", len(miss), miss, flush=True)
