# -*- coding: utf-8 -*-
"""Cổng B — Hồi quy tuyến tính: mẫu S01 + S02 + mở đầu S03, giọng clone, SFX, An."""
import json, math, os, re, subprocess, sys
os.environ.setdefault("PROJECT_ROOT", r"D:\Edit\Biagiang_Hoiquytuyentinh")
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from core import (W, H, FPS, FF, FULL, font, tw, seg, lin, draw_marker,
                  draw_marker_circle, draw_rich, paste_brand, sp_icon)
from demo20 import shadow_card, blit, tracked, chip, decode, caption
import character, sfx

PROJECT = os.environ["PROJECT_ROOT"]
IMG = PROJECT + "/img"
OUT = FULL + "/congB"
AUD, FR = OUT + "/audio", OUT + "/frames"
TAG = os.environ.get("OUT_TAG", "")
SR = sfx.SR

TXT = (236, 241, 249)
MUT = (148, 163, 184)
DIMC = (120, 136, 158)
CYAN = (56, 189, 248)
VIOLET = (167, 139, 250)
AMBER = (245, 158, 11)
EMER = (52, 211, 153)
CREAM = (245, 238, 224)
CARD = (17, 26, 45)

F_T1 = font("BeVietnamPro-Bold.ttf", 80)
F_T2 = font("BeVietnamPro-Bold.ttf", 46)
F_T4 = font("BeVietnamPro-Bold.ttf", 48)
F_T3 = font("BeVietnamPro-SemiBold.ttf", 25)
F_SUB2 = font("BeVietnamPro-Regular.ttf", 27)
F_NOTE = font("BeVietnamPro-Regular.ttf", 18)
F_BRAND = font("BeVietnamPro-SemiBold.ttf", 22)
F_MICRO = font("BeVietnamPro-Medium.ttf", 14)
F_VERSION = font("BeVietnamPro-Regular.ttf", 13)
F_BULLET = font("BeVietnamPro-SemiBold.ttf", 23)
F_BSUB = font("BeVietnamPro-Regular.ttf", 16)
F_FEAT = font("BeVietnamPro-Bold.ttf", 34)
F_FEAT_SUB = font("BeVietnamPro-Regular.ttf", 17)
F_DIM = font("BeVietnamPro-SemiBold.ttf", 21)
F_PILL = font("BeVietnamPro-SemiBold.ttf", 15)

PHOTO = "01_khai_niem_duong_hoi_quy.png"

CUES = [
    dict(id="s01c1", scene=1, pause=0.45,
         say="Xin chào các bạn! Chào mừng đến với An Tech Academy.",
         subs=["Chào các bạn!", "Chào mừng đến với An Tech Academy."]),
    dict(id="s01c2", scene=1, pause=0.40,
         say="Hôm nay chúng ta cùng tìm hiểu hồi quy tuyến tính, Linear Regression.",
         subs=["Hôm nay: Hồi quy tuyến tính", "Linear Regression."]),
    dict(id="s01c3", scene=1, pause=0.30,
         say="Một cửa hàng muốn ước tính doanh thu của ngày mai.",
         subs=["Cửa hàng cần ước tính", "doanh thu ngày mai."]),
    dict(id="s01c4", scene=1, pause=0.35,
         say="Một người mua nhà muốn biết căn nhà này khoảng bao nhiêu tiền.",
         subs=["Người mua nhà cần biết", "căn nhà giá bao nhiêu."]),
    dict(id="s01c5", scene=1, pause=0.50,
         say="Ta đều có dữ liệu trong quá khứ, và cần ước lượng một con số.",
         subs=["Có dữ liệu quá khứ,", "cần ước lượng một con số."]),
    dict(id="s02c1", scene=2, pause=0.35,
         say="Hồi quy tuyến tính là một phương pháp học có giám sát, Supervised Learning.",
         subs=["Học có giám sát", "(Supervised Learning)."]),
    dict(id="s02c2", scene=2, pause=0.30,
         say="Nó mô hình hóa quan hệ giữa biến đầu vào và một kết quả dạng số.",
         subs=["Mô hình hóa quan hệ", "giữa đầu vào và kết quả số."]),
    dict(id="s02c3", scene=2, pause=0.30,
         say="Từ dữ liệu đã có, mô hình học ra một công thức.",
         subs=["Từ dữ liệu đã có,", "mô hình học ra công thức."]),
    dict(id="s02c4", scene=2, pause=0.30,
         say="Rồi dùng công thức đó để dự đoán cho trường hợp mới.",
         subs=["Dùng công thức đó", "dự đoán trường hợp mới."]),
    dict(id="s02c5", scene=2, pause=0.40,
         say="Đây là một trong những bước khởi đầu quen thuộc của Machine Learning.",
         subs=["Bước khởi đầu quen thuộc", "của Machine Learning."]),
    dict(id="s02c6", scene=2, pause=0.50,
         say="Ví dụ, diện tích tăng thì giá thường tăng; nhưng còn vị trí, pháp lý và nhiều yếu tố khác.",
         subs=["Diện tích tăng, giá thường tăng;", "còn vị trí, pháp lý, nhiều yếu tố khác."]),
    dict(id="s03c1", scene=3, pause=0.30,
         say="Trước khi đi tiếp, ta chốt vài thuật ngữ.",
         subs=["Trước khi đi tiếp,", "chốt vài thuật ngữ."]),
    dict(id="s03c2", scene=3, pause=0.40,
         say="Feature, hay biến đầu vào X, là thông tin dùng để dự đoán; ví dụ diện tích nhà.",
         subs=["Feature: biến đầu vào X,", "thông tin dùng để dự đoán."]),
]

