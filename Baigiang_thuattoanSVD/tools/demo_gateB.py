# -*- coding: utf-8 -*-
"""Cổng B — SVD: mẫu S01 + S02 + mở đầu S03, giọng clone VieNeu, SFX, An."""
import json, math, os, re, subprocess, sys
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PROJECT_ROOT"] = PROJECT
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from core import (W, H, FPS, FF, FULL, font, tw, seg, lin, draw_marker,
                  draw_marker_circle, draw_rich, paste_brand, sp_icon)
from demo20 import shadow_card, blit, tracked, chip, decode, caption
import character, sfx

IMG = PROJECT + "/img"
OUT = FULL + "/congB"
AUD, FR = OUT + "/audio", OUT + "/frames"
TAG = os.environ.get("OUT_TAG", "_v1")
SR = sfx.SR

TXT = (236, 241, 249)
MUT = (148, 163, 184)
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
F_BULLET = font("BeVietnamPro-SemiBold.ttf", 23)
F_BSUB = font("BeVietnamPro-Regular.ttf", 16)
F_LEG = font("BeVietnamPro-Medium.ttf", 20)
F_CELL = font("PlusJakartaSans-var.ttf", 20, 600)
F_QM = font("BeVietnamPro-Bold.ttf", 30)
F_STAT = font("PlusJakartaSans-var.ttf", 36, 700)
F_STATL = font("BeVietnamPro-Regular.ttf", 18)

CUES = [
    dict(id="s01c1", scene=1, pause=0.45,
         say="Xin chào các bạn! Chào mừng đến với An Tech Academy.",
         subs=["Chào các bạn!", "Chào mừng đến với An Tech Academy."]),
    dict(id="s01c2", scene=1, pause=0.40,
         say="Bạn đã bao giờ tự hỏi: vì sao vừa xem một món hàng, trang web đã gợi ý thêm hàng loạt sản phẩm tương tự?",
         subs=["Vì sao vừa xem một món hàng,", "web đã gợi ý thêm sản phẩm tương tự?"]),
    dict(id="s01c3", scene=1, pause=0.35,
         say="Đằng sau những ô gợi ý đó thường là một thuật toán mang tên SVD.",
         subs=["Đằng sau những ô gợi ý", "là thuật toán mang tên SVD."]),
    dict(id="s01c4", scene=1, pause=0.35,
         say="Hôm nay, chúng ta cùng tìm hiểu SVD, và ứng dụng của nó trong lọc cộng tác, Collaborative Filtering.",
         subs=["Hôm nay: SVD", "và lọc cộng tác · Collaborative Filtering."]),
    dict(id="s01c5", scene=1, pause=0.45,
         say="Sau bài học, bạn sẽ hiểu bản chất, đọc được công thức, và chạy được một mô hình gợi ý đơn giản bằng Python.",
         subs=["Hiểu bản chất · đọc được công thức", "chạy được mô hình gợi ý bằng Python."]),
    dict(id="s02c1", scene=2, pause=0.35,
         say="Những mục như \"dành riêng cho bạn\" hay \"có thể bạn cũng thích\" đã trở nên quen thuộc.",
         subs=["\"Dành riêng cho bạn\",", "\"Có thể bạn cũng thích\" — đã quen thuộc."]),
    dict(id="s02c2", scene=2, pause=0.35,
         say="Chúng xuất hiện trên trang chủ, trong trang sản phẩm, và cả trong khung giỏ hàng.",
         subs=["Trên trang chủ, trong trang sản phẩm,", "và cả trong khung giỏ hàng."]),
    dict(id="s03c1", scene=3, pause=0.45,
         say="Hãy hình dung toàn bộ lượt xem, lượt mua và đánh giá được ghi lại thành một bảng.",
         subs=["Lượt xem, lượt mua, đánh giá", "được ghi lại thành một bảng."]),
]

GOALS = [
    (CYAN, "layers", "Hiểu bản chất SVD", "ma trận và yếu tố tiềm ẩn"),
    (AMBER, "braces", "Đọc được công thức", "A = U · Sigma · V chuyển vị"),
    (EMER, "code-xml", "Chạy mô hình Python", "Surprise · gợi ý Top-N"),
]

CARD_CX, CARD_CY, CARD_W, CARD_H = 1378, 390, 820, 460

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


HDR_T = 0.0


