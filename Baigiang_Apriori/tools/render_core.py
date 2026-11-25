# -*- coding: utf-8 -*-
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "D:/Edit/Baigiang_Apriori"
FULL = ROOT + "/mau/full"
FR = FULL + "/frames"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
W, H, FPS = 1920, 1080, 30

BG      = (234, 241, 249, 255)
NAVY    = (11, 42, 91, 255)
BLUE    = (47, 111, 208, 255)
BLUE_D  = (31, 78, 150, 255)
ICE     = (217, 231, 247, 255)
ICE_2   = (240, 246, 253, 255)
BORDER  = (205, 222, 242, 255)
AMBER   = (245, 196, 94, 255)
CREAM   = (252, 239, 210, 255)
INK     = (14, 27, 51, 255)
MUT     = (74, 91, 114, 255)
WHITE   = (255, 255, 255, 255)
GREEN   = (31, 138, 76, 255)
RED     = (192, 57, 43, 255)
CODE_BG = (11, 27, 51, 255)
CODE_HL = (18, 58, 110, 255)

sys.path.insert(0, ROOT + "/tools")
from prep_icons import icon_rgba

def hx(c):
    c = c.lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), 255)

def font(path, size, weight=None):
    f = ImageFont.truetype(ROOT + "/assets/fonts/" + path, size)
    if weight:
        f.set_variation_by_axes([weight])
    return f

F_BRAND = font("BeVietnamPro-SemiBold.ttf", 21)
F_BANNER = font("PlusJakartaSans-var.ttf", 54, 800)
F_BSUB  = font("BeVietnamPro-Medium.ttf", 29)
F_H2    = font("BeVietnamPro-SemiBold.ttf", 34)
F_BODY  = font("BeVietnamPro-Regular.ttf", 30)
F_BODY_M= font("BeVietnamPro-Medium.ttf", 30)
F_SM    = font("BeVietnamPro-Regular.ttf", 26)
F_SM_M  = font("BeVietnamPro-Medium.ttf", 26)
F_LBL   = font("BeVietnamPro-SemiBold.ttf", 24)
F_NUM   = font("PlusJakartaSans-var.ttf", 58, 800)
F_NUM_S = font("PlusJakartaSans-var.ttf", 42, 700)
F_FORM  = font("BeVietnamPro-SemiBold.ttf", 38)
F_CODE  = font("JetBrainsMono-var.ttf", 23)
F_CODE_T= font("JetBrainsMono-var.ttf", 22)
F_SUB   = font("BeVietnamPro-Medium.ttf", 30)
F_WM    = font("PlusJakartaSans-var.ttf", 78, 800)

PRODUCTS = {
    "Sữa":       ("milk",      "#2F6FD0"),
    "Bánh mì":   ("sandwich",  "#B45309"),
    "Trứng":     ("egg",       "#D97706"),
    "Bơ":        ("package",   "#0F766E"),
}

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3

def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)

# ---------- timeline ----------
def load_timeline(dry=False, sids=None):
    manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
    state = {} if dry else json.load(open(FULL + "/tts_state.json", encoding="utf-8"))
    scenes = {}
    for c in manifest:
        scenes.setdefault(c["scene"], []).append(c)
    GAP, TAIL = 0.22, 1.10
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

# ---------- text helpers ----------
_meas = ImageDraw.Draw(Image.new("RGBA", (8, 8)))

def tw(text, f):
    return _meas.textlength(text, font=f)

def draw_tracked(d, xy, text, f, fill, tracking=2):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x

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

# ---------- background ----------
def bg_canvas(dark=False):
    base = Image.new("RGBA", (W, H), NAVY if dark else BG)
    d = ImageDraw.Draw(base)
    if not dark:
        d.ellipse([-260, 600, 520, 1380], fill=(223, 234, 247, 255))
        d.ellipse([1480, -300, 2260, 480], fill=(226, 237, 249, 255))
        d.ellipse([1560, 760, 2120, 1320], fill=(228, 238, 249, 255))
    return base

def brand_mark(base):
    d = ImageDraw.Draw(base)
    draw_tracked(d, (96, 38), "AN TECH ACADEMY", F_BRAND, NAVY, 3.2)
    return base

