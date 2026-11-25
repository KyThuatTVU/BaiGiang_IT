# -*- coding: utf-8 -*-
"""Bản đầy đủ 18 cảnh — Hồi quy tuyến tính (115 cue, giọng clone, SFX, An)."""
import json, os, re, subprocess, sys
os.environ.setdefault("PROJECT_ROOT", r"D:\Edit\Biagiang_Hoiquytuyentinh")
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from core import W, H, FPS, FF, FULL, seg, lin
from demo20 import decode
import sfx
from full_cues import CUES
from full_common import bg_frame, live_grid, header, rich_caption, TXT, MUT, CYAN, VIOLET, AMBER, EMER
import scenes_a
import scenes_b
import scenes_c

SCENES = {}
SCENES.update(scenes_a.SCENES)
SCENES.update(scenes_b.SCENES)
SCENES.update(scenes_c.SCENES)

OUT = FULL + "/full"
AUD = OUT + "/audio"
FR = OUT + "/frames"
TAG = os.environ.get("OUT_TAG", "_v1")
SR = sfx.SR

SCENE_IDS = list(range(1, 19))
ST = {}
S = {}
TALK = []
TOTAL = 0.0


class G:
    pass


G.ST = ST
G.S = S


def is_talk(t):
    for a, b in TALK:
        if a <= t < b:
            return True
    return False


G.is_talk = staticmethod(is_talk)


def synth_all(cues):
    import tts_vieneu
    os.makedirs(AUD, exist_ok=True)
    for c in cues:
        p = f"{AUD}/{c['id']}.wav"
        if os.path.exists(p) and os.path.getsize(p) > 12000:
            x = decode(p)
            if len(x) / SR > 0.25:
                c["path"] = p
                c["dur"] = len(x) / SR
                print(f"TTS {c['id']} reuse {c['dur']:.2f}s", flush=True)
                continue
        tts_vieneu.synth(c["say"], p)
        c["path"] = p
        c["dur"] = len(decode(p)) / SR
        print(f"TTS {c['id']} {c['dur']:.2f}s", flush=True)


def build_tl(cues):
    t = 0.35
    st = {}
    talk = []
    for c in cues:
        st[c["id"]] = t
        talk.append((t, t + c["dur"]))
        t += c["dur"] + c["pause"] + 0.15
    return st, t + 1.0, talk


def build_sfx(st, total):
    n = int(total * SR) + SR
    bus = np.zeros(n)

    def put(x, at, g):
        s0 = int(at * SR)
        if s0 < 0 or s0 >= n:
            return
        m = min(len(x), n - s0)
        bus[s0:s0 + m] += x[:m] * g

    def pitch(x, r):
        nn = max(1, int(len(x) / r))
        return np.interp(np.arange(nn) * r, np.arange(len(x)), x)

    W0 = sfx.sfx("whoosh")
    PO = sfx.sfx("pop")
    TK = sfx.sfx("tick")
    CH = sfx.sfx("chime")
    MK = sfx.marker(0.6)
    # chuyển cảnh
    for k in SCENE_IDS[1:]:
        put(pitch(W0, 0.86 + 0.03 * (k % 6)), S[k] + 0.02, 0.11)
    # cue: tick nhẹ, pop ở cue đầu mỗi cảnh
    for i, c in enumerate(CUES):
        sid = c["id"]
        put(TK, st[sid] + 0.16, 0.026)
        if sid == f"s{c['scene']:02d}c1":
            put(PO, st[sid] + 0.22, 0.06)
    # điểm nhấn nội dung
    put(PO, st["s07c5"] + 1.40, 0.07)
    put(MK, st["s07c5"] + 1.80, 0.06)
    put(PO, st["s13c3"] + 0.20, 0.07)
    put(PO, st["s13c3"] + 0.34, 0.06)
    for cid in ("s15c6", "s15c7", "s15c8"):
        put(MK, st[cid] + 0.55, 0.05)
    put(PO, st["s17c5"] + 0.20, 0.06)
    put(CH, total - 0.95, 0.07)
    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.26:
        bus *= 0.26 / pk
    elif 0 < pk < 0.20:
        bus *= 0.20 / pk
    return bus


