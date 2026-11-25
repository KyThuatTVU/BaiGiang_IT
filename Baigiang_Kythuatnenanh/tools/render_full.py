# -*- coding: utf-8 -*-
"""Render frame full 17 cảnh: python render_full.py [--scene S01,S02] [--probe t1,t2]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FPS, load_timeline
from scenes_web import ORDER, XFADE, DRAW

FR = os.environ.get("FR_ROOT", FULL + "/frames")


def frames_for(tl, sids):
    ns = {}
    for sid in sids:
        n = int(round(tl[sid]["total"] * FPS))
        if sid != ORDER[-1]:
            n += int(round(XFADE * FPS))
        ns[sid] = n
    return ns


def cuts_arg():
    if "--cuts" not in sys.argv:
        return None
    cuts = {}
    for part in sys.argv[sys.argv.index("--cuts") + 1].split(","):
        sid, n = part.split(":")
        cuts[sid] = int(n)
    return cuts


def main():
    probe = None
    if "--probe" in sys.argv:
        probe = [float(x) for x in sys.argv[sys.argv.index("--probe") + 1].split(",")]
    sids = None
    if "--scene" in sys.argv:
        sids = sys.argv[sys.argv.index("--scene") + 1].split(",")
    tl = load_timeline(bool(probe), sids or ORDER, cuts=cuts_arg())
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
    rng = (0, 10 ** 9)
    if "--range" in sys.argv:
        a_, b_ = sys.argv[sys.argv.index("--range") + 1].split(",")
        rng = (int(a_), int(b_))
    for sid in sids:
        out = f"{FR}/{sid}"
        os.makedirs(out, exist_ok=True)
        n = ns[sid]
        for k in range(max(0, rng[0]), min(n, rng[1])):
            p = f"{out}/f{k:04d}.jpg"
            if os.path.exists(p):
                continue
            im = DRAW[sid](k / FPS, tl)
            im.convert("RGB").save(p, quality=90)
        print(f"RENDER_DONE {sid} {n}", flush=True)


if __name__ == "__main__":
    main()
