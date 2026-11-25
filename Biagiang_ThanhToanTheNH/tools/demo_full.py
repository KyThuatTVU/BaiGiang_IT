# -*- coding: utf-8 -*-
"""Bản đầy đủ ~7 phút — Tích hợp API thanh toán ngân hàng (12 cảnh, 102 cue).
Dùng: python demo_full.py            (render toàn bộ)
      python demo_full.py --stills   (ảnh tĩnh kiểm bố cục)
"""
import bisect, json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = r"D:\Edit\Kit"
os.environ.setdefault("PROJECT_ROOT", PROJECT)
sys.path.insert(0, KIT + "/tools")
from core import (W, H, FPS, FF, font, draw_marker, draw_marker_circle,
                  paste_brand, brand_watermark)
from demo20 import bg, shadow_card, blit, tracked, chip, decode, dur, seg, lin
from prep_icons import icon_rgba
import demo41 as S
import sfx, character

SR = sfx.SR
OUT = PROJECT + "/mau/full"
AUD = OUT + "/audio"
FR = OUT + "/frames"
TAG = "thanhtoan_full"
TARGET = 420.0

TXT = (236, 241, 249)
MUT = (148, 163, 184)
DIM = (100, 116, 139)
CYAN = (34, 211, 238)
EMER = (52, 211, 153)
AMBER = (245, 158, 11)
VIOLET = (139, 92, 246)
RED = (229, 72, 77)
BLUE = (96, 165, 250)


def C(c, a=255):
    return c[:3] + (a,)


def hx(c):
    return "#%02X%02X%02X" % c[:3]


# ---------- fonts ----------
M13 = font("JetBrainsMono-var.ttf", 13)
M14 = font("JetBrainsMono-var.ttf", 14)
M15 = font("JetBrainsMono-var.ttf", 15)
M16 = font("JetBrainsMono-var.ttf", 16)
M17 = font("JetBrainsMono-var.ttf", 17)
M18 = font("JetBrainsMono-var.ttf", 18)
M19 = font("JetBrainsMono-var.ttf", 19)
B15 = font("BeVietnamPro-Medium.ttf", 15)
B16 = font("BeVietnamPro-Regular.ttf", 16)
B17 = font("BeVietnamPro-Medium.ttf", 17)
B18 = font("BeVietnamPro-Regular.ttf", 18)
B20S = font("BeVietnamPro-SemiBold.ttf", 20)
B21S = font("BeVietnamPro-SemiBold.ttf", 21)
B22S = font("BeVietnamPro-SemiBold.ttf", 22)
B24R = font("BeVietnamPro-Regular.ttf", 24)
B24S = font("BeVietnamPro-SemiBold.ttf", 24)
B26S = font("BeVietnamPro-SemiBold.ttf", 26)
B28R = font("BeVietnamPro-Regular.ttf", 28)
B30S = font("BeVietnamPro-SemiBold.ttf", 30)
B34S = font("BeVietnamPro-SemiBold.ttf", 34)
B36B = font("BeVietnamPro-Bold.ttf", 36)
B42B = font("BeVietnamPro-Bold.ttf", 42)
B48B = font("BeVietnamPro-Bold.ttf", 48)
B60B = font("BeVietnamPro-Bold.ttf", 60)

_IC = {}


def ic(name, col):
    key = (name, col)
    if key not in _IC:
        _IC[key] = icon_rgba(name, col)
    return _IC[key]


_CH = {}


def chrome(w, h, r=22, border=(255, 255, 255, 40), fill=(22, 33, 57, 240)):
    key = (w, h, r, tuple(border), tuple(fill))
    if key not in _CH:
        _CH[key] = shadow_card(w, h, r, border=border, fill=fill)
    im, pad = _CH[key]
    return im.copy(), pad


_PIC = {}
_AR = {}
IMG = PROJECT + "/img"


def pic_w(name, h):
    if name not in _AR:
        with Image.open(IMG + "/" + name + ".jpg") as im:
            _AR[name] = im.width / im.height
    return int(round(h * _AR[name]))


def photo(name, w, h, r=22, mode="contain"):
    key = (name, w, h, r, mode)
    if key in _PIC:
        return _PIC[key]
    src = ImageOps.exif_transpose(Image.open(IMG + "/" + name + ".jpg")).convert("RGB")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if mode == "cover":
        im.paste(ImageOps.fit(src, (w, h), Image.LANCZOS), (0, 0))
    else:
        bg = ImageOps.fit(src, (w, h), Image.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(14))
        bg = Image.blend(bg, Image.new("RGB", (w, h), (12, 20, 36)), 0.5)
        sc = min(w / src.width, h / src.height)
        fg = src.resize((max(1, int(src.width * sc)), max(1, int(src.height * sc))), Image.LANCZOS)
        im.paste(bg, (0, 0))
        im.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    im.putalpha(mask)
    _PIC[key] = im
    return im


def photo_card(base, name, cx, cy, w, h, p, acc=AMBER, mode="contain", r=20, rise=14):
    if p <= 0:
        return
    if not w:
        w = pic_w(name, h)
    fw, fh = w + 16, h + 16
    im, pad = chrome(fw, fh, r + 8, C(acc, 100), (18, 27, 46, 240))
    im.alpha_composite(photo(name, w, h, r, mode), (pad + 8, pad + 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 7, pad + 7, pad + fw - 7, pad + fh - 7], r,
                        outline=(255, 255, 255, 120), width=1)
    d.line([pad + 26, pad + 1, pad + fw - 26, pad + 1], fill=C(acc, 175), width=2)
    blit(base, im, cx, cy, p, rise)


# ---------- script ----------
_D = json.load(open(PROJECT + "/tools/script.json", encoding="utf-8"))
SCENES = _D["scenes"]
CUES = [(c["id"], c["say"], float(c["pause"])) for sc in SCENES for c in sc["cues"]]
SAY = {c[0]: c[1] for c in CUES}
CUES_BY_SCENE = [[c["id"] for c in sc["cues"]] for sc in SCENES]
TAGS = ["PHẦN 01 · MỞ ĐẦU", "PHẦN 02 · KHÁI NIỆM", "PHẦN 03 · ĐIỀU KIỆN",
        "PHẦN 04 · NĂM NHÓM API", "PHẦN 05 · THÀNH PHẦN", "PHẦN 06 · LUỒNG 8 BƯỚC",
        "PHẦN 07 · RETURN URL", "PHẦN 08 · OAUTH", "PHẦN 09 · DATABASE",
        "PHẦN 10 · CODE", "PHẦN 11 · TRẠNG THÁI", "PHẦN 12 · TỔNG KẾT"]


# ---------- text helpers ----------
def wrap2(text, f, maxw=860):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or f.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def title(base, kicker, lines, acc, p, x=110, y=146, size=44, sub=None):
    if p <= 0:
        return
    hh = 44 + len(lines) * (size + 8) + (40 if sub else 0)
    im = Image.new("RGBA", (1240, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tracked(d, (2, 4), kicker, M15, C(acc), 3)
    yy = 34
    for ln in lines:
        d.text((0, yy), ln, font=font("BeVietnamPro-Bold.ttf", size), fill=C(TXT))
        yy += size + 8
    if sub:
        d.text((2, yy + 8), sub, font=B22S, fill=C(MUT))
    blit(base, im, x + 620, y + hh / 2, p, 14)


def caption_auto(base, text, p, dx=0):
    if p <= 0:
        return
    fs = 27
    for cand in (27, 25, 23, 21):
        f = font("BeVietnamPro-Medium.ttf", cand)
        lines = wrap2(text, f, 860)
        if len(lines) <= 2:
            fs = cand
            break
    w, h = 1020, 190
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 16
    d.rounded_rectangle([28, y + 8, 33, y + len(lines) * (fs + 9) + 12], 2, fill=C(VIOLET))
    for ln in lines:
        d.text((52, y), ln, font=f, fill=(226, 232, 240, 255))
        y += fs + 9
    blit(base, im, 60 + w / 2 + dx, 842 + h / 2, p, 6)


def header(base, t, tag):
    p = seg(t, 0.2, 0.9)
    if p <= 0:
        return
    bm = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bm)
    bd.rounded_rectangle([88, 62, 96, 110], 3, fill=C(AMBER))
    tracked(bd, (112, 78), "AN TECH ACADEMY", B22S, C(TXT), 2)
    tracked(bd, (112, 104), "TÍCH HỢP THANH TOÁN · API NGÂN HÀNG", M14, C(MUT), 2)
    tracked(bd, (1748, 78), tag, M14, C(MUT), 1, 1.0, "rm")
    blit(base, bm, W / 2, 70, p, 18)


def mini(base, cx, cy, w, h, p, acc, icon, kicker, ttl, sub=None, t=None,
         title_size=26):
    if p <= 0:
        return
    im, pad = chrome(w, h, 22, C(acc, 70), (22, 33, 57, 240))
    d = ImageDraw.Draw(im)
    pul = 0.5 + 0.5 * math.sin((t or 0) * 2.6)
    d.line([pad + 22, pad + 1, pad + w - 22, pad + 1], fill=C(acc, int(60 + 60 * pul)), width=2)
    tile = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, 47, 47], 13, fill=C(acc, 30), outline=C(acc, 110), width=1)
    ii = ic(icon, hx(acc)).resize((28, 28), Image.LANCZOS)
    tile.alpha_composite(ii, (10, 10))
    im.alpha_composite(tile, (pad + 20, pad + 18))
    tracked(d, (pad + 80, pad + 32), kicker, M14, C(acc), 2)
    d.text((pad + 20, pad + 70), ttl, font=font("BeVietnamPro-SemiBold.ttf", title_size), fill=C(TXT))
    if sub:
        d.text((pad + 20, pad + h - 40), sub, font=B16, fill=C(MUT))
    e = 1 - (1 - p) ** 3
    sc = 0.9 + 0.1 * e
    if abs(sc - 1) > 0.004:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx, cy, min(1.0, p * 1.5), 12)


def node_row(base, cx, cy, w, h, p, acc, icon, name, sub, t=None):
    mini(base, cx, cy, w, h, p, acc, icon, "", name, sub, t, 24)


