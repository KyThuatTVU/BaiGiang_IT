# -*- coding: utf-8 -*-
"""Scenes S01–S18."""
import math
from PIL import Image, ImageDraw
from full_common import *

F_T1 = font("PlusJakartaSans-var.ttf", 44, 800)
F_T2 = font("BeVietnamPro-SemiBold.ttf", 32)
F_B  = font("BeVietnamPro-Regular.ttf", 28)
F_BM = font("BeVietnamPro-Medium.ttf", 28)
F_S  = font("BeVietnamPro-Regular.ttf", 23)
F_SM = font("BeVietnamPro-Medium.ttf", 23)
F_L  = font("BeVietnamPro-SemiBold.ttf", 21)
F_N  = font("PlusJakartaSans-var.ttf", 34, 800)
F_BIG= font("PlusJakartaSans-var.ttf", 120, 800)

SETUPS, RENDERERS = {}, {}

def scene(fn):
    sid = fn.__name__.split("_")[-1]
    RENDERERS[sid] = fn
    return fn

# ===== S01 =====
WM = KICK = TAG = None
def setup_s01():
    global WM, KICK, TAG
    WM = Image.new("RGBA", (1000, 120), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(WM), (500, 60), "AN TECH ACADEMY", F_WM, NAVY, "mm")
    KICK = Image.new("RGBA", (1000, 50), (0, 0, 0, 0))
    dk = ImageDraw.Draw(KICK)
    txt = "BÀI GIẢNG CÔNG NGHỆ"
    fk = font("BeVietnamPro-SemiBold.ttf", 24)
    wd = sum(dk.textlength(ch, font=fk) + 3.5 for ch in txt)
    draw_tracked(dk, ((1000 - wd) / 2, 25), txt, fk, BLUE, 3.5)
    TAG = Image.new("RGBA", (1000, 60), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(TAG), (500, 30), "Học công nghệ, làm chủ tương lai", F_BODY, MUT, "mm")
    # 3 icon ứng dụng nối về một điểm
    global APPS
    APPS = []
    for name, col, label in [("pen-line", AMBER, "Ghi chú"), ("chat", BLUE, "Chat"), ("kanban", TEAL, "Bảng việc")]:
        im = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, 149, 149], 24, fill=WHITE, outline=BORDER, width=2)
        ic = ico("chat" if name == "chat" else name, col, 62)
        im.paste(ic, (44, 30), ic)
        dd.text((75, 118), label, font=font("BeVietnamPro-Medium.ttf", 20), fill=MUT, anchor="mm")
        APPS.append(im)
APPS = []

@scene
def render_S01(t):
    base = bg_canvas()
    d = ImageDraw.Draw(base)
    paste(base, KICK, 760, 328, seg(t, 0.10, 0.55), "mt")
    paste(base, WM, 760, 432, seg(t, 0.05, 0.50), "mm")
    u = seg(t, 1.00, 1.55)
    if u > 0:
        d.line([385, 500, 385 + 750 * u, 500], fill=AMBER, width=6)
    paste(base, TAG, 760, 554, seg(t, 0.55, 0.95), "mm")
    # icon ứng dụng cho cue 2
    s = SC["S01"]
    t2 = s["starts"][1]
    if t >= t2 - 0.2:
        hub = (1090, 795)
        for i, im in enumerate(APPS):
            x = 300 + i * 240
            p = seg(t, t2 + 0.0 + i * 0.18, t2 + 0.35 + i * 0.18)
            if p > 0:
                paste(base, im, x, 720, p, "tl")
                d.line([x + 150, 795, hub[0], hub[1]], fill=(47, 111, 208, 120), width=3)
        d.ellipse([hub[0] - 10, hub[1] - 10, hub[0] + 10, hub[1] + 10], fill=TEAL)
    paste_teacher(base, t, pose=("wave" if t < 3.4 else ("G" if t > 6.0 else "D")),
                  mouth=mouth_for(t, speak(t, "S01")))
    return base

# ===== S02 =====
CARD_X = [96, 556, 1016]
CARD_Y, CARD_W, CARD_H = 300, 420, 500
CARDS = {}
def setup_s02():
    global BANNER2
    BANNER2 = banner("S02", "Ba trạng thái, một bảng ghi chú", "Tình huống: dữ liệu chưa đồng bộ")
    for letter in "ABC":
        im = browser_note(letter, CARD_W, CARD_H)
        d = ImageDraw.Draw(im)
        fv = font("PlusJakartaSans-var.ttf", 44, 800)
        CARDS[letter] = im
BANNER2 = None

