# -*- coding: utf-8 -*-
"""TTS 24 cue: edge-tts NamMinh + pitch-shift hậu kỳ theo 'shift' (semitone).
Biến thể chỉ đổi dấu câu khi dịch vụ trả rỗng; không sửa nội dung."""
import json, msvcrt, os, re, subprocess, sys, time

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
FULL = ROOT + "/mau"
AUD = FULL + "/audio"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
VOICE = "vi-VN-NamMinhNeural"


def dur(p):
    r = subprocess.run([FF, "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
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


def shift_file(src, dst, semi):
    if abs(semi) < 0.01:
        os.replace(src, dst)
        return True
    f = 2 ** (semi / 12)
    af = f"asetrate=24000*{f:.6f},aresample=24000,atempo={1/f:.6f}"
    r = subprocess.run([FF, "-y", "-i", src, "-af", af, "-c:a", "libmp3lame",
                        "-q:a", "4", dst], capture_output=True, text=True)
    if r.returncode != 0:
        return False
    os.remove(src)
    return os.path.getsize(dst) > 1200


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
    os.makedirs(AUD, exist_ok=True)
    man = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    sp = FULL + "/tts_state.json"
    state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    ids = sys.argv[sys.argv.index("--ids") + 1].split(",") if "--ids" in sys.argv else None
    no_shift = "--no-shift" in sys.argv
    todo = [c for c in man if (ids is None or c["id"] in ids)
            and not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print(f"TTS START {len(todo)}/{len(man)}", flush=True)
    for c in todo:
        final = f"{AUD}/{c['id']}.mp3"
        tmp = f"{AUD}/_raw_{c['id']}.mp3"
        vs = variants(c["say"])
        ok = False
        for rnd in range(5):
            if rnd:
                time.sleep(20)
            if not raw_tts(vs[rnd % len(vs)], c["rate"], tmp):
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} miss r{rnd}", flush=True)
                continue
            if not shift_file(tmp, final, 0.0 if no_shift else c.get("shift", 0.0)):
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} shift fail", flush=True)
                continue
            d = dur(final)
            if d and d > 0.4:
                state_add(sp, c["id"], {"dur": round(d, 3), "variant": rnd,
                                        "bytes": os.path.getsize(final),
                                        "voice": "edge:vi-VN-NamMinhNeural",
                                        "rate": c["rate"],
                                        "shift": 0.0 if no_shift else c.get("shift", 0.0)})
                print(f"[{time.strftime('%H:%M:%S')}] {c['id']} ok {d:.2f}s r{rnd}",
                      flush=True)
                ok = True
                break
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} bad dur r{rnd}", flush=True)
        if not ok:
            print(f"[{time.strftime('%H:%M:%S')}] {c['id']} GIVEUP", flush=True)
    left = [c["id"] for c in man if not os.path.exists(f"{AUD}/{c['id']}.mp3")]
    print(f"TTS DONE missing {left}", flush=True)


if __name__ == "__main__":
    main()
