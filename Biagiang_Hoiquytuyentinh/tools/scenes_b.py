# -*- coding: utf-8 -*-
"""Cảnh S07–S12."""
from full_common import *  # noqa
from full_common import (scene_title, mini_card, formula_card, stat_card,
                         caveat, mono, jak)
from PIL import Image, ImageDraw

PHOTO04 = "04_binh_phuong_toi_thieu.png"
PHOTO03 = "03_phan_du_residual.png"
PHOTO06 = "06_so_do_hoi_quy_da_bien.png"
PHOTO05 = "05_cac_dang_hoi_quy.png"
PHOTO07 = "07_quy_trinh_xay_dung_mo_hinh.png"


def step_row(base, cx, cy, p, acc, num, label, w=620, h=56):
    if p <= 0:
        return
    im, pad = shadow_card(w, h, 14, (255, 255, 255, 26), (17, 26, 45, 238))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 10, pad + 10, pad + 46, pad + 46], 10,
                        fill=acc + (30,), outline=acc + (120,), width=1)
    d.text((pad + 28, pad + 28), str(num), font=jak(20, 700), fill=acc + (255,), anchor="mm")
    draw_rich(d, (pad + 66, pad + h // 2), label, font("BeVietnamPro-SemiBold.ttf", 20),
              TXT + (240,), "lm")
    blit(base, im, cx, cy, p, 8)


def stat_row(base, cx, cy, p, acc, label, value, w=760, h=62):
    if p <= 0:
        return
    im, pad = shadow_card(w, h, 12, (255, 255, 255, 24), (17, 26, 45, 240))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 1, pad + 1, pad + 8, pad + h - 1], 3, fill=acc + (220,))
    draw_rich(d, (pad + 26, pad + h // 2), label, font("BeVietnamPro-Medium.ttf", 18),
              MUT + (240,), "lm")
    draw_rich(d, (pad + w - 26, pad + h // 2), value, mono(22), TXT + (255,), "rm")
    blit(base, im, cx, cy, p, 8)


# ---------------- S07 ----------------
def s07(base, t, G):
    ST = G.ST
    s0 = G.S[7]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "OLS", "Vì sao bình phương phần dư?",
                "Chọn đường có tổng bình phương phần dư nhỏ nhất.")
    pc = seg(t, ST["s07c1"] + 0.20, ST["s07c1"] + 1.10)
    photo_card(base, PHOTO04, 1400, 560, 800, 331, pc, AMBER)
    if pc > 0:
        draw_rich(d, (1400, 748), "Minh họa: đo phần dư theo chiều dọc",
                  F_NOTE, MUT + (int(205 * pc),), "mm")
    mini_card(base, 520, 400, 820, 82, seg(t, ST["s07c3"] + 0.10, ST["s07c3"] + 0.55),
              CYAN, "BƯỚC 1", "Phần dư = y − ŷ, đo theo chiều dọc", None, tfs=20, kfs=11)
    mini_card(base, 520, 495, 820, 82, seg(t, ST["s07c4"] + 0.10, ST["s07c4"] + 0.55),
              EMER, "BƯỚC 2", "Cộng có dấu → dương và âm triệt tiêu", None, tfs=20, kfs=11)
    mini_card(base, 520, 590, 820, 82, seg(t, ST["s07c5"] + 0.10, ST["s07c5"] + 0.55),
              VIOLET, "BƯỚC 3", "Bình phương từng phần dư rồi cộng lại", None, tfs=20, kfs=11)
    formula_card(base, 520, 690, 820, 84, seg(t, ST["s07c5"] + 1.35, ST["s07c5"] + 1.90),
                 CYAN, "SSE = Σ e²", fs=30)
    caveat(base, 520, 775, seg(t, ST["s07c6"] + 0.12, ST["s07c6"] + 0.55),
           "Sai số lớn bị phạt mạnh hơn", AMBER)
    chip(base, "Chọn SSE nhỏ nhất", EMER, 520, 838,
         seg(t, ST["s07c7"] + 0.15, ST["s07c7"] + 0.65), fsize=15)
    an(base, t, "point_left", -1, 0.55, 1740, 1048, 1.0, G.is_talk(t))


# ---------------- S08 ----------------
def s08(base, t, G):
    ST = G.ST
    s0 = G.S[8]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "VÍ DỤ", "Tính tay với 5 căn nhà",
                "Dữ liệu giả định, đơn vị: diện tích m² và giá tỷ đồng.")
    tp = seg(t, ST["s08c1"] + 0.25, ST["s08c1"] + 1.10)
    if tp > 0:
        im, pad = card_base(620, 440, AMBER)
        im = im.copy()
        td = ImageDraw.Draw(im)
        draw_rich(td, (pad + 40, pad + 36), "Diện tích x", font("BeVietnamPro-SemiBold.ttf", 19),
                  MUT + (240,), "lm")
        draw_rich(td, (pad + 400, pad + 36), "Giá y", font("BeVietnamPro-SemiBold.ttf", 19),
                  MUT + (240,), "lm")
        td.line([pad + 40, pad + 62, pad + 580, pad + 62], fill=(255, 255, 255, 34), width=1)
        xs = ["60", "70", "80", "90", "100"]
        ys = ["1,55", "1,72", "2,05", "2,15", "2,48"]
        for i in range(5):
            yy = pad + 92 + i * 58
            if t >= ST["s08c2"] + 0.10 + i * 0.06:
                draw_rich(td, (pad + 40, yy), xs[i] + " m²", jak(24, 600), TXT + (250,), "lm")
            if t >= ST["s08c3"] + 0.10 + i * 0.12:
                draw_rich(td, (pad + 400, yy), ys[i], jak(24, 700), TXT + (250,), "lm")
            if i < 4:
                td.line([pad + 40, yy + 28, pad + 580, yy + 28], fill=(255, 255, 255, 20), width=1)
        blit(base, im, 420, 610, tp, 14)
    stat_row(base, 1280, 380, seg(t, ST["s08c4"] + 0.10, ST["s08c4"] + 0.50),
             CYAN, "x trung bình", "80 m²")
    stat_row(base, 1280, 448, seg(t, ST["s08c4"] + 0.18, ST["s08c4"] + 0.58),
             CYAN, "y trung bình", "1,99 tỷ")
    stat_row(base, 1280, 516, seg(t, ST["s08c5"] + 0.10, ST["s08c5"] + 0.50),
             EMER, "Tổng (x−80)(y−1,99)", "22,9")
    stat_row(base, 1280, 584, seg(t, ST["s08c6"] + 0.10, ST["s08c6"] + 0.50),
             EMER, "Tổng (x−80)²", "1000")
    stat_row(base, 1280, 652, seg(t, ST["s08c7"] + 0.10, ST["s08c7"] + 0.50),
             VIOLET, "b1", "0,0229")
    stat_row(base, 1280, 720, seg(t, ST["s08c8"] + 0.10, ST["s08c8"] + 0.50),
             AMBER, "b0", "0,158")
    an(base, t, "write", -1, 0.58, 1710, 1048, 1.0, G.is_talk(t))


# ---------------- S09 ----------------
def s09(base, t, G):
    ST = G.ST
    s0 = G.S[9]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "ÁP DỤNG", "Phương trình và dự đoán",
                "Thay diện tích vào công thức, rồi đọc phần dư.")
    formula_card(base, 660, 400, 1100, 130,
                 seg(t, ST["s09c1"] + 0.20, ST["s09c1"] + 1.10), CYAN,
                 "ŷ = 0,158 + 0,0229·x", fs=46)
    stat_card(base, 430, 555, 560, 150,
              seg(t, ST["s09c2"] + 0.15, ST["s09c2"] + 0.80), EMER,
              "85 M² DỰ ĐOÁN", "2,1045 tỷ", fs=44)
    stat_card(base, 1000, 555, 460, 150,
              seg(t, ST["s09c5"] + 0.10, ST["s09c5"] + 0.65), VIOLET,
              "PHẦN DƯ", "+0,018 … −0,069", fs=28)
    pc = seg(t, ST["s09c3"] + 0.20, ST["s09c3"] + 1.05)
    photo_card(base, PHOTO03, 1500, 560, 520, 290, pc, VIOLET)
    if pc > 0:
        draw_rich(d, (1500, 730), "Minh họa: phần dư từng căn nhà",
                  F_NOTE, MUT + (int(205 * pc),), "mm")
    draw_rich(d, (430, 690), "Dư dương: dự đoán thấp hơn thực tế.",
              font("BeVietnamPro-Medium.ttf", 19),
              CYAN + (int(240 * seg(t, ST["s09c4"] + 0.10, ST["s09c4"] + 0.50)),), "lm")
    draw_rich(d, (430, 728), "Dư âm: dự đoán cao hơn thực tế.",
              font("BeVietnamPro-Medium.ttf", 19),
              AMBER + (int(240 * seg(t, ST["s09c5"] + 0.12, ST["s09c5"] + 0.55)),), "lm")
    caveat(base, 560, 800, seg(t, ST["s09c6"] + 0.12, ST["s09c6"] + 0.60),
           "Dữ liệu học tập, không phải giá thị trường", AMBER)
    draw_rich(d, (560, 852), "Sai số chỉ mô tả mô hình, không phải quy luật chung.",
              font("BeVietnamPro-Regular.ttf", 16),
              MUT + (int(230 * seg(t, ST["s09c7"] + 0.12, ST["s09c7"] + 0.60)),), "mm")
    an(base, t, "point_right", -1, 0.55, 1700, 1048, 1.0, G.is_talk(t))


