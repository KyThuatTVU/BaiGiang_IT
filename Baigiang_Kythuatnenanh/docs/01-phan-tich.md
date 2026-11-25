# Phân tích tài liệu — Kỹ thuật nén ảnh trong website

**Thương hiệu:** AN TECH ACADEMY · **Môn:** Xử lý ảnh · **Thời lượng mục tiêu:** ~5 phút (4:45–5:15)
**Khung hình:** 1920×1080, 30 fps · **Đối tượng:** sinh viên CNTT, người mới học lập trình, người làm web.

## 1. Mục tiêu bài học

Sau video, người học có thể:
1. Hiểu nén ảnh là gì và vì sao website cần nén ảnh.
2. Phân biệt nén mất dữ liệu (Lossy) và không mất dữ liệu (Lossless).
3. Nhận biết khi nào dùng JPEG, PNG, WebP, AVIF (và vai trò của RAW).
4. Biết công cụ/thư viện nén ảnh, viết được pipeline Sharp tối thiểu.
5. Áp dụng vào website thực tế: resize, lazy loading, width/height, CDN.

## 2. Kiến thức trọng tâm (thứ tự giảng)

| # | Ý | Cách thể hiện |
|---|---|---|
| 1 | Ảnh nặng → trang chậm → mất khách | Hook 30 ảnh × 5 MB = 150 MB; ảnh tải nhanh/tải chậm |
| 2 | Nén ảnh = giảm dung lượng bằng thuật toán | Định nghĩa + ví dụ 5 MB → 350 KB (giả định) |
| 3 | Lossy: bỏ chi tiết khó thấy | JPEG, bảng quality 100→50, ô 8×8, lỗi quanh chuyển màu |
| 4 | Lossless: giữ nguyên dữ liệu | PNG, nền trong suốt, khôi phục y nguyên |
| 5 | Bốn định dạng và đánh đổi | Infographic 4 cột + số liệu minh họa có ghi nguồn |
| 6 | Chọn định dạng theo mục đích | Ma trận ảnh chụp / logo / bản đồ; RAW chỉ để chỉnh sửa |
| 7 | Thực hành Sharp + HTML | Code typing `compress.js`, pipeline, thẻ `img` + lazy |
| 8 | Ứng dụng & lưu ý | 4 lĩnh vực; 5 lưu ý; cân bằng dung lượng ↔ chất lượng |

## 3. Ví dụ thực tế được dùng

- **Thương mại điện tử:** 30 ảnh sản phẩm × 5 MB; ảnh sản phẩm trước/sau nén; trang chi tiết sản phẩm.
- **Đo lường hiệu năng:** bảng Before/After của imgix (−96% dung lượng, −41% loading) dùng làm *bằng chứng minh họa*, không phải số liệu của bài.
- **Du lịch / giáo dục / tin tức:** thẻ ứng dụng với ảnh thật.
- **Mã nguồn:** đoạn Sharp lấy nguyên từ tài liệu (`product.jpg` → `product.webp`).

## 4. Kho hình ảnh (17 ảnh người dùng cung cấp — dùng đủ)

