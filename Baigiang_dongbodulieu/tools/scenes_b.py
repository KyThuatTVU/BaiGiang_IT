# -*- coding: utf-8 -*-
"""Scenes S19–S34."""
import math
from PIL import Image, ImageDraw
from full_common import *

F_T1 = font("PlusJakartaSans-var.ttf", 40, 800)
F_T2 = font("BeVietnamPro-SemiBold.ttf", 30)
F_B  = font("BeVietnamPro-Regular.ttf", 27)
F_BM = font("BeVietnamPro-Medium.ttf", 27)
F_S  = font("BeVietnamPro-Regular.ttf", 22)
F_SM = font("BeVietnamPro-Medium.ttf", 22)
F_L  = font("BeVietnamPro-SemiBold.ttf", 20)
F_N  = font("PlusJakartaSans-var.ttf", 32, 800)

SETUPS, RENDERERS = {}, {}

def scene(fn):
    sid = fn.__name__.split("_")[-1]
    RENDERERS[sid] = fn
    return fn

_PC, _CL = {}, {}
def code_frames(w, lines, hl, title):
    h = 66 + len(lines) * 34 + 14
    key = (title, w, h)
    if key not in _PC:
        _PC[key] = sp_code([], w, h, title)
    im = _PC[key].copy()
    for i, line in enumerate(lines):
        k = (line, i in hl, w, i)
        if k not in _CL:
            _CL[k] = sp_code_line(line, i in hl, i + 1, w - 36)
        im.paste(_CL[k], (18, 62 + i * 34), _CL[k])
    return im

# ===== S19 =====
PL, PR = [], []
def setup_s19():
    global BANNER19, PL, PR
    BANNER19 = banner("S19", "SyncLab — Mục tiêu", "Hai trình duyệt, một ghi chú")
    PR.clear()
    for letter in "AB":
        im = browser_note(letter, 360, 250, deadline=False, bars=0)
        PR.append(im)
BANNER19 = None

