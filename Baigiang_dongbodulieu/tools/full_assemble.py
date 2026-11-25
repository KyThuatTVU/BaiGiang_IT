# -*- coding: utf-8 -*-
"""Ghép 34 cảnh bằng xfade 0,30 s + mux mix_norm.wav -> mau/full/full.mp4."""
import os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import full_common as C

OUT = C.FULL + "/full.mp4"
MIXN = C.FULL + "/mix_norm.wav"


def dur(path):
    r = subprocess.run([C.FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise SystemExit("cannot read duration " + path)
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def main():
    sids = C.SIDS
    for sid in sids:
        p = f"{C.SVID}/{sid}.mp4"
        if not os.path.exists(p):
            raise SystemExit("missing scene " + p)
        d = dur(p)
        exp = C.SC[sid]["dur"]
        if abs(d - exp) > 0.12:
            raise SystemExit(f"{sid} duration {d:.2f} != timeline {exp:.2f}")
        print(f"{sid} {d:.2f}s", flush=True)

    cmd = [C.FF, "-y", "-v", "error"]
    for sid in sids:
        cmd += ["-i", f"{C.SVID}/{sid}.mp4"]
    cmd += ["-i", MIXN]
    fc = ""
    prev = "[0:v]"
    cum = 0.0
    for k in range(1, len(sids)):
        cum += dur(f"{C.SVID}/{sids[k - 1]}.mp4")
        off = cum - C.XF * k
        cur = "[vout]" if k == len(sids) - 1 else f"[x{k}]"
        fc += f"{prev}[{k}:v]xfade=transition=fade:duration={C.XF}:offset={off:.4f}{cur};"
        prev = cur
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", f"{len(sids)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", "30", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{C.TOTAL:.3f}", OUT]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2500:]); raise SystemExit("assemble fail")
    print(f"ASSEMBLE_DONE {dur(OUT):.2f}s target={C.TOTAL:.2f}s", flush=True)

    r = subprocess.run([C.FF, "-hide_banner", "-i", OUT, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if m:
        import json
        j = json.loads(m[-1])
        print("FINAL_LOUDNESS", {k: j[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)


if __name__ == "__main__":
    main()
