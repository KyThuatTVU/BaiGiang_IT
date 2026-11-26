# -*- coding: utf-8 -*-
"""Cảnh S13–S18 bài SVD."""
from PIL import Image, ImageDraw
import demo_gateB as G
import full_state as FS
from full_common import (
    W, H, F_T2, F_T3, F_T4, F_SUB2, F_NOTE, F_MICRO, F_LEG, F_CELL,
    TXT, MUT, CYAN, VIOLET, AMBER, EMER, CREAM,
    scene_head, info_card, chip, photo_card, an, tracked, draw_rich,
    draw_marker, draw_marker_circle, wrap_t, seg, lin, formula_card,
    code_card, mono_box, api_card, vs_col, pill, photo_note, font,
    card_base, blit, paste_brand,
)


def draw_s13(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s13c{i}"] for i in range(1, 9)}
    scene_head(base, t, t0, "LẬP TRÌNH", "Surprise · Python",
               "scikit-surprise + pandas")
    q = lin(t, s[2] + 0.20, s[6] + 0.60)
    code_card(base, 112, 360, 900, [
        "from surprise import Dataset, Reader, SVD",
        "reader = Reader(rating_scale=(1, 5))",
        'data = Dataset.load_from_df(df[["user","item","rating"]], reader)',
        "trainset = data.build_full_trainset()",
        "algo = SVD(n_factors=2, n_epochs=100, lr_all=0.005, reg_all=0.2)",
        "algo.fit(trainset)",
        'pred = algo.predict("An", "AirPods")',
    ], q, seg(t, s[2] + 0.05, s[2] + 0.45), acc=EMER,
        title="python · surprise")
    pill(base, 560, 690, seg(t, s[3] + 0.10, s[3] + 0.50),
         "pip install scikit-surprise pandas", AMBER, fsize=15)
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "5.jpg", 1480, 400, 480, 300, p, VIOLET, mode="contain")
    if p > 0:
        draw_rich(d, (1480, 580), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    cp = seg(t, s[8] + 0.05, s[8] + 0.70)
    if cp > 0:
        a = int(255 * cp)
        d.text((112, 742), "Surprise SVD = Funk-SVD", font=F_T3, fill=AMBER + (a,))
        d.text((112, 778), "tối ưu trên đánh giá đã biết · không điền 0 vào ô trống",
               font=F_NOTE, fill=MUT + (a,))
    an(base, t, "write", -1, 0.56, 1730, 1048, 1.0, FS.is_talk(t))


ROWS14 = (("Baseline · phổ biến", "0.95", "0.74"),
          ("Cải tiến", "0.78", "0.61"),
          ("SVD · k = 2", "0.62", "0.49"))


def draw_s14(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s14c{i}"] for i in range(1, 7)}
    scene_head(base, t, t0, "ĐO LƯỜNG", "RMSE và MAE", "Sai số dự đoán")
    formula_card(base, 480, 400, seg(t, s[2] + 0.05, s[2] + 0.55), 620, AMBER,
                 "RMSE = √(Σ (y - y^)² / n)", fs=font("JetBrainsMono-var.ttf", 32))
    formula_card(base, 480, 540, seg(t, s[3] + 0.05, s[3] + 0.55), 620, CYAN,
                 "MAE = Σ |y - y^| / n", fs=font("JetBrainsMono-var.ttf", 32))
    tp = seg(t, s[3] + 0.10, s[3] + 0.75)
    if tp > 0:
        w, h = 660, 320
        cx, cy = 1330, 480
        im, pad = card_base(w, h, AMBER)
        base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        x0, y0 = cx - w / 2, cy - h / 2
        d.text((x0 + 28, y0 + 32), "Mô hình", font=F_LEG, fill=MUT + (245,))
        d.text((x0 + 372, y0 + 32), "RMSE", font=F_LEG, fill=AMBER + (245,))
        d.text((x0 + 512, y0 + 32), "MAE", font=F_LEG, fill=MUT + (245,))
        d.line([x0 + 24, y0 + 62, x0 + w - 24, y0 + 62], fill=(255, 255, 255, 30), width=1)
        hi = seg(t, s[5] + 0.10, s[5] + 0.65)
        for i, (name, r_, m_) in enumerate(ROWS14):
            yy = y0 + 84 + i * 68
            if i == 2 and hi > 0:
                d.rounded_rectangle([x0 + 16, yy - 4, x0 + w - 16, yy + 54], 10,
                                    fill=(14, 40, 34), outline=EMER + (int(190 * hi),), width=1)
            d.text((x0 + 28, yy + 18), name, font=font("BeVietnamPro-Medium.ttf", 19),
                   fill=TXT + (240,), anchor="lm")
            d.text((x0 + 372, yy + 18), r_, font=font("PlusJakartaSans-var.ttf", 24, 700),
                   fill=(AMBER if i < 2 else EMER) + (250,), anchor="lm")
            d.text((x0 + 512, yy + 18), m_, font=font("PlusJakartaSans-var.ttf", 24, 700),
                   fill=TXT + (235,), anchor="lm")
        draw_rich(d, (cx, y0 + h - 22), "Số liệu minh họa", F_NOTE, MUT + (200,), "mm")
    q = seg(t, s[6] + 0.05, t1)
    if q > 0:
        for i, text in enumerate(("RMSE thấp chưa chắc Top-N đã tốt",
                                  "Đánh giá thêm Precision · Recall · F1")):
            draw_rich(d, (1330, 704 + i * 28), text, F_NOTE,
                      (AMBER if i == 0 else MUT) + (int(225 * q),), "mm")
    an(base, t, "present", -1, 0.54, 1700, 1048, 1.0, FS.is_talk(t))


def draw_s15(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s15c{i}"] for i in range(1, 8)}
    scene_head(base, t, t0, "KIẾN TRÚC", "Mô hình đứng sau hệ thống",
               "Frontend · Backend · ML service · Cache")
    p = seg(t, s[1] + 0.15, s[1] + 0.75)
    photo_card(base, "11.jpg", 470, 556, 700, 430, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (470, 802), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    api_card(base, 1070, 385, 620, seg(t, s[4] + 0.05, s[4] + 0.55),
             "/api/recommendations/An", "GET")
    mono_box(base, 1070, 450, 620, seg(t, s[5] + 0.05, s[5] + 0.65), [
        '{"user": "An",',
        ' "items": [',
        '   {"id": "airpods", "score": 4.8},',
        '   {"id": "sony",    "score": 4.6}]}',
    ], acc=CYAN, fs=font("JetBrainsMono-var.ttf", 18), title="response · JSON")
    q = seg(t, s[7] + 0.05, t1)
    if q > 0:
        for i, text in enumerate(("SVD chỉ phân tích dữ liệu và dự đoán",
                                  "không quản lý UI, giỏ hàng hay thanh toán")):
            draw_rich(d, (1390, 746 + i * 28), text, F_NOTE,
                      (AMBER if i == 0 else MUT) + (int(225 * q),), "mm")
    an(base, t, "present", -1, 0.54, 1690, 1048, 1.0, FS.is_talk(t))


PROS = (("lightbulb", "Sở thích tiềm ẩn"), ("layers", "Giảm số chiều"),
        ("target", "Dự đoán ô trống"))
CONS = (("database", "Cần dữ liệu tương tác"), ("clock", "Cần thời gian huấn luyện"),
        ("shield-check", "Phụ thuộc chất lượng dữ liệu"))


def draw_s16(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s16c{i}"] for i in range(1, 9)}
    scene_head(base, t, t0, "ƯU & NHƯỢC ĐIỂM", "Khi nào nên dùng SVD?",
               "Không có mô hình nào tốt cho mọi bài toán")
    pp = seg(t, s[2] + 0.15, s[2] + 0.85)
    vs_col(base, 400, 470, pp, EMER, "ƯU ĐIỂM", PROS, w=480)
    cp = seg(t, s[3] + 0.15, s[3] + 0.85)
    vs_col(base, 910, 470, cp, AMBER, "HẠN CHẾ", CONS, w=480)
    ph = seg(t, t0 + 0.20, t0 + 0.80) * (1 - seg(t, s[4] - 0.30, s[4] + 0.05))
    photo_card(base, "8.jpg", 1450, 470, 460, 300, ph, VIOLET, mode="contain")
    if ph > 0:
        draw_rich(d, (1450, 640), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(200 * ph),), "mm")
    info_card(base, 1450, 440, seg(t, s[4] + 0.05, s[4] + 0.65), 500, 230,
              AMBER, "COLD START", "Dữ liệu quá ít",
              ["Người dùng mới · sản phẩm mới", "Chưa đủ lịch sử tương tác",
               "nên chưa suy ra được sở thích"], "alert-triangle")
    sols = (("Độ phổ biến", AMBER), ("Thông tin danh mục", CYAN),
            ("Hỏi sở thích ban đầu", EMER))
    for i, (text, acc) in enumerate(sols):
        chip(base, text, acc, 330 + 520 * i, 655,
             seg(t, s[7] + 0.10 + i * 0.18, s[7] + 0.50 + i * 0.18), fsize=16)
    q = seg(t, s[8] + 0.05, t1)
    if q > 0:
        draw_rich(d, (960, 752), "Kết hợp nhiều phương pháp để bù dữ liệu.", F_NOTE,
                  MUT + (int(230 * q),), "mm")
    an(base, t, "present", -1, 0.52, 1710, 1048, 1.0, FS.is_talk(t))


CF_ITEMS = (("users", "Dựa trên hành vi"), ("user", "User-based / Item-based"),
            ("target", "Mục tiêu: gợi ý"))
SVD_ITEMS = (("layers", "Phân rã ma trận"), ("filter", "Tìm yếu tố tiềm ẩn"),
             ("workflow", "Dùng bên trong CF"))


def draw_s17(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s17c{i}"] for i in range(1, 6)}
    scene_head(base, t, t0, "PHÂN BIỆT", "Phương pháp và công cụ",
               "Hai khái niệm dễ nhầm")
    p = seg(t, t0 + 0.15, t0 + 0.75)
    photo_card(base, "9.jpg", 450, 560, 620, 440, p, CYAN, mode="contain")
    if p > 0:
        draw_rich(d, (450, 812), "Ảnh minh họa · do người dùng cung cấp",
                  F_NOTE, MUT + (int(210 * p),), "mm")
    vs_col(base, 1080, 470, seg(t, s[2] + 0.10, s[2] + 0.80), CYAN,
           "LỌC CỘNG TÁC", CF_ITEMS, w=380)
    vs_col(base, 1500, 470, seg(t, s[3] + 0.10, s[3] + 0.80), VIOLET,
           "SVD", SVD_ITEMS, w=380)
    chip(base, "Lọc cộng tác = phương pháp · SVD = công cụ", AMBER, 1290, 660,
         seg(t, s[4] + 0.10, s[4] + 0.50), fsize=15)
    q = seg(t, s[5] + 0.05, t1)
    if q > 0:
        draw_rich(d, (1290, 722), "Không phải mọi hệ thống lọc cộng tác đều dùng SVD",
                  F_NOTE, MUT + (int(230 * q),), "mm")
    an(base, t, "present", -1, 0.54, 1710, 1048, 1.0, FS.is_talk(t))


SUM = (("01", "Ma trận người dùng – sản phẩm", "Hàng · cột · điểm đánh giá", CYAN, "layers"),
       ("02", "SVD tìm yếu tố tiềm ẩn", "Phân rã ma trận đánh giá", AMBER, "braces"),
       ("03", "Dự đoán & xếp hạng", "Điền ô trống · chọn Top N", EMER, "trending-up"))


def draw_s18(base, t, t0, t1):
    d = ImageDraw.Draw(base)
    s = {i: FS.ST[f"s18c{i}"] for i in range(1, 8)}
    scene_head(base, t, t0, "TỔNG KẾT", "Ba ý quan trọng", "Ghi nhớ nhanh")
    for i, (num, title, sub, acc, icon) in enumerate(SUM):
        info_card(base, 330 + 500 * i, 420,
                  seg(t, s[2] + 0.05 + i * 0.25, s[2] + 0.45 + i * 0.25),
                  440, 170, acc, num, title, [sub], icon)
    qp = seg(t, s[5] + 0.10, s[5] + 0.70)
    if qp > 0:
        w, h = 1120, 110
        cx, cy = 940, 645
        im, pad = card_base(w, h, AMBER)
        base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        dd = ImageDraw.Draw(base)
        dd.line([cx - w / 2 + 22, cy - h / 2, cx + w / 2 - 22, cy - h / 2],
                fill=AMBER + (185,), width=2)
        tracked(dd, (cx - w / 2 + 26, cy - h / 2 + 18), "CÂU HỎI", F_MICRO,
                AMBER + (235,), 2)
        dd.text((cx - w / 2 + 26, cy - h / 2 + 52),
                "Sản phẩm mới chưa ai đánh giá — em sẽ xử lý thế nào?",
                font=font("BeVietnamPro-SemiBold.ttf", 27), fill=TXT + (250,))
    op = seg(t, s[6] + 0.05, s[6] + 0.65)
    if op > 0:
        bg = G.bg_frame()
        bg.putalpha(int(255 * op))
        base.alpha_composite(bg)
        paste_brand(base, W / 2, 300, size=150, p=op, alpha=0.95)
        a = int(255 * op)
        d.text((W / 2, 452), "Cảm ơn các bạn đã theo dõi", font=F_T2,
               fill=TXT + (a,), anchor="mm")
        d.text((W / 2, 512), "Theo dõi kênh An Tech Academy", font=F_T3,
               fill=MUT + (a,), anchor="mm")
        hp = seg(t, s[7] + 0.10, s[7] + 0.60)
        if hp > 0:
            d.text((W / 2, 578), "Hẹn gặp lại trong bài giảng sau", font=F_T3,
                   fill=EMER + (int(255 * hp),), anchor="mm")
    an(base, t, "wave" if t >= s[6] else "present", -1, 0.62, 1620, 1048, 1.0,
       FS.is_talk(t))