# ---------- primitives ----------
def card(w, h, fill=WHITE, outline=BORDER, radius=18, shadow=True, ow=2):
    pad = 10 if shadow else 0
    im = Image.new("RGBA", (w + pad, h + pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        d.rounded_rectangle([0, 7, w, h + 5], radius, fill=(11, 42, 91, 26))
    d.rounded_rectangle([0, 0, w, h], radius, fill=fill,
                        outline=outline if outline else None, width=ow if outline else 0)
    return im

def sp_text(text, f, color, pad=6):
    w_ = int(rich_width(text, f)) + pad * 2
    h_ = f.size + 20
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    draw_rich(d, (pad, h_ / 2), text, f, color, "lm")
    return im

def col_hex(c):
    return c if isinstance(c, str) else "#%02X%02X%02X" % c[:3]

# Be Vietnam Pro thiếu một số glyph; rơi về Plus Jakarta Sans theo từng ký tự.
_MISS = set("→↔∪✓✕")
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

def sp_chip(text, color=BLUE, fill=WHITE, size=26, icon=None):
    f = font("BeVietnamPro-SemiBold.ttf", size)
    iw = 34 if icon else 0
    w_ = int(tw(text, f)) + 46 + iw
    h_ = 54
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w_ - 1, h_ - 1], 27, fill=fill, outline=color, width=2)
    x = 24
    if icon:
        ic = icon_rgba(icon, col_hex(color)).resize((26, 26), Image.LANCZOS)
        im.paste(ic, (x, 14), ic)
        x += iw
    draw_rich(d, (x, h_ / 2), text, f, color, "lm")
    return im

def sp_icon(icon, color, size=64):
    return icon_rgba(icon, col_hex(color)).resize((size, size), Image.LANCZOS)

