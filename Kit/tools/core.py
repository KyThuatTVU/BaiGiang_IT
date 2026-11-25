# -*- coding: utf-8 -*-
"""Core render: palette, fonts, primitives, timeline, hand-drawn strokes."""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.environ.get("PROJECT_ROOT", "D:/Edit/Baigiang_API")
ROOT = PROJECT  # tên cũ, giữ để script đời trước không gãy
FULL = PROJECT + "/mau"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
W, H, FPS = 1920, 1080, 30

BG      = (247, 249, 252, 255)   # F7F9FC
NAVY    = (18, 32, 58, 255)      # 12203A
BLUE    = (47, 107, 255, 255)    # 2F6BFF
BLUE_D  = (29, 78, 216, 255)
TEAL    = (13, 148, 136, 255)    # 0D9488
AMBER   = (245, 165, 36, 255)    # F5A524
AMBER_D = (194, 120, 8, 255)
CREAM   = (254, 243, 199, 255)   # FEF3C7
INK     = (15, 23, 42, 255)
MUT     = (100, 116, 139, 255)
BORDER  = (226, 232, 240, 255)
WHITE   = (255, 255, 255, 255)
GREEN   = (34, 160, 107, 255)
RED     = (229, 72, 77, 255)
ICE     = (239, 246, 255, 255)
ICE_2   = (248, 250, 252, 255)
CODE_BG = (15, 23, 42, 255)

sys.path.insert(0, KIT + "/tools")
from prep_icons import icon_rgba

def hx(c):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)

def font(path, size, weight=None):
    f = ImageFont.truetype(KIT + "/assets/fonts/" + path, size)
    if weight:
        f.set_variation_by_axes([weight])
    return f

F_BRAND  = font("BeVietnamPro-SemiBold.ttf", 22)
F_TITLE  = font("BeVietnamPro-Bold.ttf", 56)
F_H2     = font("BeVietnamPro-SemiBold.ttf", 44)
F_H3     = font("BeVietnamPro-SemiBold.ttf", 34)
F_BODY   = font("BeVietnamPro-Regular.ttf", 30)
F_BODY_M = font("BeVietnamPro-Medium.ttf", 30)
F_SM     = font("BeVietnamPro-Regular.ttf", 26)
F_SM_M   = font("BeVietnamPro-Medium.ttf", 26)
F_LBL    = font("PlusJakartaSans-var.ttf", 24, 600)
F_LBL_B  = font("PlusJakartaSans-var.ttf", 28, 700)
F_NUM    = font("PlusJakartaSans-var.ttf", 58, 800)
F_CODE   = font("JetBrainsMono-var.ttf", 25)
F_SUB    = font("BeVietnamPro-Medium.ttf", 28)
GRID    = (222, 231, 244, 255)

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3

def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)

def lin(t, a, b):
    return max(0.0, min(1.0, (t - a) / (b - a))) if b > a else (1.0 if t >= b else 0.0)

# ---------- timeline ----------
def load_timeline(dry=False, sids=None, sub=None):
    sfx = "" if not sub else "_" + sub
    manifest = json.load(open(FULL + f"/manifest{sfx}.json", encoding="utf-8"))
    state = {} if dry else json.load(open(FULL + f"/tts_state{sfx}.json", encoding="utf-8"))
    scenes = {}
    for c in manifest:
        scenes.setdefault(c["scene"], []).append(c)
    GAP, TAIL = 0.30, 1.00
    tl = {}
    for sid, cues in scenes.items():
        if sids and sid not in sids:
            continue
        starts, durs = [], []
        t = 0.0
        for i, c in enumerate(cues):
            d = 3.6 if dry else state[c["id"]]["dur"]
            if i > 0:
                t += GAP + cues[i - 1].get("pause_after", 0.0)
            starts.append(t)
            durs.append(d)
            t += d
        tl[sid] = {"cues": cues, "starts": starts, "durs": durs,
                   "total": t + TAIL, "gap": GAP, "tail": TAIL}
    return tl

def cue_t(tl, sid, n, frac=0.0):
    s = tl[sid]
    return s["starts"][n - 1] + frac * s["durs"][n - 1]

# ---------- text ----------
_meas = ImageDraw.Draw(Image.new("RGBA", (8, 8)))

