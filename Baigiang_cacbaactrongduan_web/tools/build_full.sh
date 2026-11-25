#!/bin/bash
# Chuỗi dựng bản nháp Cổng C: render 17 cảnh -> mix audio -> ghép + loudnorm.
set -e
cd /d/Edit/Baigiang_cacbaactrongduan_web
echo "[build] start $(date +%H:%M:%S)"
python tools/render_full.py
echo "[build] render done $(date +%H:%M:%S)"
python tools/audio_full.py --tag full
echo "[build] audio done $(date +%H:%M:%S)"
python tools/assemble_full.py --tag full
echo "[build] draft done $(date +%H:%M:%S)"