# ---------- look ----------
_BG = None


def bg_frame():
    global _BG
    if _BG is not None:
        return _BG.copy()
    im = Image.new("RGBA", (W, H), (9, 15, 28, 255))
    d = ImageDraw.Draw(im)
    for y in range(H):
        q = y / H
        d.line([0, y, W, y], fill=(int(13 - 4 * q), int(21 - 7 * q), int(38 - 12 * q), 255))
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.ellipse([1320, -300, 2100, 460], fill=(56, 189, 248, 26))
    gd.ellipse([-320, 720, 560, 1540], fill=(139, 92, 246, 24))
    gl = gl.filter(ImageFilter.GaussianBlur(170))
    im.alpha_composite(gl)
    _BG = im
    return _BG.copy()


_CG = {}


def corner_glow(acc):
    key = tuple(acc)
    if key not in _CG:
        r = 260
        s = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
        sd = ImageDraw.Draw(s)
        sd.ellipse([60, 60, r * 2 - 60, r * 2 - 60], fill=acc + (170,))
        _CG[key] = (s.filter(ImageFilter.GaussianBlur(95)), r)
    return _CG[key]


def live_grid(base, t):
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(gl)
    ox = (t * 5.0) % 64
    oy = (t * 3.2) % 64
    for x in range(-64, W + 64, 64):
        d.line([x + ox, 0, x + ox, H], fill=(208, 198, 180, 12))
    for y in range(-64, H + 64, 64):
        d.line([0, y + oy, W, y + oy], fill=(208, 198, 180, 12))
    arm, ins, gap = 64, 18, 30.0
    corners = ((ins, ins, 1, 1, CYAN), (W - ins, ins, -1, 1, CYAN),
               (ins, H - ins, 1, -1, VIOLET), (W - ins, H - ins, -1, -1, VIOLET))
    for i, (cx, cy, dx, dy, acc) in enumerate(corners):
        d.line([cx, cy, cx + dx * arm, cy], fill=CREAM + (60,), width=2)
        d.line([cx, cy, cx, cy + dy * arm], fill=CREAM + (60,), width=2)
        u = (t / 5.0 + i * 0.25) % 1.0
        s = u * (arm - gap)
        d.line([cx + dx * s, cy, cx + dx * (s + gap), cy], fill=acc + (165,), width=2)
        d.line([cx, cy + dy * s, cx, cy + dy * (s + gap)], fill=acc + (120,), width=2)
        d.ellipse([cx + dx * (s + gap) - 2, cy - 2, cx + dx * (s + gap) + 2, cy + 2],
                  fill=acc + (190,))
        sp, r = corner_glow(acc)
        wv = max(0.0, math.sin(2 * math.pi * (t / 6.0 + i * 0.25)))
        sc = 0.08 + 0.50 * wv * wv
        g = sp.copy()
        g.putalpha(g.getchannel("A").point(lambda v: int(v * sc)))
        gl.alpha_composite(g, (cx - r, cy - r))
    base.alpha_composite(gl)


