# -*- coding: utf-8 -*-
"""17 cảnh full cho video ~7 phút. Mỗi cảnh: draw(t, tl) -> frame RGBA; events(tl) -> [(t, sfx, dur, gain)].
Lịch hiện hình đều theo TỈ LỆ độ dài cue thật để không lệch khi audio dài/ngắn."""
import math
from PIL import Image, ImageDraw
from core import (W, H, BG, NAVY, BLUE, BLUE_D, TEAL, AMBER, AMBER_D, CREAM, INK, MUT,
                  BORDER, WHITE, GREEN, RED, ICE, ICE_2, CODE_BG, F_TITLE, F_H2, F_H3,
                  F_BODY, F_BODY_M, F_SM, F_SM_M, F_LBL, F_LBL_B, F_NUM, F_CODE, F_SUB,
                  font, ease, seg, lin, tw, wrap, rich_width, draw_rich, draw_tracked, bg_canvas,
                  brand_mark, watermark, card, sp_icon, sp_chip, sp_title, paste_sprite,
                  draw_conn, draw_marker, draw_marker_circle, subtitle_band, subs_for, cue_t)
import character

ORDER = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09",
         "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17"]
XFADE = 0.3

ANX = {"S01": (120, 920, 0.75), "S02": (880, 920, 0.60), "S03": (1600, 920, 0.55),
       "S04": (150, 920, 0.62), "S05": (60, 920, 0.55), "S06": (1660, 920, 0.55),
       "S07": (60, 920, 0.55), "S08": (60, 920, 0.55), "S09": (60, 920, 0.50),
       "S10": (1660, 920, 0.55), "S11": (60, 920, 0.55), "S12": (20, 920, 0.50),
       "S13": (60, 920, 0.50), "S14": (60, 920, 0.50), "S15": (60, 920, 0.50),
       "S16": (60, 920, 0.50), "S17": (1620, 920, 0.75)}


def talk(tl, sid, t):
    s = tl[sid]
    return any(st <= t < st + du for st, du in zip(s["starts"], s["durs"]))


def fr(tl, sid, i, a=0.0, b=1.0):
    """Mốc tương đối a..b trong cue i (0-based) của cảnh."""
    s = tl[sid]
    return s["starts"][i] + a * s["durs"][i], s["starts"][i] + b * s["durs"][i]


def _base():
    base = bg_canvas()
    brand_mark(base)
    watermark(base)
    return base, ImageDraw.Draw(base)


def _title(base, tl, sid, t, text, sub, p0=0.06):
    s = tl[sid]
    paste_sprite(base, sp_title(text, sub), 110, 92, seg(t, s["starts"][0] + p0, s["starts"][0] + p0 + 0.55))