def header(base, t):
    p = seg(t, HDR_T + 0.15, HDR_T + 0.85)
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([88, 62, 96, 110], 4, fill=AMBER + (255,))
    tracked(d, (112, 78), "AN TECH ACADEMY", F_BRAND, TXT + (255,), 2)
    tracked(d, (112, 104), "MACHINE LEARNING · SVD & LỌC CỘNG TÁC", F_MICRO,
            MUT + (255,), 1.5)
    paste_brand(base, W - 76, 62, size=84, p=p, alpha=0.95)


def an(base, t, pose, look, scale, x, y, p=1.0, talk=False):
    if p <= 0:
        return
    im = character.draw(t, pose, look, talk, scale)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
    base.alpha_composite(im, (int(x), int(y - im.height)))


def stat_tile(base, cx, cy, p, num, label, acc):
    if p <= 0:
        return
    im, pad = card_base(370, 84, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.text((pad + 24, pad + 42), num, font=F_STAT, fill=TXT + (255,), anchor="lm")
    d.text((pad + 156, pad + 44), label, font=F_STATL, fill=MUT + (255,), anchor="lm")
    blit(base, im, cx, cy, p, 12)


# ---------- cover ----------
_COV = None
_SCRIM = None
SHRINK_T = 10.0


def cover_big():
    global _COV
    if _COV is None:
        src = Image.open(IMG + "/anhbia.png").convert("RGB")
        _COV = ImageOps.fit(src, (int(W * 1.07), int(H * 1.07)), Image.LANCZOS)
    return _COV


def scrim():
    global _SCRIM
    if _SCRIM is None:
        sc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(sc)
        for i in range(380):
            y = 700 + i
            a = int(205 * (i / 380) ** 1.5)
            d.line([0, y, W, y], fill=(4, 8, 16, a))
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.ellipse([-360, 620, 1200, 1300], fill=(4, 8, 16, 175))
        gl = gl.filter(ImageFilter.GaussianBlur(100))
        sc.alpha_composite(gl)
        patch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pd = ImageDraw.Draw(patch)
        pd.rounded_rectangle([12, 828, 1015, 1046], 34, fill=(4, 8, 16, 150))
        patch = patch.filter(ImageFilter.GaussianBlur(46))
        sc.alpha_composite(patch)
        _SCRIM = sc
    return _SCRIM


def cover_frame(t):
    big = cover_big()
    bw, bh = big.size
    z = 1.0 + 0.035 * lin(t, 0.0, max(SHRINK_T, 0.1))
    cw, ch = int(W * 1.07 / z), int(H * 1.07 / z)
    cx = bw / 2 + 10 * math.sin(t * 0.25)
    cy = bh / 2 + 6 * math.cos(t * 0.21)
    x0 = int(max(0, min(bw - cw, cx - cw / 2)))
    y0 = int(max(0, min(bh - ch, cy - ch / 2)))
    return big.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR).convert("RGBA")


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
    put(pitch(W0, 0.85), 0.12, 0.18)
    put(PO, st.get("s01c1", 0.9) + 0.12, 0.07)
    put(TK, st.get("s01c1", 0.9) + 0.18, 0.04)
    put(pitch(W0, 1.0), SHRINK_T - 0.10, 0.13)
    put(PO, SHRINK_T + 0.55, 0.09)
    put(TK, SHRINK_T + 0.80, 0.045)
    if "s01c5" in st:
        for i in range(3):
            put(PO, st["s01c5"] + 0.12 + i * 0.28, 0.06)
            put(TK, st["s01c5"] + 0.36 + i * 0.28, 0.032)
    put(pitch(W0, 1.08), S02_START - 0.12, 0.12)
    put(PO, st["s02c1"] + 0.30, 0.08)
    if "s02c2" in st:
        put(pitch(W0, 1.16), st["s02c2"] - 0.12, 0.09)
        put(PO, st["s02c2"] + 0.22, 0.07)
    put(pitch(W0, 1.12), S03_START - 0.12, 0.12)
    for i in range(8):
        put(TK, S03_START + 0.32 + i * 0.08, 0.028)
    put(MK, st["s03c1"] + 0.80, 0.065)
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
    photo_card(base, "anhbia.png", 1378, 344, 640, 360,
               seg(t, 0.90, 1.55), CYAN, mode="cover", r=18)
    tb = 0.85
    p = seg(t, tb, tb + 0.70)
    if p > 0:
        a = int(255 * p)
        dy = int((1 - p) * 20)
        tracked(d, (112, 232 + dy), "BÀI GIẢNG · MACHINE LEARNING", F_MICRO,
                AMBER + (a,), 2.4)
        d.text((112, 302 + dy), "Thuật toán SVD", font=F_T1, fill=TXT + (a,), anchor="lm")
        d.text((112, 384 + dy), "và ứng dụng trong lọc cộng tác", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
        mp = seg(t, tb + 0.25, tb + 0.95)
        if mp > 0:
            draw_marker(d, 116, 430, 510, 430, mp, AMBER, 5, seed=3)
        chip(base, "Collaborative Filtering", VIOLET, 400, 474,
             seg(t, tb + 0.35, tb + 0.85), fsize=16)
    if "s01c5" in ST:
        for i, (acc, icon, label, sub) in enumerate(GOALS):
            bp = seg(t, ST["s01c5"] + 0.10 + i * 0.28, ST["s01c5"] + 0.45 + i * 0.28)
            bullet(base, 440, 556 + 76 * i, bp, acc, icon, label, sub)
    pose = "wave" if t < ST["s01c2"] else "present"
    an(base, t, pose, -1, 0.80, 1618, 1048, seg(t, 0.8, 1.4), is_talk(t))


def draw_s02(base, t):
    d = ImageDraw.Draw(base)
    left = 600
    p1 = seg(t, ST["s02c1"] + 0.22, ST["s02c1"] + 0.92)
    if "s02c2" in ST:
        p1 *= 1 - seg(t, ST["s02c2"] - 0.20, ST["s02c2"] + 0.25)
    photo_card(base, "7.jpg", left, 545, 860, 484, p1, CYAN, mode="contain")
    if "s02c2" in ST:
        p2 = seg(t, ST["s02c2"] + 0.05, ST["s02c2"] + 0.65)
        photo_card(base, "3.jpg", left, 545, 860, 484, p2, VIOLET, mode="contain")
    lp = seg(t, ST["s02c1"] + 0.25, ST["s02c1"] + 0.75)
    if lp > 0:
        label = "TRANG CHỦ"
        lc = AMBER
        if "s02c2" in ST and t >= ST["s02c2"]:
            label = "TRONG TRANG SẢN PHẨM"
            lc = VIOLET
        tracked(d, (188, 276), label, F_MICRO, lc + (255,), 2.2)
    note_p = max(p1, seg(t, ST["s02c2"] + 0.05, ST["s02c2"] + 0.65)) if "s02c2" in ST else p1
    if note_p > 0:
        draw_rich(d, (left, 815), "Ảnh minh họa giao diện · do người dùng cung cấp",
                  F_NOTE, MUT + (int(215 * note_p),), "mm")
    p = seg(t, S02_START + 0.15, S02_START + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (1120, 208), "THỰC TẾ", F_MICRO, AMBER + (a,), 2.4)
        d.text((1120, 252), "Gợi ý có mặt", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1120, 306), "khắp nơi", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1120, 362), "Từ trang chủ đến trang sản phẩm", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    chip(base, "Dành riêng cho bạn", CYAN, 1330, 448,
         seg(t, ST["s02c1"] + 0.25, ST["s02c1"] + 0.65), fsize=16)
    chip(base, "Có thể bạn cũng thích", VIOLET, 1330, 508,
         seg(t, ST["s02c1"] + 0.45, ST["s02c1"] + 0.85), fsize=16)
    chip(base, "Đúng người · đúng lúc", EMER, 1330, 568,
         seg(t, ST["s02c1"] + 0.65, ST["s02c1"] + 1.05), fsize=16)
    np_ = seg(t, ST["s02c1"] + 0.80, ST["s02c1"] + 1.20)
    if np_ > 0:
        lines = wrap_t("Đúng sản phẩm, trước khi người dùng phải tự tìm.", F_NOTE, 500)
        yy = 622
        for ln in lines:
            draw_rich(d, (1120, yy), ln, F_NOTE, MUT + (int(230 * np_),), "lm")
            yy += 26
    an(base, t, "present", -1, 0.68, 1650, 1048, 1.0, is_talk(t))


