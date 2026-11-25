# -*- coding: utf-8 -*-
"""Demo 30-35s OOP - huong animation, vi du tu dung (vi dien tu).
Chay: python demo_sample.py           # audio + render + mux
      python demo_sample.py --stills  # anh tinh de duyet bo cuc
      python demo_sample.py --audio  # chi sinh giong
"""
import math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = r"D:\Edit\Kit"
os.environ.setdefault("PROJECT_ROOT", PROJECT)
sys.path.insert(0, KIT + "/tools")
from core import W, H, FPS, FF, font, paste_brand, draw_marker, draw_marker_circle
from demo20 import bg, shadow_card, blit, tracked, seg, lin, decode, dur
from prep_icons import icon_rgba
import sfx, character, tts_vieneu

SR = sfx.SR
OUT = PROJECT + "/mau/sample"
AUD = OUT + "/audio"
FR = OUT + "/frames"
STILLS = OUT + "/stills"
IMG = PROJECT + "/img"

TXT = (236, 241, 249)
MUT = (148, 163, 184)
DIM = (100, 116, 139)
EMER = (52, 211, 153)
CYAN = (34, 211, 238)
AMBER = (245, 158, 11)
VIOLET = (139, 92, 246)
BLUE = (96, 165, 250)
RED = (248, 113, 113)
INK = (9, 14, 26)

BAL0 = 1_250_000
BAL1 = 1_450_000


def C(c, a=255):
    return c[:3] + (a,)


def hx(c):
    return "#%02X%02X%02X" % c[:3]


# ---------- voice ----------
SEGS = [
    ("c01", "Chào các bạn! Chào mừng đến với An Tech Academy. Vì sao dữ liệu trong lập trình hướng đối tượng lại được bảo vệ?", 0.45),
    ("c02", "Hôm nay, chúng ta cùng khám phá bốn tính chất cốt lõi.", 0.45),
    ("c02b", "Mỗi tính chất gắn với một từ khoá trong Java.", 0.50),
    ("c03", "Đầu tiên: đóng gói.", 0.55),
    ("c04", "Ví điện tử của bạn có số dư một triệu hai trăm năm mươi nghìn đồng.", 0.50),
    ("c05", "Nếu ai đó gán thẳng số dư, hệ thống chặn ngay.", 0.50),
    ("c05b", "Chỉ phương thức công khai mới được phép thay đổi dữ liệu.", 0.55),
    ("c06", "Nạp tiền qua phương thức hợp lệ, số dư thành một triệu bốn trăm năm mươi nghìn.", 1.10),
    ("c07", "Dữ liệu được bảo vệ. Đó là sức mạnh của đóng gói.", 0.0),
]
IDS = [s[0] for s in SEGS]


def synth(text, path):
    return tts_vieneu.synth(text, path)


def est_dur(text):
    return max(1.5, len(text) / 14.5 + 0.25)


def load_timeline():
    tl = {}
    t = 0.35
    durs = []
    missing = []
    for sid, text, pause in SEGS:
        p = f"{AUD}/{sid}.wav"
        if os.path.exists(p) and os.path.getsize(p) > 20000:
            dd = len(decode(p)) / SR
        else:
            missing.append(sid)
            dd = est_dur(text)
        tl[sid] = t
        durs.append(dd)
        t += dd + pause
    tl["_total"] = t + 1.6
    tl["_talk"] = [(tl[s[0]], tl[s[0]] + dd) for s, dd in zip(SEGS, durs)]
    tl["_dur"] = {s[0]: dd for s, dd in zip(SEGS, durs)}
    return tl, missing


# ---------- fonts / icons ----------
F = {}


def f(name, size):
    k = (name, size)
    if k not in F:
        F[k] = font(name, size)
    return F[k]


_IC = {}


def ic(name, col, size):
    k = (name, tuple(col), size)
    if k not in _IC:
        _IC[k] = icon_rgba(name, hx(col)).resize((size, size), Image.LANCZOS)
    return _IC[k]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def outp(x, p=3):
    return 1 - (1 - max(0.0, min(1.0, x))) ** p


def back(x, s=1.7):
    x = max(0.0, min(1.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def fmt(v):
    return f"{int(round(v)):,}".replace(",", ".")


def wrap2(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or fnt.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def with_alpha(im, q):
    if q >= 1.0:
        return im
    out = im.copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * q)))
    return out


# ---------- cached art ----------
_RAD = {}


def radial(col):
    if col not in _RAD:
        n = 256
        yy, xx = np.mgrid[0:n, 0:n]
        r = np.sqrt((xx - n / 2 + 0.5) ** 2 + (yy - n / 2 + 0.5) ** 2) / (n / 2)
        a = (np.clip(1 - r, 0, 1) ** 2 * 255).astype(np.uint8)
        arr = np.zeros((n, n, 4), np.uint8)
        arr[..., 0], arr[..., 1], arr[..., 2] = col[:3]
        arr[..., 3] = a
        _RAD[col] = Image.fromarray(arr, "RGBA")
    return _RAD[col]


def glow(base, cx, cy, rad, col, q):
    if q <= 0:
        return
    im = radial(col).resize((int(rad * 2), int(rad * 2)), Image.BILINEAR)
    base.alpha_composite(with_alpha(im, min(1.0, q)), (int(cx - rad), int(cy - rad)))


_INTRO = None


def intro_layer():
    global _INTRO
    if _INTRO is None:
        src = ImageOps.exif_transpose(Image.open(IMG + "/8.jpg")).convert("RGB")
        im = ImageOps.fit(src, (2200, 1240), Image.LANCZOS)
        im = Image.blend(im, Image.new("RGB", im.size, (7, 12, 22)), 0.84)
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for x in range(im.width):
            a = int(150 * max(0.0, 1 - x / 1600) ** 1.5)
            d.line([(x, 0), (x, im.height)], fill=(4, 8, 16, a))
        im = im.convert("RGBA")
        im.alpha_composite(ov)
        _INTRO = im
    return _INTRO


def intro_frame(t, q):
    lay = intro_layer()
    z = 1.06 + 0.012 * ease(min(1.0, t / 7))
    cw, ch = int(W / z), int(H / z)
    cx, cy = 1100 + 16 * math.sin(t * 0.12), 630
    x0 = int(min(max(cx - cw / 2, 0), lay.width - cw))
    y0 = int(min(max(cy - ch / 2, 0), lay.height - ch))
    im = lay.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    im.putalpha(Image.new("L", (W, H), int(255 * max(0.0, min(1.0, q)))))
    return im


_PIC = {}


