import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "D:/Edit/Baigiang_CacchuyennganhIT"
FULL = ROOT + "/mau/full"
FR = FULL + "/frames"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
W, H, FPS = 1920, 1080, 30
BG = (248, 250, 252, 255)
INK = (15, 23, 42, 255)
MUT = (71, 85, 105, 255)
WHITE = (255, 255, 255, 255)
LINE = (203, 213, 225, 255)
GREEN = (21, 128, 61, 255)

sys.path.insert(0, ROOT + "/tools")
from prep_icons import icon_rgba

def hx(c):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)

# accent per major (fill / text-safe)
ACC = {
    "cnpm": ("#2563EB", "#2563EB"),
    "ai":   ("#7C3AED", "#7C3AED"),
    "attt": ("#DC2626", "#DC2626"),
    "httt": ("#D97706", "#B45309"),
    "mang": ("#0284C7", "#0369A1"),
    "game": ("#0D9488", "#0F766E"),
    "neutral": ("#475569", "#475569"),
}

def font(path, size, weight=None):
    f = ImageFont.truetype(ROOT + "/assets/fonts/" + path, size)
    if weight:
        f.set_variation_by_axes([weight])
    return f

F_KICK = font("BeVietnamPro-SemiBold.ttf", 28)
F_HEAD = font("PlusJakartaSans-var.ttf", 48, 700)
F_HEAD56 = font("PlusJakartaSans-var.ttf", 56, 700)
F_LBL = font("BeVietnamPro-SemiBold.ttf", 32)
F_LBL30 = font("BeVietnamPro-SemiBold.ttf", 30)
F_SUB = font("BeVietnamPro-Regular.ttf", 28)
F_CHIP = font("BeVietnamPro-SemiBold.ttf", 28)
F_SUBT = font("BeVietnamPro-Medium.ttf", 32)
F_NUM = font("PlusJakartaSans-var.ttf", 44, 700)
F_WORD = font("PlusJakartaSans-var.ttf", 72, 700)
F_TAG = font("BeVietnamPro-Regular.ttf", 32)
F_PHONE = font("BeVietnamPro-SemiBold.ttf", 28)
F_BIG = font("PlusJakartaSans-var.ttf", 44, 700)
F_COUNT = font("PlusJakartaSans-var.ttf", 64, 700)

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3

def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)

# ---------- timeline ----------
def load_timeline(dry=False):
    manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    state = {} if dry else json.load(open(FULL + "/tts_state.json", encoding="utf-8"))
    scenes = {}
    for c in manifest:
        scenes.setdefault(c["scene"], []).append(c)
    GAP = 0.25
    TAIL = 1.5
    tl = {}
    for sid, cues in scenes.items():
        starts, durs = [], []
        t = 0.0
        for i, c in enumerate(cues):
            d = 3.5 if dry else state[c["id"]]["dur"]
            if i > 0:
                t += GAP
                prev = cues[i - 1]
                # S30: 3s pause belongs BEFORE c3 (the answer), i.e. after the question
                if c["id"] == "S30c3":
                    t += 3.0
                else:
                    t += prev["pause_after"] if prev["id"] != "S30c3" else 0.0
            starts.append(t)
            durs.append(d)
            t += d
        total = t + TAIL
        tl[sid] = {"cues": cues, "starts": starts, "durs": durs, "total": total,
                   "gap": GAP, "tail": TAIL}
    return tl

def cue_t(tl, sid, n, frac=0.0):
    s = tl[sid]
    return s["starts"][n - 1] + frac * s["durs"][n - 1]

# ---------- primitives (return RGBA sprites) ----------
def card_base(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w, h], 16, fill=(15, 23, 42, 20))
    d.rounded_rectangle([0, 0, w, h - 6], 16, fill=WHITE)
    return im

