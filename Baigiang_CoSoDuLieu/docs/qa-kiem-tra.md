# Kiểm tra thuật ngữ, SQL và tính nhất quán

## 1. Kiểm tra SQL

| Bài | Câu lệnh | Kết quả kỳ vọng | Trạng thái |
|---|---|---|---|
| 1 | `SELECT * FROM SanPham;` | 5 dòng | Đúng cú pháp, đúng dữ liệu |
| 2 | `WHERE DonGia > 10000000` | 3 dòng | Đúng; 10.000.000 là giá trị biên, dùng `>` nên loại OPPO 9,5 triệu |
| 3 | `SELECT DISTINCT ... INNER JOIN` | 3 khách | Đúng; `DISTINCT` cần vì KH01 có 2 hóa đơn |
| 4 | `SUM(SoLuong * DonGia)` | 215.000.000 | Đúng; không cần `GROUP BY` |
| 5 | `GROUP BY MaSP` + `SUM(SoLuong)` | 5 nhóm | Đúng; SP01 = 4 |
| 6 | 4 × `INNER JOIN` | 8 dòng | Đúng; tổng thành tiền khớp bài 4 |

- Tất cả tên bảng/cột dùng nhất quán: `SanPham`, `KhachHang`, `NhanVien`, `HoaDon`,
  `ChiTietHoaDon`, `MaSP`, `MaKH`, `MaNV`, `MaHD`, `DonGia`, `SoLuong`.
- Alias không dấu: `AS KhachHang`, `AS NhanVien`, `AS ThanhTien`, `AS TongDoanhThu`
  (tránh định danh có dấu khi không đặt trong ngoặc vuông).
- Chuỗi Unicode trong ví dụ SQL Server dùng tiền tố `N'...'`.
- Không dùng `SELECT *` trong câu nối bảng; mọi cột đều được định danh qua alias.

## 2. Kiểm tra dữ liệu

| Phép kiểm tra | Giá trị | Nhất quán |
|---|---|---|
| Sản phẩm | 5 | ERD, bảng mẫu, q1, q2, q5 |
| Khách hàng | 4 | bảng mẫu, q3 |
| Khách đã mua | 3 (KH01–KH03) | q3; KH04 không có hóa đơn |
| Hóa đơn | 5 (HD001–HD005) | bảng mẫu, q4, q6 |
| Dòng chi tiết | 8 | bảng mẫu, q4, q5, q6 |
| Doanh thu | 48+49+64+22+32 = 215 triệu | q4, q6, slide tổng kết |
| SP01 đã bán | 1+2+1 = 4 | q5, slide "bán chạy nhất" |
| Sản phẩm > 10 triệu | SP01, SP02, SP03 | q2 |

## 3. Thuật ngữ

| Thuật ngữ | Cách dùng thống nhất |
|---|---|
| Cơ sở dữ liệu (CSDL) | Viết đầy đủ lần đầu, sau đó có thể dùng CSDL |
| Hệ quản trị cơ sở dữ liệu (DBMS) | Giải thích ngay khi xuất hiện |
| Bảng / dòng / cột | record = bản ghi, field = trường/thuộc tính |
| Khóa chính / khóa ngoại | primary key / foreign key |
| Bảng trung gian | junction table; nhấn "khóa chính ghép" |
| Thực thể / thuộc tính / quan hệ | entity / attribute / relationship |
| Toàn vẹn tham chiếu | Giải thích bằng ví dụ lớp DA99 |
| Truy vấn / kết quả truy vấn | result set khi nói về bảng tạm |

- Tên bảng trong lời thoại đọc theo tiếng Việt; tên bảng trên màn hình giữ dạng không dấu
  (`SinhVien`, `KhachHang`…) để đồng bộ với SQL.
- Các từ viết tắt DDL/DML/DQL/DCL/TCL đều được mở rộng ngay trong lời giảng.
- Thống nhất "một-nhiều" (không dùng lẫn "1:N" trong lời thoại; trên hình có thể dùng 1—N).

## 4. Kiểm tra hình ảnh (preview)

Đã chụp 36 still tại `build/previews/` và rà soát. Các lỗi đã sửa:

- Tiêu đề dòng 2 của intro bị mất do gradient + transform → chuyển sang clip-path, cỡ chữ 96px.
- Thẻ kết quả quiz đè lên tiêu đề → thêm `position: relative` cho `.quiz-wrap`, neo đáy.
- Panel câu hỏi quiz không hiện (lệch một cue giữa mốc chuyển câu và mốc fade-in) → tính lại
  `getQ` theo cue bắt đầu từng câu; đã kiểm tra bằng ảnh dựng tại 920–1020s và render lại đoạn cuối.
- Cảnh N—N: ghi chú/kết quả đè bảng trung gian → đưa về luồng bố cục thường, stage 470px.
- q6 tràn bảng kết quả → bảng compact, ẩn ghi chú/tổng kết/toast, giảm cỡ chữ.
- Quan hệ 1—1: ghi chú đè thẻ thông tin → nâng ghi chú lên, tách khỏi thẻ.
- Quan hệ 1—N và khóa ngoại: nhãn N đè lên bảng, bảng SINHVIEN tràn phải → chỉnh nhãn ra ngoài,
  giảm padding/cỡ chữ bảng, kết thúc đường nối đúng mép bảng.
- Divider: tiêu đề dài xuống dòng xấu, watermark đè danh sách phần → cỡ chữ theo độ dài,
  `min-height: 100%` cho khung.
- Shop-schema: khoảng trống lớn dưới bảng SANPHAM → bổ sung bảng trích CHITIETHOADON.

Kiểm tra che khuất: đáy nội dung lớn nhất (q6) là y≈982, phụ đề bắt đầu y≈993 — không đè.

## 5. Giới hạn giọng đọc

- Edge TTS chỉ có `vi-VN-NamMinhNeural` (nam) và `vi-VN-HoaiMyNeural` (nữ), cả hai giọng Bắc.
  Không có giọng nam miền Nam miễn phí; đã ghi rõ trong README và giữ hook `TTS_VOICE`.
- Tốc độ đọc tự nhiên, sau đó giảm 4% (`atempo=0.96`) để người học theo kịp thuật ngữ.
- Các cue dài được tổng hợp riêng từng câu, có khoảng nghỉ 0,3 giây giữa các cue.
