# -*- coding: utf-8 -*-
"""Video bài giảng Full (~6 phút, 10 cảnh, 62 cues, 16 ảnh)
Chủ đề: Xử lý trùng lặp tên file Avatar trong phần mềm
AN TECH ACADEMY — Tuân thủ MASTER DESIGN & VOICE STANDARD 2.3
"""
import os
import sys
import json
import time
import math
import re
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter

# Kit tools
PROJECT = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem"
KIT = r"D:\Edit\Kit"
sys.path.insert(0, KIT + "/tools")

import core
import demo20
from demo20 import (
    W, H, FPS, SR, TXT, MUT, CYAN, EMER, AMBER, VIOLET,
    font, shadow_card, blit, lin, caption
)
import sfx
import character

FF = r"C:\Users\ACER\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
AUD = PROJECT + "/mau/full/audio"
OUT = PROJECT + "/mau/full"
FR = OUT + "/frames"
IMG = PROJECT + "/img"
SCRIPT_FILE = PROJECT + "/tools/script.json"
TAG = "avatar_full"

os.makedirs(OUT, exist_ok=True)
os.makedirs(FR, exist_ok=True)

# Fonts
B52B = font("BeVietnamPro-Bold.ttf", 52)
B42B = font("BeVietnamPro-Bold.ttf", 40)
B36B = font("BeVietnamPro-Bold.ttf", 36)
B28B = font("BeVietnamPro-Bold.ttf", 28)
B24S = font("BeVietnamPro-SemiBold.ttf", 24)
B22S = font("BeVietnamPro-SemiBold.ttf", 22)
B20S = font("BeVietnamPro-SemiBold.ttf", 20)
B18  = font("BeVietnamPro-Regular.ttf", 18)
B16  = font("BeVietnamPro-Regular.ttf", 16)
M18  = font("JetBrainsMono-var.ttf", 18)
M16  = font("JetBrainsMono-var.ttf", 16)
M14  = font("JetBrainsMono-var.ttf", 14)

BLUE  = (59, 130, 246)
RED   = (239, 68, 68)
GREEN = (16, 185, 129)

def C(col, a=255):
    return (col[0], col[1], col[2], a)

# Shadow & Card Caching
_CH = {}
def chrome(w, h, r=22, border=(255, 255, 255, 40), fill=(22, 33, 57, 240)):
    key = (w, h, r, tuple(border), tuple(fill))
    if key not in _CH:
        _CH[key] = shadow_card(w, h, r, border=border, fill=fill)
    im, pad = _CH[key]
    return im.copy(), pad

_PIC = {}
_AR = {}

def pic_w(name, h):
    if name not in _AR:
        with Image.open(IMG + "/" + name + ".jpg") as im:
            _AR[name] = im.width / im.height
    return int(round(h * _AR[name]))

def photo(name, w, h, r=20, mode="contain"):
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

# Header Bar (Dynamic tag per scene)
_HDR_BASE = None
def draw_header(base, tag="PHẦN 01 · ĐẶT VẤN ĐỀ TRÙNG TÊN FILE", acc=BLUE):
    global _HDR_BASE
    if _HDR_BASE is None:
        im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([80, 102, W - 80, 102], fill=(255, 255, 255, 25), width=1)
        core.paste_brand(im, 80, 32, size=52)
        d.text((144, 34), "AN TECH ACADEMY", font=B22S, fill=TXT)
        d.text((144, 62), "Nền tảng kiến thức công nghệ thực chiến", font=B16, fill=MUT)
        _HDR_BASE = im
    base.alpha_composite(_HDR_BASE, (0, 0))
    d = ImageDraw.Draw(base)
    tw = int(B18.getlength(tag))
    bx = W - 80 - tw - 32
    d.rounded_rectangle([bx, 42, W - 80, 80], 19, fill=(22, 33, 57, 220), outline=C(acc, 120), width=1)
    d.ellipse([bx + 14, 58, bx + 22, 66], fill=acc)
    d.text((bx + 30, 49), tag, font=B18, fill=TXT)

