# Storyboard chi tiết — Xử lý trùng lặp tên file Avatar
**AN TECH ACADEMY** · Thời lượng dự kiến: ~5 phút 50 giây (10 cảnh) · Ngày lập: 2026-11-24

---

## BẢNG TỔNG QUAN PHÂN CẢNH VÀ PHÂN BỔ 16 ẢNH

| Cảnh | Tiêu đề | Thời lượng | Cues | Ảnh sử dụng trong `img/` | Hiệu ứng trực quan & SFX |
|------|---------|------------|------|-------------------------|--------------------------|
| **S01** | **Dẫn nhập: Đặt vấn đề** | ~35s | 1–6 | `1.jpg` (Cloud/Upload), `2.jpg` (User A), `3.jpg` (User B), `5.jpg` (Cảnh báo ghi đè) | Whoosh, Pop, vẽ gạch chân "1.jpg", so sánh hai avatar |
| **S02** | **Bản chất: Tên file vs Đường dẫn** | ~35s | 7–12 | `4.jpg` (Tủ đồ lockers), `6.jpg` (Two-level directory) | Phân tầng thư mục, marker chỉ đường dẫn |
| **S03** | **Thiết kế giải pháp: UUID & Thư mục** | ~35s | 13–18 | `7.jpg` (UUID 128-bit ring trên server) | Kinetic table: User -> Tên gốc -> Hash |
| **S04** | **Thiết kế MySQL: Tách biệt nơi lưu** | ~35s | 19–24 | `8.jpg` (Infographic MySQL + Uploads), `10.jpg` (Flow Web-App-DB) | Bảng dữ liệu MySQL users, highlight avatar_path |
| **S05** | **Thực hành HTML/CSS: Form & Avatar tròn** | ~35s | 25–30 | `9.jpg` (CSS cắt avatar tròn), `11.jpg` (JPG, PNG, WEBP) | Code HTML enctype, CSS border-radius 50% |
| **S06** | **Xử lý PHP: 8 bước an toàn** | ~45s | 31–38 | `16.jpg` (Lập trình viên / Code editor) | Code walkthrough 8 bước upload.php an toàn |
| **S07** | **Truy xuất đúng ảnh đại diện** | ~35s | 39–44 | `15.jpg` (Kiến trúc hệ thống full luồng) | Sơ đồ luồng: PHP query -> MySQL -> Trình duyệt GET |
| **S08** | **Trùng tên file vs Trùng nội dung (SHA-256)**| ~35s | 45–50 | *(Code vector & hash visualization)* | Code SHA-256 so sánh byte, pHash giới thiệu |
| **S09** | **Ứng dụng thực tế & Sai lầm cần tránh** | ~35s | 51–56 | `12.jpg` (E-commerce), `13.jpg` (HR/School), `14.jpg` (Mạng xã hội) | 3 photo cards thực tế + bảng cảnh báo sai lầm |
| **S10** | **Tổng kết & Lời kết** | ~35s | 57–62 | *(Logo tròn AN TECH ACADEMY)* | 3 đúc kết cốt lõi, lời chào kết AN TECH ACADEMY |

---

## CHI TIẾT TỪNG PHÂN CẢNH

### CẢNH 1: DẪN NHẬP — ĐẶT VẤN ĐỀ TRÙNG TÊN FILE (00:00 – 00:35)
- **Mục tiêu sư phạm:** Đặt vấn đề trực quan, kích thích tò mò: Hai người dùng khác nhau tải lên avatar đều tên `1.jpg`, hệ thống lưu sao để không ghi đè?
- **Hình ảnh:**
  - Giáo viên An đứng bên phải, vẫy tay chào người học.
  - Photo card trung tâm hiển thị `1.jpg` (Cloud/Upload), sau đó tách đôi: bên trái `2.jpg` (User A - ảnh cô gái), bên phải `3.jpg` (User B - ảnh chú mèo).
  - Xuất hiện popup cảnh báo `5.jpg` ("already exists. Replace?").
