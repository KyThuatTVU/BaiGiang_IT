# -*- coding: utf-8 -*-
"""Helper hình ảnh dùng chung cho bản full 18 cảnh."""
import math
from PIL import Image, ImageDraw, ImageFilter
from core import (W, H, FPS, FF, font, tw, seg, lin, draw_marker,
                  draw_marker_circle, draw_rich, paste_brand, sp_icon)
from demo20 import shadow_card, blit, tracked, chip, decode, caption
from demo_gateB import (bg_frame, live_grid, card_base, wrap_t, qcard, bullet,
                        photo, chrome, photo_card, header, an, dim_slot,
                        feature_card, TXT, MUT, CYAN, VIOLET, AMBER, EMER,
                        CREAM, CARD, F_T1, F_T2, F_T3, F_T4, F_SUB2, F_NOTE,
                        F_BRAND, F_MICRO, F_VERSION, F_BULLET, F_BSUB, F_FEAT,
                        F_FEAT_SUB, F_DIM, F_PILL)
from full_cues import CUES

RED = (229, 72, 77)
F_MONO = font("JetBrainsMono-var.ttf", 30)
F_JAK = font("PlusJakartaSans-var.ttf", 26, 700)


def mono(size, weight=None):
    return font("JetBrainsMono-var.ttf", size, weight)


def jak(size, weight=600):
    return font("PlusJakartaSans-var.ttf", size, weight)


def scene_title(base, t, s0, kicker, title, sub=None, x=112, fs=48):
    p = seg(t, s0 + 0.15, s0 + 0.95)
    if p <= 0:
        return
    a = int(255 * p)
    dy = int((1 - p) * 16)
    d = ImageDraw.Draw(base)
    tracked(d, (x, 206 + dy), kicker, F_MICRO, AMBER + (a,), 2.4)
    f = F_T4 if fs >= 46 else font("BeVietnamPro-Bold.ttf", fs)
    d.text((x, 250 + dy), title, font=f, fill=TXT + (a,), anchor="lm")
    if sub:
        d.text((x, 306 + dy), sub, font=F_SUB2, fill=MUT + (a,), anchor="lm")


def mini_card(base, cx, cy, w, h, p, acc, kicker, title, sub=None, icon=None,
              kfs=13, tfs=26, sfs=17):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    tx = pad + 26
    if icon:
        d.rounded_rectangle([pad + 20, pad + 20, pad + 76, pad + 76], 12,
                            fill=acc + (24,), outline=acc + (70,), width=1)
        ic = sp_icon(icon, acc, 34)
        im.paste(ic, (pad + 31, pad + 31), ic)
        tx = pad + 92
    if kicker:
        tracked(d, (tx, pad + 22), kicker, font("BeVietnamPro-Medium.ttf", kfs),
                acc + (230,), 1.8)
    ty = pad + (46 if kicker else 30)
    lines = wrap_t(title, font("BeVietnamPro-SemiBold.ttf", tfs), w - (tx - pad) - 26)
    for ln in lines[:2]:
        draw_rich(d, (tx, ty), ln, font("BeVietnamPro-SemiBold.ttf", tfs),
                  TXT + (255,), "la")
        ty += int(tfs * 1.22)
    if sub:
        lines = wrap_t(sub, font("BeVietnamPro-Regular.ttf", sfs), w - (tx - pad) - 26)
        for ln in lines[:2]:
            draw_rich(d, (tx, ty), ln, font("BeVietnamPro-Regular.ttf", sfs),
                      MUT + (255,), "la")
            ty += int(sfs * 1.25)
    blit(base, im, cx, cy, p, 12)


