# -*- coding: utf-8 -*-
"""Cổng B — mẫu ~41 s bài ThanhToanTheNH: giọng clone + An + SFX, không nhạc nền.
Dùng: python demo41.py            (render đầy đủ)
      python demo41.py --stills   (chỉ xuất ảnh tĩnh để duyệt bố cục)
"""
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = r"D:\Edit\Kit"
os.environ.setdefault("PROJECT_ROOT", PROJECT)
sys.path.insert(0, KIT + "/tools")
from core import W, H, FPS, FF, font, draw_marker, draw_marker_circle, paste_brand, brand_watermark
from demo20 import bg, shadow_card, blit, tracked, chip, caption, decode, dur, seg, lin
from prep_icons import icon_rgba
import sfx, character, tts_vieneu

SR = sfx.SR
OUT = PROJECT + "/mau/congB_41s"
AUD = OUT + "/audio"
FR = OUT + "/frames"
TAG = "thanhtoan_congB_41s_v2"

TXT = (236, 241, 249)
MUT = (148, 163, 184)
CYAN = (34, 211, 238)
EMER = (52, 211, 153)
AMBER = (245, 158, 11)
VIOLET = (139, 92, 246)
RED = (229, 72, 77)
DIM = (100, 116, 139)


def C(c, a=255):
    return c[:3] + (a,)


def hx(c):
    return "#%02X%02X%02X" % c[:3]


# --- nhịp mẫu: lấy đúng lời trong script.json (Cổng A) ---
CUES = [
    ("s0101", "Xin chào các bạn! Chào mừng đến với An Tech Academy.", 0.45),
    ("s0102", "Hôm nay, chúng ta sẽ nối website bán hàng với ngân hàng.", 0.50),
    ("s0201", "API ngân hàng là giao diện lập trình do ngân hàng cung cấp.", 0.50),
    ("s0202", "Nó cho phép phần mềm bên ngoài gọi dịch vụ ngân hàng qua Internet.", 0.50),
    ("s0603", "Bước hai: Backend tự tính tiền từ dữ liệu trong Database.", 0.50),
    ("s0604", "Không tin số tiền do Frontend gửi lên, vì client có thể sửa.", 0.55),
    ("s0605", "Đơn hàng được lưu ở trạng thái chờ thanh toán.", 0.60),
    ("s0610", "Bước bảy: Backend kiểm tra chữ ký, mã giao dịch, số tiền và trạng thái.", 0.55),
    ("s0611", "Bước tám: hợp lệ thì cập nhật đã thanh toán và chuyển đơn sang xử lý.", 0.55),
    ("s0612", "Nếu bước bảy thất bại, tuyệt đối không cập nhật đơn hàng.", 0.45),
]

CAPS = {
    "s0101": ["Xin chào các bạn! Chào mừng đến", "với An Tech Academy."],
    "s0102": ["Hôm nay, chúng ta nối website bán hàng", "với ngân hàng."],
    "s0201": ["API ngân hàng — giao diện lập trình", "do ngân hàng cung cấp."],
    "s0202": ["Phần mềm bên ngoài gọi dịch vụ", "ngân hàng qua Internet."],
    "s0603": ["Bước 2 — Backend tự tính tiền", "từ dữ liệu trong Database."],
    "s0604": ["Không tin số tiền Frontend gửi lên,", "vì client có thể sửa."],
    "s0605": ["Đơn hàng được lưu ở trạng thái", "chờ thanh toán."],
    "s0610": ["Bước 7 — kiểm tra chữ ký, mã giao dịch,", "số tiền và trạng thái."],
    "s0611": ["Hợp lệ — cập nhật đã thanh toán,", "chuyển đơn sang xử lý."],
    "s0612": ["Bước 7 thất bại —", "không cập nhật đơn hàng."],
}

# --- fonts dùng nhiều ---
M13 = font("JetBrainsMono-var.ttf", 13)
M14 = font("JetBrainsMono-var.ttf", 14)
M15 = font("JetBrainsMono-var.ttf", 15)
M16 = font("JetBrainsMono-var.ttf", 16)
M17 = font("JetBrainsMono-var.ttf", 17)
M19 = font("JetBrainsMono-var.ttf", 19)
M22 = font("JetBrainsMono-var.ttf", 22)
B15M = font("BeVietnamPro-Medium.ttf", 15)
B18 = font("BeVietnamPro-Regular.ttf", 18)
B20S = font("BeVietnamPro-SemiBold.ttf", 20)
B22S = font("BeVietnamPro-SemiBold.ttf", 22)
B24R = font("BeVietnamPro-Regular.ttf", 24)
B26S = font("BeVietnamPro-SemiBold.ttf", 26)
B28R = font("BeVietnamPro-Regular.ttf", 28)
B32S = font("BeVietnamPro-SemiBold.ttf", 32)
B36B = font("BeVietnamPro-Bold.ttf", 36)
B38B = font("BeVietnamPro-Bold.ttf", 38)
B62B = font("BeVietnamPro-Bold.ttf", 62)


