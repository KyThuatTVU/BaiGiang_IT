# -*- coding: utf-8 -*-
"""Bài giảng API (~5 phút, 11 cảnh). Bản mẫu dựng S01, S03, S04.
Nền sáng có lưới, giáo viên An xuyên suốt, vector tự dựng, nét vẽ tay, gói request chuyển động.
Ảnh người dùng chỉ dùng làm ngữ cảnh; mọi URL/JSON/mã đều tự vẽ."""
import math
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB, F_BRAND,
                  font, ease, seg, lin, tw, wrap, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, subtitle_band, subs_for, GRID,
                  rich_width)
import character

ROOT = "D:/Edit/Baigiang_API"
IMG = {n: f"{ROOT}/img/{n}.png" for n in (
    "waiter_order", "chef_cook", "kitchen_rush", "fe_be_db", "postman_get", "order_flow_flat",
    "client_server_yellow", "handdrawn_cycle", "fetch_code", "waiter_chef_flat", "rest_cards",
    "thunder_client", "api_neon", "neon_restaurant", "http_deep_dive", "cartoon_cycle")}

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11"]
SAMPLE = ["S01", "S04"]
XFADE = 0.4

ANX = {"S01": (1660, 1020, 0.95), "S03": (1672, 1020, 0.92), "S04": (1660, 1020, 0.95)}
PURPLE = (109, 91, 208, 255)
MINT = (232, 248, 244, 255)
RED_L = (255, 237, 237, 255)
BLUE_L = (110, 156, 255, 255)
AMBER_L = (255, 199, 118, 255)
SKY = (228, 238, 255, 255)
SKY_2 = (240, 246, 255, 255)


def talk(tl, sid, t):
    s = tl[sid]
    return any(st <= t < st + du for st, du in zip(s["starts"], s["durs"]))


def fr(tl, sid, i, a=0.0, b=1.0):
    s = tl[sid]
    return s["starts"][i] + a * s["durs"][i], s["starts"][i] + b * s["durs"][i]


def _base(label=None):
    base = bg_canvas()
    brand_mark(base)
    if label:
        headbar(base, 1.0, label)
    return base, ImageDraw.Draw(base)


def _head(base, title, sub=None, x=100, y=118, p=1.0):
    ftxt(base, x, y, title, F_M, NAVY, p)
    if sub:
        ftxt(base, x, y + 58, sub, F_S, MUT, p)


def _an(base, tl, sid, t, pose="present", look=0):
    x, y, sc = ANX.get(sid, (1660, 1020, 0.95))
    character.paste(base, x, y, t, pose, look, talk(tl, sid, t), sc)


# ---------------------------------------------------------------- text sprites
_fs = {}

F_M = font("BeVietnamPro-SemiBold.ttf", 42)
F_B = font("BeVietnamPro-Regular.ttf", 29)
F_S = font("BeVietnamPro-Regular.ttf", 23)


def font_semi(size):
    if size not in _fs:
        _fs[size] = font("BeVietnamPro-SemiBold.ttf", size)
    return _fs[size]


_tc = {}


def _text_im(text, f, fill):
    key = (text, getattr(f, "path", ""), f.size, fill)
    im = _tc.get(key)
    if im is None:
        w_ = int(rich_width(text, f)) + 6
        im = Image.new("RGBA", (max(1, w_), int(f.size * 1.8)), (0, 0, 0, 0))
        draw_rich(ImageDraw.Draw(im), (0, im.height / 2), text, f, fill, "lm")
        if len(_tc) > 900:
            _tc.clear()
        _tc[key] = im
    return im


def ftxt(base, x, y, text, f, fill, p=1.0, anchor="lm"):
    if p <= 0:
        return 0
    im = _text_im(text, f, fill)
    w_, h_ = im.size
    px = x - (w_ if anchor == "rm" else (w_ / 2 if anchor == "mm" else 0))
    py = y - h_ / 2
    if p < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(px), int(py)))
    return w_


def paste_im(base, im, x, y, p=1.0, anchor="tl"):
    if p <= 0:
        return
    w0, h0 = im.size
    if anchor == "mm":
        x -= w0 / 2
        y -= h0 / 2
    elif anchor == "mt":
        x -= w0 / 2
    elif anchor == "mr":
        x -= w0
        y -= h0 / 2
    if p < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x), int(y)))


# ---------------------------------------------------------------- chrome
def headbar(base, p, label, dark=False):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, int(W * p), 5], fill=AMBER)
    w_ = int(tw(label, F_LBL))
    im = Image.new("RGBA", (w_ + 56, 40), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([0, 0, w_ + 55, 39], 19,
                         fill=(20, 30, 50, 210) if dark else (255, 255, 255, 220),
                         outline=(90, 106, 132, 200) if dark else (214, 222, 234, 255), width=2)
    dd.ellipse([16, 15, 25, 24], fill=AMBER if dark else BLUE)
    draw_rich(dd, (38, 20), label, F_LBL, (226, 234, 246, 255) if dark else MUT, "lm")
    paste_im(base, im, W - w_ - 150, 28, p)


# ---------------------------------------------------------------- photos
_cov = {}
_big = {}
_mask = {}


def _cover(path):
    if path not in _cov:
        _cov[path] = Image.open(path).convert("RGB")
    return _cov[path]


def _bigim(path, w, h):
    key = (path, w, h)
    if key not in _big:
        im = _cover(path)
        s = max(w * 1.16 / im.width, h * 1.16 / im.height)
        _big[key] = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))),
                              Image.BILINEAR)
    return _big[key]


def _rmask(w, h, r):
    key = (w, h, r)
    if key not in _mask:
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
        _mask[key] = m
    return _mask[key]


def kb(path, w, h, t, z0=1.0, z1=1.1, panx=0.0, pany=0.0, radius=16, shadow=True,
       dur=6.0, c0=0.0):
    q = ease(max(0.0, min(1.0, (t - c0) / dur)))
    z = z0 + (z1 - z0) * q
    big = _bigim(path, w, h)
    cw, ch = int(w / z), int(h / z)
    cx = (big.width - cw) / 2 + panx * big.width * (q - 0.5)
    cy = (big.height - ch) / 2 + pany * big.height * (q - 0.5)
    cx = max(0, min(big.width - cw, cx))
    cy = max(0, min(big.height - ch, cy))
    crop = big.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
    crop = crop.resize((w, h), Image.BILINEAR).convert("RGBA")
    crop.putalpha(_rmask(w, h, radius))
    if not shadow:
        return crop
    out = Image.new("RGBA", (w + 8, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([4, 8, w + 2, h + 8], radius + 2, fill=(8, 15, 28, 60))
    out.alpha_composite(crop, (2, 2))
    d.rounded_rectangle([2, 2, w + 1, h + 1], radius + 1, outline=(216, 224, 236, 255), width=2)
    return out


def ghost(base, path, x, y, w, h, mix=0.9):
    """Ảnh nền mờ hòa vào màu nền, chỉ còn gợi ý bố cục."""
    im = _cover(path)
    s = max(w / im.width, h / im.height)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    x0 = (im.width - w) // 2
    y0 = (im.height - h) // 2
    im = im.crop((x0, y0, x0 + w, y0 + h))
    im = Image.blend(im, Image.new("RGB", (w, h), BG[:3]), mix).convert("RGBA")
    base.alpha_composite(im, (int(x), int(y)))


def polaroid(base, path, x, y, w, ph, caption, ang, t, p, c0=0.0, cap_color=NAVY,
             tape=None):
    """Ảnh kiểu polaroid: khung trắng, ảnh hơi zoom, xoay nhẹ như dán tay."""
    if p <= 0:
        return
    fh = ph + 76
    im = Image.new("RGBA", (w + 24, fh + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 20, w + 20, fh + 20], 6, fill=(15, 23, 42, 34))
    d.rounded_rectangle([10, 10, w + 16, fh + 16], 6, fill=WHITE,
                        outline=(224, 232, 242, 255), width=2)
    photo = kb(path, w - 32, ph, t, 1.0, 1.06, radius=3, shadow=False, c0=c0, dur=5.5)
    im.alpha_composite(photo, (24, 18))
    if tape is not None:
        tw_, th_ = 112, 27
        tp = Image.new("RGBA", (tw_ + 16, th_ + 16), (0, 0, 0, 0))
        dd = ImageDraw.Draw(tp)
        dd.rounded_rectangle([8, 8, tw_ + 8, th_ + 8], 3, fill=tape[:3] + (228,))
        dd.line([12, th_ + 6, tw_ + 12, th_ + 6], fill=tape[:3] + (110,), width=3)
        for k in range(3):
            dd.ellipse([26 + k * 32, 17, 32 + k * 32, 23], fill=(255, 255, 255, 55))
        tp = tp.rotate(-4, expand=True, resample=Image.BICUBIC)
        im.alpha_composite(tp, (int(im.width / 2 - tp.width / 2), -1))
    draw_rich(d, (im.width // 2, fh + 2), caption, font_semi(21), cap_color, "mm")
    im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x + w / 2 - im.width / 2), int(y + fh / 2 - im.height / 2)))


def round_photo(base, path, cx, cy, r, t, p, c0=0.0, ring=BLUE, ring_w=4):
    if p <= 0:
        return
    im = kb(path, 2 * r, 2 * r, t, 1.0, 1.07, radius=4, shadow=False, c0=c0, dur=6.0)
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    im.putalpha(m)
    out = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(out)
    dd.ellipse([2, 6, 2 + 2 * r, 6 + 2 * r], outline=ring, width=ring_w)
    out.alpha_composite(im, (4, 4))
    if p < 1:
        out.putalpha(out.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(out, (int(cx - r - 4), int(cy - r - 4)))


# ---------------------------------------------------------------- shapes
def rrect_a(base, box, radius, fill, outline=None, width=2, p=1.0):
    if p <= 0:
        return
    w, h = int(box[2] - box[0]), int(box[3] - box[1])
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([4, 4, w + 4, h + 4], radius, fill=fill, outline=outline, width=width)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(box[0]) - 4, int(box[1]) - 4))


