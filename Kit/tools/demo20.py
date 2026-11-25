# -*- coding: utf-8 -*-
"""Demo 20s: DEMO_MODE=phonetic (một giọng Việt, phiên âm Việt) hoặc ml (song ngữ).

Dùng: python demo20.py            (mặc định v6)
      DEMO_MODE=ml python demo20.py
"""
import json, math, os, re, subprocess, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import FULL, FF, W, H, FPS, font, tw, draw_rich
from prep_icons import icon_rgba
import sfx

OUT = FULL + "/demo20"
V_VI = "vi-VN-NamMinhNeural"
V_ML = "en-US-AndrewMultilingualNeural"
MODE = os.environ.get("DEMO_MODE", "phonetic")
TAG = {"phonetic": "v6", "ml": "v7", "plain": "v8"}[MODE]
AUD = OUT + {"phonetic": "/audio", "ml": "/audio_ml", "plain": "/audio_plain"}[MODE]
FR = OUT + {"phonetic": "/frames", "ml": "/frames_ml", "plain": "/frames_plain"}[MODE]
SR = sfx.SR

# Thuật ngữ Anh viết phiên âm Việt để chính giọng Việt đọc đúng chuẩn IT:
# API → "ây-pi-ai", client → "cờ-lai-ừn", server → "sờ-vờ",
# request → "ri-quét", response → "ri-xờ-pon", endpoint → "en-đờ-poi",
# HTTP → "hát-ti-ti-pi", JSON → "giây-sần".
# id, text, pause_after
SEGS_PHONETIC = [
    ("s01", "Ây-pi-ai.", 0.22),
    ("s02", "Giao diện lập trình ứng dụng: hợp đồng giao tiếp giữa hai hệ thống độc lập.", 0.30),
    ("s03", "Phía cờ-lai-ừn", 0.10),
    ("s04", "gửi ri-quét", 0.08),
    ("s05", "đến sờ-vờ", 0.08),
    ("s06", "và nhận lại", 0.10),
    ("s07", "ri-xờ-pon.", 0.36),
    ("s08", "Toàn bộ luồng đi qua", 0.08),
    ("s09", "en-đờ-poi", 0.12),
    ("s10", "được chuẩn hoá bằng", 0.12),
    ("s11", "hát-ti-ti-pi,", 0.20),
    ("s12", "và giây-sần.", 0.34),
    ("s13", "Đó là một vòng gọi API trọn vẹn.", 0.30),
]

# Song ngữ: giữ chữ Anh gốc, một giọng đọc được cả hai thứ tiếng
SEGS_ML = [
    ("s01", "API.", 0.22),
    ("s02", "Giao diện lập trình ứng dụng: hợp đồng giao tiếp giữa hai hệ thống độc lập.", 0.30),
    ("s03", "Client", 0.10),
    ("s04", "gửi request đến", 0.08),
    ("s05", "server", 0.08),
    ("s06", "và nhận lại", 0.10),
    ("s07", "response.", 0.36),
    ("s08", "Toàn bộ luồng đi qua", 0.08),
    ("s09", "endpoint", 0.12),
    ("s10", "được chuẩn hoá bằng", 0.12),
    ("s11", "giao thức HTTP,", 0.20),
    ("s12", "và dữ liệu JSON.", 0.34),
    ("s13", "Đó là một vòng gọi API trọn vẹn.", 0.30),
]

SEGS_PLAIN = [
    ("s01", "API.", 0.22),
    ("s02", "Giao diện lập trình ứng dụng: hợp đồng giao tiếp giữa hai hệ thống độc lập.", 0.30),
    ("s03", "Client", 0.10),
    ("s04", "gửi request đến", 0.08),
    ("s05", "server", 0.08),
    ("s06", "và nhận lại", 0.10),
    ("s07", "ri-spon.", 0.36),
    ("s08", "Toàn bộ luồng đi qua", 0.08),
    ("s09", "endpoint", 0.12),
    ("s10", "được chuẩn hoá bằng", 0.12),
    ("s11", "giao thức HTTP,", 0.20),
    ("s12", "và dữ liệu JSON.", 0.34),
    ("s13", "Đó là một vòng gọi API trọn vẹn.", 0.30),
]

SEGS = {"phonetic": SEGS_PHONETIC, "ml": SEGS_ML, "plain": SEGS_PLAIN}[MODE]
VOICE = V_VI if MODE in ("phonetic", "plain") else V_ML
RATE = "+12%" if MODE in ("phonetic", "plain") else "+8%"
STYLE = {"phonetic": "V6 · VIỆT NGỮ", "ml": "V7 · SONG NGỮ",
         "plain": "V8 · CHỮ ANH"}[MODE]

