# -*- coding: utf-8 -*-
"""12 cảnh bài giảng Load Balancer (~5 phút).
Ảnh người dùng cung cấp dùng làm ngữ cảnh (Ken Burns, khung chứng cứ), sơ đồ kỹ thuật
và luồng dữ liệu tự dựng bằng vector. Nhân vật An xuất hiện xuyên suốt."""
import math, re
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB, F_BRAND,
                  font, ease, seg, lin, tw, wrap, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, draw_marker, subtitle_band, subs_for)
import character

ROOT = "D:/Edit/Baigiang_LoadBalancer"
IMG = {n: f"{ROOT}/img/{n}.png" for n in (
    "sale_crowd", "server_overheat", "ops_monitor", "arch_public_ip", "arch_simple",
    "lb_screen", "dc_corridor", "net_fiber", "algo_4up", "algo_wide", "server_fail")}

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"]
XFADE = 0.3

ANX = {"S01": (1668, 930, 0.50), "S02": (66, 926, 0.40), "S03": (1724, 920, 0.38),
       "S04": (1748, 920, 0.37), "S05": (1748, 920, 0.37), "S06": (1752, 920, 0.37),
       "S07": (1752, 920, 0.37), "S08": (1752, 920, 0.37), "S09": (1752, 920, 0.38),
       "S10": (1752, 920, 0.37), "S11": (1836, 920, 0.33), "S12": (1560, 924, 0.56)}
PURPLE = (109, 91, 208, 255)
PURPLE_L = (170, 158, 245, 255)
MINT = (232, 248, 244, 255)
RED_L = (255, 233, 233, 255)
BLUE_L = (110, 156, 255, 255)
TEAL_L = (72, 214, 190, 255)
AMBER_L = (255, 199, 118, 255)
SKY = (224, 236, 255, 255)
DARK = (11, 19, 34, 255)


# ---------------------------------------------------------------- timeline
def talk(tl, sid, t):
    s = tl[sid]
    return any(st <= t < st + du for st, du in zip(s["starts"], s["durs"]))


def fr(tl, sid, i, a=0.0, b=1.0):
    s = tl[sid]
    return s["starts"][i] + a * s["durs"][i], s["starts"][i] + b * s["durs"][i]


def _base():
    base = bg_canvas()
    brand_mark(base)
    return base, ImageDraw.Draw(base)


def _title(base, tl, sid, t, text, sub=None, x=110, y=96, frac=0.04):
    s = tl[sid]
    paste_sprite(base, sp_title(text, sub), x, y,
                 seg(t, s["starts"][0] + frac, s["starts"][0] + frac + 0.55))


def _an(base, tl, sid, t, pose=None, scale=None, look=0):
    x, y, sc = ANX[sid]
    character.paste(base, x, y, t, pose or "present", look=look,
                    talking=talk(tl, sid, t), scale=scale or sc)


_fs = {}


def font_semi(size):
    if size not in _fs:
        _fs[size] = font("BeVietnamPro-SemiBold.ttf", size)
    return _fs[size]


# ---------------------------------------------------------------- text sprites
_tc = {}


def _text_im(text, f, fill):
    key = (text, getattr(f, "path", ""), f.size, fill)
    im = _tc.get(key)
    if im is None:
        w_ = int(tw(text, f)) + 6
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


