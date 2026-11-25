# D:\Edit\Kit — kho code và tài nguyên dùng chung

Một nơi duy nhất để chỉnh sửa code chung cho mọi video AN TECH ACADEMY.
Dự án chỉ **import** từ đây, không copy thư viện.

## Cây thư mục

```
tools/
  core.py        khung dựng: bảng màu, font, primitive, timeline, nét bút tay
  demo20.py      helper giao diện: thẻ, khung JSON, chip, caption, chuyển động
  sfx.py         âm thanh hiệu ứng tổng hợp bằng numpy (không bản quyền)
  character.py   nhân vật giáo viên An: vector 2D, 7 tư thế, nhép miệng, chớp mắt
  tts.py         Edge TTS theo manifest, chạy tiếp được khi bị ngắt
  tts_vieneu.py  TTS giọng clone cục bộ (VieNeu-TTS) → WAV 48 kHz, cùng kiểu manifest
  prep_icons.py  SVG → PNG đen → PNG nhuộm màu; hàm icon_rgba(name, "#hex")
  icons/         logo React / Node.js / MySQL
assets/
  fonts/         Be Vietnam Pro, Plus Jakarta Sans, JetBrains Mono (giấy phép OFL)
  icons/         bộ icon SVG gốc (92 icon)
  icons_black/   PNG đen đã raster từ SVG
  icons_png/     cache PNG theo từng màu
cache/           sinh tự động (sfx/, icons_html/, ref_voice/) — không sửa tay
```

## Dùng trong dự án

Đặt `PROJECT_ROOT` trước khi import (mặc định `D:/Edit/Baigiang_API`):

```python
import os, sys
os.environ.setdefault("PROJECT_ROOT", r"D:\Edit\<TenBai>")
sys.path.insert(0, r"D:\Edit\Kit\tools")
import core, sfx, character
```

- `core.FULL` = `<PROJECT_ROOT>/mau` — nơi chứa manifest, audio, frames, video của bài.
- Font và icon luôn đọc từ Kit; SFX cache ở `Kit/cache/sfx`.
- Dự án cũ giữ nguyên lệnh chạy: các file `tools/core.py`, `demo20.py`, `sfx.py`,
  `character.py`, `prep_icons.py`, `tts.py` trong dự án chỉ là **cầu nối** tự nạp bản
  thật trong Kit. Sửa code chung tại Kit, không sửa cầu nối.

## Thêm icon mới

1. Bỏ file `.svg` vào `assets/icons/` (line icon, đúng bộ đang dùng).
2. Chạy `python tools/prep_icons.py` — cần Microsoft Edge để raster SVG.
3. Dùng trong code: `icon_rgba("ten-icon", "#22D3EE")` hoặc `core.sp_icon(...)`.

## Logo và bản quyền

- Ảnh gốc: `assets/brand/logo_an.png` (1254×1254). Bản dùng trong video:
  `assets/brand/logo_an_round.png` — cắt tròn, nền trong suốt, viền glow giữ nguyên.
- Trong code cảnh, dán huy hiệu có pop/fade:
  `core.paste_brand(base, x, y, size=180, p=tiến_trình, anchor="mm")`.
- Dán cố định một góc khung hình: `core.brand_watermark(base, size=110, pos="tr")`.
- Video đã render — dán logo không đụng bản gốc:

```bash
python D:\Edit\Kit\tools\stamp_logo.py "D:\Edit\<Bai>\mau\video.mp4" --pos tr --dy 60 --size 150 --alpha 0.9
# → xuất video_logo.mp4 cạnh file gốc
```

Với bố cục AN TECH 1920×1080 (header trái, nhãn phiên bản phải): dùng
`--pos tr --dy 60` để logo nằm dưới nhãn phiên bản; `--alpha 0.9`; size 140–160.

## Giọng clone cục bộ (VieNeu-TTS) — chuẩn từ 24/11

Giọng clone là **mặc định** cho bài giảng (người dùng đã duyệt V13); Edge TTS chỉ còn là
phương án dự phòng (`VOICE_BACKEND=edge`).

- Giọng mẫu chốt: `cache/ref_voice/ref_final.wav` — 6,06 s, hai câu trọn, nam miền Bắc.
- Chạy thử một câu:
  `python D:\Edit\Kit\tools\tts_vieneu.py --text "Xin chào" --out thu.wav`
- Chạy theo manifest (WAV từng cue + `state.json`):
  `python D:\Edit\Kit\tools\tts_vieneu.py --manifest manifest.json --out <thư mục>`
- Trong code: `import tts_vieneu; tts_vieneu.synth(text, "cue.wav")` — model nạp một lần
  (~20–45 s), mỗi câu ~0,3–0,6× thời lượng thực trên CPU 16 nhân.
- Env: `VIENEU_REF`, `VIENEU_PRECISION` (`int8` mặc định, `fp32` chậm hơn ~1,5×),
  `VIENEU_THREADS` (mặc định 8). Bản int8 đã đo RTF 0,32–0,42.
- Thuật ngữ IT nên viết nguyên tiếng Anh (`Client`, `Node.js`, `MySQL`); riêng từ
  đứng một mình rất ngắn ("API.") nên dùng phiên âm `Ây pi ai.` — đã kiểm bằng ASR.
- Audio có watermark PerTh mặc định của VieNeu; không nghe thấy, giữ nguyên.

## Mẫu triển khai đã duyệt

`D:\Edit\Baigiang_API\tools\demo30.py` — 30 giây, chuyển động + SFX + nhân vật An;
video tham chiếu `Baigiang_API\mau\demo30_vieneu\api_pro_demo30_an.mp4` (V13, giọng clone).
Mặc định `VOICE_BACKEND=vieneu`; bản Edge cũ (V11/V12) vẫn dựng lại được bằng
`VOICE_BACKEND=edge` và giữ nguyên trong `mau/demo30/`.
Đọc file này để biết cách nối Kit vào một bài cụ thể.
