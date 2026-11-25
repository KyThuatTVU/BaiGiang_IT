# Lời thoại bài giảng (bản đầy đủ)

Giọng đọc: `vi-VN-NamMinhNeural` (Edge TTS, nam, giọng Bắc chuẩn; xem README về giới hạn giọng miền Nam).
Thời lượng: 17:30. Thời gian dưới đây là mốc tuyệt đối trong video.

### Cơ sở dữ liệu và ứng dụng trong thực tế

*Cảnh 0:00 – 0:25 (25.7 giây)*

- `0:01` Chào các bạn. Chào mừng đến với bài giảng Cơ sở dữ liệu và ứng dụng trong thực tế. *[boot]*
- `0:06` Hôm nay, chúng ta sẽ đi từ những khái niệm nền tảng nhất, cho đến thiết kế sơ đồ ERD, và viết những câu truy vấn SQL thật sự. *[whoosh]*
- `0:15` Mục tiêu là: sau bài học, các bạn có thể đọc hiểu một cơ sở dữ liệu, thiết kế được mô hình dữ liệu cho một cửa hàng, và tự viết truy vấn để lấy ra thông tin mình cần.

### Mục tiêu bài học

*Cảnh 0:25 – 0:52 (26.4 giây)*

- `0:26` Bài giảng gồm bảy phần, đi theo một lộ trình rõ ràng. *[whoosh]*
- `0:30` Phần một và hai: hiểu cơ sở dữ liệu là gì, hệ quản trị cơ sở dữ liệu là gì, và các thành phần của một bảng.
- `0:37` Phần ba và bốn: ba loại mối quan hệ, và cách chuyển một bài toán thực tế thành sơ đồ ERD.
- `0:42` Phần năm, sáu và bảy: ngôn ngữ SQL, sáu bài toán truy vấn trên dữ liệu cửa hàng điện thoại, và phần tổng kết, ôn tập. *[sparkle]*


## Phần 1

### Giới thiệu cơ sở dữ liệu

*Cảnh 0:52 – 0:57 (5.7 giây)*

- `0:53` Phần một. Giới thiệu cơ sở dữ liệu. *[riser]*

### Cơ sở dữ liệu là gì?

*Cảnh 0:57 – 1:27 (30.0 giây)*

- `0:58` Hãy bắt đầu bằng câu hỏi đơn giản: cơ sở dữ liệu là gì?
- `1:02` Cơ sở dữ liệu là một tập hợp dữ liệu được tổ chức có cấu trúc, lưu trữ trên máy tính, và được quản lý để nhiều người có thể truy cập, tìm kiếm và cập nhật một cách hiệu quả. *[chime]*
- `1:12` Ví dụ: danh sách sinh viên, hóa đơn bán hàng, hay lịch sử giao dịch ngân hàng, đều có thể được lưu trong cơ sở dữ liệu.
- `1:19` Điểm quan trọng là: dữ liệu ở đây không phải một mớ hỗn độn, mà có cấu trúc rõ ràng, và các phần tử có quan hệ với nhau.

### Dữ liệu và thông tin

*Cảnh 1:27 – 1:56 (28.4 giây)*

- `1:28` Nhiều bạn nhầm lẫn giữa dữ liệu và thông tin. Dữ liệu là những sự kiện thô, chưa qua xử lý. Ví dụ: một con số, một ngày tháng, một mã đơn hàng.
- `1:40` Thông tin là kết quả sau khi dữ liệu được xử lý, tổng hợp, và đặt trong ngữ cảnh. *[chime]*
- `1:45` Cùng một tập dữ liệu, nhưng khi ta tính tổng doanh thu theo tháng, ta có thông tin để ra quyết định. Dữ liệu là nguyên liệu, còn thông tin là sản phẩm.

### Vì sao cần cơ sở dữ liệu?

*Cảnh 1:56 – 2:27 (31.5 giây)*

