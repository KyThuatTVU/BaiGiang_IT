# -*- coding: utf-8 -*-
"""Tạo các file sampler phát âm thuật ngữ trọng yếu cho Cổng B."""
import os, sys
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")
import tts_vieneu

SAMPLER_DIR = r"D:\Edit\Baigiang_OOP\mau\samplers"
os.makedirs(SAMPLER_DIR, exist_ok=True)

ITEMS = [
    ("oop_opt_a.wav", "Lập trình hướng đối tượng, hay còn gọi là Ô Ốp."),
    ("oop_opt_b.wav", "Lập trình hướng đối tượng, hay còn gọi là Ô-Ô-Pê."),
    ("oop_opt_c.wav", "Lập trình hướng đối tượng, hay còn gọi là Object-Oriented Programming."),
    ("term_java.wav", "Trong bài học hôm nay, chúng ta cùng tìm hiểu ngôn ngữ Java."),
    ("term_cpp_cs.wav", "Nó còn được ứng dụng trong nhiều ngôn ngữ như C plus plus, C thăng, Python."),
]

print("Bắt đầu sinh samplers thuật ngữ...")
for fname, text in ITEMS:
    out = os.path.join(SAMPLER_DIR, fname)
    tts_vieneu.synth(text, out)
    print(f"OK: {fname} -> {text}", flush=True)

print("Hoàn tất sinh samplers!")