def pill(text, color=BLUE, fill=WHITE, size=20, h=40, icon=None, iw=22):
    f = font_semi(size)
    w_ = int(tw(text, f)) + 30 + (iw + 8 if icon else 0)
    im = Image.new("RGBA", (w_, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w_ - 1, h - 1], h // 2, fill=fill, outline=color, width=2)
    x = 14
    if icon:
        ic = sp_icon(icon, color, 18)
        im.paste(ic, (x, (h - 18) // 2), ic)
        x += iw + 4
    draw_rich(d, (x, h / 2), text, f, color, "lm")
    return im


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


def shot(base, path, x, y, w, h, p=1.0, t=0.0, z0=1.0, z1=1.1, panx=0, pany=0,
         caption=None, cap_color=BLUE, radius=16, c0=0.0):
    if p <= 0:
        return
    im = kb(path, w, h, t, z0, z1, panx, pany, radius, True, c0=c0)
    paste_im(base, im, x, y, p)
    if caption:
        paste_im(base, sp_chip(caption, cap_color, WHITE, 19, None, h=36),
                 x + 14, y + h - 46, seg(p * 1.3, 0.35, 0.8))


def crop_frac(path, fx0, fy0, fx1, fy1, w, h, radius=12):
    im = _cover(path)
    box = (int(im.width * fx0), int(im.height * fy0), int(im.width * fx1), int(im.height * fy1))
    c = im.crop(box)
    s = max(w / c.width, h / c.height)
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    x0 = (c.width - w) // 2
    y0 = (c.height - h) // 2
    c = c.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")
    c.putalpha(_rmask(w, h, radius))
    return c


def overlay_grad(base, a_left=220, a_right=40, vertical=False, color=(8, 15, 30)):
    """Lớp gradient tối dần sang phải (hoặc dưới lên) để chữ trắng dễ đọc."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    n = 48
    if vertical:
        for i in range(n):
            y0 = int(H * i / n)
            a = int(a_left + (a_right - a_left) * i / (n - 1))
            d.rectangle([0, y0, W, int(H * (i + 1) / n) + 1], fill=color + (a,))
    else:
        for i in range(n):
            x0 = int(W * i / n)
            a = int(a_left + (a_right - a_left) * i / (n - 1))
            d.rectangle([x0, 0, int(W * (i + 1) / n) + 1, H], fill=color + (a,))
    base.alpha_composite(ov)


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


def sheen(base, q, alpha=22):
    if q <= 0 or q >= 1:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x = -460 + q * (W + 1000)
    d.polygon([(x, 0), (x + 280, 0), (x - 180, H), (x - 460, H)],
              fill=(255, 255, 255, alpha))
    base.alpha_composite(ov)


def path_pos(pts, q):
    q = max(0.0, min(1.0, q))
    L = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(L) or 1
    dd = q * tot
    for i, l in enumerate(L):
        if dd <= l or i == len(L) - 1:
            r = dd / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
        dd -= l
    return pts[-1]


def packet(base, pts, q, color=BLUE, r=8, trail=5):
    if q <= 0:
        return
    d = ImageDraw.Draw(base)
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


def ring(base, cx, cy, r, color, p=1.0, w=3):
    if p <= 0 or r <= 0:
        return
    r = int(r)
    im = Image.new("RGBA", (2 * r + 2 * w + 4, 2 * r + 2 * w + 4), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse([w + 1, w + 1, w + 1 + 2 * r, w + 1 + 2 * r],
               outline=color[:3] + (int(220 * p),), width=w)
    base.alpha_composite(im, (int(cx - r - w - 2), int(cy - r - w - 2)))


def dot(base, cx, cy, r, color, a=1.0):
    if a <= 0.004:
        return
    r = int(r)
    im = Image.new("RGBA", (2 * r + 4, 2 * r + 4), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.ellipse([2, 2, 2 + 2 * r, 2 + 2 * r], fill=color[:3] + (int(255 * min(1.0, a)),))
    base.alpha_composite(im, (int(cx - r - 2), int(cy - r - 2)))


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


def node(base, x, y, w, h, icon, label, sub=None, color=BLUE, fill=WHITE, p=1.0,
         icon_size=44, label_size=25, dark=False):
    if p <= 0:
        return
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 5, w, h + 3], 14, fill=(15, 23, 42, 30))
    d.rounded_rectangle([0, 0, w, h], 14, fill=fill, outline=color, width=2)
    ic = sp_icon(icon, color, icon_size)
    im.paste(ic, (20, (h - icon_size) // 2), ic)
    draw_rich(d, (20 + icon_size + 14, h / 2 - (11 if sub else 0)), label,
              font_semi(label_size), (226, 234, 246, 255) if dark else INK, "lm")
    if sub:
        draw_rich(d, (20 + icon_size + 14, h / 2 + 21), sub, font("BeVietnamPro-Regular.ttf", 19),
                  (148, 164, 190, 255) if dark else MUT, "lm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x), int(y)))


def srv_card(base, x, y, w, h, idx, status="ok", p=1.0, load=None, conn=None,
             color=BLUE, sub=None, dark=False):
    """Thẻ máy chủ dùng chung cho các sơ đồ thuật toán."""
    if p <= 0:
        return
    ringc = {"ok": color, "warn": AMBER, "bad": RED, "off": (148, 163, 184, 255)}[status]
    fill = WHITE if not dark else (19, 30, 50, 255)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w, h + 4], 16, fill=(11, 18, 32, 34))
    d.rounded_rectangle([0, 0, w, h], 16, fill=fill, outline=ringc, width=3)
    ic = sp_icon("server", ringc, 38)
    im.paste(ic, (22, 20), ic)
    draw_rich(d, (22 + 50, 39), f"Server {idx:02d}", font_semi(25),
              (232, 238, 248, 255) if dark else INK, "lm")
    if sub:
        draw_rich(d, (22 + 50, 66), sub, font("BeVietnamPro-Regular.ttf", 18),
                  (150, 166, 192, 255) if dark else MUT, "lm")
    if load is not None:
        bx, by, bw = 22, h - 30, w - 80
        d.rounded_rectangle([bx, by, bx + bw, by + 9], 4, fill=(226, 232, 240, 255) if not dark else (40, 54, 78, 255))
        lc = color if load < 0.7 else (AMBER if load < 0.88 else RED)
        d.rounded_rectangle([bx, by, bx + max(2, int(bw * load)), by + 9], 4, fill=lc)
        draw_rich(d, (w - 22, by + 4), f"{int(load * 100)}%", font("BeVietnamPro-Medium.ttf", 18),
                  lc, "rm")
    if conn is not None:
        draw_rich(d, (w - 22, 44), str(conn), font("PlusJakartaSans-var.ttf", 34, 800),
                  ringc, "rm")
        draw_rich(d, (w - 22, 76), "kết nối", font("BeVietnamPro-Regular.ttf", 17), MUT, "rm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.alpha_composite(im, (int(x), int(y)))


# ---------------------------------------------------------------- code panel
def _tok_nginx(line):
    if line.strip().startswith("#"):
        return [(line, (120, 137, 160, 255))]
    out = []
    for part in re.split(r'(\$[A-Za-z_]+|"[^"]*"|\{|\}|;)', line):
        if not part:
            continue
        if part.startswith("$"):
            out.append((part, (124, 170, 255, 255)))
        elif part.startswith('"'):
            out.append((part, (255, 190, 120, 255)))
        elif part in "{};":
            out.append((part, (120, 220, 200, 255)))
        else:
            m = re.match(r"(\s*)([A-Za-z_]+)(.*)$", part)
            if m and m.group(2):
                out.append((m.group(1), (210, 220, 236, 255)))
                word = m.group(2)
                kw = ("upstream", "server", "listen", "location", "proxy_pass",
                      "proxy_set_header", "http", "include")
                out.append((word, (150, 200, 255, 255) if word in kw else (226, 234, 246, 255)))
                out.append((m.group(3), (226, 234, 246, 255)))
            else:
                out.append((part, (226, 234, 246, 255)))
    return out


def code_panel(base, x, y, w, lines, typed=1.0, title="nginx.conf"):
    if typed <= 0:
        return 0
    size, lh, pad = 21, 33, 22
    h = 54 + lh * len(lines) + 18
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 8, w - 3, h - 2], 18, fill=(4, 9, 20, 120))
    d.rounded_rectangle([0, 0, w - 4, h - 8], 18, fill=(13, 21, 38, 255),
                        outline=(70, 86, 116, 255), width=2)
    d.rounded_rectangle([0, 0, w - 4, 48], 18, fill=(22, 33, 55, 255))
    d.rectangle([0, 30, w - 4, 48], fill=(22, 33, 55, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([18 + i * 21, 18, 29 + i * 21, 29], fill=c)
    draw_rich(d, (w - 24, 24), title, font("JetBrainsMono-var.ttf", 18), (140, 158, 186, 255), "rm")
    d.line([0, 48, w - 4, 48], fill=(70, 86, 116, 130), width=2)
    nf = font("JetBrainsMono-var.ttf", size - 4)
    cf = font("JetBrainsMono-var.ttf", size)
    total = sum(len(l) for l in lines)
    budget = int(total * min(1.0, typed))
    yy = 62
    for i, line in enumerate(lines):
        d.text((22, yy), f"{i + 1:02d}", font=nf, fill=(86, 104, 132, 255), anchor="lm")
        xx = 66
        reveal = max(0, min(len(line), budget))
        for tx, col in _tok_nginx(line):
            if reveal <= 0:
                break
            part = tx[:reveal]
            d.text((xx, yy), part, font=cf, fill=col, anchor="lm")
            xx += d.textlength(part, font=cf)
            reveal -= len(tx)
        if typed < 1 and 0 <= budget < len(line) and int(budget * 3) % 2 == 0:
            d.rectangle([xx + 2, yy - 12, xx + 5, yy + 12], fill=AMBER)
        budget -= len(line)
        yy += lh
    base.alpha_composite(im, (int(x), int(y)))
    return h


# ================================================================ S01 — HOOK
def draw_S01(t, tl):
    base, d = _base()
    s = tl["S01"]
    # nền ảnh sale, chuyển động chậm
    bg = kb(IMG["sale_crowd"], W, H, t, 1.04, 1.13, panx=0.05, pany=0.02, radius=0, shadow=False, dur=14)
    base.alpha_composite(bg, (0, 0))
    overlay_grad(base, 238, 70)
    d = ImageDraw.Draw(base)

    # thương hiệu trên nền tối
    draw_tracked(d, (104, 46), "AN TECH ACADEMY", F_BRAND, (240, 245, 255, 235), 3.4, seg(t, 0.1, 0.9))
    d.rounded_rectangle([104, 78, 168, 83], 2, fill=AMBER)
    headbar(base, seg(t, 0.2, 1.2), "BÀI GIẢNG · HẠ TẦNG WEB", dark=True)

    paste_im(base, pill("12.12 MEGA SALE · CASE STUDY", AMBER, (16, 25, 44, 220), 20, 42),
             104, 130, seg(t, 0.2, 0.8))

    f1 = font("BeVietnamPro-Bold.ttf", 104)
    f2 = font("BeVietnamPro-Bold.ttf", 104)
    a = seg(t, 0.1, 0.75)
    ftxt(base, 104, 268, "LOAD", f1, WHITE, a)
    ftxt(base, 104, 386, "BALANCER", f2, AMBER, seg(t, 0.25, 0.95))
    draw_marker(d, 108, 452, 108 + 470, 452, seg(t, 1.3, 2.1), AMBER, 8, 3)
    ftxt(base, 104, 494, "Bí quyết để 5.000 người mua cùng lúc mà web không sập",
         font("BeVietnamPro-Medium.ttf", 30), (228, 236, 250, 255), seg(t, 0.6, 1.2))

    # hai số liệu lớn
    c2a, c2b = fr(tl, "S01", 1, 0.06, 0.9)
    st = seg(t, c2a, c2a + 0.45)
    if st > 0:
        val = int(110000 * ease(min(1.0, (t - c2a) / max(0.8, c2b - c2a))))
        px, py = 104, 592
        d2 = ImageDraw.Draw(base)
        d2.rounded_rectangle([px, py, px + 396, py + 152], 18, fill=(15, 24, 42, 196),
                             outline=(255, 255, 255, 46), width=2)
        ftxt(base, px + 28, py + 48, f"{val:,}".replace(",", ".") + "+",
             font("PlusJakartaSans-var.ttf", 54, 800), AMBER, st)
        ftxt(base, px + 28, py + 106, "lượt truy cập / ngày", font("BeVietnamPro-Medium.ttf", 22),
             (214, 226, 244, 255), st)
    st2 = seg(t, c2a + 0.45, c2a + 0.9)
    if st2 > 0:
        px, py = 528, 592
        d2 = ImageDraw.Draw(base)
        d2.rounded_rectangle([px, py, px + 372, py + 152], 18, fill=(15, 24, 42, 196),
                             outline=(255, 255, 255, 46), width=2)
        val = int(5000 * ease(min(1.0, (t - c2a - 0.45) / 0.8)))
        ftxt(base, px + 28, py + 48, f"{val:,}".replace(",", "."),
             font("PlusJakartaSans-var.ttf", 54, 800), (255, 255, 255, 255), st2)
        ftxt(base, px + 28, py + 106, "người dùng cùng lúc", font("BeVietnamPro-Medium.ttf", 22),
             (214, 226, 244, 255), st2)

    # con dấu SẬP
    c3 = fr(tl, "S01", 2, 0.18)[0]
    sp_ = seg(t, c3, c3 + 0.5)
    if sp_ > 0:
        stamp = Image.new("RGBA", (340, 150), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp)
        sd.rounded_rectangle([6, 6, 334, 144], 14, outline=RED, width=8)
        draw_rich(sd, (170, 74), "SẬP!", font("BeVietnamPro-Bold.ttf", 88), RED, "mm")
        stamp = stamp.rotate(9, expand=True, resample=Image.BICUBIC)
        paste_im(base, stamp, 1000, 520, sp_)
        ftxt(base, 1040, 700, "Máy chủ gánh không nổi", font_semi(26), (255, 190, 190, 255), sp_)
        paste_im(base, pill("502 · timeout · quá tải", RED_L, (40, 14, 20, 220), 19, 40),
                 1040, 738, seg(t, c3 + 0.2, c3 + 0.7))

    # hạt sáng bay nhẹ (ám sự ánh đèn sale)
    for i in range(16):
        ph = (t * 0.22 + i * 0.37) % 1.0
        hx = 980 + (i * 137) % 860
        hy = 150 + ((i * 211) % 780) - ph * 90
        rr = 2 + (i % 3)
        d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=(255, 214, 150, 90))

    sheen(base, lin(t, 0.4, 3.4), 20)
    _an(base, tl, "S01", t, "present", look=1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    a, b = fr(tl, "S01", 1, 0.06), fr(tl, "S01", 1, 0.06)
    c = fr(tl, "S01", 2, 0.18)[0]
    return [(0.2, "whoosh", None, 0.55), (a[0], "tick", None, 0.5),
            (a[0] + 0.45, "tick", None, 0.4), (c, "thud", None, 0.9),
            (c + 0.3, "deny", None, 0.55)]


# ================================================================ S02 — QUÁ TẢI
def draw_S02(t, tl):
    base, d = _base()
    # nền tối command-center
    bg = kb(IMG["ops_monitor"], W, H, t, 1.02, 1.1, radius=0, shadow=False, dur=10)
    base.alpha_composite(bg, (0, 0))
    overlay_grad(base, 236, 120, color=(6, 11, 22))
    d = ImageDraw.Draw(base)
    headbar(base, seg(t, 0.2, 1.0), "01 · CAO ĐIỂM 12.12", dark=True)
    draw_tracked(d, (96, 44), "AN TECH ACADEMY", F_BRAND, (226, 234, 248, 220), 3.2, 1)

    # panel trái
    px, py, pw, ph = 96, 118, 780, 690
    d.rounded_rectangle([px, py, px + pw, py + ph], 22, fill=(9, 16, 30, 232),
                        outline=(96, 114, 142, 120), width=2)
    a0 = fr(tl, "S02", 0, 0.03)[0]
    ftxt(base, px + 34, py + 46, "HỆ THỐNG QUÁ TẢI", font("BeVietnamPro-Bold.ttf", 38),
         WHITE, seg(t, a0, a0 + 0.5))
    paste_im(base, pill("ALERT · 5.000 kết nối đồng thời", RED_L, (44, 12, 18, 235), 18, 38),
             px + 34, py + 82, seg(t, a0 + 0.2, a0 + 0.7))

    # gauge CPU / RAM / latency
    rows = [("CPU", 0.97, None), ("RAM", 0.93, None), ("Latency", 0.86, "4.8s")]
    for i, (lb, target, tail) in enumerate(rows):
        q = seg(t, a0 + 0.15 + i * 0.12, a0 + 1.0 + i * 0.12)
        yy = py + 158 + i * 92
        ftxt(base, px + 34, yy, lb, font_semi(23), (206, 218, 236, 255))
        bx, bw = px + 172, 470
        d.rounded_rectangle([bx, yy - 9, bx + bw, yy + 9], 9, fill=(34, 46, 68, 255))
        d.rounded_rectangle([bx, yy - 9, bx + max(2, int(bw * target * q)), yy + 9], 9,
                            fill=(RED if i < 2 else AMBER))
        ftxt(base, bx + bw + 16, yy, (f"{int(target * 100)}%" if not tail else tail),
             font("PlusJakartaSans-var.ttf", 26, 800), RED if i < 2 else AMBER, q)
    # nhịp tim phản hồi
    cx0, cy0 = px + 34, py + 452
    d.rounded_rectangle([cx0, cy0, cx0 + 712, cy0 + 112], 12, fill=(13, 22, 40, 255),
                        outline=(58, 74, 100, 255), width=2)
    pts = []
    for k in range(120):
        q = k / 119
        x = cx0 + 14 + q * 684
        y = cy0 + 62 - 22 * math.sin(q * 26 - t * 6) * (0.5 + 0.5 * q)
        pts.append((x, y))
    if seg(t, a0 + 0.3, a0 + 1.2) > 0:
        d.line(pts, fill=(255, 92, 92, 230), width=3)
    ftxt(base, cx0 + 14, cy0 + 24, "Thời gian phản hồi", font("BeVietnamPro-Regular.ttf", 18),
         (150, 166, 190, 255))

    # toast lỗi (cue 2)
    b0 = fr(tl, "S02", 1, 0.05)[0]
    toasts = [("502 Bad Gateway", "Khách không vào được", RED), ("Đặt hàng thất bại", "Đơn hàng bị mất", AMBER)]
    for i, (t1, t2, col) in enumerate(toasts):
        q = seg(t, b0 + i * 0.32, b0 + i * 0.32 + 0.35)
        if q <= 0:
            continue
        x = px + 34 + i * 372
        y = py + 596
        paste_im(base, card(344, 74, fill=(26, 20, 28, 245), outline=col), x, y, q)
        paste_im(base, sp_icon("alert-triangle", col, 26), x + 18, y + 24, q)
        ftxt(base, x + 58, y + 26, t1, font_semi(20), WHITE, q)
        ftxt(base, x + 58, y + 52, t2, font("BeVietnamPro-Regular.ttf", 17), (168, 178, 196, 255), q)

    # vòng cảnh báo (vẽ trước ảnh)
    for k in range(2):
        ph = ((t * 0.45 + k * 0.5) % 1.0)
        ring(base, 1350 + 220, 520 + 220, 260 + 80 * ph, RED, (1 - ph) * 0.35, 2)
    # ảnh phụ: rack quá nhiệt
    shot(base, IMG["server_overheat"], 1350, 520, 440, 440, 1, t,
         1.05, 1.12, -0.03, 0.02, "Rack nóng · đèn đỏ", RED, 18)
    ftxt(base, 1350, 986, "CPU · RAM · IO cùng chạm trần", font_semi(21), (255, 190, 190, 255),
         seg(t, b0, b0 + 0.6))

    sheen(base, lin(t, 0.6, 3.6), 14)
    _an(base, tl, "S02", t, "think", look=0)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    a0 = fr(tl, "S02", 0, 0.03)[0]
    b0 = fr(tl, "S02", 1, 0.05)[0]
    return [(a0, "thud", None, 0.7), (a0 + 0.25, "tick", None, 0.5),
            (b0, "deny", None, 0.6), (b0 + 0.32, "deny", None, 0.45)]


# ================================================================ S03 — ĐỊNH NGHĨA
def draw_S03(t, tl):
    base, d = _base()
    s = tl["S03"]
    # wash kem ấm
    d.ellipse([-280, 600, 560, 1380], fill=(253, 246, 227, 255))
    d.ellipse([1420, -280, 2200, 460], fill=(232, 240, 252, 255))
    headbar(base, seg(t, 0.2, 1.0), "02 · KHÁI NIỆM")
    _title(base, tl, "S03", t, "Load Balancer là gì?", "Một cửa ngõ, chia việc cho cả đội máy chủ")
    ftxt(base, 110, 236, "Thử tưởng tượng: quầy tính tiền ngày siêu sale.",
         font("BeVietnamPro-Medium.ttf", 27), MUT, seg(t, 0.5, 1.0))

    # LB dispatcher
    lx, ly, lw, lh = 96, 416, 280, 104
    st = seg(t, s["starts"][0] + 0.1, s["starts"][0] + 0.6)
    node(base, lx, ly, lw, lh, "split", "Load Balancer", p=st, color=AMBER,
         fill=(255, 251, 240, 255), icon_size=40, label_size=22)
    ftxt(base, lx + lw // 2, ly + lh + 24, "điều phối viên", font("BeVietnamPro-Regular.ttf", 20),
         MUT, st, "mm")

    lanes = [("Quầy 01", 470), ("Quầy 02", 760), ("Quầy 03", 1050)]
    b0 = fr(tl, "S03", 1, 0.0)[0]
    bus_y, bus_x, ly_c = 306, 428, ly + lh // 2
    def _part(pts, p):
        if p <= 0:
            return
        q = max(0.0, min(1.0, p))
        L = [math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1])
             for k in range(len(pts) - 1)]
        tot, dd, out = sum(L), q * sum(L), [pts[0]]
        for k, l in enumerate(L):
            if dd >= l:
                out.append(pts[k + 1])
                dd -= l
            else:
                r = dd / l if l else 0
                out.append((pts[k][0] + (pts[k + 1][0] - pts[k][0]) * r,
                            pts[k][1] + (pts[k + 1][1] - pts[k][1]) * r))
                break
        if len(out) >= 2:
            d.line(out, fill=(170, 180, 198, 255), width=3, joint="curve")
    for i, (lb, x) in enumerate(lanes):
        d.rounded_rectangle([x, 340, x + 210, 640], 16, fill=(255, 255, 255, 245),
                            outline=(214, 222, 234, 255), width=2)
        draw_rich(d, (x + 105, 376), lb, font_semi(23), NAVY, "mm")
        paste_im(base, sp_icon("shopping-cart", BLUE if i == 0 else (BLUE_L if i == 1 else MUT), 34),
                 x + 88, 398, seg(t, s["starts"][0] + 0.2 + i * 0.08, s["starts"][0] + 0.5))
        # hàng đợi: 5 chấm xếp dọc, cue 2 tan dần
        for k in range(5):
            fade = 1.0 - seg(t, b0 + 0.15 + k * 0.12, b0 + 0.55 + k * 0.12)
            dd = seg(t, s["starts"][0] + 0.5 + k * 0.05, s["starts"][0] + 0.8 + k * 0.05)
            if dd <= 0:
                continue
            cx = x + 105
            cy = 452 + k * 34
            dot(base, cx, cy, 11, (96, 116, 148), dd * fade)
        # bus phân phối: LB → trục dọc → ngang → thả xuống từng quầy
        trunk = [(lx + lw, ly_c), (bus_x, ly_c), (bus_x, bus_y), (x + 105, bus_y)]
        _part(trunk, seg(t, s["starts"][0] + 0.35 + i * 0.10, s["starts"][0] + 0.75 + i * 0.10))
        bp = seg(t, s["starts"][0] + 0.55 + i * 0.10, s["starts"][0] + 0.90 + i * 0.10)
        if bp > 0:
            ye = bus_y + 34 * bp
            d.line([x + 105, bus_y, x + 105, ye], fill=(170, 180, 198, 255), width=3)
            if bp > 0.9:
                d.polygon([(x + 105, 340), (x + 105 - 9, 322), (x + 105 + 9, 322)],
                          fill=(150, 160, 180, 255))
        # khách được chỉ sang quầy
        bq = seg(t, b0 + 0.10 + i * 0.10, b0 + 0.85 + i * 0.10)
        if bq > 0:
            packet(base, trunk + [(x + 105, 340)], bq, AMBER, 7)
        # trạng thái từng quầy
        ftxt(base, x + 105, 662, ["Xếp hàng dài", "Nhanh hơn", "Thoáng nhất"][i],
             font("BeVietnamPro-Medium.ttf", 19),
             [RED, TEAL, TEAL][i], seg(t, b0 + 0.3 + i * 0.15, b0 + 0.8 + i * 0.15), "mm")

    # ảnh minh hoạ sale + thẻ "1 → nhiều"
    shot(base, IMG["sale_crowd"], 1360, 296, 460, 268, seg(t, 0.4, 1.1), t,
         1.04, 1.12, 0.04, -0.02, "12.12 · khách đổ về", AMBER, 16)
    cq = seg(t, b0 + 0.15, b0 + 0.75)
    paste_im(base, card(460, 148, fill=(255, 255, 255, 250), outline=(214, 222, 234, 255)),
             1360, 596, cq)
    ftxt(base, 1392, 604, "1", font("PlusJakartaSans-var.ttf", 54, 800), AMBER, cq)
    ftxt(base, 1432, 622, "cửa ngõ", font("BeVietnamPro-Medium.ttf", 20), NAVY, cq)
    n_count = 1 + 2 * min(1.0, max(0.0, (t - (b0 + 0.3)) / 0.6))
    draw_marker(d, 1516, 634, 1588, 634, cq, (170, 180, 198, 255), 4, 3)
    ftxt(base, 1612, 604, f"{int(n_count)}+", font("PlusJakartaSans-var.ttf", 54, 800), TEAL, cq)
    ftxt(base, 1700, 622, "máy chủ", font("BeVietnamPro-Medium.ttf", 20), NAVY, cq)
    ftxt(base, 1392, 690, "Thêm máy chủ là thêm sức — không phải đổi kiến trúc.",
         font("BeVietnamPro-Regular.ttf", 17), MUT, cq)

    # callout phân biệt
    b1 = fr(tl, "S03", 1, 0.55)[0]
    paste_im(base, pill("CHỈ ĐIỀU PHỐI — KHÔNG XỬ LÝ NGHIỆP VỤ", RED, RED_L, 19, 40),
             110, 774, seg(t, b1, b1 + 0.5))
    ftxt(base, 110, 842, "Nó đứng ở cửa, chia việc — còn bán hàng là việc của máy chủ phía sau.",
         font("BeVietnamPro-Regular.ttf", 22), MUT, seg(t, b1 + 0.3, b1 + 0.9))

    sheen(base, lin(t, 1.2, 4.2), 18)
    _an(base, tl, "S03", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    s = tl["S03"]
    b0 = fr(tl, "S03", 1, 0.0)[0]
    return [(0.2, "whoosh", None, 0.6)] + [(b0 + i * 0.15, "pop", None, 0.45) for i in range(3)] + \
           [(b0 + 0.55, "chime", None, 0.6)]


# ================================================================ S04 — KIẾN TRÚC
def draw_S04(t, tl):
    base, d = _base()
    s = tl["S04"]
    # lưới blueprint
    for gx in range(80, 1860, 44):
        for gy in range(110, 960, 44):
            d.point((gx, gy), fill=(226, 233, 243, 255))
    d.ellipse([1280, -260, 2080, 500], fill=(235, 243, 255, 255))
    headbar(base, seg(t, 0.2, 1.0), "03 · KIẾN TRÚC")
    _title(base, tl, "S04", t, "Bốn lớp của hệ thống", "Client → Load Balancer → Backend → Database")

    a0 = s["starts"][0]
    # Client
    node(base, 108, 436, 214, 96, "globe", "Client", "trình duyệt", BLUE, p=seg(t, a0 + 0.05, a0 + 0.4))
    # LB
    node(base, 400, 436, 284, 96, "split", "Load Balancer", "cửa ngõ", AMBER,
         fill=(255, 251, 240, 255), p=seg(t, a0 + 0.25, a0 + 0.6), icon_size=38, label_size=23)
    # 3 server
    ys = [350, 456, 562]
    for i, yy in enumerate(ys):
        node(base, 752, yy, 268, 84, "server", f"Backend {i + 1:02d}", "xử lý nghiệp vụ",
             BLUE if i != 1 else TEAL, p=seg(t, a0 + 0.45 + i * 0.1, a0 + 0.85 + i * 0.1),
             icon_size=34, label_size=21)
    # DB
    node(base, 1132, 436, 220, 96, "database", "Database", "dữ liệu", PURPLE,
         p=seg(t, a0 + 0.7, a0 + 1.05), icon_size=40, label_size=22)

    # đường nối
    c1 = seg(t, a0 + 0.5, a0 + 0.8)
    draw_conn(d, 322, 484, 400, 484, c1, (140, 156, 180, 255), width=4)
    for i, yy in enumerate(ys):
        draw_conn(d, 684, 484, 752, yy + 42, seg(t, a0 + 0.6 + i * 0.08, a0 + 0.95 + i * 0.08),
                  (160, 174, 196, 255), width=3, hand=False)
    for i, yy in enumerate(ys):
        draw_conn(d, 1020, yy + 42, 1132, 484, seg(t, a0 + 0.8 + i * 0.07, a0 + 1.1 + i * 0.07),
                  (168, 152, 220, 255), width=3)

    # gói request cue 2
    b0 = fr(tl, "S04", 1, 0.02)[0]
    cycle = 3.2
    for k in range(3):
        q = ((t - b0) % cycle) / cycle
        q = max(0.0, min(1.0, q))
        srv_y = ys[k] + 42
        pts = [(215, 484), (400, 484), (684, 484), (752, srv_y)]
        packet(base, pts, q * 1.6, [AMBER, BLUE, TEAL][k], 8)
        pts2 = [(1020, srv_y), (1132, 484)]
        if q > 0.55:
            packet(base, pts2, (q - 0.55) / 0.45, PURPLE, 7)
    # nhãn request
    paste_im(base, pill("GET /phones/iphone-15", NAVY, (255, 255, 255, 240), 18, 36),
             108, 556, seg(t, b0, b0 + 0.5))
    paste_im(base, pill("UPDATE ... /health", NAVY, (255, 255, 255, 240), 18, 36),
             108, 604, seg(t, b0 + 0.4, b0 + 0.9))

    # ảnh mô hình tham chiếu
    shot(base, IMG["arch_public_ip"], 1390, 236, 402, 240, seg(t, b0 + 0.2, b0 + 0.8), t,
         1.03, 1.1, -0.03, 0.02, "Mô hình tham chiếu", BLUE, 14)
    ftxt(base, 1390, 500, "Public IP ở cửa, private IP bên trong", font("BeVietnamPro-Regular.ttf", 19),
         MUT, seg(t, b0 + 0.7, b0 + 1.1))

    # chip scaling
    c0 = fr(tl, "S04", 1, 0.72)[0]
    paste_im(base, pill("Horizontal Scaling", TEAL, MINT, 21, 42, "trending-up"), 1390, 560,
             seg(t, c0, c0 + 0.5))
    ftxt(base, 1390, 626, "Thêm máy chủ, không cần máy khổng lồ", font("BeVietnamPro-Regular.ttf", 19),
         MUT, seg(t, c0 + 0.2, c0 + 0.7))

    sheen(base, lin(t, 1.0, 4.0), 16)
    _an(base, tl, "S04", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    a0 = tl["S04"]["starts"][0]
    b0 = fr(tl, "S04", 1, 0.02)[0]
    return [(a0, "whoosh", None, 0.7)] + [(a0 + 0.45 + i * 0.1, "pop", None, 0.5) for i in range(3)] + \
           [(b0, "tick", None, 0.6), (b0 + 0.6, "click", None, 0.45)]


# ================================================================ S05 — HORIZONTAL
def draw_S05(t, tl):
    base, d = _base()
    s = tl["S05"]
    d.ellipse([-260, 680, 520, 1400], fill=(236, 249, 246, 255))
    headbar(base, seg(t, 0.2, 1.0), "04 · MỞ RỘNG")
    _title(base, tl, "S05", t, "Mở rộng theo chiều ngang", "Scale out — nhiều máy nhỏ thay vì một máy khổng lồ")

    a0 = s["starts"][0]
    # Card VERTICAL
    paste_im(base, card(800, 470, fill=WHITE, outline=(226, 232, 240, 255)), 96, 300,
             seg(t, a0 + 0.05, a0 + 0.5))
    ftxt(base, 130, 342, "VERTICAL SCALE", font("BeVietnamPro-Bold.ttf", 28), MUT,
         seg(t, a0 + 0.15, a0 + 0.6))
    ftxt(base, 130, 380, "Nâng CPU, RAM cho một máy", font("BeVietnamPro-Regular.ttf", 21), MUT,
         seg(t, a0 + 0.25, a0 + 0.7))
    # một server to, mũi tên lên chạm trần
    sx, sy = 366, 430
    d.rounded_rectangle([sx, sy, sx + 260, sy + 250], 16, fill=(246, 249, 253, 255),
                        outline=(203, 214, 230, 255), width=2)
    paste_im(base, sp_icon("server", NAVY, 74), sx + 93, sy + 60, 1)
    ftxt(base, sx + 130, sy + 168, "1 máy", font_semi(24), NAVY, 1, "mm")
    ftxt(base, sx + 130, sy + 202, "đắt · có trần", font("BeVietnamPro-Regular.ttf", 18), MUT, 1, "mm")
    ar = seg(t, a0 + 0.35, a0 + 0.9)
    d.line([sx + 130, sy - 20, sx + 130, sy - 20 - 96 * ar], fill=AMBER, width=7)
    if ar > 0.95:
        d.polygon([(sx + 130, sy - 132), (sx + 112, sy - 106), (sx + 148, sy - 106)], fill=AMBER)
    d.line([96 + 40, 420, 96 + 760, 420], fill=(245, 158, 11, 120), width=3)
    ftxt(base, 96 + 740, 402, "trần phần cứng", font("BeVietnamPro-Medium.ttf", 17), AMBER_D, 1, "rm")

    # Card HORIZONTAL
    paste_im(base, card(790, 470, fill=(247, 252, 251, 255), outline=(190, 230, 222, 255)),
             1006, 300, seg(t, a0 + 0.25, a0 + 0.7))
    ftxt(base, 1040, 342, "HORIZONTAL SCALE", font("BeVietnamPro-Bold.ttf", 28), TEAL,
         seg(t, a0 + 0.35, a0 + 0.8))
    ftxt(base, 1040, 380, "Thêm nhiều máy chủ bình thường", font("BeVietnamPro-Regular.ttf", 21), MUT,
         seg(t, a0 + 0.45, a0 + 0.9))
    b0 = fr(tl, "S05", 1, 0.1)[0]
    for i in range(3):
        px = 1052 + i * 236
        p = seg(t, a0 + 0.65 + i * 0.16, a0 + 1.05 + i * 0.16)
        if p <= 0:
            continue
        down = (i == 0) and t > b0 + 0.75
        col = (148, 163, 184, 255) if down else TEAL
        rrect_a(base, [px, 448, px + 208, 660], 14,
                fill=(240, 244, 249, 255) if down else WHITE,
                outline=col, width=3, p=p)
        paste_im(base, sp_icon("server", col, 60), px + 74, 476, p)
        ftxt(base, px + 104, 566, f"S{i + 1:02d}", font("PlusJakartaSans-var.ttf", 26, 800), col, p, "mm")
        ftxt(base, px + 104, 606, "bảo trì" if down else "đang chạy",
             font("BeVietnamPro-Medium.ttf", 18), MUT if not down else (148, 163, 184, 255), p, "mm")
        if down:
            d.line([px + 40, 520, px + 168, 620], fill=(220, 38, 38, 160), width=3)
    # request vẫn được phục vụ
    if t > b0 + 0.8:
        for k in range(3):
            q = ((t - b0 - 0.8) * 0.9 + k * 0.33) % 1.0
            packet(base, [(1040, 700), (1230 + k * 236, 700), (1230 + k * 236, 660)],
                   q, TEAL, 7)
        ftxt(base, 1100, 720, "Một máy nghỉ — dịch vụ vẫn chạy", font_semi(20), TEAL,
             seg(t, b0 + 0.9, b0 + 1.2))

    # ảnh cụm máy chủ
    shot(base, IMG["net_fiber"], 1010, 790, 720, 150, seg(t, a0 + 0.5, a0 + 1.1), t,
         1.03, 1.1, 0.03, 0.0, None, TEAL, 12)
    ftxt(base, 96, 810, "Một máy ốm, hai máy còn chạy.", font("BeVietnamPro-Bold.ttf", 32), NAVY,
         seg(t, b0 + 0.15, b0 + 0.6))
    ftxt(base, 96, 858, "Khỏe hơn, rẻ hơn, nâng cấp từng bước.", font("BeVietnamPro-Regular.ttf", 22),
         MUT, seg(t, b0 + 0.35, b0 + 0.8))

    sheen(base, lin(t, 1.4, 4.4), 16)
    _an(base, tl, "S05", t, "present", look=0)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    a0 = tl["S05"]["starts"][0]
    b0 = fr(tl, "S05", 1, 0.1)[0]
    return [(a0, "whoosh", None, 0.6), (a0 + 0.5, "pop", None, 0.5)] + \
           [(a0 + 0.65 + i * 0.16, "pop", None, 0.45) for i in range(3)] + \
           [(b0 + 0.8, "deny", None, 0.4), (b0 + 1.0, "success", None, 0.6)]


# ================================================================ S06 — ROUND ROBIN
def draw_S06(t, tl):
    base, d = _base()
    s = tl["S06"]
    d.ellipse([1420, 560, 2140, 1280], fill=(236, 242, 252, 255))
    headbar(base, seg(t, 0.2, 1.0), "05 · THUẬT TOÁN 1/4")
    _title(base, tl, "S06", t, "Round Robin", "Chia lần lượt — như phát bài")

    a0 = s["starts"][0]
    node(base, 110, 420, 210, 96, "split", "LB", p=seg(t, a0 + 0.05, a0 + 0.4), color=AMBER,
         fill=(255, 251, 240, 255), label_size=26)
    xs = [470, 820, 1170]
    b0 = fr(tl, "S06", 0, 0.15)[0]
    ps = []
    for i, x in enumerate(xs):
        p = seg(t, b0 + i * 0.12, b0 + 0.45 + i * 0.12)
        ps.append(p)
        srv_card(base, x, 388, 290, 150, i + 1, "ok", p, color=BLUE, sub="giống nhau")

    # token chạy vòng
    cyc = 2.0
    if t > b0:
        for i, x in enumerate(xs):
            bp = seg(t, b0 + i * 0.08, b0 + 0.38 + i * 0.08)
            if bp > 0:
                xe = 346 + (x + 145 - 346) * bp
                d.line([346, 340, xe, 340], fill=(186, 198, 216, 255), width=3)
                ye = 340 + 48 * bp
                d.line([x + 145, 340, x + 145, ye], fill=(186, 198, 216, 255), width=3)
                if bp > 0.9:
                    d.polygon([(x + 145, 388), (x + 136, 370), (x + 154, 370)],
                              fill=(160, 174, 196, 255))
        q = ((t - b0) % cyc) / cyc
        k = int(q * 4)
        qq = q * 4 - k
        stops = [(346, 468), (xs[0] + 145, 340), (xs[1] + 145, 340),
                 (xs[2] + 145, 340), (xs[0] + 145, 340)]
        if k == 0:
            pts = [(320, 468), (346, 468), (346, 340), stops[1]]
        else:
            pts = [stops[k], stops[k + 1]]
        packet(base, pts, qq, AMBER, 9)
    # dải thứ tự
    c1 = fr(tl, "S06", 0, 0.55)[0]
    dx, dy = 110, 210
    d.rounded_rectangle([dx, dy, dx + 720, dy + 60], 30, fill=(255, 255, 255, 255),
                        outline=(210, 220, 236, 255), width=2)
    for i, lab in enumerate(["R1", "R2", "R3", "R4", "R1"]):
        p = seg(t, c1 + i * 0.14, c1 + 0.4 + i * 0.14)
        if p <= 0:
            continue
        x = dx + 26 + i * 136
        col = AMBER if lab == "R1" else BLUE
        paste_im(base, pill(f"{lab} → S{['01','02','03','01','01'][i]}",
                            col, WHITE, 19, 38), x, dy + 11, p)
    # ảnh minh hoạ thuật toán
    crop = crop_frac(IMG["algo_4up"], 0.06, 0.17, 0.475, 0.535, 330, 250)
    paste_im(base, crop, 470, 610, seg(t, c1 + 0.4, c1 + 0.9))
    ftxt(base, 470, 872, "Round Robin trong bộ 4 thuật toán", font("BeVietnamPro-Regular.ttf", 18),
         MUT, seg(t, c1 + 0.6, c1 + 1.0))

    # cảnh báo cue 2
    c2 = fr(tl, "S06", 1, 0.15)[0]
    p2 = seg(t, c2, c2 + 0.5)
    paste_im(base, card(430, 150, fill=(255, 248, 233, 255), outline=AMBER), 870, 640, p2)
    if p2 > 0.3:
        ftxt(base, 892, 674, "Server 01 khỏe hơn", font_semi(22), AMBER_D, p2)
        ftxt(base, 892, 708, "Chia đều = bắt nó chờ", font("BeVietnamPro-Regular.ttf", 20), MUT, p2)
        ftxt(base, 892, 744, "chia đều ≠ chia đúng", font("BeVietnamPro-Medium.ttf", 20), RED, p2)
    pw = seg(t, c2, c2 + 0.35)
    if pw > 0:
        srv_card(base, xs[0], 388, 290, 150, 1, "warn", pw, color=AMBER, load=0.92, sub="nóng hơn")
    # counter vẽ sau thẻ cảnh báo để không bị che
    for i, x in enumerate(xs):
        p = ps[i]
        if p <= 0.5:
            continue
        cnt = sum(1 for k in range(12) if k % 3 == i and t > b0 + (k % 3) * 0.12 + (k // 3) * 0.42)
        cc = AMBER if (i == 0 and t >= c2) else BLUE
        ftxt(base, x + 268, 412, f"{cnt}", font("PlusJakartaSans-var.ttf", 26, 800),
             cc, min(1, p * 1.4), "rm")
        ftxt(base, x + 268, 434, "request", font("BeVietnamPro-Regular.ttf", 14), MUT, p, "rm")

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S06", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    a0 = tl["S06"]["starts"][0]
    b0 = fr(tl, "S06", 0, 0.15)[0]
    c1 = fr(tl, "S06", 0, 0.55)[0]
    c2 = fr(tl, "S06", 1, 0.15)[0]
    return [(a0, "whoosh", None, 0.6)] + [(b0 + i * 0.12, "pop", None, 0.5) for i in range(3)] + \
           [(c1 + i * 0.14, "tick", None, 0.4) for i in range(4)] + [(c2, "deny", None, 0.45)]


# ================================================================ S07 — WEIGHTED
def draw_S07(t, tl):
    base, d = _base()
    s = tl["S07"]
    d.ellipse([-260, 620, 520, 1340], fill=(253, 246, 227, 255))
    headbar(base, seg(t, 0.2, 1.0), "06 · THUẬT TOÁN 2/4")
    _title(base, tl, "S07", t, "Weighted Round Robin", "Máy khỏe nhận nhiều việc hơn")

    a0 = s["starts"][0]
    rows = [("Server 01", 3, AMBER, 0.60), ("Server 02", 1, BLUE, 0.20), ("Server 03", 1, TEAL, 0.20)]
    for i, (lb, wgt, col, frac) in enumerate(rows):
        p = seg(t, a0 + 0.08 + i * 0.12, a0 + 0.5 + i * 0.12)
        if p <= 0:
            continue
        y = 330 + i * 118
        d.rounded_rectangle([110, y, 980, y + 96], 16, fill=(255, 255, 255, 250),
                            outline=(216, 224, 236, 255), width=2)
        paste_im(base, sp_icon("server", col, 40), 134, y + 28, p)
        ftxt(base, 190, y + 34, lb, font_semi(24), NAVY, p)
        ftxt(base, 190, y + 66, f"weight = {wgt}", font("JetBrainsMono-var.ttf", 18), MUT, p)
        bx, bw = 400, 470
        d.rounded_rectangle([bx, y + 42, bx + bw, y + 62], 10, fill=(236, 240, 246, 255))
        d.rounded_rectangle([bx, y + 42, bx + max(2, int(bw * frac * p)), y + 62], 10, fill=col)
        ftxt(base, bx + bw + 26, y + 52, f"{int(frac * 100)}%", font("PlusJakartaSans-var.ttf", 27, 800),
             col, p)

    # băng 5 request (xuất hiện cuối cue 1 để chốt tỉ lệ 3:1:1)
    b0 = fr(tl, "S07", 1, 0.02)[0]
    s0 = a0 + 1.1
    ftxt(base, 110, 716, "Trong 5 request liên tiếp", font("BeVietnamPro-Medium.ttf", 21), MUT,
         seg(t, s0, s0 + 0.4))
    slots = ["01", "01", "01", "02", "03"]
    for i, sl in enumerate(slots):
        p = seg(t, s0 + 0.15 + i * 0.13, s0 + 0.45 + i * 0.13)
        if p <= 0:
            continue
        x = 110 + i * 168
        col = AMBER if sl == "01" else (BLUE if sl == "02" else TEAL)
        paste_im(base, card(148, 96, fill=(255, 251, 240, 255) if sl == "01" else WHITE, outline=col),
                 x, 748, p)
        ftxt(base, x + 74, 782, sl, font("PlusJakartaSans-var.ttf", 34, 800), col, p, "mm")
        ftxt(base, x + 74, 820, "request", font("BeVietnamPro-Regular.ttf", 15), MUT, p, "mm")
        if i == 0:
            draw_marker(d, x - 4, 730, x + 150, 730, seg(t, s0 + 0.2, s0 + 0.6), AMBER, 5, 7)

    # ảnh minh họa weighted
    crop = crop_frac(IMG["algo_4up"], 0.06, 0.585, 0.475, 0.955, 360, 260)
    paste_im(base, crop, 1010, 336, seg(t, a0 + 0.4, a0 + 0.9))

    # callout
    c0 = fr(tl, "S07", 1, 0.55)[0]
    paste_im(base, card(360, 150, fill=(255, 248, 233, 255), outline=AMBER), 1010, 640,
             seg(t, c0, c0 + 0.5))
    ftxt(base, 1036, 678, "5 request", font("BeVietnamPro-Regular.ttf", 20), MUT, seg(t, c0 + 0.1, c0 + 0.5))
    ftxt(base, 1036, 724, "3 · 1 · 1", font("PlusJakartaSans-var.ttf", 40, 800), AMBER_D,
         seg(t, c0 + 0.2, c0 + 0.6))
    ftxt(base, 1036, 764, "đúng sức, đúng việc", font("BeVietnamPro-Medium.ttf", 18), MUT,
         seg(t, c0 + 0.3, c0 + 0.7))

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S07", t, "present", look=0)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    a0 = tl["S07"]["starts"][0]
    b0 = fr(tl, "S07", 1, 0.02)[0]
    s0 = a0 + 1.1
    return [(a0, "whoosh", None, 0.6)] + [(a0 + 0.1 + i * 0.12, "pop", None, 0.45) for i in range(3)] + \
           [(s0 + 0.15 + i * 0.13, "tick", None, 0.4) for i in range(5)]


# ================================================================ S08 — LEAST CONN
def draw_S08(t, tl):
    base, d = _base()
    s = tl["S08"]
    d.ellipse([1400, -280, 2180, 480], fill=(232, 248, 244, 255))
    headbar(base, seg(t, 0.2, 1.0), "07 · THUẬT TOÁN 3/4")
    _title(base, tl, "S08", t, "Least Connections", "Ai rảnh nhất thì làm")

    a0 = s["starts"][0]
    vals = [100, 30, 10]
    xs = [110, 566, 1022]
    b0 = fr(tl, "S08", 1, 0.02)[0]
    # vòng quét (vẽ sau nền, trước thẻ) — halo quanh Server 03
    if t > a0 + 0.6:
        ph = ((t - a0 - 0.6) * 0.8) % 1.0
        ring(base, xs[2] + 196, 405, 226 + 6 * math.sin(t * 3), TEAL, 0.35 * (1 - ph), 3)
    for i, x in enumerate(xs):
        p = seg(t, a0 + 0.08 + i * 0.13, a0 + 0.5 + i * 0.13)
        val = int(vals[i] * ease(min(1.0, max(0.0, (t - (a0 + 0.2 + i * 0.13)) / 0.9))))
        if i == 2 and t > b0 + 0.55:
            val = 10 + int(min(1.0, (t - b0 - 0.55) / 0.5))
        srv_card(base, x, 300, 392, 210, i + 1, "ok",
                 p, conn=val, color=(TEAL if i == 2 else BLUE),
                 sub=["đang gồng", "vừa phải", "đang rảnh"][i])
        # chấm kết nối trực quan
        if p > 0.4:
            n = max(2, int(val / 8))
            for k in range(min(n, 16)):
                cx = x + 28 + (k % 8) * 16
                cy = 430 + (k // 8) * 18
                d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(BLUE if val > 40 else TEAL))

    # pill gợi ý
    c1 = fr(tl, "S08", 0, 0.65)[0]
    paste_im(base, pill("request tiếp theo → Server 03", TEAL, MINT, 21, 44, "target"),
             690, 552, seg(t, c1, c1 + 0.5))
    if t > c1 + 0.2:
        q = ((t - c1 - 0.2) % 1.6) / 1.6
        packet(base, [(xs[2] + 196, 250), (xs[2] + 196, 300)], q, TEAL, 8)

    # ảnh minh họa
    crop = crop_frac(IMG["algo_4up"], 0.524, 0.165, 0.94, 0.535, 360, 250)
    paste_im(base, crop, 1480, 300, seg(t, a0 + 0.45, a0 + 0.95))
    ftxt(base, 1480, 566, "Least Connections", font("BeVietnamPro-Medium.ttf", 18), MUT,
         seg(t, a0 + 0.65, a0 + 1.0))

    # bảng so sánh nhỏ
    c2 = fr(tl, "S08", 1, 0.5)[0]
    paste_im(base, card(700, 130, fill=(247, 252, 251, 255), outline=(190, 230, 222, 255)),
             126, 640, seg(t, c2, c2 + 0.5))
    ftxt(base, 156, 676, "100  ·  30  ·  10", font("PlusJakartaSans-var.ttf", 34, 800), TEAL,
         seg(t, c2 + 0.1, c2 + 0.5))
    ftxt(base, 156, 720, "Chọn máy đang ít kết nối nhất — không cần biết request nặng nhẹ.",
         font("BeVietnamPro-Regular.ttf", 19), MUT, seg(t, c2 + 0.25, c2 + 0.7))

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S08", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    a0 = tl["S08"]["starts"][0]
    b0 = fr(tl, "S08", 1, 0.02)[0]
    c1 = fr(tl, "S08", 0, 0.65)[0]
    return [(a0, "whoosh", None, 0.6)] + [(a0 + 0.1 + i * 0.13, "pop", None, 0.45) for i in range(3)] + \
           [(c1, "success", None, 0.6), (b0 + 0.55, "tick", None, 0.4)]


# ================================================================ S09 — IP HASH
def draw_S09(t, tl):
    base, d = _base()
    s = tl["S09"]
    d.ellipse([-280, 560, 520, 1380], fill=(242, 240, 253, 255))
    headbar(base, seg(t, 0.2, 1.0), "08 · THUẬT TOÁN 4/4")
    _title(base, tl, "S09", t, "IP Hash", "Cùng IP — thường cùng một máy chủ")

    a0 = s["starts"][0]
    # client cards
    clients = [("203.0.113.7", 302, BLUE), ("198.51.100.4", 452, AMBER)]
    for i, (ip, y, col) in enumerate(clients):
        p = seg(t, a0 + 0.05 + i * 0.12, a0 + 0.4 + i * 0.12)
        paste_im(base, card(300, 96, fill=WHITE, outline=col), 96, y, p)
        paste_im(base, sp_icon("users", col, 34), 118, y + 30, p)
        ftxt(base, 166, y + 32, "Client", font_semi(21), NAVY, p)
        ftxt(base, 166, y + 62, ip, font("JetBrainsMono-var.ttf", 18), MUT, p)

    # hash box
    hx, hy = 470, 330
    p = seg(t, a0 + 0.3, a0 + 0.7)
    paste_im(base, card(210, 190, fill=(246, 244, 255, 255), outline=PURPLE), hx, hy, p)
    ftxt(base, hx + 105, hy + 58, "#", font("PlusJakartaSans-var.ttf", 64, 800), PURPLE, p, "mm")
    ftxt(base, hx + 105, hy + 126, "hàm băm", font("BeVietnamPro-Medium.ttf", 19), MUT, p, "mm")
    ftxt(base, hx + 105, hy + 156, "IP → chỉ số máy", font("BeVietnamPro-Regular.ttf", 16), MUT, p, "mm")

    # server cards
    xs = [860, 1160, 1460]
    for i, x in enumerate(xs):
        srv_card(base, x, 330, 270, 160, i + 1, "ok", seg(t, a0 + 0.45 + i * 0.1, a0 + 0.8 + i * 0.1),
                 color=BLUE if i == 0 else (AMBER if i == 1 else TEAL), sub="giữ session")

    # đường nối + gói
    if p > 0.5:
        draw_conn(d, 396, 350, hx, 400, seg(t, a0 + 0.4, a0 + 0.8), BLUE, width=4)
        draw_conn(d, 396, 500, hx, 450, seg(t, a0 + 0.5, a0 + 0.9), AMBER, width=4)
        c = fr(tl, "S09", 0, 0.55)[0]
        draw_conn(d, hx + 210, 380, 860, 400, seg(t, c, c + 0.4), BLUE, width=4)
        # tuyến 2 vòng dưới hàng thẻ để không cắt qua Server 01
        if t > c + 0.1:
            d.line([680, 470, 750, 545, 1160, 545, 1160, 492], fill=AMBER, width=4, joint="curve")
            d.polygon([(1160, 490), (1150, 508), (1170, 508)], fill=AMBER)
        if t > c:
            q = ((t - c) % 1.8) / 1.8
            packet(base, [(396, 350), (hx, 400), (860, 400)], min(1, q * 1.4), BLUE, 8)
            packet(base, [(396, 500), (hx, 450), (750, 545), (1160, 545), (1160, 490)],
                   min(1, q * 1.4), AMBER, 8)

    # sticky note
    b0 = fr(tl, "S09", 0, 0.75)[0]
    note = Image.new("RGBA", (330, 150), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rounded_rectangle([0, 0, 329, 149], 8, fill=(255, 249, 219, 255), outline=(240, 210, 120, 255), width=2)
    draw_rich(nd, (24, 34), "Session giữ nguyên", font_semi(22), (120, 90, 20, 255), "lm")
    draw_rich(nd, (24, 70), "Giỏ hàng không nhảy", font("BeVietnamPro-Regular.ttf", 19), (140, 116, 60, 255), "lm")
    draw_rich(nd, (24, 100), "Đăng nhập không mất", font("BeVietnamPro-Regular.ttf", 19), (140, 116, 60, 255), "lm")
    paste_im(base, note, 1380, 570, seg(t, b0, b0 + 0.5))

    # ảnh minh họa
    crop = crop_frac(IMG["algo_wide"], 0.648, 0.705, 0.94, 0.962, 400, 170)
    paste_im(base, crop, 100, 660, seg(t, a0 + 0.6, a0 + 1.0))
    ftxt(base, 100, 844, "IP Hash: cùng IP → cùng máy chủ", font("BeVietnamPro-Regular.ttf", 18),
         MUT, seg(t, a0 + 0.8, a0 + 1.1))

    # cảnh báo cue 2
    c2 = fr(tl, "S09", 1, 0.1)[0]
    p2 = seg(t, c2, c2 + 0.5)
    paste_im(base, card(430, 150, fill=(255, 240, 240, 255), outline=RED), 540, 640, p2)
    if p2 > 0.3:
        ftxt(base, 566, 676, "Đổi cấu hình, thêm máy", font_semi(21), RED, p2)
        ftxt(base, 566, 710, "→ IP cũ có thể nhảy máy", font("BeVietnamPro-Regular.ttf", 19), MUT, p2)
        ftxt(base, 566, 746, "Không có thuật toán hoàn hảo", font("BeVietnamPro-Medium.ttf", 19), RED, p2)
    if t > c2 + 0.2:
        d.line([1194, 452, 1440, 470], fill=(220, 38, 38, 180), width=3)

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S09", t, "think", look=1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    a0 = tl["S09"]["starts"][0]
    c = fr(tl, "S09", 0, 0.55)[0]
    c2 = fr(tl, "S09", 1, 0.1)[0]
    return [(a0, "whoosh", None, 0.6), (a0 + 0.3, "pop", None, 0.5),
            (c, "tick", None, 0.5), (c2, "deny", None, 0.5)]


# ================================================================ S10 — HEALTH CHECK
def draw_S10(t, tl):
    base, d = _base()
    s = tl["S10"]
    d.ellipse([1420, 560, 2180, 1320], fill=(240, 243, 248, 255))
    headbar(base, seg(t, 0.2, 1.0), "09 · HEALTH CHECK")
    _title(base, tl, "S10", t, "Máy chủ chết — ai phát hiện?", "Health Check: gọi thử trước khi giao việc")

    a0 = s["starts"][0]
    xs = [180, 700, 1220]
    c2 = fr(tl, "S10", 1, 0.35)[0]
    for i, x in enumerate(xs):
        p = seg(t, a0 + 0.05 + i * 0.12, a0 + 0.4 + i * 0.12)
        bad = (i == 1) and (t > a0 + 0.75) and (t < c2)
        st = "bad" if bad else "ok"
        if bad:
            ring(base, x + 190, 380, 190 + 16 * math.sin(t * 5), RED, 0.8, 3)
        srv_card(base, x, 300, 380, 160, i + 1, st, p, color=(BLUE if i != 1 else TEAL),
                 sub=("ổn định" if i != 1 else ("mất kết nối" if bad else "đã hồi phục")))
        if bad:
            paste_im(base, sp_icon("circle-x", RED, 30), x + 330, 316, seg(t, a0 + 0.8, a0 + 1.0))

    # đường nhịp tim
    y0 = 560
    pts = []
    for k in range(170):
        q = k / 169
        x = 96 + q * 1660
        base_y = y0
        seg_i = int(q * 9) % 9
        amp = 26 if (seg_i == 4) else 7
        y = base_y - amp * math.sin(q * 60 - t * 5) * (0.35 + 0.65 * q)
        pts.append((x, y))
    d.line(pts, fill=(37, 99, 235, 60), width=2)
    # /health pings
    pb = fr(tl, "S10", 0, 0.2)[0]
    if t > pb:
        for k in range(3):
            q = ((t - pb) * 0.7 + k / 3) % 1.0
            packet(base, [(96, y0), (xs[k] + 190, y0), (xs[k] + 190, 460)], q, TEAL, 6)
    paste_im(base, pill("GET /health", TEAL, MINT, 20, 42, "gauge"), 96, 600, seg(t, pb, pb + 0.4))
    paste_im(base, pill("200 OK → khỏe", TEAL, WHITE, 19, 40, "circle-check"), 300, 600,
             seg(t, pb + 0.15, pb + 0.55))
    paste_im(base, pill("timeout → gạch tên", RED, RED_L, 19, 40, "circle-x"), 560, 600,
             seg(t, a0 + 0.8, a0 + 1.15))

    # ảnh server lỗi
    shot(base, IMG["server_fail"], 1400, 640, 320, 230, seg(t, a0 + 0.4, a0 + 0.9), t,
         1.05, 1.13, -0.04, 0.02, "Đèn đỏ · node lỗi", RED, 12)

    # phục hồi
    if t > c2:
        p3 = seg(t, c2, c2 + 0.5)
        paste_im(base, pill("Server 02 quay lại đội", TEAL, MINT, 20, 44, "refresh-cw"),
                 700, 700, p3)
        packet(base, [(1030, 460), (890, 460)], lin(t, c2, c2 + 0.8), TEAL, 7)

    # chú thích chu kỳ
    c1 = fr(tl, "S10", 0, 0.75)[0]
    ftxt(base, 96, 690, "Kiểm tra định kỳ · ngưỡng lỗi theo chính sách", font("BeVietnamPro-Regular.ttf", 19),
         MUT, seg(t, c1, c1 + 0.5))

    sheen(base, lin(t, 1.4, 4.4), 16)
    _an(base, tl, "S10", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    a0 = tl["S10"]["starts"][0]
    pb = fr(tl, "S10", 0, 0.2)[0]
    c2 = fr(tl, "S10", 1, 0.35)[0]
    return [(a0, "whoosh", None, 0.6), (a0 + 0.8, "deny", None, 0.7),
            (pb + 0.2, "tick", None, 0.45), (c2, "success", None, 0.7)]


# ================================================================ S11 — NGINX
def draw_S11(t, tl):
    base, d = _base()
    # nền tối studio
    d.rectangle([0, 0, W, H], fill=(9, 14, 26, 255))
    g = kb(IMG["dc_corridor"], W, H, t, 1.02, 1.08, radius=0, shadow=False, dur=10)
    base.alpha_composite(g, (0, 0))
    overlay_grad(base, 238, 150, color=(6, 10, 20))
    d = ImageDraw.Draw(base)
    headbar(base, seg(t, 0.2, 1.0), "10 · TRIỂN KHAI", dark=True)
    draw_tracked(d, (96, 44), "AN TECH ACADEMY", F_BRAND, (226, 234, 248, 220), 3.2, 1)
    ftxt(base, 96, 128, "Cấu hình Nginx thật gọn", font("BeVietnamPro-Bold.ttf", 46), WHITE,
         seg(t, 0.2, 0.8))
    ftxt(base, 96, 180, "Upstream + location — thế là xong một tầng cân bằng tải.",
         font("BeVietnamPro-Regular.ttf", 24), (176, 190, 214, 255), seg(t, 0.4, 0.9))

    lines = [
        "upstream ecommerce_backend {",
        "    server 192.168.1.101:3000;",
        "    server 192.168.1.102:3000;",
        "    server 192.168.1.103:3000;",
        "}",
        "",
        "server {",
        "    listen 80;",
        "    location / {",
        "        proxy_pass http://ecommerce_backend;",
        "        proxy_set_header Host $host;",
        "        proxy_set_header X-Real-IP $remote_addr;",
        "    }",
        "}",
    ]
    a0 = tl["S11"]["starts"][0]
    typed = ease(min(1.0, max(0.0, (t - a0 - 0.15) / max(1.0, tl["S11"]["durs"][0] * 0.85))))
    code_panel(base, 92, 232, 980, lines, typed)

    # upstream diagram
    b0 = fr(tl, "S11", 1, 0.0)[0]
    p = seg(t, b0 + 0.05, b0 + 0.5)
    paste_im(base, pill("UPSTREAM · 3 BACKEND", AMBER, (22, 30, 48, 235), 19, 40, "layers"),
             1120, 250, seg(t, b0, b0 + 0.4))
    for i in range(3):
        q = seg(t, b0 + 0.15 + i * 0.12, b0 + 0.5 + i * 0.12)
        if q <= 0:
            continue
        y = 316 + i * 86
        rrect_a(base, [1120, y, 1440, y + 66], 12, fill=(18, 28, 46, 240),
                outline=(90, 108, 136, 200), width=2, p=q)
        paste_im(base, sp_icon("server", TEAL, 30), 1140, y + 18, q)
        ftxt(base, 1184, y + 24, f"192.168.1.10{i + 1}", font("JetBrainsMono-var.ttf", 18),
             (226, 234, 246, 255), q)
        ftxt(base, 1184, y + 46, ":3000", font("JetBrainsMono-var.ttf", 16), (140, 158, 186, 255), q)
        if q > 0.5:
            ring(base, 1158, y + 33, 24, TEAL, 0.35 + 0.35 * math.sin(t * 3 + i))

    # ảnh data center
    shot(base, IMG["dc_corridor"], 1470, 560, 350, 220, seg(t, b0 + 0.3, b0 + 0.8), t,
         1.04, 1.12, 0.04, 0.0, "Private network", TEAL, 12)

    # highlight location
    c0 = fr(tl, "S11", 1, 0.35)[0]
    if c0 > 0 and t > c0:
        p2 = seg(t, c0, c0 + 0.4)
        rrect_a(base, [106, 540, 1056, 540 + 5 * 33 + 8], 8,
                fill=(255, 196, 110, 38), outline=(255, 196, 110, 170), width=2, p=p2)
        paste_im(base, pill("location / → proxy_pass", AMBER, (22, 30, 48, 235), 18, 38),
                 1090, 620, p2)
        ftxt(base, 1090, 678, "Nhận request, chuyển vào", font("BeVietnamPro-Regular.ttf", 18),
             (176, 190, 214, 255), p2)
        ftxt(base, 1090, 706, "nhóm upstream.", font("BeVietnamPro-Regular.ttf", 18),
             (176, 190, 214, 255), p2)

    sheen(base, lin(t, 1.6, 4.6), 14)
    _an(base, tl, "S11", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S11", t))
    return base


def events_S11(tl):
    a0 = tl["S11"]["starts"][0]
    b0 = fr(tl, "S11", 1, 0.0)[0]
    c0 = fr(tl, "S11", 1, 0.35)[0]
    return [(a0 + 0.2, "whoosh", None, 0.6), (a0 + 1.0, "tick", None, 0.3),
            (b0, "pop", None, 0.5), (c0, "click", None, 0.45)]


# ================================================================ S12 — TỔNG KẾT
def draw_S12(t, tl):
    base, d = _base()
    d.ellipse([-260, 560, 560, 1340], fill=(240, 244, 250, 255))
    d.ellipse([1400, -280, 2220, 500], fill=(253, 246, 227, 255))
    # dải ảnh mờ phía trên
    g = kb(IMG["net_fiber"], W, 220, t, 1.02, 1.08, radius=0, shadow=False, dur=12)
    g.putalpha(g.getchannel("A").point(lambda a: int(a * 0.28)))
    base.alpha_composite(g, (0, 0))
    d = ImageDraw.Draw(base)
    headbar(base, seg(t, 0.2, 1.0), "TỔNG KẾT")
    _title(base, tl, "S12", t, "Nhớ 4 điều này là đủ", None)

    a0 = tl["S12"]["starts"][0]
    cards = [("01", "Một cửa ngõ", "Load Balancer nhận request", "split", AMBER),
             ("02", "Nhiều máy chủ", "backend chạy song song", "server", BLUE),
             ("03", "Bốn thuật toán", "Robin · Weighted · Least · Hash", "workflow", PURPLE),
             ("04", "Health Check", "loại máy lỗi khỏi vòng", "gauge", TEAL)]
    for i, (num, t1, t2, ic, col) in enumerate(cards):
        p = seg(t, a0 + 0.08 + i * 0.14, a0 + 0.45 + i * 0.14)
        if p <= 0:
            continue
        x = 96 + i * 416
        paste_im(base, card(384, 178, fill=WHITE, outline=(220, 228, 240, 255)), x, 196, p)
        ftxt(base, x + 26, 230, num, font("PlusJakartaSans-var.ttf", 26, 800), col, p)
        paste_im(base, sp_icon(ic, col, 30), x + 320, 214, p)
        ftxt(base, x + 26, 282, t1, font_semi(23), NAVY, p)
        ftxt(base, x + 26, 318, t2, font("BeVietnamPro-Regular.ttf", 17), MUT, p)
        if i == 0:
            draw_marker(d, x + 22, 256, x + 118, 256, seg(t, a0 + 0.25, a0 + 0.6), AMBER, 5, 9)

    # lưu ý — nhóm 1 theo cue 1, nhóm 2 thay thế theo cue 2
    b0 = fr(tl, "S12", 1, 0.05)[0]
    ftxt(base, 96, 420, "Nhưng đừng quên", font("BeVietnamPro-Bold.ttf", 30), NAVY,
         seg(t, a0 + 0.2, a0 + 0.55))
    notes1 = [("Database quá tải", "tối ưu index, đọc/ghi", "database", PURPLE),
              ("SQL chậm", "EXPLAIN, cache hợp lý", "search", BLUE),
              ("Thanh toán lỗi", "idempotency, retry", "credit-card", RED)]
    notes2 = [("Phiên đăng nhập", "session dùng chung", "key-round", PURPLE),
              ("Đồng bộ dữ liệu", "cache · queue", "refresh-cw", TEAL),
              ("Chống đặt trùng", "idempotency key", "shield-check", AMBER)]
    fade_old = 1.0 - seg(t, b0 + 0.05, b0 + 0.35)
    for row, base_p in ((notes1, a0 + 0.25), (notes2, b0 + 0.4)):
        for i, (t1, t2, ic, col) in enumerate(row):
            p = seg(t, base_p + i * 0.13, base_p + 0.35 + i * 0.13)
            if row is notes1:
                p *= fade_old
            if p <= 0:
                continue
            x = 96 + i * 300
            paste_im(base, card(278, 92, fill=(255, 255, 255, 240), outline=(226, 232, 240, 255)), x, 460, p)
            paste_im(base, sp_icon(ic, col, 28), x + 18, 492, p)
            ftxt(base, x + 58, 492, t1, font_semi(19), INK, p)
            ftxt(base, x + 58, 520, t2, font("BeVietnamPro-Regular.ttf", 16), MUT, p)
    ftxt(base, 96, 576, "Cân bằng tải chỉ là một mảnh ghép của bức tranh lớn.",
         font("BeVietnamPro-Regular.ttf", 20), MUT, seg(t, b0 + 0.55, b0 + 0.95))

    # Kết
    c0 = fr(tl, "S12", 2, 0.05)[0]
    p = seg(t, c0, c0 + 0.5)
    d.rectangle([0, 640, int(W * p), 640 + 6], fill=(245, 158, 11, 255))
    paste_im(base, sp_icon("shield-check", BLUE, 52), 96, 676, p)
    ftxt(base, 166, 690, "AN TECH ACADEMY", font("BeVietnamPro-Bold.ttf", 34), NAVY, p)
    ftxt(base, 166, 730, "Hiểu công nghệ, làm chủ tương lai!", font("BeVietnamPro-Regular.ttf", 21), MUT, p)
    ftxt(base, 96, 800, "Hệ thống của bạn sẽ… thở đều hơn.", font("BeVietnamPro-Bold.ttf", 40), NAVY,
         seg(t, c0 + 0.3, c0 + 0.8))
    draw_marker(d, 100, 846, 640, 846, seg(t, c0 + 0.55, c0 + 1.1), AMBER, 7, 5)
    paste_im(base, pill("Bài tiếp theo: caching & CDN", MUT, WHITE, 20, 44, "cloud"), 96, 880,
             seg(t, c0 + 0.7, c0 + 1.1))
    # ảnh kết (hiện sớm để lấp khoảng trống nửa dưới)
    shot(base, IMG["arch_simple"], 700, 660, 760, 250, seg(t, a0 + 1.0, a0 + 1.5), t,
         1.03, 1.1, 0.03, 0.0, "Một kiến trúc · bốn thuật toán", BLUE, 14)

    sheen(base, lin(t, 0.8, 3.8), 20)
    _an(base, tl, "S12", t, "wave", look=-1)
    subtitle_band(d, subs_for(tl, "S12", t))
    return base


def events_S12(tl):
    a0 = tl["S12"]["starts"][0]
    b0 = fr(tl, "S12", 1, 0.05)[0]
    c0 = fr(tl, "S12", 2, 0.05)[0]
    return [(a0, "whoosh", None, 0.7)] + [(a0 + 0.08 + i * 0.14, "pop", None, 0.6) for i in range(4)] + \
           [(b0, "tick", None, 0.45), (c0, "chime", None, 0.8), (c0 + 0.6, "success", None, 0.7)]


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10, "S11": draw_S11, "S12": draw_S12}

EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03, "S04": events_S04,
          "S05": events_S05, "S06": events_S06, "S07": events_S07, "S08": events_S08,
          "S09": events_S09, "S10": events_S10, "S11": events_S11, "S12": events_S12}
