# Nội dung bài giảng — Cơ sở dữ liệu và ứng dụng trong thực tế

## Thông tin chung

| Hạng mục | Nội dung |
|---|---|
| Đối tượng | Sinh viên CNTT năm 1–2, người học nhập môn CSDL |
| Thời lượng | 17 phút 31 giây (bản dựng hoàn chỉnh) |
| Hình thức | Video bài giảng có thuyết minh, phụ đề, đồ họa chuyển động |
| Công cụ minh họa | SQL Server / MySQL (cú pháp tương thích cơ bản) |
| Bài toán xuyên suốt | Cửa hàng điện thoại: sản phẩm, khách hàng, nhân viên, hóa đơn |

## Mục tiêu bài học

Sau bài học, người học có thể:

1. Phát biểu được khái niệm cơ sở dữ liệu, phân biệt dữ liệu và thông tin.
2. Giải thích vai trò của hệ quản trị cơ sở dữ liệu (DBMS) và kể tên bốn hệ phổ biến.
3. Mô tả bảng, dòng, cột; xác định khóa chính, khóa ngoại trong một bảng cụ thể.
4. Phân biệt ba loại quan hệ 1—1, 1—N, N—N và cách hiện thực từng loại.
5. Chuyển một bài toán bán hàng thực tế thành sơ đồ ERD gồm thực thể, thuộc tính, quan hệ.
6. Phân loại năm nhóm lệnh SQL và viết được các lệnh DDL/DML/DQL cơ bản.
7. Viết sáu truy vấn thực tế: lọc, nối bảng, gộp nhóm, tính tổng.

---

## Phần 1 — Giới thiệu cơ sở dữ liệu

### 1.1. Cơ sở dữ liệu là gì?

**Cơ sở dữ liệu (database)** là một tập hợp dữ liệu được tổ chức có cấu trúc, lưu trên máy tính,
được quản lý để nhiều người có thể truy cập, tìm kiếm và cập nhật hiệu quả.

Ba đặc điểm cần nhớ:

- **Có cấu trúc**: dữ liệu được chia thành bảng, cột, kiểu dữ liệu rõ ràng.
- **Có quan hệ**: các phần tử dữ liệu liên kết với nhau (sinh viên thuộc lớp, hóa đơn thuộc khách).
- **Được quản lý**: có phần mềm kiểm soát truy cập, sao lưu, phục hồi và xử lý đồng thời.

Ví dụ: danh sách sinh viên, hóa đơn bán hàng, lịch sử giao dịch ngân hàng.

### 1.2. Dữ liệu và thông tin

| | Dữ liệu | Thông tin |
|---|---|---|
| Bản chất | Sự kiện thô, chưa xử lý | Kết quả sau khi xử lý, tổng hợp |
| Ví dụ | `32000000`, `05/03/2024`, `HD001` | "Doanh thu tháng 3 là 97 triệu" |
| Vai trò | Nguyên liệu | Sản phẩm phục vụ ra quyết định |

Cùng một tập dữ liệu, khi tính tổng doanh thu theo tháng ta thu được thông tin để ra quyết định.
Dữ liệu là nguyên liệu, thông tin là sản phẩm.

### 1.3. Vì sao cần cơ sở dữ liệu?

Lưu dữ liệu bằng file rời (Excel, sổ sách) gặp bốn vấn đề khi dữ liệu lớn:

| Vấn đề | Cách CSDL giải quyết |
|---|---|
| Dư thừa dữ liệu | Chuẩn hóa cấu trúc, lưu mỗi thông tin một nơi |
| Dữ liệu không nhất quán | Ràng buộc (constraint) kiểm tra khi nhập |
| Tìm kiếm chậm | Chỉ mục (index) |
| Không chia sẻ an toàn | Phân quyền người dùng, giao dịch đồng thời |

Nhiều người có thể làm việc cùng lúc mà không ghi đè dữ liệu của nhau.

### 1.4. Bài toán cửa hàng điện thoại

Bối cảnh: khoảng **1.200 sản phẩm**, **380 khách hàng**, hơn **5.000 hóa đơn/năm**.

- Nếu mỗi nhân viên giữ một file Excel: giá cũ, tồn kho sai, khách hàng trùng lặp, không đồng bộ được.
- Với CSDL tập trung: bán một chiếc điện thoại → tồn kho tự giảm, hóa đơn được ghi, doanh thu cập nhật ngay.

### 1.5. Hệ quản trị cơ sở dữ liệu (DBMS)

