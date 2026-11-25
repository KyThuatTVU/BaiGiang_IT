# -*- coding: utf-8 -*-
"""TTS Viettel AI - giọng nam Nam bộ thật (mặc định hcm-minhquan).

Hai chế độ:
  beats (mặc định): chia câu thành nhịp, đổi tốc độ từng nhịp, chèn nghỉ.
  flat: đọc cả câu một lượt (dùng để A/B).

Không chỉnh pitch. Chỉ highpass + compressor + limiter nhẹ trước khi mix.
Token đọc từ VIETTEL_TTS_TOKEN hoặc file mau/.viettel_token.
"""
import json, os, re, subprocess, sys, tempfile, time, wave
import urllib.error, urllib.request

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
FULL = ROOT + "/mau"
AUD = FULL + "/audio"
STATE = FULL + "/tts_state.json"
MAN = FULL + "/manifest.json"
DIRECTED = FULL + "/directed.json"
URL = os.environ.get("VIETTEL_TTS_URL", "https://viettelai.vn/tts/speech_synthesis")
VOICE = os.environ.get("VIETTEL_VOICE", "hcm-minhquan")
FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
CHAIN = ("highpass=f=70,acompressor=threshold=-18dB:ratio=2:attack=10:release=150,"
         "alimiter=limit=0.95:level=false")
KEY_TERMS = ("lossy", "lossless", "jpeg", "png", "webp", "avif", "sharp", "lazy",
             "srcset", "cdn", "quality", "resize", "lót-xi", "lót-lít", "giây-pê-gờ",
             "guép-pê", "ây-víp", "pê-en-gờ", "sáp", "lây-zi", "xê-đi-en")


def token():
    t = os.environ.get("VIETTEL_TTS_TOKEN", "").strip()
    for name in (".viettel_token", ".viettel_token.txt"):
        if not t and os.path.exists(FULL + "/" + name):
            t = open(FULL + "/" + name, encoding="utf-8-sig").read().strip()
    return t


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p, "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def variants(t):
    out = [t]
    for v in (t.rstrip(".") + ".", t.replace(":", ","), t.rstrip("."), t + " "):
        if v not in out:
            out.append(v)
    return out


def split_long(p, max_len):
    if len(p) <= max_len:
        return [p]
    mid = len(p) / 2
    def hits(pat):
        return [m.start() for m in re.finditer(r"\s(?=(?:" + pat + r")\s)", p, re.I)
                if 30 <= m.start() <= len(p) - 30]
    cands = hits("bằng cách|nhờ|để|khi|nếu|vì|nhưng") or hits("hoặc|và")
    if not cands:
        cands = [i for i, ch in enumerate(p) if ch == " " and 30 <= i <= len(p) - 30]
    if not cands:
        return [p]
    c = min(cands, key=lambda x: abs(x - mid))
    return split_long(p[:c].strip(), max_len) + split_long(p[c:].strip(), max_len)


def split_beats(text, max_len=90):
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?…])\s+|(?<=—)\s*", text)
    raw = []
    for p in parts:
        p = p.strip(" ")
        if not p:
            continue
        if len(p) > max_len:
            subs = re.split(r"(?<=[,;:])\s+", p)
            for s in subs:
                s = s.strip()
                if s:
                    raw.extend(split_long(s, max_len))
        else:
            raw.append(p)
    beats = []
    for b in raw:
        strong = b.endswith("!") or b.endswith("?") or b.endswith("…") or b.rstrip().endswith("—")
        if beats and len(b) < 6 and not strong:
            beats[-1] = beats[-1] + " " + b
        else:
            beats.append(b)
    return beats


def beat_speed(b, base):
    s = base
    if b.endswith("!") or b.endswith("?"):
        s += 0.06
    if "…" in b:
        s -= 0.03
    if len(b) < 25:
        s += 0.03
    low = b.lower()
    if any(k in low for k in KEY_TERMS):
        s -= 0.04
    return round(min(1.30, max(1.15, s)), 2)


def beat_pause(b):
    if b.endswith("!") or b.endswith("?"):
        return 0.30
    if b.endswith("…"):
        return 0.32
    if b.rstrip().endswith("—"):
        return 0.24
    if b.endswith("."):
        return 0.26
    return 0.20