def dot(base, cx, cy, r, color, a=1.0):
    if a <= 0.004:
        return
    r = int(r)
    im = Image.new("RGBA", (2 * r + 4, 2 * r + 4), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse([2, 2, 2 + 2 * r, 2 + 2 * r], fill=color[:3] + (int(255 * min(1.0, a)),))
    base.alpha_composite(im, (int(cx - r - 2), int(cy - r - 2)))


def path_pos(pts, q):
    q = max(0.0, min(1.0, q))
    L = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
         for i in range(len(pts) - 1)]
    tot = sum(L) or 1
    dd = q * tot
    for i, l in enumerate(L):
        if dd <= l or i == len(L) - 1:
            r = dd / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
        dd -= l
    return pts[-1]


def packet(base, pts, q, color=BLUE, r=8, trail=5, ghost_trail=True):
    if q <= 0:
        return
    d = ImageDraw.Draw(base)
    if ghost_trail:
        for k in range(trail, -1, -1):
            qq = q - k * 0.028
            if qq < 0:
                continue
            x, y = path_pos(pts, qq)
            rr = r * (1 - 0.11 * k)
            a = int(255 * (1 - k / (trail + 1)))
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color[:3] + (a,))
    x, y = path_pos(pts, q)
    d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=color[:3] + (46,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def paper(base, pts, q, p=1.0, scale=1.0):
    """Tờ phiếu gọi món bay theo đường đi."""
    if q <= 0 or p <= 0:
        return
    x, y = path_pos(pts, q)
    w_, h_ = int(64 * scale), int(80 * scale)
    im = Image.new("RGBA", (w_ + 10, h_ + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([7, 9, w_ + 7, h_ + 9], 5, fill=(15, 23, 42, 40))
    d.rounded_rectangle([2, 2, w_ + 2, h_ + 2], 5, fill=WHITE, outline=(203, 213, 225, 255), width=2)
    for i, ww in enumerate((0.62, 0.74, 0.5)):
        d.line([12, 22 + i * 15, 12 + (w_ - 24) * ww, 22 + i * 15], fill=(148, 163, 184, 255), width=3)
    d.rectangle([w_ - 22, h_ - 20, w_ - 12, h_ - 10], fill=AMBER)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x - w_ / 2 - 5), int(y - h_ / 2 - 6)))


def plate(base, pts, q, p=1.0):
    """Đĩa thức ăn bưng ngược về khách."""
    if q <= 0 or p <= 0:
        return
    x, y = path_pos(pts, q)
    d = ImageDraw.Draw(base)
    r = 27
    d.ellipse([x - r - 8, y - r - 4, x + r + 8, y + r + 12], fill=(15, 23, 42, 30))
    d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=WHITE,
              outline=(203, 213, 225, 255), width=3)
    d.ellipse([x - r + 6, y - r + 6, x + r - 6, y + r - 6], fill=(255, 236, 210, 255),
              outline=AMBER, width=2)
    d.arc([x - 9, y - 8, x + 9, y + 9], 200, 340, fill=AMBER_D, width=3)


def callout(base, x, y, text, color=TEAL, p=1.0, q=None):
    im = sp_chip(text, color, tint(color, 0.10), 21, None, h=44)
    if q is not None:
        stamp(base, im, x, y, q, p, 0.0, "mm")
    else:
        paste_im(base, im, x, y, p, "mm")


# ---------------------------------------------------------------- playful layer
VIOLET = (139, 92, 246, 255)
INDIGO = (79, 70, 229, 255)
CYAN = (6, 182, 212, 255)
TECH_GRN = (16, 185, 129, 255)
SKY_A = (14, 165, 233, 255)
PARTY = (BLUE, INDIGO, CYAN, VIOLET, TEAL, TECH_GRN, AMBER_D, SKY_A)


def tint(c, k=0.13):
    return tuple(int(255 - (255 - v) * k) for v in c[:3]) + (255,)


def back(q):
    q = max(0.0, min(1.0, q))
    c = 1.9
    return 1 + (c + 1) * (q - 1) ** 3 + c * (q - 1) ** 2


def stamp(base, im, x, y, q, p=1.0, ang=0.0, anchor="mm"):
    """Nảy vào (overshoot) + nghiêng nhẹ khi xuất hiện."""
    if q <= 0 or p <= 0:
        return
    s_ = back(q)
    if abs(s_ - 1) > 0.004 or abs(ang) > 0.01:
        im = im.rotate(ang, expand=True, resample=Image.BICUBIC)
        s_ = max(0.02, s_)
        im = im.resize((max(1, int(im.width * s_)), max(1, int(im.height * s_))), Image.BICUBIC)
    if p < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    paste_im(base, im, x, y, 1.0, anchor)


def star4(dd, cx, cy, r, color, a=255):
    pts = []
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.34
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    dd.polygon(pts, fill=color[:3] + (a,))


def sparkles(base, cx, cy, t, p=1.0, rad=34, n=4, phase=0.0, size=9, color=None):
    if p <= 0:
        return
    box = int(rad * 2 + size * 3)
    im = Image.new("RGBA", (box, box), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    for i in range(n):
        ang = phase + i * 2 * math.pi / n
        x = box / 2 + math.cos(ang) * rad
        y = box / 2 + math.sin(ang) * rad * 0.78
        k = 0.55 + 0.45 * math.sin(t * 4.2 + i * 1.9)
        col = color if color is not None else PARTY[i % len(PARTY)]
        star4(dd, x, y, size * k, col, int(235 * p * min(1.0, k + 0.2)))
    base.alpha_composite(im, (int(cx - box / 2), int(cy - box / 2)))


def confetti(base, cx, cy, t, t0, p=1.0, n=16, spread=210):
    q = lin(t, t0, t0 + 1.5)
    if q <= 0 or q >= 1 or p <= 0:
        return
    box = int(spread * 2)
    im = Image.new("RGBA", (box, box), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    fade = p * (1 - q) ** 0.8
    for i in range(n):
        ang = i * 2.399963 + math.sin(i * 7.13) * 0.5
        spd = 120 + (i * 53 % 120)
        x = box / 2 + math.cos(ang) * spd * q
        y = box / 2 + math.sin(ang) * spd * q * 0.75 + 190 * q * q
        r = 5 + (i * 7) % 5
        col = PARTY[i % len(PARTY)]
        rot = t * 8 + i
        ca, sa = math.cos(rot), math.sin(rot)
        pts = [(x + (dx * ca - dy * sa) * r, y + (dx * sa + dy * ca) * r)
               for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        dd.polygon(pts, fill=col[:3] + (int(235 * fade),))
    base.alpha_composite(im, (int(cx - box / 2), int(cy - box / 2)))


def draw_flow(d, x0, y0, x1, y1, p, color, t, width=4, dash=18, gap=10, head=12):
    """Mũi tên nét đứt chạy dọc theo chiều dữ liệu."""
    if p <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    if L <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    eff = L * p
    off = (t * 52) % (dash + gap)
    dist = -off
    while dist < eff:
        a, b = max(0.0, dist), min(eff, dist + dash)
        if b > a:
            d.line([x0 + ux * a, y0 + uy * a, x0 + ux * b, y0 + uy * b],
                   fill=color, width=width)
        dist += dash + gap
    if p > 0.92:
        ang = math.atan2(y1 - y0, x1 - x0)
        p1 = (x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45))
        p2 = (x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))
        d.polygon([(x1, y1), p1, p2], fill=color)


def icon_tile(base, name, color, cx, cy, r, q, p=1.0, tilt=7.0):
    """Icon trong đĩa màu, hơi nghiêng khi bật vào — kiểu sticker."""
    if q <= 0 or p <= 0:
        return
    s_ = back(q)
    if s_ <= 0.02:
        return
    rr = r * s_
    D = int(rr * 2 + 20)
    im = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    c = D / 2
    dd.ellipse([c - rr - 5, c - rr - 1, c + rr + 5, c + rr + 9], fill=(15, 23, 42, 26))
    dd.ellipse([c - rr, c - rr, c + rr, c + rr], fill=tint(color, 0.16),
               outline=color, width=3)
    ic = sp_icon(name, color, int(rr * 1.14))
    im.alpha_composite(ic, (int(c - ic.width / 2), int(c - ic.height / 2)))
    dd.ellipse([c - rr * 0.55, c - rr * 0.64, c - rr * 0.16, c - rr * 0.25],
               fill=(255, 255, 255, 215))
    im = im.rotate(tilt * math.sin(math.pi * min(1.0, q)), expand=True,
                   resample=Image.BICUBIC)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def bg_dots(base, t, p=1.0):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    specs = ((470, 96, 11, CYAN, 0.0), (742, 118, 7, INDIGO, 1.4),
             (1518, 212, 9, AMBER, 2.2), (1888, 250, 7, TEAL, 0.8),
             (128, 928, 8, VIOLET, 1.9), (1190, 950, 6, SKY_A, 2.6))
    for i, (x, y, r, col, ph) in enumerate(specs):
        xx = x + 7 * math.sin(t * 0.8 + ph)
        yy = y + 5 * math.cos(t * 0.7 + ph * 1.3)
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=tint(col, 0.42))


def code_strip(base, x, y, method, path, status, p=1.0, h=72):
    """Dải terminal nhỏ: method + path + status, tông tech."""
    if p <= 0:
        return
    fs = font("JetBrainsMono-var.ttf", 17)
    w = 66 + int(tw(method, fs)) + 14 + int(tw(path, fs)) + 26 + int(tw(status, fs))
    im = Image.new("RGBA", (w + 10, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 10, w + 2, h + 8], 14, fill=(8, 15, 28, 55))
    d.rounded_rectangle([4, 4, w + 2, h + 4], 12, fill=(15, 23, 42, 245),
                        outline=(51, 65, 85, 255), width=2)
    for k, col in enumerate((CYAN, AMBER, TECH_GRN)):
        d.ellipse([22 + k * 19, 15, 31 + k * 19, 24], fill=col)
    d.line([18, 36, w - 12, 36], fill=(51, 65, 85, 255), width=1)
    draw_rich(d, (20, 54), "›", fs, (148, 163, 184, 255), "lm")
    draw_rich(d, (38, 54), method, fs, CYAN if method == "GET" else AMBER, "lm")
    mx = 38 + int(tw(method, fs)) + 14
    draw_rich(d, (mx, 54), path, fs, (226, 234, 246, 255), "lm")
    draw_rich(d, (w - 16, 54), status, fs, TECH_GRN, "rm")
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x) - 4, int(y) - 4))


