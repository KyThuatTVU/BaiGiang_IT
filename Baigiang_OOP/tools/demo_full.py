# -*- coding: utf-8 -*-
"""Sản xuất video bài giảng OOP với Java hoàn chỉnh (~5 phút, 61 cues).
Chuẩn AN TECH ACADEMY: Giọng clone VieNeu + An lip-sync + SFX + ảnh img/ + code Java.
Không nhạc nền, loudness -14 LUFS, TP <= -1 dBTP.
Dùng:
    python demo_full.py           (render toàn bộ video)
    python demo_full.py --stills  (chỉ xuất ảnh tĩnh duyệt các cảnh)
"""
import bisect, json, math, os, re, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = r"D:\Edit\Kit"
os.environ.setdefault("PROJECT_ROOT", PROJECT)
sys.path.insert(0, KIT + "/tools")

from core import W, H, FPS, FF, font, draw_marker, draw_marker_circle, paste_brand, brand_watermark
from demo20 import bg, shadow_card, blit, chip, caption, decode, dur, seg, lin
import sfx, character, tts_vieneu

SR = sfx.SR
OUT = PROJECT + "/mau/full"
AUD = OUT + "/audio"
FR = OUT + "/frames"
TAG = "oop_full"

TXT = (236, 241, 249)
MUT = (148, 163, 184)
CYAN = (34, 211, 238)
BLUE = (96, 165, 250)
EMER = (52, 211, 153)
AMBER = (245, 158, 11)
VIOLET = (139, 92, 246)
RED = (239, 68, 68)
DIM = (100, 116, 139)

def C(c, a=255):
    return c[:3] + (a,)

# Tải script JSON 61 cues
SCRIPT_PATH = PROJECT + "/tools/script.json"
with open(SCRIPT_PATH, encoding="utf-8") as f:
    SCRIPT_DATA = json.load(f)

SCENES = SCRIPT_DATA["scenes"]
CUES = [c for sc in SCENES for c in sc["cues"]]
CUE_MAP = {c["id"]: c for c in CUES}
CUE_IDS = [c["id"] for c in CUES]
SAY = {c["id"]: c["say"] for c in CUES}

TAGS = [
    "PHẦN 01 · MỞ ĐẦU & GIỚI THIỆU",
    "PHẦN 02 · KHÁI NIỆM CLASS & OBJECT",
    "PHẦN 03 · BỐN TÍNH CHẤT CƠ BẢN",
    "PHẦN 04 · TÍNH CHẤT 1: ĐÓNG GÓI",
    "PHẦN 05 · TÍNH CHẤT 2: KẾ THỪA",
    "PHẦN 06 · TÍNH CHẤT 3: ĐA HÌNH",
    "PHẦN 07 · TÍNH CHẤT 4: TRỪU TƯỢNG",
    "PHẦN 08 · ỨNG DỤNG THỰC TẾ",
    "PHẦN 09 · TỔNG KẾT & LỜI KẾT"
]

ACC_COLORS = [BLUE, BLUE, BLUE, EMER, BLUE, AMBER, VIOLET, BLUE, BLUE]

# Fonts
B16 = font("BeVietnamPro-Regular.ttf", 16)
B18 = font("BeVietnamPro-Regular.ttf", 18)
B20S = font("BeVietnamPro-SemiBold.ttf", 20)
B22S = font("BeVietnamPro-SemiBold.ttf", 22)
B24S = font("BeVietnamPro-SemiBold.ttf", 24)
B26S = font("BeVietnamPro-SemiBold.ttf", 26)
B28S = font("BeVietnamPro-SemiBold.ttf", 28)
B32S = font("BeVietnamPro-SemiBold.ttf", 32)
B36B = font("BeVietnamPro-Bold.ttf", 36)
B42B = font("BeVietnamPro-Bold.ttf", 42)
B52B = font("BeVietnamPro-Bold.ttf", 52)

M15 = font("JetBrainsMono-var.ttf", 15)
M17 = font("JetBrainsMono-var.ttf", 17)
M19 = font("JetBrainsMono-var.ttf", 19)

# Chrome & photo card
_CH = {}
def chrome(w, h, r=22, border=(255, 255, 255, 40), fill=(22, 33, 57, 240)):
    key = (w, h, r, tuple(border), tuple(fill))
    if key not in _CH:
        _CH[key] = shadow_card(w, h, r, border=border, fill=fill)
    im, pad = _CH[key]
    return im.copy(), pad

