# ART DIRECTION & BẢNG MÀU — KHÁM PHÁ CÁC CHUYÊN NGÀNH CNTT

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.2 (mục 2, 5) · Bản trình Cổng A · 12/11/2026*
*Tương phản dưới đây được tính bằng công cụ (script WCAG) ngày 12/11/2026 trên đúng mã màu đề xuất — không phải ước lượng mắt.*

## 1. Phong cách (5.2, 5.6)

- Clean, modern, editorial, technology-focused; phẳng 2D, vector sắc nét, line icon, infographic kỹ thuật; bố cục thoáng, nhiều khoảng trắng.
- Nền sáng mặc định cho video này (chủ đề hướng nghiệp, đối tượng học sinh–sinh viên): nền #F8FAFC, panel #FFFFFF.
- Không trẻ con hóa: **không nhân vật dẫn chuyện** (mặc định 5.4), không chibi, không 3D nhựa, không emoji thay icon.
- Mỗi cảnh: 1 màu chủ đạo (màu chuyên ngành) + 1 màu nhấn ngữ nghĩa khi cần + trung tính; tối đa 3 màu ngữ nghĩa.
- Bóng đổ: tối đa 1 lớp, độ đục ≤ 12% (ngưỡng 5.6 là 20%; chọn thấp hơn). Bo góc: card 16 px, chip 8 px, nút tròn cho bản đồ. Không gradient trang trí; không glow/blur/glass; không 3D.
- Mood board đúng/sai sẽ dựng ở bước mẫu (Cổng B): đúng = sơ đồ vector phẳng + line icon + bảng màu giới hạn; sai = khối phồng bóng nhựa, gradient cầu vồng, chibi, glow tràn lan.

## 2. Typography (2.1, 2.2)

| Vai trò | Font | Cỡ dùng trong video (px @1080p) |
| --- | --- | --- |
| Tiêu đề chính / wordmark / số nổi bật | Plus Jakarta Sans (Bold/ExtraBold) | 56–72 |
| Tiêu đề phần | Plus Jakarta Sans Bold | 44–52 |
| Tiêu đề phụ / nhãn khối | Plus Jakarta Sans SemiBold | 34–40 |
| Nội dung, bullet, chip, nhãn sơ đồ | Be Vietnam Pro (Regular/Medium) | 28–36 |
| Phụ đề | Be Vietnam Pro Medium | 32 |
| Code (nếu phát sinh) | JetBrains Mono | 26–30 |

- Wordmark dùng Plus Jakarta Sans Bold; **đề xuất bỏ Quicksand** khỏi dự án (mục [CẦN CHỐT] 0.5) để giữ 3 font đúng art direction editorial.
- Font chưa cài trên máy dựng; sẽ tải từ Google Fonts (giấy phép SIL OFL) khi vào sản xuất và ghi nhật ký tài sản. Phương án dự phòng nếu offline: Segoe UI (sans-serif, đủ dấu tiếng Việt) — ghi rõ lệch chuẩn vào hồ sơ.
- Khoảng cách dòng 1,35–1,45; vùng an toàn 5% khung (96 px ngang, 54 px dọc); mọi chữ thông tin ≥ 28 px.

## 3. Icon (5.5)

- Bộ đề xuất: **Lucide** (giấy phép ISC — sẽ kiểm tra bản mới nhất và ghi nhật ký khi tải). Phương án thay thế: Phosphor, Tabler.
- Một bộ duy nhất toàn video; nét 2 px trên lưới 24 px, đầu nét tròn, bo góc nhất quán; dùng SVG gốc, không phóng raster.
- Icon dùng trong storyboard: monitor, server, database, shield-check, bar-chart-3, search, pen-tool, code-2, bug, wrench, check-circle, brain, hammer, play, shopping-cart, history, cpu, credit-card, file-warning, server-off, scan-search, eye, ban, lock, briefcase (thay cho "briefing" — không có trong bộ 1.72.0), settings-2, file-text, puzzle, building-2, handshake, network, wifi, server-cog, cloud, clock, gamepad-2, box, clapperboard, cog, glasses, palette, arrow-right, message-circle, rocket, book-open, refresh-cw, lightbulb.
- Icon rõ ở kích thước hiển thị tối thiểu 48 px trên khung 1080p.

## 4. Bảng màu + tương phản đã tính (5.9, 2.3)

Nền: #F8FAFC (chính), #FFFFFF (panel). Chữ chính #0F172A (17.06:1 trên nền), chữ phụ #475569 (7.24:1). Màu thương hiệu đề xuất [CẦN CHỐT]: #2563EB.

| Vai trò | Mã màu | Tương phản trên #F8FAFC | Dùng làm chữ? | Biến thể chữ an toàn (tương phản) |
| --- | --- | --- | --- | --- |
| CNPM / thương hiệu | #2563EB | 4.94 | Có (≥4.5) | #1D4ED8 (6.41) khi cần đậm hơn |
| KHDL & AI | #7C3AED | 5.45 | Có | #6D28D9 (6.79) |
| An toàn thông tin | #DC2626 | 4.62 | Có | #B91C1C (6.18) |
| Hệ thống thông tin | #D97706 | 3.04 | **Không** — chỉ hình/đồ họa | #B45309 (4.80) |
| Mạng & Cloud | #0284C7 | 3.91 | **Không** — chỉ hình/đồ họa | #0369A1 (5.67) |
| Đồ họa & Game | #0D9488 | 3.58 | **Không** — chỉ hình/đồ họa | #0F766E (5.23) |
| Ngữ nghĩa success | #16A34A | 3.15 | **Không** | #15803D (4.79) |

