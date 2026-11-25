import json, math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import *
from scene_specs import SCENES

RD = 0.2          # element reveal <= 200 ms (Gate B)
HEAD_RD = 0.3
FONTS = {"kick": F_KICK, "head": F_HEAD, "head56": F_HEAD56, "lbl": F_LBL, "lbl30": F_LBL30,
         "sub": F_SUB, "chip": F_CHIP, "num": F_NUM, "word": F_WORD, "tag": F_TAG,
         "big": F_BIG, "count": F_COUNT}
SPEC = {s["id"]: s for s in SCENES}

def mk(im, x, y, t0, anchor="tl", hl=None):
    return dict(im=im, x=x, y=y, t0=t0, anchor=anchor, hl=hl)

def hl_window(tl, sid, cue):
    if not cue:
        return None
    s = tl[sid]["starts"][cue - 1]
    return (s, s + tl[sid]["durs"][cue - 1])

# ---- extra sprite builders ----
def sp_phone_card(accent):
    im = card_base(420, 420)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 24, 330, 280], 24, fill=INK)
    d.rounded_rectangle([102, 36, 318, 268], 12, fill=WHITE)
    d.text((210, 58), "Gợi ý cho bạn", font=F_PHONE, fill=hx(accent), anchor="mm")
    for y0 in (82, 176):
        d.rounded_rectangle([112, y0, 308, y0 + 82], 10, fill=(241, 245, 249, 255))
        d.rounded_rectangle([122, y0 + 12, 156, y0 + 46], 8, fill=hx(accent))
        d.rounded_rectangle([166, y0 + 16, 298, y0 + 24], 4, fill=(148, 163, 184, 255))
        d.rounded_rectangle([166, y0 + 32, 278, y0 + 40], 4, fill=(203, 213, 225, 255))
        d.rounded_rectangle([122, y0 + 58, 298, y0 + 66], 4, fill=(203, 213, 225, 255))
    d.text((210, 300), "Sản phẩm gợi ý", font=F_LBL, fill=INK, anchor="mm")
    d.text((210, 346), "hợp sở thích bạn", font=F_SUB, fill=MUT, anchor="mm")
    return im

def sp_rule_card(main, sub, color, w=1200, h=380):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 6, w, h], 20, fill=(15, 23, 42, 20))
    d.rounded_rectangle([0, 0, w, h - 6], 20, fill=WHITE, outline=hx(color), width=5)
    ic = icon_rgba("lock", color).resize((110, 110), Image.LANCZOS)
    im.paste(ic, ((w - 110) // 2, 36), ic)
    d.text((w / 2, 200), main, font=F_BIG, fill=INK, anchor="mm")
    d.text((w / 2, 280), sub, font=F_LBL30, fill=hx(color), anchor="mm")
    return im

def sp_node_badge(text, color):
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = tmp.textlength(text, font=F_LBL)
    pw, ph = int(tw + 80), 84
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw, ph], 42, fill=hx(color))
    d.text((pw / 2, ph / 2), text, font=F_LBL, fill=WHITE, anchor="mm")
    return im

def sp_map_row(left, right, color):
    w = 1600
    im = Image.new("RGBA", (w, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((700, 40), left, font=F_LBL30, fill=INK, anchor="rm")
    ic = icon_rgba("arrow-right", color).resize((48, 48), Image.LANCZOS)
    im.paste(ic, (730, 16), ic)
    d.text((810, 40), right, font=F_LBL, fill=hx(color), anchor="lm")
    return im

def sp_dim_map():
    im = Image.new("RGBA", (1500, 460), (0, 0, 0, 0))
    cols = [("Công nghệ phần mềm", "#2563EB"), ("Khoa học dữ liệu & AI", "#7C3AED"),
            ("An toàn thông tin", "#DC2626"), ("Hệ thống thông tin", "#D97706"),
            ("Mạng & Đám mây", "#0284C7"), ("Đồ họa & Game", "#0D9488")]
    pos = [(120, 40), (820, 40), (120, 190), (820, 190), (120, 340), (820, 340)]
    for i, ((label, col), (x, y)) in enumerate(zip(cols, pos)):
        node = sp_major_node(i + 1, label, col, w=640)
        im.paste(node, (x, y), node)
    im.putalpha(im.getchannel("A").point(lambda a: int(a * 0.6)))
    return im

def sp_step(text, color):
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = tmp.textlength(text, font=F_LBL30)
    pw, ph = int(tw + 60), 90
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw, ph], 16, fill=WHITE, outline=hx(color), width=3)
    d.text((pw / 2, ph / 2), text, font=F_LBL30, fill=hx(color), anchor="mm")
    return im