def tw(text, f):
    return _meas.textlength(text, font=f)

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, f) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

_MISS = set("→↔∪✓✕≠•")
_FB = {}

def _fb_font(size):
    if size not in _FB:
        _FB[size] = font("PlusJakartaSans-var.ttf", size, 600)
    return _FB[size]

def rich_width(text, f):
    if not any(c in _MISS for c in text):
        return tw(text, f)
    return sum(tw(ch, _fb_font(f.size) if ch in _MISS else f) for ch in text)

def draw_rich(d, xy, text, f, fill, anchor="lm"):
    if not any(c in _MISS for c in text):
        d.text(xy, text, font=f, fill=fill, anchor=anchor)
        return tw(text, f)
    runs = []
    for ch in text:
        fn = _fb_font(f.size) if ch in _MISS else f
        if runs and runs[-1][1] is fn:
            runs[-1][0] += ch
        else:
            runs.append([ch, fn])
    total = sum(tw(s, fn) for s, fn in runs)
    ax, ay = anchor[0], anchor[1:]
    x = xy[0] - total if ax == "r" else (xy[0] - total / 2 if ax == "m" else xy[0])
    for s, fn in runs:
        d.text((x, xy[1]), s, font=fn, fill=fill, anchor="l" + ay)
        x += tw(s, fn)
    return total

def draw_tracked(d, xy, text, f, fill, tracking=2, p=1.0):
    x, y = xy
    n = len(text)
    shown = int(math.ceil(n * max(0.0, min(1.0, p))))
    for i, ch in enumerate(text[:shown]):
        a = 255
        if i == shown - 1 and p < 1.0:
            a = int(255 * (n * p - (shown - 1)))
        d.text((x, y), ch, font=f, fill=fill[:3] + (a,))
        x += d.textlength(ch, font=f) + tracking
    return x

# ---------- background ----------
_BG = None

def bg_canvas():
    global _BG
    if _BG is None:
        base = Image.new("RGBA", (W, H), BG)
        d = ImageDraw.Draw(base)
        for x in range(0, W, 64):
            d.line([x, 0, x, H], fill=GRID[:3] + (105,), width=1)
        for y in range(0, H, 64):
            d.line([0, y, W, y], fill=GRID[:3] + (105,), width=1)
        d.ellipse([-320, 660, 420, 1400], fill=(236, 242, 250, 255))
        d.ellipse([1540, -360, 2320, 420], fill=(238, 244, 252, 255))
        d.ellipse([-180, -280, 300, 220], fill=(242, 246, 252, 255))
        _BG = base
    return _BG.copy()

def brand_mark(base, p=1.0):
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([96, 24, 101, 54], 2, fill=AMBER)
    draw_tracked(d, (114, 37), "AN TECH ACADEMY", F_BRAND, NAVY, 3.2, p)
    if p >= 1.0:
        draw_rich(d, (114, 64), "API & WEB", font("BeVietnamPro-Medium.ttf", 15),
                  MUT, "lm")
    return base

def watermark(base):
    d = ImageDraw.Draw(base)
    draw_tracked(d, (W - 330, 44), "AN TECH ACADEMY", font("BeVietnamPro-SemiBold.ttf", 17),
                 NAVY[:3] + (110,), 2.0)
    return base

# ---------- brand badge ----------
BRAND_DIR = KIT + "/assets/brand"
BRAND_LOGO = BRAND_DIR + "/logo_an_round.png"
_brand_cache = {}

def brand_logo(size, alpha=1.0):
    key = (int(size), round(alpha, 3))
    if key not in _brand_cache:
        im = Image.open(BRAND_LOGO).convert("RGBA").resize((int(size), int(size)), Image.LANCZOS)
        if alpha < 1.0:
            im.putalpha(im.getchannel("A").point(lambda a: int(a * alpha)))
        _brand_cache[key] = im
    return _brand_cache[key]