_CB = {}


def card_base(w, h, acc):
    key = (w, h, tuple(acc))
    if key not in _CB:
        im, pad = shadow_card(w, h, 20, (255, 255, 255, 34), CARD + (244,))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([pad + 1, pad + 1, pad + w - 1, pad + h - 1], 20,
                            outline=(255, 255, 255, 28), width=1)
        d.line([pad + 22, pad + 1, pad + w - 22, pad + 1], fill=acc + (185,), width=2)
        _CB[key] = (im, pad)
    return _CB[key]


def wrap_t(text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if not cur or tw(trial, f) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def qcard(base, cx, cy, p, acc, icon, kicker, title):
    im, pad = card_base(560, 150, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 24, pad + 44, pad + 86, pad + 106], 14,
                        fill=acc + (24,), outline=acc + (76,), width=1)
    ic = sp_icon(icon, acc, 40)
    im.paste(ic, (pad + 35, pad + 55), ic)
    tracked(d, (pad + 100, pad + 34), kicker, F_MICRO, acc + (235,), 2)
    lines = wrap_t(title, F_T3, 420)
    yy = pad + 58
    for ln in lines[:2]:
        d.text((pad + 100, yy), ln, font=F_T3, fill=TXT + (255,))
        yy += 32
    blit(base, im, cx, cy, p, 18)