def synth(tok, text, speed, out):
    body = json.dumps({"speed": speed, "voice": VOICE, "text": text,
                       "tts_return_option": 3, "without_filter": False},
                      ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "Origin": "https://viettelai.vn",
               "Referer": "https://viettelai.vn/chuyen-giong-noi",
               "User-Agent": "Mozilla/5.0",
               "Authorization": "Bearer " + tok, "Token": tok}
    delay = 20
    for _ in range(6):
        try:
            req = urllib.request.Request(URL, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
                ct = r.headers.get("Content-Type", "")
            if ct.startswith("audio") and len(data) > 5000:
                open(out, "wb").write(data)
                return True, "ok"
            return False, "bad_response " + ct + " " + str(len(data))
        except urllib.error.HTTPError as e:
            msg = e.read()[:200].decode("utf-8", "ignore")
            if e.code in (401, 403):
                return False, "auth_" + str(e.code) + " " + msg
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = int(ra) if ra and ra.isdigit() else delay
                time.sleep(min(wait, 120))
                delay = min(delay * 2, 120)
                continue
            time.sleep(delay)
            delay = min(delay * 2, 120)
        except Exception:
            time.sleep(delay)
            delay = min(delay * 2, 120)
    return False, "retry_exhausted"


def decode(p, w):
    r = subprocess.run([FF, "-y", "-i", p, "-ar", "48000", "-ac", "1",
                        "-c:a", "pcm_s16le", w], capture_output=True, text=True)
    return r.returncode == 0


def render_beats(tok, text, base, tmpdir, out):
    beats = split_beats(text)
    chunks, plan = [], []
    for i, b in enumerate(beats):
        sp = beat_speed(b, base)
        tmp = os.path.join(tmpdir, f"b{i}.mp3")
        ok, reason = synth(tok, b, sp, tmp)
        if not ok:
            return False, reason, plan, 0.0
        w = os.path.join(tmpdir, f"b{i}.wav")
        if not decode(tmp, w):
            return False, "decode_fail", plan, 0.0
        with wave.open(w, "rb") as r:
            chunks.append(r.readframes(r.getnframes()))
        pause = 0.0 if i == len(beats) - 1 else beat_pause(b)
        plan.append((sp, pause, b))
        if i < len(beats) - 1:
            chunks.append(b"\x00\x00" * int(48000 * pause))
    joined = os.path.join(tmpdir, "joined.wav")
    with wave.open(joined, "wb") as o:
        o.setnchannels(1)
        o.setsampwidth(2)
        o.setframerate(48000)
        o.writeframes(b"".join(chunks))
    r = subprocess.run([FF, "-y", "-i", joined, "-af", CHAIN, "-ar", "48000", "-ac", "1",
                        "-c:a", "libmp3lame", "-b:a", "160k", out],
                       capture_output=True, text=True)
    return r.returncode == 0, "ok", plan, dur(out) or 0.0


def main():
    dry = "--dry-run" in sys.argv
    tok = token()
    if not dry and not tok:
        print("NO_TOKEN - đặt VIETTEL_TTS_TOKEN hoặc ghi token vào mau/.viettel_token")
        return 2
    base = float(sys.argv[sys.argv.index("--speed") + 1]) if "--speed" in sys.argv else 1.2
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "beats"
    if mode not in ("beats", "flat"):
        print("mode phải là beats|flat")
        return 2
    force = "--force" in sys.argv
    out_dir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else AUD
    no_state = "--no-state" in sys.argv
    ids = sys.argv[sys.argv.index("--ids") + 1].split(",") if "--ids" in sys.argv else None
    man = json.load(open(MAN, encoding="utf-8"))
    directed = json.load(open(DIRECTED, encoding="utf-8")) if os.path.exists(DIRECTED) else {}
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    todo = [c for c in man if ids is None or c["id"] in ids]
    os.makedirs(out_dir, exist_ok=True)
    if dry:
        for c in todo:
            text = directed.get(c["id"], c["say"])
            beats = split_beats(text)
            print(f"{c['id']} base={base} beats={len(beats)}")
            for b in beats:
                print(f"  {beat_speed(b, base):.2f}  {beat_pause(b):.2f}  {b}")
        return 0
    print(f"VIETTEL START {len(todo)} cue voice={VOICE} mode={mode} base={base}", flush=True)
    done = 0
    for c in todo:
        cid = c["id"]
        final = f"{out_dir}/{cid}.mp3"
        prev = st.get(cid, {})
        want_mode = "flat" if mode == "flat" else "beats"
        if (not force and os.path.exists(final) and prev.get("voice") == "viettel:" + VOICE
                and prev.get("mode", "flat") == want_mode
                and abs(float(prev.get("speed", 0)) - base) < 1e-6):
            print(f"{cid} skip (done)", flush=True)
            done += 1
            continue
        text = directed.get(cid, c["say"])
        if mode == "flat":
            tmp = f"{out_dir}/_vt_{cid}.mp3"
            ok, reason = synth(tok, text, base, tmp)
            if ok:
                r = subprocess.run([FF, "-y", "-i", tmp, "-af", CHAIN, "-ar", "48000",
                                    "-ac", "1", "-c:a", "libmp3lame", "-b:a", "160k", final],
                                   capture_output=True, text=True)
                os.remove(tmp)
                ok = r.returncode == 0
                d = dur(final)
                plan = [(base, 0.0, text)]
            else:
                d = 0.0
                plan = []
        else:
            with tempfile.TemporaryDirectory() as td:
                ok, reason, plan, d = render_beats(tok, text, base, td, final)
        if not ok or not d or d < 0.4:
            print(f"{cid} FAIL {reason} dur={d}", flush=True)
            if reason.startswith("auth_"):
                print("TOKEN_INVALID - kiểm tra access token Viettel", flush=True)
                return 3
            continue
        if not no_state:
            st[cid] = {"dur": round(d, 3), "variant": 0, "bytes": os.path.getsize(final),
                       "voice": "viettel:" + VOICE, "speed": base, "mode": mode,
                       "beats": len(plan)}
            json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{cid} ok {d:.2f}s beats={len(plan)} -> {final}", flush=True)
        done += 1
        time.sleep(0.8)
    print(f"VIETTEL_DONE {done}/{len(todo)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