def sp_icon_label(icon, label, color=BLUE, size=64, f=None):
    f = f or F_BODY_M
    w_ = max(int(tw(label, f)) + 20, size + 10)
    im = Image.new("RGBA", (w_, size + 46), (0, 0, 0, 0))
    ic = sp_icon(icon, color, size)
    im.paste(ic, ((w_ - size) // 2, 0), ic)
    d = ImageDraw.Draw(im)
    draw_rich(d, (w_ / 2, size + 24), label, f, INK, "mm")
    return im

def sp_check(text, color=GREEN, w=760, f=None):
    f = f or F_BODY_M
    im = Image.new("RGBA", (w, 60), (0, 0, 0, 0))
    ic = sp_icon("circle-check", color, 40)
    im.paste(ic, (0, 10), ic)
    d = ImageDraw.Draw(im)
    draw_rich(d, (58, 30), text, f, INK, "lm")
    return im

def sp_bullet(icon, text, color=BLUE, w=760, f=None):
    f = f or F_BODY_M
    im = Image.new("RGBA", (w, 60), (0, 0, 0, 0))
    ic = sp_icon(icon, color, 38)
    im.paste(ic, (0, 11), ic)
    d = ImageDraw.Draw(im)
    draw_rich(d, (56, 30), text, f, INK, "lm")
    return im

def sp_items(items, size=24, f=None, dot=True):
    f = f or F_SM_M
    parts = []
    for it in items:
        icon, col = PRODUCTS.get(it, ("package", "#4A5B72"))
        parts.append((it, icon, hx(col)))
    w_ = 0
    for it, _, _ in parts:
        w_ += size + 8 + tw(it, f) + 26
    im = Image.new("RGBA", (int(w_) + 6, size + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 0
    for it, icon, col in parts:
        ic = icon_rgba(icon, "#%02X%02X%02X" % col[:3]).resize((size, size), Image.LANCZOS)
        im.paste(ic, (int(x), 6), ic)
        x += size + 8
        d.text((x, (size + 14) / 2), it, font=f, fill=INK, anchor="lm")
        x += tw(it, f) + 26
    return im

def sp_banner(title, sub, accent=BLUE):
    t1 = F_BANNER
    t2 = F_BSUB
    w1 = rich_width(title, t1) + 150
    w2 = rich_width(sub, t2) + 110 if sub else 0
    w_ = int(max(w1, w2, 820))
    h_ = 158 if sub else 118
    im = Image.new("RGBA", (w_, h_ + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w_, h_ + 4], 30, fill=(11, 42, 91, 30))
    d.rounded_rectangle([0, 0, w_, h_], 30, fill=NAVY)
    d.rounded_rectangle([w_ / 2 - 90, h_ - 10, w_ / 2 + 90, h_ - 5], 3, fill=AMBER)
    draw_rich(d, (w_ / 2, 58 if sub else h_ / 2), title, t1, WHITE, "mm")
    if sub:
        draw_rich(d, (w_ / 2, 116), sub, t2, (249, 226, 175, 255), "mm")
    return im

def sp_table_frame(w, header_h, cols, headers, nrows, row_h):
    h_ = header_h + row_h * nrows
    im = card(w, h_)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, header_h], 18, fill=NAVY)
    d.rectangle([0, header_h - 22, w, header_h], fill=NAVY)
    x = 0
    for i, hd in enumerate(headers):
        cw = cols[i]
        d.text((x + 22, header_h / 2), hd, font=F_LBL, fill=(214, 229, 247, 255), anchor="lm")
        x += cw
    return im

def sp_row(w, cols, cells, row_h, row_i, status="", items_col=None, bar_col=None,
           fs=26, max_bar=100):
    bg = ICE_2 if row_i % 2 else WHITE
    if status == "hl":
        bg = ICE
    im = Image.new("RGBA", (w, row_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, row_h - 1], fill=bg)
    d.line([0, row_h - 1, w, row_h - 1], fill=BORDER, width=1)
    x = 0
    for i, cw in enumerate(cols):
        val = cells[i] if i < len(cells) else ""
        col = INK
        if status == "no":
            col = (140, 154, 173, 255)
        if i == items_col and val:
            its = [v.strip() for v in val.split(",") if v.strip()]
            sp = sp_items(its, size=23, f=font("BeVietnamPro-Medium.ttf", fs - 2))
            im.paste(sp, (int(x + 18), int((row_h - sp.size[1]) / 2) + 1), sp)
        elif i == bar_col and val:
            pct = float(val.replace("%", "").replace(",", "."))
            track_w = cw - 120
            d.rounded_rectangle([x + 20, row_h / 2 - 7, x + 20 + track_w, row_h / 2 + 7],
                                7, fill=(226, 235, 247, 255))
            fillc = GREEN if status == "ok" else (BLUE if status == "" else (154, 167, 186, 255))
            if status == "no":
                fillc = (198, 120, 110, 255)
            d.rounded_rectangle([x + 20, row_h / 2 - 7, x + 20 + max(14, track_w * pct / max_bar),
                                 row_h / 2 + 7], 7, fill=fillc)
            d.text((x + cw - 18, row_h / 2), val, font=font("PlusJakartaSans-var.ttf", 26, 700),
                   fill=(GREEN if status == "ok" else (MUT if status == "no" else BLUE)), anchor="rm")
        else:
            f = font("BeVietnamPro-SemiBold.ttf", fs) if i == 0 else font("BeVietnamPro-Medium.ttf", fs)
            d.text((x + 22, row_h / 2), val, font=f, fill=col, anchor="lm")
            if status == "no" and i == 0:
                pass
        x += cw
    if status == "no":
        draw_rich(d, (w - 26, row_h / 2), "✕", font("BeVietnamPro-Bold.ttf", 24), RED, "rm")
    if status == "ok":
        draw_rich(d, (w - 26, row_h / 2), "✓", font("BeVietnamPro-Bold.ttf", 24), GREEN, "rm")
    return im

def sp_bars(title, items, w=740, label_w=210, row_h=84):
    im = card(w, 84 + row_h * len(items))
    d = ImageDraw.Draw(im)
    d.text((30, 40), title, font=F_LBL, fill=hx("#4A5B72"), anchor="lm")
    for i, it in enumerate(items):
        y = 84 + i * row_h + row_h / 2
        d.text((30, y), it["label"], font=F_BODY_M, fill=INK, anchor="lm")
        tx0 = 30 + label_w
        tx1 = w - 92
        d.rounded_rectangle([tx0, y - 9, tx1, y + 9], 9, fill=(226, 235, 247, 255))
        pct = it.get("pct", 0)
        col = it.get("color", "#2F6FD0")
        d.rounded_rectangle([tx0, y - 9, tx0 + max(10, (tx1 - tx0) * pct / 100), y + 9], 9, fill=hx(col))
        d.text((w - 26, y), f"{pct:g}%", font=font("PlusJakartaSans-var.ttf", 30, 800),
               fill=hx(col), anchor="rm")
    return im

def sp_bars_dyn(items, w=740, label_w=210, row_h=84, x0=0, y0=84):
    """thanh chạy dần: trả về hàm vẽ theo p tiến trình"""
    def fn(prog_list):
        im = Image.new("RGBA", (w, row_h * len(items)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        for i, (it, pg) in enumerate(zip(items, prog_list)):
            y = i * row_h + row_h / 2
            d.text((30, y), it["label"], font=F_BODY_M, fill=INK, anchor="lm")
            tx0, tx1 = 30 + label_w, w - 92
            d.rounded_rectangle([tx0, y - 9, tx1, y + 9], 9, fill=(226, 235, 247, 255))
            pct = it.get("pct", 0) * max(0.0, min(1.0, pg))
            col = it.get("color", "#2F6FD0")
            d.rounded_rectangle([tx0, y - 9, tx0 + max(10, (tx1 - tx0) * pct / 100), y + 9], 9, fill=hx(col))
            d.text((w - 26, y), f"{round(pct):g}%", font=font("PlusJakartaSans-var.ttf", 30, 800),
                   fill=hx(col), anchor="rm")
        return im
    return fn

def sp_step(number, title, sub, w=380, h=250, color=BLUE, icon=None):
    im = card(w, h, fill=ICE_2, outline=BORDER)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, 8], 4, fill=hx("#2F6FD0"))
    d.ellipse([26, 30, 92, 96], fill=NAVY)
    d.text((59, 63), str(number), font=font("PlusJakartaSans-var.ttf", 34, 800), fill=WHITE, anchor="mm")
    ty = 130
    for ln in wrap(title, F_H2, w - 60)[:2]:
        draw_rich(d, (30, ty), ln, F_H2, INK, "lm")
        ty += 42
    if sub:
        for ln in wrap(sub, F_SM, w - 60)[:2]:
            draw_rich(d, (30, ty + 6), ln, F_SM, MUT, "lm")
            ty += 34
    return im

def sp_rule(left, right, conf=None, lift=None, w=760, h=170):
    im = card(w, h, fill=CREAM, outline=(240, 214, 160, 255))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 8, h], 4, fill=AMBER)
    f = font("BeVietnamPro-SemiBold.ttf", 32)
    x = 40
    li = sp_items(left, size=26, f=f)
    im.paste(li, (x, 36), li)
    x += li.size[0] + 18
    draw_rich(d, (x, 36 + li.size[1] / 2), "→", font("BeVietnamPro-SemiBold.ttf", 34), BLUE_D, "lm")
    x += 52
    ri = sp_items(right, size=26, f=f)
    im.paste(ri, (x, 36), ri)
    if conf:
        d.text((40, h - 34), f"Confidence {conf}", font=font("BeVietnamPro-SemiBold.ttf", 26), fill=NAVY, anchor="lm")
    if lift:
        d.text((w - 40, h - 34), f"Lift {lift}", font=font("BeVietnamPro-SemiBold.ttf", 26), fill=(122, 78, 0, 255), anchor="rm")
    return im