GRID_R, GRID_C, CELL, GAP = 8, 14, 54, 10
GX, GY = 112, 330
FILLED = {
    (0, 0): 5, (0, 1): 4, (0, 2): 5, (0, 8): 4,
    (1, 0): 5, (1, 2): 4, (1, 3): 3, (1, 9): 5,
    (2, 1): 4, (2, 2): 2, (2, 7): 5, (2, 12): 4,
    (3, 10): 4, (3, 11): 5,
    (4, 0): 3, (4, 5): 5, (4, 6): 4,
    (5, 3): 2, (5, 8): 5, (5, 13): 4,
    (6, 2): 4, (6, 9): 3,
    (7, 1): 5, (7, 4): 4, (7, 12): 5,
}
QCELL = (3, 9)


def draw_s03(base, t):
    d = ImageDraw.Draw(base)
    p = seg(t, S03_START + 0.15, S03_START + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (112, 206), "DỮ LIỆU THỰC TẾ", F_MICRO, AMBER + (a,), 2.4)
        d.text((112, 250), "Mỗi tương tác là một ô", font=F_T4, fill=TXT + (a,), anchor="lm")
        d.text((112, 304), "trong bảng người dùng – sản phẩm", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    for r in range(GRID_R):
        for c in range(GRID_C):
            i = r * GRID_C + c
            ap = seg(t, S03_START + 0.18 + min(i * 0.008, 0.90),
                     S03_START + 0.42 + min(i * 0.008, 0.90))
            if ap <= 0:
                continue
            x = GX + c * (CELL + GAP)
            y = GY + r * (CELL + GAP)
            box = [x, y, x + CELL, y + CELL]
            val = FILLED.get((r, c))
            if (r, c) == QCELL:
                d.rounded_rectangle(box, 10, fill=(52, 38, 16), outline=AMBER + (210,), width=2)
                d.text((x + CELL / 2, y + CELL / 2 - 1), "?", font=F_QM, fill=AMBER + (255,), anchor="mm")
            elif val:
                d.rounded_rectangle(box, 10, fill=(16, 40, 56), outline=CYAN + (150,), width=1)
                d.text((x + CELL / 2, y + CELL / 2), str(val), font=F_CELL, fill=CYAN + (240,), anchor="mm")
            else:
                d.rounded_rectangle(box, 10, fill=(23, 30, 45), outline=(48, 58, 78), width=1)
    qx = GX + QCELL[1] * (CELL + GAP) + CELL / 2
    qy = GY + QCELL[0] * (CELL + GAP) + CELL / 2
    if t >= ST["s03c1"] + 0.55:
        pul = 0.5 + 0.5 * math.sin(t * 3.0)
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        rr = 34 + 8 * pul
        gd.ellipse([qx - rr, qy - rr, qx + rr, qy + rr], outline=AMBER + (int(60 + 60 * pul),), width=2)
        base.alpha_composite(gl)
    mk = seg(t, ST["s03c1"] + 0.55, ST["s03c1"] + 1.15)
    if mk > 0:
        draw_marker_circle(d, qx, qy, 44, 44, mk, AMBER, 5, seed=4)
    rp = seg(t, S03_START + 0.20, S03_START + 0.70)
    stat_tile(base, 1270, 404, rp, "8 × 14", "người dùng × sản phẩm", CYAN)
    stat_tile(base, 1270, 490, seg(t, S03_START + 0.40, S03_START + 0.90),
              "≈ 80%", "ô còn trống", AMBER)
    lp = seg(t, S03_START + 0.60, S03_START + 1.00)
    if lp > 0:
        rows = ((CYAN, "Ô đã có đánh giá"), ((120, 136, 158), "Ô trống · chưa tương tác"),
                (AMBER, "Ô cần dự đoán"))
        for i, (col, text) in enumerate(rows):
            yy = 566 + i * 40
            d.ellipse([1082, yy - 6, 1094, yy + 6], fill=col + (255,))
            d.text((1108, yy), text, font=F_LEG, fill=TXT + (235,), anchor="lm")
    cp = seg(t, ST["s03c1"] + 0.25, ST["s03c1"] + 0.65)
    if cp > 0:
        chip(base, "Ma trận thưa · sparse", AMBER, 1300, 700, cp, fsize=15)
    an(base, t, "point_left", -1, 0.60, 1650, 1048, 1.0, is_talk(t))


def draw(t):
    base = bg_frame()
    live_grid(base, t)
    if t < S02_START:
        draw_s01(base, t)
    elif t < S03_START:
        draw_s02(base, t)
    else:
        draw_s03(base, t)
    if t >= SHRINK_T + 0.55:
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
    bus = build_sfx(ST, total)
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
    out = OUT + f"/svd_congB{TAG}.mp4"
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_congB{TAG}.m4a", "-c:v", "copy",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest", out])
    if r.returncode:
        print(r.stderr[-1200:])
        raise SystemExit("mux fail")
    return out