# ---------- palette ----------
INK_BG = (10, 16, 28)
CARD = (20, 30, 52)
CARD_HI = (255, 255, 255, 18)
TXT = (236, 241, 249)
MUT = (148, 163, 184)
CYAN = (34, 211, 238)
VIOLET = (139, 92, 246)
EMER = (52, 211, 153)
AMBER = (245, 158, 11)
GRIDC = (255, 255, 255, 12)


def dur(p):
    r = subprocess.run([FF, "-i", p, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)


def synth(seg):
    sid, text, _ = seg
    p = f"{AUD}/{sid}.mp3"
    if os.path.exists(p) and os.path.getsize(p) > 1200:
        return p
    voice = VOICE
    rate = RATE
    for rnd in range(7):
        if rnd:
            time.sleep(10)
        tmp = f"{AUD}/_raw_{sid}.mp3"
        if os.path.exists(tmp):
            os.remove(tmp)
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", voice,
                            f"--rate={rate}", "--text", text, "--write-media", tmp],
                           capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if os.path.exists(tmp) and os.path.getsize(tmp) > 1200 and (dur(tmp) or 0) > 0.25:
            os.replace(tmp, p)
            print(f"TTS {sid} ok {dur(p):.2f}s", flush=True)
            return p
        print(f"TTS {sid} miss r{rnd}", flush=True)
    raise SystemExit("TTS giveup " + sid)


def decode(path):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR), "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("decode fail " + path)
    x = np.frombuffer(r.stdout, dtype="<f4").astype(np.float64)
    # Edge chèn ~1s lặng cuối: cắt về đúng khoảng có tiếng + đệm nhỏ
    w = 441
    if len(x) > w * 3:
        rms = np.array([np.sqrt((x[i:i + w] ** 2).mean())
                        for i in range(0, len(x) - w + 1, w)])
        thr = max(0.006, rms.max() * 0.035)
        idx = np.nonzero(rms > thr)[0]
        if len(idx):
            a = max(0, idx[0] * w - int(0.06 * SR))
            b = min(len(x), (idx[-1] + 1) * w + int(0.10 * SR))
            x = x[a:b]
    return x


# ---------- static background ----------
_BG = None


def bg():
    global _BG
    if _BG is not None:
        return _BG.copy()
    top = np.array([7, 12, 22], dtype=np.float32)
    bot = np.array([13, 21, 38], dtype=np.float32)
    g = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    arr = (top[None, :] * (1 - g) + bot[None, :] * g).astype(np.uint8)
    arr = np.repeat(arr[:, None, :], W, axis=1)
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(gl)
    for cx, cy, r, col, a in ((960, 500, 520, VIOLET, 46), (400, 540, 380, CYAN, 30),
                              (1520, 540, 380, EMER, 26)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (a,))
    gl = gl.filter(ImageFilter.GaussianBlur(120))
    im.alpha_composite(gl)
    # lưới vẽ trên lớp trong suốt rồi composite — ImageDraw ghi alpha thô, không blend
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dg = ImageDraw.Draw(g)
    for x in range(0, W, 120):
        dg.line([x, 0, x, H], fill=(255, 255, 255, 8), width=1)
    for y in range(0, H, 120):
        dg.line([0, y, W, y], fill=(255, 255, 255, 8), width=1)
    for x in range(60, W, 120):
        for y in range(60, H, 120):
            dg.point((x, y), fill=(255, 255, 255, 20))
    im.alpha_composite(g)
    # viền tối
    vg = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(vg)
    dv.rectangle([0, 0, W, H], fill=255)
    dv.ellipse([-260, -260, W + 260, H + 260], fill=0)
    vg = vg.filter(ImageFilter.GaussianBlur(200))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    black.putalpha(vg.point(lambda v: int(v * 0.55)))
    im.alpha_composite(black)
    _BG = im
    return _BG.copy()


def shadow_card(w, h, r=22, border=(255, 255, 255, 38), fill=CARD + (238,)):
    pad = 26
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad + 10, pad + w, pad + h + 12], r, fill=(0, 0, 0, 90))
    im = im.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=fill, outline=border, width=1)
    return im, pad


def blit(base, im, cx, cy, p, rise=14):
    if p <= 0:
        return
    a = im.getchannel("A").point(lambda v: int(v * p))
    im2 = im.copy()
    im2.putalpha(a)
    base.alpha_composite(im2, (int(cx - im.width / 2), int(cy - im.height / 2 + (1 - p) * rise)))