CSDL là dữ liệu; **DBMS** là phần mềm tạo, quản lý và truy vấn dữ liệu đó.

| DBMS | Đặc điểm |
|---|---|
| MySQL | Mã nguồn mở, phổ biến cho ứng dụng web |
| SQL Server | Của Microsoft, tích hợp hệ sinh thái Windows/.NET |
| PostgreSQL | Mạnh về chuẩn SQL và khả năng mở rộng |
| Oracle | Hệ thống lớn: ngân hàng, tài chính, doanh nghiệp |

Điểm chung: cả bốn dùng **SQL**. Ngoài truy vấn, DBMS còn lo bảo mật, sao lưu, phục hồi và xử lý đồng thời.

---

## Phần 2 — Các thành phần của cơ sở dữ liệu

### 2.1. Bảng, dòng, cột

Bảng `SinhVien`:

| MaSV | HoTen | Lop | Email |
|---|---|---|---|
| SV001 | Nguyễn Văn An | DA22TTC | an@gmail.com |
| SV002 | Trần Thị Bình | DA22TTC | binh@gmail.com |
| SV003 | Lê Văn Nam | DA22TTC | nam@gmail.com |

- **Cột (field)**: thuộc tính, quy định kiểu dữ liệu và ý nghĩa — `MaSV`, `HoTen`, `Lop`, `Email`.
- **Dòng (record)**: một đối tượng cụ thể — mỗi dòng là một sinh viên.
- **Bảng (table)**: tập hợp các bản ghi cùng loại.

### 2.2. Khóa chính (primary key)

Khóa chính là một cột (hoặc tổ hợp cột) **xác định duy nhất** mỗi bản ghi:

- Không được trùng.
- Không được để trống (NULL).

Trong `SinhVien`, `MaSV` là khóa chính. Nếu không có mã định danh, hai sinh viên cùng tên
"Nguyễn Văn An" sẽ khiến hệ thống không biết đang cập nhật hồ sơ của ai.

### 2.3. Khóa ngoại (foreign key)

Khóa ngoại tạo cầu nối giữa hai bảng: giá trị của nó phải trỏ tới một khóa chính tồn tại.

Ví dụ: `MaLop` trong `SinhVien` là khóa ngoại tham chiếu `MaLop` (PK) của bảng `Lop`.

Thử `INSERT` một sinh viên với `MaLop = 'DA99'` khi lớp này không tồn tại → DBMS từ chối.
Đó là **ràng buộc toàn vẹn tham chiếu**.

---

## Phần 3 — Các loại mối quan hệ

### 3.1. Một—một (1—1)

Một sinh viên có đúng một hồ sơ; mỗi hồ sơ thuộc về đúng một sinh viên.

Cách hiện thực: đặt khóa ngoại `MaSV` trong bảng `HoSo`, kèm ràng buộc **UNIQUE** để mỗi sinh viên
chỉ có tối đa một hồ sơ.

Dùng khi cần tách thông tin ít dùng hoặc nhạy cảm sang bảng riêng để dễ phân quyền.

### 3.2. Một—nhiều (1—N)

Một lớp có nhiều sinh viên; mỗi sinh viên chỉ thuộc một lớp.

Cách hiện thực: đặt khóa ngoại ở **phía nhiều** — cột `MaLop` nằm trong bảng `SinhVien`.

Đây là quan hệ phổ biến nhất: khách hàng—hóa đơn, danh mục—sản phẩm, nhân viên—hợp đồng.

### 3.3. Nhiều—nhiều (N—N)

Một sinh viên đăng ký nhiều môn; một môn có nhiều sinh viên.

Không thể đặt khóa ngoại trực tiếp (mỗi ô chỉ chứa một giá trị). Giải pháp: **bảng trung gian** `DangKy`:

| MaSV | MaMH |
|---|---|
| SV001 | MH01 |
| SV001 | MH02 |
| SV002 | MH01 |

Hai cột `MaSV`, `MaMH` vừa là khóa ngoại vừa tạo thành **khóa chính ghép**. Quan hệ N—N được tách
thành hai quan hệ 1—N — kỹ thuật dùng rất nhiều khi thiết kế.

---

## Phần 4 — Thiết kế cơ sở dữ liệu và sơ đồ ERD

### 4.1. Thực thể, thuộc tính, quan hệ

**ERD** (Entity–Relationship Diagram) gồm:

- **Thực thể**: đối tượng cần quản lý — KhachHang, SanPham.
- **Thuộc tính**: thông tin mô tả thực thể — HoTen, DienThoai.
- **Quan hệ**: liên kết giữa các thực thể — khách hàng lập hóa đơn.

