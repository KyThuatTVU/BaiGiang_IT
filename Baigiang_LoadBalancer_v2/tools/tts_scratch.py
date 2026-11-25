# -*- coding: utf-8 -*-
"""Voice tạm Edge NamMinh cho sample — KHÔNG phải giọng Nam Bộ, chỉ để duyệt nhịp."""
import json, msvcrt, os, subprocess, sys, time

ROOT = "D:/Edit/Baigiang_LoadBalancer_v2"
FULL = ROOT + "/mau"
AUD = FULL + "/audio_sample"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"


def dur(p):
    r = subprocess.run([FF, "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    m = __import__("re").findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def raw_tts(text, rate, out):
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
              t.rstrip("."), t + " ", t.replace("? ", ". ").rstrip("?") + "."):
        if v not in out:
            out.append(v)
    return out


def state_add(sp, cid, rec):
    with open(sp + ".lock", "a") as lk:
        msvcrt.locking(lk.fileno(), msvcrt.LK_LOCK, 1)
        try:
            st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
            st[cid] = rec
            json.dump(st, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        finally:
            msvcrt.locking(lk.fileno(), msvcrt.LK_UNLCK, 1)


def main():
    st_name = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "sample"
    if st_name == "full":
        man_p, aud_dir, state_p = (FULL + "/manifest.json", FULL + "/audio",
                                  FULL + "/tts_state.json")
    else:
        man_p, aud_dir, state_p = (FULL + "/manifest_sample.json", FULL + "/audio_sample",
                                   FULL + "/tts_state_sample.json")
    os.makedirs(aud_dir, exist_ok=True)
    man = json.load(open(man_p, encoding="utf-8"))
    sp = state_p
    todo = [c for c in man if not os.path.exists(f"{aud_dir}/{c['id']}.mp3")]
    print(f"SCRATCH START {len(todo)}/{len(man)}", flush=True)
    for c in todo:
        final = f"{aud_dir}/{c['id']}.mp3"
        tmp = f"{aud_dir}/_raw_{c['id']}.mp3"
        vs = variants(c["say"])
        for rnd in range(5):
            if rnd:
                time.sleep(12)
            if not raw_tts(vs[rnd % len(vs)], c["rate"], tmp):
                print(c["id"], "miss r" + str(rnd), flush=True)
                continue
            os.replace(tmp, final)
            d = dur(final)
            if d and d > 0.4:
                state_add(sp, c["id"], {"dur": round(d, 3), "variant": rnd,
                                        "voice": "edge:vi-VN-NamMinhNeural",
                                        "scratch": True, "shift": 0.0})
                print(c["id"], f"ok {d:.2f}s r{rnd}", flush=True)
                break
    left = [c["id"] for c in man if not os.path.exists(f"{aud_dir}/{c['id']}.mp3")]
    print("SCRATCH DONE missing", left, flush=True)


if __name__ == "__main__":
    main()
