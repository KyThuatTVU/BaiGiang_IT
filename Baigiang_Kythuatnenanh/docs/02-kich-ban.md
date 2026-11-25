# Kịch bản giảng dạy — Kỹ thuật nén ảnh trong website

*Thời lượng ước tính: **5:08.0** (chốt theo file thoại thật sau khi TTS). 29 cue / 12 cảnh. Giọng: nam, tiết tấu nhanh 8–15% so với đọc thường.*

| # | Cảnh | Thời gian | Lời thoại | Phụ đề | rate |
|---|---|---|---|---|---|
| 1 | S01 | 0:00.0 | Chào các bạn! Chào mừng đến với An Tech Academy. Thử tưởng tượng: trang web bán điện thoại có ba mươi tấm ảnh, mỗi tấm năm MB. Đợi mãi… mà ảnh vẫn chưa hiện ra. | Chào các bạn! Chào mừng đến với An Tech Academy. / Trang web 30 ảnh, mỗi ảnh 5 MB — đợi mãi ảnh chưa hiện. | +15% |
| 2 | S01 | 0:11.7 | Cộng lại là một trăm năm mươi MB cho một trang chủ. Trên mạng di động, chậm khỏi bàn. Khách chờ lâu, họ bỏ đi — đơn hàng đi theo. | 30 × 5 MB = 150 MB cho một trang chủ. / Mạng di động càng chậm — khách bỏ đi, đơn hàng đi theo. | +13% |
| 3 | S01 | 0:21.7 | Hôm nay mình học cách làm ảnh nhẹ đi mà mắt vẫn thấy đẹp. Tên chuyên môn: nén ảnh — Image Compression. Bắt đầu nhé! | Hôm nay: làm ảnh nhẹ đi mà mắt vẫn thấy đẹp. / Tên chuyên môn: nén ảnh — Image Compression. | +12% |
| 4 | S02 | 0:30.3 | Vì sao phải nén? Ảnh nặng quyết định tốc độ tải trang, tốn băng thông, tốn chỗ lưu trữ. Băng thông và máy chủ đều là chi phí thật của người làm web. | Vì sao phải nén? Ảnh nặng quyết định tốc độ tải trang, / tốn băng thông, tốn lưu trữ — mỗi MB đều có chi phí. | +10% |
| 5 | S02 | 0:41.3 | Và quan trọng nhất: trải nghiệm. Trang thương mại điện tử tải chậm là trang khó bán hàng. Các bạn đã bao giờ bỏ đi vì chờ quá lâu chưa? | Quan trọng nhất: trải nghiệm. / Trang tải chậm là trang khó bán hàng. | +9% |
| 6 | S03 | 0:51.6 | Nén ảnh là quá trình giảm dung lượng hình ảnh bằng cách loại bỏ hoặc tổ chức lại thông tin theo một thuật toán. Giống dọn vali: vẫn đủ đồ, xếp khéo nên nhẹ hơn. | Nén ảnh: giảm dung lượng bằng cách loại bỏ hoặc / tổ chức lại thông tin theo một thuật toán. | +8% |
| 7 | S03 | 1:03.3 | Ví dụ: ảnh sản phẩm năm MB, sau khi nén còn ba trăm năm mươi KB — giảm chín mươi ba phần trăm. Số liệu giả định thôi nhé, thực tế còn tùy ảnh và mức nén. | Ví dụ: 5 MB → 350 KB, giảm khoảng 93%. / (Số liệu giả định để minh họa — thực tế tùy ảnh.) | +10% |
| 8 | S03 | 1:15.7 | Dung lượng nhỏ hơn là tải nhanh hơn, ít tốn băng thông, ít tốn chỗ lưu trữ, khách ở lại lâu hơn. Một mũi tên trúng bốn đích. | Tải nhanh hơn · ít băng thông · ít lưu trữ · / khách ở lại lâu hơn — một mũi tên trúng bốn đích. | +9% |
| 9 | S04 | 1:25.3 | Có hai trường phái. Thứ nhất: nén mất dữ liệu — Lossy Compression. Nó chủ động vứt chi tiết mắt người khó thấy, đổi lấy dung lượng nhỏ hơn nhiều. JPEG là ví dụ quen thuộc. | Nén mất dữ liệu (Lossy): bỏ chi tiết mắt khó thấy / để đổi lấy dung lượng nhỏ hơn nhiều. Ví dụ: JPEG. | +8% |
| 10 | S04 | 1:37.3 | Cùng một ảnh hoàng hôn: để chất lượng chín mươi, file khoảng sáu trăm mười tám KB; hạ còn năm mươi, chỉ còn một trăm chín mươi tư KB — giảm hơn ba lần. Nhưng nén quá tay, ảnh bắt đầu nhòe và xuất hiện nhiễu. | Cùng ảnh: quality 90 ≈ 618 KB → quality 50 ≈ 194 KB. / Giảm hơn ba lần — nhưng bắt đầu nhòe, xuất hiện nhiễu. | +9% |
| 11 | S04 | 1:52.5 | Dấu vết đặc trưng: những ô vuông tám nhân tám pixel và vệt lỗi quanh vùng chuyển màu. Chữ và nét mảnh mà nén mạnh là răng cưa ngay. Nhớ nhé! | Đặc trưng JPEG: ô vuông 8×8 pixel, lỗi vùng chuyển màu. / Chữ và nét mảnh nén mạnh → răng cưa ngay. | +12% |
| 12 | S05 | 2:03.0 | Thứ hai: nén không mất dữ liệu — Lossless Compression. Nén mà không vứt chi tiết nào, khôi phục lại y nguyên bản gốc. PNG là đại diện tiêu biểu. | Nén không mất dữ liệu (Lossless): không vứt chi tiết, / khôi phục y nguyên bản gốc. Đại diện: PNG. | +8% |
| 13 | S05 | 2:13.1 | Nhờ vậy, PNG giữ nét chữ sắc, giữ nền trong suốt — như logo sư tử này — nên hợp logo, icon, ảnh chụp màn hình. Đổi lại, file thường nặng hơn JPEG và WebP. | PNG: nét chữ sắc, nền trong suốt → hợp logo, icon, / ảnh chụp màn hình. Đổi lại: file nặng hơn JPEG, WebP. | +10% |
| 14 | S06 | 2:24.9 | Trên website nên dùng định dạng nào? JPEG nhẹ, hợp ảnh chụp. PNG nét, có nền trong suốt. WebP cân bằng, hỗ trợ cả hai kiểu nén. AVIF là định dạng mới, nén rất tốt. | JPEG: nhẹ, hợp ảnh chụp · PNG: nét, nền trong suốt / WebP: cân bằng · AVIF: định dạng mới, nén rất tốt. | +9% |
| 15 | S06 | 2:36.6 | Ví dụ: JPEG một trăm hai mươi tám KB, PNG năm trăm mười hai, WebP bảy mươi tám, AVIF bốn mươi lăm KB. Nhưng đây là số liệu của một infographic, không phải chân lý cho mọi ảnh. | JPEG 128 KB · PNG 512 KB · WebP 78 KB · AVIF 45 KB. / Số liệu từ infographic — ảnh khác, kết quả khác. | +11% |
| 16 | S07 | 2:49.3 | Chọn nhanh: ảnh chụp, sản phẩm, banner — JPEG hoặc WebP. Logo, icon, nền trong suốt — PNG hoặc SVG. Ảnh bản đồ, chữ nhỏ — đừng nén mạnh kiểu JPEG, chữ sẽ vỡ. | Ảnh chụp, sản phẩm → JPEG/WebP. Logo, icon → PNG/SVG. / Ảnh bản đồ, chữ nhỏ → tránh JPEG nén mạnh. | +9% |
| 17 | S07 | 3:00.7 | Còn RAW? Đó là ảnh gốc để chỉnh sửa, chưa dành cho web: nặng và trình duyệt không đọc được. Xuất sang JPEG hoặc WebP trước khi đăng. | RAW: ảnh gốc để chỉnh sửa, chưa dành cho web. / Xuất sang JPEG/WebP trước khi đăng. | +11% |
| 18 | S08 | 3:10.3 | Làm thử nhé. Có Squoosh nén trực tuyến, TinyPNG, ImageMagick cho dòng lệnh. Còn dân Node.js thì có Sharp — nén ngay trên máy chủ, rất nhanh. | Công cụ: Squoosh, TinyPNG, ImageMagick. / Dân Node.js: Sharp — nén ngay trên máy chủ. | +10% |
| 19 | S08 | 3:19.5 | Cài bằng npm install sharp. Đọc ảnh product.jpg, resize về chiều rộng tám trăm pixel, không phóng lớn ảnh nhỏ, chuyển WebP chất lượng tám mươi, lưu ra product.webp. | npm install sharp → đọc product.jpg, resize 800px, / chuyển WebP quality 80 → lưu product.webp. | +8% |
| 20 | S08 | 3:29.3 | Giải nghĩa: sharp mở ảnh; resize đổi kích thước; withoutEnlargement chặn phóng to; webp chọn định dạng; quality tám mươi là mức nén; toFile lưu kết quả. | sharp · resize · withoutEnlargement · webp · / quality 80 · toFile — ảnh nhẹ hơn, sẵn sàng lên web. | +9% |
| 21 | S09 | 3:38.5 | Ảnh nhẹ rồi, hiển thị cho khôn ngoan. Thẻ img cần src, alt, width, và đặc biệt là loading bằng lazy: khoan tải, đợi khách cuộn gần tới hãy tải. | Thẻ img: src, alt, width, loading="lazy". / lazy = khoan tải, đợi khách cuộn gần tới. | +10% |
| 22 | S09 | 3:48.6 | Khai báo width và height để trang không nhảy khi ảnh tải xong. Ảnh lớn thì dùng srcset để trình duyệt tự chọn kích thước phù hợp. | width + height: trang không nhảy khi ảnh tải xong. / srcset: trình duyệt tự chọn kích thước phù hợp. | +11% |
| 23 | S10 | 3:57.9 | Nén ảnh có mặt khắp nơi: thương mại điện tử nén ảnh sản phẩm cho trang danh sách mượt; tin tức tối ưu ảnh bài viết. | Thương mại điện tử: nén ảnh sản phẩm, trang mượt hơn. / Tin tức: tối ưu ảnh bài viết. | +10% |
| 24 | S10 | 4:06.7 | Du lịch giảm thư viện ảnh lớn — như hồ núi này. Giáo dục tối ưu ảnh khóa học. Hễ có ảnh trên web là có chỗ cho nén ảnh. | Du lịch: giảm thư viện ảnh. Giáo dục: ảnh khóa học. / Hễ có ảnh trên web — là có chỗ cho nén ảnh. | +9% |
| 25 | S11 | 4:16.9 | Vài lưu ý. Đừng nén quá tay, ảnh vỡ thì đẹp mấy cũng vô nghĩa. Resize đúng kích thước hiển thị, đừng tải ảnh bốn nghìn pixel về khung ba trăm. | Đừng nén quá tay — ảnh vỡ thì đẹp mấy cũng vô nghĩa. / Resize đúng kích thước hiển thị thực tế. | +9% |
| 26 | S11 | 4:27.3 | Khai báo width, height, dùng lazy loading. Cân nhắc CDN hoặc dịch vụ tối ưu ảnh. Cân bằng giữa dung lượng và chất lượng — đó là nghệ thuật, không phải phép tính. | width, height + lazy loading. Cân nhắc CDN / dịch vụ / tối ưu ảnh. Cân bằng dung lượng ↔ chất lượng. | +10% |
| 27 | S12 | 4:38.5 | Tóm lại, bốn điều. Một: nén ảnh giảm dung lượng, tăng tốc tải. Hai: Lossy cho ảnh chụp, Lossless cho logo và nền trong suốt. | 1. Nén ảnh giảm dung lượng, tăng tốc tải. / 2. Lossy (JPEG) cho ảnh chụp · Lossless (PNG) cho logo. | +9% |
| 28 | S12 | 4:47.1 | Ba: WebP và AVIF là lựa chọn hiện đại, nhớ kiểm tra trình duyệt. Bốn: Sharp, lazy loading và CDN giúp website nhẹ như lông hồng. | 3. WebP/AVIF: hiện đại, nhớ kiểm tra trình duyệt hỗ trợ. / 4. Sharp + lazy loading + CDN = website nhẹ. | +10% |
| 29 | S12 | 4:55.9 | Không phải nén càng nhỏ càng tốt, mà là cân bằng giữa dung lượng, chất lượng và trải nghiệm. Cảm ơn các bạn đã học cùng An Tech Academy. Hẹn gặp ở bài tiếp theo! | Không phải nén càng nhỏ càng tốt — mà là cân bằng / dung lượng, chất lượng, trải nghiệm. Hẹn gặp lại! | +12% |

## Câu dẫn tương tác & nhịp

- Mở đầu: câu hỏi tình huống (30 ảnh × 5 MB) tạo tò mò.
- Giữa bài: “Các bạn đã bao giờ bỏ đi vì chờ quá lâu chưa?”, “Được cái này, mất cái kia — đúng không?”, “Nhớ nhé!”.
- Chuyển phần: mỗi cảnh mở bằng một câu hỏi hoặc một khẳng định ngắn, không đọc tiêu đề khô.
- Kết: chốt 4 điều + câu khuyến khích thực hành + nhắc thương hiệu + hẹn bài sau.

## Ghi chú số liệu (bắt buộc đọc đúng bản chất)

- 30 ảnh × 5 MB = 150 MB: ví dụ giả định trong tài liệu.
- 5 MB → 350 KB (−93%): **số liệu giả định** của tài liệu để minh họa.
- 128 / 512 / 78 / 45 KB: số liệu của infographic so sánh 4 định dạng, không phải benchmark cho mọi ảnh.
- 618 KB → 194 KB: đọc từ biểu đồ (quality 90 → 50) của tài liệu; không đọc dòng “112 MB” vì đó là lỗi in của infographic.
