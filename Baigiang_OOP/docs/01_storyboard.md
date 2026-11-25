# STORYBOARD — LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP) VỚI JAVA

Trạng thái: **Cổng A — chờ duyệt**. Chưa sản xuất full.

## 1. Thông tin bài

- Nguồn: `Content.md` (5 phần) + `note.md` ("Video tầm 5 phút").
- Thời lượng mục tiêu: **~5:00–5:30** (chốt theo audio thật; 61 cue, ~860–900 từ).
- Kỹ thuật: 1920×1080, 30 fps, H.264 + AAC 48 kHz, loudness −14 LUFS.
- Giọng: **clone VieNeu mặc định** (`Kit/tools/tts_vieneu.py`, ref `Kit/cache/ref_voice/ref_final.wav` — nam, giọng Bắc). Không nhạc nền (theo chuỗi bài hiện hành), chỉ SFX tổng hợp.
- Nhân vật An (Kit `character.py`) xuất hiện xuyên suốt, không che code/ảnh/phụ đề.
- Nền tối tech `demo20.bg()`; chữ Be Vietnam Pro, code JetBrains Mono; logo AN TECH góc trên trái + watermark.
- Màu: nền navy (chủ đạo) · chữ trắng ngà · nhấn chính **BLUE #60A5FA**; mỗi tính chất một màu nhấn: Đóng gói **EMER #34D399**, Kế thừa **BLUE**, Đa hình **AMBER #F59E0B**, Trừu tượng **VIOLET #8B5CF6**.

## 2. Bảng thuật ngữ và cách đọc (chưa xác minh — test ở Cổng B)

| Thuật ngữ | Nhóm | Cách đọc dự kiến | Ghi chú | Trạng thái |
|---|---|---|---|---|
| OOP | Viết tắt | A: "Ô Ốp" · B: "Ô-Ô-Pê" · C: đọc đủ "Object-Oriented Programming" | A/B/C sampler ở Cổng B, user chọn | Chưa xác minh |
| Java | Ngôn ngữ | "Da-va" (giữ tiếng Anh) | không đọc "Gia-va" kiểu Việt hóa nếu clone đọc sai | Chưa xác minh |
| Class / Object | Khái niệm | giữ tiếng Anh | nói chậm, rõ | Chưa xác minh |
| Encapsulation | Tính chất | giữ tiếng Anh, chậm | fallback phiên âm nếu ASR sai | Chưa xác minh |
| Inheritance | Tính chất | giữ tiếng Anh, chậm | nt | Chưa xác minh |
| Polymorphism | Tính chất | giữ tiếng Anh, chậm | nt | Chưa xác minh |
| Abstraction | Tính chất | giữ tiếng Anh, chậm | nt | Chưa xác minh |
| extends / implements / interface / private | Java | giữ tiếng Anh | chỉ xuất hiện khi đọc code | Chưa xác minh |
| @Override / Method Overriding | Java | "Method Overriding" | không đọc ký tự @ | Chưa xác minh |
| C++ / C# | Ngôn ngữ | "C plus plus" / "C sắc" (viết cho TTS) | hiển thị trên màn hình "C++, C#" | Chưa xác minh |

Quy tắc: tên định danh trong code (hoTen, napTien, NhanVienFullTime…) **không đọc nguyên văn** — lời thoại dùng tiếng Việt ("họ tên", "nạp tiền", "nhân viên toàn thời gian"), code hiển thị trên màn hình.

## 3. Kế hoạch dùng ảnh trong `img/` (21 ảnh — dùng 16, loại 5 có lý do)

