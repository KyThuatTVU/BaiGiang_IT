# -*- coding: utf-8 -*-
"""Render bản đầy đủ 34 cảnh. --preview để QA khung hình, --only S01,S02 để shard."""
import os, subprocess, sys, time
os.environ.setdefault("FULL_DRY", "1" if "--preview" in sys.argv else "0")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import full_common as C
import scenes_a as A
import scenes_b as B
from PIL import ImageDraw

OUT = C.FULL
PREV = OUT + "/preview"
os.makedirs(C.SVID, exist_ok=True)
os.makedirs(PREV, exist_ok=True)

R = {**A.RENDERERS, **B.RENDERERS}
SETUP = {}
for sid in C.SIDS:
    fn = getattr(A, "setup_" + sid.lower(), None) or getattr(B, "setup_" + sid.lower(), None)
    if fn is None:
        raise SystemExit("missing setup " + sid)
    SETUP[sid] = fn
missing = [s for s in C.SIDS if s not in R]
if missing:
    raise SystemExit("missing renderer " + str(missing))

def picked():
    args = sys.argv[1:]
    if "--only" in args:
        ids = args[args.index("--only") + 1].split(",")
        return [s for s in C.SIDS if s in ids]
    if "--from" in args:
        a = int(args[args.index("--from") + 1])
        b = int(args[args.index("--to") + 1]) if "--to" in args else 34
        return [f"S{i:02d}" for i in range(a, b + 1)]
    return list(C.SIDS)

def frame(sid, t):
    im = R[sid](t)
    ch = C.sub_at(C.GSTART[sid] + t)
    if ch:
        C.sub_band(ImageDraw.Draw(im), ch)
    return im

def preview():
    for sid in picked():
        setup = SETUP[sid]
        setup()
        s = C.SC[sid]
        ts = [1.0]
        for i, st in enumerate(s["starts"][1:4], 1):
            ts.append(st + 0.9)
        ts.append(max(1.2, s["dur"] - 1.0))
        for k, t in enumerate(sorted(set(round(x, 2) for x in ts if x < s["dur"]))):
            t0 = time.time()
            im = frame(sid, t)
            im.convert("RGB").save(f"{PREV}/{sid}_{k}_t{t:05.1f}.png")
            print(f"{sid} t={t:5.1f} {time.time() - t0:.2f}s", flush=True)
    print("PREVIEW_DONE", flush=True)

def encode(sid):
    SETUP[sid]()
    dur = C.SC[sid]["dur"]
    N = int(round(dur * C.FPS))
    out = f"{C.SVID}/{sid}.mp4"
    cmd = [C.FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{C.W}x{C.H}",
           "-r", str(C.FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
           "-crf", "18", "-pix_fmt", "yuv420p", "-an", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    t0 = time.time()
    for f in range(N):
        p.stdin.write(frame(sid, f / C.FPS).convert("RGB").tobytes())
        if f % 150 == 0:
            print(f"{sid} {f}/{N} {time.time() - t0:.0f}s", flush=True)
    p.stdin.close()
    p.wait()
    print(f"{sid} frames={N} dur={dur:.2f}s rc={p.returncode} {time.time() - t0:.0f}s", flush=True)
    return p.returncode

if __name__ == "__main__":
    if "--preview" in sys.argv:
        preview()
    else:
        C.write_srt(OUT + "/full.srt")
        print("TOTAL", round(C.TOTAL, 2), "s", flush=True)
        for sid in picked():
            if encode(sid) != 0:
                raise SystemExit("ffmpeg failed " + sid)
        print("SCENES_DONE", flush=True)
