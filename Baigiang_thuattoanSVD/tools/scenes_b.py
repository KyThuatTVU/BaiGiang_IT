# -*- coding: utf-8 -*-
"""Cảnh S07–S12 bài SVD."""
import math
from PIL import Image, ImageDraw
import full_state as FS
from full_common import (
    F_T2, F_T3, F_T4, F_SUB2, F_NOTE, F_MICRO, F_LEG, F_CELL,
    TXT, MUT, CYAN, VIOLET, AMBER, EMER, CREAM,
    scene_head, info_card, chip, photo_card, an, tracked, draw_rich,
    draw_marker, draw_marker_circle, wrap_t, seg, lin, formula_card,
    matrix_table, pill, section_label, photo_note, step_card, font,
)

F_BIG = font("JetBrainsMono-var.ttf", 58)

VALS = {(0, 0): 5, (0, 1): 4, (0, 2): 5, (0, 3): 1,
        (1, 0): 5, (1, 1): 4, (1, 2): 4, (1, 3): 2,
        (2, 0): 1, (2, 1): 2, (2, 2): 1, (2, 3): 5,
        (3, 0): 2, (3, 1): 1, (3, 2): 2, (3, 3): 5}


def draw_s07(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s07c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "BIỂU DIỄN", "Ma trận người dùng – sản phẩm",
               "Hàng: người dùng · Cột: sản phẩm · Ô: điểm đánh giá")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "1.jpg", 400, 520, 520, 380, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (400, 760), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    geo = matrix_table(base, 1290, 480, seg(t, s[3] + 0.10, s[3] + 0.80),
                       VALS, missing=(1, 3), acc=CYAN)
    if geo:
        draw_rich(d, (1290, 688), "Thang điểm 1–5 · 5 = rất thích", F_NOTE,
                  MUT + (220,), "mm")
        mk = seg(t, s[5] + 0.20, s[5] + 0.80)
        if mk > 0:
            px, py = geo["missing"]
            draw_marker_circle(d, px, py, 50, 48, mk, AMBER, 5, seed=7)
    chip(base, "SVD · kỹ thuật điền ô thiếu", AMBER, 1290, 745,
         seg(t, s[6] + 0.10, s[6] + 0.50), fsize=15)
    an(base, t, "present", -1, 0.62, 1640, 1048, 1.0, FS.is_talk(t))


def draw_s08(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s08c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "THUẬT TOÁN", "Phân rã giá trị suy biến",
               "Singular Value Decomposition")
    formula_card(base, 820, 405, seg(t, s[3] + 0.10, s[3] + 0.75), 1000, AMBER,
                 "A = U · Σ · V^T", note="A: ma trận đánh giá · k: số yếu tố giữ lại",
                 fs=F_BIG)
    chip(base, "Đại số tuyến tính", CYAN, 820, 512,
         seg(t, s[2] + 0.05, s[2] + 0.45), fsize=15)
    c = seg(t, t0 + 0.20, t0 + 0.80)
    info_card(base, 330, 630, c, 400, 170, CYAN, "MA TRẬN TRÁI", "U",
              ["Người dùng × yếu tố tiềm ẩn"], "users")
    info_card(base, 790, 630, c, 400, 170, AMBER, "ĐƯỜNG CHÉO", "SIGMA",
              ["Mỗi yếu tố quan trọng bao nhiêu"], "bar-chart-3")
    info_card(base, 1250, 630, c, 400, 170, VIOLET, "MA TRẬN PHẢI", "V^T",
              ["Sản phẩm × yếu tố tiềm ẩn"], "package")
    for cid, cx, acc, seed in (("s08c4", 330, CYAN, 8), ("s08c5", 790, AMBER, 9),
                               ("s08c6", 1250, VIOLET, 10)):
        mk = seg(t, FS.ST[cid] + 0.15, FS.ST[cid] + 0.75)
        if mk > 0:
            draw_marker(d, cx - 150, 728, cx + 150, 728, mk, acc, 4, seed=seed)
    an(base, t, "present", -1, 0.62, 1620, 1048, 1.0, FS.is_talk(t))


