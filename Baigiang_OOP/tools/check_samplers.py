# -*- coding: utf-8 -*-
"""Kiểm tra ASR cho các file sampler bằng faster-whisper qua load_audio."""
import glob, os, subprocess
import numpy as np

FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
WHISPER = (r"C:\Users\ACER\.cache\huggingface\hub\models--Systran--faster-whisper-small"
           r"\snapshots\536b0662742c02347bc0e980a01041f333bce120")

def load_audio(path, sr=16000):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(sr), "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype="<f4").astype("float32")

from faster_whisper import WhisperModel
model = WhisperModel(WHISPER, device="cpu", compute_type="int8")

for f in sorted(glob.glob(r"D:\Edit\Baigiang_OOP\mau\samplers\*.wav")):
    x = load_audio(f)
    segs, _ = model.transcribe(x, language="vi")
    txt = " ".join(s.text.strip() for s in segs)
    print(f"{os.path.basename(f)}: \"{txt}\"", flush=True)