| Ảnh | Nội dung | Cảnh dùng | Chế độ |
|---|---|---|---|
| 1.jpg | Tổng quan 5 khái niệm Java OOP | S01 mở đầu | contain |
| 2.jpg | 4 trụ cột OOP (4 thẻ) | S09 tổng kết | contain |
| 3.jpg | Class & Object trong Java (5 cột) | S02 khái niệm | contain |
| 4.jpg | Person class → John/Dessy (data members + methods) | S02 thuộc tính/phương thức | contain |
| 5.jpg | 4 trụ cột line-icon | S03 bốn tính chất | contain |
| 6.jpg | Vehicle class → Tesla/Ford (instantiation) | S02 đối tượng cụ thể | contain |
| 8.jpg | Ảnh thật: gõ code Java trên laptop | S01 "viết code" | **cover** |
| 11.jpg | Vẽ tay: Class Car = blueprint → 3 object | S02 lớp là bản thiết kế | contain |
| 12.jpg | Encapsulation: private + getter/setter, X/✓ | S04 đóng gói | contain |
| 13.jpg | UML Animal → Dog/Cat/Horse | S05 kế thừa | contain |
| 14.jpg | Java Polymorphism: overload vs override | S06 đa hình | contain |
| 15.jpg | Open-Closed: IPaymentMethod → PayPal/CreditCard | S07 trừu tượng | contain |
| 16.jpg | Dashboard quản lý nhà hàng trên bàn làm việc | S08 thứ nhất | contain |
| 17.jpg | UI quản lý sản phẩm thương mại điện tử | S08 thứ hai | contain |
| 18.jpg | Dashboard quản lý bệnh viện | S08 thứ ba | contain |
| 19.jpg | App thanh toán trên điện thoại | S08 thứ tư | contain |

Loại có lý do: **7** (trùng ý 3/11, chất lượng thấp hơn) · **9, 10** (trùng 2/5 về bốn trụ cột) · **20** (trùng 18) · **21** (UI tiếng Ý, dễ gây rối ngữ cảnh Việt).

Cách trình bày: photo card kính tối (theo `Biagiang_ThanhToanTheNH/tools/demo_full.py` — `photo()`, `pic_w()`, `photo_card()`), ảnh chụp → `cover`, infographic/UI → `contain` (nền mờ tối, khung đúng tỉ lệ). Ảnh chỉ xuất hiện khi lời đọc nói đúng nội dung ảnh.

## 4. Storyboard 9 cảnh — 61 cue

### S01 · MỞ ĐẦU (0:00–0:30) — ảnh 1, 8 · nhấn BLUE

| Cue | Lời thoại | Hình / chữ trên màn hình | Chuyển động · SFX |
|---|---|---|---|
| c01 | Xin chào các bạn! Chào mừng các bạn đã quay trở lại với An Tech Academy. | Header AN TECH ACADEMY + logo; tiêu đề "LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG · OOP VỚI JAVA"; ảnh 1 photo card giữa | Logo pop + whoosh; An pose `wave` |
| c02 | Khi xây dựng một phần mềm, chúng ta không chỉ quan tâm đến việc viết code sao cho chương trình chạy được. | ảnh 1 thu nhỏ góc trái; dòng keyword "chạy được" | card trượt vào, tick |
| c03 | Mà còn phải tổ chức mã nguồn như thế nào để dễ quản lý, dễ mở rộng và dễ bảo trì. | Ảnh 8 (cover) photo card phải; 3 chip: Dễ quản lý · Dễ mở rộng · Dễ bảo trì | 3 chip pop lần lượt; An `point_left` |
| c04 | Và đó chính là lý do chúng ta cần tìm hiểu về lập trình hướng đối tượng, hay còn gọi là OOP. | Từ khóa lớn "OOP" viết tay (nét marker) + "Object-Oriented Programming" | draw_marker + chime |
| c05 | Trong bài học hôm nay, chúng ta sẽ tìm hiểu khái niệm OOP, bốn tính chất quan trọng nhất, thông qua ngôn ngữ Java. | Agenda 3 dòng: Khái niệm · 4 tính chất · Ứng dụng thực tế | fade từng dòng; whoosh nhẹ |
| c06 | Đồng thời, chúng ta sẽ xem OOP được ứng dụng như thế nào trong những dự án phần mềm thực tế. | nt | nt |

