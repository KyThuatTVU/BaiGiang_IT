# -*- coding: utf-8 -*-
"""Cảnh S01–S06."""
from full_common import *  # noqa
from full_common import (scene_title, mini_card, formula_card, stat_card,
                         caveat, mono, jak, F_MONO)
from PIL import Image, ImageDraw

PHOTO01 = "01_khai_niem_duong_hoi_quy.png"
PHOTO10 = "10_hoi_quy_vs_phan_loai.png"
PHOTO02 = "02_he_so_goc_va_chieu_tuong_quan.png"


# ---------------- S01 ----------------
def s01(base, t, G):
    ST = G.ST
    d = ImageDraw.Draw(base)
    p = seg(t, 0.45, 1.25)
    if p > 0:
        a = int(255 * p)
        dy = int((1 - p) * 22)
        tracked(d, (112, 252 + dy), "MACHINE LEARNING · BÀI GIẢNG", F_MICRO,
                AMBER + (a,), 2.4)
        d.text((112, 334 + dy), "Hồi quy", font=F_T1, fill=TXT + (a,), anchor="lm")
        d.text((112, 424 + dy), "tuyến tính", font=F_T1, fill=TXT + (a,), anchor="lm")
        d.text((112, 518 + dy), "Dự đoán một con số", font=F_SUB2, fill=MUT + (a,), anchor="lm")
        d.text((112, 554 + dy), "từ dữ liệu trong quá khứ.", font=F_SUB2,
               fill=MUT + (a,), anchor="lm")
    mp = seg(t, 1.15, 2.05)
    if mp > 0:
        draw_marker(d, 120, 470, 512, 470, mp, AMBER, 6, seed=3)
    for i, (sid, icon, acc, kick, ttl) in enumerate((
            ("s01c3", "trending-up", CYAN, "BÁN LẺ", "Ngày mai bán được bao nhiêu?"),
            ("s01c4", "building-2", EMER, "BẤT ĐỘNG SẢN", "Căn nhà này giá bao nhiêu?"),
            ("s01c5", "target", VIOLET, "DỮ LIỆU QUÁ KHỨ", "Cần ước lượng một con số"))):
        qp = seg(t, ST[sid] + 0.12, ST[sid] + 0.62)
        qcard(base, 1150, 300 + 170 * i, qp, acc, icon, kick, ttl)
    pose = "wave" if t < ST["s01c2"] else "present"
    an(base, t, pose, -1, 0.82, 1620, 1048, seg(t, 0.8, 1.5), G.is_talk(t))


# ---------------- S02 ----------------
def s02(base, t, G):
    ST = G.ST
    d = ImageDraw.Draw(base)
    pc = seg(t, ST["s02c1"] + 0.25, ST["s02c1"] + 1.15)
    photo_card(base, PHOTO01, 640, 545, 820, 456, pc, CYAN)
    if pc > 0:
        draw_rich(d, (640, 814), "Minh họa: 20 căn nhà giả định", F_NOTE,
                  MUT + (int(210 * pc),), "mm")
    p = seg(t, G.S[2] + 0.15, G.S[2] + 0.95)
    if p > 0:
        a = int(255 * p)
        tracked(d, (1130, 208), "KHÁI NIỆM", F_MICRO, AMBER + (a,), 2.4)
        d.text((1130, 250), "Hồi quy tuyến tính", font=F_T2, fill=TXT + (a,), anchor="lm")
        d.text((1130, 302), "là gì?", font=F_T2, fill=TXT + (a,), anchor="lm")
    bullet(base, 1430, 392, seg(t, ST["s02c1"] + 0.20, ST["s02c1"] + 0.70),
           CYAN, "users", "Học có giám sát", "Supervised Learning")
    bullet(base, 1430, 466, seg(t, ST["s02c2"] + 0.10, ST["s02c2"] + 0.60),
           EMER, "layers", "Đầu vào · kết quả dạng số", "Feature và Target")
    bullet(base, 1430, 540, seg(t, ST["s02c3"] + 0.10, ST["s02c3"] + 0.60),
           VIOLET, "workflow", "Học công thức từ dữ liệu", "rồi dự đoán trường hợp mới")
    chip(base, "Linear Regression", CYAN, 1250, 622,
         seg(t, ST["s02c1"] + 0.50, ST["s02c1"] + 0.90), fsize=16)
    chip(base, "Supervised Learning", VIOLET, 1530, 622,
         seg(t, ST["s02c1"] + 0.50, ST["s02c1"] + 0.90), fsize=16)
    chip(base, "Machine Learning", AMBER, 1245, 704,
         seg(t, ST["s02c5"] + 0.18, ST["s02c5"] + 0.58), fsize=16)
    chip(base, "Diện tích tăng · giá thường tăng", EMER, 1340, 776,
         seg(t, ST["s02c6"] + 0.22, ST["s02c6"] + 0.62), fsize=15)
    mk = seg(t, ST["s02c1"] + 0.55, ST["s02c1"] + 1.35)
    if mk > 0:
        draw_marker(d, 1142, 650, 1358, 650, mk, CYAN, 4, seed=5)
    an(base, t, "present", -1, 0.70, 1655, 1048, 1.0, G.is_talk(t))


