import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import FF, FULL
from render_full import video_frames, ORDER
from build_audio import dur

def probe(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    e = r.stderr
    v = re.search(r"Video: (\w+).*?, (\d{3,4})x(\d{3,4}).*?, (\d+(?:\.\d+)?) fps", e)
    a = re.search(r"Audio: (\w+)", e)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", e)
    h, mi, s = m[-1]
    return {"vcodec": v.group(1), "w": int(v.group(2)), "h": int(v.group(3)),
            "fps": float(v.group(4)), "acodec": a.group(1),
            "dur": int(h) * 3600 + int(mi) * 60 + float(s)}

def loud(path):
    r = subprocess.run([FF, "-i", path, "-af",
                        "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m[-1])

def parse_srt(path):
    blocks = open(path, encoding="utf-8").read().strip().split("\n\n")
    out = []
    for b in blocks:
        ln = b.split("\n")
        idx = int(ln[0])
        t0, t1 = ln[1].split(" --> ")
        def sec(t):
            h, m, s = t.replace(",", ".").split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
        out.append({"idx": idx, "start": sec(t0), "end": sec(t1), "lines": ln[2:]})
    return out

def main():
    rep = {}
    draft = FULL + "/draft.mp4"
    p = probe(draft)
    rep["specs"] = p
    rep["specs_ok"] = (p["w"], p["h"], p["fps"], p["vcodec"], p["acodec"]) == (1920, 1080, 30.0, "h264", "aac")
    L = loud(draft)
    rep["loudness"] = {k: L[k] for k in ("input_i", "input_tp", "input_lra")}
    rep["loudness_ok"] = abs(float(L["input_i"]) + 14) <= 0.5 and float(L["input_tp"]) <= -1.0
    ad = dur(FULL + "/audio_norm.m4a")
    rep["av_diff_s"] = round(p["dur"] - ad, 3)
    rep["av_ok"] = abs(p["dur"] - ad) <= 0.1

    gtl = json.load(open(FULL + "/global_timeline.json", encoding="utf-8"))
    manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    srt = parse_srt(FULL + "/full_video.srt")
    errs = []
    if len(srt) != len(manifest):
        errs.append(f"srt count {len(srt)} != manifest {len(manifest)}")
    prev_end = -1
    for c, s in zip(manifest, srt):
        g = gtl[c["id"]]
        if abs(s["start"] - g["start"]) > 0.01 or abs(s["end"] - (g["start"] + g["dur"])) > 0.01:
            errs.append(f"{c['id']} srt/time mismatch")
        if s["start"] < prev_end - 0.001:
            errs.append(f"{c['id']} overlap")
        prev_end = s["end"]
        if len(s["lines"]) > 2 or any(len(l) > 42 for l in s["lines"]):
            errs.append(f"{c['id']} subs >2x42")
        if s["lines"] != c["subs"]:
            errs.append(f"{c['id']} subs != manifest")
        for l in s["lines"]:
            if any(ch in l for ch in "[]…") or "(" in l:
                errs.append(f"{c['id']} label leak: {l}")
    rep["srt_errors"] = errs
    rep["srt_ok"] = not errs

    from render_core import load_timeline
    tl = load_timeline(False)
    Ns = video_frames(tl)
    bad = []
    for sid in ORDER:
        n = len([f for f in os.listdir(f"{FULL}/frames/{sid}") if f.startswith("f") and f.endswith(".jpg")])
        if n != Ns[sid]:
            bad.append(f"{sid}: {n} != {Ns[sid]}")
    rep["frame_errors"] = bad
    rep["frames_ok"] = not bad

    sizes = []
    for fn in ("render_core.py", "render_full.py"):
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fn), encoding="utf-8").read()
        sizes += [int(x) for x in re.findall(r"font\([^)]*?,\s*(\d+)\s*[,)]", src)]
    rep["min_font_px"] = min(sizes)
    rep["font_ok"] = min(sizes) >= 28

    rep["all_ok"] = all(rep[k] for k in ("specs_ok", "loudness_ok", "av_ok", "srt_ok", "frames_ok", "font_ok"))
    json.dump(rep, open(FULL + "/qa_report.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    print("QA_DONE", "ALL_OK" if rep["all_ok"] else "HAS_ERRORS")

if __name__ == "__main__":
    main()