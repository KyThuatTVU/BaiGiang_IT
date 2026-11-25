# -*- coding: utf-8 -*-
"""Demo 30s: luồng React -> Node.js -> MySQL, logo thật, nền công nghệ động."""
import json, math, os, re, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF, W, H, FPS, font, KIT
from demo20 import bg, shadow_card, blit, tracked, chip, json_card, seg, lin, decode, dur, caption
import sfx
import character

SR = sfx.SR
# Chuẩn từ 24/11: giọng clone là mặc định; Edge chỉ là phương án dự phòng.
BACKEND = os.environ.get("VOICE_BACKEND", "vieneu")
OUT = FULL + ("/demo30_vieneu" if BACKEND == "vieneu" else "/demo30")
AUD = OUT + "/audio"
FR = OUT + "/frames"
ICON = KIT + "/tools/icons"
VOICE = "vi-VN-NamMinhNeural"
RATE = "+12%"
WITH_AN = os.environ.get("AN_DEMO") == "1"
TAG = "_an" if WITH_AN else ""
if BACKEND == "vieneu":
    import tts_vieneu

SEGS = [
    ("s01", "Ây pi ai.", 0.25),
    ("s02", "Giao diện lập trình ứng dụng, lớp trung gian giữa các hệ thống.", 0.35),
    ("s03", "Hợp đồng giữa clai-ần và xơ vờ.", 0.45),
    ("s04", "Clai-ần viết bằng ri ắc,", 0.20),
    ("s05", "gửi ri quét, qua giao thức hát ti ti pi.", 0.45),
    ("s06", "Ây pi ai trên nốt giây,", 0.25),
    ("s07", "tiếp nhận, xác thực tâu kần và định tuyến.", 0.45),
    ("s08", "Truy vấn mai ét kiu eo", 0.25),
    ("s09", "và lấy dữ liệu cần thiết.", 0.40),
    ("s10", "Trả ri spon giây sần,", 0.40),
    ("s11", "kèm mã trạng thái hai trăm và thời gian phản hồi.", 0.45),
    ("s12", "Toàn bộ vòng gọi", 0.15),
    ("s13", "chỉ mất vài chục mili giây.", 0.50),
    ("s14", "Một vòng gọi ây pi ai trọn vẹn.", 0.30),
]

# Bản chữ cho giọng clone: thuật ngữ để nguyên tiếng Anh (ASR kiểm 24/11 đạt hơn phiên âm Edge)
TERMS_VN = {
    "s01": "Ây pi ai.",
    "s03": "Hợp đồng giữa Client và Server.",
    "s04": "Client viết bằng React,",
    "s05": "gửi request qua giao thức HTTP.",
    "s06": "API trên Node.js,",
    "s07": "tiếp nhận, xác thực token và định tuyến.",
    "s08": "Truy vấn MySQL",
    "s10": "Trả response,",
    "s11": "kèm mã trạng thái, hai trăm, và thời gian phản hồi.",
    "s13": "chỉ mất vài chục mili giây.",
    "s14": "Một vòng gọi API trọn vẹn.",
}
if BACKEND == "vieneu":
    SEGS = [(sid, TERMS_VN.get(sid, txt), pause + 0.2) for sid, txt, pause in SEGS]

TXT = (236, 241, 249)
MUT = (148, 163, 184)
AMBER = (245, 158, 11)
VIOLET = (139, 92, 246)
REACT = (97, 218, 251)
NODE = (108, 206, 112)
MYSQL = (86, 150, 200)


def synth(sid, text):
    if BACKEND == "vieneu":
        p = f"{AUD}/{sid}.wav"
        if os.path.exists(p) and os.path.getsize(p) > 20000:
            return p
        tts_vieneu.synth(text, p)
        print(f"TTS {sid} ok {dur(p):.2f}s (clone)", flush=True)
        return p
    p = f"{AUD}/{sid}.mp3"
    if os.path.exists(p) and os.path.getsize(p) > 1200:
        return p
    for rnd in range(7):
        if rnd:
            time.sleep(10)
        tmp = f"{AUD}/_raw_{sid}.mp3"
        if os.path.exists(tmp):
            os.remove(tmp)
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", VOICE, f"--rate={RATE}",
                            "--text", text, "--write-media", tmp],
                           capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if os.path.exists(tmp) and os.path.getsize(tmp) > 1200 and (dur(tmp) or 0) > 0.25:
            os.replace(tmp, p)
            print(f"TTS {sid} ok {dur(p):.2f}s", flush=True)
            return p
        print(f"TTS {sid} miss r{rnd}", flush=True)
    raise SystemExit("TTS giveup " + sid)