Ký pháp kinh điển: thực thể = hình chữ nhật, thuộc tính = elip, quan hệ = hình thoi.
Khi cài đặt: thực thể → bảng, thuộc tính → cột, khóa chính → định danh, khóa ngoại → hiện thực quan hệ.

### 4.2. Phân tích bài toán bán hàng

Yêu cầu: quản lý khách hàng, sản phẩm, nhân viên, hóa đơn và chi tiết từng hóa đơn.

**Bước 1 — Xác định thực thể** (từ các danh từ trong yêu cầu):
`KHACHHANG`, `SANPHAM`, `NHANVIEN`, `HOADON`, `CHITIETHOADON`.

**Bước 2 — Xác định thuộc tính và khóa chính** cho từng thực thể.

**Bước 3 — Xác định quan hệ và số lượng:**

- Khách hàng 1—N hóa đơn.
- Nhân viên 1—N hóa đơn.
- Hóa đơn 1—N chi tiết hóa đơn.
- Sản phẩm 1—N chi tiết hóa đơn.

### 4.3. Sơ đồ ERD hoàn chỉnh

- `KHACHHANG(MaKH PK, HoTen, DienThoai, DiaChi)`
- `NHANVIEN(MaNV PK, HoTen, ChucVu)`
- `SANPHAM(MaSP PK, TenSP, Hang, DonGia, SoLuongTon)`
- `HOADON(MaHD PK, NgayLap, MaKH FK, MaNV FK)`
- `CHITIETHOADON(MaHD PK/FK, MaSP PK/FK, SoLuong, DonGia)`

Lưu ý: `DonGia` lưu trong chi tiết hóa đơn để giữ đúng giá tại thời điểm bán, kể cả khi sản phẩm
đổi giá sau này. Thiết kế này tránh lặp dữ liệu và đảm bảo mỗi thông tin chỉ lưu ở một nơi hợp lý.

---

## Phần 5 — Ngôn ngữ SQL cơ bản

### 5.1. Năm nhóm lệnh

| Nhóm | Tên đầy đủ | Lệnh tiêu biểu |
|---|---|---|
| DDL | Data Definition Language | `CREATE`, `ALTER`, `DROP` |
| DML | Data Manipulation Language | `INSERT`, `UPDATE`, `DELETE` |
| DQL | Data Query Language | `SELECT` |
| DCL | Data Control Language | `GRANT`, `REVOKE` |
| TCL | Transaction Control Language | `COMMIT`, `ROLLBACK` |

`SELECT` là nhóm lệnh dùng nhiều nhất trong thực tế.

### 5.2. DDL — tạo bảng

```sql
CREATE TABLE SinhVien (
    MaSV  VARCHAR(10)  PRIMARY KEY,
    HoTen NVARCHAR(100),
    Lop   VARCHAR(20),
    Email VARCHAR(100)
);
```

`NVARCHAR` lưu được tiếng Việt có dấu. Chạy lệnh thành công: bảng đã có cấu trúc nhưng chưa có dữ liệu.

### 5.3. DML và DQL

```sql
INSERT INTO SinhVien
VALUES ('SV001', N'Nguyễn Văn An', 'DA22TTC', 'an@gmail.com');

SELECT * FROM SinhVien;
```

- Chữ `N` trước chuỗi giúp SQL Server hiểu đó là chuỗi Unicode.
- `SELECT *` lấy tất cả cột; kết quả là **result set** (bảng tạm), không làm thay đổi dữ liệu gốc.

---

## Phần 6 — Bài toán truy vấn thực tế

Dữ liệu mẫu đầy đủ ở [du-lieu-erd.md](du-lieu-erd.md). Mỗi bài đi theo bốn bước:
**đọc đề → phân tích → viết SQL → đọc kết quả**.

| # | Yêu cầu | Kiến thức | Kết quả |
|---|---|---|---|
| 1 | Toàn bộ sản phẩm | `SELECT *` | 5 dòng |
| 2 | Sản phẩm trên 10 triệu | `WHERE` | 3 sản phẩm |
| 3 | Khách đã từng mua | `INNER JOIN`, `DISTINCT` | 3 khách |
| 4 | Tổng doanh thu | `SUM` | 215.000.000 |
| 5 | Số lượng bán theo sản phẩm | `GROUP BY`, `SUM` | SP01 dẫn đầu: 4 |
| 6 | Bảng kê chi tiết | nối 4 bảng | 8 dòng |

### Bài 1