Mục tiêu: chào hỏi, nêu vấn đề, giới thiệu 3 phần của bài.

### S02 · OOP LÀ GÌ? CLASS & OBJECT (0:30–1:30) — ảnh 3, 11, 4, 6 + code

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c07 | Các bạn hãy tưởng tượng chúng ta đang xây dựng một phần mềm quản lý sinh viên. | Ảnh 3 photo card; kicker "VÍ DỤ THỰC TẾ" | slide-in + pop |
| c08 | Mỗi sinh viên sẽ có những thông tin như mã sinh viên, họ tên, tuổi và email. | 4 chip thuộc tính: Mã SV · Họ tên · Tuổi · Email | chip pop lần lượt |
| c09 | Đồng thời, sinh viên cũng có những hành động như đăng ký môn học, xem điểm và cập nhật thông tin. | 3 chip hành động | nt |
| c10 | Thay vì viết tất cả dữ liệu và chức năng một cách rời rạc, OOP cho phép chúng ta gom những thông tin và hành động có liên quan vào một đối tượng. | Gom 7 chip vào 1 khung "ĐỐI TƯỢNG SINH VIÊN" | các chip bay vào khung; chime |
| c11 | Trong Java, chúng ta có hai khái niệm quan trọng. | Chia đôi màn hình; nhãn "CLASS" / "OBJECT" | whoosh |
| c12 | Class — lớp — là bản thiết kế để tạo ra các đối tượng. | Ảnh 11 (blueprint Car → 3 object) | marker gạch chân "bản thiết kế"; An `point_left` |
| c13 | Object — đối tượng — là một thực thể cụ thể được tạo ra từ lớp. | nt, highlight 3 object | tick nhẹ |
| c14 | Ví dụ, lớp SinhVien có thuộc tính họ tên, tuổi, và phương thức hiển thị thông tin. | Ảnh 4 (Person → John/Dessy) | photo card trượt vào |
| c15 | Trong hàm main, chúng ta tạo đối tượng sv từ lớp SinhVien, gán họ tên là Nguyễn Văn An, tuổi hai mươi. | Code panel Java `SinhVien` + `Main` (JetBrains Mono), highlight dòng `new SinhVien()` | gõ code từng dòng + tick; An `write` |
| c16 | Sau đó gọi phương thức hiển thị thông tin. | Highlight dòng `sv.hienThiThongTin();` | marker khoanh dòng; click |
| c17 | Ở đây, SinhVien là lớp, còn sv là một đối tượng được tạo ra từ lớp đó. | Ảnh 6 (Vehicle → Tesla/Ford) | callout "class → object" |
| c18 | Đây chính là nền tảng đầu tiên của lập trình hướng đối tượng. | Chốt ý: "Class = bản thiết kế · Object = thực thể" | underline marker + chime |

Mục tiêu: hiểu class/object, thấy quan hệ blueprint → instance, đọc được code tối thiểu.

### S03 · BỐN TÍNH CHẤT (1:30–1:45) — ảnh 5

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c19 | Đây là nội dung trọng tâm của bài học. Lập trình hướng đối tượng có bốn tính chất cơ bản: Đóng gói, Kế thừa, Đa hình và Trừu tượng. | Ảnh 5 giữa; 4 nhãn màu tương ứng | 4 nhãn pop theo thứ tự, mỗi nhãn 1 tick |
| c20 | Chúng ta sẽ đi qua từng tính chất, kèm ví dụ và code Java minh họa. | 4 chip chuyển thành roadmap ngang | whoosh nhẹ |