# ---------- assets ----------
_LOGOS = {}


def logo(name, size):
    k = (name, size)
    if k not in _LOGOS:
        im = Image.open(f"{ICON}/{name}.png").convert("RGBA")
        _LOGOS[k] = im.resize((size, size), Image.LANCZOS)
    return _LOGOS[k]


def tint(im, color, a):
    mask = im.getchannel("A").point(lambda v: int(v * a))
    out = Image.new("RGBA", im.size, color + (0,))
    out.putalpha(mask)
    return out


TRACES = [
    [(0, 206), (150, 206), (150, 286), (410, 286)],
    [(1920, 246), (1740, 246), (1740, 172), (1520, 172)],
    [(0, 792), (128, 792), (128, 724), (330, 724)],
    [(1920, 1000), (1700, 1000), (1700, 900), (1520, 900)],
]


def on_poly(poly, q):
    segs = []
    tot = 0.0
    for a, b in zip(poly, poly[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        segs.append((a, b, d))
        tot += d
    target = q * tot
    for a, b, d in segs:
        if target <= d:
            u = target / d if d else 0
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        target -= d
    return poly[-1]


_BGS = None
_SW = None


def bg_static():
    global _BGS
    if _BGS is not None:
        return _BGS
    im = bg().copy()
    for name, x, y, s, a, col in (("react", -50, 700, 400, 0.045, REACT),
                                  ("mysql", 1540, 730, 400, 0.045, MYSQL)):
        im.alpha_composite(tint(logo(name, s), col, a), (x, y))
    fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fx)
    for poly in TRACES:
        d.line(poly, fill=(150, 200, 255, 16), width=1, joint="curve")
        for pt in poly:
            d.rectangle([pt[0] - 2, pt[1] - 2, pt[0] + 2, pt[1] + 2], fill=(150, 200, 255, 30))
    # góc khung
    for x, y, sx, sy in ((44, 44, 1, 1), (W - 44, 44, -1, 1), (44, H - 44, 1, -1), (W - 44, H - 44, -1, -1)):
        d.line([x, y, x + 74 * sx, y], fill=(255, 255, 255, 42), width=2)
        d.line([x, y, x, y + 74 * sy], fill=(255, 255, 255, 42), width=2)
    im.alpha_composite(fx)
    _BGS = im
    return im


def sweep():
    global _SW
    if _SW is not None:
        return _SW
    w, h = 520, 1600
    xs = np.linspace(0, 1, w)
    a = (np.sin(xs * np.pi) ** 2 * 15).astype(np.uint8)
    arr = np.dstack([np.full((h, w), 255, np.uint8), np.full((h, w), 255, np.uint8),
                     np.full((h, w), 255, np.uint8), np.tile(a, (h, 1))])
    _SW = Image.fromarray(arr, "RGBA").rotate(18, expand=True, resample=Image.BICUBIC)
    return _SW


# ---------- draw ----------
def card(base, cx, cy, w, h, p, acc, kicker, title, sub, lname, active, t, wm=None, rise=38,
         dx0=0.0, t0=None):
    if p <= 0:
        return
    e = back(p)
    sc = 0.84 + 0.16 * e
    im, pad = shadow_card(w, h, 24, border=acc + (74,), fill=(22, 33, 57, 240))
    d = ImageDraw.Draw(im)
    al = int(80 + 70 * (0.5 + 0.5 * math.sin(t * 2.6)) * active)
    d.line([pad + 26, pad + 1, pad + w - 26, pad + 1], fill=acc + (al,), width=2)
    bob = int(2.0 * math.sin(t * 2.2) * active)
    tile = Image.new("RGBA", (54, 54), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, 53, 53], 15, fill=acc + (30 + int(24 * active),), outline=acc + (100,), width=1)
    tile.alpha_composite(logo(lname, 32), (11, 11))
    if p < 1:
        ts = 0.55 + 0.45 * back(p)
        tile = tile.resize((max(1, int(54 * ts)), max(1, int(54 * ts))), Image.BILINEAR)
        im.alpha_composite(tile, (int(pad + 26 + 27 - tile.width / 2), int(pad + 22 + bob + 27 - tile.height / 2)))
    else:
        im.alpha_composite(tile, (pad + 26, pad + 22 + bob))
    tracked(d, (pad + 94, pad + 39), kicker, font("JetBrainsMono-var.ttf", 15), acc + (255,), 2)
    d.text((pad + 26, pad + 90), title, font=font("BeVietnamPro-SemiBold.ttf", 36), fill=TXT + (255,))
    d.text((pad + 26, pad + 146), sub, font=font("BeVietnamPro-Regular.ttf", 18), fill=MUT + (255,))
    im.alpha_composite(tint(logo(wm or lname, 150), acc, 0.07), (pad + w - 156, pad + h - 156))
    if sc != 1.0:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx + dx0 * (1 - e), cy + rise * (1 - e), min(1.0, p * 1.45), 0)
    if p < 1:
        db = ImageDraw.Draw(base)
        sy = cy - h / 2 + h * p
        aa = int(64 * (1 - p))
        if aa > 0:
            db.line([cx - w / 2 + 16, sy, cx + w / 2 - 16, sy], fill=acc + (aa,), width=2)
    if t0 is not None:
        fl = seg(t, t0 + 0.42, t0 + 0.52) * (1 - seg(t, t0 + 0.52, t0 + 0.8))
        if fl > 0:
            db = ImageDraw.Draw(base)
            db.rounded_rectangle([cx - w / 2 - 4, cy - h / 2 - 4, cx + w / 2 + 4, cy + h / 2 + 4],
                                 32, outline=acc + (int(95 * fl),), width=2)


