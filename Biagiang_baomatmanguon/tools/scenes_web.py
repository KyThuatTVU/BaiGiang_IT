# -*- coding: utf-8 -*-
"""12 cảnh cho bài giảng Web Shield (~5 phút). Bố cục khác nhau từng cảnh,
dùng 8 ảnh trong Noidung.docx đúng ngữ cảnh, nhân vật An xuất hiện xuyên suốt."""
import math, re
from PIL import Image, ImageDraw, ImageFilter
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB,
                  font, ease, seg, lin, tw, wrap, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, subtitle_band, subs_for)
import character

ROOT = "D:/Edit/Biagiang_baomatmanguon"
IMG = {i: f"{ROOT}/image{i}.jpeg" for i in range(1, 9)}

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"]
XFADE = 0.3

ANX = {"S01": (120, 920, 0.72), "S02": (1745, 920, 0.42), "S03": (1745, 920, 0.42),
       "S04": (140, 920, 0.46), "S05": (60, 920, 0.48), "S06": (1730, 920, 0.42),
       "S07": (1730, 920, 0.42), "S08": (70, 920, 0.46), "S09": (1730, 920, 0.40),
       "S10": (60, 920, 0.42), "S11": (1740, 920, 0.40), "S12": (1480, 920, 0.66)}

PURPLE = (109, 91, 208, 255)
PURPLE_L = (167, 155, 240, 255)
MINT = (232, 248, 244, 255)
RED_L = (255, 236, 236, 255)
BLUE_L = (96, 145, 255, 255)
TEAL_L = (72, 214, 190, 255)
AMBER_L = (255, 196, 110, 255)


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
    base.paste(im, (int(x), int(y)), im)


# ---------------------------------------------------------------- photos
_photo_cache = {}