def tracked(d, xy, text, f, fill, tr=3, p=1.0, anchor="lm"):
    if p <= 0:
        return
    ws = [f.getlength(ch) + tr for ch in text]
    wsum = sum(ws) - tr
    x = xy[0] - (wsum if anchor[0] == "r" else wsum / 2 if anchor[0] == "m" else 0)
    for ch, w in zip(text, ws):
        d.text((x, xy[1]), ch, font=f, fill=fill, anchor="lm")
        x += w


def chip(base, text, col, cx, cy, p, fsize=17, rise=8, scale=1.0):
    f = font("JetBrainsMono-var.ttf", fsize)
    w = int(tw(text, f)) + 52
    im = Image.new("RGBA", (w, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 39], 10, fill=(9, 14, 26, 235), outline=col + (170,), width=1)
    d.ellipse([12, 17, 18, 23], fill=col + (255,))
    draw_rich(d, (30, 20), text, f, (235, 241, 249, 255), "lm")
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    blit(base, im, cx, cy, p, rise)


def node(base, cx, cy, w, h, p, col, kicker, title, sub, icon, t):
    im, pad = shadow_card(w, h)
    d = ImageDraw.Draw(im)
    # icon tile
    ic = icon_rgba(icon, "#%02X%02X%02X" % col).resize((34, 34), Image.LANCZOS)
    im.paste(ic, (pad + 26, pad + 24), ic)
    tracked(d, (pad + 74, pad + 41), kicker, font("JetBrainsMono-var.ttf", 15), col + (230,), 2)
    d.text((pad + 26, pad + 74), title, font=font("BeVietnamPro-SemiBold.ttf", 32),
           fill=TXT + (255,))
    d.text((pad + 26, pad + 122), sub, font=font("BeVietnamPro-Regular.ttf", 18),
           fill=MUT + (255,))
    blit(base, im, cx, cy, p)


def connector(d, x0, x1, y, p, col):
    if p <= 0:
        return
    x = x0 + (x1 - x0) * p
    d.line([x0, y, x, y], fill=col + (70,), width=6)
    d.line([x0, y, x, y], fill=col + (235,), width=2)
    if p > 0.55:
        q = (p - 0.55) / 0.45
        c = col + (int(235 * q),)
        d.line([x - 12, y - 7, x, y, x - 12, y + 7], fill=c, width=3, joint="curve")