| # | File | Nội dung | Cảnh | Cách dùng |
|---|---|---|---|---|
| 1 | `loading_fast_slow.png` | Điện thoại Tải nhanh vs Tải chậm | S01 | Khung chứng cứ lớn, chia đôi |
| 2 | `imgix_score.png` | Before/After, điểm hiệu năng, −96% dung lượng | S02, S12 | Khung lớn S02; dải nhỏ S12 |
| 3 | `shop_product_page.png` | Trang chi tiết sản phẩm iPhone | S02, S10 | Khung nhỏ S02; thẻ E-commerce S10 |
| 4 | `before_after_5mb.png` | Ảnh sản phẩm 5 MB → 350 KB (−93%, ghi giả định) | S03 | Bằng chứng trung tâm |
| 5 | `jpeg_quality_grid.png` | Lưới JPEG quality 100→50 | S04 | Khung trái + zoom ô 8×8 |
| 6 | `jpeg_artifacts_face.png` | Lỗi nén trên mặt người, ô 8×8 | S04 | Khung phải, khoanh lỗi |
| 7 | `text_quality.png` | Chữ “a” ở các mức quality (JPG vs PNG) | S04 | Khung nhỏ minh họa chữ vỡ |
| 8 | `png_features.png` | 5 đặc điểm PNG | S05 | Khung trái |
| 9 | `logo_transparent.png` | Logo sư tử JPG → nền trong suốt | S05 | Khung phải, animation nền caro |
| 10 | `formats_4up.png` | JPEG/PNG/WebP/AVIF + dung lượng | S06 | Bằng chứng trung tâm |
| 11 | `map_jpeg_png.png` | Bản đồ JPEG nén mạnh vs PNG-24 | S07 | Zoom vùng chữ bị vỡ |
| 12 | `raw_vs_jpeg.png` | Cảnh RAW vs JPEG | S07 | Thumbnail nhóm “RAW để chỉnh sửa” |
| 13 | `elcapitan_sizes.png` | Ảnh El Capitan, chú thích JPEG vs WebP | S07 | Thumbnail nhóm ảnh chụp |
| 14 | `cat_compression.png` | Mèo nén cao vs thấp | S04 | Khung nhỏ minh họa mất chi tiết |
| 15 | `screenshot_guide.png` | PNG tốt cho screenshot, JPG gây nhòe chữ | S11 | Khung nhỏ bên phải |
| 16 | `product_devices.png` | Ảnh sản phẩm trên laptop/tablet/phone | S03 | Khung ngữ cảnh đa thiết bị |
| 17 | `lake_dolomites.png` | Hồ núi phong cảnh | S10 | Thẻ Du lịch |

*Ảnh giữ nguyên nội dung gốc; khung chứng cứ có nhãn nguồn khi ảnh mang thương hiệu bên thứ ba.*

## 5. Số liệu — phân loại trung thực

| Số liệu | Nguồn | Cách nói |
|---|---|---|
| 30 ảnh × 5 MB = 150 MB | Tài liệu (tình huống giả định) | Nói như tình huống, không như khảo sát |
| 5 MB → 350 KB, −93% | Tài liệu, ảnh ghi rõ “số liệu giả định” | Nói rõ “giả định để minh họa” |
| Quality 90: 618 KB → 50: 194 KB | Biểu đồ trong tài liệu | “Theo biểu đồ này…” (bỏ dòng “112 MB” vì là lỗi in) |
| 128 / 512 / 78 / 45 KB | Infographic so sánh | Nói rõ là số liệu infographic, ảnh khác thì khác |
| −96% dung lượng, −41% loading | Ảnh imgix | Chỉ để ảnh tự nói; không đọc như kết quả của bài |

Không thêm thống kê không có trong tài liệu (ví dụ tỉ lệ thoát trang theo %).

## 6. Giới hạn công cụ (công bố trước)

- **Giọng nam miền Nam:** Edge TTS `vi-VN` chỉ có NamMinh (giọng Bắc) và HoaiMy (nữ). Không có giọng nam Nam bộ. Phương án: NamMinh + dịch giọng +1 → +1,5 semitone, tốc độ +8…+15%, ngắt câu ngắn để nghe trẻ, gần giọng giảng viên; vẫn **không phải** giọng Nam bộ thật. Nếu cần đúng chất Nam bộ phải dùng nhà cung cấp khác (ElevenLabs/Azure custom voice) — cần tài khoản/API.
- **Diễn xuất TTS:** Edge TTS không nhận SSML cảm xúc; nhịp và sắc thái điều khiển bằng rate/shift, độ dài câu và dấu câu. Không tuyên bố “diễn xuất chuyên nghiệp”.
- **Kiểm tra phát âm:** không có công cụ nghe; sẽ đo waveform/thời lượng, còn phát âm từng thuật ngữ cần người duyệt nghe lại.
