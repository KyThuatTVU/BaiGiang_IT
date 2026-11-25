#!/usr/bin/env python3
"""
demo_creative_30s.py — Creative motion-graphics demo 30s
Không dùng ảnh tĩnh; mọi visual vẽ bằng code (animation, counter, particles, beam, UUID reveal).
"""
import sys, os, math, random, subprocess
sys.path.insert(0, r"D:\Edit\Kit\tools")

from PIL import Image, ImageDraw, ImageFont

# ─── CONFIG ──────────────────────────────────────────────────────────────────
PROJECT  = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem"
OUT_DIR  = os.path.join(PROJECT, "mau", "demo_creative")
FFMPEG   = r"C:\Users\ACER\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
FONT_DIR = r"D:\Edit\Kit\assets\fonts"
LOGO_PTH = r"D:\Edit\Kit\assets\brand\logo_an_round.png"

W, H  = 1920, 1080
FPS   = 30
DUR_S = 30.0
N_FRM = int(DUR_S * FPS)  # 900

os.makedirs(os.path.join(OUT_DIR, "audio"),  exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, "frames"), exist_ok=True)

# ─── COLORS ──────────────────────────────────────────────────────────────────
BG   = (8,  12,  28)
CYAN = (0,  212, 255)
RED  = (255, 55,  55)
GRN  = (0,  220, 110)
AMB  = (255, 185,  0)
WHT  = (255, 255, 255)
GRY  = (110, 135, 160)
PURP = (170,  80, 255)

