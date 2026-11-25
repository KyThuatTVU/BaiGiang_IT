import json, os, re, subprocess, time

ROOT = "D:/Edit/Baigiang_CacchuyennganhIT"
AUD = ROOT + "/mau/full/audio"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
os.makedirs(AUD, exist_ok=True)
manifest = json.load(open(ROOT + "/mau/full/manifest.json"))
state_path = ROOT + "/mau/full/tts_state.json"
state = json.load(open(state_path)) if os.path.exists(state_path) else {}
fails = {}

def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    h, mi, s = m[-1]
    return round(int(h) * 3600 + int(mi) * 60 + float(s), 2)

def variants(c):
    v0 = c["text"]
    v1 = re.sub(r"[.,;:!?]+$", "", v0).strip()
    return [v0, v1]

while True:
    pending = [c for c in manifest if c["id"] not in state and fails.get(c["id"], 0) < 8]
    stuck = [c["id"] for c in manifest if c["id"] not in state and fails.get(c["id"], 0) >= 8]
    if not pending:
        break
    successes = 0
    for c in pending:
        vs = variants(c)
        v = vs[fails.get(c["id"], 0) % len(vs)]
        p = f"{AUD}/{c['id']}.mp3"
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", "vi-VN-HoaiMyNeural", f"--rate={c['rate']}", "--text", v, "--write-media", p], capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            pass
        if os.path.exists(p) and os.path.getsize(p) > 0:
            state[c["id"]] = {"variant": v, "dur": dur(p)}
            json.dump(state, open(state_path, "w"), ensure_ascii=False)
            successes += 1
            print(f"[{time.strftime('%H:%M:%S')}] OK {c['id']} {state[c['id']]['dur']}s ({len(state)}/153)", flush=True)
        else:
            fails[c["id"]] = fails.get(c["id"], 0) + 1
            if os.path.exists(p):
                os.remove(p)
            print(f"[{time.strftime('%H:%M:%S')}] FAIL {c['id']} try{fails[c['id']]}", flush=True)
    if stuck:
        print("STUCK:", stuck, flush=True)
    if successes == 0:
        time.sleep(120)
print("PREFLIGHT_DONE", len(state), "stuck:", [c["id"] for c in manifest if c["id"] not in state], flush=True)