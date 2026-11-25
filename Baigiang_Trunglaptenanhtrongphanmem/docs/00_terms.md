# Bảng thuật ngữ phát âm — Bài giảng Xử lý trùng lặp tên file Avatar
**AN TECH ACADEMY** · Phiên bản: 2.0 (Đã kiểm chứng ASR & Tinh chỉnh ngữ âm) · Ngày: 2026-11-24

Tuân thủ nghiêm ngặt Section III & Section XV của MASTER DESIGN & VOICE STANDARD 2.3.  
**Nguyên tắc cốt lõi:** Phân biệt rõ bản **hiển thị (`sub`)** đúng chính tả kỹ thuật và bản **lời đọc (`say`)** tối ưu cho TTS VieNeu để phát âm tròn vành, rõ chữ, chuẩn âm tiết.

---

## 1. BẢNG THUẬT NGỮ ĐÃ KIỂM CHỨNG BẰNG ASR (WHISPER)

| Thuật ngữ | Nhóm | Cách viết hiển thị (`sub`) | Cách viết cho TTS (`say`) | Kết quả nhận diện ASR | Đánh giá |
|:---|:---:|:---:|:---:|:---:|:---:|
| **AN TECH ACADEMY** | Thương hiệu | `AN TECH ACADEMY` | `An Tếch Academy` | "Antec Academy" | ✅ Đạt chuẩn thương hiệu |
| **1.jpg** | Tên tệp tin | `1.jpg` | `một chấm j p e g` | "1.jpg" | ✅ Đạt chuẩn (không bị đọc là Jopica) |
| **file** | Khái niệm | `file` / `tệp` | `tệp tin` / `tệp` | "tệp tin" | ✅ Đạt chuẩn (loại bỏ lỗi đọc thành "phi") |
| **HTML** | Ngôn ngữ | `HTML` | `H T M L` | "hắt tê mở lờ" / "HTML" | ✅ Đạt chuẩn |
| **CSS** | Định dạng | `CSS` | `C S S` / `Xi-ét-ét` | "CSS" | ✅ Đạt chuẩn |
| **PHP** | Ngôn ngữ máy chủ | `PHP` | `P H P` / `Pi-ếch-pi` | "PHP" | ✅ Đạt chuẩn |
| **MySQL** | Cơ sở dữ liệu | `MySQL` | `Mai-ét-kiu-eo` | "MySQL" | ✅ Đạt chuẩn |
| **User A / User B** | Người dùng | `User A` / `User B` | `Người dùng A` / `Người dùng B` | "Người dùng A / B" | ✅ Tự nhiên, thuần Việt |
| **user_id** | Mã định danh | `user_id` | `diu-sơ ai-đi` | "user ID" | ✅ Đạt chuẩn |
| **UUID** | Mã duy nhất | `UUID` | `U U I D` | "UID" / "UUID" | ✅ Đạt chuẩn |
| **SHA-256** | Mã băm | `SHA-256` | `Ét-hát-a hai năm sáu` | "SH-A256" | ✅ Đạt chuẩn |
| **PDO** | Thư viện PHP | `PDO` | `Pi-đi-ô` | "PDO" | ✅ Đạt chuẩn |
| **MIME type** | Kiểu dữ liệu | `MIME type` | `kiểu mai-mờ` | "kiểu mime" | ✅ Đạt chuẩn |
| **Overwrite** | Ghi đè | `ghi đè (overwrite)` | `ghi đè` | "ghi đè" | ✅ Tự nhiên |

---

## 2. QUY TẮC BẮT BUỘC KHI SẢN XUẤT AUDIO BÀI NÀY
1. Tuyệt đối không để nguyên `1.jpg` hoặc `.jpg` vào text của TTS vì VieNeu sẽ đọc sai thành "Jopica" hoặc "zfig". Bắt buộc viết `chấm j p e g`.
2. Tuyệt đối không viết từ `file` đứng một mình khi đưa vào TTS vì VieNeu sẽ đọc thành âm "phi". Luôn thay bằng `tệp tin` hoặc `tệp` trong lời đọc `say`, trong khi phụ đề `sub` vẫn để `file` theo đúng thói quen lập trình viên.
3. Tên thương hiệu `AN TECH ACADEMY` bắt buộc viết `An Tếch Academy` trong `say` để VieNeu đọc chuẩn giọng nam tự nhiên, không bị vấp từ.