def sp_icon_card(icon, label, sub, accent, w=420, h=420, icon_size=140):
    im = card_base(w, h)
    ic = icon_rgba(icon, accent).resize((icon_size, icon_size), Image.LANCZOS)
    im.paste(ic, ((w - icon_size) // 2, 30), ic)
    d = ImageDraw.Draw(im)
    d.text((w / 2, h - 110), label, font=F_LBL, fill=INK, anchor="mm")
    if sub:
        d.text((w / 2, h - 64), sub, font=F_SUB, fill=MUT, anchor="mm")
    return im

def sp_chip(text, accent, txt=None):
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = tmp.textlength(text, font=F_CHIP)
    pw, ph = int(tw + 56), 62
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw, ph], 31, fill=WHITE, outline=hx(accent), width=2)
    d.text((pw / 2, ph / 2), text, font=F_CHIP, fill=hx(txt or accent), anchor="mm")
    return im

def sp_node(number, label, accent, r=52):
    s = r * 2 + 8
    im = Image.new("RGBA", (s, s + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([4, 4, 4 + r * 2, 4 + r * 2], fill=hx(accent))
    d.text((4 + r, 4 + r), str(number), font=F_NUM, fill=WHITE, anchor="mm")
    if label:
        d.text((s / 2, s + 28), label, font=F_LBL30, fill=INK, anchor="mm")
    return im

def sp_check(text, accent, w=760):
    im = Image.new("RGBA", (w, 64), (0, 0, 0, 0))
    ic = icon_rgba("check-circle", "#15803D").resize((44, 44), Image.LANCZOS)
    im.paste(ic, (0, 10), ic)
    d = ImageDraw.Draw(im)
    d.text((64, 32), text, font=F_LBL30, fill=INK, anchor="lm")
    return im

def sp_bullet(icon, text, accent, w=820):
    im = Image.new("RGBA", (w, 72), (0, 0, 0, 0))
    ic = icon_rgba(icon, accent).resize((52, 52), Image.LANCZOS)
    im.paste(ic, (0, 10), ic)
    d = ImageDraw.Draw(im)
    d.text((76, 36), text, font=F_LBL, fill=INK, anchor="lm")
    return im

def sp_text(text, fnt, color):
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(tmp.textlength(text, font=fnt)) + 8
    th = fnt.size + 16
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((4, th / 2), text, font=fnt, fill=hx(color) if isinstance(color, str) else color, anchor="lm")
    return im

def sp_icon_only(icon, accent, size=140):
    return icon_rgba(icon, accent).resize((size, size), Image.LANCZOS)

def sp_icon_label(icon, label, accent, w=220, icon_size=100, label_font=None):
    lf = label_font or F_SUB
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    w = max(w, int(tmp.textlength(label, font=lf)) + 24)
    im = Image.new("RGBA", (w, icon_size + 60), (0, 0, 0, 0))
    ic = icon_rgba(icon, accent).resize((icon_size, icon_size), Image.LANCZOS)
    im.paste(ic, ((w - icon_size) // 2, 0), ic)
    d = ImageDraw.Draw(im)
    d.text((w / 2, icon_size + 28), label, font=lf, fill=INK, anchor="mm")
    return im

def sp_card_bg(w, h):
    return card_base(w, h)

def sp_major_node(number, label, color, w=660):
    im = Image.new("RGBA", (w, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = 36
    d.ellipse([0, 6, r * 2, 6 + r * 2], fill=hx(color))
    d.text((r, 6 + r), str(number), font=F_NUM, fill=WHITE, anchor="mm")
    d.text((r * 2 + 28, 42), label, font=F_LBL30, fill=INK, anchor="lm")
    return im

def sp_panel(title, icon, sub, accent, w=560, h=420):
    im = card_base(w, h)
    d = ImageDraw.Draw(im)
    d.text((w / 2, 56), title, font=F_LBL, fill=hx(accent), anchor="mm")
    ic = icon_rgba(icon, accent).resize((150, 150), Image.LANCZOS)
    im.paste(ic, ((w - 150) // 2, 100), ic)
    if sub:
        d.text((w / 2, h - 70), sub, font=F_SUB, fill=MUT, anchor="mm")
    return im

def sp_wordmark():
    im = Image.new("RGBA", (1400, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((700, 70), "AN TECH ACADEMY", font=F_WORD, fill=INK, anchor="mm")
    d.rounded_rectangle([480, 130, 920, 138], 4, fill=hx("#2563EB"))
    d.text((700, 180), "Học công nghệ, làm chủ tương lai", font=F_TAG, fill=MUT, anchor="mm")
    return im

def sp_phone(accent, title="Gợi ý cho bạn"):
    im = Image.new("RGBA", (300, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 290, 510], 36, fill=INK)
    d.rounded_rectangle([24, 24, 276, 496], 24, fill=WHITE)
    d.text((150, 60), title, font=F_PHONE, fill=hx(accent), anchor="mm")
    for y0 in (90, 230, 370):
        d.rounded_rectangle([40, y0, 260, y0 + 110], 12, fill=(241, 245, 249, 255))
        d.rounded_rectangle([54, y0 + 16, 110, y0 + 72], 10, fill=hx(accent))
        d.rounded_rectangle([124, y0 + 22, 244, y0 + 32], 5, fill=(148, 163, 184, 255))
        d.rounded_rectangle([124, y0 + 44, 224, y0 + 54], 5, fill=(203, 213, 225, 255))
        d.rounded_rectangle([54, y0 + 84, 244, y0 + 94], 5, fill=(203, 213, 225, 255))
    return im

# ---------- compositing ----------
def paste_sprite(base, im, x, y, p, anchor="tl"):
    if p <= 0:
        return
    w0, h0 = im.size
    if anchor == "mm":
        x -= w0 / 2; y -= h0 / 2
    s = 0.9 + 0.1 * p
    w, h = int(w0 * s), int(h0 * s)
    r = im.resize((w, h), Image.LANCZOS) if s < 1 else im
    if p < 1:
        r = r.copy()
        r.putalpha(r.getchannel("A").point(lambda a: int(a * p)))
    base.paste(r, (int(x + (w0 - w) / 2), int(y + (h0 - h) / 2)), r)

def draw_conn(d, x0, y0, x1, y1, p, color, dotq=None, width=6):
    if p <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    head = 18
    frac = max(0.0, (L - head) / L) * p
    xe, ye = x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac
    d.line([x0, y0, xe, ye], fill=color, width=width)
    if p > 0.95:
        ang = math.atan2(y1 - y0, x1 - x0)
        p1 = (x1 - head * math.cos(ang - 0.4), y1 - head * math.sin(ang - 0.4))
        p2 = (x1 - head * math.cos(ang + 0.4), y1 - head * math.sin(ang + 0.4))
        d.polygon([(x1, y1), p1, p2], fill=color)
    if dotq is not None:
        dq = dotq * frac
        dx, dy = x0 + (x1 - x0) * dq, y0 + (y1 - y0) * dq
        d.ellipse([dx - 9, dy - 9, dx + 9, dy + 9], fill=color)

def subtitle_band(d, lines, dark=False):
    bw = max(d.textlength(l, font=F_SUBT) for l in lines) + 80
    bh = 24 + 44 * len(lines)
    x0, y0 = (W - bw) / 2, 1026 - bh
    fill = (30, 41, 59, 255) if dark else (15, 23, 42, 255)
    d.rounded_rectangle([x0, y0, x0 + bw, 1026], 12, fill=fill)
    for j, l in enumerate(lines):
        d.text((W / 2, y0 + 12 + 22 + j * 44), l, font=F_SUBT, fill=WHITE, anchor="mm")

def heading(base, d, kicker, title, accent, p, title_font=None):
    if p <= 0:
        return base
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    dy = int(14 * (1 - p))
    if kicker:
        od.text((96, 70 + dy), kicker, font=F_KICK, fill=hx(accent))
    if title:
        od.text((96, 112 + dy), title, font=title_font or F_HEAD, fill=INK)
    ov.putalpha(ov.getchannel("A").point(lambda a: int(a * p)))
    return Image.alpha_composite(base, ov)