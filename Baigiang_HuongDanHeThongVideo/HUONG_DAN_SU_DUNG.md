# 📘 Cẩm Nang Sử Dụng Hệ Thống Sản Xuất Video Tự Động (AN TECH Video Engine v1)

Hệ thống chạy **100% Offline trên Terminal**, **0% AI / 0đ API key**, tích hợp sẵn toàn bộ quy chuẩn **MASTER 2.3** (giọng clone VieNeu, nhân vật An, SFX, 8 hiệu ứng chuyển động, chuẩn `-14 LUFS`, đóng logo AN TECH ACADEMY và kiểm định QA tự động).

---

## 1. Cấu trúc hệ thống trên ổ `D:\Edit\`

```text
D:\Edit\
├── Kit\                                ← KHO DÙNG CHUNG (sửa 1 lần, mọi bài nhận ngay)
│   ├── assets\
│   │   ├── standard_2_3.json           ← Chỉnh màu sắc (theme), cỡ chữ, logo, LUFS tại đây
│   │   └── pronunciation.json          ← Thêm/sửa phát âm tiếng Anh tại đây
│   └── tools\
│       ├── build.py                    ← Lệnh Terminal chính
│       └── engine\
│           ├── parser.py               ← Đọc content.md + notes.md + img/
│           ├── pronounce.py            ← Tự đổi sub -> say chuẩn phát âm
│           └── renderer.py             ← 8 mẫu hiệu ứng animation động
└── Baigiang_<TenBai>\                  ← THƯ MỤC BÀI GIẢNG MỚI CỦA BẠN
    ├── content.md                      ← Kịch bản Markdown (ChatGPT xuất theo Prompt mẫu)
    ├── notes.md                        ← (Tùy chọn) Ghi "Không cần lời chào", "5 phút"...
    └── img\                            ← Lưu ảnh 1.jpg, 2.jpg, 3.jpg... khớp content.md
```

---

## 2. Quy trình 4 bước mỗi khi làm bài giảng mới

