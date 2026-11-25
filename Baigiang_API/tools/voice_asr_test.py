# -*- coding: utf-8 -*-
"""Do phat am bang ASR: synthesize ung vien -> Whisper (vi) -> xem co nhan ra tu tieng Anh."""
import hashlib, os, subprocess, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF
from demo20 import dur

SR = 16000
LAB = FULL + "/demo30/voice_lab/asr"
os.makedirs(LAB, exist_ok=True)
VOICE = "vi-VN-NamMinhNeural"
RATE = "+12%"

CANDS = {
    "client":   ("Ứng dụng {v} gửi yêu cầu.", ["cờ-lai-ần", "clai-ần", "cờ lai-ần"]),
    "server":   ("Chạy trên {v}.", ["xơ vờ", "xơ-vờ", "sờ vờ"]),
    "react":    ("Viết bằng {v}.", ["ri-ắc", "ri ắc", "ri-ắc s"]),
    "nodejs":   ("API trên {v}.", ["nốt giây", "nốt-giây", "nốt chấm giây"]),
    "endpoint": ("Gọi {v}.", ["en đờ pôin", "en-poi", "en đờ pôi"]),
}


def edge(text, tag):
    key = hashlib.md5((VOICE + RATE + text).encode("utf-8")).hexdigest()[:10]
    p = f"{LAB}/{tag}_{key}.mp3"
    if os.path.exists(p) and os.path.getsize(p) > 1200 and (dur(p) or 0) > 0.2:
        return p
    for rnd in range(6):
        if rnd:
            time.sleep(8)
        tmp = p + ".part"
        if os.path.exists(tmp):
            os.remove(tmp)
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE, f"--rate={RATE}",
                            "--text", text, "--write-media", tmp],
                           capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if os.path.exists(tmp) and os.path.getsize(tmp) > 1200 and (dur(tmp) or 0) > 0.2:
            os.replace(tmp, p)
            return p
    raise SystemExit("TTS giveup " + tag)


def load(p):
    r = subprocess.run([FF, "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype="<f4")


def main():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    for term, spec in CANDS.items():
        carrier, vs = spec
        print("##", term, flush=True)
        for i, v in enumerate(vs):
            text = carrier.format(v=v)
            p = edge(text, f"{term}{i}")
            segs, _ = m.transcribe(load(p), language="vi", beam_size=2, vad_filter=False)
            heard = " ".join(s.text.strip() for s in segs)
            print(f"  [{i}] {v:16s} -> {heard}", flush=True)
            time.sleep(0.3)


if __name__ == "__main__":
    main()