def paste_brand(base, x, y, size=180, p=1.0, alpha=0.95, anchor="mm"):
    """Dán huy hiệu An Tech, pop + fade theo p (0→1). anchor: mm/mr/bm/br."""
    if p <= 0:
        return
    q = min(1.0, p)
    im = brand_logo(int(size * (0.86 + 0.14 * q)), alpha * q)
    w_, h_ = im.size
    if anchor == "mm":
        x -= w_ / 2; y -= h_ / 2
    elif anchor == "mr":
        x -= w_; y -= h_ / 2
    elif anchor == "bm":
        x -= w_ / 2; y -= h_
    elif anchor == "br":
        x -= w_; y -= h_
    base.alpha_composite(im, (int(x), int(y)))

def brand_watermark(base, size=110, alpha=0.85, pos="tr", margin=28):
    """Dán logo nhỏ cố định một góc khung hình (bản quyền)."""
    im = brand_logo(size, alpha)
    x = W - size - margin if pos in ("tr", "br") else margin
    y = H - size - margin if pos in ("br", "bl") else margin
    base.alpha_composite(im, (x, y))

# ---------- primitives ----------
def card(w, h, fill=WHITE, outline=BORDER, radius=18, shadow=True, ow=2):
    pad = 10 if shadow else 0
    im = Image.new("RGBA", (w + pad, h + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        d.rounded_rectangle([0, 6, w, h + 4], radius, fill=(15, 23, 42, 20))
    d.rounded_rectangle([0, 0, w, h], radius, fill=fill,
                        outline=outline if outline else None, width=ow if outline else 0)
    return im

def col_hex(c):
    return c if isinstance(c, str) else "#%02X%02X%02X" % c[:3]

def sp_icon(icon, color, size=64):
    return icon_rgba(icon, col_hex(color)).resize((size, size), Image.LANCZOS)

def sp_chip(text, color=BLUE, fill=WHITE, size=26, icon=None, h=54):
    f = font("BeVietnamPro-SemiBold.ttf", size)
    iw = 36 if icon else 0
    w_ = int(tw(text, f)) + 46 + iw
    im = Image.new("RGBA", (w_, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w_ - 1, h - 1], h // 2, fill=fill, outline=color, width=2)
    x = 24
    if icon:
        ic = icon_rgba(icon, col_hex(color)).resize((26, 26), Image.LANCZOS)
        im.paste(ic, (x, (h - 26) // 2), ic)
        x += iw
    draw_rich(d, (x, h / 2), text, f, color, "lm")
    return im

def sp_icon_label(icon, label, color=BLUE, size=64, f=None):
    f = f or F_BODY_M
    w_ = max(int(tw(label, f)) + 20, size + 10)
    im = Image.new("RGBA", (w_, size + 46), (0, 0, 0, 0))
    ic = sp_icon(icon, color, size)
    im.paste(ic, ((w_ - size) // 2, 0), ic)
    d = ImageDraw.Draw(im)
    draw_rich(d, (w_ / 2, size + 24), label, f, INK, "mm")
    return im

def sp_title(text, sub=None, accent=AMBER):
    lines = wrap(text, F_H2, 1500)
    h_ = 52 * len(lines) + (44 if sub else 0)
    im = Image.new("RGBA", (1560, h_ + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 0
    for ln in lines:
        draw_rich(d, (0, y + 24), ln, F_H2, NAVY, "lm")
        y += 52
    if sub:
        draw_rich(d, (0, y + 20), sub, F_SM, MUT, "lm")
    d.rounded_rectangle([0, h_ + 4, 120, h_ + 10], 3, fill=accent)
    return im

def paste_sprite(base, im, x, y, p, anchor="tl"):
    if p <= 0:
        return
    w0, h0 = im.size
    if anchor == "mm":
        x -= w0 / 2; y -= h0 / 2
    elif anchor == "mt":
        x -= w0 / 2
    elif anchor == "mr":
        x -= w0; y -= h0 / 2
    s = 0.94 + 0.06 * p
    w, h = max(1, int(w0 * s)), max(1, int(h0 * s))
    r = im.resize((w, h), Image.LANCZOS) if s < 1 else im
    if p < 1:
        r = r.copy()
        r.putalpha(r.getchannel("A").point(lambda a: int(a * p)))
    base.paste(r, (int(x + (w0 - w) / 2), int(y + (h0 - h) / 2)), r)

# ---------- hand-drawn marker strokes ----------
def _wavy_pts(x0, y0, x1, y1, seed=1, amp=2.2, n=26):
    pts = []
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / (L or 1), (x1 - x0) / (L or 1)
    for i in range(n + 1):
        q = i / n
        wob = amp * math.sin(q * 9.0 + seed * 2.1) * math.sin(q * math.pi)
        pts.append((x0 + (x1 - x0) * q + nx * wob, y0 + (y1 - y0) * q + ny * wob))
    return pts

def draw_marker(d, x0, y0, x1, y1, p, color=AMBER, width=6, seed=1):
    """Nét bút marker vẽ dần từ (x0,y0) tới (x1,y1), hơi lượn sóng tự nhiên."""
    if p <= 0:
        return
    pts = _wavy_pts(x0, y0, x1, y1, seed)
    k = max(1, int(len(pts) * min(1.0, p)))
    d.line(pts[:k], fill=color, width=width, joint="curve")
    ex, ey = pts[k - 1]
    d.ellipse([ex - width / 2, ey - width / 2, ex + width / 2, ey + width / 2], fill=color)

def draw_marker_circle(d, cx, cy, rx, ry, p, color=AMBER, width=6, seed=2):
    if p <= 0:
        return
    pts = []
    n = 40
    for i in range(n + 1):
        a = -math.pi / 2 + (i / n) * 2 * math.pi * 1.04
        wob = 2.0 * math.sin(i * 0.9 + seed)
        pts.append((cx + (rx + wob) * math.cos(a), cy + (ry + wob) * math.sin(a)))
    k = max(1, int(len(pts) * min(1.0, p)))
    d.line(pts[:k], fill=color, width=width, joint="curve")

def draw_conn(d, x0, y0, x1, y1, p, color, dotq=None, width=5, hand=False, seed=1):
    if p <= 0:
        return
    if hand:
        draw_marker(d, x0, y0, x1, y1, p, color, width, seed)
        if p > 0.97:
            ang = math.atan2(y1 - y0, x1 - x0)
            hd = 15
            p1 = (x1 - hd * math.cos(ang - 0.42), y1 - hd * math.sin(ang - 0.42))
            p2 = (x1 - hd * math.cos(ang + 0.42), y1 - hd * math.sin(ang + 0.42))
            d.polygon([(x1, y1), p1, p2], fill=color)
        return
    L = math.hypot(x1 - x0, y1 - y0)
    head = 16
    frac = max(0.0, (L - head) / L) * p
    xe, ye = x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac
    d.line([x0, y0, xe, ye], fill=color, width=width)
    if p > 0.95:
        ang = math.atan2(y1 - y0, x1 - x0)
        p1 = (x1 - head * math.cos(ang - 0.42), y1 - head * math.sin(ang - 0.42))
        p2 = (x1 - head * math.cos(ang + 0.42), y1 - head * math.sin(ang + 0.42))
        d.polygon([(x1, y1), p1, p2], fill=color)
    if dotq is not None:
        dq = dotq * frac
        dx, dy = x0 + (x1 - x0) * dq, y0 + (y1 - y0) * dq
        d.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill=color)

def subtitle_band(d, lines):
    if not lines:
        return
    bh = 16 + 38 * len(lines)
    bw = min(1180, max(tw(l, F_SUB) for l in lines) + 72)
    x0, y0 = 96, 1032 - bh
    d.rounded_rectangle([x0, y0, x0 + bw, 1032], 14, fill=NAVY[:3] + (238,))
    d.rounded_rectangle([x0, y0, x0 + 8, 1032], 4, fill=AMBER)
    for j, l in enumerate(lines):
        draw_rich(d, (x0 + 34, y0 + 8 + 19 + j * 38), l, F_SUB, WHITE, "lm")

def subs_for(tl, sid, t, maxw=1100):
    s = tl[sid]
    for j, c in enumerate(s["cues"]):
        st, du = s["starts"][j], s["durs"][j]
        if st <= t < st + du + 0.12:
            lines = []
            for ln in c["subs"]:
                lines += wrap(ln, F_SUB, maxw)
            if len(lines) <= 2:
                return lines
            pages = [lines[i:i + 2] for i in range(0, len(lines), 2)]
            q = max(0.0, min(0.999, (t - st) / du))
            return pages[int(q * len(pages))]
    return []