# -*- coding: utf-8 -*-
"""Ba cảnh mẫu Cổng B: M1 intro, M2 sơ đồ 4 nhóm, M3 luồng đăng nhập.
Mỗi cảnh: draw(t, tl) -> frame RGBA; events(tl) -> [(t, sfx, dur, gain)]."""
import math
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, F_TITLE, F_H2, F_H3, F_BODY,
                  F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_CODE, F_SUB,
                  ease, seg, lin, tw, wrap, draw_rich, bg_canvas, brand_mark, watermark,
                  card, sp_icon, sp_chip, sp_title, paste_sprite, draw_conn, draw_marker,
                  subtitle_band, subs_for, cue_t, hx)
import character

ORDER = ["M1", "M2", "M3"]
XFADE = 0.3

def talking(tl, sid, t):
    s = tl[sid]
    return any(st <= t < st + du for st, du in zip(s["starts"], s["durs"]))

def path_pos(pts, q):
    q = max(0.0, min(1.0, q))
    L = [math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1]) for i in range(len(pts)-1)]
    tot = sum(L)
    d = q * tot
    for i, l in enumerate(L):
        if d <= l or i == len(L)-1:
            r = d / l if l else 0
            return (pts[i][0] + (pts[i+1][0]-pts[i][0]) * r,
                    pts[i][1] + (pts[i+1][1]-pts[i][1]) * r)
        d -= l
    return pts[-1]

# ================= M1 — INTRO =================
def draw_M1(t, tl):
    base = bg_canvas()
    d = ImageDraw.Draw(base)
    brand_mark(base, seg(t, 0.15, 1.0))
    watermark(base)
    p = seg(t, 0.6, 1.4)
    title = "Bên trong một dự án phát triển phần mềm"
    lines = wrap(title, F_TITLE, 1250)
    y = 250
    for ln in lines:
        im_ln = Image.new("RGBA", (int(tw(ln, F_TITLE)) + 4, 76), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im_ln)
        draw_rich(dd, (0, 38), ln, F_TITLE, NAVY, "lm")
        paste_sprite(base, im_ln, W/2, y, p, "mm")
        y += 78
    sub = "Học công nghệ cùng An · Ví dụ xuyên suốt: website bán hàng"
    paste_sprite(base, sp_chip(sub, MUT, WHITE, 26), W/2, y + 26, seg(t, 1.2, 1.9), "mt")
    draw_marker(d, W/2 - 300, 306, W/2 + 300, 306, seg(t, 1.6, 2.4), AMBER, 7, 3)
    c1 = cue_t(tl, "M1", 1)
    du1 = tl["M1"]["durs"][0]
    chips = [("lightbulb", "Ai lên ý tưởng?", BLUE),
             ("kanban", "Ai chia việc?", TEAL),
             ("circle-check", "Ai kiểm tra website?", AMBER_D)]
    xs = [W/2 - 430, W/2, W/2 + 430]
    for i, (ic, lb, col) in enumerate(chips):
        pt = c1 + (0.06 + i * 0.28) * du1
        sp = sp_chip(lb, col, WHITE, 28, ic, h=64)
        paste_sprite(base, sp, xs[i], 640, seg(t, pt, pt + 0.45), "mm")
    pose = "present" if t < 1.2 else "point_right"
    character.paste(base, 120, 920, t, pose, look=1, talking=talking(tl, "M1", t), scale=0.75)
    subtitle_band(d, subs_for(tl, "M1", t))
    return base

def events_M1(tl):
    c1 = cue_t(tl, "M1", 1)
    du1 = tl["M1"]["durs"][0]
    ev = [(0.0, "whoosh", None, 0.8), (0.25, "chime", None, 0.8),
          (1.6, "marker", 0.8, 0.9)]
    for i in range(3):
        ev.append((c1 + (0.06 + i * 0.28) * du1, "pop", None, 0.9))
    return ev

# ================= M2 — SƠ ĐỒ 4 NHÓM =================
GROUPS = [
    ("crown", "Lãnh đạo & định hướng", "CEO · CTO · Project Sponsor", NAVY),
    ("kanban", "Quản lý dự án", "PM · PO · BA", BLUE),
    ("compass", "Quản lý chuyên môn", "Tech Lead · UI/UX Lead · QA Lead", TEAL),
    ("code-xml", "Phát triển & triển khai", "Designer · Frontend · Backend · QA · DevOps", AMBER_D),
]

def _grp_card(i):
    ic, lb, roles, col = GROUPS[i]
    w_, h_ = 900, 122
    im = card(w_, h_)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 10, h_], 5, fill=col)
    icon = sp_icon(ic, col, 56)
    im.paste(icon, (36, 33), icon)
    draw_rich(d, (116, 42), lb, F_H3, NAVY, "lm")
    draw_rich(d, (116, 86), roles, F_SM, MUT, "lm")
    return im

