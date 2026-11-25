import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = "D:/Edit/Baigiang_CacchuyennganhIT"
MAU = ROOT + "/mau"
FR = MAU + "/motion_s10_frames"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
W, H, FPS = 1920, 1080, 30
BG = (248, 250, 252, 255)
INK = (15, 23, 42, 255)
MUT = (71, 85, 105, 255)
PUR = (124, 58, 237, 255)
WHITE = (255, 255, 255, 255)

os.makedirs(FR, exist_ok=True)

def font(path, size, weight=None):
    f = ImageFont.truetype(ROOT + "/assets/fonts/" + path, size)
    if weight:
        f.set_variation_by_axes([weight])
    return f

F_KICK = font("BeVietnamPro-SemiBold.ttf", 28)
F_HEAD = font("PlusJakartaSans-var.ttf", 56, 700)
F_LBL = font("BeVietnamPro-SemiBold.ttf", 32)
F_SUB = font("BeVietnamPro-Regular.ttf", 26)
F_CHIP = font("BeVietnamPro-SemiBold.ttf", 30)
F_SUBT = font("BeVietnamPro-Medium.ttf", 32)
F_PHONE = font("BeVietnamPro-SemiBold.ttf", 20)

def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)

def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3

def seg(t, a, b):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)

segs = {}
if "--dry" in sys.argv:
    segs = {k: 3.5 for k in ["s10a", "s10b", "s10c", "s10d"]}
else:
    for k in ["s10a", "s10b", "s10c", "s10d"]:
        segs[k] = dur(f"{MAU}/{k}.mp3")
g, tail = 0.2, 1.8
A = 0.0
B = A + segs["s10a"] + g
C = B + segs["s10b"] + g
D = C + segs["s10c"]
T = D + tail

SUBS = [
    (A, segs["s10a"], ["Ví dụ: bạn vừa xem một chiếc điện thoại", "trên trang thương mại điện tử,"]),
    (B, segs["s10b"], ["hệ thống phân tích lịch sử", "tìm kiếm và mua hàng,"]),
    (C, segs["s10c"], ["để gợi ý những sản phẩm hợp sở thích bạn."]),
]

def card_base(w=420, h=420):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w, h], 16, fill=(15, 23, 42, 20))
    d.rounded_rectangle([0, 0, w, h - 6], 16, fill=WHITE)
    return im

def node_icon(icon, label, sub):
    im = card_base()
    ic = Image.open(f"{ROOT}/assets/icons_png/{icon}.png").convert("RGBA")
    im.paste(ic, (110, 24), ic)
    d = ImageDraw.Draw(im)
    d.text((210, 300), label, font=F_LBL, fill=INK, anchor="mm")
    d.text((210, 346), sub, font=F_SUB, fill=MUT, anchor="mm")
    return im

def node_phone():
    im = card_base()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, 24, 300, 280], 24, fill=INK)
    d.rounded_rectangle([132, 36, 288, 268], 12, fill=WHITE)
    d.text((210, 58), "Gợi ý cho bạn", font=F_PHONE, fill=PUR, anchor="mm")
    for y0 in (82, 176):
        d.rounded_rectangle([142, y0, 278, y0 + 82], 10, fill=(241, 245, 249, 255))
        d.rounded_rectangle([152, y0 + 12, 186, y0 + 46], 8, fill=PUR)
        d.rounded_rectangle([196, y0 + 16, 268, y0 + 24], 4, fill=(148, 163, 184, 255))
        d.rounded_rectangle([196, y0 + 32, 256, y0 + 40], 4, fill=(203, 213, 225, 255))
        d.rounded_rectangle([152, y0 + 58, 268, y0 + 66], 4, fill=(203, 213, 225, 255))
    d.text((210, 300), "Sản phẩm gợi ý", font=F_LBL, fill=INK, anchor="mm")
    d.text((210, 346), "hợp sở thích bạn", font=F_SUB, fill=MUT, anchor="mm")
    return im

N1, N2, N3 = node_icon("history", "Lịch sử duyệt web", "xem · tìm kiếm · mua hàng"), node_icon("cpu", "Mô hình phân tích", "học từ dữ liệu"), node_phone()
NX = [150, 750, 1350]
NY = 280
CONN = [(570, 490, 750, 490), (1170, 490, 1350, 490)]

def draw_conn(d, c, p, dotq):
    x0, y0, x1, y1 = c
    L = x1 - x0
    head = 18
    xe = x0 + (L - head) * p
    d.line([x0, y0, xe, y0], fill=PUR, width=6)
    if p > 0.95:
        d.polygon([(x1, y0), (x1 - head, y0 - 9), (x1 - head, y0 + 9)], fill=PUR)
    if dotq is not None:
        dx = x0 + 6 + (L - head - 12) * dotq
        d.ellipse([dx - 9, y0 - 9, dx + 9, y0 + 9], fill=PUR)

