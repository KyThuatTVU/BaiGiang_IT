# -*- coding: utf-8 -*-
"""Ghép 12 cảnh bằng xfade theo cây (tối đa 3 input/lần) để tránh OOM."""
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF
from scenes_web import ORDER, XFADE

MP4 = FULL + "/scene_mp4/full"
TMP = FULL + "/scene_mp4/tree"


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return 0.0
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def merge(paths, out):
    if len(paths) == 1:
        shutil.copy(paths[0], out)
        return
    cmd = [FF, "-y"]
    for p in paths:
        cmd += ["-i", p]
    fc, prev, cum = "", "[0:v]", dur(paths[0])
    for k in range(1, len(paths)):
        lab = "[v]" if k == len(paths) - 1 else f"[x{k}]"
        fc += (f"{prev}[{k}:v]xfade=transition=fade:duration={XFADE}:"
               f"offset={cum - XFADE:.4f}{lab};")
        prev = lab
        cum += dur(paths[k]) - XFADE
    cmd += ["-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264",
            "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p",
            "-r", "30", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        raise SystemExit("xfade fail " + out)


def main():
    os.makedirs(TMP, exist_ok=True)
    level = [f"{MP4}/{s}.mp4" for s in ORDER]
    gen = 0
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 3):
            grp = level[i:i + 3]
            out = f"{TMP}/g{gen}_{i // 3}.mp4"
            merge(grp, out)
            print(f"MERGE g{gen}_{i//3} <{len(grp)}> {dur(out):.2f}s", flush=True)
            nxt.append(out)
        level = nxt
        gen += 1
    final = FULL + "/full_video.mp4"
    shutil.move(level[0], final)
    print(f"XFADE_TREE_DONE {dur(final):.2f}s", flush=True)


if __name__ == "__main__":
    main()