_PIC = {}
_AR = {}
IMG = PROJECT + "/img"

def pic_w(name, h):
    if name not in _AR:
        with Image.open(IMG + "/" + name + ".jpg") as im:
            _AR[name] = im.width / im.height
    return int(round(h * _AR[name]))

def photo(name, w, h, r=22, mode="contain"):
    key = (name, w, h, r, mode)
    if key in _PIC:
        return _PIC[key].copy()
    src = ImageOps.exif_transpose(Image.open(IMG + "/" + name + ".jpg")).convert("RGB")
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if mode == "cover":
        im.paste(ImageOps.fit(src, (w, h), Image.LANCZOS), (0, 0))
    else:
        bg_blur = ImageOps.fit(src, (w, h), Image.LANCZOS)
        bg_blur = bg_blur.filter(ImageFilter.GaussianBlur(14))
        bg_blur = Image.blend(bg_blur, Image.new("RGB", (w, h), (12, 20, 36)), 0.55)
        sc = min((w - 16) / src.width, (h - 16) / src.height)
        fg = src.resize((max(1, int(src.width * sc)), max(1, int(src.height * sc))), Image.LANCZOS)
        im.paste(bg_blur, (0, 0))
        im.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    im.putalpha(mask)
    _PIC[key] = im
    return im.copy()

def photo_card(base, name, cx, cy, w, h, p, acc=BLUE, mode="contain", r=20, rise=14):
    if p <= 0:
        return
    if not w:
        w = pic_w(name, h)
    fw, fh = w + 16, h + 16
    im, pad = chrome(fw, fh, r + 8, C(acc, 90), (18, 27, 46, 240))
    im.alpha_composite(photo(name, w, h, r, mode), (pad + 8, pad + 8))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad + 7, pad + 7, pad + fw - 7, pad + fh - 7], r,
                        outline=(255, 255, 255, 110), width=1)
    d.line([pad + 24, pad + 1, pad + fw - 24, pad + 1], fill=C(acc, 180), width=2)
    blit(base, im, cx, cy, p, rise)

# Header Bar
_HDR = None
def draw_header(base, tag="LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP)", acc=BLUE):
    global _HDR
    if _HDR is None:
        im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([80, 102, W - 80, 102], fill=(255, 255, 255, 25), width=1)
        paste_brand(im, 80, 32, size=52)
        d.text((144, 34), "AN TECH ACADEMY", font=B22S, fill=TXT)
        d.text((144, 62), "Nền tảng kiến thức công nghệ thực chiến", font=B16, fill=MUT)
        _HDR = im
    base.alpha_composite(_HDR, (0, 0))
    d = ImageDraw.Draw(base)
    tw = int(B18.getlength(tag))
    bx = W - 80 - tw - 32
    d.rounded_rectangle([bx, 42, W - 80, 80], 19, fill=(22, 33, 57, 220), outline=C(acc, 120), width=1)
    d.ellipse([bx + 14, 58, bx + 22, 66], fill=acc)
    d.text((bx + 30, 49), tag, font=B18, fill=TXT)

# Generic Code Card
def draw_code_card(base, cx, cy, w, h, p, title, code_lines, active_line=None):
    if p <= 0:
        return
    im, pad = chrome(w, h, 20, (255, 255, 255, 50), (16, 24, 40, 245))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w - 1, pad + 40], 20, fill=(24, 36, 60, 255))
    d.rectangle([pad, pad + 20, pad + w - 1, pad + 40], fill=(24, 36, 60, 255))
    d.ellipse([pad + 16, pad + 14, pad + 26, pad + 24], fill=(239, 68, 68))
    d.ellipse([pad + 34, pad + 14, pad + 44, pad + 24], fill=(245, 158, 11))
    d.ellipse([pad + 52, pad + 14, pad + 62, pad + 24], fill=(52, 211, 153))
    d.text((pad + 78, pad + 11), title, font=M15, fill=MUT)
    
    y0 = pad + 54
    line_h = 30
    for num, line_text, col in code_lines:
        ly = y0 + (num - 1) * line_h
        if active_line == num:
            d.rounded_rectangle([pad + 8, ly - 3, pad + w - 8, ly + 25], 6, fill=(52, 211, 153, 35), outline=(52, 211, 153, 160), width=1)
        d.text((pad + 16, ly), f"{num:2d}", font=M17, fill=(80, 95, 120))
        d.line([pad + 48, ly - 2, pad + 48, ly + 22], fill=(45, 55, 75), width=1)
        if line_text:
            d.text((pad + 62, ly), line_text, font=M17, fill=col or TXT)
            
    blit(base, im, cx, cy, p, 10)