def bg_tech(base, t, p=1.0):
    """Lớp nền IT: vệt mạch in, chấm hàn, dải nhị phân và quầng indigo/cyan."""
    if p <= 0:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([1360, -360, 2320, 440], fill=(79, 70, 229, 15))
    d.ellipse([-440, 640, 480, 1460], fill=(6, 182, 212, 13))
    traces = (
        [(0, 296), (128, 296), (128, 224), (262, 224)],
        [(W, 782), (1732, 782), (1732, 606), (1592, 606)],
        [(0, 812), (92, 812), (92, 700), (196, 700)],
        [(W, 246), (1810, 246), (1810, 132), (1694, 132)],
        [(352, H), (352, 936), (268, 936), (268, 862)],
    )
    for i, pts in enumerate(traces):
        jx = 4 * math.sin(t * 0.5 + i * 1.3)
        d.line([(px + jx, py) for px, py in pts], fill=(79, 70, 229, 30),
               width=2, joint="curve")
        for k in (0, 1):
            xx, yy = pts[-1] if k else pts[0]
            d.rectangle([xx - 5, yy - 5, xx + 5, yy + 5],
                        outline=(6, 182, 212, 46), width=2)
    fb = font("JetBrainsMono-var.ttf", 14)
    for j, (x, y0, txt) in enumerate((
            (22, 330, "0100 1011 0110"),
            (22, 470, "1001 0110 1100"),
            (W - 196, 380, "1101 0010 0111"),
            (W - 196, 520, "0011 1010 1001"))):
        draw_rich(d, (x, y0), txt, fb, (79, 70, 229, 32) if j % 2 == 0
                  else (6, 182, 212, 30), "lm")
    if p < 1:
        ov.putalpha(ov.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(ov)


def code_window(base, x, y, w, h, title, lines, p=1.0):
    """Cửa sổ IDE tối: thanh tiêu đề, số dòng, code tô màu cú pháp."""
    if p <= 0:
        return
    im = Image.new("RGBA", (w + 16, h + 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 16, w + 6, h + 12], 16, fill=(2, 6, 16, 60))
    d.rounded_rectangle([6, 6, w + 2, h + 4], 14, fill=(11, 18, 34, 248),
                        outline=(48, 63, 88, 255), width=2)
    tab = 36
    d.rounded_rectangle([6, 6, w + 2, 6 + tab], 14, fill=(19, 28, 46, 255))
    d.rectangle([6, 24, w + 2, 6 + tab], fill=(19, 28, 46, 255))
    for k, col in enumerate((CYAN, AMBER, TECH_GRN)):
        d.ellipse([20 + k * 20, 17, 31 + k * 20, 28], fill=col)
    draw_rich(d, (86, 22), title, font("JetBrainsMono-var.ttf", 14),
              (148, 163, 184, 255), "lm")
    fl = font("JetBrainsMono-var.ttf", 16)
    yy = 6 + tab + 18
    for i, (code, col) in enumerate(lines):
        draw_rich(d, (18, yy), f"{i + 1:>2}", fl, (71, 85, 105, 255), "lm")
        draw_rich(d, (54, yy), code, fl, col, "lm")
        yy += 24
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x) - 6, int(y) - 6))


def server_rack(base, x, y, w, h, p=1.0, t=0.0, label="SERVER · API"):
    """Tủ rack 3 tầng, đèn LED cyan nhấp nháy — hình minh hoạ hạ tầng IT."""
    if p <= 0:
        return
    im = Image.new("RGBA", (w + 18, h + 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 16, w + 8, h + 12], 14, fill=(2, 6, 16, 55))
    d.rounded_rectangle([6, 6, w + 2, h + 4], 12, fill=(13, 22, 39, 250),
                        outline=(45, 60, 84, 255), width=2)
    units = 3
    uh = (h - 20) // units
    for u in range(units):
        uy = 12 + u * uh
        d.rounded_rectangle([16, uy, w - 10, uy + uh - 9], 6, fill=(20, 31, 52, 255),
                            outline=(42, 58, 82, 255))
        for r in range(2):
            for c in range(6):
                d.rounded_rectangle([26 + c * 17, uy + 11 + r * 14,
                                     38 + c * 17, uy + 17 + r * 14], 2,
                                    fill=(63, 82, 112, 255))
        blink = math.sin(t * 3.4 + u * 1.9) > -0.25
        d.ellipse([w - 28, uy + uh - 26, w - 18, uy + uh - 16],
                  fill=CYAN if blink else (28, 58, 78, 255))
    draw_rich(d, (10, h + 20), label, font("JetBrainsMono-var.ttf", 13),
              (100, 116, 139, 255), "lm")
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x) - 6, int(y) - 6))


# ================================================================ S01 — HOOK
F_S01 = font("BeVietnamPro-Bold.ttf", 108)


