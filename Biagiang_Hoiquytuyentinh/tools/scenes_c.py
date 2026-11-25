# -*- coding: utf-8 -*-
"""Cảnh S13–S18."""
from full_common import *  # noqa
from full_common import (scene_title, mini_card, formula_card, stat_card,
                         caveat, cross_claim, mono, jak, CODE_LINES, code_card)
from PIL import Image, ImageDraw

PHOTO09 = "09_chia_train_test.png"
PHOTO08 = "08_danh_gia_mae_rmse.png"
PHOTO11 = "11_poster_tong_quan.png"


# ---------------- S13 ----------------
def s13(base, t, G):
    ST = G.ST
    s0 = G.S[13]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "KIỂM CHỨNG", "Chia tập train / test",
                "Học trên một tập, chấm điểm trên tập chưa từng thấy.")
    photo_card(base, PHOTO09, 1450, 540, 640, 224,
               seg(t, ST["s13c2"] + 0.30, ST["s13c2"] + 1.10), CYAN)
    mini_card(base, 560, 392, 840, 80, seg(t, ST["s13c1"] + 0.15, ST["s13c1"] + 0.65),
              AMBER, "CẢNH BÁO", "Học và chấm cùng tập → kết quả lạc quan", None,
              tfs=20, kfs=11)
    draw_rich(d, (560, 466), "Chia dữ liệu thành hai tập:",
              font("BeVietnamPro-SemiBold.ttf", 20),
              EMER + (int(240 * seg(t, ST["s13c2"] + 0.10, ST["s13c2"] + 0.50)),), "mm")
    stat_card(base, 390, 560, 460, 130, seg(t, ST["s13c3"] + 0.12, ST["s13c3"] + 0.70),
              CYAN, "TẬP HUẤN LUYỆN", "80%", fs=46)
    stat_card(base, 870, 560, 460, 130, seg(t, ST["s13c3"] + 0.24, ST["s13c3"] + 0.82),
              EMER, "TẬP KIỂM TRA", "20%", fs=46)
    draw_rich(d, (560, 688), "Tỷ lệ chỉ là ví dụ — tùy quy mô và đặc điểm dữ liệu.",
              font("BeVietnamPro-Regular.ttf", 18),
              MUT + (int(235 * seg(t, ST["s13c4"] + 0.12, ST["s13c4"] + 0.55)),), "mm")
    draw_rich(d, (560, 742), "Chuỗi thời gian: không trộn tương lai vào quá khứ.",
              font("BeVietnamPro-Medium.ttf", 17),
              AMBER + (int(235 * seg(t, ST["s13c5"] + 0.12, ST["s13c5"] + 0.55)),), "mm")
    caveat(base, 560, 800, seg(t, ST["s13c5"] + 0.50, ST["s13c5"] + 1.00),
           "Chia theo thời gian, không trộn lẫn", AMBER)
    an(base, t, "point_left", -1, 0.55, 1710, 1048, 1.0, G.is_talk(t))


# ---------------- S14 ----------------
METRICS = [
    ("s14c2", CYAN, "MAE", "Sai số tuyệt đối trung bình"),
    ("s14c3", EMER, "MSE", "Bình phương trước, rồi lấy trung bình"),
    ("s14c4", VIOLET, "RMSE", "Căn bậc hai của MSE"),
    ("s14c5", AMBER, "R²", "Mức mô hình giải thích biến thiên của Y"),
]


def s14(base, t, G):
    ST = G.ST
    s0 = G.S[14]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "CHỈ SỐ", "Đọc kết quả đúng cách",
                "Bốn chỉ số, bốn góc nhìn — đừng chỉ nhìn một con số.")
    photo_card(base, PHOTO08, 1390, 500, 700, 310,
               seg(t, ST["s14c1"] + 0.20, ST["s14c1"] + 1.00), VIOLET)
    pos = [(350, 415), (760, 415), (350, 590), (760, 590)]
    for (cid, acc, name, desc), (cx, cy) in zip(METRICS, pos):
        mini_card(base, cx, cy, 380, 150, seg(t, ST[cid] + 0.12, ST[cid] + 0.62),
                  acc, name, desc, None, tfs=20, kfs=13)
    caveat(base, 1390, 720, seg(t, ST["s14c1"] + 0.55, ST["s14c1"] + 1.00),
           "Đừng kết luận bằng một con số", AMBER)
    draw_rich(d, (560, 728), "Ví dụ: MAE ≈ 0,044 tỷ", jak(19, 600),
              CYAN + (int(240 * seg(t, ST["s14c6"] + 0.12, ST["s14c6"] + 0.55)),), "mm")
    draw_rich(d, (560, 766), "RMSE ≈ 0,0477  ·  R² ≈ 0,9787", jak(19, 600),
              VIOLET + (int(240 * seg(t, ST["s14c7"] + 0.12, ST["s14c7"] + 0.60)),), "mm")
    caveat(base, 560, 838, seg(t, ST["s14c8"] + 0.15, ST["s14c8"] + 0.70),
           "Chỉ 5 mẫu, không có test: chưa phải bằng chứng", AMBER)
    an(base, t, "point_left", -1, 0.55, 1700, 1048, 1.0, G.is_talk(t))