# ---------------- S03 ----------------
SLOTS = [
    ("Feature", "X · biến đầu vào", 300, 450, "s03c2", CYAN, "01 · ĐẦU VÀO"),
    ("Target", "Y · cần dự đoán", 680, 450, "s03c3", EMER, "02 · MỤC TIÊU"),
    ("Training data", "cặp X, Y đã biết", 1060, 450, "s03c4", AMBER, "03 · DỮ LIỆU"),
    ("y", "giá trị thực tế", 1440, 450, "s03c5", CYAN, "04 · THỰC TẾ"),
    ("y mũ", "giá trị dự đoán", 490, 650, "s03c5", VIOLET, "05 · DỰ ĐOÁN"),
    ("Coefficient", "mức & chiều liên hệ", 870, 650, "s03c6", EMER, "06 · HỆ SỐ"),
    ("Residual", "y − ŷ", 1250, 650, "s03c7", VIOLET, "07 · PHẦN DƯ"),
]


def active_slot(base, label, sub, kicker, cx, cy, p, acc):
    if p <= 0:
        return
    im, pad = card_base(330, 150, acc)
    im = im.copy()
    d = ImageDraw.Draw(im)
    tracked(d, (pad + 24, pad + 22), kicker, F_MICRO, acc + (235,), 1.8)
    draw_rich(d, (pad + 24, pad + 48), label, F_FEAT, TXT + (255,), "lm")
    draw_rich(d, (pad + 24, pad + 98), sub, F_FEAT_SUB, MUT + (255,), "lm")
    blit(base, im, cx, cy, p, 14)


def s03(base, t, G):
    ST = G.ST
    s0 = G.S[3]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "TỪ VỰNG", "Thuật ngữ cốt lõi",
                "7 khái niệm cần nắm trước khi vào công thức.")
    p = seg(t, s0 + 0.15, s0 + 0.95)
    if p > 0:
        pill = Image.new("RGBA", (280, 42), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pill)
        pd.rounded_rectangle([0, 0, 279, 41], 21, fill=(9, 14, 26, 235),
                             outline=AMBER + (160,), width=1)
        pd.ellipse([18, 17, 26, 25], fill=AMBER + (255,))
        tracked(pd, (38, 21), "07 THUẬT NGỮ", F_PILL, TXT + (240,), 1.5)
        blit(base, pill, 1700, 240, p, 10)
    for i, (label, sub, cx, cy, sid, acc, kick) in enumerate(SLOTS):
        dp = seg(t, s0 + 0.35 + i * 0.07, s0 + 0.75 + i * 0.07)
        cp = seg(t, ST[sid] + 0.10, ST[sid] + 0.55)
        if cp > 0:
            active_slot(base, label, sub, kick, cx, cy, cp, acc)
        else:
            dim_slot(base, cx, cy, dp, label)
    bp = seg(t, ST["s03c5"] + 2.0, ST["s03c5"] + 2.6)
    formula_card(base, 960, 812, 460, 74, bp, AMBER, "e = y − ŷ", fs=30,
                 note=None)
    rp = seg(t, ST["s03c7"] + 0.55, ST["s03c7"] + 1.25)
    if rp > 0:
        draw_marker_circle(d, 1250, 650, 198, 114, rp, VIOLET, 5, seed=4)
    an(base, t, "present", -1, 0.66, 1672, 1048, 1.0, G.is_talk(t))


# ---------------- S04 ----------------
def s04(base, t, G):
    ST = G.ST
    s0 = G.S[4]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "PHÂN BIỆT", "Hồi quy hay phân loại?",
                "Nhìn vào kiểu kết quả cần dự đoán.")
    pc = seg(t, ST["s04c1"] + 0.25, ST["s04c1"] + 1.10)
    photo_card(base, PHOTO10, 610, 570, 800, 350, pc, VIOLET)
    if pc > 0:
        draw_rich(d, (610, 772), "Minh họa: hồi quy (trái) · phân loại (phải)",
                  F_NOTE, MUT + (int(205 * pc),), "mm")
    mini_card(base, 1400, 440, 580, 180,
              seg(t, ST["s04c1"] + 0.15, ST["s04c1"] + 0.70),
              CYAN, "HỒI QUY", "Dự đoán một số liên tục",
              "Ví dụ: giá 2,1 tỷ · doanh thu · nhiệt độ", icon="trending-up",
              tfs=24, sfs=16)
    mini_card(base, 1400, 650, 580, 180,
              seg(t, ST["s04c2"] + 0.15, ST["s04c2"] + 0.70),
              VIOLET, "PHÂN LOẠI", "Dự đoán một nhãn",
              "Ví dụ: thấp / trung bình / cao · spam", icon="layers",
              tfs=24, sfs=16)
    caveat(base, 1200, 808, seg(t, ST["s04c5"] + 0.15, ST["s04c5"] + 0.65),
           "Nhìn vào kiểu kết quả cần dự đoán", CYAN)
    an(base, t, "point_left", -1, 0.58, 1700, 1048, 1.0, G.is_talk(t))