def beam(d, x0, x1, y, p, c0, c1, t=None):
    if p <= 0:
        return
    x = x0 + (x1 - x0) * p
    d.line([x0, y, x, y], fill=c0 + (32,), width=9)
    n = max(2, int(abs(x - x0) // 6))
    for i in range(n):
        xa = x0 + (x - x0) * i / n
        xb = x0 + (x - x0) * (i + 1) / n
        u = i / n
        c = tuple(int(c0[k] + (c1[k] - c0[k]) * u) for k in range(3))
        d.line([xa, y, xb, y], fill=c + (245,), width=3)
    if p < 0.995:
        for rr, aa in ((16, 30), (8, 90), (3, 230)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c1 + (aa,))
    if p > 0.62:
        u = min(1.0, (p - 0.62) / 0.3)
        c = tuple(int(c0[k] + (c1[k] - c0[k]) * u) for k in range(3))
        dx = 14 if x1 >= x0 else -14
        d.line([x - dx, y - 8, x, y, x - dx, y + 8], fill=c + (int(245 * u),), width=3, joint="curve")
    if t is not None and p > 0.99:
        q = (t * 0.75) % 1.0
        xs = x0 + (x1 - x0) * q
        dx = 26 if x1 >= x0 else -26
        d.line([xs, y, xs + dx, y], fill=(255, 255, 255, 46), width=2)


def packets(d, x0, x1, y, t, col, n=2, speed=0.24, scale=1.0):
    dirn = 1 if x1 >= x0 else -1
    for k in range(n):
        q = (t * speed + k / n) % 1.0
        x = x0 + (x1 - x0) * q
        a = int(235 * math.sin(q * math.pi) ** 0.5)
        for j in range(3):
            xa = x - dirn * (7 + j * 10) * scale
            aa = int(a * (0.30 - 0.08 * j))
            if aa > 0:
                d.line([xa, y, xa + dirn * 6 * scale, y], fill=col + (aa,), width=2)
        for rr, aa in ((13 * scale, a // 12), (8 * scale, a // 4), (4 * scale, a)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (aa,))


def pill(base, cx, cy, text, col, p, fsize=18, wpad=52, sc=1.0):
    if p <= 0:
        return
    f = font("JetBrainsMono-var.ttf", fsize)
    w = int(f.getlength(text)) + wpad
    im = Image.new("RGBA", (w, 42), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 41], 11, fill=(9, 14, 26, 238), outline=col + (180,), width=1)
    d.ellipse([12, 18, 18, 24], fill=col + (255,))
    d.text((30, 21), text, font=f, fill=(235, 241, 249), anchor="lm")
    if sc != 1.0:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx, cy, min(1.0, p * 1.4), 8)


def sql_strip(base, cx, cy, q, p, t=0.0, sc=1.0):
    if p <= 0:
        return
    w, h = 340, 62
    im, pad = shadow_card(w, h, 14, fill=(12, 19, 34, 240), border=MYSQL + (90,))
    d = ImageDraw.Draw(im)
    txt = "SELECT * FROM products;"
    vis = txt[:int(q * len(txt))]
    cf = font("JetBrainsMono-var.ttf", 16)
    d.text((pad + 16, pad + 14), vis, font=cf, fill=(214, 232, 250))
    if q < 1 or int(t * 2.2) % 2 == 0:
        cx0 = pad + 16 + d.textlength(vis, font=cf)
        d.rectangle([cx0 + 2, pad + 15, cx0 + 9, pad + 33], fill=MYSQL + (220,))
    if q >= 1:
        d.text((pad + w - 20, pad + 40), "MySQL 8", font=font("JetBrainsMono-var.ttf", 13),
               fill=MYSQL + (255,), anchor="rm")
    if sc != 1.0:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx, cy, min(1.0, p * 1.4), 10)


def ez(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def back(x, s=1.7):
    x = max(0.0, min(1.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def camera(im, t, total, stages):
    z = 1.018 + 0.014 * ez(t / total)
    for ts in stages:
        if t > ts:
            z += 0.006 * math.exp(-(t - ts) / 0.35)
    z -= 0.010 * ez(seg(t, total - 1.6, total))
    px = 3.2 * math.sin(t * 0.33)
    py = 2.2 * math.sin(t * 0.27 + 0.8)
    a = 1.0 / z
    c = W / 2 * (1 - a) + px
    f = H / 2 * (1 - a) + py
    return im.transform((W, H), Image.AFFINE, (a, 0, c, 0, a, f), resample=Image.BICUBIC)


def ripple(d, cx, cy, w, h, ts, t, col):
    for delay in (0.0, 0.14):
        q = seg(t, ts - 0.05 + delay, ts + 0.55 + delay)
        if q <= 0:
            continue
        e = 1 - (1 - q) ** 3
        ex, ey = 5 + 30 * e, 5 + 24 * e
        d.rounded_rectangle([cx - w / 2 - ex, cy - h / 2 - ey, cx + w / 2 + ex, cy + h / 2 + ey],
                            30 + 6 * e, outline=col + (int(120 * (1 - q) ** 1.5),), width=3)


def burst(d, cx, cy, w, h, ts, t, col, dur=0.45, n=10):
    q = lin(t, ts, ts + dur)
    if q <= 0 or q >= 1:
        return
    e = 1 - (1 - q) ** 3
    for i in range(n):
        ang = i * (2 * math.pi / n) + 0.35
        ex = w / 2 + 6 + 24 * e
        ey = h / 2 + 6 + 18 * e
        x0 = cx + math.cos(ang) * ex * 0.84
        y0 = cy + math.sin(ang) * ey * 0.84
        x1 = cx + math.cos(ang) * ex
        y1 = cy + math.sin(ang) * ey
        aa = int(170 * (1 - q) ** 2)
        if aa > 0:
            d.line([x0, y0, x1, y1], fill=col + (aa,), width=2)


def ring(d, cx, cy, ts, t, col, r0=14, r1=56, dur=0.42):
    q = lin(t, ts, ts + dur)
    if q <= 0 or q >= 1:
        return
    e = 1 - (1 - q) ** 2
    r = int(r0 + (r1 - r0) * e)
    aa = int(150 * (1 - q))
    if aa > 0:
        d.ellipse([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], outline=col + (aa,), width=2)


def make_draw(tl):
    st = [tl[s[0]] for s in SEGS]
    total = tl["_total"]

    def draw(t):
        base = bg_static().copy()
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        for i in range(44):
            x0 = (i * 137) % W
            y0 = (i * 211) % H
            y = (y0 - t * (7 + (i % 5) * 5)) % H
            x = x0 + 10 * math.sin(t * 0.5 + i)
            a = 10 + (i * 13) % 26
            do.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(198, 224, 255, a))
        for j in range(4):
            px, py = on_poly(TRACES[j], (t * 0.05 + j * 0.31) % 1)
            for rr, aa in ((10, 14), (5, 34), (2, 130)):
                do.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(120, 214, 255, aa))
        sw = sweep()
        ov.alpha_composite(sw, (int(-620 + ((t * 150) % (W + 1300))), -280))
        base.alpha_composite(ov)

        # header
        ph = seg(t, 0.25, 0.95)
        if ph > 0:
            hm = Image.new("RGBA", (900, 130), (0, 0, 0, 0))
            hd = ImageDraw.Draw(hm)
            tracked(hd, (450, 18), "REQUEST LIFECYCLE", font("JetBrainsMono-var.ttf", 15),
                    MUT + (255,), 4, 1.0, "mm")
            hd.text((450, 64), "Một vòng gọi API", font=font("BeVietnamPro-SemiBold.ttf", 40),
                    fill=TXT + (255,), anchor="mm")
            blit(base, hm, 960, 130, ph, 26)
        pb = seg(t, 0.15, 0.7)
        if pb > 0:
            bm = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bm)
            bd.rounded_rectangle([88, 62, 96, 110], 3, fill=AMBER + (255,))
            tracked(bd, (112, 78), "AN TECH ACADEMY", font("BeVietnamPro-SemiBold.ttf", 22), TXT + (255,), 2)
            tracked(bd, (112, 104), "KIẾN TRÚC HỆ THỐNG · API", font("JetBrainsMono-var.ttf", 14), MUT + (255,), 2)
            ver = (("V13 · CLONE + AN + SFX" if WITH_AN else "V13 · CLONE + SFX")
                   if BACKEND == "vieneu" else
                   ("V12 · AN + SFX" if WITH_AN else "V11 · MOTION + SFX"))
            tracked(bd, (1832, 78), ver,
                    font("JetBrainsMono-var.ttf", 14), MUT + (255,), 1, 1.0, "rm")
            blit(base, bm, W / 2, 70, pb, 18)

        # cards
        ar = seg(t, st[3] - 0.1, st[3] + 0.5)
        an = seg(t, st[5] - 0.1, st[5] + 0.5)
        am = seg(t, st[7] - 0.1, st[7] + 0.5)
        card(base, 380, 470, 340, 210, lin(t, 0.45, 1.05), REACT, "01 · CLIENT",
             "Client", "ứng dụng người dùng", "react", ar, t, dx0=-56, t0=0.45)
        card(base, 960, 470, 380, 220, lin(t, 0.7, 1.3), NODE, "02 · API",
             "API", "giao tiếp & định tuyến", "node", an, t, rise=46, t0=0.7)
        card(base, 1540, 470, 340, 210, lin(t, 0.95, 1.55), MYSQL, "03 · DATABASE",
             "MySQL", "lưu trữ dữ liệu", "mysql_mark", am, t, wm="mysql", dx0=56, t0=0.95)

        # ring khi node đang nói
        ov2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        do2 = ImageDraw.Draw(ov2)
        for cx, cy, w, h, acc, aq in ((380, 470, 340, 210, REACT, ar), (960, 470, 380, 220, NODE, an),
                                      (1540, 470, 340, 210, MYSQL, am)):
            if aq > 0:
                pul = 0.5 + 0.5 * math.sin(t * 3.0)
                do2.rounded_rectangle([cx - w / 2 - 6, cy - h / 2 - 6, cx + w / 2 + 6, cy + h / 2 + 6],
                                      30, outline=acc + (int((30 + 40 * pul) * aq),), width=3)
        ripple(do2, 380, 470, 340, 210, st[3], t, REACT)
        ripple(do2, 960, 470, 380, 220, st[5], t, NODE)
        ripple(do2, 1540, 470, 340, 210, st[7], t, MYSQL)
        burst(do2, 380, 470, 340, 210, st[3] + 0.02, t, REACT)
        burst(do2, 960, 470, 380, 220, st[5] + 0.02, t, NODE)
        burst(do2, 1540, 470, 340, 210, st[7] + 0.02, t, MYSQL)
        ring(do2, 770, 470, st[4] + 0.28, t, NODE)
        ring(do2, 1370, 470, st[7] + 0.28, t, MYSQL)
        ring(do2, 1150, 470, st[9] + 0.28, t, VIOLET)

        ql = seg(t, st[4] - 0.15, st[4] + 0.5)
        qr = seg(t, st[7] - 0.15, st[7] + 0.5)
        qle = 1 - (1 - ql) ** 2
        qre = 1 - (1 - qr) ** 2
        beam(do2, 550, 770, 470, qle, REACT, NODE, t)
        beam(do2, 1150, 1370, 470, qre, NODE, MYSQL, t)
        if ql > 0.95:
            packets(do2, 566, 754, 470, t, REACT)
        if qr > 0.95:
            packets(do2, 1166, 1354, 470, t, MYSQL)
        qb = seg(t, st[9] - 0.15, st[9] + 0.5)
        if qb > 0.95 and t < st[10] + 1.4:
            beam(do2, 1370, 1150, 470, 1 - (1 - qb) ** 2, MYSQL, VIOLET, t)
            packets(do2, 1354, 1166, 470, t, VIOLET, speed=0.3)
        base.alpha_composite(ov2)

        qc = lin(t, st[4] + 0.2, st[4] + 0.5)
        if ql > 0.9 and qc > 0:
            chip(base, "request", REACT, 660, 412, qc, rise=16, scale=0.78 + 0.22 * back(qc))
        qs2 = lin(t, st[7] + 0.2, st[7] + 0.5)
        if qr > 0.9 and qs2 > 0:
            chip(base, "SQL", MYSQL, 1260, 412, qs2, rise=16, scale=0.78 + 0.22 * back(qs2))
        qp2 = lin(t, st[9] - 0.05, st[9] + 0.25)
        if qr > 0.9 and qp2 > 0:
            chip(base, "response", VIOLET, 1218, 526, qp2, rise=16, scale=0.78 + 0.22 * back(qp2))

        qsr = lin(t, st[7] - 0.1, st[7] + 0.35)
        if qsr > 0:
            sql_strip(base, 1540, 618, lin(t, st[7] + 0.1, st[7] + 1.1), qsr, t,
                      sc=0.88 + 0.12 * back(qsr))

        qe = lin(t, st[2] - 0.2, st[2] + 0.45)
        if qe > 0:
            e = back(qe)
            sc = 0.86 + 0.14 * e
            pw = 560
            im = Image.new("RGBA", (pw, 56), (0, 0, 0, 0))
            dd = ImageDraw.Draw(im)
            dd.rounded_rectangle([0, 0, pw - 1, 55], 14, fill=(15, 23, 42, 238), outline=AMBER + (150,), width=2)
            dd.text((24, 28), "GET", font=font("JetBrainsMono-var.ttf", 19), fill=(52, 211, 153, 245), anchor="lm")
            dd.text((92, 28), "/api/v1/products", font=font("JetBrainsMono-var.ttf", 19), fill=TXT + (245,), anchor="lm")
            if sc != 1.0:
                im = im.resize((int(pw * sc), int(56 * sc)), Image.BILINEAR)
            blit(base, im, 960 + 26 * (1 - e), 706 + 34 * (1 - e), min(1.0, qe * 1.5), 0)
            em = Image.new("RGBA", (200, 26), (0, 0, 0, 0))
            tracked(ImageDraw.Draw(em), (4, 13), "ENDPOINT", font("JetBrainsMono-var.ttf", 13), AMBER + (255,), 2)
            blit(base, em, 800 + 18 * (1 - e), 667 + 10 * (1 - e), min(1.0, qe * 1.5), 0)
            if qe < 1:
                db = ImageDraw.Draw(base)
                aa = int(90 * (1 - qe))
                x0 = 960 - pw / 2
                db.line([x0, 706 + 30, x0 + pw * qe, 706 + 30], fill=AMBER + (aa,), width=2)

        qh = lin(t, st[4] + 0.2, st[4] + 0.6)
        if qh > 0:
            chip(base, "HTTP/1.1", (52, 211, 153), 1310, 706, qh, scale=0.8 + 0.2 * back(qh))
        qm = seg(t, st[11] - 0.1, st[11] + 0.3)
        if qm > 0:
            v = int(42 * lin(t, st[11], st[11] + 0.8))
            pill(base, 1512, 706, f"{v} ms", (148, 163, 184), qm, 17, 44, sc=0.7 + 0.3 * back(qm))
            q2 = seg(t, st[11] + 0.8, st[11] + 1.35)
            if q2 > 0:
                ov3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                e = 1 - (1 - q2) ** 3
                rx, ry = 46 + 46 * e, 26 + 34 * e
                ImageDraw.Draw(ov3).rounded_rectangle([1512 - rx, 706 - ry, 1512 + rx, 706 + ry],
                                                      12 + 10 * e, outline=AMBER + (int(110 * (1 - q2)),), width=2)
                base.alpha_composite(ov3)

        qj = lin(t, st[9] + 0.15, st[9] + 0.55)
        json_card(base, 1080, 800, 660, "200 OK · application/json",
                  ['{', '  "id": 1,', '  "ten": "Cơm gà",', '  "gia": 45000,', '  "con_hang": true', '}'],
                  lin(t, st[9] + 0.2, st[9] + 1.8), qj, scale=0.86 + 0.14 * back(qj), t=t)

        if WITH_AN:
            qa = lin(t, 0.95, 1.55)
            if qa > 0:
                if t < st[4]:
                    pose = "present"
                elif t < st[7]:
                    pose = "point_left"
                elif t < st[9]:
                    pose = "write"
                elif t < st[13]:
                    pose = "present"
                else:
                    pose = "wave"
                tk = tl.get("_talk")
                talk_on = any(a <= t < b for a, b in tk) if tk else True
                aim = character.draw(t, pose, -1, talk_on, 0.68)
                a_ = aim.getchannel("A").point(lambda v: int(v * min(1.0, qa * 1.5)))
                aim.putalpha(a_)
                e_ = back(qa)
                base.alpha_composite(aim, (1658, int(1042 - aim.height + 30 * (1 - e_))))

        caps = [
            (0.45, st[2], ["API — giao diện lập trình ứng dụng."]),
            (st[2], st[4], ["Hợp đồng giao tiếp", "giữa client và server."]),
            (st[4], st[7], ["Client gửi request qua HTTP."]),
            (st[7], st[9], ["Node.js tiếp nhận, định tuyến", "và truy vấn MySQL."]),
            (st[9], st[12], ["MySQL trả dữ liệu,", "API đóng gói response JSON."]),
            (st[12], total, ["Toàn bộ vòng gọi", "chỉ vài chục mili giây."]),
        ]
        for a0, a1, lines in caps:
            if a0 <= t < a1:
                pin = seg(t, a0, a0 + 0.35)
                pout = 1 - seg(t, a1 - 0.25, a1)
                caption(base, lines, pin * pout, (1 - back(pin)) * 26 - (1 - pout) * 14)
                break

        qf = lin(t, total - 0.7, total - 0.05)
        if qf > 0:
            base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(255 * qf))))
        base = camera(base, t, total, (st[3], st[5], st[7], st[9]))
        return base

    return draw


