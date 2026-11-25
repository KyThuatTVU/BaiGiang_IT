# -*- coding: utf-8 -*-
"""Sinh docs/kich-ban + storyboard từ manifest (thời lượng ước tính trước khi có TTS)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_manifest import CUES, SCENES

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
WPS = 3.15          # từ/giây ước tính (NamMinh + rate 8..15%)
GAP, TAIL, XF = 0.30, 1.0, 0.3

def fmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"

# --- dựng timeline ước tính
sc = {}
for cid, sid, rate, semi, pause, text, subs in CUES:
    sc.setdefault(sid, []).append((cid, rate, pause, text, subs))

tl = {}
for sid, cues in sc.items():
    starts, durs, t = [], [], 0.0
    for i, (cid, rate, pause, text, subs) in enumerate(cues):
        if i:
            t += GAP + cues[i - 1][2]
        d = len(text.split()) / WPS
        starts.append(t); durs.append(d); t += d
    tl[sid] = {"starts": starts, "durs": durs, "total": t + TAIL}

order = [s[0] for s in SCENES]
offs, cum = {}, 0.0
for k, sid in enumerate(order):
    offs[sid] = cum - XF * k
    cum += tl[sid]["total"]
runtime = cum - XF * (len(order) - 1)

# --- kịch bản
lines = ["# Kịch bản giảng dạy — Kỹ thuật nén ảnh trong website",
         "",
         f"*Thời lượng ước tính: **{fmt(runtime)}** (chốt theo file thoại thật sau khi TTS). "
         f"29 cue / 12 cảnh. Giọng: nam, tiết tấu nhanh 8–15% so với đọc thường.*",
         "",
         "| # | Cảnh | Thời gian | Lời thoại | Phụ đề | rate |",
         "|---|---|---|---|---|---|"]
idx = 0
for sid, cues in sc.items():
    for j, (cid, rate, pause, text, subs) in enumerate(cues):
        idx += 1
        t0 = offs[sid] + tl[sid]["starts"][j]
        lines.append(f"| {idx} | {sid} | {fmt(t0)} | {text} | {' / '.join(subs)} | {rate} |")
lines += ["", "## Câu dẫn tương tác & nhịp", "",
          "- Mở đầu: câu hỏi tình huống (30 ảnh × 5 MB) tạo tò mò.",
          "- Giữa bài: “Các bạn đã bao giờ bỏ đi vì chờ quá lâu chưa?”, “Được cái này, mất cái kia — đúng không?”, “Nhớ nhé!”.",
          "- Chuyển phần: mỗi cảnh mở bằng một câu hỏi hoặc một khẳng định ngắn, không đọc tiêu đề khô.",
          "- Kết: chốt 4 điều + câu khuyến khích thực hành + nhắc thương hiệu + hẹn bài sau.",
          "",
          "## Ghi chú số liệu (bắt buộc đọc đúng bản chất)", "",
          "- 30 ảnh × 5 MB = 150 MB: ví dụ giả định trong tài liệu.",
          "- 5 MB → 350 KB (−93%): **số liệu giả định** của tài liệu để minh họa.",
          "- 128 / 512 / 78 / 45 KB: số liệu của infographic so sánh 4 định dạng, không phải benchmark cho mọi ảnh.",
          "- 618 KB → 194 KB: đọc từ biểu đồ (quality 90 → 50) của tài liệu; không đọc dòng “112 MB” vì đó là lỗi in của infographic.",
          ""]
open(ROOT + "/docs/02-kich-ban.md", "w", encoding="utf-8").write("\n".join(lines))

# --- storyboard
lines = ["# Storyboard — Kỹ thuật nén ảnh trong website", "",
         f"*Tổng: {fmt(runtime)} · 12 cảnh · 29 cue. 1920×1080, 30 fps. "
         f"Chuyển cảnh xfade 0,3 s. Nhân vật An xuất hiện xuyên suốt.*", "",
         "| Cảnh | Thời gian | Lời thoại (cue) | Hình ảnh | Chuyển động | Chữ trên màn hình | Âm thanh |",
         "|---|---|---|---|---|---|---|"]
for sid, title, part, visual, anim, screen, sfx in SCENES:
    t0 = offs[sid]; t1 = t0 + tl[sid]["total"] - (XF if sid != order[-1] else 0)
    q = " · ".join(c[3][:64] + ("…" if len(c[3]) > 64 else "") for c in sc[sid])
    lines.append(f"| **{sid} — {title}** | {fmt(t0)}–{fmt(t1)} | {q} | {visual} | {anim} | {screen} | {sfx} |")
lines += ["", "## Nguyên tắc dựng", "",
          "- Mỗi cảnh một thông điệp; chữ trên màn hình chỉ là từ khóa, không chép lời thoại.",
          "- Ảnh gốc của tài liệu luôn nằm trong khung chứng cứ có nhãn; không dùng ảnh chỉ để trang trí.",
          "- Sơ đồ, pipeline, code, ma trận chọn định dạng tự dựng bằng vector/PIL, không để AI vẽ chữ.",
          "- Nhân vật An: 6 tư thế, cử chỉ chỉ vào nội dung, mấp máy môi khi nói, không che chữ/phụ đề.",
          "- Nét marker vẽ dần đồng bộ lời giảng; SFX khớp hành động, không lấn giọng.",
          "- Phụ đề 2 dòng, đặt trong dải navy đáy khung, giữ vùng an toàn 5%.",
          ""]
open(ROOT + "/docs/04-storyboard.md", "w", encoding="utf-8").write("\n".join(lines))
print("DOCS_OK", fmt(runtime), "scenes", len(order), "cues", len(CUES))
