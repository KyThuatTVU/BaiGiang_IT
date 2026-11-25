# Bảng thuật ngữ — Lập trình hướng đối tượng (OOP) với Java

Quy tắc chung theo MASTER 2.3 & AGENTS.md:
- Thuật ngữ tiếng Anh **hiển thị nguyên chữ** trên màn hình; lời đọc dùng tiếng Việt hoặc tiếng Anh đã kiểm.
- Phụ đề bám lời đọc thực tế, không hiển thị phiên âm.
- Tên biến, phương thức trong code (`hoTen`, `napTien`, `soDu`...): lời đọc dịch nghĩa tự nhiên, màn hình giữ nguyên code.

| Thuật ngữ | Nhóm | Hiển thị màn hình | Lời đọc dự kiến | Phương án kiểm / Fallback | Trạng thái |
|---|---|---|---|---|---|
| OOP | Viết tắt cốt lõi | OOP | A: "Ô Ốp" · B: "Ô-Ô-Pê" · C: "Object-Oriented Programming" | Thu 3 sampler A/B/C ở Cổng B, người dùng nghe & chốt | Chưa xác minh (chờ duyệt mẫu) |
| Java | Ngôn ngữ | Java | "Da-va" / "Gia-va" | Giữ tiếng Anh chuẩn, không đọc bẻ giọng | Chưa xác minh (chờ duyệt mẫu) |
| Class | Khái niệm | Class | "Lớp" hoặc "Class" | Đọc kết hợp "Class — lớp" để người mới nắm rõ | Chưa xác minh (chờ duyệt mẫu) |
| Object | Khái niệm | Object | "Đối tượng" hoặc "Object" | Đọc kết hợp "Object — đối tượng" | Chưa xác minh (chờ duyệt mẫu) |
| Encapsulation | Tính chất 1 | Encapsulation | "Encapsulation" | Đọc sau "Đóng gói" | Chưa xác minh (chờ duyệt mẫu) |
| Inheritance | Tính chất 2 | Inheritance | "Inheritance" | Đọc sau "Kế thừa" | Chưa xác minh (chờ duyệt mẫu) |
| Polymorphism | Tính chất 3 | Polymorphism | "Polymorphism" | Đọc sau "Đa hình" | Chưa xác minh (chờ duyệt mẫu) |
| Abstraction | Tính chất 4 | Abstraction | "Abstraction" | Đọc sau "Trừu tượng" | Chưa xác minh (chờ duyệt mẫu) |
| private | Từ khóa Java | private | "pờ-rai-vơ-t" / giữ tiếng Anh | Đọc chậm, nhấn mạnh bảo vệ dữ liệu | Chưa xác minh (chờ duyệt mẫu) |
| extends | Từ khóa Java | extends | "extends" | Giữ tiếng Anh trong ngữ cảnh code | Chưa xác minh (chờ duyệt mẫu) |
| implements | Từ khóa Java | implements | "implements" | Giữ tiếng Anh trong ngữ cảnh code | Chưa xác minh (chờ duyệt mẫu) |
| interface | Từ khóa Java | interface | "interface" | Giữ tiếng Anh | Chưa xác minh (chờ duyệt mẫu) |
| Method Overriding | Kỹ thuật OOP | Method Overriding | "Method Overriding" | Đọc tiếng Anh kèm giải thích "ghi đè phương thức" | Chưa xác minh (chờ duyệt mẫu) |
| @Override | Ký hiệu Annotation | @Override | "ghi đè" hoặc "Override" | Tuyệt đối không đọc ký tự a còng (@) | Tuân thủ quy chuẩn MASTER |
| C++ / C# | Ngôn ngữ khác | C++, C# | "C plus plus", "C thăng" | Hiển thị "C++, C#" trên màn hình | Chưa xác minh (chờ duyệt mẫu) |
| Python / PHP | Ngôn ngữ khác | Python, PHP | "Pai-thon", "P-H-P" | Giữ cách đọc chuẩn | Chưa xác minh |

## Kế hoạch kiểm phát âm tại Cổng B
1. Thu take phát âm thực tế bằng TTS clone (`tts_vieneu.py`).
2. Xuất các file sampler âm thanh độc lập cho các thuật ngữ trọng yếu:
   - `oop_opt_a.wav` (Ô Ốp)
   - `oop_opt_b.wav` (Ô-Ô-Pê)
   - `oop_opt_c.wav` (Object-Oriented Programming)
   - `term_java.wav` (Java)
   - `term_cpp_cs.wav` (C++, C#)
3. Cổng B video mẫu tích hợp đoạn đọc thực tế của "OOP", "Java", "Encapsulation", "private" để người dùng nghe và đánh giá trong toàn cảnh.
4. Chỉ chuyển trạng thái thành "Đạt" sau khi người dùng duyệt thực tế.
