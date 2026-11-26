# -*- coding: utf-8 -*-
"""Khối hình ảnh dùng chung cho 18 cảnh full SVD (kế thừa look đã duyệt)."""
import json, math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import demo_gateB as G
from demo_gateB import (
    TXT, MUT, CYAN, VIOLET, AMBER, EMER, CREAM, CARD,
    F_T1, F_T2, F_T3, F_T4, F_SUB2, F_NOTE, F_MICRO, F_BRAND, F_LEG,
    F_BULLET, F_BSUB, F_CELL, F_QM, F_STAT, F_STATL,
    bg_frame, live_grid, card_base, bullet, photo_card, stat_tile, an, wrap_t,
    photo, chrome, tracked, chip, blit, draw_rich, draw_marker, draw_marker_circle,
    paste_brand, sp_icon, shadow_card, font, tw, seg, lin, W, H,
)
from demo20 import json_card
import full_state as FS

F_H = font("BeVietnamPro-SemiBold.ttf", 34)
F_MONO = font("JetBrainsMono-var.ttf", 46)
F_MONO_M = font("JetBrainsMono-var.ttf", 30)
F_MONO_S = font("JetBrainsMono-var.ttf", 20)
F_CODE = font("JetBrainsMono-var.ttf", 19)
F_CODE_S = font("JetBrainsMono-var.ttf", 17)
F_NUM = font("PlusJakartaSans-var.ttf", 40, 800)
F_NUM_S = font("PlusJakartaSans-var.ttf", 28, 700)
F_LBL2 = font("BeVietnamPro-SemiBold.ttf", 21)
F_SMALL = font("BeVietnamPro-Regular.ttf", 17)


def scene_head(base, t, t0, kicker, title, sub=None, acc=AMBER, x=112):
    p = seg(t, t0 + 0.10, t0 + 0.85)
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    tracked(d, (x, 206), kicker, F_MICRO, acc + (255,), 2.4)
    d.text((x, 250), title, font=F_T4, fill=TXT + (255,), anchor="lm")
    if sub:
        d.text((x, 306), sub, font=F_SUB2, fill=MUT + (255,), anchor="lm")


def note_line(base, cx, y, p, text, fs=None, col=MUT, anchor="mm"):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    draw_rich(d, (cx, y), text, fs or F_NOTE, col + (int(225 * p),), anchor)


def info_card(base, cx, cy, p, w, h, acc, kicker, title, subs=(), icon=None):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    ix = pad + 24
    if icon:
        ic = sp_icon(icon, acc, 34)
        im.paste(ic, (ix, pad + 22), ic)
        tx = ix + 48
    else:
        tx = ix
    tracked(d, (tx, pad + 30), kicker, F_MICRO, acc + (235,), 2)
    d.text((ix, pad + 62), title, font=F_T3, fill=TXT + (255,))
    yy = pad + 100
    for s in subs:
        d.text((ix, yy), s, font=F_SMALL, fill=MUT + (255,))
        yy += 25
    blit(base, im, cx, cy, p, 14)