### S04 · TÍNH CHẤT 1 — ĐÓNG GÓI (1:45–2:25) — ảnh 12 + code · nhấn EMER

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c21 | Tính chất thứ nhất: Đóng gói — Encapsulation. | Section title "TÍNH CHẤT 1 · ĐÓNG GÓI"; ảnh 12 photo card | thud + shimmer |
| c22 | Đóng gói có nghĩa là chúng ta bảo vệ dữ liệu bên trong đối tượng, không cho phép bên ngoài truy cập và thay đổi tùy ý. | Highlight ổ khóa + "PRIVATE DATA" trên ảnh | marker khoanh; An `point_left` |
| c23 | Ví dụ, trong phần mềm quản lý ngân hàng, số dư tài khoản không nên được thay đổi trực tiếp từ bên ngoài. | Chip "Số dư tài khoản" + dấu X đỏ (trực tiếp) | pop + buzz nhẹ |
| c24 | Trong Java, ta khai báo số dư là private. Muốn nạp tiền, phải thông qua phương thức napTien. | Code panel `TaiKhoan`: `private double soDu;` + `napTien()` | gõ code; highlight `private` |
| c25 | Phương thức này kiểm tra số tiền hợp lệ trước khi cộng vào số dư. | Highlight `if (tien > 0)` | khoanh dòng; tick |
| c26 | Muốn xem số dư, ta dùng phương thức getSoDu. | Highlight `getSoDu()` | nt |
| c27 | Đóng gói đảm bảo dữ liệu an toàn, hạn chế sai sót và kiểm soát cách truy cập dữ liệu. | 3 chip: An toàn · Ít sai sót · Kiểm soát truy cập | pop + chime |

### S05 · TÍNH CHẤT 2 — KẾ THỪA (2:25–3:05) — ảnh 13 + code · nhấn BLUE

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c28 | Tính chất thứ hai: Kế thừa — Inheritance. | Section title; ảnh 13 (UML Animal) | thud + shimmer |
| c29 | Kế thừa cho phép một lớp con sử dụng lại những thuộc tính và phương thức của lớp cha. | Highlight mũi tên tam giác Animal → Dog/Cat/Horse | marker vẽ mũi tên; An `point_left` |
| c30 | Ví dụ, lớp Animal có phương thức eat và sleep. Các lớp Dog, Cat, Horse kế thừa từ Animal, và có thêm hành vi riêng. | Highlight bark/meow/neigh | tick từng subclass |
| c31 | Trong một hệ thống quản lý nhân sự, chúng ta có lớp NhanVien. | Chuyển code panel `NhanVien` | slide |
| c32 | Lớp NhanVienIT kế thừa NhanVien thông qua từ khóa extends. | Highlight `class NhanVienIT extends NhanVien` | khoanh `extends`; click |
| c33 | Nhờ vậy, nhân viên IT có thể sử dụng thuộc tính họ tên và phương thức làm việc mà không cần viết lại. | Highlight `hoTen`, `lamViec()` bên lớp cha | marker nối |
| c34 | Kế thừa giúp tái sử dụng mã nguồn, giảm trùng lặp và dễ mở rộng hệ thống. | 3 chip: Tái sử dụng · Giảm trùng lặp · Dễ mở rộng | pop + chime |

### S06 · TÍNH CHẤT 3 — ĐA HÌNH (3:05–3:45) — ảnh 14 + code · nhấn AMBER

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c35 | Tính chất thứ ba: Đa hình — Polymorphism. | Section title; ảnh 14 | thud + shimmer |
| c36 | Đa hình có nghĩa là cùng một phương thức, nhưng có thể thể hiện những hành vi khác nhau, tùy theo đối tượng. | Highlight "RUNTIME (METHOD OVERRIDING)" | marker |
| c37 | Ví dụ, chúng ta có nhiều loại nhân viên. Khi gọi phương thức tính lương, mỗi loại sẽ có cách tính riêng. | Ảnh 14 thu nhỏ; chip "tinhLuong()" chung | nt |
| c38 | Lớp NhanVienFullTime ghi đè phương thức tinhLuong để in ra lương cố định hàng tháng. | Code panel: 3 class rút gọn | gõ code; highlight FullTime |
| c39 | Lớp NhanVienPartTime cũng ghi đè phương thức này, nhưng tính lương theo giờ. | Highlight PartTime | tick |
| c40 | Đây là ví dụ về ghi đè phương thức — Method Overriding. | Nhãn "Method Overriding" viết tay | draw_marker + chime |
| c41 | Đa hình giúp chương trình linh hoạt, dễ mở rộng và xử lý nhiều loại đối tượng thông qua cùng một cách gọi. | 3 chip: Linh hoạt · Dễ mở rộng · Một cách gọi | pop |