def deadline_block(base, x0, y0, letter, t):
    d = ImageDraw.Draw(base)
    tA = phrase_t("S02", 0, "Bạn A vừa cập nhật")
    tB = phrase_t("S02", 0, "nhưng bạn B vẫn thấy")
    tC = phrase_t("S02", 0, "còn bạn C phải tải lại")
    new = letter == "A" and t >= tA
    val = "20h" if new else "18h"
    fv = font("PlusJakartaSans-var.ttf", 44, 800)
    if new:
        fl = seg(t, tA, tA + 0.35)
        if fl > 0:
            d.rounded_rectangle([x0 + 28, y0 + 288, x0 + 28 + 132 * fl, y0 + 348], 10, fill=CREAM)
    d.text((x0 + 34, y0 + 318), val, font=fv,
           fill=(INK if letter != "B" and letter != "C" else (154, 167, 186, 255)), anchor="lm")
    if new:
        ch = chip("Vừa cập nhật", GREEN, WHITE, 20)
        a = seg(t, tA + 0.1, tA + 0.4)
        if a > 0:
            if a < 1:
                ch.putalpha(ch.getchannel("A").point(lambda v: int(v * a)))
            base.alpha_composite(ch, (x0 + 30, y0 + 372))
    elif letter == "B" and t >= tB:
        ph = (t - tB) % 0.8
        p = 1.0 + (0.10 * math.sin(math.pi * ph / 0.25) if ph < 0.25 else 0)
        ch = chip("Dữ liệu cũ", RED, WHITE, 20)
        if p != 1.0:
            ch = ch.resize((int(ch.size[0] * p), int(ch.size[1] * p)), Image.LANCZOS)
        base.alpha_composite(ch, (x0 + 30, y0 + 372))
    elif letter == "C":
        base.alpha_composite(chip("Chưa cập nhật", (140, 154, 173, 255), WHITE, 20), (x0 + 30, y0 + 372))
        if t >= tC:
            p = seg(t, tC, tC + 0.3)
            bw, bh = 246, 54
            ov = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.rounded_rectangle([0, 0, bw - 1, bh - 1], 12, fill=WHITE, outline=NAVY, width=2)
            ic = ico("refresh-cw", BLUE, 24)
            ov.paste(ic, (14, 15), ic)
            do.text((48, bh / 2), "Tải lại trang", font=font("BeVietnamPro-SemiBold.ttf", 20), fill=NAVY, anchor="lm")
            if p < 1:
                ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
            base.alpha_composite(ov, (x0 + 30, y0 + 430))

@scene
def render_S02(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER2, 1000, 78, seg(t, 0.0, 0.3), "mt")
    for i, letter in enumerate("ABC"):
        p = seg(t, 0.55 + i * 0.12, 0.80 + i * 0.12)
        if p > 0:
            x = CARD_X[i]
            paste(base, CARDS[letter], x, CARD_Y, p, "tl")
            deadline_block(base, x, CARD_Y, letter, t)
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S02")))
    return base

# ===== S03 =====
MINI = []
def setup_s03():
    global BANNER3, MINI
    BANNER3 = banner("S03", "Đồng bộ dữ liệu thời gian thực", "Real-time Data Synchronization")
    MINI.clear()
    for letter in "ABC":
        im = browser_note(letter, 300, 240, deadline=False)
        MINI.append(im)
BANNER3 = None

@scene
def render_S03(t):
    base = bg_canvas()
    brand_mark(base)
    s = SC["S03"]
    t2 = s["starts"][1] - 0.15
    d = ImageDraw.Draw(base)
    if t < t2:
        # 3 khung mờ dần
        for i, im in enumerate(MINI):
            x = 170 + i * 390
            p = seg(t, 0.10 + i * 0.12, 0.40 + i * 0.12) * (1 - seg(t, t2 - 0.5, t2 - 0.1) * 0.6)
            if p > 0:
                paste(base, im, x, 330, p, "tl")
        q = 0.9 + 0.1 * seg(t, 0.30, 0.60)
        draw_rich(d, (960, 660), "?", font("PlusJakartaSans-var.ttf", int(150 * q), 800), BLUE, "mm")
        # nút reload bị gạch chéo
        rp = seg(t, 0.9, 1.2)
        if rp > 0:
            ov = Image.new("RGBA", (330, 70), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.rounded_rectangle([0, 0, 329, 69], 14, fill=WHITE, outline=NAVY, width=2)
            ic = ico("refresh-cw", BLUE, 28)
            ov.paste(ic, (18, 20), ic)
            do.text((60, 35), "Tải lại trang", font=font("BeVietnamPro-SemiBold.ttf", 24), fill=NAVY, anchor="lm")
            base.alpha_composite(ov, (795, 830))
            if rp > 0.6:
                q2 = seg(t, 1.2, 1.5)
                if q2 > 0:
                    d.line([810, 900, 810 + 300 * q2, 830], fill=RED, width=6)
    else:
        p = seg(t, t2, t2 + 0.35)
        paste(base, BANNER3, 1000, 400, p, "mt")
        u = seg(t, t2 + 1.9, t2 + 2.5)
        wd = rich_width("Real-time Data Synchronization", F_BSUB)
        hand_underline(d, 960 - wd / 2 - 10, 960 + wd / 2 + 10, 610, u)
    paste_teacher(base, t, pose="D", mouth=mouth_for(t, speak(t, "S03")))
    return base

# ===== S04 =====
ROAD = []
def setup_s04():
    global BANNER4, ROAD
    BANNER4 = banner("S04", "Lộ trình bài học", "Bốn phần chính")
    ROAD.clear()
    items = [("layers", "Cơ chế", "Realtime hoạt động thế nào", BLUE),
             ("arrow-lr", "Truyền dữ liệu", "Client ↔ Server", BLUE),
             ("split", "Xung đột", "Chọn bản cập nhật nào", AMBER),
             ("code-xml", "Thực hành", "Node.js & Socket.IO", TEAL)]
    for ic, tt, ss, col in items:
        im = card(310, 250, fill=ICE_2)
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, 310, 8], 4, fill=col)
        dd.ellipse([24, 28, 88, 92], fill=col)
        icn = ico(ic, WHITE, 40) if ic in ("arrow-lr", "layers") else ico(ic, WHITE, 40)
        im.paste(icn, (36, 40), icn)
        dd.text((24, 128), tt, font=F_T2, fill=INK, anchor="lm")
        for j, l in enumerate(wrap(ss, F_S, 260)[:2]):
            draw_rich(dd, (24, 172 + j * 30), l, F_S, MUT, "lm")
        ROAD.append(im)