def formula_card(base, cx, cy, p, w, acc, formula, note=None, fs=None, h=None):
    if p <= 0:
        return
    hh = h or (150 if note else 108)
    im, pad = card_base(w, hh, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.text((pad + w / 2, pad + (hh / 2 if not note else hh / 2 - 14)), formula,
           font=fs or F_MONO, fill=TXT + (255,), anchor="mm")
    if note:
        d.text((pad + w / 2, pad + hh - 30), note, font=F_NOTE,
               fill=MUT + (255,), anchor="mm")
    blit(base, im, cx, cy, p, 12)


def pill(base, cx, cy, p, text, acc, fsize=15):
    if p <= 0:
        return
    f = font("JetBrainsMono-var.ttf", fsize)
    w = int(tw(text, f)) + 54
    im = Image.new("RGBA", (w, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 39], 10, fill=(9, 14, 26, 235),
                        outline=acc + (170,), width=1)
    d.ellipse([13, 17, 19, 23], fill=acc + (255,))
    draw_rich(d, (30, 20), text, f, TXT + (255,), "lm")
    blit(base, im, cx, cy, p, 8)


def code_card(base, x, y, w, lines, q, p, acc=EMER, title="python · surprise"):
    if p <= 0:
        return 0
    h = 52 + len(lines) * 30 + 18
    im, pad = shadow_card(w, h, 18, (255, 255, 255, 34), (11, 19, 34, 246))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 1, pad + 1, pad + w - 1, pad + h - 1], 18,
                        outline=(255, 255, 255, 30), width=1)
    d.line([pad + 22, pad + 1, pad + w - 22, pad + 1], fill=acc + (185,), width=2)
    d.text((pad + 22, pad + 16), title, font=font("JetBrainsMono-var.ttf", 14),
           fill=AMBER + (235,))
    n = int(q * sum(len(s) + 1 for s in lines))
    used = 0
    yy = pad + 46
    cx0, cy0 = pad + 22, yy
    for s in lines:
        vis = s[:max(0, n - used)]
        d.text((pad + 22, yy), vis, font=F_CODE, fill=(248, 251, 255, 255))
        cx0, cy0 = pad + 22 + d.textlength(vis, font=F_CODE), yy
        used += len(s) + 1
        yy += 30
        if used >= n:
            break
    if q < 1 or int((q * 10) % 2) == 0:
        d.rectangle([cx0 + 2, cy0 + 2, cx0 + 9, cy0 + 22], fill=AMBER + (200,))
    blit(base, im, x + w / 2, y + h / 2 + 26, p, 10)
    return h


def photo_note(base, cx, y, p, text):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    draw_rich(d, (cx, y), text, F_NOTE, MUT + (int(215 * p),), "mm")


def matrix_table(base, cx, cy, p, vals, rows=("An", "Bình", "Chi", "Dũng"),
                 cols=("iPhone", "Samsung", "MacBook", "Chuột"), acc=CYAN,
                 cw=118, ch=64, missing=None, row_colors=None, qp=0.0, pulse=0.0):
    if p <= 0:
        return None
    lw = 110
    w = lw + 4 * cw + 44
    h = 74 + 4 * ch + 24
    im, pad = card_base(w, h, acc)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    x0 = cx - w / 2 + 22
    y0 = cy - h / 2 + 20
    d = ImageDraw.Draw(base)
    for c, name in enumerate(cols):
        d.text((x0 + lw + c * cw + cw / 2, y0 + 18), name,
               font=font("BeVietnamPro-SemiBold.ttf", 18), fill=MUT + (255,), anchor="mm")
    for r, name in enumerate(rows):
        d.text((x0 + 10, y0 + 58 + r * ch + ch / 2), name,
               font=font("BeVietnamPro-SemiBold.ttf", 20), fill=TXT + (235,), anchor="lm")
    geo = {}
    for r in range(4):
        for c in range(4):
            bx = x0 + lw + c * cw
            by = y0 + 44 + r * ch
            col = (18, 27, 44)
            border = (46, 58, 78)
            if row_colors and r in row_colors:
                col = (16, 38, 52) if row_colors[r] == CYAN else (36, 26, 58)
                border = row_colors[r] + (70,)
            d.rounded_rectangle([bx + 4, by + 4, bx + cw - 4, by + ch - 4], 10,
                                fill=col, outline=border, width=1)
            if missing is not None and (r, c) == missing:
                pul = 0.5 + 0.5 * math.sin(pulse * 3.0)
                d.rounded_rectangle([bx + 4, by + 4, bx + cw - 4, by + ch - 4], 10,
                                    fill=(52, 38, 16), outline=AMBER + (200,), width=2)
                d.text((bx + cw / 2, by + ch / 2), "?", font=F_QM,
                       fill=AMBER + (255,), anchor="mm")
                geo["missing"] = (bx + cw / 2, by + ch / 2)
            else:
                v = vals.get((r, c))
                if v is not None:
                    d.text((bx + cw / 2, by + ch / 2), str(v), font=F_CELL,
                           fill=TXT + (245,), anchor="mm")
            geo[(r, c)] = (bx + cw / 2, by + ch / 2)
    return geo