# ---- spec expansion ----
def build_scene(spec, tl):
    sid = spec["id"]
    af, at = ACC[spec["accent"]]
    sprites, dynamics = [], []
    def T(cue, frac=0.0):
        return cue_t(tl, sid, cue, frac)
    for el in spec["sprites"]:
        t = el["t"]; cue = el.get("cue", 1); frac = el.get("frac", 0.0)
        t0 = T(cue, frac); hl = hl_window(tl, sid, el.get("hl"))
        col = el.get("color", af); txt = el.get("txt", col)
        x, y = el.get("x", 0), el.get("y", 0); anch = el.get("anchor", "tl")
        if t == "card":
            im = sp_icon_card(el["icon"], el["label"], el.get("sub"), col,
                              el.get("w", 420), el.get("h", 420), el.get("icon_size", 140))
            sprites.append(mk(im, x, y, t0, anch, hl))
        elif t == "card_bg":
            sprites.append(mk(sp_card_bg(el["w"], el["h"]), x, y, t0, anch, hl))
        elif t == "icon_label":
            im = sp_icon_label(el["icon"], el["label"], col, el.get("w", 220),
                               el.get("icon_size", 100), el.get("label_font"))
            sprites.append(mk(im, x, y, t0, anch, hl))
        elif t == "icon":
            sprites.append(mk(sp_icon_only(el["icon"], col, el.get("size", 140)), x, y, t0, anch, hl))
        elif t == "chip":
            sprites.append(mk(sp_chip(el["text"], col, txt), x, y, t0, anch, hl))
        elif t == "node":
            sprites.append(mk(sp_node(el["number"], el.get("label"), col), x, y, t0, anch, hl))
        elif t == "major_node":
            sprites.append(mk(sp_major_node(el["number"], el["label"], col), x, y, t0, anch, hl))
        elif t == "check":
            sprites.append(mk(sp_check(el["text"], col), x, y, t0, anch, hl))
        elif t == "bullet":
            sprites.append(mk(sp_bullet(el["icon"], el["text"], col), x, y, t0, anch, hl))
        elif t == "text":
            f = FONTS[el.get("font", "sub")]
            sprites.append(mk(sp_text(el["text"], f, el.get("color", "#0F172A")), x, y, t0, anch, hl))
        elif t == "panel":
            im = sp_panel(el["title"], el["icon"], el.get("sub"), col, el.get("w", 560), el.get("h", 420))
            sprites.append(mk(im, x, y, t0, anch, hl))
        elif t == "wordmark":
            sprites.append(mk(sp_wordmark(), x, y, t0, anch, hl))
        elif t == "phone":
            sprites.append(mk(sp_phone(col, el.get("title", "App")), x, y, t0, anch, hl))
        elif t == "phone_card":
            sprites.append(mk(sp_phone_card(col), x, y, t0, anch, hl))
        elif t == "rule_card":
            sprites.append(mk(sp_rule_card(el["main"], el["sub"], col, el.get("w", 1200), el.get("h", 380)), x, y, t0, anch, hl))
        elif t == "node_badge":
            sprites.append(mk(sp_node_badge(el["text"], col), x, y, t0, "mm", hl))
        elif t == "dim_map":
            sprites.append(mk(sp_dim_map(), x, y, t0, "mm", hl))
        elif t == "chip_row":
            items = el["items"]; gap = el.get("gap", 24)
            chips = [sp_chip(it["text"], col, txt) for it in items]
            total = sum(c.size[0] for c in chips) + gap * (len(chips) - 1)
            cx = el.get("cx", W / 2); xx = cx - total / 2
            for it, cim in zip(items, chips):
                sprites.append(mk(cim, xx, y, T(it["cue"], it.get("frac", 0)), "tl", hl))
                xx += cim.size[0] + gap
        elif t == "chip_col":
            cx = el.get("cx", W / 2); dy = el.get("dy", 74)
            for i, it in enumerate(el["items"]):
                cim = sp_chip(it["text"], col, txt)
                sprites.append(mk(cim, cx, y + i * dy, T(it["cue"], it.get("frac", 0)), "mm", hl))
        elif t == "check_col":
            dy = el.get("dy", 90)
            for i, it in enumerate(el["items"]):
                sprites.append(mk(sp_check(it["text"], col), x, y + i * dy, T(it["cue"], it.get("frac", 0)), "tl", hl))
        elif t == "bullet_col":
            dy = el.get("dy", 100)
            for i, it in enumerate(el["items"]):
                sprites.append(mk(sp_bullet(it["icon"], it["text"], col), x, y + i * dy, T(it["cue"], it.get("frac", 0)), "tl", hl))
        elif t == "fit_card":
            w, h = el.get("w", 1000), el.get("h", 420)
            sprites.append(mk(sp_card_bg(w, h), x, y, t0, "tl", hl))
            for i, b in enumerate(el["bullets"]):
                sprites.append(mk(sp_bullet(b["icon"], b["text"], col, w - 120),
                                  x + 60, y + 60 + i * 110, T(b["cue"], b.get("frac", 0)), "tl", None))
        elif t == "map_rows":
            dy = el.get("dy", 95)
            for i, r in enumerate(el["rows"]):
                sprites.append(mk(sp_map_row(r["left"], r["right"], r["color"]),
                                  x, y + i * dy, T(r["cue"], 0.0), "tl", hl_window(tl, sid, r["cue"])))
        elif t == "steps":
            steps = el["steps"]; boxes = [sp_step(s["text"], col) for s in steps]
            gap = 70; total = sum(b.size[0] for b in boxes) + gap * (len(boxes) - 1)
            xx = W / 2 - total / 2
            for i, (s, bim) in enumerate(zip(steps, boxes)):
                sprites.append(mk(bim, xx, y, T(s["cue"], s.get("frac", 0)), "tl", None))
                if i < len(boxes) - 1:
                    ax = xx + bim.size[0] + 8
                    dynamics.append(conn_dyn(ax + 0, y + 45, ax + gap - 16, y + 45,
                                             T(s["cue"], s.get("frac", 0)) + 0.2, hx(col), None, 5))
                xx += bim.size[0] + gap
        else:
            raise ValueError("unknown sprite type " + t)
    for c in spec.get("conns", []):
        t0 = T(c["cue"], c.get("frac", 0))
        cue_end = T(c["cue"], 1.0)
        dot_end = max(cue_end, t0 + 1.5) if c.get("dot") else None
        col = hx(c.get("color", af))
        dynamics.append(conn_dyn(c["x0"], c["y0"], c["x1"], c["y1"], t0, col, dot_end, c.get("width", 6)))
    if spec.get("custom") == "s24":
        dynamics.append(s24_dyn(tl, sid, hx(af)))
    if spec.get("custom") == "s30":
        sprites, dynamics = s30_build(tl, sid, sprites, dynamics)
    return sprites, dynamics