def synth(sid, text):
    p = f"{AUD}/{sid}.wav"
    if os.path.exists(p) and os.path.getsize(p) > 20000:
        return p
    tts_vieneu.synth(text, p)
    print(f"TTS {sid} ok {dur(p):.2f}s (clone)", flush=True)
    return p


# ---------- nền ----------
TRACES = [
    [(0, 232), (150, 232), (150, 300), (392, 300)],
    [(1920, 268), (1750, 268), (1750, 196), (1546, 196)],
    [(0, 838), (128, 838), (128, 772), (320, 772)],
    [(1920, 962), (1706, 962), (1706, 894), (1512, 894)],
]


def on_poly(poly, q):
    segs, tot = [], 0.0
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


def stage_bg(t):
    base = bg().copy()
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for poly in TRACES:
        d.line(poly, fill=(150, 200, 255, 16), width=1, joint="curve")
        for pt in poly:
            d.rectangle([pt[0] - 2, pt[1] - 2, pt[0] + 2, pt[1] + 2], fill=(150, 200, 255, 28))
    for x, y, sx, sy in ((44, 44, 1, 1), (W - 44, 44, -1, 1),
                         (44, H - 44, 1, -1), (W - 44, H - 44, -1, -1)):
        d.line([x, y, x + 74 * sx, y], fill=(255, 255, 255, 40), width=2)
        d.line([x, y, x, y + 74 * sy], fill=(255, 255, 255, 40), width=2)
    for i in range(40):
        x0 = (i * 137) % W
        y0 = (i * 211) % H
        y = (y0 - t * (6 + (i % 5) * 4)) % H
        x = x0 + 9 * math.sin(t * 0.45 + i)
        a = 9 + (i * 13) % 22
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(198, 224, 255, a))
    for j in range(4):
        px, py = on_poly(TRACES[j], (t * 0.05 + j * 0.31) % 1)
        for rr, aa in ((10, 14), (5, 34), (2, 130)):
            d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(120, 214, 255, aa))
    base.alpha_composite(ov)
    return base


def header(base, t):
    p = seg(t, 0.2, 0.9)
    if p <= 0:
        return
    bm = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bm)
    bd.rounded_rectangle([88, 62, 96, 110], 3, fill=C(AMBER))
    tracked(bd, (112, 78), "AN TECH ACADEMY", B22S, C(TXT), 2)
    tracked(bd, (112, 104), "TÍCH HỢP THANH TOÁN · API NGÂN HÀNG", M14, C(MUT), 2)
    tracked(bd, (1748, 78), "MẪU CỔNG B · CLONE + AN + SFX", M14, C(MUT), 1, 1.0, "rm")
    blit(base, bm, W / 2, 70, p, 18)


def an_sprite(base, t, pose, talk, alpha=1.0, scale=0.66, x=1752, y=1042):
    if alpha <= 0:
        return
    im = character.draw(t, pose, -1, talk, scale)
    if alpha < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(x - im.width / 2), int(y - im.height)))


def panel(base, cx, cy, w, h, p, acc, icon, kicker, title, t, inner=None):
    if p <= 0:
        return
    im, pad = shadow_card(w, h, 24, border=C(acc, 74), fill=(22, 33, 57, 240))
    d = ImageDraw.Draw(im)
    pul = 0.5 + 0.5 * math.sin(t * 2.6)
    d.line([pad + 24, pad + 1, pad + w - 24, pad + 1], fill=C(acc, int(70 + 60 * pul)), width=2)
    tile = Image.new("RGBA", (54, 54), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.rounded_rectangle([0, 0, 53, 53], 15, fill=C(acc, 30), outline=C(acc, 110), width=1)
    ii = icon_rgba(icon, hx(acc)).resize((32, 32), Image.LANCZOS)
    tile.alpha_composite(ii, (11, 11))
    im.alpha_composite(tile, (pad + 24, pad + 20))
    tracked(d, (pad + 92, pad + 38), kicker, M15, C(acc), 2)
    d.text((pad + 24, pad + 84), title, font=B32S, fill=C(TXT))
    if inner:
        inner(im, d, pad)
    e = 1 - (1 - p) ** 3
    sc = 0.87 + 0.13 * e
    if abs(sc - 1) > 0.004:
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx, cy, min(1.0, p * 1.45), 12)