def photo(name, w, h, r=18, mode="contain"):
    key = (name, w, h, r, mode)
    if key in _PIC:
        return _PIC[key]
    src = ImageOps.exif_transpose(Image.open(IMG + "/" + name + ".jpg")).convert("RGB")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if mode == "cover":
        im.paste(ImageOps.fit(src, (w, h), Image.LANCZOS), (0, 0))
    else:
        b = ImageOps.fit(src, (w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(16))
        b = Image.blend(b, Image.new("RGB", (w, h), (10, 16, 30)), 0.55)
        sc = min(w / src.width, h / src.height)
        fg = src.resize((max(1, int(src.width * sc)), max(1, int(src.height * sc))), Image.LANCZOS)
        im.paste(b, (0, 0))
        im.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    im.putalpha(mask)
    _PIC[key] = im
    return im


_PC = {}


def photo_card(name, w, h, acc):
    key = (name, w, h, acc)
    if key not in _PC:
        im, pad = shadow_card(w + 18, h + 18, 26, border=acc + (110,), fill=(18, 27, 46, 242))
        im.alpha_composite(photo(name, w, h, 14, "contain"), (pad + 9, pad + 9))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([pad + 8, pad + 8, pad + w + 9, pad + h + 9], 14,
                            outline=(255, 255, 255, 110), width=1)
        d.line([pad + 24, pad + 1, pad + w - 6, pad + 1], fill=acc + (190,), width=2)
        _PC[key] = im
    return _PC[key]


_CH = {}


def chrome(w, h, r, border, fill):
    k = (w, h, r, tuple(border), tuple(fill))
    if k not in _CH:
        _CH[k] = shadow_card(w, h, r, border=border, fill=fill)
    im, pad = _CH[k]
    return im.copy(), pad


_GS = {}


def gtext(text, fnt, c0, c1):
    key = (text, fnt.path if hasattr(fnt, "path") else id(fnt), fnt.size, tuple(c0), tuple(c1))
    if key in _GS:
        return _GS[key]
    w = int(fnt.getlength(text)) + 10
    h = int(fnt.size * 1.42)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((5, int(h * 0.06)), text, font=fnt, fill=255)
    arr = np.zeros((h, w, 3), np.uint8)
    for y in range(h):
        q = y / max(1, h - 1)
        arr[y, :, :] = [int(c0[i] + (c1[i] - c0[i]) * q) for i in range(3)]
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    im.putalpha(m)
    _GS[key] = im
    return im


_TOP = None


def top_shade():
    global _TOP
    if _TOP is None:
        arr = np.zeros((150, W, 4), np.uint8)
        for y in range(150):
            arr[y, :, 3] = int(140 * (1 - y / 149) ** 1.7)
        _TOP = Image.fromarray(arr, "RGBA")
    return _TOP


_SW = None


def sweep():
    global _SW
    if _SW is None:
        w, h = 560, 1600
        xs = np.linspace(0, 1, w)
        a = (np.sin(xs * np.pi) ** 2 * 15).astype(np.uint8)
        arr = np.dstack([np.full((h, w), 255, np.uint8), np.full((h, w), 255, np.uint8),
                         np.full((h, w), 255, np.uint8), np.tile(a, (h, 1))])
        _SW = Image.fromarray(arr, "RGBA").rotate(18, expand=True, resample=Image.BICUBIC)
    return _SW


_RND = np.random.default_rng(7)
_PARTS = [(_RND.uniform(0, W), _RND.uniform(0, H), _RND.uniform(0.4, 1.4),
           _RND.uniform(6, 20), _RND.uniform(0.8, 2.2)) for _ in range(52)]


def ambient(base, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x, y, sp, amp, sz in _PARTS:
        yy = (y - t * amp * 12) % H
        xx = (x + amp * 18 * math.sin(t * 0.35 + y)) % W
        a = int(14 + 16 * (0.5 + 0.5 * math.sin(t * 0.9 + x)))
        d.ellipse([xx - sz / 2, yy - sz / 2, xx + sz / 2, yy + sz / 2], fill=(180, 220, 255, a))
    base.alpha_composite(ov)
    sw = sweep()
    base.alpha_composite(sw, (int(-650 + (t * 105) % (W + 1300)), -300))


# ---------- header / captions ----------
def header(base, t, p=1.0):
    if p <= 0:
        return
    base.alpha_composite(top_shade())
    paste_brand(base, 72, 60, size=44, p=p, alpha=1.0)
    d = ImageDraw.Draw(base)
    tracked(d, (108, 45), "AN TECH ACADEMY", f("BeVietnamPro-SemiBold.ttf", 19), C(TXT, 250), 2, p)
    tracked(d, (108, 68), "KIẾN THỨC CÔNG NGHỆ THỰC CHIẾN", f("JetBrainsMono-var.ttf", 10),
            C(MUT, 225), 2, p)
    tracked(d, (1844, 45), "LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG", f("JetBrainsMono-var.ttf", 12),
            C(MUT, 230), 1, p, "rm")
    tracked(d, (1844, 68), "BÀI 01 · OOP", f("JetBrainsMono-var.ttf", 12), C(EMER, 245), 1, p, "rm")
    d.line([60, 96, 1860, 96], fill=C((255, 255, 255), int(24 * p)), width=1)
    for k in range(90):
        a = int((150 - k) * p)
        if a > 0:
            d.line([60 + k * 2, 96, 62 + k * 2, 96], fill=C(EMER, a), width=2)


def progress(base, t, total):
    q = max(0.0, min(1.0, t / max(total, 0.01)))
    w = int(W * q)
    if w <= 0:
        return
    d = ImageDraw.Draw(base)
    d.line([0, H - 3, w, H - 3], fill=C(EMER, 190), width=3)
    d.line([max(0, w - 90), H - 3, w, H - 3], fill=C(CYAN, 220), width=3)
    d.ellipse([w - 3, H - 6, w + 3, H], fill=(255, 255, 255, 235))


def caption(base, text, col, p):
    if p <= 0:
        return
    fnt = f("BeVietnamPro-Medium.ttf", 24)
    lines = wrap2(text, fnt, 730)
    h = 34 * len(lines) + 26
    im = Image.new("RGBA", (820, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 819, h - 1], 14, fill=(8, 13, 24, 214),
                        outline=(255, 255, 255, 22), width=1)
    d.rounded_rectangle([0, 12, 5, h - 13], 2, fill=C(col, 255))
    y = 15
    for ln in lines:
        d.text((28, y), ln, font=fnt, fill=C(TXT, 250))
        y += 34
    blit(base, im, 60 + 410, 936, p, 12)


def section(base, kicker, title, sub, col, p):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([116, 128, 122, 206], 3, fill=C(col, 235))
    tracked(d, (140, 140), kicker, f("JetBrainsMono-var.ttf", 13), C(col, 250), 2, p)
    d.text((138, 162), title, font=f("BeVietnamPro-SemiBold.ttf", 40), fill=C(TXT, int(250 * p)))
    if sub:
        d.text((140, 214), sub, font=f("BeVietnamPro-Regular.ttf", 17),
               fill=C(MUT, int(235 * p)))


# ---------- pillars ----------
PILLARS = [
    ("Đóng gói", "ENCAPSULATION", "private", "lock", EMER),
    ("Kế thừa", "INHERITANCE", "extends", "git-branch", BLUE),
    ("Đa hình", "POLYMORPHISM", "override", "layers", AMBER),
    ("Trừu tượng", "ABSTRACTION", "interface", "eye", VIOLET),
]
TILE_W, TILE_H = 330, 190
_TILE = {}


def tile_im(i):
    if i in _TILE:
        return _TILE[i]
    vn, en, kw, icon, col = PILLARS[i]
    im = Image.new("RGBA", (TILE_W + 52, TILE_H + 52), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([26, 30, 26 + TILE_W, 30 + TILE_H + 8], 22, fill=(0, 0, 0, 95))
    im = im.filter(ImageFilter.GaussianBlur(9))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([26, 26, 26 + TILE_W, 26 + TILE_H], 20,
                        fill=(17, 26, 45, 240), outline=C(col, 85), width=1)
    for k in range(0, TILE_W - 40, 6):
        q = k / (TILE_W - 40)
        al = int(115 + 85 * math.sin(q * math.pi))
        d.line([26 + 20 + k, 27, 26 + 20 + k + 6, 27], fill=C(col, al), width=2)
    d.rounded_rectangle([26 + 22, 26 + 22, 26 + 78, 26 + 78], 15,
                        fill=C(col, 30), outline=C(col, 95), width=1)
    im.alpha_composite(ic(icon, col, 34), (26 + 33, 26 + 33))
    d.text((26 + 92, 26 + 24), vn, font=f("BeVietnamPro-SemiBold.ttf", 25), fill=C(TXT, 255))
    tracked(d, (26 + 93, 26 + 66), en, f("JetBrainsMono-var.ttf", 10), C(MUT, 245), 2)
    d.text((26 + 306, 26 + 22), "0%d" % (i + 1), font=f("JetBrainsMono-var.ttf", 12),
           fill=C(DIM, 230), anchor="ra")
    d.line([26 + 24, 26 + 116, 26 + TILE_W - 24, 26 + 116], fill=(255, 255, 255, 20), width=1)
    d.text((26 + 24, 26 + 134), kw, font=f("JetBrainsMono-var.ttf", 14), fill=C(col, 250))
    d.text((26 + 24, 26 + 158), "từ khoá", font=f("BeVietnamPro-Regular.ttf", 11),
           fill=C(DIM, 210))
    _TILE[i] = im
    return im


def marker_oval(base, cx, cy, rx, ry, p, col, al=1.0):
    if p <= 0:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for pi_ in range(2):
        pts = []
        for k in range(73):
            a = 2 * math.pi * k / 72
            j = 1 + 0.035 * math.sin(k * 2.2 + pi_ * 1.9) + 0.018 * math.sin(k * 5.1)
            pts.append((cx + rx * j * math.cos(a) + 2 * pi_, cy + ry * j * math.sin(a) + 1.5 * pi_))
        kk = max(3, int(len(pts) * p))
        d.line(pts[:kk], fill=C(col, int((235 if pi_ == 0 else 160) * al)), width=2)
    base.alpha_composite(ov)


def pillars(base, t, t0, t_hi):
    xs = [360, 720, 1080, 1440]
    cy = 590
    d = ImageDraw.Draw(base)
    axy = cy + 150
    d.line([xs[0], axy, xs[-1], axy], fill=(255, 255, 255, 26), width=1)
    for i, x in enumerate(xs):
        q = seg(t, t0 + 0.16 * i, t0 + 0.16 * i + 0.62)
        if q <= 0:
            continue
        dim = 1.0 - 0.58 * seg(t, t_hi + 0.1, t_hi + 0.7) if i else 1.0
        sc = (0.9 + 0.1 * back(q)) * (1.06 if (i == 0 and t >= t_hi) else 1.0)
        im = tile_im(i)
        if sc != 1.0:
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
        if dim < 1.0:
            im = with_alpha(im, dim)
        by = cy - 40 + 36 * (1 - back(q))
        blit(base, im, x, by, q * (dim if i else 1.0), 0)
        nq = ease(seg(t, t_hi + 0.2, t_hi + 0.7))
        if i == 0 and nq > 0:
            marker_oval(base, x - 113 * sc, by + 46 * sc, 50, 15, nq, EMER)
        if t >= t_hi + 0.3:
            dc = ImageDraw.Draw(base)
            q2 = ease(seg(t, t_hi + 0.3, t_hi + 0.9))
            for k in range(4):
                xx = xs[0] + (x - xs[0]) * q2
                dc.ellipse([xx - 3, axy - 3, xx + 3, axy + 3], fill=C(EMER if xx < x else MUT, 150))


# ---------- wallet ----------
_WALL = {}


def chrome_wallet():
    if "w" not in _WALL:
        _WALL["w"] = chrome(660, 470, 18, C(EMER, 70), (16, 25, 44, 244))
    im, pad = _WALL["w"]
    return im.copy(), pad


def bal_at(t, st):
    v = BAL0 * ease(seg(t, st["c04"] + 0.55, st["c04"] + 2.65))
    v += (BAL1 - BAL0) * ease(seg(t, st["c06"] + 2.4, st["c06"] + 3.3))
    return v


def squiggle(d, x0, y, w, col):
    pts = []
    n = max(3, int(w / 6))
    for i in range(n + 1):
        pts.append((x0 + w * i / n, y + 2.4 * math.sin(i * 1.9)))
    d.line(pts, fill=C(col, 220), width=2)


def wallet_im(t, st):
    im, pad = chrome_wallet()
    d = ImageDraw.Draw(im)
    ox, oy = pad, pad
    # header
    d.rounded_rectangle([ox + 26, oy + 20, ox + 74, oy + 68], 14,
                        fill=C(EMER, 28), outline=C(EMER, 95), width=1)
    im.alpha_composite(ic("wallet", EMER, 34), (ox + 33, oy + 27))
    d.text((ox + 88, oy + 24), "VÍ AN PAY", font=f("BeVietnamPro-SemiBold.ttf", 21), fill=C(TXT, 255))
    d.text((ox + 88, oy + 53), "Ví điện tử · •••• 2048", font=f("JetBrainsMono-var.ttf", 11),
           fill=C(MUT, 235))
    pulse = 0.5 + 0.5 * math.sin(t * 3.0)
    d.ellipse([ox + 552, oy + 43, ox + 560, oy + 51], fill=C(EMER, int(160 + 80 * pulse)))
    d.text((ox + 568, oy + 41), "HOẠT ĐỘNG", font=f("JetBrainsMono-var.ttf", 10), fill=C(EMER, 230))
    d.text((ox + 568, oy + 56), "Hôm nay · 3.247 GD", font=f("JetBrainsMono-var.ttf", 9),
           fill=C(DIM, 220))
    d.line([ox + 26, oy + 92, ox + 634, oy + 92], fill=(255, 255, 255, 26), width=1)
    # balance
    tracked(d, (ox + 30, oy + 112), "SỐ DƯ KHẢ DỤNG", f("JetBrainsMono-var.ttf", 10), C(MUT, 235), 2)
    atk = seg(t, st["c05"] + 1.35, st["c05"] + 1.75) * (1 - seg(t, st["c05b"] + 0.1, st["c05b"] + 0.5))
    lockc = RED if atk > 0.2 else EMER
    im.alpha_composite(ic("lock", lockc, 13), (ox + 268, oy + 104))
    d.text((ox + 286, oy + 103), "private", font=f("JetBrainsMono-var.ttf", 11),
           fill=C(lockc, int(220 + 35 * atk)))
    v = bal_at(t, st)
    counting = (st["c04"] + 0.5 < t < st["c04"] + 2.7 or
                st["c06"] + 2.35 < t < st["c06"] + 3.4)
    if counting:
        glow(base=im, cx=ox + 170, cy=oy + 170, rad=150, col=EMER, q=0.22)
    amount = fmt(v)
    d.text((ox + 30, oy + 196), amount, font=f("BeVietnamPro-Bold.ttf", 50), fill=C(TXT, 255), anchor="ls")
    aw = d.textlength(amount, font=f("BeVietnamPro-Bold.ttf", 50))
    d.text((ox + 38 + aw, oy + 196), "đ", font=f("BeVietnamPro-Medium.ttf", 26),
           fill=C(EMER, 245), anchor="ls")
    # sparkline
    d.rounded_rectangle([ox + 424, oy + 108, ox + 636, oy + 200], 12,
                        fill=(9, 15, 27, 150), outline=(255, 255, 255, 18), width=1)
    d.text((ox + 434, oy + 116), "SỐ DƯ · 7 NGÀY", font=f("JetBrainsMono-var.ttf", 8),
           fill=C(DIM, 235))
    vals = [0.72, 0.83, 0.76, 0.95, 0.88, 1.02, v / 1e6]
    pts = []
    for i, val in enumerate(vals):
        xx = ox + 436 + i * 30
        yy = oy + 186 - (val - 0.6) / 1.0 * 54
        pts.append((xx, yy))
    d.polygon(pts + [(pts[-1][0], oy + 190), (pts[0][0], oy + 190)], fill=C(EMER, 26))
    d.line(pts, fill=C(EMER, 200), width=2, joint="curve")
    ex, ey = pts[-1]
    d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=C(EMER, 28))
    d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=C(EMER, 255))
    # transactions
    d.line([ox + 26, oy + 234, ox + 634, oy + 234], fill=(255, 255, 255, 22), width=1)
    tracked(d, (ox + 30, oy + 254), "GIAO DỊCH GẦN ĐÂY", f("JetBrainsMono-var.ttf", 10), C(MUT, 235), 2)
    sh = 42 * ease(seg(t, st["c06"] + 3.05, st["c06"] + 3.4))
    pn = ease(seg(t, st["c06"] + 2.95, st["c06"] + 3.25))
    if pn > 0:
        row(d, im, ox, oy + 282 + 10 * (1 - pn), "+ 200.000 đ", "Nạp tiền · vừa xong", EMER, "plus", pn)
    row(d, im, ox, oy + 292 + sh, "+ 850.000 đ", "Hoàn tiền Shopee · 21:10", EMER, "arrow-down", 1.0)
    row(d, im, ox, oy + 334 + sh, "- 35.000 đ", "Cà phê · 08:42", MUT, "receipt", 1.0)
    # new balance glow line
    if t > st["c06"] + 3.35:
        q = seg(t, st["c06"] + 3.35, st["c06"] + 3.7)
        d.line([ox + 30, oy + 210, ox + 30 + int(240 * q), oy + 210], fill=C(EMER, 120), width=2)
    return im


def row(d, im, ox, y, amount, label, col, icon, p):
    if p <= 0:
        return
    im.alpha_composite(with_alpha(ic(icon, col, 15), p), (ox + 32, int(y + 8)))
    d.text((ox + 62, int(y)), label, font=f("BeVietnamPro-Regular.ttf", 13),
           fill=C(TXT, int(230 * p)))
    d.text((ox + 62, int(y + 19)), "đã xử lý", font=f("JetBrainsMono-var.ttf", 8),
           fill=C(DIM, int(190 * p)))
    d.text((ox + 634, int(y + 4)), amount, font=f("JetBrainsMono-var.ttf", 13),
           fill=C(col, int(245 * p)), anchor="ra")


# ---------- code ----------
KW, TYP, CLS, FLD, MET, NUM, PUN, PLAIN = (
    (167, 139, 250), (96, 165, 250), (34, 211, 238), (52, 211, 153),
    (251, 191, 36), (245, 158, 11), (148, 163, 184), (226, 232, 240))
CODE = [
    [("public ", KW), ("class ", KW), ("ViDienTu ", CLS), ("{", PUN)],
    [("    ", PUN), ("private ", KW), ("double ", TYP), ("soDu", FLD), (" = ", PUN),
     ("1_250_000", NUM), (";", PUN)],
    [("    ", PUN), ("public ", KW), ("void ", TYP), ("napTien", MET), ("(", PUN),
     ("double ", TYP), ("tien", PLAIN), (") ", PUN), ("{", PUN)],
    [("        ", PUN), ("if ", KW), ("(", PUN), ("tien ", PLAIN), ("> ", PUN),
     ("0", NUM), (") ", PUN), ("soDu ", FLD), ("+= ", PUN), ("tien", PLAIN), (";", PUN)],
    [("    ", PUN), ("}", PUN)],
    [("    ", PUN), ("public ", KW), ("double ", TYP), ("getSoDu", MET), ("() ", PUN), ("{", PUN)],
    [("        ", PUN), ("return ", KW), ("soDu", FLD), (";", PUN)],
    [("    ", PUN), ("}", PUN)],
    [("}", PUN)],
]
CODE_TOTAL = sum(len(t) for line in CODE for t, _ in line)
CODE_CHARS = [sum(len(t) for t, _ in line) for line in CODE]
CODESTART = [sum(CODE_CHARS[:i]) for i in range(len(CODE))]


def code_budget(t, st):
    q = ease(seg(t, st["c04"] + 0.45, st["c04"] + 3.3))
    return int(q * CODE_TOTAL)


def code_card_im(t, st):
    im, pad = chrome(660, 470, 18, (255, 255, 255, 46), (16, 25, 44, 244))
    d = ImageDraw.Draw(im)
    ox, oy = pad, pad
    for k, col in enumerate(((248, 113, 113), (245, 158, 11), (52, 211, 153))):
        d.ellipse([ox + 18 + k * 18, oy + 18, ox + 28 + k * 18, oy + 28], fill=C(col, 235))
    d.text((ox + 78, oy + 16), "ViDienTu.java", font=f("JetBrainsMono-var.ttf", 12), fill=C(TXT, 240))
    atk = seg(t, st["c05"] + 1.3, st["c05"] + 1.6) * (1 - seg(t, st["c05b"] + 0.15, st["c05b"] + 0.6))
    ok = t > st["c06"] + 3.35
    lockc = RED if atk > 0.2 else (EMER if ok else MUT)
    im.alpha_composite(ic("lock", lockc, 13), (ox + 552, oy + 17))
    d.text((ox + 570, oy + 15), "Java 21", font=f("JetBrainsMono-var.ttf", 10), fill=C(MUT, 230))
    d.rounded_rectangle([ox + 14, oy + 44, ox + 646, oy + 452], 12, fill=(9, 15, 28, 190),
                        outline=(255, 255, 255, 16), width=1)
    fy = f("JetBrainsMono-var.ttf", 17)
    fl = f("JetBrainsMono-var.ttf", 11)
    y0 = oy + 66
    budget = code_budget(t, st)
    typing = budget < CODE_TOTAL
    # highlights (drawn under text weight: low alpha so code stays readable)
    if atk > 0.1:
        d.rounded_rectangle([ox + 50, y0 + 14, ox + 638, y0 + 40], 6,
                            fill=C(RED, int(22 * atk)))
        d.rounded_rectangle([ox + 50, y0 + 14, ox + 54, y0 + 40], 2, fill=C(RED, int(220 * atk)))
    if ok:
        q = ease(seg(t, st["c06"] + 2.3, st["c06"] + 2.6))
        d.rounded_rectangle([ox + 50, y0 + 46, ox + 638, y0 + 130], 6,
                            fill=C(EMER, int(20 * q)))
        d.rounded_rectangle([ox + 50, y0 + 46, ox + 54, y0 + 130], 2, fill=C(EMER, int(210 * q)))
    for i, line in enumerate(CODE):
        yy = y0 + i * 30
        d.text((ox + 20, yy - 8), "%02d" % (i + 1), font=fl, fill=C(DIM, 190))
        bx = ox + 56
        used = 0
        for txt, col in line:
            if used >= budget:
                break
            vis = txt[:budget - used]
            d.text((bx, yy - 10), vis, font=fy, fill=C(col, 255))
            bx += fy.getlength(vis)
            used += len(vis)
        if i == 1 and atk > 0.3:
            x0 = ox + 56 + fy.getlength("    private double ")
            squiggle(d, x0, yy + 16, fy.getlength("soDu"), (255, 150, 150))
        if used and i == len(CODE) - 1:
            pass
    cx = ox + 56
    if typing:
        line_i = 0
        for i in range(len(CODE)):
            if budget >= CODESTART[i] + CODE_CHARS[i]:
                continue
            line_i = i
            break
        yy = y0 + line_i * 30
        bx = ox + 56
        rem = budget - CODESTART[line_i]
        for txt, col in CODE[line_i]:
            vis = txt[:max(0, rem)]
            bx += fy.getlength(vis)
            rem -= len(vis)
        if int(t * 2.4) % 2 == 0:
            d.rectangle([bx + 2, yy - 8, bx + 9, yy + 12], fill=C(EMER, 220))
    d.line([ox + 22, oy + 424, ox + 638, oy + 424], fill=(255, 255, 255, 20), width=1)
    pub = seg(t, st["c05b"] + 0.35, st["c05b"] + 0.75) * (1 - seg(t, st["c06"] - 0.3, st["c06"] + 0.05))
    if ok:
        im.alpha_composite(ic("check-circle", EMER, 13), (ox + 24, oy + 430))
        d.text((ox + 44, oy + 429), "napTien(200_000) → OK", font=f("JetBrainsMono-var.ttf", 11),
               fill=C(EMER, 240))
    elif atk > 0.2:
        im.alpha_composite(ic("circle-x", RED, 13), (ox + 24, oy + 430))
        d.text((ox + 44, oy + 429), "soDu has private access", font=f("JetBrainsMono-var.ttf", 11),
               fill=C(RED, 240))
    elif pub > 0.05:
        im.alpha_composite(with_alpha(ic("lock", AMBER, 13), pub), (ox + 24, oy + 430))
        d.text((ox + 44, oy + 429), "public napTien() — cửa hợp lệ để đổi dữ liệu",
               font=f("JetBrainsMono-var.ttf", 11), fill=C(AMBER, int(240 * pub)))
    else:
        d.text((ox + 24, oy + 430), "soDu  private  ·  chỉ đọc qua getSoDu()",
               font=f("JetBrainsMono-var.ttf", 11), fill=C(DIM, 235))
    return im


# ---------- attack modal ----------
ATK_TEXT = [("vi.", MUT), ("soDu", RED), (" = ", PLAIN), ("999_000_000", AMBER), (";", PLAIN)]


def console_im(t, st):
    im, pad = chrome(640, 168, 14, C(RED, 120), (20, 14, 24, 246))
    d = ImageDraw.Draw(im)
    ox, oy = pad, pad
    d.text((ox + 22, oy + 14), "console · truy cập trực tiếp", font=f("JetBrainsMono-var.ttf", 10),
           fill=C(RED, 235))
    q = ease(seg(t, st["c05"] + 0.25, st["c05"] + 1.35))
    budget = int(q * sum(len(s) for s, _ in ATK_TEXT))
    fy = f("JetBrainsMono-var.ttf", 22)
    bx = ox + 22
    used = 0
    for txt, col in ATK_TEXT:
        if used >= budget:
            break
        vis = txt[:budget - used]
        d.text((bx, oy + 48), vis, font=fy, fill=C(col, 245))
        bx += fy.getlength(vis)
        used += len(vis)
    fail = t > st["c05"] + 1.45
    if not fail and int(t * 2.4) % 2 == 0:
        d.rectangle([bx + 2, oy + 50, bx + 9, oy + 72], fill=C(RED, 220))
    if fail:
        d.text((ox + 22, oy + 100), "error: soDu has private access in ViDienTu",
               font=f("JetBrainsMono-var.ttf", 11), fill=C(RED, 235))
    d.text((ox + 22, oy + 126), "không thể gán trực tiếp từ bên ngoài lớp",
           font=f("BeVietnamPro-Regular.ttf", 13), fill=C(MUT, 230))
    return im


def draw_x(base, cx, cy, r, p, col=RED):
    if p <= 0:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rr = int(r * (0.6 + 0.4 * back(p)))
    glow(ov, cx, cy, rr * 2, col, 0.5 * p)
    for s in (-1, 1):
        d.line([cx - rr, cy - rr * s, cx + rr, cy + rr * s],
               fill=(255, 255, 255, int(240 * p)), width=9)
        d.line([cx - rr, cy - rr * s, cx + rr, cy + rr * s],
               fill=C(col, int(240 * p)), width=5)
    base.alpha_composite(ov)


_STAMP = {}


def stamp_im(text, col):
    if text in _STAMP:
        return _STAMP[text]
    fnt = f("BeVietnamPro-Bold.ttf", 30)
    w = int(fnt.getlength(text)) + 56
    h = 64
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, w - 3, h - 3], 10, outline=C(col, 255), width=3)
    d.rounded_rectangle([8, 8, w - 9, h - 9], 7, outline=C(col, 120), width=1)
    d.text((w / 2, h / 2), text, font=fnt, fill=C(col, 255), anchor="mm")
    _STAMP[text] = im.rotate(-8, expand=True, resample=Image.BICUBIC)
    return _STAMP[text]


