

# ================================================================ helpers mới
F_XL  = font("BeVietnamPro-Bold.ttf", 104)
F_L   = font("BeVietnamPro-Bold.ttf", 64)
F_M   = font("BeVietnamPro-SemiBold.ttf", 42)
F_B   = font("BeVietnamPro-Regular.ttf", 29)
F_S   = font("BeVietnamPro-Regular.ttf", 23)
F_MONO= font("JetBrainsMono-var.ttf", 21)


def _base(label=None):
    base = bg_canvas()
    brand_mark(base)
    if label:
        headbar(base, 1.0, label)
    return base, ImageDraw.Draw(base)


def _head(base, title, sub=None, x=100, y=118, p=1.0):
    ftxt(base, x, y, title, F_M, NAVY, p)
    if sub:
        ftxt(base, x, y + 58, sub, F_S, MUT, p)


def _an(base, tl, sid, t, pose="present", look=0):
    x, y, sc = ANX[sid]
    character.paste(base, x, y, t, pose, look, talk(tl, sid, t), sc)


def _lbhex(base, cx, cy, r, p=1.0, color=BLUE, label="LB"):
    if p <= 0:
        return
    d = ImageDraw.Draw(base)
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
           for a in (-90, -30, 30, 90, 150, 210)]
    d.polygon(pts, fill=WHITE, outline=color)
    d.line(pts + [pts[0]], fill=color, width=4, joint="curve")
    ftxt(base, cx, cy - 2, label, font("BeVietnamPro-Bold.ttf", int(r * 0.62)),
         color, p, "mm")