def draw_S01(t, tl):
    base, d = _base("01 · MỞ ĐẦU")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S01"]
    q1 = seg(t, 0.12, 0.85)
    ftxt(base, 100, 104, "CHUYÊN ĐỀ WEB  ·  5 PHÚT", F_S, AMBER_D, q1)
    ftxt(base, 98, 206, "API", F_S01, NAVY, q1)
    ftxt(base, 98, 342, "LÀ GÌ?", F_S01, BLUE, seg(t, 0.35, 1.0))
    ftxt(base, 102, 486, "Giao diện lập trình ứng dụng", F_M, NAVY, seg(t, 0.5, 1.0))
    desc = wrap("Bộ quy tắc để frontend và backend nói chuyện với nhau.", F_B, 700)
    for i, ln in enumerate(desc):
        ftxt(base, 102, 548 + i * 42, ln, F_B, MUT, seg(t, 0.68 + i * 0.08, 1.0))

    sparkles(base, 468, 296, t, seg(t, 0.8, 1.3) * (1 - seg(t, 4.6, 5.2)),
             rad=40, n=5, size=11)

    s2 = s["starts"][1]
    polaroid(base, IMG["waiter_order"], 888, 148, 268, 188, "BỒI BÀN", -5, t,
             seg(t, 1.0, 1.7), c0=1.0, tape=BLUE)
    polaroid(base, IMG["chef_cook"], 1166, 232, 268, 188, "NHÀ BẾP", 6, t,
             seg(t, 1.25, 1.95), c0=1.25, tape=CYAN)
    confetti(base, 1030, 300, t, s2 + 0.9, n=10, spread=150)
    confetti(base, 1310, 360, t, s2 + 1.15, n=10, spread=150)

    t3 = s["starts"][2] if len(s["starts"]) > 2 else s["total"] + 1
    qc = seg(t, s2 + 0.35, s2 + 1.0) * (1 - seg(t, t3 - 0.3, t3 + 0.15))
    if qc > 0:
        draw_conn(d, 986, 540, 1330, 540, qc, BLUE, width=4, hand=True, seed=3)
        qdot = lin(t, s2 + 1.0, s2 + 2.2)
        if 0 < qdot < 1:
            packet(base, [(986, 540), (1330, 540)], qdot, AMBER, 9, 5)
    q3 = seg(t, t3 + 0.02, t3 + 0.55)
    if q3 > 0:
        bx0, by0, bw, bh = 100, 640, 430, 104
        rrect_a(base, (bx0, by0, bx0 + bw, by0 + bh), 20, NAVY, None, 0, q3)
        d.rounded_rectangle([bx0, by0, bx0 + 10, by0 + bh], 5, fill=AMBER)
        ic = sp_icon("link", WHITE, 44)
        base.alpha_composite(ic, (bx0 + 28, by0 + 30))
        ftxt(base, bx0 + 92, by0 + 46, "API", font("BeVietnamPro-Bold.ttf", 44), WHITE, q3)
        ftxt(base, bx0 + 94, by0 + 82, "cầu nối hai phần mềm", font("BeVietnamPro-Medium.ttf", 21), AMBER_L, q3)
        sparkles(base, bx0 + bw + 26, by0 + bh / 2, t, q3, rad=44, n=5, size=10)
        confetti(base, bx0 + bw + 120, by0 + 30, t, t3 + 0.15, n=12, spread=150)

    code_strip(base, 100, 800, "GET", "/api/mon-an", "200 OK",
               seg(t, s2 + 0.3, s2 + 0.9))
    code_window(base, 996, 664, 500, 196, "app.js — đặt món",
                (("const res = await fetch('/api/order', {", (226, 234, 246, 255)),
                 ("  method: 'POST',", (245, 165, 36, 255)),
                 ("  body: JSON.stringify(monAn)", (16, 185, 129, 255)),
                 ("});", (226, 234, 246, 255)),
                 ("if (res.ok) toast('Đã đặt món!')", (6, 182, 212, 255))),
                seg(t, s2 + 0.55, s2 + 1.15))

    draw_marker(d, 100, 418, 504, 418, seg(t, 0.9, 1.25), AMBER, 7, 3)

    pose = "wave" if t < s2 - 0.2 else ("point_left" if t < t3 else "present")
    _an(base, tl, "S01", t, pose, look=-1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    s = tl["S01"]
    ev = [(0.25, "chime", None, 0.45), (s["starts"][1] - 0.5, "whoosh", None, 0.38)]
    if len(s["starts"]) > 2:
        ev.append((s["starts"][2] + 0.05, "pop", None, 0.50))
    return ev


# ================================================================ S02 — VẤN ĐỀ
def _side_card(base, x, y, w, h, title, sub, color, icon, rows, p, q_icon=1.0):
    if p <= 0:
        return
    im = card(w, h, WHITE, tint(color, 0.55), 20, True, 2)
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([16, 12, w - 6, 22], 4, fill=color)
    star4(dd, w - 28, 40, 8, tint(color, 0.30), 235)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (x - 5, y - 5))
    icon_tile(base, icon, color, x + w // 2, y + 84, 42, q_icon)
    ftxt(base, x + w // 2, y + 158, title, font_semi(30), INK, p, "mm")
    ftxt(base, x + w // 2, y + 194, sub, font("BeVietnamPro-Regular.ttf", 20),
         MUT, p, "mm")
    for i, (t1, t2) in enumerate(rows):
        ftxt(base, x + 44, y + 246 + i * 36, "▸", font_semi(20), color, p)
        ftxt(base, x + 70, y + 246 + i * 36, t1, font_semi(21), INK, p)
        ftxt(base, x + 70 + int(tw(t1, font_semi(21))) + 12,
             y + 246 + i * 36, t2, font("BeVietnamPro-Regular.ttf", 19), MUT, p)


def draw_S02(t, tl):
    base, d = _base("02 · VẤN ĐỀ")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S02"]
    st = s["starts"]
    _head(base, "Vì sao cần API?",
          "Frontend và backend: hai thế giới, chưa có quy tắc chung",
          p=seg(t, 0.08, 0.7))
    q1 = seg(t, 0.2, 0.9)
    q2 = seg(t, 0.55, 1.2) if len(st) > 1 else 0
    _side_card(base, 100, 268, 470, 300, "FRONTEND", "MẶT TIỀN",
               BLUE, "smartphone",
               (("Nút bấm", "bấm là có phản hồi"),
                ("Danh sách", "sản phẩm, giá, ảnh")), q1, q1)
    _side_card(base, 1140, 268, 470, 300, "BACKEND", "PHÍA SAU",
               TEAL, "server",
               (("Xử lý nghiệp vụ", "tính toán, kiểm tra"),
                ("Lưu dữ liệu", "database, file, cache")), q2, q2)

    t2 = st[1] if len(st) > 1 else s["total"] + 1
    t3 = st[2] if len(st) > 2 else s["total"] + 1
    # c2: không có quy tắc chung + giá chép cứng khắp nơi
    qbad = seg(t, t2 - 0.1, t2 + 0.5) * (1 - seg(t, t3 - 0.2, t3 + 0.2))
    if qbad > 0:
        d.line([626, 430, 840, 430], fill=RED[:3] + (int(200 * qbad),),
               width=4)
        d.line([880, 430, 1092, 430], fill=RED[:3] + (int(200 * qbad),),
               width=4)
        cx, cy = 864, 430
        d.line([cx - 20, cy - 20, cx + 20, cy + 20],
               fill=RED[:3] + (int(235 * qbad),), width=7)
        d.line([cx - 20, cy + 20, cx + 20, cy - 20],
               fill=RED[:3] + (int(235 * qbad),), width=7)
        im = sp_chip("0 QUY TẮC CHUNG", RED, tint(RED, 0.08), 22, "circle-x", 50)
        stamp(base, im, 875, 330, seg(t, t2, t2 + 0.4), qbad, -2.0)
        prices = ("price = 15.900.000", "price = 15.900.000",
                  "price = 15.900.000", "price = 15.900.000")
        for i, code in enumerate(prices):
            qq = seg(t, t2 + 0.6 + i * 0.5, t2 + 1.0 + i * 0.5)
            if qq <= 0:
                continue
            x = 100 + i * 330
            im2 = Image.new("RGBA", (344, 84), (0, 0, 0, 0))
            dd = ImageDraw.Draw(im2)
            dd.rounded_rectangle([4, 8, 340, 82], 10, fill=(15, 23, 42, 26))
            dd.rounded_rectangle([0, 0, 336, 76], 10, fill=WHITE,
                                 outline=(252, 205, 211, 255), width=2)
            draw_rich(dd, (18, 22), f"MÀN HÌNH {i + 1}", font_semi(16),
                      RED, "lm")
            draw_rich(dd, (18, 52), code, font("JetBrainsMono-var.ttf", 19),
                      NAVY, "lm")
            if qq > 0.55:
                dd.line([18, 52, 18 + int(tw(code, font("JetBrainsMono-var.ttf", 19))), 52],
                        fill=RED[:3] + (230,), width=3)
            stamp(base, im2, x + 168, 712, qq, qbad, 0.0)
        callout(base, 875, 846, "Đổi một cái giá là sửa cả chục chỗ!", RED,
                seg(t, t2 + 2.4, t2 + 2.9) * (1 - seg(t, t3 - 0.2, t3 + 0.2)),
                q=seg(t, t2 + 2.4, t2 + 2.95))

    # c3: quầy giao dịch chung
    q3 = seg(t, t3 - 0.1, t3 + 0.6) if len(st) > 2 else 0
    if q3 > 0:
        im = card(470, 232, WHITE, tint(INDIGO, 0.5), 20, True, 2)
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([16, 12, 464, 22], 4, fill=INDIGO)
        base.alpha_composite(im, (875 - 235 - 5, 348 - 5))
        icon_tile(base, "store", INDIGO, 875, 408, 36, q3)
        ftxt(base, 875, 468, "QUẦY GIAO DỊCH CHUNG", font_semi(28), INK, q3, "mm")
        ftxt(base, 875, 506, "nhận yêu cầu · trả kết quả", font("BeVietnamPro-Regular.ttf", 20),
             MUT, q3, "mm")
        im2 = sp_chip("1 QUY TẮC CHUNG", TECH_GRN, tint(TECH_GRN, 0.10),
                      22, "link", 50)
        stamp(base, im2, 875, 306, seg(t, t3 + 0.3, t3 + 0.8), 1.0, 2.0)
        draw_flow(d, 580, 430, 634, 430, seg(t, t3 + 0.5, t3 + 0.9), BLUE, t)
        draw_flow(d, 1116, 430, 1168, 430, seg(t, t3 + 0.8, t3 + 1.2), TEAL, t)
        im3 = sp_chip("Request →", BLUE, tint(BLUE, 0.10), 17, "send", 36)
        stamp(base, im3, 604, 602, seg(t, t3 + 0.6, t3 + 1.0), 1.0)
        im4 = sp_chip("← Response", TEAL, tint(TEAL, 0.10), 17, "refresh-cw", 36)
        stamp(base, im4, 1140, 602, seg(t, t3 + 0.9, t3 + 1.3), 1.0)
        sparkles(base, 875, 430, t, seg(t, t3 + 1.0, t3 + 1.4), rad=150, n=4, size=8)

    pose = "present" if t < t2 else ("point_left" if t < t3 else "point_right")
    _an(base, tl, "S02", t, pose, look=-1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    s = tl["S02"]
    st = s["starts"]
    ev = [(0.3, "whoosh", None, 0.32), (0.9, "pop", None, 0.35)]
    if len(st) > 1:
        ev.append((st[1] + 0.3, "deny", 0.5, 0.34))
    if len(st) > 2:
        ev.append((st[2] + 0.4, "pop", None, 0.45))
        ev.append((st[2] + 1.0, "success", None, 0.32))
    return ev


# ================================================================ S03 — ĐỊNH NGHĨA
F_XL = font("BeVietnamPro-Bold.ttf", 82)


def _socket(base, cx, cy, p=1.0, color=BLUE):
    if p <= 0:
        return
    im = Image.new("RGBA", (212, 222), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 18, 204, 214], 28, fill=(15, 23, 42, 30))
    d.rounded_rectangle([6, 6, 198, 206], 28, fill=WHITE, outline=color, width=5)
    d.rounded_rectangle([32, 32, 172, 180], 20, fill=ICE, outline=(212, 224, 240, 255), width=2)
    for sx in (82, 122):
        d.rounded_rectangle([sx - 7, 54, sx + 7, 122], 7, fill=NAVY)
    d.ellipse([92, 140, 108, 156], fill=(148, 163, 184, 255))
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(cx - 106), int(cy - 111)))


