# -*- coding: utf-8 -*-
"""Lab phat am: so sanh cach doc thuat ngu tieng Anh bang giong Viet."""
import hashlib, os, subprocess, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF
from demo20 import decode, dur
import sfx

SR = sfx.SR
LAB = FULL + "/demo30/voice_lab"
RAW = LAB + "/raw"
TERMS = LAB + "/terms"
for d in (LAB, RAW, TERMS):
    os.makedirs(d, exist_ok=True)

VOICE = "vi-VN-NamMinhNeural"
RATE = "+12%"


def edge(text, tag):
    key = hashlib.md5((VOICE + RATE + text).encode("utf-8")).hexdigest()[:10]
    p = f"{RAW}/{tag}_{key}.mp3"
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
            print(f"  ok {tag:12s} {text[:44]}", flush=True)
            time.sleep(0.7)
            return p
        print(f"  miss {tag} r{rnd}", flush=True)
    raise SystemExit("TTS giveup " + tag)


def sil(t):
    return np.zeros(int(t * SR))


def write_mp3(name, parts, path=None):
    x = np.concatenate([sil(0.25)] + [decode(p) if isinstance(p, str) else p for p in parts] + [sil(0.35)])
    peak = np.abs(x).max()
    if peak > 0:
        x = x / peak * 0.82
    wav = f"{LAB}/{name}.wav"
    sfx.write_wav(wav, x)
    mp3 = path or f"{LAB}/{name}.mp3"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", wav, "-b:a", "96k", mp3], check=True)
    print(f"{name}.mp3  {len(x)/SR:.2f}s", flush=True)
    return mp3


# ---------- cau so sanh ----------
A = [
    "Đây là một vòng gọi ây pi ai.",
    "Cờ lai ần viết bằng ri ắc, gửi ri quét qua hát ti ti pi.",
    "Sờ vờ trên nốt giây xác thực tâu kần, truy vấn mai ét kiu eo, rồi trả ri spon giây sần.",
]
B = [
    "Đây là một vòng gọi ây pi ai.",
    "Cờ lai ần viết bằng ri ắc, gửi ri quét qua hát tê tê pê.",
    "Sờ vờ trên nốt giây xác thực tâu kần, truy vấn mai xì quồ, rồi trả ri spon giây sần.",
]
C_PLAIN = ("Đây là một vòng gọi API. Client viết bằng React, gửi request qua HTTP. "
           "Server trên Node.js xác thực token, truy vấn MySQL, rồi trả response JSON.")

def build_sentences():
    for name, segs in (("SENTENCE_A", A), ("SENTENCE_B", B)):
        parts = []
        for i, t in enumerate(segs):
            parts.append(edge(t, f"{name}_{i}"))
            if i < len(segs) - 1:
                parts.append(sil(0.30))
        write_mp3(name, parts)
    # C: gTTS
    try:
        from gtts import gTTS
        p = f"{LAB}/SENTENCE_C_google.mp3"
        gTTS(C_PLAIN, lang="vi").save(p)
        print("SENTENCE_C_google.mp3", os.path.getsize(p), flush=True)
    except Exception as e:
        print("gTTS fail", repr(e), flush=True)


# ---------- tung tu khoa ----------
NUM = {0: "một.", 1: "hai.", 2: "ba.", 3: "bốn."}

VARIANTS = {
    "api":      ["ây pi ai", "a pi ai", "API"],
    "mysql":    ["mai ét kiu eo", "mai xì quồ", "mai ét quy eo", "MySQL"],
    "http":     ["hát ti ti pi", "hát tê tê pê"],
    "nodejs":   ["nốt giây", "nốt chấm giây", "nốt đi ét"],
    "react":    ["ri ắc", "ri ác"],
    "json":     ["giây sần", "giây sơn"],
    "client":   ["cờ lai ần", "cờ-lai-ần"],
    "server":   ["sờ vờ", "sơ vơ"],
    "request":  ["ri quét", "ri-quét"],
    "response": ["ri spon", "ri-spon"],
    "token":    ["tâu kần", "tốc kần"],
    "sql":      ["ét kiu eo", "xì quồ"],
    "endpoint": ["en đờ poi", "en-poi"],
    "get":      ["gét"],
}

def build_terms():
    for term, vs in VARIANTS.items():
        parts = []
        for i, v in enumerate(vs):
            if len(vs) > 1:
                parts.append(edge(NUM[i], f"num{i}"))
                parts.append(sil(0.22))
            parts.append(edge(v, f"{term}{i}"))
            if i < len(vs) - 1:
                parts.append(sil(0.55))
        write_mp3(term, parts, f"{TERMS}/{term}.mp3")


if __name__ == "__main__":
    build_sentences()
    build_terms()
    print("DONE", LAB)