def chip_row(base, items, y, p, gap=16, fs=16):
    if p <= 0:
        return
    widths = [int(M16.getlength(t)) + 52 for t, _, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = 960 - total / 2
    for (txt_, col, _), wd in zip(items, widths):
        chip(base, txt_, col, x + wd / 2, y, p, fs, 8, 1.0)
        x += wd + gap


# ---------- S01 hook ----------
def order_card(base, cx, cy, p, t):
    if p <= 0:
        return
    im, pad = chrome(460, 330, 24, C(AMBER, 80), (22, 33, 57, 242))
    d = ImageDraw.Draw(im)
    pul = 0.5 + 0.5 * math.sin(t * 2.8)
    d.line([pad + 24, pad + 1, pad + 460 - 24, pad + 1], fill=C(AMBER, int(80 + 60 * pul)), width=2)
    tracked(d, (pad + 26, pad + 30), "ĐƠN HÀNG #DH001", M16, C(MUT), 2)
    d.text((pad + 26, pad + 62), "Điện thoại thông minh", font=B30S, fill=C(TXT))
    d.text((pad + 26, pad + 104), "SP001 · số lượng 1", font=B18, fill=C(MUT))
    for xx in range(pad + 26, pad + 460 - 26, 14):
        d.line([xx, pad + 152, xx + 7, pad + 152], fill=(90, 105, 130, 180), width=1)
    d.text((pad + 26, pad + 182), "15.000.000đ", font=font("BeVietnamPro-Bold.ttf", 46), fill=C(AMBER))
    d.text((pad + 26, pad + 248), "TRẠNG THÁI", font=M14, fill=C(MUT))
    d.rounded_rectangle([pad + 26, pad + 274, pad + 26 + 246, pad + 274 + 44], 12,
                        fill=C(AMBER, int(26 + 16 * pul)), outline=C(AMBER, 210), width=2)
    d.ellipse([pad + 44, pad + 292, pad + 54, pad + 302], fill=C(AMBER))
    d.text((pad + 66, pad + 296), "CHỜ THANH TOÁN", font=B20S, fill=(253, 230, 200, 255), anchor="lm")
    blit(base, im, cx, cy, p, 16)


def bank_phone(base, cx, cy, p, t):
    if p <= 0:
        return
    im, pad = chrome(360, 420, 34, C(EMER, 80), (13, 21, 38, 248))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 22, pad + 20, pad + 338, pad + 400], 28,
                        fill=(10, 17, 30, 255), outline=C(EMER, 90), width=2)
    d.rounded_rectangle([pad + 46, pad + 54, pad + 314, pad + 150], 16,
                        fill=C(EMER, 22), outline=C(EMER, 80), width=1)
    tracked(d, (pad + 62, pad + 72), "BIẾN ĐỘNG SỐ DƯ", M13, C(EMER), 2)
    d.text((pad + 62, pad + 96), "+ 15.000.000 ₫", font=font("BeVietnamPro-Bold.ttf", 30), fill=C(EMER))
    d.text((pad + 46, pad + 176), "ỨNG DỤNG NGÂN HÀNG", font=M13, fill=C(MUT))
    d.text((pad + 46, pad + 208), "TK: 0123 456 789", font=M16, fill=C(TXT))
    d.text((pad + 46, pad + 240), "ND: DH001", font=M16, fill=C(TXT))
    d.text((pad + 46, pad + 272), "Số tiền: 15.000.000", font=M16, fill=C(TXT))
    pul = 0.5 + 0.5 * math.sin(t * 2.2)
    d.ellipse([pad + 46, pad + 320, pad + 58, pad + 332], fill=C(EMER, int(160 + 80 * pul)))
    d.text((pad + 70, pad + 326), "Đã nhận tiền", font=B18, fill=C(EMER), anchor="lm")
    blit(base, im, cx, cy, p, 16)


def s01(base, t, tl, durs, s0, s1):
    p = seg(t, 0.25, 1.0)
    title(base, "BÀI GIẢNG · THANH TOÁN TRỰC TUYẾN",
          ["Nối website bán hàng", "với ngân hàng"], AMBER, p, y=146, size=52)
    q = seg(t, 0.55, 1.25)
    if q > 0:
        ov = Image.new("RGBA", (W, 40), (0, 0, 0, 0))
        draw_marker(ImageDraw.Draw(ov), 108, 24, 468, 24, q, C(AMBER), 6, seed=3)
        base.alpha_composite(ov, (0, 292))

    q1 = seg(t, tl["s0101"] - 0.1, tl["s0101"] + 0.5)
    order_card(base, 430, 620, q1, t)
    q2 = seg(t, tl["s0102"] + 0.15, tl["s0102"] + 0.8)
    bank_phone(base, 1120, 600, q2, t)
    qp = seg(t, tl["s0101"] + 0.5, tl["s0101"] + 1.1)
    if qp > 0:
        photo_card(base, "16", 1515, 356, 484, 250, qp, AMBER, "contain")

    if tl["s0103"] <= t < tl["s0105"] + 0.5:
        a = seg(t, tl["s0103"], tl["s0103"] + 0.4) * (1 - seg(t, tl["s0105"], tl["s0105"] + 0.4))
        qm = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
        dq = ImageDraw.Draw(qm)
        dq.text((110, 104), "?", font=font("BeVietnamPro-Bold.ttf", 120),
                fill=C(AMBER, int(200 * a)), anchor="mm")
        base.alpha_composite(qm, (820, 410))
    if tl["s0103"] <= t < tl["s0104"] + durs["s0104"]:
        tc = seg(t, tl["s0103"] + 0.55, tl["s0103"] + 0.9)
        if tc > 0:
            draw_marker_circle(ImageDraw.Draw(base), 335, 756, 140, 32, tc, C(AMBER), 4)
    if tl["s0104"] <= t < tl["s0104"] + durs["s0104"] + 0.4:
        qc = seg(t, tl["s0104"] + 0.35, tl["s0104"] + 0.8)
        chip(base, "dò từng giao dịch mỗi ngày", RED, 1120, 852, qc, 16, 8, 1.0)
    q3 = seg(t, tl["s0106"] - 0.1, tl["s0106"] + 0.35)
    chip_row(base, [("Node.js · Express", EMER, 0), ("MySQL", CYAN, 0),
                    ("Webhook · IPN", AMBER, 0)], 700, q3, gap=18)
    q4 = seg(t, tl["s0107"] - 0.1, tl["s0107"] + 0.4)
    if q4 > 0:
        chip(base, "chống xử lý trùng · đối soát", VIOLET, 960, 770, q4, 16, 8, 1.0)


# ---------- S02 definition ----------
def s02(base, t, tl, durs, s0, s1):
    p = seg(t, s0, s0 + 0.6)
    title(base, "ĐỊNH NGHĨA", ["API ngân hàng là gì?"], CYAN, p, y=130, size=44)
    qd = seg(t, tl["s0201"] - 0.1, tl["s0201"] + 0.45)
    if qd > 0:
        w = 1040
        im = Image.new("RGBA", (w, 92), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, 91], 20, fill=(20, 31, 54, 242), outline=C(CYAN, 90), width=2)
        d.text((30, 46), "Giao diện lập trình do ngân hàng cung cấp", font=B30S, fill=C(TXT), anchor="lm")
        blit(base, im, 960, 290, qd, 14)
        qm = seg(t, tl["s0201"] + 0.5, tl["s0201"] + 0.9)
        if qm > 0:
            ov = Image.new("RGBA", (W, 24), (0, 0, 0, 0))
            draw_marker(ImageDraw.Draw(ov), 452, 12, 712, 12, qm, C(CYAN), 5, seed=5)
            base.alpha_composite(ov, (0, 310))
    # 3-node diagram
    q1 = seg(t, tl["s0201"] + 0.2, tl["s0201"] + 0.7)
    q2 = seg(t, tl["s0202"], tl["s0202"] + 0.5)
    node_row(base, 330, 470, 340, 180, q1, CYAN, "monitor", "Website", "bán hàng")
    node_row(base, 960, 470, 300, 165, q1, VIOLET, "layers", "API", "ngân hàng")
    node_row(base, 1590, 470, 340, 180, q2, EMER, "building-2", "Ngân hàng", "xử lý giao dịch")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ql = seg(t, tl["s0202"], tl["s0202"] + 0.5)
    qr = seg(t, tl["s0202"] + 0.2, tl["s0202"] + 0.7)
    S.beam(d, 512, 800, 470, ql, CYAN, VIOLET, t)
    S.beam(d, 1120, 1410, 470, qr, VIOLET, EMER, t)
    if ql > 0.95:
        S.packets(d, 520, 790, 470, t, CYAN)
    if qr > 0.95:
        S.packets(d, 1130, 1400, 470, t + 0.4, EMER)
    base.alpha_composite(ov)

    # comparison cards
    ql2 = seg(t, tl["s0204"] - 0.15, tl["s0204"] + 0.5)
    qr2 = seg(t, tl["s0206"] - 0.15, tl["s0206"] + 0.5)
    if ql2 > 0:
        im, pad = chrome(600, 240, 24, C(RED, 60), (20, 28, 48, 238))
        d = ImageDraw.Draw(im)
        tracked(d, (pad + 22, pad + 28), "CHƯA TÍCH HỢP", M15, C(RED), 2)
        steps = ["Nhân viên", "App ngân hàng", "Đối chiếu", "Website"]
        act = int(max(0, min(3, (t - tl["s0204"]) / max(0.4, durs["s0204"] / 4))))
        for i, st in enumerate(steps):
            yy = pad + 62 + i * 38
            on = ql2 > 0.9 and i <= act
            d.text((pad + 22, yy), "→" if i else "•", font=M18, fill=C(RED, 220 if on else 110))
            d.text((pad + 52, yy), st, font=B18, fill=C(TXT if on else MUT))
        qx = seg(t, tl["s0205"] + 0.2, tl["s0205"] + 0.7)
        if qx > 0:
            d.text((pad + 400, pad + 26), "×", font=font("BeVietnamPro-Bold.ttf", 46), fill=C(RED, 220))
            d.text((pad + 388, pad + 188), "chậm · thủ công", font=B16, fill=C(RED, 210))
        blit(base, im, 430, 716, ql2, 14)
    if qr2 > 0:
        im, pad = chrome(600, 240, 24, C(EMER, 70), (20, 32, 48, 238))
        d = ImageDraw.Draw(im)
        tracked(d, (pad + 22, pad + 28), "ĐÃ TÍCH HỢP", M15, C(EMER), 2)
        d.text((pad + 22, pad + 60), "Frontend → Backend → Bank API", font=M17, fill=C(TXT))
        d.text((pad + 22, pad + 96), "Webhook → Database", font=M17, fill=C(TXT))
        qp = seg(t, tl["s0206"] + 0.5, tl["s0207"])
        if qp > 0:
            d.text((pad + 22, pad + 140), "15.000.000đ · PENDING → PAID", font=M17, fill=C(AMBER, 240))
        qv = seg(t, tl["s0207"] + 0.1, tl["s0207"] + 0.5)
        if qv > 0:
            d.text((pad + 22, pad + 176), "xác minh rồi mới cập nhật", font=B17, fill=C(EMER))
        blit(base, im, 1280, 716, qr2, 14)
    qa = seg(t, tl["s0208"] + 0.1, tl["s0208"] + 0.5)
    if qa > 0:
        chip(base, "tự động hóa · đồng bộ dữ liệu", EMER, 960, 790, qa, 16, 8, 1.0)
    qn = seg(t, tl["s0209"] + 0.1, tl["s0209"] + 0.5)
    if qn > 0:
        chip(base, "100+ đơn / ngày", AMBER, 1520, 790, qn, 16, 8, 1.0)