def _bar(base, x, y, w, q, color=BLUE, h=10, bg=(226, 234, 246, 255)):
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=bg)
    d.rounded_rectangle([x, y, x + max(4, int(w * max(0, min(1, q)))), y + h],
                        h // 2, fill=color)


def _stat(base, x, y, num, label, color=NAVY, p=1.0):
    ftxt(base, x, y, num, F_L, color, p)
    ftxt(base, x + 2, y + 76, label, F_S, MUT, p)


# ================================================================ S01 — HOOK
def draw_S01(t, tl):
    base, d = _base("01 · MỞ ĐẦU")
    s = tl["S01"]
    q1 = seg(t, 0.15, 0.95)
    ftxt(base, 100, 150, "CASE STUDY  ·  12/12", F_S, AMBER_D, q1)
    ftxt(base, 98, 196, "LOAD", F_XL, NAVY, q1)
    ftxt(base, 98, 306, "BALANCER", F_XL, BLUE, seg(t, 0.35, 1.0))
    ftxt(base, 102, 432, "Bộ cân bằng tải", F_M, NAVY, seg(t, 0.5, 1.0))
    desc = wrap("Giữ website đứng vững khi hàng nghìn người truy cập cùng lúc.", F_B, 700)
    for i, ln in enumerate(desc):
        ftxt(base, 102, 502 + i * 42, ln, F_B, MUT, seg(t, 0.7 + i * 0.08, 1.0))

    px, py, pw, ph = 980, 150, 520, 450
    base.alpha_composite(card(pw, ph), (px, py))
    dd = ImageDraw.Draw(base)
    ftxt(base, px + 28, py + 40, "CAO ĐIỂM 12/12", F_S, MUT, seg(t, 0.5, 1.0))
    dd.ellipse([px + pw - 62, py + 30, px + pw - 40, py + 52], fill=AMBER)
    _stat(base, px + 28, py + 78, "5.000", "người truy cập cùng lúc", AMBER_D, seg(t, 0.7, 1.0))
    _stat(base, px + 28, py + 214, "110.000", "lượt truy cập / ngày", NAVY, seg(t, 0.9, 1.0))
    dd.line([px + 28, py + 316, px + pw - 28, py + 316], fill=BORDER, width=2)
    ftxt(base, px + 28, py + 344, "Một server duy nhất", F_S, RED, seg(t, 1.05, 1.0))
    for i, (lab, q) in enumerate((("CPU", 0.91), ("RAM", 0.86), ("Độ trễ", 0.78))):
        yy = py + 372 + i * 24
        ftxt(base, px + 28, yy, lab, font("BeVietnamPro-Medium.ttf", 18), MUT, 1)
        _bar(base, px + 108, yy - 7, 300, q * seg(t, 1.1 + i * 0.05, 1.0),
             RED if i < 2 else AMBER, 9)

    if s["starts"][1] <= t:
        q = seg(t, s["starts"][1], s["starts"][1] + 0.8)
        _lbhex(base, 1130, 680, 44, q, TEAL, "LB")
        for i in range(3):
            x = 1250 + i * 88
            ic = sp_icon("server", TEAL, 44)
            base.alpha_composite(ic, (x, 656))
            ftxt(base, x + 22, 716, f"S{i+1:02d}", F_S, MUT, q)

    draw_marker(d, 100, 410, 500, 410, seg(t, 1.0, 1.35), AMBER, 7, 3)
    draw_marker_circle(d, 1120, 660, 150, 74, seg(t, s["starts"][1] + 0.5, s["starts"][1] + 1.4),
                       AMBER, 5, 5)
    _an(base, tl, "S01", t, "point_left" if t < s["starts"][1] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    s = tl["S01"]
    return [(0.3, "pop", None, 0.20), (s["starts"][1] - 0.1, "whoosh", None, 0.16),
            (s["starts"][1] + 0.5, "pop", None, 0.18)]


# ================================================================ S02 — SẬP
def draw_S02(t, tl):
    base, d = _base("02 · VẤN ĐỀ")
    s = tl["S02"]
    q = seg(t, 0.1, 0.8)
    _head(base, "Một server gánh 5.000 kết nối", "Cao điểm 12/12 — request dồn hết về một chỗ", p=q)

    shot(base, IMG["sale_crowd"], 100, 240, 360, 236, seg(t, 0.25, 0.8), t,
         caption="5.000 người cùng lúc", radius=16)
    shot(base, IMG["server_overheat"], 1000, 240, 300, 196, seg(t, 0.4, 0.95), t,
         caption="Server quá nhiệt", cap_color=RED, radius=16)

    sx, sy, sw, sh = 530, 240, 400, 330
    base.alpha_composite(card(sw, sh), (sx, sy))
    dd = ImageDraw.Draw(base)
    ic = sp_icon("server", RED, 46)
    base.alpha_composite(ic, (sx + 26, sy + 26))
    ftxt(base, sx + 86, sy + 48, "BACKEND DUY NHẤT", font("BeVietnamPro-Bold.ttf", 24), RED, 1)
    q2 = seg(t, s["starts"][1], s["starts"][1] + 1.2)
    for i, (lab, val, col) in enumerate((("CPU", "96%", RED), ("RAM", "92%", RED),
                                          ("Độ trễ", "8,4 s", AMBER_D))):
        yy = sy + 112 + i * 60
        ftxt(base, sx + 26, yy, lab, F_S, MUT, 1)
        ftxt(base, sx + sw - 26, yy, val, font("BeVietnamPro-Bold.ttf", 24), col, q2, "rm")
        _bar(base, sx + 26, yy + 20, sw - 52, (0.96 if i == 0 else 0.92 if i == 1 else 0.78) * q2, col, 8)
    ftxt(base, sx + 26, sy + 294, "Trang quay mãi…", F_S, MUT, seg(t, s["starts"][1] + 0.6, 1))

    if t > s["starts"][1] + 0.8:
        qe = seg(t, s["starts"][1] + 0.8, s["starts"][1] + 1.3)
        for i, txt in enumerate(("502 Bad Gateway", "Thanh toán thất bại")):
            im = sp_chip(txt, RED, RED_L, 20, "alert-triangle", 44)
            paste_im(base, im, sx + 10, sy + sh + 18 + i * 52, qe)

    shot(base, IMG["ops_monitor"], 1000, 470, 300, 200, seg(t, 0.55, 1.0), t,
         caption="Cảnh báo quá tải", cap_color=RED, radius=16)

    draw_marker_circle(d, sx + sw / 2, sy + sh / 2, 240, 200,
                       seg(t, s["starts"][1] + 0.3, s["starts"][1] + 1.3), RED, 6, 4)
    _an(base, tl, "S02", t, "think", look=-1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    s = tl["S02"]
    return [(0.4, "pop", None, 0.18), (s["starts"][1], "deny", None, 0.24),
            (s["starts"][1] + 0.45, "thud", None, 0.20),
            (s["starts"][1] + 0.9, "marker", 0.7, 0.16)]


# ================================================================ S03 — ĐỊNH NGHĨA
def draw_S03(t, tl):
    base, d = _base("03 · KHÁI NIỆM")
    s = tl["S03"]
    _head(base, "Load Balancer là gì?", "Người điều phối lưu lượng đứng trước các server",
          p=seg(t, 0.1, 0.8))

    dx, dy, dw, dh = 100, 230, 620, 260
    base.alpha_composite(card(dw, dh), (dx, dy))
    dd = ImageDraw.Draw(base)
    ftxt(base, dx + 28, dy + 44, "LOAD BALANCER", font("BeVietnamPro-Bold.ttf", 34), BLUE,
         seg(t, 0.2, 0.9))
    ftxt(base, dx + 28, dy + 92, "Bộ cân bằng tải", F_S, MUT, seg(t, 0.3, 0.9))
    ftxt(base, dx + 28, dy + 146, "Nhận request", F_B, NAVY, seg(t, 0.4, 1.0))
    ftxt(base, dx + 28, dy + 186, "Chọn server phù hợp", F_B, NAVY, seg(t, 0.5, 1.0))
    ftxt(base, dx + 28, dy + 226, "Chia đều tải", F_B, BLUE, seg(t, 0.6, 1.0))
    draw_marker_circle(d, dx + 132, dy + 226, 82, 26,
                       seg(t, s["starts"][1], s["starts"][1] + 0.9), AMBER, 5, 6)

    ox, oy = 790, 210
    dd.rounded_rectangle([ox, oy, ox + 700, oy + 470], 22, fill=WHITE, outline=BORDER, width=2)
    ftxt(base, ox + 26, oy + 38, "TRẠM THU PHÍ CAO TỐC", F_S, MUT, seg(t, 0.5, 1.0))
    dd.rounded_rectangle([ox + 30, oy + 90, ox + 300, oy + 130], 20, fill=(237, 242, 249, 255))
    dd.rounded_rectangle([ox + 30, oy + 330, ox + 650, oy + 410], 30, fill=(237, 242, 249, 255))
    qt = t - s["starts"][1]
    for i in range(3):
        cx = ox + 60 + ((qt * 80 + i * 70) % 230)
        dd.rounded_rectangle([cx, oy + 98 + i * 10, cx + 34, oy + 112 + i * 10], 6,
                             fill=AMBER if i == 0 else BLUE)
    _lbhex(base, ox + 350, oy + 245, 54, seg(t, s["starts"][1] + 0.1, s["starts"][1] + 0.8),
           TEAL, "LB")
    for i in range(3):
        lx = ox + 450 + i * 75
        dd.line([lx, oy + 300, lx, oy + 370], fill=TEAL, width=5)
        ic = sp_icon("server", TEAL, 42)
        base.alpha_composite(ic, (lx - 21, oy + 372))
        ftxt(base, lx, oy + 428, f"S{i+1:02d}", F_S, MUT, seg(t, s["starts"][1] + 0.5 + i * 0.1, 1))
    for i in range(3):
        qq = (qt * 0.55 + i * 0.31) % 1.0
        if qq < 0.7:
            p0 = (ox + 350, oy + 280)
            p1 = (ox + 450 + i * 75, oy + 372)
            x = p0[0] + (p1[0] - p0[0]) * (qq / 0.7)
            y = p0[1] + (p1[1] - p0[1]) * (qq / 0.7)
            dd.ellipse([x - 9, y - 9, x + 9, y + 9], fill=AMBER)
    draw_marker(d, ox + 300, oy + 245, ox + 420, oy + 245,
                seg(t, s["starts"][1] + 0.7, s["starts"][1] + 1.4), AMBER, 5, 2)

    if t > s["starts"][-1]:
        q3 = seg(t, s["starts"][-1], s["starts"][-1] + 0.7)
        im = sp_chip("Không xử lý nghiệp vụ — chỉ điều phối", TEAL, MINT, 22, "circle-check", 48)
        paste_im(base, im, 100, 560, q3)
        ftxt(base, 100, 640, "Điểm cốt lõi: LB giúp nhiều server cùng làm việc.",
             F_B, NAVY, q3)

    _an(base, tl, "S03", t, "point_left" if t < s["starts"][1] else "write", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    s = tl["S03"]
    return [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][1] + 0.7, "marker", 0.7, 0.16),
            (s["starts"][-1], "chime", None, 0.14)]
