# -*- coding: utf-8 -*-
"""Nhân vật giáo viên "Thầy Minh" — vector 2D vẽ bằng PIL.
Character sheet 04_ArtDirection §5: nam 30–34, tóc đen, sơ mi trắng, blazer navy,
cà vạt teal, cao 430 px, pose D/C/G, idle 2 px, chớp mắt 4,2 s.
"""
import math
from PIL import Image, ImageDraw

SKIN    = (240, 196, 160, 255)   # #F0C4A0
SKIN_SH = (217, 165, 121, 255)   # #D9A579
HAIR    = (27, 27, 31, 255)      # #1B1B1F
WHITE   = (255, 255, 255, 255)
NAVY    = (11, 42, 91, 255)      # #0B2A5B
LAPEL   = (27, 74, 138, 255)
SLEEVE  = (22, 62, 118, 255)
TEAL    = (15, 157, 143, 255)    # #0F9D8F
TROUSER = (34, 48, 74, 255)      # #22304A
SHOE    = (42, 33, 24, 255)      # #2A2118
OUTL    = (10, 26, 51, 150)
EYE     = (14, 27, 51, 255)

CW, CH = 400, 520
CX = 200
FEET = 472

def _ell(d, box, fill, w=2):
    d.ellipse(box, fill=fill, outline=OUTL, width=w)

def _poly(d, pts, fill, w=3):
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=OUTL, width=w, joint="curve")

def _arm(d, sh, el, hand, sleeve=NAVY, cuff=True):
    # một polyline có bo góc để khuỷu tay không bị gãy khúc
    d.line([sh, el, hand], fill=OUTL, width=34, joint="curve")
    d.line([sh, el, hand], fill=sleeve, width=28, joint="curve")
    if cuff:
        hx, hy = hand
        ux, uy = hx - el[0], hy - el[1]
        n = math.hypot(ux, uy) or 1.0
        ax, ay = hx - ux / n * 24, hy - uy / n * 24   # đầu cổ tay áo
        bx, by = hx - ux / n * 13, hy - uy / n * 13   # sát bàn tay
        d.line([ax, ay, bx, by], fill=WHITE, width=24)
    _ell(d, [hand[0] - 13, hand[1] - 13, hand[0] + 13, hand[1] + 13], SKIN, 2)

def _hand_open(d, x, y, ang=0.0, spread=0.5):
    r = 12
    d.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], fill=OUTL)
    d.ellipse([x - r, y - r, x + r, y + r], fill=SKIN)
    for k in (-1, 0, 1):
        a = ang + k * spread
        d.line([x + math.cos(a) * 8, y + math.sin(a) * 8,
                x + math.cos(a) * 24, y + math.sin(a) * 24],
               fill=OUTL, width=11)
        d.line([x + math.cos(a) * 8, y + math.sin(a) * 8,
                x + math.cos(a) * 24, y + math.sin(a) * 24],
               fill=SKIN, width=7)

