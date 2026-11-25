# -*- coding: utf-8 -*-
"""Render frame full 17 cảnh: python render_full.py [--scene S01,S02] [--probe t1,t2]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FPS, load_timeline
from scenes_full import ORDER, XFADE, DRAW

FR = FULL + "/frames"


def frames_for(tl, sids):
    ns = {}
    for i, sid in enumerate(sids):
        n = int(round(tl[sid]["total"] * FPS))
        if i < len(sids) - 1:
            n += int(round(XFADE * FPS))
        ns[sid] = n
    return ns


def main():
    probe = None
    if "--probe" in sys.argv:
        probe = [float(x) for x in sys.argv[sys.argv.index("--probe") + 1].split(",")]
    sids = None
    if "--scene" in sys.argv:
        sids = sys.argv[sys.argv.index("--scene") + 1].split(",")
    tl = load_timeline(bool(probe), sids or ORDER)
    sids = sids or ORDER
    if probe:
        os.makedirs(FULL + "/probe", exist_ok=True)
        for sid in sids:
            for t in probe:
                im = DRAW[sid](t, tl)
                im.convert("RGB").save(f"{FULL}/probe/{sid}_{t:.1f}.jpg", quality=90)
                print("probe", sid, t, flush=True)
        return
    ns = frames_for(tl, sids)
    for sid in sids:
        out = f"{FR}/{sid}"
        os.makedirs(out, exist_ok=True)
        n = ns[sid]
        for k in range(n):
            p = f"{out}/f{k:04d}.jpg"
            if os.path.exists(p):
                continue
            im = DRAW[sid](k / FPS, tl)
            im.convert("RGB").save(p, quality=90)
        print(f"RENDER_DONE {sid} {n}", flush=True)


if __name__ == "__main__":
    main()