def paste_node(base, im, x, y, p):
    if p <= 0:
        return
    s = 0.9 + 0.1 * p
    w = int(420 * s)
    r = im.resize((w, w), Image.LANCZOS) if s < 1 else im
    if p < 1:
        r.putalpha(r.getchannel("A").point(lambda a: int(a * p)))
    base.paste(r, (x + (420 - w) // 2, y + (420 - w) // 2), r)

N = int(math.ceil(T * FPS))
for i in range(N):
    t = i / FPS
    base = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(base)
    hp = seg(t, 0, 0.4)
    if hp > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        dy = int(14 * (1 - hp))
        od.text((96, 70 + dy), "KHOA HỌC DỮ LIỆU & AI · VÍ DỤ THỰC TẾ", font=F_KICK, fill=PUR)
        od.text((96, 112 + dy), "Hệ thống gợi ý sản phẩm", font=F_HEAD, fill=INK)
        ov.putalpha(ov.getchannel("A").point(lambda a: int(a * hp)))
        base = Image.alpha_composite(base, ov)
        d = ImageDraw.Draw(base)
    p1, p2, p3 = seg(t, 0.1, 0.5), seg(t, B, B + 0.4), seg(t, C, C + 0.4)
    paste_node(base, N1, NX[0], NY, p1)
    paste_node(base, N2, NX[1], NY, p2)
    paste_node(base, N3, NX[2], NY, p3)
    d = ImageDraw.Draw(base)
    act = 0 if t < B else (1 if t < C else (2 if t < D else -1))
    if act >= 0 and [p1, p2, p3][act] >= 1:
        x = NX[act]
        d.rounded_rectangle([x - 3, NY - 3, x + 423, NY + 417], 18, outline=PUR, width=3)
    db, dc = segs["s10b"], segs["s10c"]
    c1p = seg(t, B + 0.4, B + db - 0.8)
    c1dot = None
    if B + db - 0.8 <= t < B + db:
        c1dot = ((t - (B + db - 0.8)) / 0.8 * 2) % 1
    c2p = seg(t, C + 0.4, C + dc - 0.8)
    c2dot = None
    if C + dc - 0.8 <= t < C + dc:
        c2dot = ((t - (C + dc - 0.8)) / 0.8 * 2) % 1
    if c1p > 0:
        draw_conn(d, CONN[0], c1p, c1dot)
    if c2p > 0:
        draw_conn(d, CONN[1], c2p, c2dot)
    cp = seg(t, D + 0.3, D + 0.8)
    if cp > 0:
        txt = "Một ứng dụng rất đời thường của AI"
        tw = d.textlength(txt, font=F_CHIP)
        pw, ph = tw + 56, 62
        x0, y0 = (W - pw) / 2, 780
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        od.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 31, fill=WHITE, outline=PUR, width=2)
        od.text((W / 2, y0 + ph / 2), txt, font=F_CHIP, fill=PUR, anchor="mm")
        ov.putalpha(ov.getchannel("A").point(lambda a: int(a * cp)))
        base = Image.alpha_composite(base, ov)
        d = ImageDraw.Draw(base)
    for st, du, lines in SUBS:
        if st <= t < st + du:
            bw = max(d.textlength(l, font=F_SUBT) for l in lines) + 80
            bh = 24 + 44 * len(lines)
            x0, y0 = (W - bw) / 2, 1026 - bh
            d.rounded_rectangle([x0, y0, x0 + bw, 1026], 12, fill=(15, 23, 42, 199))
            for j, l in enumerate(lines):
                d.text((W / 2, y0 + 12 + 22 + j * 44), l, font=F_SUBT, fill=WHITE, anchor="mm")
            break
    base.convert("RGB").save(f"{FR}/f{i:04d}.png")

if "--dry" in sys.argv:
    print(json.dumps({"durations": segs, "cue_starts": {"a": A, "b": B, "c": C, "d": D}, "total": T, "frames": N}))
    print("DRY_DONE")
    sys.exit(0)

sil = {}
for name, sec in [("sil02", 0.2), ("sil18", 1.8)]:
    subprocess.run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(sec), "-q:a", "9", f"{MAU}/{name}.mp3"], capture_output=True)
    sil[name] = f"{MAU}/{name}.mp3"
lst = MAU + "/motion_concat.txt"
with open(lst, "w") as f:
    for p in [f"{MAU}/s10a.mp3", sil["sil02"], f"{MAU}/s10b.mp3", sil["sil02"], f"{MAU}/s10c.mp3", sil["sil18"]]:
        f.write(f"file '{p}'\n")
subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{MAU}/motion_audio.mp3"], capture_output=True)
r = subprocess.run([FF, "-y", "-framerate", str(FPS), "-i", f"{FR}/f%04d.png", "-i", f"{MAU}/motion_audio.mp3", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", f"{MAU}/motion_sample_S10.mp4"], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-2000:])
    sys.exit(1)
tl = {"durations": segs, "cue_starts": {"a": A, "b": B, "c": C, "d": D}, "total": T, "frames": N}
with open(MAU + "/motion_s10_timeline.json", "w") as f:
    json.dump(tl, f, indent=2)
print(json.dumps(tl))
print("MOTION_DONE")