Quy tắc chip/nền đặc (đã tính chữ trắng trên màu): trắng trên #2563EB = 5.17 ✓, #7C3AED = 5.70 ✓, #DC2626 = 4.83 ✓; với #D97706, #0D9488, #16A34A dùng **chữ tối #0F172A** (5.60 / 4.77 / 5.42 ✓); riêng #0284C7 chữ tối chỉ 4.36 ✗ → chip Mạng dùng nền #0369A1 chữ trắng (5.93 ✓).
Màu nhấn ngữ nghĩa: warning #D97706 (chữ #B45309), danger #DC2626 (chữ #B91C1C), success #16A34A (chữ #15803D). Không dùng màu bão hòa thứ tư trong cùng cảnh.

## 5. Chuyển động (5.10) — gắn với năng lực công cụ thật

- Làm được và sẽ dùng: reveal tuần tự (fade + scale 0,9→1 ≤ 200 ms), connector vẽ theo lời (stroke-dashoffset), data-flow chấm chạy trên connector, highlight khối đang nói, parallax trượt một chiều, đếm ngược stroke, chuyển cảnh fade/slide 300 ms nhất quán.
- Dựng bằng: chuỗi khung PNG sinh từ HTML/CSS (headless Edge) hoặc Pillow cho chuyển động tham số; ghép và chuyển cảnh bằng ffmpeg (xfade/overlay). Đã kiểm tra headless Edge xuất khung 1920×1080 ngày 12/11/2026.
- Có điều kiện, mặc định KHÔNG dùng: motion blur, light sweep, glow, particle, 3D layer, cinematic transition — chỉ thêm nếu bước mẫu chứng minh lý do thị giác rõ và đạt 5.6.
- Không xoay/nảy/rung/lắc/zoom lặp; không nhiều nhóm chuyển động đồng thời; giữ khung tĩnh ≥ 1,5 s sau khi sơ đồ xong; điểm dừng 3 s ở S30.
- Không làm được: morph thật, 3D thật, camera 3D — không yêu cầu trong storyboard này (0.4).

## 6. Phụ đề (6.2)

- Be Vietnam Pro Medium 32 px, chữ trắng #FFFFFF trên dải nền #0F172A độ đục 78% (tương phản chữ/nền dải ≈ 13:1, đạt); đặt đáy khung, trong vùng an toàn, tối đa 2 dòng × ≤ 42 ký tự.
- Không che sơ đồ/code: dải phụ đề nằm dưới vùng nội dung (nội dung kết thúc ở y ≤ 900 px).
- Nguồn chữ: cột 1 kịch bản ba cột; xuất .srt rời + bản đốt vào video.

## 7. Nhật ký tài sản (7.5) — khung, điền khi sản xuất

| Tài sản | Nguồn | Giấy phép / quyền | Ngày kiểm tra | Trạng thái |
| --- | --- | --- | --- | --- |
| Plus Jakarta Sans (var), Be Vietnam Pro (4 weight), JetBrains Mono (var) | raw.githubusercontent.com/google/fonts | SIL OFL 1.1 — kèm OFL-PlusJakartaSans.txt, OFL-BeVietnamPro.txt, OFL-JetBrainsMono.txt trong assets/fonts/ | 12/11/2026 | Đã tải, đã đối chiếu giấy phép; render thử frame_type.png thấy dấu tiếng Việt đủ |
| Bộ icon Lucide (21 SVG: gamepad-2, box, clapperboard, cog, glasses, history, cpu, check-circle, circle-check, monitor, server, shield-check, brain, code-2, code-xml, database, arrow-right, lightbulb, search, play, shopping-cart) | unpkg.com/lucide-static@1.72.0/icons | ISC — kèm assets/LUCIDE-LICENSE.txt | 12/11/2026 | Đã tải bản pinned 1.72.0; render thử frame_icon/frame_diagram đúng nét |
| Bộ icon Lucide mở rộng cho sản xuất toàn bộ (28 SVG: ban, bar-chart-3, book-open, briefcase, bug, building-2, clock, cloud, credit-card, eye, file-text, file-warning, hammer, handshake, lock, message-circle, network, palette, pen-tool, puzzle, refresh-cw, rocket, scan-search, server-cog, server-off, settings-2, wifi, wrench) | unpkg.com/lucide-static@1.72.0/icons | ISC — cùng assets/LUCIDE-LICENSE.txt | 12/11/2026 | Đã tải; "briefing" không tồn tại trong bộ 1.72.0 (404) → thay bằng briefcase, ghi lệch tại §3; render PNG đen bằng Edge headless rồi nhuộm màu qua mặt nạ luminance, cache tại assets/icons_png/ |
| Nhạc nền instrumental | không dùng | quyết định Cổng B (12/11/2026): không nhạc nền do chưa xác minh quyền | 12/11/2026 | Không dùng — chỉ voice |
| SFX tick mềm | không dùng | không áp dụng | 12/11/2026 | Không dùng — chỉ voice, giữ đúng mẫu Cổng B đã duyệt |
| Logo bên thứ ba | không dùng (text chip) | không áp dụng | 12/11/2026 | Đã quyết |
| Hình AI | không dùng cho video này (toàn bộ vector tự dựng) | không áp dụng | 12/11/2026 | Đã quyết |
| Logo AN TECH ACADEMY | chưa được cung cấp → wordmark chữ | thương hiệu riêng | 12/11/2026 | Chờ người dùng cung cấp nếu có |

## 8. Nhận diện (1.x)

- Intro: cold open 8 s + chào 12 s (S01–S02); outro 10 s (S34) + tổng kết 15 s (S32) nằm trong phần kết.
- Wordmark chữ thống nhất "AN TECH ACADEMY"; tagline "HỌC CÔNG NGHỆ, LÀM CHỦ TƯƠNG LAI" (từ docx gốc).
- Không nhạc hiệu/logo động khi chưa có tài sản được cấp quyền.