def status_pill(base, cx, cy, text, col, p, fsize=17, filled=False, glow=0.0):
    if p <= 0:
        return
    f = font("JetBrainsMono-var.ttf", fsize)
    w = int(f.getlength(text)) + 58
    h = 46
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if filled:
        d.rounded_rectangle([0, 0, w - 1, h - 1], 13, fill=C(col, 235))
        d.text((w / 2, h / 2), text, font=f, fill=(10, 16, 28, 255), anchor="mm")
    else:
        d.rounded_rectangle([0, 0, w - 1, h - 1], 13, fill=(9, 14, 26, 235),
                            outline=C(col, 200), width=2)
        d.ellipse([16, h / 2 - 4, 24, h / 2 + 4], fill=C(col))
        d.text((34, h / 2), text, font=f, fill=C(TXT), anchor="lm")
    if glow > 0:
        d.rounded_rectangle([-5, -5, w + 4, h + 4], 16, outline=C(col, int(120 * glow)), width=2)
    sc = 0.82 + 0.18 * (1 - (1 - p) ** 3)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
    blit(base, im, cx, cy, min(1, p * 1.5), 10)


def beam(d, x0, x1, y, p, c0, c1, t=None):
    if p <= 0:
        return
    x = x0 + (x1 - x0) * p
    d.line([x0, y, x, y], fill=C(c0, 32), width=9)
    n = max(2, int(abs(x - x0) // 6))
    for i in range(n):
        xa = x0 + (x - x0) * i / n
        xb = x0 + (x - x0) * (i + 1) / n
        u = i / n
        c = tuple(int(c0[k] + (c1[k] - c0[k]) * u) for k in range(3))
        d.line([xa, y, xb, y], fill=C(c, 245), width=3)
    if p < 0.995:
        for rr, aa in ((16, 30), (8, 90), (3, 230)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=C(c1, aa))
    if p > 0.96:
        ang = 0 if x1 >= x0 else math.pi
        hd = 14
        p1 = (x1 - hd * math.cos(ang - 0.5), y + hd * math.sin(ang - 0.5))
        p2 = (x1 - hd * math.cos(ang + 0.5), y + hd * math.sin(ang + 0.5))
        d.polygon([(x1, y), p1, p2], fill=C(c1, 230))
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
                d.line([xa, y, xa + dirn * 6 * scale, y], fill=C(col, aa), width=2)
        for rr, aa in ((13 * scale, a // 12), (8 * scale, a // 4), (4 * scale, a)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=C(col, aa))


def back(x, s=1.7):
    x = max(0.0, min(1.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def camera(im, t, total, stages):
    z = 1.018 + 0.014 * seg(t, 0, total)
    for ts in stages:
        if t > ts:
            z += 0.006 * math.exp(-(t - ts) / 0.35)
    z -= 0.010 * seg(t, total - 1.6, total)
    px = 3.2 * math.sin(t * 0.33)
    py = 2.2 * math.sin(t * 0.27 + 0.8)
    a = 1.0 / z
    c = W / 2 * (1 - a) + px
    f = H / 2 * (1 - a) + py
    return im.transform((W, H), Image.AFFINE, (a, 0, c, 0, a, f), resample=Image.BICUBIC)


# ---------- phase 1: hook + lời chào ----------
def receipt_card(base, cx, cy, p, t):
    if p <= 0:
        return
    w, h = 420, 372
    im, pad = shadow_card(w, h, 22, border=C(AMBER, 90), fill=(22, 33, 57, 244))
    d = ImageDraw.Draw(im)
    pul = 0.5 + 0.5 * math.sin(t * 3.0)
    d.line([pad + 22, pad + 1, pad + w - 22, pad + 1], fill=C(AMBER, int(80 + 70 * pul)), width=2)
    ic = icon_rgba("receipt", hx(AMBER)).resize((30, 30), Image.LANCZOS)
    im.paste(ic, (pad + 24, pad + 22), ic)
    tracked(d, (pad + 64, pad + 38), "HÓA ĐƠN · DH001", M16, C(AMBER), 2)
    d.text((pad + 24, pad + 86), "Điện thoại thông minh", font=B26S, fill=C(TXT))
    d.text((pad + 24, pad + 124), "× 1  ·  Chưa thanh toán", font=B18, fill=C(MUT))
    for xx in range(pad + 24, pad + w - 24, 14):
        d.line([xx, pad + 168, xx + 7, pad + 168], fill=(90, 105, 130, 180), width=1)
    d.text((pad + 24, pad + 186), "TỔNG TIỀN", font=M14, fill=C(MUT))
    d.text((pad + w - 24, pad + 204), "15.000.000đ", font=B38B, fill=C(TXT), anchor="rm")
    for xx in range(pad + 24, pad + w - 24, 14):
        d.line([xx, pad + 246, xx + 7, pad + 246], fill=(90, 105, 130, 180), width=1)
    d.text((pad + 24, pad + 262), "TRẠNG THÁI", font=M14, fill=C(MUT))
    px, py, pw, ph = pad + 24, pad + 288, 250, 52
    d.rounded_rectangle([px, py, px + pw, py + ph], 14, fill=C(AMBER, int(26 + 18 * pul)),
                        outline=C(AMBER, 210), width=2)
    d.ellipse([px + 20, py + 22, px + 30, py + 32], fill=C(AMBER))
    d.text((px + 44, py + 26), "CHỜ THANH TOÁN", font=B20S, fill=(253, 230, 200, 255), anchor="lm")
    e = 1 - (1 - p) ** 3
    sc = 0.88 + 0.12 * e
    if abs(sc - 1) > 0.004:
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
    blit(base, im, cx, cy, min(1, p * 1.4), 16)


def phase1(base, t, st):
    q = lin(t, 0.25, 1.05)
    if q > 0:
        im = Image.new("RGBA", (1000, 380), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        tracked(d, (0, 16), "BÀI GIẢNG · THANH TOÁN TRỰC TUYẾN", M17, C(AMBER), 3)
        d.text((0, 58), "Nối website bán hàng", font=B62B, fill=C(TXT))
        d.text((0, 136), "với ngân hàng", font=B62B, fill=C(TXT))
        draw_marker(d, 4, 214, 336, 214, seg(t, 0.6, 1.3), C(AMBER), 7, seed=3)
        d.text((2, 242), "API thanh toán · Node.js · MySQL", font=B28R, fill=C(MUT))
        blit(base, im, 565, 350, q, 26)
    for txt_, col, ct, cx in (("Node.js · Express", EMER, 1.05, 238),
                              ("MySQL", CYAN, 1.25, 470),
                              ("Webhook · IPN", AMBER, 1.45, 704)):
        qq = seg(t, ct, ct + 0.4)
        if qq > 0:
            chip(base, txt_, col, cx, 560, qq, 16, 10, 0.86 + 0.14 * qq)
    receipt_card(base, 1345, 540, seg(t, st["s0102"] - 0.05, st["s0102"] + 0.55), t)


# ---------- phase 2: API ngân hàng là gì ----------
def phase2(base, t, st, b2):
    p1 = seg(t, b2, b2 + 0.55)
    p2 = seg(t, b2 + 0.18, b2 + 0.73)
    p3 = seg(t, b2 + 0.36, b2 + 0.91)

    def inner_w(im, d, pad):
        d.text((pad + 24, pad + 146), "khách chọn hàng", font=B18, fill=C(MUT))

    def inner_b(im, d, pad):
        d.text((pad + 24, pad + 146), "xử lý giao dịch", font=B18, fill=C(MUT))

    panel(base, 330, 470, 360, 200, p1, CYAN, "monitor", "WEBSITE", "Bán hàng", t, inner_w)
    panel(base, 1590, 470, 360, 200, p3, EMER, "building-2", "NGÂN HÀNG", "Giao dịch", t, inner_b)
    panel(base, 960, 470, 300, 170, p2, VIOLET, "layers", "GIAO DIỆN", "API", t)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ql = seg(t, b2 + 0.55, b2 + 1.05)
    qr = seg(t, b2 + 0.75, b2 + 1.25)
    beam(d, 515, 800, 470, ql, CYAN, VIOLET, t)
    beam(d, 1115, 1400, 470, qr, VIOLET, EMER, t)
    if ql > 0.95:
        packets(d, 522, 792, 470, t, CYAN)
    if qr > 0.95:
        packets(d, 1122, 1393, 470, t, EMER)
    draw_marker_circle(d, 960, 470, 172, 106, seg(t, st["s0201"] + 0.25, st["s0201"] + 1.1),
                       C(VIOLET), 5, seed=4)
    base.alpha_composite(ov)

    qs = seg(t, st["s0202"] - 0.05, st["s0202"] + 0.5)
    if qs > 0:
        w, h = 780, 96
        im, pad = shadow_card(w, h, 20, border=C(CYAN, 70), fill=(18, 28, 49, 240))
        di = ImageDraw.Draw(im)
        ic = icon_rgba("globe", hx(CYAN)).resize((34, 34), Image.LANCZOS)
        im.paste(ic, (pad + 26, pad + 31), ic)
        di.text((pad + 76, h / 2 + pad - 2), "Phần mềm bên ngoài gọi dịch vụ qua Internet",
                font=B20S, fill=C(TXT), anchor="lm")
        ic2 = icon_rgba("lock", hx(EMER)).resize((24, 24), Image.LANCZOS)
        im.paste(ic2, (pad + w - 132, pad + 36), ic2)
        di.text((pad + w - 100, h / 2 + pad - 2), "HTTPS", font=M16, fill=C(EMER), anchor="lm")
        blit(base, im, 960, 700, qs, 14)


# ---------- phase 3: tính tiền ở Backend ----------
def phase3(base, t, st, b3):
    p = seg(t, b3, b3 + 0.7)
    if p <= 0:
        return
    xs = [150 + i * 231.4 for i in range(8)]
    y = 196
    labels = ["Đặt hàng", "Tính tiền", "Lưu đơn", "Gọi bank",
              "Nhận URL", "Khách trả", "Webhook", "Cập nhật"]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    xe = xs[0] + (xs[-1] - xs[0]) * p
    d.line([xs[0], y, xe, y], fill=(148, 163, 184, 60), width=3)
    for i, x in enumerate(xs):
        if x > xe + 2:
            break
        active = i in (1, 2)
        done = i == 0
        r = 15
        if active:
            pul = 0.5 + 0.5 * math.sin(t * 3.2 + i)
            d.ellipse([x - r - 7, y - r - 7, x + r + 7, y + r + 7],
                      outline=C(AMBER, int(60 + 50 * pul)), width=2)
            d.ellipse([x - r, y - r, x + r, y + r], fill=C(AMBER))
            d.text((x, y), str(i + 1), font=M14, fill=(15, 23, 42, 255), anchor="mm")
        elif done:
            d.ellipse([x - r, y - r, x + r, y + r], fill=C(EMER, 220))
            d.line([x - 5, y, x - 1, y + 5], fill=(10, 40, 28, 255), width=3)
            d.line([x - 1, y + 5, x + 6, y - 6], fill=(10, 40, 28, 255), width=3)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], outline=C(DIM, 180), width=2)
            d.text((x, y), str(i + 1), font=M14, fill=C(MUT), anchor="mm")
        lab = C(TXT) if active else (C(EMER) if done else C(MUT, 220))
        d.text((x, y + 36), labels[i], font=B15M, fill=lab, anchor="mm")
    base.alpha_composite(ov)

    def inner_a(im, d, pad):
        bx0, by0 = pad + 20, pad + 152
        d.rounded_rectangle([bx0, by0, bx0 + 300, by0 + 84], 12,
                            fill=(12, 19, 34, 240), outline=(148, 163, 184, 70), width=1)
        d.text((bx0 + 14, by0 + 10), "POST /api/checkout", font=M15, fill=(214, 232, 250, 255))
        d.text((bx0 + 14, by0 + 44), '{ "total": 9000000 }', font=M15, fill=(251, 191, 120, 255))

    def inner_b(im, d, pad):
        d.text((pad + 22, pad + 136), "SELECT price, qty", font=M15, fill=C(MUT))
        d.text((pad + 22, pad + 162), "FROM order_items", font=M15, fill=C(MUT))
        d.text((pad + 22, pad + 196), "15.000.000đ", font=B36B, fill=C(TXT))

    def inner_c(im, d, pad):
        d.text((pad + 22, pad + 146), "#DH001", font=M22, fill=C(TXT))

    pa = seg(t, b3 + 0.25, b3 + 0.8)
    pb = seg(t, b3 + 0.45, b3 + 1.0)
    pc = seg(t, b3 + 0.65, b3 + 1.2)
    panel(base, 360, 560, 340, 280, pa, CYAN, "monitor", "01 · FRONTEND", "Gửi yêu cầu", t, inner_a)
    panel(base, 960, 560, 400, 290, pb, VIOLET, "server", "02 · BACKEND", "Tính lại từ DB", t, inner_b)
    panel(base, 1500, 540, 310, 250, pc, EMER, "database", "03 · ORDERS", "Lưu đơn", t, inner_c)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    qab = seg(t, b3 + 0.6, b3 + 1.1)
    qbc = seg(t, b3 + 0.8, b3 + 1.3)
    beam(d, 545, 745, 560, qab, CYAN, VIOLET, t)
    beam(d, 1175, 1330, 560, qbc, VIOLET, EMER, t)
    if qab > 0.95:
        packets(d, 552, 738, 560, t, CYAN, n=2, speed=0.3)
    if qbc > 0.95:
        packets(d, 1182, 1323, 560, t, EMER, n=2, speed=0.3)
    draw_marker_circle(d, 894, 634, 134, 34, seg(t, st["s0603"] + 0.15, st["s0603"] + 0.95),
                       C(AMBER), 5, seed=2)
    draw_marker(d, 216, 636, 500, 636, seg(t, st["s0604"] + 0.2, st["s0604"] + 0.65),
                C(RED), 6, seed=5)
    base.alpha_composite(ov)

    chip(base, "client sửa được", RED, 360, 732, seg(t, st["s0604"] - 0.05, st["s0604"] + 0.35),
         16, 10, 0.9)
    chip(base, "nguồn tin cậy · DB", EMER, 960, 740, seg(t, st["s0603"] + 0.3, st["s0603"] + 0.7),
         16, 10, 0.9)
    pul = 0.5 + 0.5 * math.sin(t * 3.4)
    status_pill(base, 1500, 622, "PENDING_PAYMENT", AMBER,
                seg(t, st["s0605"] - 0.1, st["s0605"] + 0.4), 16, False, pul)


# ---------- phase 4: webhook + xác minh ----------
def phase4(base, t, st, b4, durs):
    p1 = seg(t, b4, b4 + 0.55)
    p2 = seg(t, b4 + 0.18, b4 + 0.73)

    def inner_bank(im, d, pad):
        d.rounded_rectangle([pad + 20, pad + 146, pad + 340, pad + 218], 12,
                            fill=(12, 19, 34, 240), outline=C(EMER, 70), width=1)
        d.text((pad + 34, pad + 158), "POST /webhooks/bank", font=M15, fill=(214, 232, 250, 255))
        d.text((pad + 34, pad + 188), "{ txn, amount, signature }", font=M15, fill=C(MUT))

    def inner_back(im, d, pad):
        ic = icon_rgba("shield-check", hx(VIOLET)).resize((44, 44), Image.LANCZOS)
        im.alpha_composite(ic, (pad + 26, pad + 152))
        d.text((pad + 84, pad + 160), "xác minh chữ ký", font=B18, fill=C(MUT))
        d.text((pad + 84, pad + 188), "rồi cập nhật", font=B18, fill=C(MUT))

    panel(base, 330, 460, 360, 240, p1, EMER, "building-2", "BANK SERVER", "Ngân hàng", t, inner_bank)
    panel(base, 1000, 460, 400, 240, p2, VIOLET, "server", "BACKEND", "/webhooks/bank", t, inner_back)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    qw = seg(t, b4 + 0.55, b4 + 1.05)
    beam(d, 515, 795, 460, qw, EMER, VIOLET, t)
    if qw > 0.95:
        packets(d, 522, 788, 460, t, EMER)
    base.alpha_composite(ov)
    chip(base, "webhook", EMER, 655, 404, seg(t, b4 + 0.7, b4 + 1.0), 16, 12, 0.9)

    # checklist
    pq = seg(t, b4 + 0.5, b4 + 1.0)
    if pq > 0:
        w, h = 380, 350
        im, pad = shadow_card(w, h, 24, border=C(EMER, 74), fill=(22, 33, 57, 240))
        di = ImageDraw.Draw(im)
        pul = 0.5 + 0.5 * math.sin(t * 2.6)
        di.line([pad + 24, pad + 1, pad + w - 24, pad + 1], fill=C(EMER, int(70 + 60 * pul)), width=2)
        tile = Image.new("RGBA", (54, 54), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.rounded_rectangle([0, 0, 53, 53], 15, fill=C(EMER, 30), outline=C(EMER, 110), width=1)
        ic = icon_rgba("shield-check", hx(EMER)).resize((32, 32), Image.LANCZOS)
        tile.alpha_composite(ic, (11, 11))
        im.alpha_composite(tile, (pad + 24, pad + 20))
        tracked(di, (pad + 92, pad + 38), "XÁC MINH", M15, C(EMER), 2)
        di.text((pad + 24, pad + 84), "Kiểm tra", font=B32S, fill=C(TXT))
        di.text((pad + 24, pad + 124), "trước khi cập nhật", font=B18, fill=C(MUT))
        rows = [("Chữ ký HMAC", "circle-check", EMER),
                ("Mã giao dịch khớp", "circle-check", EMER),
                ("Số tiền khớp", "circle-check", EMER),
                ("FOR UPDATE · transaction", "lock", AMBER)]
        fr = (0.28, 0.48, 0.68, 0.86)
        for i, (lab, icn, col) in enumerate(rows):
            rp = seg(t, st["s0610"] + durs["s0610"] * fr[i], st["s0610"] + durs["s0610"] * fr[i] + 0.3)
            if rp <= 0:
                continue
            yy = pad + 172 + i * 44
            ic2 = icon_rgba(icn, hx(col)).resize((22, 22), Image.LANCZOS)
            ic2.putalpha(ic2.getchannel("A").point(lambda v: int(v * rp)))
            im.alpha_composite(ic2, (pad + 24, yy - 11))
            di.text((pad + 58, yy), lab, font=M16,
                    fill=C(col if col == AMBER else TXT, int(255 * rp)), anchor="lm")
        e = 1 - (1 - pq) ** 3
        sc = 0.87 + 0.13 * e
        if abs(sc - 1) > 0.004:
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
        blit(base, im, 1470, 460, min(1, pq * 1.45), 12)

    # pipeline trạng thái
    q0 = seg(t, b4 + 0.9, b4 + 1.3)
    q1 = seg(t, st["s0611"] + durs["s0611"] * 0.30, st["s0611"] + durs["s0611"] * 0.30 + 0.4)
    q2 = seg(t, st["s0611"] + durs["s0611"] * 0.58, st["s0611"] + durs["s0611"] * 0.58 + 0.4)
    status_pill(base, 500, 730, "PENDING_PAYMENT", AMBER, q0, 16)
    status_pill(base, 830, 730, "PAID", EMER, q1, 16, True)
    status_pill(base, 1170, 730, "PROCESSING", CYAN, q2, 16, False)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    beam(d, 625, 745, 730, q1, AMBER, EMER, t)
    beam(d, 925, 1075, 730, q2, EMER, CYAN, t)
    base.alpha_composite(ov)
    chip(base, "✕ sai bước 7 → không cập nhật", RED, 1430, 690,
         seg(t, st["s0612"] - 0.05, st["s0612"] + 0.4), 16, 10, 0.92)


# ---------- phase 5: kết mẫu ----------
def phase5(base, t, st, b5, total):
    q = lin(t, b5, b5 + 0.8)
    if q <= 0:
        return
    base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(196 * q))))
    paste_brand(base, 960, 320, 150, q)
    d = ImageDraw.Draw(base)
    tracked(d, (960, 432), "AN TECH ACADEMY", font("BeVietnamPro-SemiBold.ttf", 26),
            C(TXT, int(255 * q)), 4, q, "mm")
    d.text((960, 492), "TÍCH HỢP THANH TOÁN NGÂN HÀNG",
           font=font("BeVietnamPro-SemiBold.ttf", 40), fill=C(TXT, int(255 * q)), anchor="mm")
    d.text((960, 546), "Bản đầy đủ 7 phút · Hẹn gặp lại", font=B24R,
           fill=C(MUT, int(255 * q)), anchor="mm")
    for i, (txt_, col, cx) in enumerate((("Node.js", EMER, 830), ("MySQL", CYAN, 960),
                                        ("Webhook", AMBER, 1090))):
        qq = seg(t, b5 + 0.5 + i * 0.12, b5 + 0.85 + i * 0.12)
        if qq > 0:
            chip(base, txt_, col, cx, 610, qq, 16, 10, 0.92)


# ---------- ghép ----------
def make_draw(tl, total, bounds, durs):
    st = tl
    b2, b3, b4, b5 = bounds
    talk = [(st[c[0]], st[c[0]] + durs[c[0]]) for c in CUES]

    def draw(t):
        base = stage_bg(t)
        header(base, t)
        if t < b2:
            phase1(base, t, st)
            pose = "wave" if t < st["s0102"] else "present"
        elif t < b3:
            phase2(base, t, st, b2)
            pose = "point_left"
        elif t < b4:
            phase3(base, t, st, b3)
            pose = "write"
        elif t < b5:
            phase4(base, t, st, b4, durs)
            pose = "present"
        else:
            phase5(base, t, st, b5, total)
            pose = "wave"
        talk_on = any(a <= t < b for a, b in talk)
        qa = seg(t, 0.9, 1.5)
        an_sprite(base, t, pose, talk_on, qa)
        for c in CUES:
            stc, dd = st[c[0]], durs[c[0]]
            if stc <= t < stc + dd + 0.15:
                pin = seg(t, stc, stc + 0.3)
                pout = 1 - seg(t, stc + dd - 0.15, stc + dd + 0.15)
                caption(base, CAPS[c[0]], pin * pout, (1 - back(pin)) * 26 - (1 - pout) * 14)
                break
        qf = lin(t, total - 0.8, total - 0.05)
        if qf > 0:
            base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(255 * qf))))
        im = camera(base, t, total, (b2, b3, b4, b5))
        wq = seg(t, 0.25, 0.85) * (1 - qf)
        if wq > 0:
            brand_watermark(im, size=120, alpha=0.9 * wq, pos="tr", margin=28)
        return im

    return draw