def section_label(base, x, y, p, text, acc):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    tracked(d, (x, y), text, F_MICRO, acc + (255,), 2.2)


def mono_box(base, x, y, w, p, lines, acc=VIOLET, fs=None, title=None):
    if p <= 0:
        return
    f = fs or F_MONO_S
    h = 26 + len(lines) * 34 + (26 if title else 8)
    im, pad = shadow_card(w, h, 14, (255, 255, 255, 30), (13, 21, 38, 240))
    d = ImageDraw.Draw(im)
    d.line([pad + 18, pad + 1, pad + w - 18, pad + 1], fill=acc + (170,), width=2)
    yy = pad + 16
    if title:
        d.text((pad + 20, yy), title, font=font("JetBrainsMono-var.ttf", 13),
               fill=acc + (230,))
        yy += 26
    for s in lines:
        d.text((pad + 20, yy), s, font=f, fill=TXT + (250,))
        yy += 34
    blit(base, im, x + w / 2, y + h / 2 + 20, p, 10)


def vs_col(base, cx, cy, p, acc, title, items, w=380):
    if p <= 0:
        return
    h = 110 + len(items) * 46
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    tracked(d, (pad + 24, pad + 26), title, F_MICRO, acc + (235,), 2)
    for i, (ic, t_) in enumerate(items):
        yy = pad + 66 + i * 46
        icon = sp_icon(ic, acc, 22)
        im.paste(icon, (pad + 24, yy), icon)
        d.text((pad + 58, yy + 11), t_, font=F_SMALL, fill=TXT + (235,), anchor="lm")
    blit(base, im, cx, cy, p, 14)


def api_card(base, x, y, w, p, path, method="GET", acc=AMBER):
    if p <= 0:
        return
    h = 64
    im, pad = shadow_card(w, h, 14, (255, 255, 255, 30), (13, 21, 38, 242))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 18, pad + 14, pad + 96, pad + 50], 9,
                        fill=(16, 40, 34), outline=EMER + (170,), width=1)
    d.text((pad + 57, pad + 32), method, font=font("JetBrainsMono-var.ttf", 17),
           fill=EMER + (245,), anchor="mm")
    d.text((pad + 112, pad + 32), path, font=font("JetBrainsMono-var.ttf", 19),
           fill=TXT + (245,), anchor="lm")
    blit(base, im, x + w / 2, y + h / 2 + 20, p, 10)


def step_row(base, cx, cy, p, acc, num, text, w=600, h=76):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.ellipse([pad + 18, pad + h / 2 - 21, pad + 60, pad + h / 2 + 21],
              fill=(10, 16, 28), outline=acc + (200,), width=2)
    d.text((pad + 39, pad + h / 2), str(num), font=font("PlusJakartaSans-var.ttf", 21, 800),
           fill=acc + (255,), anchor="mm")
    d.text((pad + 78, pad + h / 2), text, font=font("BeVietnamPro-Medium.ttf", 20),
           fill=TXT + (250,), anchor="lm")
    blit(base, im, cx, cy, p, 10)


def step_card(base, cx, cy, p, acc, num, lines, w=280, h=104):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.text((pad + 22, pad + 20), num, font=font("PlusJakartaSans-var.ttf", 26, 800),
           fill=acc + (255,))
    yy = pad + 26
    for ln in lines:
        d.text((pad + 74, yy), ln, font=font("BeVietnamPro-Medium.ttf", 16),
               fill=TXT + (240,))
        yy += 24
    blit(base, im, cx, cy, p, 10)


def dim_slot_lbl(base, cx, cy, p, label, w=280, h=120, acc=None):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 16,
                        fill=(20, 27, 42), outline=(52, 62, 82), width=1)
    d.text((cx, cy), label, font=font("BeVietnamPro-SemiBold.ttf", 20),
           fill=CREAM + (190,), anchor="mm")