# Generic Code / Data Card
def draw_code_card(base, cx, cy, w, h, p, title, lines, active_line=None):
    if p <= 0:
        return
    im, pad = chrome(w, h, 20, (255, 255, 255, 50), (16, 24, 40, 245))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w - 1, pad + 38], 20, fill=(24, 36, 60, 255))
    d.rectangle([pad, pad + 18, pad + w - 1, pad + 38], fill=(24, 36, 60, 255))
    d.ellipse([pad + 16, pad + 14, pad + 26, pad + 24], fill=(239, 68, 68))
    d.ellipse([pad + 34, pad + 14, pad + 44, pad + 24], fill=(245, 158, 11))
    d.ellipse([pad + 52, pad + 14, pad + 62, pad + 24], fill=(52, 211, 153))
    d.text((pad + 78, pad + 11), title, font=M14, fill=MUT)
    
    y = pad + 54
    for idx, l in enumerate(lines):
        if idx == active_line:
            d.rounded_rectangle([pad + 8, y - 2, pad + w - 10, y + 22], 6, fill=(30, 58, 138, 180), outline=(96, 165, 250, 150), width=1)
        d.text((pad + 16, y), f"{idx+1:2d}  {l}", font=M14, fill=TXT if idx == active_line else (180, 195, 220))
        y += 24
    blit(base, im, cx, cy, p, 12)

# Subtitle auto
def caption_auto(base, text, p=1.0):
    if p <= 0 or not text:
        return
    words = text.split()
    lines, cur = [], ""
    f = font("BeVietnamPro-Medium.ttf", 25)
    for w in words:
        cand = (cur + " " + w).strip()
        if not cur or f.getlength(cand) <= 750:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    caption(base, lines[:2], p=min(1.0, p))

# Audio helpers
def decode(path):
    cmd = [FF, "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"]
    p = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768.0

def dur(path):
    cmd = [FF, "-i", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3)) if m else 0.0

# Load script
with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
    SCRIPT_DATA = json.load(f)

ALL_CUES = []
SCENE_MAP = {}
for sc in SCRIPT_DATA["scenes"]:
    SCENE_MAP[sc["id"]] = sc
    for c in sc["cues"]:
        c["scene_id"] = sc["id"]
        c["scene_tag"] = sc["tag"]
        ALL_CUES.append(c)

def build_full_timeline():
    tl = {}
    durs = {}
    cur = 1.0  # 1s mở đầu
    starts = {}
    for c in ALL_CUES:
        cid = c["id"]
        scid = c["scene_id"]
        if scid not in starts:
            starts[scid] = cur
        p = f"{AUD}/{cid}.wav"
        d = dur(p)
        durs[cid] = d
        tl[cid] = cur
        cur += d + 0.45
    total = cur + 1.5
    return tl, durs, total, starts

def build_full_sfx(tl, durs, total, starts):
    bus = np.zeros(int(total * SR) + SR)
    def add(name, t, gain=1.0, dur_sfx=None):
        raw = sfx.sfx(name)
        if dur_sfx and name == "marker":
            raw = sfx.sfx(name, dur=dur_sfx)
        i0 = int(t * SR)
        i1 = min(len(bus), i0 + len(raw))
        bus[i0:i1] += raw[:i1 - i0] * gain

    # Whoosh mở đầu
    add("whoosh", 0.1, 0.45)
    add("pop", 0.9, 0.45)
    
    for scid, st in starts.items():
        if st > 1.0:
            add("whoosh", st - 0.2, 0.4)
            add("pop", st + 0.3, 0.45)
            
    # SFX chi tiết cho các điểm quan trọng
    add("marker", tl["c03"] + 0.8, 0.5, dur_sfx=0.5)
    add("marker", tl["c04"] + 0.8, 0.5, dur_sfx=0.5)
    add("pop", tl["c06"], 0.6)  # Overwrite alert
    add("marker", tl["c16"] + 0.8, 0.5, dur_sfx=0.5)  # UUID formula
    add("pop", tl["c22"], 0.5)  # avatar_path column
    add("marker", tl["c26"] + 0.8, 0.5, dur_sfx=0.5)  # enctype
    add("pop", tl["c38"], 0.6)  # Prepared statements
    add("chime", tl["c43"], 0.5)  # Browser loads correct avatar
    add("marker", tl["c48"] + 0.8, 0.5, dur_sfx=0.5)  # SHA-256
    add("pop", tl["c58"], 0.5)  # Takeaways 1
    add("pop", tl["c59"], 0.5)  # Takeaways 2
    add("pop", tl["c60"], 0.5)  # Takeaways 3
    add("chime", tl["c62"], 0.6)  # Outro chime
    
    return bus