# ---------- sfx ----------
def _pitch(x, r):
    n = max(1, int(len(x) / r))
    return np.interp(np.arange(n) * r, np.arange(len(x)), x)


def build_sfx(tl, durs, total, bounds):
    st = tl
    b2, b3, b4, b5 = bounds
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
    CL = sfx.sfx("click")
    TH = sfx.sfx("thud")
    CH = sfx.sfx("chime")
    SU = sfx.sfx("success")
    MK = sfx.sfx("marker", 0.55)

    put(_pitch(W0, 0.85), 0.12, 0.17)
    put(PO, 0.44, 0.09)
    put(TH, st["s0102"] - 0.05, 0.12)
    put(PO, st["s0102"] + 0.03, 0.07)
    put(_pitch(W0, 1.12), 0.85, 0.08)
    put(PO, 1.4, 0.06)
    put(_pitch(W0, 1.0), b2 - 0.12, 0.15)
    put(PO, b2 + 0.28, 0.08)
    put(TK, b2 + 0.40, 0.06)
    put(PO, b2 + 0.55, 0.08)
    put(_pitch(W0, 1.18), st["s0202"] - 0.1, 0.08)
    put(PO, st["s0202"] + 0.25, 0.07)
    put(_pitch(W0, 0.94), b3 - 0.12, 0.16)
    for k in range(4):
        put(TK, b3 + 0.12 + k * 0.09, 0.05)
    put(TH, b3 + 0.32, 0.14)
    put(PO, b3 + 0.36, 0.07)
    put(TH, b3 + 0.52, 0.12)
    put(PO, b3 + 0.56, 0.07)
    put(TH, b3 + 0.72, 0.12)
    put(MK, st["s0603"] + 0.2, 0.18)
    put(CL, st["s0604"] + 0.3, 0.12)
    put(CL, st["s0604"] + 0.42, 0.10)
    put(TH, st["s0605"] + 0.15, 0.13)
    put(TK, st["s0605"] + 0.55, 0.06)
    put(_pitch(W0, 1.06), b4 - 0.12, 0.15)
    put(TH, b4 + 0.28, 0.13)
    put(PO, b4 + 0.32, 0.07)
    dd = durs["s0610"]
    for fr in (0.30, 0.50, 0.70):
        put(TK, st["s0610"] + dd * fr, 0.07)
    put(CH, st["s0610"] + dd * 0.9, 0.07)
    put(TH, st["s0611"] + 0.1, 0.11)
    put(SU, st["s0611"] + durs["s0611"] * 0.55, 0.10)
    put(sfx.sfx("deny"), st["s0612"] + 0.15, 0.10)
    put(_pitch(W0, 1.15), b5 - 0.1, 0.14)
    put(SU, b5 + 0.35, 0.08)
    put(CH, b5 + 1.1, 0.05)

    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.30:
        bus *= 0.30 / pk
    elif 0 < pk < 0.22:
        bus *= 0.22 / pk
    return bus