# ---------- sampler ----------
TERMS = [
    ("a01", "SVD."),
    ("a02", "S-V-D."),
    ("a03", "ét vê đê."),
    ("t01", "Singular Value Decomposition."),
    ("t02", "Collaborative Filtering."),
    ("t03", "Lọc cộng tác."),
    ("t04", "User-Item Matrix."),
    ("t05", "Ma trận người dùng, sản phẩm."),
    ("t06", "Latent factors."),
    ("t07", "Yếu tố tiềm ẩn."),
    ("t08", "U, Sigma, V chuyển vị."),
    ("t09", "R mũ bằng U con k, Sigma con k, V chuyển vị con k."),
    ("t10", "r mũ bằng mu, cộng b-u, cộng b-i, cộng q-i chuyển vị nhân p-u."),
    ("t11", "Top N."),
    ("t12", "RMSE."),
    ("t13", "MAE."),
    ("t14", "Cold Start."),
    ("t15", "Surprise."),
    ("t16", "scikit-surprise."),
    ("t17", "Flask."),
    ("t18", "Node.js."),
    ("t19", "AirPods."),
]


def sampler():
    import tts_vieneu
    d = OUT + "/sampler"
    os.makedirs(d, exist_ok=True)
    parts = []
    idx = []
    for sid, text in TERMS:
        p = f"{d}/{sid}.wav"
        tts_vieneu.synth(text, p)
        x = decode(p)
        parts.append(x)
        parts.append(np.zeros(int(0.30 * SR)))
        idx.append(f"{sid}\t{text}")
        print("SAMPLER", sid, f"{len(x)/SR:.2f}s", text, flush=True)
    with open(OUT + "/sampler_index.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(idx) + "\n")
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
    global S02_START, S03_START, ST, TALK, ACTIVE, TOTAL, SHRINK_T, HDR_T
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    synth_all(CUES)
    active = list(CUES)
    st, total, talk = build_tl(active)
    dropped = []
    for cid in ("s01c5", "s02c2"):
        if total > 45.5:
            active = [c for c in active if c["id"] != cid]
            dropped.append(cid)
            st, total, talk = build_tl(active)
    if dropped:
        print("BỎ", ",".join(dropped), f"để mẫu còn {total:.1f}s", flush=True)
    ST, TALK, ACTIVE, TOTAL = st, talk, active, total
    SHRINK_T = st["s01c3"] - 0.25
    HDR_T = SHRINK_T + 0.45
    s02 = [c for c in active if c["scene"] == 2]
    s03 = [c for c in active if c["scene"] == 3]
    S02_START = st[s02[0]["id"]] - 0.80
    S03_START = st[s03[0]["id"]] - 0.80
    words = sum(len(c["say"].split()) for c in active)
    print(f"WORD {words}  TOTAL {total:.2f}s  cues {len(active)}", flush=True)
    if "--stills" in sys.argv:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        picks = [("01_cover", 1.2), ("02_title", st["s01c4"] + 1.0),
                 ("03_goals", st.get("s01c5", st["s01c4"]) + 1.2),
                 ("04_photo_luma", st["s02c1"] + 1.2)]
        if "s02c2" in st:
            picks.append(("05_photo_carousel", st["s02c2"] + 1.2))
        picks.append(("06_grid", st["s03c1"] + 0.9))
        picks.append(("07_grid_marker", st["s03c1"] + 1.6))
        for name, tt in picks:
            draw(min(tt, total - 0.2)).convert("RGB").save(f"{sd}/{name}.png", quality=95)
            print("STILL", name, round(tt, 2), flush=True)
        return
    mix_audio(total)
    n = int(total * FPS)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 150 == 0:
            print("frame", k, "/", n, flush=True)
    out = encode(total)
    print("DONE", out, "frames", n, flush=True)
    sampler()


if __name__ == "__main__":
    if "--sampler" in sys.argv:
        os.makedirs(OUT, exist_ok=True)
        sampler()
    elif "--encode" in sys.argv:
        os.makedirs(OUT, exist_ok=True)
        synth_all(CUES)
        st, total, talk = build_tl(CUES)
        print("TOTAL", round(total, 2), flush=True)
        out = encode(total)
        print("DONE", out, flush=True)
    else:
        main()