def draw_s09(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s09c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "YẾU TỐ TIỀM ẨN", "Hệ thống tự học",
               "Không phải nhãn do con người đặt trước")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "12.jpg", 480, 556, 700, 430, p, VIOLET, mode="contain")
    if p > 0:
        draw_rich(d, (480, 802), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    old = 1 - seg(t, s[6] - 0.25, s[6] + 0.05)
    chip(base, "Thích thiết bị công nghệ", CYAN, 1330, 430,
         seg(t, s[2] + 0.10, s[2] + 0.50) * old, fsize=15)
    chip(base, "Thích phụ kiện", VIOLET, 1330, 490,
         seg(t, s[2] + 0.30, s[2] + 0.70) * old, fsize=15)
    chip(base, "Giữ ít yếu tố quan trọng nhất", AMBER, 1330, 570,
         seg(t, s[3] + 0.10, s[3] + 0.50) * old, fsize=15)
    chip(base, "Đã biết → tìm vector người dùng & sản phẩm", CYAN, 1330, 650,
         seg(t, s[4] + 0.10, s[4] + 0.50) * old, fsize=15)
    chip(base, "Nhân vector → ước lượng ô trống", EMER, 1330, 720,
         seg(t, s[5] + 0.10, s[5] + 0.50) * old, fsize=15)
    info_card(base, 1330, 520, seg(t, s[6] + 0.05, s[6] + 0.65), 600, 170,
              AMBER, "Ý TƯỞNG CỐT LÕI", "Phân rã phần đã biết",
              ["để suy ra phần chưa biết"], "lightbulb")
    an(base, t, "present", -1, 0.60, 1660, 1048, 1.0, FS.is_talk(t))


def draw_s10(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s10c{i}"] for i in range(1, 6)}
    p = seg(t, t0 + 0.10, t0 + 0.85)
    if p > 0:
        a = int(255 * p)
        tracked(d, (112, 186), "HAI YẾU TỐ", F_MICRO, AMBER + (a,), 2.4)
        d.text((112, 226), "Giữ lại k = 2", font=F_T4, fill=TXT + (a,), anchor="lm")
        d.text((112, 278), "Yếu tố 1: thiết bị · Yếu tố 2: phụ kiện", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    matrix_table(base, 620, 545, seg(t, s[1] + 0.10, s[1] + 0.80), VALS,
                 row_colors={0: CYAN, 1: CYAN, 2: VIOLET, 3: VIOLET}, acc=CYAN)
    chip(base, "k = 2 · số yếu tố giữ lại", AMBER, 620, 760,
         seg(t, s[3] + 0.10, s[3] + 0.50), fsize=15)
    info_card(base, 1380, 430, seg(t, s[4] + 0.10, s[4] + 0.75), 460, 170,
              CYAN, "YẾU TỐ 1", "Xu hướng thiết bị",
              ["An, Bình nghiêng nhóm này"], "smartphone")
    info_card(base, 1380, 640, seg(t, s[4] + 0.30, s[4] + 0.95), 460, 170,
              VIOLET, "YẾU TỐ 2", "Xu hướng phụ kiện",
              ["Chi, Dũng nghiêng nhóm này"], "headphones")
    q = seg(t, s[5] + 0.10, s[5] + 0.75)
    if q > 0:
        draw_rich(d, (1380, 762), "Cách diễn giải để dễ hiểu", F_NOTE,
                  AMBER + (int(235 * q),), "mm")
        draw_rich(d, (1380, 786), "thuật toán không tự đặt tên", F_NOTE,
                  MUT + (int(230 * q),), "mm")
    an(base, t, "present", -1, 0.56, 1660, 1048, 1.0, FS.is_talk(t))


def draw_s11(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s11c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "MA TRẬN XẤP XỈ", "Lấp các ô còn trống",
               "Sai số càng nhỏ càng tốt")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "6.jpg", 470, 556, 680, 430, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (470, 802), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    formula_card(base, 1390, 420, seg(t, s[2] + 0.05, s[2] + 0.65), 640, CYAN,
                 "R^ = U_k · Σ_k · V_k^T", fs=font("JetBrainsMono-var.ttf", 34))
    chip(base, "AirPods ≈ 4,8", EMER, 1390, 545,
         seg(t, s[5] + 0.10, s[5] + 0.50), fsize=18)
    chip(base, "Tai nghe Sony ≈ 4,6", CYAN, 1390, 610,
         seg(t, s[5] + 0.30, s[5] + 0.70), fsize=18)
    q = seg(t, s[6] + 0.10, s[6] + 0.75)
    if q > 0:
        lines = wrap_t("Điểm minh họa · kết quả phụ thuộc dữ liệu và cách huấn luyện.",
                       F_NOTE, 600)
        yy = 692
        for ln in lines:
            draw_rich(d, (1390, yy), ln, F_NOTE, MUT + (int(225 * q),), "mm")
            yy += 26
    an(base, t, "present", -1, 0.52, 1710, 1048, 1.0, FS.is_talk(t))


STEPS = [
    ("01", ["Thu thập", "dữ liệu tương tác"], CYAN),
    ("02", ["Xây dựng", "ma trận"], CYAN),
    ("03", ["Huấn luyện", "tìm vector"], AMBER),
    ("04", ["Dự đoán", "điểm"], VIOLET),
    ("05", ["Xếp hạng", "Top N"], EMER),
]


def draw_s12(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s12c{i}"] for i in range(1, 8)}
    scene_head(base, t, t0, "QUY TRÌNH", "Năm bước",
               "Từ dữ liệu thô đến danh sách gợi ý")
    for i, (num, lines, acc) in enumerate(STEPS):
        step_card(base, 252 + 294 * i, 390, seg(t, s[1] + 0.15 + i * 0.12, s[1] + 0.45 + i * 0.12),
                  acc, num, lines, 288, 104)
    formula_card(base, 800, 580, seg(t, s[5] + 0.05, s[5] + 0.65), 1150, AMBER,
                 "r^ = μ + b_u + b_i + q_i^T · p_u",
                 fs=font("JetBrainsMono-var.ttf", 40))
    q = seg(t, s[6] + 0.05, s[6] + 0.70)
    if q > 0:
        for i, text in enumerate((
                "trung bình chung · b_u, b_i: độ lệch người dùng / sản phẩm",
                "p_u, q_i: vector tiềm ẩn của người dùng và sản phẩm")):
            draw_rich(d, (800, 678 + i * 28), text, F_NOTE,
                      MUT + (int(235 * q),), "mm")
    chip(base, "q_i^T · p_u = mức tương thích", EMER, 800, 762,
         seg(t, s[7] + 0.10, s[7] + 0.50), fsize=16)
    an(base, t, "present", -1, 0.55, 1660, 1048, 1.0, FS.is_talk(t))
