# 03 — STORYBOARD (34 cảnh · bản cắt 7:40)

Thời lượng là **ước tính** từ 6.631 ký tự lời thoại @15,73 ký tự/giây (calibration Apriori, NamMinh +18%); chốt chính xác sau khi render voice.
Tổng dự kiến **7:40,7** (421,6 s audio + 37,4 s đuôi cảnh − 9,9 s crossfade + 11,7 s gap).

Ký hiệu nhân vật: **Đ** = đứng giảng (tay mở), **C** = chỉ tay, **V** = cầm bút viết, **G** = giải thích hai tay, **Nhỏ** = thu nhỏ góc phải khi có code.

| # | Cảnh | Nội dung thị giác | Chuyển động | Giáo viên / SFX | Mục tiêu sư phạm | ~giây |
|---|---|---|---|---|---|---|
| 1 | S01 Mở đầu | Wordmark AN TECH ACADEMY + tagline; 3 icon ứng dụng nối về một điểm | Wordmark fade+scale 200ms; gạch chân amber vẽ 0,5s; icon hiện so le 120ms | Đ vẫy tay / chime mềm | Nhận diện thương hiệu | 13,0 |
| 2 | S02 Tình huống | 3 khung trình duyệt A/B/C; A có "Deadline 20h", B vẫn "18h" nhãn đỏ, C có nút reload | Khung hiện so le 120ms; nhãn "dữ liệu cũ" pulse 1 lần | C chỉ A→B→C / pop | Tạo vấn đề | 11,1 |
| 3 | S03 Câu hỏi | 3 khung mờ, dấu "?" lớn, nút reload bị gạch chéo; sau đó tiêu đề bài toán | "?" scale 0,9→1; tiêu đề trượt lên 12px | Đ / whoosh khi đổi ý | Đặt câu hỏi trung tâm | 11,9 |
| 4 | S04 Lộ trình | 4 thẻ: Cơ chế → Truyền dữ liệu → Xung đột → Thực hành + chip Node.js/Socket.IO | Thẻ hiện so le; chip bật sáng cuối | G / pop từng thẻ | Nêu lộ trình | 8,7 |
| 5 | S05 Định nghĩa | Câu định nghĩa 3 dòng, 3 từ khóa được khoanh | Khoanh từng từ khóa theo nét bút | V khoanh 3 vòng / pen | Hiểu khái niệm | 8,9 |
| 6 | S06 Luồng đồng bộ | A → Server → B, C; sau đó cả 3 khung cùng "20h" | Chấm dữ liệu chạy 0,9s mỗi chặng; mũi tên vẽ 0,6s | C chỉ theo chấm / tick nhẹ | Thấy dữ liệu đi đâu | 10,5 |
| 7 | S07 HTTP | Hai cột so sánh; cột HTTP: request → response → request mới | Vòng lặp vẽ dần, nhãn "hỏi lại" hiện sau | G / pop | Hiểu request–response | 11,5 |
| 8 | S08 Polling | Trục 0–20s, request lặp mỗi 5s | Gói request hiện đều; nhãn Polling đóng khung | C / tick đều | Nhận diện Polling | 5,7 |
| 9 | S09 WebSocket | Hai đầu nối, hai mũi tên ngược chiều, gói dữ liệu chạy liên tục | Đường nối vẽ 0,6s; gói chạy 2 chiều | G / whoosh nhẹ | Hiểu kết nối 2 chiều | 10,5 |
| 10 | S10 Socket.IO | Thẻ Socket.IO, nhãn "library", nhánh fallback nét đứt | Thẻ vào; nhánh nét đứt vẽ sau | C / pop | Phân loại đúng | 10,3 |
| 11 | S11 Bốn bước | 4 ô quy trình | Ô sáng lần lượt đúng cue | C theo ô / pop mỗi ô | Nắm quy trình | 13,4 |
| 12 | S12 Server trung tâm | Sơ đồ hình sao: server giữa, 4 client; sau đó 4 client tách rời có ✗ | Đường nối tỏa ra 0,4s mỗi nhánh; ✗ hiện khi c2 | G / chime chốt | Hiểu vai trò server | 10,8 |
| 13 | S13 Ba khái niệm | 3 thẻ 1-2-3 | Hiện so le 120ms | Đ / pop | Dẫn vào P3 | 3,2 |
| 14 | S14 Client–Server | Laptop + điện thoại; server rack, mũi tên yêu cầu/kết quả | Thẻ 1 phóng to; mũi tên vẽ 0,6s | C / tick | Phân biệt hai phía | 9,6 |
| 15 | S15 Event | Bảng sự kiện 3 dòng + hướng truyền | Từng dòng hiện theo cue; mũi tên đúng hướng | C chỉ bảng / click nhẹ | Hiểu event | 15,7 |
| 16 | S16 Xung đột | Hai bản sửa bay về server cùng lúc, dấu "?" | Hai thẻ hội tụ; "?" pulse 1 lần | G / whoosh | Nhận diện vấn đề | 7,7 |
| 17 | S17 LWW | Trục thời gian 12:00:01 / 12:00:02; bản B thắng | Thẻ thua mờ 40%; nhãn LWW đóng khung | C / tick | Hiểu LWW | 7,4 |
| 18 | S18 Optimistic Lock | Thẻ version 3 → server version 4 → ✗ → "tải lại"; 2 thẻ OT/CRDT mờ góc | Số version nhảy; ✗ hiện; thẻ nâng cao mờ 60% | C / buzz nhẹ | Hiểu kiểm tra version | 13,3 |
| 19 | S19 Mục tiêu + setup | Mockup 2 trình duyệt; Terminal `D:\synclab>`; lệnh npm | Cửa sổ terminal gõ lệnh (clip ngắn), thanh tiến trình | Nhỏ / key click đúng lúc | Bắt đầu thực hành | 19,5 |
| 20 | S20 Thư viện + cây | 2 thẻ Express/Socket.IO; cây thư mục | Cây vẽ dần 3 nhánh | C / pop | Hiểu cấu trúc dự án | 8,4 |
| 21 | S21 Code server 1 | Code panel `server.js` dòng 1–12; callout `sharedData` | Panel trượt vào; highlight theo cue | Nhỏ / click | Đọc phần khởi tạo | 13,7 |
| 22 | S22 Code server 2 | `io.on`, `socket.on`, `io.emit`; 3 mũi tên tỏa; caption "bản demo chưa kiểm tra version khi ghi" | Highlight chuyển dòng; mũi tên tỏa 0,4s | Nhỏ / tick | Hiểu luồng server | 22,8 |
| 23 | S23 Giao diện | Mockup UI (textarea, nút, badge); code `const socket = io()` | UI hiện; highlight dòng io() | Nhỏ / click nút | Hiểu phần UI | 11,0 |
| 24 | S24 Code client | 2 handler + nút gửi; mũi tên sự kiện → textarea/badge | Highlight theo cue | Nhỏ / click | Hiểu client | 13,0 |
| 25 | S25 Hoàn tất | 3 lớp Client ↔ Server; dấu ✓; A/B cùng nội dung | Sơ đồ vẽ 0,8s; ✓ hiện | G / chime | Chốt mốc demo | 7,8 |
| 26 | S26 Chạy thử | Terminal log "localhost:3000"; 2 tab xanh "Đã kết nối" | Terminal chạy; tab 2 mở | C / key click | Chạy được demo | 12,5 |
| 27 | S27 Demo | A gõ câu, click; B đổi ngay; badge 0→1 | Con trỏ nhấp nháy; nội dung B đổi tức thì | C chỉ A→B / click + pop | Thấy kết quả | 14,3 |
| 28 | S28 Phía sau | 4 bước animation: update-data → xử lý → version++ → tỏa data-updated | Tuần tự, mỗi bước 0,8s | C / whoosh | Hiểu cơ chế | 17,7 |
| 29 | S29 Ứng dụng | 4 thẻ: Kanban, bán hàng, lớp học, chat, bài nhóm | Thẻ hiện lần lượt, 3 thẻ ở c2 | G / pop | Liên hệ thực tế | 18,3 |
| 30 | S30 Giới hạn | Callout RAM; DB MySQL/PostgreSQL; 4 icon production; dấu ≠ | Callout vào; icon lần lượt; ≠ hiện chốt | C / alert nhẹ | Tránh hiểu sai | 21,9 |
| 31 | S31 Ưu điểm | 3 ô ✓ | Ô sáng lần lượt | G / tick | Củng cố lợi ích | 17,8 |
| 32 | S32 Hạn chế | Cột "!" 3 mục + minh họa tải server, mất kết nối, nhiều server; biểu đồ chi phí | Mục hiện so le | C / buzz nhẹ | Cân bằng đánh giá | 18,1 |
| 33 | S33 Tổng kết | 3 dòng tổng kết + dòng xung đột + chip công nghệ | Dòng hiện so le 150ms | G / pop | Củng cố | 11,7 |
| 34 | S34 Bài tập + outro | Thẻ bài tập 3 gạch đầu dòng; wordmark cuối | Thẻ vào; wordmark + gạch chân | Đ vẫy tay / chime | Kết thúc, thương hiệu | 21,7 |

## Quy tắc đồng bộ

- Mọi thành phần hình xuất hiện đúng cue trong `manifest.json`, không sớm hơn 0,15s.
- Code highlight đổi dòng khi lời giảng nhắc đúng khái niệm (không theo thời gian tuyệt đối).
- Nhân vật không che code, bảng, phụ đề: ở cảnh code, nhân vật thu nhỏ và đặt góc phải (x ≥ 1600).
- Phụ đề đáy y=1026, tối đa 2 dòng, nền mờ 60% chỉ khi chữ nằm trên vùng sáng.
- Chuyển cảnh crossfade 0,30s; không zoom, không rung, không hiệu ứng nhấp nháy.
