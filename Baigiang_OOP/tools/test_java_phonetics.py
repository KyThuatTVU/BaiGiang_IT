# -*- coding: utf-8 -*-
import os, sys
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")
import tts_vieneu, subprocess
import numpy as np
from faster_whisper import WhisperModel

FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
WHISPER = (r"C:\Users\ACER\.cache\huggingface\hub\models--Systran--faster-whisper-small"
           r"\snapshots\536b0662742c02347bc0e980a01041f333bce120")

def load_audio(path, sr=16000):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(sr), "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype="<f4").astype("float32")

model = WhisperModel(WHISPER, device="cpu", compute_type="int8")

variants = [
    ("java_v1_dava.wav", "Ngôn ngữ lập trình Da-va."),
    ("java_v2_giava.wav", "Ngôn ngữ lập trình Gia-va."),
    ("java_v3_dzava.wav", "Ngôn ngữ lập trình Dza-va."),
    ("java_v4_raw.wav", "Ngôn ngữ lập trình Java."),
]

OUT = r"D:\Edit\Baigiang_OOP\mau\samplers\java_tests"
os.makedirs(OUT, exist_ok=True)

for fname, text in variants:
    p = os.path.join(OUT, fname)
    tts_vieneu.synth(text, p)
    x = load_audio(p)
    segs, _ = model.transcribe(x, language="vi")
    txt = " ".join(s.text.strip() for s in segs)
    print(f"{fname} (input='{text}') -> ASR: '{txt}'", flush=True)