def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    stills = "--stills" in sys.argv

    paths = [synth(sid, txt) for sid, txt, _ in CUES]
    durs = {c[0]: len(decode(p)) / SR for c, p in zip(CUES, paths)}
    tl = {}
    t = 0.40
    for sid, txt, pause in CUES:
        tl[sid] = t
        t += durs[sid] + pause
    total = t + 4.4
    print("CUES", {k: (round(v, 2), round(durs[k], 2)) for k, v in tl.items()}, flush=True)
    print("TOTAL", round(total, 2), "s", flush=True)

    b2 = tl["s0201"] - 0.25
    b3 = tl["s0603"] - 0.25
    b4 = tl["s0610"] - 0.25
    b5 = tl["s0612"] + durs["s0612"] + 0.35
    bounds = (b2, b3, b4, b5)
    draw = make_draw(tl, total, bounds, durs)

    if stills:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        picks = [1.2, tl["s0102"] + 1.0, tl["s0201"] + 1.2, tl["s0603"] + 1.0,
                 tl["s0604"] + 1.0, tl["s0610"] + durs["s0610"] * 0.7,
                 tl["s0611"] + durs["s0611"] * 0.8, tl["s0612"] + 0.8, total - 1.2]
        for i, tt in enumerate(picks):
            draw(tt).convert("RGB").save(f"{sd}/still_{i}_{tt:.1f}.png")
            print("STILL", i, round(tt, 2), flush=True)
        return

    n = int(total * FPS)
    mix = np.zeros(int(total * SR) + SR)
    for sid, txt, pause in CUES:
        x = decode(f"{AUD}/{sid}.wav")
        s0 = int(tl[sid] * SR)
        mix[s0:s0 + len(x)] += x
    bus = build_sfx(tl, durs, total, bounds)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = np.max(np.abs(mix))
    print("PEAK", round(pk, 3), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + f"/voice_{TAG}.wav", mix)

    for k in range(n):
        fp = f"{FR}/f{k:04d}.jpg"
        if not os.path.exists(fp):
            draw(k / FPS).convert("RGB").save(fp, quality=92)
        if k % 150 == 0:
            print("frame", k, "/", n, flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/video_{TAG}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")

    mixp = OUT + f"/voice_{TAG}.wav"
    comp = OUT + f"/voice_{TAG}_comp.wav"
    run([FF, "-y", "-i", mixp, "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    mixp = comp
    mm = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", mixp, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr, re.S)[-1]
    mm = json.loads(mm)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:"
          f"measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:"
          f"offset={mm['target_offset']}:linear=true,volume=-0.2dB")
    run([FF, "-y", "-i", mixp, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         OUT + f"/audio_{TAG}.m4a"])
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_{TAG}.m4a", "-c:v", "copy", "-c:a", "copy",
             "-movflags", "+faststart", "-shortest", OUT + f"/{TAG}.mp4"])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
    print("DONE", OUT + f"/{TAG}.mp4", dur(OUT + f"/{TAG}.mp4"), flush=True)


if __name__ == "__main__":
    main()