def draw_M2(t, tl):
    base = bg_canvas()
    d = ImageDraw.Draw(base)
    brand_mark(base)
    watermark(base)
    paste_sprite(base, sp_title("Cơ cấu đội ngũ phần mềm", "Bốn nhóm chức năng trong dự án"),
                 110, 110, seg(t, 0.1, 0.7))
    c1 = cue_t(tl, "M2", 1)
    du1 = tl["M2"]["durs"][0]
    x0, y0 = 780, 268
    times = [c1 + (0.10 + i * 0.22) * du1 for i in range(4)]
    cw = min(0.5, 0.12 * du1)
    for i in range(4):
        if i > 0:
            ya = y0 + (i-1) * 152 + 122
            yb = y0 + i * 152
            draw_marker(d, x0 + 450, ya + 4, x0 + 450, yb - 4,
                        seg(t, times[i] - cw, times[i] - 0.05), AMBER, 6, i)
        paste_sprite(base, _grp_card(i), x0, y0 + i * 152, seg(t, times[i], times[i] + 0.5))
    nt = c1 + 0.90 * du1
    paste_sprite(base, sp_chip("Mô hình tham khảo — thực tế tổ chức linh hoạt", AMBER_D, CREAM, 24,
                               "alert-triangle", h=50),
                 x0 + 450, y0 + 4 * 152 - 8, seg(t, nt, nt + 0.5), "mt")
    character.paste(base, 150, 920, t, "point_right", look=1,
                    talking=talking(tl, "M2", t), scale=0.62)
    subtitle_band(d, subs_for(tl, "M2", t))
    return base

def events_M2(tl):
    c1 = cue_t(tl, "M2", 1)
    du1 = tl["M2"]["durs"][0]
    times = [c1 + (0.10 + i * 0.22) * du1 for i in range(4)]
    cw = min(0.5, 0.12 * du1)
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(4):
        ev.append((times[i], "pop", None, 0.9))
        if i > 0:
            ev.append((times[i] - cw, "marker", cw, 0.9))
    ev.append((c1 + 0.90 * du1, "chime", None, 0.7))
    return ev

