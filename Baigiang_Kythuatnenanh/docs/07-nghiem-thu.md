# Nghiệm thu bản full — 2026-11-22

File giao: `mau/full.mp4` (H.264/AAC, 1920×1080, 30 fps, 5:03,20) và `mau/full.srt` (29 cue).

| Hạng mục | Kết quả đo | Kết luận |
|---|---|---|
| Thời lượng | 303,20 s (5:03,2), đích 4:45–5:15 | Đạt |
| Hình | 1920×1080, 30 fps, H.264 High, 12 cảnh, xfade 0,6 s | Đạt |
| Ảnh | 17/17 PNG được dùng trong 12 cảnh (kiểm tra contact sheet) | Đạt |
| Nhận diện | Logo/chữ AN TECH ACADEMY xuất hiện trên các cảnh | Đạt |
| Lời thoại | 29/29 cue từ manifest, đúng timeline | Đạt |
| Phụ đề | 29/29 cue, lệch so với timeline < 0,02 s | Đạt |
| Audio | −14,47 LUFS, true peak −1,81 dBFS, không clipping | Đạt |
| Nhạc/SFX | Nhạc tạo bằng code, không dùng nhạc ngoài có bản quyền | Đạt |
| Giọng nam Nam Bộ | Dùng Edge `vi-VN-NamMinhNeural` (giọng Bắc), không pitch | **Không đạt** — fallback có ghi nhận, xem `06-giong-doc.md` |
| Phát âm thuật ngữ | Công cụ không nghe được | **Chưa xác minh** |
| Ngữ điệu/cảm xúc | Giọng TTS đều, chưa có bản thu người so sánh | **Chưa xác minh** |
| Đồng bộ A/V | Một timeline chung cho voice, SRT và hình; kiểm tra cấu trúc khớp | Đạt (theo cấu trúc) |

## Ghi chú kỹ thuật

- Video gắn cờ màu full-range (`yuvj420p/pc` do khung JPEG gốc); trình phát đọc đúng, nhưng nếu upload nền tảng tự ép TV-range thì nên kiểm tra lại màu.
- Bản nháp trung gian: `mau/full_draft.mp4`, `mau/full_video.mp4`, `mau/full_voice.wav`, `mau/full_audio.m4a`.
- Contact sheet QA: `mau/qa/contact_sheet.jpg`.

## Việc còn lại trước khi phát hành

1. Người nghe duyệt phát âm thuật ngữ và ngữ điệu (bắt buộc, vì chưa xác minh được bằng công cụ).
2. Nếu cần đúng quy chuẩn giọng Nam: thu người thật theo `mau/voice_human/script_thu.html` rồi chạy `tools/voice_human_prep.py`, sau đó mix/ghép lại.
