# ================================================================ S04 — KIẾN TRÚC
def draw_S04(t, tl):
    base, d = _base("04 · KIẾN TRÚC")
    s = tl["S04"]
    _head(base, "Bốn lớp của một hệ thống", "Client → Load Balancer → Backend → Database",
          p=seg(t, 0.1, 0.7))
    q1 = seg(t, 0.25, 0.9)
    q2 = seg(t, s["starts"][1], s["starts"][1] + 0.9)
    q3 = seg(t, s["starts"][2], s["starts"][2] + 0.8)

    node(base, 100, 320, 250, 160, "smartphone", "CLIENT", "Trình duyệt / App", BLUE, p=q1)
    _lbhex(base, 450, 400, 60, q1, BLUE, "LB")
    ftxt(base, 450, 478, "LOAD BALANCER", font_semi(21), NAVY, q1, "mm")
    ftxt(base, 450, 506, "cửa ngõ tiếp nhận", F_S, MUT, q1, "mm")

    ftxt(base, 690, 290, "BACKEND · XỬ LÝ NGHIỆP VỤ", font_semi(19), MUT, q2)
    for i in range(3):
        srv_card(base, 690, 320 + i * 104, 290, 92, i + 1, "ok", q2, None, None,
                 BLUE, "Node.js · Express")
    node(base, 1120, 320, 260, 160, "database", "DATABASE", "Lưu trữ dữ liệu", TEAL, p=q2)

    draw_conn(d, 350, 400, 390, 400, q1, BLUE, width=4)
    for i in range(3):
        draw_conn(d, 510, 400, 690, 366 + i * 104, q2, BLUE, width=3)
    for i in range(3):
        draw_conn(d, 980, 366 + i * 104, 1120, 400, q2, TEAL, width=2)

    if t >= s["starts"][2]:
        pts = [(355, 400), (450, 400), (690, 470), (980, 470), (1120, 400)]
        qq = min(1.0, ((t - s["starts"][2]) % 2.2) / 1.55)
        packet(base, pts, qq, AMBER, 10)
        im = sp_chip("LB đứng giữa nhưng không thay server làm việc", AMBER, CREAM, 21,
                     "circle-help", 46)
        paste_im(base, im, 100, 706, q3)
        ftxt(base, 100, 782, "4 lớp, một luồng: request đi vào — dữ liệu trả về.",
             F_B, NAVY, seg(t, s["starts"][2] + 0.4, s["starts"][2] + 1.0))

    _an(base, tl, "S04", t, "point_left" if t < s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    s = tl["S04"]
    return [(0.3, "pop", None, 0.2), (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][2], "tick", None, 0.14),
            (s["starts"][2] + 0.6, "marker", 0.6, 0.14),
            (s["starts"][2] + 1.7, "chime", None, 0.12)]


