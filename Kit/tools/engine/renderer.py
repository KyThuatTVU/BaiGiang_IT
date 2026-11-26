# -*- coding: utf-8 -*-
"""Motion Graphics Renderer — 8 templates sáng tạo, đa theme, nhân vật An, 0% chồng chéo."""
import math
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

KIT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS_DIR = os.path.join(KIT_ROOT, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import character

W, H = 1920, 1080


# ─── EASING & HELPERS ────────────────────────────────────────────────────────
def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else (hi if x > hi else x)


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    t = clamp(t)
    return 1.0 - (1.0 - t) ** 3


def ease_in_out(t):
    t = clamp(t)
    return t * t * (3.0 - 2.0 * t)


def c_rgba(rgb, a=255):
    return (int(rgb[0]), int(rgb[1]), int(rgb[2]), int(clamp(a, 0, 255)))


# ─── FONT & ASSET CACHING ────────────────────────────────────────────────────
_FONTS = {}
_BG_CACHE = {}
_LOGO_SM = None
_CHAR_CACHE = {}
_IMG_SRC = {}

_RND = random.Random(2026)
_PARTICLES = [
    (_RND.uniform(0, W), _RND.uniform(90, H - 140),
     _RND.uniform(-0.35, 0.35), _RND.uniform(-0.28, 0.28),
     _RND.uniform(2.0, 4.2), _RND.uniform(0, 6.28))
    for _ in range(55)
]


def get_font(cfg, style, size):
    fname = cfg["fonts"][style]
    key = (fname, size)
    if key not in _FONTS:
        p = os.path.join(KIT_ROOT, "assets", "fonts", fname)
        _FONTS[key] = ImageFont.truetype(p, size)
    return _FONTS[key]


def get_small_logo(cfg):
    global _LOGO_SM
    if _LOGO_SM is None:
        lp = os.path.join(KIT_ROOT, cfg["brand"]["logo_path"])
        if os.path.exists(lp):
            _LOGO_SM = Image.open(lp).convert("RGBA").resize((50, 50), Image.LANCZOS)
        else:
            _LOGO_SM = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    return _LOGO_SM


def get_bg_gradient(theme):
    key = (tuple(theme["bg_top"]), tuple(theme["bg_bottom"]))
    if key not in _BG_CACHE:
        im = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(im)
        t0, t1 = theme["bg_top"], theme["bg_bottom"]
        for y in range(H):
            r = y / (H - 1)
            col = (
                int(lerp(t0[0], t1[0], r)),
                int(lerp(t0[1], t1[1], r)),
                int(lerp(t0[2], t1[2], r)),
                255,
            )
            d.line([(0, y), (W, y)], fill=col)
        # Subtle ambient radial glow (cached once!)
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        pcol = theme["primary"]
        scol = theme["accent"]
        for rad in range(520, 40, -40):
            a = int(14 * (1 - rad / 520) ** 1.5)
            gd.ellipse((320 - rad, 420 - rad, 320 + rad, 420 + rad), fill=c_rgba(pcol, a))
        for rad in range(460, 40, -40):
            a = int(12 * (1 - rad / 460) ** 1.5)
            gd.ellipse((1360 - rad, 660 - rad, 1360 + rad, 660 + rad), fill=c_rgba(scol, a))
        im.alpha_composite(glow)
        _BG_CACHE[key] = im
    return _BG_CACHE[key].copy()


def get_char_cached(t_global, pose, look, talking, scale):
    # Quantize to 10fps (0.1s) to accelerate rendering 3x with smooth animation
    tq = round(t_global * 10) / 10.0
    mouth_bit = 1 if (talking and int(tq * 5.5) % 2 == 0) else 0
    bob_step = int((tq * 10) % 28)
    blink_bit = 1 if (tq % 3.4) > 3.26 else 0
    key = (pose, look, mouth_bit, blink_bit, bob_step, round(scale, 2))
    if key not in _CHAR_CACHE:
        if len(_CHAR_CACHE) > 220:
            _CHAR_CACHE.clear()
        _CHAR_CACHE[key] = character.draw(tq, pose=pose, look=look, talking=talking, scale=scale)
    return _CHAR_CACHE[key]


def paste_an(base, x, y, t_global, pose="idle", look=-1, talking=False, scale=0.78):
    im = get_char_cached(t_global, pose, look, talking, scale)
    w_, h_ = im.size
    px, py = int(x - w_ / 2), int(y - h_)
    base.paste(im, (px, py), im)


def load_project_image(project_dir, filename):
    key = (project_dir, filename)
    if key not in _IMG_SRC:
        p = os.path.join(project_dir, "img", filename)
        if os.path.exists(p):
            _IMG_SRC[key] = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        else:
            _IMG_SRC[key] = None
    return _IMG_SRC[key]


def wrap_text(d, text, fnt, max_w, max_lines=3):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textbbox((0, 0), test, font=fnt)[2] <= max_w or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        if len(lines[-1]) > 3:
            lines[-1] = lines[-1].rstrip(".,;:") + "..."
    return lines


def fit_font(d, cfg, style, text, start_size, min_size, max_w):
    sz = start_size
    while sz >= min_size:
        f = get_font(cfg, style, sz)
        if d.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        sz -= 2
    return get_font(cfg, style, min_size)


# ─── SHARED CHROME (GRID, PARTICLES, HEADER, TITLE, SUBTITLE) ─────────────────
def draw_ambient_motion(img, theme, f_global):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    gcol = theme["grid"]

    # Subtle scrolling grid
    sp = 96
    off_y = int(f_global * 0.45) % sp
    for x in range(0, W, sp):
        d.line([(x, 84), (x, H)], fill=c_rgba(gcol, 11), width=1)
    for y in range(84 - sp, H, sp):
        yy = y + off_y
        if yy >= 84:
            d.line([(0, yy), (W, yy)], fill=c_rgba(gcol, 11), width=1)

    # Floating luminous particles
    for px, py, vx, vy, sz, ph in _PARTICLES:
        nx = (px + vx * f_global) % W
        ny = 90 + ((py - 90 + vy * f_global) % (H - 220))
        pulse = 0.45 + 0.55 * math.sin(f_global * 0.05 + ph)
        a = int(95 * pulse)
        r = max(1, int(sz * (0.75 + 0.35 * pulse)))
        d.ellipse((nx - r, ny - r, nx + r, ny + r), fill=c_rgba(gcol, a))

    img.alpha_composite(ov)


_HEADER_CACHE = {}


def draw_header(img, cfg, theme, tag, progress):
    key = (tag, tuple(theme["bg_top"]), tuple(theme["primary"]), tuple(theme["surface"]))
    if key not in _HEADER_CACHE:
        ov = Image.new("RGBA", (W, 84), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rectangle([(0, 0), (W, 82)], fill=c_rgba(theme["bg_top"], 235))
        d.line([(0, 82), (W, 82)], fill=c_rgba(theme["primary"], 55), width=1)

        logo = get_small_logo(cfg)
        ov.paste(logo, (28, 16), logo)
        d.text((92, 16), cfg["brand"]["name"], font=get_font(cfg, "bold", 22), fill=c_rgba(theme["text"], 245))
        d.text((92, 46), cfg["brand"]["tagline"], font=get_font(cfg, "regular", 15), fill=c_rgba(theme["muted"], 210))

        tf = fit_font(d, cfg, "semibold", tag, 17, 13, 620)
        tb = d.textbbox((0, 0), tag, font=tf)
        tw = tb[2] - tb[0]
        pw = tw + 44
        px2 = W - 36
        px1 = px2 - pw
        d.rounded_rectangle((px1, 20, px2, 58), radius=19,
                            fill=c_rgba(theme["surface"], 230),
                            outline=c_rgba(theme["primary"], 130), width=1)
        d.ellipse((px1 + 14, 34, px1 + 24, 44), fill=c_rgba(theme["primary"], 255))
        d.text((px1 + 32, 28), tag, font=tf, fill=c_rgba(theme["text"], 240))
        _HEADER_CACHE[key] = ov

    img.alpha_composite(_HEADER_CACHE[key], (0, 0))
    bar_w = int(W * clamp(progress))
    if bar_w > 0:
        ImageDraw.Draw(img).rectangle([(0, 79), (bar_w, 82)], fill=c_rgba(theme["primary"], 235))


def draw_scene_title(img, cfg, theme, kicker, title, subtitle, lt):
    p = ease_out(clamp(lt / 0.55))
    dy = int((1 - p) * 18)
    a = int(255 * p)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Kicker
    d.text((96, 108 + dy), kicker.upper(), font=get_font(cfg, "bold", 17), fill=c_rgba(theme["primary"], a))

    # Main title (strictly within x=96..1560 to stay far left of stamped logo!)
    tf = fit_font(d, cfg, "bold", title, 44, 28, 1450)
    d.text((96, 134 + dy), title, font=tf, fill=c_rgba(theme["text"], a))

    # Subtitle
    if subtitle:
        sf = fit_font(d, cfg, "regular", subtitle, 22, 16, 1450)
        d.text((96, 192 + dy), subtitle, font=sf, fill=c_rgba(theme["muted"], int(a * 0.92)))

    # Animated underline accent
    uw = int(180 * ease_out(clamp((lt - 0.15) / 0.6)))
    if uw > 2:
        d.rounded_rectangle((96, 232, 96 + uw, 237), radius=2, fill=c_rgba(theme["primary"], a))

    img.alpha_composite(ov)


def draw_subtitle_bar(img, cfg, theme, sub_text, cue_lt):
    if not sub_text:
        return
    a = int(255 * ease_out(clamp(cue_lt / 0.25)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    fnt = get_font(cfg, "semibold", 27)
    lines = wrap_text(d, sub_text, fnt, W - 260, max_lines=2)
    lh = 38
    box_h = max(76, len(lines) * lh + 26)
    y2 = H - 36
    y1 = y2 - box_h

    d.rounded_rectangle((96, y1, W - 96, y2), radius=14,
                        fill=c_rgba(theme["bg_top"], int(a * 0.88)),
                        outline=c_rgba(theme["primary"], int(a * 0.28)), width=1)
    d.rounded_rectangle((96, y1 + 8, 104, y2 - 8), radius=4, fill=c_rgba(theme["accent"], a))

    ty = y1 + (box_h - len(lines) * lh) // 2 - 2
    for i, ln in enumerate(lines):
        d.text((126, ty + i * lh), ln, font=fnt, fill=c_rgba(theme["text"], a))

    img.alpha_composite(ov)


def draw_glass_card(d, theme, box, radius=18, border_col=None, border_a=90, fill_a=225, accent_top=None):
    x1, y1, x2, y2 = box
    bc = border_col or theme["primary"]
    d.rounded_rectangle((x1, y1, x2, y2), radius=radius,
                        fill=c_rgba(theme["surface"], fill_a),
                        outline=c_rgba(bc, border_a), width=2)
    if accent_top is not None:
        d.rounded_rectangle((x1 + 22, y1, x2 - 22, y1 + 4), radius=2, fill=c_rgba(accent_top, min(255, border_a + 80)))


def draw_ken_burns_photo(img, cfg, theme, project_dir, filename, caption, box, lt, dur, accent_col=None, active=True):
    """Hiển thị ảnh trong img/ với chuyển động zoom/pan Ken Burns mượt + nhãn chú thích động."""
    x1, y1, x2, y2 = [int(v) for v in box]
    bw, bh = x2 - x1, y2 - y1
    p = ease_out(clamp(lt / 0.55))
    dy = int((1 - p) * 20)
    y1 += dy
    y2 += dy
    a = int(255 * p)
    ac = accent_col or theme["primary"]

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Outer glass frame
    draw_glass_card(d, theme, (x1, y1, x2, y2), radius=20,
                    border_col=ac, border_a=int(180 if active else 75),
                    fill_a=int(235 * p), accent_top=ac if active else None)

    pad = 10
    iw, ih = max(10, bw - pad * 2), max(10, bh - pad * 2)
    src = load_project_image(project_dir, filename)
    if src is not None:
        # Subtle Ken Burns zoom (1.0 -> 1.07 over scene duration)
        prog = clamp(lt / max(1.0, dur))
        zoom = 1.0 + 0.065 * ease_in_out(prog)

        # Preserve aspect ratio cleanly (contain on blurred dark backdrop so nothing gets clipped!)
        src_ar = src.width / max(1, src.height)
        box_ar = iw / max(1, ih)
        canvas = Image.new("RGB", (iw, ih), tuple(theme["bg_top"]))

        # Fit foreground inside zoomed frame
        if abs(src_ar - box_ar) < 0.35:
            # Close to box aspect -> smooth cover + zoom
            zw, zh = int(iw * zoom), int(ih * zoom)
            fitted = ImageOps.fit(src, (zw, zh), Image.BILINEAR)
            ox = int((zw - iw) * (0.5 + 0.15 * math.sin(prog * math.pi)))
            oy = int((zh - ih) * 0.5)
            ox = max(0, min(zw - iw, ox))
            oy = max(0, min(zh - ih, oy))
            canvas = fitted.crop((ox, oy, ox + iw, oy + ih))
        else:
            # Infographic / wide / tall -> contain with blurred dark fill
            bg = ImageOps.fit(src, (iw, ih), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10))
            bg = Image.blend(bg, Image.new("RGB", (iw, ih), tuple(theme["bg_top"])), 0.62)
            canvas.paste(bg, (0, 0))
            sc = min((iw - 12) / src.width, (ih - 12) / src.height) * (0.98 + 0.04 * prog)
            fw, fh = max(1, int(src.width * sc)), max(1, int(src.height * sc))
            fg = src.resize((fw, fh), Image.BILINEAR)
            # Clip cleanly if slightly oversized during zoom
            px = (iw - fw) // 2
            py = (ih - fh) // 2
            canvas.paste(fg, (px, py))

        photo_rgba = canvas.convert("RGBA")
        mask = Image.new("L", (iw, ih), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, iw - 1, ih - 1), radius=14, fill=a)
        photo_rgba.putalpha(mask)
        ov.paste(photo_rgba, (x1 + pad, y1 + pad), photo_rgba)

    # Floating caption pill at bottom-left of photo card
    if caption:
        cf = fit_font(d, cfg, "semibold", caption, 19, 14, iw - 40)
        cb = d.textbbox((0, 0), caption, font=cf)
        cw = cb[2] - cb[0] + 34
        cx1 = x1 + 20
        cy2 = y2 - 20
        cy1 = cy2 - 38
        d.rounded_rectangle((cx1, cy1, cx1 + cw, cy2), radius=19,
                            fill=c_rgba(theme["bg_top"], int(225 * p)),
                            outline=c_rgba(ac, int(200 * p)), width=1)
        d.ellipse((cx1 + 12, cy1 + 14, cx1 + 22, cy1 + 24), fill=c_rgba(ac, a))
        d.text((cx1 + 28, cy1 + 7), caption, font=cf, fill=c_rgba(theme["text"], a))

    img.alpha_composite(ov)


# ─── 8 MOTION-GRAPHICS SCENE TEMPLATES ───────────────────────────────────────

def tpl_intro(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 1: Intro kinetic — vòng sáng quỹ đạo, hero card, các cột mốc nội dung."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Pulsing orbital rings centered in stage
    cx, cy = 800, 560
    for i in range(4):
        rp = clamp((lt - i * 0.25) / 2.2)
        rad = int(120 + i * 85 + 25 * math.sin(lt * 1.4 + i))
        ra = int(50 * rp * (1 - i * 0.18))
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad),
                  outline=c_rgba(theme["primary"], ra), width=2)

    draw_scene_title(img, cfg, theme, "BÀI GIẢNG CÔNG NGHỆ · AN TECH ACADEMY",
                     sc["title"], sc["subtitle"] or "Hệ thống sản xuất video bài giảng tự động 100% offline trên Terminal", lt)

    # Left hero visual (either image from img/ or dynamic hero emblem)
    if sc["images"]:
        im0 = sc["images"][0]
        draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], im0["file"], im0["caption"],
                             (96, 275, 960, 845), lt, dur, accent_col=theme["primary"], active=True)
        right_x1 = 995
        right_x2 = 1500
    else:
        # Dynamic hero badge card on left
        p0 = ease_out(clamp(lt / 0.7))
        draw_glass_card(d, theme, (96, 285, 860, 825), radius=24,
                        border_col=theme["primary"], border_a=int(150 * p0),
                        fill_a=int(210 * p0), accent_top=theme["primary"])
        # Big animated concentric emblem
        ec_x, ec_y = 478, 515
        for k in range(3):
            rr = 85 + k * 42 + int(6 * math.sin(lt * 2.5 + k))
            d.ellipse((ec_x - rr, ec_y - rr, ec_x + rr, ec_y + rr),
                      outline=c_rgba(theme["primary"], int((160 - k * 45) * p0)), width=2)
        logo = get_small_logo(cfg).resize((116, 116), Image.LANCZOS)
        ov.paste(logo, (ec_x - 58, ec_y - 58), logo)
        d.text((220, 695), "0% AI · 0% API KEY · 100% OFFLINE",
               font=get_font(cfg, "bold", 26), fill=c_rgba(theme["primary"], int(255 * p0)))
        right_x1 = 900
        right_x2 = 1500

    # Right side: animated highlights / steps cards cascading in
    items = sc["steps"] or [
        {"title": "100% Chạy Terminal", "desc": "Không cần Agent hay API"},
        {"title": "Giọng Clone VieNeu", "desc": "Chuẩn -14 LUFS tự động"},
        {"title": "Animation Sáng Tạo", "desc": "Kho 8 template dùng chung"},
    ]
    n = min(4, len(items))
    card_h = 118 if n <= 4 else 100
    gap = 20
    start_y = 285 + max(0, (550 - (n * card_h + (n - 1) * gap)) // 2)
    for i, it in enumerate(items[:n]):
        ip = ease_out(clamp((lt - 0.35 - i * 0.32) / 0.55))
        if ip <= 0:
            continue
        dx = int((1 - ip) * 36)
        cy1 = start_y + i * (card_h + gap)
        cy2 = cy1 + card_h
        col = [theme["primary"], theme["accent"], theme["success"], theme["warning"]][i % 4]
        draw_glass_card(d, theme, (right_x1 + dx, cy1, right_x2 + dx, cy2),
                        radius=16, border_col=col, border_a=int(150 * ip), fill_a=int(220 * ip))
        d.rounded_rectangle((right_x1 + dx, cy1 + 14, right_x1 + dx + 7, cy2 - 14),
                            radius=3, fill=c_rgba(col, int(255 * ip)))
        tf = fit_font(d, cfg, "bold", it["title"], 23, 17, right_x2 - right_x1 - 45)
        d.text((right_x1 + dx + 26, cy1 + 22), it["title"], font=tf, fill=c_rgba(theme["text"], int(255 * ip)))
        if it["desc"]:
            df = fit_font(d, cfg, "regular", it["desc"], 18, 14, right_x2 - right_x1 - 45)
            d.text((right_x1 + dx + 26, cy1 + 60), it["desc"], font=df, fill=c_rgba(theme["muted"], int(230 * ip)))

    img.alpha_composite(ov)
    pose = "wave" if lt < 2.8 else "present"
    paste_an(img, 1715, 875, t_global, pose=pose, look=-1, talking=talking, scale=0.80)


def tpl_va_cham(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 2: Va chạm / Xung đột — 2 luồng chạy vào tâm, tia năng lượng, cảnh báo."""
    draw_scene_title(img, cfg, theme, "PHÂN TÍCH VẤN ĐỀ · XUNG ĐỘT LUỒNG",
                     sc["title"], sc["subtitle"], lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    left = sc["left"] or {"name": "Cách cũ thủ công", "detail": "Chạy từng lệnh rời rạc"}
    right = sc["right"] or {"name": "Viết code cứng", "detail": "Mỗi bài viết lại 700 dòng"}
    warn = sc["warning"] or "Mất thời gian, dễ quên bước QA hoặc lỗi phát âm!"

    stage_cx = 800
    card_y1, card_y2 = 310, 560
    p_move = ease_out(clamp(lt / 1.4))

    # Left entity slides in from left
    lx1 = int(lerp(20, 120, p_move))
    lx2 = lx1 + 430
    draw_glass_card(d, theme, (lx1, card_y1, lx2, card_y2), radius=20,
                    border_col=theme["secondary"], border_a=int(200 * p_move),
                    fill_a=int(230 * p_move), accent_top=theme["secondary"])
    d.text((lx1 + 28, card_y1 + 26), "LUỒNG A", font=get_font(cfg, "bold", 16),
           fill=c_rgba(theme["secondary"], int(255 * p_move)))
    lf = fit_font(d, cfg, "bold", left["name"], 30, 20, 374)
    d.text((lx1 + 28, card_y1 + 60), left["name"], font=lf, fill=c_rgba(theme["text"], int(255 * p_move)))
    for i, ln in enumerate(wrap_text(d, left["detail"], get_font(cfg, "regular", 20), 374, 3)):
        d.text((lx1 + 28, card_y1 + 114 + i * 30), ln, font=get_font(cfg, "regular", 20),
               fill=c_rgba(theme["muted"], int(235 * p_move)))

    # Right entity slides in from right
    rx1 = int(lerp(1160, 1050, p_move))
    rx2 = rx1 + 430
    draw_glass_card(d, theme, (rx1, card_y1, rx2, card_y2), radius=20,
                    border_col=theme["warning"], border_a=int(200 * p_move),
                    fill_a=int(230 * p_move), accent_top=theme["warning"])
    d.text((rx1 + 28, card_y1 + 26), "LUỒNG B", font=get_font(cfg, "bold", 16),
           fill=c_rgba(theme["warning"], int(255 * p_move)))
    rf = fit_font(d, cfg, "bold", right["name"], 30, 20, 374)
    d.text((rx1 + 28, card_y1 + 60), right["name"], font=rf, fill=c_rgba(theme["text"], int(255 * p_move)))
    for i, ln in enumerate(wrap_text(d, right["detail"], get_font(cfg, "regular", 20), 374, 3)):
        d.text((rx1 + 28, card_y1 + 114 + i * 30), ln, font=get_font(cfg, "regular", 20),
               fill=c_rgba(theme["muted"], int(235 * p_move)))

    # Animated energy beams + traveling packets toward center
    cy_mid = (card_y1 + card_y2) // 2
    d.line([(lx2 + 12, cy_mid), (stage_cx - 62, cy_mid)], fill=c_rgba(theme["secondary"], 160), width=4)
    d.line([(rx1 - 12, cy_mid), (stage_cx + 62, cy_mid)], fill=c_rgba(theme["warning"], 160), width=4)
    pkt = (lt * 0.9) % 1.0
    plx = int(lerp(lx2 + 12, stage_cx - 65, pkt))
    prx = int(lerp(rx1 - 12, stage_cx + 65, pkt))
    d.ellipse((plx - 9, cy_mid - 9, plx + 9, cy_mid + 9), fill=c_rgba(theme["primary"], 255))
    d.ellipse((prx - 9, cy_mid - 9, prx + 9, cy_mid + 9), fill=c_rgba(theme["warning"], 255))

    # Central conflict shockwave rings
    for k in range(3):
        rp = ((lt * 0.85) + k * 0.33) % 1.0
        rr = int(48 + rp * 76)
        ra = int(185 * (1 - rp))
        d.ellipse((stage_cx - rr, cy_mid - rr, stage_cx + rr, cy_mid + rr),
                  outline=c_rgba(theme["danger"], ra), width=3)

    d.ellipse((stage_cx - 56, cy_mid - 56, stage_cx + 56, cy_mid + 56),
              fill=c_rgba(theme["danger"], 42), outline=c_rgba(theme["danger"], 240), width=3)
    d.text((stage_cx - 17, cy_mid - 26), "!", font=get_font(cfg, "bold", 50),
           fill=c_rgba(theme["danger"], 255))

    # Warning banner below (animates in after 1.3s)
    wp = ease_out(clamp((lt - 1.2) / 0.65))
    if wp > 0:
        wy1, wy2 = 615, 720
        pulse = int(170 + 70 * math.sin(lt * 5.0))
        d.rounded_rectangle((120, wy1, 1480, wy2), radius=16,
                            fill=c_rgba(theme["danger"], int(34 * wp)),
                            outline=c_rgba(theme["danger"], int(pulse * wp)), width=2)
        d.rounded_rectangle((120, wy1 + 10, 129, wy2 - 10), radius=4, fill=c_rgba(theme["danger"], int(255 * wp)))
        wf = fit_font(d, cfg, "bold", "CẢNH BÁO: " + warn, 27, 19, 1300)
        d.text((154, wy1 + 34), "CẢNH BÁO: " + warn, font=wf, fill=c_rgba(theme["text"], int(255 * wp)))

    # Optional bottom chips from steps
    if sc["steps"] and wp > 0:
        n = min(3, len(sc["steps"]))
        cw = (1360 - (n - 1) * 22) // n
        for i, st in enumerate(sc["steps"][:n]):
            sp = ease_out(clamp((lt - 1.8 - i * 0.25) / 0.45))
            if sp <= 0:
                continue
            bx1 = 120 + i * (cw + 22)
            draw_glass_card(d, theme, (bx1, 750, bx1 + cw, 845), radius=14,
                            border_col=theme["danger"], border_a=int(120 * sp), fill_a=int(215 * sp))
            tf = fit_font(d, cfg, "semibold", st["title"], 20, 15, cw - 30)
            d.text((bx1 + 18, 768), st["title"], font=tf, fill=c_rgba(theme["text"], int(255 * sp)))
            if st["desc"]:
                df = fit_font(d, cfg, "regular", st["desc"], 16, 13, cw - 30)
                d.text((bx1 + 18, 804), st["desc"], font=df, fill=c_rgba(theme["muted"], int(225 * sp)))

    img.alpha_composite(ov)
    paste_an(img, 1715, 875, t_global, pose="think" if lt < 2.5 else "point_left", look=-1, talking=talking, scale=0.78)


def tpl_dem_so(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 3: Số liệu đếm động + progress bar + optional visual card."""
    draw_scene_title(img, cfg, theme, "CHỈ SỐ & QUY MÔ HỆ THỐNG",
                     sc["title"], sc["subtitle"], lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    stats = sc["stats"] or [
        {"value": 100, "suffix": "%", "label": "Chạy Offline hoàn toàn trên máy"},
        {"value": 0, "suffix": "đ", "label": "Chi phí API key hàng tháng"},
        {"value": 8, "suffix": "", "label": "Mẫu hiệu ứng Animation sáng tạo"},
        {"value": 14, "suffix": " LUFS", "label": "Chuẩn âm lượng phát sóng tự động"},
    ]

    has_img = bool(sc["images"])
    col_x1 = 96
    col_x2 = 965 if has_img else 1480
    n = min(4, len(stats))
    row_h = 122 if n <= 4 else 104
    gap = 22
    start_y = 285 + max(0, (560 - (n * row_h + (n - 1) * gap)) // 2)
    palette = [theme["primary"], theme["success"], theme["accent"], theme["warning"]]

    for i, st in enumerate(stats[:n]):
        sp = ease_out(clamp((lt - i * 0.4) / 1.4))
        a = int(255 * ease_out(clamp((lt - i * 0.35) / 0.5)))
        if a <= 0:
            continue
        col = palette[i % len(palette)]
        y1 = start_y + i * (row_h + gap)
        y2 = y1 + row_h

        draw_glass_card(d, theme, (col_x1, y1, col_x2, y2), radius=16,
                        border_col=col, border_a=int(150 * (a / 255)), fill_a=int(225 * (a / 255)))
        d.rounded_rectangle((col_x1, y1 + 12, col_x1 + 7, y2 - 12), radius=3, fill=c_rgba(col, a))

        # Animated count-up number
        target = st["value"]
        cur_v = target * sp
        suf = st.get("suffix", "")
        if suf and suf[0].isalpha() and suf not in ("đ", "d"):
            suf = " " + suf
        if isinstance(target, int):
            num_txt = f"{int(round(cur_v)):,}".replace(",", ".") + suf
        else:
            num_txt = f"{cur_v:.1f}" + suf

        nf = get_font(cfg, "bold", 44)
        nb = d.textbbox((0, 0), num_txt, font=nf)
        nw = nb[2] - nb[0]
        d.text((col_x2 - nw - 28, y1 + 16), num_txt, font=nf, fill=c_rgba(col, a))

        # Label
        lf = fit_font(d, cfg, "semibold", st["label"], 24, 17, col_x2 - col_x1 - nw - 80)
        d.text((col_x1 + 28, y1 + 26), st["label"], font=lf, fill=c_rgba(theme["text"], a))

        # Animated progress bar
        bx1, bx2 = col_x1 + 28, col_x2 - 28
        by1, by2 = y2 - 30, y2 - 16
        d.rounded_rectangle((bx1, by1, bx2, by2), radius=7, fill=c_rgba(theme["bg_top"], a))
        fill_frac = 0.22 + 0.72 * ((i % 3 + 1) / 3.0) if target == 0 else 0.88
        fw = max(14, int((bx2 - bx1) * fill_frac * sp))
        d.rounded_rectangle((bx1, by1, bx1 + fw, by2), radius=7, fill=c_rgba(col, a))

    img.alpha_composite(ov)

    if has_img:
        im0 = sc["images"][0]
        draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], im0["file"], im0["caption"],
                             (995, 285, 1500, 845), lt, dur, accent_col=theme["accent"], active=True)

    paste_an(img, 1715, 875, t_global, pose="present", look=-1, talking=talking, scale=0.78)


def tpl_so_sanh(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 4: So sánh Trước vs Sau có tia quét năng lượng ở giữa."""
    draw_scene_title(img, cfg, theme, "SO SÁNH TRỰC QUAN · TRƯỚC & SAU",
                     sc["title"], sc["subtitle"], lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    before_list = sc["before"] or ["Phải chờ Agent viết code mới", "Chạy rời rạc 5 lệnh thủ công", "Dễ quên logo hoặc sai phát âm"]
    after_list = sc["after"] or ["Dùng chung 1 kho Kit chuẩn hóa", "Gõ 1 lệnh Terminal ra thẳng MP4", "Tự động QA -14 LUFS & đóng logo"]

    p_l = ease_out(clamp(lt / 0.65))
    p_r = ease_out(clamp((lt - 0.55) / 0.65))

    # Left card (Before - danger/red)
    lx1, ly1, lx2, ly2 = 96, 285, 745, 845
    draw_glass_card(d, theme, (lx1, ly1, lx2, ly2), radius=20,
                    border_col=theme["danger"], border_a=int(180 * p_l),
                    fill_a=int(225 * p_l), accent_top=theme["danger"])
    d.rounded_rectangle((lx1 + 24, ly1 + 24, lx1 + 280, ly1 + 66), radius=12,
                        fill=c_rgba(theme["danger"], int(42 * p_l)))
    # Crisp vector X icon
    d.line([(lx1 + 42, ly1 + 38), (lx1 + 56, ly1 + 52)], fill=c_rgba(theme["danger"], int(255 * p_l)), width=3)
    d.line([(lx1 + 56, ly1 + 38), (lx1 + 42, ly1 + 52)], fill=c_rgba(theme["danger"], int(255 * p_l)), width=3)
    d.text((lx1 + 72, ly1 + 32), "CÁCH CŨ", font=get_font(cfg, "bold", 22),
           fill=c_rgba(theme["danger"], int(255 * p_l)))

    for i, item in enumerate(before_list[:5]):
        ip = ease_out(clamp((lt - 0.35 - i * 0.35) / 0.5))
        if ip <= 0:
            continue
        iy = ly1 + 98 + i * 86
        d.ellipse((lx1 + 28, iy + 8, lx1 + 44, iy + 24), fill=c_rgba(theme["danger"], int(230 * ip)))
        lines = wrap_text(d, item, get_font(cfg, "semibold", 21), 560, 2)
        for j, ln in enumerate(lines):
            d.text((lx1 + 60, iy + j * 30), ln, font=get_font(cfg, "semibold", 21),
                   fill=c_rgba(theme["text"], int(240 * ip)))

    # Center glowing transformation beam + animated arrow
    cx, cy = 800, 565
    bp = ease_out(clamp((lt - 0.35) / 0.6))
    pulse_r = int(42 + 6 * math.sin(lt * 4.5))
    d.ellipse((cx - pulse_r, cy - pulse_r, cx + pulse_r, cy + pulse_r),
              fill=c_rgba(theme["primary"], int(38 * bp)),
              outline=c_rgba(theme["primary"], int(220 * bp)), width=3)
    d.polygon([(cx - 12, cy - 14), (cx - 12, cy + 14), (cx + 16, cy)],
              fill=c_rgba(theme["primary"], int(255 * bp)))

    # Right card (After - success/emerald)
    rx1, ry1, rx2, ry2 = 855, 285, 1504, 845
    draw_glass_card(d, theme, (rx1, ry1, rx2, ry2), radius=20,
                    border_col=theme["success"], border_a=int(200 * p_r),
                    fill_a=int(230 * p_r), accent_top=theme["success"])
    d.rounded_rectangle((rx1 + 24, ry1 + 24, rx1 + 320, ry1 + 66), radius=12,
                        fill=c_rgba(theme["success"], int(42 * p_r)))
    # Crisp vector checkmark icon
    d.line([(rx1 + 40, ry1 + 46), (rx1 + 47, ry1 + 53), (rx1 + 60, ry1 + 38)],
           fill=c_rgba(theme["success"], int(255 * p_r)), width=3)
    d.text((rx1 + 74, ry1 + 32), "CÁCH MỚI (KIT)", font=get_font(cfg, "bold", 22),
           fill=c_rgba(theme["success"], int(255 * p_r)))

    for i, item in enumerate(after_list[:5]):
        ip = ease_out(clamp((lt - 0.9 - i * 0.35) / 0.5))
        if ip <= 0:
            continue
        iy = ry1 + 98 + i * 86
        d.ellipse((rx1 + 28, iy + 8, rx1 + 44, iy + 24), fill=c_rgba(theme["success"], int(245 * ip)))
        lines = wrap_text(d, item, get_font(cfg, "semibold", 21), 560, 2)
        for j, ln in enumerate(lines):
            d.text((rx1 + 60, iy + j * 30), ln, font=get_font(cfg, "semibold", 21),
                   fill=c_rgba(theme["text"], int(255 * ip)))

    img.alpha_composite(ov)
    paste_an(img, 1715, 875, t_global, pose="point_left", look=-1, talking=talking, scale=0.78)


def tpl_code(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 5: Terminal / Code Spotlight — gõ từng dòng + khung sáng trượt theo tiến độ."""
    draw_scene_title(img, cfg, theme, f"THỰC HÀNH LỆNH · {(sc['code_lang'] or 'TERMINAL').upper()}",
                     sc["title"], sc["subtitle"], lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    has_img = bool(sc["images"])
    x1, y1 = 96, 280
    x2 = 975 if has_img else 1490
    y2 = 850
    p = ease_out(clamp(lt / 0.55))

    # IDE / Terminal dark window
    d.rounded_rectangle((x1, y1, x2, y2), radius=18,
                        fill=(11, 17, 30, int(245 * p)),
                        outline=c_rgba(theme["primary"], int(150 * p)), width=2)
    # Title bar
    d.rounded_rectangle((x1, y1, x2, y1 + 48), radius=18, fill=c_rgba(theme["surface_alt"], int(240 * p)))
    d.rectangle((x1, y1 + 30, x2, y1 + 48), fill=c_rgba(theme["surface_alt"], int(240 * p)))
    for k, dot_c in enumerate([(239, 68, 68), (245, 158, 11), (16, 185, 129)]):
        d.ellipse((x1 + 22 + k * 24, y1 + 17, x1 + 36 + k * 24, y1 + 31), fill=c_rgba(dot_c, int(235 * p)))
    win_lbl = f"PowerShell · {(sc['code_lang'] or 'terminal').lower()}"
    d.text((x1 + 106, y1 + 13), win_lbl, font=get_font(cfg, "mono", 17), fill=c_rgba(theme["muted"], int(230 * p)))

    code_lines = (sc["code"] or "python D:\\Edit\\Kit\\tools\\build.py render Baigiang_Moi").splitlines()
    code_lines = code_lines[:13]
    n_lines = max(1, len(code_lines))
    lh = min(40, max(28, (y2 - y1 - 80) // n_lines))
    mf = get_font(cfg, "mono", 20 if not has_img else 17)

    # Reveal progress & active highlight line (skip blank lines)
    reveal_p = clamp((lt - 0.25) / max(1.8, dur * 0.55))
    total_chars = sum(len(ln) + 1 for ln in code_lines)
    shown_chars = int(total_chars * reveal_p)
    non_empty = [idx for idx, ln in enumerate(code_lines) if ln.strip()] or [0]
    active_line = non_empty[min(len(non_empty) - 1, int(clamp(lt / max(1.0, dur)) * len(non_empty)))]

    # Moving spotlight highlight bar on active line
    hy1 = y1 + 66 + active_line * lh - 4
    d.rounded_rectangle((x1 + 14, hy1, x2 - 14, hy1 + lh), radius=8,
                        fill=c_rgba(theme["primary"], 32),
                        outline=c_rgba(theme["primary"], 90), width=1)

    rem = shown_chars
    for i, ln in enumerate(code_lines):
        ly = y1 + 66 + i * lh
        # Line number
        d.text((x1 + 22, ly), f"{i + 1:2d}", font=mf, fill=c_rgba(theme["muted"], 120))
        if rem <= 0:
            break
        part = ln[:rem]
        rem -= (len(ln) + 1)

        # Simple syntax tinting
        s_strip = ln.strip()
        if s_strip.startswith("#") or s_strip.startswith("//"):
            col = theme["muted"]
        elif s_strip.startswith("python") or s_strip.startswith("$") or s_strip.startswith("##"):
            col = theme["primary"]
        elif s_strip.startswith(">") or s_strip.startswith("[OK]"):
            col = theme["success"]
        elif s_strip.startswith("-"):
            col = theme["warning"]
        else:
            col = theme["text"]

        # Clip text cleanly inside window
        while part and d.textbbox((0, 0), part, font=mf)[2] > (x2 - x1 - 90):
            part = part[:-1]
        d.text((x1 + 66, ly), part, font=mf, fill=c_rgba(col, 255))

        # Blinking cursor on currently typed line
        if rem <= 0 and int(lt * 4) % 2 == 0:
            cw = d.textbbox((0, 0), part, font=mf)[2]
            d.rectangle((x1 + 68 + cw, ly + 2, x1 + 78 + cw, ly + lh - 10), fill=c_rgba(theme["primary"], 255))

    img.alpha_composite(ov)

    if has_img:
        im0 = sc["images"][0]
        draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], im0["file"], im0["caption"],
                             (1000, 280, 1500, 850), lt, dur, accent_col=theme["success"], active=True)

    paste_an(img, 1715, 875, t_global, pose="write" if reveal_p < 0.9 else "point_left", look=-1, talking=talking, scale=0.78)


def tpl_quy_trinh(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 6: Quy trình các bước nối dây phát sáng + nhịp năng lượng chạy dọc pipeline."""
    draw_scene_title(img, cfg, theme, "QUY TRÌNH TỰ ĐỘNG HÓA · PIPELINE",
                     sc["title"], sc["subtitle"], lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    steps = sc["steps"] or [
        {"title": "Bước 1 · Đọc Markdown", "desc": "Phân tích cảnh, ảnh, lời đọc"},
        {"title": "Bước 2 · Giọng Clone", "desc": "VieNeu-TTS offline + Cache"},
        {"title": "Bước 3 · Render Động", "desc": "Đa nhân CPU + Nhân vật An"},
        {"title": "Bước 4 · Logo & QA", "desc": "Chuẩn -14 LUFS & kiểm định"},
    ]
    n = min(5, len(steps))
    has_img = bool(sc["images"])
    active_idx = min(n - 1, int(clamp(lt / max(1.0, dur)) * n))
    palette = [theme["primary"], theme["secondary"], theme["accent"], theme["success"], theme["warning"]]

    if has_img:
        # Left vertical glowing pipeline + right Ken Burns photo
        px1, px2 = 96, 870
        card_h = min(122, (560 - (n - 1) * 18) // max(1, n))
        gap = 18
        sy = 285 + max(0, (560 - (n * card_h + (n - 1) * gap)) // 2)
        for i, st in enumerate(steps[:n]):
            ip = ease_out(clamp((lt - i * 0.35) / 0.5))
            if ip <= 0:
                continue
            y1 = sy + i * (card_h + gap)
            y2 = y1 + card_h
            col = palette[i % len(palette)]
            is_act = (i == active_idx)
            # Connector line to next step
            if i < n - 1:
                cx = px1 + 36
                d.line([(cx, y2), (cx, y2 + gap)], fill=c_rgba(col, 140), width=4)
                py_dot = int(lerp(y2, y2 + gap, (lt * 1.4) % 1.0))
                d.ellipse((cx - 5, py_dot - 5, cx + 5, py_dot + 5), fill=c_rgba(theme["primary"], 255))

            draw_glass_card(d, theme, (px1, y1, px2, y2), radius=16,
                            border_col=col, border_a=int((240 if is_act else 95) * ip),
                            fill_a=int(235 * ip), accent_top=col if is_act else None)
            # Step badge circle
            d.ellipse((px1 + 16, y1 + card_h // 2 - 20, px1 + 56, y1 + card_h // 2 + 20),
                      fill=c_rgba(col, int((230 if is_act else 70) * ip)))
            d.text((px1 + 29, y1 + card_h // 2 - 14), str(i + 1), font=get_font(cfg, "bold", 22),
                   fill=c_rgba(theme["bg_top"] if is_act else theme["text"], int(255 * ip)))
            tf = fit_font(d, cfg, "bold", st["title"], 23, 17, px2 - px1 - 95)
            d.text((px1 + 74, y1 + 18), st["title"], font=tf, fill=c_rgba(theme["text"], int(255 * ip)))
            if st["desc"]:
                df = fit_font(d, cfg, "regular", st["desc"], 18, 14, px2 - px1 - 95)
                d.text((px1 + 74, y1 + 56), st["desc"], font=df, fill=c_rgba(theme["muted"], int(230 * ip)))

        img.alpha_composite(ov)
        im0 = sc["images"][0]
        draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], im0["file"], im0["caption"],
                             (900, 285, 1500, 845), lt, dur, accent_col=theme["primary"], active=True)
    else:
        # Full-stage horizontal glowing pipeline with moving energy pulse
        gap = 34
        card_w = (1404 - (n - 1) * gap) // n
        cy1, cy2 = 340, 770
        for i, st in enumerate(steps[:n]):
            ip = ease_out(clamp((lt - i * 0.38) / 0.55))
            if ip <= 0:
                continue
            x1 = 96 + i * (card_w + gap)
            x2 = x1 + card_w
            col = palette[i % len(palette)]
            is_act = (i == active_idx)
            dy = -10 if is_act else 0

            # Animated arrow to next node
            if i < n - 1:
                ay = (cy1 + cy2) // 2
                d.line([(x2 + 2, ay), (x2 + gap - 6, ay)], fill=c_rgba(col, 160), width=4)
                d.polygon([(x2 + gap - 10, ay - 9), (x2 + gap - 10, ay + 9), (x2 + gap, ay)],
                          fill=c_rgba(col, 220))
                px_dot = int(lerp(x2 + 2, x2 + gap - 8, (lt * 1.3 + i * 0.2) % 1.0))
                d.ellipse((px_dot - 6, ay - 6, px_dot + 6, ay + 6), fill=c_rgba(theme["text"], 255))

            draw_glass_card(d, theme, (x1, cy1 + dy, x2, cy2 + dy), radius=20,
                            border_col=col, border_a=int((245 if is_act else 100) * ip),
                            fill_a=int(232 * ip), accent_top=col)

            # Big circular step badge
            bcx = (x1 + x2) // 2
            bcy = cy1 + dy + 68
            if is_act:
                rr = int(42 + 6 * math.sin(lt * 5))
                d.ellipse((bcx - rr, bcy - rr, bcx + rr, bcy + rr), outline=c_rgba(col, 130), width=2)
            d.ellipse((bcx - 34, bcy - 34, bcx + 34, bcy + 34), fill=c_rgba(col, int(230 * ip)))
            d.text((bcx - 10, bcy - 20), str(i + 1), font=get_font(cfg, "bold", 34),
                   fill=c_rgba(theme["bg_top"], int(255 * ip)))

            # Title wrapped centered
            tf = get_font(cfg, "bold", 22 if n <= 4 else 19)
            t_lines = wrap_text(d, st["title"], tf, card_w - 30, 3)
            for j, ln in enumerate(t_lines):
                tw = d.textbbox((0, 0), ln, font=tf)[2]
                d.text((bcx - tw // 2, cy1 + dy + 132 + j * 30), ln, font=tf, fill=c_rgba(theme["text"], int(255 * ip)))

            # Description wrapped centered
            if st["desc"]:
                df = get_font(cfg, "regular", 18 if n <= 4 else 16)
                d_lines = wrap_text(d, st["desc"], df, card_w - 30, 4)
                for j, ln in enumerate(d_lines):
                    dw = d.textbbox((0, 0), ln, font=df)[2]
                    d.text((bcx - dw // 2, cy1 + dy + 235 + j * 26), ln, font=df, fill=c_rgba(theme["muted"], int(230 * ip)))

        img.alpha_composite(ov)

    paste_an(img, 1715, 875, t_global, pose="point_left", look=-1, talking=talking, scale=0.78)


def tpl_anh_dong(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 7: Trình diễn ảnh từ img/ có chuyển động Ken Burns + spotlight theo tiến độ."""
    draw_scene_title(img, cfg, theme, "MINH HỌA TRỰC QUAN · HÌNH ẢNH ĐỘNG",
                     sc["title"], sc["subtitle"], lt)

    imgs = sc["images"]
    if not imgs:
        # Fallback cleanly to quy_trinh if no images given
        tpl_quy_trinh(img, cfg, theme, sc, lt, dur, t_global, talking)
        return

    n = min(3, len(imgs))
    active_i = min(n - 1, int(clamp(lt / max(1.0, dur)) * n))
    palette = [theme["primary"], theme["accent"], theme["success"]]

    if n == 1:
        draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], imgs[0]["file"], imgs[0]["caption"],
                             (96, 275, 1495, 855), lt, dur, accent_col=palette[0], active=True)
    elif n == 2:
        gap = 26
        w_each = (1400 - gap) // 2
        for i in range(2):
            bx1 = 96 + i * (w_each + gap)
            draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], imgs[i]["file"], imgs[i]["caption"],
                                 (bx1, 285, bx1 + w_each, 845), max(0.0, lt - i * 0.45), dur,
                                 accent_col=palette[i], active=(i == active_i))
    else:
        gap = 22
        w_each = (1404 - gap * 2) // 3
        for i in range(3):
            bx1 = 96 + i * (w_each + gap)
            draw_ken_burns_photo(img, cfg, theme, sc["_project_dir"], imgs[i]["file"], imgs[i]["caption"],
                                 (bx1, 305, bx1 + w_each, 825), max(0.0, lt - i * 0.4), dur,
                                 accent_col=palette[i], active=(i == active_i))

    paste_an(img, 1715, 875, t_global, pose="point_left", look=-1, talking=talking, scale=0.78)


def tpl_outro(img, cfg, theme, sc, lt, dur, t_global, talking):
    """Template 8: Tổng kết cốt lõi + tụ hạt logo AN TECH ACADEMY + lời kết."""
    draw_scene_title(img, cfg, theme, "TỔNG KẾT BÀI GIẢNG · AN TECH ACADEMY",
                     sc["title"], sc["subtitle"] or "Ghi nhớ nhanh để áp dụng ngay trên máy của bạn", lt)

    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Left column: 3 core takeaways popping in
    items = sc["steps"] or [
        {"title": "100% Offline & Miễn phí", "desc": "Không cần Agent hay API key"},
        {"title": "Chỉ 3 lệnh Terminal", "desc": "check -> preview -> render"},
        {"title": "Dễ nâng cấp giao diện", "desc": "Chỉnh màu & template ngay trong Kit"},
    ]
    n = min(3, len(items))
    palette = [theme["primary"], theme["success"], theme["accent"]]
    for i, it in enumerate(items[:n]):
        ip = ease_out(clamp((lt - 0.3 - i * 0.45) / 0.55))
        if ip <= 0:
            continue
        col = palette[i % len(palette)]
        y1 = 290 + i * 155
        y2 = y1 + 132
        dx = int((1 - ip) * -32)
        draw_glass_card(d, theme, (96 + dx, y1, 930 + dx, y2), radius=18,
                        border_col=col, border_a=int(180 * ip), fill_a=int(230 * ip))
        d.ellipse((122 + dx, y1 + 42, 166 + dx, y1 + 86), fill=c_rgba(col, int(230 * ip)))
        d.line([(134 + dx, y1 + 64), (142 + dx, y1 + 73), (156 + dx, y1 + 55)],
               fill=c_rgba(theme["bg_top"], int(255 * ip)), width=4)
        tf = fit_font(d, cfg, "bold", it["title"], 26, 18, 720)
        d.text((186 + dx, y1 + 26), it["title"], font=tf, fill=c_rgba(theme["text"], int(255 * ip)))
        if it["desc"]:
            df = fit_font(d, cfg, "regular", it["desc"], 20, 15, 720)
            d.text((186 + dx, y1 + 70), it["desc"], font=df, fill=c_rgba(theme["muted"], int(235 * ip)))

    # Right card: Brand Outro Spotlight
    bp = ease_out(clamp((lt - 0.5) / 0.7))
    draw_glass_card(d, theme, (970, 290, 1500, 742), radius=24,
                    border_col=theme["primary"], border_a=int(190 * bp),
                    fill_a=int(225 * bp), accent_top=theme["primary"])
    cx, cy = 1235, 455
    for k in range(3):
        rr = 76 + k * 28 + int(5 * math.sin(lt * 2.8 + k))
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr),
                  outline=c_rgba(theme["primary"], int((140 - k * 35) * bp)), width=2)
    logo = get_small_logo(cfg).resize((118, 118), Image.LANCZOS)
    ov.paste(logo, (cx - 59, cy - 59), logo)

    bn = cfg["brand"]["name"]
    bf = get_font(cfg, "bold", 30)
    bw = d.textbbox((0, 0), bn, font=bf)[2]
    d.text((cx - bw // 2, 565), bn, font=bf, fill=c_rgba(theme["primary"], int(255 * bp)))

    cta = "Theo dõi kênh · Hẹn gặp bài sau!"
    cf = get_font(cfg, "semibold", 20)
    cw = d.textbbox((0, 0), cta, font=cf)[2]
    d.rounded_rectangle((cx - cw // 2 - 22, 628, cx + cw // 2 + 22, 676), radius=24,
                        fill=c_rgba(theme["primary"], int(38 * bp)),
                        outline=c_rgba(theme["primary"], int(200 * bp)), width=2)
    d.text((cx - cw // 2, 639), cta, font=cf, fill=c_rgba(theme["text"], int(255 * bp)))

    img.alpha_composite(ov)
    paste_an(img, 1715, 875, t_global, pose="wave", look=0, talking=talking, scale=0.82)


TEMPLATE_DISPATCH = {
    "intro": tpl_intro,
    "va_cham": tpl_va_cham,
    "dem_so": tpl_dem_so,
    "so_sanh": tpl_so_sanh,
    "code": tpl_code,
    "quy_trinh": tpl_quy_trinh,
    "anh_dong": tpl_anh_dong,
    "outro": tpl_outro,
}

TEMPLATE_DESCRIPTIONS = {
    "intro": "Mở đầu động (vòng sáng quỹ đạo, thẻ nội dung trượt, nhân vật An chào)",
    "va_cham": "Minh họa xung đột 2 luồng dữ liệu, tia năng lượng & cảnh báo",
    "dem_so": "Bảng chỉ số đếm tăng dần + thanh tiến độ động (kèm ảnh tùy chọn)",
    "so_sanh": "So sánh Trước vs Sau trực quan với tia chuyển đổi ở giữa",
    "code": "Cửa sổ Terminal/Code gõ từng dòng + khung sáng highlight trượt",
    "quy_trinh": "Sơ đồ các bước nối dây phát sáng theo nhịp lời giảng",
    "anh_dong": "Trình diễn 1–3 ảnh img/ với chuyển động Ken Burns zoom/pan + chú thích",
    "outro": "Tổng kết 3 ý cốt lõi + hiệu ứng thương hiệu AN TECH ACADEMY",
}


def render_frame(cfg, theme, scene, lt, scene_dur, f_global, total_frames, active_cue_sub, cue_lt, talking):
    """Vẽ 1 khung hình RGB 1920x1080 hoàn chỉnh."""
    img = get_bg_gradient(theme)
    draw_ambient_motion(img, theme, f_global)

    fn = TEMPLATE_DISPATCH.get(scene["template"], tpl_quy_trinh)
    fn(img, cfg, theme, scene, lt, scene_dur, f_global / float(cfg["video"]["fps"]), talking)

    draw_header(img, cfg, theme, scene["tag"], f_global / max(1, total_frames - 1))
    draw_subtitle_bar(img, cfg, theme, active_cue_sub, cue_lt)
    return img.convert("RGB")