# Draw Full Frame
def draw_frame(t, tl, durs, starts):
    base = demo20.bg()
    
    # Xác định scene hiện tại
    cur_sc = "s01"
    for sc in SCRIPT_DATA["scenes"]:
        scid = sc["id"]
        if t >= starts[scid]:
            cur_sc = scid
            
    tag = SCENE_MAP[cur_sc]["tag"]
    draw_header(base, tag, CYAN if cur_sc in ["s01","s03","s05","s07","s09"] else EMER)
    
    # Determine which cue is speaking
    cur_cue = None
    for c in ALL_CUES:
        cid = c["id"]
        t0 = tl[cid]
        t1 = t0 + durs[cid]
        if t0 <= t <= t1 + 0.4:
            cur_cue = c
            break
            
    # Character pose and look
    is_talking = any(tl[c["id"]] <= t <= tl[c["id"]] + durs[c["id"]] for c in ALL_CUES)
    
    if cur_sc == "s01":
        pose = "wave" if t < starts["s01"] + 3.5 else ("point_left" if t < tl["c05"] else "think")
        look = 0 if t < starts["s01"] + 3.5 else (-1 if t < tl["c06"] else 0)
    elif cur_sc in ["s02", "s03", "s04", "s05", "s07"]:
        pose = "point_left"
        look = -1
    elif cur_sc == "s06":
        pose = "present" if t < tl["c34"] else "point_left"
        look = -1
    elif cur_sc == "s08":
        pose = "think" if t < tl["c48"] else "present"
        look = 0 if t < tl["c48"] else -1
    elif cur_sc == "s09":
        pose = "point_left" if t < tl["c55"] else "think"
        look = -1
    else:  # s10
        pose = "present" if t < tl["c61"] else "wave"
        look = -1 if t < tl["c61"] else 0
        
    character.paste(base, x=1560, y=930, t=t, pose=pose, look=look, talking=is_talking, scale=0.95, anchor="bl")

    d = ImageDraw.Draw(base)

    # SCENE 1: ĐẶT VẤN ĐỀ TRÙNG TÊN FILE
    if cur_sc == "s01":
        d.text((120, 160), "BÀI GIẢNG CÔNG NGHỆ CHUYÊN ĐỀ", font=B20S, fill=CYAN)
        d.text((120, 195), "XỬ LÝ TRÙNG LẶP TÊN FILE AVATAR", font=B52B, fill=TXT)
        d.text((120, 270), "Hai người dùng tải lên cùng tên 1.jpg — Lưu trữ & truy xuất thế nào?", font=B24S, fill=MUT)
        
        t_c03 = tl["c03"]
        t_c05 = tl["c05"]
        if t < t_c03:
            photo_card(base, "1", 640, 630, 840, 480, lin(t, starts["s01"], starts["s01"] + 0.6), acc=BLUE, mode="contain")
            if t >= tl["c02"]:
                demo20.chip(base, "HỆ THỐNG QUẢN LÝ NGƯỜI DÙNG", CYAN, 640, 410, p=lin(t, tl["c02"], tl["c02"] + 0.4))
        else:
            p_a = lin(t, t_c03, t_c03 + 0.5)
            photo_card(base, "2", 430, 620, 460, 460, p_a, acc=EMER, mode="cover")
            demo20.chip(base, "USER A: 1.jpg (Chân dung)", EMER, 430, 410, p=p_a)
            if t >= t_c03 + 0.6:
                core.draw_marker(d, 330, 430, 530, 430, lin(t, t_c03 + 0.6, t_c03 + 1.2), color=(52, 211, 153, 230), width=6)
                
            if t >= tl["c04"]:
                p_b = lin(t, tl["c04"], tl["c04"] + 0.5)
                photo_card(base, "3", 940, 620, 460, 460, p_b, acc=CYAN, mode="cover")
                demo20.chip(base, "USER B: 1.jpg (Chú mèo)", CYAN, 940, 410, p=p_b)
                if t >= tl["c04"] + 0.6:
                    core.draw_marker(d, 840, 430, 1040, 430, lin(t, tl["c04"] + 0.6, tl["c04"] + 1.2), color=(56, 189, 248, 230), width=6)
                    
            if t >= t_c05:
                p_warn = lin(t, t_c05, t_c05 + 0.5)
                photo_card(base, "5", 685, 620, 700, 360, p_warn, acc=AMBER if t < tl["c06"] else RED, mode="contain", rise=20)
                if t < tl["c06"]:
                    demo20.chip(base, "CÙNG LƯU VÀO: uploads/1.jpg ?", AMBER, 685, 460, p=p_warn)
                else:
                    p_err = lin(t, tl["c06"], tl["c06"] + 0.4)
                    demo20.chip(base, "CẢNH BÁO: GHI ĐÈ FILE (OVERWRITE)!", RED, 685, 460, p=p_err)

    # SCENE 2: BẢN CHẤT TÊN FILE VS ĐƯỜNG DẪN
    elif cur_sc == "s02":
        d.text((120, 160), "BẢN CHẤT LƯU TRỮ HỆ THỐNG", font=B20S, fill=EMER)
        d.text((120, 195), "TÊN FILE KHÔNG PHẢI ĐỊNH DANH DUY NHẤT", font=B42B, fill=TXT)
        d.text((120, 260), "Đường dẫn đầy đủ (Full Path) mới là thứ xác định vị trí file trên đĩa", font=B22S, fill=MUT)
        
        st = starts["s02"]
        p_s02 = lin(t, st, st + 0.6)
        # Lockers (4.jpg)
        photo_card(base, "4", 450, 620, 480, 440, p_s02, acc=BLUE, mode="contain")
        demo20.chip(base, "ẨN DỤ: THƯ MỤC NHƯ NGĂN TỦ", BLUE, 450, 410, p=p_s02)
        
        # Two-level directory (6.jpg)
        if t >= tl["c09"]:
            p_dir = lin(t, tl["c09"], tl["c09"] + 0.5)
            photo_card(base, "6", 980, 620, 520, 440, p_dir, acc=EMER, mode="contain")
            demo20.chip(base, "MỖI USER CÓ MỘT THƯ MỤC RIÊNG", EMER, 980, 410, p=p_dir)
            
        if t >= tl["c10"]:
            # Path comparison highlight
            d.rounded_rectangle([250, 810, 1180, 850], 8, fill=(16, 24, 40, 240), outline=(59, 130, 246, 120), width=1)
            d.text((270, 820), "User A: Website/UserA/1.jpg   ≠   User B: Website/UserB/1.jpg", font=M16, fill=CYAN)

    # SCENE 3: GIẢI PHÁP UUID VÀ THƯ MỤC RIÊNG
    elif cur_sc == "s03":
        d.text((120, 160), "THIẾT KẾ GIẢI PHÁP TIÊU CHUẨN", font=B20S, fill=CYAN)
        d.text((120, 195), "KẾT HỢP USER_ID VÀ UUID TÊN FILE", font=B42B, fill=TXT)
        d.text((120, 260), "Triệt tiêu 100% nguy cơ trùng lặp tên file bằng hàm ngẫu nhiên", font=B22S, fill=MUT)
        
        st = starts["s03"]
        p_s03 = lin(t, st, st + 0.6)
        # UUID Ring server (7.jpg)
        photo_card(base, "7", 450, 620, 500, 460, p_s03, acc=CYAN, mode="cover")
        demo20.chip(base, "CHUỖI UUID 128-BIT ĐỘC NHẤT", CYAN, 450, 400, p=p_s03)
        
        # Right Mapping Table Card
        if t >= tl["c14"]:
            p_tbl = lin(t, tl["c14"], tl["c14"] + 0.5)
            tbl_lines = [
                "// Cấu trúc thư mục tối ưu",
                "uploads/",
                " ├── user_101/ (User A)",
                " │    └── a83f91c2d45e7890a12b...jpg",
                " └── user_205/ (User B)",
                "      └── d71b42e9a12c34f56789...jpg",
                "",
                "// PHP Tạo tên ngẫu nhiên 32 ký tự:",
                "$newName = bin2hex(random_bytes(16)) . '.' . $ext;"
            ]
            draw_code_card(base, 980, 620, 520, 460, p_tbl, "folder_structure.txt", tbl_lines, active_line=8)

    # SCENE 4: THIẾT KẾ MYSQL: TÁCH NƠI LƯU VÀ METADATA
    elif cur_sc == "s04":
        d.text((120, 160), "KIẾN TRÚC CƠ SỞ DỮ LIỆU", font=B20S, fill=EMER)
        d.text((120, 195), "TÁCH BIỆT FILE STORAGE VÀ MYSQL", font=B42B, fill=TXT)
        d.text((120, 260), "File lưu trên ổ đĩa máy chủ — MySQL chỉ lưu đường dẫn avatar_path", font=B22S, fill=MUT)
        
        st = starts["s04"]
        p_s04 = lin(t, st, st + 0.6)
        # Infographic Data & File Separated (8.jpg)
        photo_card(base, "8", 470, 620, 540, 440, p_s04, acc=EMER, mode="contain")
        demo20.chip(base, "DỮ LIỆU & FILE LƯU TÁCH RỜI", EMER, 470, 410, p=p_s04)
        
        # Web - App - DB Flow (10.jpg)
        if t >= tl["c21"]:
            p_flow = lin(t, tl["c21"], tl["c21"] + 0.5)
            photo_card(base, "10", 990, 620, 480, 440, p_flow, acc=BLUE, mode="contain")
            demo20.chip(base, "LUỒNG TRUY VẤN QUA DATABASE", BLUE, 990, 410, p=p_flow)

    # SCENE 5: THỰC HÀNH HTML & CSS
    elif cur_sc == "s05":
        d.text((120, 160), "THỰC HÀNH GIAO DIỆN WEB", font=B20S, fill=CYAN)
        d.text((120, 195), "FORM UPLOAD HTML VÀ CẮT AVATAR TRÒN CSS", font=B42B, fill=TXT)
        d.text((120, 260), "Kỹ thuật object-fit: cover và border-radius: 50% chống méo ảnh", font=B22S, fill=MUT)
        
        st = starts["s05"]
        p_s05 = lin(t, st, st + 0.6)
        html_lines = [
            "<form action=\"upload.php\" method=\"POST\"",
            "      enctype=\"multipart/form-data\">",
            "    <input type=\"file\" name=\"avatar\"",
            "           accept=\"image/jpeg,image/png,image/webp\"",
            "           required>",
            "    <button type=\"submit\">Cập nhật ảnh</button>",
            "</form>",
            "",
            "/* CSS Avatar Tròn */",
            ".avatar {",
            "    width: 140px; height: 140px;",
            "    border-radius: 50%;",
            "    object-fit: cover; /* Không méo */",
            "}"
        ]
        draw_code_card(base, 450, 620, 500, 460, p_s05, "index.php & style.css", html_lines, active_line=1)
        
        # Circle Crop Avatar (9.jpg) & Format Frames (11.jpg)
        if t >= tl["c27"]:
            p_img9 = lin(t, tl["c27"], tl["c27"] + 0.5)
            photo_card(base, "9", 980, 520, 520, 260, p_img9, acc=CYAN, mode="contain")
            demo20.chip(base, "CSS OBJECT-FIT: COVER", CYAN, 980, 400, p=p_img9)
            
        if t >= tl["c30"]:
            p_img11 = lin(t, tl["c30"], tl["c30"] + 0.5)
            photo_card(base, "11", 980, 750, 520, 180, p_img11, acc=BLUE, mode="cover")

    # SCENE 6: XỬ LÝ PHP 8 BƯỚC AN TOÀN
    elif cur_sc == "s06":
        d.text((120, 160), "LẬP TRÌNH BACKEND AN TOÀN", font=B20S, fill=EMER)
        d.text((120, 195), "QUY TRÌNH 8 BƯỚC XỬ LÝ UPLOAD TRONG PHP", font=B42B, fill=TXT)
        d.text((120, 260), "Kiểm tra MIME byte thực tế và bảo vệ CSDL với Prepared Statements", font=B22S, fill=MUT)
        
        st = starts["s06"]
        p_s06 = lin(t, st, st + 0.6)
        # Developer Photo (16.jpg)
        photo_card(base, "16", 430, 620, 460, 460, p_s06, acc=EMER, mode="cover")
        demo20.chip(base, "LẬP TRÌNH VIÊN THỰC CHIẾN", EMER, 430, 400, p=p_s06)
        
        # 8-step security checklist card
        p_steps = lin(t, st + 0.3, st + 0.8)
        step_lines = [
            "1. Xác thực session user_id (không tin client)",
            "2. Kiểm tra $_FILES['avatar']['error'] == OK",
            "3. Giới hạn kích thước file <= 5 MiB",
            "4. Kiểm tra MIME byte thực tế bằng finfo",
            "5. Tự động sinh tên ngẫu nhiên bin2hex()",
            "6. Tạo thư mục user riêng: mkdir(0755)",
            "7. Di chuyển file: move_uploaded_file()",
            "8. Cập nhật MySQL với Prepared Statements"
        ]
        # Active step depends on cue
        act = None
        if tl["c32"] <= t < tl["c33"]: act = 0
        elif tl["c33"] <= t < tl["c34"]: act = 2
        elif tl["c34"] <= t < tl["c35"]: act = 3
        elif tl["c35"] <= t < tl["c36"]: act = 4
        elif tl["c36"] <= t < tl["c37"]: act = 5
        elif tl["c37"] <= t < tl["c38"]: act = 6
        elif t >= tl["c38"]: act = 7
        
        draw_code_card(base, 980, 620, 520, 460, p_steps, "upload.php (Security Flow)", step_lines, active_line=act)

    # SCENE 7: TRUY XUẤT ĐÚNG ẢNH ĐẠI DIỆN
    elif cur_sc == "s07":
        d.text((120, 160), "LUỒNG TRUY VẤN VÀ HIỂN THỊ", font=B20S, fill=CYAN)
        d.text((120, 195), "CƠ CHẾ TRUY XUẤT ĐÚNG ẢNH CỦA TỪNG USER", font=B42B, fill=TXT)
        d.text((120, 260), "PHP truy vấn đường dẫn từ MySQL — Trình duyệt gửi HTTP GET tải file", font=B22S, fill=MUT)
        
        st = starts["s07"]
        p_s07 = lin(t, st, st + 0.6)
        # Architecture Diagram (15.jpg)
        photo_card(base, "15", 720, 620, 840, 480, p_s07, acc=CYAN, mode="contain")
        
        if t >= tl["c41"]:
            demo20.chip(base, "1. PHP: SELECT avatar_path FROM users WHERE id = ?", CYAN, 430, 395, p=lin(t, tl["c41"], tl["c41"]+0.4))
        if t >= tl["c42"]:
            demo20.chip(base, "2. MySQL trả về: uploads/user_1/a83f91c2.jpg", EMER, 980, 395, p=lin(t, tl["c42"], tl["c42"]+0.4))
        if t >= tl["c43"]:
            demo20.chip(base, "3. Trình duyệt HTTP GET tải ảnh về hiển thị", BLUE, 720, 850, p=lin(t, tl["c43"], tl["c43"]+0.4))

    # SCENE 8: TRÙNG TÊN VS TRÙNG NỘI DUNG (SHA-256)
    elif cur_sc == "s08":
        d.text((120, 160), "MỞ RỘNG KIẾN THỨC", font=B20S, fill=AMBER)
        d.text((120, 195), "PHÂN BIỆT TRÙNG TÊN FILE VÀ TRÙNG NỘI DUNG", font=B42B, fill=TXT)
        d.text((120, 260), "Dùng thuật toán băm SHA-256 để phát hiện file có nội dung byte giống hệt nhau", font=B22S, fill=MUT)
        
        st = starts["s08"]
        p_s08 = lin(t, st, st + 0.6)
        
        sha_lines = [
            "// Kiểm tra 2 file có nội dung byte giống nhau:",
            "$hashA = hash_file('sha256', 'uploads/1.jpg');",
            "$hashB = hash_file('sha256', 'uploads/avatar.png');",
            "",
            "if ($hashA === $hashB) {",
            "    echo 'Nội dung byte trùng khớp 100%!';",
            "} else {",
            "    echo 'Nội dung dữ liệu khác nhau.';",
            "}",
            "",
            "// Nhận diện ảnh tương đồng thị giác:",
            "// -> Sử dụng Perceptual Hashing (pHash, aHash, dHash)"
        ]
        draw_code_card(base, 460, 620, 520, 460, p_s08, "sha256_deduplication.php", sha_lines, active_line=4 if t >= tl["c49"] else 1)
        
        # Right comparison visual
        if t >= tl["c46"]:
            p_comp = lin(t, tl["c46"], tl["c46"] + 0.5)
            im_cmp, pad = chrome(480, 460, 20, C(AMBER, 80), (18, 27, 46, 240))
            d_cmp = ImageDraw.Draw(im_cmp)
            d_cmp.text((pad + 24, pad + 24), "SO SÁNH BẢN CHẤT", font=B24S, fill=AMBER)
            d_cmp.text((pad + 24, pad + 70), "• Trùng tên file:", font=B20S, fill=TXT)
            d_cmp.text((pad + 40, pad + 105), "Cùng '1.jpg' nhưng ảnh khác nhau", font=B18, fill=MUT)
            d_cmp.text((pad + 40, pad + 135), "-> Giải quyết: Thư mục riêng + UUID", font=B18, fill=CYAN)
            
            d_cmp.text((pad + 24, pad + 190), "• Trùng nội dung byte:", font=B20S, fill=TXT)
            d_cmp.text((pad + 40, pad + 225), "Khác tên nhưng dữ liệu nhị phân trùng", font=B18, fill=MUT)
            d_cmp.text((pad + 40, pad + 255), "-> Giải quyết: Băm SHA-256", font=B18, fill=EMER)
            
            d_cmp.text((pad + 24, pad + 315), "• Tương đồng hình ảnh thị giác:", font=B20S, fill=TXT)
            d_cmp.text((pad + 40, pad + 350), "Ảnh cùng góc chụp nhưng đổi màu/nén", font=B18, fill=MUT)
            d_cmp.text((pad + 40, pad + 380), "-> Giải quyết: Perceptual Hashing (pHash)", font=B18, fill=AMBER)
            blit(base, im_cmp, 980, 620, p_comp, 12)

    # SCENE 9: ỨNG DỤNG THỰC TẾ & SAI LẦM CẦN TRÁNH
    elif cur_sc == "s09":
        d.text((120, 160), "ỨNG DỤNG THỰC CHIẾN", font=B20S, fill=CYAN)
        d.text((120, 195), "ÁP DỤNG HỆ THỐNG LỚN VÀ CÁC BẪY CẦN TRÁNH", font=B42B, fill=TXT)
        d.text((120, 260), "Thương mại điện tử, mạng xã hội, quản lý nhân sự và Cloud Storage", font=B22S, fill=MUT)
        
        st = starts["s09"]
        p_s09 = lin(t, st, st + 0.6)
        
        # 3 Real-world photos: E-commerce (12.jpg), HR/School (13.jpg), Community (14.jpg)
        photo_card(base, "12", 360, 520, 360, 260, p_s09, acc=CYAN, mode="cover")
        demo20.chip(base, "E-COMMERCE (12.jpg)", CYAN, 360, 400, p=p_s09)
        
        if t >= tl["c52"]:
            p_s09_2 = lin(t, tl["c52"], tl["c52"] + 0.5)
            photo_card(base, "13", 720, 520, 340, 260, p_s09_2, acc=BLUE, mode="cover")
            demo20.chip(base, "QUẢN LÝ NHÂN SỰ (13.jpg)", BLUE, 720, 400, p=p_s09_2)
            
            photo_card(base, "14", 1070, 520, 340, 260, p_s09_2, acc=EMER, mode="cover")
            demo20.chip(base, "MẠNG XÃ HỘI (14.jpg)", EMER, 1070, 400, p=p_s09_2)
            
        # Bottom Warning Bar
        if t >= tl["c55"]:
            p_warn_bar = lin(t, tl["c55"], tl["c55"] + 0.5)
            d.rounded_rectangle([190, 690, 1250, 840], 16, fill=(28, 20, 30, 245), outline=C(RED, 120), width=1)
            d.text((220, 715), "4 SAI LẦM CHÍ MẠNG CẦN TRÁNH:", font=B20S, fill=RED)
            d.text((220, 755), "1. Tin đuôi file .jpg mà không kiểm tra MIME type  •  2. Không giới hạn kích thước upload", font=B16, fill=TXT)
            d.text((220, 790), "3. Không dọn dẹp ảnh cũ khi cập nhật ảnh mới  •  4. Nghĩ tên ngẫu nhiên là đã bảo mật", font=B16, fill=(220, 200, 200))

    # SCENE 10: TỔNG KẾT & LỜI KẾT
    else:
        d.text((120, 160), "TỔNG KẾT BÀI HỌC", font=B20S, fill=EMER)
        d.text((120, 195), "3 NGUYÊN TẮC VÀNG QUẢN LÝ TỆP TIN", font=B42B, fill=TXT)
        d.text((120, 260), "Tổ chức khoa học, xác thực chủ sở hữu và truy xuất chính xác", font=B22S, fill=MUT)
        
        st = starts["s10"]
        p_s10 = lin(t, st, st + 0.6)
        
        # 3 Core takeaways
        chips_data = [
            ("1. TRÁNH GHI ĐÈ", "Tạo thư mục riêng theo user_id kết hợp tên UUID ngẫu nhiên", EMER, 480, tl["c58"]),
            ("2. XÁC THỰC CHỦ SỞ HỮU", "Luôn lấy user_id từ phiên làm việc Session phía server đã đăng nhập", CYAN, 590, tl["c59"]),
            ("3. TRUY XUẤT CHÍNH XÁC", "MySQL lưu avatar_path tương đối, truy vấn qua Prepared Statements", BLUE, 700, tl["c60"]),
        ]
        
        for title_chip, desc_chip, col_chip, y_chip, t_cue in chips_data:
            if t >= t_cue:
                p_c = lin(t, t_cue, t_cue + 0.4)
                im_c, pad = chrome(880, 88, 16, C(col_chip, 90), (18, 27, 46, 240))
                d_c = ImageDraw.Draw(im_c)
                d_c.rounded_rectangle([pad + 12, pad + 16, pad + 190, pad + 52], 12, fill=C(col_chip, 40), outline=col_chip, width=1)
                d_c.text((pad + 24, pad + 24), title_chip, font=B18, fill=col_chip)
                d_c.text((pad + 205, pad + 24), desc_chip, font=B18, fill=TXT)
                blit(base, im_c, 640, y_chip, p_c, 8)
                
        if t >= tl["c61"]:
            # Outro AN TECH ACADEMY badge
            p_out = lin(t, tl["c61"], tl["c61"] + 0.5)
            core.paste_brand(base, 600, 800, size=64)
            d.text((680, 810), "AN TECH ACADEMY — CÙNG BẠN CHINH PHỤC CÔNG NGHỆ!", font=B20S, fill=CYAN)

    # Subtitle
    if cur_cue:
        caption_auto(base, cur_cue["sub"], p=1.0)
        
    return base