### S07 · TÍNH CHẤT 4 — TRỪU TƯỢNG (3:45–4:25) — ảnh 15 + code · nhấn VIOLET

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c42 | Tính chất thứ tư: Trừu tượng — Abstraction. | Section title; ảnh 15 | thud + shimmer |
| c43 | Trừu tượng là việc tập trung vào những chức năng cần thiết và ẩn đi cách thức triển khai phức tạp bên trong. | Highlight `IPaymentMethod` (khung xanh) | marker khoanh |
| c44 | Ví dụ, khi thanh toán trực tuyến, người dùng chỉ cần chọn phương thức thanh toán và thực hiện giao dịch. | 2 nhánh PayPalPayment / CreditCardPayment sáng lên | tick lần lượt |
| c45 | Họ không cần biết hệ thống xử lý kết nối ngân hàng như thế nào. | Ẩn mờ phần "triển khai bên trong" | fade |
| c46 | Trong Java, interface ThanhToan định nghĩa chức năng chung. Mỗi lớp sẽ triển khai cách thanh toán riêng. | Code panel `interface ThanhToan` + 2 `implements` | gõ code; highlight `implements` |
| c47 | Trừu tượng giảm sự phức tạp, tách biệt chức năng và cách triển khai, giúp hệ thống dễ thay đổi. | 3 chip: Giảm phức tạp · Tách triển khai · Dễ thay đổi | pop + chime |