def bullet(base, cx, cy, p, acc, icon, label, sub):
    im, pad = card_base(600, 62, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    ic = sp_icon(icon, acc, 26)
    im.paste(ic, (pad + 22, pad + 18), ic)
    d.text((pad + 62, pad + 14), label, font=F_BULLET, fill=TXT + (255,))
    d.text((pad + 62, pad + 40), sub, font=F_BSUB, fill=MUT + (255,))
    blit(base, im, cx, cy, p, 12)


_PIC = {}
_CH = {}


def photo(name, w, h, r=20, mode="contain"):
    key = (name, w, h, r, mode)
    if key in _PIC:
        return _PIC[key]
    src = Image.open(IMG + "/" + name).convert("RGB")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if mode == "cover":
        im.paste(ImageOps.fit(src, (w, h), Image.LANCZOS), (0, 0))
    else:
        bgi = ImageOps.fit(src, (w, h), Image.LANCZOS)
        bgi = bgi.filter(ImageFilter.GaussianBlur(14))
        bgi = Image.blend(bgi, Image.new("RGB", (w, h), (12, 20, 36)), 0.5)
        sc = min(w / src.width, h / src.height)
        fg = src.resize((max(1, int(src.width * sc)), max(1, int(src.height * sc))), Image.LANCZOS)
        im.paste(bgi, (0, 0))
        im.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    im.putalpha(mask)
    _PIC[key] = im
    return im


def chrome(fw, fh, acc, r=28):
    key = (fw, fh, tuple(acc))
    if key not in _CH:
        im, pad = shadow_card(fw, fh, r, acc + (110,), (18, 27, 46, 240))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([pad + 1, pad + 1, pad + fw - 1, pad + fh - 1], r,
                            outline=(255, 255, 255, 110), width=1)
        d.line([pad + 24, pad + 1, pad + fw - 24, pad + 1], fill=acc + (185,), width=2)
        _CH[key] = (im, pad)
    return _CH[key]


def photo_card(base, name, cx, cy, w, h, p, acc, mode="contain", r=20, rise=16):
    if p <= 0:
        return
    fw, fh = w + 16, h + 16
    im, pad = chrome(fw, fh, acc)
    im = im.copy()
    im.alpha_composite(photo(name, w, h, r, mode), (pad + 8, pad + 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 7, pad + 7, pad + fw - 7, pad + fh - 7], r,
                        outline=(255, 255, 255, 110), width=1)
    blit(base, im, cx, cy, p, rise)


def header(base, t):
    p = seg(t, 0.15, 0.85)
    if p <= 0:
        return
    a = int(255 * p)
    dy = int((1 - p) * 10)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([88, 62 - dy, 96, 110 - dy], 4, fill=AMBER + (a,))
    tracked(d, (112, 78 - dy), "AN TECH ACADEMY", F_BRAND, TXT + (a,), 2)
    tracked(d, (112, 104 - dy), "MACHINE LEARNING · HỒI QUY TUYẾN TÍNH", F_MICRO,
            MUT + (a,), 1.5)
    paste_brand(base, W - 76, 62, size=84, p=p, alpha=0.95)


def an(base, t, pose, look, scale, x, y, p=1.0, talk=False):
    if p <= 0:
        return
    im = character.draw(t, pose, look, talk, scale)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
    base.alpha_composite(im, (int(x), int(y - im.height)))


def dim_slot(base, cx, cy, p, label):
    if p <= 0:
        return
    a = int(150 * p)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([cx - 165, cy - 75, cx + 165, cy + 75], 18,
                        fill=(30, 32, 40, min(225, int(220 * p))),
                        outline=CREAM + (int(76 * p),), width=1)
    d.text((cx, cy), label, font=F_DIM, fill=CREAM + (int(168 * p),), anchor="mm")


def feature_card(base, cx, cy, p):
    if p <= 0:
        return
    im, pad = card_base(330, 150, CYAN)
    im = im.copy()
    d = ImageDraw.Draw(im)
    tracked(d, (pad + 24, pad + 30), "01 · ĐẦU VÀO", F_MICRO, CYAN + (235,), 2)
    d.text((pad + 24, pad + 52), "Feature", font=F_FEAT, fill=TXT + (255,))
    d.text((pad + 24, pad + 100), "X · diện tích nhà", font=F_FEAT_SUB, fill=MUT + (255,))
    blit(base, im, cx, cy, p, 14)


# ---------- timeline ----------
def synth_all(cues):
    import tts_vieneu
    os.makedirs(AUD, exist_ok=True)
    for c in cues:
        p = f"{AUD}/{c['id']}.wav"
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


def build_sfx(st, total, ids):
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

    def shimmer(dur=0.5):
        nn = int(dur * SR)
        tt = np.arange(nn) / SR
        x = sfx._band(sfx._noise(nn, 55), 3000, 8000)
        return x * (np.sin(np.pi * tt / dur) ** 1.5) * 0.35

    W0 = sfx.sfx("whoosh")
    PO = sfx.sfx("pop")
    TK = sfx.sfx("tick")
    CH = sfx.sfx("chime")
    MK = sfx.marker(0.6)
    put(pitch(W0, 0.85), 0.12, 0.18)
    put(PO, 0.95, 0.08)
    put(TK, 1.02, 0.05)
    for i, sid in enumerate(("s01c3", "s01c4", "s01c5")):
        ts = st[sid]
        put(pitch(W0, 0.88 + 0.07 * i), ts - 0.10, 0.10)
        put(PO, ts + 0.14, 0.09)
        put(TK, ts + 0.18, 0.045)
    put(pitch(W0, 1.05), S02_START - 0.12, 0.12)
    put(PO, st["s02c1"] + 0.34, 0.08)
    put(MK, st["s02c1"] + 0.58, 0.07)
    for sid in ("s02c1", "s02c2", "s02c3"):
        put(PO, st[sid] + 0.16, 0.07)
        put(TK, st[sid] + 0.20, 0.035)
    put(PO, st["s02c5"] + 0.22, 0.06)
    put(PO, st["s02c6"] + 0.25, 0.07)
    put(pitch(W0, 1.10), S03_START - 0.12, 0.10)
    for i in range(7):
        put(TK, S03_START + 0.35 + i * 0.09, 0.03)
    if "s03c2" in ids:
        put(PO, st["s03c2"] + 0.18, 0.09)
        put(shimmer(0.45), st["s03c2"] + 0.62, 0.055)
    else:
        put(PO, S03_START + 1.18, 0.08)
        put(shimmer(0.40), S03_START + 1.58, 0.05)
    put(CH, total - 0.95, 0.07)
    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.26:
        bus *= 0.26 / pk
    elif 0 < pk < 0.20:
        bus *= 0.20 / pk
    return bus


# ---------- scenes ----------
S02_START = S03_START = 0.0
ST = {}
TALK = []
ACTIVE = []
TOTAL = 0.0


def is_talk(t):
    for a, b in TALK:
        if a <= t < b:
            return True
    return False


def draw_s01(base, t):
    d = ImageDraw.Draw(base)
    p = seg(t, 0.45, 1.25)
    if p > 0:
        a = int(255 * p)
        dy = int((1 - p) * 22)
        tracked(d, (112, 252 + dy), "MACHINE LEARNING · BÀI GIẢNG", F_MICRO,
                AMBER + (a,), 2.4)
        d.text((112, 334 + dy), "Hồi quy", font=F_T1, fill=TXT + (a,), anchor="lm")
        d.text((112, 424 + dy), "tuyến tính", font=F_T1, fill=TXT + (a,), anchor="lm")
        d.text((112, 518 + dy), "Dự đoán một con số", font=F_SUB2, fill=MUT + (a,), anchor="lm")
        d.text((112, 554 + dy), "từ dữ liệu trong quá khứ.", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    mp = seg(t, 1.15, 2.05)
    if mp > 0:
        draw_marker(d, 120, 470, 512, 470, mp, AMBER, 6, seed=3)
    for i, (sid, icon, acc, kick, ttl) in enumerate((
            ("s01c3", "trending-up", CYAN, "BÁN LẺ", "Ngày mai bán được bao nhiêu?"),
            ("s01c4", "building-2", EMER, "BẤT ĐỘNG SẢN", "Căn nhà này giá bao nhiêu?"),
            ("s01c5", "target", VIOLET, "DỮ LIỆU QUÁ KHỨ", "Cần ước lượng một con số"))):
        qp = seg(t, ST[sid] + 0.12, ST[sid] + 0.62)
        qcard(base, 1150, 300 + 170 * i, qp, acc, icon, kick, ttl)
    pose = "wave" if t < ST["s01c2"] else "present"
    an(base, t, pose, -1, 0.82, 1620, 1048, seg(t, 0.8, 1.5), is_talk(t))


def draw_s02(base, t):
    d = ImageDraw.Draw(base)
    pc = seg(t, ST["s02c1"] + 0.25, ST["s02c1"] + 1.15)
    photo_card(base, PHOTO, 640, 545, 820, 456, pc, CYAN)
    if pc > 0:
        draw_rich(d, (640, 814), "Minh họa: 20 căn nhà giả định", F_NOTE,
                  MUT + (int(210 * pc),), "mm")
    p = seg(t, S02_START + 0.15, S02_START + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (1130, 208), "KHÁI NIỆM", F_MICRO, AMBER + (a,), 2.4)
        d.text((1130, 250), "Hồi quy tuyến tính", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1130, 302), "là gì?", font=F_T2, fill=TXT + (a,), anchor="lm")
    bullet(base, 1430, 392, seg(t, ST["s02c1"] + 0.20, ST["s02c1"] + 0.70),
           CYAN, "users", "Học có giám sát", "Supervised Learning")
    bullet(base, 1430, 466, seg(t, ST["s02c2"] + 0.10, ST["s02c2"] + 0.60),
           EMER, "layers", "Đầu vào · kết quả dạng số", "Feature và Target")
    bullet(base, 1430, 540, seg(t, ST["s02c3"] + 0.10, ST["s02c3"] + 0.60),
           VIOLET, "workflow", "Học công thức từ dữ liệu", "rồi dự đoán trường hợp mới")
    chip(base, "Linear Regression", CYAN, 1250, 622,
         seg(t, ST["s02c1"] + 0.50, ST["s02c1"] + 0.90), fsize=16)
    chip(base, "Supervised Learning", VIOLET, 1530, 622,
         seg(t, ST["s02c1"] + 0.50, ST["s02c1"] + 0.90), fsize=16)
    chip(base, "Machine Learning", AMBER, 1245, 704,
         seg(t, ST["s02c5"] + 0.18, ST["s02c5"] + 0.58), fsize=16)
    chip(base, "Diện tích tăng · giá thường tăng", EMER, 1340, 776,
         seg(t, ST["s02c6"] + 0.22, ST["s02c6"] + 0.62), fsize=15)
    mk = seg(t, ST["s02c1"] + 0.55, ST["s02c1"] + 1.35)
    if mk > 0:
        draw_marker(d, 1142, 650, 1358, 650, mk, CYAN, 4, seed=5)
    an(base, t, "present", -1, 0.70, 1655, 1048, 1.0, is_talk(t))


SLOTS = [("Feature", 300, 450), ("Target", 680, 450), ("Training data", 1060, 450),
         ("y", 1440, 450), ("y mũ", 490, 650), ("Coefficient", 870, 650),
         ("Residual", 1250, 650)]


def draw_s03(base, t):
    d = ImageDraw.Draw(base)
    p = seg(t, S03_START + 0.15, S03_START + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (112, 206), "TỪ VỰNG", F_MICRO, AMBER + (a,), 2.4)
        d.text((112, 250), "Thuật ngữ cốt lõi", font=F_T4, fill=TXT + (a,), anchor="lm")
        d.text((112, 306), "7 khái niệm cần nắm trước khi vào công thức", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
        pill = Image.new("RGBA", (280, 42), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pill)
        pd.rounded_rectangle([0, 0, 279, 41], 21, fill=(9, 14, 26, 235),
                             outline=AMBER + (160,), width=1)
        pd.ellipse([18, 17, 26, 25], fill=AMBER + (255,))
        tracked(pd, (38, 21), "07 THUẬT NGỮ", F_PILL, TXT + (240,), 1.5)
        blit(base, pill, 1700, 240, p, 10)
    for i, (label, cx, cy) in enumerate(SLOTS):
        dp = seg(t, S03_START + 0.35 + i * 0.07, S03_START + 0.75 + i * 0.07)
        if i == 0:
            ft = ST.get("s03c2")
            fs = (ft + 0.12) if ft else (S03_START + 1.05)
            fp = seg(t, fs, fs + 0.50)
            if fp > 0:
                feature_card(base, cx, cy, fp)
            else:
                dim_slot(base, cx, cy, dp, label)
        else:
            dim_slot(base, cx, cy, dp, label)
    ft = ST.get("s03c2")
    cs = (ft + 0.58) if ft else (S03_START + 1.55)
    cp = seg(t, cs, cs + 0.67)
    if cp > 0:
        draw_marker_circle(d, 300, 450, 198, 114, cp, CYAN, 5, seed=4)
    an(base, t, "present", -1, 0.66, 1672, 1048, 1.0, is_talk(t))


def draw(t):
    base = bg_frame()
    live_grid(base, t)
    if t < S02_START:
        draw_s01(base, t)
    elif t < S03_START:
        draw_s02(base, t)
    else:
        draw_s03(base, t)
    header(base, t)
    for c in ACTIVE:
        s = ST[c["id"]]
        if s <= t < s + c["dur"] + 0.20:
            pin = seg(t, s, s + 0.20)
            pout = 1 - seg(t, s + c["dur"] - 0.02, s + c["dur"] + 0.20)
            caption(base, c["subs"], pin * pout)
            break
    a = 0
    if t < 0.35:
        a = int(255 * (1 - t / 0.35))
    for sb in (S02_START, S03_START):
        if 0 <= t - sb < 0.28:
            a = max(a, int(230 * (1 - (t - sb) / 0.28)))
    if t > TOTAL - 0.55:
        a = max(a, int(255 * lin(t, TOTAL - 0.55, TOTAL)))
    if a > 0:
        base.alpha_composite(Image.new("RGBA", (W, H), (6, 10, 18, a)))
    return base


# ---------- audio ----------
def mix_audio(total):
    mix = np.zeros(int(total * SR) + SR)
    for c in ACTIVE:
        x = decode(c["path"])
        s0 = int(ST[c["id"]] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(ST, total, set(ST))
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = float(np.max(np.abs(mix)))
    print("PEAK", round(pk, 3), "TOTAL", round(total, 2), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + "/voice_congB.wav", mix)


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def encode(total):
    n = int(total * FPS)
    vid = OUT + f"/video_congB{TAG}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("encode fail")
    mixp = OUT + "/voice_congB.wav"
    comp = OUT + "/voice_congB_comp.wav"
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
             "-b:a", "192k", OUT + f"/audio_congB{TAG}.m4a"])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("audio fail")
    out = OUT + f"/hoiquy_congB{TAG}.mp4"
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_congB{TAG}.m4a", "-c:v", "copy",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest", out])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("mux fail")
    return out


