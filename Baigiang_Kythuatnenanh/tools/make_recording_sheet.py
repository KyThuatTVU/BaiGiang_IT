# -*- coding: utf-8 -*-
"""Sinh script thu âm 29 cue (HTML + TXT) từ manifest và storyboard."""
import html, json, os, re

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
MAN = ROOT + "/mau/manifest.json"
REF = ROOT + "/mau/tts_state_namminh.json"
STORY = ROOT + "/docs/04-storyboard.md"
OUT = ROOT + "/mau/voice_human"
RAW = OUT + "/raw"

GLOSS = [
    ("An Tếch", "An Tech"), ("A-ca-đê-mi", "Academy"),
    ("i-mịch com-pờ-ré-sần", "Image Compression"),
    ("mê-ga-bai", "MB"), ("ki-lô-bai", "KB"),
    ("lót-xi", "Lossy"), ("lót-lít", "Lossless"),
    ("giây-pê-gờ", "JPEG"), ("guép-pê", "WebP"),
    ("pê-en-gờ", "PNG"), ("ây-víp", "AVIF"), ("ét-vi-giờ", "SVG"),
    ("ro", "RAW"), ("xê-đi-en", "CDN"), ("lây-zi", "lazy"),
    ("lô-đinh", "loading"), ("sooc-sét", "srcset"),
    ("ét-xờ-xê", "src"), ("uých", "width"), ("hai-tờ", "height"),
    ("pích-xồ", "pixel"), ("quoa-li-ti", "quality"),
    ("pro-đớt", "product"), ("ri-sai", "resize"),
    ("sờ-quút", "Squoosh"), ("tai-ni pê-en-gờ", "TinyPNG"),
    ("i-mịch ma-gích", "ImageMagick"), ("sáp", "sharp"),
    ("giây-ét", "JS"), ("en-pi-em", "npm"), ("in-sto", "install"),
    ("gu-i-dao en-lát-mần", "withoutEnlargement"),
    ("tu-phai", "toFile"),
]


def titles():
    t = {}
    if not os.path.exists(STORY):
        return t
    for ln in open(STORY, encoding="utf-8"):
        m = re.search(r"\*\*(S\d+) — ([^*]+)\*\*", ln)
        if m:
            t[m.group(1)] = m.group(2).strip()
    return t


def target(c, ref):
    if c["id"] in ref:
        return ref[c["id"]]["dur"]
    return max(0.8, len(c["say"]) / 17.5)


def main():
    man = json.load(open(MAN, encoding="utf-8"))
    ref = json.load(open(REF, encoding="utf-8")) if os.path.exists(REF) else {}
    tt = titles()
    os.makedirs(RAW, exist_ok=True)
    total = len(man)
    cards = []
    txt = [
        "SCRIPT THU ÂM — NÉN ẢNH TRONG WEBSITE",
        "AN TECH ACADEMY",
        "",
        f"{total} cue. Mỗi cue một file riêng, lưu vào mau\\voice_human\\raw\\",
        "Tên file đúng nhãn: S01c1.wav, S01c2.wav, ... (WAV/M4A/MP3 đều được).",
        "Đọc đúng chữ phiên âm trong ngoặc/phiên âm; không tự sửa chính tả.",
        "Tốc độ hơi nhanh như giảng cho lớp; số giây chỉ là gợi ý.",
        "— ngắt ngắn; … ngắt dài hơn và hạ giọng; ! lên giọng, tươi.",
        "Đầu/cuối file để khoảng 1 giây im lặng; không thêm nghỉ dài giữa câu.",
        "",
    ]
    cur = None
    for i, c in enumerate(man):
        if c["scene"] != cur:
            cur = c["scene"]
            title = tt.get(cur, "Cảnh " + cur)
            cards.append(f'<h2 id="{cur}">{html.escape(cur)} — {html.escape(title)}</h2>')
            txt.append("")
            txt.append(f"[{cur}] {title}")
        sec = target(c, ref)
        say = html.escape(c["say"])
        cid = c["id"]
        cards.append(f'''<article class="card" data-id="{cid}">
  <div class="meta"><span class="file">{cid}</span><span class="target">đích ~{sec:.1f}s</span>
  <label class="chk"><input type="checkbox" data-id="{cid}"> đã thu</label></div>
  <p class="say">{say}</p>
</article>''')
        txt.append("")
        txt.append(f"{cid} (~{sec:.1f}s)")
        txt.append(c["say"])
    gloss = "".join(
        f"<li><b>{html.escape(a)}</b><span>{html.escape(b)}</span></li>" for a, b in GLOSS)

    doc = f'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Script thu âm — Nén ảnh trong website</title>