def conn_dyn(x0, y0, x1, y1, t0, color, dot_end, width):
    def fn(t, base, d):
        p = seg(t, t0, t0 + 0.6)
        if p <= 0:
            return
        dotq = None
        if dot_end is not None and t0 + 0.6 <= t < dot_end:
            dotq = ((t - (t0 + 0.6)) / 0.9) % 1
        draw_conn(d, x0, y0, x1, y1, p, color, dotq, width)
    return fn

# ---- custom S24 parallax ----
def s24_dyn(tl, sid, accent):
    sky_top, sky_bot = (204, 251, 241), (240, 253, 250)
    sky = Image.new("RGBA", (1728, 610), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sky)
    for yy in range(610):
        f = yy / 610
        col = tuple(int(sky_top[i] + (sky_bot[i] - sky_top[i]) * f) for i in range(3))
        sd.line([(0, yy), (1728, yy)], fill=col + (255,))
    hills = Image.new("RGBA", (2400, 300), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hills)
    for cx, r, col in [(200, 220, (153, 246, 228)), (700, 300, (153, 246, 228)),
                       (1300, 260, (153, 246, 228)), (1900, 320, (153, 246, 228))]:
        hd.ellipse([cx - r, 300 - r, cx + r, 300 + r], fill=col + (255,))
    ground = Image.new("RGBA", (2400, 120), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ground)
    gd.rectangle([0, 0, 2400, 120], fill=(13, 148, 136, 255))
    for x in range(0, 2400, 160):
        gd.rounded_rectangle([x, 0, x + 120, 26], 8, fill=(15, 118, 110, 255))
    char = Image.new("RGBA", (90, 130), (0, 0, 0, 0))
    cd = ImageDraw.Draw(char)
    cd.rounded_rectangle([20, 0, 70, 50], 12, fill=(15, 23, 42, 255))
    cd.rounded_rectangle([10, 55, 80, 110], 14, fill=(13, 148, 136, 255))
    cd.rectangle([22, 110, 40, 130], fill=(15, 23, 42, 255))
    cd.rectangle([50, 110, 68, 130], fill=(15, 23, 42, 255))
    def fn(t, base, d):
        cv = Image.new("RGBA", (1728, 610), (0, 0, 0, 0))
        cv.paste(sky, (0, 0))
        off1 = int(t * 20) % 2400
        cv.paste(hills, (-off1, 310), hills)
        cv.paste(hills, (-off1 + 2400, 310), hills)
        off2 = int(t * 45) % 2400
        cv.paste(ground, (-off2, 490), ground)
        cv.paste(ground, (-off2 + 2400, 490), ground)
        cv.paste(char, (804, 360), char)
        base.paste(cv, (96, 250), cv)
    return fn