# ---------- S03 conditions ----------
def s03(base, t, tl, durs, s0, s1):
    title(base, "ĐIỀU KIỆN CẤP API", ["Mở tài khoản chưa đủ"], AMBER,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    steps = [("01", "Tài khoản", "doanh nghiệp"), ("02", "Đăng ký", "dịch vụ"),
             ("03", "Hợp đồng", "& xác minh"), ("04", "Sandbox", "· UAT"),
             ("05", "Production", "chính thức")]
    for i, (no, l1, l2) in enumerate(steps):
        cx = 250 + i * 355
        q = seg(t, tl["s0301"] + 0.2 + i * 0.28, tl["s0301"] + 0.6 + i * 0.28)
        if q <= 0:
            continue
        im, pad = chrome(300, 140, 20, C(AMBER if i == 3 else CYAN, 65), (20, 31, 54, 238))
        d = ImageDraw.Draw(im)
        d.text((pad + 20, pad + 16), no, font=M15, fill=C(AMBER))
        d.text((pad + 20, pad + 46), l1, font=B24S, fill=C(TXT))
        d.text((pad + 20, pad + 80), l2, font=B18, fill=C(MUT))
        if i < 4 and t >= tl["s0302"] + i * 0.3:
            d.line([pad + 244, pad + 30, pad + 251, pad + 37, pad + 264, pad + 18],
                   fill=C(EMER), width=3, joint="curve")
        blit(base, im, cx, 360, q, 12)
        if i < 4:
            qa = seg(t, tl["s0302"] + i * 0.3, tl["s0302"] + 0.65 + i * 0.3)
            if qa > 0:
                ov = Image.new("RGBA", (W, 20), (0, 0, 0, 0))
                S.beam(ImageDraw.Draw(ov), cx + 158, cx + 202, 10, qa, AMBER, AMBER, t)
                base.alpha_composite(ov, (0, 350))
    # credentials
    qc = seg(t, tl["s0305"] - 0.1, tl["s0305"] + 0.5)
    if qc > 0:
        im, pad = chrome(780, 268, 24, C(VIOLET, 75), (20, 30, 54, 242))
        d = ImageDraw.Draw(im)
        tracked(d, (pad + 24, pad + 28), "BỘ THÔNG TIN TÍCH HỢP", M15, C(VIOLET), 2)
        rows = [("CLIENT ID", "merchant_abc_001"), ("CLIENT SECRET", "••••••••••"),
                ("SIGNING KEY", "merchant-private-key.pem"), ("MERCHANT ID", "MERCHANT_001")]
        for i, (k, v) in enumerate(rows):
            yy = pad + 64 + i * 44
            d.text((pad + 24, yy), k, font=M14, fill=C(MUT))
            d.text((pad + 210, yy), v, font=M16, fill=C(TXT))
            d.line([pad + 24, yy + 30, pad + 756, yy + 30], fill=(90, 105, 130, 80), width=1)
        ql = seg(t, tl["s0308"] - 0.05, tl["s0308"] + 0.45)
        if ql > 0:
            d.rounded_rectangle([pad + 560, pad + 18, pad + 750, pad + 54], 10,
                                fill=C(AMBER, int(40 * ql)), outline=C(AMBER, 220), width=2)
            d.text((pad + 655, pad + 36), "CHỈ BACKEND", font=M14, fill=C(AMBER), anchor="mm")
        blit(base, im, 560, 690, qc, 14)
        qmk = seg(t, tl["s0308"] + 0.2, tl["s0308"] + 0.65)
        if qmk > 0:
            ov = Image.new("RGBA", (W, 26), (0, 0, 0, 0))
            draw_marker(ImageDraw.Draw(ov), 736, 14, 930, 14, qmk, C(AMBER), 5, seed=7)
            base.alpha_composite(ov, (0, 640))
    # browser card
    qb = seg(t, tl["s0307"] - 0.1, tl["s0307"] + 0.5)
    if qb > 0:
        im, pad = chrome(380, 228, 22, C(RED, 70), (26, 24, 38, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 22), "JavaScript · trình duyệt", font=B20S, fill=C(TXT))
        d.text((pad + 22, pad + 58), "client thấy được mọi thứ", font=B16, fill=C(MUT))
        d.text((pad + 22, pad + 96), "CLIENT SECRET", font=M16, fill=C(RED))
        d.text((pad + 22, pad + 126), "API KEY", font=M16, fill=C(RED))
        qx = seg(t, tl["s0307"] + 0.5, tl["s0307"] + 0.9)
        if qx > 0:
            for yy in (130, 160):
                d.line([pad + 20, yy, pad + 20 + 250 * qx, yy], fill=C(RED, 230), width=3)
            d.text((pad + 276, pad + 112), "×", font=font("BeVietnamPro-Bold.ttf", 38),
                   fill=C(RED, int(230 * qx)))
        blit(base, im, 1400, 690, qb, 14)
    if tl["s0309"] <= t:
        chip(base, "mỗi ngân hàng một bộ tài liệu", VIOLET, 960, 860 - 40,
             seg(t, tl["s0309"], tl["s0309"] + 0.5), 15, 8, 1.0)


# ---------- S04 five groups ----------
GROUPS = [("credit-card", "Payment Gateway", "tạo giao dịch · chuyển trang thanh toán"),
          ("scan", "QR Payment", "sinh mã QR theo số tiền · mã đơn"),
          ("message-circle", "Transaction Notification", "thông báo biến động số dư"),
          ("wallet", "Virtual Account", "tài khoản định danh từng đơn"),
          ("banknote", "Transfer API", "chi hộ theo quyền được cấp")]


def s04(base, t, tl, durs, s0, s1):
    title(base, "NĂM NHÓM API NGÂN HÀNG", ["Chọn theo nhu cầu"], CYAN,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    starts = [tl[f"s040{i}"] for i in (1, 2, 3, 4, 5, 6)]
    for i, (icon, name, sub) in enumerate(GROUPS):
        cx = 250 + i * 355
        q = seg(t, starts[0] + 0.2, starts[0] + 0.6)
        if q <= 0:
            continue
        active = 0.0
        if i > 0:
            a0 = starts[i + 1]
            active = seg(t, a0, a0 + 0.3) * (1 - seg(t, starts[i + 2] if i < 4 else tl["s0407"], starts[i + 2] + 0.3 if i < 4 else tl["s0407"] + 0.3))
            q = max(q, seg(t, a0, a0 + 0.35))
        border = C(AMBER if active > 0.4 else CYAN, 90 + int(120 * active))
        im, pad = chrome(320, 230, 22, border, (20, 31, 54, 240))
        d = ImageDraw.Draw(im)
        tile = Image.new("RGBA", (54, 54), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        col = AMBER if active > 0.4 else CYAN
        td.rounded_rectangle([0, 0, 53, 53], 15, fill=C(col, 32), outline=C(col, 120), width=1)
        ii = ic(icon, hx(col)).resize((32, 32), Image.LANCZOS)
        tile.alpha_composite(ii, (11, 11))
        im.alpha_composite(tile, (pad + 22, pad + 20))
        tracked(d, (pad + 88, pad + 40), "NHÓM %d" % (i + 1), M14, C(col), 2)
        lines = wrap2(name, B24S, 276)
        for j, ln in enumerate(lines):
            d.text((pad + 22, pad + 90 + j * 30), ln, font=B24S, fill=C(TXT))
        sd = wrap2(sub, B15, 276)
        for j, ln in enumerate(sd[:2]):
            d.text((pad + 22, pad + 158 + j * 20), ln, font=B15, fill=C(MUT))
        blit(base, im, cx, 400, q, 12)

    for i, nm in enumerate(("12", "31", "23", "20", "8")):
        a0 = starts[i + 1] + 0.1
        b0 = starts[i + 2] if i < 4 else tl["s0407"]
        q = seg(t, a0, a0 + 0.45) * (1 - seg(t, b0 - 0.05, b0 + 0.25))
        if q > 0:
            photo_card(base, nm, 960, 668, None, 268, q, AMBER, "contain")

    qw = seg(t, tl["s0407"] - 0.1, tl["s0407"] + 0.45)
    if qw > 0:
        im, pad = chrome(980, 168, 24, C(RED, 80), (28, 24, 36, 244))
        d = ImageDraw.Draw(im)
        d.text((pad + 28, pad + 24), "QR ≠ XÁC NHẬN THANH TOÁN", font=B36B, fill=C(TXT))
        d.text((pad + 28, pad + 78), "Tạo được mã QR không có nghĩa là khách đã trả tiền.",
               font=B20S, fill=C(MUT))
        d.text((pad + 28, pad + 114), "Cần thông báo giao dịch hoặc đối soát.", font=B18,
               fill=C(AMBER))
        blit(base, im, 960, 640, qw, 14)
        qn = seg(t, tl["s0407"] + 0.4, tl["s0407"] + 0.9)
        if qn > 0:
            draw_marker_circle(ImageDraw.Draw(base), 581, 603, 36, 30, qn, C(AMBER), 4)
    qa = seg(t, tl["s0408"] + 0.1, tl["s0408"] + 0.5)
    if qa > 0:
        S.beam(ImageDraw.Draw(base), 1452, 1473, 640, qa, AMBER, EMER, t)
        chip(base, "Thông báo · Đối soát", EMER, 1590, 640, qa, 16, 8, 1.0)
    qe = seg(t, tl["s0409"] + 0.1, tl["s0409"] + 0.45)
    if qe > 0:
        chip(base, "đừng chỉ nhìn vào tên gọi", VIOLET, 960, 810, qe, 15, 8, 1.0)


# ---------- S05 components ----------
def s05(base, t, tl, durs, s0, s1):
    title(base, "NĂM THÀNH PHẦN HỆ THỐNG", ["Backend là trung tâm"], VIOLET,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    nodes = [("user", "Customer", "người mua"), ("monitor", "Frontend", "giao diện web"),
             ("server", "Backend", "nghiệp vụ đơn"), ("building-2", "Bank API", "cổng ngân hàng"),
             ("database", "Database", "đơn & giao dịch")]
    xs = [220, 570, 960, 1350, 1700]
    q0 = seg(t, tl["s0501"] + 0.2, tl["s0501"] + 0.6)
    for i, (icon, name, sub) in enumerate(nodes):
        q = max(q0, seg(t, tl[f"s050{i + 2}"] - 0.1, tl[f"s050{i + 2}"] + 0.3))
        if q <= 0:
            continue
        col = VIOLET if i == 2 else CYAN
        mini(base, xs[i], 430, 270, 180, q, col, icon, "", name, sub, t, 24)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    qc1 = seg(t, tl["s0502"], tl["s0502"] + 0.4)
    qc2 = seg(t, tl["s0503"], tl["s0503"] + 0.4)
    qc3 = seg(t, tl["s0504"], tl["s0504"] + 0.4)
    qc4 = seg(t, tl["s0505"], tl["s0505"] + 0.4)
    qc5 = seg(t, tl["s0506"], tl["s0506"] + 0.4)
    S.beam(d, 358, 432, 430, qc1, CYAN, CYAN, t)
    S.beam(d, 708, 822, 430, qc2, CYAN, VIOLET, t)
    S.beam(d, 1098, 1212, 430, qc3, VIOLET, EMER, t)
    # Backend - Database (bottom arc)
    if qc5 > 0.1:
        d.line([960, 522, 960, 530], fill=C(CYAN, 200), width=2)
        qq = qc5
        d.line([960, 530, 960, 530 + 70 * min(1, qq * 3)], fill=C(CYAN, 200), width=2)
        if qq > 0.33:
            d.line([960, 600, 960 + (1700 - 960) * min(1, (qq - 0.33) * 3), 600],
                   fill=C(CYAN, 200), width=2)
        if qq > 0.66:
            y0 = 600 + (522 - 600) * ((qq - 0.66) / 0.34)
            d.line([1700, 600, 1700, y0], fill=C(CYAN, 200), width=2)
    if qc3 > 0.9:
        S.packets(d, 1100, 1205, 430, t, EMER)
    base.alpha_composite(ov)
    qph = seg(t, tl["s0501"] + 0.5, tl["s0501"] + 1.05)
    if qph > 0:
        photo_card(base, "6", 1340, 760, None, 300, qph, VIOLET, "contain")
    ql = seg(t, tl["s0507"] - 0.1, tl["s0507"] + 0.4)
    if ql > 0:
        pul = 0.5 + 0.5 * math.sin(t * 2.6)
        d = ImageDraw.Draw(base)
        d.rounded_rectangle([960 - 158, 430 - 108, 960 + 158, 430 + 108], 26,
                            outline=C(AMBER, int(120 + 80 * pul * ql)), width=3)
        chip(base, "chỉ Backend gọi ngân hàng", AMBER, 1110, 296, ql, 15, 8, 1.0)
        chip(base, "Backend = trung tâm", AMBER, 960, 648, ql, 16, 8, 1.0)


# ---------- S06 eight steps ----------
STEPS = ["Đặt hàng", "Tính tiền", "Lưu đơn", "Gọi bank", "Nhận URL", "Khách trả", "Webhook", "Cập nhật"]


def rail(base, t, tl):
    y = 196
    d = ImageDraw.Draw(base)
    d.line([150, y, 150 + 231.4 * 7, y], fill=(120, 140, 170, 90), width=2)
    cur = 0
    # active step derived from cue starts
    starts = [tl["s0602"], tl["s0603"], tl["s0605"], tl["s0606"], tl["s0607"],
              tl["s0608"], tl["s0609"], tl["s0611"]]
    for i in range(7, -1, -1):
        if t >= starts[i]:
            cur = i
            break
    for i in range(8):
        cx = 150 + 231.4 * i
        done = i < cur
        active = i == cur
        col = EMER if done else (AMBER if active else (90, 105, 130))
        if done:
            d.ellipse([cx - 17, y - 17, cx + 17, y + 17], fill=C(EMER, 235))
            d.line([cx - 7, y, cx - 1, y + 7, cx + 9, y - 7], fill=(8, 14, 24, 255), width=3)
        else:
            d.ellipse([cx - 17, y - 17, cx + 17, y + 17], fill=(14, 22, 40, 240),
                      outline=C(col, 200 if active else 110), width=2)
            d.text((cx, y), str(i + 1), font=M15, fill=C(col), anchor="mm")
        d.text((cx, y + 40), STEPS[i], font=B16, fill=C(TXT if active else MUT), anchor="mm")


def s06(base, t, tl, durs, s0, s1):
    tracked(ImageDraw.Draw(base), (110, 150), "LUỒNG THANH TOÁN · 8 BƯỚC", M15, C(AMBER), 3)
    rail(base, t, tl)
    bB, bC, bD = tl["s0603"], tl["s0606"], tl["s0609"]

    def fade_out(b):
        return 1 - seg(t, b, b + 0.35)

    # A: step 1
    if t < bB + 0.35:
        p = seg(t, tl["s0601"] + 0.2, tl["s0601"] + 0.7) * fade_out(bB)
        if p > 0:
            im, pad = chrome(440, 300, 24, C(CYAN, 70), (22, 33, 57, 242))
            d = ImageDraw.Draw(im)
            tracked(d, (pad + 24, pad + 26), "01 · FRONTEND", M14, C(CYAN), 2)
            d.text((pad + 24, pad + 58), "Gửi yêu cầu đặt hàng", font=B26S, fill=C(TXT))
            d.rounded_rectangle([pad + 24, pad + 112, pad + 416, pad + 252], 14,
                                fill=(12, 19, 34, 245), outline=C(CYAN, 90), width=1)
            d.text((pad + 44, pad + 132), "POST /api/orders", font=M17, fill=C(EMER))
            d.text((pad + 44, pad + 166), '{ "items": [', font=M17, fill=C(TXT))
            d.text((pad + 44, pad + 192), '    { "id": "SP001", "qty": 1 }', font=M15, fill=C(TXT))
            d.text((pad + 44, pad + 218), '] }', font=M17, fill=C(TXT))
            blit(base, im, 960, 560, p, 14)
        qm = seg(t, tl["s0602"] + 0.4, tl["s0602"] + 0.8)
        if qm > 0:
            draw_marker_circle(ImageDraw.Draw(base), 960, 636, 250, 62, qm, C(AMBER), 4)

    # B: step 2-3
    if bB <= t < bC + 0.35:
        pa = seg(t, bB, bB + 0.4) * fade_out(bC)
        pb = seg(t, bB + 0.15, bB + 0.55) * fade_out(bC)
        pc = seg(t, tl["s0605"] - 0.1, tl["s0605"] + 0.3) * fade_out(bC)
        if pa > 0:
            mini(base, 330, 570, 340, 280, pa, CYAN, "monitor", "01 · FRONTEND", "Gửi yêu cầu", None, t, 24)
            d = ImageDraw.Draw(base)
            d.text((230, 690), '{ "total": 9000000 }', font=M15, fill=C(MUT))
            d.text((230, 716), "client sửa được", font=B15, fill=C(RED))
        if pb > 0:
            im, pad = chrome(420, 300, 24, C(VIOLET, 75), (22, 33, 57, 242))
            d = ImageDraw.Draw(im)
            tracked(d, (pad + 24, pad + 26), "02 · BACKEND", M14, C(VIOLET), 2)
            d.text((pad + 24, pad + 58), "Tính lại từ Database", font=B26S, fill=C(TXT))
            d.text((pad + 24, pad + 112), "SELECT price, qty", font=M17, fill=C(CYAN))
            d.text((pad + 24, pad + 140), "FROM order_items", font=M17, fill=C(CYAN))
            d.text((pad + 24, pad + 178), "15.000.000đ", font=font("BeVietnamPro-Bold.ttf", 40), fill=C(AMBER))
            blit(base, im, 960, 560, pb, 14)
        if pc > 0:
            mini(base, 1500, 540, 310, 250, pc, EMER, "receipt", "03 · ORDERS", "Lưu đơn", None, t, 24)
            S.status_pill(base, 1500, 636, "PENDING_PAYMENT", AMBER, pc, 15, False, 0.5)
        qm = seg(t, tl["s0603"] + 0.45, tl["s0603"] + 0.85)
        if qm > 0:
            draw_marker_circle(ImageDraw.Draw(base), 960, 636, 190, 58, qm * fade_out(bC), C(AMBER), 4)
        qx = seg(t, tl["s0604"] + 0.3, tl["s0604"] + 0.7)
        if qx > 0:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.line([232, 703, 232 + 178 * qx, 703], fill=C(RED, 220), width=4)
            base.alpha_composite(ov)
            chip(base, "nguồn tin cậy · DB", EMER, 960, 740, qx * fade_out(bC), 15, 8, 1.0)

    # C: step 4-6
    if bC <= t < bD + 0.35:
        p1 = seg(t, bC, bC + 0.45) * fade_out(bD)
        p2 = seg(t, bC + 0.15, bC + 0.6) * fade_out(bD)
        mini(base, 330, 540, 360, 240, p1, CYAN, "building-2", "NGÂN HÀNG", "Tạo giao dịch", "POST /payments", t, 24)
        mini(base, 960, 540, 400, 240, p2, VIOLET, "server", "BACKEND", "Gửi yêu cầu", "orderId · amount · returnUrl", t, 24)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        ql = seg(t, bC + 0.4, bC + 0.8) * fade_out(bD)
        S.beam(d, 522, 748, 540, ql, CYAN, VIOLET, t)
        qr = seg(t, tl["s0607"] - 0.1, tl["s0607"] + 0.35) * fade_out(bD)
        S.beam(d, 1170, 1250, 540, qr, VIOLET, EMER, t)
        base.alpha_composite(ov)
        if qr > 0:
            chip(base, "payment URL · QR", EMER, 1380, 500, qr, 15, 8, 1.0)
        qphone = seg(t, tl["s0608"] - 0.1, tl["s0608"] + 0.4) * fade_out(bD)
        if qphone > 0:
            photo_card(base, "3", 1470, 556, 420, 286, qphone, EMER, "cover")
        qh = seg(t, tl["s0608"] + 0.5, tl["s0608"] + 0.9) * fade_out(bD)
        if qh > 0:
            chip(base, "xác thực trong app ngân hàng", EMER, 960, 760, qh, 15, 8, 1.0)

    # D: step 7-8 + failure
    if t >= bD:
        p = seg(t, bD, bD + 0.5)
        mini(base, 330, 470, 360, 240, p, CYAN, "building-2", "NGÂN HÀNG", "Gọi Webhook", "POST /webhooks/bank", t, 24)
        mini(base, 1000, 470, 400, 240, p, VIOLET, "server", "BACKEND", "/webhooks/bank", "xác minh chữ ký rồi cập nhật", t, 24)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        ql = seg(t, bD + 0.3, bD + 0.7)
        S.beam(d, 522, 788, 470, ql, CYAN, VIOLET, t)
        if ql > 0.95:
            S.packets(d, 530, 780, 470, t, CYAN)
        base.alpha_composite(ov)
        chip(base, "webhook", CYAN, 660, 420, ql, 15, 8, 1.0)
        # checklist
        qc = seg(t, tl["s0610"] - 0.1, tl["s0610"] + 0.3)
        if qc > 0:
            im, pad = chrome(390, 360, 24, C(EMER, 75), (22, 33, 57, 242))
            d = ImageDraw.Draw(im)
            tracked(d, (pad + 24, pad + 26), "XÁC MINH", M14, C(EMER), 2)
            d.text((pad + 24, pad + 56), "Kiểm tra", font=B28R, fill=C(TXT))
            rows = [("Chữ ký HMAC", 0.28), ("Mã giao dịch khớp", 0.48),
                    ("Số tiền khớp", 0.68), ("FOR UPDATE · transaction", 0.86)]
            dd = durs["s0610"]
            for i, (txt_, fr) in enumerate(rows):
                on = t >= tl["s0610"] + dd * fr
                y0 = pad + 104 + i * 38
                d.ellipse([pad + 26, y0 + 8, pad + 36, y0 + 18],
                          outline=C(EMER if on else MUT, 220), width=2)
                if on:
                    d.line([pad + 28, y0 + 13, pad + 31, y0 + 16, pad + 35, y0 + 9],
                           fill=C(EMER), width=2)
                d.text((pad + 50, y0), txt_, font=B17, fill=C(TXT if on else MUT))
            blit(base, im, 1490, 470, qc, 14)
        # pipeline
        qp = seg(t, tl["s0611"] - 0.1, tl["s0611"] + 0.3)
        if qp > 0:
            S.status_pill(base, 500, 760, "PENDING_PAYMENT", AMBER, qp, 16, False, 0.3)
            q3 = seg(t, tl["s0611"] + 0.35, tl["s0611"] + 0.7)
            if q3 > 0:
                S.status_pill(base, 830, 760, "PAID", EMER, q3, 16, True, 0.8)
                S.beam(ImageDraw.Draw(base), 660, 745, 760, q3, AMBER, EMER)
            q4 = seg(t, tl["s0611"] + 0.7, tl["s0611"] + 1.05)
            if q4 > 0:
                S.status_pill(base, 1190, 760, "PROCESSING", CYAN, q4, 16, False, 0.6)
                S.beam(ImageDraw.Draw(base), 920, 1080, 760, q4, EMER, CYAN)
        qx = seg(t, tl["s0612"] + 0.1, tl["s0612"] + 0.45)
        if qx > 0:
            chip(base, "✕ sai bước 7 → không cập nhật", RED, 1420, 700, qx, 15, 8, 1.0)


# ---------- S07 return url vs webhook ----------
def s07(base, t, tl, durs, s0, s1):
    title(base, "HAI KHÁI NIỆM DỄ NHẦM", ["Return URL và Webhook"], AMBER,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    p1 = seg(t, tl["s0701"] + 0.2, tl["s0701"] + 0.7)
    p2 = seg(t, tl["s0704"] - 0.1, tl["s0704"] + 0.4)
    # lane 1
    mini(base, 300, 390, 300, 180, p1, AMBER, "monitor", "TRÌNH DUYỆT", "Khách hàng", None, t, 24)
    mini(base, 1450, 390, 300, 180, p1, AMBER, "globe", "WEBSITE", "Return URL", None, t, 24)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    q1 = seg(t, tl["s0702"] - 0.05, tl["s0702"] + 0.4)
    S.beam(d, 462, 1262, 390, q1, AMBER, AMBER, t)
    if q1 > 0.95:
        S.packets(d, 470, 1255, 390, t, AMBER)
    # lane 2
    q2 = seg(t, tl["s0704"] + 0.3, tl["s0704"] + 0.7)
    S.beam(d, 462, 1262, 650, q2, VIOLET, VIOLET, t)
    if q2 > 0.95:
        S.packets(d, 470, 1255, 650, t + 0.6, VIOLET)
    base.alpha_composite(ov)
    mini(base, 300, 650, 300, 180, p2, VIOLET, "building-2", "BANK SERVER", "Ngân hàng", None, t, 24)
    mini(base, 1450, 650, 300, 180, p2, VIOLET, "server", "BACKEND", "doanh nghiệp", None, t, 24)
    chip(base, "Return URL", AMBER, 900, 330, q1, 16, 8, 1.0)
    chip(base, "chỉ hiển thị kết quả", AMBER, 900, 455, q1, 15, 8, 1.0)
    chip(base, "Webhook / IPN", VIOLET, 900, 590, q2, 16, 8, 1.0)
    ql = seg(t, tl["s0704"] + 0.6, tl["s0704"] + 1.0)
    if ql > 0:
        chip(base, "server → server · bằng chứng", VIOLET, 900, 715, ql, 15, 8, 1.0)
        qmk = seg(t, tl["s0704"] + 0.9, tl["s0704"] + 1.3)
        if qmk > 0:
            ov = Image.new("RGBA", (W, 26), (0, 0, 0, 0))
            draw_marker(ImageDraw.Draw(ov), 710, 14, 1090, 14, qmk, C(VIOLET), 5, seed=11)
            base.alpha_composite(ov, (0, 738))
    qx = seg(t, tl["s0706"] - 0.1, tl["s0706"] + 0.4)
    if qx > 0:
        im, pad = chrome(660, 104, 22, C(RED, 90), (30, 24, 36, 244))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 22), "× Không xác nhận đơn từ Return URL", font=B24S, fill=C(TXT))
        d.text((pad + 22, pad + 62), "kẻ giả mạo tự mở được địa chỉ này", font=B15, fill=C(MUT))
        blit(base, im, 1400, 215, qx, 10)
    qv = seg(t, tl["s0707"] - 0.05, tl["s0707"] + 0.4)
    if qv > 0:
        chip(base, "xác minh dữ liệu ngân hàng", EMER, 1450, 790, qv, 15, 8, 1.0)


# ---------- S08 oauth ----------
def s08(base, t, tl, durs, s0, s1):
    title(base, "OAUTH 2.0 · CLIENT CREDENTIALS", ["Xác thực và giữ khóa bí mật"], VIOLET,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    p1 = seg(t, tl["s0801"] + 0.2, tl["s0801"] + 0.6)
    p2 = seg(t, tl["s0802"] - 0.05, tl["s0802"] + 0.4)
    mini(base, 280, 390, 300, 180, p1, VIOLET, "server", "BACKEND", "giữ bí mật", None, t, 24)
    mini(base, 800, 390, 330, 190, p2, CYAN, "shield-check", "TOKEN SERVER", "máy chủ xác thực", None, t, 24)
    mini(base, 1460, 390, 300, 180, max(p1, p2), EMER, "layers", "PAYMENT API", "API thanh toán", None, t, 24)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    q1 = seg(t, tl["s0802"], tl["s0802"] + 0.45)
    S.beam(d, 442, 616, 390, q1, VIOLET, CYAN, t)
    q2 = seg(t, tl["s0803"] - 0.05, tl["s0803"] + 0.4)
    S.beam(d, 986, 1290, 390, q2, CYAN, EMER, t)
    if q2 > 0.95:
        S.packets(d, 995, 1280, 390, t, EMER)
    base.alpha_composite(ov)
    f8 = 1 - seg(t, tl["s0808"] - 0.1, tl["s0808"] + 0.3)
    if q1 * f8 > 0:
        chip(base, "Client ID + Client Secret", AMBER, 520, 536, q1 * f8, 15, 8, 1.0)
    qt = seg(t, tl["s0803"] + 0.2, tl["s0803"] + 0.6)
    if qt * f8 > 0:
        S.status_pill(base, 1120, 470, "ACCESS TOKEN", EMER, qt * f8, 15, False, 0.8)
    qh = seg(t, tl["s0804"] - 0.05, tl["s0804"] + 0.35)
    if qh * f8 > 0:
        chip(base, "Authorization: Bearer …", CYAN, 1460, 536, qh * f8, 14, 8, 1.0)
    qr = seg(t, tl["s0805"] + 0.1, tl["s0805"] + 0.5)
    if qr * f8 > 0:
        chip(base, "hết hạn → lấy token mới", VIOLET, 840, 536, qr * f8, 14, 8, 1.0)
    qs = seg(t, tl["s0808"] - 0.05, tl["s0808"] + 0.4)
    if qs > 0:
        chip_row(base, [("HTTPS", EMER, 0), ("xoay vòng khóa", CYAN, 0),
                        ("giới hạn quyền", VIOLET, 0)], 536, qs, gap=14)
    # env card
    qe = seg(t, tl["s0806"] - 0.05, tl["s0806"] + 0.4)
    if qe > 0:
        im, pad = chrome(600, 226, 24, C(AMBER, 75), (20, 30, 50, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 20), ".env · Backend", font=B22S, fill=C(TXT))
        d.text((pad + 22, pad + 58), "BANK_CLIENT_ID=merchant_abc_001", font=M15, fill=C(CYAN))
        d.text((pad + 22, pad + 88), "BANK_CLIENT_SECRET=••••••••", font=M15, fill=C(AMBER))
        d.text((pad + 22, pad + 118), "BANK_WEBHOOK_SECRET=••••••••", font=M15, fill=C(VIOLET))
        d.text((pad + 22, pad + 158), "biến môi trường · không commit", font=B15, fill=C(MUT))
        blit(base, im, 470, 700, qe, 14)
    qb = seg(t, tl["s0807"] - 0.05, tl["s0807"] + 0.4)
    if qb > 0:
        im, pad = chrome(400, 226, 24, C(RED, 75), (28, 24, 38, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 20), "Mã trình duyệt", font=B22S, fill=C(TXT))
        d.text((pad + 22, pad + 58), "Client Secret", font=M16, fill=C(RED))
        d.text((pad + 22, pad + 86), "Private Key", font=M16, fill=C(RED))
        d.text((pad + 22, pad + 114), "API Key", font=M16, fill=C(RED))
        qx = seg(t, tl["s0807"] + 0.4, tl["s0807"] + 0.8)
        if qx > 0:
            for yy in (92, 120, 148):
                d.line([pad + 20, yy, pad + 20 + 200 * qx, yy], fill=C(RED, 230), width=3)
            d.text((pad + 276, pad + 108), "×", font=font("BeVietnamPro-Bold.ttf", 38), fill=C(RED))
        blit(base, im, 1110, 700, qb, 14)
    qm = seg(t, tl["s0809"] + 0.05, tl["s0809"] + 0.45)
    if qm > 0:
        chip(base, "không ghi log · không mã nguồn công khai", RED, 790, 810, qm, 15, 8, 1.0)


# ---------- S09 database ----------
def field_rows(d, pad, rows, y0, rh=38):
    for i, (name, typ, pk) in enumerate(rows):
        y = y0 + i * rh
        d.text((pad + 54, y), name, font=M16, fill=C(TXT))
        d.text((pad + 330, y), typ, font=M15, fill=C(MUT))
        if pk:
            d.text((pad + 24, y), "◈", font=M14, fill=C(AMBER))


def s09(base, t, tl, durs, s0, s1):
    title(base, "THIẾT KẾ DATABASE", ["orders và payments"], CYAN,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    qo = seg(t, tl["s0901"] + 0.2, tl["s0901"] + 0.6)
    qp = seg(t, tl["s0903"] - 0.05, tl["s0903"] + 0.4)
    if qo > 0:
        im, pad = chrome(560, 360, 24, C(CYAN, 70), (20, 30, 52, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 18), "orders", font=font("BeVietnamPro-SemiBold.ttf", 30), fill=C(CYAN))
        d.line([pad + 22, pad + 60, pad + 538, pad + 60], fill=C(CYAN, 90), width=1)
        field_rows(d, pad, [("id", "BIGINT · PK", 1), ("order_code", "VARCHAR", 0),
                            ("total_amount", "DECIMAL", 0), ("payment_status", "VARCHAR", 0),
                            ("order_status", "VARCHAR", 0)], pad + 78, 42)
        qs = seg(t, tl["s0902"] + 0.1, tl["s0902"] + 0.5)
        d.text((pad + 22, pad + 300), "1 đơn · N lần thử thanh toán", font=B16,
               fill=C(AMBER if qs > 0.5 else MUT))
        blit(base, im, 400, 480, qo, 14)
    if qp > 0:
        im, pad = chrome(600, 386, 24, C(EMER, 70), (20, 32, 50, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 18), "payments", font=font("BeVietnamPro-SemiBold.ttf", 30), fill=C(EMER))
        d.line([pad + 22, pad + 60, pad + 578, pad + 60], fill=C(EMER, 90), width=1)
        field_rows(d, pad, [("id", "BIGINT · PK", 1), ("order_id", "BIGINT · FK", 0),
                            ("provider", "VARCHAR", 0), ("provider_transaction_id", "VARCHAR", 0),
                            ("amount", "DECIMAL", 0), ("status", "VARCHAR", 0),
                            ("paid_at", "DATETIME", 0)], pad + 78, 38)
        qu = seg(t, tl["s0906"] - 0.05, tl["s0906"] + 0.4)
        if qu > 0:
            d.rounded_rectangle([pad + 22, pad + 356, pad + 578, pad + 356], 1, fill=C(AMBER, 0))
        blit(base, im, 1240, 470, qp, 14)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ql = seg(t, tl["s0902"] + 0.4, tl["s0902"] + 0.8)
    if ql > 0:
        d.line([690, 480, 690 + 230 * ql, 480], fill=C(AMBER, 200), width=2)
        if ql > 0.9:
            d.text((805, 450), "1 : N", font=M17, fill=C(AMBER), anchor="mm")
    base.alpha_composite(ov)
    # attempts
    qa = seg(t, tl["s0904"] - 0.1, tl["s0904"] + 0.35)
    if qa > 0:
        im = Image.new("RGBA", (420, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        tracked(d, (24, 4), "CÁC LẦN THỬ", M13, C(VIOLET), 2)
        rows = [("FAILED", RED), ("FAILED", RED), ("SUCCESS", EMER)]
        for i, (st_, col) in enumerate(rows):
            on = t >= tl["s0904"] + 0.25 + i * 0.28
            d.text((24, 30 + i * 26), "payment #%d" % (i + 1), font=M15,
                   fill=C(TXT if on else MUT))
            d.text((250, 30 + i * 26), st_, font=M15,
                   fill=C(col, 240 if on else 90))
        blit(base, im, 340, 752, qa, 8)
    qu = seg(t, tl["s0906"] - 0.05, tl["s0906"] + 0.4)
    if qu > 0:
        im, pad = chrome(600, 64, 16, C(AMBER, 110), (22, 30, 44, 244))
        d = ImageDraw.Draw(im)
        d.text((pad + 20, pad + 18), "UNIQUE(provider, provider_transaction_id)", font=M15, fill=C(AMBER))
        blit(base, im, 1240, 700, qu, 10)
        qm = seg(t, tl["s0907"] - 0.05, tl["s0907"] + 0.4)
        if qm > 0:
            draw_marker_circle(ImageDraw.Draw(base), 1240, 700, 316, 26, qm, C(AMBER), 4)


# ---------- S10 code ----------
CODE_A = [
    "router.post('/api/orders', async (req, res) => {",
    "  const items = req.body.items;",
    "  let total = 0;",
    "  for (const it of items) {",
    "    const p = await db.product(it.id);",
    "    total += p.price * it.qty;   // giá từ DB",
    "  }",
    "  const order = await db.orders.insert({",
    "    code: 'DH001',",
    "    total_amount: total,",
    "    payment_status: 'PENDING_PAYMENT'",
    "  });",
    "  res.json({ orderId: order.id, total });",
    "});",
]
CODE_B = [
    "router.post('/api/payments', async (req, res) => {",
    "  const token = await getBankToken();",
    "  const r = await fetch(BANK + '/payments', {",
    "    method: 'POST',",
    "    headers: {",
    "      Authorization: 'Bearer ' + token",
    "    },",
    "    body: JSON.stringify({",
    "      orderId, amount, returnUrl, notifyUrl",
    "    })",
    "  });",
    "  const data = await r.json();",
    "  res.json({ paymentUrl: data.paymentUrl });",
    "});",
]
CODE_C = [
    "router.post('/webhooks/bank', async (req, res) => {",
    "  const ok = verifySignature(req.rawBody, req);",
    "  if (!ok) return res.status(400).end();  // fail",
    "  await db.transaction(async (tx) => {",
    "    const o = await tx.query(",
    "      'SELECT * FROM orders WHERE id=? FOR UPDATE',",
    "      [orderId]",
    "    );",
    "    if (o.total_amount !== amount) {",
    "      throw new Error('amount_mismatch');",
    "    }",
    "    await tx.update('payments', { status: 'SUCCESS' });",
    "    await tx.update('orders', {",
    "      payment_status: 'PAID',",
    "      order_status: 'PROCESSING'",
    "    });",
    "  });",
    "  res.json({ ok: true });",
    "});",
]
CODE_F = font("JetBrainsMono-var.ttf", 15)
CODE_LH = 23


def code_card(base, cx, top, w, h, p, kicker, ttl, lines, q, act_lines, t, box=None):
    if p <= 0:
        return
    im, pad = chrome(w, h, 22, C(VIOLET, 70), (15, 23, 40, 246))
    d = ImageDraw.Draw(im)
    d.text((pad + 20, pad + 14), kicker, font=M13, fill=C(AMBER))
    d.text((pad + 20, pad + 36), ttl, font=B21S, fill=C(TXT))
    d.line([pad + 20, pad + 72, pad + w - 20, pad + 72], fill=(120, 140, 170, 70), width=1)
    n = int(q * sum(len(s) + 1 for s in lines))
    used = 0
    y = pad + 88
    for i, s in enumerate(lines):
        vis = s[:max(0, n - used)] if q < 1 else s
        if vis:
            if i in act_lines:
                d.rounded_rectangle([pad + 14, y - 3, pad + w - 14, y + CODE_LH - 4], 6,
                                    fill=C(AMBER, 26), outline=C(AMBER, 70), width=1)
            com = vis.find("//")
            if com >= 0:
                d.text((pad + 22, y), vis[:com], font=CODE_F, fill=C(TXT))
                d.text((pad + 22 + CODE_F.getlength(vis[:com]), y), vis[com:], font=CODE_F, fill=C(EMER, 220))
            else:
                d.text((pad + 22, y), vis, font=CODE_F, fill=C(TXT))
        used += len(s) + 1
        y += CODE_LH
        if used >= n and q < 1:
            break
    if box:
        y0, y1, lbl = box
        yy0 = pad + 88 + y0 * CODE_LH - 6
        yy1 = pad + 88 + y1 * CODE_LH + 2
        d.rounded_rectangle([pad + 10, yy0, pad + w - 10, yy1], 10,
                            outline=C(AMBER, 160), width=2)
        d.text((pad + w - 18 - M13.getlength(lbl), yy0 + 6), lbl, font=M13, fill=C(AMBER))
    blit(base, im, cx, top + h / 2, p, 10)


def s10(base, t, tl, durs, s0, s1):
    tracked(ImageDraw.Draw(base), (110, 140), "NODE.JS · EXPRESS · MYSQL", M14, C(CYAN), 3)
    base_text = ["Ba bước code Node.js"]
    d = ImageDraw.Draw(base)
    d.text((110, 164), base_text[0], font=B42B, fill=C(TXT))

    def qa():
        return lin(t, tl["s1001"] - 0.05, tl["s1002"] + durs["s1002"] - 0.2)

    progs = [(tl["s1001"] - 0.05, tl["s1002"] + durs["s1002"] - 0.2),
             (tl["s1003"] - 0.05, tl["s1005"] + durs["s1005"] - 0.2),
             (tl["s1006"] - 0.05, tl["s1010"] + 0.5)]
    acts = [set(), set(), set()]
    if tl["s1002"] <= t:
        acts[0].add(4)
    if tl["s1003"] <= t:
        acts[0].add(5)
    if tl["s1004"] <= t:
        acts[1].add(1)
    if tl["s1005"] <= t:
        acts[1].add(12)
    if tl["s1007"] <= t:
        acts[2].add(1)
    if tl["s1008"] <= t:
        acts[2].add(3)
    if tl["s1009"] <= t:
        acts[2].update({11, 12, 13, 14})
    if tl["s1010"] <= t:
        acts[2].add(9)
    qs = [lin(t, a, b) for a, b in progs]
    code_card(base, 395, 230, 570, 560, 1.0, "BƯỚC 1 · TẠO ĐƠN", "POST /api/orders",
              CODE_A, qs[0], acts[0], t)
    code_card(base, 995, 230, 570, 560, 1.0, "BƯỚC 2 · TẠO PAYMENT", "POST /api/payments",
              CODE_B, qs[1], acts[1], t)
    code_card(base, 1595, 230, 570, 560, 1.0, "BƯỚC 3 · WEBHOOK", "POST /webhooks/bank",
              CODE_C, qs[2], acts[2], t,
              box=(3, 16, "transaction") if t >= tl["s1008"] else None)
    qv = seg(t, tl["s1007"] - 0.05, tl["s1007"] + 0.35)
    if qv > 0:
        chip(base, "verifySignature ok", EMER, 820, 826, qv, 14, 6, 1.0)
    qr = seg(t, tl["s1010"] - 0.05, tl["s1010"] + 0.35)
    if qr > 0:
        chip(base, "✕ → rollback toàn bộ", RED, 1090, 826, qr, 14, 6, 1.0)
    qd = seg(t, tl["s1011"] - 0.05, tl["s1011"] + 0.4)
    if qd > 0:
        chip(base, "mô hình minh họa · không phải SDK ngân hàng", VIOLET, 1560, 172, qd, 15, 8, 1.0)


# ---------- S11 states ----------
def s11(base, t, tl, durs, s0, s1):
    title(base, "TRẠNG THÁI THỰC TẾ", ["Không chỉ thành công và thất bại"], AMBER,
          seg(t, s0, s0 + 0.6), y=130, size=42)
    states = [("PENDING", AMBER), ("PAID", EMER), ("PROCESSING", CYAN),
              ("SHIPPING", BLUE), ("COMPLETED", DIM)]
    xs = [220, 540, 860, 1180, 1500]
    q0 = seg(t, tl["s1101"] + 0.2, tl["s1101"] + 0.6)
    for i, (st_, col) in enumerate(states):
        q = max(q0, seg(t, tl["s1102"] - 0.1, tl["s1102"] + 0.2))
        S.status_pill(base, xs[i], 330, st_, col, q, 16, i == 0, 0.4 if i == 0 else 0.0)
        if i < 4:
            qb = seg(t, tl["s1102"] + 0.2 + i * 0.1, tl["s1102"] + 0.55 + i * 0.1)
            if qb > 0:
                S.beam(ImageDraw.Draw(base), xs[i] + 80, xs[i + 1] - 80, 330, qb, col, states[i + 1][1])
    qe = seg(t, tl["s1102"] - 0.05, tl["s1102"] + 0.3)
    if qe > 0:
        S.status_pill(base, 540, 430, "FAILED", RED, qe, 15, False, 0.3)
        S.status_pill(base, 860, 430, "EXPIRED", RED, qe, 15, False, 0.3)
        d = ImageDraw.Draw(base)
        d.line([540, 430 - 24, 540, 380], fill=C(RED, 140), width=2)
        d.line([860, 430 - 24, 860, 380], fill=C(RED, 140), width=2)
    f11 = 1 - seg(t, tl["s1107"] - 0.12, tl["s1107"] + 0.3)
    qt = seg(t, tl["s1103"] - 0.05, tl["s1103"] + 0.4)
    if qt * f11 > 0:
        im, pad = chrome(600, 150, 22, C(AMBER, 85), (26, 28, 36, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 20), "TIMEOUT ≠ FAILED", font=B30S, fill=C(AMBER))
        d.text((pad + 22, pad + 70), "Ngân hàng có thể đã xử lý — hãy truy vấn lại.", font=B17, fill=C(MUT))
        d.text((pad + 22, pad + 100), "Không cập nhật, cũng không đánh dấu thất bại.", font=B15, fill=C(TXT))
        blit(base, im, 420, 600, qt * f11, 12)
    qd = seg(t, tl["s1104"] - 0.05, tl["s1104"] + 0.4)
    if qd * f11 > 0:
        im, pad = chrome(620, 150, 22, C(VIOLET, 85), (24, 26, 44, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 20), "DUPLICATE · idempotent", font=B28R, fill=C(VIOLET))
        d.text((pad + 22, pad + 68), "Gửi lặp vẫn chỉ tạo một kết quả.", font=B17, fill=C(MUT))
        d.text((pad + 22, pad + 100), "Nhận diện bằng provider_transaction_id.", font=M15, fill=C(TXT))
        blit(base, im, 1140, 600, qd * f11, 12)
    qs = seg(t, tl["s1106"] - 0.05, tl["s1106"] + 0.4)
    if qs > 0:
        chip_row(base, [("HTTPS", EMER, 0), ("chữ ký", CYAN, 0),
                        ("timestamp", VIOLET, 0), ("giới hạn IP", AMBER, 0)], 475, qs, gap=12, fs=14)
    # reconciliation table
    qr = seg(t, tl["s1107"] - 0.05, tl["s1107"] + 0.4)
    if qr > 0:
        im, pad = chrome(560, 226, 22, C(EMER, 65), (18, 28, 46, 244))
        d = ImageDraw.Draw(im)
        tracked(d, (pad + 20, pad + 16), "ĐỐI SOÁT CUỐI NGÀY", M13, C(EMER), 2)
        rows = [("DH001", "15.000.000", "Khớp", EMER), ("DH002", "9.500.000", "Khớp", EMER),
                ("DH003", "2.000.000", "Cần kiểm tra", AMBER), ("DH004", "450.000", "Khớp", EMER)]
        for i, (code, amt, st_, col) in enumerate(rows):
            on = t >= tl["s1107"] + 0.2 + i * 0.22
            yy = pad + 46 + i * 38
            d.text((pad + 20, yy), code, font=M15, fill=C(TXT if on else MUT))
            d.text((pad + 130, yy), amt, font=M15, fill=C(MUT if not on else TXT))
            d.text((pad + 400, yy), st_, font=B15, fill=C(col, 235 if on else 80))
        blit(base, im, 960, 640, qr, 12)
    qf = seg(t, tl["s1108"] - 0.05, tl["s1108"] + 0.4)
    if qf > 0:
        chip(base, "webhook thất lạc → truy vấn trạng thái", RED, 420, 800, qf, 15, 8, 1.0)


# ---------- S12 summary ----------
def s12(base, t, tl, durs, s0, s1):
    q0 = seg(t, s0, s0 + 0.6)
    title(base, "TỔNG KẾT", ["Ba điều cần nhớ"], AMBER, q0, y=130, size=42)
    qt = seg(t, tl["s1201"] + 0.2, tl["s1201"] + 0.7)
    if qt > 0:
        chip(base, "tạo đơn → tạo giao dịch → xác minh → cập nhật", CYAN, 960, 300, qt, 15, 8, 1.0)
    cards = [("1", "Tính tiền ở Backend", "không tin total từ client"),
             ("2", "Xác minh chữ ký", "verify trước khi đọc dữ liệu"),
             ("3", "Chống trùng + đối soát", "UNIQUE · idempotent · cuối ngày")]
    for i, (no, ttl, sub) in enumerate(cards):
        q = seg(t, tl["s1203"] + 0.15 + i * 0.28, tl["s1203"] + 0.55 + i * 0.28)
        if q <= 0:
            continue
        im, pad = chrome(430, 220, 24, C(AMBER if i < 3 else CYAN, 70), (22, 32, 54, 242))
        d = ImageDraw.Draw(im)
        d.text((pad + 22, pad + 12), no, font=font("BeVietnamPro-Bold.ttf", 44), fill=C(AMBER))
        d.text((pad + 22, pad + 76), ttl, font=B28R, fill=C(TXT))
        d.text((pad + 22, pad + 124), sub, font=B16, fill=C(MUT))
        blit(base, im, 400 + i * 560, 470, q, 12)
        qm = seg(t, tl["s1203"] + 0.5 + i * 0.28, tl["s1203"] + 0.85 + i * 0.28)
        if qm > 0:
            ov = Image.new("RGBA", (W, 26), (0, 0, 0, 0))
            draw_marker(ImageDraw.Draw(ov), 300 + i * 560, 14, 300 + i * 560 + 250, 14, qm, C(AMBER), 5, seed=13 + i)
            base.alpha_composite(ov, (0, 474))
    qr = seg(t, tl["s1204"] - 0.05, tl["s1204"] + 0.4)
    if qr > 0:
        chip(base, "đối soát cho giao dịch thất lạc", EMER, 960, 650, qr, 15, 8, 1.0)
    qe = seg(t, tl["s1205"] - 0.1, tl["s1205"] + 0.5)
    if qe > 0:
        base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(232 * qe))))
        base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(180 * qe))))
        paste_brand(base, 960, 330, 160, qe)
        tracked(ImageDraw.Draw(base), (960, 430), "AN TECH ACADEMY", B24S, C(TXT), 4, qe, "mm")
        d = ImageDraw.Draw(base)
        d.text((960, 486), "TÍCH HỢP THANH TOÁN NGÂN HÀNG", font=B36B, fill=C(TXT), anchor="mm")
        d.text((960, 540), "Cảm ơn các bạn đã theo dõi", font=B22S, fill=C(MUT), anchor="mm")
        chip_row(base, [("Node.js", EMER, 0), ("MySQL", CYAN, 0), ("Webhook", AMBER, 0)],
                 600, qe, gap=14)
        qn = seg(t, tl["s1206"] - 0.05, tl["s1206"] + 0.35)
        if qn > 0:
            d.text((960, 668), "Bài tiếp theo · hẹn gặp lại", font=B18, fill=C(DIM), anchor="mm")
        qh = seg(t, tl["s1207"] + 0.1, tl["s1207"] + 0.5)
        if qh > 0:
            d.text((960, 716), "HẸN GẶP LẠI CÁC BẠN", font=B24S, fill=C(AMBER), anchor="mm")


SCENE_FN = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12]
POSES = ["wave", "point_left", "write", "present", "point_left", "write",
         "point_left", "write", "present", "present", "present", "wave"]