# ---------- sampler ----------
TERMS = [
    ("t01", "Supervised Learning."),
    ("t02", "Linear Regression."),
    ("t03", "Feature."),
    ("t04", "Target."),
    ("t05", "Residual."),
    ("t06", "MAE."),
    ("t07", "MSE."),
    ("t08", "RMSE."),
    ("t09", "R bình phương."),
    ("t10", "scikit-learn."),
    ("t11", "pandas."),
    ("t12", "tệp CSV."),
]


def sampler():
    import tts_vieneu
    d = OUT + "/sampler"
    os.makedirs(d, exist_ok=True)
    parts = []
    for sid, text in TERMS:
        p = f"{d}/{sid}.wav"
        tts_vieneu.synth(text, p)
        x = decode(p)
        parts.append(x)
        parts.append(np.zeros(int(0.25 * SR)))
        print("SAMPLER", sid, f"{len(x)/SR:.2f}s", text, flush=True)
    x = np.concatenate(parts)
    pk = float(np.max(np.abs(x)))
    if pk > 0:
        x *= 0.9 / pk
    wav = OUT + "/sampler_thuat_ngu.wav"
    sfx.write_wav(wav, x)
    run([FF, "-y", "-i", wav, "-af", "loudnorm=I=-16:TP=-1:LRA=11", "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k", OUT + "/sampler_thuat_ngu.m4a"])
    print("SAMPLER DONE", round(len(x) / SR, 2), "s", flush=True)


