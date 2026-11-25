# -*- coding: utf-8 -*-
"""Chuẩn hóa loudness có limiter rồi mux vào video đã ghép (không render lại)."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF
from assemble_full import run, dur, loudnorm_json

tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else "full"
video = FULL + f"/{tag}_video.mp4"
wav = FULL + f"/{tag}_voice.wav"
m = loudnorm_json(wav)
print("LOUDNORM_IN", {k: m[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:"
      f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
      f"volume=1.2dB,alimiter=limit=0.794:level=false")
anorm = FULL + f"/{tag}_audio.m4a"
run([FF, "-y", "-i", wav, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", anorm])
draft = FULL + f"/{tag}_draft.mp4"
run([FF, "-y", "-i", video, "-i", anorm, "-c:v", "copy", "-c:a", "copy",
     "-movflags", "+faststart", "-shortest", draft])
fin = loudnorm_json(draft)
print("FINAL_LOUDNESS", {k: fin[k] for k in ("input_i", "input_tp", "input_lra")}, flush=True)
print(f"DRAFT_DONE {tag} {dur(draft):.2f}s", flush=True)