# ---------- timeline ----------
def build_timeline(durs):
    base_end = 0.40 + sum(durs[c[0]] + c[2] for c in CUES)
    sum_hold = sum(sc["hold"] for sc in SCENES[:-1])
    scale = max(0.0, min(2.0, (TARGET - base_end - 4.8) / max(1e-6, sum_hold)))
    tl = {}
    t = 0.40
    for si, sc in enumerate(SCENES):
        for c in sc["cues"]:
            tl[c["id"]] = t
            t += durs[c["id"]] + float(c["pause"])
        if si < len(SCENES) - 1:
            t += sc["hold"] * scale
    total = t + 4.8
    starts = [tl[sc["cues"][0]["id"]] for sc in SCENES]
    return tl, total, starts, scale


# ---------- render ----------
def make_draw(tl, total, starts, durs):
    cue_ids = [c[0] for c in CUES]
    cue_starts = [tl[i] for i in cue_ids]
    talk = [(tl[c[0]], tl[c[0]] + durs[c[0]]) for c in CUES]
    n_sc = len(SCENES)

    def draw(t):
        base = S.stage_bg(t)
        si = bisect.bisect_right(starts, t) - 1
        si = max(0, min(n_sc - 1, si))
        header(base, t, TAGS[si])
        s0 = starts[si]
        s1 = starts[si + 1] if si + 1 < n_sc else total
        SCENE_FN[si](base, t, tl, durs, s0, s1)
        talk_on = any(a <= t < b for a, b in talk)
        an_sprite(base, t, POSES[si], talk_on, seg(t, 0.9, 1.5),
                  0.46 if si == 9 else 0.66,
                  1822 if si == 9 else 1752, 1042)
        # caption
        ci = bisect.bisect_right(cue_starts, t) - 1
        if 0 <= ci < len(cue_ids):
            cid = cue_ids[ci]
            stc, dd = tl[cid], durs[cid]
            if stc <= t < stc + dd + 0.15:
                pin = seg(t, stc, stc + 0.3)
                pout = 1 - seg(t, stc + dd - 0.15, stc + dd + 0.15)
                caption_auto(base, SAY[cid], pin * pout, (1 - back(pin)) * 26 - (1 - pout) * 14)
        qf = lin(t, total - 0.9, total - 0.05)
        if qf > 0:
            base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(255 * qf))))
        im = S.camera(base, t, total, starts[1:] + [tl["s0606"], tl["s0609"]])
        wq = seg(t, 0.25, 0.85) * (1 - qf)
        if wq > 0:
            brand_watermark(im, size=120, alpha=0.9 * wq, pos="tr", margin=28)
        return im

    return draw


