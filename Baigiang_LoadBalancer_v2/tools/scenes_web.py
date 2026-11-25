# -*- coding: utf-8 -*-
"""10 cảnh Load Balancer v2 (~5 phút). Nền sáng blueprint, giáo viên xuyên suốt,
sơ đồ vector tự dựng, nét vẽ tay, gói request chuyển động. Ảnh nguồn chỉ làm ngữ cảnh."""
import math, re
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB, F_BRAND,
                  font, ease, seg, lin, tw, wrap, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, subtitle_band, subs_for, GRID,
                  rich_width)
import character

ROOT = "D:/Edit/Baigiang_LoadBalancer_v2"
IMG = {n: f"{ROOT}/img/{n}.png" for n in (
    "sale_crowd", "server_overheat", "ops_monitor", "arch_public_ip", "arch_simple",
    "lb_screen", "dc_corridor", "net_fiber", "algo_4up", "algo_wide", "server_fail")}

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10"]
SAMPLE = ["S01", "S02", "S03"]
XFADE = 0.4

ANX = {s: (1660, 1020, 0.95) for s in ORDER}
PURPLE = (109, 91, 208, 255)
PURPLE_L = (170, 158, 245, 255)
MINT = (232, 248, 244, 255)
RED_L = (255, 237, 237, 255)
BLUE_L = (110, 156, 255, 255)
AMBER_L = (255, 199, 118, 255)
SKY = (228, 238, 255, 255)
DARK = (11, 19, 34, 255)

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



# ================================================================ helpers mới
F_XL  = font("BeVietnamPro-Bold.ttf", 104)
F_L   = font("BeVietnamPro-Bold.ttf", 64)
F_M   = font("BeVietnamPro-SemiBold.ttf", 42)
F_B   = font("BeVietnamPro-Regular.ttf", 29)
F_S   = font("BeVietnamPro-Regular.ttf", 23)
F_MONO= font("JetBrainsMono-var.ttf", 21)


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
    x, y, sc = ANX[sid]
    character.paste(base, x, y, t, pose, look, talk(tl, sid, t), sc)


def _lbhex(base, cx, cy, r, p=1.0, color=BLUE, label="LB"):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
           for a in (-90, -30, 30, 90, 150, 210)]
    d.polygon(pts, fill=WHITE, outline=color)
    d.line(pts + [pts[0]], fill=color, width=4, joint="curve")
    ftxt(base, cx, cy - 2, label, font("BeVietnamPro-Bold.ttf", int(r * 0.62)),
         color, p, "mm")


