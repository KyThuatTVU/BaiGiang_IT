# -*- coding: utf-8 -*-
# Declarative scene specs for the full lecture video. Coordinates in 1920x1080.
# cue = 1-based cue index within the scene; frac = fraction into that cue's audio.
# Element types interpreted by render_full.py. Accent keys map to ACC in render_core.

SCENES = [
 # ---------------- S01 cold open ----------------
 dict(id="S01", accent="cnpm", kicker="CÔNG NGHỆ THÔNG TIN", title="1 ứng dụng = ? người",
      title_font="head56",
      sprites=[
        dict(t="phone", x=820, y=320, color="#2563EB", title="App mua sắm", cue=1, frac=0.0),
        dict(t="icon_label", icon="monitor", label="Giao diện", x=380, y=300, cue=2, frac=0.0),
        dict(t="icon_label", icon="server", label="Máy chủ", x=1300, y=300, cue=2, frac=0.3),
        dict(t="icon_label", icon="database", label="Dữ liệu", x=320, y=580, cue=2, frac=0.6),
        dict(t="icon_label", icon="shield-check", label="Bảo mật", x=1360, y=580, cue=3, frac=0.0),
        dict(t="icon_label", icon="bar-chart-3", label="Phân tích", x=850, y=800, icon_size=80, cue=3, frac=0.3),
      ]),
 # ---------------- S02 wordmark ----------------
 dict(id="S02", accent="cnpm", kicker=None, title=None,
      sprites=[dict(t="wordmark", x=960, y=470, anchor="mm", cue=1, frac=0.0)]),
 # ---------------- S03 goals + 6-node map ----------------
 dict(id="S03", accent="neutral", kicker="MỞ ĐẦU", title="Mục tiêu & lộ trình 6 nhóm",
      sprites=[
        dict(t="check_col", x=120, y=320, dy=100, items=[
            dict(text="Phân biệt 6 nhóm chuyên ngành", cue=1, frac=0.0),
            dict(text="Kể vị trí nghề nghiệp tiêu biểu", cue=2, frac=0.0),
            dict(text="Tự đối chiếu sở thích của bạn", cue=3, frac=0.0)]),
        dict(t="major_node", number=1, label="Công nghệ phần mềm", color="#2563EB", x=1120, y=270, cue=4, frac=0.0),
        dict(t="major_node", number=2, label="Khoa học dữ liệu & AI", color="#7C3AED", x=1120, y=360, cue=4, frac=0.4),
        dict(t="major_node", number=3, label="An toàn thông tin", color="#DC2626", x=1120, y=450, cue=5, frac=0.0),
        dict(t="major_node", number=4, label="Hệ thống thông tin", color="#D97706", x=1120, y=540, cue=5, frac=0.3),
        dict(t="major_node", number=5, label="Mạng & Đám mây", color="#0284C7", x=1120, y=630, cue=5, frac=0.6),
        dict(t="major_node", number=6, label="Đồ họa & Game", color="#0D9488", x=1120, y=720, cue=6, frac=0.0),
      ]),
 # ---------------- S04 pipeline ----------------
 dict(id="S04", accent="cnpm", kicker="CHUYÊN NGÀNH 01", title="Công nghệ phần mềm",
      sprites=[
        dict(t="card", icon="search", label="Phân tích", x=130, y=380, w=290, h=300, icon_size=110, cue=2, frac=0.10),
        dict(t="card", icon="pen-tool", label="Thiết kế", x=470, y=380, w=290, h=300, icon_size=110, cue=2, frac=0.30),
        dict(t="card", icon="code-2", label="Xây dựng", x=810, y=380, w=290, h=300, icon_size=110, cue=2, frac=0.50),
        dict(t="card", icon="bug", label="Kiểm thử", x=1150, y=380, w=290, h=300, icon_size=110, cue=2, frac=0.70),
        dict(t="card", icon="wrench", label="Bảo trì", x=1490, y=380, w=290, h=300, icon_size=110, cue=3, frac=0.10),
      ],
      conns=[
        dict(x0=420, y0=530, x1=470, y1=530, cue=2, frac=0.25),
        dict(x0=760, y0=530, x1=810, y1=530, cue=2, frac=0.45),
        dict(x0=1100, y0=530, x1=1150, y1=530, cue=2, frac=0.65),
        dict(x0=1440, y0=530, x1=1490, y1=530, cue=3, frac=0.05),
      ]),
 # ---------------- S05 three dev columns ----------------
 dict(id="S05", accent="cnpm", kicker="CÔNG NGHỆ PHẦN MỀM", title="Ba hướng lập trình",
      sprites=[
        dict(t="card_bg", x=150, y=250, w=460, h=560, cue=2, frac=0.0),
        dict(t="icon", icon="monitor", x=330, y=280, size=100, cue=2, frac=0.0),
        dict(t="text", text="Frontend", x=380, y=395, font="lbl", color="#0F172A", anchor="mm", cue=2, frac=0.0),
        dict(t="chip_col", cx=380, y=470, dy=74, color="#2563EB", items=[
            dict(text="HTML", cue=3, frac=0.0), dict(text="CSS", cue=3, frac=0.2),
            dict(text="JavaScript", cue=3, frac=0.4), dict(text="React", cue=3, frac=0.6)]),
        dict(t="card_bg", x=730, y=250, w=460, h=560, cue=4, frac=0.0),
        dict(t="icon", icon="server", x=910, y=280, size=100, cue=4, frac=0.0),
        dict(t="text", text="Backend", x=960, y=395, font="lbl", color="#0F172A", anchor="mm", cue=4, frac=0.0),
        dict(t="chip_col", cx=960, y=470, dy=70, color="#2563EB", items=[
            dict(text="Node.js", cue=5, frac=0.0), dict(text="Java", cue=5, frac=0.25),
            dict(text="PHP", cue=5, frac=0.5), dict(text="Python", cue=6, frac=0.0),
            dict(text="C#", cue=6, frac=0.3)]),
        dict(t="card_bg", x=1310, y=250, w=460, h=560, cue=7, frac=0.0),
        dict(t="icon", icon="monitor", x=1420, y=290, size=90, cue=7, frac=0.0),
        dict(t="icon", icon="server", x=1560, y=290, size=90, cue=7, frac=0.0),
        dict(t="text", text="Full-stack", x=1540, y=410, font="lbl", color="#0F172A", anchor="mm", cue=7, frac=0.0),
        dict(t="text", text="làm được cả hai phía", x=1540, y=480, font="sub", color="#475569", anchor="mm", cue=7, frac=0.2),
        dict(t="text", text="React: thư viện  ·  Node.js: runtime", x=960, y=840, font="sub", color="#475569", anchor="mm", cue=7, frac=0.5),
      ],
      conns=[dict(x0=1512, y0=335, x1=1558, y1=335, cue=7, frac=0.1, width=5)]),
 # ---------------- S06 testing ----------------
 dict(id="S06", accent="cnpm", kicker="CÔNG NGHỆ PHẦN MỀM", title="Chạy được ≠ Chạy đúng",
      title_font="big",
      sprites=[
        dict(t="icon", icon="bug", x=420, y=380, size=180, color="#DC2626", cue=2, frac=0.0),
        dict(t="icon", icon="shield-check", x=420, y=380, size=180, color="#2563EB", cue=2, frac=0.5),
        dict(t="check_col", x=820, y=360, dy=110, items=[
            dict(text="Kiểm thử đăng nhập", cue=3, frac=0.2),
            dict(text="Kiểm thử thanh toán", cue=4, frac=0.0),
            dict(text="Kiểm thử giao diện", cue=5, frac=0.0)]),
      ]),
 # ---------------- S07 fit CNPM ----------------
 dict(id="S07", accent="cnpm", kicker="CÔNG NGHỆ PHẦN MỀM", title="Hợp với bạn nếu…",
      sprites=[
        dict(t="fit_card", x=460, y=300, w=1000, h=420, color="#2563EB", cue=1, frac=0.0, bullets=[
            dict(icon="code-2", text="Thích lập trình", cue=1, frac=0.2),
            dict(icon="brain", text="Tư duy logic", cue=1, frac=0.6),
            dict(icon="hammer", text="Muốn tự tay làm sản phẩm thực tế", cue=2, frac=0.2)]),
      ]),
 # ---------------- S08 data sources ----------------
 dict(id="S08", accent="ai", kicker="CHUYÊN NGÀNH 02 · KHOA HỌC DỮ LIỆU & AI", title="Dữ liệu ở khắp nơi",
      sprites=[
        dict(t="icon_label", icon="search", label="Tìm kiếm", x=200, y=300, cue=2, frac=0.0),
        dict(t="icon_label", icon="play", label="Xem video", x=200, y=520, cue=2, frac=0.3),
        dict(t="icon_label", icon="shopping-cart", label="Mua hàng", x=200, y=740, cue=2, frac=0.6),
        dict(t="card", icon="database", label="Dữ liệu thô", x=1350, y=420, w=380, h=340, icon_size=130, cue=3, frac=0.2),
      ],
      conns=[
        dict(x0=420, y0=360, x1=1350, y1=540, cue=3, frac=0.0, dot=True),
        dict(x0=420, y0=580, x1=1350, y1=580, cue=3, frac=0.15, dot=True),
        dict(x0=420, y0=800, x1=1350, y1=620, cue=3, frac=0.3, dot=True),
      ]),
 # ---------------- S09 DS vs AI branch ----------------
 dict(id="S09", accent="ai", kicker="KHOA HỌC DỮ LIỆU & AI", title="Hai nhánh: Data Science & AI",
      sprites=[
        dict(t="card", icon="database", label="Dữ liệu", x=770, y=250, w=380, h=250, icon_size=100, cue=1, frac=0.0),
        dict(t="card", icon="bar-chart-3", label="Data Science", sub="xu hướng · quy luật", x=280, y=560, w=460, h=280, icon_size=100, cue=1, frac=0.3),
        dict(t="card", icon="brain", label="AI", sub="học · nhiệm vụ thông minh", x=1180, y=560, w=460, h=280, icon_size=100, cue=3, frac=0.2),
      ],
      conns=[
        dict(x0=860, y0=500, x1=510, y1=560, cue=1, frac=0.2),
        dict(x0=1060, y0=500, x1=1410, y1=560, cue=3, frac=0.1),
      ]),
 # ---------------- S10 recommender (like sample) ----------------
 dict(id="S10", accent="ai", kicker="KHOA HỌC DỮ LIỆU & AI · VÍ DỤ THỰC TẾ", title="Hệ thống gợi ý sản phẩm",
      sprites=[
        dict(t="card", icon="history", label="Lịch sử duyệt web", sub="xem · tìm kiếm · mua hàng", x=150, y=280, cue=1, frac=0.05, hl=1),
        dict(t="card", icon="cpu", label="Mô hình phân tích", sub="học từ dữ liệu", x=750, y=280, cue=2, frac=0.05, hl=2),
        dict(t="phone_card", x=1350, y=280, color="#7C3AED", cue=3, frac=0.05, hl=3),
        dict(t="chip", text="Một ứng dụng rất đời thường của AI", x=960, y=790, anchor="mm", color="#7C3AED", cue=4, frac=0.3),
      ],
      conns=[
        dict(x0=570, y0=490, x1=750, y1=490, cue=2, frac=0.1, dot=True),
        dict(x0=1170, y0=490, x1=1350, y1=490, cue=3, frac=0.1, dot=True),
      ]),
 # ---------------- S11 DS/AI chips ----------------
 dict(id="S11", accent="ai", kicker="KHOA HỌC DỮ LIỆU & AI", title="Công nghệ & nghề nghiệp",
      sprites=[
        dict(t="text", text="Công nghệ", x=120, y=300, font="lbl", color="#7C3AED", cue=1, frac=0.0),
        dict(t="chip_row", cx=960, y=350, color="#7C3AED", items=[
            dict(text="Python", cue=1, frac=0.0), dict(text="SQL", cue=1, frac=0.15),
            dict(text="Pandas", cue=1, frac=0.3), dict(text="Scikit-learn", cue=1, frac=0.45),
            dict(text="TensorFlow", cue=1, frac=0.6), dict(text="PyTorch", cue=1, frac=0.75)]),
        dict(t="text", text="Nghề nghiệp", x=120, y=520, font="lbl", color="#7C3AED", cue=2, frac=0.0),
        dict(t="chip_row", cx=960, y=570, color="#7C3AED", items=[
            dict(text="Data Analyst", cue=2, frac=0.1), dict(text="Data Scientist", cue=2, frac=0.5),
            dict(text="ML Engineer", cue=3, frac=0.1), dict(text="AI Engineer", cue=3, frac=0.5)]),
        dict(t="text", text="Hợp với bạn nếu thích toán, thống kê, và tò mò cách máy học hỏi.", x=960, y=760, font="sub", color="#475569", anchor="mm", cue=4, frac=0.1),
      ]),
 # ---------------- S12 security consequences ----------------
 dict(id="S12", accent="attt", kicker="CHUYÊN NGÀNH 03", title="An toàn thông tin",
      sprites=[
        dict(t="icon", icon="shield-check", x=860, y=400, size=200, color="#DC2626", cue=1, frac=0.2),
        dict(t="card", icon="credit-card", label="Tài khoản bị cắp", x=180, y=300, w=420, h=280, icon_size=100, color="#DC2626", cue=2, frac=0.1),
        dict(t="card", icon="file-warning", label="Rò rỉ dữ liệu", x=1320, y=300, w=420, h=280, icon_size=100, color="#DC2626", cue=3, frac=0.0),
        dict(t="card", icon="server-off", label="Máy chủ bị tấn công", x=750, y=640, w=420, h=250, icon_size=90, color="#DC2626", cue=3, frac=0.4),
      ]),
 # ---------------- S13 security cycle ----------------
 dict(id="S13", accent="attt", kicker="AN TOÀN THÔNG TIN", title="Vòng việc bảo mật",
      sprites=[
        dict(t="icon_label", icon="scan-search", label="Tìm lỗ hổng", x=800, y=250, w=320, cue=1, frac=0.05, hl=1),
        dict(t="icon_label", icon="shield-check", label="Kiểm tra phòng thủ", x=1300, y=480, w=320, cue=1, frac=0.5, hl=1),
        dict(t="icon_label", icon="eye", label="Giám sát", x=800, y=700, w=320, cue=2, frac=0.05, hl=2),
        dict(t="icon_label", icon="ban", label="Ngăn chặn", x=300, y=480, w=320, cue=2, frac=0.4, hl=2),
      ],
      conns=[
        dict(x0=1070, y0=330, x1=1400, y1=480, cue=1, frac=0.4),
        dict(x0=1400, y0=620, x1=1070, y1=760, cue=2, frac=0.0),
        dict(x0=850, y0=760, x1=520, y1=620, cue=2, frac=0.3),
        dict(x0=520, y0=480, x1=850, y1=330, cue=2, frac=0.6),
      ]),
 # ---------------- S14 authorization rule ----------------
 dict(id="S14", accent="attt", kicker="AN TOÀN THÔNG TIN · NGUYÊN TẮC", title=None,
      sprites=[
        dict(t="rule_card", x=360, y=320, w=1200, h=380, color="#DC2626", cue=1, frac=0.0,
             main="Chỉ kiểm thử trong phạm vi được cho phép",
             sub="Bảo mật = bảo vệ, không tấn công tùy tiện"),
      ]),
 # ---------------- S15 security jobs ----------------
 dict(id="S15", accent="attt", kicker="AN TOÀN THÔNG TIN", title="Nghề nghiệp & kiến thức nền",
      sprites=[
        dict(t="text", text="Nghề nghiệp", x=120, y=290, font="lbl", color="#DC2626", cue=1, frac=0.0),
        dict(t="chip_row", cx=960, y=340, color="#DC2626", items=[
            dict(text="Security Analyst", cue=1, frac=0.1), dict(text="Penetration Tester", cue=1, frac=0.4),
            dict(text="Security Engineer", cue=1, frac=0.7)]),
        dict(t="text", text="Kiến thức nền", x=120, y=510, font="lbl", color="#DC2626", cue=2, frac=0.0),
        dict(t="chip_row", cx=960, y=560, color="#DC2626", items=[
            dict(text="Mạng máy tính", cue=2, frac=0.05), dict(text="Hệ điều hành", cue=2, frac=0.25),
            dict(text="Linux", cue=2, frac=0.45), dict(text="Mã hóa", cue=2, frac=0.65),
            dict(text="Bảo mật ứng dụng", cue=3, frac=0.1)]),
        dict(t="text", text="Hợp với bạn nếu cẩn thận, thích khám phá và muốn bảo vệ hệ thống.", x=960, y=760, font="sub", color="#475569", anchor="mm", cue=4, frac=0.1),
      ]),
 # ---------------- S16 IS bridge ----------------
 dict(id="S16", accent="httt", kicker="CHUYÊN NGÀNH 04", title="Hệ thống thông tin",
      sprites=[
        dict(t="panel", title="Doanh nghiệp", icon="briefcase", sub="quy trình + dữ liệu", x=150, y=380, w=480, h=360, color="#B45309", cue=1, frac=0.2),
        dict(t="panel", title="Công nghệ", icon="settings-2", sub="hệ thống", x=1290, y=380, w=480, h=360, color="#B45309", cue=2, frac=0.0),
        dict(t="node_badge", text="Hệ thống thông tin", x=960, y=560, color="#D97706", cue=1, frac=0.5),
      ],
      conns=[
        dict(x0=765, y0=560, x1=630, y1=560, cue=1, frac=0.6),
        dict(x0=1155, y0=560, x1=1290, y1=560, cue=2, frac=0.2),
      ]),
 # ---------------- S17 HR -> BA -> dev ----------------
 dict(id="S17", accent="httt", kicker="HỆ THỐNG THÔNG TIN · VÍ DỤ", title="Từ nghiệp vụ đến đội phát triển",
      sprites=[
        dict(t="card_bg", x=120, y=300, w=460, h=420, cue=1, frac=0.2),
        dict(t="text", text="Quy trình nhân sự", x=350, y=340, font="lbl", color="#B45309", anchor="mm", cue=1, frac=0.2),
        dict(t="check_col", x=160, y=390, dy=78, color="#B45309", items=[
            dict(text="Tuyển dụng", cue=2, frac=0.1), dict(text="Chấm công", cue=2, frac=0.4),
            dict(text="Tính lương", cue=3, frac=0.0), dict(text="Phân quyền", cue=3, frac=0.3)]),
        dict(t="card", icon="file-text", label="Business Analyst", sub="phân tích nghiệp vụ", x=730, y=380, w=460, h=300, icon_size=110, color="#B45309", cue=4, frac=0.2),
        dict(t="card", icon="code-2", label="Đội phát triển", x=1340, y=380, w=460, h=300, icon_size=110, color="#B45309", cue=4, frac=0.6),
      ],
      conns=[
        dict(x0=580, y0=530, x1=730, y1=530, cue=4, frac=0.1),
        dict(x0=1190, y0=530, x1=1340, y1=530, cue=4, frac=0.5),
      ]),
 # ---------------- S18 IS jobs ----------------
 dict(id="S18", accent="httt", kicker="HỆ THỐNG THÔNG TIN", title="Nghề nghiệp & kiến thức",
      sprites=[
        dict(t="text", text="Nghề nghiệp", x=120, y=290, font="lbl", color="#B45309", cue=1, frac=0.0),
        dict(t="chip_row", cx=960, y=340, color="#D97706", txt="#B45309", items=[
            dict(text="System Analyst", cue=1, frac=0.1), dict(text="Database Administrator", cue=1, frac=0.5),
            dict(text="Chuyên viên ERP", cue=2, frac=0.2)]),
        dict(t="text", text="Kiến thức", x=120, y=510, font="lbl", color="#B45309", cue=3, frac=0.0),
        dict(t="chip_row", cx=960, y=560, color="#D97706", txt="#B45309", items=[
            dict(text="SQL", cue=3, frac=0.05), dict(text="CSDL", cue=3, frac=0.2),
            dict(text="UML", cue=3, frac=0.35), dict(text="BPMN", cue=3, frac=0.5),
            dict(text="Phân tích nghiệp vụ", cue=4, frac=0.0), dict(text="Thiết kế hệ thống", cue=4, frac=0.4)]),
      ]),
 # ---------------- S19 fit IS ----------------
 dict(id="S19", accent="httt", kicker="HỆ THỐNG THÔNG TIN", title="Hợp với bạn nếu…",
      sprites=[
        dict(t="fit_card", x=460, y=300, w=1000, h=420, color="#D97706", cue=1, frac=0.0, bullets=[
            dict(icon="puzzle", text="Thích phân tích vấn đề", cue=1, frac=0.2),
            dict(icon="building-2", text="Tìm hiểu cách doanh nghiệp vận hành", cue=2, frac=0.1),
            dict(icon="handshake", text="Làm cầu nối người dùng – đội lập trình", cue=2, frac=0.6)]),
      ]),
 # ---------------- S20 campus network ----------------
 dict(id="S20", accent="mang", kicker="CHUYÊN NGÀNH 05", title="Mạng máy tính & Đám mây",
      sprites=[
        dict(t="icon_label", icon="network", label="Router", x=850, y=420, icon_size=120, cue=2, frac=0.0),
        dict(t="icon_label", icon="monitor", label="Cụm PC", x=250, y=280, cue=2, frac=0.3),
        dict(t="icon_label", icon="wifi", label="Wi-Fi AP", x=250, y=640, cue=2, frac=0.5),
        dict(t="icon_label", icon="server", label="Máy chủ", x=1450, y=460, cue=2, frac=0.7),
      ],
      conns=[
        dict(x0=850, y0=470, x1=470, y1=340, cue=3, frac=0.0, dot=True),
        dict(x0=850, y0=520, x1=470, y1=700, cue=3, frac=0.2),
        dict(x0=1070, y0=480, x1=1450, y1=520, cue=3, frac=0.4),
      ]),
 # ---------------- S21 network work ----------------
 dict(id="S21", accent="mang", kicker="MẠNG MÁY TÍNH & ĐÁM MÂY", title="Công việc & kiến thức nền",
      sprites=[
        dict(t="icon", icon="server-cog", x=200, y=360, size=200, color="#0284C7", cue=1, frac=0.0),
        dict(t="check_col", x=620, y=320, dy=90, items=[
            dict(text="Thiết kế mạng", cue=1, frac=0.1), dict(text="Cấu hình", cue=1, frac=0.35),
            dict(text="Triển khai", cue=1, frac=0.6), dict(text="Bảo trì", cue=2, frac=0.1)]),
        dict(t="chip_row", cx=960, y=720, color="#0284C7", txt="#0369A1", items=[
            dict(text="TCP/IP", cue=3, frac=0.0), dict(text="DNS", cue=3, frac=0.15),
            dict(text="DHCP", cue=3, frac=0.3), dict(text="Linux", cue=3, frac=0.45),
            dict(text="Windows Server", cue=3, frac=0.6), dict(text="Ảo hóa", cue=3, frac=0.75)]),
      ]),
 # ---------------- S22 server vs cloud ----------------
 dict(id="S22", accent="mang", kicker="MẠNG MÁY TÍNH & ĐÁM MÂY", title="Tự mua máy chủ vs thuê đám mây",
      sprites=[
        dict(t="panel", title="Tự mua máy chủ", icon="server", sub="vài tuần", x=180, y=300, w=620, h=380, color="#0369A1", cue=1, frac=0.1),
        dict(t="panel", title="Đám mây", icon="cloud", sub="vài phút", x=1120, y=300, w=620, h=380, color="#0284C7", cue=2, frac=0.1, hl=5),
        dict(t="chip_row", cx=1430, y=730, color="#0284C7", txt="#0369A1", items=[
            dict(text="Amazon Web Services", cue=3, frac=0.0), dict(text="Microsoft Azure", cue=3, frac=0.35),
            dict(text="Google Cloud", cue=3, frac=0.7)]),
      ]),
 # ---------------- S23 infra jobs ----------------
 dict(id="S23", accent="mang", kicker="MẠNG MÁY TÍNH & ĐÁM MÂY", title="Nghề nghiệp hạ tầng",
      sprites=[
        dict(t="chip_row", cx=960, y=360, color="#0284C7", txt="#0369A1", items=[
            dict(text="Network Engineer", cue=1, frac=0.05), dict(text="System Administrator", cue=1, frac=0.35),
            dict(text="Cloud Engineer", cue=1, frac=0.65), dict(text="IT Support", cue=2, frac=0.2)]),
        dict(t="text", text="Hợp với bạn nếu thích tìm hiểu cách Internet, máy chủ và thiết bị kết nối.", x=960, y=620, font="sub", color="#475569", anchor="mm", cue=3, frac=0.1),
      ]),
 # ---------------- S24 game parallax (custom) ----------------
 dict(id="S24", accent="game", kicker="CHUYÊN NGÀNH 06", title="Đồ họa & Game", custom="s24",
      sprites=[]),
 # ---------------- S25 game products ----------------
 dict(id="S25", accent="game", kicker="ĐỒ HỌA & GAME", title="Phổ sản phẩm của lĩnh vực",
      sprites=[
        dict(t="card", icon="gamepad-2", label="Game", x=110, y=380, w=320, h=300, icon_size=110, color="#0D9488", cue=1, frac=0.05),
        dict(t="card", icon="box", label="Mô hình 3D", x=460, y=380, w=320, h=300, icon_size=110, color="#0D9488", cue=1, frac=0.3),
        dict(t="card", icon="clapperboard", label="Hoạt hình", x=810, y=380, w=320, h=300, icon_size=110, color="#0D9488", cue=1, frac=0.55),
        dict(t="card", icon="cog", label="Mô phỏng", x=1160, y=380, w=320, h=300, icon_size=110, color="#0D9488", cue=2, frac=0.05),
        dict(t="card", icon="glasses", label="VR", x=1510, y=380, w=320, h=300, icon_size=110, color="#0D9488", cue=2, frac=0.3),
      ]),
 # ---------------- S26 game tech ----------------
 dict(id="S26", accent="game", kicker="ĐỒ HỌA & GAME", title="Công nghệ & nghề nghiệp",
      sprites=[
        dict(t="text", text="Công nghệ", x=120, y=290, font="lbl", color="#0F766E", cue=1, frac=0.0),
        dict(t="chip_row", cx=960, y=340, color="#0D9488", txt="#0F766E", items=[
            dict(text="Unity", cue=1, frac=0.0), dict(text="Unreal Engine", cue=1, frac=0.2),
            dict(text="C#", cue=1, frac=0.4), dict(text="C++", cue=1, frac=0.55),
            dict(text="Blender", cue=1, frac=0.7)]),
        dict(t="text", text="Nghề nghiệp", x=120, y=510, font="lbl", color="#0F766E", cue=3, frac=0.0),
        dict(t="chip_row", cx=960, y=560, color="#0D9488", txt="#0F766E", items=[
            dict(text="Game Developer", cue=3, frac=0.05), dict(text="Game Designer", cue=3, frac=0.35),
            dict(text="3D Artist", cue=3, frac=0.65), dict(text="Graphics Programmer", cue=4, frac=0.2)]),
        dict(t="text", text="Unity / Unreal: engine", x=960, y=760, font="sub", color="#475569", anchor="mm", cue=2, frac=0.2),
      ]),
 # ---------------- S27 fit game ----------------
 dict(id="S27", accent="game", kicker="ĐỒ HỌA & GAME", title="Hợp với bạn nếu…",
      sprites=[
        dict(t="fit_card", x=460, y=300, w=1000, h=420, color="#0D9488", cue=1, frac=0.0, bullets=[
            dict(icon="palette", text="Mê công nghệ, thích thiết kế hình ảnh", cue=1, frac=0.2),
            dict(icon="code-2", text="Yêu trò chơi điện tử", cue=2, frac=0.1),
            dict(icon="gamepad-2", text="Làm thế giới ảo chuyển động đúng và mượt", cue=3, frac=0.2)]),
      ]),
 # ---------------- S28 no best major ----------------
 dict(id="S28", accent="neutral", kicker="LỰA CHỌN CỦA BẠN", title="Không có “tốt nhất” — chỉ có “phù hợp”",
      title_font="big",
      sprites=[
        dict(t="dim_map", x=960, y=560, cue=1, frac=0.0),
      ]),
 # ---------------- S29 mapping table ----------------
 dict(id="S29", accent="neutral", kicker="GHÉP SỞ THÍCH → CHUYÊN NGÀNH", title="Bạn hợp với nhóm nào?",
      sprites=[
        dict(t="map_rows", x=160, y=270, dy=95, rows=[
            dict(left="Thích lập trình, xây ứng dụng", right="Công nghệ phần mềm", color="#2563EB", cue=1),
            dict(left="Mê phân tích dữ liệu và AI", right="Khoa học dữ liệu", color="#7C3AED", cue=2),
            dict(left="Quan tâm bảo mật, phòng chống tấn công", right="An toàn thông tin", color="#DC2626", cue=3),
            dict(left="Thích quy trình và bài toán quản lý", right="Hệ thống thông tin", color="#D97706", cue=4),
            dict(left="Mê hạ tầng, máy chủ, kết nối mạng", right="Mạng và đám mây", color="#0284C7", cue=5),
            dict(left="Đam mê hình ảnh, thiết kế, trò chơi", right="Đồ họa và game", color="#0D9488", cue=6)]),
      ]),
 # ---------------- S30 countdown (custom, dark) ----------------
 dict(id="S30", accent="neutral", kicker=None, title=None, custom="s30", dark=True, sprites=[]),
 # ---------------- S31 advice ----------------
 dict(id="S31", accent="cnpm", kicker="LỜI KHUYÊN", title="Thực hành trước khi chọn",
      sprites=[
        dict(t="icon", icon="lightbulb", x=860, y=250, size=140, color="#2563EB", cue=1, frac=0.0),
        dict(t="steps", y=560, color="#2563EB", steps=[
            dict(text="Tìm hiểu bản chất", cue=3, frac=0.0),
            dict(text="Thực hành dự án nhỏ", cue=3, frac=0.5),
            dict(text="Tự đánh giá phù hợp", cue=4, frac=0.2)]),
      ]),
 # ---------------- S32 three takeaways ----------------
 dict(id="S32", accent="cnpm", kicker="TỔNG KẾT", title="Ba hành trang cốt lõi",
      sprites=[
        dict(t="card", icon="book-open", label="Nền tảng vững", x=200, y=380, w=460, h=340, icon_size=130, cue=4, frac=0.05),
        dict(t="card", icon="hammer", label="Thực hành", x=730, y=380, w=460, h=340, icon_size=130, cue=4, frac=0.5),
        dict(t="card", icon="refresh-cw", label="Học không ngừng", x=1260, y=380, w=460, h=340, icon_size=130, cue=5, frac=0.1),
      ]),
 # ---------------- S33 call to action ----------------
 dict(id="S33", accent="cnpm", kicker="KẾT NỐI", title="Bạn nghiêng về chuyên ngành nào?",
      sprites=[
        dict(t="icon_label", icon="message-circle", label="Để lại câu trả lời", x=480, y=420, icon_size=130, cue=2, frac=0.0),
        dict(t="icon_label", icon="rocket", label="Thử dự án nhỏ đầu tiên", x=1180, y=420, icon_size=130, cue=2, frac=0.5),
        dict(t="text", text="ngay tuần này nhé!", x=960, y=720, font="lbl", color="#2563EB", anchor="mm", cue=3, frac=0.1),
      ]),
 # ---------------- S34 outro wordmark ----------------
 dict(id="S34", accent="cnpm", kicker=None, title=None,
      sprites=[
        dict(t="wordmark", x=960, y=430, anchor="mm", cue=1, frac=0.0),
        dict(t="text", text="Hẹn gặp lại ở bài học tiếp theo", x=960, y=680, font="tag", color="#475569", anchor="mm", cue=4, frac=0.1),
      ]),
]