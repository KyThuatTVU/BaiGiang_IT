# -*- coding: utf-8 -*-
"""Dán huy hiệu logo An Tech lên video đã render; giữ nguyên file gốc.

Dùng:
  python stamp_logo.py input.mp4
  python stamp_logo.py input.mp4 --out out.mp4 --pos br --size 120 --alpha 0.9
"""
import argparse, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FF, BRAND_LOGO


def main():
    ap = argparse.ArgumentParser(description="Stamp logo An Tech lên video")
    ap.add_argument("video")
    ap.add_argument("--out", help="mặc định <input>_logo.mp4")
    ap.add_argument("--pos", default="tr", choices=["tr", "tl", "br", "bl"])
    ap.add_argument("--size", type=int, default=110)
    ap.add_argument("--margin", type=int, default=28)
    ap.add_argument("--dx", type=int, default=0, help="dịch ngang thêm")
    ap.add_argument("--dy", type=int, default=0, help="dịch dọc thêm")
    ap.add_argument("--alpha", type=float, default=0.85)
    a = ap.parse_args()

    if not os.path.exists(a.video):
        raise SystemExit("Không thấy video: " + a.video)
    out = a.out or os.path.splitext(a.video)[0] + "_logo.mp4"
    if os.path.abspath(out) == os.path.abspath(a.video):
        raise SystemExit("Output trùng input — chọn tên khác.")

    mx = a.margin + a.dx
    my = a.margin + a.dy
    x = f"W-w-{mx}" if a.pos in ("tr", "br") else str(mx)
    y = f"H-h-{my}" if a.pos in ("br", "bl") else str(my)
    fc = (f"[1:v]scale={a.size}:-1,format=rgba,colorchannelmixer=aa={a.alpha}[lg];"
          f"[0:v][lg]overlay={x}:{y}")
    cmd = [FF, "-y", "-i", a.video, "-i", BRAND_LOGO,
           "-filter_complex", fc, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("stamp fail")
    print("STAMPED", out)


if __name__ == "__main__":
    main()
