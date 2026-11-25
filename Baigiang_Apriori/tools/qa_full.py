# -*- coding: utf-8 -*-
"""Trích frame tại giữa mỗi cảnh, ghép contact sheet để QA bản đầy đủ."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import FF, FULL, load_timeline
from PIL import Image, ImageDraw

tag = sys.argv[1] if len(sys.argv) > 1 else "full"
tl = load_timeline(False)
gtl = json.load(open(f"{FULL}/{tag}_timeline.json", encoding="utf-8"))
video = f"{FULL}/{tag}_draft.mp4"
outdir = f"D:/Edit/Baigiang_Apriori/mau/qa/{tag}"
os.makedirs(outdir, exist_ok=True)

shots = []
for i, sid in enumerate(tl):
    cid = tl[sid]["cues"][0]["id"]
    t = gtl[cid]["start"] + tl[sid]["total"] * 0.45
    p = f"{outdir}/q{i:02d}_{sid}.png"
    subprocess.run([FF, "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", p],
                   capture_output=True)
    shots.append((sid, p))

COLS, TW, TH = 4, 480, 270
rows = (len(shots) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW, rows * TH), (240, 244, 248))
d = ImageDraw.Draw(sheet)
for k, (sid, p) in enumerate(shots):
    if not os.path.exists(p):
        continue
    im = Image.open(p).resize((TW, TH))
    x, y = (k % COLS) * TW, (k // COLS) * TH
    sheet.paste(im, (x, y))
    d.rectangle([x, y, x + 78, y + 26], fill=(15, 41, 77))
    d.text((x + 8, y + 6), sid, fill=(255, 255, 255))
sheet.save(f"D:/Edit/Baigiang_Apriori/mau/qa/{tag}_sheet.png")
print("QA_DONE", len(shots), f"D:/Edit/Baigiang_Apriori/mau/qa/{tag}_sheet.png")
