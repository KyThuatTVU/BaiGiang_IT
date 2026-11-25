# Đề cương bài giảng — Ngôn ngữ lập trình & Framework trong Backend

## 1. Thông tin chung

| Hạng mục | Nội dung |
|---|---|
| Tên video | KHÁM PHÁ CÁC NGÔN NGỮ LẬP TRÌNH VÀ FRAMEWORK PHỔ BIẾN TRONG BACKEND DEVELOPMENT |
| Đối tượng | Sinh viên CNTT, người mới học web, frontend developer muốn hiểu backend |
| Vai trò người dẫn | Giảng viên CNTT, chuyên gia backend, đạo diễn video giáo dục |
| Thời lượng | **8:30** (510 giây) — nằm trong khung 7–9 phút |
| Định dạng | MP4 1920×1080, 16:9, 25 fps, H.264 High, AAC 48 kHz |
| Giọng đọc | Edge TTS `vi-VN-NamMinhNeural`, tốc độ **+22%** (≈1.22x), loudnorm |
| Phụ đề | Tiếng Việt gắn trong video + file SRT rời |
| Ngôn ngữ hình ảnh | Phẳng, sáng, thân thiện; bảng trắng động; thầy giáo chibi; logo công nghệ; sơ đồ client–server; code panel có highlight dòng |

## 2. Mục tiêu học tập

Sau bài giảng, người học có thể:

1. Giải thích Backend là gì và nó xử lý những việc gì trong một ứng dụng web.
2. Phân biệt chính xác **ngôn ngữ lập trình – môi trường thực thi – framework – thư viện**.
3. Kể tên và mô tả thế mạnh của bảy hệ sinh thái backend phổ biến: JavaScript/TypeScript, Python, PHP, Java, C#, Go, Ruby.
4. Chọn công nghệ theo quy mô, nghiệp vụ, hiệu năng, đội ngũ, hệ sinh thái và khả năng bảo trì — thay vì chạy theo trend.
5. Mô tả được luồng một request đăng nhập an toàn từ frontend đến database và quay về.

## 3. Cấu trúc và phân bổ thời gian

| Phần | Nội dung | Thời gian thực tế | Ghi chú so với brief |
|---|---|---|---|
| Mở đầu | Chào, hook đăng nhập, giới thiệu 4 chặng | 0:00 – 0:38 | Có lời chào “Tôi là An Tech Academy” |
| 1 | Backend là gì? Mô hình 5 lớp, luồng request | 0:38 – 1:44 | Brief ghi 0:00–0:50; kéo dài do phần minh họa + giọng Việt |
| 2 | Ngôn ngữ vs Framework vs Runtime vs Library | 1:45 – 2:29 | Brief 0:50–1:40 |
| 3 | Bảy hệ sinh thái, mỗi hệ một cảnh riêng | 2:29 – 5:44 | Brief 1:40–5:40; chia đều 25–38 giây/hệ |
| 4 | Bảng so sánh, tiêu chí chọn, 3 kịch bản | 5:44 – 6:40 | Brief 5:40–6:50 |
| 5 | Mô phỏng 8 bước đăng nhập + code Express/bcrypt/JWT | 6:40 – 7:17 | Brief 6:50–7:50; UI + code chạy song song |
| 6 | Tổng kết 5 điểm, 3 câu quiz có đếm ngược, câu kết | 7:17 – 8:30 | Brief 7:50–8:30; quiz 3×3 giây chiếm nhiều thời gian hơn |

Tổng 8:30 chốt theo độ dài WAV giọng đọc thật, nằm trong khung 7–9 phút. Thời lượng các phần được cân theo độ nặng nội dung thay vì bám cứng mốc brief.

## 4. Danh sách cảnh

