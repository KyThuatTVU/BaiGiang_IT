# -*- coding: utf-8 -*-
"""Thư viện dựng hình dùng chung cho bản đầy đủ 34 cảnh."""
import json, math, os, re, sys
from PIL import Image, ImageDraw

PROJ = "D:/Edit/Baigiang_dongbodulieu"

sys.path.insert(0, "D:/Edit/Baigiang_Apriori/tools")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import *            # noqa: F401,F403
import render_core as RC
from char_teacher import teacher_sprite, mouth_for

FULL = PROJ + "/mau/full"
AUD = FULL + "/audio"
SFXD = FULL + "/sfx"
SVID = FULL + "/scenes"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

TEAL = (15, 157, 143, 255)
TEAL_D = (10, 122, 112, 255)
GAP, TAIL, XF = 0.22, 1.10, 0.30
SUB_W = 1100
SIDS = [f"S{i:02d}" for i in range(1, 35)]

MAN = json.load(open(PROJ + "/manifest.json", encoding="utf-8"))
_STP = FULL + "/tts_state.json"
STATE = json.load(open(_STP, encoding="utf-8")) if os.path.exists(_STP) else {}
DRY = os.environ.get("FULL_DRY") == "1"

SC, GSTART, TOTAL = {}, {}, 0.0
for sid in SIDS:
    cues = [c for c in MAN if c["scene"] == sid]
    starts, durs, t = [], [], 0.0
    for i, c in enumerate(cues):
        if i:
            t += GAP
        starts.append(t)
        durs.append(3.6 if DRY else STATE[c["id"]]["dur"])
        t += durs[-1]
    SC[sid] = dict(cues=cues, starts=starts, durs=durs, dur=t + TAIL)
    GSTART[sid] = TOTAL
    TOTAL += SC[sid]["dur"] - XF
TOTAL += XF

def speak(t, sid):
    s = SC[sid]
    return any(a <= t < a + d for a, d in zip(s["starts"], s["durs"]))

def phrase_t(sid, cue_i, sub, offset=0.0):
    s = SC[sid]
    text = s["cues"][cue_i]["text"]
    i = text.find(sub)
    if i < 0:
        return s["starts"][cue_i] + offset
    return s["starts"][cue_i] + s["durs"][cue_i] * (i / len(text)) + offset

# ---------------- phụ đề ----------------
def sub_chunks(text):
    units = []
    for part in re.split(r"(?<=[.!?])\s+", text):
        if len(part) <= 90:
            units.append(part)
            continue
        cur = ""
        for s in re.split(r"(?<=,)\s+", part):
            t_ = (cur + " " + s).strip()
            if cur and len(t_) > 90:
                units.append(cur)
                cur = s
            else:
                cur = t_
        if cur:
            units.append(cur)
    chunks, cur = [], ""
    for u in units:
        t_ = (cur + " " + u).strip()
        if cur and (len(t_) > 90 or len(wrap(t_, F_SUB, SUB_W)) > 2):
            chunks.append(cur)
            cur = u
        else:
            cur = t_
    if cur:
        chunks.append(cur)
    if len(chunks) > 1 and len(chunks[-1]) < 25:
        chunks[-1] = chunks[-2] + " " + chunks[-1]
        chunks.pop(-2)
    return [wrap(c, F_SUB, SUB_W) for c in chunks]

SEGS = []
for sid in SIDS:
    s = SC[sid]
    for c, st, du in zip(s["cues"], s["starts"], s["durs"]):
        chunks = sub_chunks(c["text"])
        weights = [sum(len(x) for x in ch) for ch in chunks]
        tot = sum(weights) or 1
        acc = 0
        for ch, w_ in zip(chunks, weights):
            a = st + du * acc / tot
            acc += w_
            b = st + du * acc / tot
            SEGS.append((GSTART[sid] + a, GSTART[sid] + b, ch))

def sub_at(g):
    for a, b, ch in SEGS:
        if a <= g < b:
            return ch
    return None

def sub_band(d, lines):
    bw = max(rich_width(l, F_SUB) for l in lines) + 64
    bh = 16 + 42 * len(lines)
    x1 = 920 + bw / 2
    y1 = 1030
    y0 = y1 - bh
    d.rounded_rectangle([x1 - bw, y0, x1, y1], 12, fill=(11, 42, 91, 238))
    for j, l in enumerate(lines):
        draw_rich(d, (x1 - bw / 2, y0 + 10 + 21 + j * 42), l, F_SUB, WHITE, "mm")

