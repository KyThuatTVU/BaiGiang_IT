# -*- coding: utf-8 -*-
"""Bản full bài SVD — 18 cảnh, 108 cue, giọng clone VieNeu, SFX, An."""
import json, os, re, subprocess, sys
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PROJECT_ROOT"] = PROJECT
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, r"D:\Edit\Kit\tools")
import numpy as np
from PIL import Image
from core import W, H, FPS, FULL
import demo_gateB as G
from demo_gateB import decode, caption, bg_frame, live_grid, header
import full_state as FS
from full_cues import CUES, SCENE_CUES
import scenes_a as A
import scenes_b as B
import scenes_c as C

OUT = FULL + "/full"
AUD, FR = OUT + "/audio", OUT + "/frames"
TAG = os.environ.get("OUT_TAG", "_v1")
SR = G.SR

SCENE_FN = {1: A.draw_s01, 2: A.draw_s02, 3: A.draw_s03, 4: A.draw_s04,
            5: A.draw_s05, 6: A.draw_s06, 7: B.draw_s07, 8: B.draw_s08,
            9: B.draw_s09, 10: B.draw_s10, 11: B.draw_s11, 12: B.draw_s12,
            13: C.draw_s13, 14: C.draw_s14, 15: C.draw_s15, 16: C.draw_s16,
            17: C.draw_s17, 18: C.draw_s18}


def synth_all(cues):
    import tts_vieneu
    os.makedirs(AUD, exist_ok=True)
    for c in cues:
        p = f"{AUD}/{c['id']}.wav"
        if not (os.path.exists(p) and os.path.getsize(p) > 20000):
            tts_vieneu.synth(c["say"], p)
        c["path"] = p
        c["dur"] = len(decode(p)) / SR
        print(f"TTS {c['id']} {c['dur']:.2f}s", flush=True)


def prepare():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    synth_all(CUES)
    st, total, talk = G.build_tl(CUES)
    FS.ST, FS.TALK = st, talk
    G.ST, G.TALK = st, talk
    G.SHRINK_T = st["s01c3"] - 0.25
    G.HDR_T = 0.95
    scenes = sorted(SCENE_CUES)
    for i, sc in enumerate(scenes):
        if i == 0:
            FS.S0[sc] = 0.0
            continue
        prev = SCENE_CUES[scenes[i - 1]][-1]
        FS.S0[sc] = st[prev["id"]] + prev["dur"] + 0.03
    bounds = [FS.S0[sc] for sc in scenes[1:]] + [total]
    for sc, b in zip(scenes, bounds):
        FS.S1[sc] = b
    words = sum(len(c["say"].split()) for c in CUES)
    print(f"WORD {words}  TOTAL {total:.2f}s  cues {len(CUES)}  frames {int(total * FPS)}",
          flush=True)
    with open(OUT + "/timeline.json", "w", encoding="utf-8") as f:
        json.dump({"total": total, "words": words,
                   "scene_start": {str(k): round(v, 3) for k, v in FS.S0.items()},
                   "cues": [{"id": c["id"], "scene": c["scene"], "start": round(st[c["id"]], 3),
                             "dur": round(c["dur"], 3)} for c in CUES]},
                  f, ensure_ascii=False, indent=1)
    return st, total, talk


def build_sfx(st, total):
    n = int(total * SR) + SR
    bus = np.zeros(n)

    def put(x, at, g):
        s0 = int(at * SR)
        if 0 <= s0 < n:
            m = min(len(x), n - s0)
            bus[s0:s0 + m] += x[:m] * g

    def pitch(x, r):
        nn = max(1, int(len(x) / r))
        return np.interp(np.arange(nn) * r, np.arange(len(x)), x)

    W0 = G.sfx.sfx("whoosh")
    PO = G.sfx.sfx("pop")
    TK = G.sfx.sfx("tick")
    CH = G.sfx.sfx("chime")
    MK = G.sfx.marker(0.6)
    put(pitch(W0, 0.85), 0.12, 0.16)
    put(PO, st["s01c1"] + 0.12, 0.07)
    put(PO, 0.98, 0.05)
    for i in range(3):
        put(PO, st["s01c5"] + 0.12 + i * 0.28, 0.055)
        put(TK, st["s01c5"] + 0.36 + i * 0.28, 0.03)
    for sc in sorted(FS.S0):
        if sc == 1:
            continue
        at = FS.S0[sc]
        put(pitch(W0, 0.95 + 0.025 * (sc % 6)), at, 0.10)
        put(PO, st[SCENE_CUES[sc][0]["id"]] + 0.15, 0.05)
    for i in range(8):
        put(TK, FS.S0[3] + 0.34 + i * 0.08, 0.026)
    put(MK, st["s07c5"] + 0.30, 0.055)
    put(MK, st["s08c4"] + 0.20, 0.045)
    put(MK, st["s08c5"] + 0.20, 0.045)
    put(MK, st["s08c6"] + 0.20, 0.045)
    put(MK, st["s14c5"] + 0.20, 0.045)
    put(pitch(W0, 1.06), st["s18c6"] - 0.10, 0.10)
    put(CH, total - 0.95, 0.07)
    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.26:
        bus *= 0.26 / pk
    elif 0 < pk < 0.20:
        bus *= 0.20 / pk
    return bus