- **Hand-drawn:** Nét bút vẽ tay gạch chân từ khóa `1.jpg`, mũi tên đỏ trỏ vào nguy cơ ghi đè.
- **SFX:** Whoosh mở đầu, Pop xuất hiện card, Marker gạch chân.
- **Lời thoại (Cues 1–6):**
  1. Xin chào các bạn! Chào mừng đến với AN TECH ACADEMY, nền tảng kiến thức công nghệ thực chiến.
  2. Hãy tưởng tượng chúng ta đang xây dựng một ứng dụng quản lý người dùng.
  3. Người dùng A tải lên ảnh đại diện tên 1.jpg là ảnh chân dung của mình.
  4. Cùng lúc đó, người dùng B cũng tải lên một ảnh tên 1.jpg, nhưng lại là ảnh một chú mèo dễ thương.
  5. Nếu hệ thống chỉ lưu theo tên file vào một thư mục chung, chuyện gì sẽ xảy ra?
  6. Đúng vậy, ảnh của người dùng A sẽ bị ảnh của người dùng B ghi đè hoàn toàn!

---

### CẢNH 2: BẢN CHẤT — TÊN FILE KHÔNG PHẢI ĐỊNH DANH DUY NHẤT (00:35 – 01:10)
- **Mục tiêu sư phạm:** Giúp người học hiểu bản chất lưu trữ: Tên file chỉ có ý nghĩa khi đi kèm Đường dẫn (Path).
- **Hình ảnh:**
  - Photo card `4.jpg` (Tủ đồ lockers) làm ẩn dụ cho các ngăn thư mục.
  - Sơ đồ `6.jpg` (Two-level directory: mỗi user có thư mục riêng).
  - Hai khung code đường dẫn: `Website/UserA/1.jpg` và `Website/UserB/1.jpg`.
- **Hand-drawn:** Khoanh tròn phần khác biệt giữa hai đường dẫn (`UserA` vs `UserB`).
- **SFX:** Whoosh chuyển cảnh, Pop xuất hiện sơ đồ.
- **Lời thoại (Cues 7–12):**
  7. Tên 1.jpg thực chất chỉ là một cái tên, không phải mã định danh duy nhất của dữ liệu.
  8. Bạn có thể hình dung thư mục như một ngăn tủ, tên file như món đồ bên trong, còn đường dẫn chính là địa chỉ ngăn tủ.
  9. Hai file hoàn toàn có thể trùng tên nếu chúng nằm ở hai thư mục khác nhau trên ổ đĩa.
  10. Ví dụ: Website gạch chéo User A gạch chéo 1.jpg hoàn toàn khác với User B gạch chéo 1.jpg.
  11. Vấn đề không nằm ở việc người dùng đặt tên file giống nhau.
  12. Vấn đề là chương trình của chúng ta đã dùng chung một vị trí lưu trữ cho hai file khác nhau.

---

### CẢNH 3: THIẾT KẾ GIẢI PHÁP — UUID VÀ THƯ MỤC RIÊNG (01:10 – 01:45)
- **Mục tiêu sư phạm:** Đưa ra 2 giải pháp kỹ thuật chuẩn: Đổi tên bằng UUID ngẫu nhiên và phân thư mục theo user_id.
- **Hình ảnh:**
  - Photo card `7.jpg` (Vòng tròn UUID 128-bit trên server rack).
  - Bảng ánh xạ: User A -> 1.jpg -> `a83f91c2.jpg`.
  - Cấu trúc thư mục tối ưu: `uploads/user_101/a83f91c2.jpg`.
- **Hand-drawn:** Mũi tên biến đổi từ `1.jpg` sang chuỗi Hex ngẫu nhiên.
- **SFX:** Whoosh, Marker viết công thức `bin2hex(random_bytes(16))`.
- **Lời thoại (Cues 13–18):**
  13. Để giải quyết triệt để, chúng ta có hai giải pháp kỹ thuật tiêu chuẩn.
  14. Thứ nhất: Tạo thư mục riêng cho từng người dùng dựa trên mã định danh user_id.
  15. Thứ hai: Không dùng tên gốc của người dùng để lưu trữ, mà tự sinh tên file mới bằng chuỗi ngẫu nhiên UUID.
  16. Trong PHP, chúng ta có thể kết hợp hàm random_bytes và bin2hex để tạo chuỗi 32 ký tự độc nhất.
  17. Cách tiếp cận hoàn hảo nhất là kết hợp cả hai: thư mục theo user_id, bên trong là tên file ngẫu nhiên.
  18. Cấu trúc này vừa triệt tiêu hoàn toàn xung đột tên, vừa giúp máy chủ phân vùng dữ liệu cực kỳ ngăn nắp.