def photo(path, w, h, radius=16):
    key = (path, w, h, radius)
    if key in _photo_cache:
        return _photo_cache[key]
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((x0, y0, x0 + w, y0 + h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=255)
    out = Image.new("RGBA", (w + 6, h + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([3, 6, w + 3, h + 8], radius + 2, fill=(15, 23, 42, 26))
    out.paste(im, (3, 3), mask)
    d.rounded_rectangle([3, 3, w + 2, h + 2], radius + 1, outline=(210, 218, 230, 255), width=2)
    _photo_cache[key] = out
    return out


def shot(base, path, x, y, w, h, p=1.0, caption=None, cap_color=BLUE, radius=16):
    if p <= 0:
        return
    paste_im(base, photo(path, w, h, radius), x, y, p)
    if caption:
        paste_im(base, sp_chip(caption, cap_color, WHITE, 19, None, h=36),
                 x + 14, y + h - 46, seg(p * 1.3, 0.35, 0.8))


# ---------------------------------------------------------------- chrome
def headbar(base, p, label):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, int(W * p), 5], fill=AMBER)
    w_ = int(tw(label, F_LBL))
    im = Image.new("RGBA", (w_ + 56, 40), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([0, 0, w_ + 55, 39], 19, fill=(255, 255, 255, 220),
                         outline=(214, 222, 234, 255), width=2)
    dd.ellipse([16, 15, 25, 24], fill=BLUE)
    draw_rich(dd, (38, 20), label, F_LBL, MUT, "lm")
    paste_im(base, im, W - w_ - 140, 28, p)


def browser(base, x, y, w, h, url):
    """khung trình duyệt rỗng (chỉ thanh trên), trả về y nội dung"""
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x, y, x + w, y + h], 18, fill=WHITE, outline=BORDER, width=2)
    d.rounded_rectangle([x, y, x + w, y + 54], 18, fill=(238, 242, 248, 255))
    d.rectangle([x, y + 40, x + w, y + 54], fill=(238, 242, 248, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([x + 22 + i * 24, y + 20, x + 34 + i * 24, y + 32], fill=c)
    d.rounded_rectangle([x + 108, y + 12, x + w - 22, y + 42], 15, fill=WHITE, outline=BORDER, width=2)
    draw_rich(d, (x + 126, y + 27), url, font("JetBrainsMono-var.ttf", 20), MUT, "lm")
    return y + 54


# ---------------------------------------------------------------- code
def _tok_apache(line):
    if line.strip().startswith("#"):
        return [(line, (120, 134, 156, 255))]
    out = []
    m = re.match(r"(\s*)(</?[A-Za-z]+|\S+)(.*)$", line)
    if not m:
        return [(line, (226, 232, 240, 255))]
    if m.group(1):
        out.append((m.group(1), (226, 232, 240, 255)))
    head = m.group(2)
    col = BLUE_L if head.startswith("<") else (PURPLE_L if head in
          ("Require", "Options", "RewriteEngine", "RewriteRule", "RewriteCond",
           "ErrorDocument", "DirectoryIndex") else (226, 232, 240, 255))
    out.append((head, col))
    rest = m.group(3)
    for part in re.split(r'("(?:[^"]*)")', rest):
        if not part:
            continue
        if part.startswith('"'):
            out.append((part, AMBER_L))
        elif re.search(r"\[[A-Z,]*\]", part):
            for q in re.split(r"(\[[A-Z,]+\])", part):
                if q:
                    out.append((q, TEAL_L if q.startswith("[") else (226, 232, 240, 255)))
        elif part.strip() in ("all", "denied", "-Indexes", "On"):
            out.append((part, (255, 138, 138, 255)))
        else:
            out.append((part, (226, 232, 240, 255)))
    return out


def _tok_php(line):
    if line.strip().startswith("//"):
        return [(line, (156, 163, 175, 255))]
    out = []
    for part in re.split(r'(\$[A-Za-z_]+|"[^"]*"|\'[^\']*\')', line):
        if not part:
            continue
        if part.startswith("$"):
            out.append((part, (96, 145, 255, 255)))
        elif part.startswith('"') or part.startswith("'"):
            out.append((part, (16, 150, 120, 255)))
        else:
            out.append((part, (40, 52, 76, 255)))
    return out


def code_panel(base, x, y, w, lines, typed=1.0, dark=True, title=".htaccess",
               hl=None, mode="apache", size=24, alpha=1.0):
    if typed <= 0:
        return 0
    lh = int(size * 1.55)
    pad = 20
    h = 50 + lh * len(lines) + 14
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bgc = (13, 22, 40, 255) if dark else (255, 255, 255, 255)
    d.rounded_rectangle([2, 6, w - 3, h - 2], 16, fill=(15, 23, 42, 30))
    d.rounded_rectangle([0, 0, w - 5, h - 8], 16, fill=bgc,
                        outline=(255, 255, 255, 34) if dark else (203, 214, 230, 255), width=2)
    d.rounded_rectangle([0, 0, w - 5, 46], 16, fill=(26, 38, 62, 255) if dark else (231, 238, 248, 255))
    d.rectangle([0, 30, w - 5, 46], fill=(26, 38, 62, 255) if dark else (231, 238, 248, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([18 + i * 21, 17, 29 + i * 21, 28], fill=c)
    draw_rich(d, (w - 22, 23), title, font("JetBrainsMono-var.ttf", 18),
              (150, 166, 192, 255) if dark else MUT, "rm")
    d.line([0, 46, w - 5, 46], fill=(255, 255, 255, 26) if dark else BORDER, width=2)
    nf = font("JetBrainsMono-var.ttf", size - 4)
    cf = font("JetBrainsMono-var.ttf", size)
    total = sum(len(l) for l in lines)
    budget = int(total * min(1.0, typed))
    yy = 58
    for i, line in enumerate(lines):
        if hl == i:
            d.rounded_rectangle([8, yy - lh // 2, w - 16, yy + lh // 2], 6,
                                fill=(255, 196, 110, 30) if dark else (255, 244, 224, 255))
        d.text((20, yy), str(i + 1), font=nf,
               fill=(88, 104, 128, 255) if dark else (176, 186, 200, 255), anchor="lm")
        xx = 62
        reveal = max(0, min(len(line), budget))
        for tx, col in (_tok_apache(line) if mode == "apache" else _tok_php(line)):
            if reveal <= 0:
                break
            part = tx[:reveal]
            d.text((xx, yy), part, font=cf, fill=col, anchor="lm")
            xx += d.textlength(part, font=cf)
            reveal -= len(tx)
        if typed < 1 and 0 <= budget < len(line) and int(budget * 3) % 2 == 0:
            d.rectangle([xx + 2, yy - 13, xx + 5, yy + 13], fill=AMBER)
        budget -= len(line)
        yy += lh
    im.putalpha(im.getchannel("A").point(lambda a: int(a * alpha)))
    base.paste(im, (int(x), int(y)), im)
    return h


# ---------------------------------------------------------------- effects
def sheen(base, q, alpha=22):
    if q <= 0 or q >= 1:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x = -420 + q * (W + 900)
    d.polygon([(x, 0), (x + 260, 0), (x - 160, H), (x - 420, H)],
              fill=(255, 255, 255, alpha))
    base.alpha_composite(ov)


def path_pos(pts, q):
    q = max(0.0, min(1.0, q))
    L = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(L)
    dd = q * tot
    for i, l in enumerate(L):
        if dd <= l or i == len(L) - 1:
            r = dd / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
        dd -= l
    return pts[-1]


def node(base, x, y, w, h, icon, label, sub=None, color=BLUE, fill=WHITE, p=1.0):
    if p <= 0:
        return
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 5, w, h + 3], 16, fill=(15, 23, 42, 20))
    d.rounded_rectangle([0, 0, w, h], 16, fill=fill, outline=color, width=2)
    ic = sp_icon(icon, color, 46)
    im.paste(ic, (22, (h - 46) // 2), ic)
    draw_rich(d, (82, h / 2 - (12 if sub else 0)), label, font_semi(27), INK, "lm")
    if sub:
        draw_rich(d, (82, h / 2 + 24), sub, F_SM, MUT, "lm")
    im.putalpha(im.getchannel("A").point(lambda a: int(a * p)))
    base.paste(im, (int(x), int(y)), im)


# ================================================================ S01
def draw_S01(t, tl):
    base, d = _base()
    s = tl["S01"]
    # nền trang trí
    d.ellipse([-260, 560, 520, 1340], fill=(240, 244, 250, 255))
    d.ellipse([1560, -280, 2300, 460], fill=(240, 244, 250, 255))
    for gx in range(100, 1840, 48):
        for gy in range(120, 940, 48):
            d.point((gx, gy), fill=(226, 232, 242, 255))
    headbar(base, seg(t, 0.2, 1.4), "BÀI 01 · WEB SHIELD")

    paste_im(base, sp_chip("WEB SHIELD · BẢO MẬT ỨNG DỤNG WEB", BLUE, ICE, 20, "shield", 42),
             110, 138, seg(t, 0.15, 0.8))
    lines = [("BẢO VỆ", NAVY), ("MÃ NGUỒN", NAVY), ("& KIỂM SOÁT TRUY CẬP", NAVY)]
    y = 208
    starts = [0.05, 0.5, 0.95]
    for i, (ln, col) in enumerate(lines):
        f = font("BeVietnamPro-Bold.ttf", 76 if i < 2 else 60)
        im = Image.new("RGBA", (int(tw(ln, f)) + 8, 92), (0, 0, 0, 0))
        draw_rich(ImageDraw.Draw(im), (0, 46), ln, f, col, "lm")
        paste_im(base, im, 110, y, seg(t, 0.15 + starts[i] * 0.55, 0.7 + starts[i] * 0.55))
        y += 88 if i < 2 else 0
    y += 78
    draw_marker(d, 112, 470, 112 + 560, 470, seg(t, 2.2, 3.0), AMBER, 8, 4)
    paste_im(base, sp_chip("Lộ mã nguồn · Lộ cấu trúc · Vượt quyền truy cập",
                           RED, RED_L, 22, "alert-triangle", 48),
             112, 500, seg(t, 3.0, 3.6))
    chips = [("Apache", "server", BLUE), (".htaccess", "file-text", TEAL),
             ("Front Controller", "route", PURPLE)]
    x = 330
    for i, (lb, ic, col) in enumerate(chips):
        c = sp_chip(lb, col, WHITE, 24, ic, 56)
        paste_im(base, c, x, 590, seg(t, 3.6 + i * 0.45, 4.1 + i * 0.45))
        x += c.width + 18
    paste_im(base, sp_chip("5 phút · 3 vũ khí · 1 kiến trúc an toàn", MUT, WHITE, 21, None, 44),
             330, 690, seg(t, 5.2, 5.9))
    # ảnh bìa
    ph = photo(IMG[1], 700, 470, 20)
    paste_im(base, ph, 1050, 230, seg(t, 0.7, 1.6))
    sheen(base, lin(t, 1.2, 2.2), 30)
    draw_marker_circle(d, 1348, 500, 170, 195, seg(t, 2.6, 3.6), AMBER, 5, 3)
    paste_im(base, sp_chip(".htaccess", AMBER_D, CREAM, 22, "file-text", 48),
             1560, 760, seg(t, 3.2, 3.8))
    _an(base, tl, "S01", t, "wave" if t < s["starts"][1] else "present", look=1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    return [(0.1, "whoosh", None, 0.8), (0.6, "chime", None, 0.6),
            (2.2, "marker", 0.9, 0.8), (3.0, "pop", None, 0.8),
            (3.6, "pop", None, 0.8), (4.05, "pop", None, 0.8), (4.5, "pop", None, 0.8),
            (5.2, "tick", None, 0.6)]


# ================================================================ S02
def draw_S02(t, tl):
    base, d = _base()
    headbar(base, 1, "01 · NHÌN TỪ TRÌNH DUYỆT")
    _title(base, tl, "S02", t, "DevTools nhìn thấy gì?", "Mọi thứ gửi xuống trình duyệt đều kiểm tra được")
    y0 = browser(base, 80, 218, 1120, 682, "https://example.com/products")
    p1 = seg(t, 0.8, 1.6)
    ph = photo(IMG[5], 1104, 620, 12)
    paste_im(base, ph, 88, y0 + 6, p1)
    bx, by, bw, bh = 92, y0 + 8, 1096, 616
    # khoanh tab Network
    a = fr(tl, "S02", 0, 0.15)[0]
    draw_marker_circle(d, bx + 0.27 * bw, by + 0.40 * bh, 76, 26, seg(t, a, a + 0.8), AMBER, 4, 2)
    paste_im(base, sp_chip("Network", AMBER_D, CREAM, 20, None, 38),
             bx + 0.27 * bw - 62, by + 0.40 * bh - 78, seg(t, a + 0.6, a + 1.0))
    # dải quét
    s2 = fr(tl, "S02", 1, 0.0)[0]
    q = lin(t, s2, s2 + 3.4)
    if 0 < q < 1:
        yq = by + 0.46 * bh + q * 0.5 * bh
        d.rounded_rectangle([bx + 8, yq, bx + bw - 8, yq + 44], 6,
                            outline=(47, 99, 232, 140), width=3)
        d.rectangle([bx + 8, yq, bx + bw - 8, yq + 44], fill=(47, 99, 232, 18))
    # thẻ nguyên tắc
    cx, cy = 1240, 250
    ca = seg(t, 1.6, 2.3)
    paste_im(base, card(590, 300), cx, cy, ca)
    paste_im(base, sp_icon("eye", RED, 54), cx + 30, cy + 28, seg(t, 1.8, 2.4))
    if ca > 0.3:
        draw_rich(d, (cx + 100, cy + 56), "Nguyên tắc vàng", F_H3, NAVY, "lm")
        for i, ln in enumerate(["Thứ gì đã gửi xuống", "trình duyệt — người dùng", "đều có thể xem."]):
            draw_rich(d, (cx + 32, cy + 120 + i * 46), ln, F_BODY_M, INK, "lm")
    draw_marker(d, cx + 32, cy + 258, cx + 300, cy + 258, seg(t, 3.0, 3.7), AMBER, 6, 5)
    # F12 keycap
    kp = seg(t, 2.4, 2.9)
    if kp > 0:
        kb = Image.new("RGBA", (150, 96), (0, 0, 0, 0))
        kd = ImageDraw.Draw(kb)
        kd.rounded_rectangle([0, 8, 146, 96], 14, fill=(210, 218, 230, 255))
        kd.rounded_rectangle([0, 0, 146, 86], 14, fill=WHITE, outline=BORDER, width=2)
        draw_rich(kd, (73, 44), "F12", font("PlusJakartaSans-var.ttf", 40, 700), NAVY, "mm")
        paste_im(base, kb, 1250, 600, kp)
        draw_rich(d, (1430, 648), "mở DevTools", F_SM, MUT, "lm")
    # chip tài nguyên bay lên
    tags = [("HTML", BLUE), ("CSS", TEAL), ("JS", AMBER_D), ("API", PURPLE)]
    for i, (lb, col) in enumerate(tags):
        b = fr(tl, "S02", 1, 0.55 + i * 0.1)[0]
        c = sp_chip(lb, col, WHITE, 21, None, 42)
        rise = 1 - seg(t, b, b + 0.6)
        paste_im(base, c, 1258 + i * 118, 736 + rise * 110, seg(t, b, b + 0.3))
    _an(base, tl, "S02", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    a = fr(tl, "S02", 0, 0.15)[0]
    b = [fr(tl, "S02", 1, 0.55 + i * 0.1)[0] for i in range(4)]
    return [(0.2, "whoosh", None, 0.8), (a, "click", None, 0.9),
            (1.9, "pop", None, 0.7), (3.0, "marker", 0.7, 0.8)] + \
        [(x, "pop", None, 0.6) for x in b]


# ================================================================ S03
def draw_S03(t, tl):
    base, d = _base()
    headbar(base, 1, "02 · RỦI RO LỘ MÃ NGUỒN")
    _title(base, tl, "S03", t, "Khi thư mục nội bộ bị phơi ra", "URL không phải cửa công khai")
    # thanh URL gõ dần
    uy = 212
    paste_im(base, card(980, 62), 100, uy, seg(t, 0.1, 0.5))
    draw_rich(d, (124, uy + 31), "https://example.com/", font("JetBrainsMono-var.ttf", 22), (120, 134, 156, 255), "lm")
    typed = "backend/config/"
    n = int(len(typed) * lin(t, 0.7, 2.4))
    draw_rich(d, (124 + tw("https://example.com/", font("JetBrainsMono-var.ttf", 22)), uy + 31),
              typed[:n], font("JetBrainsMono-var.ttf", 22), RED, "lm")
    if 0 < n < len(typed) and int(t * 3) % 2 == 0:
        xx = 124 + tw("https://example.com/" + typed[:n], font("JetBrainsMono-var.ttf", 22))
        d.rectangle([xx + 2, uy + 18, xx + 4, uy + 44], fill=RED)
    # ảnh cây thư mục
    shot(base, IMG[6], 100, 300, 620, 402, seg(t, 1.2, 1.9), "Cấu trúc thư mục thực tế", MUT)
    # khoanh điểm nóng
    b = fr(tl, "S03", 1, 0.1)[0]
    draw_marker_circle(d, 100 + 0.53 * 620, 300 + 0.62 * 402, 150, 34, seg(t, b, b + 0.7), RED, 4, 2)
    draw_marker(d, 100 + 0.25 * 620, 300 + 0.50 * 402, 100 + 0.52 * 620, 300 + 0.62 * 402,
                seg(t, b + 0.4, b + 1.1), RED, 4, 3)
    # mock Index of
    c = fr(tl, "S03", 1, 0.55)[0]
    ix, iy = 100, 740
    cp = seg(t, c, c + 0.5)
    paste_im(base, card(700, 160), ix, iy, cp)
    if cp > 0.3:
        draw_rich(d, (ix + 24, iy + 30), "Index of /backend/config/", font("JetBrainsMono-var.ttf", 22), NAVY, "lm")
        d.line([ix + 20, iy + 56, ix + 680, iy + 56], fill=BORDER, width=2)
        for i, nm in enumerate(["database.php  4.1K", "../", ".env  ▸ 1.2K"]):
            draw_rich(d, (ix + 24, iy + 88 + i * 26), nm, font("JetBrainsMono-var.ttf", 20),
                      RED if "env" in nm else (90, 104, 124, 255), "lm")
    # danh sách rủi ro
    risks = [("Lộ cấu trúc mã nguồn", "layers", RED),
             ("Lộ thông tin cấu hình", "settings", AMBER_D),
             ("Lộ dữ liệu / bản sao lưu", "database", RED),
             ("Bàn đạp tấn công tiếp", "bug", PURPLE)]
    for i, (lb, ic, col) in enumerate(risks):
        bb = fr(tl, "S03", 2, 0.05 + i * 0.2)[0]
        yy = 300 + i * 118
        paste_im(base, card(660, 96), 1000, yy, seg(t, bb, bb + 0.45))
        paste_im(base, sp_icon(ic, col, 42), 1026, yy + 27, seg(t, bb + 0.1, bb + 0.45))
        if seg(t, bb, bb + 0.45) > 0.3:
            draw_rich(d, (1088, yy + 48), lb, F_BODY_M, INK, "lm")
        paste_im(base, sp_icon("x", RED, 22), 1590, yy + 37, seg(t, bb + 0.35, bb + 0.6))
    # note
    npos = fr(tl, "S03", 2, 0.75)[0]
    paste_im(base, sp_chip("Chưa chắc khai thác được ngay — nhưng phải loại bỏ",
                           AMBER_D, CREAM, 20, "alert-triangle", 44),
             1000, 810, seg(t, npos, npos + 0.5))
    _an(base, tl, "S03", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    b = fr(tl, "S03", 1, 0.1)[0]
    c = fr(tl, "S03", 1, 0.55)[0]
    r = [fr(tl, "S03", 2, 0.05 + i * 0.2)[0] for i in range(4)]
    return [(0.2, "whoosh", None, 0.8), (0.7, "click", None, 0.6),
            (b, "marker", 0.8, 0.8), (c, "thud", None, 0.6)] + \
        [(x, "deny", None, 0.45) for x in r]


# ================================================================ S04
def draw_S04(t, tl):
    base, d = _base()
    headbar(base, 1, "03 · APACHE & .HTACCESS")
    _title(base, tl, "S04", t, "Apache và tệp .htaccess", "Bộ luật đặt ngay tại thư mục")
    # flow
    a = fr(tl, "S04", 0, 0.15)[0]
    node(base, 96, 250, 300, 150, "monitor", "Trình duyệt", "gửi request", BLUE, WHITE, seg(t, a, a + 0.4))
    node(base, 500, 230, 330, 190, "server", "Apache", "nhận & xử lý", NAVY, ICE, seg(t, a + 0.3, a + 0.7))
    node(base, 920, 270, 210, 110, "braces", "PHP", None, PURPLE, WHITE, seg(t, a + 0.6, a + 0.95))
    pts = [(400, 325), (496, 325)]
    draw_conn(d, *pts[0], *pts[1], seg(t, a + 0.5, a + 0.8), BLUE, width=4)
    pts2 = [(836, 325), (914, 325)]
    draw_conn(d, *pts2[0], *pts2[1], seg(t, a + 0.8, a + 1.1), PURPLE, width=4)
    # gói dữ liệu chạy
    if t > a + 0.5:
        q = (t - a) / 3.2 % 1.0
        px, py = path_pos([(100, 325), (500, 325), (920, 325)], q)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=AMBER)
    if seg(t, a, a + 0.7) > 0.3:
        draw_rich(d, (96, 430), "Apache phục vụ tệp tĩnh, gọi PHP khi cần", F_SM, MUT, "lm")
    # ảnh thực tế trong VS Code
    shot(base, IMG[2], 400, 578, 542, 351, seg(t, a + 1.0, a + 1.5), None)
    paste_im(base, sp_chip("VS Code thực tế", MUT, WHITE, 18, None, 34),
             950, 578, seg(t, a + 1.3, a + 1.7))
    # code
    cp = fr(tl, "S04", 1, 0.05)[0]
    code_panel(base, 1130, 190, 680,
               ["# .htaccess — luật của thư mục",
                "Options -Indexes",
                "",
                "<FilesMatch \"(?i)\\.(env|sql|log|bak)$\">",
                "    Require all denied",
                "</FilesMatch>"],
               typed=lin(t, cp + 0.3, cp + 2.2), title=".htaccess", hl=1,
               size=23, alpha=seg(t, cp, cp + 0.3))
    # điều kiện
    qs = fr(tl, "S04", 1, 0.55)[0]
    paste_im(base, sp_chip("AllowOverride All", BLUE, WHITE, 20, "settings", 44),
             1140, 560, seg(t, qs, qs + 0.4))
    paste_im(base, sp_chip("mod_rewrite", PURPLE, WHITE, 20, "git-branch", 44),
             1140, 620, seg(t, qs + 0.25, qs + 0.65))
    paste_im(base, sp_chip("Thiếu 2 điều kiện = .htaccess chỉ là file văn bản",
                           AMBER_D, CREAM, 19, "alert-triangle", 40),
             1140, 690, seg(t, qs + 0.8, qs + 1.2))
    _an(base, tl, "S04", t, "point_right" if t > cp else "present", look=1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    a = fr(tl, "S04", 0, 0.15)[0]
    cp = fr(tl, "S04", 1, 0.05)[0]
    qs = fr(tl, "S04", 1, 0.55)[0]
    return [(0.2, "whoosh", None, 0.75), (a + 0.3, "pop", None, 0.7),
            (a + 0.6, "pop", None, 0.7), (cp + 0.4, "click", None, 0.5),
            (cp + 1.1, "click", None, 0.5), (qs, "pop", None, 0.8),
            (qs + 0.25, "pop", None, 0.7), (qs + 0.8, "marker", 0.6, 0.6)]


# ================================================================ S05
def draw_S05(t, tl):
    base, d = _base()
    headbar(base, 1, "04 · CHẶN DUYỆT THƯ MỤC")
    _title(base, tl, "S05", t, "Tắt danh sách & chặn thư mục", "Options -Indexes · Require all denied")
    # thẻ listing
    cx, cy, cw, chh = 252, 230, 628, 520
    paste_im(base, card(cw, chh), cx, cy, seg(t, 0.2, 0.6))
    draw_rich(d, (cx + 26, cy + 34), "Index of /frontend/assets/", font("JetBrainsMono-var.ttf", 24), NAVY, "lm")
    d.line([cx + 24, cy + 62, cx + cw - 24, cy + 62], fill=BORDER, width=2)
    rows = ["css/", "js/", "images/", "config.php", ".env"]
    a = fr(tl, "S05", 0, 0.2)[0]
    off = seg(t, a + 0.5, a + 1.2)
    for i, nm in enumerate(rows):
        yy = cy + 100 + i * 74
        rr = seg(t, a + i * 0.1, a + i * 0.1 + 0.3)
        draw_rich(d, (cx + 30, yy), nm, font("JetBrainsMono-var.ttf", 22),
                  MUT if off > 0.5 else (60, 76, 100, 255), "lm")
        d.line([cx + 24, yy + 36, cx + cw - 24, yy + 36], fill=(240, 243, 248, 255), width=2)
        if off > 0.3:
            draw_marker(d, cx + 24, yy, cx + cw - 24, yy, min(1, off), RED, 3, i + 1)
    # tem Options
    st = fr(tl, "S05", 0, 0.55)[0]
    paste_im(base, sp_chip("Options -Indexes", TEAL, MINT, 26, "shield-check", 60),
             cx + 30, cy + chh + 24, seg(t, st, st + 0.5))
    # ảnh 403
    b = fr(tl, "S05", 1, 0.35)[0]
    shot(base, IMG[7], 980, 250, 640, 400, seg(t, b, b + 0.6), None)
    draw_marker_circle(d, 980 + 320, 250 + 190, 250, 160, seg(t, b + 0.4, b + 1.1), RED, 5, 4)
    big = Image.new("RGBA", (300, 150), (0, 0, 0, 0))
    bd = ImageDraw.Draw(big)
    bd.rounded_rectangle([0, 0, 296, 146], 18, fill=(220, 38, 38, 235))
    draw_rich(bd, (148, 58), "403", font("PlusJakartaSans-var.ttf", 62, 800), WHITE, "mm")
    draw_rich(bd, (148, 112), "FORBIDDEN", font("PlusJakartaSans-var.ttf", 20, 700), (255, 220, 220, 255), "mm")
    paste_im(base, big, 1400, 700, seg(t, b + 0.9, b + 1.3))
    # hai chip kết luận
    c2 = fr(tl, "S05", 1, 0.8)[0]
    paste_im(base, sp_chip("Directory Listing: OFF", TEAL, MINT, 21, "circle-check", 46),
             980, 690, seg(t, c2, c2 + 0.4))
    paste_im(base, sp_chip("Require all denied → 403", RED, RED_L, 21, "lock", 46),
             980, 748, seg(t, c2 + 0.3, c2 + 0.7))
    _an(base, tl, "S05", t, "present", look=1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    a = fr(tl, "S05", 0, 0.55)[0]
    b = fr(tl, "S05", 1, 0.35)[0]
    return [(0.2, "whoosh", None, 0.75), (0.8, "pop", None, 0.7),
            (a, "marker", 0.7, 0.8), (b, "deny", None, 0.7),
            (b + 0.9, "thud", None, 0.7), (b + 1.4, "chime", None, 0.6)]


# ================================================================ S06
def draw_S06(t, tl):
    base, d = _base()
    headbar(base, 1, "05 · CHẶN TỆP NHẠY CẢM")
    _title(base, tl, "S06", t, "FilesMatch — chặn theo phần mở rộng", "Nhưng đừng chỉ tin vào phần mở rộng")
    a = fr(tl, "S06", 0, 0.1)[0]
    code_panel(base, 90, 230, 1040,
               ["<FilesMatch \"(?i)\\.(env|sql|log|bak|ini|sh)$\">",
                "    Require all denied",
                "</FilesMatch>"],
               typed=lin(t, a + 0.2, a + 1.8), title=".htaccess", hl=0,
               size=25, alpha=seg(t, a, a + 0.3))
    paste_im(base, sp_chip("(?i) = không phân biệt hoa thường", PURPLE, WHITE, 19, "search", 40),
             110, 470, seg(t, a + 1.2, a + 1.6))
    paste_im(base, sp_chip("Require all denied = từ chối mọi yêu cầu", RED, RED_L, 19, "lock", 40),
             110, 524, seg(t, a + 1.5, a + 1.9))
    # các tệp bay vào rồi bị gạch
    exts = [".env", ".sql", ".log", ".bak", ".ini", ".sh"]
    b = fr(tl, "S06", 0, 0.55)[0]
    for i, e in enumerate(exts):
        bb = b + i * 0.12
        x = 110 + i * 158
        y = 640 - 30 * math.sin(i)
        c = sp_chip(e, NAVY, WHITE, 24, "file-text", 52)
        paste_im(base, c, x, y, seg(t, bb, bb + 0.4))
        if t > bb + 0.5:
            draw_marker(d, x + 6, y + 26, x + c.width - 6, y + 26,
                        seg(t, bb + 0.5, bb + 0.8), RED, 4, i + 2)
            paste_im(base, sp_icon("x", RED, 20), x + c.width - 26, y + 4, seg(t, bb + 0.8, bb + 0.95))
    # thẻ ngoài DocumentRoot
    c2 = fr(tl, "S06", 1, 0.2)[0]
    cc = seg(t, c2, c2 + 0.5)
    paste_im(base, card(600, 280, fill=CREAM, outline=(255, 214, 150, 255)), 1200, 250, cc)
    paste_im(base, sp_icon("folder", AMBER_D, 56), 1228, 278, seg(t, c2 + 0.1, c2 + 0.5))
    if cc > 0.3:
        draw_rich(d, (1300, 306), "Bí mật nên nằm", F_H3, NAVY, "lm")
        draw_rich(d, (1300, 348), "ngoài DocumentRoot", F_H3, NAVY, "lm")
        draw_rich(d, (1228, 410), "Như nhật ký — đừng bỏ quên", F_SM, (120, 90, 50, 255), "lm")
        draw_rich(d, (1228, 450), "trên bàn cà phê.", F_SM, (120, 90, 50, 255), "lm")
    draw_marker(d, 1228, 492, 1700, 492, seg(t, c2 + 0.6, c2 + 1.1), AMBER_D, 5, 3)
    _an(base, tl, "S06", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    a = fr(tl, "S06", 0, 0.1)[0]
    b = fr(tl, "S06", 0, 0.55)[0]
    c2 = fr(tl, "S06", 1, 0.2)[0]
    return [(0.2, "whoosh", None, 0.7), (a + 0.4, "click", None, 0.5),
            (b, "pop", None, 0.6)] + [(b + i * 0.12 + 0.5, "deny", None, 0.32) for i in range(6)] + \
        [(c2, "chime", None, 0.6), (c2 + 0.6, "marker", 0.5, 0.6)]


# ================================================================ S07
def draw_S07(t, tl):
    base, d = _base()
    headbar(base, 1, "06 · URL REWRITE")
    _title(base, tl, "S07", t, "Giấu đường dẫn vật lý", "Rewrite nội bộ ≠ Redirect 301")
    # address bar biến đổi
    ay = 208
    paste_im(base, card(1680, 84), 100, ay, seg(t, 0.1, 0.5))
    fmono = font("JetBrainsMono-var.ttf", 24)
    long_url = "https://example.com/frontend/pages/about/index.html"
    a = fr(tl, "S07", 0, 0.05)[0]
    ph = lin(t, a, a + 1.4)
    if ph < 1:
        draw_rich(d, (130, ay + 42), long_url, fmono, (110, 124, 146, 255), "lm")
        if ph > 0.1:
            draw_marker(d, 130, ay + 44, 130 + tw(long_url, fmono), ay + 44, ph, RED, 4, 2)
    short = "https://example.com/about/"
    s = b7 = fr(tl, "S07", 0, 0.6)[0]
    q = seg(t, s, s + 0.7)
    if q > 0:
        draw_rich(d, (130, ay + 42), short, fmono, NAVY, "lm")
        paste_im(base, sp_icon("circle-check", TEAL, 30), 130 + tw(short, fmono) + 20, ay + 27, q)
    paste_im(base, sp_chip("/about/  →  frontend/pages/about/index.html", TEAL, MINT, 19, "route", 40),
             130, ay + 98, seg(t, s + 0.4, s + 0.9))
    # code thực tế image8, sau đó đổi sang flowchart image3
    c1 = fr(tl, "S07", 0, 0.35)[0]
    c2s = fr(tl, "S07", 1, 0.15)[0]
    if t < c2s + 0.4:
        shot(base, IMG[8], 260, 340, 700, 438, seg(t, c1, c1 + 0.6), "RewriteRule thực tế", PURPLE)
    else:
        shot(base, IMG[3], 330, 340, 560, 438, seg(t, c2s + 0.4, c2s + 0.9),
             "Luồng xử lý của Apache", MUT)
    # so sánh
    c2 = fr(tl, "S07", 1, 0.15)[0]
    p2 = seg(t, c2, c2 + 0.5)
    paste_im(base, card(860, 190), 1000, 330, p2)
    paste_im(base, sp_icon("server", TEAL, 44), 1026, 356, seg(t, c2 + 0.1, c2 + 0.5))
    if p2 > 0.3:
        draw_rich(d, (1088, 378), "Rewrite nội bộ", F_H3, NAVY, "lm")
        draw_rich(d, (1088, 422), "Máy chủ đổi cách phục vụ · URL giữ nguyên", F_SM, MUT, "lm")
        draw_rich(d, (1088, 460), "Trình duyệt không hay biết", F_SM_M, TEAL, "lm")
    c3 = fr(tl, "S07", 1, 0.6)[0]
    p3 = seg(t, c3, c3 + 0.5)
    paste_im(base, card(860, 190), 1000, 550, p3)
    paste_im(base, sp_icon("refresh-cw", AMBER_D, 44), 1026, 576, seg(t, c3 + 0.1, c3 + 0.5))
    if p3 > 0.3:
        draw_rich(d, (1088, 598), "Redirect 301", F_H3, NAVY, "lm")
        draw_rich(d, (1088, 642), "Máy chủ bảo trình duyệt đổi địa chỉ", F_SM, MUT, "lm")
        draw_rich(d, (1088, 680), "Thanh địa chỉ thay đổi", F_SM_M, AMBER_D, "lm")
    _an(base, tl, "S07", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    a = fr(tl, "S07", 0, 0.05)[0]
    s = fr(tl, "S07", 0, 0.6)[0]
    c2 = fr(tl, "S07", 1, 0.15)[0]
    c3 = fr(tl, "S07", 1, 0.6)[0]
    return [(0.2, "whoosh", None, 0.8), (a + 0.3, "click", None, 0.5),
            (s, "pop", None, 0.8), (s + 0.2, "chime", None, 0.7),
            (c2, "pop", None, 0.7), (c3, "pop", None, 0.7)]


# ================================================================ S08
def draw_S08(t, tl):
    base, d = _base()
    headbar(base, 1, "07 · FRONT CONTROLLER")
    _title(base, tl, "S08", t, "Một cửa duy nhất: index.php", "Tập trung kiểm soát, dễ thêm phân quyền")
    # các tệp rời rạc (mờ dần)
    files = ["login.php", "register.php", "products.php", "orders.php", "profile.php", "settings.php"]
    a = fr(tl, "S08", 0, 0.05)[0]
    collapse = seg(t, a + 0.6, a + 2.0)
    for i, nm in enumerate(files):
        x = 130 + (i % 3) * 230
        y = 236 + (i // 3) * 96
        c = sp_chip(nm, MUT, WHITE, 19, "file-text", 40)
        paste_im(base, c, x, y, (1 - collapse) * seg(t, a + i * 0.08, a + i * 0.08 + 0.3))
    # hub
    cx, cy = 760, 470
    b = fr(tl, "S08", 0, 0.75)[0]
    hubp = seg(t, b, b + 0.6)
    if hubp > 0:
        d.ellipse([cx - 96, cy - 96, cx + 96, cy + 96], fill=(47, 99, 232, 18))
        nm = sp_chip("index.php", BLUE, WHITE, 26, "route", 66)
        paste_im(base, nm, cx - nm.width / 2, cy - 33, hubp)
        routes = [("Trang chủ", "/"), ("Giới thiệu", "/about/"), ("Liên hệ", "/contact/"),
                  ("API", "/api/settings"), ("Admin", "/admin/")]
        for i, (lb, rt) in enumerate(routes):
            ang = -math.pi / 2 + (i - 2) * 0.52
            rx = cx + math.cos(ang) * 330
            ry = cy + math.sin(ang) * 260
            bb = b + 0.5 + i * 0.16
            draw_conn(d, cx, cy, rx, ry, seg(t, bb, bb + 0.35), TEAL if i != 4 else RED, width=3)
            cc = sp_chip(rt, TEAL if i != 4 else RED, WHITE, 18, None, 38)
            paste_im(base, cc, rx - cc.width / 2, ry - 19, seg(t, bb + 0.2, bb + 0.5))
    # ảnh sơ đồ tham chiếu
    c2 = fr(tl, "S08", 1, 0.1)[0]
    shot(base, IMG[4], 1330, 240, 500, 390, seg(t, c2, c2 + 0.6), "Sơ đồ Front Controller", PURPLE)
    draw_marker_circle(d, 1330 + 330, 240 + 120, 150, 78, seg(t, c2 + 0.5, c2 + 1.1), AMBER, 4, 3)
    # 3 nhãn nhiệm vụ
    tasks = [("Đọc URL", "search"), ("Kiểm quyền", "shield-check"), ("Gọi xử lý", "workflow")]
    for i, (lb, ic) in enumerate(tasks):
        bb = fr(tl, "S08", 1, 0.15 + i * 0.25)[0]
        paste_im(base, sp_chip(lb, BLUE if i < 2 else PURPLE, WHITE, 19, ic, 42),
                 1330, 690 + i * 52, seg(t, bb, bb + 0.4))
    _an(base, tl, "S08", t, "present", look=1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    a = fr(tl, "S08", 0, 0.05)[0]
    b = fr(tl, "S08", 0, 0.75)[0]
    c2 = fr(tl, "S08", 1, 0.1)[0]
    return [(0.2, "whoosh", None, 0.8)] + [(a + i * 0.08, "click", None, 0.4) for i in range(6)] + \
        [(b, "chime", None, 0.7)] + [(b + 0.5 + i * 0.16 + 0.2, "pop", None, 0.5) for i in range(5)] + \
        [(c2, "marker", 0.6, 0.6)]


# ================================================================ S09
def draw_S09(t, tl):
    base, d = _base()
    headbar(base, 1, "08 · WHITELIST ROUTING")
    _title(base, tl, "S09", t, "Chỉ mở đúng cửa đã khai báo", "Route lạ → 404, không phải lỗi buồn")
    a = fr(tl, "S09", 0, 0.05)[0]
    code_panel(base, 90, 220, 1040,
               ["<?php",
                "$routes = [",
                "  '/' => 'home',",
                "  '/about/' => 'about',",
                "  '/contact/' => 'contact',",
                "];",
                "$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);"],
               typed=lin(t, a + 0.2, a + 2.6), dark=False, title="index.php",
               hl=None, mode="php", size=22, alpha=seg(t, a, a + 0.3))
    # whitelist card
    b = fr(tl, "S09", 0, 0.55)[0]
    wc = seg(t, b, b + 0.5)
    paste_im(base, card(600, 330), 1200, 250, wc)
    if wc > 0.3:
        draw_rich(d, (1228, 284), "Danh sách được phép", F_H3, NAVY, "lm")
    rows = [("/", True), ("/about/", True), ("/contact/", True), ("/admin/", False)]
    for i, (rt, ok) in enumerate(rows):
        bb = b + 0.35 + i * 0.18
        yy = 342 + i * 54
        paste_im(base, sp_icon("circle-check" if ok else "circle-x", TEAL if ok else RED, 28),
                 1228, yy, seg(t, bb, bb + 0.3))
        if seg(t, bb, bb + 0.3) > 0.3:
            draw_rich(d, (1270, yy + 14), rt, font("JetBrainsMono-var.ttf", 22), INK, "lm")
        if not ok:
            draw_marker(d, 1262, yy + 16, 1400, yy + 16, seg(t, bb + 0.3, bb + 0.6), RED, 3, 2)
    # tem 404
    c2 = fr(tl, "S09", 0, 0.75)[0]
    st = Image.new("RGBA", (360, 190), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([4, 4, 356, 186], 18, fill=(220, 38, 38, 232))
    draw_rich(sd, (180, 68), "404", font("PlusJakartaSans-var.ttf", 78, 800), WHITE, "mm")
    draw_rich(sd, (180, 132), "NOT FOUND", font("PlusJakartaSans-var.ttf", 24, 700), (255, 220, 220, 255), "mm")
    st = st.rotate(-7, expand=True, resample=Image.BICUBIC)
    paste_im(base, st, 1320, 600, seg(t, c2, c2 + 0.35))
    paste_im(base, sp_chip("Không có cửa → không mở", TEAL, MINT, 20, "lock", 44),
             1200, 800, seg(t, c2 + 0.5, c2 + 0.9))
    paste_im(base, sp_chip("Router không thay thế cấu hình Apache", AMBER_D, CREAM, 19,
                           "alert-triangle", 42), 900, 858, seg(t, c2 + 0.8, c2 + 1.2))
    _an(base, tl, "S09", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    a = fr(tl, "S09", 0, 0.05)[0]
    b = fr(tl, "S09", 0, 0.55)[0]
    c2 = fr(tl, "S09", 0, 0.75)[0]
    return [(0.2, "whoosh", None, 0.75), (a + 0.5, "click", None, 0.45),
            (b + 0.5, "pop", None, 0.7), (c2, "thud", None, 0.75),
            (c2 + 0.6, "marker", 0.5, 0.6)]


# ================================================================ S10
def draw_S10(t, tl):
    base, d = _base()
    headbar(base, 1, "09 · KIẾN TRÚC AN TOÀN")
    _title(base, tl, "S10", t, "Tách public và private", "DocumentRoot trỏ thẳng vào thư mục public")
    # cây thư mục
    x0, y0 = 100, 200
    paste_im(base, card(760, 490), x0, y0, seg(t, 0.15, 0.55))
    a = fr(tl, "S10", 0, 0.1)[0]
    pub = [("frontend/", "assets, pages"), ("public/", "index.php, css, js")]
    priv = [("app/", "nghiệp vụ"), ("config/", ".env, DB"), ("routes/", "định tuyến"), ("storage/", "dữ liệu nội bộ")]
    d.rounded_rectangle([x0 + 24, y0 + 80, x0 + 736, y0 + 232], 14, fill=(236, 249, 244, 255),
                        outline=(150, 220, 200, 255), width=2)
    draw_rich(d, (x0 + 44, y0 + 108), "PUBLIC", font("PlusJakartaSans-var.ttf", 20, 700), TEAL, "lm")
    for i, (nm, sub) in enumerate(pub):
        bb = a + 0.3 + i * 0.3
        paste_im(base, sp_icon("folder", TEAL, 26), x0 + 44 + i * 340, y0 + 138, seg(t, bb, bb + 0.3))
        draw_rich(d, (x0 + 78 + i * 340, y0 + 140), nm, font_semi(22), INK, "lm")
        draw_rich(d, (x0 + 78 + i * 340, y0 + 172), sub, F_SM, MUT, "lm")
    d.rounded_rectangle([x0 + 24, y0 + 252, x0 + 736, y0 + 476], 14, fill=(255, 242, 242, 255),
                        outline=(240, 178, 178, 255), width=2)
    draw_rich(d, (x0 + 44, y0 + 280), "PRIVATE", font("PlusJakartaSans-var.ttf", 20, 700), RED, "lm")
    for i, (nm, sub) in enumerate(priv):
        bb = a + 0.8 + i * 0.22
        xx = x0 + 44 + (i % 2) * 340
        yy = y0 + 312 + (i // 2) * 82
        paste_im(base, sp_icon("folder", RED, 26), xx, yy, seg(t, bb, bb + 0.3))
        draw_rich(d, (xx + 34, yy + 2), nm, font_semi(22), INK, "lm")
        draw_rich(d, (xx + 34, yy + 34), sub, F_SM, MUT, "lm")
    # mũi tên DocumentRoot
    dr = fr(tl, "S10", 0, 0.65)[0]
    draw_conn(d, 860, 272, 984, 272, seg(t, dr, dr + 0.5), BLUE, width=5)
    paste_im(base, sp_chip("DocumentRoot", BLUE, ICE, 20, "target", 44), 990, 250, seg(t, dr + 0.3, dr + 0.7))
    # flow 5 bước
    steps = [("Trình duyệt", "monitor"), ("Apache", "server"), ("Kiểm luật", "shield"),
             ("Front Controller", "route"), ("Router → xử lý", "workflow")]
    b = fr(tl, "S10", 1, 0.1)[0]
    for i, (lb, ic) in enumerate(steps):
        bb = b + i * 0.22
        yy = 300 + i * 112
        paste_im(base, card(640, 84), 1000, yy, seg(t, bb, bb + 0.35))
        paste_im(base, sp_icon(ic, BLUE if i < 4 else PURPLE, 34), 1026, yy + 25, seg(t, bb + 0.1, bb + 0.4))
        if seg(t, bb, bb + 0.35) > 0.3:
            draw_rich(d, (1080, yy + 42), lb, F_BODY_M, INK, "lm")
        if i > 0:
            draw_conn(d, 1320, yy - 28, 1320, yy - 2, seg(t, bb - 0.12, bb), BLUE, width=3)
    paste_im(base, sp_chip("403", RED, RED_L, 20, "x", 40), 1680, 512, seg(t, b + 0.9, b + 1.2))
    paste_im(base, sp_chip("404", AMBER_D, CREAM, 20, "search", 40), 1680, 848, seg(t, b + 1.4, b + 1.7))
    _an(base, tl, "S10", t, "present", look=1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    a = fr(tl, "S10", 0, 0.1)[0]
    b = fr(tl, "S10", 1, 0.1)[0]
    return [(0.2, "whoosh", None, 0.75), (a + 0.3, "pop", None, 0.6),
            (a + 0.6, "pop", None, 0.6)] + [(b + i * 0.22, "pop", None, 0.55) for i in range(5)] + \
        [(b + 1.5, "chime", None, 0.6)]


# ================================================================ S11
def draw_S11(t, tl):
    base, d = _base()
    headbar(base, 1, "10 · TỔNG KẾT")
    _title(base, tl, "S11", t, "Tóm gọn trong ba ý", None)
    cards = [("01", "DevTools thấy mọi thứ", "gửi xuống trình duyệt", "eye", BLUE),
             ("02", ".htaccess chặn & đổi URL", "ngay tại máy chủ", "shield-check", TEAL),
             ("03", "Whitelist Routing", "chỉ mở đúng route", "route", PURPLE)]
    for i, (num, t1, t2, ic, col) in enumerate(cards):
        a = fr(tl, "S11", 0, 0.05 + i * 0.25)[0]
        x = 100 + i * 540
        ca = seg(t, a, a + 0.45)
        paste_im(base, card(500, 260), x, 196, ca)
        paste_im(base, sp_icon(ic, col, 46), x + 410, 212, seg(t, a + 0.2, a + 0.5))
        if ca > 0.3:
            draw_rich(d, (x + 30, 226), num, font("PlusJakartaSans-var.ttf", 30, 800), col, "lm")
            draw_rich(d, (x + 30, 292), t1, font_semi(24), INK, "lm")
            draw_rich(d, (x + 30, 332), t2, F_SM, MUT, "lm")
    # quiz
    b = fr(tl, "S11", 1, 0.05)[0]
    qb = seg(t, b, b + 0.4)
    paste_im(base, card(1500, 330), 100, 500, qb)
    if qb > 0.3:
        draw_rich(d, (130, 540), "Dòng nào tắt danh sách thư mục?", F_H3, NAVY, "lm")
    opts = [("A", "Require all denied"), ("B", "Options -Indexes"), ("C", "RewriteEngine On")]
    correct = fr(tl, "S11", 1, 0.62)[0]
    for i, (k, txt) in enumerate(opts):
        bb = b + 0.3 + i * 0.15
        x = 130 + i * 470
        ok = (k == "B") and t > correct
        fillc = MINT if ok else WHITE
        linec = TEAL if ok else BORDER
        paste_im(base, card(440, 96, fill=fillc, outline=linec), x, 600 + 0, seg(t, bb, bb + 0.35))
        if seg(t, bb, bb + 0.35) > 0.3:
            draw_rich(d, (x + 30, 648), k, font("PlusJakartaSans-var.ttf", 34, 800),
                      TEAL if ok else MUT, "lm")
            draw_rich(d, (x + 76, 648), txt, font("JetBrainsMono-var.ttf", 20), INK, "lm")
        if ok:
            paste_im(base, sp_icon("circle-check", TEAL, 34), x + 380, 630, seg(t, correct, correct + 0.3))
    paste_im(base, sp_chip("Đáp án: B", TEAL, MINT, 26, "circle-check", 56),
             130, 760, seg(t, correct + 0.2, correct + 0.6))
    _an(base, tl, "S11", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S11", t))
    return base


def events_S11(tl):
    a = [fr(tl, "S11", 0, 0.05 + i * 0.25)[0] for i in range(3)]
    b = fr(tl, "S11", 1, 0.05)[0]
    c = fr(tl, "S11", 1, 0.62)[0]
    return [(0.2, "whoosh", None, 0.75)] + [(x, "pop", None, 0.7) for x in a] + \
        [(b + 0.3 + i * 0.15, "click", None, 0.5) for i in range(3)] + \
        [(c, "success", None, 0.8)]


# ================================================================ S12
def draw_S12(t, tl):
    base, d = _base()
    headbar(base, 1, "KẾT THÚC")
    d.ellipse([-240, 520, 540, 1300], fill=(240, 244, 250, 255))
    d.ellipse([1500, -300, 2280, 480], fill=(240, 244, 250, 255))
    a = fr(tl, "S12", 0, 0.05)[0]
    paste_im(base, sp_icon("shield-check", BLUE, 84), 150, 200, seg(t, a, a + 0.4))
    f = font("BeVietnamPro-Bold.ttf", 64)
    if seg(t, a + 0.1, a + 0.6) > 0.3:
        draw_rich(d, (150, 352), "AN TECH ACADEMY", f, NAVY, "lm")
        draw_rich(d, (152, 410), "Học công nghệ cùng An", F_BODY, MUT, "lm")
    draw_marker(d, 152, 452, 700, 452, seg(t, a + 0.3, a + 0.9), AMBER, 7, 4)
    if seg(t, a + 0.5, a + 1.0) > 0.3:
        draw_rich(d, (150, 520), "Bảo mật không phải che giấu,", F_H2, INK, "lm")
    if seg(t, a + 0.65, a + 1.15) > 0.3:
        draw_rich(d, (150, 580), "mà là kiểm soát đúng chỗ.", F_H2, INK, "lm")
    chips = [("Dựng WebShield trên XAMPP", "terminal", BLUE),
             ("Gõ thử một URL lạ", "search", TEAL)]
    for i, (lb, ic, col) in enumerate(chips):
        paste_im(base, sp_chip(lb, col, WHITE, 22, ic, 52), 150, 660 + i * 62,
                 seg(t, a + 0.7 + i * 0.25, a + 1.1 + i * 0.25))
    paste_im(base, sp_chip("Bài tiếp theo: triển khai an toàn lên máy chủ thật",
                           MUT, WHITE, 20, "rocket", 46), 150, 820, seg(t, a + 1.4, a + 1.8))
    sheen(base, lin(t, 0.6, 2.0), 26)
    _an(base, tl, "S12", t, "wave", look=-1)
    subtitle_band(d, subs_for(tl, "S12", t))
    return base


def events_S12(tl):
    return [(0.2, "whoosh", None, 0.7), (0.5, "chime", None, 0.7),
            (1.2, "pop", None, 0.6), (1.45, "pop", None, 0.6),
            (2.0, "success", None, 0.7)]


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10, "S11": draw_S11, "S12": draw_S12}

EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03, "S04": events_S04,
          "S05": events_S05, "S06": events_S06, "S07": events_S07, "S08": events_S08,
          "S09": events_S09, "S10": events_S10, "S11": events_S11, "S12": events_S12}