| # | ID | Tên cảnh | Bắt đầu | Dài |
|---|---|---|---|---|
| 1 | intro | Backend — bộ não phía sau giao diện | 0:00.0 | 24.0s |
| 2 | goals | Bốn chặng trên lộ trình | 0:24.3 | 14.0s |
| 3 | div1 | Backend là gì? | 0:38.7 | 2.5s |
| 4 | backend | Backend làm việc gì? | 0:41.5 | 38.9s |
| 5 | flow | Một yêu cầu đi qua hệ thống | 1:20.7 | 23.9s |
| 6 | div2 | Ngôn ngữ vs Framework | 1:45.0 | 3.0s |
| 7 | langfw | Phân biệt ngôn ngữ, runtime, framework | 1:48.3 | 40.8s |
| 8 | div3 | Bảy hệ sinh thái | 2:29.5 | 2.8s |
| 9 | js | JavaScript & TypeScript | 2:32.6 | 36.0s |
| 10 | python | Python | 3:08.9 | 34.3s |
| 11 | php | PHP | 3:43.6 | 26.3s |
| 12 | java | Java | 4:10.2 | 25.0s |
| 13 | csharp | C# & .NET | 4:35.6 | 24.1s |
| 14 | go | Go (Golang) | 5:00.1 | 22.0s |
| 15 | ruby | Ruby | 5:22.4 | 22.0s |
| 16 | compare | So sánh bảy hệ sinh thái | 5:44.7 | 30.0s |
| 17 | choose | Chọn công nghệ theo bài toán | 6:15.1 | 24.9s |
| 18 | login | Backend hoạt động thật | 6:40.3 | 37.3s |
| 19 | recap | Năm điều mang về | 7:17.9 | 19.1s |
| 20 | quiz | Kiểm tra nhanh | 7:37.4 | 40.0s |
| 21 | outro | Chọn đúng công cụ | 8:17.7 | 12.0s |

## 5. Nguyên tắc nội dung

- Không đọc danh sách tên công nghệ. Mỗi hệ sinh thái trả lời bốn câu: **nó là gì → chạy bằng ngôn ngữ nào → mạnh ở đâu → dùng cho bài toán nào**.
- Phân loại chính xác từng khái niệm: Node.js là **runtime**, Express/NestJS/Fastify là **framework**, bcrypt là **thư viện**, Entity Framework Core là **ORM**.
- Không tuyên bố “framework tốt nhất”. Bảng so sánh chỉ nêu **định hướng thế mạnh**, không chấm điểm hiệu năng tuyệt đối.
- Ví dụ đăng nhập dùng bcrypt + JWT ở mức khái niệm; không có mật khẩu thật, không lưu mật khẩu dạng văn bản thuần, lỗi 401 không tiết lộ tài khoản tồn tại.
- Mọi số liệu hiệu năng minh họa (ví dụ thanh khởi động Quarkus/Micronaut) đều ghi rõ **“minh họa”**, không phải benchmark.

## 6. Hình ảnh, hiệu ứng, âm thanh

- **Bảng màu**: nền trắng ngà `#F8FAFC`, mực `#334155`, xanh `#2563EB`, cyan `#06B6D4`, tím `#8B5CF6`, hổ phách `#F59E0B`, xanh lá `#10B981`, panel code tối `#0F172A`.
- **Font**: Quicksand (tiêu đề), Be Vietnam Pro (nội dung), Plus Jakarta Sans (số liệu/nhãn), JetBrains Mono (code). Không dùng serif; kiểm tra dấu tiếng Việt ở cả bốn font.
- **Chuyển động**: phần tử vào theo nhịp cue, packet bay dọc sơ đồ, dòng code highlight theo lời giảng, thanh tiến trình quiz đếm ngược.
- **SFX**: `whoosh` chuyển cảnh, `click` ví dụ, `data` cho request/response API, `success` khi đáp án đúng, `chime` mở/đóng ý, `tick` đếm ngược, `riser` vào chương.
- **Nhạc nền**: pad Cmaj7–G–Am7–Fmaj7, arpeggio pentatonic, pulse 58 Hz; sidechain giảm 80% khi có giọng đọc; giọng luôn rõ trên nhạc và SFX.

## 7. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Giọng Nam không có trên Edge TTS | Dùng `vi-VN-NamMinhNeural` (giọng miền Bắc). Nếu cần đúng giọng Nam, phải đổi sang dịch vụ TTS khác — sẽ báo trước khi dựng. |
| Tốc độ đọc Gen Z 1.15–1.25x lấn át độ rõ | Chọn +22%, loudnorm, ngắt cue ngắn; nghe QA từng cảnh trước khi render. |
| Thời lượng vượt 9 phút | Đã chốt 8:30 từ WAV thật, vẫn trong khung 7–9 phút. |
| Sai lệch khái niệm language/runtime/framework | Bảng kiểm tra riêng trong `docs/kiem-tra-noi-dung.md`. |
| Logo thương hiệu | Dùng bộ logo vector Simple Icons (CC0) khi dựng; nếu thiếu thì vẽ emblem cách điệu, không giả mạo logo. |
| Dịch vụ TTS chập chờn | Có retry từng cue; giữ file WAV cue để chạy tiếp, không tổng hợp lại từ đầu. |
