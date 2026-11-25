# Storyboard — Cơ sở dữ liệu và ứng dụng trong thực tế

Video 16:9, 1920×1080, 25 fps. Toàn bộ hình ảnh được dựng bằng HTML/CSS/SVG (không dùng ảnh tĩnh ghép slide);
mỗi cảnh là một "sân khấu" động, render theo từng khung hình từ `window.renderFrame(t)`.

- Tổng số cảnh: **36**
- Tổng số cue thuyết minh: **131**
- Thời lượng: **17:30 (17.5 phút)**
- Ảnh still QA: `build/previews/<scene-id>.png` (36 ảnh, chụp ở cuối mỗi cảnh)

## Bảng storyboard

| # | Scene ID | Phần | Tiêu đề | Hình ảnh chính | Chuyển động / nhấn | SFX | Thời lượng | Bắt đầu |
|---|---|---|---|---|---|---|---|---|
| 1 | `intro` | Mở đầu | **Cơ sở dữ liệu và ứng dụng trong thực tế** | Nền tối navy, lưới kỹ thuật, trụ dữ liệu 3D phát sáng; tiêu đề lớn hai dòng màu trắng/cyan. | Tiêu đề trượt và mở bằng clip-path; hạt sáng và vòng quét; nhịp boot. | boot, whoosh | 0:25 | 0:00 |
| 2 | `objectives` | Mở đầu | **Mục tiêu bài học** | Bảy thẻ lộ trình học tập xếp thành lưới, đánh số phần 1–7. | Thẻ hiện dần theo nhóm nội dung; thẻ đang nói được viền cyan. | whoosh, sparkle | 0:26 | 0:25 |
| 3 | `div1` | P1 | **Giới thiệu cơ sở dữ liệu** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:05 | 0:52 |
| 4 | `db-concept` | P1 | **Cơ sở dữ liệu là gì?** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | chime | 0:29 | 0:57 |
| 5 | `data-info` | P1 | **Dữ liệu và thông tin** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | chime | 0:28 | 1:27 |
| 6 | `why-db` | P1 | **Vì sao cần cơ sở dữ liệu?** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | whoosh, sparkle | 0:31 | 1:56 |
| 7 | `shop` | P1 | **Bài toán: cửa hàng điện thoại** | Bối cảnh cửa hàng điện thoại: 1.200 sản phẩm, 380 khách, 5.000+ hóa đơn/năm; so sánh Excel rời rạc và CSDL tập trung. | Bộ đếm tăng dần; các file Excel tản mát bị gom về một khối dữ liệu. | whoosh, success | 0:33 | 2:27 |
| 8 | `dbms` | P1 | **Hệ quản trị cơ sở dữ liệu** | Bốn thẻ DBMS: MySQL, SQL Server, PostgreSQL, Oracle; lõi chung SQL ở giữa. | Thẻ lật/hiện lần lượt; dòng "SQL" chạy qua cả bốn. | whoosh | 0:44 | 3:01 |
| 9 | `div2` | P2 | **Các thành phần của cơ sở dữ liệu** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:05 | 3:45 |
| 10 | `table-anatomy` | P2 | **Bảng, dòng và cột** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | chime | 0:35 | 3:51 |
| 11 | `primary-key` | P2 | **Khóa chính** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | chime, error | 0:35 | 4:26 |
| 12 | `foreign-key` | P2 | **Khóa ngoại** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | chime, error | 0:26 | 5:01 |
| 13 | `div3` | P3 | **Các loại mối quan hệ** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:05 | 5:28 |
| 14 | `rel-1-1` | P3 | **Quan hệ một-một** | Hai thẻ SINHVIEN và HOSO, đường 1—1, nhãn UNIQUE trên MaSV của HOSO. | Thẻ trượt vào; đường nối vẽ; cột FK+UNIQUE nhấn sáng; ghi chú hiện dưới. | whoosh | 0:24 | 5:34 |
| 15 | `rel-1-n` | P3 | **Quan hệ một-nhiều** | Thẻ LOP bên trái, bảng SINHVIEN bên phải, đường 1—N trỏ vào bảng. | Đường nối và mũi tên vẽ; cột MaLop của cả 4 dòng sáng lên; ví dụ thực tế hiện dần. | whoosh, chime | 0:21 | 5:58 |
| 16 | `rel-n-n` | P3 | **Quan hệ nhiều-nhiều** | Hai thẻ SINHVIEN và MONHOC, bảng trung gian DANGKY ở giữa với khóa chính ghép. | Hai nhánh 1—N vẽ xuống bảng giữa; MaSV+MaMH chuyển vàng; kết luận "2 quan hệ 1—N". | whoosh, chime, success | 0:33 | 6:19 |
| 17 | `div4` | P4 | **Thiết kế cơ sở dữ liệu và sơ đồ ERD** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:06 | 6:53 |
| 18 | `erd-concepts` | P4 | **Thực thể, thuộc tính, quan hệ** | Ký pháp ERD: hình chữ nhật thực thể, elip thuộc tính, hình thoi quan hệ; ánh xạ sang bảng. | Ba ký pháp hiện lần lượt; phép biến đổi entity→table, attribute→column. | chime | 0:41 | 7:00 |
| 19 | `erd-analysis` | P4 | **Phân tích bài toán bán hàng** | Yêu cầu bài toán → gạch chân danh từ → 5 thực thể; sơ đồ quan hệ sơ bộ. | Các danh từ được đánh dấu và bay vào thẻ thực thể; đường quan hệ nối dần. | whoosh, chime | 0:47 | 7:41 |
| 20 | `erd-build` | P4 | **Sơ đồ ERD cửa hàng điện thoại** | ERD hoàn chỉnh 5 bảng của cửa hàng điện thoại; PK vàng, FK xanh; nhãn 1—N. | Từng bảng và đường quan hệ hiện theo lời giảng; ghi chú DonGia trong ChiTietHoaDon. | whoosh, chime, sparkle | 0:34 | 8:28 |
| 21 | `div5` | P5 | **Ngôn ngữ SQL cơ bản** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:06 | 9:03 |
| 22 | `sql-groups` | P5 | **Năm nhóm lệnh SQL** | Năm cột nhóm lệnh DDL, DML, DQL, DCL, TCL kèm lệnh đại diện. | Cột hiện lần lượt; lệnh đang nói được đóng khung; bản đồ tổng thể hoàn chỉnh. | chime, sparkle | 0:46 | 9:09 |
| 23 | `sql-create` | P5 | **DDL: tạo bảng** | Trình soạn SQL tối màu; gõ CREATE TABLE SinhVien; thẻ kết quả "tạo bảng thành công". | Con trỏ gõ từng ký tự, token đổi màu; toast xanh sau khi chạy. | whoosh, type, success | 0:33 | 9:56 |
| 24 | `sql-insert` | P5 | **DML và DQL** | Gõ INSERT INTO SinhVien; bảng kết quả SELECT * hiện bản ghi mới. | Gõ lệnh, dòng mới trượt vào result set; nhấn chữ N trước chuỗi Unicode. | type, chime, success | 0:32 | 10:29 |
| 25 | `div6` | P6 | **Bài toán truy vấn thực tế** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:06 | 11:01 |
| 26 | `shop-schema` | P6 | **Dữ liệu cửa hàng điện thoại** | Bốn bảng dữ liệu mẫu: SANPHAM, KHACHHANG, HOADON, CHITIET HOADON; quy trình 4 bước đọc đề → SQL → kết quả. | Bảng hiện dần; badge số dòng; dải 4 bước sáng lên. | whoosh | 0:24 | 11:07 |
| 27 | `q1` | P6 | **Bài toán 1: Toàn bộ sản phẩm** | Đề bài, phân tích, SQL SELECT * FROM SanPham, bảng kết quả 5 dòng. | Các bước phân tích hiện; gõ SQL; kết quả và toast thành công. | whoosh, type, success | 0:21 | 11:32 |
| 28 | `q2` | P6 | **Bài toán 2: Sản phẩm trên 10 triệu** | SQL WHERE DonGia > 10000000; kết quả 3 sản phẩm cao cấp. | Gõ lệnh; các dòng không thỏa bị làm mờ; 3 dòng đạt được nhấn. | whoosh, type, success | 0:31 | 11:53 |
| 29 | `q3` | P6 | **Bài toán 3: Khách đã mua hàng** | SQL DISTINCT + INNER JOIN KhachHang/HoaDon; kết quả 3 khách đã mua. | Sơ đồ nối bảng; bảng kết quả lọc trùng; khách chưa mua bị loại. | whoosh, type, success | 0:33 | 12:25 |
| 30 | `q4` | P6 | **Bài toán 4: Tổng doanh thu** | SQL SUM(SoLuong*DonGia); bảng tính doanh thu từng hóa đơn và tổng 215 triệu. | Từng hóa đơn cộng dồn; tổng tiền đếm lên; nhấn hàm SUM. | whoosh, type, success | 0:22 | 12:58 |
| 31 | `q5` | P6 | **Bài toán 5: Số lượng đã bán** | SQL GROUP BY MaSP với SUM(SoLuong); biểu đồ thanh số lượng theo sản phẩm. | Các thanh mọc lần lượt; SP01 dẫn đầu 4 chiếc. | whoosh, type, success | 0:24 | 13:21 |
| 32 | `q6` | P6 | **Bài toán 6: Kết hợp nhiều bảng** | SQL nối 4 bảng INNER JOIN; sơ đồ join; bảng kê 8 dòng với thành tiền. | Sơ đồ nối bảng sáng dần; gõ câu lệnh dài; bảng kết quả 8 dòng. | whoosh, type, success | 0:36 | 13:46 |
| 33 | `div7` | P7 | **Tổng kết và ôn tập** | Bố cục bài giảng theo chủ đề, tiêu đề và nội dung chính. | Các khối nội dung hiện dần theo lời thoại. | riser | 0:05 | 14:22 |
| 34 | `summary` | P7 | **Tổng kết** | Sáu thẻ tổng kết: khái niệm, bảng/PK/FK, quan hệ, ERD, SQL, quy trình thực tế. | Thẻ hiện lần lượt theo lời thoại; dấu kiểm hoàn thành. | whoosh, chime, success | 0:44 | 14:28 |
| 35 | `quiz` | P7 | **Câu hỏi ôn tập** | Năm câu hỏi trắc nghiệm A–D, tiến độ 5 câu, thẻ điểm cuối 5/5. | Câu hỏi hiện; đáp án đúng sáng xanh; chuyển câu; vòng điểm kết thúc. | whoosh, success, sparkle | 1:52 | 15:12 |
| 36 | `outro` | P7 | **Kết thúc bài giảng** | Lời kết, ba bước thực hành, lời cảm ơn; nền tối dần. | Nội dung hiện rồi fade out; logo và tiêu đề giữ lại. | chime, sparkle | 0:25 | 17:05 |

