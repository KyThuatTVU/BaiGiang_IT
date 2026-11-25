# -*- coding: utf-8 -*-
"""Video mẫu Cổng B — 3 cảnh S01, S02, S06 (~32 s).
Voice NamMinh +18 %, nhân vật Thầy Minh, nét vẽ tay, SFX tổng hợp, phụ đề burn + SRT.
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw

sys.path.insert(0, "D:/Edit/Baigiang_Apriori/tools")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import *            # noqa: F401,F403
from char_teacher import draw_teacher, mouth_for
import char_teacher

PROJ = "D:/Edit/Baigiang_dongbodulieu"
MAU = PROJ + "/mau"
AUD = MAU + "/audio"
SFXD = MAU + "/sfx"
SVID = MAU + "/scenes"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
SAMPLE = ["S01", "S02", "S06"]
TEAL = (15, 157, 143, 255)
GAP, TAIL, XF = 0.22, 1.10, 0.30
SUB_W = 1100

for d_ in (SVID, SFXD):
    os.makedirs(d_, exist_ok=True)

MAN = json.load(open(PROJ + "/manifest.json", encoding="utf-8"))
STATE = json.load(open(MAU + "/tts_state.json", encoding="utf-8"))

# ---------------- timeline ----------------
SC = {}
for sid in SAMPLE:
    cues = [c for c in MAN if c["scene"] == sid]
    starts, durs, t = [], [], 0.0
    for i, c in enumerate(cues):
        if i:
            t += GAP
        starts.append(t)
        durs.append(STATE[c["id"]]["dur"])
        t += durs[-1]
    SC[sid] = dict(cues=cues, starts=starts, durs=durs, dur=t + TAIL)

GSTART = {}
t = 0.0
for sid in SAMPLE:
    GSTART[sid] = t
    t += SC[sid]["dur"] - XF
TOTAL = t + XF

def speak(t, sid):
    s = SC[sid]
    return any(a <= t < a + d for a, d in zip(s["starts"], s["durs"]))

def at(sid, frac):
    return SC[sid]["dur"] * frac

def phrase_t(sid, cue_i, sub, offset=0.0):
    """Thời điểm tương đối trong cảnh ứng với một cụm từ của cue (ước theo ký tự)."""
    s = SC[sid]
    text = s["cues"][cue_i]["text"]
    i = text.find(sub)
    if i < 0:
        return s["starts"][cue_i] + offset
    return s["starts"][cue_i] + s["durs"][cue_i] * (i / len(text)) + offset

# ---------------- subtitles ----------------
def sub_chunks(text):
    # cắt theo câu/mệnh đề để phụ đề không bắt đầu giữa cụm từ
    units = []
    for part in re.split(r"(?<=[.!?])\s+", text):
        if len(part) <= 90:
            units.append(part)
            continue
        cur = ""
        for s in re.split(r"(?<=,)\s+", part):
            t_ = (cur + " " + s).strip()
            if cur and len(t_) > 90:
                units.append(cur)
                cur = s
            else:
                cur = t_
        if cur:
            units.append(cur)
    chunks, cur = [], ""
    for u in units:
        t_ = (cur + " " + u).strip()
        if cur and (len(t_) > 90 or len(wrap(t_, F_SUB, SUB_W)) > 2):
            chunks.append(cur)
            cur = u
        else:
            cur = t_
    if cur:
        chunks.append(cur)
    if len(chunks) > 1 and len(chunks[-1]) < 25:
        chunks[-1] = chunks[-2] + " " + chunks[-1]
        chunks.pop(-2)
    return [wrap(c, F_SUB, SUB_W) for c in chunks]

def sub_segments():
    segs = []
    for sid in SAMPLE:
        s = SC[sid]
        for c, st, du in zip(s["cues"], s["starts"], s["durs"]):
            chunks = sub_chunks(c["text"])
            weights = [sum(len(x) for x in ch) for ch in chunks]
            tot = sum(weights)
            acc = 0
            for ch, w_ in zip(chunks, weights):
                a = st + du * acc / tot
                acc += w_
                b = st + du * acc / tot
                segs.append((GSTART[sid] + a, GSTART[sid] + b, ch))
    return segs

SEGS = sub_segments()

def sub_at(g):
    for a, b, ch in SEGS:
        if a <= g < b:
            return ch
    return None

def sub_band(d, lines):
    bw = max(rich_width(l, F_SUB) for l in lines) + 64
    bh = 16 + 42 * len(lines)
    x1 = 920 + bw / 2
    y1 = 1030
    y0 = y1 - bh
    d.rounded_rectangle([x1 - bw, y0, x1, y1], 12, fill=(11, 42, 91, 238))
    for j, l in enumerate(lines):
        draw_rich(d, (x1 - bw / 2, y0 + 10 + 21 + j * 42), l, F_SUB, WHITE, "mm")

def write_srt(path):
    fmt = lambda s: "%02d:%02d:%02d,%03d" % (int(s // 3600), int(s % 3600 // 60),
                                             int(s % 60), int(round((s % 1) * 1000)) % 1000)
    out = []
    for i, (a, b, ch) in enumerate(SEGS, 1):
        out.append(f"{i}\n{fmt(a)} --> {fmt(b)}\n" + "\n".join(ch) + "\n")
    open(path, "w", encoding="utf-8").write("\n".join(out))

# ---------------- S01 ----------------
WM = None
KICK = None
TAG = None

def setup_s01():
    global WM, KICK, TAG
    WM = Image.new("RGBA", (1000, 120), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(WM), (500, 60), "AN TECH ACADEMY", F_WM, NAVY, "mm")
    KICK = Image.new("RGBA", (1000, 50), (0, 0, 0, 0))
    dk = ImageDraw.Draw(KICK)
    txt = "BÀI GIẢNG CÔNG NGHỆ"
    fk = font("BeVietnamPro-SemiBold.ttf", 24)
    wd = sum(dk.textlength(ch, font=fk) + 3.5 for ch in txt)
    draw_tracked(dk, ((1000 - wd) / 2, 25), txt, fk, BLUE, 3.5)
    TAG = Image.new("RGBA", (1000, 60), (0, 0, 0, 0))
    draw_rich(ImageDraw.Draw(TAG), (500, 30), "Học công nghệ, làm chủ tương lai",
              F_BODY, MUT, "mm")

def render_S01(t):
    base = bg_canvas()
    d = ImageDraw.Draw(base)
    p1 = seg(t, 0.10, 0.55)
    paste_sprite(base, KICK, 760, 328, p1, "mt")
    paste_sprite(base, WM, 760, 432, seg(t, 0.05, 0.50), "mm")
    # gạch chân vàng vẽ tay 0,55 s
    u = seg(t, 1.00, 1.55)
    if u > 0:
        x0, x1, y = 385, 1135, 500
        d.line([x0, y, x0 + (x1 - x0) * u, y], fill=AMBER, width=6)
    paste_sprite(base, TAG, 760, 554, seg(t, 0.55, 0.95), "mm")
    if t > 0.30:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pose = "wave" if t < 3.4 else ("G" if speak(t, "S01") and t > 6.0 else "D")
        draw_teacher(ov, t, pose=pose, mouth=mouth_for(t, speak(t, "S01")))
        a = seg(t, 0.30, 0.75)
        if a < 1:
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * a)))
        base.alpha_composite(ov)
    return base

# ---------------- S02 ----------------
CARD_X = [96, 556, 1016]
CARD_Y = 300
CARD_W, CARD_H = 420, 500
CARDS = {}
BANNER2 = None

def setup_s02():
    global BANNER2
    BANNER2 = sp_banner("Ba trạng thái, một bảng ghi chú", "Tình huống: dữ liệu chưa đồng bộ")
    for letter in "ABC":
        im = card(CARD_W, CARD_H)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, CARD_W, 46], 18, fill=(240, 246, 253, 255))
        d.rectangle([0, 28, CARD_W, 46], fill=(240, 246, 253, 255))
        for i, c in enumerate([(226, 116, 106), (235, 190, 110), (140, 200, 160)]):
            d.ellipse([18 + i * 22, 17, 28 + i * 22, 27], fill=c + (255,))
        d.rounded_rectangle([86, 12, CARD_W - 62, 36], 12, fill=WHITE)
        d.text((98, 24), "note.edu.vn/bang-nhom", font=font("BeVietnamPro-Regular.ttf", 17),
               fill=(120, 136, 160, 255), anchor="lm")
        d.ellipse([CARD_W - 48, 9, CARD_W - 12, 39], fill=NAVY)
        d.text((CARD_W - 30, 24), letter, font=font("PlusJakartaSans-var.ttf", 20, 800),
               fill=WHITE, anchor="mm")
        d.text((34, 82), "Bảng ghi chú nhóm", font=font("BeVietnamPro-SemiBold.ttf", 25),
               fill=INK, anchor="lm")
        d.text((34, 114), "Ghi chú chung của nhóm", font=font("BeVietnamPro-Regular.ttf", 19),
               fill=MUT, anchor="lm")
        for i in range(3):
            d.rounded_rectangle([34, 150 + i * 26, CARD_W - 40 - i * 30, 162 + i * 26],
                                6, fill=(226, 235, 247, 255))
        d.line([30, 244, CARD_W - 30, 244], fill=BORDER, width=2)
        txt = "DEADLINE"
        fk = font("BeVietnamPro-SemiBold.ttf", 19)
        L = sum(d.textlength(ch, font=fk) + 3 for ch in txt)
        draw_tracked(d, (34, 270), txt, fk, MUT, 3)
        CARDS[letter] = im

def deadline_block(base, x0, y0, letter, t):
    d = ImageDraw.Draw(base)
    tA = phrase_t("S02", 0, "Bạn A vừa cập nhật")
    tB = phrase_t("S02", 0, "nhưng bạn B vẫn thấy")
    tC = phrase_t("S02", 0, "còn bạn C phải tải lại")
    new = letter == "A" and t >= tA
    val = "20h" if new else "18h"
    fv = font("PlusJakartaSans-var.ttf", 44, 800)
    if new:
        fl = seg(t, tA, tA + 0.35)
        if fl > 0:
            d.rounded_rectangle([x0 + 28, y0 + 288, x0 + 28 + 132 * fl, y0 + 348], 10,
                                fill=(252, 239, 210, 255))
    d.text((x0 + 34, y0 + 318), val, font=fv,
           fill=(INK if letter != "B" and letter != "C" else (154, 167, 186, 255)), anchor="lm")
    if new:
        chip = sp_chip("Vừa cập nhật", GREEN, WHITE, 20)
        a = seg(t, tA + 0.1, tA + 0.4)
        if a > 0:
            if a < 1:
                chip.putalpha(chip.getchannel("A").point(lambda v: int(v * a)))
            base.alpha_composite(chip, (x0 + 30, y0 + 372))
    elif letter == "B" and t >= tB:
        p = 1.0
        ph = (t - tB) % 0.8
        if ph < 0.25:
            p = 1.0 + 0.10 * math.sin(math.pi * ph / 0.25)
        chip = sp_chip("Dữ liệu cũ", RED, WHITE, 20)
        if p != 1.0:
            chip = chip.resize((int(chip.size[0] * p), int(chip.size[1] * p)), Image.LANCZOS)
        base.alpha_composite(chip, (x0 + 30, y0 + 372))
    elif letter == "C":
        chip = sp_chip("Chưa cập nhật", (140, 154, 173, 255), WHITE, 20)
        base.alpha_composite(chip, (x0 + 30, y0 + 372))
        if t >= tC:
            p = seg(t, tC, tC + 0.3)
            bw, bh = 246, 54
            if p > 0:
                ov = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
                do = ImageDraw.Draw(ov)
                do.rounded_rectangle([0, 0, bw - 1, bh - 1], 12, fill=WHITE, outline=NAVY, width=2)
                ic = sp_icon("refresh-cw", BLUE, 24)
                ov.paste(ic, (14, 15), ic)
                do.text((48, bh / 2), "Tải lại trang", font=font("BeVietnamPro-SemiBold.ttf", 20),
                        fill=NAVY, anchor="lm")
                if p < 1:
                    ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
                base.alpha_composite(ov, (x0 + 30, y0 + 430))

def render_S02(t):
    base = bg_canvas()
    brand_mark(base)
    paste_sprite(base, BANNER2, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    for letter, t0 in zip("ABC", (0.55, 0.67, 0.79)):
        p = seg(t, t0, t0 + 0.25)
        if p > 0:
            x = CARD_X["ABC".index(letter)]
            paste_sprite(base, CARDS[letter], x, CARD_Y, p, "tl")
            deadline_block(base, x, CARD_Y, letter, t)
    if t > 0.30:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_teacher(ov, t, pose="C", mouth=mouth_for(t, speak(t, "S02")))
        a = seg(t, 0.30, 0.75)
        if a < 1:
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * a)))
        base.alpha_composite(ov)
    return base

# ---------------- S06 ----------------
BANNER6 = None
NODES = {}
ARROW_A = ((432, 590), (812, 590))
ARROW_B = ((1092, 548), (1272, 438))
ARROW_C = ((1092, 622), (1272, 706))

def node_card(icon, title, sub, w, h):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    ic = sp_icon(icon, BLUE, 44)
    im.paste(ic, (24, 22), ic)
    d.text((24, 86), title, font=font("BeVietnamPro-SemiBold.ttf", 24), fill=INK, anchor="lm")
    if sub:
        d.text((24, 118), sub, font=font("BeVietnamPro-Regular.ttf", 18), fill=MUT, anchor="lm")
    return im

def setup_s06():
    global BANNER6
    BANNER6 = sp_banner("Luồng đồng bộ", "A thay đổi → Server xử lý → B và C cập nhật")
    NODES["A"] = node_card("globe", "A · Trình duyệt", "bảng ghi chú", 250, 150)
    NODES["S"] = node_card("server", "Server", "xử lý & phát sự kiện", 280, 190)
    NODES["B"] = node_card("globe", "B · Trình duyệt", "đang mở ứng dụng", 260, 140)
    NODES["C"] = node_card("smartphone", "C · Điện thoại", "đang mở ứng dụng", 260, 140)

def render_S06(t):
    base = bg_canvas()
    brand_mark(base)
    paste_sprite(base, BANNER6, 1000, 78, seg(t, 0.0, 0.3), "mt")
    d = ImageDraw.Draw(base)
    pos = {"A": (170, 515), "S": (812, 495), "B": (1272, 368), "C": (1272, 636)}
    for k, t0 in [("A", 0.20), ("S", 0.45), ("B", 0.70), ("C", 0.95)]:
        paste_sprite(base, NODES[k], pos[k][0], pos[k][1], seg(t, t0, t0 + 0.25), "tl")

    s = SC["S06"]
    t_arrow = 1.05
    t_dot1 = 1.70
    t_ring = 2.55
    t_arrow2 = 3.60
    t_dot2 = 4.25
    t_sync = s["starts"][1] - 0.15

    p1 = seg(t, t_arrow, t_arrow + 0.6)
    dq1 = None
    if t_dot1 <= t < t_dot1 + 0.9:
        dq1 = (t - t_dot1) / 0.9
    elif t >= t_dot1 + 0.9:
        dq1 = 1.0
    draw_conn(d, *ARROW_A[0], *ARROW_A[1], p1, BLUE, dq1, 5)

    if t_ring <= t < t_ring + 1.0:
        ph = (t - t_ring) / 1.0
        for k in range(2):
            q = ph - k * 0.25
            if 0 < q < 1:
                r = 96 + 52 * ease(q)
                col = (47, 111, 208, 255) if q < 0.5 else (15, 157, 143, 255)
                d.ellipse([952 - r, 590 - r, 952 + r, 590 + r], outline=col, width=5)

    p2 = seg(t, t_arrow2, t_arrow2 + 0.6)
    dqB = dqC = None
    if t_dot2 <= t < t_dot2 + 0.9:
        dqB = (t - t_dot2) / 0.9
    elif t >= t_dot2 + 0.9:
        dqB = 1.0
    if t_dot2 + 0.2 <= t < t_dot2 + 1.1:
        dqC = (t - t_dot2 - 0.2) / 0.9
    elif t >= t_dot2 + 1.1:
        dqC = 1.0
    draw_conn(d, *ARROW_B[0], *ARROW_B[1], p2, TEAL, dqB, 5)
    draw_conn(d, *ARROW_C[0], *ARROW_C[1], p2, TEAL, dqC, 5)

    if t >= t_sync:
        p = seg(t, t_sync, t_sync + 0.35)
        for k in ("B", "C"):
            x, y = pos[k]
            ov = Image.new("RGBA", (260, 140), (0, 0, 0, 0))
            do = ImageDraw.Draw(ov)
            do.rounded_rectangle([1, 1, 258, 138], 18, outline=TEAL, width=4)
            ic = sp_icon("circle-check", TEAL, 26)
            ov.paste(ic, (204, 20), ic)
            if p < 1:
                ov.putalpha(ov.getchannel("A").point(lambda v: int(v * p)))
            base.alpha_composite(ov, (x, y))
        x, y = pos["A"]
        chip = sp_chip("Đã gửi", BLUE, WHITE, 18)
        if p > 0:
            base.alpha_composite(chip, (x + 137, y + 14))

    if t > 0.30:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_teacher(ov, t, pose="C", mouth=mouth_for(t, speak(t, "S06")))
        a = seg(t, 0.30, 0.75)
        if a < 1:
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * a)))
        base.alpha_composite(ov)
    return base

RENDERERS = {"S01": render_S01, "S02": render_S02, "S06": render_S06}

# ---------------- frame encode ----------------
def encode_scene(sid):
    setup = {"S01": setup_s01, "S02": setup_s02, "S06": setup_s06}[sid]
    setup()
    dur = SC[sid]["dur"]
    N = int(round(dur * FPS))
    out = f"{SVID}/{sid}.mp4"
    cmd = [FF, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-an", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    for f in range(N):
        t = f / FPS
        im = RENDERERS[sid](t)
        g = GSTART[sid] + t
        ch = sub_at(g)
        if ch:
            sub_band(ImageDraw.Draw(im), ch)
        p.stdin.write(im.convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    print(f"{sid} frames={N} dur={dur:.2f}s rc={p.returncode}", flush=True)

def preview():
    for sid in SAMPLE:
        {"S01": setup_s01, "S02": setup_s02, "S06": setup_s06}[sid]()
    for g in (0.6, 2.0, 5.0, 9.5, 13.2, 17.0, 21.0, 24.0, 28.0, 31.5):
        im = None
        for sid in SAMPLE:
            if GSTART[sid] <= g < GSTART[sid] + SC[sid]["dur"]:
                im = RENDERERS[sid](g - GSTART[sid])
                break
        if im is None:
            continue
        ch = sub_at(g)
        if ch:
            sub_band(ImageDraw.Draw(im), ch)
        im.convert("RGB").save(f"{MAU}/preview_{g:05.1f}.png")
    print("PREVIEW_DONE", flush=True)

if __name__ == "__main__":
    if "--preview" in sys.argv:
        preview()
    else:
        write_srt(MAU + "/sample_congB.srt")
        for sid in SAMPLE:
            encode_scene(sid)
        print("SCENES_DONE total", round(TOTAL, 2), flush=True)
