# -*- coding: utf-8 -*-
import json, math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_core import *
from scene_specs import SCENES

RD = 0.22
F_H1 = font("PlusJakartaSans-var.ttf", 44, 800)
F_H1_40 = font("PlusJakartaSans-var.ttf", 40, 800)
F_H2S = font("BeVietnamPro-SemiBold.ttf", 30)
F_MONO_S = font("JetBrainsMono-var.ttf", 21)
FONTS = {"h1": F_H1, "h1s": F_H1_40, "h2": F_H2, "body": F_BODY, "body_m": F_BODY_M,
         "sm": F_SM, "sm_m": F_SM_M, "lbl": F_LBL, "num": F_NUM, "nums": F_NUM_S,
         "form": F_FORM, "sub": F_SUB}
SPEC = {s["id"]: s for s in SCENES}

def mk(im, x, y, t0, anchor="tl"):
    return dict(im=im, x=x, y=y, t0=t0, anchor=anchor)

def conn_dyn(x0, y0, x1, y1, t0, color, dot_end=None, width=5):
    def fn(t, base, d):
        p = seg(t, t0, t0 + 0.55)
        if p <= 0:
            return
        dq = None
        if dot_end is not None and t0 + 0.55 <= t < dot_end:
            dq = ((t - (t0 + 0.55)) / 0.9) % 1
        draw_conn(d, x0, y0, x1, y1, p, color, dq, width)
    return fn

def sp_panel(icon, title, sub, w=430, h=300, color=BLUE, tag=None, icon_size=76):
    im = card(w, h)
    d = ImageDraw.Draw(im)
    ic = sp_icon(icon, color, icon_size)
    im.paste(ic, (30, 28), ic)
    ty = 34 + icon_size
    for ln in wrap(title, F_H2, w - 60)[:2]:
        d.text((30, ty), ln, font=F_H2, fill=INK, anchor="lm")
        ty += 42
    if sub:
        for ln in wrap(sub, F_SM, w - 60)[:2]:
            d.text((30, ty + 4), ln, font=F_SM, fill=MUT, anchor="lm")
            ty += 33
    if tag:
        chip = sp_chip(tag, color)
        im.paste(chip, (w - chip.size[0] - 24, 26), chip)
    return im