def _bar(base, x, y, w, q, color=BLUE, h=10, bg=(226, 234, 246, 255)):
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=bg)
    d.rounded_rectangle([x, y, x + max(4, int(w * max(0, min(1, q)))), y + h],
                        h // 2, fill=color)


def _stat(base, x, y, num, label, color=NAVY, p=1.0):
    ftxt(base, x, y, num, F_L, color, p)
    ftxt(base, x + 2, y + 76, label, F_S, MUT, p)


# ================================================================ S01 — HOOK
def draw_S01(t, tl):
    base, d = _base("01 · MỞ ĐẦU")
    s = tl["S01"]
    q1 = seg(t, 0.15, 0.95)
    ftxt(base, 100, 166, "CASE STUDY  ·  12/12", F_S, AMBER_D, q1)
    ftxt(base, 98, 222, "LOAD", F_XL, NAVY, q1)
    ftxt(base, 98, 330, "BALANCER", F_XL, BLUE, seg(t, 0.35, 1.0))
    ftxt(base, 102, 456, "Bộ cân bằng tải", F_M, NAVY, seg(t, 0.5, 1.0))
    desc = wrap("Giữ website đứng vững khi hàng nghìn người truy cập cùng lúc.", F_B, 700)
    for i, ln in enumerate(desc):
        ftxt(base, 102, 526 + i * 42, ln, F_B, MUT, seg(t, 0.7 + i * 0.08, 1.0))

    px, py, pw, ph = 980, 150, 520, 450
    base.alpha_composite(card(pw, ph), (px, py))
    dd = ImageDraw.Draw(base)
    ftxt(base, px + 28, py + 40, "CAO ĐIỂM 12/12", F_S, MUT, seg(t, 0.5, 1.0))
    dd.ellipse([px + pw - 62, py + 30, px + pw - 40, py + 52], fill=AMBER)
    _stat(base, px + 28, py + 78, "5.000", "người truy cập cùng lúc", AMBER_D, seg(t, 0.7, 1.0))
    _stat(base, px + 28, py + 214, "110.000", "lượt truy cập / ngày", NAVY, seg(t, 0.9, 1.0))
    dd.line([px + 28, py + 316, px + pw - 28, py + 316], fill=BORDER, width=2)
    ftxt(base, px + 28, py + 344, "Một server duy nhất", F_S, RED, seg(t, 1.05, 1.0))
    for i, (lab, q) in enumerate((("CPU", 0.91), ("RAM", 0.86), ("Độ trễ", 0.78))):
        yy = py + 372 + i * 24
        ftxt(base, px + 28, yy, lab, font("BeVietnamPro-Medium.ttf", 18), MUT, 1)
        _bar(base, px + 108, yy - 7, 300, q * seg(t, 1.1 + i * 0.05, 1.0),
             RED if i < 2 else AMBER, 9)

    if s["starts"][1] <= t:
        q = seg(t, s["starts"][1], s["starts"][1] + 0.8)
        _lbhex(base, 1150, 690, 48, q, TEAL, "LB")
        dd.line([1150 + 52, 690, 1240, 690], fill=TEAL, width=4)
        for i in range(3):
            x = 1262 + i * 92
            ic = sp_icon("server", TEAL, 44)
            base.alpha_composite(ic, (x, 668))
            ftxt(base, x + 22, 728, f"S{i+1:02d}", F_S, MUT, q)

    draw_marker(d, 100, 486, 500, 486, seg(t, 1.0, 1.35), AMBER, 7, 3)
    draw_marker_circle(d, 1310, 694, 268, 84,
                       seg(t, s["starts"][1] + 0.5, s["starts"][1] + 1.4),
                       AMBER, 5, 5)
    _an(base, tl, "S01", t, "point_left" if t < s["starts"][1] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    s = tl["S01"]
    return [(0.3, "pop", None, 0.20), (s["starts"][1] - 0.1, "whoosh", None, 0.16),
            (s["starts"][1] + 0.5, "pop", None, 0.18)]


# ================================================================ S02 — SẬP
def draw_S02(t, tl):
    base, d = _base("02 · VẤN ĐỀ")
    s = tl["S02"]
    _head(base, "Một server gánh 5.000 kết nối", "Cao điểm 12/12 — request dồn hết về một chỗ",
          p=seg(t, 0.1, 0.8))

    shot(base, IMG["sale_crowd"], 100, 250, 380, 540, seg(t, 0.25, 0.8), t,
         caption="5.000 người cùng lúc", radius=16)
    shot(base, IMG["server_overheat"], 1000, 250, 380, 270, seg(t, 0.4, 0.95), t,
         caption="Server quá nhiệt", cap_color=RED, radius=16)
    shot(base, IMG["ops_monitor"], 1000, 560, 380, 240, seg(t, 0.55, 1.0), t,
         caption="Cảnh báo quá tải", cap_color=RED, radius=16)

    sx, sy, sw, sh = 520, 250, 420, 430
    base.alpha_composite(card(sw, sh), (sx, sy))
    dd = ImageDraw.Draw(base)
    ic = sp_icon("server", RED, 40)
    base.alpha_composite(ic, (sx + 26, sy + 26))
    ftxt(base, sx + 80, sy + 44, "BACKEND DUY NHẤT", font("BeVietnamPro-Bold.ttf", 22), RED, 1)
    ftxt(base, sx + 26, sy + 80, "1 máy · 5.000 kết nối dồn về", F_S, MUT, 1)
    q2 = seg(t, s["starts"][1], s["starts"][1] + 1.2)
    seen = t >= s["starts"][1]
    for i, (lab, val, col, qv) in enumerate((("CPU", "96%", RED, 0.96),
                                            ("RAM", "92%", RED, 0.92),
                                            ("Độ trễ", "8,4 s", AMBER_D, 0.78))):
        yy = sy + 142 + i * 62
        ftxt(base, sx + 26, yy, lab, font("BeVietnamPro-Medium.ttf", 21), MUT, 1)
        ftxt(base, sx + sw - 26, yy, val, font("BeVietnamPro-Bold.ttf", 24), col, q2, "rm")
        _bar(base, sx + 26, yy + 26, sw - 52, qv * (q2 if seen else 0.0), col, 9)
    if seen:
        ftxt(base, sx + 26, sy + 348, "Trang quay mãi…", F_S, AMBER_D, seg(q2, 0.4, 1))
    else:
        ftxt(base, sx + 26, sy + 348, "Đang xử lý request…", F_S, MUT, 1)

    if t > s["starts"][1] + 0.8:
        qe = seg(t, s["starts"][1] + 0.8, s["starts"][1] + 1.3)
        for i, txt in enumerate(("502 Bad Gateway", "Thanh toán thất bại")):
            im = sp_chip(txt, RED, RED_L, 20, "alert-triangle", 44)
            paste_im(base, im, sx + 10, sy + sh + 16 + i * 52, qe)

    draw_marker_circle(d, sx + sw - 52, sy + 142, 62, 30,
                       seg(t, s["starts"][1] + 0.5, s["starts"][1] + 1.2), RED, 5, 4)
    draw_marker(d, sx + 26, sy + 392, sx + 250, sy + 392,
                seg(t, s["starts"][1] + 1.2, s["starts"][1] + 1.8), AMBER, 6, 2)
    _an(base, tl, "S02", t, "think", look=-1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    s = tl["S02"]
    return [(0.4, "pop", None, 0.18), (s["starts"][1], "deny", None, 0.24),
            (s["starts"][1] + 0.45, "thud", None, 0.20),
            (s["starts"][1] + 0.9, "marker", 0.7, 0.16)]


# ================================================================ S03 — ĐỊNH NGHĨA
def draw_S03(t, tl):
    base, d = _base("03 · KHÁI NIỆM")
    s = tl["S03"]
    _head(base, "Load Balancer là gì?", "Người điều phối lưu lượng đứng trước các server",
          p=seg(t, 0.1, 0.8))

    dx, dy, dw, dh = 96, 232, 600, 330
    base.alpha_composite(card(dw, dh), (dx, dy))
    dd = ImageDraw.Draw(base)
    ftxt(base, dx + 30, dy + 50, "LOAD BALANCER", font("BeVietnamPro-Bold.ttf", 34), BLUE,
         seg(t, 0.15, 0.6))
    ftxt(base, dx + 30, dy + 92, "Bộ cân bằng tải", F_S, MUT, seg(t, 0.25, 0.7))
    dd.line([dx + 30, dy + 120, dx + dw - 30, dy + 120], fill=BORDER, width=2)
    hy = dy + 164 + 2 * 44
    qh = seg(t, s["starts"][1] + 0.1, s["starts"][1] + 0.7)
    rrect_a(base, (dx + 18, hy - 26, dx + 232, hy + 22), 10, CREAM, None, 0, qh)
    for i, (txt, col) in enumerate((("Nhận request", NAVY), ("Chọn server phù hợp", NAVY),
                                     ("Chia đều tải", BLUE))):
        ftxt(base, dx + 32, dy + 164 + i * 44, txt, F_B, col, seg(t, 0.35 + i * 0.12, 0.9))
    draw_marker(d, dx + 32, hy + 28, dx + 230, hy + 28, qh, AMBER, 6, 3)

    tx, ty, tw, th = 750, 232, 790, 470
    p = seg(t, s["starts"][1], s["starts"][1] + 0.7)
    if p > 0:
        base.alpha_composite(card(tw, th), (tx, ty))
        ftxt(base, tx + 30, ty + 40, "TRẠM THU PHÍ — ẨN DỤ", F_S, MUT, p)
        ry0, ry1 = ty + 296, ty + 404
        rrect_a(base, (tx + 26, ry0, tx + tw - 26, ry1), 24, (236, 242, 250, 255), None, 0, p)
        for ly in (ty + 332, ty + 368):
            for xx in range(tx + 40, tx + tw - 40, 34):
                d.line([xx, ly, xx + 18, ly], fill=WHITE, width=4)
        lanes = [ty + 314, ty + 350, ty + 386]
        box = (tx + 250, ty + 78, tx + tw - 26, ty + 178)
        rrect_a(base, box, 16, SKY, BLUE, 2, p)
        ic = sp_icon("users", BLUE, 34)
        base.alpha_composite(ic, (box[0] + 18, box[1] + 20))
        ftxt(base, box[0] + 62, box[1] + 36, "1 NHÂN VIÊN ĐIỀU PHỐI", font_semi(20), BLUE, p)
        ftxt(base, box[0] + 62, box[1] + 66, "Load Balancer", F_S, MUT, p)
        for i, cy in enumerate(lanes):
            span = tw - 190
            x = tx + 94 + ((t - s["starts"][1]) * (95 + i * 12) + i * 150) % span
            col = (AMBER, BLUE, TEAL)[i]
            d.rounded_rectangle([x, cy - 13, x + 54, cy + 13], 7, fill=WHITE,
                                outline=col, width=3)
            d.rounded_rectangle([x + 10, cy - 8, x + 26, cy + 8], 4, fill=col)
            d.ellipse([x + 8, cy + 10, x + 20, cy + 20], fill=NAVY)
            d.ellipse([x + 34, cy + 10, x + 46, cy + 20], fill=NAVY)
        gx = tx + 520
        for i, cy in enumerate(lanes):
            draw_conn(d, 1150 + i * 110, box[3], gx + 20, cy - 20,
                      seg(t, s["starts"][1] + 0.3 + i * 0.1,
                          s["starts"][1] + 0.9 + i * 0.1), TEAL, width=3)
            d.line([gx - 58, cy - 18, gx, cy - 18], fill=AMBER, width=5)
            d.rounded_rectangle([gx, cy - 18, gx + 38, cy + 18], 7, fill=WHITE,
                                outline=AMBER, width=3)
            d.ellipse([gx + 15, cy - 6, gx + 25, cy + 4],
                      fill=GREEN if p > 0.5 else AMBER)
            ftxt(base, tx + 40, cy, f"L{i+1}", font_semi(17), MUT, p, "lm")

    t3 = s["starts"][2] if len(s["starts"]) > 2 else s["total"] + 1.0
    if t > t3:
        q3 = seg(t, t3, t3 + 0.7)
        im = sp_chip("Không xử lý nghiệp vụ — chỉ điều phối", TEAL, MINT, 22,
                     "circle-check", 48)
        paste_im(base, im, 96, 604, q3)
        ftxt(base, 96, 684, "Điểm cốt lõi: LB giúp nhiều server cùng làm việc.",
             F_S, NAVY, q3)

    _an(base, tl, "S03", t, "present" if t < t3 else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    s = tl["S03"]
    ev = [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16),
          (s["starts"][1] + 0.5, "marker", 0.7, 0.16)]
    if len(s["starts"]) > 2:
        ev.append((s["starts"][2], "chime", None, 0.14))
    return ev


# ================================================================ S04 — KIẾN TRÚC
def draw_S04(t, tl):
    base, d = _base("04 · KIẾN TRÚC")
    s = tl["S04"]
    _head(base, "Bốn lớp của một hệ thống", "Client → Load Balancer → Backend → Database",
          p=seg(t, 0.1, 0.7))
    q1 = seg(t, 0.25, 0.9)
    q2 = seg(t, s["starts"][1], s["starts"][1] + 0.9)
    q3 = seg(t, s["starts"][2], s["starts"][2] + 0.8)

    node(base, 100, 320, 250, 160, "smartphone", "CLIENT", "Trình duyệt / App", BLUE, p=q1)
    _lbhex(base, 450, 400, 60, q1, BLUE, "LB")
    ftxt(base, 450, 478, "LOAD BALANCER", font_semi(21), NAVY, q1, "mm")
    ftxt(base, 450, 506, "cửa ngõ tiếp nhận", F_S, MUT, q1, "mm")

    ftxt(base, 690, 290, "BACKEND · XỬ LÝ NGHIỆP VỤ", font_semi(19), MUT, q2)
    for i in range(3):
        srv_card(base, 690, 320 + i * 104, 290, 92, i + 1, "ok", q2, None, None,
                 BLUE, "Node.js · Express")
    node(base, 1120, 320, 260, 160, "database", "DATABASE", "Lưu trữ dữ liệu", TEAL, p=q2)

    draw_conn(d, 350, 400, 390, 400, q1, BLUE, width=4)
    for i in range(3):
        draw_conn(d, 510, 400, 690, 366 + i * 104, q2, BLUE, width=3)
    for i in range(3):
        draw_conn(d, 980, 366 + i * 104, 1120, 400, q2, TEAL, width=2)

    if t >= s["starts"][2]:
        qq = min(1.0, ((t - s["starts"][2]) % 2.2) / 1.3)
        packet(base, [(355, 400), (450, 400), (690, 470)], qq, AMBER, 10)
        qq2 = min(1.0, (((t - s["starts"][2]) + 1.1) % 2.2) / 1.0)
        packet(base, [(980, 470), (1120, 400)], qq2, AMBER, 8)
        im = sp_chip("LB đứng giữa nhưng không thay server làm việc", AMBER, CREAM, 21,
                     "circle-help", 46)
        paste_im(base, im, 100, 706, q3)
        ftxt(base, 100, 782, "4 lớp, một luồng: request đi vào — dữ liệu trả về.",
             F_B, NAVY, seg(t, s["starts"][2] + 0.4, s["starts"][2] + 1.0))

    _an(base, tl, "S04", t, "point_left" if t < s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    s = tl["S04"]
    return [(0.3, "pop", None, 0.2), (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][2], "tick", None, 0.14),
            (s["starts"][2] + 0.6, "marker", 0.6, 0.14),
            (s["starts"][2] + 1.7, "chime", None, 0.12)]


# ================================================================ S05 — LUỒNG
def draw_S05(t, tl):
    base, d = _base("05 · LUỒNG REQUEST")
    s = tl["S05"]
    _head(base, "Một request đi qua những đâu?", "Luồng xử lý và cách mở rộng hệ thống",
          p=seg(t, 0.1, 0.7))
    q = seg(t, 0.2, 0.8)

    node(base, 100, 300, 240, 130, "globe", "Trình duyệt", "HTTP request", BLUE, p=q)
    _lbhex(base, 430, 365, 52, q, BLUE, "LB")
    for i in range(3):
        srv_card(base, 640, 260 + i * 105, 270, 90, i + 1, "ok", q, None, None,
                 BLUE, "Node.js · Express")
    node(base, 1040, 300, 210, 130, "database", "Database", "truy vấn", TEAL, p=q)

    draw_conn(d, 340, 365, 378, 365, q, BLUE, width=4)
    for i in range(3):
        draw_conn(d, 482, 365, 640, 305 + i * 105, q, BLUE, width=3)
        draw_conn(d, 910, 305 + i * 105, 1040, 365, q, (184, 198, 222, 255), width=2)

    lx, ly, lw, lh = 1300, 260, 260, 330
    base.alpha_composite(card(lw, lh), (lx, ly))
    ftxt(base, lx + 22, ly + 36, "NHẬT KÝ REQUEST", font_semi(18), MUT, 1)
    rows = (("#1042", "S01", "42 ms", BLUE), ("#1043", "S02", "39 ms", TEAL),
            ("#1044", "S03", "47 ms", GREEN))
    for i, (rid, srv, ms, col) in enumerate(rows):
        b = s["starts"][1] if i else s["starts"][0]
        rr = seg(t, b + (0.8 if i < 2 else 1.6), b + (1.3 if i < 2 else 2.1))
        yy = ly + 96 + i * 72
        if rr > 0:
            rrect_a(base, (lx + 18, yy - 26, lx + lw - 18, yy + 26), 10, ICE, None, 0, rr)
            ftxt(base, lx + 30, yy, rid, font("JetBrainsMono-var.ttf", 18), NAVY, rr)
            ftxt(base, lx + 112, yy, "→ " + srv, font_semi(18), col, rr)
            ftxt(base, lx + lw - 30, yy, ms, font("BeVietnamPro-Medium.ttf", 17), MUT, rr, "rm")

    if t < s["starts"][2]:
        idx = 0 if t < s["starts"][1] else 1
        t0 = s["starts"][0] + 1.0 if idx == 0 else s["starts"][1] + 0.6
        if t >= t0:
            pts = [(345, 365), (430, 365), (640, 305 + idx * 105)]
            qq = min(1.0, ((t - t0) % 1.9) / 1.2)
            packet(base, pts, qq, AMBER, 9)

    if t >= s["starts"][2]:
        qs = seg(t, s["starts"][2], s["starts"][2] + 0.8)
        base.alpha_composite(card(580, 240), (100, 620))
        ftxt(base, 128, 660, "SCALE-UP · DỌC", font_semi(22), AMBER_D, qs)
        ic = sp_icon("server", AMBER, 62)
        base.alpha_composite(ic, (128, 696))
        ftxt(base, 208, 712, "Nâng CPU / RAM", F_B, NAVY, qs)
        ftxt(base, 208, 750, "cho một máy mạnh hơn", F_S, MUT, qs)
        ftxt(base, 128, 814, "Giới hạn bởi phần cứng", F_S, RED, qs)

        base.alpha_composite(card(660, 240), (720, 620))
        ftxt(base, 748, 660, "SCALE-OUT · NGANG", font_semi(22), BLUE, qs)
        _lbhex(base, 802, 752, 28, qs, BLUE, "LB")
        for i in range(3):
            draw_conn(d, 828, 752, 864 + i * 84, 752, qs, BLUE, width=3)
            ic = sp_icon("server", BLUE, 52)
            base.alpha_composite(ic, (864 + i * 84, 726))
        ftxt(base, 748, 814, "Thêm máy + Load Balancer", F_B, NAVY, qs)
        ftxt(base, 1140, 702, "Horizontal", font_semi(24), GREEN, qs)
        ftxt(base, 1140, 736, "Scaling", font_semi(24), GREEN, qs)

    _an(base, tl, "S05", t, "point_left" if t < s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    s = tl["S05"]
    return [(0.3, "pop", None, 0.18), (s["starts"][0] + 1.0, "tick", None, 0.16),
            (s["starts"][1] + 0.6, "tick", None, 0.16),
            (s["starts"][2], "whoosh", None, 0.16),
            (s["starts"][2] + 0.7, "success", None, 0.16)]


# ================================================================ S06 — RR / WRR
def _tabs(base, active, p):
    labels = (("Round Robin", "route"), ("Weighted RR", "scale"),
              ("Least Connections", "git-fork"), ("IP Hash", "key-round"))
    x = 100
    for i, (lab, ic) in enumerate(labels):
        act = i == active
        im = sp_chip(lab, BLUE if act else (148, 163, 184, 255),
                     SKY if act else WHITE, 19, ic, 42)
        paste_im(base, im, x, 238, p)
        x += im.width + 12


def draw_S06(t, tl):
    base, d = _base("06 · THUẬT TOÁN")
    s = tl["S06"]
    _head(base, "Thuật toán chọn server", "Bốn cách phổ biến để chia tải", p=seg(t, 0.1, 0.7))
    stage2 = t >= s["starts"][1]
    stage3 = t >= s["starts"][2]
    _tabs(base, 0 if not stage3 else 1, seg(t, 0.1, 0.7))

    if not stage2:
        items = (("Round Robin", "Luân phiên theo thứ tự", "route"),
                 ("Weighted RR", "Chia theo trọng số", "scale"),
                 ("Least Connections", "Chọn máy ít kết nối", "git-fork"),
                 ("IP Hash", "Băm IP, giữ phiên", "key-round"))
        for i, (nm, ds, ic) in enumerate(items):
            x = 100 + i * 352
            y = 330
            base.alpha_composite(card(320, 290), (x, y))
            base.alpha_composite(sp_icon(ic, BLUE, 54), (x + 28, y + 32))
            ftxt(base, x + 28, y + 128, nm, font_semi(22), NAVY, seg(t, 0.3 + i * 0.12, 0.8))
            for k, ln in enumerate(wrap(ds, F_S, 262)):
                ftxt(base, x + 28, y + 176 + k * 32, ln, F_S, MUT,
                     seg(t, 0.36 + i * 0.12 + k * 0.04, 0.9))
        ftxt(base, 100, 690, "Mỗi thuật toán trả lời một câu hỏi khác nhau.", F_B, NAVY,
             seg(t, 0.8, 1.0))

    elif not stage3:
        el = t - s["starts"][1]
        _lbhex(base, 240, 520, 60, 1, BLUE, "LB")
        for i, cy in enumerate((428, 538, 648)):
            srv_card(base, 740, cy - 48, 300, 96, i + 1, "ok", 1)
            draw_conn(d, 300, 520, 740, cy, 1, BLUE, width=3)
        i = int(el / 1.15) % 3
        qq = min(1.0, (el % 1.15) / 0.85)
        packet(base, [(300, 520), (520, 520), (740, 428 + i * 110)], qq, AMBER, 10)
        draw_marker_circle(d, 890, 428 + i * 110, 170, 64, 1, AMBER, 4, 3)
        x = 100
        for k in range(5):
            if el >= 0.4 + k * 0.7:
                im = sp_chip(f"#{k+1} → S0{(k % 3)+1}", BLUE, ICE, 18, None, 40)
                paste_im(base, im, x, 760, 1)
                x += im.width + 10
        base.alpha_composite(card(330, 320), (1150, 380))
        ftxt(base, 1178, 418, "ROUND ROBIN", font_semi(20), BLUE, 1)
        ftxt(base, 1178, 458, "Lần lượt 1 → 2 → 3", F_B, NAVY, 1)
        ftxt(base, 1178, 500, "rồi quay lại 1.", F_B, NAVY, 1)
        ftxt(base, 1178, 556, "Hợp khi các server", F_S, MUT, 1)
        ftxt(base, 1178, 588, "cấu hình giống nhau.", F_S, MUT, 1)
        base.alpha_composite(sp_icon("refresh-cw", BLUE, 40), (1178, 626))

    else:
        el = t - s["starts"][2]
        _lbhex(base, 240, 520, 60, 1, BLUE, "LB")
        wts = (3, 1, 1)
        for i, cy in enumerate((428, 538, 648)):
            srv_card(base, 740, cy - 48, 300, 96, i + 1, "ok", 1)
            draw_conn(d, 300, 520, 740, cy, 1, BLUE, width=3)
            im = sp_chip(f"×{wts[i]}", AMBER if i == 0 else (148, 163, 184, 255),
                         CREAM if i == 0 else WHITE, 18, None, 34)
            paste_im(base, im, 740 + 300 - im.width - 12, cy - 48 + 10, 1)
        seq = (0, 0, 0, 1, 2)
        i = seq[int(el / 1.2) % 5]
        qq = min(1.0, (el % 1.2) / 0.9)
        packet(base, [(300, 520), (520, 520), (740, 428 + i * 110)], qq, AMBER, 10)
        draw_marker_circle(d, 890, 428 + i * 110, 170, 64, 1, AMBER, 4, 3)
        x = 100
        for k in range(5):
            if el >= 0.4 + k * 0.7:
                im = sp_chip(f"#{k+1} → S0{seq[k]+1}", AMBER_D, CREAM, 18, None, 40)
                paste_im(base, im, x, 760, 1)
                x += im.width + 10
        base.alpha_composite(card(330, 320), (1150, 380))
        ftxt(base, 1178, 418, "WEIGHTED RR", font_semi(20), AMBER_D, 1)
        ftxt(base, 1178, 458, "Server mạnh nhận", F_B, NAVY, 1)
        ftxt(base, 1178, 500, "nhiều request hơn.", F_B, NAVY, 1)
        ftxt(base, 1178, 556, "S01 : S02 : S03", F_S, MUT, 1)
        ftxt(base, 1178, 588, "= 3 : 1 : 1", font_semi(22), AMBER_D, 1)
        bx, by, bw = 1178, 634, 274
        for frac, col in ((0.6, AMBER), (0.2, BLUE), (0.2, TEAL)):
            w = int(bw * frac)
            d.rounded_rectangle([bx, by, bx + w - 3, by + 15], 6, fill=col)
            bx += w + 1
        for lab, x0 in (("S01", 1178), ("S02", 1343), ("S03", 1400)):
            ftxt(base, x0, 660, lab, font("BeVietnamPro-Medium.ttf", 14), MUT, 1)

    _an(base, tl, "S06", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    s = tl["S06"]
    ev = [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16)]
    for k in range(5):
        ev.append((s["starts"][1] + 0.4 + k * 0.7, "tick", None, 0.14))
    ev.append((s["starts"][2], "whoosh", None, 0.16))
    for k in range(5):
        ev.append((s["starts"][2] + 0.4 + k * 0.7, "tick", None, 0.14))
    return ev


# ================================================================ S07 — LC / IP HASH
def draw_S07(t, tl):
    base, d = _base("07 · THUẬT TOÁN (TT)")
    s = tl["S07"]
    _head(base, "Chọn theo kết nối và theo IP", "Least Connections và IP Hash", p=seg(t, 0.1, 0.7))
    _tabs(base, 2 if t < s["starts"][1] else 3, 1)

    if t < s["starts"][1] + 0.12:
        _lbhex(base, 240, 500, 60, 1, BLUE, "LB")
        conns = (100, 30, 10)
        for i, cy in enumerate((408, 518, 628)):
            srv_card(base, 760, cy - 48, 300, 96, i + 1, "ok", 1, None, conns[i], BLUE)
            draw_conn(d, 300, 500, 760, cy, 1, BLUE, width=3)
        el = t - s["starts"][0]
        qq = min(1.0, (el % 1.8) / 1.3)
        packet(base, [(300, 500), (520, 500), (760, 628)], qq, AMBER, 10)
        draw_marker_circle(d, 910, 628, 170, 64, 1, AMBER, 4, 3)
        im = sp_chip("CHỌN", AMBER_D, CREAM, 16, "circle-check", 34)
        paste_im(base, im, 1010, 574, 1)
        base.alpha_composite(card(330, 320), (1180, 380))
        ftxt(base, 1208, 418, "LEAST CONN.", font_semi(20), BLUE, 1)
        ftxt(base, 1208, 458, "Chọn server đang ít", F_B, NAVY, 1)
        ftxt(base, 1208, 500, "kết nối nhất.", F_B, NAVY, 1)
        ftxt(base, 1208, 556, "S03 chỉ có 10 →", F_S, MUT, 1)
        ftxt(base, 1208, 588, "request tiếp theo", F_S, MUT, 1)
        ftxt(base, 1208, 620, "ưu tiên S03.", F_S, MUT, 1)

    if t >= s["starts"][1]:
        q = seg(t, s["starts"][1], s["starts"][1] + 0.6)
        users = (("NGƯỜI DÙNG A", "203.0.113.7", 400, BLUE),
                 ("NGƯỜI DÙNG B", "198.51.100.22", 560, TEAL))
        for lab, ip, cy, col in users:
            rrect_a(base, (120, cy - 48, 490, cy + 48), 14, WHITE, col, 2, q)
            ftxt(base, 146, cy - 22, lab, font_semi(16), MUT, q)
            ftxt(base, 146, cy + 16, ip, font("JetBrainsMono-var.ttf", 22), NAVY, q)
        rrect_a(base, (560, 424, 830, 576), 16, SKY, BLUE, 2, q)
        ftxt(base, 590, 462, "hash(IP)", font("JetBrainsMono-var.ttf", 24), BLUE, q)
        ftxt(base, 590, 500, "% 3", font("JetBrainsMono-var.ttf", 24), BLUE, q)
        ftxt(base, 590, 540, "chọn server", F_S, MUT, q)
        for i, cy in enumerate((408, 518, 628)):
            srv_card(base, 1000, cy - 48, 300, 96, i + 1, "ok", q)
        draw_conn(d, 490, 400, 560, 440, q, BLUE, width=3)
        draw_conn(d, 490, 560, 560, 560, q, TEAL, width=3)
        draw_conn(d, 830, 450, 1000, 408, q, BLUE, width=3)
        draw_conn(d, 830, 520, 1000, 518, q, TEAL, width=3)
        im = sp_chip("Cùng IP → cùng server (giữ phiên)", BLUE, ICE, 18, "refresh-cw", 40)
        paste_im(base, im, 560, 620, seg(t, s["starts"][1] + 1.2, s["starts"][1] + 1.6))
        im = sp_chip("Không đảm bảo tuyệt đối khi danh sách server đổi", AMBER_D, CREAM,
                     18, "alert-triangle", 40)
        paste_im(base, im, 120, 730, seg(t, s["starts"][1] + 1.8, s["starts"][1] + 2.4))

    _an(base, tl, "S07", t, "think" if t < s["starts"][1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    s = tl["S07"]
    return [(0.3, "pop", None, 0.18), (0.9, "tick", None, 0.14),
            (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][1] + 0.6, "tick", None, 0.14),
            (s["starts"][1] + 1.2, "chime", None, 0.12),
            (s["starts"][1] + 1.9, "marker", 0.6, 0.14)]


# ================================================================ S08 — HEALTH CHECK
def _dash(base, x0, y0, x1, y1, p, color, width=3, dash=12, gap=9):
    if p <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0) or 1
    d = ImageDraw.Draw(base)
    n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = (i * (dash + gap)) / L
        if a >= p:
            break
        b = min(a + dash / L, p)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a,
                x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=color, width=width)


def draw_S08(t, tl):
    base, d = _base("08 · HEALTH CHECK")
    s = tl["S08"]
    _head(base, "Health Check — tự loại server lỗi", "LB định kỳ hỏi từng server: còn sống không?",
          p=seg(t, 0.1, 0.7))
    fail = t >= s["starts"][1] + 0.8
    rec = t >= s["starts"][2] + 0.6

    _lbhex(base, 240, 500, 62, 1, BLUE, "LB")
    ftxt(base, 240, 582, "LOAD BALANCER", font_semi(19), NAVY, 1, "mm")

    for i, cy in enumerate((400, 520, 640)):
        st = "bad" if (i == 1 and fail and not rec) else "ok"
        srv_card(base, 800, cy - 50, 300, 100, i + 1, st, 1)
        _dash(base, 302, 500, 800, cy, 1, (150, 168, 196, 255), 2, 10, 8)
        qq = (t * 0.6 + i * 0.3) % 1.0
        dot(base, 302 + (800 - 302) * qq, 500 + (cy - 500) * qq, 5, TEAL, 0.9)

    im = sp_chip("GET /health", TEAL, MINT, 18, "gauge", 38)
    paste_im(base, im, 520, 296, seg(t, 0.4, 0.8))

    base.alpha_composite(card(330, 420), (1180, 320))
    ftxt(base, 1208, 356, "TRẠNG THÁI", font_semi(18), MUT, 1)
    for i, cy in enumerate((430, 500, 570)):
        if i == 1 and fail and not rec:
            col, txt = RED, "TIMEOUT"
        elif i == 1 and rec:
            col, txt = GREEN, "200 OK"
        else:
            col, txt = GREEN, "200 OK"
        dot(base, 1214, cy, 6, col, 1)
        ftxt(base, 1234, cy, f"S0{i+1}", font_semi(18), NAVY, 1)
        ftxt(base, 1480, cy, txt, font("BeVietnamPro-Medium.ttf", 17), col, 1, "rm")
        if i == 1 and fail and not rec:
            ftxt(base, 1208, 636, "S02 · tạm ngắt khỏi nhóm", F_S, RED,
                 seg(t, s["starts"][1] + 1.2, s["starts"][1] + 1.7))
        if i == 1 and rec:
            ftxt(base, 1208, 636, "S02 · đã trở lại nhóm", F_S, GREEN,
                 seg(t, s["starts"][2] + 0.6, s["starts"][2] + 1.0))
    d.line([1208, 616, 1482, 616], fill=BORDER, width=2)

    if fail and not rec:
        for k in range(2):
            cy = (400, 640)[k]
            qq = ((t - s["starts"][1]) * 0.8 + k * 0.5) % 1.0
            packet(base, [(302, 500), (560, 500), (800, cy)], min(1, qq * 1.3), AMBER, 8)
    if rec:
        draw_marker_circle(d, 950, 520, 154, 54,
                           seg(t, s["starts"][2] + 0.4, s["starts"][2] + 0.9), GREEN, 5, 3)

    if t >= s["starts"][2]:
        ftxt(base, 110, 820, "Một server lỗi không kéo cả website chết theo.", F_M, NAVY,
             seg(t, s["starts"][2] + 0.6, s["starts"][2] + 1.2))

    _an(base, tl, "S08", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    s = tl["S08"]
    ev = [(0.3, "pop", None, 0.18)]
    for k in range(8):
        ev.append((0.8 + k * 1.1, "tick", None, 0.10))
    ev += [(s["starts"][1] + 0.8, "deny", None, 0.22),
           (s["starts"][1] + 1.2, "thud", None, 0.18),
           (s["starts"][2] + 0.6, "success", None, 0.18)]
    return ev


# ================================================================ S09 — THỰC TẾ
def draw_S09(t, tl):
    base, d = _base("09 · THỰC TẾ")
    s = tl["S09"]
    _head(base, "Load Balancer trong thực tế", "Phần mềm, dịch vụ đám mây và giới hạn",
          p=seg(t, 0.1, 0.7))

    if t < s["starts"][1] + 0.15:
        tools = (("Nginx", "Phần mềm · Reverse Proxy", "server"),
                 ("HAProxy", "Phần mềm · Hiệu năng cao", "shield-check"),
                 ("AWS ELB", "Dịch vụ đám mây", "cloud"),
                 ("Google CLB", "Dịch vụ đám mây", "cloud"))
        for i, (nm, ds, ic) in enumerate(tools):
            x = 100 + i * 352
            base.alpha_composite(card(300, 180), (x, 300))
            base.alpha_composite(sp_icon(ic, BLUE, 44), (x + 24, 326))
            ftxt(base, x + 82, 350, nm, font_semi(23), NAVY, seg(t, 0.3 + i * 0.12, 0.8))
            ftxt(base, x + 24, 404, ds, F_S, MUT, seg(t, 0.36 + i * 0.12, 0.9))
            paste_im(base, sp_chip("PHẦN MỀM" if i < 2 else "ĐÁM MÂY",
                                   AMBER_D if i < 2 else TEAL, CREAM if i < 2 else MINT,
                                   15, None, 30), x + 24, 440, 1)
        ftxt(base, 100, 552, "Cùng một vai trò: nhận request và điều phối về backend.",
             F_B, NAVY, seg(t, 0.9, 1.0))

    if s["starts"][1] <= t < s["starts"][2] + 0.3:
        p = seg(t, s["starts"][1], s["starts"][1] + 0.5)
        lines = ["upstream backend {", "    server 192.168.1.101;",
                 "    server 192.168.1.102;", "    server 192.168.1.103;", "}",
                 "server {", "    listen 80;", "    location / {",
                 "        proxy_pass http://backend;", "    }", "}"]
        code_panel(base, 100, 300, 640, lines,
                   typed=seg(t, s["starts"][1] + 0.9, s["starts"][1] + 4.2), title="nginx.conf")
        rrect_a(base, (820, 300, 1380, 660), 18, WHITE, BORDER, 2, p)
        ftxt(base, 850, 340, "UPSTREAM BACKEND", font_semi(20), MUT, p)
        for i, ip in enumerate(("192.168.1.101", "192.168.1.102", "192.168.1.103")):
            rrect_a(base, (850, 380 + i * 70, 1350, 438 + i * 70), 12, ICE, None, 0, p)
            ftxt(base, 874, 409 + i * 70, f"Server 0{i+1}", font_semi(19), NAVY, p)
            ftxt(base, 1140, 409 + i * 70, ip, font("JetBrainsMono-var.ttf", 18), MUT, p)
        ftxt(base, 850, 604, "Nginx nhận request → chọn backend", F_S, MUT, p)

    if t >= s["starts"][2]:
        q = seg(t, s["starts"][2], s["starts"][2] + 0.7)
        base.alpha_composite(card(1380, 440), (100, 290))
        ftxt(base, 136, 342, "LB KHÔNG CHỮA ĐƯỢC MỌI BỆNH", font_semi(30), RED, q)
        ftxt(base, 136, 390, "Những vấn đề nằm ngoài tầng cân bằng tải:", F_S, MUT, q)
        probs = ("Database quá tải", "Câu SQL chậm", "Thanh toán lỗi",
                 "Phiên đăng nhập", "Đặt hàng trùng", "Thiếu cache")
        for i, txt in enumerate(probs):
            x = 136 + (i % 3) * 440
            y = 440 + (i // 3) * 74
            im = sp_chip(txt, AMBER_D, CREAM, 19, "alert-triangle", 42)
            paste_im(base, im, x, y, seg(t, s["starts"][2] + 0.2 + i * 0.1,
                                          s["starts"][2] + 0.8 + i * 0.1))
        ftxt(base, 136, 640, "Cần xử lý thêm ở tầng dữ liệu và nghiệp vụ.", F_B, NAVY,
             seg(t, s["starts"][2] + 1.0, s["starts"][2] + 1.5))

    _an(base, tl, "S09", t, "present" if t < s["starts"][1] else "write", look=-1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    s = tl["S09"]
    return [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][1] + 1.0, "tick", None, 0.12),
            (s["starts"][1] + 1.6, "tick", None, 0.12),
            (s["starts"][2], "deny", None, 0.18),
            (s["starts"][2] + 1.0, "chime", None, 0.12)]


# ================================================================ S10 — TỔNG KẾT
def draw_S10(t, tl):
    base, d = _base("10 · TỔNG KẾT")
    s = tl["S10"]
    _head(base, "Tóm lại", "Bốn thuật toán · Health Check · bước tiếp theo",
          p=seg(t, 0.1, 0.7))
    q = seg(t, 0.2, 0.8)

    node(base, 100, 300, 220, 120, "smartphone", "Client", None, BLUE, p=q)
    _lbhex(base, 420, 360, 48, q, BLUE, "LB")
    for i in range(3):
        ic = sp_icon("server", TEAL, 44)
        base.alpha_composite(ic, (560 + i * 104, 338))
        ftxt(base, 560 + i * 104 + 22, 398, f"S0{i+1}", F_S, MUT, q)
        draw_conn(d, 468, 360, 560 + i * 104, 360, q, BLUE, width=3)
    draw_conn(d, 320, 360, 372, 360, q, BLUE, width=4)

    im = sp_chip("Health Check loại server lỗi", GREEN, MINT, 19, "shield-check", 44)
    paste_im(base, im, 100, 480, seg(t, 0.5, 0.9))
    ftxt(base, 100, 566, "Bước tiếp theo:", F_S, MUT, seg(t, 0.8, 1.0))
    x = 100
    for nm in ("Cache", "Message Queue", "Database Scaling", "CDN"):
        im = sp_chip(nm, (100, 116, 139, 255), ICE_2, 17, None, 38)
        paste_im(base, im, x, 604, seg(t, 0.9, 1.0))
        x += im.width + 10

    algos = (("Round Robin", "luân phiên", "route"), ("Weighted RR", "theo trọng số", "scale"),
             ("Least Conn.", "ít kết nối nhất", "git-fork"), ("IP Hash", "băm theo IP", "key-round"))
    for i, (nm, ds, ic) in enumerate(algos):
        x = 960 + (i % 2) * 300
        y = 300 + (i // 2) * 160
        base.alpha_composite(card(270, 130), (x, y))
        base.alpha_composite(sp_icon(ic, BLUE, 36), (x + 22, y + 24))
        ftxt(base, x + 70, y + 44, nm, font_semi(20), NAVY, seg(t, 0.45 + i * 0.1, 0.9))
        ftxt(base, x + 22, y + 92, ds, F_S, MUT, seg(t, 0.5 + i * 0.1, 0.95))

    if t >= s["starts"][2]:
        q3 = seg(t, s["starts"][2], s["starts"][2] + 0.7)
        rrect_a(base, (96, 240, 900, 800), 26, NAVY, None, 0, q3)
        ftxt(base, 150, 322, "BÀI 12 · HẠ TẦNG WEB", F_S, AMBER, q3)
        ftxt(base, 150, 386, "CẢM ƠN CÁC BẠN", F_L, WHITE, q3)
        ftxt(base, 150, 478, "AN TECH ACADEMY", font_semi(30), AMBER, q3)
        ftxt(base, 150, 552, "Hiểu Load Balancer là bước đầu", F_B, (200, 214, 236, 255), q3)
        ftxt(base, 150, 594, "để thiết kế hệ thống chịu tải lớn.", F_B, (200, 214, 236, 255), q3)
        im = pill("Theo dõi kênh · Bài tiếp theo", NAVY, AMBER, 20, 48)
        paste_im(base, im, 150, 664, q3)

    _an(base, tl, "S10", t, "wave" if t >= s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    s = tl["S10"]
    return [(0.3, "pop", None, 0.18), (0.6, "chime", None, 0.12),
            (s["starts"][2], "success", None, 0.2),
            (s["starts"][2] + 0.5, "chime", None, 0.16)]


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10}
EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03, "S04": events_S04,
          "S05": events_S05, "S06": events_S06, "S07": events_S07, "S08": events_S08,
          "S09": events_S09, "S10": events_S10}