# ─── FONTS ───────────────────────────────────────────────────────────────────
def fnt(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

FB  = "BeVietnamPro-Bold.ttf"
FS  = "BeVietnamPro-SemiBold.ttf"
FM  = "JetBrainsMono-var.ttf"

# ─── EASING / MATH ───────────────────────────────────────────────────────────
def clamp(x, lo=0.0, hi=1.0): return max(lo, min(hi, x))
def lerp(a, b, t): return a + (b - a) * t
def eout(t): return 1 - (1 - clamp(t)) ** 3
def ein(t):  return clamp(t) ** 2
def eio(t):  t = clamp(t); return t * t * (3 - 2 * t)

def rng(f_start, f_end, frame):
    """Return 0..1 for frame in [f_start, f_end]"""
    if frame < f_start: return 0.0
    if frame >= f_end:  return 1.0
    return (frame - f_start) / (f_end - f_start)

def ts(s): return int(s * FPS)   # seconds → frame index

# ─── PARTICLE SYSTEM ─────────────────────────────────────────────────────────
rnd = random.Random(99)
PARTS = [(rnd.uniform(0,W), rnd.uniform(0,H),
          rnd.uniform(-0.4,0.4), rnd.uniform(-0.3,0.3),
          rnd.uniform(1.5, 3.5)) for _ in range(90)]

def draw_particles(img, f, alpha=0.4):
    ov = Image.new("RGBA", (W,H), (0,0,0,0))
    d  = ImageDraw.Draw(ov)
    for px,py,vx,vy,sz in PARTS:
        nx = (px + vx*f) % W
        ny = (py + vy*f) % H
        pulse = 0.5 + 0.5*math.sin(f*0.04 + px*0.01)
        a = int(255*alpha*pulse*0.6)
        r = max(1, int(sz*pulse))
        d.ellipse((nx-r,ny-r,nx+r,ny+r), fill=(*CYAN,a))
    img.alpha_composite(ov)

def draw_grid(d, f, a=0.05):
    """Moving grid lines"""
    al = int(255*a)
    sp = 90
    off = int(f*0.6) % sp
    for x in range(0, W+sp, sp):
        d.line([(x,0),(x,H)], fill=(*CYAN,al), width=1)
    for y in range(-sp, H+sp, sp):
        yy = (y + off) % H
        d.line([(0,yy),(W,yy)], fill=(*CYAN,al), width=1)

def draw_scanline(d, f):
    yy = int(f*1.8) % H
    d.rectangle([(0,yy),(W,yy+2)], fill=(*CYAN,12))

# ─── HELPER SHAPES ───────────────────────────────────────────────────────────
def file_icon(img, cx, cy, sz, label, col, alpha=255):
    ov = Image.new("RGBA",(W,H),(0,0,0,0))
    d  = ImageDraw.Draw(ov)
    r,g,b = col
    fold = sz//4
    # body polygon
    pts = [(cx-sz//2, cy-sz//2+fold),(cx-sz//2+fold, cy-sz//2),
           (cx+sz//2, cy-sz//2),(cx+sz//2, cy+sz//2),(cx-sz//2, cy+sz//2)]
    d.polygon(pts, fill=(r,g,b,int(alpha*0.12)), outline=(r,g,b,alpha))
    # fold triangle
    d.polygon([(cx-sz//2,cy-sz//2+fold),(cx-sz//2+fold,cy-sz//2),
               (cx-sz//2+fold,cy-sz//2+fold)], fill=(r,g,b,int(alpha*0.3)))
    # label
    f2 = fnt(FM, max(10, sz//5))
    bb = d.textbbox((0,0),label,font=f2)
    tw,th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((cx-tw//2, cy-th//2+4), label, font=f2, fill=(r,g,b,alpha))
    img.alpha_composite(ov)

def user_icon(img, cx, cy, sz, label, col, alpha=255):
    ov = Image.new("RGBA",(W,H),(0,0,0,0))
    d  = ImageDraw.Draw(ov)
    r,g,b = col
    hr = sz//4
    # head
    d.ellipse((cx-hr, cy-sz//2, cx+hr, cy-sz//2+hr*2),
              outline=(r,g,b,alpha), width=3, fill=(r,g,b,int(alpha*0.12)))
    # body
    bw = sz//3
    by = cy - sz//2 + hr*2 + 5
    d.rounded_rectangle((cx-bw, by, cx+bw, cy+sz//3),
                        radius=7, outline=(r,g,b,alpha), width=3,
                        fill=(r,g,b,int(alpha*0.12)))
    # name
    f2 = fnt(FS, max(14, sz//6))
    bb = d.textbbox((0,0),label,font=f2)
    tw = bb[2]-bb[0]
    d.text((cx-tw//2, cy+sz//3+6), label, font=f2, fill=(r,g,b,alpha))
    img.alpha_composite(ov)

def glow_circle(d, cx, cy, r, col, alpha):
    for dr in range(r,0,-4):
        a = int(alpha*(dr/r)**2*0.4)
        d.ellipse((cx-dr,cy-dr,cx+dr,cy+dr), fill=(*col,a))
    d.ellipse((cx-r//4,cy-r//4,cx+r//4,cy+r//4), fill=(*col,alpha))

# ─── BRAND BAR ───────────────────────────────────────────────────────────────
def brand_bar(img, f):
    ov = Image.new("RGBA",(W,H),(0,0,0,0))
    d  = ImageDraw.Draw(ov)
    d.rectangle([(0,0),(W,80)], fill=(*BG,230))
    d.line([(0,80),(W,80)], fill=(*CYAN,55), width=1)

    # Logo
    if os.path.exists(LOGO_PTH):
        logo = Image.open(LOGO_PTH).convert("RGBA")
        logo = logo.resize((56,56), Image.LANCZOS)
        ov.paste(logo, (14,12), logo)

    d.text((82,10), "AN TECH ACADEMY",
           font=fnt(FB,24), fill=(*WHT,230))
    d.text((82,43), "Nền tảng kiến thức công nghệ thực chiến",
           font=fnt(FS,15), fill=(*GRY,180))

    # progress bar
    pw = int(W * f/N_FRM)
    d.rectangle([(0,78),(pw,80)], fill=(*CYAN,210))

    img.alpha_composite(ov)

# ─── SUBTITLE ────────────────────────────────────────────────────────────────
CUES = [
    {"id":"c01","say":"Hai người dùng cùng tải lên một tệp tên một chấm j p e g. Điều gì xảy ra?",
     "sub":"Hai user cùng upload file 1.jpg — Điều gì xảy ra?", "t":0.6},
    {"id":"c02","say":"Tệp sau ghi đè tệp trước. Dữ liệu của người dùng A — mất hoàn toàn.",
     "sub":"File sau ghi đè file trước → Dữ liệu User A: MẤT.", "t":5.2},
    {"id":"c03","say":"Với hàng nghìn người dùng đồng thời, xung đột xảy ra mỗi giây.",
     "sub":"1.247 users · 8.934 upload/ngày → 847 xung đột tên file", "t":11.5},
    {"id":"c04","say":"Giải pháp: đặt tên bằng UUID. Mỗi tệp có mã độc nhất, không bao giờ trùng.",
     "sub":"UUID → Mã 128-bit độc nhất — không bao giờ trùng.", "t":18.5},
    {"id":"c05","say":"An Tếch Academy — nền tảng kiến thức công nghệ thực chiến.",
     "sub":"AN TECH ACADEMY · Nền tảng kiến thức công nghệ thực chiến", "t":25.5},
]

def draw_sub(img, t):
    cue = None
    for i,c in enumerate(CUES):
        end = CUES[i+1]["t"] if i+1<len(CUES) else DUR_S
        if c["t"] <= t < end:
            cue = c; break
    if not cue: return
    lt = t - cue["t"]
    al = int(255*clamp(lt/0.35))
    f2 = fnt(FS,30)
    # measure
    tmp = Image.new("RGBA",(10,10))
    td  = ImageDraw.Draw(tmp)
    max_w = W-220
    words = cue["sub"].split()
    lines, cur = [], ""
    for w in words:
        test = cur+(" " if cur else "")+w
        bw = td.textbbox((0,0),test,font=f2)[2]
        if bw>max_w and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    lh=40; th=len(lines)*lh+16
    sy = H-150-th
    ov = Image.new("RGBA",(W,H),(0,0,0,0))
    d  = ImageDraw.Draw(ov)
    d.rounded_rectangle((90,sy-8,W-90,sy+th+8), radius=8,
                        fill=(*BG,int(al*0.88)))
    d.rectangle([(90,sy-8),(96,sy+th+8)], fill=(*CYAN,al))
    for i,line in enumerate(lines):
        d.text((112, sy+i*lh+5), line, font=f2, fill=(*WHT,al))
    img.alpha_composite(ov)

# ─── SCENES ──────────────────────────────────────────────────────────────────

def scene1(img, d, f, t):
    """0–5s: Problem setup — two users, same filename, approaching"""
    lt = t  # 0-5

    # expanding rings from center (problem building)
    for ring in range(4):
        rt = clamp((lt - ring*0.4)/2.5)
        rr = int(rt*350)
        ra = int(70*(1-rt))
        d.ellipse((W//2-rr, H//2+40-rr, W//2+rr, H//2+40+rr),
                 outline=(*CYAN,ra), width=1)

    # Title
    al_title = int(255*eout(clamp(lt/0.6)))
    d.text((W//2-370, 100), "Cùng tên file — Ai thắng?",
           font=fnt(FB,58), fill=(*WHT,al_title))
    d.text((W//2-440, 170), "Hai người dùng upload cùng tên 1.jpg lên cùng thư mục",
           font=fnt(FS,28), fill=(*GRY,al_title))

    # Animated movement of users + files
    UA_TARGET, UB_TARGET = W//2-310, W//2+310
    p = eout(clamp(lt/3.8))
    ua_x = int(lerp(60,  UA_TARGET, p))
    ub_x = int(lerp(W-60,UB_TARGET, p))

    al_icon = int(255*eout(clamp(lt/0.5)))

    user_icon(img, ua_x, H//2-100, 110, "User A", (80,160,255), al_icon)
    file_icon(img, ua_x, H//2+70,   80, "1.jpg",  (80,160,255), al_icon)

    user_icon(img, ub_x, H//2-100, 110, "User B", (255,120,50), al_icon)
    file_icon(img, ub_x, H//2+70,   80, "1.jpg",  (255,120,50), al_icon)

    # speed lines (motion blur feel) when moving fast
    if lt > 1.5:
        sp = clamp((lt-1.5)/2.0)
        for i in range(6):
            lx = ua_x + i*18
            d.line([(lx,H//2+65),(lx+35,H//2+65)], fill=(80,160,255,int(90*sp)), width=2)
            rx = ub_x - i*18 - 35
            d.line([(rx,H//2+65),(rx+35,H//2+65)], fill=(255,120,50,int(90*sp)), width=2)

    # VS badge in center
    vs_a = int(255*eout(clamp((lt-1.0)/0.5)))
    cx, cy = W//2, H//2+20
    d.ellipse((cx-38,cy-38,cx+38,cy+38), fill=(*BG,vs_a), outline=(*AMB,vs_a), width=3)
    d.text((cx-18,cy-22), "VS", font=fnt(FB,38), fill=(*AMB,vs_a))


def scene2(img, d, f, t):
    """5–12s: Collision + data-loss visualization"""
    lt = t - 5.0  # 0-7

    # collision at lt=1.3
    # pre-collision: files moving to center
    p = eout(clamp(lt/1.0))
    ua_x = int(lerp(W//2-310, W//2, p))
    ub_x = int(lerp(W//2+310, W//2, p))

    if lt < 1.6:
        file_icon(img, ua_x, H//2, 90, "1.jpg", (80,160,255), 255)
        file_icon(img, ub_x, H//2, 90, "1.jpg", (255,120,50), 255)

    # COLLISION FLASH (lt 1.0–2.2)
    if 1.0 <= lt <= 2.2:
        fl = clamp((lt-1.0)/0.4)
        fa = int(220*math.sin(fl*math.pi))
        ov = Image.new("RGBA",(W,H),(255,80,40,fa))
        img.alpha_composite(ov)
        # explosion rings
        for ring in range(5):
            rt = clamp((lt-1.0-ring*0.07)/0.7)
            rr = int(rt*350)
            ra = int(200*(1-rt))
            d.ellipse((W//2-rr,H//2-rr,W//2+rr,H//2+rr),
                     outline=(*RED,ra), width=max(1,3-ring))
        # CONFLICT! text
        ctxt_a = int(255*math.sin(fl*math.pi))
        d.text((W//2-220,H//2-70), "CONFLICT!", font=fnt(FB,110),
               fill=(*RED,ctxt_a))

    # post-collision: scatter fragments + warning
    if lt > 1.5:
        post = clamp((lt-1.5)/1.5)
        # file fragments
        angles = [20,80,145,210,270,330]
        for i,ang in enumerate(angles):
            rad = math.radians(ang)
            dist = 60 + i*20
            fx = W//2 + int(dist*post*math.cos(rad))
            fy = H//2 + int(dist*post*math.sin(rad))
            fa = int(220*(1-post*0.85))
            sz = 18-i*2
            d.rectangle((fx-sz,fy-sz,fx+sz,fy+sz), fill=(*RED,fa))

        # WARNING BOX
        wa = int(255*eout(post))
        bx1, bx2, by1, by2 = W//2-480, W//2+480, H//2+120, H//2+210
        d.rounded_rectangle((bx1,by1,bx2,by2), radius=12,
                            fill=(*RED,int(wa*0.12)), outline=(*RED,wa), width=2)
        # pulsing left accent
        pulse_w = int(6+2*math.sin(lt*8))
        d.rounded_rectangle((bx1,by1,bx1+pulse_w,by2), radius=4, fill=(*RED,wa))
        d.text((bx1+20,by1+12), "⚠  Tệp User A bị GHI ĐÈ — Dữ liệu MẤT VĨNH VIỄN",
               font=fnt(FB,46), fill=(*RED,wa))

    # Timeline showing which file won
    if lt > 3.0:
        tl_p = clamp((lt-3.0)/2.0)
        tl_a = int(255*eout(tl_p))
        ty = H//2 - 220
        # Timeline bar
        d.rounded_rectangle((W//2-480,ty,W//2+480,ty+6), radius=3,
                            fill=(*GRY,int(tl_a*0.4)))
        # Event dots
        events = [
            (W//2-350, "User A upload\n1.jpg", (80,160,255)),
            (W//2+120,  "User B upload\n1.jpg (ghi đè)", RED),
            (W//2+350,  "User A's file:\nBIẾN MẤT", RED),
        ]
        for i,(ex,elbl,ecol) in enumerate(events):
            ep = clamp((tl_p - i*0.2)/0.5)
            ea = int(tl_a*ep)
            glow_circle(d, ex, ty+3, 16, ecol, ea)
            lines = elbl.split("\n")
            for li,line in enumerate(lines):
                bb = d.textbbox((0,0),line,font=fnt(FS,20))
                tw = bb[2]-bb[0]
                d.text((ex-tw//2, ty+22+li*26), line, font=fnt(FS,20),
                       fill=(*ecol,ea))


def scene3(img, d, f, t):
    """12–19s: Scale counter — animated numbers"""
    lt = t - 12.0  # 0-7

    # Vignette-dark background, grid of tiny file icons as decoration
    icon_a = int(45*clamp(lt/1.0))
    for row in range(7):
        for col in range(16):
            ix = 30+col*120; iy = 95+row*140
            col_idx = (row+col) % 3
            ic = [RED, AMB, (50,90,180)][col_idx]
            # tiny file dot
            d.rectangle((ix,iy,ix+22,iy+28), outline=(*ic,icon_a), width=1)

    # dark overlay to push background behind
    ov2 = Image.new("RGBA",(W,H),(0,0,0,0))
    gd  = ImageDraw.Draw(ov2)
    for y in range(H):
        gy = abs(y-H//2)/(H//2)
        gd.line([(0,y),(W,y)], fill=(8,12,28,int(160*gy**1.5)))
    for x in range(W):
        gx = abs(x-W//2)/(W//2)
        gd.line([(x,0),(x,H)], fill=(8,12,28,int(100*gx**2)))
    img.alpha_composite(ov2)

    # Title
    tl_a = int(255*eout(clamp(lt/0.6)))
    d.text((W//2-290, 100), "Quy mô vấn đề — Mỗi ngày:", font=fnt(FB,46), fill=(*WHT,tl_a))

    # 4 animated counter rows
    counters = [
        ("Người dùng hoạt động",  1247, CYAN, 250),
        ("File upload / ngày",    8934, AMB,  400),
        ("Xung đột tên file",      847, RED,  550),
        ("Dữ liệu bị mất (MB)",  2341, RED,  700),
    ]
    for i,(lbl,target,col,cy) in enumerate(counters):
        p = eout(clamp((lt-i*0.55)/2.2))
        a = int(255*p)
        val = int(target*eout(clamp((lt-i*0.55)/2.0)))

        # background card
        bx1,bx2 = W//2-520, W//2+520
        d.rounded_rectangle((bx1,cy-14,bx2,cy+90), radius=10,
                            fill=(*BG,int(a*0.9)))

        # label
        d.text((bx1+16,cy), lbl, font=fnt(FS,26), fill=(*GRY,a))

        # animated number (big)
        num_s = f"{val:,}".replace(",",".")
        bb = d.textbbox((0,0),num_s,font=fnt(FB,52))
        tw = bb[2]-bb[0]
        d.text((bx2-tw-16, cy-6), num_s, font=fnt(FB,52), fill=(*col,a))

        # progress bar
        bar_full = bx2-bx1-32
        bar_now  = int(bar_full*p)
        d.rounded_rectangle((bx1+16,cy+58,bx1+16+bar_now,cy+74), radius=4, fill=(*col,a))
        d.rounded_rectangle((bx1+16,cy+58,bx2-16,cy+74), radius=4,
                            outline=(*col,int(a*0.3)), width=1)

    # pulsing warning (lt>5)
    if lt > 4.5:
        wp = clamp((lt-4.5)/0.8)
        wa = int(255*wp)
        pulse_a = int(wa*(0.65+0.35*math.sin(lt*5)))
        wt = "⚠  Không thể phân biệt tệp nào thuộc về ai!"
        bb = d.textbbox((0,0),wt,font=fnt(FB,34))
        tw = bb[2]-bb[0]
        wx = W//2-tw//2
        d.text((wx, H-130), wt, font=fnt(FB,34), fill=(*RED,pulse_a))
        ul_w = int(tw*clamp((lt-5.0)/0.8))
        d.rectangle((wx, H-82, wx+ul_w, H-77), fill=(*RED,pulse_a))


def scene4(img, d, f, t):
    """19–28s: UUID solution — beam transform + before/after code"""
    lt = t - 19.0  # 0-9

    # Green radial glow
    glow_r = int(500*clamp(lt/2.0))
    for r in range(glow_r,0,-30):
        a = int(10*(r/glow_r)**2)
        d.ellipse((W//2-r,H//2-r,W//2+r,H//2+r), fill=(*GRN,a))

    # Title
    ta = int(255*eout(clamp(lt/0.6)))
    d.text((W//2-310,100), "Giải pháp: UUID Renaming", font=fnt(FB,54), fill=(*GRN,ta))
    d.text((W//2-400,168), "Mỗi file nhận mã 128-bit duy nhất — không bao giờ trùng",
           font=fnt(FS,28), fill=(*GRY,ta))

    # === PHASE 1 (lt 0-2.5): show original file ===
    orig_a = int(255*clamp(1.0 - (lt-1.5)/0.8))
    if lt < 2.5:
        file_icon(img, W//2-350, H//2, 110, "1.jpg", AMB, max(0,orig_a))
        d.text((W//2-440, H//2+90), "Tên gốc: 1.jpg", font=fnt(FS,24), fill=(*AMB,max(0,orig_a)))

    # === PHASE 2 (lt 1.5-4.5): transformation beam + spinner ===
    if 1.0 < lt < 5.0:
        bp = clamp((lt-1.0)/3.0)
        ba = int(220*math.sin(bp*math.pi))

        # beam line
        bx_start = W//2 - 290
        bx_end   = int(lerp(bx_start, W//2+290, bp))
        d.line([(bx_start, H//2),(bx_end, H//2)], fill=(*CYAN,ba), width=5)
        # arrowhead
        d.polygon([(bx_end,H//2-14),(bx_end,H//2+14),(bx_end+22,H//2)],
                  fill=(*CYAN,ba))

        # spinning orbit
        cx2,cy2 = W//2, H//2
        for tooth in range(8):
            ang = math.radians(tooth*45 + lt*200)
            tx = cx2+int(44*math.cos(ang))
            ty = cy2+int(44*math.sin(ang))
            d.ellipse((tx-5,ty-5,tx+5,ty+5), fill=(*CYAN,ba))
        d.ellipse((cx2-20,cy2-20,cx2+20,cy2+20), outline=(*CYAN,ba), width=3)

        # "Generating…"
        dots = "." * (int(lt*4) % 4)
        d.text((W//2-110, H//2+65), f"Generating UUID{dots}",
               font=fnt(FM,22), fill=(*CYAN,ba))

    # === PHASE 3 (lt 3.5+): UUID result typed out ===
    if lt > 3.0:
        new_name = "a83f91c2-d45e-7890-b12c-56789abcdef0.jpg"
        rp = eout(clamp((lt-3.0)/2.0))
        chars  = int(len(new_name)*rp)
        shown  = new_name[:chars]
        rfa    = int(255*rp)

        file_icon(img, W//2+380, H//2, 110, ".jpg", GRN, rfa)

        # UUID string character-by-character
        d.text((W//2+100, H//2+88), shown, font=fnt(FM,22), fill=(*GRN,rfa))
        # cursor blink
        if chars < len(new_name) and int(lt*4)%2==0:
            cx3 = W//2+100 + chars*13
            d.rectangle((cx3,H//2+88,cx3+2,H//2+112), fill=(*GRN,255))

        # UNIQUE badge
        if rp > 0.75:
            ba2 = int(255*clamp((rp-0.75)/0.25))
            bx3,by3 = W//2+350, H//2-80
            d.rounded_rectangle((bx3-72,by3-16,bx3+72,by3+16),
                               radius=14, fill=(*GRN,int(ba2*0.2)),
                               outline=(*GRN,ba2), width=2)
            d.text((bx3-56,by3-11), "✓  UNIQUE", font=fnt(FB,22), fill=(*GRN,ba2))

    # === Before/After code card (lt > 5) ===
    if lt > 5.0:
        cp = eout(clamp((lt-5.0)/1.5))
        ca = int(255*cp)

        # BEFORE card
        bk1_x1,bk1_y1 = W//2-520, H//2+140
        bk1_x2,bk1_y2 = W//2-20,  H//2+320
        d.rounded_rectangle((bk1_x1,bk1_y1,bk1_x2,bk1_y2), radius=10,
                            fill=(*RED,int(ca*0.1)), outline=(*RED,ca), width=2)
        d.text((bk1_x1+12,bk1_y1+8),  "✗  Trước (không an toàn)",font=fnt(FB,22),fill=(*RED,ca))
        d.text((bk1_x1+12,bk1_y1+42), "$fn = $_FILES['f']['name'];",font=fnt(FM,18),fill=(*AMB,ca))
        d.text((bk1_x1+12,bk1_y1+68), "// User A → 1.jpg",         font=fnt(FM,18),fill=(*GRY,ca))
        d.text((bk1_x1+12,bk1_y1+94), "// User B → 1.jpg ← GHI ĐÈ!", font=fnt(FM,18),fill=(*RED,ca))

        # AFTER card
        bk2_x1 = W//2+20
        d.rounded_rectangle((bk2_x1,bk1_y1,bk2_x1+500,bk1_y2), radius=10,
                            fill=(*GRN,int(ca*0.08)), outline=(*GRN,ca), width=2)
        d.text((bk2_x1+12,bk1_y1+8),  "✓  Sau (an toàn)",             font=fnt(FB,22),fill=(*GRN,ca))
        d.text((bk2_x1+12,bk1_y1+42), "$n = bin2hex(random_bytes(16));",font=fnt(FM,18),fill=(*CYAN,ca))
        d.text((bk2_x1+12,bk1_y1+68), "// User A → a83f91c2….jpg",    font=fnt(FM,18),fill=(*GRN,ca))
        d.text((bk2_x1+12,bk1_y1+94), "// User B → d71b42e9….jpg ✓",  font=fnt(FM,18),fill=(*GRN,ca))


def scene5(img, d, f, t):
    """28–30s: Outro brand"""
    lt = t - 28.0
    # converging particles
    pa = int(200*eout(clamp(lt/0.6)))
    for px,py,vx,vy,sz in PARTS[:40]:
        cx4 = int(W//2 + (px-W//2)*(1-eout(clamp(lt/1.5))))
        cy4 = int(H//2 + (py-H//2)*(1-eout(clamp(lt/1.5))))
        r = max(1,int(sz))
        d.ellipse((cx4-r,cy4-r,cx4+r,cy4+r), fill=(*CYAN,int(pa*0.5)))

    fa = int(255*eout(clamp(lt/0.5)))
    brand = "AN TECH ACADEMY"
    bb = d.textbbox((0,0),brand,font=fnt(FB,80))
    tw = bb[2]-bb[0]
    d.text((W//2-tw//2, H//2-80), brand, font=fnt(FB,80), fill=(*CYAN,fa))

    tag = "Nền tảng kiến thức công nghệ thực chiến"
    bb2 = d.textbbox((0,0),tag,font=fnt(FS,34))
    tw2 = bb2[2]-bb2[0]
    d.text((W//2-tw2//2, H//2+20), tag, font=fnt(FS,34), fill=(*WHT,fa))

    # animated underline
    max_w = max(tw,tw2)
    ul_w  = int(max_w*clamp(lt/1.2))
    d.rectangle((W//2-max_w//2, H//2+68, W//2-max_w//2+ul_w, H//2+73),
               fill=(*CYAN,fa))

# ─── MASTER FRAME RENDER ─────────────────────────────────────────────────────
def render(f):
    t = f / FPS
    img = Image.new("RGBA",(W,H),(*BG,255))
    d   = ImageDraw.Draw(img)

    draw_grid(d, f)
    draw_particles(img, f)
    draw_scanline(d, f)

    if   t < 5.0:  scene1(img,d,f,t)
    elif t < 12.0: scene2(img,d,f,t)
    elif t < 19.0: scene3(img,d,f,t)
    elif t < 28.0: scene4(img,d,f,t)
    else:          scene5(img,d,f,t)

    brand_bar(img,f)
    draw_sub(img,t)
    return img.convert("RGB")

# ─── AUDIO ───────────────────────────────────────────────────────────────────
def synth_audio():
    import tts_vieneu
    for c in CUES:
        out = os.path.join(OUT_DIR,"audio",f"{c['id']}.wav")
        if not os.path.exists(out):
            tts_vieneu.synth(c["say"], out, retries=2)
            print(f"  TTS: {c['id']} → {out}")
        else:
            print(f"  TTS cached: {c['id']}")

def build_audio():
    silent = os.path.join(OUT_DIR,"audio","silent30.wav")
    subprocess.run([FFMPEG,"-y","-f","lavfi","-i","anullsrc=r=48000:cl=mono",
                   "-t","30", silent], capture_output=True)

    n = len(CUES)
    cmd = [FFMPEG,"-y","-i",silent]
    for c in CUES:
        cmd += ["-i", os.path.join(OUT_DIR,"audio",f"{c['id']}.wav")]

    flt = ""
    for i,c in enumerate(CUES):
        ms = int(c["t"]*1000)
        flt += f"[{i+1}:a]adelay={ms}|{ms}[da{i}];"
    mix_in = "[0:a]"+"".join(f"[da{i}]" for i in range(n))
    flt += f"{mix_in}amix=inputs={n+1}:duration=first:normalize=0[aout]"

    mixed = os.path.join(OUT_DIR,"audio","mixed.wav")
    cmd  += ["-filter_complex",flt,"-map","[aout]","-t","30", mixed]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print("Mix error:", r.stderr.decode()[-400:])

    normed = os.path.join(OUT_DIR,"audio","normed.wav")
    subprocess.run([FFMPEG,"-y","-i",mixed,"-af","loudnorm=I=-14:TP=-1:LRA=7",
                   normed], capture_output=True)
    return normed

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("=== CREATIVE DEMO 30S ===\n")

    print("[1] TTS audio…")
    synth_audio()

    print("[2] Build audio timeline…")
    normed = build_audio()

    print("[3] Render frames…")
    frames_dir = os.path.join(OUT_DIR,"frames")
    for f in range(N_FRM):
        frame_img = render(f)
        frame_img.save(os.path.join(frames_dir,f"f{f:05d}.jpg"), quality=92)
        if f % 90 == 0:
            print(f"  {f}/{N_FRM}  t={f/FPS:.1f}s")

    print("[4] Encode video…")
    raw_mp4 = os.path.join(OUT_DIR,"raw.mp4")
    subprocess.run([
        FFMPEG,"-y","-framerate","30",
        "-i", os.path.join(frames_dir,"f%05d.jpg"),
        "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
        raw_mp4
    ], capture_output=True)

    print("[5] Mux audio+video…")
    final = os.path.join(OUT_DIR,"demo_creative_30s.mp4")
    r = subprocess.run([
        FFMPEG,"-y","-i",raw_mp4,"-i",normed,
        "-c:v","copy","-c:a","aac","-b:a","192k","-t","30",
        final
    ], capture_output=True)
    print("Mux exit:", r.returncode)
    if r.returncode == 0:
        print(f"\n✅ DONE → {final}")
    else:
        print("Error:", r.stderr.decode()[-300:])

if __name__ == "__main__":
    main()
