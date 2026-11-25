# -*- coding: utf-8 -*-
"""Video mẫu Cổng B (30s) — Bài giảng: Xử lý trùng lặp tên file Avatar
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

# Thiết lập đường dẫn Kit dùng chung
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
AUD = PROJECT + "/mau/sample/audio"
OUT = PROJECT + "/mau/sample"
FR = OUT + "/frames"
IMG = PROJECT + "/img"
TAG = "avatar_sample_30s"

os.makedirs(OUT, exist_ok=True)
os.makedirs(FR, exist_ok=True)

# Fonts
B52B = font("BeVietnamPro-Bold.ttf", 52)
B42B = font("BeVietnamPro-Bold.ttf", 40)
B28B = font("BeVietnamPro-Bold.ttf", 28)
B24S = font("BeVietnamPro-SemiBold.ttf", 24)
B20S = font("BeVietnamPro-SemiBold.ttf", 20)
B18  = font("BeVietnamPro-Regular.ttf", 18)
B16  = font("BeVietnamPro-Regular.ttf", 16)
B22S = font("BeVietnamPro-SemiBold.ttf", 22)
M18  = font("JetBrainsMono-var.ttf", 18)
M16  = font("JetBrainsMono-var.ttf", 16)

BLUE = (59, 130, 246)
RED  = (239, 68, 68)

def C(col, a=255):
    return (col[0], col[1], col[2], a)

# Caching Chrome
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
def draw_header(base, tag="PHẦN 01 · ĐẶT VẤN ĐỀ TRÙNG TÊN FILE", acc=BLUE):
    global _HDR
    if _HDR is None:
        im = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([80, 102, W - 80, 102], fill=(255, 255, 255, 25), width=1)
        core.paste_brand(im, 80, 32, size=52)
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

# Decode WAV
def decode(path):
    cmd = [FF, "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"]
    p = subprocess.run(cmd, capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768.0

def dur(path):
    cmd = [FF, "-i", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3)) if m else 0.0

# 6 Cues for Scene 1 (Tách riêng say cho TTS và sub cho hiển thị)
CUES = [
    {
        "id": "c01",
        "say": "Xin chào các bạn! Chào mừng đến với An Tếch Academy, nền tảng kiến thức công nghệ thực chiến.",
        "sub": "Xin chào các bạn! Chào mừng đến với AN TECH ACADEMY, nền tảng kiến thức công nghệ thực chiến."
    },
    {
        "id": "c02",
        "say": "Hãy tưởng tượng chúng ta đang xây dựng một ứng dụng quản lý người dùng.",
        "sub": "Hãy tưởng tượng chúng ta đang xây dựng một ứng dụng quản lý người dùng."
    },
    {
        "id": "c03",
        "say": "Người dùng A tải lên ảnh đại diện tên một chấm j p e g là ảnh chân dung của mình.",
        "sub": "Người dùng A tải lên ảnh đại diện tên 1.jpg là ảnh chân dung của mình."
    },
    {
        "id": "c04",
        "say": "Cùng lúc đó, người dùng B cũng tải lên một ảnh tên một chấm j p e g, nhưng lại là ảnh một chú mèo dễ thương.",
        "sub": "Cùng lúc đó, người dùng B cũng tải lên một ảnh tên 1.jpg, nhưng lại là ảnh một chú mèo dễ thương."
    },
    {
        "id": "c05",
        "say": "Nếu hệ thống chỉ lưu theo tên tệp tin vào một thư mục chung, chuyện gì sẽ xảy ra?",
        "sub": "Nếu hệ thống chỉ lưu theo tên file vào một thư mục chung, chuyện gì sẽ xảy ra?"
    },
    {
        "id": "c06",
        "say": "Đúng vậy, ảnh của người dùng A sẽ bị ảnh của người dùng B ghi đè hoàn toàn!",
        "sub": "Đúng vậy, ảnh của người dùng A sẽ bị ảnh của người dùng B ghi đè hoàn toàn!"
    },
]

def build_timeline():
    tl = {}
    durs = {}
    cur = 1.0  # 1s mở đầu
    for c in CUES:
        cid = c["id"]
        p = f"{AUD}/{cid}.wav"
        d = dur(p)
        durs[cid] = d
        tl[cid] = cur
        cur += d + 0.52
    total = cur + 1.2
    return tl, durs, total

# Build SFX Bus
def build_sfx(tl, durs, total):
    bus = np.zeros(int(total * SR) + SR)
    def add(name, t, gain=1.0, dur_sfx=None):
        raw = sfx.sfx(name)
        if dur_sfx and name == "marker":
            raw = sfx.sfx(name, dur=dur_sfx)
        i0 = int(t * SR)
        i1 = min(len(bus), i0 + len(raw))
        bus[i0:i1] += raw[:i1 - i0] * gain

    add("whoosh", 0.1, 0.45)
    add("pop", 0.9, 0.45)
    
    # User A xuất hiện
    add("whoosh", tl["c03"] - 0.2, 0.4)
    add("pop", tl["c03"], 0.5)
    add("marker", tl["c03"] + 0.8, 0.5, dur_sfx=0.5)
    
    # User B xuất hiện
    add("whoosh", tl["c04"] - 0.2, 0.4)
    add("pop", tl["c04"], 0.5)
    add("marker", tl["c04"] + 0.8, 0.5, dur_sfx=0.5)
    
    # Warning ghi đè
    add("whoosh", tl["c05"] - 0.1, 0.45)
    add("pop", tl["c05"] + 0.2, 0.6)
    add("pop", tl["c06"], 0.6)
    
    return bus

# Draw Single Frame
def draw_frame(t, tl, durs):
    base = demo20.bg()
    draw_header(base, "PHẦN 01 · ĐẶT VẤN ĐỀ TRÙNG TÊN FILE", CYAN)
    
    # Text Header cảnh 1
    d = ImageDraw.Draw(base)
    d.text((120, 160), "BÀI GIẢNG CÔNG NGHỆ CHUYÊN ĐỀ", font=B20S, fill=CYAN)
    d.text((120, 195), "XỬ LÝ TRÙNG LẶP TÊN FILE AVATAR", font=B52B, fill=TXT)
    d.text((120, 270), "Hai người dùng tải lên cùng tên 1.jpg — Lưu trữ & truy xuất thế nào?", font=B24S, fill=MUT)
    
    # Nhân vật An
    t_c03 = tl["c03"]
    t_c05 = tl["c05"]
    
    if t < t_c03:
        pose = "wave" if t < 4.0 else "idle"
        look = 0 if t < 4.0 else -1
    elif t < t_c05:
        pose = "point_left"
        look = -1
    else:
        pose = "think"
        look = -1 if t >= tl["c06"] else 0
        
    is_talking = any(tl[c["id"]] <= t <= tl[c["id"]] + durs[c["id"]] for c in CUES)
    character.paste(base, x=1560, y=930, t=t, pose=pose, look=look, talking=is_talking, scale=0.95, anchor="bl")

    # Trung tâm hiển thị
    if t < t_c03:
        # Cue 1 & 2: Ảnh Cloud / Lưu trữ người dùng (1.jpg)
        p_card = lin(t, 0.8, 1.4)
        photo_card(base, "1", 640, 630, 840, 480, p_card, acc=BLUE, mode="contain")
        if t >= tl["c02"]:
            p_chip = lin(t, tl["c02"], tl["c02"] + 0.4)
            demo20.chip(base, "HỆ THỐNG QUẢN LÝ NGƯỜI DÙNG", CYAN, 640, 410, p=p_chip)
    else:
        # Cue 3 trở đi: User A và User B
        # Card User A (2.jpg)
        p_a = lin(t, t_c03, t_c03 + 0.5)
        photo_card(base, "2", 430, 620, 460, 460, p_a, acc=EMER, mode="cover")
        demo20.chip(base, "USER A: 1.jpg (Chân dung)", EMER, 430, 410, p=p_a)
        
        # Hand-drawn marker gạch chân tên 1.jpg của User A
        if t >= t_c03 + 0.6:
            p_mk_a = lin(t, t_c03 + 0.6, t_c03 + 1.2)
            d_base = ImageDraw.Draw(base)
            core.draw_marker(d_base, 330, 430, 530, 430, p_mk_a, color=(52, 211, 153, 230), width=6)
            
        # Card User B (3.jpg)
        if t >= tl["c04"]:
            p_b = lin(t, tl["c04"], tl["c04"] + 0.5)
            photo_card(base, "3", 940, 620, 460, 460, p_b, acc=CYAN, mode="cover")
            demo20.chip(base, "USER B: 1.jpg (Chú mèo)", CYAN, 940, 410, p=p_b)
            
            # Hand-drawn marker gạch chân tên 1.jpg của User B
            if t >= tl["c04"] + 0.6:
                p_mk_b = lin(t, tl["c04"] + 0.6, tl["c04"] + 1.2)
                d_base = ImageDraw.Draw(base)
                core.draw_marker(d_base, 840, 430, 1040, 430, p_mk_b, color=(56, 189, 248, 230), width=6)
                
        # Cue 5 & 6: Popup cảnh báo ghi đè (5.jpg)
        if t >= t_c05:
            p_warn = lin(t, t_c05, t_c05 + 0.5)
            # Popup đè trung tâm
            photo_card(base, "5", 685, 620, 700, 360, p_warn, acc=AMBER if t < tl["c06"] else RED, mode="contain", rise=20)
            
            if t < tl["c06"]:
                demo20.chip(base, "CÙNG LƯU VÀO: uploads/1.jpg ?", AMBER, 685, 460, p=p_warn)
            else:
                p_err = lin(t, tl["c06"], tl["c06"] + 0.4)
                demo20.chip(base, "CẢNH BÁO: GHI ĐÈ FILE (OVERWRITE)!", RED, 685, 460, p=p_err)
                # Dấu gạch chéo đỏ hoặc khung viền cảnh báo
                d_base = ImageDraw.Draw(base)
                d_base.rounded_rectangle([335, 435, 1035, 805], 24, outline=(239, 68, 68, int(200 * p_err)), width=4)

    # Subtitle
    cur_sub = ""
    cur_p = 1.0
    for c in CUES:
        cid = c["id"]
        t0 = tl[cid]
        t1 = t0 + durs[cid]
        if t0 <= t <= t1 + 0.4:
            cur_sub = c["sub"]
            cur_p = 1.0 if t <= t1 else (1.0 - lin(t, t1, t1 + 0.4))
            break
            
    caption_auto(base, cur_sub, p=cur_p)
    return base

def main():
    tl, durs, total = build_timeline()
    print(f"Tổng thời lượng mẫu Cổng B: {total:.2f}s (~{int(total)}s)")
    
    if "--stills" in sys.argv:
        sd = OUT + "/stills"
        os.makedirs(sd, exist_ok=True)
        picks = [2.0, 7.5, 12.0, 16.5, 22.0, 26.5]
        for i, tt in enumerate(picks):
            draw_frame(tt, tl, durs).convert("RGB").save(f"{sd}/still_{i:02d}_{tt:.1f}s.png")
            print(f"STILL {i}: {tt:.1f}s")
        print("Đã xuất stills thành công!")
        return

    n = int(total * FPS)
    mix = np.zeros(int(total * SR) + SR)
    for c in CUES:
        cid = c["id"]
        x = decode(f"{AUD}/{cid}.wav")
        s0 = int(tl[cid] * SR)
        mix[s0:s0 + len(x)] += x
        
    bus = build_sfx(tl, durs, total)
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
            draw_frame(k / FPS, tl, durs).convert("RGB").save(fp, quality=92)
        if k % 150 == 0 or k == n - 1:
            fps_speed = (k + 1) / max(0.1, time.time() - t_f0)
            eta = (n - k) / max(0.1, fps_speed)
            print(f"Frame {k:5d}/{n} ({k/n*100:4.1f}%) | {fps_speed:.1f} fps | ETA: {eta:.0f}s", flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/video_{TAG}.mp4"
    print("Encode Video H.264...", flush=True)
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%05d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")

    # Chuẩn hóa âm thanh -14 LUFS
    print("Chuẩn hóa âm thanh EBU R128 (-14 LUFS)...", flush=True)
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
        
    print(f"DONE SAMPLE VIDEO: {final_mp4} ({dur(final_mp4):.2f}s)", flush=True)

if __name__ == "__main__":
    main()
