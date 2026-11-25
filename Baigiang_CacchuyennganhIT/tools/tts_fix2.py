import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import FF, FULL
from build_audio import dur, concat_filter

AUD = FULL + "/audio"
state_path = FULL + "/tts_state.json"
state = json.load(open(state_path, encoding="utf-8"))
manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))

def tts(text, rate, out):
    try:
        subprocess.run(["python", "-m", "edge_tts", "--voice", "vi-VN-HoaiMyNeural",
                        f"--rate={rate}", "--text", text, "--write-media", out],
                       capture_output=True, timeout=90)
    except subprocess.TimeoutExpired:
        pass
    return os.path.exists(out) and os.path.getsize(out) > 0

def variants(t):
    base = t.rstrip(".,;:!?")
    return [t, base, base + ",", base + "!", base + ".",
            t[0].lower() + t[1:], base.replace(",", ";") + ",",
            base.replace("Ba Đê", "ba đê") + ","]

def split_fallback(c, out):
    t = c["text"]
    cut = t.rfind(",", 0, len(t) - 1)
    if cut < 10:
        cut = len(t) // 2
    a, b = t[:cut + 1], t[cut + 1:].strip()
    pa, pb = out + ".a.wav", out + ".b.wav"
    ma, mb = out + ".a.mp3", out + ".b.mp3"
    if not tts(a, c["rate"], ma) or not tts(b, c["rate"], mb):
        return False
    for src, dst in ((ma, pa), (mb, pb)):
        subprocess.run([FF, "-y", "-i", src, "-c:a", "pcm_s16le", "-ar", "24000", "-ac", "1", dst],
                       capture_output=True)
    concat_filter([pa, pb], out + ".wav")
    subprocess.run([FF, "-y", "-i", out + ".wav", "-c:a", "libmp3lame", "-q:a", "2", out],
                   capture_output=True)
    return os.path.getsize(out) > 0

for c in manifest:
    if c["id"] in state:
        continue
    out = f"{AUD}/{c['id']}.mp3"
    done = False
    for v in variants(c["text"]):
        if tts(v, c["rate"], out):
            state[c["id"]] = {"variant": v, "dur": dur(out)}
            print(f"FIX_OK {c['id']} variant={v!r} {state[c['id']]['dur']}s", flush=True)
            done = True
            break
        if os.path.exists(out):
            os.remove(out)
    if not done and split_fallback(c, out):
        state[c["id"]] = {"variant": "split:" + c["text"], "dur": dur(out)}
        print(f"FIX_OK {c['id']} split-fallback {state[c['id']]['dur']}s", flush=True)
        done = True
    if not done:
        print(f"fix fail {c['id']}", flush=True)
    json.dump(state, open(state_path, "w"), ensure_ascii=False)
print("FIX2_DONE", len(state), flush=True)