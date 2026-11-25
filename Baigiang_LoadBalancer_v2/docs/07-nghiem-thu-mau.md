# 07 · Nghiệm thu video mẫu 34,6 giây

**File:** `D:\Edit\Baigiang_LoadBalancer_v2\mau\sample_draft.mp4` (bản nháp, chưa đặt tên final)
**Phụ đề:** `mau\sample.srt` · **Timeline:** `mau\sample_timeline.json`
**Thông số:** 1920×1080 (16:9), 30 fps, H.264 High, AAC 48 kHz mono, 34,57 giây, ~940 kb/s
**Nội dung:** S01 mở đầu → S02 vấn đề một server → S03 khái niệm + trạm thu phí.

| Hạng mục | Trạng thái | Ghi chú + timestamp |
|---|---|---|
| Kiến thức và ví dụ | Đạt | Hook 5.000 người, quá tải 96%/92%, định nghĩa + ẩn dụ trạm thu phí; ví dụ đúng mạch |
| Thuật ngữ và phát âm | Chưa xác minh | Giọng Edge tạm; chưa nghe từng thuật ngữ. Cần nghe lại Load Balancer, request, server |
| Giọng đọc và cảm xúc | Chưa xác minh | Không phải giọng miền Nam cuối cùng; chỉ để duyệt nhịp và phụ đề |
| Giáo viên | Đạt (trên still) | An xuất hiện cả 3 cảnh, đổi pose chỉ tay/đứng/suy nghĩ, không che nội dung; chưa duyệt chuyển động liên tục |
| Hình ảnh, icon, vẽ tay | Đạt (trên still) | Icon Lucide một bộ; nét vẽ tay là stroke reveal mô phỏng, không phải nét cọ thật |
| Sơ đồ, code | Đạt | S01 có topology nhỏ LB → 3 server; S03 có sơ đồ trạm thu phí 3 làn. Mẫu không có cảnh code |
| Đồng bộ hình – tiếng – SFX | Đạt theo số liệu | Cue và SRT khớp timeline: 0:00 / 0:07,97 / 0:13,08 / 0:18,42 / 0:25,54 / 0:30,30. Chưa nghe kiểm |
| Phụ đề | Đạt | Burn-in, tối đa 2 dòng, không che sơ đồ/mặt; .srt xuất kèm |
| Âm thanh/nhạc/SFX | Chưa xác minh | Đo được −14,65 LUFS, true peak −0,86 dBTP; mix peak 0,731. Chưa nghe cân bằng thực tế |
| Thời lượng và định dạng | Đạt | 34,57 s nằm trong 30–45 s; đúng 1920×1080, 30 fps, mp4 |

## Đối chiếu yêu cầu mẫu

| Yêu cầu | Có trong mẫu |
|---|---|
| Intro/lời chào An Tech Academy | Có, 0:00–0:13 |
| Đoạn giảng có thuật ngữ CNTT | Load Balancer, request, server, CPU, RAM |
| Cảnh animation đúng nội dung | Trạm thu phí: xe chạy, điều phối vào 3 làn, 0:30–0:34 |
| Bộ icon | Có (server, users, smartphone, shield, gauge…) |
| Sơ đồ/infographic kỹ thuật | Topology LB → 3 server; sơ đồ trạm thu phí |
| Typography + bảng màu | Be Vietnam Pro / Plus Jakarta Sans, nền sáng + navy/blue/amber |
| Nhân vật giáo viên | An, 3 pose, xuyên suốt |
| Hiệu ứng vẽ tay | Gạch chân "Bộ cân bằng tải", "Chia đều tải"; khoanh cụm LB; khoanh 96% |
| SFX | pop, whoosh, deny, thud, marker, chime, nhạc nền |

## Giới hạn còn lại

- Giọng trong mẫu là Edge `vi-VN-NamMinhNeural` tạm, **không phải** giọng miền Nam của bạn; phát âm và cảm xúc chưa xác minh.
- Chưa kiểm bằng tai đồng bộ tiếng–hình và mức nhạc/SFX; mới kiểm bằng số liệu.
- Mẫu chỉ gồm S01–S03; chưa thể hiện cảnh kiến trúc đầy đủ (S04) và cảnh code Nginx (S09) — sẽ có trong bản full.
- Nét vẽ tay là mô phỏng bằng code, không phải nét cọ vẽ thật.

## Cần bạn quyết

Mẫu đã sẵn sàng để duyệt. Nếu duyệt, bước tiếp theo là thu 6 cue mẫu bằng giọng thật (phiếu ở `docs\06-script-thu.md`), thay vào video mẫu để nghe kiểm, rồi mới sản xuất toàn bộ 10 cảnh.
