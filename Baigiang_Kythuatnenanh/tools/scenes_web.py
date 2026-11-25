# -*- coding: utf-8 -*-
"""12 cảnh bài giảng "Kỹ thuật nén ảnh trong website" (~5 phút).
17 ảnh người dùng cung cấp được dùng đúng ngữ cảnh (Ken Burns, khung chứng cứ);
sơ đồ, bảng so sánh và code panel tự dựng bằng vector. Nhân vật An xuất hiện xuyên suốt."""
import math, re
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB, F_BRAND,
                  font, ease, seg, lin, tw, wrap, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, subtitle_band, subs_for)
import character

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
IMG = {n: f"{ROOT}/img/{n}.png" for n in (
    "elcapitan_sizes", "raw_vs_jpeg", "jpeg_quality_grid", "screenshot_guide",
    "jpeg_artifacts_face", "product_devices", "cat_compression", "before_after_5mb",
    "formats_4up", "png_features", "lake_dolomites", "imgix_score", "text_quality",
    "logo_transparent", "shop_product_page", "loading_fast_slow", "map_jpeg_png")}

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"]
XFADE = 0.3

ANX = {"S01": (1668, 930, 0.46), "S02": (1760, 926, 0.36), "S03": (1752, 920, 0.36),
       "S04": (1752, 920, 0.36), "S05": (1752, 920, 0.36), "S06": (1752, 920, 0.36),
       "S07": (1752, 920, 0.36), "S08": (1770, 930, 0.32), "S09": (1790, 936, 0.32),
       "S10": (1752, 920, 0.36), "S11": (1752, 920, 0.36), "S12": (1500, 930, 0.50)}
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
    if i >= len(s["starts"]):
        return 1e9, 1e9
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
_th = {}


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


def _thumb(path, size=84):
    key = (path, size)
    if key not in _th:
        im = _cover(path)
        s = max(size / im.width, size / im.height)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        x0 = (im.width - size) // 2
        y0 = (im.height - size) // 2
        c = im.crop((x0, y0, x0 + size, y0 + size)).convert("RGBA")
        c.putalpha(_rmask(size, size, 10))
        out = Image.new("RGBA", (size + 6, size + 6), (0, 0, 0, 0))
        d = ImageDraw.Draw(out)
        d.rounded_rectangle([0, 2, size + 4, size + 5], 11, fill=(0, 0, 0, 80))
        out.alpha_composite(c, (3, 3))
        d.rounded_rectangle([2, 1, size + 3, size + 2], 11,
                            outline=(255, 255, 255, 190), width=2)
        _th[key] = out
    return _th[key]


def overlay_grad(base, a_left=220, a_right=40, vertical=False, color=(8, 15, 30)):
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


# ---------------------------------------------------------------- code panels
_tok_cache = {}


def _tok_js(line):
    key = ("js", line)
    if key in _tok_cache:
        return _tok_cache[key]
    if line.strip().startswith("//"):
        out = [(line, (110, 128, 152, 255))]
        _tok_cache[key] = out
        return out
    out = []
    for part in re.split(r"('[^']*'|\"[^\"]*\"|\b\d+\b|[A-Za-z_$][\w$]*|.)", line):
        if not part:
            continue
        if part[0] in "'\"":
            out.append((part, (255, 190, 120, 255)))
        elif part.isdigit():
            out.append((part, (120, 220, 200, 255)))
        elif part in ("const", "require", "true", "false", "new"):
            out.append((part, (150, 200, 255, 255)))
        elif part in ("resize", "webp", "toFile", "sharp"):
            out.append((part, (124, 190, 255, 255)))
        elif part in ("width", "withoutEnlargement", "quality"):
            out.append((part, (255, 214, 150, 255)))
        elif part.strip() == "":
            out.append((part, (226, 234, 246, 255)))
        else:
            out.append((part, (226, 234, 246, 255)))
    _tok_cache[key] = out
    return out


def _tok_html(line):
    key = ("html", line)
    if key in _tok_cache:
        return _tok_cache[key]
    out = []
    for part in re.split(r"(\"[^\"]*\"|<|>|/|=[A-Za-z-]+|[A-Za-z-]+)", line):
        if not part:
            continue
        if part.startswith('"'):
            out.append((part, (255, 190, 120, 255)))
        elif part in ("<", ">", "/"):
            out.append((part, (120, 220, 200, 255)))
        elif part.startswith("="):
            out.append((part, (226, 234, 246, 255)))
        elif part in ("img", "picture", "source", "srcset", "src", "alt", "width",
                      "height", "loading", "lazy", "sizes"):
            col = (255, 214, 150, 255) if part in ("loading", "lazy", "srcset") else (150, 200, 255, 255)
            out.append((part, col))
        else:
            out.append((part, (226, 234, 246, 255)))
    _tok_cache[key] = out
    return out


