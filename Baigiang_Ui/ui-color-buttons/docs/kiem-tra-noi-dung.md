# KIỂM TRA NỘI DUNG, THUẬT NGỮ VÀ TƯƠNG PHẢN

## 1. Đối chiếu yêu cầu đề bài

| Yêu cầu | Cảnh đáp ứng | Trạng thái |
|---|---|---|
| Nguyên tắc 60–30–10 | `rule` | Đạt |
| Chọn màu chủ đạo / phụ / nhấn | `rule`, `wheel` | Đạt |
| Phối màu theo thương hiệu và mục đích | `why`, `wheel` | Đạt |
| Quy tắc màu cho chữ, nền, viền, trạng thái | `why`, `mistakes`, `states` | Đạt |
| Hệ thống nút bấm thống nhất | `anatomy`, `types`, `states` | Đạt |
| Kích thước, khoảng cách, bo góc, font, màu nút | `anatomy` | Đạt |
| 6 trạng thái nút | `states` | Đạt |
| Lỗi thường gặp | `mistakes` | Đạt |
| Thực hành cải tiến giao diện | `makeover` | Đạt |
| 3 câu trắc nghiệm, đếm ngược 3 giây | `quiz` | Đạt |
| Lời nhắn kết bài | `outro` | Đạt |
| Phụ đề + SRT + kịch bản có mốc thời gian | `build/subtitles.srt`, `build/ui-color-buttons.srt`, `docs/storyboard.md` | Đạt |
| Danh sách hình ảnh / hiệu ứng / âm thanh | `docs/storyboard.md` | Đạt |
| Font không chân, đúng thứ tự ưu tiên | `src/styles.css` | Đạt |
| Không dùng slideshow ảnh tĩnh | toàn bộ engine | Đạt |

## 2. Kiểm tra chuyên môn

| Nội dung | Cách diễn đạt trong video | Cơ sở / lưu ý |
|---|---|---|
| 60–30–10 | “Tỷ lệ định hướng cho cảm nhận thị giác, không phải công thức bắt buộc” | Quy tắc thiết kế phổ biến; video nói rõ không cần đo pixel |
| Vai trò 3 nhóm màu | Nền 60, phụ 30, nhấn 10 | Đúng cách hiểu thông dụng |
| Phối đơn sắc | Các sắc độ của cùng một màu | Monochromatic |
| Phối tương đồng | Các màu nằm cạnh nhau trên bánh xe | Analogous |
| Phối bổ sung | Hai màu đối diện | Complementary |
| Bảng màu theo ngành | Giáo dục, TMĐT, công nghệ | Ví dụ minh họa, không phải quy định tuyệt đối |
| Chiều cao nút desktop | 40–48 px | Khoảng phổ biến trong design system |
| Vùng chạm mobile | ≥ 44 px | Khuyến nghị phổ biến (Apple 44pt, Material 48dp) |
| Bo góc | 6 / 8 / 12 px, chọn một hệ thống | Đúng tinh thần “nhất quán” |
| Tương phản chữ | WCAG AA: 4.5:1 cho chữ thường, 3:1 cho chữ lớn và thành phần UI | Nhắc trong `mistakes`; bảng màu video được kiểm bên dưới |
| Sáu trạng thái | Default, Hover, Active, Focus, Disabled, Loading | Đúng danh sách đề bài |
| Focus | Viền rõ khi dùng bàn phím | Yêu cầu accessibility |
| Disabled | Giảm tương phản nhưng vẫn đọc được | Tránh chữ quá nhạt |
| Loading | Giữ nguyên kích thước nút | Tránh layout shift |
| Primary | Một nút chính mỗi màn hình | Nguyên tắc phân cấp hành động |

## 3. Bảng tương phản màu (đã tính theo WCAG 2.1)