## Danh sách hình ảnh & tài nguyên

| Nhóm | Tệp / nguồn | Dùng cho |
|---|---|---|
| Ảnh still QA | `build/previews/*.png` (36 tệp) | Kiểm tra bố cục từng cảnh |
| Font tiêu đề | `assets/fonts/be-vietnam-pro-*.woff2` | Toàn bộ chữ Latin + tiếng Việt |
| Font code | `assets/fonts/jetbrains-mono-*.woff2` | SQL, mã bảng, nhãn kỹ thuật |
| Nền & hiệu ứng | CSS gradient + lưới + hạt (không tệp) | Nền công nghệ navy/cyan |
| Sơ đồ ERD, mũi tên, biểu đồ | SVG nội tuyến trong `src/app.js` | Phần 3, 4, 6 |
| Dữ liệu mẫu | `src/app.js` (SV, SP, KH, HD, CT) + `build/script.json` | Bảng, ERD, truy vấn |
| Giọng đọc | `build/voice/scenes/*.wav` | Thuyết minh từng cảnh |
| Nhạc nền & SFX | Sinh bằng numpy trong `tools/build-audio.py` | Ambient pad, pulse, pluck, whoosh/chime/type… |
| Phụ đề | `build/captions.srt` | Bản dịch thoại kèm video |

## Nguyên tắc hình ảnh

- Nền navy `#050d1a` → `#0a1c30`, lưới mảnh, hạt sáng, glow cyan `#22d3ee`.
- Màu ngữ nghĩa: vàng `#fbbf24` = khóa chính; xanh `#38bdf8` = khóa ngoại; đỏ `#f87171` = lỗi;
  xanh lá `#6ee7b7` = thành công.
- Mỗi cảnh có nhịp: tiêu đề → nội dung chính → nhấn trọng tâm → kết luận, khớp với cue thuyết minh.