# ---------- sfx ----------
def _nse(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip((f - lo) / 120, 0, 1) * np.clip((hi - f) / 120, 0, 1)
    return np.fft.irfft(X * m, len(x))


def _pitch(x, r):
    n = max(1, int(len(x) / r))
    return np.interp(np.arange(n) * r, np.arange(len(x)), x)


def zap(f0, f1, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    q = t / dur
    f = f0 * (f1 / f0) ** q
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x += 0.35 * _band(_nse(n, 41), 1200, 6000)
    e = np.minimum(1, t / 0.02) * np.exp(-np.maximum(0, t - dur * 0.55) / (dur * 0.22))
    return x * e * 0.42


def shimmer(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = _band(_nse(n, 55), 3000, 8000)
    return x * (np.sin(np.pi * t / dur) ** 1.5) * 0.35


def ping(f=1567.0, dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t)
    return x * np.minimum(1, t / 0.004) * np.exp(-t / 0.18) * 0.22


def build_sfx(tl, total):
    st = [tl[s[0]] for s in SEGS]
    n = int(total * SR) + SR
    bus = np.zeros(n)

    def put(x, at, g):
        s0 = int(at * SR)
        if s0 < 0 or s0 >= n:
            return
        m = min(len(x), n - s0)
        bus[s0:s0 + m] += x[:m] * g

    W0 = sfx.sfx("whoosh"); PO = sfx.sfx("pop"); TK = sfx.sfx("tick")
    TH = sfx.sfx("thud"); CL = sfx.sfx("click"); CH = sfx.sfx("chime")

    put(_pitch(W0, 0.82), 0.14, 0.20)
    put(_pitch(W0, 1.12), 0.46, 0.15)
    for tc, r in ((0.42, 0.90), (0.67, 1.0), (0.92, 1.10)):
        put(_pitch(W0, r), tc, 0.18)
        put(TH, tc + 0.58, 0.10)
        put(PO, tc + 0.60, 0.10)
    put(_pitch(W0, 1.06), st[2] - 0.22, 0.16)
    put(PO, st[2] + 0.40, 0.09)
    for ts, r in ((st[3], 1.0), (st[5], 1.06), (st[7], 0.9)):
        put(_pitch(TH, r), ts, 0.25)
        put(shimmer(), ts + 0.02, 0.11)
        put(TK, ts + 0.10, 0.07)
    put(zap(300, 1500, 0.55), st[4] - 0.12, 0.15)
    put(PO, st[4] + 0.22, 0.08)
    put(PO, st[4] + 0.30, 0.08)
    put(PO, st[4] + 0.32, 0.06)
    put(_pitch(W0, 1.2), st[4] + 0.48, 0.07)
    put(PO, st[7] + 0.22, 0.08)
    txt = "SELECT * FROM products;"
    t0 = st[7] + 0.12
    for i in range(len(txt)):
        put(_pitch(CL, 0.9 + 0.05 * ((i * 7) % 5)), t0 + i / len(txt), 0.15 if i % 2 == 0 else 0.11)
    put(TK, t0 + 1.02, 0.08)
    put(zap(1400, 300, 0.55), st[9] - 0.16, 0.14)
    put(PO, st[9] - 0.04, 0.08)
    put(_pitch(W0, 0.95), st[9] + 0.12, 0.15)
    put(PO, st[9] + 0.52, 0.07)
    lines = [1, 10, 15, 13, 17, 1]
    tot = sum(l + 1 for l in lines)
    acc = 0
    for l in lines:
        acc += l + 1
        put(TK, st[9] + 0.2 + 1.6 * acc / tot, 0.055)
    put(CH, st[9] + 1.84, 0.09)
    put(PO, st[11] - 0.08, 0.08)
    put(TK, st[11] + 0.02, 0.05)
    put(TK, st[11] + 0.76, 0.05)
    put(ping(), st[11] + 0.80, 0.10)
    put(shimmer(0.35), st[11] + 0.82, 0.06)
    for a0 in (st[2], st[4], st[7], st[9]):
        put(_pitch(W0, 1.35), a0, 0.04)
    put(_pitch(W0, 1.08), st[12], 0.08)
    put(CH, st[13], 0.08)
    put(shimmer(0.6), total - 0.9, 0.05)
    if WITH_AN:
        put(_pitch(W0, 1.18), 0.95, 0.12)
        put(PO, 1.52, 0.10)
        put(TK, 1.56, 0.06)

    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.30:
        bus *= 0.30 / pk
        print("SFX scaled to 0.30", flush=True)
    elif 0 < pk < 0.22:
        bus *= 0.22 / pk
        print("SFX scaled up to 0.22", flush=True)
    return bus


def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    paths = [synth(sid, txt) for sid, txt, _ in SEGS]
    durs = [len(decode(p)) / SR for p in paths]
    tl = {}
    t = 0.35
    for (sid, txt, pause), dd in zip(SEGS, durs):
        tl[sid] = t
        t += dd + pause
    total = t + (0.9 if BACKEND == "vieneu" else 0.45)
    tl["_total"] = total
    tl["_talk"] = [(tl[sid], tl[sid] + dd) for (sid, _, _), dd in zip(SEGS, durs)]
    n = int(total * FPS)

    mix = np.zeros(int(total * SR) + SR)
    for (sid, txt, pause), pth in zip(SEGS, paths):
        x = decode(pth)
        s0 = int(tl[sid] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(tl, total)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = np.max(np.abs(mix))
    print("PEAK", round(pk, 3), "TOTAL", round(total, 2), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + f"/voice30{TAG}.wav", mix)

    draw = make_draw(tl)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 150 == 0:
            print("frame", k, "/", n, flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/video30{TAG}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")
    mixp = OUT + f"/voice30{TAG}.wav"
    if BACKEND == "vieneu":
        comp = OUT + f"/voice30{TAG}_comp.wav"
        run([FF, "-y", "-i", mixp, "-af",
             "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
        mixp = comp
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", mixp, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr, re.S)[-1]
    m = json.loads(m)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true")
    if BACKEND == "vieneu":
        af += ",volume=-0.2dB"  # AAC overshoot: giữ true peak ≤ -1 dBTP
    run([FF, "-y", "-i", mixp, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         OUT + f"/audio30{TAG}.m4a"])
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio30{TAG}.m4a", "-c:v", "copy", "-c:a", "copy",
             "-movflags", "+faststart", "-shortest", OUT + f"/api_pro_demo30{TAG}.mp4"])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
    print("DONE", dur(OUT + f"/api_pro_demo30{TAG}.mp4"), flush=True)


if __name__ == "__main__":
    main()