- `1:57` Vậy tại sao phải dùng cơ sở dữ liệu, thay vì lưu bằng file Excel hay sổ sách?
- `2:01` Khi dữ liệu lớn dần, cách lưu file truyền thống bộc lộ bốn vấn đề: dư thừa dữ liệu, dữ liệu không nhất quán, tìm kiếm chậm, và không thể chia sẻ an toàn cho nhiều người. *[whoosh]*
- `2:11` Cơ sở dữ liệu giải quyết bằng bốn cách: chuẩn hóa cấu trúc để giảm dư thừa, dùng ràng buộc để đảm bảo nhất quán, dùng chỉ mục để tìm nhanh, và phân quyền để kiểm soát truy cập. *[sparkle]*
- `2:21` Đặc biệt, nhiều người có thể làm việc cùng lúc, mà không ghi đè lên dữ liệu của nhau.

### Bài toán: cửa hàng điện thoại

*Cảnh 2:27 – 3:01 (33.2 giây)*

- `2:28` Hãy hình dung một cửa hàng điện thoại, với khoảng một nghìn hai trăm sản phẩm, ba trăm tám mươi khách hàng, và hơn năm nghìn hóa đơn mỗi năm. *[whoosh]*
- `2:36` Nếu lưu bằng file rời rạc, mỗi nhân viên giữ một bản Excel, thì việc đồng bộ gần như không thể: giá cũ, tồn kho sai, khách hàng bị trùng.
- `2:45` Với cơ sở dữ liệu, tất cả nằm trong một nguồn dữ liệu duy nhất. Bán một chiếc điện thoại, tồn kho tự giảm, hóa đơn được ghi lại, doanh thu cập nhật ngay. *[success]*
- `2:55` Đó là lý do gần như mọi ứng dụng hiện đại đều có một cơ sở dữ liệu phía sau.

### Hệ quản trị cơ sở dữ liệu

*Cảnh 3:01 – 3:45 (44.2 giây)*

- `3:01` Cơ sở dữ liệu là dữ liệu. Còn phần mềm dùng để tạo, quản lý và truy vấn dữ liệu đó, gọi là hệ quản trị cơ sở dữ liệu, viết tắt là DBMS.
- `3:12` Bốn hệ quản trị phổ biến nhất hiện nay: MySQL, mã nguồn mở, rất phổ biến với ứng dụng web; SQL Server của Microsoft; PostgreSQL, mạnh về tính chuẩn và khả năng mở rộng; và Oracle, thường dùng trong hệ thống lớn như ngân hàng, tài chính. *[whoosh]*
- `3:27` Điểm chung: cả bốn đều dùng ngôn ngữ SQL để làm việc với dữ liệu. Học tốt SQL, các bạn có thể chuyển đổi giữa chúng khá dễ dàng.
- `3:37` Ngoài truy vấn, DBMS còn lo bảo mật, sao lưu, phục hồi, và xử lý nhiều người dùng cùng lúc.


## Phần 2

### Các thành phần của cơ sở dữ liệu

*Cảnh 3:45 – 3:51 (6.0 giây)*

- `3:46` Phần hai. Các thành phần của cơ sở dữ liệu. *[riser]*

### Bảng, dòng và cột

*Cảnh 3:51 – 4:26 (35.1 giây)*

- `3:52` Bây giờ, hãy mổ xẻ một cơ sở dữ liệu để xem bên trong có gì. Đơn vị cơ bản nhất là bảng, hay table.
- `3:59` Bảng SinhVien có bốn cột: MaSV, HoTen, Lop, Email. Mỗi cột là một thuộc tính, hay còn gọi là trường, field. *[chime]*
- `4:09` Mỗi dòng là một bản ghi, record, đại diện cho một đối tượng cụ thể. Ở đây, mỗi dòng là một sinh viên.
- `4:16` Cột quy định kiểu dữ liệu và ý nghĩa. Dòng chứa các giá trị thực tế. Toàn bộ các dòng tạo thành dữ liệu của bảng.

### Khóa chính

*Cảnh 4:26 – 5:01 (35.6 giây)*