# ---------------- S05 ----------------
def s05(base, t, G):
    ST = G.ST
    s0 = G.S[5]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "ĐỌC BIỂU ĐỒ", "Dấu của hệ số góc",
                "Mỗi chấm là một quan sát; độ dốc cho biết chiều liên hệ.")
    pc = seg(t, ST["s05c1"] + 0.20, ST["s05c1"] + 1.10)
    photo_card(base, PHOTO02, 650, 545, 960, 350, pc, CYAN)
    if pc > 0:
        draw_rich(d, (650, 742), "Minh họa: ba kiểu xu hướng trên biểu đồ phân tán",
                  F_NOTE, MUT + (int(205 * pc),), "mm")
    chip(base, "dốc lên", EMER, 380, 800, seg(t, ST["s05c2"] + 0.12, ST["s05c2"] + 0.52), fsize=15)
    chip(base, "dốc xuống", AMBER, 650, 800, seg(t, ST["s05c3"] + 0.10, ST["s05c3"] + 0.50), fsize=15)
    chip(base, "gần ngang", VIOLET, 920, 800, seg(t, ST["s05c4"] + 0.12, ST["s05c4"] + 0.52), fsize=15)
    bullet(base, 1430, 392, seg(t, ST["s05c1"] + 0.12, ST["s05c1"] + 0.52),
           CYAN, "scan", "Mỗi chấm", "một quan sát")
    bullet(base, 1430, 460, seg(t, ST["s05c2"] + 0.10, ST["s05c2"] + 0.50),
           EMER, "trending-up", "Dốc lên", "hệ số góc dương")
    bullet(base, 1430, 528, seg(t, ST["s05c3"] + 0.08, ST["s05c3"] + 0.48),
           AMBER, "trending-up", "Dốc xuống", "hệ số góc âm")
    bullet(base, 1430, 596, seg(t, ST["s05c4"] + 0.10, ST["s05c4"] + 0.50),
           VIOLET, "scan", "Gần ngang", "góc ≈ 0, chưa chắc rời nhau")
    draw_rich(d, (1430, 672), "Góc ≈ 0 có thể là quan hệ phi tuyến.",
              font("BeVietnamPro-Regular.ttf", 17), MUT + (int(235 * seg(t, ST["s05c5"] + 0.12, ST["s05c5"] + 0.55)),), "mm")
    caveat(base, 720, 862, seg(t, ST["s05c6"] + 0.12, ST["s05c6"] + 0.62),
           "Tương quan không chứng minh nhân quả", AMBER)
    draw_rich(d, (1430, 716), "Yếu tố thứ ba có thể tác động cả hai biến.",
              font("BeVietnamPro-Regular.ttf", 17), MUT + (int(235 * seg(t, ST["s05c7"] + 0.10, ST["s05c7"] + 0.55)),), "mm")
    an(base, t, "point_right", -1, 0.55, 1690, 1048, 1.0, G.is_talk(t))


# ---------------- S06 ----------------
def s06(base, t, G):
    ST = G.ST
    s0 = G.S[6]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "CÔNG THỨC", "Mô hình và công thức dự đoán",
                "Từ mô hình tổng thể đến công thức ước lượng từ dữ liệu.")
    formula_card(base, 960, 425, 980, 170,
                 seg(t, ST["s06c1"] + 0.20, ST["s06c1"] + 1.10), AMBER,
                 "Y = β₀ + β₁·X + ε", fs=58,
                 note="hệ số chặn · hệ số góc · sai số")
    formula_card(base, 700, 590, 760, 140,
                 seg(t, ST["s06c2"] + 0.15, ST["s06c2"] + 0.90), CYAN,
                 "ŷ = b₀ + b₁·x", fs=54)
    mk = seg(t, ST["s06c3"] + 0.15, ST["s06c3"] + 0.85)
    if mk > 0:
        draw_marker(d, 380, 664, 1020, 664, mk, CYAN, 5, seed=6)
    mini_card(base, 420, 745, 420, 120, seg(t, ST["s06c4"] + 0.12, ST["s06c4"] + 0.60),
              EMER, "b0 · HỆ SỐ CHẶN", "Giá trị khi X = 0", None, tfs=22)
    mini_card(base, 900, 745, 420, 120, seg(t, ST["s06c5"] + 0.12, ST["s06c5"] + 0.60),
              EMER, "b1 · HỆ SỐ GÓC", "Y đổi khi X tăng 1", None, tfs=22)
    mini_card(base, 1480, 600, 520, 90, seg(t, ST["s06c6"] + 0.15, ST["s06c6"] + 0.65),
              VIOLET, None, "ŷ = 0,5 + 0,02·x", None, tfs=22)
    caveat(base, 1480, 712, seg(t, ST["s06c7"] + 0.15, ST["s06c7"] + 0.65),
           "x +1 m² → giá +~20 triệu", AMBER)
    an(base, t, "write", -1, 0.58, 1710, 1048, 1.0, G.is_talk(t))


SCENES = {1: s01, 2: s02, 3: s03, 4: s04, 5: s05, 6: s06}