def sp_callout(icon, title, lines, w=800, h=150, tone="amber"):
    fill = CREAM if tone == "amber" else ICE_2
    outline = (240, 214, 160, 255) if tone == "amber" else BORDER
    im = card(w, h, fill=fill, outline=outline)
    d = ImageDraw.Draw(im)
    ic = sp_icon(icon, (122, 78, 0) if tone == "amber" else BLUE, 56)
    im.paste(ic, (28, 26 if not lines else 30), ic)
    draw_rich(d, (104, 42 if lines else h / 2), title, F_H2, NAVY, "lm")
    yy = 82
    for ln in lines[:2]:
        draw_rich(d, (104, yy), ln, F_SM, (112, 84, 35, 255) if tone == "amber" else MUT, "lm")
        yy += 34
    return im

def sp_stat(value, label, color=BLUE, w=360, h=170, note=None):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    draw_rich(d, (30, 62), value, font("PlusJakartaSans-var.ttf", 62, 800), color, "lm")
    draw_rich(d, (30, 124), label, F_BODY_M, INK, "lm")
    if note:
        d.text((w - 26, 34), note, font=F_LBL, fill=AMBER, anchor="rm")
    return im

# ---- code panel ----
_TOK = re.compile(r"(#[^\n]*)|(\"[^\"]*\"|'[^']*')|(\b(?:import|from|def|for|if|in|return|lambda|await|async|const|print)\b)|(\b\d+\.?\d*\b)")

def hl_line(text):
    out, pos = [], 0
    col_kw = (127, 179, 255, 255)
    col_str = (245, 196, 94, 255)
    col_num = (143, 214, 168, 255)
    col_com = (124, 140, 166, 255)
    base = (220, 231, 245, 255)
    for m in _TOK.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], base))
        s = m.group(0)
        if m.group(1):
            out.append((s, col_com))
        elif m.group(2):
            out.append((s, col_str))
        elif m.group(3):
            out.append((s, col_kw))
        else:
            out.append((s, col_num))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], base))
    return out

