# -*- coding: utf-8 -*-
"""Kiem tra cau hoan chinh: VI + EN ASR tren 2 bien the viet lai."""
import hashlib, os, subprocess, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF
from demo20 import dur

LAB = FULL + "/demo30/voice_lab/final"
os.makedirs(LAB, exist_ok=True)
VOICE = "vi-VN-NamMinhNeural"
RATE = "+12%"

S = {
    "D1": ["Đây là một vòng gọi ây pi ai.",
           "Clai-ần viết bằng ri ắc, gửi ri quét qua hát ti ti pi.",
           "Xơ vờ trên nốt giây xác thực tâu kần, truy vấn mai ét kiu eo, rồi trả ri spon giây sần."],
    "D2": ["Đây là một vòng gọi ây pi ai.",
           "Cờ-lai-ần viết bằng ri-ắc, gửi ri quét qua hát ti ti pi.",
           "Xơ vờ trên nốt-đi-ét xác thực tâu kần, truy vấn mai ét kiu eo, rồi trả ri spon giây sần."],
}


def edge(text, tag):
    key = hashlib.md5((VOICE + RATE + text).encode("utf-8")).hexdigest()[:10]
    p = f"{LAB}/_{tag}_{key}.mp3"
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


def join(parts):
    x = np.concatenate([np.zeros(4000, np.float32)] + parts + [np.zeros(6400, np.float32)])
    return x


def main():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    for name, segs in S.items():
        parts = []
        for i, t in enumerate(segs):
            parts.append(load(edge(t, f"{name}_{i}")))
            parts.append(np.zeros(4800, np.float32))
        audio = join(parts)
        for lang in ("vi", "en"):
            out, _ = m.transcribe(audio, language=lang, beam_size=2, vad_filter=False)
            txt = " ".join(s.text.strip() for s in out)
            print(f"== {name} [{lang}] {txt}", flush=True)


if __name__ == "__main__":
    main()
