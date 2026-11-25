# Baigiang_API — bổ sung cho chuẩn chung

Đọc theo thứ tự: `D:\Edit\MASTER_DESIGN_VOICE_STANDARD_2.3.md` (quy chuẩn chính) → `D:\Edit\AGENTS.md` (cách nhận bài) → file này (phần riêng của dự án).

## Bài & bản mẫu

- "API là gì và nó chạy như thế nào" — 11 cảnh, 32 cue (~5 phút).
- Mẫu 30 s: **chuẩn đã chốt 24/11 = V13 giọng clone + An + SFX** — `mau/demo30_vieneu/api_pro_demo30_an.mp4` (30,40 s). V11/V12 (Edge) giữ nguyên làm lịch sử.
- Bản full 11 cảnh cũ đã bị trả lại; phải làm lại theo chuẩn trước khi tái sử dụng.

## Điều chỉnh riêng đã duyệt

- **Font:** Be Vietnam Pro + JetBrains Mono trong bản demo (tương đương theo MASTER vì bộ font chung chưa có Quicksand); không dùng font thiếu dấu.
- **Voice:** chuẩn là **giọng clone cục bộ** (VieNeu-TTS) — `Kit/tools/tts_vieneu.py`, giọng mẫu `Kit/cache/ref_voice/ref_final.wav` (6,06 s từ video người dùng). `demo30.py` mặc định `VOICE_BACKEND=vieneu`; Edge `vi-VN-NamMinhNeural` +12% chỉ còn là dự phòng (`VOICE_BACKEND=edge`, bảng phiên âm `SEGS`/`TERMS_VN`). Chữ thuật ngữ để nguyên tiếng Anh; riêng "API." đứng một mình dùng "Ây pi ai."; cue khó tạo nhiều take, chọn bằng ASR. V13 đã được người dùng chốt ngày 24/11 (nghe bằng tai — agent chưa từng nghe).
- **Âm thanh:** không nhạc nền (yêu cầu riêng của bài này); SFX tổng hợp đồng bộ từng hành động, bus đỉnh 0,22; loudness −14 LUFS, TP ≤ −1.
- **Nhân vật An:** có mặt trong toàn bộ cảnh full (theo MASTER mục XVIII); nền tối tech như demo30.

## Mã & dữ liệu

- **Code chung:** `D:\Edit\Kit\tools` — `core.py`, `demo20.py`, `sfx.py`, `character.py`, `tts.py`, `prep_icons.py`; font/icon ở `D:\Edit\Kit\assets`. Sửa code chung tại Kit.
- Trong `tools\` của dự án, các file trùng tên trên chỉ là **cầu nối** tự nạp bản Kit — không sửa các file này.
- **Code riêng bài này:** `tools\demo30.py` (mẫu tham chiếu đã duyệt: motion + SFX + An), `tools\scenes_api.py` (11 cảnh cũ), các script build/QA.
- Ảnh bài giảng: `img/`; tài liệu lịch sử: `docs/00–07`.
- Chạy lại mẫu: `cd tools && AN_DEMO=1 python demo30.py` — lưu ý ghi đè file trong `mau/demo30/`, đổi `OUT` trước nếu cần giữ bản cũ.