def mix_audio(total):
    mix = np.zeros(int(total * SR) + SR)
    for c in CUES:
        x = decode(c["path"])
        s0 = int(FS.ST[c["id"]] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(FS.ST, total)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = float(np.max(np.abs(mix)))
    print("PEAK", round(pk, 3), "TOTAL", round(total, 2), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    G.sfx.write_wav(OUT + "/voice_full.wav", mix)
    return OUT + "/voice_full.wav"


def draw(t):
    base = bg_frame()
    live_grid(base, t)
    sc = 1
    for k in sorted(FS.S0):
        if t >= FS.S0[k]:
            sc = k
    SCENE_FN[sc](base, t, FS.S0[sc], FS.S1[sc])
    if t >= G.HDR_T:
        header(base, t)
    for c in CUES:
        s = FS.ST[c["id"]]
        if s <= t < s + c["dur"] + 0.20:
            pin = G.seg(t, s, s + 0.20)
            pout = 1 - G.seg(t, s + c["dur"] - 0.02, s + c["dur"] + 0.20)
            caption(base, c["subs"], pin * pout)
            break
    a = 0
    if t < 0.35:
        a = int(255 * (1 - t / 0.35))
    for sc in sorted(FS.S0)[1:]:
        b = FS.S0[sc]
        if 0 <= t - b < 0.22:
            a = max(a, int(200 * (1 - (t - b) / 0.22)))
    total = FS.S1[sorted(FS.S0)[-1]]
    if t > total - 0.55:
        a = max(a, int(255 * G.lin(t, total - 0.55, total)))
    if a > 0:
        base.alpha_composite(Image.new("RGBA", (W, H), (6, 10, 18, a)))
    return base


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def encode(total):
    n = int(total * FPS)
    vid = OUT + f"/video_full{TAG}.mp4"
    r = run([G.FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("encode fail")
    mixp = OUT + "/voice_full.wav"
    comp = OUT + "/voice_full_comp.wav"
    run([G.FF, "-y", "-i", mixp, "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [G.FF, "-i", comp, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"]).stderr, re.S)[-1]
    m = json.loads(m)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true,volume=-0.2dB")
    r = run([G.FF, "-y", "-i", comp, "-af", af, "-ar", "48000", "-c:a", "aac",
             "-b:a", "192k", OUT + f"/audio_full{TAG}.m4a"])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("audio fail")
    out = OUT + f"/svd_full{TAG}.mp4"
    r = run([G.FF, "-y", "-i", vid, "-i", OUT + f"/audio_full{TAG}.m4a", "-c:v", "copy",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest", out])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("mux fail")
    return out


PICKS = [
    ("01_cover", "s01c1", 0.8), ("02_title", "s01c4", 0.9), ("03_goals", "s01c5", 1.2),
    ("04_s02_photo", "s02c2", 1.2), ("05_s02_scale", "s02c5", 1.2),
    ("06_s03_grid", "s03c4", 1.2), ("07_s04_cf", "s04c4", 1.2),
    ("08_s05_approaches", "s05c5", 1.2), ("09_s06_movies", "s06c5", 1.0),
    ("10_s07_matrix", "s07c5", 1.0), ("11_s08_formula", "s08c4", 1.2),
    ("12_s09_latent", "s09c2", 1.5), ("13_s10_k2", "s10c4", 1.2),
    ("14_s11_pred", "s11c5", 1.0), ("15_s12_steps", "s12c2", 1.0),
    ("16_s12_formula", "s12c7", 1.0), ("17_s13_code", "s13c6", 1.0),
    ("18_s13_caveat", "s13c8", 1.0), ("19_s14_table", "s14c5", 1.0),
    ("20_s15_api", "s15c5", 1.0), ("21_s16_proscons", "s16c3", 1.0),
    ("22_s16_cold", "s16c7", 1.0), ("23_s17_compare", "s17c4", 1.0),
    ("24_s18_sum", "s18c3", 1.0), ("25_s18_question", "s18c5", 1.0),
    ("26_s18_outro", "s18c7", 0.8),
]


def stills(total):
    sd = OUT + "/stills"
    os.makedirs(sd, exist_ok=True)
    for name, cid, off in PICKS:
        tt = min(FS.ST[cid] + off, total - 0.2)
        draw(tt).convert("RGB").save(f"{sd}/{name}.png", quality=95)
        print("STILL", name, round(tt, 2), flush=True)


def render(a, b, total):
    n = int(total * FPS)
    a, b = max(0, a), min(n, b)
    for k in range(a, b):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 200 == 0:
            print("frame", k, "/", n, flush=True)
    print("RANGE DONE", a, b, flush=True)


def main():
    args = sys.argv[1:]
    st, total, talk = prepare()
    if "--tts" in args:
        return
    if "--stills" in args:
        stills(total)
        return
    if "--frames" in args:
        i = args.index("--frames")
        render(int(args[i + 1]), int(args[i + 2]), total)
        return
    if "--audio" in args:
        mix_audio(total)
        return
    if "--encode" in args:
        n = int(total * FPS)
        have = len([x for x in os.listdir(FR) if x.endswith(".jpg")])
        if have < n:
            raise SystemExit(f"frames {have}/{n} chưa đủ")
        if not os.path.exists(OUT + "/voice_full.wav"):
            mix_audio(total)
        print("DONE", encode(total), flush=True)
        return
    mix_audio(total)
    render(0, int(total * FPS), total)
    print("DONE", encode(total), flush=True)


if __name__ == "__main__":
    main()