@scene
def render_S19(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER19, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S19"]
    c3, c4, c5 = s["starts"][2], s["starts"][3], s["starts"][4]
    # tiêu đề SyncLab
    tt = card(520, 120, fill=CREAM, outline=(240, 214, 160, 255))
    dt = ImageDraw.Draw(tt)
    dt.text((32, 46), "SyncLab", font=font("PlusJakartaSans-var.ttf", 44, 800), fill=NAVY, anchor="lm")
    dt.text((32, 88), "bảng ghi chú dùng chung", font=F_S, fill=(122, 78, 0, 255), anchor="lm")
    paste(base, tt, 150, 300, seg(t, 0.2, 0.5), "tl")
    # hai trình duyệt
    for i, letter in enumerate("AB"):
        p = seg(t, 0.5 + i * 0.15, 0.75 + i * 0.15)
        if p > 0:
            x = 150 + i * 380
            y = 460
            paste(base, PR[i], x, y, p, "tl")
            dd = ImageDraw.Draw(base)
            if i == 0 and t >= s["starts"][1] + 1.2:
                dd.text((x + 34, y + 168), "Deadline: 20h", font=F_SM, fill=TEAL, anchor="lm")
            if i == 1 and t >= s["starts"][1] + 3.0:
                dd.text((x + 34, y + 168), "Deadline: 20h", font=F_SM, fill=TEAL, anchor="lm")
    # Terminal
    if t >= c3 - 0.3:
        typed1 = ""
        p1 = seg(t, c4 + 0.1, c4 + 0.8)
        if p1 > 0:
            typed1 = "npm init -y"[:max(1, int(len("npm init -y") * p1))]
        typed2 = ""
        p2 = seg(t, c5 + 0.1, c5 + 0.9)
        if p2 > 0:
            typed2 = "npm install express socket.io"[:max(1, int(len("npm install express socket.io") * p2))]
        lines = ["D:\\synclab>"]
        if typed1:
            lines.append("$ " + typed1)
        if p1 >= 1:
            lines.append("# package.json đã được tạo")
        if typed2:
            lines.append("$ " + typed2)
        if p2 >= 1:
            lines.append("# added 79 packages")
        term = terminal(0, 0, 600, lines, "Terminal — synclab")
        p = seg(t, c3 - 0.3, c3)
        if p > 0:
            paste(base, term, 1040, 300, p, "tl")
            if 0 < p2 < 1:
                bw = 520
                d.rounded_rectangle([1064, 300 + term.size[1] - 18, 1064 + bw * p2, 300 + term.size[1] - 6], 6, fill=TEAL)
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S19")), small=True)
    return base

# ===== S20 =====
def setup_s20():
    global BANNER20
    BANNER20 = banner("S20", "Thư viện & cấu trúc", "Express và Socket.IO")

@scene
def render_S20(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER20, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S20"]
    ex = card(560, 190, fill=WHITE); de = ImageDraw.Draw(ex)
    ex.paste(ico("server", BLUE, 60), (30, 36), ico("server", BLUE, 60))
    de.text((108, 52), "Express", font=F_T2, fill=INK, anchor="lm")
    de.text((108, 96), "xây máy chủ Web", font=F_S, fill=MUT, anchor="lm")
    ex.alpha_composite(chip("npm install express", NAVY, WHITE, 18), (30, 128))
    si = card(560, 190, fill=WHITE); ds = ImageDraw.Draw(si)
    si.paste(ico("zap", AMBER, 60), (30, 36), ico("zap", AMBER, 60))
    ds.text((108, 52), "Socket.IO", font=F_T2, fill=INK, anchor="lm")
    ds.text((108, 96), "giao tiếp thời gian thực", font=F_S, fill=MUT, anchor="lm")
    si.alpha_composite(chip("npm install socket.io", NAVY, WHITE, 18), (30, 128))
    paste(base, ex, 160, 330, seg(t, 0.2, 0.5), "tl")
    paste(base, si, 160, 570, seg(t, 0.45, 0.75), "tl")
    # cây thư mục
    cx = 900
    rows = [("synclab/", 0, NAVY), ("server.js", 1, INK), ("public/", 1, INK), ("index.html", 2, MUT)]
    c2 = s["starts"][1]
    for i, (name, lvl, col) in enumerate(rows):
        p = seg(t, c2 - 0.6 + i * 0.35, c2 - 0.3 + i * 0.35)
        if p > 0:
            y = 360 + i * 100
            x = cx + lvl * 70
            im = card(560 - lvl * 60, 74, fill=ICE_2)
            di = ImageDraw.Draw(im)
            icn = "package" if name.endswith("/") else ("code-xml" if name.endswith(".js") else "code-xml")
            im.paste(ico(icn, BLUE if lvl == 0 else MUT, 30), (20, 22), ico(icn, BLUE if lvl == 0 else MUT, 30))
            di.text((64, 37), name, font=F_SM, fill=col, anchor="lm")
            paste(base, im, x, y, p, "tl")
            if i > 0:
                d.line([x - 30, y - 26, x - 30, y + 37], fill=(47, 111, 208, 150), width=3)
                d.line([x - 30, y - 26, x - 8, y - 26], fill=(47, 111, 208, 150), width=3)
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S20")))
    return base

# ===== S21 =====
CODE21 = [
    'const express = require("express");',
    'const http = require("http");',
    'const { Server } = require("socket.io");',
    '',
    'const app = express();',
    'const server = http.createServer(app);',
    'const io = new Server(server);',
    '',
    'app.use(express.static("public"));',
    '',
    'const sharedData = {',
    '  content: "",',
    '  version: 0',
    '};',
]
def setup_s21():
    global BANNER21
    BANNER21 = banner("S21", "Bước 2 — Server", "server.js · khởi tạo")

@scene
def render_S21(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER21, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S21"]
    c2, c3 = s["starts"][1], s["starts"][2]
    hl = set()
    if t >= 0.3:
        hl |= {0, 1, 2}
    if t >= c2 - 0.3:
        hl |= {4, 5, 6, 8}
    if t >= c3 - 0.2:
        hl |= {10, 11, 12, 13}
    im = code_frames(1330, CODE21, hl, "server.js")
    paste(base, im, 96, 260, seg(t, 0.15, 0.45), "tl")
    if t >= c3:
        ch = card(360, 90, fill=CREAM, outline=(240, 214, 160, 255))
        dc = ImageDraw.Draw(ch)
        dc.text((24, 30), "trạng thái chung", font=F_L, fill=(122, 78, 0, 255), anchor="lm")
        dc.text((24, 62), "content + version", font=F_S, fill=(122, 78, 0, 255), anchor="lm")
        paste(base, ch, 96, 890, seg(t, c3, c3 + 0.3), "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S21")), small=True)
    return base

# ===== S22 =====
CODE22 = [
    'io.on("connection", (socket) => {',
    '  socket.emit("sync-state", sharedData);',
    '',
    '  socket.on("update-data", (content) => {',
    '    if (typeof content !== "string") return;',
    '    if (content.length > 500) return;',
    '',
    '    sharedData.content = content;',
    '    sharedData.version += 1;',
    '',
    '    io.emit("data-updated", sharedData);',
    '  });',
    '});',
]
def setup_s22():
    global BANNER22
    BANNER22 = banner("S22", "Server — kết nối & phát sự kiện", "server.js · luồng xử lý")

@scene
def render_S22(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER22, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S22"]
    c2, c3 = s["starts"][1], s["starts"][2]
    hl = set()
    if t >= 0.3:
        hl |= {0, 1}
    if t >= c2 - 0.3:
        hl |= {3, 4, 5, 7, 8}
    if t >= c3 - 0.2:
        hl |= {10}
    im = code_frames(1330, CODE22, hl, "server.js")
    paste(base, im, 96, 260, seg(t, 0.15, 0.45), "tl")
    d = ImageDraw.Draw(base)
    c4 = s["starts"][3] - 0.3
    if t >= c4:
        cap = card(1330, 80, fill=CREAM, outline=(240, 214, 160, 255))
        dc = ImageDraw.Draw(cap)
        dc.text((24, 40), "Lưu ý: bản demo chưa kiểm tra version khi ghi", font=F_S, fill=(122, 78, 0, 255), anchor="lm")
        paste(base, cap, 96, 800, seg(t, c4, c4 + 0.3), "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S22")), small=True)
    return base