def main():
    tl, durs, total, starts = build_full_timeline()
    print(f"Tổng số cảnh: 10, Tổng số cues: {len(ALL_CUES)}")
    print(f"Tổng thời lượng video: {total:.2f}s (~{int(total//60)} phút {int(total%60)} giây)")
    
    if "--stills" in sys.argv:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        # Lấy mỗi scene 1 ảnh tĩnh đại diện
        picks = [st + 2.0 for st in starts.values()]
        for i, tt in enumerate(picks):
            draw_frame(tt, tl, durs, starts).convert("RGB").save(f"{sd}/scene_{i+1:02d}_{tt:.1f}s.png")
            print(f"STILL Scene {i+1}: {tt:.1f}s")
        print("Đã xuất stills toàn bộ 10 cảnh thành công!")
        return

    n = int(total * FPS)
    mix = np.zeros(int(total * SR) + SR)
    for c in ALL_CUES:
        cid = c["id"]
        x = decode(f"{AUD}/{cid}.wav")
        s0 = int(tl[cid] * SR)
        mix[s0:s0 + len(x)] += x
        
    bus = build_full_sfx(tl, durs, total, starts)
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
            draw_frame(k / FPS, tl, durs, starts).convert("RGB").save(fp, quality=92)
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

    # Chuẩn hóa âm thanh EBU R128 (-14 LUFS)
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