- `4:27` Trong bốn cột đó, MaSV có một vai trò đặc biệt: nó là khóa chính, primary key. *[chime]*
- `4:32` Khóa chính là một cột, hoặc một tổ hợp cột, xác định duy nhất mỗi bản ghi trong bảng. Không được trùng, và không được để trống.
- `4:41` Vì sao cần? Vì tên có thể trùng. Có hai bạn cùng tên Nguyễn Văn An, cùng lớp. Nếu không có mã định danh, hệ thống không biết đang cập nhật hồ sơ của ai. *[error]*
- `4:53` Nhờ MaSV, mỗi sinh viên là duy nhất. Khóa chính thường là mã, số căn cước, hoặc một mã do hệ thống sinh ra.

### Khóa ngoại

*Cảnh 5:01 – 5:28 (26.7 giây)*

- `5:02` Nếu khóa chính định danh bản ghi trong bảng của nó, thì khóa ngoại tạo cầu nối giữa hai bảng.
- `5:08` Cột MaLop trong bảng SinhVien là khóa ngoại, tham chiếu đến khóa chính MaLop của bảng Lop. *[chime]*
- `5:13` Ràng buộc khóa ngoại đảm bảo: không thể gán một sinh viên vào lớp không tồn tại. Thử nhập MaLop là DA99, hệ thống sẽ từ chối. *[error]*
- `5:22` Nhờ vậy, dữ liệu luôn liên kết đúng, và ta có thể truy vấn chéo giữa các bảng.


## Phần 3

### Các loại mối quan hệ

*Cảnh 5:28 – 5:34 (5.5 giây)*

- `5:29` Phần ba. Các loại mối quan hệ. *[riser]*

### Quan hệ một-một

*Cảnh 5:34 – 5:58 (24.6 giây)*

- `5:35` Có ba loại mối quan hệ chính. Thứ nhất, một-một. Một sinh viên có đúng một hồ sơ cá nhân, và mỗi hồ sơ thuộc về đúng một sinh viên. *[whoosh]*
- `5:44` Trong mô hình, ta đặt khóa ngoại MaSV vào bảng HoSo, kèm ràng buộc duy nhất, để mỗi sinh viên chỉ có tối đa một hồ sơ.
- `5:52` Quan hệ một-một thường dùng để tách những thông tin ít dùng, hoặc nhạy cảm, sang một bảng riêng.

### Quan hệ một-nhiều

*Cảnh 5:58 – 6:19 (21.1 giây)*

- `5:59` Thứ hai, một-nhiều. Một lớp có nhiều sinh viên, nhưng mỗi sinh viên chỉ thuộc một lớp. *[whoosh]*
- `6:05` Cách hiện thực rất gọn: đặt khóa ngoại ở phía nhiều. Cột MaLop nằm trong bảng SinhVien. *[chime]*
- `6:12` Đây là quan hệ phổ biến nhất trong thực tế: khách hàng và hóa đơn, danh mục và sản phẩm, nhân viên và hợp đồng.

### Quan hệ nhiều-nhiều

*Cảnh 6:19 – 6:53 (33.4 giây)*

- `6:20` Thứ ba, nhiều-nhiều. Một sinh viên đăng ký nhiều môn học, và một môn học có nhiều sinh viên. *[whoosh]*
- `6:27` Không thể đặt khóa ngoại trực tiếp, vì mỗi ô chỉ chứa một giá trị. Giải pháp là tạo một bảng trung gian, ở đây là DangKy. *[chime]*
- `6:35` Bảng DangKy chứa hai khóa ngoại: MaSV và MaMH, và hai cột này cùng tạo thành khóa chính. Mỗi dòng là một lần đăng ký.
- `6:44` Nhìn lại, quan hệ nhiều-nhiều đã được tách thành hai quan hệ một-nhiều. Đây là kỹ thuật các bạn sẽ dùng rất nhiều khi thiết kế. *[success]*


## Phần 4

### Thiết kế cơ sở dữ liệu và sơ đồ ERD

*Cảnh 6:53 – 7:00 (7.0 giây)*