---

### CẢNH 4: THIẾT KẾ MYSQL — TÁCH BIỆT NƠI LƯU FILE VÀ METADATA (01:45 – 02:20)
- **Mục tiêu sư phạm:** Phân biệt rõ ràng giữa File Storage (lưu file nhị phân) và MySQL (lưu đường dẫn).
- **Hình ảnh:**
  - Photo card `8.jpg` (Infographic dữ liệu và file tách rời) và `10.jpg` (Web Server - App Server - DB flow).
  - Bảng MySQL `users`: cột `id`, `username`, `avatar_path`.
- **Hand-drawn:** Mũi tên từ cột `avatar_path` trỏ sang thư mục file thực tế.
- **SFX:** Pop xuất hiện bảng dữ liệu.
- **Lời thoại (Cues 19–24):**
  19. Nhiều bạn mới lập trình thường băn khoăn: Có nên lưu luôn file ảnh vào cơ sở dữ liệu MySQL không?
  20. Câu trả lời chuẩn mực là không! Chúng ta tách biệt hoàn toàn giữa nơi lưu trữ file và nơi lưu thông tin.
  21. File ảnh thực tế được lưu trên ổ đĩa máy chủ trong thư mục uploads.
  22. Còn MySQL chỉ lưu trữ siêu dữ liệu và đường dẫn tương đối tới file đó trong cột avatar_path.
  23. Với thiết kế này, cơ sở dữ liệu luôn nhẹ nhàng, sao lưu nhanh chóng và truy vấn cực kỳ mượt mà.
  24. PHP sẽ dùng user_id để truy vấn lấy avatar_path, sau đó cấp đường dẫn này cho trình duyệt hiển thị.

---

### CẢNH 5: THỰC HÀNH HTML & CSS — FORM UPLOAD VÀ AVATAR TRÒN (02:20 – 02:55)
- **Mục tiêu sư phạm:** Nắm vững thuộc tính HTML Form upload và kỹ thuật CSS avatar chuẩn không méo tỷ lệ.
- **Hình ảnh:**
  - Khung code HTML `index.php`: `enctype="multipart/form-data"`.
  - Photo card `9.jpg` (Ảnh gốc biến thành avatar tròn) và `11.jpg` (So sánh JPG, PNG, WEBP).
  - Code CSS: `border-radius: 50%`, `object-fit: cover`.
- **Hand-drawn:** Khung chữ nhật khoanh tròn thành hình tròn để mô phỏng `border-radius: 50%`.
- **SFX:** Whoosh, Marker gạch chân `enctype="multipart/form-data"`.
- **Lời thoại (Cues 25–30):**
  25. Bước vào phần thực hành, trước hết là biểu mẫu HTML trong file index.php.
  26. Hãy luôn ghi nhớ thuộc tính bắt buộc: enctype bằng multipart gạch chéo form-data, nếu thiếu, file sẽ không thể tải lên!
  27. Về phía CSS, để tạo khung ảnh đại diện hình tròn hoàn hảo, chúng ta dùng border-radius 50 phần trăm.
  28. Và đặc biệt là thuộc tính object-fit bằng cover.
  29. Cover giúp hình ảnh lấp đầy khung tròn tự nhiên mà không bao giờ bị méo mó tỷ lệ, bất kể ảnh gốc vuông hay chữ nhật.
  30. Chúng ta cũng giới hạn thuộc tính accept cho các định dạng ảnh phổ biến như JPG, PNG và WEBP.

---

### CẢNH 6: XỬ LÝ PHP — 8 BƯỚC UPLOAD AN TOÀN (02:55 – 03:40)
- **Mục tiêu sư phạm:** Trình bày rõ ràng 8 bước xử lý upload trong `upload.php`, nhấn mạnh các điểm phòng chống tấn công.
- **Hình ảnh:**
  - Photo card `16.jpg` (Lập trình viên / code editor).
  - Khung code PHP cuộn qua 8 bước trọng yếu:
    1. Check Session; 2. Check `$_FILES['error']`; 3. Giới hạn 5MB; 4. Check MIME thực tế (`finfo`); 5. Sinh tên mới; 6. Tạo thư mục `mkdir`; 7. `move_uploaded_file`; 8. MySQL Prepared Statement.
