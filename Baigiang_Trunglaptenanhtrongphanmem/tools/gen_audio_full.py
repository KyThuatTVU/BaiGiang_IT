import os
import sys
import json
import time

sys.path.insert(0, r"D:\Edit\Kit\tools")
import tts_vieneu

SCRIPT_PATH = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem\tools\script.json"
OUT_DIR = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem\mau\full\audio"
os.makedirs(OUT_DIR, exist_ok=True)

with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

cues = []
for scene in data["scenes"]:
    for cue in scene["cues"]:
        cues.append(cue)

print(f"Tổng số cues cần xử lý: {len(cues)}")
t0 = time.time()

for i, c in enumerate(cues):
    cid = c["id"]
    say = c["say"]
    out_wav = os.path.join(OUT_DIR, f"{cid}.wav")
    
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 20000:
        print(f"[{i+1}/{len(cues)}] {cid} đã tồn tại ({os.path.getsize(out_wav)} bytes), bỏ qua.")
        continue
        
    print(f"[{i+1}/{len(cues)}] Đang tạo {cid}: {say[:40]}...")
    tts_vieneu.synth(say, out_wav)
    print(f"-> {out_wav} ({os.path.getsize(out_wav)} bytes)")

print(f"Hoàn tất toàn bộ {len(cues)} audio cues trong {time.time()-t0:.1f}s!")
