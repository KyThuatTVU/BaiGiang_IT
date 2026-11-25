# -*- coding: utf-8 -*-
"""TTS manifest -> audio. Dùng: python tts.py [--sub sample] [--only S01c1,S01c2]"""
import json, msvcrt, os, re, subprocess, sys, time

PROJECT = os.environ.get("PROJECT_ROOT", "D:/Edit/Baigiang_API")
FULL = PROJECT + "/mau"
FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
VOICE = "vi-VN-NamMinhNeural"

SUB = sys.argv[sys.argv.index("--sub") + 1] if "--sub" in sys.argv else None
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
AUD = FULL + ("/audio_sample" if SUB else "/audio")
MAN = FULL + ("/manifest_sample.json" if SUB else "/manifest.json")
STATE = FULL + ("/tts_state_sample.json" if SUB else "/tts_state.json")


def dur(p):
    r = subprocess.run([FF, "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def raw_tts(text, rate, out):
    if os.path.exists(out):
        os.remove(out)
    try:
        subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE, f"--rate={rate}",
                        "--text", text, "--write-media", out],
                       capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False
    return os.path.exists(out) and os.path.getsize(out) > 1200


def variants(t):
    out = [t]
    for v in (t.rstrip(".") + ".", t.replace(":", ","), t.replace(", ", " — "),
              t.rstrip("."), t + " "):
        if v not in out:
            out.append(v)
    return out


def state_add(cid, rec):
    with open(STATE + ".lock", "a") as lk:
        msvcrt.locking(lk.fileno(), msvcrt.LK_LOCK, 1)
        try:
            st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
            st[cid] = rec
            json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        finally:
            msvcrt.locking(lk.fileno(), msvcrt.LK_UNLCK, 1)


def main():
    os.makedirs(AUD, exist_ok=True)
    man = json.load(open(MAN, encoding="utf-8"))
    if ONLY:
        man = [c for c in man if c["id"] in ONLY]
    todo = [c for c in man if not os.path.exists(f"{AUD}/{c['id']}.mp3")
            or os.path.getsize(f"{AUD}/{c['id']}.mp3") < 1200]
    print(f"TTS START {len(todo)}/{len(man)} sub={SUB or 'full'}", flush=True)
    for c in todo:
        final = f"{AUD}/{c['id']}.mp3"
        for rnd in range(6):
            if rnd:
                time.sleep(12)
            tmp = f"{AUD}/_raw_{c['id']}.mp3"
            vs = variants(c["say"])
            if not raw_tts(vs[rnd % len(vs)], c["rate"], tmp):
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} miss r{rnd}", flush=True)
                continue
            d = dur(tmp)
            if d and d > 0.4:
                os.replace(tmp, final)
                state_add(c["id"], {"dur": round(d, 3), "variant": rnd,
                                    "bytes": os.path.getsize(final)})
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} ok {d:.2f}s r{rnd}", flush=True)
                break
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} bad dur r{rnd}", flush=True)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} GIVEUP", flush=True)
    left = [c["id"] for c in man if not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print(f"TTS DONE missing {left}", flush=True)


if __name__ == "__main__":
    main()