def packets(d, x0, x1, y, t, p, col, n=2):
    if p < 1:
        return
    for k in range(n):
        q = (t * 0.28 + k / n) % 1.0
        x = x0 + (x1 - x0) * q
        a = int(230 * math.sin(q * math.pi) ** 0.6)
        for rr, aa in ((11, a // 10), (7, a // 4), (3.5, a)):
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (aa,))


def json_card(base, x, y, w, title, lines, q, p, scale=1.0, t=None):
    if p <= 0:
        return
    h = 60 + len(lines) * 27
    im, pad = shadow_card(w, h, 16, fill=(13, 20, 36, 240))
    d = ImageDraw.Draw(im)
    d.text((pad + 20, pad + 14), title, font=font("JetBrainsMono-var.ttf", 15),
           fill=AMBER + (235,))
    n = int(q * sum(len(s) + 1 for s in lines))
    used = 0
    fy = pad + 44
    cx0, cy0 = pad + 20, fy
    for s in lines:
        vis = s[:max(0, n - used)]
        d.text((pad + 20, fy), vis, font=font("JetBrainsMono-var.ttf", 19), fill=(248, 251, 255, 255))
        cx0, cy0 = pad + 20 + d.textlength(vis, font=font("JetBrainsMono-var.ttf", 19)), fy
        used += len(s) + 1
        fy += 27
        if used >= n:
            break
    if t is not None and (q < 1 or int(t * 2.4) % 2 == 0):
        d.rectangle([cx0 + 2, cy0 + 2, cx0 + 9, cy0 + 22], fill=AMBER + (200,))
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    blit(base, im, x + w / 2, y + h / 2 + 26, p, 10)


def caption(base, lines, p=1.0, dx=0):
    if not lines or p <= 0:
        return
    w, h = 900, 170
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font("BeVietnamPro-Medium.ttf", 27)
    y = 81
    d.rounded_rectangle([28, y - 16, 32, y + len(lines) * 38 + 8], 2, fill=VIOLET + (255,))
    for ln in lines:
        d.text((52, y - 20), ln, font=f, fill=(226, 232, 240, 255))
        y += 38
    blit(base, im, 60 + w / 2 + dx, 855 + h / 2, p, 0)


# ---------- draw ----------
def make_draw(tl):
    st = [tl[s[0]] for s in SEGS]

    def draw(t):
        base = bg().copy()
        dur_all = tl["_total"]

        # brand — vẽ lên tile trong suốt để fade đúng
        pb = seg(t, 0.15, 0.65)
        if pb > 0:
            bm = Image.new("RGBA", (W, 140), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bm)
            bd.rounded_rectangle([88, 62, 96, 110], 3, fill=AMBER + (255,))
            tracked(bd, (112, 78), "AN TECH ACADEMY", font("BeVietnamPro-SemiBold.ttf", 22),
                    TXT + (255,), 2)
            tracked(bd, (112, 104), "KIẾN TRÚC HỆ THỐNG · API", font("JetBrainsMono-var.ttf", 14),
                    MUT + (255,), 2)
            tracked(bd, (1832, 78), STYLE, font("JetBrainsMono-var.ttf", 14),
                    MUT + (255,), 1, anchor="rm")
            blit(base, bm, W / 2, 70, pb, 0)

        # nodes — cùng trục y
        node(base, 400, 540, 300, 190, seg(t, 0.45, 1.05), CYAN, "01 · CLIENT",
             "Client", "ứng dụng gửi yêu cầu", "monitor", t)
        node(base, 960, 540, 360, 220, seg(t, 0.62, 1.22), VIOLET, "API GATEWAY",
             "API", "hợp đồng giao tiếp", "layers", t)
        pa = seg(t, 0.9, 1.4)
        if pa > 0:
            lm = Image.new("RGBA", (300, 26), (0, 0, 0, 0))
            tracked(ImageDraw.Draw(lm), (150, 13), "request / response",
                    font("JetBrainsMono-var.ttf", 13), MUT + (255,), 2, 1.0, "mm")
            blit(base, lm, 960, 620, pa, 0)
        node(base, 1520, 540, 300, 190, seg(t, 0.78, 1.38), EMER, "03 · SERVER",
             "Server", "hệ thống xử lý", "server", t)

        # lớp phủ: vòng glow, đèn, connector, gói tin — composite đúng alpha
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        do = ImageDraw.Draw(ov)
        pg = seg(t, 0.9, 1.5)
        if pg > 0:
            pul = 0.5 + 0.5 * math.sin(t * 2.4)
            do.rounded_rectangle([960 - 188, 540 - 118, 960 + 188, 540 + 118], 30,
                                 outline=VIOLET + (int((16 + 22 * pul) * pg),), width=4)
            do.rounded_rectangle([960 - 184, 540 - 114, 960 + 184, 540 + 114], 27,
                                 outline=VIOLET + (int((40 + 50 * pul) * pg),), width=1)
            sa = int(255 * (0.55 + 0.45 * math.sin(t * 3.1)))
            do.ellipse([1638, 464, 1648, 474], fill=EMER + (sa,))
            do.ellipse([1635, 461, 1651, 477], outline=EMER + (int(60 * pg),), width=1)

        ql = seg(t, st[2] - 0.15, st[2] + 0.55)
        qr = seg(t, st[4] - 0.15, st[4] + 0.55)
        connector(do, 555, 776, 540, ql, CYAN)
        connector(do, 1144, 1368, 540, qr, EMER)
        if ql > 0.9:
            packets(do, 566, 770, 540, t, ql, CYAN)
        if qr > 0.9:
            packets(do, 1150, 1360, 540, t + 0.5, qr, EMER)
        base.alpha_composite(ov)

        if ql > 0.9:
            chip(base, "request", CYAN, 666, 492, seg(t, st[2] + 0.45, st[2] + 0.8))
        if qr > 0.9:
            chip(base, "response", EMER, 1256, 588, seg(t, st[6] - 0.1, st[6] + 0.25))

        # endpoint path + underline
        qe = seg(t, st[8] - 0.25, st[8] + 0.35)
        if qe > 0:
            pw = 560
            im = Image.new("RGBA", (pw, 56), (0, 0, 0, 0))
            dd = ImageDraw.Draw(im)
            dd.rounded_rectangle([0, 0, pw - 1, 55], 14, fill=(15, 23, 42, 235),
                                 outline=AMBER + (140,), width=2)
            dd.text((24, 28), "GET", font=font("JetBrainsMono-var.ttf", 19),
                    fill=EMER + (240,), anchor="lm")
            dd.text((92, 28), "/api/v1/products", font=font("JetBrainsMono-var.ttf", 19),
                    fill=TXT + (245,), anchor="lm")
            blit(base, im, 960, 715, qe, 10)
            em = Image.new("RGBA", (200, 26), (0, 0, 0, 0))
            tracked(ImageDraw.Draw(em), (4, 13), "ENDPOINT",
                    font("JetBrainsMono-var.ttf", 13), AMBER + (255,), 2)
            blit(base, em, 800, 676, qe, 0)

        # HTTP / JSON
        qh = seg(t, st[10] - 0.1, st[10] + 0.3)
        if qh > 0:
            chip(base, "HTTP/1.1", CYAN, 1332, 715, qh)
        qj = seg(t, st[11] - 0.15, st[11] + 0.25)
        json_card(base, 1130, 784, 640, "200 OK · application/json",
                  ['{', '  "id": 1,', '  "ten": "Cơm gà",', '  "gia": 45000', '}'],
                  lin(t, st[11] - 0.1, st[11] + 1.3), qj)

        # captions
        if t < st[2]:
            caption(base, ["API — hợp đồng giao tiếp", "giữa hai hệ thống độc lập."])
        elif t < st[7]:
            caption(base, ["Client gửi request,", "server trả response."])
        elif t < st[12]:
            caption(base, ["Chuẩn hoá luồng dữ liệu", "qua endpoint, HTTP và JSON."])
        else:
            caption(base, ["Một vòng gọi API", "trọn vẹn."])

        qf = lin(t, dur_all - 0.6, dur_all - 0.05)
        if qf > 0:
            base.alpha_composite(Image.new("RGBA", (W, H), (5, 8, 14, int(255 * qf))))

        return base

    return draw


def main():
    os.makedirs(AUD, exist_ok=True)
    os.makedirs(FR, exist_ok=True)
    paths = [synth(s) for s in SEGS]
    durs = [len(decode(p)) / SR for p in paths]
    tl = {}
    t = 0.35
    for (sid, txt, pause), dd in zip(SEGS, durs):
        tl[sid] = t
        t += dd + pause
    total = t + 0.45
    tl["_total"] = total
    n = int(total * FPS)

    mix = np.zeros(int(total * SR) + SR)
    for (sid, txt, pause), pth in zip(SEGS, paths):
        x = decode(pth)
        st = int(tl[sid] * SR)
        mix[st:st + len(x)] += x
    pk = np.max(np.abs(mix))
    print("PEAK", round(pk, 3), "TOTAL", round(total, 2), flush=True)
    if pk > 0.98:
        mix *= 0.98 / pk
    sfx.write_wav(OUT + f"/demo_voice_{TAG}.wav", mix)

    draw = make_draw(tl)
    for k in range(n):
        draw(k / FPS).convert("RGB").save(f"{FR}/f{k:04d}.jpg", quality=92)
        if k % 120 == 0:
            print("frame", k, "/", n, flush=True)

    run = lambda c: subprocess.run(c, capture_output=True, text=True)
    vid = OUT + f"/demo_video_{TAG}.mp4"
    r = run([FF, "-y", "-framerate", "30", "-i", f"{FR}/f%04d.jpg", "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", vid])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("encode fail")
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", run(
        [FF, "-i", OUT + f"/demo_voice_{TAG}.wav", "-af",
         "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]).stderr, re.S)[-1]
    m = json.loads(m)
    af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true")
    run([FF, "-y", "-i", OUT + f"/demo_voice_{TAG}.wav", "-af", af, "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k", OUT + f"/demo_audio_{TAG}.m4a"])
    r = run([FF, "-y", "-i", vid, "-i", OUT + f"/demo_audio_{TAG}.m4a", "-c:v", "copy",
             "-c:a", "copy", "-movflags", "+faststart", "-shortest",
             OUT + f"/api_pro_demo20_{TAG}.mp4"])
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit("mux fail")
    print("DONE", dur(OUT + "/api_pro_demo20.mp4"), flush=True)


def seg(t, a, b):
    p = max(0.0, min(1.0, (t - a) / (b - a))) if b > a else (1.0 if t >= b else 0.0)
    return 1 - (1 - p) ** 3


def lin(t, a, b):
    return max(0.0, min(1.0, (t - a) / (b - a))) if b > a else (1.0 if t >= b else 0.0)


if __name__ == "__main__":
    main()