# Caption auto-wrap helper
def caption_auto(base, text, p=1.0):
    if p <= 0 or not text:
        return
    words = text.split()
    lines, cur = [], ""
    f = font("BeVietnamPro-Medium.ttf", 25)
    for w in words:
        cand = (cur + " " + w).strip()
        if not cur or f.getlength(cand) <= 780:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    caption(base, lines[:2], p=min(1.0, p))

# SCENE FUNCTIONS (s01 to s09)
def s01(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 170), "BÀI GIẢNG CÔNG NGHỆ CHUYÊN ĐỀ", font=B20S, fill=CYAN)
    d.text((120, 205), "LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP)", font=B52B, fill=TXT)
    d.text((120, 280), "Tổ chức mã nguồn khoa học, dễ mở rộng và bảo trì với Java", font=B24S, fill=MUT)
    
    if t < tl["c03"]:
        photo_card(base, "1", 620, 660, 860, 460, lin(t, s0, s0 + 0.6), acc=BLUE, mode="contain")
    else:
        photo_card(base, "8", 500, 660, 680, 440, lin(t, tl["c03"], tl["c03"] + 0.5), acc=BLUE, mode="cover")
        # 3 chips
        chip(base, "Dễ quản lý", EMER, 980, 520, lin(t, tl["c03"] + 0.3, tl["c03"] + 0.6))
        chip(base, "Dễ mở rộng", CYAN, 980, 610, lin(t, tl["c03"] + 0.6, tl["c03"] + 0.9))
        chip(base, "Dễ bảo trì", AMBER, 980, 700, lin(t, tl["c03"] + 0.9, tl["c03"] + 1.2))
        
    if t >= tl["c04"]:
        p_mk = lin(t, tl["c04"] + 0.2, tl["c04"] + 0.8)
        if p_mk > 0:
            draw_marker(d, 120, 268, 760, 268, p=p_mk, color=C(CYAN, 220), width=5)

def s02(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "KHÁI NIỆM CỐT LÕI", font=B20S, fill=CYAN)
    d.text((120, 195), "LỚP (CLASS) VÀ ĐỐI TƯỢNG (OBJECT)", font=B42B, fill=TXT)
    
    if t < tl["c11"]:
        photo_card(base, "3", 520, 570, 780, 500, lin(t, s0, s0 + 0.5), acc=BLUE, mode="contain")
        chip(base, "Thuộc tính: Mã SV, Họ tên, Tuổi", BLUE, 1240, 480, lin(t, tl["c08"], tl["c08"] + 0.4))
        chip(base, "Hành động: Đăng ký môn, Xem điểm", EMER, 1240, 560, lin(t, tl["c09"], tl["c09"] + 0.4))
        chip(base, "Gom thành Đối tượng SinhVien", AMBER, 1240, 640, lin(t, tl["c10"], tl["c10"] + 0.4))
    elif t < tl["c15"]:
        photo_card(base, "11", 520, 570, 780, 500, lin(t, tl["c11"], tl["c11"] + 0.5), acc=CYAN, mode="contain")
        photo_card(base, "4", 1240, 570, 660, 480, lin(t, tl["c14"], tl["c14"] + 0.4), acc=BLUE, mode="contain")
    else:
        # Code SinhVien
        lines = [
            (1, "class SinhVien {", (248, 113, 113)),
            (2, "    String hoTen;", (236, 241, 249)),
            (3, "    int tuoi;", (236, 241, 249)),
            (4, "    void hienThiThongTin() {", (96, 165, 250)),
            (5, "        System.out.println(hoTen + \" - \" + tuoi);", (148, 163, 184)),
            (6, "    }", (96, 165, 250)),
            (7, "}", (248, 113, 113)),
            (8, "public class Main {", (248, 113, 113)),
            (9, "    public static void main(String[] args) {", (96, 165, 250)),
            (10, "        SinhVien sv = new SinhVien();", (52, 211, 153)),
            (11, "        sv.hoTen = \"Nguyen Van An\";", (245, 158, 11)),
            (12, "        sv.tuoi = 20;", (245, 158, 11)),
            (13, "        sv.hienThiThongTin();", (52, 211, 153)),
            (14, "    }", (96, 165, 250)),
            (15, "}", (248, 113, 113)),
        ]
        act = 10 if t < tl["c16"] else 13
        draw_code_card(base, 500, 570, 720, 550, lin(t, tl["c15"], tl["c15"] + 0.4), "SinhVien.java", lines, active_line=act)
        photo_card(base, "6", 1260, 570, 660, 480, lin(t, tl["c17"], tl["c17"] + 0.4), acc=BLUE, mode="contain")