# ---- custom S30 countdown ----
def s30_build(tl, sid, sprites, dynamics):
    s = tl[sid]
    c3_start = s["starts"][2]
    pause0 = c3_start - 3.0
    qcard = Image.new("RGBA", (1300, 300), (0, 0, 0, 0))
    qd = ImageDraw.Draw(qcard)
    qd.rounded_rectangle([0, 0, 1300, 300], 24, fill=(30, 41, 59, 255), outline=(148, 163, 184, 255), width=2)
    qd.text((650, 90), "Mình thích tạo ra sản phẩm,", font=F_LBL, fill=WHITE, anchor="mm")
    qd.text((650, 150), "phân tích dữ liệu, hay bảo vệ hệ thống?", font=F_LBL, fill=WHITE, anchor="mm")
    sprites.append(mk(qcard, 960, 360, cue_t(tl, sid, 2, 0.0), "mm", None))
    ans = sp_text("Câu trả lời là manh mối đầu tiên của bạn.", F_LBL30, "#94A3B8")
    sprites.append(mk(ans, 960, 760, cue_t(tl, sid, 3, 0.1), "mm", None))
    def ring(t, base, d):
        if not (pause0 <= t < c3_start):
            return
        rem = c3_start - t
        cx, cy, r = 960, 620, 90
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(71, 85, 105, 255), width=10)
        ang = 360 * (rem / 3.0)
        d.arc([cx - r, cy - r, cx + r, cy + r], start=-90, end=-90 + ang, fill=(56, 189, 248, 255), width=10)
        n = max(0, math.ceil(rem - 1e-6))
        d.text((cx, cy), str(n), font=F_COUNT, fill=WHITE, anchor="mm")
    dynamics.append(ring)
    return sprites, dynamics