### Bước 1: Dùng ChatGPT soạn `content.md` và tạo ảnh
Copy **Prompt mẫu** ở Mục 5 bên dưới dán vào ChatGPT + điền chủ đề bài giảng.
- Dán **Phần 1** ChatGPT trả về vào `D:\Edit\Baigiang_<TenBai>\content.md`.
- Lưu các ảnh ở **Phần 2** đúng tên `1.jpg`, `2.jpg`... vào `D:\Edit\Baigiang_<TenBai>\img\`.

### Bước 2: Kiểm tra đầu vào bằng Terminal (`check`)
Mở PowerShell tại `D:\Edit` và gõ:
```powershell
python D:\Edit\Kit\tools\build.py check Baigiang_<TenBai>
```
- Máy báo ngay số cảnh, số câu, ảnh nào thiếu/dư, và danh sách thuật ngữ đã tự động phiên âm.
- Nếu muốn xem ảnh lưới đánh số toàn bộ thư mục `img/`, gõ:
```powershell
python D:\Edit\Kit\tools\build.py scan Baigiang_<TenBai>
```

### Bước 3: Xuất bản xem thử 30 giây (`preview`) & sửa nhanh từng cảnh
```powershell
python D:\Edit\Kit\tools\build.py preview Baigiang_<TenBai>
```
- Mở xem file `mau\preview\preview_30s_v1_logo.mp4` và ảnh kiểm tra trong `mau\preview\stills\`.
- Nếu muốn sửa riêng **Cảnh 2**, chỉnh chữ/hiệu ứng trong `content.md` rồi chạy:
```powershell
python D:\Edit\Kit\tools\build.py preview Baigiang_<TenBai> --scene s02
```
*(Giọng đọc cũ được giữ trong Cache, chỉ dựng lại hình ảnh rất nhanh).*

### Bước 4: Xuất video hoàn chỉnh (`render`)
```powershell
python D:\Edit\Kit\tools\build.py render Baigiang_<TenBai>
```
Máy tự chạy trọn gói 6 bước: **Đọc kịch bản → TTS VieNeu + Cache → Render đa nhân CPU → Mix SFX + Loudnorm `-14 LUFS` → Đóng logo → In bảng QA**.
- Thành phẩm nằm tại: `mau\full\video_v1_logo.mp4` (bản gốc không logo là `video_v1.mp4`, không bao giờ ghi đè bản cũ).

---

## 3. Danh sách 8 hiệu ứng chuyển động (`[hieu_ung: ...]`)

| Tên hiệu ứng | Khi nào dùng | Cú pháp đặc trưng trong `content.md` |
|---|---|---|
| `intro` | Cảnh mở đầu + lời chào | `- ảnh: 1.jpg \| Chú thích` + gạch đầu dòng nổi bật |
| `va_cham` | Minh họa lỗi / xung đột 2 luồng | `- trái: ...`, `- phải: ...`, `- cảnh_báo: ...` |
| `dem_so` | Số liệu đếm tăng dần + thanh tiến độ | `- 1247 \| Nhãn mô tả` |
| `so_sanh` | So sánh Cách cũ vs Cách mới | `- trước: ...`, `- sau: ...` |
| `code` | Gõ lệnh Terminal / Code từng dòng | Khối ```` ```powershell ... ``` ```` |
| `quy_trinh` | Sơ đồ 3–5 bước nối dây phát sáng | `- Tên bước \| Mô tả ngắn` |
| `anh_dong` | Trình diễn 1–3 ảnh `img/` zoom/pan mượt | `- ảnh: 1.jpg \| Chú thích ngắn` |
| `outro` | Tổng kết 3 ý + thương hiệu AN TECH | `- Ý cốt lõi \| Mô tả ngắn` |

Xem nhanh trên Terminal bất cứ lúc nào:
```powershell
python D:\Edit\Kit\tools\build.py templates
```

---

## 4. Tùy biến màu sắc (Theme) & Phát âm (không đụng code)

- **Đổi màu ngay bằng cờ `--theme`:**
  ```powershell
  python D:\Edit\Kit\tools\build.py render Baigiang_<TenBai> --theme dark_purple
  python D:\Edit\Kit\tools\build.py render Baigiang_<TenBai> --theme midnight_emerald
  ```
- **Tự chỉnh bảng màu vĩnh viễn:** Mở `D:\Edit\Kit\assets\standard_2_3.json`, sửa mã RGB trong mục `"themes"` (ví dụ `primary`, `bg_top`, `accent`). Không làm hỏng code và không ảnh hưởng video cũ.
- **Thêm từ phát âm tiếng Anh mới:** Mở `D:\Edit\Kit\assets\pronunciation.json`, thêm 1 dòng vào `"exact_phrases"`, ví dụ `"Kubernetes": "Cu bơ nét tít"`.

---

## 5. Prompt mẫu copy-paste vào ChatGPT

````text
Bạn là biên kịch bài giảng công nghệ cho kênh AN TECH ACADEMY.
Hãy soạn kịch bản video bài giảng về chủ đề: [ĐIỀN TÊN CHỦ ĐỀ VÀO ĐÂY]
Thời lượng mục tiêu: [ĐIỀN SỐ PHÚT, ví dụ: 5 phút]

YÊU CẦU ĐẦU RA GỒM 2 PHẦN:

=== PHẦN 1: NỘI DUNG FILE content.md (đúng cấu trúc để tool Python đọc tự động) ===
Quy tắc bắt buộc:
1. Dòng đầu tiên là tiêu đề chính: `# Tên bài giảng`
2. Chia thành 6–10 cảnh, mỗi cảnh bắt đầu bằng: `## Cảnh X: Tên cảnh ngắn [hieu_ung: TEN_HIEU_UNG]`
3. Phối hợp ĐA DẠNG các hiệu ứng động sau:
   - `intro`: Mở đầu, chào người xem đến với AN TECH ACADEMY.
   - `va_cham`: Minh họa xung đột/lỗi giữa 2 đối tượng (ghi `- trái: ...`, `- phải: ...`, `- cảnh_báo: ...`).
   - `dem_so`: Trình bày 3–4 số liệu ấn tượng/giả định (ghi `- SỐ | Nhãn mô tả`).
   - `so_sanh`: So sánh Cách cũ vs Cách mới (ghi `- trước: ...`, `- sau: ...`).
   - `code`: Minh họa đoạn code/lệnh 4–10 dòng trong khối ```ngon_ngu ... ```.
   - `quy_trinh`: Sơ đồ 3–4 bước nối tiếp (ghi `- Tên bước | Mô tả ngắn`).
   - `anh_dong`: Hiển thị 1–3 ảnh minh họa chuyển động (ghi `- ảnh: 1.jpg | Chú thích ngắn`).
   - `outro`: Tổng kết 3 ý cốt lõi, cảm ơn, nhắc theo dõi kênh AN TECH ACADEMY.
4. Gắn ảnh bằng dòng `- ảnh: 1.jpg | Chú thích`. Tên ảnh đánh số liên tục `1.jpg`, `2.jpg`...
5. Lời đọc thuyết minh đặt dưới mỗi cảnh, MỖI CÂU 1 DÒNG bắt đầu bằng `> ` (12–22 từ, tự nhiên).
6. Luôn có lời chào mở đầu ở Cảnh 1 và lời kết ở Cảnh cuối.

=== PHẦN 2: DANH SÁCH ẢNH CẦN TẠO ===
Liệt kê bảng các ảnh `1.jpg`, `2.jpg`... khớp 100% với Phần 1 kèm prompt tiếng Anh tạo ảnh 16:9 dark-tech nền tối, không có chữ rối, rồi hỏi tôi có muốn tạo từng ảnh ngay không.
````
