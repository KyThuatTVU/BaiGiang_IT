# ART DIRECTION — CỔNG A

## 1. Ý tưởng hình ảnh

"Bảng giấy kỹ thuật" (technical paper): nền giấy sáng, chữ đậm, nét bút dạ amber đánh dấu chỗ quan trọng, khung code tối như màn hình thật, ảnh tài liệu gốc được đóng khung như thẻ chứng cứ. Toàn bộ là vector phẳng 2D — không bóng đổ nặng, không 3D nhựa, không ảnh AI.

## 2. Bảng màu (tỷ lệ 60–30–10)

| Vai trò | Mã | Dùng ở đâu | Tỷ lệ |
|---|---|---|---|
| Nền giấy | `#F6F8FB` | toàn bộ canvas, thẻ trắng | ~60% |
| Navy | `#1B2A4A` | chữ chính, dải phụ đề, code panel tối, tóc/áo An | ~30% |
| Blue | `#2563EB` | nhấn cấu trúc, mũi tên, chip chính | ~7% |
| Amber | `#F59E0B` | bút dạ, gạch chân, tiến trình chương | ~3% |
| Teal | `#0D9488` | "an toàn/đúng" — check, rewrite nội bộ, 403 chip | phụ |
| Red | `#DC2626` | rủi ro, gạch chéo, 403/404 | phụ |
| Purple | `#6D5BD0` | route, khái niệm phụ | phụ |
| Mint `#E8F8F4`, Kem `#FDF6E3`, Hồng nhạt `#FFECEC` | nền thẻ ngữ nghĩa | nền chip/thẻ | phụ |

Không dùng gradient lớn làm nền; chỉ dùng sheen mảnh quét qua ảnh/thẻ như ánh sáng trên giấy bóng.

## 3. Kiểu chữ

| Vai trò | Font | Cỡ @1080p |
|---|---|---|
| Tiêu đề cảnh | Be Vietnam Pro Bold | 56–64 |
| Tiêu đề phụ | Be Vietnam Pro Medium | 28–30 |
| Thân / thẻ | Be Vietnam Pro Regular/Medium | 22–26 |
| Chip | Be Vietnam Pro SemiBold | 19–21 |
| Phụ đề | Be Vietnam Pro SemiBold, trắng | 32 |
| Code | JetBrains Mono | 22–24; số dòng 18 |
| Số lớn (403, 404) | Plus Jakarta Sans ExtraBold | 62–78 |

Từ tiếng Anh trong tiêu đề giữ nguyên, không viết hoa toàn bộ (trừ nhãn PUBLIC/PRIVATE).

## 4. Icon

- Bộ Lucide, nét đều 2 px, tô đơn sắc theo ngữ nghĩa.
- Pipeline: rasterize SVG đen → đổi màu RGBA → cache `assets/icons_png/<name>_<HEX>.png`. Không dùng icon 3D, không emoji, không icon nhiều màu.
- Mỗi icon chỉ xuất hiện khi có nghĩa: shield=chặn, eye=quan sát, route=định tuyến, lock=khoá, monitor=trình duyệt, server=Apache.

## 5. Nhân vật giáo viên An

- Vector phẳng, 360×560 gốc, vẽ 2× rồi hạ mẫu; viền navy 3 px; áo sơ mi xanh navy, thẻ tên "AN" amber, tóc đen, quần navy, giày trắng.
- 7 tư thế: idle, present, point_left, point_right, think, wave, write. Giữ nguyên trang phục suốt video.
- Nhịp thở: bob 2 px chu kỳ ~2,9 s; chớp mắt mỗi 3,4 s; mấp máy môi khi cue đang đọc.
- Vị trí: S01/S12 scale 0,66–0,72 (hero/outro); cảnh nội dung 0,40–0,48, đặt trái hoặc phải sao cho không che nội dung.
- Ánh sáng: chỉ bóng ellipse mờ dưới chân, không đổ bóng lên nền.

## 6. Hệ ngôn ngữ chuyển động

| Hiệu ứng | Cách làm | Dùng cho |
|---|---|---|
| IN (fade + rise 14 px) | alpha theo `seg` | thẻ, ảnh, chip |
| TYPE | đếm ký tự theo thời gian | code, URL |
| DRAW | nội suy điểm + nhiễu nhẹ | gạch chân, khoanh tròn, gạch dòng, mũi tên nối |
| POP | scale 0,86→1,0 + overshoot nhẹ | chip, node, tem |
| SWAP | ảnh cũ mờ đi, ảnh mới hiện | S07 image8→image3 |
| Sheen | dải sáng chéo alpha 22 | ảnh minh hoạ, thẻ lớn |
| Gói dữ liệu | chấm sáng chạy dọc path | S04 browser→Apache→PHP |

Quy ước: một cảnh chỉ có **một** hiệu ứng chủ đạo + tối đa hai hiệu ứng phụ; mọi animation phải kết thúc trước khi chuyển cảnh 0,3 s.

## 7. Bố cục theo cảnh (đa dạng nền, cùng một hệ)

- Hero sáng (S01, S12) — tiêu đề lớn, khoảng thở rộng.
- Giả lập trình duyệt (S02).
- Danh sách + bảng rủi ro (S03).
- Flow 3 node + panel code tối (S04).
- Split listing / minh hoạ isometric (S05).
- Panel code + thẻ kem (S06).
- Morph URL + đổi ảnh giữa cảnh (S07).
- Hub-and-spoke (S08).
- Code sáng + tem nghiêng (S09).
- Cây phân vùng + flow dọc (S10).
- Thẻ tổng hợp + quiz (S11).

Mỗi cảnh có tối thiểu 3 sắc độ nền khác nhau (giấy, thẻ trắng, panel tối/màu ngữ nghĩa) để tránh "một màu".

## 8. Âm thanh

- Nhạc nền: pad ấm + pluck arpeggio, vòng Am–F–C–G, 84 BPM, tự tổng hợp bằng numpy, mức thấp (~−30 dBFS dưới thoại), không lời.
- SFX: pop, click, whoosh, tick, marker (nét bút), chime, success; thêm **deny** (âm rơi) cho 403 và **thud** cho tem/khẳng định.
- Quy tắc: SFX gắn với hành động hình ảnh, không quá 1 SFX/0,6 s; cao trào S11 dùng success.
- Chuẩn loudness: đo 2 lượt (trước/sau), đích −14 LUFS, TP −1 dB, LRA 11.

## 9. Phụ đề

- Dải navy bo góc, chữ trắng 32 px, tối đa 2 dòng, lề 160 px.
- Nội dung khớp lời đọc, rút gọn từ ngữ thừa; thuật ngữ giữ đúng chính tả hiển thị.

## 10. Checklist duyệt hình

- [ ] Không có chữ nào bị nhân vật/khung che.
- [ ] Mọi ảnh gốc nằm trong khung bo góc + chú thích ngữ cảnh.
- [ ] Không quá 3 màu nhấn trong một khung hình.
- [ ] Code hiển thị đúng cú pháp, highlight đúng dòng đang nói.
- [ ] Phụ đề không tràn quá 2 dòng ở 1080p.
- [ ] SFX khớp điểm rơi của animation.