def sp_wordmark():
    im = Image.new("RGBA", (1200, 320), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((600, 96), "AN TECH ACADEMY", font=F_WM, fill=NAVY, anchor="mm")
    d.rounded_rectangle([330, 158, 870, 168], 5, fill=AMBER)
    d.text((600, 212), "Học công nghệ, làm chủ tương lai", font=F_BODY, fill=MUT, anchor="mm")
    return im

def sp_formula(parts, size=38):
    f = font("BeVietnamPro-SemiBold.ttf", size)
    w_ = int(sum(rich_width(s, f) for s, _ in parts)) + 20
    h_ = size + 34
    im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 10
    for s, c in parts:
        x += draw_rich(d, (x, h_ / 2), s, f, c, "lm")
    return im

# ---- build ----
def build_scene(spec, tl):
    sid = spec["id"]
    sprites, dynamics = [], []

    def T(cue, frac=0.0):
        return cue_t(tl, sid, cue, frac)

    for el in spec.get("sprites", []):
        t = el["t"]; cue = el.get("cue", 1); frac = el.get("frac", 0.0)
        t0 = T(cue, frac)
        x, y = el.get("x", 0), el.get("y", 0); anch = el.get("anchor", "tl")
        if t == "panel":
            sprites.append(mk(sp_panel(el["icon"], el["title"], el.get("sub"), el.get("w", 430),
                                       el.get("h", 300), el.get("color", BLUE), el.get("tag")), x, y, t0, anch))
        elif t == "card":
            sprites.append(mk(card(el.get("w", 400), el.get("h", 300), el.get("fill", WHITE),
                                   el.get("outline", BORDER)), x, y, t0, anch))
        elif t == "step":
            sprites.append(mk(sp_step(el["number"], el["title"], el.get("sub"), el.get("w", 380),
                                      el.get("h", 250), el.get("color", BLUE)), x, y, t0, anch))
        elif t == "rule":
            sprites.append(mk(sp_rule(el["left"], el["right"], el.get("conf"), el.get("lift"),
                                      el.get("w", 760), el.get("h", 170)), x, y, t0, anch))
        elif t == "callout":
            sprites.append(mk(sp_callout(el["icon"], el["title"], el.get("lines", []), el.get("w", 800),
                                         el.get("h", 150), el.get("tone", "amber")), x, y, t0, anch))
        elif t == "stat":
            sprites.append(mk(sp_stat(el["value"], el["label"], el.get("color", BLUE),
                                      el.get("w", 360), el.get("h", 170), el.get("note")), x, y, t0, anch))
        elif t == "text":
            f = FONTS[el.get("font", "body")]
            sprites.append(mk(sp_text(el["text"], f, el.get("color", INK)), x, y, t0, anch))
        elif t == "icon":
            sprites.append(mk(sp_icon(el["icon"], el.get("color", BLUE), el.get("size", 64)), x, y, t0, anch))
        elif t == "icon_label":
            sprites.append(mk(sp_icon_label(el["icon"], el["label"], el.get("color", BLUE),
                                            el.get("size", 64), el.get("f")), x, y, t0, anch))
        elif t == "check":
            sprites.append(mk(sp_check(el["text"], el.get("color", GREEN), el.get("w", 740)), x, y, t0, anch))
        elif t == "bullet":
            sprites.append(mk(sp_bullet(el["icon"], el["text"], el.get("color", BLUE), el.get("w", 740)),
                             x, y, t0, anch))
        elif t == "chip":
            sprites.append(mk(sp_chip(el["text"], el.get("color", BLUE), el.get("fill", WHITE),
                                      el.get("size", 26), el.get("icon")), x, y, t0, anch))
        elif t == "items":
            sprites.append(mk(sp_items(el["items"], el.get("size", 26), el.get("f")), x, y, t0, anch))
        elif t == "formula":
            parts = [(s, hx(c) if isinstance(c, str) else c) for s, c in el["parts"]]
            sprites.append(mk(sp_formula(parts, el.get("size", 38)), x, y, t0, anch))
        elif t == "wordmark":
            sprites.append(mk(sp_wordmark(), x, y, t0, anch))
        elif t == "browser":
            sprites.append(mk(sp_browser(el.get("w", 760), el.get("h", 520), el.get("state", False)),
                              x, y, t0, anch))
        elif t == "table":
            w = el["w"]; ch = el.get("header_h", 60); rh = el.get("row_h", 58)
            cols = el["cols"]; rows = el["rows"]
            frame = sp_table_frame(w, ch, cols, el["headers"], len(rows), rh)
            sprites.append(mk(frame, x, y, T(rows[0]["cue"], rows[0].get("frac", 0)), "tl"))
            for i, r in enumerate(rows):
                row = sp_row(w, cols, r["c"], rh, i, r.get("status", ""),
                             el.get("items_col"), el.get("bar_col"), el.get("fs", 26),
                             el.get("max_bar", 100))
                sprites.append(mk(row, x, y + ch + i * rh,
                                  T(r["cue"], r.get("frac", 0)), "tl"))
        elif t == "bars":
            w = el.get("w", 740); rh = el.get("row_h", 84); items = el["items"]
            h = 84 + rh * len(items)
            fr = card(w, h)
            dd = ImageDraw.Draw(fr)
            dd.text((30, 40), el.get("title", ""), font=F_LBL, fill=MUT, anchor="lm")
            sprites.append(mk(fr, x, y, T(el.get("title_cue", items[0]["cue"]), 0.0), "tl"))
            tx0, tx1 = 30 + el.get("label_w", 210), w - 92

            def bars_dyn(t, base, d, items=items, x=x, y=y, tx0=tx0, tx1=tx1, rh=rh, w=w):
                for i, it in enumerate(items):
                    s0 = T(it["cue"], it.get("frac", 0.0))
                    p = seg(t, s0, s0 + 0.85)
                    if p <= 0:
                        continue
                    yy = y + 84 + i * rh + rh / 2
                    d.text((x + 30, yy), it["label"], font=F_BODY_M, fill=INK, anchor="lm")
                    d.rounded_rectangle([x + tx0, yy - 9, x + tx1, yy + 9], 9, fill=(226, 235, 247, 255))
                    col = hx(it.get("color", "#2F6FD0"))
                    val = it["pct"] * p
                    d.rounded_rectangle([x + tx0, yy - 9, x + tx0 + max(10, (tx1 - tx0) * val / 100), yy + 9],
                                        9, fill=col)
                    d.text((x + w - 26, yy), f"{round(val):g}%",
                           font=font("PlusJakartaSans-var.ttf", 30, 800), fill=col, anchor="rm")
            dynamics.append(bars_dyn)
        elif t == "code":
            w, h = el["w"], el["h"]
            fr = sp_code(el["lines"], w, h, el.get("title", "main.py"))
            sprites.append(mk(fr, x, y, T(1, 0.0), "tl"))
            lines = el["lines"]; lh = el.get("line_h", 34)

            def code_dyn(t, base, d, lines=lines, x=x, y=y, w=w, lh=lh):
                for i, ln in enumerate(lines):
                    s0 = T(ln.get("cue", 1), ln.get("frac", 0.0))
                    if t < s0:
                        continue
                    ly = y + 74 + i * lh
                    hi = False
                    if ln.get("mark"):
                        m = ln["mark"]
                        ms = tl[sid]["starts"][m - 1]
                        me = ms + tl[sid]["durs"][m - 1] + 0.3
                        hi = ms <= t < me
                    if hi:
                        d.rectangle([x + 14, ly - lh / 2 + 1, x + w - 14, ly + lh / 2 - 1], fill=CODE_HL)
                    d.text((x + 62, ly), str(i + 1), font=font("JetBrainsMono-var.ttf", 18),
                           fill=(96, 118, 148, 255), anchor="rm")
                    xx = x + 82
                    for s, c in hl_line(ln["s"]):
                        d.text((xx, ly), s, font=F_CODE, fill=c, anchor="lm")
                        xx += tw(s, F_CODE)
            dynamics.append(code_dyn)
        elif t == "strike":
            x0 = x; y0 = y; ww = el["w"]; hh = el["h"]; cue2 = cue; frac2 = frac
            def strike_dyn(t, base, d, x0=x0, y0=y0, ww=ww, hh=hh, cue2=cue2, frac2=frac2):
                s0 = T(cue2, frac2)
                p = seg(t, s0, s0 + 0.4)
                if p <= 0:
                    return
                yy = y0 + hh
                d.line([x0, yy, x0 + ww * p, yy], fill=RED, width=6)
                if p > 0.9:
                    d.line([x0 + 16, yy - 24, x0 + 40, yy], fill=RED, width=6)
                    d.line([x0 + 16, yy, x0 + 40, yy - 24], fill=RED, width=6)
            dynamics.append(strike_dyn)
        else:
            raise ValueError("unknown sprite " + t)

    for c in spec.get("conns", []):
        t0 = T(c["cue"], c.get("frac", 0.0))
        end = T(c["cue"], 1.0) + (c.get("ext", 0.0))
        dynamics.append(conn_dyn(c["x0"], c["y0"], c["x1"], c["y1"], t0,
                                 hx(c.get("color", "#2F6FD0")),
                                 end if c.get("dot") else None, c.get("width", 5)))
    if spec.get("custom") == "lift_scale":
        dynamics.extend(lift_scale(tl, sid))
    return sprites, dynamics

def lift_scale(tl, sid):
    dyn = []
    x0, x1, y = 300, 1620, 806
    vmin, vmax = 0.5, 2.0
    tick = x0 + (x1 - x0) * (1.0 - vmin) / (vmax - vmin)   # Lift = 1

    def fn(t, base, d):
        p = seg(t, cue_t(tl, sid, 4, 0.0), cue_t(tl, sid, 4, 0.0) + 0.8)
        if p <= 0:
            return
        xe = x0 + (x1 - x0) * p
        d.rounded_rectangle([x0, y - 10, x0 + (x1 - x0), y + 10], 10, fill=(226, 235, 247, 255))
        d.rounded_rectangle([x0, y - 10, min(tick, xe), y + 10], 10, fill=(226, 160, 150, 255))
        if xe > tick:
            d.rounded_rectangle([tick, y - 10, xe, y + 10], 10, fill=(150, 205, 168, 255))
        d.line([tick, y - 24, tick, y + 24], fill=NAVY, width=4)
    dyn.append(fn)

    def marker(t, base, d):
        s0 = cue_t(tl, sid, 4, 0.0) + 0.8
        p = seg(t, s0, s0 + 0.5)
        if p <= 0:
            return
        mx = x0 + (x1 - x0) * (1.25 - vmin) / (vmax - vmin)
        d.polygon([(mx, y - 6), (mx - 12, y - 26), (mx + 12, y - 26)], fill=NAVY)
        d.rounded_rectangle([mx - 48, y - 64, mx + 48, y - 26], 10, fill=NAVY)
        d.text((mx, y - 45), "1,25", font=font("PlusJakartaSans-var.ttf", 28, 800), fill=WHITE, anchor="mm")
    dyn.append(marker)
    return dyn

# ---- render ----
ORDER = [s["id"] for s in SCENES]
XFADE = 0.3

def frames_for(tl, sids):
    Ns = {}; cum = 0.0; prev = 0
    for k, sid in enumerate(sids):
        cum += tl[sid]["total"] + (XFADE if k < len(sids) - 1 else 0.0)
        f = round(cum * FPS)
        Ns[sid] = f - prev; prev = f
    return Ns

def video_frames(tl):
    return frames_for(tl, ORDER)

def render_scene(sid, tl, outdir, preview=False, N=None):
    spec = SPEC[sid]
    sprites, dynamics = build_scene(spec, tl)
    total = tl[sid]["total"]
    if N is None:
        N = int(math.ceil(total * FPS))
    os.makedirs(outdir, exist_ok=True)
    cues = tl[sid]["cues"]; starts = tl[sid]["starts"]; durs = tl[sid]["durs"]
    if preview:
        times = sorted({min(total - 0.1, s + d * 0.6) for s, d in zip(starts, durs)} | {total - 0.3})
        frames = [(int(t * FPS), t) for t in times]
    else:
        frames = [(i, i / FPS) for i in range(N)]
    banner = None
    if spec.get("title"):
        banner = sp_banner(spec["title"], spec.get("sub"), hx(spec.get("accent", "#2F6FD0")))
    for i, t in frames:
        base = bg_canvas(spec.get("dark", False))
        brand_mark(base)
        if banner is not None:
            bp = seg(t, 0, 0.3)
            paste_sprite(base, banner, 1030, 78, bp, "mt")
        for sp in sprites:
            p = seg(t, sp["t0"], sp["t0"] + RD)
            paste_sprite(base, sp["im"], sp["x"], sp["y"], p, sp["anchor"])
        d = ImageDraw.Draw(base)
        for fn in dynamics:
            fn(t, base, d)
            d = ImageDraw.Draw(base)
        for j, c in enumerate(cues):
            if starts[j] <= t < starts[j] + durs[j]:
                subtitle_band(d, c["subs"])
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
    only = None
    if "--scene" in args:
        only = args[args.index("--scene") + 1].split(",")
    tl = load_timeline(dry, only)
    sids = only or ORDER
    Ns = frames_for(tl, sids)
    grand = 0
    for sid in sids:
        n = render_scene(sid, tl, f"{FR}/{sid}", preview, None if preview else Ns[sid])
        grand += n
        print(f"{sid} frames={n} total={tl[sid]['total']:.2f}s", flush=True)
    print("RENDER_DONE", grand, "frames", f"{grand / FPS:.1f}s")

if __name__ == "__main__":
    main()