def _frontend_node(base, x, y, p=1.0):
    if p <= 0:
        return
    im = Image.new("RGBA", (230, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, 226, 118], 16, fill=(15, 23, 42, 26))
    d.rounded_rectangle([0, 0, 226, 112], 16, fill=WHITE, outline=BLUE, width=3)
    ic = sp_icon("smartphone", BLUE, 44)
    im.paste(ic, (20, 34), ic)
    draw_rich(d, (78, 40), "ỨNG DỤNG", font_semi(25), INK, "lm")
    draw_rich(d, (78, 72), "gửi yêu cầu", font("BeVietnamPro-Regular.ttf", 19), MUT, "lm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x), int(y)))


def _backend_node(base, x, y, p=1.0):
    if p <= 0:
        return
    im = Image.new("RGBA", (250, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, 246, 118], 16, fill=(15, 23, 42, 26))
    d.rounded_rectangle([0, 0, 246, 112], 16, fill=WHITE, outline=TEAL, width=3)
    ic = sp_icon("server", TEAL, 44)
    im.paste(ic, (20, 34), ic)
    draw_rich(d, (78, 40), "BACKEND", font_semi(25), INK, "lm")
    draw_rich(d, (78, 72), "xử lý nghiệp vụ", font("BeVietnamPro-Regular.ttf", 19), MUT, "lm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x), int(y)))


def _feature_row(base, y, icon, title, desc, color, p):
    if p <= 0:
        return
    im = Image.new("RGBA", (850, 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 2, 846, 68], 14, fill=tint(color, 0.05),
                        outline=(226, 232, 240, 255), width=2)
    d.rectangle([0, 14, 6, 56], fill=color)
    draw_rich(d, (80, 24), title, font_semi(24), INK, "lm")
    draw_rich(d, (80, 48), desc, font("BeVietnamPro-Regular.ttf", 18), MUT, "lm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(580), int(y)))
    icon_tile(base, icon, color, 626, y + 35, 23, p)


def draw_S03(t, tl):
    base, d = _base("03 · KHÁI NIỆM")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S03"]
    _head(base, "API là gì?",
          "Application Programming Interface — giao diện lập trình ứng dụng",
          p=seg(t, 0.08, 0.7))
    q1 = seg(t, 0.2, 0.85)

    dx, dy, dw, dh = 96, 280, 420, 324
    base.alpha_composite(card(dw, dh), (dx, dy))
    dd = ImageDraw.Draw(base)
    dd.rounded_rectangle([dx + 10, dy + 10, dx + 108, dy + 16], 3, fill=AMBER)
    ftxt(base, dx + 30, dy + 84, "API", F_XL, BLUE, q1)
    ftxt(base, dx + 32, dy + 142, "application programming interface",
         font("JetBrainsMono-var.ttf", 17), MUT, seg(t, 0.32, 0.85))
    dd.line([dx + 30, dy + 178, dx + dw - 30, dy + 178], fill=BORDER, width=2)
    ftxt(base, dx + 30, dy + 212, "Giao diện lập trình ứng dụng", F_SM_M, NAVY, seg(t, 0.4, 0.9))
    ftxt(base, dx + 30, dy + 252, "Bộ quy tắc chung để hai", F_SM, MUT, seg(t, 0.5, 1.0))
    ftxt(base, dx + 30, dy + 282, "phần mềm nói chuyện.", F_SM, MUT, seg(t, 0.56, 1.0))

    s2 = s["starts"][1]
    q2 = seg(t, s2 - 0.1, s2 + 0.5)
    _frontend_node(base, 560, 340, q2)
    _socket(base, 950, 412, seg(t, s2 - 0.05, s2 + 0.45))
    _backend_node(base, 1108, 340, seg(t, s2 + 0.1, s2 + 0.6))

    d2 = ImageDraw.Draw(base)
    draw_flow(d2, 786, 396, 842, 396, seg(t, s2 - 0.1, s2 + 0.2), BLUE, t, width=4)
    draw_flow(d2, 1058, 396, 1106, 396, seg(t, s2 + 0.15, s2 + 0.55), TEAL, t, width=4)
    qdot = lin(t, s2 + 0.5, s2 + 1.9)
    if 0 < qdot < 1:
        packet(base, [(1058, 396), (1106, 396)], qdot, AMBER, 9, 5)

    callout(base, 950, 568, "API = Ổ CẮM ĐIỆN", BLUE,
            seg(t, s2 + 0.25, s2 + 0.75), q=seg(t, s2 + 0.25, s2 + 0.8))
    sparkles(base, 950, 568, t, seg(t, s2 + 0.5, s2 + 0.9), rad=104, n=5, size=8)
    confetti(base, 950, 330, t, s2 + 0.45, n=12, spread=130)
    star4(ImageDraw.Draw(base), 492, 300, 12, AMBER, 235)

    # câu ví dụ
    qq = seg(t, s2 + 0.6, s2 + 1.2)
    if qq > 0:
        rrect_a(base, (96, 610, 486, 700), 14, SKY_2, None, 0, qq)
        d2.rounded_rectangle([96, 610, 102, 700], 3, fill=AMBER)
        ftxt(base, 120, 632, "Cắm phích là có điện.", font_semi(24), NAVY, qq)
        ftxt(base, 120, 666, "Không cần biết nhà máy điện", font("BeVietnamPro-Regular.ttf", 21), MUT, qq)
        ftxt(base, 120, 692, "xây thế nào.", font("BeVietnamPro-Regular.ttf", 21), MUT, qq)
        for k, col in enumerate((BLUE, TEAL, AMBER)):
            d2.ellipse([462, 626 + k * 26, 472, 636 + k * 26], fill=col)

    code_window(base, 100, 724, 386, 160, "GET /api/menu",
                (("GET /api/menu HTTP/1.1", (6, 182, 212, 255)),
                 ("Host: antech.vn", (226, 234, 246, 255)),
                 ("Accept: application/json", (148, 163, 184, 255)),
                 ("← 200 OK · 4 món", (16, 185, 129, 255))),
                seg(t, s2 + 0.9, s2 + 1.5))

    # 3 đặc điểm
    t3 = s["starts"][2] if len(s["starts"]) > 2 else s["total"] + 1
    rows = (("list-checks", "Có quy tắc chung", "Ai gọi cũng theo cùng một luật", BLUE),
            ("workflow", "Có đầu vào — đầu ra", "Gửi yêu cầu, nhận kết quả", CYAN),
            ("box", "Giấu phần xử lý", "Không cần thấy mã nguồn bên trong", AMBER_D))
    code_strip(base, 580, 836, "GET", "/api/menu", "200 OK",
               seg(t, t3 + 0.7, t3 + 1.2))
    for i, (ic, ti, de, col) in enumerate(rows):
        _feature_row(base, 600 + i * 72, ic, ti, de, col,
                     seg(t, t3 + 0.05 + i * 0.22, t3 + 0.5 + i * 0.22))

    draw_marker_circle(d, 950, 412, 112, 116,
                       seg(t, s2 + 0.35, s2 + 1.15), AMBER, 6, 5)

    _an(base, tl, "S03", t, "present" if t < s2 else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    s = tl["S03"]
    ev = [(0.3, "pop", None, 0.40), (s["starts"][1] + 0.25, "marker", 0.6, 0.32)]
    if len(s["starts"]) > 2:
        ev.append((s["starts"][2] + 0.1, "chime", None, 0.26))
    return ev


# ================================================================ S04 — NHÀ HÀNG
def _station(base, x, y, w, h, p=1.0, accent=None):
    """Thẻ trạm trắng, viền màu nhẹ, có bóng đổ."""
    if p <= 0:
        return
    im = card(w, h, WHITE, tint(accent, 0.55) if accent else (226, 232, 240, 255),
              18, True, 2)
    dd = ImageDraw.Draw(im)
    if accent is not None:
        dd.rounded_rectangle([14, 10, w - 6, 19], 4, fill=accent)
        star4(dd, w - 24, 34, 8, tint(accent, 0.30), 235)
    if p < 1:
        im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x) - 5, int(y) - 5))


def draw_S04(t, tl):
    base, d = _base("04 · ẨN DỤ NHÀ HÀNG")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S04"]
    _head(base, "API = anh bồi bàn",
          "Khách gọi món, bồi bàn chuyển phiếu, bếp nấu — ai cũng có vai",
          p=seg(t, 0.08, 0.7))

    CW_, CH_ = 230, 272
    xs = [100, 410, 720, 1030]
    ys = 300
    q1 = seg(t, 0.2, 0.8)

    _station(base, xs[0], ys, CW_, CH_, q1, accent=BLUE)
    icon_tile(base, "users", BLUE, xs[0] + CW_ // 2, ys + 92, 38, q1)
    ftxt(base, xs[0] + CW_ // 2, ys + 154, "KHÁCH", font_semi(27), INK, q1, "mm")
    ftxt(base, xs[0] + CW_ // 2, ys + 190, "Client", F_S, MUT, q1, "mm")

    _station(base, xs[1], ys, CW_, CH_, q1, accent=INDIGO)
    round_photo(base, IMG["waiter_order"], xs[1] + CW_ // 2, ys + 118, 84, t,
                seg(t, 0.35, 0.95), c0=0.3, ring=INDIGO, ring_w=5)
    ftxt(base, xs[1] + CW_ // 2, ys + 218, "BỒI BÀN", font_semi(27), INK, seg(t, 0.45, 1.0), "mm")
    ftxt(base, xs[1] + CW_ // 2, ys + 250, "API", font_semi(24), INDIGO, seg(t, 0.5, 1.0), "mm")

    _station(base, xs[2], ys, CW_, CH_, q1, accent=TEAL)
    round_photo(base, IMG["chef_cook"], xs[2] + CW_ // 2, ys + 118, 84, t,
                seg(t, 0.45, 1.05), c0=0.4, ring=TEAL, ring_w=5)
    ftxt(base, xs[2] + CW_ // 2, ys + 218, "NHÀ BẾP", font_semi(27), INK, seg(t, 0.55, 1.1), "mm")
    ftxt(base, xs[2] + CW_ // 2, ys + 250, "Backend", font_semi(24), TEAL, seg(t, 0.6, 1.1), "mm")

    _station(base, xs[3], ys, CW_, CH_, q1, accent=AMBER_D)
    icon_tile(base, "database", AMBER_D, xs[3] + CW_ // 2, ys + 92, 38, q1)
    ftxt(base, xs[3] + CW_ // 2, ys + 154, "KHO", font_semi(27), INK, q1, "mm")
    ftxt(base, xs[3] + CW_ // 2, ys + 190, "Database", F_S, MUT, q1, "mm")

    # mũi tên nối các trạm — mỗi chặng một màu, nét chạy
    for i, col in enumerate((BLUE, INDIGO, TEAL)):
        draw_flow(d, xs[i] + CW_ + 4, ys + 136, xs[i + 1] - 10, ys + 136,
                  seg(t, 0.75 + i * 0.15, 1.15 + i * 0.15), col, t, width=4)

    # 6 dòng mapping — mỗi dòng một màu
    pairs = (("Khách", "Client", BLUE), ("Bồi bàn", "API", INDIGO),
             ("Phiếu món", "Request", AMBER_D), ("Bếp", "Backend", TEAL),
             ("Món bưng ra", "Response", TECH_GRN), ("Nguyên liệu", "Database", VIOLET))
    t1 = s["starts"][0]
    for i, (a, b, col) in enumerate(pairs):
        qq = seg(t, t1 + 1.6 + i * 0.55, t1 + 2.1 + i * 0.55)
        if qq <= 0:
            continue
        cx = 100 + (i % 3) * 400
        cy = 640 + (i // 3) * 66
        im = sp_chip(f"{a}  =  {b}", col, tint(col, 0.10), 21, None, 48)
        stamp(base, im, cx + im.width / 2, cy + im.height / 2, qq, 1.0,
              4.0 * math.sin(math.pi * min(1.0, qq)), "mm")

    code_strip(base, 100, 792, "POST", "/orders", "201 Created",
               seg(t, t1 + 4.9, t1 + 5.5))
    server_rack(base, 1246, 700, 188, 146, seg(t, t1 + 4.4, t1 + 5.0), t,
                label="SERVER · BACKEND")

    # c2: phiếu bay sang bếp, đĩa bưng về
    if len(s["starts"]) > 1:
        s2 = s["starts"][1]
        pts_go = [(xs[0] + CW_ + 10, ys + 136), (xs[1] + CW_ // 2, ys + 136),
                  (xs[2] - 10, ys + 136)]
        pts_back = [(xs[2] - 10, ys + 176), (xs[1] + CW_ // 2, ys + 176),
                    (xs[0] + CW_ // 2, ys + 228)]
        qg = lin(t, s2 + 0.2, s2 + 2.0)
        if 0 < qg < 1:
            paper(base, pts_go, min(1.0, qg / 0.55))
            px_, py_ = path_pos(pts_go, min(1.0, qg / 0.55))
            sparkles(base, px_, py_, t, 0.9, rad=26, n=4, size=7, phase=1.0)
        qb = lin(t, s2 + 2.1, s2 + 3.6)
        if qb > 0:
            plate(base, pts_back, qb, seg(t, s2 + 2.1, s2 + 2.4))
            if qb < 1:
                px_, py_ = path_pos(pts_back, qb)
                sparkles(base, px_, py_, t, 0.85, rad=30, n=4, size=7,
                         color=AMBER, phase=0.4)
        t3 = s["starts"][2] if len(s["starts"]) > 2 else s["total"] + 1
        fade2 = 1 - seg(t, t3 - 0.35, t3 - 0.05)
        callout(base, xs[0] + CW_ // 2, 244, "cơm gà của bạn đây!", GREEN,
                seg(t, s2 + 3.4, s2 + 3.9) * fade2,
                q=seg(t, s2 + 3.4, s2 + 3.95))
        sparkles(base, xs[0] + CW_ // 2, 244, t, seg(t, s2 + 3.6, s2 + 4.0) * fade2,
                 rad=70, n=5, size=8)
        confetti(base, xs[0] + CW_ // 2, 222, t, s2 + 3.6, n=14, spread=170)
        star4(ImageDraw.Draw(base), xs[1] + CW_ - 16, ys + 28, 9, CYAN, 220)

    # c3: bồi bàn không nấu ăn — API không tự xử lý
    if len(s["starts"]) > 2:
        t3 = s["starts"][2]
        qc = seg(t, t3 - 0.1, t3 + 0.5)
        if qc > 0:
            im = sp_chip("Bồi bàn KHÔNG nấu ăn — API KHÔNG tự xử lý!",
                         AMBER_D, tint(AMBER_D, 0.10), 22, "alert-triangle", 52)
            stamp(base, im, 875, 244, qc, 1.0, -1.5)
            sparkles(base, 875, 244, t, seg(t, t3 + 0.3, t3 + 0.8), rad=160,
                     n=4, size=8, color=AMBER_D)
            xm = xs[1] + CW_ - 8
            d.line([xm, ys + 128, xm + 26, ys + 128], fill=RED[:3] + (220,), width=4)
            d.line([xm + 4, ys + 122, xm + 22, ys + 134], fill=RED[:3] + (220,), width=4)
            d.line([xm + 4, ys + 134, xm + 22, ys + 122], fill=RED[:3] + (220,), width=4)

    pose = "present" if len(s["starts"]) < 2 or t < s["starts"][1] else "point_left"
    _an(base, tl, "S04", t, pose, look=-1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    s = tl["S04"]
    st = s["starts"]
    ev = [(0.35, "whoosh", None, 0.30), (st[0] + 0.8, "pop", None, 0.35),
          (st[0] + 1.7, "pop", None, 0.30)]
    if len(st) > 1:
        ev += [(st[1] + 0.25, "whoosh", None, 0.38),
               (st[1] + 2.2, "whoosh", None, 0.32),
               (st[1] + 3.5, "success", None, 0.40)]
    if len(st) > 2:
        ev += [(st[2] + 0.1, "marker", 0.45, 0.30),
               (st[2] + 0.6, "pop", None, 0.34)]
    return ev


# ================================================================ S05 — ENDPOINT & URL
def draw_S05(t, tl):
    base, d = _base("05 · ENDPOINT")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S05"]
    st = s["starts"]
    _head(base, "Endpoint & URL",
          "Mỗi endpoint là một địa chỉ để gửi yêu cầu",
          p=seg(t, 0.08, 0.7))
    fm = font("JetBrainsMono-var.ttf", 34)
    segs = (("https://", SKY_A, "giao thức"),
            ("example.com", BLUE_L, "tên miền"),
            ("/api", CYAN, "khu vực API"),
            ("/products", TECH_GRN, "tài nguyên"),
            ("/1", AMBER, "mã sản phẩm"))
    wid = [int(tw(x0, fm)) + 30 for x0, _, _ in segs]
    total = sum(wid) + 44
    x0 = (W - total) // 2
    qb = seg(t, 0.25, 0.9)
    centers = []
    if qb > 0:
        im = Image.new("RGBA", (total + 16, 112), (0, 0, 0, 0))
        d0 = ImageDraw.Draw(im)
        d0.rounded_rectangle([8, 14, total + 8, 108], 18, fill=(6, 10, 22, 60))
        d0.rounded_rectangle([4, 4, total + 4, 100], 16, fill=(11, 18, 34, 250),
                             outline=(48, 63, 88, 255), width=2)
        draw_rich(d0, (22, 52), "›", font("JetBrainsMono-var.ttf", 28),
                  (148, 163, 184, 255), "lm")
        xx = 44
        for i, (txt, col, _) in enumerate(segs):
            draw_rich(d0, (xx, 52), txt, fm, col, "lm")
            centers.append(x0 - 4 + xx + (wid[i] - 30) // 2)
            xx += wid[i]
        if qb < 1:
            im.putalpha(im.getchannel("A").point(lambda a: int(a * qb)))
        base.alpha_composite(im, (x0 - 4, 296))

    # c2: nhãn bóc tách từng phần
    if len(st) > 1:
        for i, (txt, col, lab) in enumerate(segs):
            qq = seg(t, st[1] + 0.35 + i * 0.55, st[1] + 0.75 + i * 0.55)
            if qq <= 0:
                continue
            cx = centers[i]
            d.line([cx, 408, cx, 426], fill=col[:3] + (int(190 * qq),), width=2)
            im = sp_chip(lab, col, tint(col, 0.10), 17, None, 38)
            stamp(base, im, cx, 448, qq, 1.0)
        mq = seg(t, st[1] + 2.4, st[1] + 2.9)
        if mq > 0:
            cx = centers[3]
            draw_marker(d, cx - 92, 414, cx + 92, 414, mq, AMBER, 6, 2)

    # c1: ba quầy endpoint
    cards = (("GET", "/api/products", "sản phẩm", BLUE),
             ("GET", "/api/orders", "đơn hàng", INDIGO),
             ("GET", "/api/users", "người dùng", TEAL))
    for i, (m, pth, lab, col) in enumerate(cards):
        qq = seg(t, 0.9 + i * 0.22, 1.35 + i * 0.22)
        if qq <= 0:
            continue
        x, y = 110 + i * 432, 560
        im = card(392, 132, WHITE, tint(col, 0.55), 18, True, 2)
        base.alpha_composite(im, (x - 5, y - 5))
        chip = sp_chip(m, col, tint(col, 0.12), 17, None, 36)
        stamp(base, chip, x + 40, y + 42, qq, 1.0)
        ftxt(base, x + 26, y + 84, pth, font("JetBrainsMono-var.ttf", 20),
             NAVY, qq)
        ftxt(base, x + 26, y + 112, lab, font("BeVietnamPro-Regular.ttf", 18),
             MUT, qq)

    # c3: cửa + method
    if len(st) > 2:
        t3 = st[2]
        q3 = seg(t, t3, t3 + 0.5)
        callout(base, 960, 742, "Endpoint là cái cửa — method là việc bạn muốn làm.",
                INDIGO, q3, q=seg(t, t3, t3 + 0.55))
        methods = (("GET", "lấy", TECH_GRN), ("POST", "tạo", BLUE),
                   ("PUT", "sửa", AMBER_D), ("DELETE", "xóa", RED))
        ims = [sp_chip(f"{m} · {a}", c, tint(c, 0.10), 19, None, 42)
               for m, a, c in methods]
        tot = sum(im.width for im in ims) + 26 * (len(ims) - 1)
        xx = (W - tot) // 2
        for i, im in enumerate(ims):
            qq = seg(t, t3 + 0.35 + i * 0.2, t3 + 0.75 + i * 0.2)
            stamp(base, im, xx + im.width / 2, 826, qq, 1.0)
            xx += im.width + 26

    _an(base, tl, "S05", t, "present" if t < st[1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    s = tl["S05"]
    st = s["starts"]
    ev = [(0.3, "whoosh", None, 0.32), (0.95, "pop", None, 0.34)]
    if len(st) > 1:
        ev += [(st[1] + 0.3, "marker", 0.5, 0.28), (st[1] + 2.5, "tick", None, 0.3)]
    if len(st) > 2:
        ev.append((st[2] + 0.4, "pop", None, 0.35))
    return ev


# ================================================================ S06 — REQUEST
def draw_S06(t, tl):
    base, d = _base("06 · REQUEST")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S06"]
    st = s["starts"]
    _head(base, "Request — lá phiếu gửi đi",
          "Bốn phần: method · URL · headers · body",
          p=seg(t, 0.08, 0.7))
    lines = (("POST /api/products HTTP/1.1", (245, 165, 36, 255)),
             ("Host: api.antech.vn", (226, 234, 246, 255)),
             ("Content-Type: application/json", (148, 163, 184, 255)),
             ("Authorization: Bearer eyJhbGciOi...", (139, 92, 246, 255)),
             ("{", (226, 234, 246, 255)),
             ('  "ten": "Cơm gà",', (16, 185, 129, 255)),
             ('  "gia": 45000,', (139, 92, 246, 255)),
             ('  "soLuong": 2', (245, 165, 36, 255)),
             ("}", (226, 234, 246, 255)))
    code_window(base, 100, 300, 800, 300, "POST /api/products — request",
                lines, seg(t, 0.2, 0.9))
    imgp = seg(t, st[0] + 0.9, st[0] + 1.5)
    if imgp > 0:
        paste_im(base, kb(IMG["waiter_chef_flat"], 300, 212, t, 1.0, 1.05,
                          c0=st[0] + 0.8), 1170, 300, imgp)
        ftxt(base, 1320, 546, "phiếu → bếp", font_semi(18), TEAL, imgp, "mm")

    # c2: bốn nhãn phần
    if len(st) > 1:
        labs = (("METHOD", 0, AMBER, "send", 332),
                ("URL", 0, CYAN, "globe", 394),
                ("HEADERS", 2, VIOLET, "file-text", 470),
                ("BODY", 5, TECH_GRN, "braces", 560))
        for i, (txt, li, col, icon, cy) in enumerate(labs):
            qq = seg(t, st[1] + 0.3 + i * 0.45, st[1] + 0.7 + i * 0.45)
            if qq <= 0:
                continue
            lx = 902
            ly = 300 + 54 + li * 24
            d.line([lx, ly, lx + 18, ly], fill=col[:3] + (int(200 * qq),), width=2)
            d.line([lx + 18, ly, lx + 18, cy], fill=col[:3] + (int(200 * qq),), width=2)
            im = sp_chip(txt, col, tint(col, 0.10), 18, icon, 40)
            stamp(base, im, 944 + im.width / 2, cy, qq, 1.0)

    # c3: bếp đọc phiếu
    if len(st) > 2:
        t3 = st[2]
        code_strip(base, 100, 700, "POST", "/api/products", "201 Created",
                   seg(t, t3 + 0.2, t3 + 0.8))
        callout(base, 780, 752, "Bếp đọc phiếu là biết nấu gì!", TECH_GRN,
                seg(t, t3 + 0.4, t3 + 0.9), q=seg(t, t3 + 0.4, t3 + 0.95))
        sparkles(base, 1320, 406, t, seg(t, t3 + 0.5, t3 + 0.9), rad=90, n=4, size=8)

    _an(base, tl, "S06", t, "present" if t < st[1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    s = tl["S06"]
    st = s["starts"]
    ev = [(0.3, "pop", None, 0.4)]
    if len(st) > 1:
        ev += [(st[1] + 0.25, "whoosh", None, 0.32),
               (st[1] + 1.2, "tick", None, 0.3)]
    if len(st) > 2:
        ev += [(st[2] + 0.3, "marker", 0.5, 0.28), (st[2] + 0.9, "success", None, 0.32)]
    return ev


# ================================================================ S07 — METHOD + STATUS
def draw_S07(t, tl):
    base, d = _base("07 · METHOD + STATUS")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S07"]
    st = s["starts"]
    _head(base, "Method làm gì? Status nói gì?",
          "Bốn method quen thuộc, CRUD và mã trạng thái",
          p=seg(t, 0.08, 0.7))
    rows = (("GET", "lấy dữ liệu", "Read", TECH_GRN),
            ("POST", "tạo mới", "Create", BLUE),
            ("PUT", "cập nhật toàn bộ", "Update", AMBER_D),
            ("PATCH", "sửa một phần", "Update*", VIOLET),
            ("DELETE", "xóa", "Delete", RED))
    for i, (m, mean, crud, col) in enumerate(rows):
        qq = seg(t, 0.15 + i * 0.33, 0.6 + i * 0.33)
        if qq <= 0:
            continue
        y = 272 + i * 74
        im = Image.new("RGBA", (676, 68), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([4, 6, 670, 66], 12, fill=(15, 23, 42, 26))
        dd.rounded_rectangle([0, 2, 666, 62], 12, fill=tint(col, 0.05),
                             outline=(226, 232, 240, 255), width=2)
        dd.rectangle([0, 12, 6, 52], fill=col)
        draw_rich(dd, (26, 24), m, font("JetBrainsMono-var.ttf", 24), col, "lm")
        draw_rich(dd, (150, 20), mean, font_semi(21), INK, "lm")
        draw_rich(dd, (150, 44), crud, font("BeVietnamPro-Regular.ttf", 16), MUT, "lm")
        if qq < 1:
            im.putalpha(im.getchannel("A").point(lambda a: int(a * qq)))
        base.alpha_composite(im, (96, y))

    # c2: CRUD card
    if len(st) > 1:
        q2 = seg(t, st[1] + 0.1, st[1] + 0.6)
        if q2 > 0:
            im = card(470, 296, WHITE, tint(INDIGO, 0.55), 20, True, 2)
            dd = ImageDraw.Draw(im)
            dd.rounded_rectangle([16, 12, 464, 22], 4, fill=INDIGO)
            paste_im(base, im, 895, 296, q2)
            ftxt(base, 925, 350, "CRUD", font("JetBrainsMono-var.ttf", 30),
                 INDIGO, q2)
            ftxt(base, 1030, 352, "bốn thao tác cơ bản", font("BeVietnamPro-Regular.ttf", 18),
                 MUT, q2)
            cr = (("Create", "POST", BLUE), ("Read", "GET", TECH_GRN),
                  ("Update", "PUT / PATCH", AMBER_D), ("Delete", "DELETE", RED))
            for i, (name, mm, col) in enumerate(cr):
                qq = seg(t, st[1] + 0.45 + i * 0.28, st[1] + 0.85 + i * 0.28)
                if qq <= 0:
                    continue
                cy = 412 + i * 46
                im2 = sp_chip(mm, col, tint(col, 0.10), 14, None, 30)
                stamp(base, im2, 1010 + im2.width / 2, cy, qq, 1.0)
                ftxt(base, 925, cy, name, font_semi(20), INK, qq)
            draw_conn(d, 772, 470, 888, 470, seg(t, st[1] + 0.25, st[1] + 0.75),
                      INDIGO, width=3, hand=True, seed=5)

    # c3: dải status code
    if len(st) > 2:
        t3 = st[2]
        ftxt(base, 100, 664, "2XX THÀNH CÔNG · 4XX LỖI PHÍA CLIENT · 5XX LỖI SERVER",
             font("BeVietnamPro-Medium.ttf", 16), MUT, seg(t, t3, t3 + 0.4))
        sts = (("200 OK", TECH_GRN, 110, 700), ("201 Created", CYAN, 500, 700),
               ("400 gửi sai", AMBER_D, 950, 700),
               ("401 chưa đăng nhập", VIOLET, 110, 772),
               ("404 không thấy", AMBER_D, 560, 772),
               ("500 server lỗi", RED, 1010, 772))
        for i, (txt, col, x, y) in enumerate(sts):
            qq = seg(t, t3 + 0.25 + i * 0.3, t3 + 0.65 + i * 0.3)
            if qq <= 0:
                continue
            im = sp_chip(txt, col, tint(col, 0.10), 19, None, 44)
            stamp(base, im, x + im.width / 2, y, qq, 1.0,
                  3.0 * math.sin(math.pi * min(1.0, qq)))

    _an(base, tl, "S07", t, "present" if t < st[1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    s = tl["S07"]
    st = s["starts"]
    ev = [(0.3, "pop", None, 0.36), (0.7, "tick", None, 0.3)]
    if len(st) > 1:
        ev += [(st[1] + 0.2, "whoosh", None, 0.32),
               (st[1] + 0.8, "tick", None, 0.3)]
    if len(st) > 2:
        ev += [(st[2] + 0.3, "tick", None, 0.32),
               (st[2] + 1.8, "chime", None, 0.3)]
    return ev


# ================================================================ S08 — RESPONSE & JSON
def draw_S08(t, tl):
    base, d = _base("08 · RESPONSE & JSON")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S08"]
    st = s["starts"]
    _head(base, "Response = status + headers + body",
          "Body thường là JSON — dễ đọc cho cả người lẫn máy",
          p=seg(t, 0.08, 0.7))
    lines = (("HTTP/1.1 200 OK", (16, 185, 129, 255)),
             ("Content-Type: application/json", (148, 163, 184, 255)),
             ("{", (226, 234, 246, 255)),
             ('  "id": 1,', (226, 234, 246, 255)),
             ('  "ten": "Cơm gà",', (16, 185, 129, 255)),
             ('  "gia": 45000,', (139, 92, 246, 255)),
             ('  "conHang": true,', (245, 165, 36, 255)),
             ('  "tags": ["món chính", "best-seller"]', (6, 182, 212, 255)),
             ("}", (226, 234, 246, 255)))
    code_window(base, 100, 290, 660, 330, "200 OK — response", lines,
                seg(t, 0.2, 0.9))

    types = (("string", '"Cơm gà"', TECH_GRN), ("number", "45000", VIOLET),
             ("boolean", "true", AMBER_D), ("null", "null", (100, 116, 139, 255)),
             ("object", "{ ... }", CYAN), ("array", "[ ... ]", BLUE))
    for i, (nm, ex, col) in enumerate(types):
        qq = seg(t, st[1] + 0.25 + i * 0.32, st[1] + 0.65 + i * 0.32) \
            if len(st) > 1 else 0
        if qq <= 0:
            continue
        x = 840 + (i % 2) * 310
        y = 300 + (i // 2) * 100
        im = card(285, 76, tint(col, 0.06), tint(col, 0.5), 14, True, 2)
        paste_im(base, im, x - 5, y - 5, qq)
        ftxt(base, x + 20, y + 28, nm, font("JetBrainsMono-var.ttf", 21), col, qq)
        ftxt(base, x + 20, y + 56, ex, font("JetBrainsMono-var.ttf", 15), MUT, qq)

    # c3: stringify / parse
    if len(st) > 2:
        t3 = st[2]
        qa = seg(t, t3 + 0.2, t3 + 0.8)
        draw_flow(d, 320, 712, 1520, 712, qa, INDIGO, t, width=5)
        im = sp_chip("JSON.stringify → gửi đi", INDIGO, tint(INDIGO, 0.10),
                     20, "send", 42)
        stamp(base, im, 920, 676, qa, 1.0)
        qb = seg(t, t3 + 0.9, t3 + 1.5)
        draw_flow(d, 1520, 806, 320, 806, qb, TEAL, t, width=5)
        im2 = sp_chip("← JSON.parse mở ra", TEAL, tint(TEAL, 0.10),
                      20, "braces", 42)
        stamp(base, im2, 920, 842, qb, 1.0)

    _an(base, tl, "S08", t, "present" if t < st[1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    s = tl["S08"]
    st = s["starts"]
    ev = [(0.3, "pop", None, 0.36)]
    if len(st) > 1:
        ev += [(st[1] + 0.3, "tick", None, 0.3),
               (st[1] + 1.2, "whoosh", None, 0.3)]
    if len(st) > 2:
        ev += [(st[2] + 0.4, "pop", None, 0.35), (st[2] + 1.1, "success", None, 0.3)]
    return ev


# ================================================================ S09 — THỰC CHIẾN
def draw_S09(t, tl):
    base, d = _base("09 · THỰC CHIẾN")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S09"]
    st = s["starts"]
    _head(base, "Thực chiến: Node.js + Express",
          "Một server API tối giản — chưa tới 20 dòng",
          p=seg(t, 0.08, 0.7))
    lines = (("const express = require('express');", (226, 234, 246, 255)),
             ("const app = express();", (226, 234, 246, 255)),
             ("app.use(express.json());", (6, 182, 212, 255)),
             ("", (148, 163, 184, 255)),
             ("app.get('/api/products', (req, res) => {", (245, 165, 36, 255)),
             ("  res.json([", (226, 234, 246, 255)),
             ("    { id: 1, ten: 'Cơm gà', gia: 45000 },", (16, 185, 129, 255)),
             ("    { id: 2, ten: 'Bún bò', gia: 50000 }", (16, 185, 129, 255)),
             ("  ]);", (226, 234, 246, 255)),
             ("});", (226, 234, 246, 255)),
             ("", (148, 163, 184, 255)),
             ("app.listen(3000);", (139, 92, 246, 255)),
             ("console.log('Server: 3000');", (148, 163, 184, 255)))
    code_window(base, 100, 290, 860, 390, "server.js", lines, seg(t, 0.2, 0.9))

    qi = seg(t, st[1] + 0.2, st[1] + 0.8) if len(st) > 1 else 0
    if qi > 0:
        paste_im(base, kb(IMG["postman_get"], 400, 270, t, 1.0, 1.05,
                          c0=st[1] + 0.2), 1040, 300, qi)
        ftxt(base, 1240, 598, "POSTMAN · GET /api/products",
             font("JetBrainsMono-var.ttf", 16), MUT, qi, "mm")
        sparkles(base, 1240, 430, t, seg(t, st[1] + 0.6, st[1] + 1.0),
                 rad=110, n=4, size=8, color=CYAN)

    if len(st) > 1:
        code_strip(base, 100, 720, "GET", "/api/products", "200 OK",
                   seg(t, st[1] + 0.6, st[1] + 1.2))

    if len(st) > 2:
        t3 = st[2]
        q3 = seg(t, t3 + 0.2, t3 + 0.8)
        code_window(base, 1040, 620, 474, 156, "app.js — fetch",
                    (("const res = await fetch(endpoint);", (226, 234, 246, 255)),
                     ("const data = await res.json();", (16, 185, 129, 255)),
                     ("render(data); // đổ lên giao diện", (6, 182, 212, 255))),
                    q3)
        im = sp_chip("Frontend không cần biết backend lưu ở đâu",
                     TEAL, tint(TEAL, 0.10), 18, "shield-check", 40)
        stamp(base, im, 1170 + im.width / 2, 812, q3, 1.0)

    _an(base, tl, "S09", t, "present" if t < st[1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    s = tl["S09"]
    st = s["starts"]
    ev = [(0.3, "click", None, 0.45), (0.75, "pop", None, 0.34)]
    if len(st) > 1:
        ev += [(st[1] + 0.4, "tick", None, 0.32), (st[1] + 1.0, "pop", None, 0.3)]
    if len(st) > 2:
        ev += [(st[2] + 0.5, "whoosh", None, 0.3), (st[2] + 1.1, "success", None, 0.32)]
    return ev


# ================================================================ S10 — LỖI + TỔNG KẾT
def draw_S10(t, tl):
    base, d = _base("10 · LỖI + TỔNG KẾT")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S10"]
    st = s["starts"]
    _head(base, "Lỗi hay gặp · Tổng kết",
          "Ba lỗi, ba điều nhớ, một lời hẹn",
          p=seg(t, 0.08, 0.7))
    t2 = st[1] if len(st) > 1 else s["total"] + 1
    f2 = 1 - seg(t, t2 - 0.05, t2 + 0.35)
    errs = (("Quên express.json", "body rỗng", 100),
            ("Quên CORS", "trình duyệt chặn", 570),
            ("Không validate", "tin frontend mù quáng", 1040))
    for i, (ti, de, x) in enumerate(errs):
        qq = seg(t, 0.25 + i * 0.35, 0.8 + i * 0.35) * f2
        if qq <= 0:
            continue
        y = 280
        im = card(420, 220, WHITE, tint(RED, 0.45), 18, True, 2)
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([16, 12, 414, 22], 4, fill=RED)
        if qq < 1:
            im.putalpha(im.getchannel("A").point(lambda a: int(a * qq)))
        base.alpha_composite(im, (x - 5, y - 5))
        icon_tile(base, "alert-triangle", RED, x + 64, y + 84, 34, qq)
        ftxt(base, x + 118, y + 70, ti, font_semi(24), INK, qq)
        ftxt(base, x + 118, y + 104, de, font("BeVietnamPro-Regular.ttf", 19), MUT, qq)
        qs = seg(t, 0.8 + i * 0.35, 1.2 + i * 0.35) * f2
        if qs > 0:
            d.line([x + 30, y + 150, x + 30 + int(360 * qs), y + 178],
                   fill=RED[:3] + (225,), width=5)

    # c2: ba điều nhớ + sơ đồ một dòng
    if len(st) > 1:
        chips = (("API = cầu nối", INDIGO), ("Endpoint = địa chỉ", CYAN),
                 ("Method + status = ngôn ngữ chung", TECH_GRN))
        ims = [sp_chip(txt, col, tint(col, 0.10), 23, None, 50) for txt, col in chips]
        tot = sum(im.width for im in ims) + 28 * (len(ims) - 1)
        xx = (W - tot) // 2
        for i, im in enumerate(ims):
            qq = seg(t, t2 + 0.3 + i * 0.3, t2 + 0.7 + i * 0.3)
            stamp(base, im, xx + im.width / 2, 520, qq, 1.0)
            xx += im.width + 28
        nodes = (("Request", "send", BLUE), ("API", "link", INDIGO),
                 ("JSON", "braces", TECH_GRN), ("Response", "refresh-cw", TEAL))
        nx = (290, 640, 990, 1340)
        for i, (nm, icon, col) in enumerate(nodes):
            qq = seg(t, t2 + 0.9 + i * 0.28, t2 + 1.3 + i * 0.28)
            if qq <= 0:
                continue
            icon_tile(base, icon, col, nx[i], 700, 32, qq)
            ftxt(base, nx[i], 760, nm, font("JetBrainsMono-var.ttf", 18), MUT, qq, "mm")
            if i:
                draw_flow(d, nx[i - 1] + 42, 700, nx[i] - 42, 700,
                          seg(t, t2 + 0.9 + i * 0.28, t2 + 1.35 + i * 0.28), col, t, width=4)

    # c3: bài sau
    if len(st) > 2:
        t3 = st[2]
        q3 = seg(t, t3 + 0.3, t3 + 0.9)
        callout(base, 960, 858, "Bài sau: RESTful · JWT · Bảo mật API", VIOLET,
                q3, q=seg(t, t3 + 0.3, t3 + 0.95))
        sparkles(base, 960, 858, t, seg(t, t3 + 0.6, t3 + 1.0), rad=130, n=4, size=8,
                 color=VIOLET)

    _an(base, tl, "S10", t, "present" if t < t2 else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    s = tl["S10"]
    st = s["starts"]
    ev = [(0.5, "deny", 0.4, 0.32), (1.3, "deny", 0.4, 0.30),
          (2.1, "deny", 0.4, 0.30)]
    if len(st) > 1:
        ev += [(st[1] + 0.2, "chime", None, 0.32), (st[1] + 1.0, "pop", None, 0.3)]
    if len(st) > 2:
        ev.append((st[2] + 0.4, "marker", 0.5, 0.28))
    return ev


# ================================================================ S11 — OUTRO
def draw_S11(t, tl):
    base, d = _base("11 · KẾT")
    bg_tech(base, t)
    bg_dots(base, t)
    s = tl["S11"]
    st = s["starts"]
    q1 = seg(t, 0.15, 0.8)
    ftxt(base, 150, 300, "AN TECH", font("BeVietnamPro-Bold.ttf", 96), NAVY, q1)
    ftxt(base, 150, 408, "ACADEMY", font("BeVietnamPro-Bold.ttf", 96), BLUE,
         seg(t, 0.35, 1.0))
    d.rounded_rectangle([152, 470, 152 + 520, 478], 4, fill=AMBER)
    ftxt(base, 150, 540, "Hiểu công nghệ, làm chủ tương lai!",
         font_semi(38), NAVY, seg(t, 0.6, 1.2))
    ftxt(base, 150, 596, "Cảm ơn các bạn đã theo dõi An Tech Academy.",
         font("BeVietnamPro-Regular.ttf", 25), MUT, seg(t, 0.9, 1.5))

    # mạng lưới công nghệ bên phải
    pts = ((1210, 286), (1400, 236), (1470, 404), (1270, 452))
    qnet = seg(t, 0.5, 1.2)
    if qnet > 0:
        for a, b in ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2)):
            draw_conn(d, pts[a][0], pts[a][1], pts[b][0], pts[b][1], qnet,
                      tint(INDIGO, 0.55), width=2, hand=True, seed=a + b)
        for i, (icon, col) in enumerate((("globe", CYAN), ("server", TECH_GRN),
                                         ("smartphone", BLUE), ("code-xml", VIOLET))):
            icon_tile(base, icon, col, pts[i][0], pts[i][1], 30, qnet)
        pq = lin(t, 1.4, 3.4)
        if 0 < pq < 1:
            packet(base, [pts[0], pts[1], pts[2]], pq, CYAN, 6, 4)

    if len(st) > 1:
        t2 = st[1]
        chips = (("Theo dõi kênh", BLUE, "users"),
                 ("Để lại câu hỏi", CYAN, "message-circle"),
                 ("Hẹn gặp lại!", AMBER_D, "arrow-right"))
        ims = [sp_chip(txt, col, tint(col, 0.10), 21, icon, 46)
               for txt, col, icon in chips]
        tot = sum(im.width for im in ims) + 24 * (len(ims) - 1)
        xx = 150
        for i, im in enumerate(ims):
            qq = seg(t, t2 + 0.3 + i * 0.3, t2 + 0.7 + i * 0.3)
            stamp(base, im, xx + im.width / 2, 690, qq, 1.0)
            xx += im.width + 24
        confetti(base, 1370, 620, t, t2 + 0.5, n=16, spread=210)
        for i in range(4):
            sparkles(base, 160 + i * 220, 760 + (i % 2) * 30, t,
                     seg(t, t2 + 0.5 + i * 0.3, t2 + 0.9 + i * 0.3),
                     rad=26, n=3, size=7, phase=i)

    _an(base, tl, "S11", t, "wave" if t < (st[1] if len(st) > 1 else 9) else "present",
        look=-1)
    subtitle_band(d, subs_for(tl, "S11", t))
    return base


def events_S11(tl):
    s = tl["S11"]
    st = s["starts"]
    ev = [(0.3, "chime", None, 0.45), (1.0, "pop", None, 0.34)]
    if len(st) > 1:
        ev += [(st[1] + 0.4, "whoosh", None, 0.32),
               (st[1] + 1.0, "success", None, 0.34)]
    return ev


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10, "S11": draw_S11}
EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03,
          "S04": events_S04, "S05": events_S05, "S06": events_S06,
          "S07": events_S07, "S08": events_S08, "S09": events_S09,
          "S10": events_S10, "S11": events_S11}