- `6:54` Phần bốn. Thiết kế cơ sở dữ liệu và sơ đồ ERD. *[riser]*

### Thực thể, thuộc tính, quan hệ

*Cảnh 7:00 – 7:41 (41.1 giây)*

- `7:01` Để thiết kế cơ sở dữ liệu, ta dùng sơ đồ thực thể liên kết, gọi tắt là ERD.
- `7:06` Ba thành phần chính: thực thể, là đối tượng cần quản lý, ví dụ khách hàng; thuộc tính, là thông tin mô tả thực thể, ví dụ họ tên, số điện thoại; và mối quan hệ, là sự liên kết giữa các thực thể. *[chime]*
- `7:19` Trong ký pháp kinh điển, thực thể là hình chữ nhật, thuộc tính là hình elip, quan hệ là hình thoi. Trong thực tế, ta thường dùng dạng bảng gọn hơn, nhưng ý nghĩa không đổi.
- `7:30` Một thực thể sẽ trở thành một bảng. Một thuộc tính trở thành một cột. Khóa chính đảm bảo định danh, còn khóa ngoại hiện thực mối quan hệ.

### Phân tích bài toán bán hàng

*Cảnh 7:41 – 8:28 (47.1 giây)*

- `7:42` Bài toán: xây dựng cơ sở dữ liệu quản lý bán hàng cho một cửa hàng điện thoại. *[whoosh]*
- `7:46` Bước một, phân tích yêu cầu. Cửa hàng cần quản lý khách hàng, sản phẩm, nhân viên, hóa đơn, và chi tiết từng hóa đơn.
- `7:56` Từ các danh từ trong yêu cầu, ta xác định thực thể: KhachHang, SanPham, NhanVien, HoaDon. Và vì một hóa đơn có nhiều sản phẩm, với số lượng và đơn giá riêng, ta cần thêm ChiTietHoaDon. *[chime]*
- `8:09` Bước hai: xác định thuộc tính và khóa chính cho từng thực thể. Bước ba: xác định quan hệ và số lượng giữa chúng.
- `8:16` Một khách hàng có nhiều hóa đơn. Một nhân viên lập nhiều hóa đơn. Một hóa đơn có nhiều chi tiết. Và mỗi chi tiết ứng với một sản phẩm.

### Sơ đồ ERD cửa hàng điện thoại

*Cảnh 8:28 – 9:03 (34.8 giây)*

- `8:29` Đây là sơ đồ ERD hoàn chỉnh: năm thực thể, với khóa chính màu vàng và khóa ngoại màu xanh. *[whoosh]*
- `8:35` KhachHang một-nhiều HoaDon qua MaKH. NhanVien một-nhiều HoaDon qua MaNV. *[chime]*
- `8:40` HoaDon một-nhiều ChiTietHoaDon. SanPham một-nhiều ChiTietHoaDon. Và ChiTietHoaDon có khóa chính ghép: MaHD cộng với MaSP. *[chime]*
- `8:49` Lưu ý: DonGia được lưu trong chi tiết hóa đơn, để giữ đúng giá tại thời điểm bán, kể cả sau này sản phẩm đổi giá. *[sparkle]*
- `8:57` Thiết kế này tránh lặp dữ liệu, và đảm bảo mỗi thông tin chỉ được lưu ở một nơi hợp lý.


## Phần 5

### Ngôn ngữ SQL cơ bản

*Cảnh 9:03 – 9:09 (6.3 giây)*

- `9:04` Phần năm. Ngôn ngữ SQL cơ bản. *[riser]*

### Năm nhóm lệnh SQL

*Cảnh 9:09 – 9:56 (46.5 giây)*

