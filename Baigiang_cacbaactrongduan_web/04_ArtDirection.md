# ART DIRECTION & BẢNG MÀU — CỔNG A
## Bên trong một dự án phát triển phần mềm

*MASTER 2.3 · XII Clean Visual System · 18/11/2026 · Chờ duyệt*

## 1. Bảng màu (60-30-10, chủ đề tổ chức/con người/quy trình)

| Vai trò | Màu | Hex | Dùng cho |
| --- | --- | --- | --- |
| Nền (60%) | Giấy sáng | #F6F8FB | nền chính; thẻ trắng #FFFFFF |
| Chủ đạo (30%) | Navy đậm | #1B2A4A | tiêu đề, khung sơ đồ, nhân vật, chữ chính |
| Thông tin | Xanh dương | #2563EB | connector, nhãn nhóm quản lý, link dữ liệu |
| Nhấn (10%) | Amber | #F59E0B | nét vẽ tay, highlight từ khóa, CTA, thẻ nhấn |
| Chức năng | Xanh lá / Đỏ | #16A34A / #DC2626 | đạt/lỗi, pass/fail (chỉ dùng đúng ngữ cảnh) |
| Trung tính | Xám nhạt | #E2E8F0 / #64748B | viền, chú thích |

- Nhóm chức năng sơ đồ: lãnh đạo = navy; quản lý dự án = xanh dương; chuyên môn = teal #0D9488; phát triển = amber đậm #D97706. Giữ nhất quán từ S04→S17.
- Không gradient trang trí, không neon/glow tràn lan; bóng đổ thẻ rất nhẹ (0 2px 8px rgba(15,23,42,.08)) để tách lớp, không tạo cảm giác nhựa.
- Tương phản chữ/nền kiểm bằng script trước khi render (đã có công cụ từ dự án trước).

## 2. Typography (kế thừa font đã tải, giấy phép OFL trong assets)

| Thành phần | Font | Cỡ (1080p) |
| --- | --- | --- |
| Tiêu đề chính | Be Vietnam Pro Bold | 56 |
| Tiêu đề phần | Be Vietnam Pro SemiBold | 44 |
| Nội dung | Be Vietnam Pro Regular/Medium | 28–30 |
| Chú thích/nhãn sơ đồ | Plus Jakarta Sans | 22–24 |
| Code/kỹ thuật (GET /api…, JSON) | JetBrains Mono | 24–26 |
| Phụ đề đốt video | Be Vietnam Pro Medium | 30, tối đa 2 dòng, nền bán trong navy 70% |

Vùng an toàn 5%; phụ đề cách đáy 60px, không che nhân vật/nội dung.

## 3. Icon

- Bộ **Lucide** (giấy phép ISC, đã có trong workspace) — nét 2px, bo tròn, đồng nhất; dùng bản SVG gốc, tô màu theo bảng màu; kích thước 48–96px trong thẻ, 28px trong nhãn.
- Không emoji thay icon; không icon 3D bóng nhựa; không phóng raster.
- Icon cần mới (vai trò): dựng SVG cùng hệ nét 2px (ví dụ sponsor = hand-coins, tech lead = git-branch+user).

## 4. Character sheet — giáo viên "An" (BẮT BUỘC 2.3 XVIII)

- **Nhận diện:** nam, trẻ (~25 tuổi), tóc ngắn đen gọn, không kính; áo sơ mi xanh navy #1B2A4A xắn tay, thẻ tên amber "AN" ngực trái, quần âu sáng #334155, giày trắng; cầm bút marker amber ở tay phải khi viết bảng.
- **Phong cách:** vector phẳng 2D, nét viền navy 3px, tỷ lệ thân ~1:4.5 (hơi chibi vừa phải, không trẻ con hóa), không đổ bóng nhựa, không highlight giả.
- **Tư thế (5 pose + wave):** idle-standing (2 tay thả lỏng), present (2 tay mở về nội dung), point-left, point-right (tay chỉ đúng hướng nội dung đang giảng), think (tay chống cằm), wave (chào kết). Chuyển pose bằng crossfade 6 frame + cử chỉ tay animate trong pose (nhẹ, có điểm dừng).
- **Nhất quán:** MỘT file SVG gốc duy nhất, mọi cảnh dùng chung; chỉ đổi transform nhóm tay/đầu, không vẽ lại nhân vật khác. Không đổi trang phục/màu giữa cảnh.
- **Bố cục:** mặc định góc trái dưới cao ~380px; cảnh sơ đồ/code (S10, S13) thu nhỏ ~240px hoặc dời góc phải; không bao giờ che chữ/code/phụ đề.
- **Giới hạn công bố:** đây là animation 2D theo tư thế + cử chỉ tay, không phải rig nhân vật 3D hay full character animation.