# ===== S23 =====
CODE23 = [
    '<!doctype html>',
    '<html lang="vi">',
    '<head>',
    '  <meta charset="utf-8" />',
    '  <title>SyncLab</title>',
    '  <script src="/socket.io/socket.io.js"></script>',
    '</head>',
    '<body>',
    '  <textarea id="content"></textarea>',
    '  <button id="send">Gửi cập nhật</button>',
    '  <p>Phiên bản dữ liệu:',
    '    <span id="ver">0</span></p>',
    '  <script src="app.js"></script>',
    '</body>',
    '</html>',
]
def setup_s23():
    global BANNER23
    BANNER23 = banner("S23", "Bước 3 — Giao diện Client", "public/index.html")

@scene
def render_S23(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER23, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S23"]
    c2, c3 = s["starts"][1], s["starts"][2]
    hl = set()
    if t >= 0.3:
        hl |= {0, 1, 2}
    if t >= c2 - 0.3:
        hl |= {8, 9, 10}
    im = code_frames(900, CODE23, hl, "public/index.html")
    paste(base, im, 90, 260, seg(t, 0.15, 0.45), "tl")
    # mockup UI
    ui = card(560, 480, fill=WHITE)
    du = ImageDraw.Draw(ui)
    du.text((30, 40), "SyncLab", font=font("PlusJakartaSans-var.ttf", 32, 800), fill=NAVY, anchor="lm")
    du.rounded_rectangle([30, 84, 530, 240], 12, fill=(246, 249, 253, 255), outline=BORDER, width=2)
    du.text((48, 110), "Nội dung ghi chú…", font=F_S, fill=(150, 165, 188, 255), anchor="lm")
    du.rounded_rectangle([30, 266, 236, 322], 12, fill=BLUE)
    du.text((133, 294), "Gửi cập nhật", font=F_SM, fill=WHITE, anchor="mm")
    du.text((30, 366), "Phiên bản dữ liệu:", font=F_S, fill=MUT, anchor="lm")
    ui.alpha_composite(chip("0", TEAL, WHITE, 26), (236, 342))
    p = seg(t, c2 - 0.6, c2 - 0.2)
    if p > 0:
        paste(base, ui, 1010, 300, p, "tl")
    # callout io()
    if t >= c3 - 0.2:
        cal = card(560, 92, fill=(11, 27, 51, 255), outline=(11, 27, 51, 255))
        dc = ImageDraw.Draw(cal)
        dc.text((26, 46), "const socket = io();", font=font("JetBrainsMono-var.ttf", 24), fill=(220, 231, 245, 255), anchor="lm")
        paste(base, cal, 1010, 810, seg(t, c3 - 0.1, c3 + 0.2), "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S23")), small=True)
    return base

# ===== S24 =====
CODE24 = [
    'const socket = io();',
    'const content = document.getElementById("content");',
    'const ver = document.getElementById("ver");',
    '',
    'socket.on("sync-state", (data) => {',
    '  content.value = data.content;',
    '  ver.textContent = data.version;',
    '});',
    '',
    'socket.on("data-updated", (data) => {',
    '  content.value = data.content;',
    '  ver.textContent = data.version;',
    '});',
    '',
    'document.getElementById("send").onclick = () => {',
    '  socket.emit("update-data", content.value);',
    '};',
]
def setup_s24():
    global BANNER24
    BANNER24 = banner("S24", "Client app.js", "Nhận sự kiện và gửi cập nhật")