# ---------------- S15 ----------------
KNOW = [
    ("s15c2", EMER, "GIẢ ĐỊNH", "Quan hệ gần tuyến tính, sai số độc lập"),
    ("s15c3", EMER, "NGOẠI LỆ", "Ngoại lệ mạnh kéo đường lệch hẳn"),
    ("s15c4", AMBER, "ĐA CỘNG TUYẾN", "Hệ số khó diễn giải"),
    ("s15c4", AMBER, "RÒ RỈ DỮ LIỆU", "Kết quả ảo, không tái lập được"),
    ("s15c5", VIOLET, "NGOẠI SUY", "Quá xa vùng dữ liệu: rất rủi ro"),
]
WRONG = [
    ("s15c6", "Đường hồi quy phải đi qua mọi điểm"),
    ("s15c7", "R² cao là mô hình tốt"),
    ("s15c8", "Càng nhiều dữ liệu càng tốt"),
]


def s15(base, t, G):
    ST = G.ST
    s0 = G.S[15]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "GIỚI HẠN", "Cần biết và hiểu đúng",
                "Giả định, giới hạn — và những hiểu sai thường gặp.")
    pa = seg(t, ST["s15c1"] + 0.20, ST["s15c1"] + 0.70)
    if pa > 0:
        tracked(d, (140, 340), "CẦN BIẾT", F_MICRO, EMER + (int(235 * pa),), 2.4)
        tracked(d, (1130, 340), "HIỂU SAI", F_MICRO, RED + (int(235 * pa),), 2.4)
    for i, (cid, acc, kicker, title) in enumerate(KNOW):
        mini_card(base, 460, 384 + i * 92, 640, 84,
                  seg(t, ST[cid] + 0.10 + i * 0.05, ST[cid] + 0.55 + i * 0.05),
                  acc, kicker, title, None, tfs=19, kfs=11)
    for i, (cid, title) in enumerate(WRONG):
        p = seg(t, ST[cid] + 0.10, ST[cid] + 0.55)
        mini_card(base, 1430, 384 + i * 92, 600, 84, p, RED, "KHÔNG ĐÚNG",
                  title, None, tfs=19, kfs=11)
        pq = seg(t, ST[cid] + 0.55, ST[cid] + 1.00)
        if pq > 0:
            cross_claim(d, 1430, 384 + i * 92, 600, 84, pq)
    an(base, t, "present", -1, 0.55, 960, 1048, 1.0, G.is_talk(t))


# ---------------- S16 ----------------
INDUSTRIES = [
    ("s16c2", CYAN, "Thương mại điện tử"),
    ("s16c3", EMER, "Bất động sản"),
    ("s16c3", EMER, "Tài chính"),
    ("s16c4", VIOLET, "Giáo dục"),
    ("s16c4", VIOLET, "Y tế"),
    ("s16c5", AMBER, "Nông nghiệp · năng lượng"),
]


def s16(base, t, G):
    ST = G.ST
    s0 = G.S[16]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "ỨNG DỤNG", "Có mặt ở nhiều ngành",
                "Cùng một công thức, nhiều bài toán thực tế.")
    photo_card(base, PHOTO11, 470, 590, 660, 440,
               seg(t, ST["s16c1"] + 0.25, ST["s16c1"] + 1.05), CYAN)
    pos = [(1075, 400), (1545, 400), (1075, 480), (1545, 480), (1075, 560), (1545, 560)]
    for (cid, acc, label), (cx, cy) in zip(INDUSTRIES, pos):
        mini_card(base, cx, cy, 430, 62, seg(t, ST[cid] + 0.10, ST[cid] + 0.50),
                  acc, None, label, None, tfs=18)
    caveat(base, 470, 848, seg(t, ST["s16c6"] + 0.12, ST["s16c6"] + 0.62),
           "Mỗi ngành cần dữ liệu và kiểm định phù hợp", AMBER)
    an(base, t, "point_right", -1, 0.55, 1710, 1048, 1.0, G.is_talk(t))