def pill(text, color=BLUE, fill=WHITE, size=20, h=36, icon=None, iw=24):
    f = font_semi(size)
    w_ = int(tw(text, f)) + 28 + (iw + 8 if icon else 0)
    im = Image.new("RGBA", (w_, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w_ - 1, h - 1], h // 2, fill=fill, outline=color, width=2)
    x = 14
    if icon:
        ic = sp_icon(icon, color, 18)
        im.paste(ic, (x, (h - 18) // 2), ic)
        x += iw + 4
    draw_rich(d, (x, h / 2), text, f, color, "lm")
    return im


_fs = {}


def font_semi(size):
    if size not in _fs:
        from core import font
        _fs[size] = font("BeVietnamPro-SemiBold.ttf", size)
    return _fs[size]


def path_pos(pts, q):
    q = max(0.0, min(1.0, q))
    L = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    tot = sum(L)
    d = q * tot
    for i, l in enumerate(L):
        if d <= l or i == len(L) - 1:
            r = d / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r,
                    pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r)
        d -= l
    return pts[-1]


def _an(base, tl, sid, t, pose=None, scale=None, look=None):
    x, y, sc = ANX[sid]
    character.paste(base, x, y, t, pose or "present", look=look if look is not None else 0,
                    talking=talk(tl, sid, t), scale=scale or sc)


# ============================================================ S01 INTRO
def draw_S01(t, tl):
    base, d = _base()
    s = tl["S01"]
    p = seg(t, 0.6, 1.4)
    title = "Bên trong một dự án phát triển phần mềm"
    y = 250
    for ln in wrap(title, F_TITLE, 1250):
        im_ln = Image.new("RGBA", (int(tw(ln, F_TITLE)) + 4, 76), (0, 0, 0, 0))
        draw_rich(ImageDraw.Draw(im_ln), (0, 38), ln, F_TITLE, NAVY, "lm")
        paste_sprite(base, im_ln, W / 2, y, p, "mm")
        y += 78
    sub = "Học công nghệ cùng An · Ví dụ xuyên suốt: website bán hàng"
    paste_sprite(base, sp_chip(sub, MUT, WHITE, 26), W / 2, y + 26, seg(t, 1.2, 1.9), "mt")
    draw_marker(d, W / 2 - 300, 306, W / 2 + 300, 306, seg(t, 1.6, 2.4), AMBER, 7, 3)
    chips = [("lightbulb", "Ai lên ý tưởng?", BLUE),
             ("kanban", "Ai chia việc?", TEAL),
             ("circle-check", "Ai kiểm tra website?", AMBER_D)]
    xs = [W / 2 - 430, W / 2, W / 2 + 430]
    for i, (ic, lb, col) in enumerate(chips):
        a, b = fr(tl, "S01", 1, 0.06 + i * 0.28, 0.06 + i * 0.28)
        paste_sprite(base, sp_chip(lb, col, WHITE, 28, ic, h=64), xs[i], 640,
                     seg(t, a, a + 0.45), "mm")
    a2, _ = fr(tl, "S01", 2, 0.30)
    paste_sprite(base, sp_chip("Website bán hàng — ví dụ xuyên suốt", AMBER_D, CREAM, 26,
                               "store", h=58), W / 2, 760, seg(t, a2, a2 + 0.5), "mm")
    c2, _ = fr(tl, "S01", 1)
    _an(base, tl, "S01", t, "present" if t < c2 else "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S01", t))
    return base


def events_S01(tl):
    a = [fr(tl, "S01", 1, 0.06 + i * 0.28)[0] for i in range(3)]
    b = fr(tl, "S01", 2, 0.30)[0]
    return [(0.0, "whoosh", None, 0.8), (0.25, "chime", None, 0.8), (1.6, "marker", 0.8, 0.9)] + \
        [(x, "pop", None, 0.9) for x in a] + [(b, "pop", None, 0.8)]


# ============================================================ S02 KHÁI NIỆM
KW = [("target", "Mục tiêu", "Cần đạt được gì"),
      ("calendar", "Thời gian", "Mốc bắt đầu — kết thúc"),
      ("users", "Nguồn lực", "Con người · ngân sách"),
      ("scan", "Phạm vi", "Làm gì — không làm gì")]


def draw_S02(t, tl):
    base, d = _base()
    _title(base, tl, "S02", t, "Dự án phần mềm là gì?",
           "Tập hợp hoạt động có mục tiêu, thời gian, nguồn lực, phạm vi")
    c1, _ = fr(tl, "S02", 0)
    paste_sprite(base, sp_chip("Một sản phẩm mới hoặc nâng cấp", BLUE, ICE, 24, "rocket", h=52),
                 110, 236, seg(t, c1 + 0.3, c1 + 0.8))
    dc = card(660, 430)
    dd = ImageDraw.Draw(dc)
    for i, (ic, lb, sub) in enumerate(KW):
        yy = 34 + i * 98
        dd.rounded_rectangle([26, yy, 106, yy + 80], 14, fill=ICE)
        icon = sp_icon(ic, [BLUE, TEAL, AMBER_D, NAVY][i], 44)
        dc.paste(icon, (44, yy + 18), icon)
        draw_rich(dd, (128, yy + 26), lb, F_H3, NAVY, "lm")
        draw_rich(dd, (128, yy + 62), sub, F_SM, MUT, "lm")
    paste_sprite(base, dc, 110, 310, seg(t, c1 + 0.5, c1 + 0.95))
    for i in range(4):
        a, b = fr(tl, "S02", 1, 0.12 + i * 0.19, 0.12 + i * 0.19)
        ux0 = 128 + 110
        uw = tw(KW[i][2], F_SM) + 12
        uy = 310 + 34 + i * 98 + 84
        draw_marker(d, ux0, uy, ux0 + uw, uy, seg(t, a, a + 0.35), AMBER, 5, 10 + i)
    # mockup điện thoại
    ph = card(360, 600)
    pd = ImageDraw.Draw(ph)
    pd.rounded_rectangle([16, 14, 344, 90], 16, fill=NAVY)
    draw_rich(pd, (36, 52), "Shop Điện Thoại", F_BODY_M, WHITE, "lm")
    pd.rounded_rectangle([16, 106, 344, 300], 14, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(pd, (180, 200), "Hình sản phẩm", F_SM, MUT, "mm")
    fp = font("PlusJakartaSans-var.ttf", 20, 700)
    for r, (nm, pr) in enumerate([("Điện thoại A", "12.990.000₫"),
                                  ("Điện thoại B", "8.490.000₫")]):
        pd.rounded_rectangle([16, 316 + r * 74, 344, 378 + r * 74], 12, fill=ICE_2,
                             outline=BORDER, width=2)
        draw_rich(pd, (30, 340 + r * 74), nm, F_SM, NAVY, "lm")
        draw_rich(pd, (322, 340 + r * 74), pr, fp, AMBER_D, "rm")
    pd.rounded_rectangle([16, 528, 344, 584], 14, fill=BLUE)
    draw_rich(pd, (180, 556), "Mua ngay", F_BODY_M, WHITE, "mm")
    paste_sprite(base, ph, 1150, 190, seg(t, c1 + 0.8, c1 + 1.3))
    feats = [("package", "Sản phẩm", BLUE), ("shopping-cart", "Giỏ hàng", TEAL),
             ("clipboard-list", "Đặt hàng", NAVY), ("credit-card", "Thanh toán", AMBER_D),
             ("bar-chart-3", "Thống kê", GREEN)]
    for i, (ic, lb, col) in enumerate(feats):
        a, _ = fr(tl, "S02", 2, 0.08 + i * 0.16)
        paste_sprite(base, pill(lb, col, WHITE, 24, 46, ic, 26), 1560, 218 + i * 84,
                     seg(t, a, a + 0.4))
    a3, _ = fr(tl, "S02", 2, 0.86)
    paste_sprite(base, sp_chip("Từ phân tích yêu cầu đến triển khai", NAVY, ICE, 24,
                               "workflow", h=52), 110, 800, seg(t, a3, a3 + 0.4))
    _an(base, tl, "S02", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S02", t))
    return base


def events_S02(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(4):
        ev.append((fr(tl, "S02", 1, 0.12 + i * 0.19)[0], "marker", 0.35, 0.85))
    for i in range(5):
        ev.append((fr(tl, "S02", 2, 0.08 + i * 0.16)[0], "pop", None, 0.85))
    ev.append((fr(tl, "S02", 2, 0.86)[0], "chime", None, 0.7))
    return ev


# ============================================================ S03 CÔNG TY ≠ DỰ ÁN
def draw_S03(t, tl):
    base, d = _base()
    _title(base, tl, "S03", t, "Công ty ≠ Dự án", "Một tổ chức — nhiều dự án song song")
    co = card(1160, 178)
    cd = ImageDraw.Draw(co)
    ic = sp_icon("building-2", NAVY, 56)
    co.paste(ic, (30, 28), ic)
    draw_rich(cd, (104, 56), "Công ty phần mềm", F_H3, NAVY, "lm")
    paste_sprite(base, co, 110, 240, seg(t, 0.1, 0.6))
    projs = [("Website bán hàng", BLUE), ("Quản lý nhân sự", TEAL), ("Đặt lịch khám", AMBER_D)]
    pims = [sp_chip(lb, col, WHITE, 18, "folder", h=42) for lb, col in projs]
    px0 = 430
    for i, im in enumerate(pims):
        a, _ = fr(tl, "S03", 0, 0.18 + i * 0.22)
        paste_sprite(base, im, px0, 342, seg(t, a, a + 0.4))
        px0 += im.size[0] + 26
    # 1 dev ôm hết việc
    ov = card(300, 300)
    od = ImageDraw.Draw(ov)
    ic = sp_icon("user", NAVY, 52)
    ov.paste(ic, (124, 22), ic)
    draw_rich(od, (150, 96), "1 lập trình viên", F_SM_M, NAVY, "mm")
    draw_rich(od, (150, 126), "ôm hết mọi việc?", F_SM, MUT, "mm")
    for i, icn in enumerate(["search", "pen-tool", "code-xml", "flask-conical", "rocket"]):
        a, _ = fr(tl, "S03", 0, 0.45 + i * 0.09)
        pv = seg(t, a, a + 0.3)
        if pv > 0:
            wob = math.sin(t * 7 + i) * 3 * pv
            s_ic = sp_icon(icn, AMBER_D, 30)
            ov.paste(s_ic, (int(40 + (i % 3) * 80 + wob), 160 + (i // 3) * 54), s_ic)
    paste_sprite(base, ov, 110, 450, seg(t, 0.1, 0.6))
    # tách nhóm
    roles = [("search", "Phân tích", BLUE), ("pen-tool", "Thiết kế", TEAL),
             ("code-xml", "Code", NAVY), ("flask-conical", "Kiểm thử", AMBER_D),
             ("rocket", "Triển khai", GREEN)]
    for i, (icn, lb, col) in enumerate(roles):
        a, _ = fr(tl, "S03", 1, 0.10 + i * 0.16)
        paste_sprite(base, pill(lb, col, WHITE, 22, 44, icn, 24), 470, 480 + i * 62,
                     seg(t, a, a + 0.35))
    a3, _ = fr(tl, "S03", 2, 0.20)
    paste_sprite(base, sp_chip("Chia theo chuyên môn — chung một mục tiêu", AMBER_D, CREAM, 26,
                               "users", h=56), 470, 810, seg(t, a3, a3 + 0.45))
    draw_marker(d, 480, 862, 1000, 862, seg(t, a3 + 0.35, a3 + 0.8), AMBER, 6, 21)
    _an(base, tl, "S03", t, "think" if t < fr(tl, "S03", 2)[0] else "present", look=-1)
    subtitle_band(d, subs_for(tl, "S03", t))
    return base


def events_S03(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(3):
        ev.append((fr(tl, "S03", 0, 0.18 + i * 0.22)[0], "pop", None, 0.85))
    for i in range(5):
        ev.append((fr(tl, "S03", 0, 0.45 + i * 0.09)[0], "pop", None, 0.6))
    for i in range(5):
        ev.append((fr(tl, "S03", 1, 0.10 + i * 0.16)[0], "whoosh", 0.3, 0.6))
    ev.append((fr(tl, "S03", 2, 0.20)[0], "chime", None, 0.7))
    return ev


# ============================================================ S04 BỐN NHÓM
G4 = [("crown", "Lãnh đạo & định hướng", "CEO · CTO · Project Sponsor", NAVY),
      ("kanban", "Quản lý dự án", "PM · PO · BA", BLUE),
      ("compass", "Quản lý chuyên môn", "Tech Lead · UI/UX Lead · QA Lead", TEAL),
      ("code-xml", "Phát triển & triển khai", "Designer · Frontend · Backend · QA · DevOps", AMBER_D)]


def _g4(i):
    ic, lb, roles, col = G4[i]
    im = card(900, 122)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 10, 122], 5, fill=col)
    icon = sp_icon(ic, col, 56)
    im.paste(icon, (36, 33), icon)
    draw_rich(d, (116, 42), lb, F_H3, NAVY, "lm")
    draw_rich(d, (116, 86), roles, F_SM, MUT, "lm")
    return im


def draw_S04(t, tl):
    base, d = _base()
    _title(base, tl, "S04", t, "Cơ cấu đội ngũ phần mềm", "Bốn nhóm chức năng trong dự án")
    x0, y0 = 780, 268
    times = [fr(tl, "S04", 0, 0.10 + i * 0.22)[0] for i in range(4)]
    cw = min(0.5, 0.12 * tl["S04"]["durs"][0])
    for i in range(4):
        if i > 0:
            ya, yb = y0 + (i - 1) * 152 + 122, y0 + i * 152
            draw_marker(d, x0 + 450, ya + 4, x0 + 450, yb - 4,
                        seg(t, times[i] - cw, times[i] - 0.05), AMBER, 6, i)
        paste_sprite(base, _g4(i), x0, y0 + i * 152, seg(t, times[i], times[i] + 0.5))
    nt = fr(tl, "S04", 1, 0.18)[0]
    paste_sprite(base, sp_chip("Mô hình tham khảo — thực tế tổ chức linh hoạt", AMBER_D, CREAM, 24,
                               "alert-triangle", h=50), x0 + 450, y0 + 4 * 152 - 8,
                 seg(t, nt, nt + 0.5), "mt")
    _an(base, tl, "S04", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S04", t))
    return base


def events_S04(tl):
    times = [fr(tl, "S04", 0, 0.10 + i * 0.22)[0] for i in range(4)]
    cw = min(0.5, 0.12 * tl["S04"]["durs"][0])
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(4):
        ev.append((times[i], "pop", None, 0.9))
        if i > 0:
            ev.append((times[i] - cw, "marker", cw, 0.9))
    ev.append((fr(tl, "S04", 1, 0.18)[0], "chime", None, 0.7))
    return ev


# ============================================================ S05 LÃNH ĐẠO
def draw_S05(t, tl):
    base, d = _base()
    _title(base, tl, "S05", t, "Nhóm lãnh đạo & định hướng",
           "CEO · CTO · Project Sponsor")
    cards = []
    # CEO
    im = card(480, 470)
    dd = ImageDraw.Draw(im)
    ic = sp_icon("crown", NAVY, 64)
    im.paste(ic, (34, 30), ic)
    draw_rich(dd, (34, 118), "CEO", F_H3, NAVY, "lm")
    draw_rich(dd, (34, 156), "Giám đốc điều hành", F_SM, MUT, "lm")
    for j, ln in enumerate(["Chiến lược kinh doanh", "Khách hàng · Doanh thu"]):
        draw_rich(dd, (34, 206 + j * 38), ln, F_SM, INK, "lm")
    cards.append(im)
    # CTO
    im = card(480, 470)
    dd = ImageDraw.Draw(im)
    ic = sp_icon("terminal", BLUE, 64)
    im.paste(ic, (34, 30), ic)
    draw_rich(dd, (34, 118), "CTO", F_H3, NAVY, "lm")
    draw_rich(dd, (34, 156), "Giám đốc công nghệ", F_SM, MUT, "lm")
    draw_rich(dd, (34, 206), "Định hướng công nghệ", F_SM, INK, "lm")
    draw_rich(dd, (34, 242), "Kiến trúc hệ thống", F_SM, INK, "lm")
    pairs = [("Node.js", "PHP"), ("MySQL", "PostgreSQL")]
    for r, (a, b) in enumerate(pairs):
        dd.rounded_rectangle([34, 288 + r * 58, 156, 330 + r * 58], 10, fill=ICE,
                             outline=BORDER, width=2)
        draw_rich(dd, (95, 309 + r * 58), a, F_LBL, BLUE_D, "mm")
        draw_rich(dd, (176, 309 + r * 58), "hoặc", F_SM, MUT, "lm")
        dd.rounded_rectangle([246, 288 + r * 58, 446, 330 + r * 58], 10, fill=ICE,
                             outline=BORDER, width=2)
        draw_rich(dd, (346, 309 + r * 58), b, F_LBL, TEAL, "mm")
    cards.append(im)
    # Sponsor
    im = card(480, 470)
    dd = ImageDraw.Draw(im)
    ic = sp_icon("shield-check", TEAL, 64)
    im.paste(ic, (34, 30), ic)
    draw_rich(dd, (34, 118), "Project Sponsor", F_H3, NAVY, "lm")
    draw_rich(dd, (34, 156), "Người bảo trợ dự án", F_SM, MUT, "lm")
    for j, ln in enumerate(["Phê duyệt mục tiêu", "Phê duyệt ngân sách", "Gỡ vướng vượt thẩm quyền PM"]):
        draw_rich(dd, (34, 206 + j * 38), ln, F_SM, INK, "lm")
    cards.append(im)
    xs = [240, 760, 1280]
    for i in range(3):
        a = fr(tl, "S05", i, 0.03)[0]
        pv = seg(t, a, a + 0.5)
        lift = 8 * seg(t, a + 0.05, a + 0.6)
        base.paste(cards[i], (xs[i], int(250 - lift)), cards[i])
        if pv < 1:
            overlay = Image.new("RGBA", cards[i].size, (246, 248, 251, 255))
            overlay.putalpha(int(255 * (1 - pv)))
            base.paste(overlay, (xs[i], int(250 - lift)), overlay)
        on = seg(t, a + 0.1, a + 0.5)
        if i < 2:
            nx = fr(tl, "S05", i + 1, 0.03)[0]
            on *= 1 - seg(t, nx - 0.05, nx + 0.3)
        if on > 0:
            d.rounded_rectangle([xs[i] - 4, int(250 - lift) - 4, xs[i] + 484,
                                 int(250 - lift) + 474], 20,
                                outline=AMBER[:3] + (int(255 * on),), width=4)
    a = fr(tl, "S05", 0, 0.55)[0]
    paste_sprite(base, pill("Ví dụ: đầu tư nền tảng TMĐT", AMBER_D, CREAM, 20, 38),
                 240 + 24, 740, seg(t, a, a + 0.3))
    _an(base, tl, "S05", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S05", t))
    return base


def events_S05(tl):
    return [(0.0, "whoosh", None, 0.8)] + \
        [(fr(tl, "S05", i, 0.03)[0], "pop", None, 0.9) for i in range(3)] + \
        [(fr(tl, "S05", 0, 0.55)[0], "click", None, 0.7)]


# ============================================================ S06 PM — KANBAN
TASKS6 = [("log-in", "Đăng nhập"), ("shopping-cart", "Giỏ hàng"),
          ("credit-card", "Thanh toán"), ("search", "Tìm kiếm"), ("bar-chart-3", "Thống kê")]


def _kanban_col(w, h, title, col):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, 64], 18, fill=col[:3] + (28,))
    d.text((24, 32), "", font=F_SM)
    draw_rich(d, (24, 32), title, F_BODY_M, col, "lm")
    return im


def draw_S06(t, tl):
    base, d = _base()
    _title(base, tl, "S06", t, "Project Manager — PM", "Lập kế hoạch · Điều phối · Theo dõi tiến độ")
    cols = [("Cần làm", BLUE), ("Đang làm", AMBER_D), ("Xong", GREEN)]
    xs = [110, 630, 1150]
    for i, (lb, col) in enumerate(cols):
        paste_sprite(base, _kanban_col(460, 520, lb, col), xs[i], 250, seg(t, 0.1 + i * 0.08, 0.4 + i * 0.08))
    for i, (icn, lb) in enumerate(TASKS6):
        a, _ = fr(tl, "S06", 0, 0.12 + i * 0.12)
        paste_sprite(base, pill(lb, NAVY, WHITE, 22, 56, icn, 26), 130, 335 + i * 64,
                     seg(t, a, a + 0.35))
    risk_a, risk_b = fr(tl, "S06", 0, 0.74, 1.0)
    pv = seg(t, risk_a, risk_a + 0.3)
    if pv > 0:
        risk = sp_chip("Dev nghỉ việc", RED, (254, 226, 226, 255), 22, "alert-triangle", h=52)
        mv_a, mv_b = fr(tl, "S06", 1, 0.12, 0.42)
        q = ease(lin(t, mv_a, mv_b))
        x = 130 + (650 - 130) * q
        y = 665 + (430 - 665) * q
        paste_sprite(base, risk, x, y, pv)
        if q >= 1:
            paste_sprite(base, pill("PM xử lý", AMBER_D, CREAM, 18, 32), x + 252, y + 10,
                         seg(t, mv_b + 0.1, mv_b + 0.4))
    a, _ = fr(tl, "S06", 1, 0.55)
    foot = sp_chip("Không cần code giỏi nhất — cần tổ chức & giao tiếp", AMBER_D,
                   CREAM, 24, "lightbulb", h=52)
    paste_sprite(base, foot, 110, 806, seg(t, a, a + 0.45))
    draw_marker(d, 122, 862, 110 + foot.size[0] - 30, 862, seg(t, a + 0.3, a + 0.7), AMBER, 6, 32)
    _an(base, tl, "S06", t, "present", look=-1)
    subtitle_band(d, subs_for(tl, "S06", t))
    return base


def events_S06(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(5):
        ev.append((fr(tl, "S06", 0, 0.12 + i * 0.12)[0], "pop", None, 0.8))
    ev += [(fr(tl, "S06", 0, 0.74)[0], "whoosh", None, 0.7),
           (fr(tl, "S06", 1, 0.12)[0], "marker", 0.3, 0.8),
           (fr(tl, "S06", 1, 0.55)[0], "chime", None, 0.7)]
    return ev


# ============================================================ S07 PO & BA
BACKLOG7 = ["Thanh toán QR", "Giỏ hàng", "Đăng nhập", "Tìm kiếm", "Đánh giá sản phẩm"]


def draw_S07(t, tl):
    base, d = _base()
    _title(base, tl, "S07", t, "Product Owner & Business Analyst", "Ưu tiên đúng — hiểu đúng yêu cầu")
    bl = card(620, 480)
    dd = ImageDraw.Draw(bl)
    draw_rich(dd, (28, 34), "Product Backlog", F_BODY_M, NAVY, "lm")
    for i, lb in enumerate(BACKLOG7):
        a, _ = fr(tl, "S07", 0, 0.12 + i * 0.14)
        pv = seg(t, a, a + 0.3)
        if pv > 0:
            yy = 70 + i * 76
            ddd = ImageDraw.Draw(bl)
            ddd.rounded_rectangle([22, yy, 598, yy + 62], 12,
                                  fill=(255, 251, 235, 255) if i == 0 else WHITE,
                                  outline=AMBER if i == 0 else BORDER, width=2)
            draw_rich(ddd, (40, yy + 31), f"{i + 1}. {lb}", F_SM_M, NAVY, "lm")
            if i == 0:
                paste_sprite(bl, pill("Ưu tiên", AMBER_D, CREAM, 18, 30), 500, yy + 16, pv)
    paste_sprite(base, bl, 150, 230, seg(t, 0.1, 0.5))
    # chat khách hàng + BA
    a = fr(tl, "S07", 1, 0.08)[0]
    cust = card(560, 84)
    dd = ImageDraw.Draw(cust)
    ic = sp_icon("user", NAVY, 34)
    cust.paste(ic, (22, 24), ic)
    draw_rich(dd, (70, 42), "Khách: Tôi muốn website bán hàng", F_SM_M, NAVY, "lm")
    paste_sprite(base, cust, 800, 262, seg(t, a, a + 0.35))
    qs = ["Có cần đăng nhập không?", "Thanh toán bằng gì?", "Hủy đơn xử lý sao?"]
    for i, qq in enumerate(qs):
        a, _ = fr(tl, "S07", 1, 0.30 + i * 0.20)
        bubble = card(540, 70)
        dd = ImageDraw.Draw(bubble)
        ic = sp_icon("message-circle", BLUE, 30)
        bubble.paste(ic, (20, 20), ic)
        draw_rich(dd, (64, 35), "BA hỏi: " + qq, F_SM_M, BLUE_D, "lm")
        paste_sprite(base, bubble, 1000 + i * 40, 370 + i * 84, seg(t, a, a + 0.35))
    docs = [("file-text", "SRS", "Đặc tả chức năng"), ("list-checks", "Use Case", "Kịch bản sử dụng"),
            ("book-open", "User Story", "Mô tả tính năng")]
    for i, (icn, lb, sub) in enumerate(docs):
        a, _ = fr(tl, "S07", 2, 0.25 + i * 0.22)
        dcm = card(300, 140)
        dd = ImageDraw.Draw(dcm)
        ic = sp_icon(icn, TEAL, 44)
        dcm.paste(ic, (24, 22), ic)
        draw_rich(dd, (84, 44), lb, F_BODY_M, NAVY, "lm")
        draw_rich(dd, (24, 100), sub, F_SM, MUT, "lm")
        paste_sprite(base, dcm, 800 + i * 330, 680, seg(t, a, a + 0.4))
    c1, _ = fr(tl, "S07", 0)
    c2, _ = fr(tl, "S07", 1)
    _an(base, tl, "S07", t, "point_right" if t < c2 else "point_left", look=1 if t < c2 else -1)
    subtitle_band(d, subs_for(tl, "S07", t))
    return base


def events_S07(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(5):
        ev.append((fr(tl, "S07", 0, 0.12 + i * 0.14)[0], "pop", None, 0.6))
    ev.append((fr(tl, "S07", 1, 0.08)[0], "pop", None, 0.8))
    for i in range(3):
        ev.append((fr(tl, "S07", 1, 0.30 + i * 0.20)[0], "pop", None, 0.75))
    for i in range(3):
        ev.append((fr(tl, "S07", 2, 0.25 + i * 0.22)[0], "marker", 0.3, 0.7))
    return ev


# ============================================================ S08 BA LEAD
def draw_S08(t, tl):
    base, d = _base()
    _title(base, tl, "S08", t, "Ba trưởng nhóm chuyên môn",
           "Tech Lead · UI/UX Lead · QA Lead")
    grp = [("code-xml", "Tech Lead", "Định hướng kỹ thuật · Review code", BLUE),
           ("palette", "UI/UX Lead", "Giao diện · Trải nghiệm người dùng", TEAL),
           ("clipboard-check", "QA Lead", "Chiến lược kiểm thử", AMBER_D)]
    xs = [150, 710, 1270]
    for i, (icn, lb, sub2, col) in enumerate(grp):
        a, _ = fr(tl, "S08", 0, 0.12 + i * 0.34)
        im = card(500, 300)
        dd = ImageDraw.Draw(im)
        ic = sp_icon(icn, col, 64)
        im.paste(ic, (218, 34), ic)
        draw_rich(dd, (250, 142), lb, F_H3, NAVY, "mm")
        draw_rich(dd, (250, 190), sub2, F_SM, MUT, "mm")
        paste_sprite(base, im, xs[i], 330, seg(t, a, a + 0.45))
        on = seg(t, a + 0.1, a + 0.4)
        if i < 2:
            nx = fr(tl, "S08", 0, 0.12 + (i + 1) * 0.34)[0]
            on *= 1 - seg(t, nx - 0.05, nx + 0.2)
        if on > 0:
            d.rounded_rectangle([xs[i] - 4, 326, xs[i] + 504, 634], 20,
                                outline=AMBER[:3] + (int(255 * on),), width=4)
    _an(base, tl, "S08", t, "present", look=0)
    subtitle_band(d, subs_for(tl, "S08", t))
    return base


def events_S08(tl):
    return [(0.0, "whoosh", None, 0.8)] + \
        [(fr(tl, "S08", 0, 0.12 + i * 0.34)[0], "pop", None, 0.9) for i in range(3)]


# ============================================================ S09 FIGMA → TRÌNH DUYỆT
def draw_S09(t, tl):
    base, d = _base()
    _title(base, tl, "S09", t, "Từ thiết kế đến giao diện chạy",
           "Figma → Trình duyệt — HTML · CSS · JavaScript · React")
    c2, _ = fr(tl, "S09", 1)
    # khung Figma wireframe
    fg = card(600, 460)
    fd = ImageDraw.Draw(fg)
    fd.rounded_rectangle([20, 18, 580, 60], 10, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(fd, (36, 39), "Figma — thiết kế", F_SM_M, MUT, "lm")
    fd.rounded_rectangle([20, 78, 580, 150], 10, fill=(226, 232, 240, 255))
    fd.rounded_rectangle([20, 168, 300, 330], 10, fill=(226, 232, 240, 255))
    fd.rounded_rectangle([320, 168, 580, 240], 10, fill=(241, 245, 249, 255), outline=BORDER, width=2)
    fd.rounded_rectangle([320, 256, 580, 328], 10, fill=(241, 245, 249, 255), outline=BORDER, width=2)
    fd.rounded_rectangle([320, 346, 580, 424], 10, fill=(255, 255, 255, 255), outline=AMBER, width=3)
    draw_rich(fd, (450, 385), "Nút đăng nhập", F_SM, AMBER_D, "mm")
    pleft = seg(t, 0.15, 0.6) * (1 - 0.60 * seg(t, c2 + 0.10, c2 + 0.35))
    paste_sprite(base, fg, 150, 200, pleft)
    # khung trình duyệt
    br = card(880, 460)
    bd = ImageDraw.Draw(br)
    bd.rounded_rectangle([0, 0, 880, 56], 18, fill=ICE_2)
    for i, col in enumerate([(248, 113, 113, 255), (251, 191, 36, 255), (74, 222, 128, 255)]):
        bd.ellipse([18 + i * 26, 20, 34 + i * 26, 36], fill=col)
    bd.rounded_rectangle([104, 12, 856, 44], 16, fill=WHITE, outline=BORDER, width=2)
    draw_rich(bd, (124, 28), "shopdienthoai.vn", F_SM, MUT, "lm")
    bd.rounded_rectangle([20, 74, 860, 152], 12, fill=NAVY)
    draw_rich(bd, (44, 113), "Shop Điện Thoại", F_BODY_M, WHITE, "lm")
    bd.rounded_rectangle([20, 170, 470, 330], 12, fill=ICE)
    bd.rounded_rectangle([500, 170, 860, 236], 10, fill=WHITE, outline=BORDER, width=2)
    bd.rounded_rectangle([500, 252, 860, 318], 10, fill=WHITE, outline=BORDER, width=2)
    bd.rounded_rectangle([500, 340, 860, 420], 14, fill=BLUE)
    draw_rich(bd, (680, 380), "Đăng nhập", F_BODY_M, WHITE, "mm")
    paste_sprite(base, br, 830, 200, seg(t, c2 + 0.02, c2 + 0.4))
    a, _ = fr(tl, "S09", 1, 0.32)
    paste_sprite(base, sp_chip("Figma → Trình duyệt", BLUE_D, ICE, 24, "arrow-right", h=48),
                 830, 690, seg(t, a, a + 0.35))
    techs = [("code-xml", "HTML", BLUE), ("palette", "CSS", TEAL),
             ("braces", "JavaScript", AMBER_D), ("atom", "React", NAVY)]
    for i, (icn, lb, col) in enumerate(techs):
        a, _ = fr(tl, "S09", 1, 0.50 + i * 0.12)
        paste_sprite(base, sp_chip(lb, col, WHITE, 24, icn, h=50), 400 + i * 360, 790,
                     seg(t, a, a + 0.35), "mm")
    _an(base, tl, "S09", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S09", t))
    return base


def events_S09(tl):
    c2, _ = fr(tl, "S09", 1)
    ev = [(0.0, "whoosh", None, 0.8), (c2 + 0.02, "whoosh", None, 0.9),
          (fr(tl, "S09", 1, 0.32)[0], "marker", 0.4, 0.7)]
    for i in range(4):
        ev.append((fr(tl, "S09", 1, 0.50 + i * 0.12)[0], "pop", None, 0.8))
    return ev


# ============================================================ S10 LUỒNG ĐĂNG NHẬP
def _node10(ic, lb, col, w_=300, h_=190):
    im = card(w_, h_)
    d = ImageDraw.Draw(im)
    icon = sp_icon(ic, col, 72)
    im.paste(icon, ((w_ - 72) // 2, 26), icon)
    draw_rich(d, (w_ / 2, 140), lb, F_H3, NAVY, "mm")
    return im


def draw_S10(t, tl):
    base, d = _base()
    _title(base, tl, "S10", t, "Chuyện gì xảy ra khi nhấn Đăng nhập?",
           "Frontend ↔ Backend ↔ Database, kết nối qua API")
    s = tl["S10"]
    c1, du1 = s["starts"][0], s["durs"][0]
    c2, du2 = s["starts"][1], s["durs"][1]
    q = lambda a, b: lin(t, c2 + a * du2, c2 + b * du2)
    f = lambda a, b: seg(t, c1 + a * du1, c1 + b * du1)
    ny = 430
    fe, api, be, db = (250, ny), (705, ny + 60), (900, ny), (1350, ny)
    draw_conn(d, 550, ny + 95, 660, ny + 95, f(0.14, 0.26), BLUE, width=5)
    draw_conn(d, 790, ny + 95, 900, ny + 95, f(0.30, 0.42), BLUE, width=5)
    draw_conn(d, 1200, ny + 95, 1350, ny + 95, f(0.50, 0.62), TEAL, width=5)
    paste_sprite(base, _node10("monitor", "Frontend", BLUE), fe[0], fe[1], f(0.04, 0.14))
    paste_sprite(base, sp_chip("API", BLUE_D, ICE, 30, "link", h=64), api[0] + 45, api[1] + 30,
                 f(0.22, 0.34), "mm")
    paste_sprite(base, _node10("server", "Backend", NAVY), be[0], be[1], f(0.38, 0.50))
    paste_sprite(base, _node10("database", "Database", TEAL), db[0], db[1], f(0.58, 0.70))
    lc = card(280, 150)
    dd = ImageDraw.Draw(lc)
    dd.rounded_rectangle([24, 22, 256, 52], 8, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(dd, (36, 37), "email", F_SM, MUT, "lm")
    dd.rounded_rectangle([24, 62, 256, 92], 8, fill=ICE_2, outline=BORDER, width=2)
    draw_rich(dd, (36, 77), "••••••••", F_SM, MUT, "lm")
    clicked = q(0.02, 0.06)
    dd.rounded_rectangle([24, 104, 256, 136], 8, fill=BLUE_D if clicked > 0 else NAVY)
    draw_rich(dd, (140, 120), "Đăng nhập", F_SM_M, WHITE, "mm")
    paste_sprite(base, lc, 260, 210, f(0.08, 0.20))
    p1 = q(0.06, 0.34)
    if 0 < p1 < 1:
        pos = path_pos([(550, ny + 95), (705, ny + 95), (900, ny + 95)], ease(p1))
        paste_sprite(base, sp_chip("email + ••••••", AMBER_D, CREAM, 22, "lock", h=46),
                     pos[0], pos[1] - 40, 1.0, "mm")
    ring = q(0.34, 0.5)
    if ring > 0 and t < c2 + 0.70 * du2:
        d.rounded_rectangle([be[0] - 8, ny - 8, be[0] + 308, ny + 198], 22, outline=AMBER, width=5)
        paste_sprite(base, sp_chip("Kiểm tra · xác thực", AMBER_D, CREAM, 22, "shield-check", h=46),
                     be[0] + 120, ny + 230, seg(t, c2 + 0.36 * du2, c2 + 0.42 * du2), "mt")
    p2 = q(0.46, 0.66)
    if 0 < p2 < 1:
        qq = p2 * 2 if p2 < 0.5 else (1 - p2) * 2
        pos = path_pos([(1200, ny + 95), (1350, ny + 95)], ease(qq))
        d.ellipse([pos[0] - 11, pos[1] - 11, pos[0] + 11, pos[1] + 11], fill=TEAL)
        paste_sprite(base, sp_chip("Truy vấn", TEAL, WHITE, 22, "database", h=46),
                     1290, ny + 230, seg(t, c2 + 0.48 * du2, c2 + 0.54 * du2), "mt")
    p3 = q(0.70, 0.90)
    if 0 < p3 < 1:
        pos = path_pos([(900, ny + 95), (705, ny + 95), (550, ny + 95)], ease(p3))
        paste_sprite(base, sp_chip("kết quả", GREEN, WHITE, 22, "circle-check", h=46),
                     pos[0], pos[1] - 40, 1.0, "mm")
    paste_sprite(base, sp_chip("JSON", BLUE_D, ICE, 24, "code-xml", h=50),
                 705, ny - 60, seg(t, c2 + 0.80 * du2, c2 + 0.86 * du2), "mm")
    tt = seg(t, c2 + 0.90 * du2, c2 + 0.96 * du2)
    if tt > 0:
        paste_sprite(base, sp_chip("Đăng nhập thành công", GREEN, WHITE, 26, "circle-check", h=58),
                     390, 395, tt, "mm")
    paste_sprite(base, sp_chip("Gửi yêu cầu", BLUE, WHITE, 22, "send", h=46),
                 400, ny + 230, seg(t, c2 + 0.08 * du2, c2 + 0.14 * du2), "mt")
    lab = sp_chip("Công nghệ backend", NAVY, ICE_2, 18, None, h=38)
    paste_sprite(base, lab, 400, 780, seg(t, fr(tl, "S10", 2, 0.10)[0], fr(tl, "S10", 2, 0.18)[0]), "mm")
    tech = [("Node.js + Express", GREEN), ("PHP + Laravel", BLUE_D), ("Java + Spring Boot", AMBER_D)]
    for i, (lb, col) in enumerate(tech):
        a, _ = fr(tl, "S10", 2, 0.18 + i * 0.26)
        paste_sprite(base, sp_chip(lb, col, WHITE, 22, "code-xml", h=48),
                     720 + i * 330, 780, seg(t, a, a + 0.4), "mm")
    _an(base, tl, "S10", t, "point_left", look=-1)
    subtitle_band(d, subs_for(tl, "S10", t))
    return base


def events_S10(tl):
    s = tl["S10"]
    c1, du1 = s["starts"][0], s["durs"][0]
    c2, du2 = s["starts"][1], s["durs"][1]
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
    for i in range(3):
        ev.append((fr(tl, "S10", 2, 0.15 + i * 0.26)[0], "pop", None, 0.7))
    return ev


# ============================================================ S11 DB & QA
def draw_S11(t, tl):
    base, d = _base()
    _title(base, tl, "S11", t, "Database Engineer & QA", "Thiết kế dữ liệu — kiểm thử kỹ càng")
    fm = font("BeVietnamPro-Regular.ttf", 22)
    fc = (148, 163, 184, 255)
    tbls = [("users", "Users", 130, 220, "id · email · password"),
            ("package", "Products", 130, 480, "id · tên · giá"),
            ("receipt", "Orders", 470, 380, "id · user_id · total")]
    for i, (icn, lb, x, y, fl) in enumerate(tbls):
        a, _ = fr(tl, "S11", 0, 0.05 + i * 0.20)
        im = card(280, 160)
        dd = ImageDraw.Draw(im)
        dd.rounded_rectangle([0, 0, 280, 52], 16, fill=[TEAL, AMBER_D, BLUE][i])
        ic = sp_icon(icn, WHITE, 30)
        im.paste(ic, (18, 11), ic)
        draw_rich(dd, (58, 26), lb, F_BODY_M, WHITE, "lm")
        draw_rich(dd, (20, 82), fl, fm, MUT, "lm")
        draw_rich(dd, (20, 116), "khóa chính · ngoại", font("BeVietnamPro-Regular.ttf", 20), fc, "lm")
        paste_sprite(base, im, x, y, seg(t, a, a + 0.4))
    a1, _ = fr(tl, "S11", 0, 0.55)
    a2, _ = fr(tl, "S11", 0, 0.72)
    draw_conn(d, 410, 300, 470, 430, a1, AMBER, width=4, hand=True, seed=41)
    draw_conn(d, 410, 560, 470, 500, a2, AMBER, width=4, hand=True, seed=42)
    ck = card(760, 430)
    dd = ImageDraw.Draw(ck)
    draw_rich(dd, (28, 34), "Kiểm thử chức năng", F_BODY_M, NAVY, "lm")
    cases = [("circle-check", "Đăng nhập đúng → vào được", GREEN),
             ("circle-x", "Sai mật khẩu → báo lỗi", RED),
             ("alert-triangle", "Bỏ trống thông tin → chặn", AMBER_D)]
    for i, (icn, lb, col) in enumerate(cases):
        a, _ = fr(tl, "S11", 1, 0.12 + i * 0.24)
        yy = 90 + i * 104
        ckd = ImageDraw.Draw(ck)
        ckd.rounded_rectangle([22, yy, 738, yy + 86], 14, fill=ICE_2, outline=BORDER, width=2)
        ic = sp_icon(icn, col, 40)
        ck.paste(ic, (44, yy + 23), ic)
        draw_rich(ckd, (104, yy + 43), lb, F_SM_M, INK, "lm")
        paste_sprite(ck, pill("", col, WHITE, 18, 30), 700, yy + 28, seg(t, a, a + 0.3))
    paste_sprite(base, ck, 880, 220, seg(t, 0.1, 0.5))
    a, _ = fr(tl, "S11", 1, 0.82)
    bgc = card(700, 110)
    dd = ImageDraw.Draw(bgc)
    ic = sp_icon("bug", RED, 40)
    bgc.paste(ic, (24, 30), ic)
    draw_rich(dd, (80, 36), "Bug Report #A1", F_SM_M, RED, "lm")
    draw_rich(dd, (80, 70), "Sai mật khẩu không hiện thông báo lỗi", F_SM, MUT, "lm")
    paste_sprite(base, bgc, 880, 690, seg(t, a, a + 0.4))
    _an(base, tl, "S11", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S11", t))
    return base


def events_S11(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(3):
        ev.append((fr(tl, "S11", 0, 0.05 + i * 0.20)[0], "pop", None, 0.8))
    ev += [(fr(tl, "S11", 0, 0.55)[0], "marker", 0.35, 0.7),
           (fr(tl, "S11", 0, 0.72)[0], "marker", 0.35, 0.7)]
    for i in range(3):
        ev.append((fr(tl, "S11", 1, 0.12 + i * 0.24)[0], "tick", None, 0.85))
    ev.append((fr(tl, "S11", 1, 0.82)[0], "pop", None, 0.9))
    return ev


# ============================================================ S12 DEVOPS / SEC / WRITER
def draw_S12(t, tl):
    base, d = _base()
    _title(base, tl, "S12", t, "DevOps · Security · Technical Writer",
           "Đưa lên máy chủ an toàn — viết tài liệu đầy đủ")
    steps = [("code-xml", "Code", BLUE), ("hammer", "Build", TEAL),
             ("flask-conical", "Test", AMBER_D), ("rocket", "Deploy", NAVY)]
    for i, (icn, lb, col) in enumerate(steps):
        a, _ = fr(tl, "S12", 0, 0.06 + i * 0.16)
        paste_sprite(base, sp_chip(lb, col, WHITE, 26, icn, h=58), 240 + i * 350, 300,
                     seg(t, a, a + 0.35), "mm")
        if i < 3:
            a2, _ = fr(tl, "S12", 0, 0.12 + i * 0.16)
            draw_conn(d, 330 + i * 350, 300, 490 + i * 350, 300, seg(t, a2, a2 + 0.25), BLUE, width=5)
    srv = card(220, 170)
    sd = ImageDraw.Draw(srv)
    ic = sp_icon("server", NAVY, 56)
    srv.paste(ic, (82, 24), ic)
    draw_rich(sd, (110, 124), "Máy chủ", F_SM_M, NAVY, "mm")
    paste_sprite(base, srv, 1590, 240, seg(t, fr(tl, "S12", 0, 0.70)[0], fr(tl, "S12", 0, 0.70)[0] + 0.4))
    a, _ = fr(tl, "S12", 0, 0.74)
    draw_conn(d, 1390, 300, 1582, 300, seg(t, a, a + 0.16), NAVY, width=5)
    a, _ = fr(tl, "S12", 0, 0.80)
    paste_sprite(base, sp_chip("HTTPS", GREEN, WHITE, 24, "lock", h=46), 1645, 450,
                 seg(t, a, a + 0.35), "mt")
    s = card(640, 230)
    dd = ImageDraw.Draw(s)
    ic = sp_icon("shield-check", RED, 48)
    s.paste(ic, (26, 24), ic)
    draw_rich(dd, (90, 46), "Security Engineer", F_BODY_M, NAVY, "lm")
    draw_rich(dd, (26, 96), "Rà soát lỗ hổng bảo mật", F_SM, MUT, "lm")
    paste_sprite(s, sp_chip("SQL Injection", RED, (254, 226, 226, 255), 20, "bug", h=40), 26, 140, 1.0)
    paste_sprite(s, sp_chip("XSS", RED, (254, 226, 226, 255), 20, "bug", h=40), 360, 140, 1.0)
    a, _ = fr(tl, "S12", 1, 0.25)
    paste_sprite(base, s, 200, 600, seg(t, a, a + 0.45))
    w = card(640, 230)
    dd = ImageDraw.Draw(w)
    ic = sp_icon("file-text", TEAL, 48)
    w.paste(ic, (26, 24), ic)
    draw_rich(dd, (90, 46), "Technical Writer", F_BODY_M, NAVY, "lm")
    draw_rich(dd, (26, 96), "Tài liệu kỹ thuật", F_SM, MUT, "lm")
    draw_rich(dd, (26, 140), "Hướng dẫn sử dụng", F_SM, MUT, "lm")
    a, _ = fr(tl, "S12", 1, 0.50)
    paste_sprite(base, w, 880, 600, seg(t, a, a + 0.45))
    _an(base, tl, "S12", t, "present", look=0)
    subtitle_band(d, subs_for(tl, "S12", t))
    return base


def events_S12(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(4):
        ev.append((fr(tl, "S12", 0, 0.06 + i * 0.16)[0], "pop", None, 0.8))
    for i in range(3):
        ev.append((fr(tl, "S12", 0, 0.12 + i * 0.16)[0], "marker", 0.25, 0.75))
    ev += [(fr(tl, "S12", 0, 0.74)[0], "whoosh", 0.25, 0.7),
           (fr(tl, "S12", 0, 0.80)[0], "click", None, 0.8),
           (fr(tl, "S12", 1, 0.25)[0], "pop", None, 0.85),
           (fr(tl, "S12", 1, 0.50)[0], "pop", None, 0.85)]
    return ev


# ============================================================ S13 SÁU GIAI ĐOẠN
PH = [("rocket", "Khởi động", "Project Charter", "CEO · Sponsor · PM", BLUE),
      ("search", "Phân tích yêu cầu", "Tài liệu SRS", "BA", TEAL),
      ("pen-tool", "Thiết kế hệ thống", "Bản thiết kế", "Designer · Tech Lead · DB", NAVY),
      ("code-xml", "Phát triển", "Mã nguồn", "Frontend · Backend", AMBER_D),
      ("flask-conical", "Kiểm thử", "Báo cáo kiểm thử", "QA · Tester", GREEN),
      ("rocket", "Triển khai & bàn giao", "Website chạy thật", "DevOps · PM", RED)]


def draw_S13(t, tl):
    base, d = _base()
    _title(base, tl, "S13", t, "Sáu giai đoạn của một dự án",
           "Mỗi giai đoạn có kết quả rõ ràng và người chủ trì")
    xs = [150 + i * 310 for i in range(6)]
    yline = 430
    a, _ = fr(tl, "S13", 0, 0.38)
    draw_conn(d, xs[0], yline, xs[-1], yline, seg(t, a, a + 1.2), NAVY, width=4)
    for i, (icn, lb, res, roles, col) in enumerate(PH):
        a1, _ = fr(tl, "S13", 1, 0.06 + i * 0.145)
        a0, _ = fr(tl, "S13", 0, 0.40 + i * 0.075)
        a = min(a1, a0)
        pv = seg(t, a, a + 0.3)
        if pv > 0:
            d.ellipse([xs[i] - 38, yline - 38, xs[i] + 38, yline + 38], fill=WHITE, outline=col, width=4)
            ic = sp_icon(icn, col, 36)
            base.paste(ic, (xs[i] - 18, yline - 18), ic)
            name = wrap(lb, F_SM_M, 250)
            for j, ln in enumerate(name):
                draw_rich(d, (xs[i], yline + 58 + j * 34), ln, F_SM_M, NAVY, "mm")
            paste_sprite(base, pill(res, col, WHITE, 18, 34), xs[i], yline - 86, pv, "mt")
            paste_sprite(base, pill(roles, MUT, ICE_2, 17, 30), xs[i], yline + 58 + len(name) * 34 + 6,
                         pv, "mt")
        pa, _ = fr(tl, "S13", 2, i / 6.0 + 0.01)
        on = seg(t, pa, pa + 0.12)
        if on > 0:
            draw_marker_circle(d, xs[i], yline, 46, 46, on, AMBER, 5, seed=40 + i)
    _an(base, tl, "S13", t, "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S13", t))
    return base


def events_S13(tl):
    ev = [(0.0, "whoosh", None, 0.8), (fr(tl, "S13", 1, 0.0)[0], "marker", 0.55, 0.85)]
    for i in range(6):
        ev.append((fr(tl, "S13", 1, 0.06 + i * 0.145)[0], "pop", None, 0.8))
    for i in range(6):
        ev.append((fr(tl, "S13", 2, i / 6.0 + 0.01)[0], "tick", None, 0.6))
    return ev


# ============================================================ S14 PHỐI HỢP + CÔNG CỤ
CH14 = [("user", "Khách hàng", 300, 280, AMBER_D), ("clipboard-list", "BA", 720, 280, TEAL),
        ("kanban", "PM", 1140, 280, BLUE), ("code-xml", "Tech Lead", 1410, 280, NAVY),
        ("monitor", "Designer + Dev", 1340, 450, BLUE), ("flask-conical", "QA", 920, 450, AMBER_D),
        ("rocket", "DevOps", 560, 450, GREEN)]


def draw_S14(t, tl):
    base, d = _base()
    _title(base, tl, "S14", t, "Yêu cầu đi qua cả quy trình",
           "Khách hàng → BA → PM → Tech Lead → Dev/Design → QA → DevOps")
    relay = [("user", "Khách hàng", AMBER_D), ("clipboard-list", "BA", TEAL),
             ("kanban", "PM", BLUE), ("code-xml", "Tech Lead", NAVY),
             ("monitor", "Designer + Dev", BLUE), ("flask-conical", "QA", AMBER_D),
             ("rocket", "DevOps", GREEN)]
    ims = [pill(lb, col, WHITE, 18, 50, icn, 24) for icn, lb, col in relay]
    gap = 56
    total = sum(im.size[0] for im in ims) + gap * 6
    x = max(120.0, (1920 - total) / 2)
    cy = 397
    xs = []
    for im in ims:
        xs.append((x, x + im.size[0]))
        x += im.size[0] + gap
    for j in range(6):
        a, _ = fr(tl, "S14", 0, 0.10 + j * 0.10)
        draw_conn(d, xs[j][1] + 4, cy, xs[j + 1][0] - 6, cy, seg(t, a, a + 0.20), AMBER, width=4)
    for i, im in enumerate(ims):
        a, _ = fr(tl, "S14", 0, 0.04 + i * 0.09)
        paste_sprite(base, im, xs[i][0], cy - 25, seg(t, a, a + 0.3))
    a, b = fr(tl, "S14", 0, 0.12, 0.92)
    pp = ease(lin(t, a, b))
    if 0 < pp < 1:
        px = xs[0][0] + (xs[-1][1] - xs[0][0]) * pp
        paste_sprite(base, sp_chip("Thanh toán", AMBER_D, CREAM, 20, "credit-card", h=40),
                     px, cy - 78, 1.0, "mm")
    a, _ = fr(tl, "S14", 1, 0.10)
    paste_sprite(base, sp_chip("Code ngay? Chưa đâu nhé!", AMBER_D, CREAM, 28,
                               "lightbulb", h=58), 960, 600, seg(t, a, a + 0.4), "mm")
    tools = [("kanban", "Jira", BLUE), ("pen-tool", "Figma", TEAL),
             ("git-branch", "Git · GitHub", NAVY), ("send", "Postman", AMBER_D),
             ("code-xml", "VS Code", BLUE_D), ("box", "Docker", GREEN)]
    for i, (icn, lb, col) in enumerate(tools):
        a, _ = fr(tl, "S14", 2, 0.08 + i * 0.13)
        pv = seg(t, a, a + 0.35)
        if pv > 0:
            tc = card(150, 122)
            dd = ImageDraw.Draw(tc)
            ic = sp_icon(icn, col, 40)
            tc.paste(ic, (55, 16), ic)
            draw_rich(dd, (75, 92), lb, F_LBL, NAVY, "mm")
            paste_sprite(base, tc, 260 + i * 260, 700, pv)
    c2, _ = fr(tl, "S14", 1)
    _an(base, tl, "S14", t, "think" if t >= c2 else "present", look=0)
    subtitle_band(d, subs_for(tl, "S14", t))
    return base


def events_S14(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(7):
        ev.append((fr(tl, "S14", 0, 0.04 + i * 0.09)[0], "pop", None, 0.7))
    for j in range(6):
        ev.append((fr(tl, "S14", 0, 0.10 + j * 0.10)[0], "whoosh", 0.25, 0.6))
    ev.append((fr(tl, "S14", 1, 0.10)[0], "chime", None, 0.8))
    for i in range(6):
        ev.append((fr(tl, "S14", 2, 0.08 + i * 0.13)[0], "pop", None, 0.8))
    return ev


# ============================================================ S15 NGƯỜI MỚI + BÀI TẬP
def draw_S15(t, tl):
    base, d = _base()
    _title(base, tl, "S15", t, "Người mới bắt đầu từ đâu?",
           "Chọn theo sở thích — không chỉ theo lương")
    dirs = [("monitor", "Frontend", "Thích giao diện", BLUE),
            ("server", "Backend", "Thích logic & dữ liệu", TEAL),
            ("users", "Business Analyst", "Thích phân tích & khách hàng", AMBER_D)]
    xs = [150, 710, 1270]
    for i, (icn, lb, sub, col) in enumerate(dirs):
        a, _ = fr(tl, "S15", 0, 0.08 + i * 0.24)
        im = card(500, 360)
        dd = ImageDraw.Draw(im)
        ic = sp_icon(icn, col, 64)
        im.paste(ic, (218, 36), ic)
        draw_rich(dd, (250, 160), lb, F_H3, NAVY, "mm")
        draw_rich(dd, (250, 212), sub, F_SM, MUT, "mm")
        paste_sprite(base, im, xs[i], 260, seg(t, a, a + 0.45))
        on = seg(t, fr(tl, "S15", 0, 0.50 + i * 0.16)[0], fr(tl, "S15", 0, 0.50 + i * 0.16)[0] + 0.3)
        if on > 0:
            d.rounded_rectangle([xs[i] - 4, 256, xs[i] + 504, 624], 20,
                                outline=col[:3] + (int(255 * on),), width=5)
    for i in range(8):
        a, _ = fr(tl, "S15", 1, 0.10 + i * 0.085)
        pv = seg(t, a, a + 0.3)
        if pv > 0:
            av = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
            dd = ImageDraw.Draw(av)
            dd.ellipse([10, 10, 86, 86], fill=[BLUE, TEAL, AMBER_D, NAVY][i % 4])
            dd.ellipse([32, 28, 64, 60], fill=(255, 224, 189, 255))
            dd.ellipse([36, 28, 60, 44], fill=NAVY)
            draw_rich(dd, (48, 74), str(i + 1), F_LBL, WHITE, "mm")
            paste_sprite(base, av, 560 + i * 100, 700, pv, "mm")
    a, _ = fr(tl, "S15", 1, 0.82)
    paste_sprite(base, sp_chip("Bài tập: website nhà hàng · 8 người · 8 tuần", AMBER_D,
                               CREAM, 26, "clipboard-list", h=56), 960, 800,
                 seg(t, a, a + 0.45), "mm")
    _an(base, tl, "S15", t, "present", look=0)
    subtitle_band(d, subs_for(tl, "S15", t))
    return base


def events_S15(tl):
    ev = [(0.0, "whoosh", None, 0.8)]
    for i in range(3):
        ev.append((fr(tl, "S15", 0, 0.08 + i * 0.24)[0], "pop", None, 0.85))
    for i in range(8):
        ev.append((fr(tl, "S15", 1, 0.10 + i * 0.085)[0], "pop", None, 0.55))
    ev.append((fr(tl, "S15", 1, 0.82)[0], "chime", None, 0.8))
    return ev


# ============================================================ S16 QUIZ
QZ = [("Ai điều phối tiến độ và công việc của dự án?",
       ["Frontend Developer", "Project Manager", "Tester"], 1),
      ("Công cụ nào dùng để thiết kế giao diện?",
       ["MySQL", "Docker", "Figma"], 2)]


def _quiz_sprite(qi, reveal=None):
    qt, opts, _ = QZ[qi]
    im = card(1360, 590, fill=WHITE, outline=BORDER, radius=24)
    d = ImageDraw.Draw(im)
    draw_rich(d, (60, 56), f"Câu {qi + 1}", F_LBL_B, AMBER_D, "lm")
    lines = wrap(qt, F_H3, 1200)
    for j, ln in enumerate(lines):
        draw_rich(d, (60, 110 + j * 46), ln, F_H3, NAVY, "lm")
    ys = []
    for i, op in enumerate(opts):
        yy = 240 + i * 96
        ys.append(yy)
        correct = reveal is not None and i == reveal
        dim = reveal is not None and i != reveal
        fill = (240, 253, 244, 255) if correct else (ICE_2 if not dim else (248, 250, 252, 255))
        outline = GREEN if correct else BORDER
        d.rounded_rectangle([60, yy, 1300, yy + 82], 16, fill=fill, outline=outline, width=3)
        d.ellipse([86, yy + 15, 138, yy + 67], fill=GREEN if correct else ICE)
        draw_rich(d, (112, yy + 41), "ABC"[i], F_LBL_B, WHITE if correct else NAVY, "mm")
        draw_rich(d, (168, yy + 41), op, F_BODY_M, GREEN if correct else (MUT if dim else NAVY), "lm")
        if correct:
            ic = sp_icon("circle-check", GREEN, 36)
            im.paste(ic, (1236, yy + 23), ic)
    return im, ys


def draw_S16(t, tl):
    base, d = _base()
    s = tl["S16"]
    c1, c3, c4 = s["starts"][0], s["starts"][2], s["starts"][3]
    out1 = seg(t, c3, c3 + 0.12 * s["durs"][2])
    in2 = seg(t, c3 + 0.15 * s["durs"][2], c3 + 0.32 * s["durs"][2])
    q1, ys1 = _quiz_sprite(0)
    p1 = seg(t, c1 + 0.05, c1 + 0.5) * (1 - 0.92 * out1)
    paste_sprite(base, q1, 280 - 90 * out1, 210, p1)
    paste_sprite(base, sp_chip("Thẻ câu hỏi", NAVY, ICE, 20, "circle-help", h=40), 280, 150,
                 seg(t, c1 + 0.1, c1 + 0.4))
    rev1 = None
    a, _ = fr(tl, "S16", 1, 0.03)
    if t >= a:
        rev1 = 1
        q1r, ys1 = _quiz_sprite(0, rev1)
        paste_sprite(base, q1r, 280 - 90 * out1, 210, p1)
        for i, yy in enumerate(ys1):
            if i == 1:
                draw_marker_circle(d, 560, 210 + yy + 41, 236, 44, seg(t, a, a + 0.35), AMBER, 5, 61)
    q2, ys2 = _quiz_sprite(1)
    p2 = in2
    paste_sprite(base, q2, 280 + 90 * (1 - in2), 210, p2)
    a4, _ = fr(tl, "S16", 3, 0.03)
    rev2 = None
    if t >= a4:
        rev2 = 2
        q2r, ys2 = _quiz_sprite(1, 2)
        paste_sprite(base, q2r, 280 + 90 * (1 - in2), 210, p2)
        for i, yy in enumerate(ys2):
            if i == 2:
                draw_marker_circle(d, 560, 210 + yy + 41, 236, 44, seg(t, a4, a4 + 0.35), AMBER, 5, 62)
    _an(base, tl, "S16", t, "think" if t < a else "point_right", look=1)
    subtitle_band(d, subs_for(tl, "S16", t))
    return base


def events_S16(tl):
    return [(0.0, "whoosh", None, 0.8),
            (fr(tl, "S16", 0, 0.55)[0], "pop", None, 0.8),
            (fr(tl, "S16", 1, 0.03)[0], "success", None, 0.9),
            (fr(tl, "S16", 2, 0.0)[0], "whoosh", None, 0.9),
            (fr(tl, "S16", 2, 0.50)[0], "pop", None, 0.8),
            (fr(tl, "S16", 3, 0.03)[0], "success", None, 0.9)]


# ============================================================ S17 OUTRO
def draw_S17(t, tl):
    base, d = _base()
    s = tl["S17"]
    sums = ["Một sản phẩm web là công sức của cả đội ngũ",
            "Mỗi vị trí gắn với quy trình sáu giai đoạn",
            "Bắt đầu từ vị trí hợp với sở thích của bạn"]
    for i, lb in enumerate(sums):
        a, _ = fr(tl, "S17", 0, 0.16 + i * 0.24)
        fade = 1 - seg(t, s["starts"][2] + 0.05, s["starts"][2] + 0.3)
        paste_sprite(base, sp_chip(lb, [BLUE, TEAL, AMBER_D][i], WHITE, 27,
                                   ["users", "workflow", "compass"][i], h=62),
                     200, 260 + i * 96, seg(t, a, a + 0.4) * fade)
    a, _ = fr(tl, "S17", 1, 0.10)
    p = seg(t, a, a + 0.5)
    if p > 0:
        msg = "Lập trình = Giải quyết vấn đề + Phối hợp con người"
        im = Image.new("RGBA", (1500, 120), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        draw_rich(dd, (750, 60), msg, F_H2, NAVY, "mm")
        fade = 1 - seg(t, s["starts"][2] + 0.05, s["starts"][2] + 0.3)
        paste_sprite(base, im, 960, 640, p * fade, "mm")
    a, _ = fr(tl, "S17", 2, 0.18)
    pv = seg(t, a, a + 0.5)
    if pv > 0:
        draw_tracked(d, (W / 2 - 240, 470), "AN TECH ACADEMY", F_H2, NAVY[:3] + (int(255 * pv),), 4)
        draw_marker(d, W / 2 - 150, 540, W / 2 + 150, 540, seg(t, a + 0.25, a + 0.6), AMBER, 7, 71)
        paste_sprite(base, sp_chip("Học công nghệ cùng An", MUT, WHITE, 26),
                     W / 2, 570, seg(t, a + 0.30, a + 0.6), "mt")
    _an(base, tl, "S17", t, "present" if t < s["starts"][2] else "wave", look=0)
    subtitle_band(d, subs_for(tl, "S17", t))
    return base


def events_S17(tl):
    return [(0.0, "whoosh", None, 0.8)] + \
        [(fr(tl, "S17", 0, 0.16 + i * 0.24)[0], "pop", None, 0.85) for i in range(3)] + \
        [(fr(tl, "S17", 1, 0.10)[0], "chime", None, 0.7),
         (fr(tl, "S17", 2, 0.18)[0], "chime", None, 0.85),
         (fr(tl, "S17", 2, 0.45)[0], "marker", 0.35, 0.8)]


DRAW = {"S01": draw_S01, "S02": draw_S02, "S03": draw_S03, "S04": draw_S04,
        "S05": draw_S05, "S06": draw_S06, "S07": draw_S07, "S08": draw_S08,
        "S09": draw_S09, "S10": draw_S10, "S11": draw_S11, "S12": draw_S12,
        "S13": draw_S13, "S14": draw_S14, "S15": draw_S15, "S16": draw_S16,
        "S17": draw_S17}
EVENTS = {"S01": events_S01, "S02": events_S02, "S03": events_S03, "S04": events_S04,
          "S05": events_S05, "S06": events_S06, "S07": events_S07, "S08": events_S08,
          "S09": events_S09, "S10": events_S10, "S11": events_S11, "S12": events_S12,
          "S13": events_S13, "S14": events_S14, "S15": events_S15, "S16": events_S16,
          "S17": events_S17}
