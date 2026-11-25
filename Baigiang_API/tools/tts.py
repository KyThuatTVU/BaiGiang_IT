# -*- coding: utf-8 -*-
"""Cầu nối — chạy code thật ở D:/Edit/Kit/tools/tts.py."""
import os, runpy

_p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "Kit", "tools", "tts.py")
runpy.run_path(_p, run_name="__main__")