## 5. Hiệu ứng vẽ tay (18.3)

- Kỹ thuật: SVG path + stroke-dashoffset reveal theo frame, nét marker amber 5px, đầu nét tròn, tốc độ ~600px/s, có điểm bắt đầu/kết thúc.
- Dùng cho: gạch chân từ khóa định nghĩa (S02), connector sơ đồ 4 nhóm (S04), khoanh đáp án quiz (S16), mũi tên quan hệ ERD (S11), timeline 6 giai đoạn (S13).
- Đồng bộ: nét bắt đầu đúng cue lời tương ứng; tiếng bút marker chỉ phát trong khoảng nét đang vẽ.
- Không vẽ trang trí liên tục; không dùng vẽ tay thay sơ đồ kỹ thuật chính xác (sơ đồ dựng sẵn, chỉ connector/underline vẽ tay).

## 6. Chuyển động & chuyển cảnh (VI + 12.7)

- Thành phần: fade+scale nhẹ (0.96→1), slide có easing cubic, data-flow gói tin chạy dọc connector đúng chiều, highlight đúng đối tượng được nhắc.
- Camera: pan/zoom rất nhẹ có chủ đích (S13 pan theo timeline); không rung, không zoom vô cớ.
- Chuyển cảnh: crossfade 0.3s nhất quán + whoosh ngắn ≤0.25s; không glitch/nhấp nháy.
- Không quá 3 nhóm chuyển động đồng thời; mọi chuyển động có điểm dừng quan sát.

## 7. Thiết kế âm thanh (VIII + 18.4)

- **Voice:** lớp ưu tiên cao nhất, chuẩn hoá −14 LUFS toàn video.
- **Nhạc nền:** tự soạn bằng tổng hợp (pad ấm + pluck arpeggio nhịp ~84 BPM, không lời), mức ~−26 LUFS, ducking nhẹ khi voice; không dùng nhạc có bản quyền. Công bố: nhạc tổng hợp đơn giản, không phải phối khí phòng thu.
- **SFX tự tổng hợp (numpy, không bản quyền), mỗi loại 1 biến thể ngắn sạch:**
  | SFX | Đặc tính | Dùng khi |
  | --- | --- | --- |
  | marker | noise lọc dải hẹp, ~0.3–0.8s theo độ dài nét | nét vẽ tay đang chạy |
  | pop | sine burst 600→900Hz, 60ms | thẻ/icon xuất hiện |
  | whoosh | noise sweep bandpass, 200ms | chuyển cảnh, gói tin bắt đầu chạy |
  | click | impulse 2kHz 15ms | nhấn nút, kéo task, chọn lựa |
  | tick | woodblock nhẹ 1kHz 30ms | checklist tick, đồng hồ quiz |
  | chime | 2 nốt hợp âm trưởng (E5+A5) 300ms | chốt ý, đáp án đúng, thương hiệu |
- Mật độ: chỉ phát khi có hành động tương ứng trên màn hình; không SFX cho mọi chuyển động nhỏ; voice không bị che (SFX ≤ −20 LUFS tức thời).

## 8. Nhận diện thương hiệu

- Intro: chữ "AN TECH ACADEMY" stroke reveal + tagline "Học công nghệ cùng An"; outro cùng hệ. Không tự vẽ logo hình nếu người dùng chưa cung cấp — dùng wordmark chữ.
- Watermark góc phải trên: wordmark nhỏ 120px, opacity 60%, xuyên suốt (không chiếm diện tích lớn).