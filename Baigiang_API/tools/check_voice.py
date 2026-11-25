# -*- coding: utf-8 -*-
"""Nghe lai file long tieng bang Whisper (vi/en) de kiem tra ten tieng Anh."""
import os, re, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FF, FULL

SRC = sys.argv[1] if len(sys.argv) > 1 else FULL + "/demo30/voice30.wav"

TERMS = {
    "API":      r"\bapi\b|ây pi|a pi|ey pi",
    "client":   r"client|clai|cờ lai|clang|clan",
    "server":   r"server|xơ vờ|sờ vờ",
    "React":    r"react|ri ắc|ri-ắc",
    "request":  r"request|ri quét",
    "HTTP":     r"https?\b|hát ti",
    "Node.js":  r"node|nốt giây|nút dây|nốt-đi-ét",
    "token":    r"token|tâu kần|tâu cần",
    "MySQL":    r"mysql|mai sql|mai ét|mai xì",
    "response": r"response|respawn|ri spon",
    "JSON":     r"json|giây sần|giấy sân|dây sân|jason",
}


def load(p):
    r = subprocess.run([FF, "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype="<f4")


def main():
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    audio = load(SRC)
    for lang in ("vi", "en"):
        segs, _ = m.transcribe(audio, language=lang, beam_size=2, vad_filter=False)
        txt = " ".join(s.text.strip() for s in segs)
        print(f"[{lang}] {txt}\n", flush=True)
        low = txt.lower()
        for k, pat in TERMS.items():
            print(f"  {'OK ' if re.search(pat, low) else '-- '}{k}", end="")
        print()
    print("SRC", SRC)


if __name__ == "__main__":
    main()