BANNER4 = None

@scene
def render_S04(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER4, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    for i, im in enumerate(ROAD):
        x = 96 + i * 356
        p = seg(t, 0.35 + i * 0.22, 0.65 + i * 0.22)
        if p > 0:
            paste(base, im, x, 350, p, "tl")
        if i < 3:
            ap = seg(t, 0.55 + i * 0.22, 0.8 + i * 0.22)
            if ap > 0:
                draw_conn(d, x + 318, 475, x + 348, 475, ap, BLUE, width=4)
    # chip công nghệ sáng cuối
    for i, (txt, t0) in enumerate([("Node.js", 5.4), ("Socket.IO", 6.0)]):
        p = seg(t, t0, t0 + 0.3)
        if p > 0:
            ch = chip(txt, TEAL, WHITE, 26)
            if p < 1:
                ch.putalpha(ch.getchannel("A").point(lambda v: int(v * p)))
            base.alpha_composite(ch, (700 + i * 230, 700))
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S04")))
    return base

# ===== S05 =====
KEY = []
def setup_s05():
    global BANNER5, KEYS
    BANNER5 = banner("S05", "Đồng bộ dữ liệu thời gian thực", "Định nghĩa")
    KEYS = [("nhiều thiết bị", "nhận thay đổi dữ liệu"), ("gần như ngay lập tức", ""), ("có người cập nhật", "")]
BANNER5 = None
KEYS = []

@scene
def render_S05(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER5, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    k_t = [phrase_t("S05", 1, "nhiều thiết bị"), phrase_t("S05", 1, "gần như ngay lập tức"),
           phrase_t("S05", 1, "có người cập nhật")]
    f5 = font("BeVietnamPro-SemiBold.ttf", 40)
    lines = [("Cơ chế giúp", "nhiều thiết bị", 392),
             ("nhận thay đổi dữ liệu", "gần như ngay lập tức", 522),
             ("khi", "có người cập nhật", 652)]
    for i, (lead, kw, y) in enumerate(lines):
        wl, wk = tw(lead, f5), tw(kw, f5)
        x = 900 - (wl + 16 + wk) / 2
        xk = x + wl + 16
        p = seg(t, k_t[i], k_t[i] + 0.45)
        if p > 0:
            hand_ellipse(d, xk + wk / 2, y, wk / 2 + 18, 36, p, BLUE, 3)
        draw_rich(d, (x, y), lead, f5, MUT, "lm")
        draw_rich(d, (xk, y), kw, f5, NAVY, "lm")
    paste_teacher(base, t, pose="V", mouth=mouth_for(t, speak(t, "S05")))
    return base

# ===== S06 =====
NODES6 = {}
def setup_s06():
    global BANNER6, NODES6
    BANNER6 = banner("S06", "Luồng đồng bộ", "A thay đổi → Server xử lý → B và C cập nhật")
    NODES6["A"] = node("globe", "A · Trình duyệt", "bảng ghi chú", 250, 150)
    NODES6["S"] = node("server", "Server", "xử lý & phát sự kiện", 280, 190)
    NODES6["B"] = node("globe", "B · Trình duyệt", "đang mở ứng dụng", 260, 140)
    NODES6["C"] = node("smartphone", "C · Điện thoại", "đang mở ứng dụng", 260, 140, tone=TEAL)
BANNER6 = None

@scene
def render_S06(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER6, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    pos = {"A": (170, 515), "S": (812, 495), "B": (1272, 368), "C": (1272, 636)}
    for k, t0 in [("A", 0.20), ("S", 0.45), ("B", 0.70), ("C", 0.95)]:
        paste(base, NODES6[k], pos[k][0], pos[k][1], seg(t, t0, t0 + 0.25), "tl")
    s = SC["S06"]
    t_arrow, t_dot1, t_ring, t_arrow2, t_dot2 = 1.05, 1.70, 2.55, 3.60, 4.25
    t_sync = s["starts"][1] - 0.15
    p1 = seg(t, t_arrow, t_arrow + 0.6)
    dq1 = None
    if t_dot1 <= t < t_dot1 + 0.9:
        dq1 = (t - t_dot1) / 0.9
    elif t >= t_dot1 + 0.9:
        dq1 = 1.0
    draw_conn(d, 432, 590, 812, 590, p1, BLUE, dq1, 5)
    if t_ring <= t < t_ring + 1.0:
        ph = (t - t_ring) / 1.0
        for k in range(2):
            q = ph - k * 0.25
            if 0 < q < 1:
                r = 96 + 52 * ease(q)
                col = BLUE if q < 0.5 else TEAL
                d.ellipse([952 - r, 590 - r, 952 + r, 590 + r], outline=col, width=5)
    p2 = seg(t, t_arrow2, t_arrow2 + 0.6)
    dqB = dqC = None
    if t_dot2 <= t < t_dot2 + 0.9:
        dqB = (t - t_dot2) / 0.9
    elif t >= t_dot2 + 0.9:
        dqB = 1.0
    if t_dot2 + 0.2 <= t < t_dot2 + 1.1:
        dqC = (t - t_dot2 - 0.2) / 0.9
    elif t >= t_dot2 + 1.1:
        dqC = 1.0
    draw_conn(d, 1092, 548, 1272, 438, p2, TEAL, dqB, 5)
    draw_conn(d, 1092, 622, 1272, 706, p2, TEAL, dqC, 5)
    if t >= t_sync:
        p = seg(t, t_sync, t_sync + 0.35)
        for k in ("B", "C"):
            x, y = pos[k]
            ov = Image.new("RGBA", (260, 140), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.rounded_rectangle([1, 1, 258, 138], 18, outline=TEAL, width=4)
            ic = ico("circle-check", TEAL, 26)
            ov.paste(ic, (204, 20), ic)
            if p < 1:
                ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
            base.alpha_composite(ov, (x, y))
        x, y = pos["A"]
        ch = chip("Đã gửi", BLUE, WHITE, 18)
        if p > 0:
            base.alpha_composite(ch, (x + 137, y + 14))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S06")))
    return base

# ===== S07 =====
def setup_s07():
    global BANNER7
    BANNER7 = banner("S07", "Hai cơ chế truyền thông", "HTTP Request – Response")

@scene
def render_S07(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER7, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S07"]
    col = card(720, 620, fill=WHITE)
    dc = ImageDraw.Draw(col)
    dc.rounded_rectangle([0, 0, 720, 64], 18, fill=NAVY)
    dc.rectangle([0, 40, 720, 64], fill=NAVY)
    dc.text((30, 32), "HTTP", font=font("PlusJakartaSans-var.ttf", 30, 800), fill=WHITE, anchor="lm")
    dc.text((690, 32), "Request – Response", font=F_S, fill=(214, 229, 247, 255), anchor="rm")
    ic = ico("globe", BLUE, 50); col.paste(ic, (42, 96), ic)
    dc.text((67, 170), "Trình duyệt", font=F_SM, fill=INK, anchor="mm")
    ic = ico("server", BLUE, 50); col.paste(ic, (628, 96), ic)
    dc.text((653, 170), "Server", font=F_SM, fill=INK, anchor="mm")
    pill = chip("GET /du-lieu", BLUE, WHITE, 18)
    col.alpha_composite(pill, (365 - pill.size[0] // 2, 186))
    pill2 = chip("200 OK", GREEN, WHITE, 18)
    col.alpha_composite(pill2, (365 - pill2.size[0] // 2, 316))
    a1 = seg(t, 0.5, 1.1)
    draw_conn(dc, 130, 250, 600, 250, a1, BLUE, width=5)
    a2 = seg(t, 1.4, 2.0)
    draw_conn(dc, 600, 300, 130, 300, a2, TEAL, width=5)
    c2 = s["starts"][1]
    loop = seg(t, c2 + 0.6, c2 + 1.3)
    if loop > 0:
        dc.arc([150, 372, 580, 512], 0, 180 * loop, fill=RED, width=4)
        if loop > 0.25:
            draw_rich(dc, (365, 470), "request mới", F_S, RED, "mm")
    ph = chip("hỏi lại", RED, WHITE, 18)
    col.alpha_composite(ph, (365 - ph.size[0] // 2, 540))
    paste(base, col, 150, 320, seg(t, 0.30, 0.65), "tl")
    ghost = card(360, 240, fill=ICE_2)
    dg = ImageDraw.Draw(ghost)
    dg.text((24, 34), "WebSocket ?", font=F_T2, fill=MUT, anchor="lm")
    dg.text((24, 84), "phần tiếp theo", font=F_S, fill=MUT, anchor="lm")
    paste(base, ghost, 1040, 380, seg(t, 0.6, 1.0), "tl")
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S07")))
    return base

# ===== S08 =====
def setup_s08():
    global BANNER8
    BANNER8 = banner("S08", "Polling", "Hỏi lại mỗi 5 giây")

@scene
def render_S08(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER8, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    # trục thời gian
    x0, x1, y = 220, 1360, 560
    d.line([x0, y, x1, y], fill=(154, 167, 186, 255), width=4)
    for i, sec in enumerate(range(0, 21, 5)):
        x = x0 + (x1 - x0) * sec / 20
        d.line([x, y - 14, x, y + 14], fill=(154, 167, 186, 255), width=3)
        d.text((x, y + 40), f"{sec}s", font=F_S, fill=MUT, anchor="mm")
        if sec > 0 or sec == 0:
            p = seg(t, 0.5 + i * 0.35, 0.8 + i * 0.35)
            if p > 0:
                im = card(150, 88, fill=WHITE)
                di = ImageDraw.Draw(im)
                di.text((75, 30), "GET", font=font("PlusJakartaSans-var.ttf", 22, 800), fill=BLUE, anchor="mm")
                di.text((75, 62), f"{sec}s", font=F_S, fill=MUT, anchor="mm")
                paste(base, im, x - 75, 380, p, "tl")
                draw_conn(d, x, 476, x, y - 16, seg(t, 0.75 + i * 0.35, 1.0 + i * 0.35), BLUE, width=4)
    # hai đầu
    ic = ico("globe", BLUE, 56); base.paste(ic, (120, y - 28), ic)
    ic = ico("server", BLUE, 56); base.paste(ic, (1400, y - 28), ic)
    p = seg(t, 3.6, 3.9)
    if p > 0:
        ch = chip("Polling", AMBER, WHITE, 28)
        ov = Image.new("RGBA", (ch.size[0] + 16, ch.size[1] + 16), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle([0, 0, ov.size[0] - 1, ov.size[1] - 1], 20, outline=AMBER, width=3)
        ov.alpha_composite(ch, (8, 8))
        if p < 1:
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
        base.alpha_composite(ov, (900, 760))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S08")))
    return base

# ===== S09 =====
def setup_s09():
    global BANNER9
    BANNER9 = banner("S09", "WebSocket", "Kết nối hai chiều Client – Server")

@scene
def render_S09(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER9, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S09"]
    p = seg(t, 0.25, 0.55)
    left = card(300, 180, fill=WHITE); dl = ImageDraw.Draw(left)
    left.paste(ico("globe", BLUE, 48), (26, 26), ico("globe", BLUE, 48))
    dl.text((90, 54), "Client", font=F_T2, fill=INK, anchor="lm")
    dl.text((26, 120), "đang mở ứng dụng", font=F_S, fill=MUT, anchor="lm")
    right = card(300, 180, fill=WHITE); dr = ImageDraw.Draw(right)
    right.paste(ico("server", TEAL, 48), (26, 26), ico("server", TEAL, 48))
    dr.text((90, 54), "Server", font=F_T2, fill=INK, anchor="lm")
    dr.text((26, 120), "giữ kết nối", font=F_S, fill=MUT, anchor="lm")
    if p > 0:
        paste(base, left, 180, 450, p, "tl")
        paste(base, right, 1160, 450, p, "tl")
    line_p = seg(t, 0.9, 1.5)
    if line_p > 0:
        d.line([480, 540, 480 + 680 * line_p, 540], fill=(154, 167, 186, 255), width=8)
    c2 = s["starts"][1]
    a1 = seg(t, c2 - 2.0, c2 - 1.4)
    a2 = seg(t, c2 - 1.8, c2 - 1.2)
    draw_conn(d, 520, 500, 1120, 500, a1, BLUE, width=5)
    draw_conn(d, 1120, 580, 520, 580, a2, TEAL, width=5)
    # gói dữ liệu chạy 2 chiều
    for k in range(6):
        ph = ((t - c2) / 1.6 + k / 6.0) % 1.0 if t >= c2 else None
        if ph is not None:
            x = 520 + 600 * ph
            d.rounded_rectangle([x - 34, 478, x + 34, 510], 8, fill=BLUE)
            x2 = 1120 - 600 * ((ph + 0.5) % 1.0)
            d.rounded_rectangle([x2 - 34, 570, x2 + 34, 602], 8, fill=TEAL)
    p2 = seg(t, c2 + 2.6, c2 + 3.0)
    if p2 > 0:
        ch = chip("một kết nối duy nhất", TEAL, WHITE, 24)
        if p2 < 1:
            ch.putalpha(ch.getchannel("A").point(lambda v: int(v * p2)))
        base.alpha_composite(ch, (830, 690))
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S09")))
    return base

# ===== S10 =====
def setup_s10():
    global BANNER10
    BANNER10 = banner("S10", "Socket.IO", "Thư viện giao tiếp thời gian thực theo sự kiện")

@scene
def render_S10(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER10, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S10"]
    big = card(620, 320, fill=WHITE)
    db = ImageDraw.Draw(big)
    ic = ico("zap", AMBER, 84)
    big.paste(ic, (40, 40), ic)
    db.text((140, 78), "Socket.IO", font=font("PlusJakartaSans-var.ttf", 52, 800), fill=INK, anchor="lm")
    big.alpha_composite(chip("library", BLUE, WHITE, 20), (146, 116))
    db.text((40, 210), "Giao tiếp theo sự kiện", font=F_BM, fill=MUT, anchor="lm")
    db.text((40, 254), "Dùng chung máy chủ HTTP", font=F_BM, fill=MUT, anchor="lm")
    p = seg(t, 0.25, 0.55)
    if p > 0:
        paste(base, big, 170, 330, p, "tl")
    c2 = s["starts"][1]
    # nhánh chính
    ws = node("zap", "WebSocket", "khi trình duyệt hỗ trợ", 330, 140, tone=TEAL, name="zap")
    wa = seg(t, c2 - 1.2, c2 - 0.6)
    if wa > 0:
        paste(base, ws, 1030, 330, wa, "tl")
        draw_conn(d, 800, 400, 1010, 400, seg(t, c2 - 1.0, c2 - 0.3), TEAL, width=5)
    # nhánh dự phòng nét đứt
    fb = node("refresh-cw", "Fallback", "khi WebSocket bị chặn", 330, 140, tone=MUT)
    fa = seg(t, c2 + 0.9, c2 + 1.4)
    if fa > 0:
        paste(base, fb, 1030, 560, fa, "tl")
        for i in range(7):
            q = seg(t, c2 + 0.6 + i * 0.1, c2 + 0.7 + i * 0.1)
            if q > 0:
                x0 = 800 + i * 32
                d.line([x0, 600, x0 + 18, 600], fill=(154, 167, 186, 255), width=4)
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S10")))
    return base

# ===== S11 =====
STEPS = []
def setup_s11():
    global BANNER11, STEPS
    BANNER11 = banner("S11", "Quy trình đồng bộ", "Bốn bước")
    STEPS.clear()
    specs = [("globe", "Kết nối", "Client → Server"),
             ("cursor", "Cập nhật", "Người dùng thao tác"),
             ("server", "Xử lý", "Server nhận & xử lý"),
             ("arrow-lr", "Phát sự kiện", "Server → các Client")]
    for i, (ic, tt, ss) in enumerate(specs):
        im = card(310, 300, fill=WHITE)
        dd = ImageDraw.Draw(im)
        dd.ellipse([24, 24, 80, 80], fill=NAVY)
        dd.text((52, 52), str(i + 1), font=F_N, fill=WHITE, anchor="mm")
        im.paste(ico(ic, BLUE, 52), (130, 34), ico(ic, BLUE, 52))
        dd.text((24, 130), tt, font=F_T2, fill=INK, anchor="lm")
        for j, l in enumerate(wrap(ss, F_S, 262)[:2]):
            draw_rich(dd, (24, 180 + j * 30), l, F_S, MUT, "lm")
        STEPS.append(im)
BANNER11 = None

@scene
def render_S11(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER11, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S11"]
    active = 0
    for i in range(1, 5):
        if t >= s["starts"][i] - 0.15:
            active = i
    for i, im in enumerate(STEPS):
        x = 96 + i * 360
        p = seg(t, 0.3 + i * 0.15, 0.55 + i * 0.15)
        if p > 0:
            paste(base, im, x, 370, p, "tl")
        if i < 3:
            ap = seg(t, 0.5 + i * 0.15, 0.7 + i * 0.15)
            if ap > 0:
                draw_conn(d, x + 318, 520, x + 348, 520, ap, BLUE, width=4)
    # ô đang giảng: viền teal + nâng nhẹ
    if active:
        x = 96 + (active - 1) * 360
        p = seg(t, s["starts"][active] - 0.15, s["starts"][active] + 0.2)
        ov = Image.new("RGBA", (314, 304), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        do.rounded_rectangle([1, 1, 313, 303], 20, outline=TEAL, width=5)
        if p < 1:
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
        base.alpha_composite(ov, (x, 370))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S11")))
    return base

# ===== S12 =====
def setup_s12():
    global BANNER12
    BANNER12 = banner("S12", "Server là trung tâm", "Mọi thiết bị cùng một trạng thái")

@scene
def render_S12(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER12, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S12"]
    cen = (820, 560)
    sv = node("server", "Server", "trạng thái chung", 300, 180)
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, sv, cen[0] - 150, cen[1] - 90, p, "tl")
    clients = [(180, 320), (180, 720), (1240, 320), (1240, 720)]
    c2 = s["starts"][1]
    for i, (x, y) in enumerate(clients):
        sep = seg(t, c2 - 0.8, c2 + 0.2) * 40 if i in (0, 3) else 0
        xx = x - sep if x < 800 else x + sep
        yy = y - sep if y < 500 else y + sep
        cp = seg(t, 0.45 + i * 0.12, 0.7 + i * 0.12)
        if cp > 0:
            cl = node("globe" if i < 2 else "smartphone", f"Client {chr(65 + i)}",
                      "dữ liệu riêng" if t >= c2 else "đã kết nối", 220, 120)
            paste(base, cl, xx, yy, cp, "tl")
        ex = cen[0] + (-1 if x < 800 else 1) * 150
        ey = cen[1] + (-1 if y < 500 else 1) * 90
        lp = seg(t, 0.7 + i * 0.1, 1.0 + i * 0.1)
        col = BLUE if t < c2 else (198, 120, 110, 255)
        draw_conn(d, ex, ey, xx + (220 if x < 800 else 0), yy + 60, lp, col, width=4)
        if t >= c2:
            mx, my = (ex + xx) / 2 + (110 if x < 800 else 0), (ey + yy) / 2 + 30
            cross(d, mx, my, 16, RED, 5)
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S12")))
    return base

# ===== S13 =====
NUMC = []
def setup_s13():
    global BANNER13, NUMC
    BANNER13 = banner("S13", "Ba khái niệm cần nắm", "Trước khi viết code")
    NUMC.clear()
    specs = [("globe", "Client – Server", "Hai phía của một kết nối"),
             ("zap", "Event", "Tín hiệu được gửi và lắng nghe"),
             ("split", "Xử lý xung đột", "Khi nhiều người sửa cùng lúc")]
    for i, (ic, tt, ss) in enumerate(specs):
        im = card(440, 300, fill=ICE_2)
        dd = ImageDraw.Draw(im)
        dd.text((36, 50), str(i + 1), font=font("PlusJakartaSans-var.ttf", 84, 800), fill=(205, 222, 242, 255), anchor="lm")
        icn = ico(ic, BLUE, 44)
        im.paste(icn, (356, 44), icn)
        dd.text((36, 160), tt, font=F_T2, fill=INK, anchor="lm")
        for j, l in enumerate(wrap(ss, F_S, 360)[:2]):
            draw_rich(dd, (36, 208 + j * 30), l, F_S, MUT, "lm")
        NUMC.append(im)
BANNER13 = None

@scene
def render_S13(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER13, 1000, 78, seg(t, 0.0, 0.3), "mt")
    for i, im in enumerate(NUMC):
        p = seg(t, 0.35 + i * 0.25, 0.65 + i * 0.25)
        paste(base, im, 120 + i * 460, 420, p, "tl")
    paste_teacher(base, t, pose="D", mouth=mouth_for(t, speak(t, "S13")))
    return base

# ===== S14 =====
def setup_s14():
    global BANNER14
    BANNER14 = banner("S14", "Client – Server", "Hai phía của một kết nối")

@scene
def render_S14(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER14, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S14"]
    lap = card(360, 230, fill=WHITE); dl = ImageDraw.Draw(lap)
    ic = ico("laptop", BLUE, 70); lap.paste(ic, (40, 40), ic)
    dl.text((130, 60), "Laptop", font=F_T2, fill=INK, anchor="lm")
    dl.text((40, 150), "Trình duyệt", font=F_S, fill=MUT, anchor="lm")
    ph = card(230, 230, fill=WHITE); dp = ImageDraw.Draw(ph)
    ic = ico("smartphone", BLUE, 64); ph.paste(ic, (40, 40), ic)
    dp.text((40, 150), "Điện thoại", font=F_S, fill=MUT, anchor="lm")
    sv = card(340, 300, fill=WHITE); ds = ImageDraw.Draw(sv)
    ic = ico("server", TEAL, 90); sv.paste(ic, (40, 40), ic)
    ds.text((150, 70), "Server", font=F_T2, fill=INK, anchor="lm")
    ds.text((40, 180), "nhận yêu cầu", font=F_S, fill=MUT, anchor="lm")
    ds.text((40, 216), "xử lý & trả kết quả", font=F_S, fill=MUT, anchor="lm")
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, lap, 150, 380, p, "tl")
        paste(base, ph, 150, 680, p, "tl")
        paste(base, sv, 1080, 440, p, "tl")
    c2 = s["starts"][1]
    a1 = seg(t, c2 - 1.0, c2 - 0.3)
    a2 = seg(t, c2 + 0.6, c2 + 1.4)
    draw_conn(d, 520, 470, 1060, 470, a1, BLUE, width=5)
    draw_conn(d, 1060, 640, 520, 640, a2, TEAL, width=5)
    d.text((760, 435), "yêu cầu", font=F_SM, fill=BLUE, anchor="mm")
    d.text((760, 680), "kết quả", font=F_SM, fill=TEAL, anchor="mm")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S14")))
    return base

# ===== S15 =====
ROWS = []
def setup_s15():
    global BANNER15, ROWS
    BANNER15 = banner("S15", "Event trong Socket.IO", "Gửi và lắng nghe sự kiện")
    ROWS.clear()
    specs = [("update-data", "Client → Server", "người dùng muốn cập nhật", BLUE),
             ("sync-state", "Server → Client", "gửi trạng thái hiện tại", NAVY),
             ("data-updated", "Server → Client", "báo dữ liệu vừa cập nhật", TEAL)]
    for name, direction, desc, col in specs:
        im = card(1180, 120, fill=WHITE)
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, 10, 120], 5, fill=col)
        dd.text((40, 38), name, font=font("JetBrainsMono-var.ttf", 30), fill=col, anchor="lm")
        dd.text((40, 84), desc, font=F_S, fill=MUT, anchor="lm")
        draw_rich(dd, (720, 60), direction, F_SM, INK, "lm")
        ROWS.append(im)
BANNER15 = None

@scene
def render_S15(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER15, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S15"]
    for i, im in enumerate(ROWS):
        t0 = s["starts"][i + 1] - 0.25 if i < 3 else 0
        if i < 3:
            p = seg(t, t0, t0 + 0.3)
            if p > 0:
                paste(base, im, 170, 360 + i * 140, p, "tl")
        else:
            pass
    # nhịp sáng nhẹ cuối cảnh
    if t >= s["starts"][4]:
        base.alpha_composite(Image.new("RGBA", (1, 1)))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S15")))
    return base

# ===== S16 =====
def setup_s16():
    global BANNER16
    BANNER16 = banner("S16", "Xung đột dữ liệu", "Hai người sửa cùng một tài liệu")

@scene
def render_S16(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER16, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S16"]
    a = doc_card("Bản A", [0.9, 0.7, 0.5], 340, 200, tag=("gửi lúc 12:00:01", BLUE))
    b = doc_card("Bản B", [0.8, 0.6, 0.4], 340, 200, tag=("gửi lúc 12:00:02", TEAL))
    sv = node("server", "Server", "chọn bản nào?", 300, 180)
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, a, 200, 380, p, "tl")
        paste(base, b, 200, 650, p, "tl")
        paste(base, sv, 1180, 500, p, "tl")
    c2 = s["starts"][0] + s["durs"][0] * 0.55
    draw_conn(d, 560, 470, 1160, 540, seg(t, c2 - 0.8, c2 - 0.2), BLUE, width=5)
    draw_conn(d, 560, 720, 1160, 620, seg(t, c2 - 0.6, c2 + 0.1), TEAL, width=5)
    if t >= c2 + 0.6:
        ph = (t - c2 - 0.6) % 1.2
        r = 1.0 + 0.12 * math.sin(math.pi * min(ph / 0.4, 1))
        draw_rich(d, (960, 700), "?", font("PlusJakartaSans-var.ttf", int(96 * r), 800), NAVY, "mm")
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S16")))
    return base

# ===== S17 =====
def setup_s17():
    global BANNER17
    BANNER17 = banner("S17", "Last Write Wins", "Bản cập nhật cuối thắng")

@scene
def render_S17(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER17, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S17"]
    y = 620
    d.line([220, y, 1360, y], fill=(154, 167, 186, 255), width=4)
    cA = doc_card("Bản A", [0.8, 0.6], 300, 180, tag=("12:00:01", BLUE))
    cB = doc_card("Bản B", [0.9, 0.8], 300, 180, tag=("12:00:02", TEAL))
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, cA, 330, 330, p, "tl")
        paste(base, cB, 940, 330, p, "tl")
    d.text((480, y + 40), "đến trước", font=F_S, fill=MUT, anchor="mm")
    d.text((1090, y + 40), "đến sau", font=F_S, fill=MUT, anchor="mm")
    win = phrase_t("S17", 0, "áp dụng bản cập nhật cuối")
    if t >= win:
        dim_rect(base, (330, 330, 630, 510), 150)
        draw_rich(d, (480, 420), "bị ghi đè", F_SM, WHITE, "mm")
        ch = chip("B thắng", TEAL, WHITE, 22)
        base.alpha_composite(ch, (1040, 530))
    p2 = seg(t, 4.4, 4.7)
    if p2 > 0:
        fw = card(300, 100, fill=CREAM, outline=(240, 214, 160, 255))
        ImageDraw.Draw(fw).text((150, 50), "LWW", font=font("PlusJakartaSans-var.ttf", 40, 800), fill=(122, 78, 0, 255), anchor="mm")
        paste(base, fw, 760, 760, p2, "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S17")))
    return base

# ===== S18 =====
def setup_s18():
    global BANNER18
    BANNER18 = banner("S18", "Optimistic Locking", "Kiểm tra phiên bản trước khi ghi")

@scene
def render_S18(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER18, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S18"]
    cl = doc_card("Client", [0.8, 0.6], 330, 200, tag=("version 3", BLUE))
    sv = node("server", "Server", "version 4", 320, 180)
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, cl, 240, 400, p, "tl")
        paste(base, sv, 1120, 410, p, "tl")
    c2 = s["starts"][1]
    draw_conn(d, 590, 480, 1110, 480, seg(t, c2 - 0.8, c2 - 0.2), BLUE, width=5)
    d.text((850, 440), "gửi v3", font=F_S, fill=BLUE, anchor="mm")
    if t >= c2 + 0.4:
        cross(d, 850, 560, 30, RED, 7)
        toast = card(420, 110, fill=(252, 233, 230, 255), outline=(198, 120, 110, 255))
        dt = ImageDraw.Draw(toast)
        dt.text((28, 36), "Dữ liệu đã thay đổi", font=font("BeVietnamPro-SemiBold.ttf", 26), fill=RED, anchor="lm")
        dt.text((28, 76), "Tải lại trước khi gửi", font=font("BeVietnamPro-Regular.ttf", 21), fill=(120, 60, 50, 255), anchor="lm")
        p2 = seg(t, c2 + 0.6, c2 + 0.9)
        if p2 > 0:
            paste(base, toast, 300, 700, p2, "tl")
    # OT/CRDT mờ góc
    p3 = seg(t, c2 + 3.0, c2 + 3.4)
    if p3 > 0:
        ot = doc_card("OT / CRDT", [0.6, 0.4], 300, 160, tag=("bài sau", MUT))
        ot.putalpha(ot.getchannel("A").point(lambda v: int(v * 0.6)))
        paste(base, ot, 1160, 700, p3, "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S18")))
    return base