def s03(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((960, 170), "BỐN TÍNH CHẤT NỀN TẢNG CỦA OOP", font=B42B, fill=TXT, anchor="mm")
    d.text((960, 220), "Bốn trụ cột quyết định tư duy lập trình hướng đối tượng", font=B22S, fill=MUT, anchor="mm")
    photo_card(base, "5", 520, 570, 780, 500, lin(t, s0, s0 + 0.5), acc=BLUE, mode="contain")
    
    pillars = [
        ("1. Đóng gói (Encapsulation)", "Bảo vệ dữ liệu, chống truy cập tùy tiện", EMER, 350),
        ("2. Kế thừa (Inheritance)", "Tái sử dụng mã nguồn, chia sẻ thuộc tính", BLUE, 450),
        ("3. Đa hình (Polymorphism)", "Một phương thức, nhiều hành vi khác nhau", AMBER, 550),
        ("4. Trừu tượng (Abstraction)", "Ẩn chi tiết triển khai, lộ giao diện chung", VIOLET, 650),
    ]
    for i, (title, sub, col, y) in enumerate(pillars):
        p_row = lin(t, s0 + 0.3 + i * 0.4, s0 + 0.7 + i * 0.4)
        if p_row > 0:
            d.rounded_rectangle([1000, y - 10, 1650, y + 60], 12, fill=(22, 33, 57, 230), outline=C(col, 150), width=1)
            d.text((1030, y + 5), title, font=B22S, fill=col)
            d.text((1030, y + 33), sub, font=B16, fill=MUT)

def s04(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "TÍNH CHẤT 1 · ENCAPSULATION", font=B20S, fill=EMER)
    d.text((120, 195), "TÍNH ĐÓNG GÓI — BẢO VỆ DỮ LIỆU", font=B42B, fill=TXT)
    photo_card(base, "12", 480, 540, 740, 480, lin(t, s0, s0 + 0.5), acc=EMER, mode="contain")
    
    lines = [
        (1, "public class TaiKhoan {", (248, 113, 113)),
        (2, "    private double soDu;  // Ẩn dữ liệu", (52, 211, 153)),
        (3, "", None),
        (4, "    // Kiểm tra hợp lệ khi nạp tiền", (148, 163, 184)),
        (5, "    public void napTien(double tien) {", (96, 165, 250)),
        (6, "        if (tien > 0) soDu += tien;", (245, 158, 11)),
        (7, "    }", (96, 165, 250)),
        (8, "", None),
        (9, "    // Getter đọc số dư", (148, 163, 184)),
        (10, "    public double getSoDu() {", (96, 165, 250)),
        (11, "        return soDu;", (236, 241, 249)),
        (12, "    }", (96, 165, 250)),
        (13, "}", (248, 113, 113)),
    ]
    act = 2 if t < tl["c25"] else 6
    draw_code_card(base, 1260, 530, 720, 490, lin(t, tl["c24"], tl["c24"] + 0.4), "TaiKhoan.java", lines, active_line=act)
    
    if t >= tl["c27"]:
        chip(base, "An toàn dữ liệu", EMER, 260, 850, lin(t, tl["c27"] + 0.2, tl["c27"] + 0.5))
        chip(base, "Hạn chế sai sót", CYAN, 520, 850, lin(t, tl["c27"] + 0.5, tl["c27"] + 0.8))
        chip(base, "Kiểm soát truy cập", AMBER, 780, 850, lin(t, tl["c27"] + 0.8, tl["c27"] + 1.1))

def s05(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "TÍNH CHẤT 2 · INHERITANCE", font=B20S, fill=BLUE)
    d.text((120, 195), "TÍNH KẾ THỪA — TÁI SỬ DỤNG MÃ NGUỒN", font=B42B, fill=TXT)
    photo_card(base, "13", 480, 540, 740, 480, lin(t, s0, s0 + 0.5), acc=BLUE, mode="contain")
    
    lines = [
        (1, "class NhanVien {", (248, 113, 113)),
        (2, "    String hoTen; // Lớp cha chia sẻ thuộc tính", (148, 163, 184)),
        (3, "    void lamViec() {", (96, 165, 250)),
        (4, "        System.out.println(\"Dang lam viec\");", (236, 241, 249)),
        (5, "    }", (96, 165, 250)),
        (6, "}", (248, 113, 113)),
        (7, "// NhanVienIT kế thừa từ NhanVien", (148, 163, 184)),
        (8, "class NhanVienIT extends NhanVien {", (52, 211, 153)),
        (9, "    void lapTrinh() {", (96, 165, 250)),
        (10, "        System.out.println(\"Dang lap trinh Java\");", (245, 158, 11)),
        (11, "    }", (96, 165, 250)),
        (12, "}", (248, 113, 113)),
    ]
    act = 8 if t < tl["c33"] else 2
    draw_code_card(base, 1260, 530, 720, 490, lin(t, tl["c31"], tl["c31"] + 0.4), "NhanVienIT.java", lines, active_line=act)
    
    if t >= tl["c34"]:
        chip(base, "Tái sử dụng mã nguồn", BLUE, 260, 850, lin(t, tl["c34"] + 0.2, tl["c34"] + 0.5))
        chip(base, "Giảm trùng lặp", CYAN, 520, 850, lin(t, tl["c34"] + 0.5, tl["c34"] + 0.8))
        chip(base, "Dễ mở rộng", EMER, 780, 850, lin(t, tl["c34"] + 0.8, tl["c34"] + 1.1))

def s06(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "TÍNH CHẤT 3 · POLYMORPHISM", font=B20S, fill=AMBER)
    d.text((120, 195), "TÍNH ĐA HÌNH — MỘT PHƯƠNG THỨC, NHIỀU HÀNH VI", font=B42B, fill=TXT)
    photo_card(base, "14", 480, 540, 740, 480, lin(t, s0, s0 + 0.5), acc=AMBER, mode="contain")
    
    lines = [
        (1, "class NhanVien { void tinhLuong() {...} }", (148, 163, 184)),
        (2, "class NhanVienFullTime extends NhanVien {", (248, 113, 113)),
        (3, "    @Override", (245, 158, 11)),
        (4, "    void tinhLuong() {", (96, 165, 250)),
        (5, "        System.out.println(\"Luong co dinh thang\");", (52, 211, 153)),
        (6, "    }", (96, 165, 250)),
        (7, "}", (248, 113, 113)),
        (8, "class NhanVienPartTime extends NhanVien {", (248, 113, 113)),
        (9, "    @Override", (245, 158, 11)),
        (10, "    void tinhLuong() {", (96, 165, 250)),
        (11, "        System.out.println(\"Luong tinh theo gio\");", (34, 211, 238)),
        (12, "    }", (96, 165, 250)),
        (13, "}", (248, 113, 113)),
    ]
    act = 3 if t < tl["c39"] else 9
    draw_code_card(base, 1260, 530, 720, 490, lin(t, tl["c38"], tl["c38"] + 0.4), "Polymorphism.java", lines, active_line=act)
    
    if t >= tl["c41"]:
        chip(base, "Linh hoạt mã nguồn", AMBER, 260, 850, lin(t, tl["c41"] + 0.2, tl["c41"] + 0.5))
        chip(base, "Dễ mở rộng", CYAN, 520, 850, lin(t, tl["c41"] + 0.5, tl["c41"] + 0.8))
        chip(base, "Chung cách gọi hàm", EMER, 780, 850, lin(t, tl["c41"] + 0.8, tl["c41"] + 1.1))

def s07(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "TÍNH CHẤT 4 · ABSTRACTION", font=B20S, fill=VIOLET)
    d.text((120, 195), "TÍNH TRỪU TƯỢNG — ẨN CHI TIẾT TRIỂN KHAI", font=B42B, fill=TXT)
    photo_card(base, "15", 480, 540, 740, 480, lin(t, s0, s0 + 0.5), acc=VIOLET, mode="contain")
    
    lines = [
        (1, "interface ThanhToan {", (248, 113, 113)),
        (2, "    void thanhToan(double soTien);", (139, 92, 246)),
        (3, "}", (248, 113, 113)),
        (4, "class ThanhToanMoMo implements ThanhToan {", (52, 211, 153)),
        (5, "    public void thanhToan(double soTien) {", (96, 165, 250)),
        (6, "        System.out.println(\"Thanh toan MoMo\");", (236, 241, 249)),
        (7, "    }", (96, 165, 250)),
        (8, "}", (52, 211, 153)),
        (9, "class ThanhToanThe implements ThanhToan {", (34, 211, 238)),
        (10, "    public void thanhToan(double soTien) {", (96, 165, 250)),
        (11, "        System.out.println(\"Thanh toan bang the\");", (236, 241, 249)),
        (12, "    }", (96, 165, 250)),
        (13, "}", (34, 211, 238)),
    ]
    act = 2 if t < tl["c46"] else 4
    draw_code_card(base, 1260, 530, 720, 490, lin(t, tl["c46"], tl["c46"] + 0.4), "ThanhToan.java", lines, active_line=act)
    
    if t >= tl["c47"]:
        chip(base, "Giảm phức tạp", VIOLET, 260, 850, lin(t, tl["c47"] + 0.2, tl["c47"] + 0.5))
        chip(base, "Tách rời triển khai", CYAN, 520, 850, lin(t, tl["c47"] + 0.5, tl["c47"] + 0.8))
        chip(base, "Dễ thay đổi", EMER, 780, 850, lin(t, tl["c47"] + 0.8, tl["c47"] + 1.1))

def s08(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    d.text((120, 160), "ỨNG DỤNG THỰC TẾ", font=B20S, fill=CYAN)
    d.text((120, 195), "OOP TRONG CÁC DỰ ÁN PHẦN MỀM THỰC CHIẾN", font=B42B, fill=TXT)
    
    if t < tl["c51"]:
        photo_card(base, "16", 520, 540, 780, 480, lin(t, s0, s0 + 0.4), acc=AMBER, mode="contain")
        chip(base, "Quản lý nhà hàng", AMBER, 1240, 460, 1.0)
        chip(base, "Lớp: MonAn, BanAn, HoaDon", BLUE, 1240, 540, 1.0)
        chip(base, "Lớp: NhanVien, KhachHang", EMER, 1240, 620, 1.0)
    elif t < tl["c52"]:
        photo_card(base, "17", 520, 540, 780, 480, lin(t, tl["c51"], tl["c51"] + 0.4), acc=CYAN, mode="contain")
        chip(base, "Website thương mại điện tử", CYAN, 1240, 460, 1.0)
        chip(base, "Lớp: SanPham, GioHang", BLUE, 1240, 540, 1.0)
        chip(base, "Lớp: DonHang, KhachHang", EMER, 1240, 620, 1.0)
    elif t < tl["c53"]:
        photo_card(base, "18", 520, 540, 780, 480, lin(t, tl["c52"], tl["c52"] + 0.4), acc=BLUE, mode="contain")
        chip(base, "Hệ thống quản lý bệnh viện", BLUE, 1240, 460, 1.0)
        chip(base, "Lớp: BenhNhan, BacSi", EMER, 1240, 540, 1.0)
        chip(base, "Lớp: LichKham, DonThuoc", AMBER, 1240, 620, 1.0)
    else:
        photo_card(base, "19", 520, 540, 780, 480, lin(t, tl["c53"], tl["c53"] + 0.4), acc=EMER, mode="contain")
        chip(base, "Ứng dụng ngân hàng tài chính", EMER, 1240, 460, 1.0)
        chip(base, "Lớp: TaiKhoan, GiaoDich", BLUE, 1240, 540, 1.0)
        if t >= tl["c55"]:
            chip(base, "Ngôn ngữ: C++, C#, Python, PHP, Java", CYAN, 1240, 620, lin(t, tl["c55"], tl["c55"] + 0.4))

def s09(base, t, tl, durs, s0, s1):
    d = ImageDraw.Draw(base)
    if t < tl["c61"]:
        d.text((120, 160), "TỔNG KẾT BÀI HỌC", font=B20S, fill=CYAN)
        d.text((120, 195), "GHI NHỚ 4 TÍNH CHẤT & TƯ DUY THIẾT KẾ OOP", font=B42B, fill=TXT)
        photo_card(base, "2", 520, 560, 780, 480, lin(t, s0, s0 + 0.5), acc=BLUE, mode="contain")
        
        rows = [
            ("1. Đóng gói (Encapsulation)", "Bảo vệ an toàn dữ liệu bên trong", EMER, 420),
            ("2. Kế thừa (Inheritance)", "Tái sử dụng & mở rộng mã nguồn", BLUE, 510),
            ("3. Đa hình (Polymorphism)", "Một phương thức, nhiều cách thực hiện", AMBER, 600),
            ("4. Trừu tượng (Abstraction)", "Ẩn phức tạp, tập trung chức năng cốt lõi", VIOLET, 690),
        ]
        for title, sub, col, y in rows:
            d.rounded_rectangle([980, y - 8, 1650, y + 62], 10, fill=(22, 33, 57, 230), outline=C(col, 130))
            d.text((1010, y + 6), title, font=B20S, fill=col)
            d.text((1010, y + 34), sub, font=B16, fill=MUT)
    else:
        # Outro màn hình kết AN TECH ACADEMY
        paste_brand(base, 960, 380, size=180, alpha=lin(t, tl["c61"], tl["c61"] + 0.5))
        d.text((960, 520), "AN TECH ACADEMY", font=B42B, fill=TXT, anchor="mm")
        d.text((960, 580), "Cảm ơn các bạn đã theo dõi bài giảng!", font=B28S, fill=CYAN, anchor="mm")
        d.text((960, 640), "Hẹn gặp lại các bạn trong những bài học lập trình tiếp theo.", font=B22S, fill=MUT, anchor="mm")

SCENE_FN = [s01, s02, s03, s04, s05, s06, s07, s08, s09]
POSES = ["wave", "point_left", "present", "point_left", "point_left", "point_left", "point_left", "present", "wave"]

def make_draw(tl, total, starts, durs):
    n_sc = len(SCENES)
    
    def draw_frame(t):
        im = bg()
        
        # Xác định scene hiện tại
        si = bisect.bisect_right(starts, t) - 1
        si = max(0, min(n_sc - 1, si))
        s0 = starts[si]
        s1 = starts[si + 1] if si + 1 < n_sc else total
        
        # Vẽ Header bar
        draw_header(im, TAGS[si], ACC_COLORS[si])
        
        # Vẽ cảnh nội dung
        SCENE_FN[si](im, t, tl, durs, s0, s1)
        
        # Xác định cue hiện tại & kiểm tra An có nói không
        ci = bisect.bisect_right([tl[cid] for cid in CUE_IDS], t) - 1
        cur_cid = CUE_IDS[ci] if 0 <= ci < len(CUE_IDS) else None
        is_talking = False
        if cur_cid:
            stc = tl[cur_cid]
            if stc <= t < stc + durs[cur_cid]:
                is_talking = True
                
        # Nhân vật An
        pose = POSES[si]
        an_x = 1720 if si in (1, 3, 4, 5, 6) else 1620
        an_y = 850 if si in (1, 3, 4, 5, 6) else 820
        an_scale = 0.74 if si in (1, 3, 4, 5, 6) else 0.84
        character.paste(im, an_x, an_y, t=t, pose=pose, talking=is_talking, scale=an_scale)
        
        # Phụ đề chạy tự động
        if cur_cid:
            stc = tl[cur_cid]
            if stc <= t < stc + durs[cur_cid] + 0.3:
                caption_auto(im, SAY[cur_cid])
                
        return im

    return draw_frame

def build_sfx(tl, durs, total, starts):
    bus = np.zeros(int(total * SR) + SR)
    def put(snd, t, vol=1.0):
        if snd is None or t < 0:
            return
        idx = int(t * SR)
        arr = snd * vol
        end = min(len(bus), idx + len(arr))
        bus[idx:end] += arr[:end - idx]

    W0 = sfx.sfx("whoosh")
    PO = sfx.sfx("pop")
    TK = sfx.sfx("tick")
    CH = sfx.sfx("chime")
    TH = sfx.sfx("thud")
    SU = sfx.sfx("success")
    MK = sfx.sfx("marker", 0.5)

    # Chuyển cảnh whoosh + thud
    for st in starts:
        put(W0, st - 0.2, 0.22)
        put(TH, st + 0.1, 0.16)
        
    # S01 SFX
    put(PO, 0.4, 0.15)
    put(MK, tl["c04"] + 0.2, 0.20)
    put(CH, tl["c04"] + durs["c04"] * 0.8, 0.15)
    
    # Tick khi xuất hiện code / chip trong các cảnh
    for cid in ("c10", "c15", "c16", "c24", "c25", "c27", "c32", "c34", "c38", "c40", "c41", "c46", "c47", "c50", "c51", "c52", "c53", "c55", "c57", "c58"):
        if cid in tl:
            put(TK, tl[cid] + 0.4, 0.16)
            put(PO, tl[cid] + 0.8, 0.14)
            
    # Kết thúc
    put(SU, total - 4.5, 0.20)
    put(CH, total - 2.0, 0.22)

    pk = float(np.max(np.abs(bus)))
    print("SFX peak", round(pk, 3), flush=True)
    if pk > 0.26:
        bus *= 0.26 / pk
    elif 0 < pk < 0.18:
        bus *= 0.18 / pk
    return bus

def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    stills = "--stills" in sys.argv

    # Đo độ dài toàn bộ audio cues
    durs = {}
    for c in CUES:
        cid = c["id"]
        p = f"{AUD}/{cid}.wav"
        if not os.path.exists(p) or os.path.getsize(p) < 10000:
            print(f"Synthesizing missing cue {cid}...", flush=True)
            tts_vieneu.synth(c["say"], p)
        durs[cid] = len(decode(p)) / SR

    # Xây dựng timeline theo từng scene
    tl = {}
    starts = []
    t = 0.40
    for sc in SCENES:
        starts.append(t)
        for c in sc["cues"]:
            cid = c["id"]
            tl[cid] = t
            t += durs[cid] + float(c.get("pause", 0.4))
        t += float(sc.get("hold", 1.5))
        
    total = t + 2.5
    print(f"Tổng số cảnh: {len(SCENES)}, Tổng số cues: {len(CUES)}")
    print(f"Tổng thời lượng video: {total:.2f}s (~{int(total//60)} phút {int(total%60)} giây)", flush=True)

    draw = make_draw(tl, total, starts, durs)

    if stills:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        # Lấy mỗi scene 1 ảnh tĩnh đại diện
        picks = [st + 1.2 for st in starts] + [total - 1.0]
        for i, tt in enumerate(picks):
            draw(tt).convert("RGB").save(f"{sd}/scene_{i:02d}_{tt:.1f}.png")
            print(f"STILL Scene {i}: {tt:.1f}s", flush=True)
        return

    n = int(total * FPS)
    mix = np.zeros(int(total * SR) + SR)
    for c in CUES:
        cid = c["id"]
        x = decode(f"{AUD}/{cid}.wav")
        s0 = int(tl[cid] * SR)
        mix[s0:s0 + len(x)] += x
        
    bus = build_sfx(tl, durs, total, starts)
    m = min(len(mix), len(bus))
    mix[:m] += bus[:m]
    pk = np.max(np.abs(mix))
    print("PEAK Audio:", round(pk, 3), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + f"/voice_{TAG}.wav", mix)

    # Render Frames
    print(f"Bắt đầu render {n} frames ({total:.1f}s @ 30fps)...", flush=True)
    t_f0 = time.time()
    for k in range(n):
        fp = f"{FR}/f{k:05d}.jpg"
        if not os.path.exists(fp):
            draw(k / FPS).convert("RGB").save(fp, quality=92)
        if k % 300 == 0 or k == n - 1:
            fps_speed = (k + 1) / max(0.1, time.time() - t_f0)
            eta = (n - k) / max(0.1, fps_speed)
            print(f"Frame {k:5d}/{n} ({k/n*100:4.1f}%) | {fps_speed:.1f} fps | ETA: {eta:.0f}s", flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/video_{TAG}.mp4"
    print("Bắt đầu encode Video H.264 qua FFmpeg...", flush=True)
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%05d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")

    # Chuẩn hóa âm thanh -14 LUFS
    print("Bắt đầu chuẩn hóa âm thanh EBU R128 (-14 LUFS)...", flush=True)
    mixp = OUT + f"/voice_{TAG}.wav"
    comp = OUT + f"/voice_{TAG}_comp.wav"
    run([FF, "-y", "-i", mixp, "-af",
         "acompressor=threshold=0.125:ratio=3:attack=5:release=100", comp])
    mixp = comp
    mm = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", mixp, "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr, re.S)[-1]
    mm = json.loads(mm)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={mm['input_i']}:measured_TP={mm['input_tp']}:"
          f"measured_LRA={mm['input_lra']}:measured_thresh={mm['input_thresh']}:"
          f"offset={mm['target_offset']}:linear=true,volume=-0.2dB")
    run([FF, "-y", "-i", mixp, "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
         OUT + f"/audio_{TAG}.m4a"])
         
    # Mux final video
    final_mp4 = OUT + f"/{TAG}.mp4"
    print("Muxing Video và Audio...", flush=True)
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/audio_{TAG}.m4a", "-c:v", "copy", "-c:a", "copy",
             "-movflags", "+faststart", "-shortest", final_mp4])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
        
    print(f"DONE FULL VIDEO: {final_mp4} ({dur(final_mp4):.2f}s)", flush=True)

if __name__ == "__main__":
    main()
