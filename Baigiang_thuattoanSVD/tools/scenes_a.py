# -*- coding: utf-8 -*-
"""Cảnh S01–S06 bài SVD."""
import math
from PIL import Image, ImageDraw
import demo_gateB as G
import full_state as FS
from full_common import (
    F_T2, F_T3, F_T4, F_SUB2, F_NOTE, F_MICRO, F_LEG, F_CELL, F_QM,
    TXT, MUT, CYAN, VIOLET, AMBER, EMER, CREAM,
    scene_head, info_card, chip, photo_card, stat_tile, an, tracked,
    draw_rich, draw_marker, draw_marker_circle, wrap_t, seg, lin,
    card_base, blit, step_row, note_line,
)


def draw_s01(base, t, t0, t1):
    G.draw_s01(base, t)


def draw_s02(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s1, s2, s3, s4, s5 = (FS.ST[f"s02c{i}"] for i in range(1, 6))
    fade_out = 1 - seg(t, s5 - 0.30, s5 + 0.10)
    p1 = seg(t, s1 + 0.22, s1 + 0.92) * (1 - seg(t, s2 - 0.20, s2 + 0.25))
    p3 = seg(t, s2 + 0.05, s2 + 0.65) * fade_out
    photo_card(base, "7.jpg", 600, 535, 860, 484, p1, CYAN, mode="contain")
    photo_card(base, "3.jpg", 600, 535, 860, 484, p3, VIOLET, mode="contain")
    lp = seg(t, s1 + 0.25, s1 + 0.75)
    la = int(255 * max(p1, p3))
    if lp > 0 and la > 4:
        label, lc = "TRANG CHỦ", AMBER
        if t >= s2:
            label, lc = "TRONG TRANG SẢN PHẨM", VIOLET
        tracked(d, (188, 250), label, F_MICRO, lc + (la,), 2.2)
    note_p = max(p1, p3)
    if note_p > 0:
        draw_rich(d, (600, 805), "Ảnh minh họa giao diện · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * note_p),), "mm")
    p = seg(t, t0 + 0.15, t0 + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (1120, 208), "THỰC TẾ", F_MICRO, AMBER + (a,), 2.4)
        d.text((1120, 252), "Gợi ý có mặt", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1120, 306), "khắp nơi", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1120, 362), "Từ trang chủ đến trang sản phẩm", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    chip(base, "Dành riêng cho bạn", CYAN, 1330, 448,
         seg(t, s1 + 0.25, s1 + 0.65) * (1 - seg(t, s3 - 0.20, s3 + 0.05)), fsize=16)
    chip(base, "Có thể bạn cũng thích", VIOLET, 1330, 508,
         seg(t, s1 + 0.45, s1 + 0.85) * (1 - seg(t, s3 - 0.20, s3 + 0.05)), fsize=16)
    chip(base, "Đúng sản phẩm · đúng người", EMER, 1330, 448,
         seg(t, s3 + 0.10, s3 + 0.50), fsize=15)
    chip(base, "Không hề đơn giản", AMBER, 1330, 570,
         seg(t, s4 + 0.05, s4 + 0.45), fsize=15)
    stats = [("10K+", "người dùng", CYAN), ("50K+", "sản phẩm", VIOLET),
             ("≈ 1%", "ô có tương tác", AMBER)]
    for i, (num, lab, acc) in enumerate(stats):
        stat_tile(base, 616, 430 + 96 * i, seg(t, s5 + 0.10 + i * 0.22, s5 + 0.50 + i * 0.22),
                  num, lab, acc)
    q = seg(t, s5 + 0.35, s5 + 0.85)
    if q > 0:
        lines = wrap_t("Mỗi người chỉ tương tác với một phần rất nhỏ của bảng.", F_NOTE, 520)
        yy = 700
        for ln in lines:
            draw_rich(d, (616, yy), ln, F_NOTE, MUT + (int(225 * q),), "mm")
            yy += 26
    an(base, t, "present", -1, 0.66, 1650, 1048, 1.0, FS.is_talk(t))


def draw_s03(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s03c{i}"] for i in range(1, 6)}
    scene_head(base, t, t0, "DỮ LIỆU THỰC TẾ", "Mỗi tương tác là một ô",
               "trong bảng người dùng – sản phẩm")
    for r in range(G.GRID_R):
        for c in range(G.GRID_C):
            i = r * G.GRID_C + c
            ap = seg(t, t0 + 0.18 + min(i * 0.008, 0.90), t0 + 0.42 + min(i * 0.008, 0.90))
            if ap <= 0:
                continue
            x = G.GX + c * (G.CELL + G.GAP)
            y = G.GY + r * (G.CELL + G.GAP)
            box = [x, y, x + G.CELL, y + G.CELL]
            val = G.FILLED.get((r, c))
            if (r, c) == G.QCELL:
                d.rounded_rectangle(box, 10, fill=(52, 38, 16), outline=AMBER + (210,), width=2)
                d.text((x + G.CELL / 2, y + G.CELL / 2 - 1), "?", font=F_QM,
                       fill=AMBER + (255,), anchor="mm")
            elif val:
                d.rounded_rectangle(box, 10, fill=(16, 40, 56), outline=CYAN + (150,), width=1)
                d.text((x + G.CELL / 2, y + G.CELL / 2), str(val), font=F_CELL,
                       fill=CYAN + (240,), anchor="mm")
            else:
                d.rounded_rectangle(box, 10, fill=(23, 30, 45), outline=(48, 58, 78), width=1)
    qx = G.GX + G.QCELL[1] * (G.CELL + G.GAP) + G.CELL / 2
    qy = G.GY + G.QCELL[0] * (G.CELL + G.GAP) + G.CELL / 2
    if t >= s[4] + 0.20:
        pul = 0.5 + 0.5 * math.sin(t * 3.0)
        gl = Image.new("RGBA", (G.W, G.H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        rr = 34 + 8 * pul
        gd.ellipse([qx - rr, qy - rr, qx + rr, qy + rr],
                   outline=AMBER + (int(60 + 60 * pul),), width=2)
        base.alpha_composite(gl)
    mk = seg(t, s[4] + 0.20, s[4] + 0.80)
    if mk > 0:
        draw_marker_circle(d, qx, qy, 44, 44, mk, AMBER, 5, seed=4)
    rp = seg(t, t0 + 0.20, t0 + 0.70)
    stat_tile(base, 1270, 404, rp, "8 × 14", "người dùng × sản phẩm", CYAN)
    stat_tile(base, 1270, 490, seg(t, t0 + 0.40, t0 + 0.90), "≈ 80%", "ô còn trống", AMBER)
    lp = seg(t, t0 + 0.60, t0 + 1.00)
    if lp > 0:
        rows = ((CYAN, "Ô đã có đánh giá"), ((120, 136, 158), "Ô trống · chưa tương tác"),
                (AMBER, "Ô cần dự đoán"))
        for i, (col, text) in enumerate(rows):
            yy = 580 + i * 40
            d.ellipse([1082, yy - 6, 1094, yy + 6], fill=col + (255,))
            d.text((1108, yy), text, font=F_LEG, fill=TXT + (235,), anchor="lm")
    chip(base, "Gợi ý = điền ô trống", AMBER, 1290, 730,
         seg(t, s[5] + 0.10, s[5] + 0.50), fsize=15)
    an(base, t, "point_left", -1, 0.60, 1650, 1048, 1.0, FS.is_talk(t))


def draw_s04(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s04c{i}"] for i in range(1, 6)}
    scene_head(base, t, t0, "Ý TƯỞNG", "Người giống nhau",
               "thì thích những thứ giống nhau")
    p = seg(t, s[1] + 0.20, s[1] + 0.80)
    photo_card(base, "2.jpg", 520, 556, 700, 430, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (520, 802), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    old = 1 - seg(t, s[4] - 0.25, s[4] + 0.05)
    c1 = seg(t, s[1] + 0.25, s[1] + 0.85) * old
    info_card(base, 1330, 470, c1, 580, 168, CYAN, "CÁCH TỰ NHIÊN",
              "Dựa vào người giống mình",
              ["Hai người cùng gu, cùng sở thích", "Gợi ý dựa trên hành vi chung"], "users")
    chip(base, "Cùng thích điện thoại + laptop", CYAN, 1330, 612,
         seg(t, s[2] + 0.10, s[2] + 0.50) * old, fsize=15)
    chip(base, "Collaborative Filtering · lọc cộng tác", VIOLET, 1330, 682,
         seg(t, s[3] + 0.10, s[3] + 0.50) * old, fsize=15)
    c4 = seg(t, s[4] + 0.05, s[4] + 0.65)
    info_card(base, 1330, 480, c4, 580, 170, EMER, "VÍ DỤ · AN · BÌNH",
              "Gu gần giống nhau",
              ["An: iPhone · MacBook · AirPods", "Bình: iPhone · MacBook"], "user")
    c5 = seg(t, s[5] + 0.10, s[5] + 0.70)
    if c5 > 0:
        chip(base, "→ Gợi ý AirPods cho Bình", EMER, 1330, 640, c5, fsize=17)
    an(base, t, "present", -1, 0.62, 1660, 1048, 1.0, FS.is_talk(t))


def draw_s05(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s05c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "HAI CÁCH TIẾP CẬN", "User-based · Item-based",
               "Dựa trên người dùng · dựa trên sản phẩm")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "4.jpg", 470, 556, 680, 430, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (470, 800), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    c3 = seg(t, s[3] + 0.10, s[3] + 0.70)
    info_card(base, 1330, 420, c3, 600, 156, CYAN, "USER-BASED",
              "Tìm người giống mình",
              ["Xem những người đó thích gì"], "users")
    info_card(base, 1330, 592, c3, 600, 156, VIOLET, "ITEM-BASED",
              "Tìm sản phẩm đi cùng nhau",
              ["Món thường xuất hiện cùng món đã xem"], "package")
    mu = seg(t, s[4] + 0.15, s[4] + 0.75)
    if mu > 0:
        draw_marker(d, 1150, 505, 1510, 505, mu, CYAN, 4, seed=5)
    mi = seg(t, s[5] + 0.15, s[5] + 0.75)
    if mi > 0:
        draw_marker(d, 1150, 679, 1510, 679, mi, VIOLET, 4, seed=6)
    chip(base, "Cần: cách so sánh & dự đoán đủ mạnh", AMBER, 1330, 735,
         seg(t, s[6] + 0.10, s[6] + 0.50), fsize=15)
    an(base, t, "present", -1, 0.60, 1660, 1048, 1.0, FS.is_talk(t))


def draw_s06(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s06c{i}"] for i in range(1, 6)}
    scene_head(base, t, t0, "VÍ DỤ", "Gợi ý phim",
               "Hai người xem cùng ba bộ phim")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "10.jpg", 470, 556, 680, 430, p, VIOLET, mode="contain")
    if p > 0:
        draw_rich(d, (470, 800), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    step_row(base, 1330, 410, seg(t, s[2] + 0.05, s[2] + 0.65), CYAN, 1,
             "Cùng xem và thích 3 phim giống nhau")
    step_row(base, 1330, 506, seg(t, s[3] + 0.05, s[3] + 0.65), VIOLET, 2,
             "Một người xem thêm một phim khác")
    step_row(base, 1330, 602, seg(t, s[4] + 0.05, s[4] + 0.65), EMER, 3,
             "Gợi ý phim đó cho người còn lại")
    chip(base, "Dạng đơn giản nhất của user-based CF", EMER, 1330, 706,
         seg(t, s[5] + 0.10, s[5] + 0.50), fsize=15)
    an(base, t, "present", -1, 0.62, 1660, 1048, 1.0, FS.is_talk(t))