<style>
:root{{--navy:#1b2a4a;--ink:#0f172a;--red:#dc2626;--amber:#d97706;--bg:#f6f8fb;--mut:#64748b;--line:#e2e8f0}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,"Segoe UI",Roboto,Arial,sans-serif}}
.wrap{{max-width:940px;margin:0 auto;padding:0 18px}}
header{{background:var(--navy);color:#fff;padding:18px 0 14px;position:sticky;top:0;z-index:5;box-shadow:0 2px 10px rgba(15,23,42,.15)}}
.brand{{font-size:12px;letter-spacing:.14em;color:#cbd5e1;font-weight:700}}
h1{{margin:4px 0 6px;font-size:22px;line-height:1.3}}
.sub{{font-size:13px;color:#cbd5e1}} code{{background:#0b1730;padding:1px 5px;border-radius:4px}}
.prog{{margin-top:10px;display:flex;align-items:center;gap:12px;font-size:14px;font-weight:600}}
.prog b{{color:#fbbf24;font-size:18px}}
.prog button{{margin-left:auto;background:transparent;border:1px solid #94a3b8;color:#e2e8f0;border-radius:6px;padding:4px 10px;cursor:pointer;font:inherit;font-size:12px}}
main{{padding:20px 0 60px}}
.guide{{background:#fff;border:1px solid var(--line);border-left:6px solid var(--amber);border-radius:12px;padding:16px 20px;margin:8px 0 22px}}
.guide h3{{margin:0 0 8px;font-size:16px}}
.guide ul{{margin:0;padding-left:20px}} .guide li{{margin:4px 0}}
details{{margin-top:10px}} summary{{cursor:pointer;font-weight:700;color:var(--navy)}}
.gloss{{list-style:none;padding:0;margin:10px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px 18px;font-size:14px}}
.gloss li{{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dotted #cbd5e1;padding:3px 0}}
.gloss span{{color:var(--mut)}}
h2{{font-size:18px;color:var(--navy);margin:30px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--red)}}
.card{{background:#fff;border:1px solid var(--line);border-left:6px solid var(--red);border-radius:12px;padding:14px 18px 16px;margin:12px 0;transition:opacity .15s}}
.meta{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.file{{background:var(--navy);color:#fff;font:700 13px/1 ui-monospace,Consolas,monospace;padding:6px 9px;border-radius:6px;letter-spacing:.04em}}
.target{{background:#fef3c7;color:#92400e;font-size:12px;font-weight:700;padding:4px 8px;border-radius:999px}}
.chk{{margin-left:auto;font-size:13px;color:var(--mut);display:flex;align-items:center;gap:6px;cursor:pointer}}
.chk input{{width:18px;height:18px;accent-color:var(--red);cursor:pointer}}
.say{{margin:10px 0 2px;font-size:21px;line-height:1.75;letter-spacing:.1px}}
.card.done{{opacity:.5;background:#f8fafc;border-left-color:#94a3b8}}
.card.done .say{{text-decoration:line-through;text-decoration-color:#cbd5e1}}
@media (max-width:560px){{.say{{font-size:19px}} h1{{font-size:19px}}}}
@media print{{header{{position:static;background:#fff;color:#000;box-shadow:none}} .prog,.chk{{display:none}} .card{{break-inside:avoid}} body{{background:#fff}}}}
</style></head><body>
<header><div class="wrap">
<div class="brand">AN TECH ACADEMY · SCRIPT THU ÂM</div>
<h1>Nén ảnh trong website — 29 cue</h1>
<div class="sub">Lưu file vào <code>mau\\voice_human\\raw\\</code> · tên đúng nhãn · WAV / M4A / MP3</div>
<div class="prog"><b id="cnt">0</b><span>/ {total} cue đã thu</span><button id="reset">Đặt lại</button></div>
</div></header>
<main class="wrap">
<section class="guide">
<h3>Trước khi thu</h3>
<ul>
<li>Phòng yên tĩnh, tắt quạt/điều hòa nếu được; mic cách miệng 15–20 cm, hơi lệch sang bên.</li>
<li>Mỗi cue thu thành một file, tên đúng nhãn (ví dụ <b>S01c1.wav</b>). Sai thì thu lại và ghi đè.</li>
<li>Đọc <b>đúng chữ phiên âm</b> trong bài (An Tếch, mê-ga-bai, giây-pê-gờ…), không tự sửa lại.</li>
<li>Tốc độ hơi nhanh như đang giảng cho lớp; cột <b>đích</b> chỉ là gợi ý để giữ tổng thời lượng ~5 phút.</li>
<li><b>—</b> ngắt ngắn; <b>…</b> ngắt dài hơn và hạ giọng; <b>!</b> lên giọng, tươi. Đầu/cuối file để ~1 giây im lặng.</li>
<li>Không bật giảm ồn/âm thanh vòng trong app ghi âm; mình xử lý hậu kỳ sau.</li>
</ul>
<details><summary>Từ phiên âm → nghĩa</summary><ul class="gloss">{gloss}</ul></details>
</section>
{"".join(cards)}
</main>
<script>
const KEY='rec_nenanh_v1_';
const boxes=[...document.querySelectorAll('input[type=checkbox]')];
const cnt=document.getElementById('cnt');
function sync(){{let n=0;boxes.forEach(b=>{{const c=b.closest('.card');c.classList.toggle('done',b.checked);if(b.checked)n++;}});cnt.textContent=n;}}
boxes.forEach(b=>{{
  b.checked=localStorage.getItem(KEY+b.dataset.id)==='1';
  b.addEventListener('change',()=>{{localStorage.setItem(KEY+b.dataset.id,b.checked?'1':'0');sync();}});
}});
document.getElementById('reset').addEventListener('click',()=>{{
  if(!confirm('Bỏ đánh dấu tất cả cue?'))return;
  boxes.forEach(b=>{{localStorage.removeItem(KEY+b.dataset.id);b.checked=false;}});sync();
}});
sync();
</script>
</body></html>'''
    open(OUT + "/script_thu.html", "w", encoding="utf-8").write(doc)
    open(OUT + "/script_thu.txt", "w", encoding="utf-8").write("\n".join(txt) + "\n")
    tot = sum(target(c, ref) for c in man)
    print("SHEET_DONE", total, "cues", round(tot, 1), "s speech target")


if __name__ == "__main__":
    main()
