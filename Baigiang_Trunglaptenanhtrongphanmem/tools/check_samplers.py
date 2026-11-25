import os
import subprocess
import numpy as np

sampler_dir = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem\mau\sample\samplers"
ffmpeg = r"C:\Users\ACER\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")

def load_audio(path):
    cmd = [ffmpeg, "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(proc.stdout, np.int16).flatten().astype(np.float32) / 32768.0

print(f"{'FILE':20s} | {'TRANSCRIPTION'}")
print("-" * 75)
for f in sorted(os.listdir(sampler_dir)):
    if not f.endswith(".wav"): continue
    p = os.path.join(sampler_dir, f)
    audio = load_audio(p)
    segments, _ = model.transcribe(audio, language="vi", beam_size=3)
    text = " ".join([s.text.strip() for s in segments])
    print(f"{f:20s} | {text}")
