# Nghiệm thu bản nháp FULL — Load Balancer (10 cảnh)

Ngày: 2026-11-23 · File: `mau/full_draft.mp4` · Phụ đề: `mau/full.srt` · Timeline: `mau/full_timeline.json`

## Thông số kỹ thuật đo được

| Hạng mục | Giá trị |
|---|---|
| Thời lượng | 4:40,30 (280,29 s) |
| Hình | H.264 High, 1920×1080, 30 fps, yuvj420p |
| Tiếng | AAC LC, 48 kHz, mono, 174 kb/s |
| Loudness | −14,60 LUFS, true peak −0,87 dBTP (đo sau ghép) |
| Mean / max volume | −14,2 dB / −0,9 dB |
| Dung lượng | 25,6 MB |
| Cảnh / cue | 10 cảnh / 28 cue |
| Phụ đề | 28 block, block cuối kết thúc 4:39,3 |

## Bảng nghiệm thu 10 mục

| # | Tiêu chí | Kết quả | Ghi chú |
|---|---|---|---|
| 1 | Đủ nội dung 10 cảnh, 28 cue theo kịch bản | Đạt | Đối chiếu `manifest.json` ↔ `full.srt` |
| 2 | Hình ảnh đúng chuẩn 1920×1080 30 fps | Đạt | Kiểm bằng ffmpeg stream info |
| 3 | Bố cục 10 cảnh không tràn/che chữ | Đạt sau sửa | Soát 19 still từ bản ghép; sửa 1 lỗi S06 (xem dưới) |
| 4 | Phụ đề khớp timeline, không chồng block | Đạt | 28 block, không block nào end ≤ start |
| 5 | Loudness chuẩn nền tảng | Đạt | −14,6 LUFS / −0,87 dBTP |
| 6 | Chuyển cảnh xfade 0,4 s đúng mốc | Đạt | Offset tính theo tổng frame từng cảnh; đã soát still quanh 9 mốc |
| 7 | Giọng đọc đúng yêu cầu (người thật, Nam bộ) | **Chưa đạt** | Bản nháp dùng Edge `vi-VN-NamMinhNeural` làm giọng tạm; chờ 28 file thu trong `mau/ghi_am` |
| 8 | Phát âm thuật ngữ (Nginx, HAProxy, IP Hash…) | **Chưa thể xác minh** | Chưa nghe kiểm từng cue; sẽ soát khi có giọng người |
| 9 | Cảm xúc / nhịp đọc | **Chưa thể xác minh** | Giọng tạm không đại diện cho bản thu người thật |
| 10 | Cân bằng voice – SFX – nhạc nền | **Chưa thể xác minh** | Mới đo loudness tổng; chưa nghe kiểm chi tiết từng cảnh |

## Lỗi đã phát hiện và sửa trong QA

- **S06 — tab thuật toán sáng sai**: trong đoạn giảng Round Robin, tab “Weighted RR” đã được highlight từ đầu cue 2. Đã sửa điều kiện highlight (`scenes_web.py`, `draw_S06`: chuyển tab khi vào cue 3), render lại 934 frame S06 và ghép lại bản nháp. Đã xác nhận bằng still tại t=148 (Round Robin) và t=165 (Weighted RR).

## Điểm cần lưu ý

- Toàn bộ giọng trong bản nháp là **giọng tạm Edge**, không phải bản thu người thật đã chốt. Khi thay giọng, thời lượng cue thay đổi → phải trim lại, tính lại timeline, render lại các cảnh bị ảnh hưởng.
- Các animation trong cảnh chạy theo `starts` của timeline; nếu độ dài cue thay đổi nhiều, cần soát lại các mốc: S03 (xe qua trạm), S06 (đổi tab RR→WRR), S07 (đổi tab LC→IP Hash), S08 (S02 lỗi → phục hồi).
- Chưa kiểm bằng tai: phát âm, ngắt nghỉ, SFX có bị rè/ồn hay không.

## File bàn giao

- `mau/full_draft.mp4` — bản nháp 10 cảnh
- `mau/full.srt` — phụ đề tiếng Việt
- `mau/full_timeline.json` — mốc thời gian từng cue
- `mau/full_voice.wav` — track voice+SFX+nhạc trước loudnorm
- `mau/qa_full/` — still QA các mốc chuyển cảnh
- `mau/ghi_am/` — thư mục chờ 28 file thu giọng người thật