### S08 · ỨNG DỤNG THỰC TẾ (4:25–5:00) — ảnh 16, 17, 18, 19

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c48 | Vậy lập trình hướng đối tượng được ứng dụng như thế nào trong những dự án thực tế? | Section title "ỨNG DỤNG THỰC TẾ" | whoosh |
| c49 | Thực tế, OOP được sử dụng rất rộng rãi trong quá trình phát triển phần mềm. | 4 ô lưới trống → hiện dần | fade |
| c50 | Thứ nhất, hệ thống quản lý nhà hàng. Chúng ta có thể xây dựng các lớp như MonAn, BanAn, NhanVien, HoaDon và KhachHang. | Ảnh 16 + 5 chip tên lớp | photo card + chip pop |
| c51 | Thứ hai, website thương mại điện tử, với các lớp SanPham, KhachHang, GioHang và DonHang. | Ảnh 17 + 4 chip | nt |
| c52 | Thứ ba, hệ thống quản lý bệnh viện, với các lớp BenhNhan, BacSi, LichKham và DonThuoc. | Ảnh 18 + 4 chip | nt |
| c53 | Thứ tư, ứng dụng ngân hàng, với các đối tượng TaiKhoan, GiaoDich và KhachHang. | Ảnh 19 + 3 chip | nt |
| c54 | Điều quan trọng cần nhớ là OOP không chỉ dành riêng cho Java. | 4 logo ngôn ngữ (C++, C#, Python, PHP — chữ) | logo row pop |
| c55 | Nó còn được ứng dụng trong nhiều ngôn ngữ như C++, C#, Python, PHP và nhiều công nghệ khác. | nt | chime |

### S09 · TỔNG KẾT + OUTRO (5:00–5:30) — ảnh 2 + logo

| Cue | Lời thoại | Hình / chữ | Chuyển động · SFX |
|---|---|---|---|
| c56 | Như vậy, trong bài học hôm nay, chúng ta đã tìm hiểu những kiến thức quan trọng nhất của lập trình hướng đối tượng. | Ảnh 2 photo card; kicker "TỔNG KẾT" | slide-in |
| c57 | Hãy ghi nhớ bốn tính chất. Đóng gói: bảo vệ dữ liệu. Kế thừa: tái sử dụng mã nguồn. | Highlight 2 thẻ đầu trên ảnh | tick từng thẻ |
| c58 | Đa hình: một phương thức, nhiều cách thực hiện. Trừu tượng: ẩn đi sự phức tạp, tập trung vào chức năng cần thiết. | Highlight 2 thẻ còn lại | nt |
| c59 | OOP không đơn thuần là một cách viết code, mà còn là tư duy thiết kế phần mềm. | Câu chốt lớn giữa khung | underline marker |
| c60 | Khi nắm vững những nguyên tắc này, các bạn sẽ có nền tảng tốt hơn để xây dựng những dự án lớn, chuyên nghiệp và dễ bảo trì. | nt, An `present` | fade |
| c61 | Cảm ơn các bạn đã theo dõi bài giảng của An Tech Academy. Hẹn gặp lại các bạn trong những bài học lập trình tiếp theo! | Logo AN TECH + "Hẹn gặp lại"; An `wave` | logo pop + chime kết |

Lưu ý: mốc thời gian trên là dự kiến theo ước lượng từ; timeline thật lấy từ độ dài audio từng cue (như `demo30.py`).

## 5. Code hiển thị (đúng cú pháp Java, font JetBrains Mono 22–24)

- S02: `class SinhVien { String hoTen; int tuoi; void hienThiThongTin() {...} }` + `Main` với `new SinhVien()`.
- S04: `class TaiKhoan { private double soDu; public void napTien(double tien) { if (tien > 0) soDu += tien; } public double getSoDu() { return soDu; } }`
- S05: `NhanVien` (hoTen, lamViec) + `NhanVienIT extends NhanVien` (lapTrinh).
- S06: `NhanVien.tinhLuong()` + `@Override` ở `NhanVienFullTime`, `NhanVienPartTime`.
- S07: `interface ThanhToan { void thanhToan(double soTien); }` + 2 lớp `implements`.

## 6. SFX và chuyển động

- SFX: whoosh chuyển cảnh, pop khi chip/card xuất hiện, tick khi highlight dòng code, thud khi vào tính chất mới, chime khi chốt ý/kết thúc; bus đỉnh ~0.22; không nhạc nền.
- Chuyển động: camera drift nhẹ có điểm dừng; marker vẽ tay (gạch chân/khoanh/mũi tên) đồng bộ lời đọc; không rung/lắc, không hiệu ứng thừa.
- An: `wave` (mở đầu/kết), `present`, `point_left` (chỉ ảnh), `write` (cảnh code); nhép miệng theo `_talk`; đứng bên phải, nhỏ lại ở cảnh code để không che nội dung.

## 7. Cổng B — nội dung mẫu 30–45 s (sau khi Cổng A duyệt)

1. `c01` lời chào + tiêu đề + logo (ảnh 1).
2. `c21–c24` đóng gói: ảnh 12 + code `TaiKhoan` + An + SFX (~25 s).
3. 3 sampler phát âm rời (wav): OOP (A/B/C), Java, "C++/C#" — user chọn trước khi sản xuất full.

Tiêu chí duyệt mẫu: giọng/ngắt nghỉ, cách đọc thuật ngữ, photo card + màu, code + highlight, chuyển động + SFX, nhận diện AN TECH.

## 8. Kỹ thuật triển khai (dự kiến)

- `tools/script.json` — 61 cue + scene + ảnh; `tools/demo_sample.py` — mẫu Cổng B; `tools/demo_full.py` — full.
- Xuất: `mau/sample_oop.mp4`, `mau/full/oop_full.mp4` + `_logo.mp4` (stamp logo) — không ghi đè bản đã duyệt.
- Chạy nền bằng `nohup`/background; tiến trình TTS clone ~0,3–0,6× thời lượng thật/câu trên CPU.