# ---- render ----
ORDER = [s["id"] for s in SCENES]
XFADE = 0.3

def video_frames(tl):
    # đuôi video dài hơn audio 0.3s (trừ cảnh cuối) để bù phần crossfade 300ms;
    # làm tròn lũy kế giữ tổng frame khớp tổng thời lượng audio
    Ns = {}; cum = 0.0; prev = 0
    for k, sid in enumerate(ORDER):
        cum += tl[sid]["total"] + (XFADE if k < len(ORDER) - 1 else 0.0)
        f = round(cum * FPS)
        Ns[sid] = f - prev; prev = f
    return Ns

def render_scene(sid, tl, outdir, dark=False, preview=False, N=None):
    spec = SPEC[sid]
    sprites, dynamics = build_scene(spec, tl)
    total = tl[sid]["total"]
    if N is None:
        N = int(math.ceil(total * FPS))
    os.makedirs(outdir, exist_ok=True)
    af, at = ACC[spec["accent"]]
    cues = tl[sid]["cues"]; starts = tl[sid]["starts"]; durs = tl[sid]["durs"]
    bg = (15, 23, 42, 255) if dark else BG
    if preview:
        # representative moments: after each cue reveals + final hold
        times = sorted({min(total - 0.1, s + d * 0.6) for s, d in zip(starts, durs)} | {total - 0.3})
        frames = [(int(t * FPS), t) for t in times]
    else:
        frames = [(i, i / FPS) for i in range(N)]
    for i, t in frames:
        base = Image.new("RGBA", (W, H), bg)
        d = ImageDraw.Draw(base)
        hp = seg(t, 0, HEAD_RD)
        if spec.get("title") or spec.get("kicker"):
            base = heading(base, d, spec.get("kicker"), spec.get("title"), at, hp,
                           FONTS.get(spec.get("title_font", "head")))
            d = ImageDraw.Draw(base)
        for sp in sprites:
            p = seg(t, sp["t0"], sp["t0"] + RD)
            paste_sprite(base, sp["im"], sp["x"], sp["y"], p, sp["anchor"])
        d = ImageDraw.Draw(base)
        for sp in sprites:
            if sp["hl"] and sp["hl"][0] <= t < sp["hl"][1]:
                p = seg(t, sp["t0"], sp["t0"] + RD)
                if p >= 1:
                    w0, h0 = sp["im"].size
                    x, y = sp["x"], sp["y"]
                    if sp["anchor"] == "mm":
                        x -= w0 / 2; y -= h0 / 2
                    d.rounded_rectangle([x - 4, y - 4, x + w0 + 4, y + h0 + 4], 18, outline=hx(at), width=3)
        for fn in dynamics:
            fn(t, base, d)
            d = ImageDraw.Draw(base)
        for j, c in enumerate(cues):
            if starts[j] <= t < starts[j] + durs[j]:
                subtitle_band(d, c["subs"], dark)
                break
        if preview:
            base.convert("RGB").save(f"{outdir}/p{i:04d}.png")
        else:
            base.convert("RGB").save(f"{outdir}/f{i:04d}.jpg", quality=95)
    return N

def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    preview = "--preview" in args
    tl = load_timeline(dry)
    only = None
    if "--scene" in args:
        only = args[args.index("--scene") + 1].split(",")
    sids = only or [s["id"] for s in SCENES]
    Ns = video_frames(tl)
    grand = 0
    for sid in sids:
        spec = SPEC[sid]
        out = f"{FR}/{sid}"
        n = render_scene(sid, tl, out, spec.get("dark", False), preview,
                         None if preview else Ns[sid])
        grand += n
        print(f"{sid} frames={n} total={tl[sid]['total']:.2f}s", flush=True)
    print("RENDER_DONE", grand, "frames", f"{grand/FPS:.1f}s")

if __name__ == "__main__":
    main()