# -*- coding: utf-8 -*-
"""Cầu nối tương thích — code thật nằm ở D:/Edit/Kit/tools/sfx.py, sửa tại đó."""
import importlib.util as _u, os as _os, sys as _sys

_p = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__)))), "Kit", "tools", "sfx.py")
_s = _u.spec_from_file_location(__name__, _p)
_m = _u.module_from_spec(_s)
_sys.modules[__name__] = _m
_s.loader.exec_module(_m)
