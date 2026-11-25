# -*- coding: utf-8 -*-
"""Mix audio full: voice theo timeline video (khớp xfade) + SFX (không nhạc nền); xuất SRT."""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF, load_timeline
from scenes_api import ORDER, EVENTS
import sfx

AUD = FULL + "/audio"
SR = sfx.SR


def decode(path):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("decode fail " + path)
    return np.frombuffer(r.stdout, dtype="<f4").astype(np.float64)


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    sub = sys.argv[sys.argv.index("--sub") + 1] if "--sub" in sys.argv else None
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else (sub or "full")
    sids = sys.argv[sys.argv.index("--scenes") + 1].split(",") if "--scenes" in sys.argv else ORDER
    tl = load_timeline(False, sids, sub=sub)
    totals = [tl[s]["total"] for s in sids]
    # clip cảnh không-cuối đã chừa XFADE giây đệm nên cảnh k vẫn bắt đầu ở cum
    offs = [sum(totals[:k]) for k in range(len(sids))]
    video_total = sum(totals)
    n = int(video_total * SR) + SR
    mix = np.zeros(n)
    srt, idx, gtl = [], 0, {}
    for k, sid in enumerate(sids):
        s = tl[sid]
        t = 0.0
        for j, c in enumerate(s["cues"]):
            if j > 0:
                t += s["gap"] + s["cues"][j - 1].get("pause_after", 0.0)
            if sub:
                src = f"{FULL}/audio_sample/{c['id']}.wav"
            else:
                wav = f"{AUD}/{c['id']}.wav"
                src = wav if os.path.exists(wav) else f"{AUD}/{c['id']}.mp3"
            x = decode(src)
            st = int((offs[k] + t) * SR)
            mix[st:st + len(x)] += x
            g = offs[k] + t
            gtl[c["id"]] = {"scene": sid, "start": round(g, 3), "dur": round(s["durs"][j], 3)}
            idx += 1
            srt.append(f"{idx}\n{srt_time(g)} --> {srt_time(g + s['durs'][j])}\n" +
                       "\n".join(c["subs"]) + "\n")
            t += s["durs"][j]
        for (et, name, du, gain) in EVENTS[sid](tl):
            x = sfx.sfx(name, du) * gain
            st = int((offs[k] + et) * SR)
            mix[st:st + len(x)] += x
    peak = np.max(np.abs(mix))
    print("MIX_PEAK", round(peak, 3), flush=True)
    if peak > 0.98:
        mix *= 0.98 / peak
    sfx.write_wav(FULL + f"/{tag}_voice.wav", mix)
    open(FULL + f"/{tag}.srt", "w", encoding="utf-8").write("\n".join(srt))
    json.dump(gtl, open(FULL + f"/{tag}_timeline.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"AUDIO_DONE {tag} {video_total:.2f}s cues={idx}", flush=True)


if __name__ == "__main__":
    main()