# ---------- beam ----------
def bez(p0, p1, p2, q):
    return ((1 - q) ** 2 * p0[0] + 2 * (1 - q) * q * p1[0] + q * q * p2[0],
            (1 - q) ** 2 * p0[1] + 2 * (1 - q) * q * p1[1] + q * q * p2[1])


def beam(base, t, st, p0, p1, p2, col, q, t_all):
    if q <= 0:
        return
    pts = [bez(p0, p1, p2, i / 40) for i in range(41)]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.line(pts, fill=C(col, 38), width=7, joint="curve")
    k = max(2, int(len(pts) * q))
    d.line(pts[:k], fill=C(col, 220), width=2, joint="curve")
    for j in range(2):
        u = (t_all * 0.65 + j * 0.5) % 1.0
        if u <= q:
            x, y = bez(p0, p1, p2, u)
            for rr, aa in ((13, 26), (7, 90), (3, 230)):
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=C(col, aa))
    base.alpha_composite(ov)


# ---------- draw ----------
def make_draw(tl):
    st = {k: tl[k] for k in IDS}
    total = tl["_total"]
    talk = tl.get("_talk", [])

    def draw(t):
        base = bg()
        # intro photo
        q_intro = 1 - seg(t, st["c02"] - 0.55, st["c02"] + 0.7)
        if q_intro > 0:
            base.alpha_composite(intro_frame(t, q_intro))
        else:
            glow(base, 520, 560, 420, EMER, 0.10)
            glow(base, 1345, 560, 380, BLUE, 0.08)
        ambient(base, t)
        header(base, t)

        # ---- intro ----
        pi = seg(t, 0.3, 1.05) * (1 - seg(t, st["c02"] - 0.55, st["c02"] + 0.15))
        if pi > 0:
            q = back(seg(t, 0.3, 1.05))
            d = ImageDraw.Draw(base)
            tracked(d, (116, 292), "BÀI GIẢNG · LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG",
                    f("JetBrainsMono-var.ttf", 14), C(AMBER, 245), 2, pi)
            g = gtext("OOP", f("BeVietnamPro-Bold.ttf", 158), EMER, CYAN)
            base.alpha_composite(with_alpha(g, pi), (104, int(322 + 26 * (1 - q))))
            d.text((120, 534), "Lập trình hướng đối tượng",
                   font=f("BeVietnamPro-SemiBold.ttf", 40), fill=C(TXT, int(250 * pi)))
            pmark = seg(t, 1.0, 1.7) * (1 - seg(t, st["c02"] - 0.5, st["c02"]))
            draw_marker(d, 121, 588, 630, 588, pmark, color=C(EMER, 220), width=5, seed=3)
            tracked(d, (122, 612), "ĐÓNG GÓI · KẾ THỪA · ĐA HÌNH · TRỪU TƯỢNG",
                    f("JetBrainsMono-var.ttf", 13), C(MUT, int(235 * pi)), 1)

        # ---- pillars ----
        pp = seg(t, st["c02"] - 0.35, st["c02"] + 0.2) * (1 - seg(t, st["c03"] + 1.35, st["c03"] + 1.9))
        if pp > 0:
            section(base, "BỐN TÍNH CHẤT CỦA OOP", "Từ khoá cốt lõi",
                    "Mỗi tính chất — một từ khoá trong Java", EMER, pp)
            pillars(base, t, st["c02"] + 0.05, st["c03"] + 0.05)

        # ---- wallet / code ----
        pw = seg(t, st["c03"] + 1.45, st["c03"] + 1.95) * (1 - seg(t, st["c07"] - 0.55, st["c07"] + 0.1))
        if pw > 0:
            q = back(seg(t, st["c03"] + 1.45, st["c03"] + 2.1))
            secp = seg(t, st["c03"] + 1.6, st["c03"] + 2.1)
            section(base, "TÍNH CHẤT 01 · ENCAPSULATION", "Đóng gói",
                    "Che giấu dữ liệu — chỉ mở một cửa hợp lệ.", EMER, secp)
            # dots 4 pillars
            d = ImageDraw.Draw(base)
            for k in range(4):
                xx = 1640 + k * 54
                d.rounded_rectangle([xx, 160, xx + 44, 166], 3,
                                    fill=C(EMER if k == 0 else MUT, 210 if k == 0 else 55))
            glow(base, 520, 560, 400, EMER, 0.09 * pw)
            glow(base, 1345, 560, 380, BLUE, 0.07 * pw)
            shake = 0.0
            if st["c05"] + 1.45 < t < st["c05"] + 2.1:
                shake = 9 * math.exp(-(t - st["c05"] - 1.45) / 0.16)
            shx = int(shake * math.sin(t * 95))
            shy = int(shake * 0.7 * math.sin(t * 77 + 1))
            wim = wallet_im(t, st)
            cim = code_card_im(t, st)
            # wallets slide/fade
            qw = seg(t, st["c03"] + 1.5, st["c03"] + 2.15)
            qc = seg(t, st["c03"] + 1.62, st["c03"] + 2.27)
            blit(base, wim, 520 - 40 * (1 - back(qw)) + shx, 560 + 300 * (1 - qw) + shy,
                 min(1.0, qw * 1.3), 0)
            blit(base, cim, 1345 + 40 * (1 - back(qc)), 560 + 300 * (1 - qc),
                 min(1.0, qc * 1.3), 0)
            # call chip (above the code card, clear of the Java text)
            pc = seg(t, st["c06"] + 0.35, st["c06"] + 0.75)
            if pc > 0:
                im2 = Image.new("RGBA", (250, 40), (0, 0, 0, 0))
                d2 = ImageDraw.Draw(im2)
                d2.rounded_rectangle([0, 0, 249, 39], 11, fill=C(EMER, 26), outline=C(EMER, 150), width=1)
                im2.alpha_composite(ic("terminal", EMER, 16), (12, 12))
                d2.text((36, 20), "napTien(200_000)", font=f("JetBrainsMono-var.ttf", 12),
                        fill=C(EMER, 245), anchor="lm")
                d2.text((168, 20), "→", font=f("JetBrainsMono-var.ttf", 12), fill=C(MUT, 220))
                blit(base, im2, 1345, 278, pc, 8)
                dd = ImageDraw.Draw(base)
                dd.line([1345, 300, 1345, 322], fill=C(EMER, int(90 * pc)), width=1)
                if t > st["c06"] + 2.3:
                    rq = seg(t, st["c06"] + 2.3, st["c06"] + 2.7)
                    rr = 22 + 34 * rq
                    ovr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    dr = ImageDraw.Draw(ovr)
                    dr.ellipse([1345 - rr, 278 - rr * 0.55, 1345 + rr, 278 + rr * 0.55],
                               outline=C(EMER, int(150 * (1 - rq))), width=2)
                    base.alpha_composite(ovr)
            # beam: chip -> balance, skirting above the code card
            p0, p1, p2 = (1220, 278), (940, 278), (858, 492)
            bq = seg(t, st["c06"] + 2.4, st["c06"] + 3.15) * (
                1 - seg(t, st["c06"] + 3.3, st["c06"] + 3.7))
            if bq > 0:
                beam(base, t, st, p0, p1, p2, EMER, bq, t)
            # attack
            pa = seg(t, st["c05"] + 0.05, st["c05"] + 0.35) * (1 - seg(t, st["c05b"] + 0.02, st["c05b"] + 0.35))
            if pa > 0:
                sov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                sd = ImageDraw.Draw(sov)
                sd.rounded_rectangle([174 + shx, 330 + shy, 866 + shx, 811 + shy], 16,
                                     fill=(6, 10, 18, int(120 * pa)))
                base.alpha_composite(sov)
                con = console_im(t, st)
                blit(base, con, 520, 552 - 24 * (1 - back(pa)), min(1.0, pa * 1.4), 0)
                fade = 1 - seg(t, st["c05b"] + 0.05, st["c05b"] + 0.4)
                fq = seg(t, st["c05"] + 1.45, st["c05"] + 1.75)
                if fq > 0:
                    draw_x(base, 764 + 20 * (1 - back(fq)), 546, 22, fq * fade)
                    stq = seg(t, st["c05"] + 1.7, st["c05"] + 2.05)
                    if stq > 0:
                        si = stamp_im("BỊ CHẶN", RED)
                        si = with_alpha(si, stq * fade)
                        if stq < 1:
                            si = si.resize((int(si.width * (0.8 + 0.2 * back(stq))),
                                            int(si.height * (0.8 + 0.2 * back(stq)))), Image.BILINEAR)
                        base.alpha_composite(si, (520 - si.width // 2, 692 - si.height // 2))
                # error toast
                tq = seg(t, st["c05"] + 1.9, st["c05"] + 2.2) * (1 - seg(t, st["c05b"] + 0.1, st["c05b"] + 0.45))
                if tq > 0:
                    toast(base, "soDu là private — không thể gán trực tiếp", RED, "circle-x", 832, tq)
            # public-method beat: only the public door may change data
            pb = seg(t, st["c05b"] + 0.35, st["c05b"] + 0.75) * (1 - seg(t, st["c06"] - 0.3, st["c06"] + 0.05))
            if pb > 0:
                glow(base, 470, 424, 60, EMER, 0.30 * pb)
                marker_oval(base, 1102, 452, 44, 13, pb, AMBER, al=pb)
            # success toast
            sq = seg(t, st["c06"] + 3.4, st["c06"] + 3.7) * (1 - seg(t, st["c07"] - 0.2, st["c07"] + 0.3))
            if sq > 0:
                toast(base, "Giao dịch hợp lệ — đã cộng 200.000 đ", EMER, "check-circle", 832, sq)
            # balance change flash
            fq2 = seg(t, st["c06"] + 3.35, st["c06"] + 3.6) * (1 - seg(t, st["c06"] + 3.65, st["c06"] + 4.05))
            if fq2 > 0:
                dd = ImageDraw.Draw(base)
                dd.rounded_rectangle([191, 444, 849, 522], 16, outline=C(EMER, int(110 * fq2)), width=2)

        # ---- closing ----
        pc = seg(t, st["c07"] - 0.15, st["c07"] + 0.4)
        if pc > 0:
            section(base, "TÍNH CHẤT 01 · ENCAPSULATION", "Một cửa duy nhất",
                    "Che giấu dữ liệu bên trong lớp.", EMER, pc)
            d = ImageDraw.Draw(base)
            g = gtext("ĐÓNG GÓI", f("BeVietnamPro-Bold.ttf", 58), EMER, CYAN)
            base.alpha_composite(with_alpha(g, pc), (116, int(326 + 20 * (1 - back(pc)))))
            d.text((120, 452), "Dữ liệu được bảo vệ.", font=f("BeVietnamPro-SemiBold.ttf", 32),
                   fill=C(TXT, int(250 * pc)))
            d.text((120, 500), "Chỉ thay đổi qua phương thức công khai.",
                   font=f("BeVietnamPro-Regular.ttf", 19), fill=C(MUT, int(235 * pc)))
            for k, (vn, _, _, _, col) in enumerate(PILLARS):
                q = seg(t, st["c07"] + 0.35 + 0.09 * k, st["c07"] + 0.7 + 0.09 * k)
                if q <= 0:
                    continue
                on = k == 0
                wch = 116
                imc = Image.new("RGBA", (wch, 34), (0, 0, 0, 0))
                dc = ImageDraw.Draw(imc)
                dc.rounded_rectangle([0, 0, wch - 1, 33], 9, fill=C(col, 24 if on else 10),
                                     outline=C(col, 160 if on else 45), width=1)
                dc.text((wch / 2, 16), vn, font=f("BeVietnamPro-Medium.ttf", 13),
                        fill=C(col if on else MUT, 245 if on else 170), anchor="mm")
                blit(base, imc, 120 + wch / 2 + k * 126, 566, q, 6)
            pcard = seg(t, st["c07"] + 0.1, st["c07"] + 0.7)
            if pcard > 0:
                cim = photo_card("12", 480, 350, EMER)
                blit(base, cim, 1330, 540 + 24 * (1 - back(pcard)), pcard, 0)
                d.text((1330, 748), "Encapsulation — ảnh minh hoạ từ bài giảng",
                       font=f("JetBrainsMono-var.ttf", 9), fill=C(DIM, int(200 * pcard)), anchor="mm")

        # ---- captions ----
        caps = [
            (0.0, st["c02"], "Chào các bạn! Chào mừng đến với An Tech Academy. Vì sao dữ liệu trong lập trình hướng đối tượng lại được bảo vệ?", EMER),
            (st["c02"], st["c03"], "Bốn tính chất cốt lõi của lập trình hướng đối tượng.", EMER),
            (st["c03"], st["c04"], "Tính chất 01 — Đóng gói.", EMER),
            (st["c04"], st["c05"], "Ví điện tử: số dư 1.250.000 đ.", EMER),
            (st["c05"], st["c05b"], "Gán trực tiếp số dư thì bị chặn.", RED),
            (st["c05b"], st["c06"], "Chỉ phương thức công khai được đổi dữ liệu.", EMER),
            (st["c06"], st["c06"] + 2.4, "Nạp tiền qua phương thức công khai.", EMER),
            (st["c06"] + 2.4, st["c06"] + 3.35, "Hệ thống kiểm tra và cộng tiền.", EMER),
            (st["c06"] + 3.35, st["c07"], "Số dư mới: 1.450.000 đ — hợp lệ.", EMER),
            (st["c07"], total, "Dữ liệu được bảo vệ — đó là đóng gói.", EMER),
        ]
        for a0, a1, text, col in caps:
            if a0 - 0.05 <= t < a1:
                pin = seg(t, a0, a0 + 0.3)
                pout = 1 - seg(t, a1 - 0.2, a1)
                caption(base, text, col, pin * pout)
                break

        # ---- An ----
        qa = seg(t, 0.85, 1.45) * (1 - seg(t, total - 1.8, total - 1.25))
        if qa > 0:
            if t < st["c02"]:
                pose = "wave" if t < 3.2 else "present"
            elif t < st["c03"] + 1.7:
                pose = "point_left"
            elif t < st["c05"] + 0.3:
                pose = "present"
            elif t < st["c05b"] + 0.6:
                pose = "think"
            elif t < st["c06"] + 0.2:
                pose = "write"
            elif t < st["c06"] + 4.2:
                pose = "point_left"
            else:
                pose = "wave"
            talk_on = any(a <= t < b for a, b in talk) if talk else True
            aim = character.draw(t, pose, -1, talk_on, 0.62)
            aim = with_alpha(aim, min(1.0, qa * 1.6))
            ex = 1762
            ey = 1048 + 24 * (1 - back(qa))
            base.alpha_composite(aim, (int(ex - aim.width / 2), int(ey - aim.height)))
            if st["c05"] + 0.6 < t < st["c05b"] + 0.3:
                q = 0.5 + 0.5 * math.sin(t * 7)
                d = ImageDraw.Draw(base)
                d.ellipse([1676, 686, 1728, 738], fill=(60, 12, 18, int(150 + 60 * q)),
                          outline=C(RED, 200), width=1)
                d.text((1702, 711), "!", font=f("BeVietnamPro-Bold.ttf", 24), fill=C(TXT, 250),
                       anchor="mm")

        # ---- camera + shake ----
        shake = 0.0
        if st["c05"] + 1.45 < t < st["c05"] + 2.1:
            shake = 12 * math.exp(-(t - st["c05"] - 1.45) / 0.16)
        z = 1.004 + 0.006 * ease(t / total)
        impulses = (st["c02"], st["c03"] + 1.45, st["c04"], st["c05"] + 1.45,
                    st["c05b"] + 0.4, st["c06"] + 2.4, st["c07"])
        for ts in impulses:
            if t > ts:
                z += 0.0035 * math.exp(-(t - ts) / 0.3)
        px = 2.2 * math.sin(t * 0.33) + shake * math.sin(t * 95)
        py = 1.6 * math.sin(t * 0.27 + 0.8) + shake * 0.6 * math.sin(t * 77 + 1)
        a = 1.0 / z
        ccx = W / 2 * (1 - a) + px
        ccy = H / 2 * (1 - a) + py
        base = base.transform((W, H), Image.AFFINE, (a, 0, ccx, 0, a, ccy), resample=Image.BICUBIC)

        # ---- end plate ----
        eq = seg(t, total - 1.55, total - 0.95)
        if eq > 0:
            veil = Image.new("RGBA", (W, H), (4, 7, 14, int(255 * eq)))
            base.alpha_composite(veil)
            glow(base, 960, 470, 340, EMER, 0.18 * eq)
            paste_brand(base, 960, 430, size=168, p=eq, alpha=1.0)
            d = ImageDraw.Draw(base)
            d.text((960, 566), "AN TECH ACADEMY", font=f("BeVietnamPro-SemiBold.ttf", 34),
                   fill=C(TXT, int(250 * eq)), anchor="mm")
            tracked(d, (960, 606), "HẸN GẶP LẠI · KẾ THỪA — TÍNH CHẤT 02",
                    f("JetBrainsMono-var.ttf", 13), C(MUT, int(235 * eq)), 2, 1.0, "mm")

        # fade in/out
        fin = 1 - seg(t, 0.0, 0.28)
        fout = seg(t, total - 0.32, total)
        q = max(fin, fout)
        if q > 0:
            base.alpha_composite(Image.new("RGBA", (W, H), (4, 7, 14, int(255 * q))))
        progress(base, t, total)
        return base

    return draw


def toast(base, text, col, icon, cy, p):
    if p <= 0:
        return
    fnt = f("BeVietnamPro-Medium.ttf", 16)
    w = int(fnt.getlength(text)) + 86
    im = Image.new("RGBA", (w, 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 43], 12, fill=(9, 15, 27, 238), outline=C(col, 170), width=1)
    im.alpha_composite(ic(icon, col, 18), (14, 13))
    d.text((40, 22), text, font=fnt, fill=C(TXT, 245), anchor="lm")
    blit(base, im, 520, cy, p, 12)


# ---------- sfx ----------
def _nse(n, seed):
    return np.random.default_rng(seed).standard_normal(n)


def _band(x, lo, hi):
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip((fr - lo) / 120, 0, 1) * np.clip((hi - fr) / 120, 0, 1)
    return np.fft.irfft(X * m, len(x))


def _pitch(x, r):
    n = max(1, int(len(x) / r))
    return np.interp(np.arange(n) * r, np.arange(len(x)), x)


def zap(f0, f1, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    q = tt / dur
    freq = f0 * (f1 / f0) ** q
    x = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    x += 0.35 * _band(_nse(n, 41), 1200, 6000)
    e = np.minimum(1, tt / 0.02) * np.exp(-np.maximum(0, tt - dur * 0.55) / (dur * 0.22))
    return x * e * 0.42


def shimmer(dur=0.5):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    x = _band(_nse(n, 55), 3000, 8000)
    return x * (np.sin(np.pi * tt / dur) ** 1.5) * 0.35


def coin(seed=1, dur=0.55, f0=1900.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    freq = f0 * (1 + 0.55 * np.exp(-tt * 28))
    x = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt / 0.15)
    x += 0.45 * np.sin(2 * np.pi * f0 * 2.01 * tt) * np.exp(-tt / 0.08)
    return x * 0.30


def build_sfx(tl, total):
    st = {k: tl[k] for k in IDS}
    n = int(total * SR) + SR
    bus = np.zeros(n)

    def put(x, at, g):
        s0 = int(at * SR)
        if s0 < 0 or s0 >= n:
            return
        m = min(len(x), n - s0)
        bus[s0:s0 + m] += x[:m] * g

    W0 = sfx.sfx("whoosh")
    PO = sfx.sfx("pop")
    TK = sfx.sfx("tick")
    TH = sfx.sfx("thud")
    CL = sfx.sfx("click")
    CH = sfx.sfx("chime")

    put(_pitch(W0, 0.85), 0.10, 0.18)
    put(PO, 0.48, 0.09)
    put(sfx.marker(0.4), 0.95, 0.11)
    put(shimmer(0.45), 1.05, 0.05)
    put(_pitch(W0, 1.05), st["c02"] - 0.35, 0.14)
    for i in range(4):
        put(PO, st["c02"] + 0.22 + 0.16 * i, 0.065)
    put(TK, st["c02"] + 0.95, 0.05)
    put(TK, st["c02b"] + 0.55, 0.04)
    put(PO, st["c02b"] + 0.7, 0.05)
    put(PO, st["c03"] + 0.12, 0.08)
    put(zap(1200, 300, 0.4), st["c03"] + 0.28, 0.09)
    put(sfx.marker(0.5), st["c03"] + 0.3, 0.12)
    put(_pitch(W0, 1.1), st["c03"] + 1.35, 0.16)
    put(TH, st["c03"] + 1.5, 0.16)
    put(PO, st["c03"] + 1.6, 0.07)
    put(PO, st["c03"] + 1.78, 0.07)
    # balance count + code typing
    for i in range(9):
        put(TK, st["c04"] + 0.6 + i * 0.22, 0.035)
    for i in range(16):
        put(_pitch(CL, 0.92 + 0.05 * (i % 5)), st["c04"] + 0.5 + i * 0.17, 0.032)
    put(coin(1), st["c04"] + 2.5, 0.10)
    put(CH, st["c04"] + 2.62, 0.05)
    # attack
    put(zap(500, 90, 0.5), st["c05"] + 0.05, 0.13)
    put(_pitch(W0, 1.25), st["c05"] + 0.08, 0.08)
    for i in range(9):
        put(_pitch(CL, 1.0 + 0.03 * (i % 3)), st["c05"] + 0.3 + i * 0.12, 0.045)
    put(sfx.deny(), st["c05"] + 1.48, 0.18)
    put(TH, st["c05"] + 1.5, 0.22)
    put(PO, st["c05"] + 1.72, 0.08)
    put(_pitch(W0, 0.8), st["c05b"] + 0.05, 0.08)
    put(sfx.marker(0.5), st["c05b"] + 0.55, 0.10)
    put(PO, st["c05b"] + 0.9, 0.06)
    put(shimmer(0.4), st["c05b"] + 0.95, 0.04)
    # deposit
    put(CL, st["c06"] + 2.35, 0.12)
    put(_pitch(W0, 1.15), st["c06"] + 2.4, 0.10)
    put(coin(2, f0=1750), st["c06"] + 2.55, 0.12)
    put(coin(3, f0=2100), st["c06"] + 2.75, 0.11)
    put(coin(4, f0=1950), st["c06"] + 2.95, 0.10)
    for i in range(5):
        put(TK, st["c06"] + 2.6 + i * 0.2, 0.03)
    put(sfx.success(), st["c06"] + 3.45, 0.13)
    put(shimmer(0.5), st["c06"] + 3.5, 0.05)
    # closing
    put(_pitch(W0, 1.05), st["c07"] - 0.2, 0.10)
    put(PO, st["c07"] + 0.18, 0.06)
    put(CH, st["c07"] + 0.32, 0.06)
    put(shimmer(0.7), total - 1.7, 0.05)
    put(sfx.success(), total - 1.5, 0.07)
    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.28:
        bus *= 0.28 / pk
    elif 0 < pk < 0.20:
        bus *= 0.20 / pk
    return bus


# ---------- main ----------
def synth_all():
    os.makedirs(AUD, exist_ok=True)
    for sid, text, _ in SEGS:
        p = f"{AUD}/{sid}.wav"
        ok = os.path.exists(p) and os.path.getsize(p) > 20000
        print(("CACHE " if ok else "TTS   ") + sid, flush=True)
        synth(text, p)


def stills():
    tl, missing = load_timeline()
    if missing:
        print("STILLS dùng thời lượng ước tính:", ",".join(missing), flush=True)
    os.makedirs(STILLS, exist_ok=True)
    st = {k: tl[k] for k in IDS}
    draw = make_draw(tl)
    shots = [
        ("01_intro_a", 1.30), ("01_intro_b", 3.50),
        ("02_pillars", st["c02"] + 1.30), ("02_pillars_hi", st["c03"] + 1.10),
        ("03_wallet_in", st["c04"] + 0.55), ("03_wallet_bal", st["c04"] + 2.85),
        ("04_attack_typed", st["c05"] + 1.15), ("04_attack_fail", st["c05"] + 2.10),
        ("04b_public", st["c05b"] + 1.20),
        ("05_deposit", st["c06"] + 2.75), ("05_deposit_bal", st["c06"] + 3.7),
        ("06_closing", st["c07"] + 1.30), ("07_end", tl["_total"] - 0.90),
    ]
    for name, t in shots:
        t = min(t, tl["_total"] - 0.05)
        draw(t).convert("RGB").save(f"{STILLS}/{name}.jpg", quality=92)
        print("STILL", name, round(t, 2), flush=True)


def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    synth_all()
    tl, missing = load_timeline()
    if missing:
        raise SystemExit("thiếu audio: " + ",".join(missing))
    total = tl["_total"]
    n = int(total * FPS)
    print("TOTAL", round(total, 2), "s ·", n, "frames", flush=True)

    mix = np.zeros(int(total * SR) + SR)
    for sid, _, _ in SEGS:
        x = decode(f"{AUD}/{sid}.wav")
        s0 = int(tl[sid] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(tl, total)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = float(np.max(np.abs(mix)))
    print("PEAK", round(pk, 3), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + "/voice_sample.wav", mix)

    draw = make_draw(tl)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 150 == 0:
            print("frame", k, "/", n, flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + "/oop_sample_v3.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")

    comp = OUT + "/voice_sample_comp.wav"
    run([FF, "-y", "-i", OUT + "/voice_sample.wav", "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    m2 = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", comp, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"]).stderr, re.S)[-1]
    m2 = __import__("json").loads(m2)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m2['input_i']}:measured_TP={m2['input_tp']}:"
          f"measured_LRA={m2['input_lra']}:measured_thresh={m2['input_thresh']}:"
          f"offset={m2['target_offset']}:linear=true,volume=-0.2dB")
    run([FF, "-y", "-i", comp, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         OUT + "/audio_sample.m4a"])
    final = OUT + "/oop_sample_v3_audio.mp4"
    r = run([FF, "-y", "-i", vid, "-i", OUT + "/audio_sample.m4a", "-c:v", "copy", "-c:a", "copy",
             "-movflags", "+faststart", "-shortest", final])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
    print("DONE", dur(final), final, flush=True)


if __name__ == "__main__":
    if "--stills" in sys.argv:
        stills()
    elif "--audio" in sys.argv:
        synth_all()
    else:
        main()