def an_sprite(base, t, pose, talk, alpha=1.0, scale=0.66, x=1752, y=1042):
    if alpha <= 0:
        return
    im = character.draw(t, pose, -1, talk, scale)
    if alpha < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(x - im.width / 2), int(y - im.height)))


def back(x, s=1.7):
    x = max(0.0, min(1.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


# ---------- sfx ----------
def _pitch(x, r):
    n = max(1, int(len(x) / r))
    return np.interp(np.arange(n) * r, np.arange(len(x)), x)


def build_sfx(tl, durs, total, starts):
    n = int(total * SR) + SR
    bus = np.zeros(n)

    def put(x, at, g):
        s0 = int(at * SR)
        if s0 < 0 or s0 >= n:
            return
        m = min(len(x), n - s0)
        bus[s0:s0 + m] += x[:m] * g

    W0, PO, TK = sfx.sfx("whoosh"), sfx.sfx("pop"), sfx.sfx("tick")
    CL, TH, CH = sfx.sfx("click"), sfx.sfx("thud"), sfx.sfx("chime")
    SU, DY = sfx.sfx("success"), sfx.sfx("deny")
    MK = sfx.sfx("marker", 0.55)
    for si, sc in enumerate(SCENES):
        st0 = tl[sc["cues"][0]["id"]]
        if si:
            put(_pitch(W0, 0.95 + (si % 3) * 0.06), st0 - 0.12, 0.14)
        put(PO, st0 + 0.35, 0.06)
    ev = [
        (tl["s0103"] + 0.5, "tk", 0.05), (tl["s0104"] + 0.3, "th", 0.08),
        (tl["s0105"] + 0.4, "ch", 0.05), (tl["s0106"] + 0.2, "po", 0.05),
        (tl["s0202"] + 0.5, "tk", 0.05), (tl["s0204"] + 0.3, "tk", 0.05),
        (tl["s0204"] + 0.9, "tk", 0.05), (tl["s0205"] + 0.5, "dy", 0.06),
        (tl["s0207"] + 0.4, "su", 0.05), (tl["s0208"] + 0.2, "ch", 0.05),
        (tl["s0302"] + 0.2, "tk", 0.04), (tl["s0303"] + 0.2, "tk", 0.04),
        (tl["s0304"] + 0.2, "su", 0.05), (tl["s0305"] + 0.1, "po", 0.05),
        (tl["s0307"] + 0.6, "dy", 0.07), (tl["s0308"] + 0.3, "mk", 0.10),
        (tl["s0401"] + 0.3, "po", 0.05), (tl["s0402"] + 0.2, "tk", 0.04),
        (tl["s0403"] + 0.2, "tk", 0.04), (tl["s0404"] + 0.2, "tk", 0.04),
        (tl["s0405"] + 0.2, "tk", 0.04), (tl["s0406"] + 0.2, "tk", 0.04),
        (tl["s0407"] + 0.5, "dy", 0.07), (tl["s0408"] + 0.2, "ch", 0.05),
        (tl["s0501"] + 0.3, "po", 0.05), (tl["s0505"] + 0.1, "tk", 0.04),
        (tl["s0507"] + 0.2, "ch", 0.06),
        (tl["s0602"] + 0.2, "tk", 0.05), (tl["s0603"] + 0.2, "th", 0.08),
        (tl["s0604"] + 0.4, "cl", 0.06), (tl["s0605"] + 0.2, "tk", 0.04),
        (tl["s0606"] + 0.2, "tk", 0.04), (tl["s0607"] + 0.2, "tk", 0.04),
        (tl["s0608"] + 0.2, "tk", 0.04), (tl["s0609"] + 0.2, "tk", 0.04),
        (tl["s0610"] + 0.8, "tk", 0.04), (tl["s0610"] + 2.0, "tk", 0.04),
        (tl["s0611"] + 0.3, "ch", 0.06), (tl["s0612"] + 0.2, "dy", 0.07),
        (tl["s0702"] + 0.3, "tk", 0.04), (tl["s0704"] + 0.3, "th", 0.07),
        (tl["s0706"] + 0.3, "dy", 0.06), (tl["s0707"] + 0.2, "mk", 0.09),
        (tl["s0802"] + 0.3, "tk", 0.04), (tl["s0803"] + 0.4, "ch", 0.05),
        (tl["s0806"] + 0.2, "po", 0.05), (tl["s0807"] + 0.5, "dy", 0.06),
        (tl["s0809"] + 0.2, "mk", 0.09),
        (tl["s0901"] + 0.3, "po", 0.05), (tl["s0903"] + 0.3, "po", 0.05),
        (tl["s0904"] + 0.3, "tk", 0.04), (tl["s0904"] + 0.6, "tk", 0.04),
        (tl["s0904"] + 0.9, "tk", 0.04), (tl["s0906"] + 0.3, "ch", 0.05),
        (tl["s1001"] + 0.3, "cl", 0.05), (tl["s1003"] + 0.3, "cl", 0.05),
        (tl["s1006"] + 0.3, "cl", 0.05), (tl["s1008"] + 0.2, "th", 0.08),
        (tl["s1009"] + 0.4, "ch", 0.06), (tl["s1010"] + 0.2, "dy", 0.06),
        (tl["s1102"] + 0.3, "tk", 0.04), (tl["s1103"] + 0.3, "th", 0.07),
        (tl["s1104"] + 0.3, "dy", 0.05), (tl["s1105"] + 0.4, "ch", 0.05),
        (tl["s1107"] + 0.4, "tk", 0.04), (tl["s1108"] + 0.2, "tk", 0.04),
        (tl["s1203"] + 0.3, "po", 0.05), (tl["s1203"] + 0.6, "po", 0.05),
        (tl["s1203"] + 0.9, "po", 0.05), (tl["s1205"] + 0.5, "ch", 0.06),
    ]
    names = {"tk": TK, "po": PO, "th": TH, "cl": CL, "ch": CH, "su": SU, "dy": DY, "mk": MK}
    for at, k, g in ev:
        put(names[k], at, g)
    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.30:
        bus *= 0.30 / pk
    elif 0 < pk < 0.22:
        bus *= 0.22 / pk
    return bus


# ---------- main ----------
def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    stills = "--stills" in sys.argv
    missing = [c[0] for c in CUES if not (os.path.exists(f"{AUD}/{c[0]}.wav")
                                          and os.path.getsize(f"{AUD}/{c[0]}.wav") > 20000)]
    if missing:
        raise SystemExit("Thiếu audio: " + ", ".join(missing))
    durs = {c[0]: len(decode(f"{AUD}/{c[0]}.wav")) / SR for c in CUES}
    tl, total, starts, scale = build_timeline(durs)
    print("HOLD scale", round(scale, 2), flush=True)
    print("TOTAL", round(total, 2), "s", flush=True)
    draw = make_draw(tl, total, starts, durs)

    if stills:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        picks = []
        for si, sc in enumerate(SCENES):
            ids = [c["id"] for c in sc["cues"]]
            a, b = tl[ids[0]], tl[ids[-1]] + durs[ids[-1]]
            picks.append((si, a + (b - a) * 0.55))
        picks.append((11, total - 1.5))
        for si, tt in picks:
            draw(tt).convert("RGB").save(f"{sd}/s{si + 1:02d}_{tt:.1f}.png")
            print("STILL", si + 1, round(tt, 1), flush=True)
        return

    demo = None
    if "--demo" in sys.argv:
        i = sys.argv.index("--demo")
        demo = (float(sys.argv[i + 1]), float(sys.argv[i + 2]))
    tag = "images30" if demo else TAG
    frm = OUT + "/frames_demo" if demo else FR
    n = int(total * FPS)
    mix = np.zeros(int(total * SR) + SR)
    for sid, _, _ in CUES:
        x = decode(f"{AUD}/{sid}.wav")
        s0 = int(tl[sid] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(tl, durs, total, starts)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = float(np.max(np.abs(mix)))
    print("PEAK", round(pk, 3), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    if demo:
        a0 = int(demo[0] * SR)
        mix = mix[a0:a0 + int((demo[1] - demo[0]) * SR)]
    sfx.write_wav(OUT + f"/voice_{tag}.wav", mix)

    if demo:
        n = int(round((demo[1] - demo[0]) * FPS))
        os.makedirs(frm, exist_ok=True)
        for k in range(n):
            fp = f"{frm}/f{k:04d}.jpg"
            if not os.path.exists(fp):
                draw(demo[0] + k / FPS).convert("RGB").save(fp, quality=92)
            if k % 300 == 0:
                print("frame", k, "/", n, flush=True)
    else:
        for k in range(n):
            fp = f"{frm}/f{k:04d}.jpg"
            if not os.path.exists(fp):
                draw(k / FPS).convert("RGB").save(fp, quality=92)
            if k % 300 == 0:
                print("frame", k, "/", n, flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/video_{tag}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{frm}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")

    mixp = OUT + f"/voice_{tag}.wav"
    comp = OUT + f"/voice_{tag}_comp.wav"
    run([FF, "-y", "-i", mixp, "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    mm = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", comp, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr, re.S)[-1]
    mm = json.loads(mm)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:"
          f"measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:"
          f"offset={mm['target_offset']}:linear=true,volume=-0.2dB")
    run([FF, "-y", "-i", comp, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         OUT + f"/audio_{tag}.m4a"])
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_{tag}.m4a", "-c:v", "copy", "-c:a", "copy",
             "-movflags", "+faststart", "-shortest", OUT + f"/{tag}.mp4"])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
    print("DONE", OUT + f"/{tag}.mp4", dur(OUT + f"/{tag}.mp4"), flush=True)


if __name__ == "__main__":
    main()