- `9:10` SQL là ngôn ngữ chuẩn để làm việc với cơ sở dữ liệu quan hệ. Các lệnh được chia thành năm nhóm.
- `9:17` DDL, ngôn ngữ định nghĩa dữ liệu: CREATE tạo, ALTER sửa cấu trúc, DROP xóa. *[chime]*
- `9:24` DML, ngôn ngữ thao tác dữ liệu: INSERT thêm, UPDATE cập nhật, DELETE xóa bản ghi.
- `9:31` DQL, ngôn ngữ truy vấn: SELECT. Đây là nhóm lệnh các bạn sẽ dùng nhiều nhất. *[chime]*
- `9:38` DCL, ngôn ngữ điều khiển truy cập: GRANT cấp quyền, REVOKE thu hồi quyền. Và TCL, điều khiển giao dịch: COMMIT xác nhận, ROLLBACK hoàn tác.
- `9:50` Nắm được năm nhóm này, các bạn đã có bản đồ tổng thể về SQL. *[sparkle]*

### DDL: tạo bảng

*Cảnh 9:56 – 10:29 (33.1 giây)*

- `9:56` Hãy tạo bảng SinhVien. CREATE TABLE, tên bảng, sau đó là danh sách cột trong ngoặc. *[whoosh]*
- `10:03` MaSV kiểu VARCHAR mười ký tự, và ghi PRIMARY KEY ngay sau khai báo. *[type]*
- `10:09` HoTen dùng NVARCHAR một trăm, để lưu được tiếng Việt có dấu. Lop là VARCHAR hai mươi. Email là VARCHAR một trăm.
- `10:20` Chạy lệnh, hệ quản trị trả về thông báo tạo bảng thành công. Cấu trúc đã sẵn sàng, nhưng bảng chưa có dữ liệu. *[success]*

### DML và DQL

*Cảnh 10:29 – 11:01 (32.1 giây)*

- `10:30` Thêm một bản ghi bằng INSERT INTO, theo sau là tên bảng và danh sách giá trị, đúng thứ tự các cột. *[type]*
- `10:36` Chuỗi tiếng Việt có dấu nên đặt sau chữ N, ví dụ N Nguyễn Văn An. Đây là cách SQL Server hiểu đó là chuỗi Unicode. *[chime]*
- `10:45` Để xem dữ liệu, dùng SELECT dấu sao FROM SinhVien. Dấu sao nghĩa là lấy tất cả các cột.
- `10:52` Kết quả là một bảng tạm, gọi là result set. Lưu ý: câu lệnh SELECT không làm thay đổi dữ liệu gốc. *[success]*


## Phần 6

### Bài toán truy vấn thực tế

*Cảnh 11:01 – 11:07 (6.0 giây)*

- `11:02` Phần sáu. Các bài toán truy vấn thực tế. *[riser]*

### Dữ liệu cửa hàng điện thoại

*Cảnh 11:07 – 11:32 (24.9 giây)*

- `11:08` Giờ chúng ta vận dụng vào cơ sở dữ liệu cửa hàng điện thoại vừa thiết kế. Đây là dữ liệu mẫu. *[whoosh]*
- `11:14` Bảng SanPham có năm sản phẩm, với giá từ tám triệu đến ba mươi hai triệu. KhachHang có bốn khách. HoaDon và ChiTietHoaDon ghi lại các lần mua.
- `11:24` Mỗi bài toán dưới đây sẽ đi theo bốn bước: đọc đề, phân tích, viết SQL, và đọc kết quả.

### Bài toán 1: Toàn bộ sản phẩm

*Cảnh 11:32 – 11:53 (21.8 giây)*

- `11:32` Bài toán một: hiển thị toàn bộ danh sách sản phẩm để kiểm kê. *[whoosh]*
- `11:36` Phân tích: cần tất cả các cột, của tất cả các dòng, trong bảng SanPham.
- `11:41` Câu lệnh: SELECT dấu sao FROM SanPham. Không có điều kiện, nên lấy toàn bộ năm dòng. *[type]*
- `11:48` Kết quả trả về đủ năm sản phẩm, đúng thứ tự các cột trong bảng. *[success]*

### Bài toán 2: Sản phẩm trên 10 triệu

*Cảnh 11:53 – 12:25 (31.7 giây)*