# ---------- main ----------
def main():
    global S02_START, S03_START, ST, TALK, ACTIVE, TOTAL
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    synth_all(CUES)
    st, total, talk = build_tl(CUES)
    if total > 45.0 and CUES[-1]["id"] == "s03c2":
        print(f"bỏ s03c2 vì mẫu {total:.1f}s > 45s", flush=True)
        active = [c for c in CUES if c["id"] != "s03c2"]
        st, total, talk = build_tl(active)
    else:
        active = CUES
    ST, TALK, ACTIVE, TOTAL = st, talk, active, total
    S02_START = st["s02c1"] - 0.80
    S03_START = st["s03c1"] - 0.80
    words = sum(len(c["say"].split()) for c in active)
    print(f"WORD {words}  TOTAL {total:.2f}s  cues {len(active)}", flush=True)
    if "--stills" in sys.argv:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        picks = [("01_title", "s01c2", 0.7), ("02_card1", "s01c3", 0.8),
                 ("03_card2", "s01c4", 0.8), ("04_card3", "s01c5", 0.8),
                 ("05_photo", "s02c2", 0.5), ("06_chips", "s02c6", 0.5),
                 ("07_grid", "s03c1", 0.7)]
        if "s03c2" in st:
            picks.append(("08_feature", "s03c2", 0.8))
        for name, sid, q in picks:
            tt = st[sid] + q * next(c["dur"] for c in active if c["id"] == sid)
            draw(tt).convert("RGB").save(f"{sd}/{name}.png", quality=95)
            print("STILL", name, round(tt, 2), flush=True)
        return
    mix_audio(total)
    n = int(total * FPS)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 120 == 0:
            print("frame", k, "/", n, flush=True)
    out = encode(total)
    print("DONE", out, "frames", n, flush=True)
    sampler()


if __name__ == "__main__":
    if "--sampler" in sys.argv:
        os.makedirs(OUT, exist_ok=True)
        sampler()
    else:
        main()
