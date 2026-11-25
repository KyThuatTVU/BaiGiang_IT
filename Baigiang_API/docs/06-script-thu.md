# 06 — Khai báo năng lực công cụ & phiếu giọng đọc

## Bước 0 — Năng lực thực tế (Cấp B)

| Việc | Có/Không | Ghi chú |
|---|---|---|
| Render video từ code | **Có** | PIL vẽ frame → ffmpeg encode/xfade/mux |
| Tạo giọng nam miền Nam **thật, có diễn xuất** | **Không** | Không có bản thu người thật trong phiên này |
| Điều khiển cảm xúc/SSML | **Không** | Edge TTS chỉ có `rate`; dùng nhịp câu + dấu câu để tạo nhấn nhá |
| Nghe lại audio để kiểm tra | **Không** | Không có khả năng nghe/phân tích âm thanh |
| Nhân vật giáo viên chuyển động | **Có (giới hạn)** | Vector 2D, đổi tư thế/nhép miệng/chớp mắt, không mocap |
| Hiệu ứng vẽ tay | **Có (mô phỏng)** | Stroke reveal marker, không phải hand-tracking |
| SFX | **Có** | Tổng hợp numpy, không bản quyền |
| Phụ đề khớp audio | **Có (theo timeline đo được)** | SRT sinh từ thời lượng file voice thực tế |

## Giọng đọc dùng trong mẫu

- **Edge TTS `vi-VN-NamMinhNeural`**, rate **+18%**, không pitch-shift.
- Đây là **giọng nam tiếng Việt phổ thông do Microsoft tổng hợp**, **không phải giọng nam miền Nam thu thật** và không có tham số cảm xúc. Dùng làm **bản tạm để duyệt nhịp/hình**, không tuyên bố đạt chuẩn 2.3.
- Để đạt chuẩn "giảng viên thật, dí dỏm": cần **bạn thu giọng** (điện thoại cũng được) theo phiếu dưới, hoặc cấp **token Viettel `hcm-minhquan`** (nam miền Nam, có speed) và tôi chạy theo nhịp.

## Phiếu thu giọng (nếu bạn thu)

- Thiết bị: điện thoại, phòng yên tĩnh, cách miệng 20–25 cm, không dùng tai nghe.
- Đọc **đúng chữ trong `01-kich-ban.md`**, mỗi cue một file: `S01c1.wav`, `S01c2.wav`, …
- Tốc độ: nhanh như đang giảng cho sinh viên (khoảng 1,2 lần đọc tin tức), không đều đều; xuống giọng cuối câu; nhấn từ khóa.
- Giữa các câu: nghỉ 0,3–0,5 s rồi bấm dừng; không cần cắt im lặng thủ công (tôi trim).
- Không đọc phần `[tag]`.
- Đặt file vào `mau/ghi_am/`. Khi có đủ, tôi trim, tính lại timeline và render lại các cảnh bị đổi.

## Những gì tôi **không** được phép tuyên bố

- Không nói "giọng đã chuẩn miền Nam/diễn xuất tốt" khi đang dùng Edge.
- Không nói "đã nghe kiểm phát âm" — chỉ có thể đối chiếu chữ và timeline.
- Không nói "phụ đề khớp 100%" — chỉ khớp theo thời lượng file; cần bạn xem để xác nhận cảm nhận.