def code_panel(base, x, y, w, lines, typed=1.0, title="compress.js", lang="js"):
    if typed <= 0:
        return 0
    size, lh = 21, 33
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
    toks = _tok_html if lang == "html" else _tok_js
    total = sum(len(l) for l in lines)
    budget = int(total * min(1.0, typed))
    yy = 62
    for i, line in enumerate(lines):
        d.text((22, yy), f"{i + 1:02d}", font=nf, fill=(86, 104, 132, 255), anchor="lm")
        xx = 66
        reveal = max(0, min(len(line), budget))
        for tx, col in toks(line):
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
    bg = kb(IMG["loading_fast_slow"], W, H, t, 1.03, 1.10, panx=0.03, pany=0.01,
            radius=0, shadow=False, dur=14)
    base.alpha_composite(bg, (0, 0))
    overlay_grad(base, 244, 96)
    d = ImageDraw.Draw(base)

    draw_tracked(d, (104, 46), "AN TECH ACADEMY", F_BRAND, (240, 245, 255, 235), 3.4, seg(t, 0.1, 0.9))
    d.rounded_rectangle([104, 78, 168, 83], 2, fill=AMBER)
    headbar(base, seg(t, 0.2, 1.2), "BÀI GIẢNG · XỬ LÝ ẢNH", dark=True)

    paste_im(base, pill("IMAGE COMPRESSION · CASE STUDY", AMBER, (16, 25, 44, 220), 20, 42),
             104, 132, seg(t, 0.2, 0.8))

    ftxt(base, 104, 262, "NÉN ẢNH", font("BeVietnamPro-Bold.ttf", 100), WHITE, seg(t, 0.1, 0.7))
    ftxt(base, 104, 378, "TRONG WEBSITE", font("BeVietnamPro-Bold.ttf", 100), AMBER,
         seg(t, 0.25, 0.9))
    draw_marker(d, 108, 440, 108 + 560, 440, seg(t, 1.2, 1.9), AMBER, 8, 3)
    ftxt(base, 104, 486, "30 tấm ảnh × 5 MB — trang chủ ì ạch, khách bỏ đi.",
         font("BeVietnamPro-Medium.ttf", 30), (228, 236, 250, 255), seg(t, 0.6, 1.2))

    # lưới 30 thumbnail
    a0 = s["starts"][0]
    names = list(IMG.values())
    gw, gh = 84, 84
    for i in range(30):
        p = seg(t, a0 + 0.9 + i * 0.045, a0 + 1.25 + i * 0.045)
        if p <= 0:
            continue
        col, row = i % 6, i // 6
        x = 1164 + col * 96
        y = 152 + row * 96
        th = _thumb(names[i % len(names)], gw)
        paste_im(base, th, x, y, p * 0.96)
    paste_im(base, pill("30 ảnh · mỗi ảnh 5 MB", RED, (40, 14, 20, 225), 19, 40),
             1164, 640, seg(t, a0 + 2.3, a0 + 2.8))

    # bộ đếm dung lượng (cue 2)
    c2a = fr(tl, "S01", 1, 0.05)[0]
    st = seg(t, c2a, c2a + 0.5)
    if st > 0:
        px, py, pw, ph = 104, 592, 520, 200
        rrect_a(base, [px, py, px + pw, py + ph], 18, (15, 24, 42, 205),
                (255, 255, 255, 46), 2, st)
        ftxt(base, px + 28, py + 36, "TỔNG DUNG LƯỢNG MỘT TRANG CHỦ",
             font("BeVietnamPro-SemiBold.ttf", 18), (176, 192, 216, 255), st)
        q = ease(min(1.0, max(0.0, (t - c2a - 0.2) / 1.2)))
        val = int(150 * q)
        ftxt(base, px + 28, py + 94, f"{val} MB", font("PlusJakartaSans-var.ttf", 62, 800),
             RED if q > 0.98 else AMBER, st)
        ftxt(base, px + 280, py + 104, "= 30 × 5 MB", font("BeVietnamPro-Medium.ttf", 22),
             (214, 226, 244, 255), st)
        bw = pw - 56
        d.rounded_rectangle([px + 28, py + 148, px + 28 + bw, py + 160], 6, fill=(48, 60, 82, 255))
        d.rounded_rectangle([px + 28, py + 148, px + 28 + max(3, int(bw * q)), py + 160], 6,
                            fill=RED)

    # cue 3: chốt chủ đề
    c3 = fr(tl, "S01", 2, 0.05)[0]
    paste_im(base, pill("Hôm nay: làm nhẹ ảnh — vẫn đẹp", TEAL, (12, 42, 40, 220), 21, 44, "eye"),
             104, 830, seg(t, c3, c3 + 0.6))

    for i in range(14):
        ph = (t * 0.2 + i * 0.37) % 1.0
        hx = 980 + (i * 137) % 860
        hy = 150 + ((i * 211) % 760) - ph * 90
        rr = 2 + (i % 3)
        d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=(255, 214, 150, 80))

    sheen(base, lin(t, 0.5, 3.5), 18)
    _an(base, tl, "S01", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    a0 = tl["S01"]["starts"][0]
    c2 = fr(tl, "S01", 1, 0.05)[0]
    c3 = fr(tl, "S01", 2, 0.05)[0]
    return ([(0.2, "whoosh", None, 0.55), (a0 + 0.9, "pop", None, 0.4),
             (a0 + 1.5, "pop", None, 0.35), (a0 + 2.1, "pop", None, 0.3),
             (c2, "thud", None, 0.7), (c3, "chime", None, 0.5)])


# ================================================================ S02 — VÌ SAO NÉN
def draw_S02(t, tl):
    base, d = _base()
    s = tl["S02"]
    d.ellipse([-280, 620, 520, 1380], fill=(253, 246, 227, 255))
    d.ellipse([1420, -280, 2180, 460], fill=(232, 240, 252, 255))
    headbar(base, seg(t, 0.2, 1.0), "01 · VÌ SAO?")
    _title(base, tl, "S02", t, "Vì sao phải nén ảnh?",
           "Mỗi MB đều là chi phí thật của người làm web")

    a0 = s["starts"][0]
    rows = [("gauge", "Tốc độ tải", "Ảnh nặng = trang chậm", BLUE),
            ("cloud", "Băng thông", "Mỗi lần xem là một lần tải", TEAL),
            ("database", "Lưu trữ", "Ảnh gốc chiếm chỗ máy chủ", PURPLE)]
    for i, (ic, t1, t2, col) in enumerate(rows):
        p = seg(t, a0 + 0.1 + i * 0.14, a0 + 0.5 + i * 0.14)
        if p <= 0:
            continue
        y = 230 + i * 136
        rrect_a(base, [96, y, 656, y + 116], 16, (255, 255, 255, 248),
                (216, 224, 236, 255), 2, p)
        paste_im(base, sp_icon(ic, col, 40), 122, y + 38, p)
        ftxt(base, 182, y + 36, t1, font_semi(24), NAVY, p)
        ftxt(base, 182, y + 70, t2, font("BeVietnamPro-Regular.ttf", 20), MUT, p)

    # trải nghiệm (cue 2)
    c2 = fr(tl, "S02", 1, 0.05)[0]
    p2 = seg(t, c2, c2 + 0.55)
    if p2 > 0:
        rrect_a(base, [96, 660, 796, 826], 18, (255, 248, 233, 255), AMBER, 3, p2)
        paste_im(base, sp_icon("users", AMBER_D, 44), 124, 694, p2)
        ftxt(base, 186, 700, "Trải nghiệm = doanh thu", font("BeVietnamPro-Bold.ttf", 28),
             AMBER_D, p2)
        ftxt(base, 186, 742, "Trang tải chậm là trang khó bán hàng.", font_semi(21),
             NAVY, p2)
        ftxt(base, 186, 778, "Bạn đã bao giờ bỏ đi vì chờ quá lâu chưa?", font("BeVietnamPro-Regular.ttf", 19),
             MUT, p2)
        pulse = 0.5 + 0.5 * math.sin(t * 3.2)
        ring(base, 146, 716, 30 + 4 * pulse, AMBER, 0.35 * pulse, 2)

    # ảnh trang sản phẩm (cue 1)
    shot(base, IMG["shop_product_page"], 816, 190, 264, 500, seg(t, a0 + 0.5, a0 + 1.1), t,
         1.10, 1.04, 0.0, -0.03, "Trang sản phẩm", BLUE, 14)
    ftxt(base, 816, 702, "Ảnh nặng → chờ lâu", font("BeVietnamPro-Medium.ttf", 19), RED,
         seg(t, a0 + 1.2, a0 + 1.6))

    # ảnh imgix (cue 2)
    b0 = fr(tl, "S02", 1, 0.12)[0]
    shot(base, IMG["imgix_score"], 1112, 168, 660, 342, seg(t, b0, b0 + 0.75), t,
         0.86, 0.88, 0.0, 0.0, None, TEAL, 16)
    paste_im(base, pill("−96% dung lượng", TEAL, MINT, 20, 42, "trending-up"),
             1112, 532, seg(t, b0 + 0.4, b0 + 0.8))
    paste_im(base, pill("−41% thời gian tải", BLUE, ICE, 20, 42, "gauge"),
             1360, 532, seg(t, b0 + 0.55, b0 + 0.95))
    ftxt(base, 1112, 600, "Nén đúng cách: ảnh nhẹ hơn, tải nhanh hơn.",
         font("BeVietnamPro-Regular.ttf", 20), MUT, seg(t, b0 + 0.7, b0 + 1.1))

    sheen(base, lin(t, 0.8, 3.8), 16)
    _an(base, tl, "S02", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    a0 = tl["S02"]["starts"][0]
    b0 = fr(tl, "S02", 0, 0.5)[0]
    c2 = fr(tl, "S02", 1, 0.05)[0]
    return [(a0 + 0.1, "whoosh", None, 0.6)] + \
           [(a0 + 0.1 + i * 0.14, "pop", None, 0.4) for i in range(3)] + \
           [(b0, "tick", None, 0.5), (c2, "chime", None, 0.55)]


# ================================================================ S03 — ĐỊNH NGHĨA
def draw_S03(t, tl):
    base, d = _base()
    s = tl["S03"]
    d.ellipse([1420, 600, 2200, 1360], fill=(232, 244, 241, 255))
    headbar(base, seg(t, 0.2, 1.0), "02 · KHÁI NIỆM")
    _title(base, tl, "S03", t, "Nén ảnh là gì?", "Giảm dung lượng — vẫn giữ chất lượng đủ đẹp")

    a0 = s["starts"][0]
    # thẻ định nghĩa
    p = seg(t, a0 + 0.05, a0 + 0.55)
    if p > 0:
        rrect_a(base, [96, 226, 986, 486], 20, (255, 255, 255, 250), (214, 222, 234, 255), 2, p)
        ftxt(base, 128, 268, "NÉN ẢNH = GIẢM DUNG LƯỢNG", font("BeVietnamPro-Bold.ttf", 30),
             AMBER_D, p)
        lines = wrap("Quá trình giảm dung lượng hình ảnh bằng cách loại bỏ hoặc tổ chức lại "
                     "thông tin theo một thuật toán.", font("BeVietnamPro-Medium.ttf", 27), 800)
        for i, ln in enumerate(lines[:3]):
            ftxt(base, 128, 326 + i * 40, ln, font("BeVietnamPro-Medium.ttf", 27), NAVY,
                 seg(t, a0 + 0.3 + i * 0.1, a0 + 0.6 + i * 0.1))
        ftxt(base, 128, 452, "Giống dọn vali: vẫn đủ đồ, xếp khéo nên nhẹ hơn.",
             font("BeVietnamPro-Regular.ttf", 21), MUT, seg(t, a0 + 0.6, a0 + 1.0))
        draw_marker(d, 132, 300, 500, 300, seg(t, a0 + 0.45, a0 + 0.95), AMBER, 5, 7)

    # ảnh 5MB -> 350KB
    shot(base, IMG["before_after_5mb"], 1060, 250, 500, 319, seg(t, a0 + 0.4, a0 + 1.0), t,
         0.86, 0.88, 0.0, 0.0, "5 MB → 350 KB", TEAL, 18)

    # thanh so sánh (cue 2)
    c2 = fr(tl, "S03", 1, 0.05)[0]
    p2 = seg(t, c2, c2 + 0.5)
    if p2 > 0:
        rrect_a(base, [96, 526, 986, 726], 18, WHITE, (226, 232, 240, 255), 2, p2)
        q = seg(t, c2 + 0.2, c2 + 1.0)
        bw = 520
        ftxt(base, 124, 558, "TRƯỚC", font_semi(19), MUT, p2)
        d.rounded_rectangle([310, 542, 310 + bw, 574], 8, fill=RED)
        ftxt(base, 846, 558, "5 MB", font("PlusJakartaSans-var.ttf", 24, 800), RED, p2)
        ftxt(base, 124, 616, "SAU", font_semi(19), MUT, p2 * q)
        d.rounded_rectangle([310, 600, 310 + bw, 632], 8, fill=(236, 240, 246, 255))
        aw = max(4, int(bw * 0.07 * q))
        d.rounded_rectangle([310, 600, 310 + aw, 632], 8, fill=TEAL)
        ftxt(base, 846, 616, "350 KB", font("PlusJakartaSans-var.ttf", 24, 800), TEAL, p2 * q)
        ftxt(base, 846, 650, "−93%", font("BeVietnamPro-Bold.ttf", 24), TEAL, p2 * q)
        ftxt(base, 124, 688, "Ảnh sản phẩm · số liệu minh họa",
             font("BeVietnamPro-Regular.ttf", 18), MUT, p2 * q)

    # 4 lợi ích (cue 3)
    c3 = fr(tl, "S03", 2, 0.02)[0]
    chips = [("gauge", "Nhanh hơn"), ("cloud", "Ít băng thông"),
             ("database", "Ít lưu trữ"), ("users", "Khách ở lại")]
    for i, (ic, lab) in enumerate(chips):
        pp = seg(t, c3 + i * 0.14, c3 + 0.45 + i * 0.14)
        x = 96 + i * 224
        rrect_a(base, [x, 766, x + 208, 880], 14, WHITE, (216, 224, 236, 255), 2, pp)
        paste_im(base, sp_icon(ic, BLUE if i % 2 == 0 else TEAL, 34), x + 22, 790, pp)
        ftxt(base, x + 22, 846, lab, font_semi(20), NAVY, pp)

    # ảnh thiết bị nhỏ
    shot(base, IMG["product_devices"], 1090, 660, 460, 230, seg(t, c3 + 0.1, c3 + 0.6), t,
         0.86, 0.88, 0.0, 0.0, None, BLUE, 14)

    sheen(base, lin(t, 1.0, 4.0), 16)
    _an(base, tl, "S03", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    a0 = tl["S03"]["starts"][0]
    c2 = fr(tl, "S03", 1, 0.05)[0]
    c3 = fr(tl, "S03", 2, 0.02)[0]
    return ([(a0, "whoosh", None, 0.6), (a0 + 0.45, "marker", 0.5, 0.4),
             (c2, "tick", None, 0.5), (c3, "chime", None, 0.55)] +
            [(c3 + i * 0.14, "pop", None, 0.4) for i in range(4)])


# ================================================================ S04 — LOSSY
def draw_S04(t, tl):
    base, d = _base()
    s = tl["S04"]
    d.ellipse([-280, 620, 520, 1380], fill=(255, 240, 240, 255))
    headbar(base, seg(t, 0.2, 1.0), "03 · NÉN MẤT DỮ LIỆU")
    _title(base, tl, "S04", t, "Nén mất dữ liệu — Lossy",
           "Bỏ chi tiết mắt khó thấy, đổi lấy file nhỏ hơn nhiều")

    a0 = s["starts"][0]
    paste_im(base, pill("JPEG", AMBER, CREAM, 20, 40), 246, 186, seg(t, a0 + 0.1, a0 + 0.5))

    # bảng quality
    shot(base, IMG["jpeg_quality_grid"], 84, 238, 596, 451, seg(t, a0 + 0.15, a0 + 0.7), t,
         0.86, 0.86, 0.0, 0.0, "Quality 100 → 5", AMBER, 16)

    # slider quality (cue 2)
    c2 = fr(tl, "S04", 1, 0.04)[0]
    p2 = seg(t, c2, c2 + 0.5)
    if p2 > 0:
        rrect_a(base, [84, 728, 680, 900], 16, WHITE, (226, 232, 240, 255), 2, p2)
        ftxt(base, 112, 758, "Chất lượng (quality)", font_semi(20), MUT, p2)
        qs = seg(t, c2 + 0.15, c2 + 1.45)
        qual = int(round(90 - 40 * qs))
        d.rounded_rectangle([112, 800, 640, 812], 6, fill=(232, 236, 244, 255))
        d.rounded_rectangle([112, 800, 112 + max(4, int(528 * qs)), 812], 6, fill=AMBER)
        hx = 112 + 528 * qs
        d.ellipse([hx - 12, 794, hx + 12, 818], fill=AMBER)
        ftxt(base, 112, 838, f"Q{qual}", font("PlusJakartaSans-var.ttf", 26, 800), AMBER_D, p2)
        ftxt(base, 360, 838, "618 KB → 194 KB", font("BeVietnamPro-Medium.ttf", 21), NAVY, p2)
        if qs > 0.75:
            paste_im(base, pill("≈ 3× nhẹ hơn", TEAL, MINT, 19, 38),
                     112, 856, seg(t, c2 + 1.2, c2 + 1.6))

    # ảnh artifacts
    shot(base, IMG["jpeg_artifacts_face"], 700, 196, 560, 420, seg(t, a0 + 0.35, a0 + 0.9), t,
         0.86, 0.86, 0.0, 0.0, None, RED, 16)
    shot(base, IMG["text_quality"], 1280, 196, 280, 280, seg(t, a0 + 0.5, a0 + 1.0), t,
         0.86, 0.86, 0.0, 0.0, None, BLUE, 12)

    # zoom 8x8 (cue 3)
    c3 = fr(tl, "S04", 2, 0.03)[0]
    p3 = seg(t, c3, c3 + 0.5)
    if p3 > 0:
        rrect_a(base, [1000, 640, 1240, 880], 14, WHITE, AMBER, 3, p3)
        zoom = crop_frac(IMG["jpeg_artifacts_face"], 0.40, 0.46, 0.56, 0.62, 214, 198)
        paste_im(base, zoom, 1012, 652, p3)
        for k in range(1, 8):
            x = 1012 + k * 214 / 8
            y = 652 + k * 198 / 8
            d.line([x, 652, x, 850], fill=(255, 196, 110, 170), width=2)
            d.line([1012, y, 1226, y], fill=(255, 196, 110, 170), width=2)
        ftxt(base, 1120, 862, "ô 8×8 pixel", font_semi(18), AMBER_D, p3, "mm")
    paste_im(base, pill("chữ mảnh → răng cưa", RED, RED_L, 19, 38),
             1252, 500, seg(t, c3 + 0.2, c3 + 0.6))
    draw_marker_circle(d, 1420, 336, 150, 148, seg(t, c3 + 0.15, c3 + 0.7), RED, 4, 4)

    # ảnh mèo minh họa mức nén
    shot(base, IMG["cat_compression"], 700, 640, 280, 158, seg(t, a0 + 0.6, a0 + 1.1), t,
         0.86, 0.88, 0.0, 0.0, None, TEAL, 12)

    sheen(base, lin(t, 1.0, 4.0), 14)
    _an(base, tl, "S04", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    a0 = tl["S04"]["starts"][0]
    c2 = fr(tl, "S04", 1, 0.04)[0]
    c3 = fr(tl, "S04", 2, 0.03)[0]
    return [(a0, "whoosh", None, 0.6), (c2, "tick", None, 0.5),
            (c2 + 1.0, "deny", None, 0.35), (c3, "deny", None, 0.35)]


# ================================================================ S05 — LOSSLESS
def draw_S05(t, tl):
    base, d = _base()
    s = tl["S05"]
    d.ellipse([-260, 640, 540, 1400], fill=(236, 249, 246, 255))
    headbar(base, seg(t, 0.2, 1.0), "04 · NÉN KHÔNG MẤT DỮ LIỆU")
    _title(base, tl, "S05", t, "Nén không mất dữ liệu — Lossless",
           "Khôi phục y nguyên bản gốc — PNG là đại diện")

    a0 = s["starts"][0]
    paste_im(base, pill("PNG", TEAL, MINT, 20, 40), 246, 186, seg(t, a0 + 0.1, a0 + 0.5))
    shot(base, IMG["png_features"], 84, 236, 680, 425, seg(t, a0 + 0.2, a0 + 0.8), t,
         0.86, 0.86, 0.0, 0.0, None, TEAL, 16)

    # checklist
    c2 = fr(tl, "S05", 1, 0.05)[0]
    items = ["Không vứt chi tiết nào", "Khôi phục y nguyên", "Nét chữ sắc · nền trong suốt"]
    for i, it in enumerate(items):
        p = seg(t, a0 + 0.5 + i * 0.15, a0 + 0.85 + i * 0.15)
        y = 700 + i * 62
        paste_im(base, sp_icon("check-circle", TEAL, 30), 96, y - 15, p)
        ftxt(base, 142, y, it, font("BeVietnamPro-Medium.ttf", 23), NAVY, p)

    # logo trong suốt
    b0 = fr(tl, "S05", 1, 0.12)[0]
    shot(base, IMG["logo_transparent"], 800, 190, 580, 328, seg(t, b0, b0 + 0.75), t,
         0.86, 0.88, 0.0, 0.0, None, TEAL, 16)
    # bảng caro động mô phỏng vùng trong suốt
    cq = seg(t, b0 + 0.45, b0 + 0.9)
    if cq > 0:
        bx, by, bw2, bh2 = 860, 540, 460, 220
        rrect_a(base, [bx, by, bx + bw2, by + bh2], 14, (250, 252, 255, 255),
                (203, 214, 230, 255), 2, cq)
        cell = 30
        for gy in range(7):
            for gx in range(15):
                if (gx + gy) % 2 == 0:
                    continue
                x0 = bx + 3 + gx * cell - int((t * 22) % cell)
                y0 = by + 3 + gy * cell
                if bx + 3 <= x0 <= bx + bw2 - cell and by + 3 <= y0 <= by + bh2 - cell:
                    d.rectangle([x0, y0, x0 + cell, y0 + cell], fill=(226, 232, 240, 255))
        lion = crop_frac(IMG["logo_transparent"], 0.52, 0.06, 0.98, 0.94, 280, 168)
        paste_im(base, lion, 880, 556, cq)
        ftxt(base, 1176, 620, "nền trong suốt", font_semi(18), TEAL, cq)
        paste_im(base, sp_icon("check-circle", TEAL, 26), 1252, 668, cq, "mm")
    if cq > 0.5:
        paste_im(base, pill("giữ nét · không mất dữ liệu", TEAL, MINT, 19, 38),
                 800, 800, seg(t, b0 + 0.9, b0 + 1.3))

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S05", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    a0 = tl["S05"]["starts"][0]
    b0 = fr(tl, "S05", 1, 0.12)[0]
    return ([(a0, "whoosh", None, 0.6)] +
            [(a0 + 0.5 + i * 0.15, "tick", None, 0.4) for i in range(3)] +
            [(b0, "pop", None, 0.5), (b0 + 0.8, "success", None, 0.55)])


# ================================================================ S06 — 4 ĐỊNH DẠNG
def draw_S06(t, tl):
    base, d = _base()
    s = tl["S06"]
    d.ellipse([1400, 560, 2160, 1320], fill=(236, 242, 252, 255))
    headbar(base, seg(t, 0.2, 1.0), "05 · ĐỊNH DẠNG")
    _title(base, tl, "S06", t, "Bốn định dạng phổ biến",
           "Chọn theo nhu cầu — không theo thói quen")

    a0 = s["starts"][0]
    cards = [("JPEG", "nhẹ · ảnh chụp", AMBER, "scan"),
             ("PNG", "nét · trong suốt", TEAL, "layers"),
             ("WebP", "cân bằng hai kiểu", BLUE, "globe"),
             ("AVIF", "mới · nén rất tốt", PURPLE, "rocket")]
    for i, (nm, sub, col, ic) in enumerate(cards):
        p = seg(t, a0 + 0.08 + i * 0.14, a0 + 0.4 + i * 0.14)
        x = 96 + i * 384
        rrect_a(base, [x, 186, x + 356, 322], 16, WHITE, (216, 224, 236, 255), 2, p)
        paste_im(base, sp_icon(ic, col, 34), x + 20, 206, p)
        ftxt(base, x + 66, 208, nm, font("BeVietnamPro-Bold.ttf", 26), col, p)
        ftxt(base, x + 66, 242, sub, font("BeVietnamPro-Regular.ttf", 18), MUT, p)
        d.rounded_rectangle([x + 20, 306, x + 336, 312], 3, fill=col[:3] + (int(255 * p),))

    # ảnh 4up
    shot(base, IMG["formats_4up"], 360, 350, 840, 560, seg(t, a0 + 0.4, a0 + 1.0), t,
         0.86, 0.86, 0.0, 0.0, None, BLUE, 18)

    # thanh dung lượng (cue 2)
    c2 = fr(tl, "S06", 1, 0.05)[0]
    vals = [("JPEG", 128, AMBER), ("PNG", 512, TEAL), ("WebP", 78, BLUE), ("AVIF", 45, PURPLE)]
    base_y, maxh = 840, 330
    for i, (nm, kb_, col) in enumerate(vals):
        p = seg(t, c2 + 0.1 + i * 0.13, c2 + 0.55 + i * 0.13)
        if p <= 0:
            continue
        x = 1268 + i * 108
        hgt = int(maxh * kb_ / 512 * ease(min(1.0, (t - c2 - 0.1 - i * 0.13) / 0.7)))
        d.rounded_rectangle([x, base_y, x + 74, base_y + 6], 3, fill=(220, 226, 236, 255))
        if hgt > 2:
            d.rounded_rectangle([x, base_y - hgt, x + 74, base_y + 6], 8, fill=col)
        ftxt(base, x + 37, base_y - hgt - 22, f"{kb_} KB", font("PlusJakartaSans-var.ttf", 20, 800),
             col, p, "mm")
        ftxt(base, x + 37, base_y + 30, nm, font_semi(19), NAVY, p, "mm")
    ftxt(base, 1268, 902, "Theo infographic · ảnh khác, kết quả khác",
         font("BeVietnamPro-Regular.ttf", 18), MUT, seg(t, c2 + 0.6, c2 + 1.0))

    sheen(base, lin(t, 1.0, 4.0), 16)
    _an(base, tl, "S06", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    a0 = tl["S06"]["starts"][0]
    c2 = fr(tl, "S06", 1, 0.05)[0]
    return [(a0, "whoosh", None, 0.6)] + \
           [(a0 + 0.08 + i * 0.14, "pop", None, 0.45) for i in range(4)] + \
           [(c2 + 0.1 + i * 0.13, "tick", None, 0.4) for i in range(4)]


# ================================================================ S07 — CHỌN ĐỊNH DẠNG
def draw_S07(t, tl):
    base, d = _base()
    s = tl["S07"]
    d.ellipse([-260, 620, 520, 1340], fill=(253, 246, 227, 255))
    headbar(base, seg(t, 0.2, 1.0), "06 · CHỌN ĐỊNH DẠNG")
    _title(base, tl, "S07", t, "Chọn định dạng theo mục đích",
           "Ảnh chụp ≠ logo ≠ bản đồ chữ nhỏ")

    a0 = s["starts"][0]
    cols = [("smartphone", "Ảnh chụp · sản phẩm", "JPEG / WebP", BLUE),
            ("pen-tool", "Logo · icon", "PNG / SVG", TEAL),
            ("compass", "Bản đồ · chữ nhỏ", "PNG · nén nhẹ", AMBER)]
    for i, (ic, t1, t2, col) in enumerate(cols):
        p = seg(t, a0 + 0.1 + i * 0.15, a0 + 0.5 + i * 0.15)
        if p <= 0:
            continue
        x = 96 + i * 404
        rrect_a(base, [x, 186, x + 376, 288], 16, WHITE, (216, 224, 236, 255), 2, p)
        paste_im(base, sp_icon(ic, col, 38), x + 20, 208, p)
        ftxt(base, x + 72, 206, t1, font_semi(21), NAVY, p)
        ftxt(base, x + 72, 238, t2, font("BeVietnamPro-Bold.ttf", 19), col, p)
        if i < 2:
            draw_conn(d, x + 350, 238, x + 396, 238, p, (160, 174, 196, 255), width=4)

    # ba ảnh chứng cứ
    shot(base, IMG["raw_vs_jpeg"], 96, 350, 430, 271, seg(t, a0 + 0.4, a0 + 1.0), t,
         0.86, 0.86, 0.0, 0.0, "RAW vs JPEG", BLUE, 14)
    shot(base, IMG["elcapitan_sizes"], 552, 350, 400, 289, seg(t, a0 + 0.55, a0 + 1.1), t,
         0.86, 0.86, 0.0, 0.0, "JPEG 16,5 KB · WebP 17,8 KB", TEAL, 14)
    shot(base, IMG["map_jpeg_png"], 978, 350, 466, 285, seg(t, a0 + 0.7, a0 + 1.2), t,
         0.86, 0.86, 0.0, 0.0, "JPEG vs PNG", AMBER, 14)
    zoom = crop_frac(IMG["map_jpeg_png"], 0.03, 0.63, 0.55, 0.92, 250, 150)
    paste_im(base, zoom, 1444, 664, seg(t, a0 + 1.0, a0 + 1.35))
    rrect_a(base, [1444, 664, 1694, 814], 12, None, RED, 3, seg(t, a0 + 1.0, a0 + 1.35))

    # RAW (cue 2)
    c2 = fr(tl, "S07", 1, 0.05)[0]
    p2 = seg(t, c2, c2 + 0.55)
    if p2 > 0:
        rrect_a(base, [96, 690, 900, 900], 18, (255, 248, 233, 255), AMBER, 2, p2)
        paste_im(base, sp_icon("alert-triangle", AMBER_D, 40), 124, 720, p2)
        ftxt(base, 180, 718, "RAW / DNG: ảnh gốc để chỉnh sửa", font_semi(24), AMBER_D, p2)
        ftxt(base, 180, 754, "Nặng, trình duyệt không đọc được — chưa dành cho web.",
             font("BeVietnamPro-Regular.ttf", 21), MUT, p2)
        paste_im(base, pill("Xuất sang JPEG / WebP trước khi đăng", AMBER, CREAM, 19, 40, "arrow-right"),
                 180, 800, seg(t, c2 + 0.25, c2 + 0.65))
    ftxt(base, 978, 664, "Chữ nhỏ · nén mạnh → vỡ nét", font("BeVietnamPro-Medium.ttf", 19),
         RED, seg(t, a0 + 1.1, a0 + 1.5))

    sheen(base, lin(t, 1.2, 4.2), 16)
    _an(base, tl, "S07", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    a0 = tl["S07"]["starts"][0]
    c2 = fr(tl, "S07", 1, 0.05)[0]
    return ([(a0, "whoosh", None, 0.6)] +
            [(a0 + 0.1 + i * 0.15, "pop", None, 0.4) for i in range(3)] +
            [(c2, "deny", None, 0.5), (c2 + 0.3, "tick", None, 0.4)])


# ================================================================ S08 — SHARP
JS_LINES = [
    "const sharp = require('sharp');",
    "",
    "sharp('product.jpg')",
    "  .resize({ width: 800, withoutEnlargement: true })",
    "  .webp({ quality: 80 })",
    "  .toFile('product.webp');",
]
JS_W = 1000
JS_Y = 262


def draw_S08(t, tl):
    base = Image.new("RGBA", (W, H), (10, 16, 29, 255))
    d = ImageDraw.Draw(base)
    for gx in range(60, 1900, 48):
        for gy in range(90, 980, 48):
            d.point((gx, gy), fill=(22, 31, 49, 255))
    d.ellipse([1300, -300, 2200, 560], fill=(14, 24, 42, 255))
    headbar(base, seg(t, 0.2, 1.0), "07 · THỰC HÀNH", dark=True)
    draw_tracked(d, (96, 44), "AN TECH ACADEMY", F_BRAND, (226, 234, 248, 220), 3.2, 1)
    ftxt(base, 96, 120, "Thực hành: nén bằng Sharp", font("BeVietnamPro-Bold.ttf", 46), WHITE,
         seg(t, 0.2, 0.8))
    ftxt(base, 96, 172, "Node.js · nén ngay trên máy chủ, tự động và rất nhanh.",
         font("BeVietnamPro-Regular.ttf", 23), (176, 190, 214, 255), seg(t, 0.35, 0.9))

    s = tl["S08"]
    a0 = s["starts"][0]
    tools = [("globe", "Squoosh"), ("package", "TinyPNG"), ("terminal", "ImageMagick")]
    for i, (ic, lab) in enumerate(tools):
        p = seg(t, a0 + 0.12 + i * 0.14, a0 + 0.45 + i * 0.14)
        x = 96 + i * 230
        rrect_a(base, [x, 208, x + 208, 252], 22, (18, 28, 46, 240), (90, 108, 136, 200), 2, p)
        paste_im(base, sp_icon(ic, (226, 234, 246, 255), 20), x + 16, 220, p)
        ftxt(base, x + 46, 230, lab, font("BeVietnamPro-Medium.ttf", 19), (226, 234, 246, 255), p)

    # code typing (cue 2)
    c2 = fr(tl, "S08", 1, 0.03)[0]
    c2e = fr(tl, "S08", 1, 0.90)[0]
    typed = ease(max(0.0, min(1.0, (t - c2 - 0.1) / max(0.8, c2e - c2))))
    code_panel(base, 88, JS_Y, JS_W, JS_LINES, typed if t > a0 + 0.3 else 0.0,
               "compress.js", "js")
    ftxt(base, 1080, 232, "npm install sharp", font("JetBrainsMono-var.ttf", 19),
         (140, 158, 186, 255), seg(t, a0 + 0.4, a0 + 0.8), "rm")

    # pipeline
    px, py, pw = 1130, 262, 540
    steps = [("product.jpg", "5 MB · ảnh gốc", AMBER),
             ("resize 800", "không phóng to", BLUE),
             ("WebP q80", "nén hợp lý", TEAL),
             ("product.webp", "350 KB (minh họa)", TEAL)]
    for i, (t1, t2, col) in enumerate(steps):
        p = seg(t, c2 + 0.15 + i * 0.18, c2 + 0.5 + i * 0.18)
        if p <= 0:
            continue
        y = py + i * 128
        rrect_a(base, [px, y, px + pw, y + 92], 14, (18, 28, 46, 245), col, 2, p)
        ftxt(base, px + 24, y + 30, t1, font("JetBrainsMono-var.ttf", 22), (232, 238, 248, 255), p)
        ftxt(base, px + 24, y + 62, t2, font("BeVietnamPro-Regular.ttf", 17), (150, 166, 192, 255), p)
        paste_im(base, sp_icon("server" if i == 0 else ("scan" if i == 1 else ("layers" if i == 2 else "check-circle")),
                               col, 30), px + pw - 46, y + 32, p)
        if i < 3:
            draw_conn(d, px + pw / 2, y + 94, px + pw / 2, y + 122, p, (90, 108, 136, 255), width=3)
    if t > c2 + 0.4:
        q = ((t - c2 - 0.4) % 2.4) / 2.4
        pts = [(px + pw / 2, py + 92), (px + pw / 2, py + 474)]
        packet(base, pts, q, TEAL, 7)

    # bảng giải nghĩa (cue 3)
    c3 = fr(tl, "S08", 2, 0.03)[0]
    terms = [("sharp", 0), ("resize", 3), ("withoutEnlargement", 3),
             ("webp", 4), ("quality 80", 4), ("toFile", 5)]
    for i, (term, li) in enumerate(terms):
        tp = c3 + i * (s["durs"][2] * 0.85 / 6)
        p = seg(t, tp, tp + 0.3)
        if p <= 0:
            continue
        col, row = i % 3, i // 3
        bx = 88 + col * 328
        by = 600 + row * 84
        rrect_a(base, [bx, by, bx + 310, by + 66], 12, (22, 34, 56, 245), AMBER, 2, p)
        ftxt(base, bx + 16, by + 22, term, font("JetBrainsMono-var.ttf", 19), AMBER, p)
        li_p = seg(t, tp, tp + 0.3)
        if li_p > 0:
            ly = JS_Y + 62 + li * 33
            rrect_a(base, [100, ly - 20, 100 + JS_W - 40, ly + 14], 8,
                    (255, 196, 110, 26), (255, 196, 110, int(190 * li_p)), 2, li_p)

    ftxt(base, 88, 806, "Một pipeline: đọc → resize → đổi định dạng → lưu.",
         font("BeVietnamPro-Medium.ttf", 22), (196, 210, 232, 255), seg(t, a0 + 1.4, a0 + 1.8))

    sheen(base, lin(t, 1.4, 4.4), 12)
    _an(base, tl, "S08", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    a0 = tl["S08"]["starts"][0]
    c2 = fr(tl, "S08", 1, 0.03)[0]
    c3 = fr(tl, "S08", 2, 0.03)[0]
    s = tl["S08"]
    return ([(a0 + 0.2, "whoosh", None, 0.55)] +
            [(c2 + 0.15 + i * 0.18, "tick", None, 0.4) for i in range(4)] +
            [(c3 + i * (s["durs"][2] * 0.85 / 6), "click", None, 0.35) for i in range(6)])


# ================================================================ S09 — HTML
HTML_LINES = [
    '<img',
    '  src="product.webp"',
    '  alt="Áo thun cotton"',
    '  width="800" height="600"',
    '  loading="lazy"',
    '  srcset="product-400.webp 400w,',
    '          product-800.webp 800w,',
    '          product-1600.webp 1600w">',
]
HTML_W = 880
HTML_Y = 246


def draw_S09(t, tl):
    base, d = _base()
    s = tl["S09"]
    d.ellipse([1420, 600, 2160, 1340], fill=(240, 243, 248, 255))
    headbar(base, seg(t, 0.2, 1.0), "08 · HIỂN THỊ ẢNH")
    _title(base, tl, "S09", t, "Hiển thị ảnh thông minh",
           "Nhẹ thôi chưa đủ — phải tải đúng lúc, đúng cỡ")

    a0 = s["starts"][0]
    typed = ease(max(0.0, min(1.0, (t - a0 - 0.2) / max(1.5, s["durs"][0] * 0.95))))
    code_panel(base, 84, HTML_Y, HTML_W, HTML_LINES, typed, "index.html", "html")
    c1 = fr(tl, "S09", 0, 0.25)[0]
    c2 = fr(tl, "S09", 1, 0.08)[0]

    def band(li, p, col=AMBER):
        ly = HTML_Y + 62 + li * 33
        rrect_a(base, [96, ly - 20, 96 + HTML_W - 44, ly + 14], 8,
                (255, 196, 110, 26), (255, 196, 110, int(200 * p)), 2, p)

    if t > c1:
        band(4, seg(t, c1, c1 + 0.4))
        paste_im(base, pill("loading=\"lazy\" — đợi khách cuộn tới", AMBER, CREAM, 19, 40),
                 984, 596, seg(t, c1 + 0.2, c1 + 0.6))
    if t > c2:
        band(3, seg(t, c2, c2 + 0.4))
        band(5, seg(t, c2 + 0.3, c2 + 0.7))
        paste_im(base, pill("width + height: giữ chỗ, trang không nhảy", TEAL, MINT, 19, 40),
                 984, 644, seg(t, c2 + 0.4, c2 + 0.8))
        paste_im(base, pill("srcset: trình duyệt tự chọn cỡ", BLUE, ICE, 19, 40),
                 984, 692, seg(t, c2 + 0.8, c2 + 1.2))

    # mock trình duyệt (lazy load)
    bx, by, bw, bh = 984, 260, 620, 320
    rrect_a(base, [bx, by, bx + bw, by + bh], 16, WHITE, (214, 222, 234, 255), 2, 1)
    d.rounded_rectangle([bx, by, bx + bw, by + 38], 16, fill=(241, 245, 250, 255))
    d.rectangle([bx, by + 24, bx + bw, by + 38], fill=(241, 245, 250, 255))
    d.ellipse([bx + 16, by + 12, bx + 28, by + 24], fill=(255, 95, 86))
    d.ellipse([bx + 34, by + 12, bx + 46, by + 24], fill=(255, 189, 46))
    d.ellipse([bx + 52, by + 12, bx + 64, by + 24], fill=(39, 201, 63))
    d.rounded_rectangle([bx + 80, by + 10, bx + bw - 20, by + 28], 8, fill=WHITE)
    ftxt(base, bx + 96, by + 19, "shop.example.com", font("BeVietnamPro-Regular.ttf", 15), MUT)
    # nội dung giả lập
    for i, (kw, hh) in enumerate([(bw - 60, 16), (420, 16), (bw - 90, 60)]):
        yy = by + 56 + i * 36
        d.rounded_rectangle([bx + 20, yy, bx + 20 + kw, yy + hh], 6, fill=(236, 240, 246, 255))
    # ảnh lazy trong khung
    img_y = by + 200
    loaded = seg(t, c1 + 0.6, c1 + 1.2)
    if loaded < 1:
        d.rounded_rectangle([bx + 20, img_y, bx + bw - 40, img_y + 96], 8,
                            fill=(228, 233, 241, 255))
        ftxt(base, bx + (bw - 20) / 2, img_y + 34, "chưa tải — ngoài màn hình",
             font("BeVietnamPro-Regular.ttf", 17), MUT, 1, "mm")
        paste_im(base, sp_icon("clock", MUT, 22), bx + (bw - 20) / 2 - 10, img_y + 52, 1)
    if loaded > 0:
        cat = crop_frac(IMG["cat_compression"], 0.04, 0.02, 0.62, 0.98, bw - 60, 96, 8)
        paste_im(base, cat, bx + 20, img_y, loaded)
        ftxt(base, bx + 30, img_y + 108, "ảnh tải khi cuộn gần tới", font_semi(16), TEAL, loaded)
    # thanh cuộn
    d.rounded_rectangle([bx + bw - 14, by + 52, bx + bw - 8, by + bh - 14], 3,
                        fill=(226, 232, 240, 255))
    q = ((t - a0) % 7.0) / 7.0
    ty = by + 52 + int((bh - 100) * q)
    d.rounded_rectangle([bx + bw - 14, ty, bx + bw - 8, ty + 56], 3, fill=BLUE_L)

    # layout shift demo (cue 2)
    if t > c2:
        p = seg(t, c2 + 0.2, c2 + 0.6)
        for i, (lab, col) in enumerate([("thiếu width/height → nhảy", RED),
                                        ("có width/height → giữ chỗ", TEAL)]):
            x = 96 + i * 380
            rrect_a(base, [x, 748, x + 340, 900], 14, WHITE, col, 2, p)
            jit = 0 if i else int(7 * math.sin(t * 6))
            d.rounded_rectangle([x + 16, 778 + jit, x + 250, 806 + jit], 5, fill=(230, 235, 243, 255))
            d.rounded_rectangle([x + 16, 814 + jit, x + 324, 874 + jit], 6,
                                fill=(219, 226, 236, 255) if i == 0 else (222, 240, 236, 255))
            ftxt(base, x + 16, 730, lab, font("BeVietnamPro-Medium.ttf", 17), col, p)

    sheen(base, lin(t, 1.2, 4.2), 14)
    _an(base, tl, "S09", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    a0 = tl["S09"]["starts"][0]
    c1 = fr(tl, "S09", 0, 0.25)[0]
    c2 = fr(tl, "S09", 1, 0.08)[0]
    return [(a0 + 0.2, "type", None, 0.3) if False else (a0 + 0.2, "tick", None, 0.35),
            (c1 + 0.6, "success", None, 0.55), (c2, "pop", None, 0.5),
            (c2 + 0.8, "tick", None, 0.4)]


# ================================================================ S10 — ỨNG DỤNG
def draw_S10(t, tl):
    base, d = _base()
    s = tl["S10"]
    d.ellipse([-260, 600, 540, 1380], fill=(236, 246, 252, 255))
    headbar(base, seg(t, 0.2, 1.0), "09 · ỨNG DỤNG")
    _title(base, tl, "S10", t, "Nén ảnh có mặt khắp nơi", "Hễ có ảnh trên web — là có chỗ cho nén ảnh")

    a0 = s["starts"][0]
    c2 = fr(tl, "S10", 1, 0.03)[0]
    cards = [("shop", "Thương mại điện tử", "Ảnh sản phẩm · trang danh sách mượt", BLUE, 0),
             ("file-text", "Tin tức", "Tối ưu ảnh bài viết", PURPLE, 1),
             ("lake", "Du lịch", "Giảm thư viện ảnh lớn", TEAL, 2),
             ("book-open", "Giáo dục", "Ảnh khóa học nhẹ, tải nhanh", AMBER, 3)]
    for i, (kind, t1, t2, col, idx) in enumerate(cards):
        p = seg(t, a0 + 0.1 + i * 0.13, a0 + 0.45 + i * 0.13) if t < c2 else \
            seg(t, c2 + 0.08 + (i - 2) * 0.13, c2 + 0.4 + (i - 2) * 0.13) if i >= 2 else 1
        if p <= 0:
            continue
        x = 90 + i * 406
        rrect_a(base, [x, 214, x + 380, 640], 18, WHITE, (216, 224, 236, 255), 2, p)
        if kind == "shop":
            im = crop_frac(IMG["shop_product_page"], 0.0, 0.02, 1.0, 0.31, 344, 214)
            paste_im(base, im, x + 18, 232, p)
        elif kind == "lake":
            im = crop_frac(IMG["lake_dolomites"], 0.05, 0.02, 0.95, 0.98, 344, 214)
            paste_im(base, im, x + 18, 232, p)
        else:
            d.rounded_rectangle([x + 18, 232, x + 362, 446], 12, fill=(x % 3 and (246, 249, 253, 255) or ICE))
            paste_im(base, sp_icon(kind, col, 86), x + 147, 300, p)
        ftxt(base, x + 24, 486, t1, font("BeVietnamPro-Bold.ttf", 25), NAVY, p)
        ftxt(base, x + 24, 524, t2, font("BeVietnamPro-Regular.ttf", 18), MUT, p)
        d.rounded_rectangle([x + 24, 610, x + 80, 616], 3, fill=col)

    # câu chốt
    c3 = fr(tl, "S10", 1, 0.55)[0]
    ftxt(base, 96, 712, "Ảnh nhẹ — nhưng vẫn đủ đẹp để bán hàng.", font("BeVietnamPro-Bold.ttf", 36),
         NAVY, seg(t, c2 + 0.6, c2 + 1.0))
    draw_marker(d, 100, 748, 760, 748, seg(t, c2 + 0.9, c2 + 1.4), AMBER, 6, 4)
    paste_im(base, pill("Cùng một kỹ thuật · bốn ngành khác nhau", BLUE, ICE, 19, 40),
             96, 782, seg(t, c3, c3 + 0.4))

    sheen(base, lin(t, 1.0, 4.0), 16)
    _an(base, tl, "S10", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    a0 = tl["S10"]["starts"][0]
    c2 = fr(tl, "S10", 1, 0.03)[0]
    return ([(a0 + 0.1, "whoosh", None, 0.55)] +
            [(a0 + 0.1 + i * 0.13, "pop", None, 0.4) for i in range(2)] +
            [(c2 + 0.08 + i * 0.13, "pop", None, 0.4) for i in range(2)] +
            [(c2 + 0.7, "chime", None, 0.45)])


# ================================================================ S11 — LƯU Ý
def draw_S11(t, tl):
    base, d = _base()
    s = tl["S11"]
    d.ellipse([1420, 560, 2180, 1340], fill=(253, 246, 235, 255))
    headbar(base, seg(t, 0.2, 1.0), "10 · LƯU Ý")
    _title(base, tl, "S11", t, "Vài lưu ý trước khi đăng", "Đừng đổi chất lượng lấy con số")

    a0 = s["starts"][0]
    c2 = fr(tl, "S11", 1, 0.03)[0]
    items = [("alert-triangle", "Đừng nén quá tay", "Ảnh vỡ — đẹp mấy cũng vô nghĩa", RED),
             ("scan", "Resize đúng kích thước hiển thị", "Đừng tải 4000px về khung 300px", BLUE),
             ("sliders-horizontal", "width, height + lazy loading", "Chống nhảy bố cục, tải đúng lúc", TEAL),
             ("cloud", "Cân nhắc CDN / dịch vụ tối ưu ảnh", "Nén tự động theo thiết bị", PURPLE),
             ("scale", "Cân bằng dung lượng ↔ chất lượng", "Nghệ thuật, không phải phép tính", AMBER)]
    for i, (ic, t1, t2, col) in enumerate(items):
        tp = a0 + 0.1 + i * 0.2 if i < 2 else c2 + 0.05 + (i - 2) * 0.2
        p = seg(t, tp, tp + 0.4)
        if p <= 0:
            continue
        y = 200 + i * 108
        rrect_a(base, [96, y, 800, y + 92], 14, WHITE, (219, 226, 238, 255), 2, p)
        paste_im(base, sp_icon(ic, col, 34), 118, y + 28, p)
        ftxt(base, 172, y + 26, t1, font_semi(21), NAVY, p)
        ftxt(base, 172, y + 58, t2, font("BeVietnamPro-Regular.ttf", 18), MUT, p)
        cq = seg(t, tp + 0.1, tp + 0.4)
        paste_im(base, sp_icon("circle-x" if i == 0 else "circle-check", col, 26), 770, y + 33, cq)

    # cán cân
    scx, scy = 1090, 430
    tilt = (1 - seg(t, c2 + 0.2, c2 + 1.2)) * 10
    ang = math.radians(tilt)
    lx, ly = scx - 190 * math.cos(ang), scy - 190 * math.sin(ang)
    rx, ry = scx + 190 * math.cos(ang), scy + 190 * math.sin(ang)
    d.line([scx, scy, scx, scy + 150], fill=NAVY, width=8)
    d.ellipse([scx - 12, scy - 12, scx + 12, scy + 12], fill=AMBER)
    d.line([lx, ly, rx, ry], fill=NAVY, width=7)
    for (x, y, lab, col) in ((lx, ly, "Chất lượng", BLUE), (rx, ry, "Dung lượng", TEAL)):
        d.line([x, y, x, y + 62], fill=(140, 156, 180, 255), width=3)
        d.arc([x - 56, y + 50, x + 56, y + 118], 0, 180, fill=col, width=5)
        ftxt(base, x, y + 132, lab, font_semi(18), col, 1, "mm")
    ftxt(base, scx, scy + 168, "cân bằng", font_semi(20), AMBER_D, seg(t, c2 + 1.0, c2 + 1.4), "mm")

    # ảnh hướng dẫn
    shot(base, IMG["screenshot_guide"], 900, 620, 540, 295, seg(t, a0 + 0.5, a0 + 1.1), t,
         0.86, 0.86, 0.0, 0.0, None, BLUE, 14)

    sheen(base, lin(t, 1.4, 4.4), 16)
    _an(base, tl, "S11", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S11", t))
    return base


def events_S11(tl):
    a0 = tl["S11"]["starts"][0]
    c2 = fr(tl, "S11", 1, 0.03)[0]
    return ([(a0 + 0.1, "whoosh", None, 0.55)] +
            [(a0 + 0.1 + i * 0.2, "tick", None, 0.4) for i in range(2)] +
            [(c2 + 0.05 + i * 0.2, "tick", None, 0.4) for i in range(3)] +
            [(c2 + 1.1, "chime", None, 0.45)])


# ================================================================ S12 — TỔNG KẾT
def draw_S12(t, tl):
    base, d = _base()
    s = tl["S12"]
    d.ellipse([-260, 560, 560, 1340], fill=(240, 244, 250, 255))
    d.ellipse([1400, -280, 2220, 500], fill=(253, 246, 227, 255))
    headbar(base, seg(t, 0.2, 1.0), "TỔNG KẾT")
    _title(base, tl, "S12", t, "Nhớ 4 điều này là đủ", None)

    a0 = s["starts"][0]
    cards = [("01", "Nén ảnh = nhẹ + nhanh", "giảm dung lượng, tăng tốc tải", "gauge", AMBER),
             ("02", "Lossy · Lossless", "JPEG cho ảnh chụp · PNG cho logo", "layers", BLUE),
             ("03", "WebP · AVIF", "hiện đại — nhớ kiểm tra trình duyệt", "rocket", TEAL),
             ("04", "Sharp + lazy + CDN", "tự động hoá, nhẹ như lông hồng", "code-xml", PURPLE)]
    for i, (num, t1, t2, ic, col) in enumerate(cards):
        p = seg(t, a0 + 0.08 + i * 0.14, a0 + 0.45 + i * 0.14)
        if p <= 0:
            continue
        x = 96 + i * 398
        rrect_a(base, [x, 188, x + 372, 366], 18, WHITE, (220, 228, 240, 255), 2, p)
        ftxt(base, x + 24, 220, num, font("PlusJakartaSans-var.ttf", 24, 800), col, p)
        paste_im(base, sp_icon(ic, col, 30), x + 314, 206, p)
        ftxt(base, x + 24, 276, t1, font_semi(22), NAVY, p)
        for j, ln in enumerate(wrap(t2, font("BeVietnamPro-Regular.ttf", 17), 320)[:2]):
            ftxt(base, x + 24, 314 + j * 24, ln, font("BeVietnamPro-Regular.ttf", 17), MUT, p)
        if i == 0:
            draw_marker(d, x + 20, 252, x + 112, 252, seg(t, a0 + 0.3, a0 + 0.65), AMBER, 5, 9)

    # dải before/after
    b0 = fr(tl, "S12", 1, 0.03)[0]
    shot(base, IMG["imgix_score"], 96, 410, 600, 311, seg(t, b0, b0 + 0.7), t,
         0.86, 0.88, 0.0, 0.0, None, TEAL, 14)
    ftxt(base, 96, 748, "Cùng một bức ảnh — nhẹ hơn 96%.", font("BeVietnamPro-Medium.ttf", 19),
         MUT, seg(t, b0 + 0.5, b0 + 0.9))

    # khối kết
    c2 = fr(tl, "S12", 2, 0.03)[0]
    p = seg(t, c2, c2 + 0.5)
    d.rectangle([760, 420, 760 + int(560 * p), 426], fill=AMBER)
    paste_im(base, sp_icon("shield-check", BLUE, 46), 760, 448, p)
    ftxt(base, 822, 458, "AN TECH ACADEMY", font("BeVietnamPro-Bold.ttf", 30), NAVY, p)
    ftxt(base, 822, 496, "Hiểu công nghệ, làm chủ tương lai!", font("BeVietnamPro-Regular.ttf", 20),
         MUT, p)
    lines = wrap("Cân bằng dung lượng · chất lượng · trải nghiệm.", font("BeVietnamPro-Bold.ttf", 38), 620)
    for j, ln in enumerate(lines[:2]):
        ftxt(base, 760, 566 + j * 46, ln, font("BeVietnamPro-Bold.ttf", 38), NAVY,
             seg(t, c2 + 0.25 + j * 0.12, c2 + 0.6 + j * 0.12))
    draw_marker(d, 764, 650, 1100, 650, seg(t, c2 + 0.6, c2 + 1.1), AMBER, 6, 5)
    paste_im(base, pill("Bài tiếp theo: CDN & caching ảnh", MUT, WHITE, 19, 42, "cloud"),
             760, 680, seg(t, c2 + 0.75, c2 + 1.1))

    sheen(base, lin(t, 0.8, 3.8), 18)
    _an(base, tl, "S12", t, "wave", look=-1)
    subtitle_band(d, subs_for(tl, "S12", t))
    return base


def events_S12(tl):
    a0 = tl["S12"]["starts"][0]
    b0 = fr(tl, "S12", 1, 0.03)[0]
    c2 = fr(tl, "S12", 2, 0.03)[0]
    return ([(a0, "whoosh", None, 0.7)] +
            [(a0 + 0.08 + i * 0.14, "pop", None, 0.55) for i in range(4)] +
            [(b0, "tick", None, 0.4), (c2, "chime", None, 0.75),
             (c2 + 0.6, "success", None, 0.65)])


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10, "S11": draw_S11, "S12": draw_S12}

EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03, "S04": events_S04,
          "S05": events_S05, "S06": events_S06, "S07": events_S07, "S08": events_S08,
          "S09": events_S09, "S10": events_S10, "S11": events_S11, "S12": events_S12}