# ---------------- S17 ----------------
def s17(base, t, G):
    ST = G.ST
    s0 = G.S[17]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "PYTHON", "Code thực tế",
                "pandas đọc dữ liệu, scikit-learn huấn luyện và dự đoán.")
    rv = max(lin(t, ST["s17c1"] + 0.30, ST["s17c2"] + 0.80) * 0.30,
             lin(t, ST["s17c2"] + 0.30, ST["s17c3"] + 0.80) * 0.55,
             lin(t, ST["s17c3"] + 0.30, ST["s17c4"] + 0.80) * 0.75,
             lin(t, ST["s17c4"] + 0.30, ST["s17c5"] + 1.60))
    code_card(base, 610, 560, seg(t, ST["s17c1"] + 0.15, ST["s17c1"] + 0.75), rv,
              w=1000, h=440)
    mini_card(base, 1470, 390, 460, 78, seg(t, ST["s17c2"] + 0.10, ST["s17c2"] + 0.50),
              CYAN, "PANDAS", "read_csv()", None, tfs=19, kfs=11)
    mini_card(base, 1470, 480, 460, 78, seg(t, ST["s17c3"] + 0.10, ST["s17c3"] + 0.50),
              EMER, "SCIKIT-LEARN", "LinearRegression().fit()", None, tfs=19, kfs=11)
    mini_card(base, 1470, 570, 460, 78, seg(t, ST["s17c4"] + 0.10, ST["s17c4"] + 0.50),
              VIOLET, "HỆ SỐ", "coef_ · intercept_", None, tfs=19, kfs=11)
    mini_card(base, 1470, 660, 460, 78, seg(t, ST["s17c5"] + 0.10, ST["s17c5"] + 0.50),
              AMBER, "DỰ ĐOÁN", "predict([[85]])", None, tfs=19, kfs=11)
    caveat(base, 610, 848, seg(t, ST["s17c6"] + 0.12, ST["s17c6"] + 0.62),
           "10 dòng dữ liệu: quá ít để kết luận tổng quát", AMBER)
    an(base, t, "point_left", -1, 0.55, 1740, 1048, 1.0, G.is_talk(t))


# ---------------- S18 ----------------
def s18(base, t, G):
    ST = G.ST
    s0 = G.S[18]
    d = ImageDraw.Draw(base)
    scene_title(base, t, s0, "TỔNG KẾT", "Ba điều mang theo",
                "Và một câu hỏi cho bạn.")
    mini_card(base, 600, 392, 900, 86, seg(t, ST["s18c1"] + 0.12, ST["s18c1"] + 0.62),
              CYAN, "1 · MÔ HÌNH", "Quan hệ giữa đầu vào và kết quả số", None,
              tfs=21, kfs=11)
    mini_card(base, 600, 494, 900, 86, seg(t, ST["s18c2"] + 0.12, ST["s18c2"] + 0.62),
              EMER, "2 · OLS", "Chọn hệ số có tổng bình phương phần dư nhỏ nhất", None,
              tfs=21, kfs=11)
    mini_card(base, 600, 596, 900, 86, seg(t, ST["s18c3"] + 0.12, ST["s18c3"] + 0.62),
              VIOLET, "3 · ĐÁNH GIÁ", "Chia train/test; đọc MAE, RMSE, R²", None,
              tfs=21, kfs=11)
    mini_card(base, 600, 712, 900, 96, seg(t, ST["s18c4"] + 0.12, ST["s18c4"] + 0.62),
              AMBER, "CÂU HỎI CHO BẠN", "Biến mục tiêu của bạn là gì?", None,
              tfs=24, kfs=11)
    mini_card(base, 1460, 470, 520, 170, seg(t, ST["s18c5"] + 0.12, ST["s18c5"] + 0.62),
              CREAM, "LỜI CẢM ƠN", "Cảm ơn các bạn!", "Theo dõi An Tech Academy nhé",
              tfs=30, kfs=11, sfs=17)
    mini_card(base, 1460, 650, 520, 92, seg(t, ST["s18c6"] + 0.12, ST["s18c6"] + 0.62),
              CYAN, "HẸN GẶP LẠI", "Bài giảng tiếp theo", None, tfs=22, kfs=11)
    an(base, t, "wave", -1, 0.60, 1690, 1048, 1.0, G.is_talk(t))


SCENES = {13: s13, 14: s14, 15: s15, 16: s16, 17: s17, 18: s18}