BOUNDS = []


def scene_of(t):
    for k in SCENE_IDS:
        if S[k] <= t < (S[k + 1] if k < 18 else TOTAL):
            return k
    return 18


def draw(t):
    base = bg_frame()
    live_grid(base, t)
    k = scene_of(t) if S else 1
    SCENES[k](base, t, G)
    header(base, t)
    for c in CUES:
        s = ST[c["id"]]
        if s <= t < s + c["dur"] + 0.20:
            pin = seg(t, s, s + 0.20)
            pout = 1 - seg(t, s + c["dur"] - 0.02, s + c["dur"] + 0.20)
            rich_caption(base, c["subs"], pin * pout)
            break
    a = 0
    if t < 0.35:
        a = int(255 * (1 - t / 0.35))
    for kk in SCENE_IDS[1:]:
        sb = S[kk]
        if 0 <= t - sb < 0.28:
            a = max(a, int(230 * (1 - (t - sb) / 0.28)))
    if t > TOTAL - 0.55:
        a = max(a, int(255 * lin(t, TOTAL - 0.55, TOTAL)))
    if a > 0:
        base.alpha_composite(Image.new("RGBA", (W, H), (6, 10, 18, a)))
    return base


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def mix_audio(total):
    os.makedirs(OUT, exist_ok=True)
    mix = np.zeros(int(total * SR) + SR)
    for c in CUES:
        x = decode(c["path"])
        s0 = int(ST[c["id"]] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(ST, total)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = float(np.max(np.abs(mix)))
    print("PEAK", round(pk, 3), "TOTAL", round(total, 2), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + f"/voice_full{TAG}.wav", mix)


def encode(total):
    n = int(total * FPS)
    vid = OUT + f"/video_full{TAG}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("encode fail")
    mixp = OUT + f"/voice_full{TAG}.wav"
    comp = OUT + f"/voice_full{TAG}_comp.wav"
    run([FF, "-y", "-i", mixp, "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", comp, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"]).stderr, re.S)[-1]
    m = json.loads(m)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true,volume=-0.2dB")
    r = run([FF, "-y", "-i", comp, "-af", af, "-ar", "48000", "-c:a", "aac",
             "-b:a", "192k", OUT + f"/audio_full{TAG}.m4a"])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("audio fail")
    out = OUT + f"/hoiquy_full{TAG}.mp4"
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_full{TAG}.m4a", "-c:v", "copy",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest", out])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("mux fail")
    return out


def main():
    global ST, TALK, TOTAL
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    synth_all(CUES)
    st, total, talk = build_tl(CUES)
    ST.clear(); ST.update(st)
    TALK[:] = talk
    TOTAL = total
    for k in SCENE_IDS:
        first = next(c["id"] for c in CUES if c["scene"] == k)
        S[k] = 0.0 if k == 1 else ST[first] - 0.80
    words = sum(len(c["say"].split()) for c in CUES)
    print(f"WORD {words}  TOTAL {TOTAL:.2f}s  cues {len(CUES)} "
          f"scenes {len(SCENE_IDS)}", flush=True)
    if "--synth" in sys.argv:
        return
    if "--stills" in sys.argv:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        for k in SCENE_IDS:
            cues = [c for c in CUES if c["scene"] == k]
            last = cues[-1]
            picks = [("mid", cues[len(cues) // 2], 0.60), ("end", last, 0.70)]
            for tag, c, q in picks:
                tt = ST[c["id"]] + q * c["dur"]
                draw(tt).convert("RGB").save(f"{sd}/s{k:02d}_{tag}.png")
                print("STILL", k, tag, round(tt, 2), flush=True)
        return
    mix_audio(TOTAL)
    n = int(TOTAL * FPS)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 150 == 0:
            print("frame", k, "/", n, flush=True)
    out = encode(TOTAL)
    print("DONE", out, "frames", n, flush=True)


if __name__ == "__main__":
    main()