- `11:54` Bài toán hai: tìm những sản phẩm có giá trên mười triệu, để đưa vào nhóm cao cấp. *[whoosh]*
- `11:59` Phân tích: lọc theo cột DonGia, dùng mệnh đề WHERE với điều kiện lớn hơn mười triệu. Đơn giá tính bằng đồng.
- `12:07` SELECT dấu sao FROM SanPham, WHERE DonGia lớn hơn mười triệu. *[type]*
- `12:13` Ba sản phẩm thỏa điều kiện: iPhone 15 Pro Max, Galaxy S24 Ultra và Xiaomi 14. Hai dòng còn lại bị loại, vì giá không lớn hơn mười triệu. *[success]*

### Bài toán 3: Khách đã mua hàng

*Cảnh 12:25 – 12:58 (33.2 giây)*

- `12:26` Bài toán ba: liệt kê khách hàng đã từng mua hàng, mỗi người một lần. *[whoosh]*
- `12:30` Phân tích: thông tin khách nằm ở bảng KhachHang, nhưng việc mua hàng nằm ở bảng HoaDon. Cần nối hai bảng qua MaKH. Dùng DISTINCT để loại trùng.
- `12:41` SELECT DISTINCT cột HoTen, FROM KhachHang, INNER JOIN HoaDon, ON MaKH bằng nhau. *[type]*
- `12:48` Kết quả chỉ còn những khách có hóa đơn. Khách chưa mua hàng không xuất hiện, vì INNER JOIN chỉ giữ các dòng khớp ở cả hai bảng. *[success]*

### Bài toán 4: Tổng doanh thu

*Cảnh 12:58 – 13:21 (23.0 giây)*

- `12:59` Bài toán bốn: tính tổng doanh thu của cửa hàng. *[whoosh]*
- `13:02` Phân tích: doanh thu của một dòng chi tiết bằng số lượng nhân đơn giá. Tổng doanh thu là tổng của tất cả các dòng.
- `13:10` SELECT SUM của SoLuong nhân DonGia, FROM ChiTietHoaDon. *[type]*
- `13:14` Kết quả: hai trăm mười lăm triệu đồng. Hàm SUM gộp nhiều dòng thành một giá trị duy nhất. *[success]*

### Bài toán 5: Số lượng đã bán

*Cảnh 13:21 – 13:46 (24.7 giây)*

- `13:22` Bài toán năm: thống kê số lượng đã bán của từng sản phẩm. *[whoosh]*
- `13:26` Phân tích: cần nhóm các dòng theo sản phẩm, rồi cộng số lượng trong mỗi nhóm. Đó là GROUP BY.
- `13:33` SELECT MaSP, SUM SoLuong, FROM ChiTietHoaDon, GROUP BY MaSP. *[type]*
- `13:38` iPhone 15 Pro Max dẫn đầu với bốn chiếc. Nhóm theo mã sản phẩm giúp tổng hợp chính xác từng mặt hàng. *[success]*

### Bài toán 6: Kết hợp nhiều bảng

*Cảnh 13:46 – 14:22 (36.4 giây)*

- `13:47` Bài toán sáu, cũng là bài tổng hợp: in ra bảng kê chi tiết, gồm tên khách hàng, tên nhân viên, tên sản phẩm, số lượng và thành tiền. *[whoosh]*
- `13:56` Phân tích: thông tin nằm rải ở bốn bảng. Ta nối HoaDon với KhachHang, NhanVien, rồi ChiTietHoaDon, rồi SanPham, tất cả bằng INNER JOIN.
- `14:06` Câu lệnh nối bốn bảng, và tính thành tiền bằng SoLuong nhân DonGia. *[type]*
- `14:11` Kết quả là một bảng kê đầy đủ, đúng như hóa đơn in cho khách. Đây là sức mạnh của mô hình quan hệ: dữ liệu tách nhỏ để tránh trùng lặp, nhưng vẫn ghép lại được khi cần. *[success]*


## Phần 7

### Tổng kết và ôn tập

*Cảnh 14:22 – 14:28 (6.0 giây)*

- `14:23` Phần bảy. Tổng kết và câu hỏi ôn tập. *[riser]*