- **Hand-drawn:** Đánh dấu tick xanh cho từng bước an toàn.
- **SFX:** Pop nhẹ mỗi khi một bước được duyệt qua.
- **Lời thoại (Cues 31–38):**
  31. Trái tim của hệ thống nằm ở file upload.php với quy trình tám bước bảo mật nghiêm ngặt.
  32. Bước một: Luôn lấy user_id từ phiên đăng nhập session phía máy chủ, tuyệt đối không tin ID gửi từ trình duyệt!
  33. Bước hai và ba: Kiểm tra mã lỗi upload và giới hạn dung lượng file tối đa năm mê-ga-bai.
  34. Bước bốn: Dùng thư viện finfo để đọc MIME type thực tế từ nội dung byte, ngăn chặn kẻ xấu đổi đuôi file mã độc thành chấm jpg.
  35. Bước năm: Tạo tên file mới bằng hàm bin2hex kết hợp random_bytes.
  36. Bước sáu: Kiểm tra và tự động tạo thư mục riêng theo user_id với quyền không cho thực thi mã kịch bản.
  37. Bước bảy: Dùng move_uploaded_file chuyển file từ thư mục tạm vào vị trí chính thức.
  38. Và bước tám: Dùng Prepared Statement cập nhật đường dẫn avatar_path vào MySQL, triệt tiêu nguy cơ SQL Injection.

---

### CẢNH 7: TRUY XUẤT ĐÚNG ẢNH ĐẠI DIỆN (03:40 – 04:15)
- **Mục tiêu sư phạm:** Hiểu rõ luồng dữ liệu hai chiều: PHP truy vấn MySQL -> Trình duyệt gửi HTTP GET tải ảnh.
- **Hình ảnh:**
  - Photo card `15.jpg` (Kiến trúc toàn luồng Browser -> Backend -> MySQL -> Uploads).
  - Mô phỏng hai user: User A (id=1) nhận `uploads/user_1/a83f91c2.jpg`; User B (id=2) nhận `uploads/user_2/d71b42e9.jpg`.
- **Hand-drawn:** Mũi tên 2 chiều giữa Trình duyệt và Server.
- **SFX:** Whoosh, Chime khi hiển thị đúng hai ảnh đại diện khác nhau.
- **Lời thoại (Cues 39–44):**
  39. Khi cả hai người dùng đã lưu ảnh thành công, làm thế nào hệ thống hiển thị đúng ảnh cho từng người?
  40. Hãy phân biệt rõ hai công đoạn riêng biệt này.
  41. Đầu tiên, khi User A đăng nhập với ID bằng một, PHP gửi truy vấn SELECT avatar_path FROM users WHERE id bằng một.
  42. MySQL trả về chuỗi đường dẫn tương đối của User A.
  43. Sau đó, trình duyệt nhận đường dẫn và gửi yêu cầu HTTP để tải đúng bức ảnh từ thư mục máy chủ về hiển thị.
  44. MySQL không tự tìm file; nó chỉ lưu chỉ mục, còn việc phân phát ảnh là nhiệm vụ của web server.

---

### CẢNH 8: PHÂN BIỆT TRÙNG TÊN VÀ TRÙNG NỘI DUNG (SHA-256) (04:15 – 04:50)
- **Mục tiêu sư phạm:** Phân biệt bài toán trùng tên (Filename collision) và trùng nội dung nhị phân (Deduplication qua SHA-256).
- **Hình ảnh:**
  - So sánh 2 file khác tên: `1.jpg` vs `avatar.png` nhưng có cùng SHA-256 hash.
  - Khung code PHP: `hash_file('sha256', $file)`.
  - Khái niệm mở rộng: Perceptual Hashing (pHash) cho ảnh tương đồng thị giác.
- **Hand-drawn:** Khung băm hash 64 ký tự hex.
- **SFX:** Pop, Marker gạch chân SHA-256.
- **Lời thoại (Cues 45–50):**
  45. Một điểm thú vị mở rộng: Trùng tên file hoàn toàn khác với việc trùng nội dung file!
  46. Hai file cùng tên 1.jpg có thể mang dữ liệu hoàn toàn khác nhau.
  47. Ngược lại, hai file khác tên vẫn có thể chứa cùng những byte dữ liệu giống hệt nhau.
  48. Để phát hiện hai file có trùng nội dung byte hay không, chúng ta sử dụng thuật toán băm SHA-256 qua hàm hash_file.
  49. Nếu giá trị băm giống hệt nhau, nội dung nhị phân của chúng chắc chắn trùng khớp.
  50. Còn nếu muốn nhận diện hai ảnh chụp cùng một góc nhìn đã qua chỉnh sửa, các bạn hãy tìm hiểu thêm về Perceptual Hashing nhé!

