# -*- coding: utf-8 -*-
"""Tổng hợp audio toàn bộ 61 cues cho bài OOP bằng VieNeu TTS."""
import json, os, sys, time

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")

import tts_vieneu, sfx

SCRIPT_PATH = os.path.join(PROJECT, "tools", "script.json")
with open(SCRIPT_PATH, encoding="utf-8") as f:
    data = json.load(f)

AUD_DIR = os.path.join(PROJECT, "mau", "full", "audio")
os.makedirs(AUD_DIR, exist_ok=True)

cues = [c for sc in data["scenes"] for c in sc["cues"]]
print(f"Tổng số cues cần xử lý: {len(cues)}")

t0 = time.time()
for i, c in enumerate(cues):
    cid = c["id"]
    text = c["say"]
    out_p = os.path.join(AUD_DIR, f"{cid}.wav")
    
    if os.path.exists(out_p) and os.path.getsize(out_p) > 10000:
        continue
        
    t_start = time.time()
    tts_vieneu.synth(text, out_p)
    d = sfx.dur(out_p) if hasattr(sfx, 'dur') else 0
    print(f"[{i+1:2d}/{len(cues)}] {cid}: {d:.2f}s ({time.time()-t_start:.2f}s) -> {text[:45]}...", flush=True)

print(f"Hoàn thành toàn bộ {len(cues)} audio cues trong {time.time()-t0:.1f}s!")