def _head(t, mouth="smile", tilt=0.0, blink=None):
    im = Image.new("RGBA", (140, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # tai
    _ell(d, [33, 62, 45, 84], SKIN, 2)
    _ell(d, [95, 62, 107, 84], SKIN, 2)
    # tóc nền
    _ell(d, [35, 27, 105, 94], HAIR, 3)
    # mặt
    _ell(d, [37, 38, 103, 116], SKIN, 2)
    # mái tóc
    d.polygon([(37, 62), (37, 44), (50, 35), (70, 32), (92, 37), (103, 48), (103, 62),
               (96, 54), (88, 62), (80, 53), (70, 62), (58, 53), (50, 62), (44, 54)],
              fill=HAIR)
    # lông mày
    d.line([51, 68, 64, 67], fill=HAIR, width=3)
    d.line([76, 67, 89, 68], fill=HAIR, width=3)
    # mắt
    bl = blink if blink is not None else (((t + 0.7) % 4.2) < 0.12)
    if bl:
        d.line([53, 79, 63, 79], fill=EYE, width=3)
        d.line([77, 79, 87, 79], fill=EYE, width=3)
    else:
        d.ellipse([53, 73, 63, 84], fill=EYE)
        d.ellipse([77, 73, 87, 84], fill=EYE)
    # mũi
    d.line([70, 82, 67, 92], fill=SKIN_SH, width=3)
    # miệng
    if mouth == "open":
        d.ellipse([62, 98, 78, 110], fill=(122, 52, 44, 255), outline=OUTL, width=2)
    elif mouth == "smile":
        d.arc([60, 94, 80, 110], 20, 160, fill=(122, 52, 44, 255), width=3)
    else:
        d.line([63, 102, 77, 102], fill=(122, 52, 44, 255), width=3)
    if abs(tilt) > 0.01:
        im = im.rotate(tilt, resample=Image.BICUBIC, center=(70, 75))
    return im

def teacher_sprite(t, pose="D", mouth="smile"):
    """Trả về sprite Thầy Minh 400×520, chân ở y=472, tâm x=200."""
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dy = int(round(2 * math.sin(2 * math.pi * t / 4.0)))
    tilt = max(-2.0, min(2.0, 2.0 * math.sin(2 * math.pi * t / 6.0)))

    # bóng chân (tĩnh)
    sh = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([128, 462, 272, 480], fill=(11, 42, 91, 34))
    im.alpha_composite(sh)

    # chân
    _poly(d, [(170, 276), (199, 276), (197, 452), (173, 452)], TROUSER)
    _poly(d, [(201, 276), (230, 276), (227, 452), (203, 452)], TROUSER)
    d.line([200, 284, 200, 330], fill=OUTL, width=2)
    for x0 in (168, 202):
        d.rounded_rectangle([x0, 448, x0 + 34, FEET], 8, fill=SHOE, outline=OUTL, width=2)
        d.line([x0 + 4, 462, x0 + 30, 462], fill=(62, 50, 38, 255), width=2)

    # tay (vẽ trước áo; vai neo vào trong thân để đầu tay áo bị blazer che)
    # tay trái của nhân vật = bên phải khung hình
    if pose == "G":
        _arm(d, (224, 162 + dy), (272, 212 + dy), (292, 258 + dy))
        _hand_open(d, 292, 260 + dy, 0.62)
    elif pose == "V":
        # tay trái chống hông
        _arm(d, (224, 162 + dy), (266, 236 + dy), (244, 252 + dy), cuff=False)
    else:
        # các pose khác: tay trái thả lỏng, hơi chếch ra ngoài áo
        _arm(d, (224, 162 + dy), (258, 212 + dy), (266, 268 + dy))
    # tay phải của nhân vật = bên trái khung hình, đổi theo pose
    if pose == "C":
        _arm(d, (176, 162 + dy), (122, 180 + dy), (92, 152 + dy))
        d.line([92, 152 + dy, 64, 142 + dy], fill=OUTL, width=8)
        d.line([92, 152 + dy, 64, 142 + dy], fill=SKIN, width=5)
    elif pose == "G":
        _arm(d, (176, 162 + dy), (128, 212 + dy), (108, 258 + dy))
        _hand_open(d, 108, 260 + dy, 2.52)
    elif pose == "V":
        # tay phải cầm bút đưa về phía bảng
        _arm(d, (176, 162 + dy), (132, 238 + dy), (96, 300 + dy))
        d.line([96, 300 + dy, 78, 278 + dy], fill=(27, 27, 31, 255), width=5)
        d.line([96, 300 + dy, 78, 278 + dy], fill=(245, 196, 94, 255), width=2)
    elif pose == "wave" and t < 3.2:
        wob = 8 * math.sin(2 * math.pi * t * 1.4)
        ex, ey = 124 + wob * 0.5, 122 + dy
        hx, hy = 100 + wob, 86 + dy
        _arm(d, (176, 162 + dy), (ex, ey), (hx, hy))
        _hand_open(d, hx, hy, -1.45, 0.30)
    else:  # D
        _arm(d, (176, 162 + dy), (126, 198 + dy), (98, 234 + dy))
        _hand_open(d, 98, 236 + dy, 2.7)

    # thân trên (bob)
    # cổ
    d.rectangle([188, 112 + dy, 212, 146 + dy], fill=SKIN, outline=OUTL, width=2)
    d.ellipse([186, 108 + dy, 214, 128 + dy], fill=SKIN_SH)
    # sơ mi
    _poly(d, [(174, 142 + dy), (226, 142 + dy), (232, 282 + dy), (168, 282 + dy)], WHITE)
    # cổ áo sơ mi
    _poly(d, [(186, 140 + dy), (200, 152 + dy), (194, 166 + dy), (181, 146 + dy)], WHITE, 2)
    _poly(d, [(214, 140 + dy), (200, 152 + dy), (206, 166 + dy), (219, 146 + dy)], WHITE, 2)
    # blazer chừa V cổ
    _poly(d, [(158, 148 + dy), (182, 140 + dy), (200, 178 + dy), (218, 140 + dy),
              (242, 148 + dy), (248, 210 + dy), (240, 284 + dy), (160, 284 + dy),
              (152, 210 + dy)], NAVY)
    _poly(d, [(182, 140 + dy), (200, 178 + dy), (190, 182 + dy), (172, 148 + dy)], LAPEL, 2)
    _poly(d, [(218, 140 + dy), (200, 178 + dy), (210, 182 + dy), (228, 148 + dy)], LAPEL, 2)
    # túi áo ngực
    d.line([216, 206 + dy, 240, 203 + dy], fill=(6, 28, 62, 255), width=2)
    # cà vạt
    _poly(d, [(194, 149 + dy), (206, 149 + dy), (204, 159 + dy), (196, 159 + dy)], TEAL, 2)
    _poly(d, [(196, 159 + dy), (204, 159 + dy), (208, 198 + dy), (200, 216 + dy),
              (192, 198 + dy)], TEAL, 2)
    # cúc áo
    for yy in (242, 266):
        d.ellipse([197, yy + dy, 203, yy + 6 + dy], fill=(6, 28, 62, 255))

    # đầu
    hd = _head(t, mouth, tilt)
    im.alpha_composite(hd, (130, 8 + dy))
    return im

def draw_teacher(base, t, pose="D", mouth="smile", x_shift=0.0):
    """Vẽ Thầy Minh lên `base` (RGBA) ở vị trí mặc định (chân y=1010, tâm x≈1755)."""
    im = teacher_sprite(t, pose, mouth)
    base.alpha_composite(im, (int(1755 - CX + x_shift), 1010 - FEET))

def mouth_for(t, speaking):
    if not speaking:
        return "smile" if (t % 6.0) < 0.8 else "neutral"
    ph = (t * 1.9) % 3.0
    return "open" if ph < 1.0 else ("neutral" if ph < 2.0 else "smile")
