# -*- coding: utf-8 -*-
"""Encode 17 cảnh -> xfade -> loudnorm -> mux bản nháp full."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF, load_timeline
from scenes_web import ORDER, XFADE
from render_full import frames_for

MP4 = FULL + "/scene_mp4"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit("ffmpeg fail: " + " ".join(cmd[:6]))
    return r


def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return 0.0
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def loudnorm_json(path):
    r = subprocess.run([FF, "-i", path, "-af",
                        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        print(r.stderr[-1500:])
        raise SystemExit("loudnorm measure fail")
    return json.loads(m[-1])


def main():
    sub = sys.argv[sys.argv.index("--sub") + 1] if "--sub" in sys.argv else None
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else (sub or "full")
    sids = sys.argv[sys.argv.index("--scenes") + 1].split(",") if "--scenes" in sys.argv else ORDER
    force = set(sys.argv[sys.argv.index("--force") + 1].split(",")) if "--force" in sys.argv else set()
    fr = os.environ.get("FR_ROOT") or (FULL + ("/frames_" + sub if sub else "/frames"))
    tl = load_timeline(False, sids, sub=sub)
    ns = frames_for(tl, sids)
    outdir = f"{MP4}/{tag}"
    os.makedirs(outdir, exist_ok=True)
    for sid in sids:
        n = ns[sid]
        out = f"{outdir}/{sid}.mp4"
        if sid not in force and os.path.exists(out) and abs(dur(out) - n / 30) < 0.06:
            print(f"{sid} encode skip", flush=True)
            continue
        last = f"{fr}/{sid}/f{n-1:04d}.jpg"
        if not os.path.exists(last):
            raise SystemExit(f"missing frames {sid}: need {n}")
        run([FF, "-y", "-framerate", "30", "-start_number", "0",
             "-i", f"{fr}/{sid}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", out])
        print(f"{sid} encoded {n}", flush=True)
    cmd = [FF, "-y"]
    for sid in sids:
        cmd += ["-i", f"{outdir}/{sid}.mp4"]
    fc, prev, cum = "", "[0:v]", 0.0
    for k in range(1, len(sids)):
        cum += ns[sids[k - 1]] / 30
        off = cum - XFADE * k
        cur = "[vout]" if k == len(sids) - 1 else f"[x{k}]"
        fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XFADE}:offset={off:.4f}{cur};"
        prev = cur
    video = FULL + f"/{tag}_video.mp4"
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-c:v", "libx264",
            "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", video]
    run(cmd)
    print(f"VIDEO {tag} {dur(video):.2f}s", flush=True)
    wav = FULL + f"/{tag}_voice.wav"
    m = loudnorm_json(wav)
    print("LOUDNORM_IN", {k: m[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    anorm = FULL + f"/{tag}_audio.m4a"
    run([FF, "-y", "-i", wav, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", anorm])
    draft = FULL + f"/{tag}_draft.mp4"
    run([FF, "-y", "-i", video, "-i", anorm, "-c:v", "copy", "-c:a", "copy",
         "-movflags", "+faststart", "-shortest", draft])
    fin = loudnorm_json(draft)
    print("FINAL_LOUDNESS", {k: fin[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
    print(f"DRAFT_DONE {tag} {dur(draft):.2f}s", flush=True)


if __name__ == "__main__":
    main()