# ================= M3 — LUỒNG ĐĂNG NHẬP =================
def _node(ic, lb, col, w_=300, h_=190):
    im = card(w_, h_)
    d = ImageDraw.Draw(im)
    icon = sp_icon(ic, col, 72)
    im.paste(icon, ((w_-72)//2, 26), icon)
    draw_rich(d, (w_/2, 140), lb, F_H3, NAVY, "mm")
    return im

def draw_M3(t, tl):
    base = bg_canvas()
    d = ImageDraw.Draw(base)
    brand_mark(base)
    watermark(base)
    paste_sprite(base, sp_title("Chuyện gì xảy ra khi nhấn Đăng nhập?",
                                "Frontend ↔ Backend ↔ Database, kết nối qua API"),
                 110, 100, seg(t, 0.1, 0.7))
    c1 = cue_t(tl, "M3", 1)
    c2 = cue_t(tl, "M3", 2)
    du1 = tl["M3"]["durs"][0]
    du2 = tl["M3"]["durs"][1]
    q = lambda a, b: lin(t, c2 + a * du2, c2 + b * du2)
    f = lambda a, b: seg(t, c1 + a * du1, c1 + b * du1)
    ny = 470
    fe = (250, ny); api = (705, ny + 60); be = (900, ny); db = (1350, ny)
    # connectors vẽ dần trong c1
    draw_conn(d, 550, ny + 95, 660, ny + 95, f(0.14, 0.26), BLUE, width=5)
    draw_conn(d, 790, ny + 95, 900, ny + 95, f(0.30, 0.42), BLUE, width=5)
    draw_conn(d, 1200, ny + 95, 1350, ny + 95, f(0.50, 0.62), TEAL, width=5)
    paste_sprite(base, _node("monitor", "Frontend", BLUE), fe[0], fe[1], f(0.04, 0.14))
    paste_sprite(base, sp_chip("API", BLUE_D, ICE, 30, "link", h=64), api[0] + 45, api[1] + 30,
                 f(0.22, 0.34), "mm")
    paste_sprite(base, _node("server", "Backend", NAVY), be[0], be[1], f(0.38, 0.50))
    paste_sprite(base, _node("database", "Database", TEAL), db[0], db[1], f(0.58, 0.70))
    # mini login card trên Frontend
    lc = card(280, 150)
    dd = ImageDraw.Draw(lc)
    dd.rounded_rectangle([24, 22, 256, 52], 8, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(dd, (36, 37), "email", F_SM, MUT, "lm")
    dd.rounded_rectangle([24, 62, 256, 92], 8, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(dd, (36, 77), "••••••••", F_SM, MUT, "lm")
    clicked = q(0.02, 0.06)
    btn_col = BLUE_D if clicked > 0 else NAVY
    dd.rounded_rectangle([24, 104, 256, 136], 8, fill=btn_col)
    draw_rich(dd, (140, 120), "Đăng nhập", F_SM_M, WHITE, "mm")
    paste_sprite(base, lc, 260, 250, f(0.08, 0.20))
    # bước 1: gói email+mật khẩu FE -> API -> BE
    p1 = q(0.06, 0.34)
    if 0 < p1 < 1:
        pos = path_pos([(550, ny + 95), (705, ny + 95), (900, ny + 95)], ease(p1))
        pk = sp_chip("email + ••••••", AMBER_D, CREAM, 22, "lock", h=46)
        paste_sprite(base, pk, pos[0], pos[1] - 40, 1.0, "mm")
    # bước 2: BE kiểm tra (ring) + truy vấn DB
    ring = q(0.34, 0.5)
    if ring > 0 and t < c2 + 0.70 * du2:
        d.rounded_rectangle([be[0] - 8, ny - 8, be[0] + 308, ny + 198], 22,
                            outline=AMBER, width=5)
        paste_sprite(base, sp_chip("Kiểm tra · xác thực", AMBER_D, CREAM, 22, "shield-check", h=46),
                     be[0] + 120, ny + 230, seg(t, c2 + 0.36 * du2, c2 + 0.42 * du2), "mt")
    p2 = q(0.46, 0.66)
    if 0 < p2 < 1:
        qq = p2 * 2 if p2 < 0.5 else (1 - p2) * 2
        pos = path_pos([(1200, ny + 95), (1350, ny + 95)], ease(qq))
        d.ellipse([pos[0] - 11, pos[1] - 11, pos[0] + 11, pos[1] + 11], fill=TEAL)
        paste_sprite(base, sp_chip("Truy vấn", TEAL, WHITE, 22, "database", h=46),
                     1290, ny + 230, seg(t, c2 + 0.48 * du2, c2 + 0.54 * du2), "mt")
    # bước 3: kết quả BE -> FE + JSON
    p3 = q(0.70, 0.90)
    if 0 < p3 < 1:
        pos = path_pos([(900, ny + 95), (705, ny + 95), (550, ny + 95)], ease(p3))
        pk = sp_chip("kết quả", GREEN, WHITE, 22, "circle-check", h=46)
        paste_sprite(base, pk, pos[0], pos[1] - 40, 1.0, "mm")
    paste_sprite(base, sp_chip("JSON", BLUE_D, ICE, 24, "code-xml", h=50),
                 705, ny - 60, seg(t, c2 + 0.80 * du2, c2 + 0.86 * du2), "mm")
    # toast thành công
    tt = seg(t, c2 + 0.90 * du2, c2 + 0.96 * du2)
    if tt > 0:
        toast = sp_chip("Đăng nhập thành công", GREEN, WHITE, 26, "circle-check", h=58)
        paste_sprite(base, toast, 390, 435, tt, "mm")
    paste_sprite(base, sp_chip("Gửi yêu cầu", BLUE, WHITE, 22, "send", h=46),
                 400, ny + 230, seg(t, c2 + 0.08 * du2, c2 + 0.14 * du2), "mt")
    character.paste(base, 1660, 920, t, "point_left", look=-1,
                    talking=talking(tl, "M3", t), scale=0.55)
    subtitle_band(d, subs_for(tl, "M3", t))
    return base

def events_M3(tl):
    c1 = cue_t(tl, "M3", 1)
    c2 = cue_t(tl, "M3", 2)
    du1 = tl["M3"]["durs"][0]
    du2 = tl["M3"]["durs"][1]
    ev = [(0.0, "whoosh", None, 0.8),
          (c1 + 0.14 * du1, "marker", 0.6, 0.7), (c1 + 0.30 * du1, "marker", 0.6, 0.7),
          (c1 + 0.50 * du1, "marker", 0.6, 0.7),
          (c2 + 0.03 * du2, "click", None, 1.0),
          (c2 + 0.06 * du2, "whoosh", None, 0.8),
          (c2 + 0.36 * du2, "tick", None, 0.9),
          (c2 + 0.48 * du2, "whoosh", None, 0.7),
          (c2 + 0.70 * du2, "whoosh", None, 0.8),
          (c2 + 0.80 * du2, "pop", None, 0.9),
          (c2 + 0.90 * du2, "success", None, 0.9)]
    return ev

DRAW = {"M1": draw_M1, "M2": draw_M2, "M3": draw_M3}
EVENTS = {"M1": events_M1, "M2": events_M2, "M3": events_M3}