def sp_code(lines, w, h, title="main.py"):
    im = Image.new("RGBA", (w, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 8, w, h + 6], 18, fill=(0, 0, 0, 40))
    d.rounded_rectangle([0, 0, w, h], 18, fill=CODE_BG)
    d.rounded_rectangle([0, 0, w, 56], 18, fill=(16, 38, 74, 255))
    d.rectangle([0, 38, w, 56], fill=(16, 38, 74, 255))
    for i, c in enumerate([(255, 107, 107), (245, 196, 94), (98, 199, 132)]):
        d.ellipse([22 + i * 26, 21, 36 + i * 26, 35], fill=c + (255,))
    d.text((120, 28), title, font=F_CODE_T, fill=(168, 187, 214, 255), anchor="lm")
    return im

def sp_code_line(text, hl=False, num=None, width=1050):
    im = Image.new("RGBA", (width, 34), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if hl:
        d.rectangle([0, 0, width, 33], fill=CODE_HL)
    if num is not None:
        d.text((62, 17), str(num), font=font("JetBrainsMono-var.ttf", 18), fill=(96, 118, 148, 255), anchor="rm")
    x = 82
    for s, col in hl_line(text):
        d.text((x, 17), s, font=F_CODE, fill=col, anchor="lm")
        x += tw(s, F_CODE)
    return im

# ---- browser mock ----
def sp_browser(w=760, h=520, state=False):
    im = card(w, h, fill=WHITE)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, 52], 18, fill=(240, 246, 253, 255))
    d.rectangle([0, 34, w, 52], fill=(240, 246, 253, 255))
    for i, c in enumerate([(226, 116, 106), (235, 190, 110), (140, 200, 160)]):
        d.ellipse([22 + i * 24, 18, 34 + i * 24, 30], fill=c + (255,))
    d.rounded_rectangle([110, 14, w - 30, 40], 13, fill=WHITE)
    d.text((128, 27), "shop.example.vn/san-pham/banh-mi", font=font("BeVietnamPro-Regular.ttf", 20),
           fill=(120, 136, 160, 255), anchor="lm")
    d.text((36, 92), "Bánh mì", font=font("PlusJakartaSans-var.ttf", 40, 800), fill=INK, anchor="lm")
    d.rounded_rectangle([36, 130, 236, 240], 14, fill=ICE)
    ic = sp_icon("sandwich", (180, 83, 9), 72)
    im.paste(ic, (100, 148), ic)
    d.text((36, 268), "35.000 đ", font=font("PlusJakartaSans-var.ttf", 30, 800), fill=BLUE, anchor="lm")
    d.rounded_rectangle([36, 300, 236, 352], 12, fill=NAVY)
    d.text((136, 326), "Thêm vào giỏ", font=font("BeVietnamPro-SemiBold.ttf", 24), fill=WHITE, anchor="mm")
    d.text((300, 300), "Mô tả sản phẩm", font=F_SM, fill=MUT, anchor="lm")
    for i in range(3):
        d.rounded_rectangle([300, 330 + i * 22, w - 40 - i * 40, 340 + i * 22], 5, fill=(226, 235, 247, 255))
    if state:
        d.rounded_rectangle([290, 392, w - 24, 486], 14, fill=CREAM, outline=(240, 214, 160, 255), width=2)
        d.text((310, 418), "Có thể bạn thích", font=font("BeVietnamPro-SemiBold.ttf", 20), fill=(122, 78, 0, 255), anchor="lm")
        sp = sp_items(["Sữa"], size=24, f=font("BeVietnamPro-SemiBold.ttf", 22))
        im.paste(sp, (310, 440), sp)
    return im

# ---------- compositing ----------
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
    w, h = int(w0 * s), int(h0 * s)
    r = im.resize((w, h), Image.LANCZOS) if s < 1 else im
    if p < 1:
        r = r.copy()
        r.putalpha(r.getchannel("A").point(lambda a: int(a * p)))
    base.paste(r, (int(x + (w0 - w) / 2), int(y + (h0 - h) / 2)), r)

def draw_conn(d, x0, y0, x1, y1, p, color, dotq=None, width=5):
    if p <= 0:
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
    bh = 18 + 42 * len(lines)
    bw = max(tw(l, F_SUB) for l in lines) + 76
    x0, y0 = (W - bw) / 2, 1028 - bh
    d.rounded_rectangle([x0, y0, x0 + bw, 1028], 12, fill=(11, 42, 91, 240))
    for j, l in enumerate(lines):
        draw_rich(d, (W / 2, y0 + 9 + 21 + j * 42), l, F_SUB, WHITE, "mm")