```sql
SELECT * FROM SanPham;
```

Không có điều kiện → lấy toàn bộ 5 dòng, đúng thứ tự cột.

### Bài 2

```sql
SELECT * FROM SanPham
WHERE DonGia > 10000000;
```

Ba sản phẩm thỏa: iPhone 15 Pro Max, Galaxy S24 Ultra, Xiaomi 14. Hai dòng còn lại bị loại
vì giá không lớn hơn 10 triệu.

### Bài 3

```sql
SELECT DISTINCT KH.HoTen
FROM KhachHang KH
INNER JOIN HoaDon HD ON KH.MaKH = HD.MaKH;
```

`INNER JOIN` chỉ giữ các dòng khớp ở cả hai bảng, nên khách chưa mua hàng không xuất hiện.
`DISTINCT` loại trùng khi một khách có nhiều hóa đơn.

### Bài 4

```sql
SELECT SUM(SoLuong * DonGia) AS TongDoanhThu
FROM ChiTietHoaDon;
```

Doanh thu một dòng = `SoLuong × DonGia`; `SUM` gộp nhiều dòng thành một giá trị: 215.000.000.

### Bài 5

```sql
SELECT MaSP, SUM(SoLuong) AS TongSoLuong
FROM ChiTietHoaDon
GROUP BY MaSP;
```

`GROUP BY` gom các dòng theo sản phẩm rồi cộng số lượng trong mỗi nhóm.
iPhone 15 Pro Max dẫn đầu với 4 chiếc.

### Bài 6

```sql
SELECT HD.MaHD, KH.HoTen AS KhachHang,
       NV.HoTen AS NhanVien, SP.TenSP,
       CT.SoLuong, CT.SoLuong * CT.DonGia AS ThanhTien
FROM HoaDon HD
INNER JOIN KhachHang KH ON HD.MaKH = KH.MaKH
INNER JOIN NhanVien NV ON HD.MaNV = NV.MaNV
INNER JOIN ChiTietHoaDon CT ON HD.MaHD = CT.MaHD
INNER JOIN SanPham SP ON CT.MaSP = SP.MaSP;
```

Kết quả là bảng kê đầy đủ như hóa đơn in cho khách. Đây là sức mạnh của mô hình quan hệ:
dữ liệu tách nhỏ để tránh trùng lặp nhưng vẫn ghép lại được khi cần.

---

## Phần 7 — Tổng kết và ôn tập

### 7.1. Tổng kết

1. CSDL là tập dữ liệu có cấu trúc, được quản lý; DBMS là phần mềm quản lý.
2. Bảng gồm cột (thuộc tính) và dòng (bản ghi); khóa chính định danh, khóa ngoại liên kết.
3. Ba loại quan hệ: 1—1, 1—N, N—N; N—N cần bảng trung gian.
4. ERD chuyển bài toán thực tế thành mô hình dữ liệu.
5. SQL gồm DDL, DML, DQL, DCL, TCL.
6. Quy trình thực tế: hiểu yêu cầu → thiết kế ERD → tạo bảng → nhập dữ liệu → truy vấn.

### 7.2. Câu hỏi ôn tập

| # | Câu hỏi | Đáp án | Giải thích |
|---|---|---|---|
| 1 | Thành phần nào xác định duy nhất mỗi bản ghi? | **B. Khóa chính** | Không trùng, không để trống |
| 2 | Quan hệ giữa Lop và SinhVien? | **B. Một—nhiều** | Một lớp có nhiều SV, mỗi SV thuộc một lớp |
| 3 | Lệnh nào thuộc DDL? | **C. CREATE TABLE** | Định nghĩa cấu trúc bảng |
| 4 | Lọc sản phẩm giá trên 10 triệu dùng mệnh đề nào? | **C. WHERE** | Lọc từng dòng; HAVING lọc sau khi nhóm |
| 5 | N—N được xử lý bằng cách nào? | **B. Bảng trung gian chứa hai khóa ngoại** | Hai FK tạo thành khóa chính ghép |

### 7.3. Bài tập tự luyện

1. Tạo bảng `SanPham` với các cột trong tài liệu dữ liệu, dùng `CREATE TABLE`.
2. Viết truy vấn liệt kê sản phẩm có tồn kho dưới 10.
3. Tính doanh thu theo từng khách hàng (gợi ý: nối `HoaDon` với `ChiTietHoaDon`, `GROUP BY MaKH`).
4. Thiết kế ERD cho thư viện: độc giả, sách, phiếu mượn, chi tiết phiếu mượn.