# ================================================================ S05 — LUỒNG
def draw_S05(t, tl):
    base, d = _base("05 · LUỒNG REQUEST")
    s = tl["S05"]
    _head(base, "Một request đi qua những đâu?", "Luồng xử lý và cách mở rộng hệ thống",
          p=seg(t, 0.1, 0.7))
    q = seg(t, 0.2, 0.8)

    node(base, 100, 300, 240, 130, "globe", "Trình duyệt", "HTTP request", BLUE, p=q)
    _lbhex(base, 430, 365, 52, q, BLUE, "LB")
    for i in range(3):
        srv_card(base, 640, 260 + i * 105, 270, 90, i + 1, "ok", q, None, None,
                 BLUE, "Node.js · Express")
    node(base, 1040, 300, 210, 130, "database", "Database", "truy vấn", TEAL, p=q)

    draw_conn(d, 340, 365, 378, 365, q, BLUE, width=4)
    for i in range(3):
        draw_conn(d, 482, 365, 640, 305 + i * 105, q, BLUE, width=3)
        draw_conn(d, 910, 305 + i * 105, 1040, 365, q, (184, 198, 222, 255), width=2)

    lx, ly, lw, lh = 1300, 260, 260, 330
    base.alpha_composite(card(lw, lh), (lx, ly))
    ftxt(base, lx + 22, ly + 36, "NHẬT KÝ REQUEST", font_semi(18), MUT, 1)
    rows = (("#1042", "S01", "42 ms", BLUE), ("#1043", "S02", "39 ms", TEAL),
            ("#1044", "S03", "47 ms", GREEN))
    for i, (rid, srv, ms, col) in enumerate(rows):
        b = s["starts"][1] if i else s["starts"][0]
        rr = seg(t, b + (0.8 if i < 2 else 1.6), b + (1.3 if i < 2 else 2.1))
        yy = ly + 96 + i * 72
        if rr > 0:
            rrect_a(base, (lx + 18, yy - 26, lx + lw - 18, yy + 26), 10, ICE, None, 0, rr)
            ftxt(base, lx + 30, yy, rid, font("JetBrainsMono-var.ttf", 18), NAVY, rr)
            ftxt(base, lx + 112, yy, "→ " + srv, font_semi(18), col, rr)
            ftxt(base, lx + lw - 30, yy, ms, font("BeVietnamPro-Medium.ttf", 17), MUT, rr, "rm")

    if t < s["starts"][2]:
        idx = 0 if t < s["starts"][1] else 1
        t0 = s["starts"][0] + 1.0 if idx == 0 else s["starts"][1] + 0.6
        if t >= t0:
            pts = [(345, 365), (430, 365), (640, 305 + idx * 105)]
            qq = min(1.0, ((t - t0) % 1.9) / 1.2)
            packet(base, pts, qq, AMBER, 9)
            im = sp_chip(f"S0{idx+1} đang xử lý", BLUE, ICE, 16, None, 30)
            paste_im(base, im, 640, 305 + idx * 105 - 56, seg(t, t0, t0 + 0.3))

    if t >= s["starts"][2]:
        qs = seg(t, s["starts"][2], s["starts"][2] + 0.8)
        base.alpha_composite(card(580, 240), (100, 620))
        ftxt(base, 128, 660, "SCALE-UP · DỌC", font_semi(22), AMBER_D, qs)
        ic = sp_icon("server", AMBER, 62)
        base.alpha_composite(ic, (128, 696))
        ftxt(base, 208, 712, "Nâng CPU / RAM", F_B, NAVY, qs)
        ftxt(base, 208, 750, "cho một máy mạnh hơn", F_S, MUT, qs)
        ftxt(base, 128, 814, "Giới hạn bởi phần cứng", F_S, RED, qs)

        base.alpha_composite(card(660, 240), (720, 620))
        ftxt(base, 748, 660, "SCALE-OUT · NGANG", font_semi(22), BLUE, qs)
        _lbhex(base, 802, 752, 28, qs, BLUE, "LB")
        for i in range(3):
            draw_conn(d, 828, 752, 864 + i * 84, 752, qs, BLUE, width=3)
            ic = sp_icon("server", BLUE, 52)
            base.alpha_composite(ic, (864 + i * 84, 726))
        ftxt(base, 748, 814, "Thêm máy + Load Balancer", F_B, NAVY, qs)
        ftxt(base, 1140, 702, "Horizontal", font_semi(24), GREEN, qs)
        ftxt(base, 1140, 736, "Scaling", font_semi(24), GREEN, qs)

    _an(base, tl, "S05", t, "point_left" if t < s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    s = tl["S05"]
    return [(0.3, "pop", None, 0.18), (s["starts"][0] + 1.0, "tick", None, 0.16),
            (s["starts"][1] + 0.6, "tick", None, 0.16),
            (s["starts"][2], "whoosh", None, 0.16),
            (s["starts"][2] + 0.7, "success", None, 0.16)]


# ================================================================ S06 — RR / WRR
def _tabs(base, active, p):
    labels = (("Round Robin", "route"), ("Weighted RR", "scale"),
              ("Least Connections", "git-fork"), ("IP Hash", "key-round"))
    x = 100
    for i, (lab, ic) in enumerate(labels):
        act = i == active
        im = sp_chip(lab, BLUE if act else (148, 163, 184, 255),
                     SKY if act else WHITE, 19, ic, 42)
        paste_im(base, im, x, 238, p)
        x += im.width + 12


def draw_S06(t, tl):
    base, d = _base("06 · THUẬT TOÁN")
    s = tl["S06"]
    _head(base, "Thuật toán chọn server", "Bốn cách phổ biến để chia tải", p=seg(t, 0.1, 0.7))
    stage2 = t >= s["starts"][1]
    stage3 = t >= s["starts"][2]
    _tabs(base, 0 if not stage2 else (1 if not stage3 else 2), seg(t, 0.1, 0.7))

    if not stage2:
        items = (("Round Robin", "Luân phiên theo thứ tự", "route"),
                 ("Weighted RR", "Chia theo trọng số", "scale"),
                 ("Least Connections", "Chọn máy ít kết nối", "git-fork"),
                 ("IP Hash", "Băm IP, giữ phiên", "key-round"))
        for i, (nm, ds, ic) in enumerate(items):
            x = 100 + (i % 2) * 360
            y = 330 + (i // 2) * 180
            base.alpha_composite(card(330, 150), (x, y))
            base.alpha_composite(sp_icon(ic, BLUE, 40), (x + 24, y + 24))
            ftxt(base, x + 78, y + 46, nm, font_semi(21), NAVY, seg(t, 0.3 + i * 0.12, 0.8))
            ftxt(base, x + 24, y + 104, ds, F_S, MUT, seg(t, 0.36 + i * 0.12, 0.9))
        ftxt(base, 100, 700, "Mỗi thuật toán trả lời một câu hỏi khác nhau.", F_B, NAVY,
             seg(t, 0.8, 1.0))

    elif not stage3:
        el = t - s["starts"][1]
        _lbhex(base, 240, 520, 60, 1, BLUE, "LB")
        for i, cy in enumerate((428, 538, 648)):
            srv_card(base, 740, cy - 48, 300, 96, i + 1, "ok", 1)
            draw_conn(d, 300, 520, 740, cy, 1, BLUE, width=3)
        i = int(el / 1.15) % 3
        qq = min(1.0, (el % 1.15) / 0.85)
        packet(base, [(300, 520), (520, 520), (740, 428 + i * 110)], qq, AMBER, 10)
        draw_marker_circle(d, 890, 428 + i * 110, 170, 64, 1, AMBER, 4, 3)
        x = 100
        for k in range(5):
            if el >= 0.4 + k * 0.7:
                im = sp_chip(f"#{k+1} → S0{(k % 3)+1}", BLUE, ICE, 18, None, 40)
                paste_im(base, im, x, 760, 1)
                x += im.width + 10
        base.alpha_composite(card(330, 320), (1150, 380))
        ftxt(base, 1178, 418, "ROUND ROBIN", font_semi(20), BLUE, 1)
        ftxt(base, 1178, 458, "Lần lượt 1 → 2 → 3", F_B, NAVY, 1)
        ftxt(base, 1178, 500, "rồi quay lại 1.", F_B, NAVY, 1)
        ftxt(base, 1178, 556, "Hợp khi các server", F_S, MUT, 1)
        ftxt(base, 1178, 588, "cấu hình giống nhau.", F_S, MUT, 1)
        base.alpha_composite(sp_icon("refresh-cw", BLUE, 40), (1178, 626))

    else:
        el = t - s["starts"][2]
        _lbhex(base, 240, 520, 60, 1, BLUE, "LB")
        wts = (3, 1, 1)
        for i, cy in enumerate((428, 538, 648)):
            srv_card(base, 740, cy - 48, 300, 96, i + 1, "ok", 1)
            draw_conn(d, 300, 520, 740, cy, 1, BLUE, width=3)
            im = sp_chip(f"×{wts[i]}", AMBER if i == 0 else (148, 163, 184, 255),
                         CREAM if i == 0 else WHITE, 18, None, 34)
            paste_im(base, im, 742 + 300 - im.width - 8, cy - 48 - 26, 1)
        seq = (0, 0, 0, 1, 2)
        i = seq[int(el / 1.2) % 5]
        qq = min(1.0, (el % 1.2) / 0.9)
        packet(base, [(300, 520), (520, 520), (740, 428 + i * 110)], qq, AMBER, 10)
        draw_marker_circle(d, 890, 428 + i * 110, 170, 64, 1, AMBER, 4, 3)
        x = 100
        for k in range(5):
            if el >= 0.4 + k * 0.7:
                im = sp_chip(f"#{k+1} → S0{seq[k]+1}", AMBER_D, CREAM, 18, None, 40)
                paste_im(base, im, x, 760, 1)
                x += im.width + 10
        base.alpha_composite(card(330, 320), (1150, 380))
        ftxt(base, 1178, 418, "WEIGHTED RR", font_semi(20), AMBER_D, 1)
        ftxt(base, 1178, 458, "Server mạnh nhận", F_B, NAVY, 1)
        ftxt(base, 1178, 500, "nhiều request hơn.", F_B, NAVY, 1)
        ftxt(base, 1178, 556, "S01 : S02 : S03", F_S, MUT, 1)
        ftxt(base, 1178, 588, "= 3 : 1 : 1", font_semi(22), AMBER_D, 1)

    _an(base, tl, "S06", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    s = tl["S06"]
    ev = [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16)]
    for k in range(5):
        ev.append((s["starts"][1] + 0.4 + k * 0.7, "tick", None, 0.14))
    ev.append((s["starts"][2], "whoosh", None, 0.16))
    for k in range(5):
        ev.append((s["starts"][2] + 0.4 + k * 0.7, "tick", None, 0.14))
    return ev


# ================================================================ S07 — LC / IP HASH
def draw_S07(t, tl):
    base, d = _base("07 · THUẬT TOÁN (TT)")
    s = tl["S07"]
    _head(base, "Chọn theo kết nối và theo IP", "Least Connections và IP Hash", p=seg(t, 0.1, 0.7))
    _tabs(base, 2 if t < s["starts"][1] else 3, 1)

    if t < s["starts"][1] + 0.12:
        _lbhex(base, 240, 500, 60, 1, BLUE, "LB")
        conns = (100, 30, 10)
        for i, cy in enumerate((408, 518, 628)):
            srv_card(base, 760, cy - 48, 300, 96, i + 1, "ok", 1, None, conns[i], BLUE)
            draw_conn(d, 300, 500, 760, cy, 1, BLUE, width=3)
        el = t - s["starts"][0]
        qq = min(1.0, (el % 1.8) / 1.3)
        packet(base, [(300, 500), (520, 500), (760, 628)], qq, AMBER, 10)
        draw_marker_circle(d, 910, 628, 170, 64, 1, AMBER, 4, 3)
        im = sp_chip("CHỌN", AMBER_D, CREAM, 16, "circle-check", 34)
        paste_im(base, im, 1010, 574, 1)
        base.alpha_composite(card(330, 320), (1180, 380))
        ftxt(base, 1208, 418, "LEAST CONN.", font_semi(20), BLUE, 1)
        ftxt(base, 1208, 458, "Chọn server đang ít", F_B, NAVY, 1)
        ftxt(base, 1208, 500, "kết nối nhất.", F_B, NAVY, 1)
        ftxt(base, 1208, 556, "S03 chỉ có 10 →", F_S, MUT, 1)
        ftxt(base, 1208, 588, "request tiếp theo", F_S, MUT, 1)
        ftxt(base, 1208, 620, "ưu tiên S03.", F_S, MUT, 1)

    if t >= s["starts"][1]:
        q = seg(t, s["starts"][1], s["starts"][1] + 0.6)
        users = (("NGƯỜI DÙNG A", "203.0.113.7", 400, BLUE),
                 ("NGƯỜI DÙNG B", "198.51.100.22", 560, TEAL))
        for lab, ip, cy, col in users:
            rrect_a(base, (120, cy - 48, 490, cy + 48), 14, WHITE, col, 2, q)
            ftxt(base, 146, cy - 22, lab, font_semi(16), MUT, q)
            ftxt(base, 146, cy + 16, ip, font("JetBrainsMono-var.ttf", 22), NAVY, q)
        rrect_a(base, (560, 424, 830, 576), 16, SKY, BLUE, 2, q)
        ftxt(base, 590, 462, "hash(IP)", font("JetBrainsMono-var.ttf", 24), BLUE, q)
        ftxt(base, 590, 500, "% 3", font("JetBrainsMono-var.ttf", 24), BLUE, q)
        ftxt(base, 590, 540, "chọn server", F_S, MUT, q)
        for i, cy in enumerate((408, 518, 628)):
            srv_card(base, 1000, cy - 48, 300, 96, i + 1, "ok", q)
        draw_conn(d, 490, 400, 560, 440, q, BLUE, width=3)
        draw_conn(d, 490, 560, 560, 560, q, TEAL, width=3)
        draw_conn(d, 830, 450, 1000, 408, q, BLUE, width=3)
        draw_conn(d, 830, 520, 1000, 518, q, TEAL, width=3)
        draw_conn(d, 830, 540, 1000, 628, q, (184, 198, 222, 255), width=2)
        im = sp_chip("Cùng IP → cùng server (giữ phiên)", BLUE, ICE, 18, "refresh-cw", 40)
        paste_im(base, im, 560, 620, seg(t, s["starts"][1] + 1.2, s["starts"][1] + 1.6))
        im = sp_chip("Không đảm bảo tuyệt đối khi danh sách server đổi", AMBER_D, CREAM,
                     18, "alert-triangle", 40)
        paste_im(base, im, 120, 820, seg(t, s["starts"][1] + 1.8, s["starts"][1] + 2.4))

    _an(base, tl, "S07", t, "think" if t < s["starts"][1] else "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    s = tl["S07"]
    return [(0.3, "pop", None, 0.18), (0.9, "tick", None, 0.14),
            (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][1] + 0.6, "tick", None, 0.14),
            (s["starts"][1] + 1.2, "chime", None, 0.12),
            (s["starts"][1] + 1.9, "marker", 0.6, 0.14)]


# ================================================================ S08 — HEALTH CHECK
def _dash(base, x0, y0, x1, y1, p, color, width=3, dash=12, gap=9):
    if p <= 0:
        return
    L = math.hypot(x1 - x0, y1 - y0) or 1
    d = ImageDraw.Draw(base)
    n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = (i * (dash + gap)) / L
        if a >= p:
            break
        b = min(a + dash / L, p)
        d.line([x0 + (x1 - x0) * a, y0 + (y1 - y0) * a,
                x0 + (x1 - x0) * b, y0 + (y1 - y0) * b], fill=color, width=width)


def draw_S08(t, tl):
    base, d = _base("08 · HEALTH CHECK")
    s = tl["S08"]
    _head(base, "Health Check — tự loại server lỗi", "LB định kỳ hỏi từng server: còn sống không?",
          p=seg(t, 0.1, 0.7))
    fail = t >= s["starts"][1] + 0.8
    rec = t >= s["starts"][2] + 0.6

    _lbhex(base, 240, 500, 62, 1, BLUE, "LB")
    ftxt(base, 240, 582, "LOAD BALANCER", font_semi(19), NAVY, 1, "mm")

    for i, cy in enumerate((400, 520, 640)):
        st = "bad" if (i == 1 and fail and not rec) else "ok"
        srv_card(base, 800, cy - 50, 300, 100, i + 1, st, 1)
        _dash(base, 302, 500, 800, cy, 1, (150, 168, 196, 255), 2, 10, 8)
        qq = (t * 0.6 + i * 0.3) % 1.0
        dot(base, 302 + (800 - 302) * qq, 500 + (cy - 500) * qq, 5, TEAL, 0.9)

    im = sp_chip("GET /health", TEAL, MINT, 18, "activity", 38)
    paste_im(base, im, 520, 296, seg(t, 0.4, 0.8))

    base.alpha_composite(card(330, 420), (1180, 320))
    ftxt(base, 1208, 356, "TRẠNG THÁI", font_semi(18), MUT, 1)
    for i, cy in enumerate((430, 500, 570)):
        if i == 1 and fail and not rec:
            col, txt = RED, "TIMEOUT"
        elif i == 1 and rec:
            col, txt = GREEN, "200 OK"
        else:
            col, txt = GREEN, "200 OK"
        dot(base, 1214, cy, 6, col, 1)
        ftxt(base, 1234, cy, f"S0{i+1}", font_semi(18), NAVY, 1)
        ftxt(base, 1480, cy, txt, font("BeVietnamPro-Medium.ttf", 17), col, 1, "rm")
        if i == 1 and fail and not rec:
            ftxt(base, 1208, 596, "Tạm ngắt khỏi nhóm phục vụ", F_S, RED,
                 seg(t, s["starts"][1] + 1.2, s["starts"][1] + 1.7))
        if i == 1 and rec:
            ftxt(base, 1208, 596, "Đã đưa trở lại nhóm", F_S, GREEN,
                 seg(t, s["starts"][2] + 0.6, s["starts"][2] + 1.0))

    if fail and not rec:
        im = sp_chip("TIMEOUT ×3", RED, RED_L, 18, "circle-x", 40)
        paste_im(base, im, 1010, 466, 1)
        for k in range(2):
            cy = (400, 640)[k]
            qq = ((t - s["starts"][1]) * 0.8 + k * 0.5) % 1.0
            packet(base, [(302, 500), (560, 500), (800, cy)], min(1, qq * 1.3), AMBER, 8)
    if rec:
        ring(base, 950, 520, 166, GREEN, seg(t, s["starts"][2] + 0.4,
                                              s["starts"][2] + 0.9), 4)

    if t >= s["starts"][2]:
        ftxt(base, 110, 820, "Một server lỗi không kéo cả website chết theo.", F_M, NAVY,
             seg(t, s["starts"][2] + 0.6, s["starts"][2] + 1.2))

    _an(base, tl, "S08", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    s = tl["S08"]
    ev = [(0.3, "pop", None, 0.18)]
    for k in range(8):
        ev.append((0.8 + k * 1.1, "tick", None, 0.10))
    ev += [(s["starts"][1] + 0.8, "deny", None, 0.22),
           (s["starts"][1] + 1.2, "thud", None, 0.18),
           (s["starts"][2] + 0.6, "success", None, 0.18)]
    return ev


# ================================================================ S09 — THỰC TẾ
def draw_S09(t, tl):
    base, d = _base("09 · THỰC TẾ")
    s = tl["S09"]
    _head(base, "Load Balancer trong thực tế", "Phần mềm, dịch vụ đám mây và giới hạn",
          p=seg(t, 0.1, 0.7))

    if t < s["starts"][1] + 0.15:
        tools = (("Nginx", "Phần mềm · Reverse Proxy", "server"),
                 ("HAProxy", "Phần mềm · Hiệu năng cao", "shield-check"),
                 ("AWS ELB", "Dịch vụ đám mây", "cloud"),
                 ("Google CLB", "Dịch vụ đám mây", "cloud"))
        for i, (nm, ds, ic) in enumerate(tools):
            x = 100 + i * 352
            base.alpha_composite(card(300, 180), (x, 300))
            base.alpha_composite(sp_icon(ic, BLUE, 44), (x + 24, 326))
            ftxt(base, x + 82, 350, nm, font_semi(23), NAVY, seg(t, 0.3 + i * 0.12, 0.8))
            ftxt(base, x + 24, 404, ds, F_S, MUT, seg(t, 0.36 + i * 0.12, 0.9))
            paste_im(base, sp_chip("PHẦN MỀM" if i < 2 else "ĐÁM MÂY",
                                   AMBER_D if i < 2 else TEAL, CREAM if i < 2 else MINT,
                                   15, None, 30), x + 24, 440, 1)
        ftxt(base, 100, 552, "Cùng một vai trò: nhận request và điều phối về backend.",
             F_B, NAVY, seg(t, 0.9, 1.0))

    if s["starts"][1] <= t < s["starts"][2] + 0.3:
        p = seg(t, s["starts"][1], s["starts"][1] + 0.5)
        lines = ["upstream backend {", "    server 192.168.1.101;",
                 "    server 192.168.1.102;", "    server 192.168.1.103;", "}",
                 "server {", "    listen 80;", "    location / {",
                 "        proxy_pass http://backend;", "    }", "}"]
        code_panel(base, 100, 300, 640, lines,
                   typed=seg(t, s["starts"][1] + 0.9, s["starts"][1] + 4.2), title="nginx.conf")
        rrect_a(base, (820, 300, 1380, 660), 18, WHITE, BORDER, 2, p)
        ftxt(base, 850, 340, "UPSTREAM BACKEND", font_semi(20), MUT, p)
        for i, ip in enumerate(("192.168.1.101", "192.168.1.102", "192.168.1.103")):
            rrect_a(base, (850, 380 + i * 70, 1350, 438 + i * 70), 12, ICE, None, 0, p)
            ftxt(base, 874, 409 + i * 70, f"Server 0{i+1}", font_semi(19), NAVY, p)
            ftxt(base, 1140, 409 + i * 70, ip, font("JetBrainsMono-var.ttf", 18), MUT, p)
        ftxt(base, 850, 604, "Nginx nhận request → chọn backend", F_S, MUT, p)

    if t >= s["starts"][2]:
        q = seg(t, s["starts"][2], s["starts"][2] + 0.7)
        base.alpha_composite(card(1380, 440), (100, 290))
        ftxt(base, 136, 342, "LB KHÔNG CHỮA ĐƯỢC MỌI BỆNH", font_semi(30), RED, q)
        ftxt(base, 136, 390, "Những vấn đề nằm ngoài tầng cân bằng tải:", F_S, MUT, q)
        probs = ("Database quá tải", "Câu SQL chậm", "Thanh toán lỗi",
                 "Phiên đăng nhập", "Đặt hàng trùng", "Thiếu cache")
        for i, txt in enumerate(probs):
            x = 136 + (i % 3) * 440
            y = 440 + (i // 3) * 74
            im = sp_chip(txt, AMBER_D, CREAM, 19, "alert-triangle", 42)
            paste_im(base, im, x, y, seg(t, s["starts"][2] + 0.2 + i * 0.1,
                                          s["starts"][2] + 0.8 + i * 0.1))
        ftxt(base, 136, 640, "Cần xử lý thêm ở tầng dữ liệu và nghiệp vụ.", F_B, NAVY,
             seg(t, s["starts"][2] + 1.0, s["starts"][2] + 1.5))

    _an(base, tl, "S09", t, "present" if t < s["starts"][1] else "write", look=-1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    s = tl["S09"]
    return [(0.3, "pop", None, 0.18), (s["starts"][1], "whoosh", None, 0.16),
            (s["starts"][1] + 1.0, "tick", None, 0.12),
            (s["starts"][1] + 1.6, "tick", None, 0.12),
            (s["starts"][2], "deny", None, 0.18),
            (s["starts"][2] + 1.0, "chime", None, 0.12)]


# ================================================================ S10 — TỔNG KẾT
def draw_S10(t, tl):
    base, d = _base("10 · TỔNG KẾT")
    s = tl["S10"]
    _head(base, "Tóm lại", "Bốn thuật toán · Health Check · bước tiếp theo",
          p=seg(t, 0.1, 0.7))
    q = seg(t, 0.2, 0.8)

    node(base, 100, 300, 220, 120, "smartphone", "Client", None, BLUE, p=q)
    _lbhex(base, 420, 360, 48, q, BLUE, "LB")
    for i in range(3):
        ic = sp_icon("server", TEAL, 44)
        base.alpha_composite(ic, (560 + i * 104, 338))
        ftxt(base, 560 + i * 104 + 22, 398, f"S0{i+1}", F_S, MUT, q)
        draw_conn(d, 468, 360, 560 + i * 104, 360, q, BLUE, width=3)
    draw_conn(d, 320, 360, 372, 360, q, BLUE, width=4)

    im = sp_chip("Health Check loại server lỗi", GREEN, MINT, 19, "shield-check", 44)
    paste_im(base, im, 100, 480, seg(t, 0.5, 0.9))
    ftxt(base, 100, 566, "Bước tiếp theo:", F_S, MUT, seg(t, 0.8, 1.0))
    x = 100
    for nm in ("Cache", "Message Queue", "Database Scaling", "CDN"):
        im = sp_chip(nm, (100, 116, 139, 255), ICE_2, 17, None, 38)
        paste_im(base, im, x, 604, seg(t, 0.9, 1.0))
        x += im.width + 10

    algos = (("Round Robin", "luân phiên", "route"), ("Weighted RR", "theo trọng số", "scale"),
             ("Least Conn.", "ít kết nối nhất", "git-fork"), ("IP Hash", "băm theo IP", "key-round"))
    for i, (nm, ds, ic) in enumerate(algos):
        x = 960 + (i % 2) * 300
        y = 300 + (i // 2) * 160
        base.alpha_composite(card(270, 130), (x, y))
        base.alpha_composite(sp_icon(ic, BLUE, 36), (x + 22, y + 24))
        ftxt(base, x + 70, y + 44, nm, font_semi(20), NAVY, seg(t, 0.45 + i * 0.1, 0.9))
        ftxt(base, x + 22, y + 92, ds, F_S, MUT, seg(t, 0.5 + i * 0.1, 0.95))

    if t >= s["starts"][2]:
        q3 = seg(t, s["starts"][2], s["starts"][2] + 0.7)
        rrect_a(base, (96, 240, 900, 800), 26, NAVY, None, 0, q3)
        ftxt(base, 150, 322, "BÀI 12 · HẠ TẦNG WEB", F_S, AMBER, q3)
        ftxt(base, 150, 386, "CẢM ƠN CÁC BẠN", F_L, WHITE, q3)
        ftxt(base, 150, 478, "AN TECH ACADEMY", font_semi(30), AMBER, q3)
        ftxt(base, 150, 552, "Hiểu Load Balancer là bước đầu", F_B, (200, 214, 236, 255), q3)
        ftxt(base, 150, 594, "để thiết kế hệ thống chịu tải lớn.", F_B, (200, 214, 236, 255), q3)
        im = pill("Theo dõi kênh · Bài tiếp theo", NAVY, AMBER, 20, 48)
        paste_im(base, im, 150, 664, q3)

    _an(base, tl, "S10", t, "wave" if t >= s["starts"][2] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    s = tl["S10"]
    return [(0.3, "pop", None, 0.18), (0.6, "chime", None, 0.12),
            (s["starts"][2], "success", None, 0.2),
            (s["starts"][2] + 0.5, "chime", None, 0.16)]