# ---------------- S10 ----------------
def s10(base, t, G):
    ST = G.ST
    s0 = G.S[10]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "MỞ RỘNG", "Hồi quy tuyến tính đa biến",
                "Nhiều đầu vào, vẫn một công thức tuyến tính.")
    formula_card(base, 770, 408, 1160, 150,
                 seg(t, ST["s10c2"] + 0.15, ST["s10c2"] + 1.00), VIOLET,
                 "ŷ = b₀ + b₁x₁ + b₂x₂ + … + b_p x_p", fs=38)
    mk = seg(t, ST["s10c3"] + 0.15, ST["s10c3"] + 0.85)
    if mk > 0:
        draw_marker(d, 640, 452, 900, 452, mk, VIOLET, 4, seed=7)
    photo_card(base, PHOTO06, 470, 665, 540, 306,
               seg(t, ST["s10c1"] + 0.25, ST["s10c1"] + 1.10), CYAN)
    mini_card(base, 1560, 420, 520, 66, seg(t, ST["s10c1"] + 0.15, ST["s10c1"] + 0.55),
              CYAN, None, "Diện tích · x1", None, tfs=20)
    mini_card(base, 1560, 492, 520, 66, seg(t, ST["s10c1"] + 0.25, ST["s10c1"] + 0.65),
              EMER, None, "Số phòng · x2", None, tfs=20)
    mini_card(base, 1560, 564, 520, 66, seg(t, ST["s10c1"] + 0.35, ST["s10c1"] + 0.75),
              AMBER, None, "Khoảng cách · x3", None, tfs=20)
    mini_card(base, 1460, 690, 520, 100, seg(t, ST["s10c4"] + 0.12, ST["s10c4"] + 0.65),
              VIOLET, "DIỄN GIẢI", "Giữ các biến khác cố định", None, tfs=21)
    mk2 = seg(t, ST["s10c5"] + 0.15, ST["s10c5"] + 0.85)
    if mk2 > 0:
        draw_marker(d, 1210, 745, 1710, 745, mk2, AMBER, 4, seed=8)
    an(base, t, "point_right", -1, 0.55, 1710, 1048, 1.0, G.is_talk(t))


