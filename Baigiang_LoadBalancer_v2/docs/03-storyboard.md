# 03 · Storyboard — Bài 12: Load Balancer

Thời gian là **dự kiến** theo tốc độ đọc 1,2 lần (≈19,5 ký tự/giây, đã tính nghỉ), sai số ±10–15%.
Mốc chính xác sẽ chốt theo file thu thật. 10 cảnh, chuyển cảnh xfade 0,4 giây.

| Cảnh | Thời gian dự kiến | Lời thoại | Mục tiêu học tập | Hình / animation (nhân vật) | Vẽ tay | Chữ trên màn hình | SFX |
|---|---|---|---|---|---|---|---|
| S01 · Mở đầu | 0:00–0:16 | S01c1–c2 | Tạo câu hỏi: traffic tăng 5.000 người thì sao? | Thẻ số liệu 5.000 / 110.000, thanh CPU–RAM–độ trễ đỏ, sơ đồ nhỏ LB → 3 server hiện ở cue 2; An chỉ tay rồi đứng giới thiệu | Gạch chân "Bộ cân bằng tải", khoanh cụm LB + server | LOAD BALANCER, Bộ cân bằng tải, CAO ĐIỂM 12/12 | pop, whoosh, pop |
| S02 · Vấn đề | 0:16–0:42 | S02c1–c3 | Hiểu vì sao một server không đủ | 3 ảnh minh họa (đám đông, server nóng, cảnh báo), card backend duy nhất với CPU 96%, RAM 92%, 8,4s, chip 502 / Thanh toán; An suy nghĩ | Khoanh đỏ 96%, gạch chân "Trang quay mãi" | Một server gánh 5.000 kết nối, BACKEND DUY NHẤT | deny, thud, marker |
| S03 · Khái niệm | 0:42–1:09 | S03c1–c3 | Định nghĩa LB và ẩn dụ trạm thu phí | Card định nghĩa 3 bước; trạm thu phí 3 làn, xe chạy, nhân viên điều phối nối xuống 3 cổng; An đứng giảng | Gạch chân "Chia đều tải", gạch chân tiêu đề | Load Balancer là gì?, TRẠM THU PHÍ — ẨN DỤ, Không xử lý nghiệp vụ | whoosh, marker, chime |
| S04 · Kiến trúc | 1:09–1:34 | S04c1–c3 | Nhớ 4 thành phần và luồng cơ bản | Client → LB (lục giác) → 3 Server → Database; gói tin chạy, tách 2 chặng ở cue 3; An đứng giảng | Gạch chân tiêu đề, khoanh LB | Mô hình cơ bản, CLIENT / LOAD BALANCER / BACKEND / DATABASE | pop, whoosh, tick |
| S05 · Luồng request | 1:34–1:58 | S05c1–c3 | Thấy request đi qua LB và trả về; hiểu scale-out | Trình duyệt → LB → server → DB, panel log #1042–1044; hai card so sánh Scale-up và Scale-out; An chỉ trái | Gạch chân "Horizontal Scaling" | Một request đi qua đâu?, REQUEST LOG, SCALE-UP / SCALE-OUT | tick ×3, pop |
| S06 · Thuật toán 1–2 | 1:58–2:23 | S06c1–c3 | Hiểu Round Robin và Weighted RR | 4 tab thuật toán, 4 card giới thiệu; demo RR gói tin 1→2→3 + chip thứ tự; demo WRR trọng số ×3/×1/×1, thanh tỉ lệ; An chỉ trái | Khoanh server đang nhận | Thuật toán chọn server, ROUND ROBIN / WEIGHTED RR, 3 : 1 : 1 | tick ×5, whoosh |
| S07 · Thuật toán 3–4 | 2:23–2:42 | S07c1–c2 | Hiểu Least Connections và IP Hash | Demo kết nối 100/30/10, gói tin chọn Server 03 + chip "CHỌN"; demo 2 người dùng → hộp băm → cùng server, ghi chú điều kiện; An đứng giảng | Khoanh Server 03, gạch chân "Cùng IP → cùng server" | LEAST CONNECTIONS, IP HASH | tick ×4, marker |
| S08 · Health Check | 2:42–3:06 | S08c1–c3 | Hiểu LB tự loại server lỗi và đưa lại nhóm | 3 server, đường probe nét đứt + chấm chạy, chip GET /health; S02 đỏ + TIMEOUT + "S02 · tạm ngắt", gói tin chuyển sang S01/S03; phục hồi khoanh xanh S02; An đứng giảng | Khoanh xanh S02 khi hồi phục | Health Check — tự loại server lỗi, TRẠNG THÁI | tick, deny, thud, success |
| S09 · Thực tế | 3:06–3:31 | S09c1–c3 | Biết công cụ thật, cấu hình mẫu và giới hạn | 4 card công cụ; panel code Nginx gõ từng dòng + card upstream 3 IP; overlay 6 giới hạn + ghi chú; An đứng giảng | Gạch chân dòng `proxy_pass` | Load Balancer trong thực tế, UPSTREAM | tick code, whoosh |
| S10 · Tổng kết | 3:31–3:57 | S10c1–c3 | Chốt 4 thuật toán + health check, mở sang bài sau | Sơ đồ tóm tắt, chip Health Check, chip bước tiếp theo, 4 card thuật toán; cue 3 phủ card CTA navy, An vẫy tay | Gạch chân tiêu đề | Tóm lại, CẢM ƠN CÁC BẠN, AN TECH ACADEMY | pop, chime, success |

## Nguyên tắc chuyển cảnh

- Chỉ dùng fade 0,4 giây; không dùng wipe/zoom mạnh.
- Mỗi cảnh giữ một tiêu đề trái, nội dung phải; nhân vật luôn ở vùng phải dưới.
- Phụ đề đặt dưới trái, không che sơ đồ và không che mặt nhân vật.

## Nhân vật

An: áo xanh, kính, tóc đen, đeo bảng tên "AN". Pose dùng trong bài: chỉ trái (giảng sơ đồ), đứng giới thiệu, suy nghĩ (S02), vẫy tay (S10).
