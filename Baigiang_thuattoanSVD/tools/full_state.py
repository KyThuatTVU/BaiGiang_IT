# -*- coding: utf-8 -*-
"""Trạng thái chia sẻ giữa demo_full và các module cảnh."""
ST = {}
TALK = []
S0 = {}   # scene -> thời điểm bắt đầu khung (trước cue đầu 0.75 s)
S1 = {}   # scene -> thời điểm kết thúc khung


def is_talk(t):
    for a, b in TALK:
        if a <= t <= b:
            return True
    return False