---

### CẢNH 9: ỨNG DỤNG THỰC TẾ VÀ SAI LẦM CẦN TRÁNH (04:50 – 05:25)
- **Mục tiêu sư phạm:** Kết nối kiến thức vào dự án thực chiến: Mạng xã hội, HR, E-commerce, và các bẫy thường gặp.
- **Hình ảnh:**
  - 3 photo cards thực tế: `12.jpg` (E-commerce catalog sản phẩm), `13.jpg` (Quản lý hồ sơ nhân viên), `14.jpg` (Mạng xã hội thành viên).
  - Bảng tổng kết sai lầm: 1. Tin tưởng đuôi JPG; 2. Không giới hạn size; 3. Không dọn dẹp ảnh cũ; 4. Nghĩ tên ngẫu nhiên là bảo mật.
- **Hand-drawn:** Dấu gạch chéo đỏ cho các sai lầm nguy hiểm.
- **SFX:** Whoosh lướt qua 3 cards thực tế, Pop cảnh báo sai lầm.
- **Lời thoại (Cues 51–56):**
  51. Mô hình xử lý này chính là xương sống của mọi hệ thống lớn mà bạn tiếp xúc hàng ngày.
  52. Từ mạng xã hội hiển thị hàng triệu avatar, hệ thống nhân sự quản lý hồ sơ, cho đến sàn thương mại điện tử với hàng vạn ảnh sản phẩm.
  53. Trong các dự án quy mô lớn, các bạn có thể chuyển thư mục cục bộ sang các dịch vụ lưu trữ đám mây như Amazon S3 hay Cloudinary.
  54. Tuy nhiên, nguyên tắc cốt lõi về định danh chủ sở hữu và lưu đường dẫn trong cơ sở dữ liệu vẫn không bao giờ thay đổi.
  55. Hãy luôn ghi nhớ: Đừng bao giờ chỉ dựa vào đuôi file, hãy dọn dẹp ảnh cũ khi người dùng cập nhật ảnh mới.
  56. Và tên file ngẫu nhiên không thể thay thế cho cơ chế kiểm tra phân quyền truy cập!

---

### CẢNH 10: TỔNG KẾT VÀ LỜI KẾT (05:25 – 05:55)
- **Mục tiêu sư phạm:** Đúc kết 3 nguyên tắc vàng và chào kết AN TECH ACADEMY.
- **Hình ảnh:**
  - Giáo viên An đứng giữa, biểu cảm vui vẻ, chỉ tay vào 3 đúc kết.
  - 3 chip đúc kết:
    1. Tránh ghi đè: Thư mục riêng + Tên UUID.
    2. Định danh chủ sở hữu: Liên kết bằng user_id.
    3. Truy xuất an toàn: MySQL lưu avatar_path + Prepared Statements.
  - Outro: Logo AN TECH ACADEMY, khẩu hiệu "Cùng bạn chinh phục công nghệ!".
- **Hand-drawn:** Nét bút vẽ khung bao quanh 3 đúc kết.
- **SFX:** Pop nhẹ mỗi chip, Chime kết bài giảng.
- **Lời thoại (Cues 57–62):**
  57. Để tổng kết bài học hôm nay, các bạn chỉ cần ghi nhớ trọn vẹn ba điều:
  58. Thứ nhất: Tránh ghi đè bằng cách kết hợp thư mục người dùng với tên file UUID ngẫu nhiên.
  59. Thứ hai: Luôn xác định chủ sở hữu dữ liệu dựa trên phiên đăng nhập user_id.
  60. Và thứ ba: Lưu đường dẫn ảnh trong MySQL để truy xuất an toàn, chính xác.
  61. Hy vọng bài học này đã giúp các bạn hiểu sâu về cách quản lý tệp tin và dữ liệu trong phần mềm thực chiến.
  62. Cảm ơn các bạn đã đồng hành cùng AN TECH ACADEMY. Hãy đăng ký kênh và hẹn gặp lại các bạn trong những bài học lập trình tiếp theo!