### Tổng kết

*Cảnh 14:28 – 15:12 (44.0 giây)*

- `14:29` Chúng ta đã đi qua toàn bộ nền tảng. Hãy chốt lại những ý quan trọng nhất. *[whoosh]*
- `14:34` Cơ sở dữ liệu là dữ liệu có cấu trúc, được quản lý bởi DBMS. Dữ liệu là nguyên liệu, thông tin là kết quả sau xử lý. *[chime]*
- `14:43` Bảng gồm cột và dòng. Khóa chính định danh duy nhất, khóa ngoại liên kết các bảng.
- `14:49` Ba loại quan hệ: một-một, một-nhiều, nhiều-nhiều. Quan hệ nhiều-nhiều cần bảng trung gian.
- `14:56` ERD giúp chuyển bài toán thực tế thành mô hình dữ liệu. Và SQL là công cụ để tạo, cập nhật và truy vấn.
- `15:05` Quy trình thực tế: hiểu yêu cầu, thiết kế ERD, tạo bảng, nhập dữ liệu, rồi truy vấn. *[success]*

### Câu hỏi ôn tập

*Cảnh 15:12 – 17:05 (112.7 giây)*

- `15:13` Đến phần tự kiểm tra. Năm câu hỏi trắc nghiệm, các bạn hãy chọn đáp án trước khi đáp án hiện ra nhé. *[whoosh]*
- `15:20` Câu một: thành phần nào xác định duy nhất mỗi bản ghi trong bảng? A, khóa ngoại. B, khóa chính. C, chỉ mục. D, khóa ghép.
- `15:33` Đáp án đúng là B, khóa chính. Khóa chính không được trùng và không được để trống. *[success]*
- `15:39` Câu hai: quan hệ giữa Lop và SinhVien là loại nào? A, một-một. B, một-nhiều. C, nhiều-nhiều. D, không xác định.
- `15:51` Đáp án đúng là B. Một lớp có nhiều sinh viên, mỗi sinh viên thuộc một lớp. *[success]*
- `15:56` Câu ba: lệnh nào thuộc nhóm DDL? A, INSERT. B, SELECT. C, CREATE TABLE. D, COMMIT.
- `16:09` Đáp án đúng là C. CREATE TABLE định nghĩa cấu trúc bảng, nên thuộc DDL. *[success]*
- `16:14` Câu bốn: để lọc sản phẩm có giá trên mười triệu, dùng mệnh đề nào? A, GROUP BY. B, ORDER BY. C, WHERE. D, HAVING.
- `16:29` Đáp án đúng là C, WHERE. HAVING dùng để lọc sau khi nhóm, còn WHERE lọc từng dòng. *[success]*
- `16:38` Câu năm: quan hệ nhiều-nhiều được xử lý bằng cách nào? A, thêm khóa ngoại vào một bảng. B, tạo bảng trung gian chứa hai khóa ngoại. C, gộp hai bảng làm một. D, dùng khóa chính ghép trong bảng gốc.
- `16:54` Đáp án đúng là B. Bảng trung gian chứa hai khóa ngoại, và chúng tạo thành khóa chính ghép. *[success]*
- `16:59` Nếu các bạn trả lời đúng từ bốn câu trở lên, các bạn đã nắm khá chắc phần nền tảng. *[sparkle]*

### Kết thúc bài giảng

*Cảnh 17:05 – 17:30 (25.2 giây)*

- `17:06` Cơ sở dữ liệu không chỉ là một môn học, mà là nền móng của mọi hệ thống phần mềm. Hiểu dữ liệu, bạn hiểu cách hệ thống vận hành.
- `17:15` Hãy thực hành ngay: cài MySQL hoặc PostgreSQL, tạo bảng SinhVien, và thử viết những truy vấn đầu tiên. *[chime]*
- `17:21` Cảm ơn các bạn đã theo dõi. Chúc các bạn học tốt, và hẹn gặp lại ở bài giảng tiếp theo. *[sparkle]*