def write_srt(path):
    fmt = lambda s: "%02d:%02d:%02d,%03d" % (int(s // 3600), int(s % 3600 // 60),
                                             int(s % 60), int(round((s % 1) * 1000)) % 1000)
    out = []
    for i, (a, b, ch) in enumerate(SEGS, 1):
        out.append(f"{i}\n{fmt(a)} --> {fmt(b)}\n" + "\n".join(ch) + "\n")
    open(path, "w", encoding="utf-8").write("\n".join(out))

# ---------------- icon bổ sung (Lucide-like, stroke 2) ----------------
def _glyph(name, color, size=64):
    S = size * 3
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = color
    lw = max(3, int(S * 0.075))
    k = S / 24.0
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    def ln(pts, w=lw):
        d.line(P(pts), fill=c, width=w, joint="curve")
    def arc(box, a0, a1, w=lw):
        d.arc([box[0] * k, box[1] * k, box[2] * k, box[3] * k], a0, a1, fill=c, width=w)
    def poly(pts):
        d.polygon(P(pts), fill=c)
    if name == "monitor":
        d.rounded_rectangle([3 * k, 4 * k, 21 * k, 16 * k], 2 * k, outline=c, width=lw)
        ln([(9, 17), (9, 20)]); ln([(15, 17), (15, 20)]); ln([(8, 20), (16, 20)])
    elif name == "laptop":
        d.rounded_rectangle([4 * k, 5 * k, 20 * k, 16 * k], 2 * k, outline=c, width=lw)
        ln([(2, 19), (22, 19)])
    elif name == "wifi":
        arc((2, 6, 22, 24), 200, 340); arc((6, 11, 18, 22), 205, 335); arc((9, 15, 15, 22), 210, 330)
        d.ellipse([10.5 * k, 18.5 * k, 13.5 * k, 21.5 * k], fill=c)
    elif name == "wifi-off":
        arc((2, 6, 22, 24), 200, 340); arc((6, 11, 18, 22), 205, 335)
        d.ellipse([10.5 * k, 18.5 * k, 13.5 * k, 21.5 * k], fill=c)
        ln([(3, 3), (21, 21)], int(lw * 1.1))
    elif name == "zap":
        poly([(13, 2), (4, 14), (11, 14), (10, 22), (20, 10), (13, 10)])
    elif name == "terminal":
        d.rounded_rectangle([2 * k, 4 * k, 22 * k, 20 * k], 2 * k, outline=c, width=lw)
        ln([(6, 9), (9, 12), (6, 15)]); ln([(12, 15), (17, 15)])
    elif name == "users":
        d.ellipse([8 * k, 3 * k, 14 * k, 9 * k], outline=c, width=lw)
        arc((4, 9, 18, 22), 180, 360)
        d.ellipse([15 * k, 5 * k, 19 * k, 9 * k], outline=c, width=lw)
        arc((14, 10, 22, 20), 200, 340)
    elif name == "kanban":
        d.rounded_rectangle([3 * k, 3 * k, 21 * k, 21 * k], 2 * k, outline=c, width=lw)
        ln([(9, 3), (9, 21)]); ln([(15, 3), (15, 21)])
    elif name == "book":
        ln([(3, 5), (3, 20), (11, 20), (12, 18), (13, 20), (21, 20), (21, 5), (13, 5), (12, 8), (11, 5), (3, 5)])
    elif name == "school":
        poly([(12, 3), (2, 8), (12, 13), (22, 8)])
        ln([(6, 10), (6, 16)]); arc((6, 12, 18, 20), 0, 180); ln([(20, 9), (20, 15)])
    elif name == "chat":
        d.rounded_rectangle([3 * k, 4 * k, 21 * k, 17 * k], 4 * k, outline=c, width=lw)
        poly([(7, 16), (6, 21), (12, 17)])
        for x in (8, 12, 16):
            d.ellipse([(x - 0.7) * k, 10 * k, (x + 0.7) * k, 11.4 * k], fill=c)
    elif name == "cursor":
        poly([(5, 3), (5, 18), (9, 14), (12, 21), (14, 20), (11, 13), (17, 13)])
    elif name == "arrow-lr":
        ln([(3, 12), (21, 12)])
        poly([(3, 12), (7, 8), (7, 16)])
        poly([(21, 12), (17, 8), (17, 16)])
    elif name == "layers":
        poly([(12, 3), (21, 8), (12, 13), (3, 8)])
        ln([(3, 12), (12, 17), (21, 12)])
        ln([(3, 16), (12, 21), (21, 16)])
    elif name == "radio":
        d.ellipse([10.5 * k, 10.5 * k, 13.5 * k, 13.5 * k], fill=c)
        arc((6, 6, 18, 18), 200, 340); arc((6, 6, 18, 18), 20, 160)
        arc((2, 2, 22, 22), 200, 340); arc((2, 2, 22, 22), 20, 160)
    elif name == "sparkles":
        poly([(12, 2), (13.6, 8.4), (20, 10), (13.6, 11.6), (12, 18), (10.4, 11.6), (4, 10), (10.4, 8.4)])
    elif name == "pen-line":
        d.polygon(P([(4, 20), (4.8, 15.6), (15.6, 4.8), (19.2, 8.4), (8.4, 19.2)]), fill=c)
        ln([(13, 21), (21, 21)])
    else:
        return RC.sp_icon(name, color, size)
    return im.resize((size, size), Image.LANCZOS)

def ico(name, color, size=64):
    return _glyph(name, color, size)

# ---------------- nhân vật ----------------
def paste_teacher(base, t, pose="D", mouth=None, scale=1.0, cx=1720, feet=1010,
                  fade=(0.30, 0.75), sid=None, small=False):
    if small:
        scale = 0.55
        cx = max(cx, 1770)
    if fade and fade[0] > 0 and t < fade[0]:
        return
    spr = teacher_sprite(t, pose, mouth or "smile")
    if scale != 1.0:
        spr = spr.resize((int(spr.size[0] * scale), int(spr.size[1] * scale)), Image.LANCZOS)
    x = int(cx - spr.size[0] * 0.5)
    y = int(feet - (472 * scale))
    if fade and fade[0] > 0 and t < fade[1]:
        a = seg(t, fade[0], fade[1])
        spr = spr.copy()
        spr.putalpha(spr.getchannel("A").point(lambda v: int(v * a)))
    base.alpha_composite(spr, (x, y))

# ---------------- component ----------------
_BN = {}
def banner(sid, title, sub=None):
    if sid not in _BN:
        _BN[sid] = sp_banner(title, sub)
    return _BN[sid]

def node(icon, title, sub, w, h, tone=BLUE, name=None):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    im.paste(ico(name or icon, tone, 42), (22, 20), ico(name or icon, tone, 42))
    d.text((22, 84), title, font=font("BeVietnamPro-SemiBold.ttf", 23), fill=INK, anchor="lm")
    if sub:
        d.text((22, 114), sub, font=font("BeVietnamPro-Regular.ttf", 17), fill=MUT, anchor="lm")
    return im

def chip(text, color=BLUE, fill=WHITE, size=20, icon=None):
    return sp_chip(text, color, fill, size, icon)

def browser_frame(w, h, url="note.edu.vn/bang-nhom", letter=None, chrome=True):
    im = card(w, h, fill=WHITE)
    d = ImageDraw.Draw(im)
    if chrome:
        d.rounded_rectangle([0, 0, w, 46], 18, fill=(240, 246, 253, 255))
        d.rectangle([0, 28, w, 46], fill=(240, 246, 253, 255))
        for i, c in enumerate([(226, 116, 106), (235, 190, 110), (140, 200, 160)]):
            d.ellipse([18 + i * 22, 17, 28 + i * 22, 27], fill=c + (255,))
        d.rounded_rectangle([86, 12, w - (62 if letter else 18), 36], 12, fill=WHITE)
        d.text((98, 24), url, font=font("BeVietnamPro-Regular.ttf", 16),
               fill=(120, 136, 160, 255), anchor="lm")
        if letter:
            d.ellipse([w - 48, 9, w - 12, 39], fill=NAVY)
            d.text((w - 30, 24), letter, font=font("PlusJakartaSans-var.ttf", 20, 800),
                   fill=WHITE, anchor="mm")
    return im

def browser_note(letter, w=420, h=500, deadline=True, bars=3):
    im = browser_frame(w, h, "note.edu.vn" if w < 360 else "note.edu.vn/bang-nhom", letter=letter)
    d = ImageDraw.Draw(im)
    d.text((34, 82), "Bảng ghi chú nhóm", font=font("BeVietnamPro-SemiBold.ttf", 25), fill=INK, anchor="lm")
    d.text((34, 114), "Ghi chú chung của nhóm", font=font("BeVietnamPro-Regular.ttf", 19), fill=MUT, anchor="lm")
    for i in range(bars):
        d.rounded_rectangle([34, 150 + i * 26, w - 40 - i * 30, 162 + i * 26], 6, fill=(226, 235, 247, 255))
    d.line([30, 244, w - 30, 244], fill=BORDER, width=2)
    if deadline:
        fk = font("BeVietnamPro-SemiBold.ttf", 19)
        draw_tracked(d, (34, 270), "DEADLINE", fk, MUT, 3)
    return im

def doc_card(title, lines, w=380, h=250, tag=None):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    d.text((26, 34), title, font=font("BeVietnamPro-SemiBold.ttf", 24), fill=INK, anchor="lm")
    yy = 76
    for ln in lines:
        d.rounded_rectangle([26, yy, 26 + (w - 60) * ln, yy + 12], 6, fill=(226, 235, 247, 255))
        yy += 26
    if tag:
        im.alpha_composite(chip(tag[0], tag[1], WHITE, 18), (24, h - 54))
    return im

def code_panel(x, y, w, lines, hl=(), title="server.js", fs=23, lh=34):
    h = 66 + len(lines) * lh + 14
    im = sp_code([], w, h, title)
    d = ImageDraw.Draw(im)
    for i, line in enumerate(lines):
        row = sp_code_line(line, hl=(i in hl), num=i + 1, width=w - 36)
        im.paste(row, (18, 62 + i * lh), row)
    return im

def terminal(x, y, w, lines, title="Terminal", typed=None, caret=False):
    h = 70 + 34 * max(len(lines), 6)
    im = Image.new("RGBA", (w, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 8, w, h + 6], 16, fill=(0, 0, 0, 45))
    d.rounded_rectangle([0, 0, w, h], 16, fill=(17, 24, 39, 255))
    d.rounded_rectangle([0, 0, w, 46], 16, fill=(30, 41, 59, 255))
    d.rectangle([0, 30, w, 46], fill=(30, 41, 59, 255))
    for i, c in enumerate([(255, 107, 107), (245, 196, 94), (98, 199, 132)]):
        d.ellipse([18 + i * 22, 17, 28 + i * 22, 27], fill=c + (255,))
    d.text((100, 23), title, font=font("JetBrainsMono-var.ttf", 18), fill=(148, 163, 184, 255), anchor="lm")
    yy = 70
    for ln in lines:
        col = (226, 232, 240, 255)
        if ln.startswith("$"):
            col = (110, 231, 183, 255)
        elif ln.startswith("#"):
            col = (148, 163, 184, 255)
        d.text((24, yy), ln, font=font("JetBrainsMono-var.ttf", 21), fill=col, anchor="lm")
        yy += 34
    if caret:
        d.rectangle([24, yy - 20, 34, yy + 4], fill=(110, 231, 183, 255))
    return im

def check_card(icon, title, sub, w=500, h=150, color=GREEN, active=1.0, name=None):
    im = card(w, h, fill=WHITE)
    d = ImageDraw.Draw(im)
    im.paste(ico(name or icon, color, 48), (26, 28), ico(name or icon, color, 48))
    d.text((92, 54), title, font=font("BeVietnamPro-SemiBold.ttf", 27), fill=INK, anchor="lm")
    if sub:
        d.text((92, 92), sub, font=font("BeVietnamPro-Regular.ttf", 21), fill=MUT, anchor="lm")
    if active < 1:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * active)))
    return im

def paste(base, im, x, y, p=1.0, anchor="tl"):
    paste_sprite(base, im, x, y, p, anchor)

def dim_rect(base, box, alpha=120):
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle(box, fill=(11, 42, 91, alpha))
    base.alpha_composite(ov)

def hand_underline(d, x0, x1, y, p, color=AMBER, width=6):
    if p > 0:
        d.line([x0, y, x0 + (x1 - x0) * p, y + 3 * p], fill=color, width=width)

def hand_ellipse(d, cx, cy, rx, ry, p, color=BLUE, width=5):
    if p <= 0:
        return
    box = [cx - rx, cy - ry, cx + rx, cy + ry]
    d.arc(box, -100, -100 + 360 * p, fill=color, width=width)

def cross(d, cx, cy, r, color=RED, width=6):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=color, width=width)
    d.line([cx - r, cy + r, cx + r, cy - r], fill=color, width=width)

def title_block(base, title, sub=None, t=1.0, accent=BLUE):
    d = ImageDraw.Draw(base)
    if sub:
        draw_rich(d, (960, 330), sub, F_BSUB, MUT, "mm")
    draw_rich(d, (960, 410), title, F_BANNER, INK, "mm")
    return d