# ---------------- S11 ----------------
def s11(base, t, G):
    ST = G.ST
    s0 = G.S[11]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "MỞ RỘNG", "Hồi quy đa thức",
                "Đường cong, nhưng vẫn tuyến tính theo hệ số.")
    photo_card(base, PHOTO05, 700, 520, 980, 351,
               seg(t, ST["s11c1"] + 0.20, ST["s11c1"] + 1.05), EMER)
    mini_card(base, 1440, 560, 480, 120, seg(t, ST["s11c4"] + 0.12, ST["s11c4"] + 0.65),
              EMER, "VẪN TUYẾN TÍNH", "Đường cong, hệ số tuyến tính", None, tfs=20)
    formula_card(base, 700, 745, 560, 90, seg(t, ST["s11c2"] + 0.15, ST["s11c2"] + 0.65),
                 CYAN, "ŷ = b₀ + b₁x + b₂x²", fs=28)
    caveat(base, 1440, 690, seg(t, ST["s11c5"] + 0.12, ST["s11c5"] + 0.60),
           "Bậc cao dễ bám nhiễu", AMBER)
    draw_rich(d, (700, 828), "Kiểm tra trước khi tin: dữ liệu chưa thấy.",
              font("BeVietnamPro-Regular.ttf", 17),
              MUT + (int(230 * seg(t, ST["s11c5"] + 0.55, ST["s11c5"] + 1.05)),), "mm")
    an(base, t, "point_left", -1, 0.58, 1690, 1048, 1.0, G.is_talk(t))


# ---------------- S12 ----------------
STEPS = [("Thu thập dữ liệu", CYAN), ("Làm sạch, khám phá", CYAN),
         ("Chia train / test", EMER), ("Huấn luyện mô hình", EMER),
         ("Đánh giá hiệu suất", VIOLET), ("Dự đoán, theo dõi", VIOLET)]


def s12(base, t, G):
    ST = G.ST
    s0 = G.S[12]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "THỰC TẾ", "Quy trình 6 bước",
                "Từ dữ liệu thô đến dự đoán và theo dõi.")
    photo_card(base, PHOTO07, 1270, 550, 970, 369,
               seg(t, ST["s12c1"] + 0.20, ST["s12c1"] + 1.05), CYAN)
    starts = [ST["s12c2"] + 0.10, ST["s12c2"] + 0.55, ST["s12c3"] + 0.10,
              ST["s12c3"] + 0.55, ST["s12c4"] + 0.10, ST["s12c4"] + 0.55]
    for i, (label, acc) in enumerate(STEPS):
        step_row(base, 430, 390 + i * 65, seg(t, starts[i], starts[i] + 0.40),
                 acc, i + 1, label)
    caveat(base, 430, 792, seg(t, ST["s12c6"] + 0.12, ST["s12c6"] + 0.60),
           "Ngoại lệ: lỗi hay trường hợp thật?", AMBER)
    chip(base, "Quan hệ đổi → huấn luyện lại", VIOLET, 430, 850,
         seg(t, ST["s12c7"] + 0.15, ST["s12c7"] + 0.65), fsize=15)
    an(base, t, "present", -1, 0.55, 1720, 1048, 1.0, G.is_talk(t))


SCENES = {7: s07, 8: s08, 9: s09, 10: s10, 11: s11, 12: s12}