def formula_card(base, cx, cy, w, h, p, acc, text, fs=56, kicker=None, note=None):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    if kicker:
        tracked(d, (pad + 26, pad + 20), kicker, F_MICRO, acc + (230,), 2)
    f = mono(fs)
    yy = pad + h // 2 + (6 if note else 0)
    draw_rich(d, (pad + w // 2, yy), text, f, TXT + (255,), "mm")
    if note:
        draw_rich(d, (pad + w // 2, pad + h - 20), note, F_NOTE, MUT + (225,), "mm")
    blit(base, im, cx, cy, p, 14)


def stat_card(base, cx, cy, w, h, p, acc, label, value, fs=54):
    if p <= 0:
        return
    im, pad = card_base(w, h, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    tracked(d, (pad + 24, pad + 20), label, F_MICRO, acc + (230,), 2)
    draw_rich(d, (pad + w // 2, pad + h // 2 + 16), value, mono(fs), TXT + (255,), "mm")
    blit(base, im, cx, cy, p, 12)


def caveat(base, cx, cy, p, text, acc=AMBER, w=None, fs=17):
    if p <= 0:
        return
    f = font("BeVietnamPro-SemiBold.ttf", fs)
    w = w or int(tw(text, f)) + 96
    im, pad = shadow_card(w, 52, 14, acc + (90,), (22, 22, 30, 242))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 1, pad + 1, pad + w - 1, pad + 51], 14,
                        outline=acc + (150,), width=1)
    ic = sp_icon("alert-triangle", acc, 24)
    im.paste(ic, (pad + 22, pad + 14), ic)
    draw_rich(d, (pad + 56, pad + 26), text, f, TXT + (245,), "lm")
    blit(base, im, cx, cy, p, 10)


def rich_caption(base, lines, p=1.0):
    if not lines or p <= 0:
        return
    w, h = 900, 170
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font("BeVietnamPro-Medium.ttf", 27)
    y = 81
    d.rounded_rectangle([28, y - 16, 32, y + len(lines) * 38 + 8], 2, fill=VIOLET + (255,))
    for ln in lines:
        draw_rich(d, (52, y - 20), ln, f, (226, 232, 240, 255), "la")
        y += 38
    blit(base, im, 60 + w / 2, 855 + h / 2, p, 0)


def cross_claim(d, cx, cy, w, h, p):
    if p <= 0:
        return
    draw_marker(d, cx - w // 2 + 18, cy - h // 2 + 10, cx + w // 2 - 18,
                cy + h // 2 - 10, p, RED, 5, seed=int(cx) % 7 + 1)
    draw_marker(d, cx + w // 2 - 18, cy - h // 2 + 10, cx - w // 2 + 18,
                cy + h // 2 - 10, max(0.0, p - 0.35) / 0.65, RED, 5, seed=int(cy) % 7 + 11)


CODE_LINES = [
    ("import pandas as pd", "kw"),
    ("from sklearn.linear_model import LinearRegression", "kw"),
    ("", ""),
    ('df = pd.read_csv("gia_nha.csv")', "str"),
    ("model = LinearRegression()", "var"),
    ("model.fit(df[[\"dien_tich\"]], df[\"gia\"])", "var"),
    ("", ""),
    ("print(model.coef_, model.intercept_)", "fn"),
    ("model.predict([[85]])", "fn"),
]


def code_card(base, cx, cy, p, reveal, w=1000, h=440):
    if p <= 0:
        return
    im, pad = card_base(w, h, CYAN)
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 24, pad + 22, pad + 72, pad + 30], 4, fill=RED + (210,))
    d.rounded_rectangle([pad + 82, pad + 22, pad + 130, pad + 30], 4, fill=AMBER + (210,))
    d.rounded_rectangle([pad + 140, pad + 22, pad + 188, pad + 30], 4, fill=EMER + (210,))
    f = mono(21)
    cols = {"kw": VIOLET, "str": AMBER, "var": TXT, "fn": CYAN, "": MUT}
    total = sum(len(t) for t, _ in CODE_LINES) + len(CODE_LINES)
    budget = int(total * max(0.0, min(1.0, reveal)))
    y = pad + 58
    for text, kind in CODE_LINES:
        if budget <= 0:
            break
        part = text[:budget]
        budget -= len(text) + 1
        if part:
            draw_rich(d, (pad + 30, y), part, f, cols[kind] + (255,), "lm")
        y += 38
    blit(base, im, cx, cy, p, 16)