@scene
def render_S24(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER24, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S24"]
    c2 = s["starts"][1]
    hl = set()
    if t >= 0.3:
        hl |= {0}
    if t >= 1.0:
        hl |= {4, 5, 6}
    if t >= 3.0:
        hl |= {9, 10, 11}
    if t >= c2 - 0.3:
        hl |= {14, 15}
    im = code_frames(1060, CODE24, hl, "public/app.js")
    paste(base, im, 96, 260, seg(t, 0.15, 0.45), "tl")
    # bảng sự kiện bên phải
    ev = [("sync-state", "Server → textarea", TEAL, 0.8),
          ("data-updated", "Server → textarea + badge", TEAL, 2.8),
          ("update-data", "Nút Gửi → Server", BLUE, c2 - 0.2)]
    y = 300
    for name, desc, col, t0 in ev:
        p = seg(t, t0, t0 + 0.3)
        if p > 0:
            im2 = card(400, 110, fill=WHITE)
            di = ImageDraw.Draw(im2)
            di.text((22, 34), name, font=font("JetBrainsMono-var.ttf", 20), fill=col, anchor="lm")
            draw_rich(di, (22, 76), desc, F_S, MUT, "lm")
            paste(base, im2, 1200, y, p, "tl")
        y += 140
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S24")), small=True)
    return base

# ===== S25 =====
def setup_s25():
    global BANNER25
    BANNER25 = banner("S25", "Demo hoàn tất", "Hai trình duyệt, một ghi chú")

@scene
def render_S25(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER25, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S25"]
    A = node("globe", "Client A", "đang mở SyncLab", 240, 150)
    B = node("globe", "Client B", "đang mở SyncLab", 240, 150)
    S = node("server", "Server", "giữ trạng thái", 280, 170, tone=TEAL)
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, A, 180, 420, p, "tl")
        paste(base, S, 760, 410, p, "tl")
        paste(base, B, 1280, 420, p, "tl")
    a1 = seg(t, 0.5, 1.2)
    a2 = seg(t, 0.7, 1.4)
    draw_conn(d, 430, 500, 750, 500, a1, BLUE, width=5)
    draw_conn(d, 1050, 500, 1270, 500, a2, BLUE, width=5)
    if t >= 1.4:
        for x, y in ((745, 470), (1045, 470)):
            ic = ico("circle-check", GREEN, 34)
            base.paste(ic, (x, y), ic)
    note = card(620, 110, fill=CREAM, outline=(240, 214, 160, 255))
    dn = ImageDraw.Draw(note)
    dn.text((30, 34), "Cùng một nội dung ghi chú", font=F_L, fill=(122, 78, 0, 255), anchor="lm")
    dn.text((30, 74), "không cần tải lại trang", font=F_S, fill=(122, 78, 0, 255), anchor="lm")
    paste(base, note, 610, 680, seg(t, 1.4, 1.7), "tl")
    st = chip("Demo hoàn tất", GREEN, WHITE, 26, icon="circle-check")
    base.alpha_composite(st, (860, 840))
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S25")))
    return base

# ===== S26 =====
def setup_s26():
    global BANNER26
    BANNER26 = banner("S26", "Chạy thử", "node server.js · localhost:3000")

@scene
def render_S26(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER26, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S26"]
    c1, c2, c3 = s["starts"]
    # terminal
    typed = ""
    p1 = seg(t, c1 + 0.4, c1 + 1.4)
    if p1 > 0:
        typed = "node server.js"[:max(1, int(len("node server.js") * p1))]
    lines = ["D:\\synclab>"]
    if typed:
        lines.append("$ " + typed)
    if p1 >= 1:
        lines.append("# SyncLab đang chạy tại http://localhost:3000")
        lines.append("# Socket.IO đã sẵn sàng")
    term = terminal(0, 0, 820, lines, "Terminal — synclab")
    paste(base, term, 140, 320, seg(t, 0.2, 0.5), "tl")
    # trình duyệt
    br = browser_frame(540, 500, "localhost:3000", letter="1")
    db = ImageDraw.Draw(br)
    if t >= c2 + 0.9:
        db.text((34, 108), "SyncLab", font=font("PlusJakartaSans-var.ttf", 32, 800), fill=NAVY, anchor="lm")
        db.rounded_rectangle([34, 144, 506, 308], 12, fill=(246, 249, 253, 255), outline=BORDER, width=2)
        db.text((52, 174), "Nội dung ghi chú…", font=F_S, fill=(150, 165, 188, 255), anchor="lm")
        db.rounded_rectangle([34, 330, 240, 386], 12, fill=BLUE)
        db.text((137, 358), "Gửi cập nhật", font=F_SM, fill=WHITE, anchor="mm")
        db.text((34, 418), "Phiên bản: 0", font=F_S, fill=MUT, anchor="lm")
    paste(base, br, 1060, 300, seg(t, c2 - 0.4, c2 - 0.1), "tl")
    if t >= c3 - 0.2:
        # tab thứ hai
        tab = card(440, 120, fill=WHITE)
        dt = ImageDraw.Draw(tab)
        dt.rounded_rectangle([0, 0, 440, 50], 16, fill=(240, 246, 253, 255))
        dt.text((24, 26), "SyncLab — tab 2", font=F_SM, fill=INK, anchor="lm")
        dt.text((24, 84), "http://localhost:3000", font=F_S, fill=MUT, anchor="lm")
        paste(base, tab, 1060, 840, seg(t, c3 - 0.2, c3 + 0.1), "tl")
        if t >= c3:
            base.alpha_composite(chip("Đã kết nối máy chủ", GREEN, WHITE, 18), (1092, 440))
        if t >= c3 + 0.5:
            base.alpha_composite(chip("Đã kết nối", GREEN, WHITE, 16), (1300, 848))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S26")), small=True)
    return base

# ===== S27 =====
def setup_s27():
    global BANNER27
    BANNER27 = banner("S27", "Demo cập nhật", "A gửi — B nhận ngay")

@scene
def render_S27(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER27, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S27"]
    c1, c2, c3 = s["starts"]
    txt = "Đây là dữ liệu cập nhật từ người dùng A"
    pt = seg(t, c1 + 1.0, c1 + 4.0)
    shown = txt[:max(0, int(len(txt) * pt))] if pt > 0 else ""
    clicked = t >= c1 + 4.6
    for i, letter in enumerate("AB"):
        x, y = 110 + i * 750, 300
        br = browser_frame(640, 540, "localhost:3000", letter=letter)
        db = ImageDraw.Draw(br)
        db.text((30, 78), "SyncLab", font=font("PlusJakartaSans-var.ttf", 30, 800), fill=NAVY, anchor="lm")
        db.rounded_rectangle([30, 110, 606, 330], 12, fill=(246, 249, 253, 255), outline=BORDER, width=2)
        body = ""
        if i == 0:
            body = shown
        else:
            body = txt if t >= c2 - 0.3 else ""
        db.text((48, 140), body or "Nội dung ghi chú…", font=F_S,
                fill=INK if body else (150, 165, 188, 255), anchor="la")
        db.rounded_rectangle([30, 356, 246, 412], 12, fill=BLUE if i == 0 else (190, 205, 224, 255))
        db.text((138, 384), "Gửi cập nhật", font=F_SM, fill=WHITE if i == 0 else (110, 125, 148, 255), anchor="mm")
        vb = 1 if t >= c3 - 0.2 else 0
        db.text((30, 456), "Phiên bản dữ liệu:", font=F_S, fill=MUT, anchor="lm")
        br.alpha_composite(chip(str(vb), TEAL if vb else (140, 154, 173, 255), WHITE, 24), (250, 432))
        paste(base, br, x, y, seg(t, 0.2 + i * 0.15, 0.45 + i * 0.15), "tl")
    if clicked and t < c2 + 1:
        x, y = 110 + 138, 300 + 384
        for r in (16, 30):
            ph = (t - (c1 + 4.6)) / 0.5
            if 0 < ph < 1:
                d.ellipse([x - r * ph, y - r * ph, x + r * ph, y + r * ph], outline=BLUE, width=3)
    if t >= c2 + 0.4 and t < c3 + 1:
        ch = chip("Không reload", GREEN, WHITE, 20)
        base.alpha_composite(ch, (960, 860))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S27")))
    return base

# ===== S28 =====
def setup_s28():
    global BANNER28
    BANNER28 = banner("S28", "Điều gì xảy ra phía sau?", "update-data → xử lý → data-updated")

@scene
def render_S28(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER28, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S28"]
    A = node("globe", "Client A", "gửi thay đổi", 220, 150)
    S = node("server", "Server", "xử lý + version++", 270, 170, tone=TEAL)
    B = node("globe", "Client B", "nhận sự kiện", 220, 150)
    p = seg(t, 0.2, 0.5)
    if p > 0:
        paste(base, A, 170, 430, p, "tl")
        paste(base, S, 800, 420, p, "tl")
        paste(base, B, 1300, 430, p, "tl")
    c1 = s["starts"][1]
    p1 = seg(t, c1 - 1.0, c1 - 0.5)
    draw_conn(d, 390, 500, 790, 500, p1, BLUE, width=5)
    if p1 > 0.9:
        base.alpha_composite(chip("update-data", BLUE, WHITE, 18), (480, 460))
    p2 = seg(t, c1 + 2.4, c1 + 2.9)
    if p2 > 0:
        ov = Image.new("RGBA", (270, 170), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        do.rounded_rectangle([0, 0, 268, 168], 18, outline=AMBER, width=4)
        base.alpha_composite(ov, (800, 420))
        draw_rich(d, (935, 610), "version 0 → 1", font("PlusJakartaSans-var.ttf", 26, 800), AMBER, "mm")
    p3 = seg(t, c1 + 4.6, c1 + 5.1)
    draw_conn(d, 1070, 500, 1290, 500, p3, TEAL, width=5)
    if p3 > 0.9:
        base.alpha_composite(chip("data-updated", TEAL, WHITE, 18), (1072, 460))
    p4 = seg(t, s["starts"][2] - 0.4, s["starts"][2] + 0.1)
    if p4 > 0:
        ov = Image.new("RGBA", (220, 150), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        do.rounded_rectangle([0, 0, 218, 148], 18, outline=GREEN, width=4)
        base.alpha_composite(ov, (1300, 430))
        base.alpha_composite(chip("nội dung mới", GREEN, WHITE, 18), (1320, 600))
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S28")))
    return base

# ===== S29 =====
APP = []
def setup_s29():
    global BANNER29, APP
    BANNER29 = banner("S29", "Ứng dụng thực tế", "Đồng bộ có mặt ở khắp nơi")
    APP.clear()
    specs = [("kanban", "Quản lý công việc", "nhiều người theo dõi trạng thái"),
             ("shopping-cart", "Bán hàng", "đơn hàng & tồn kho"),
             ("school", "Quản lý lớp học", "danh sách & kết quả"),
             ("chat", "Trò chuyện", "gửi nhận tin nhắn"),
             ("users", "Giáo dục", "học sinh làm bài nhóm")]
    for ic, tt, ss in specs:
        im = card(400, 230, fill=WHITE)
        dd = ImageDraw.Draw(im)
        icn = ico(ic, TEAL if ic in ("chat", "kanban") else BLUE, 52)
        im.paste(icn, (26, 24), icn)
        dd.text((26, 108), tt, font=F_T2, fill=INK, anchor="lm")
        for j, l in enumerate(wrap(ss, F_S, 348)[:2]):
            dd.text((26, 156 + j * 28), l, font=F_S, fill=MUT, anchor="lm")
        APP.append(im)
BANNER29 = None

@scene
def render_S29(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER29, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S29"]
    c2, c3 = s["starts"][1], s["starts"][2]
    slots = [(96, 330, 0.2), (536, 330, c2 - 0.4), (976, 330, c2 + 1.6),
             (96, 600, c2 + 3.2), (536, 600, c3 - 0.2)]
    for i, (x, y, t0) in enumerate(slots):
        paste(base, APP[i], x, y, seg(t, t0, t0 + 0.3), "tl")
    # mini minh họa cho thẻ 1: 3 avatar
    if t >= 0.6:
        d = ImageDraw.Draw(base)
        for i in range(3):
            d.ellipse([320 + i * 52, 360, 358 + i * 52, 398], fill=(214, 228, 245, 255), outline=BLUE, width=2)
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S29")))
    return base

# ===== S30 =====
def setup_s30():
    global BANNER30
    BANNER30 = banner("S30", "Lưu ý & giới hạn", "Truyền nhanh ≠ nhất quán")

@scene
def render_S30(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER30, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S30"]
    c2, c3, c4 = s["starts"][1], s["starts"][2], s["starts"][3]
    # 1: RAM
    ram = card(660, 260, fill=CREAM, outline=(240, 214, 160, 255))
    dr = ImageDraw.Draw(ram)
    dr.text((28, 40), "Dữ liệu lưu trong RAM", font=F_T2, fill=(122, 78, 0, 255), anchor="lm")
    draw_rich(dr, (28, 84), "Khởi động lại Server → mất dữ liệu", F_S, (122, 78, 0, 255), "lm")
    ram.paste(ico("server", (122, 78, 0), 48), (28, 130), ico("server", (122, 78, 0), 48))
    gone = t >= c2 - 1.2
    if not gone:
        dr.rounded_rectangle([110, 146, 300, 210], 10, fill=WHITE, outline=(240, 214, 160, 255), width=2)
        dr.text((205, 178), "ghi chú + version", font=F_S, fill=(122, 78, 0, 255), anchor="mm")
    else:
        cross(dr, 118, 178, 10, RED, 4)
        draw_rich(dr, (140, 178), "dữ liệu biến mất", F_S, RED, "lm")
    paste(base, ram, 96, 300, seg(t, 0.2, 0.5), "tl")
    # 2: DB
    db = card(660, 260, fill=WHITE)
    dd = ImageDraw.Draw(db)
    db.paste(ico("database", BLUE, 52), (28, 30), ico("database", BLUE, 52))
    dd.text((96, 56), "MySQL / PostgreSQL", font=F_T2, fill=INK, anchor="lm")
    dd.text((28, 124), "lưu trữ lâu dài", font=F_S, fill=MUT, anchor="lm")
    dd.text((28, 168), "dữ liệu không mất khi restart", font=F_S, fill=MUT, anchor="lm")
    p2 = seg(t, c2 - 0.2, c2 + 0.3)
    paste(base, db, 800, 300, p2, "tl")
    if p2 > 0:
        draw_conn(d, 760, 470, 798, 470, p2, BLUE, width=5)
    # 3: 4 icon
    icons = [("shield-check", "Xác thực"), ("lock", "Phân quyền"),
             ("wifi-off", "Mất kết nối"), ("merge", "Xung đột")]
    for i, (ic, lab) in enumerate(icons):
        p = seg(t, c3 - 0.4 + i * 0.35, c3 - 0.1 + i * 0.35)
        if p > 0:
            x = 96 + i * 168
            ov = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.rounded_rectangle([0, 0, 149, 149], 20, fill=WHITE, outline=BORDER, width=2)
            icn = ico(ic, BLUE, 54)
            ov.paste(icn, (48, 26), icn)
            do.text((75, 116), lab, font=F_L, fill=INK, anchor="mm")
            if p < 1:
                ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
            base.alpha_composite(ov, (x, 620))
    # 4: ≠
    p4 = seg(t, c4 - 0.4, c4 + 0.2)
    if p4 > 0:
        a = card(280, 150, fill=WHITE)
        da = ImageDraw.Draw(a)
        a.paste(ico("zap", BLUE, 42), (22, 24), ico("zap", BLUE, 42))
        da.text((80, 46), "truyền nhanh", font=F_T2, fill=INK, anchor="lm")
        da.text((22, 108), "Socket.IO", font=F_S, fill=MUT, anchor="lm")
        b = card(280, 150, fill=WHITE)
        db2 = ImageDraw.Draw(b)
        b.paste(ico("database", TEAL, 42), (22, 24), ico("database", TEAL, 42))
        db2.text((80, 46), "nhất quán", font=F_T2, fill=INK, anchor="lm")
        db2.text((22, 108), "logic + lưu trữ", font=F_S, fill=MUT, anchor="lm")
        paste(base, a, 800, 650, p4, "tl")
        paste(base, b, 1180, 650, p4, "tl")
        draw_rich(d, (1130, 725), "≠", font("PlusJakartaSans-var.ttf", 70, 800), RED, "mm")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S30")))
    return base

# ===== S31 =====
CARDS31 = []
def setup_s31():
    global BANNER31, CARDS31
    BANNER31 = banner("S31", "Ưu điểm", "Ba lợi ích chính")
    CARDS31 = [check_card("zap", "Cập nhật gần như tức thì", "trải nghiệm người dùng tốt hơn", 1250, 150, BLUE, name="zap"),
               check_card("users", "Nhiều Client, một trạng thái", "không cần tải lại trang", 1250, 150, TEAL, name="users"),
               check_card("code-xml", "Xây dựng dễ dàng với Socket.IO", "API theo sự kiện", 1250, 150, GREEN)]
BANNER31 = None

@scene
def render_S31(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER31, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S31"]
    for i, im in enumerate(CARDS31):
        t0 = 0.3 if i == 0 else s["starts"][i]
        p = seg(t, t0 - 0.2, t0 + 0.1)
        paste(base, im, 96, 330 + i * 180, p, "tl")
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S31")))
    return base

# ===== S32 =====
def setup_s32():
    global BANNER32
    BANNER32 = banner("S32", "Hạn chế", "Cần cân nhắc khi triển khai")

@scene
def render_S32(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER32, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    s = SC["S32"]
    rows = [("Nhiều kết nối đồng thời", "áp lực lên máy chủ"),
            ("Mất kết nối, xung đột", "cần cơ chế phục hồi"),
            ("Nhiều máy chủ", "cần chia sẻ trạng thái")]
    for i, (tt, ss) in enumerate(rows):
        t0 = 0.3 if i == 0 else s["starts"][i]
        p = seg(t, t0 - 0.2, t0 + 0.1)
        if p > 0:
            im = card(880, 140, fill=WHITE)
            di = ImageDraw.Draw(im)
            im.paste(ico("alert-triangle", RED, 44), (24, 24), ico("alert-triangle", RED, 44))
            di.text((88, 44), tt, font=F_T2, fill=INK, anchor="lm")
            di.text((88, 92), ss, font=F_S, fill=MUT, anchor="lm")
            paste(base, im, 96, 330 + i * 170, p, "tl")
    c2, c3, c4 = s["starts"][1], s["starts"][2], s["starts"][3]
    # minh họa tải server
    if t >= 0.8:
        p = seg(t, 0.8, 1.6)
        d.rounded_rectangle([1060, 350, 1440, 372], 11, fill=(226, 235, 247, 255))
        d.rounded_rectangle([1060, 350, 1060 + 380 * (0.45 + 0.5 * p), 372], 11, fill=RED)
        d.text((1060, 320), "tải máy chủ", font=F_S, fill=MUT, anchor="lm")
        d.text((1440, 320), f"{int(45 + 50 * p)}%", font=font("PlusJakartaSans-var.ttf", 24, 800), fill=RED, anchor="rm")
    if t >= c2:
        p = seg(t, c2 - 0.2, c2 + 0.2)
        ov = Image.new("RGBA", (380, 130), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        do.rounded_rectangle([0, 0, 379, 129], 16, fill=WHITE, outline=BORDER, width=2)
        ic = ico("wifi-off", RED, 44)
        ov.paste(ic, (22, 22), ic)
        do.text((84, 34), "Mất kết nối", font=F_SM, fill=INK, anchor="lm")
        draw_rich(do, (84, 72), "tự kết nối lại", F_S, MUT, "lm")
        do.text((84, 102), "đồng bộ lại trạng thái", font=F_S, fill=MUT, anchor="lm")
        paste(base, ov, 1060, 410, p, "tl")
    if t >= c3:
        p = seg(t, c3 - 0.2, c3 + 0.2)
        for i, x in enumerate((1060, 1300)):
            sv = node("server", f"Server {i + 1}", "riêng trạng thái", 200, 132)
            paste(base, sv, x, 570, p, "tl")
        ad = card(180, 76, fill=CREAM, outline=(240, 214, 160, 255))
        ImageDraw.Draw(ad).text((90, 38), "adapter", font=F_T2, fill=(122, 78, 0, 255), anchor="mm")
        paste(base, ad, 1200, 710, p, "tl")
    if t >= c4:
        p = seg(t, c4 - 0.2, c4 + 0.3)
        chart = card(420, 150, fill=WHITE)
        dc = ImageDraw.Draw(chart)
        dc.text((18, 26), "chi phí hạ tầng", font=F_SM, fill=MUT, anchor="lm")
        for i, h in enumerate((36, 60, 88)):
            dc.rectangle([40 + i * 70, 128 - h, 90 + i * 70, 128], fill=(BLUE if i < 2 else RED))
        paste(base, chart, 96, 840, p, "tl")
    paste_teacher(base, t, pose="C", mouth=mouth_for(t, speak(t, "S32")))
    return base

# ===== S33 =====
def setup_s33():
    global BANNER33
    BANNER33 = banner("S33", "Tổng kết", "Những điểm cần nhớ")

@scene
def render_S33(t):
    base = bg_canvas()
    brand_mark(base)
    paste(base, BANNER33, 1000, 78, seg(t, 0.0, 0.3), "mt")
    s = SC["S33"]
    rows = [("zap", "Đồng bộ dữ liệu thời gian thực là gì", 0.3),
            ("arrow-lr", "Phân biệt HTTP và WebSocket", 1.3),
            ("link", "Client – Server và Event trong Socket.IO", 3.0),
            ("split", "Cách xử lý xung đột dữ liệu", s["starts"][1] - 0.2)]
    for i, (ic, txt, t0) in enumerate(rows):
        p = seg(t, t0, t0 + 0.3)
        if p > 0:
            im = card(1100, 110, fill=WHITE)
            di = ImageDraw.Draw(im)
            im.paste(ico(ic, TEAL if i == 3 else BLUE, 38), (24, 36), ico(ic, TEAL if i == 3 else BLUE, 38))
            di.text((80, 55), txt, font=F_BM, fill=INK, anchor="lm")
            paste(base, im, 96, 330 + i * 130, p, "tl")
    p2 = seg(t, s["starts"][1] + 0.8, s["starts"][1] + 1.1)
    if p2 > 0:
        ch1 = chip("Node.js", TEAL, WHITE, 24)
        ch2 = chip("Socket.IO", TEAL, WHITE, 24)
        base.alpha_composite(ch1, (1100, 860))
        base.alpha_composite(ch2, (1280, 860))
    paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S33")))
    return base

# ===== S34 =====
def setup_s34():
    global WM34, TAG34
    WM34 = Image.new("RGBA", (1200, 130), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(WM34), (600, 65), "AN TECH ACADEMY", F_WM, NAVY, "mm")
    TAG34 = Image.new("RGBA", (1200, 60), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(TAG34), (600, 30), "Học công nghệ, làm chủ tương lai", F_BODY, MUT, "mm")
WM34 = TAG34 = None

@scene
def render_S34(t):
    base = bg_canvas()
    brand_mark(base)
    s = SC["S34"]
    c2, c3 = s["starts"][1], s["starts"][2]
    d = ImageDraw.Draw(base)
    if t < c2 - 0.3:
        paste(base, banner("S34", "Bài tập về nhà", "Phát triển SyncLab thành bảng công việc"), 1000, 78,
              seg(t, 0.0, 0.3), "mt")
        ex = card(980, 460, fill=WHITE)
        de = ImageDraw.Draw(ex)
        de.text((36, 48), "Nâng cấp SyncLab", font=font("PlusJakartaSans-var.ttf", 38, 800), fill=NAVY, anchor="lm")
        for i, (ic, txt) in enumerate([
                ("plus", "Thêm, sửa, cập nhật trạng thái công việc"),
                ("database", "Lưu dữ liệu vào MySQL"),
                ("git-branch", "Kiểm soát phiên bản khi ghi")]):
            ex.paste(ico(ic, TEAL, 36), (36, 130 + i * 96), ico(ic, TEAL, 36))
            de.text((86, 148 + i * 96), txt, font=F_BM, fill=INK, anchor="lm")
        paste(base, ex, 150, 340, seg(t, 0.25, 0.55), "tl")
        paste_teacher(base, t, pose="D", mouth=mouth_for(t, speak(t, "S34")))
    elif t < c3 - 0.3:
        draw_rich(d, (960, 430), "Cảm ơn các bạn đã theo dõi!", font("PlusJakartaSans-var.ttf", 58, 800), NAVY, "mm")
        draw_rich(d, (960, 520), "Hẹn gặp lại trong bài học tiếp theo.", F_BODY, MUT, "mm")
        paste_teacher(base, t, pose="G", mouth=mouth_for(t, speak(t, "S34")))
    else:
        p = seg(t, c3 - 0.2, c3 + 0.3)
        paste(base, WM34, 960, 470, p, "mm")
        u = seg(t, c3 + 1.2, c3 + 1.8)
        hand_underline(d, 400, 1520, 540, u)
        paste(base, TAG34, 960, 610, seg(t, c3 + 0.6, c3 + 1.0), "mm")
        paste_teacher(base, t, pose="wave" if t < c3 + 4 else "D", mouth=mouth_for(t, speak(t, "S34")))
    return base
