# -*- coding: utf-8 -*-
"""Giáo viên An: vector phẳng 2D, một hệ tạo hình duy nhất, 6 tư thế + cử chỉ.
Vẽ bằng PIL ở 2x rồi hạ mẫu để khử răng cưa. Không đổi trang phục giữa các cảnh."""
import math
from PIL import Image, ImageDraw

NAVY = (27, 42, 74, 255)
SHIRT = (59, 130, 246, 255)
SKIN = (242, 201, 160, 255)
SKIN_D = (224, 178, 132, 255)
HAIR = (30, 41, 59, 255)
PANTS = (51, 65, 85, 255)
SHOE = (248, 250, 252, 255)
AMBER = (245, 158, 11, 255)
WHITE = (255, 255, 255, 255)
OUT = NAVY

CW, CH = 360, 560
S = 2  # supersample

def _cap(d, a, b, w, fill, outline=OUT, ow=3):
    d.line([a, b], fill=outline, width=w + ow * 2)
    for p in (a, b):
        r = (w + ow * 2) / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=outline)
    d.line([a, b], fill=fill, width=w)
    for p in (a, b):
        r = w / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill)

def _arm(d, sh, ang, bend, pointing=False, marker=False, open_hand=False):
    """ang: độ lệch khỏi phương thẳng đứng (dương = sang phải), bend: gập khuỷu."""
    a1 = math.radians(ang)
    L1, L2 = 62, 56
    elbow = (sh[0] + L1 * math.sin(a1), sh[1] + L1 * math.cos(a1))
    a2 = math.radians(ang + bend)
    hand = (elbow[0] + L2 * math.sin(a2), elbow[1] + L2 * math.cos(a2))
    _cap(d, sh, elbow, 24, SHIRT)
    _cap(d, elbow, hand, 18, SKIN)
    if pointing:
        tip = (hand[0] + 20 * math.sin(a2), hand[1] + 20 * math.cos(a2))
        _cap(d, hand, tip, 9, SKIN, ow=2)
    elif open_hand:
        for da in (-24, 0, 24):
            ar = math.radians(ang + bend + da)
            tip = (hand[0] + 15 * math.sin(ar), hand[1] + 15 * math.cos(ar))
            _cap(d, hand, tip, 7, SKIN, ow=2)
    else:
        r = 12
        d.ellipse([hand[0] - r - 2, hand[1] - r - 2, hand[0] + r + 2, hand[1] + r + 2], fill=OUT)
        d.ellipse([hand[0] - r, hand[1] - r, hand[0] + r, hand[1] + r], fill=SKIN)
    if marker:
        ar = math.radians(ang + bend)
        m1 = (hand[0] + 6 * math.sin(ar), hand[1] + 6 * math.cos(ar))
        m2 = (hand[0] + 38 * math.sin(ar), hand[1] + 38 * math.cos(ar))
        _cap(d, m1, m2, 10, AMBER, ow=2)
    return hand

POSES = {
    # (left_ang, left_bend, left_mode), (right_ang, right_bend, right_mode)
    "idle":        ((-12, -6, "fist"), (12, 6, "marker")),
    "present":     ((-58, -18, "open"), (58, 18, "open")),
    "point_left":  ((-92, -4, "point"), (14, 8, "fist")),
    "point_right": ((-14, -8, "fist"), (92, 4, "point")),
    "think":       ((-10, 79, "fist"), (157, 122, "fist")),
    "wave":        ((-12, -6, "fist"), (148, 22, "open")),
    "write":       ((-20, -10, "fist"), (66, 120, "marker")),
}