| Cặp màu | Tỷ lệ | Kết luận | Cách dùng |
|---|---:|---|---|
| `#334155` trên `#FFFFFF` | 10.35:1 | Đạt AAA | Chữ chính trên nền trắng |
| `#334155` trên `#EAF6FF` | 9.43:1 | Đạt AAA | Chữ chính trên nền xanh nhạt |
| `#2563EB` trên `#FFFFFF` | 5.17:1 | Đạt AA | Link, nhãn xanh |
| `#FFFFFF` trên `#2563EB` | 5.17:1 | Đạt AA | Chữ trên nút primary |
| `#1E293B` trên `#F59E0B` | 6.81:1 | Đạt AA | Chữ trên nút cam |
| `#FFFFFF` trên `#F59E0B` | 2.15:1 | Không đạt | **Không dùng** chữ trắng trên cam |
| `#FFFFFF` trên `#7C3AED` | 5.70:1 | Đạt AA | Nút tím (dùng `#7C3AED`, không dùng `#8B5CF6` cho chữ trắng) |
| `#FFFFFF` trên `#8B5CF6` | 4.23:1 | Không đạt AA thường | Chỉ dùng trang trí hoặc chữ lớn |
| `#64748B` trên `#FFFFFF` | 4.76:1 | Đạt AA | Chữ phụ, disabled vẫn đọc được |
| `#94A3B8` trên `#FFFFFF` | 2.56:1 | Không đạt | Chỉ dùng viền/đường kẻ, không dùng chữ |
| `#FFFFFF` trên `#06B6D4` | 2.43:1 | Không đạt | Không dùng chữ trắng trên cyan |
| `#0F172A` trên `#06B6D4` | 7.35:1 | Đạt AAA | Chữ đậm trên cyan |

**Quy tắc áp dụng trong video:** nút cam dùng chữ `#1E293B`; nút xanh dùng chữ trắng; tím dùng `#7C3AED`; chữ phụ dùng `#64748B`; không đặt chữ trắng trên cyan/cam.

## 4. Kiểm tra typography

| Vai trò | Font | Cỡ | Ghi chú |
|---|---|---|---|
| Tiêu đề chính | Quicksand 700 | 56–60 px | Đúng “Ưu tiên 1” |
| Tiêu đề cảnh | Quicksand 700 | 38–44 px | |
| Nội dung | Be Vietnam Pro 400/500 | 26–32 px | Hỗ trợ tiếng Việt đầy đủ |
| Chú thích | Be Vietnam Pro 500 | 22–26 px | Không nhỏ hơn 22 px |
| Số liệu nổi bật | Plus Jakarta Sans 800 | 48–64 px | |
| Phụ đề | Be Vietnam Pro 500 | 26 px | Tối đa 78 ký tự/cụm, gộp cụm ngắn dưới 0,9 giây |

- Không đặt chữ đè lên vùng ảnh phức tạp: mọi khối chữ đều có nền hoặc scrim.
- Tiêu đề không quá 2 dòng; nếu dài, giảm còn 1 dòng hoặc tách cảnh.

## 5. Nhất quán thuật ngữ

- Dùng thống nhất “nút bấm” trong lời thoại, “button” chỉ xuất hiện trong nhãn tiếng Anh của trạng thái/loại nút khi cần đối chiếu.
- “Màu chủ đạo / màu phụ / màu nhấn” dùng xuyên suốt; không đổi sang “màu chính / màu nền / màu điểm nhấn” giữa bài.
- “Default, Hover, Active, Focus, Disabled, Loading” giữ nguyên tiếng Anh, có giải thích tiếng Việt lần đầu.
- “Primary, Secondary, Outline, Danger” giữ nguyên, kèm vai trò tiếng Việt.

## 6. Ghi chú giọng đọc

- Edge TTS miễn phí chỉ có giọng nam `vi-VN-NamMinhNeural` (giọng Bắc). Không có giọng nam miền Nam.
- Video dùng `vi-VN-NamMinhNeural` với tốc độ +10%; có thể đổi nhà cung cấp TTS nếu cần đúng chất giọng Nam.
- Toàn bộ pipeline không phụ thuộc nhà cung cấp: mỗi cue là một file WAV, timeline tự căn theo thời lượng thật.

## 7. Kiểm tra bản xuất cuối

| Hạng mục | Kết quả |
|---|---|
| Video | `build/ui-color-buttons.mp4` — 1920×1080, 25 fps, H.264 High, 73 MB |
| Thời lượng | 00:05:02.32 |
| Âm thanh | AAC-LC 48 kHz stereo, 192 kbps; −16,1 LUFS, true peak −2,6 dBFS |
| Phụ đề | `build/ui-color-buttons.srt` — 130 cụm, khớp timeline thoại thật |
| Nhạc nền | Pad Cmaj7–G–Am7–Fmaj7, arpeggio ngũ cung, pulse 58 Hz; duck −80% theo lời giảng |
| SFX | 50 sự kiện: error, whoosh, pop, marker, click, hover, chime, success, riser, tick |
| Kiểm tra khung hình | Đã xem still từng cảnh ở 55% và 92%, contact sheet 12 mốc, frame cuối |
