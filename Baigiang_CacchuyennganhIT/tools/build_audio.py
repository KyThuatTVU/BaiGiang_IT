import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import load_timeline, FF, FULL, ROOT

AUD = FULL + "/audio"
SCAUD = FULL + "/audio_scene"
SIL = FULL + "/sil"
os.makedirs(SCAUD, exist_ok=True)
os.makedirs(SIL, exist_ok=True)

def silence(sec):
    key = f"{sec:.3f}"
    p = f"{SIL}/sil_{key}.wav"
    if not os.path.exists(p):
        subprocess.run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", key, "-c:a", "pcm_s16le", p], capture_output=True)
    return p

def concat(paths, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    r = subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c", "copy", out], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); raise SystemExit("concat fail " + out)
    return out

def concat_filter(paths, out):
    cmd = [FF, "-y"]
    for p in paths:
        cmd += ["-i", p]
    fc = "".join(f"[{i}:a]aformat=sample_fmts=fltp:sample_rates=24000:channel_layouts=mono[a{i}];"
                 for i in range(len(paths)))
    fc += "".join(f"[a{i}]" for i in range(len(paths)))
    fc += f"concat=n={len(paths)}:v=0:a=1[aout]"
    cmd += ["-filter_complex", fc, "-map", "[aout]", "-c:a", "pcm_s16le", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); raise SystemExit("concat_filter fail " + out)
    return out

def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)

def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    state = json.load(open(FULL + "/tts_state.json", encoding="utf-8"))
    manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    missing = [c["id"] for c in manifest if c["id"] not in state]
    if missing:
        print("MISSING_DURATIONS", len(missing), missing[:20]); raise SystemExit(1)
    tl = load_timeline(False)
    order = [f"S{i:02d}" for i in range(1, 35)]
    # build per-scene audio
    scene_files = []
    for sid in order:
        s = tl[sid]; cues = s["cues"]
        parts = []
        for i, c in enumerate(cues):
            if i > 0:
                gap = s["gap"]
                prev = cues[i - 1]
                if c["id"] == "S30c3":
                    gap += 3.0
                else:
                    gap += prev["pause_after"] if prev["id"] != "S30c3" else 0.0
                parts.append(silence(gap))
            parts.append(f"{AUD}/{c['id']}.mp3")
        parts.append(silence(s["tail"]))
        out = f"{SCAUD}/{sid}.wav"
        tmp = out + ".tmp.wav"
        concat_filter(parts, tmp)
        # mp3 padding làm audio dài hơn timeline vài chục ms; cắt đúng phần đuôi im lặng
        r = subprocess.run([FF, "-y", "-i", tmp, "-t", f"{s['total']:.3f}",
                            "-c:a", "pcm_s16le", out], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-1500:]); raise SystemExit("trim fail " + sid)
        os.remove(tmp)
        scene_files.append(out)
        print(f"{sid} audio={dur(out):.2f}s timeline={s['total']:.2f}s", flush=True)
    full = concat(scene_files, FULL + "/full_voice.wav")
    total = dur(full)
    # global timeline + SRT
    gtl = {}; offset = 0.0; srt = []; idx = 0
    for sid in order:
        s = tl[sid]
        for j, c in enumerate(s["cues"]):
            g = offset + s["starts"][j]
            gtl[c["id"]] = {"scene": sid, "start": round(g, 3), "dur": round(s["durs"][j], 3)}
            idx += 1
            end = g + s["durs"][j]
            srt.append(f"{idx}\n{srt_time(g)} --> {srt_time(end)}\n" + "\n".join(c["subs"]) + "\n")
        offset += s["total"]
    json.dump(gtl, open(FULL + "/global_timeline.json", "w"), ensure_ascii=False, indent=1)
    open(FULL + "/full_video.srt", "w", encoding="utf-8").write("\n".join(srt))
    print(f"FULL_AUDIO {total:.2f}s  cues={idx}  video_total={offset:.2f}s")
    print("AUDIO_DONE")

if __name__ == "__main__":
    main()