def draw(t=0.0, pose="idle", look=0, talking=False, scale=1.0):
    """Trả về ảnh RGBA nhân vật. look: -1 trái, 0 giữa, +1 phải. talking: mấp máy môi."""
    im = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def P(x, y):
        return (x * S, y * S)
    def cap(a, b, w, fill, outline=OUT, ow=3):
        _cap(d, P(*a), P(*b), w * S, fill, outline, ow * S)
    def ell(box, fill, outline=None, ow=3):
        x0, y0, x1, y1 = [v * S for v in box]
        if outline:
            d.ellipse([x0 - ow * S, y0 - ow * S, x1 + ow * S, y1 + ow * S], fill=outline)
        d.ellipse([x0, y0, x1, y1], fill=fill)
    def rr(box, r, fill, outline=None, ow=3):
        x0, y0, x1, y1 = [v * S for v in box]
        if outline:
            d.rounded_rectangle([x0 - ow * S, y0 - ow * S, x1 + ow * S, y1 + ow * S],
                                (r + ow) * S, fill=outline)
        d.rounded_rectangle([x0, y0, x1, y1], r * S, fill=fill)

    bob = 2.0 * math.sin(t * 2 * math.pi * 0.35)
    dy = bob
    # bóng dưới chân (rất nhẹ, phẳng)
    d.ellipse([P(110, 512 + 0)[0], P(0, 512)[1], P(250, 530)[0], P(0, 530)[1]],
              fill=(15, 23, 42, 26))
    # chân
    cap((158, 330 + dy), (150, 478 + dy), 30, PANTS)
    cap((202, 330 + dy), (210, 478 + dy), 30, PANTS)
    rr((128, 476 + dy, 178, 500 + dy), 10, SHOE)
    rr((190, 476 + dy, 240, 500 + dy), 10, SHOE)
    # thân áo sơ mi
    rr((122, 202 + dy, 238, 348 + dy), 26, SHIRT)
    # dây đeo thẻ teal
    d.line([P(168, 206 + dy), P(148, 252 + dy)], fill=(13, 148, 136, 255), width=5 * S)
    d.line([P(192, 206 + dy), P(180, 252 + dy)], fill=(13, 148, 136, 255), width=5 * S)
    # cổ áo trắng
    d.polygon([P(160, 204 + dy), P(180, 226 + dy), P(200, 204 + dy)], fill=WHITE)
    # thẻ tên AN
    rr((136, 246 + dy, 172, 268 + dy), 5, AMBER, ow=2)
    f = None
    from PIL import ImageFont
    try:
        f = ImageFont.truetype("D:/Edit/Baigiang_LoadBalancer_v2/assets/fonts/BeVietnamPro-Bold.ttf", 13 * S)
    except Exception:
        pass
    if f:
        d.text(P(154, 257 + dy), "AN", font=f, fill=NAVY, anchor="mm")
    # tay
    la, lb, lm = POSES[pose][0]
    ra, rb, rm = POSES[pose][1]
    _arm(d, P(132, 220 + dy), la, lb, pointing=(lm == "point"),
         marker=(lm == "marker"), open_hand=(lm == "open"))
    _arm(d, P(228, 220 + dy), ra, rb, pointing=(rm == "point"),
         marker=(rm == "marker"), open_hand=(rm == "open"))
    # cổ
    rr((168, 172 + dy, 192, 210 + dy), 8, SKIN, ow=2)
    # đầu
    ell((128, 78 + dy, 232, 182 + dy), SKIN)
    # tóc: khối trên + mái
    d.pieslice([P(126, 74 + dy)[0], P(126, 74 + dy)[1], P(234, 168 + dy)[0], P(234, 168 + dy)[1]],
               180, 360, fill=HAIR)
    rr((126, 96 + dy, 234, 106 + dy), 5, HAIR, ow=0)
    d.polygon([P(150, 112 + dy), P(166, 92 + dy), P(178, 112 + dy)], fill=HAIR)
    # tai
    ell((122, 124 + dy, 136, 148 + dy), SKIN, ow=2)
    ell((224, 124 + dy, 238, 148 + dy), SKIN, ow=2)
    # mắt (nhìn theo look, chớp định kỳ)
    blink = (t % 3.4) > 3.25
    ex = 5 * look
    for cx in (160, 200):
        if blink:
            d.line([P(cx - 7 + ex, 132 + dy), P(cx + 7 + ex, 132 + dy)], fill=NAVY, width=3 * S)
        else:
            ell((cx - 5 + ex, 126 + dy, cx + 5 + ex, 138 + dy), NAVY, ow=0)
    # lông mày
    d.line([P(150 + ex, 116 + dy), P(168 + ex, 113 + dy)], fill=HAIR, width=4 * S)
    d.line([P(192 + ex, 113 + dy), P(210 + ex, 116 + dy)], fill=HAIR, width=4 * S)
    # kính gọng navy
    d.rounded_rectangle([P(147 + ex, 120 + dy)[0], P(147 + ex, 120 + dy)[1],
                         P(176 + ex, 146 + dy)[0], P(176 + ex, 146 + dy)[1]],
                        6 * S, outline=NAVY, width=3 * S)
    d.rounded_rectangle([P(184 + ex, 120 + dy)[0], P(184 + ex, 120 + dy)[1],
                         P(213 + ex, 146 + dy)[0], P(213 + ex, 146 + dy)[1]],
                        6 * S, outline=NAVY, width=3 * S)
    d.line([P(176 + ex, 132 + dy), P(184 + ex, 132 + dy)], fill=NAVY, width=3 * S)
    d.line([P(147 + ex, 130 + dy), P(136 + ex, 128 + dy)], fill=NAVY, width=3 * S)
    d.line([P(213 + ex, 130 + dy), P(224 + ex, 128 + dy)], fill=NAVY, width=3 * S)
    # mũi nhẹ
    d.line([P(180 + ex, 138 + dy), P(177 + ex, 148 + dy)], fill=SKIN_D, width=3 * S)
    # miệng: cười hoặc mấp máy khi nói
    if talking and int(t * 5.5) % 2 == 0:
        ell((170 + ex, 152 + dy, 190 + ex, 166 + dy), (146, 84, 60, 255), ow=2)
    else:
        d.arc([P(166 + ex, 144 + dy)[0], P(166 + ex, 144 + dy)[1],
               P(194 + ex, 164 + dy)[0], P(194 + ex, 164 + dy)[1]], 15, 165, fill=NAVY, width=3 * S)
    # má hồng nhẹ
    ell((142, 146 + dy, 156, 156 + dy), (238, 178, 140, 160), ow=0)
    ell((204, 146 + dy, 218, 156 + dy), (238, 178, 140, 160), ow=0)

    im = im.resize((CW, CH), Image.LANCZOS)
    if scale != 1.0:
        im = im.resize((max(1, int(CW * scale)), max(1, int(CH * scale))), Image.LANCZOS)
    return im

def paste(base, x, y, t=0.0, pose="idle", look=0, talking=False, scale=1.0, anchor="bl"):
    im = draw(t, pose, look, talking, scale)
    w_, h_ = im.size
    if anchor == "bl":
        px, py = int(x), int(y - h_)
    elif anchor == "bm":
        px, py = int(x - w_ / 2), int(y - h_)
    else:
        px, py = int(x), int(y)
    base.paste(im, (px, py), im)
    return im.size