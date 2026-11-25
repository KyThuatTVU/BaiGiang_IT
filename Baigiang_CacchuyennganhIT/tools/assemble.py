import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import FF, FULL
from render_full import video_frames, ORDER, XFADE
from build_audio import dur

FR = FULL + "/frames"
MP4 = FULL + "/scene_mp4"
os.makedirs(MP4, exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:]); raise SystemExit("ffmpeg fail: " + " ".join(cmd[:6]))
    return r

def loudnorm_json(path):
    r = subprocess.run([FF, "-i", path, "-af",
                        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        print(r.stderr[-1500:]); raise SystemExit("loudnorm measure fail")
    return json.loads(m[-1])

def main():
    from render_core import load_timeline
    tl = load_timeline(False)
    Ns = video_frames(tl)

    for sid in ORDER:
        n = Ns[sid]
        out = f"{MP4}/{sid}.mp4"
        if os.path.exists(out) and abs(dur(out) - n / 30) < 0.05:
            print(f"{sid} encode skip ({n} frames)", flush=True); continue
        if not os.path.exists(f"{FR}/{sid}/f{n-1:04d}.jpg"):
            raise SystemExit(f"missing frames {sid}: need {n}")
        run([FF, "-y", "-framerate", "30", "-start_number", "0",
             "-i", f"{FR}/{sid}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", out])
        print(f"{sid} encoded {n} frames", flush=True)

    cmd = [FF, "-y"]
    for sid in ORDER:
        cmd += ["-i", f"{MP4}/{sid}.mp4"]
    fc = ""; prev = "[0:v]"; cum = 0.0
    for k in range(1, len(ORDER)):
        cum += Ns[ORDER[k - 1]] / 30
        off = cum - XFADE * k
        cur = "[vout]" if k == len(ORDER) - 1 else f"[x{k}]"
        fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XFADE}:offset={off:.4f}{cur};"
        prev = cur
    cmd += ["-filter_complex", fc, "-map", "[vout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", "30", "-an", FULL + "/video_only.mp4"]
    run(cmd)
    vd = dur(FULL + "/video_only.mp4")
    print(f"VIDEO_ONLY {vd:.2f}s", flush=True)

    wav = FULL + "/full_voice.wav"
    m = loudnorm_json(wav)
    print("LOUDNORM_IN", {k: m[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh")}, flush=True)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run([FF, "-y", "-i", wav, "-af", af, "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k", FULL + "/audio_norm.m4a"])
    run([FF, "-y", "-i", FULL + "/video_only.mp4", "-i", FULL + "/audio_norm.m4a",
         "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", FULL + "/draft.mp4"])
    dd = dur(FULL + "/draft.mp4")
    fin = loudnorm_json(FULL + "/draft.mp4")
    print("FINAL_LOUDNESS", {k: fin[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
    print(f"DRAFT_DONE {dd:.2f}s video={vd:.2f}s audio={dur(FULL+'/audio_norm.m4a'):.2f}s", flush=True)

if __name__ == "__main__":
    main()