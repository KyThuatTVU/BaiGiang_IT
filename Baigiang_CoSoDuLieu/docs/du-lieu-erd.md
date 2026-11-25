# Dữ liệu & mô hình ERD — Cửa hàng điện thoại

Tài liệu này là nguồn tham chiếu duy nhất cho dữ liệu hiển thị trong video: sơ đồ ERD (Phần 4),
bảng dữ liệu mẫu (Phần 6) và kết quả của 6 bài toán truy vấn.

## 1. Lược đồ quan hệ

```
KHACHHANG(MaKH PK, HoTen, DienThoai, DiaChi)
NHANVIEN (MaNV PK, HoTen, ChucVu)
SANPHAM  (MaSP PK, TenSP, Hang, DonGia, SoLuongTon)
HOADON   (MaHD PK, NgayLap, MaKH FK→KHACHHANG, MaNV FK→NHANVIEN)
CHITIETHOADON(MaHD PK/FK→HOADON, MaSP PK/FK→SANPHAM, SoLuong, DonGia)
```

| Bảng | Khóa chính | Khóa ngoại | Ghi chú thiết kế |
|---|---|---|---|
| KHACHHANG | MaKH | — | Một khách có nhiều hóa đơn |
| NHANVIEN | MaNV | — | Một nhân viên lập nhiều hóa đơn |
| SANPHAM | MaSP | — | Đơn giá hiện hành, tồn kho |
| HOADON | MaHD | MaKH, MaNV | Tổng tiền là thuộc tính dẫn xuất, tính từ chi tiết |
| CHITIETHOADON | (MaHD, MaSP) | MaHD, MaSP | Lưu DonGia tại thời điểm bán (giá lịch sử) |

### Quan hệ

- KHACHHANG 1—N HOADON (qua `MaKH`)
- NHANVIEN 1—N HOADON (qua `MaNV`)
- HOADON 1—N CHITIETHOADON (qua `MaHD`)
- SANPHAM 1—N CHITIETHOADON (qua `MaSP`)
- CHITIETHOADON là bảng trung gian giải quyết quan hệ N—N giữa HOADON và SANPHAM;
  khóa chính ghép `(MaHD, MaSP)` đảm bảo mỗi sản phẩm xuất hiện tối đa một lần trong một hóa đơn.

`DonGia` được lưu trong CHITIETHOADON thay vì chỉ đọc từ SANPHAM, để hóa đơn cũ vẫn giữ đúng
giá tại thời điểm bán kể cả khi sản phẩm đổi giá về sau.

## 2. Dữ liệu mẫu

### SANPHAM — 5 dòng

| MaSP | TenSP | Hang | DonGia | SoLuongTon |
|---|---|---|---:|---:|
| SP01 | iPhone 15 Pro Max | Apple | 32.000.000 | 12 |
| SP02 | Galaxy S24 Ultra | Samsung | 30.000.000 | 8 |
| SP03 | Xiaomi 14 | Xiaomi | 14.000.000 | 21 |
| SP04 | OPPO Reno 11 | OPPO | 9.500.000 | 17 |
| SP05 | Galaxy A55 | Samsung | 8.000.000 | 34 |

### KHACHHANG — 4 dòng

| MaKH | HoTen | DienThoai | DiaChi |
|---|---|---|---|
| KH01 | Nguyễn Văn An | 0901 234 567 | Quận 1, TP.HCM |
| KH02 | Trần Thị Bình | 0912 345 678 | Thủ Đức, TP.HCM |
| KH03 | Lê Văn Nam | 0987 654 321 | Quận 7, TP.HCM |
| KH04 | Phạm Thu Hà | 0909 888 777 | Bình Thạnh, TP.HCM |

### NHANVIEN — 2 dòng

| MaNV | HoTen | ChucVu |
|---|---|---|
| NV01 | Nguyễn Minh Tuấn | Quản lý cửa hàng |
| NV02 | Trần Hoài An | Nhân viên bán hàng |

### HOADON — 5 dòng

| MaHD | NgayLap | MaKH | MaNV |
|---|---|---|---|
| HD001 | 05/03/2024 | KH01 | NV01 |
| HD002 | 12/03/2024 | KH02 | NV01 |
| HD003 | 02/04/2024 | KH01 | NV02 |
| HD004 | 18/04/2024 | KH03 | NV02 |
| HD005 | 25/04/2024 | KH03 | NV01 |

### CHITIETHOADON — 8 dòng

| MaHD | MaSP | SoLuong | DonGia | Thành tiền |
|---|---|---:|---:|---:|
| HD001 | SP01 | 1 | 32.000.000 | 32.000.000 |
| HD001 | SP05 | 2 | 8.000.000 | 16.000.000 |
| HD002 | SP02 | 1 | 30.000.000 | 30.000.000 |
| HD002 | SP04 | 2 | 9.500.000 | 19.000.000 |
| HD003 | SP01 | 2 | 32.000.000 | 64.000.000 |
| HD004 | SP03 | 1 | 14.000.000 | 14.000.000 |
| HD004 | SP05 | 1 | 8.000.000 | 8.000.000 |
| HD005 | SP01 | 1 | 32.000.000 | 32.000.000 |

Tổng doanh thu: **215.000.000 đồng** (48 + 49 + 64 + 22 + 32 triệu).

## 3. Sáu bài toán truy vấn

### Bài 1 — Toàn bộ sản phẩm

```sql
SELECT * FROM SanPham;
```

Kết quả: 5 dòng, đủ 5 cột.

### Bài 2 — Sản phẩm trên 10 triệu

```sql
SELECT * FROM SanPham
WHERE DonGia > 10000000;
```

Kết quả: SP01 (32 triệu), SP02 (30 triệu), SP03 (14 triệu).

### Bài 3 — Khách đã từng mua hàng

```sql
SELECT DISTINCT KH.HoTen
FROM KhachHang KH
INNER JOIN HoaDon HD ON KH.MaKH = HD.MaKH;
```

Kết quả: Nguyễn Văn An, Trần Thị Bình, Lê Văn Nam. KH04 (Phạm Thu Hà) không xuất hiện
vì chưa có hóa đơn.

### Bài 4 — Tổng doanh thu

```sql
SELECT SUM(SoLuong * DonGia) AS TongDoanhThu
FROM ChiTietHoaDon;
```

Kết quả: **215.000.000**.

### Bài 5 — Số lượng đã bán theo sản phẩm

```sql
SELECT MaSP, SUM(SoLuong) AS TongSoLuong
FROM ChiTietHoaDon
GROUP BY MaSP;
```

| MaSP | TongSoLuong |
|---|---:|
| SP01 | 4 |
| SP02 | 1 |
| SP03 | 1 |
| SP04 | 2 |
| SP05 | 3 |

### Bài 6 — Bảng kê chi tiết (nối 4 bảng)

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

Kết quả: 8 dòng, tổng thành tiền 215.000.000 — khớp với bài 4.

## 4. Kiểm tra tính nhất quán

| Kiểm tra | Kết quả |
|---|---|
| Số sản phẩm | 5 |
| Số khách hàng | 4 |
| Số hóa đơn | 5 |
| Số dòng chi tiết | 8 |
| Doanh thu (SUM) | 215.000.000 |
| Sản phẩm bán chạy | SP01 — 4 chiếc |
| Số khách đã mua | 3 |
| Số sản phẩm > 10 triệu | 3 |
