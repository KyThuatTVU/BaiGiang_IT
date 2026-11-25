# 01 — KỊCH BẢN BA CỘT (CỔNG A · BẢN 2 — CẮT VỀ 7:40)

**Bài:** Đồng bộ dữ liệu thời gian thực — Node.js & Socket.IO
**Tổng:** 34 cảnh, 87 cue, 6.631 ký tự lời đọc → ước tính **7:40,7** video
**Giọng:** `vi-VN-NamMinhNeural` (nam, giọng Bắc) — tốc độ +18 % — **ngoại lệ có khai báo** so với §4.1 của chuẩn 2.3 (chuẩn yêu cầu nam miền Nam; toolchain hiện không có giọng Nam, đã được bạn duyệt).
**Chỉ dẫn trong ngoặc vuông là chỉ đạo diễn xuất — không đọc thành tiếng.**

## 0. Thay đổi so với bản .docx (cần duyệt)

| # | Thay đổi | Lý do |
|---|---|---|
| 1 | "cứ mỗi năm giây" → **"cứ năm giây một lần"** | Tránh TTS đọc "năm" thành year; nghĩa không đổi |
| 2 | Bỏ các dòng trích nguồn tiếng Anh và số trang (Medium, dev.to, "12", "6", "8") | Không phải lời giảng; chuyển sang phụ lục tài liệu |
| 3 | **Thêm lời thoại cho các đoạn code** (S21–S24) | Bản gốc chỉ có code, không có lời dẫn → sẽ thành khoảng lặng |
| 4 | `io.emit` → "hàm emit của io"; `localhost:3000` → "localhost, cổng ba nghìn"; `node server.js` → "node, file server chấm giây-ét" | Tránh TTS đọc ký hiệu sai |
| 5 | Thêm "Hẹn gặp lại trong bài học tiếp theo" + tagline AN TECH ACADEMY | Đủ cấu trúc outro mục 1.4 |
| 6 | Cấu trúc lại "Về ưu điểm / Về hạn chế" thành câu liền mạch | Mục 15.1: viết để nói, tránh tiêu đề rời |

> Ước tính theo hiệu suất đo thực tế 15,73 ký tự/giây (hiệu chuẩn từ bài Apriori, cùng giọng, cùng tốc độ). Con số thực sẽ chốt sau khi render voice ở Cổng B.
> Mốc thời gian trong bảng là thời gian cộng dồn **trước crossfade**; video cuối ngắn hơn 9,9 s (33 lần chuyển cảnh × 0,30 s).

## 0b. Danh sách cắt (từ bản 10:27 xuống 7:40)

| # | Cắt gì | Tiết kiệm |
|---|---|---|
| 1 | Bỏ hẳn cảnh ẩn dụ "HTTP như gọi điện, WebSocket như cuộc gọi đang giữ" | ~11 s |
| 2 | Bỏ cảnh riêng "OT và CRDT", gộp còn 1 câu cuối S18 | ~12 s |
| 3 | Rút gọn dẫn nhập, câu đệm ở S04, S05, S07, S19, S31, S33 | ~35 s |
| 4 | Ứng dụng thực tế: 4 thẻ riêng → 3 cue gộp trong 1 cảnh (S29) | ~18 s |
| 5 | Code: giữ đủ ý kỹ thuật, bỏ câu lặp và từ đệm (S21–S24) | ~30 s |
| 6 | Ưu điểm / Hạn chế: bỏ câu dẫn dài, giữ 3 ý mỗi phần | ~25 s |
| 7 | Chạy thử + demo: gộp mô tả thao tác, bỏ câu nhắc lại | ~15 s |
| 8 | Tổng kết: gộp 2 câu thành 1 câu chính + 1 câu ngắn | ~20 s |

**Không cắt:** định nghĩa, HTTP/Polling/WebSocket, 4 bước, 3 khái niệm, LWW, Optimistic Locking, toàn bộ code, cảnh báo RAM, câu "truyền nhanh ≠ nhất quán", bài tập. Toàn bộ code giữ nguyên như file gốc.

---

## PHẦN 1 — MỞ ĐẦU (0:00–0:47)

### S01 — Mở đầu thương hiệu | 0:00–0:12

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:00 (7,1s) | Xin chào các bạn! Chào mừng các bạn đến với An Tech Academy – nơi cùng nhau học công nghệ và làm chủ tương lai. **[Thân thiện, năng lượng tốt]** | Wordmark AN TECH ACADEMY trên nền sky, thầy Minh đứng bên phải vẫy tay nhẹ, gạch chân amber vẽ dần |
| c2 | 0:07 (5,7s) | Hôm nay chúng ta cùng tìm hiểu cách ứng dụng hiện đại chia sẻ dữ liệu theo thời gian thực. **[Giới thiệu, nhịp đều]** | Ba biểu tượng ứng dụng (ghi chú, chat, bảng việc) hiện so le, đường nối chạy về một điểm chung |

### S02 — Tình huống ba người dùng | 0:14–0:25

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:14 (11,1s) | Hãy tưởng tượng một nhóm sinh viên cùng làm việc trên một bảng ghi chú trực tuyến. Bạn A vừa cập nhật nội dung, nhưng bạn B vẫn thấy dữ liệu cũ, còn bạn C phải tải lại trang. **[Kể chuyện, chậm vừa]** | 3 khung trình duyệt A/B/C. A gõ "Deadline: 20h" → B vẫn "Deadline: 18h" (nhãn "dữ liệu cũ" đỏ), C có nút reload xoay. Thầy Minh chỉ lần lượt A→B→C |

### S03 — Câu hỏi và tên bài toán | 0:26–0:38

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:26 (6,2s) | Vậy làm sao để mọi người thấy dữ liệu mới ngay khi có người cập nhật, mà không cần tải lại trang? **[Tò mò, lên giọng cuối]** | 3 khung B/C mờ đi, dấu hỏi lớn giữa màn hình; nút reload bị gạch chéo |
| c2 | 0:32 (5,5s) | Đây chính là bài toán đồng bộ dữ liệu thời gian thực – Real-time Data Synchronization. **[Nhấn mạnh, chậm]** | Tiêu đề lớn hiện giữa, cụm "Real-time Data Synchronization" gạch chân amber theo nét vẽ |

### S04 — Lộ trình bài học | 0:39–0:47

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:39 (8,7s) | Bài học hôm nay gồm bốn phần: cơ chế hoạt động, truyền dữ liệu giữa Client và Server, xử lý xung đột và thực hành với Node.js, Socket.IO. **[Giới thiệu rõ, nhịp đều]** | 4 thẻ lộ trình hiện so le: Cơ chế → Truyền dữ liệu → Xung đột → Thực hành; chip Node.js và Socket.IO bật sáng cuối |

---

## PHẦN 2 — NGUYÊN LÝ HOẠT ĐỘNG (0:49–2:18)

### S05 — Định nghĩa | 0:49–0:57

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:49 (2,4s) | Đồng bộ dữ liệu thời gian thực là gì? **[Giải thích bình tĩnh]** | Tiêu đề mục; thầy Minh đứng cạnh bảng trống |
| c2 | 0:51 (6,3s) | Đây là cơ chế giúp nhiều thiết bị nhận thay đổi dữ liệu gần như ngay lập tức khi có người cập nhật. **[Định nghĩa, chắc giọng]** | Câu định nghĩa hiện thành 3 dòng, 3 từ khóa được khoanh: nhiều thiết bị / gần như ngay lập tức / có người cập nhật |

### S06 — Luồng đồng bộ | 0:58–1:09

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 0:58 (7,0s) | Khi A thay đổi ghi chú, hệ thống nhận dữ liệu, xử lý tại máy chủ và gửi cập nhật đến những người đang kết nối. **[Giải thích, nhịp đều]** | A → Server → B, C. Chấm dữ liệu chạy theo mũi tên, mỗi chặng sáng lên đúng lúc nhắc |
| c2 | 1:05 (3,3s) | Nhờ vậy, ai đang mở ứng dụng cũng thấy bản mới nhất. **[Kết ý]** | Cả 3 khung cùng hiện "Deadline: 20h", nhãn "cùng trạng thái" |

### S07 — HTTP Request – Response | 1:10–1:22

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 1:10 (4,6s) | Có hai cơ chế truyền thông phổ biến. Thứ nhất là HTTP Request – Response. **[Chuyển ý, tăng nhịp nhẹ]** | Hai cột so sánh dựng khung; cột trái "HTTP" sáng lên |
| c2 | 1:15 (6,7s) | Với HTTP, trình duyệt gửi yêu cầu, máy chủ trả kết quả. Muốn biết dữ liệu đổi chưa, phải gửi yêu cầu mới. **[Giải thích từng bước, ngắt sau mỗi bước]** | Vòng lặp request → response → request mới; mũi tên vẽ dần, nhãn "hỏi lại" xuất hiện |

### S08 — Polling | 1:23–1:28

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 1:23 (5,7s) | Ví dụ, cứ năm giây một lần, website gọi API để kiểm tra dữ liệu. Cách này gọi là Polling. **[Nhấn "Polling", hơi chậm]** | Trục thời gian 0–20s, các gói request lặp đều mỗi 5s; nhãn "Polling" đóng khung |

### S09 — WebSocket | 1:30–1:40

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 1:30 (4,0s) | Thứ hai là WebSocket – kết nối hai chiều giữa Client và Server. **[Chắc giọng, sang ý mới]** | Cột phải sáng; đường nối hai đầu với hai mũi tên ngược chiều |
| c2 | 1:34 (6,2s) | Sau khi kết nối, hai bên gửi dữ liệu cho nhau mà không cần yêu cầu HTTP mới cho từng lần cập nhật. **[Giải thích]** | Nhiều gói dữ liệu chạy liên tục hai chiều trên cùng một đường nối, không có vòng lặp mới |

### S10 — Socket.IO | 1:41–1:51

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 1:41 (6,0s) | Trong bài thực hành, chúng ta dùng Socket.IO – thư viện giao tiếp thời gian thực theo sự kiện. **[Giới thiệu]** | Thẻ Socket.IO (icon tia chớp) + nhãn "thư viện realtime"; phân loại rõ dưới chữ "library" |
| c2 | 1:47 (4,1s) | Socket.IO thường dùng WebSocket khi có thể, kèm cơ chế dự phòng. **[Nhấn "dự phòng"]** | Mũi tên chính WebSocket, nhánh phụ "fallback" nét đứt |

### S11 — Bốn bước | 1:52–2:06

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 1:52 (1,5s) | Quy trình gồm bốn bước. **[Dẫn nhập]** | 4 ô trống hiện khung |
| c2 | 1:54 (1,7s) | Client kết nối đến Server. **[Nhịp đều]** | Ô 1 sáng: client → server |
| c3 | 1:55 (3,0s) | Người dùng thực hiện thao tác cập nhật dữ liệu. **[Nhịp đều]** | Ô 2 sáng: bàn phím/chuột |
| c4 | 1:58 (2,2s) | Server tiếp nhận và xử lý dữ liệu. **[Nhịp đều]** | Ô 3 sáng: server xử lý |
| c5 | 2:01 (4,3s) | Server phát sự kiện đến các Client liên quan để cập nhật giao diện. **[Nhấn "các Client"]** | Ô 4 sáng: server → nhiều client, giao diện đổi màu |

### S12 — Server trung tâm | 2:07–2:18

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:07 (6,2s) | Server là trung tâm tiếp nhận và phân phối dữ liệu để mọi thiết bị cùng nhìn một trạng thái chung. **[Nhấn mạnh, kết ý]** | Sơ đồ hình sao: Server ở giữa, 4 client vệ tinh, đường nối hai chiều đều nhau |
| c2 | 2:13 (4,3s) | Nếu không có máy chủ, mỗi trình duyệt chỉ thấy dữ liệu riêng của nó. **[Giải thích]** | 4 client tách rời, mỗi khung hiện nội dung khác nhau, dấu ✗ giữa chúng |

---

## PHẦN 3 — BA KHÁI NIỆM QUAN TRỌNG (2:19–3:21)

### S13 — Ba khái niệm | 2:19–2:22

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:19 (3,2s) | Trước khi viết code, chúng ta cần nắm ba khái niệm. **[Dẫn nhập, tạo mong đợi]** | 3 thẻ 1-2-3 hiện so le |

### S14 — Client – Server | 2:23–2:33

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:23 (1,5s) | Một là Client – Server. **[Chắc giọng]** | Thẻ 1 phóng to |
| c2 | 2:24 (7,9s) | Client là phía người dùng, như trình duyệt trên máy tính hoặc điện thoại. Server nhận yêu cầu, xử lý và gửi kết quả trở lại. **[Giải thích, chỉ rõ hai phía]** | Trái: laptop + điện thoại; phải: server rack. Mũi tên yêu cầu đi, kết quả về |

### S15 — Event và bảng sự kiện | 2:34–2:49

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:34 (3,8s) | Hai là Event. Trong Socket.IO, ta gửi và lắng nghe sự kiện. **[Giải thích]** | Thẻ 2 phóng to, icon phát sóng |
| c2 | 2:38 (2,9s) | update-data: người dùng muốn cập nhật dữ liệu. **[Đọc tên sự kiện rõ, hơi chậm]** | Bảng 3 dòng dựng khung; dòng `update-data` hiện, mũi tên Client → Server |
| c3 | 2:41 (2,8s) | sync-state: gửi trạng thái dữ liệu hiện tại. **[Rõ, hơi chậm]** | Dòng `sync-state`, mũi tên Server → Client |
| c4 | 2:44 (2,5s) | data-updated: báo dữ liệu vừa cập nhật. **[Rõ, hơi chậm]** | Dòng `data-updated`, mũi tên Server → Client, màu teal |
| c5 | 2:46 (2,9s) | Nhờ vậy, hệ thống trao đổi dữ liệu linh hoạt. **[Nhẹ, kết ý]** | Ba dòng phát sáng nhịp nhàng, đường nối nhấp theo |

### S16 — Xung đột dữ liệu | 2:51–2:58

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:51 (7,7s) | Ba là xử lý xung đột – Conflict Resolution. Hai người cùng sửa một tài liệu gần như cùng lúc. Hệ thống chọn nội dung nào? **[Tò mò, dựng tình huống]** | Hai khung tài liệu giống nhau, hai phiên bản sửa khác nhau bay về Server cùng lúc; dấu "?" giữa |

### S17 — Last Write Wins | 2:59–3:07

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 2:59 (7,4s) | Một cách đơn giản là Last Write Wins – LWW: áp dụng bản cập nhật cuối theo thứ tự xác định, ví dụ thứ tự Server nhận. **[Giải thích, nhấn "cuối"]** | Trục thời gian: bản A đến 12:00:01, bản B đến 12:00:02 → B thắng, A mờ đi; nhãn LWW |

### S18 — Optimistic Locking | 3:08–3:21

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 3:08 (4,3s) | Cách khác là Optimistic Locking, dùng phiên bản dữ liệu để kiểm tra. **[Giải thích]** | Thẻ dữ liệu có nhãn version 3 |
| c2 | 3:12 (8,8s) | Nếu dữ liệu đã đổi từ lúc người dùng đọc, hệ thống từ chối cập nhật và yêu cầu tải lại. OT và CRDT là kỹ thuật nâng cao, sẽ học ở bài sau. **[Cảnh báo nhẹ, rõ]** | Client gửi version 3, server đã version 4 → dấu ✗, thông báo "tải lại"; hai thẻ OT/CRDT hiện mờ ở góc, gắn nhãn "bài sau" |

---

## PHẦN 4 — THỰC HÀNH CODE (3:22–5:05)

### S19 — Mục tiêu và khởi tạo | 3:22–3:42

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 3:22 (3,0s) | Bây giờ, chúng ta sẽ xây dựng ứng dụng SyncLab. **[Hào hứng, chuyển phần]** | Thẻ tiêu đề SyncLab + icon bút chì/bảng |
| c2 | 3:25 (7,1s) | Mục tiêu: khu vực ghi chú dùng chung. Khi A nhập và nhấn Gửi, trình duyệt B nhận thay đổi gần như ngay lập tức. **[Giải thích mục tiêu]** | Mockup 2 trình duyệt; A gõ → B đổi nội dung, không reload |
| c3 | 3:32 (4,7s) | Bước 1: khởi tạo dự án. Tạo thư mục synclab, mở Terminal và chạy các lệnh. **[Hướng dẫn từng bước]** | Cửa sổ Terminal, prompt `D:\synclab>` |
| c4 | 3:37 (1,5s) | npm init, gạch ngang y. **[Đọc lệnh rõ]** | Dòng `npm init -y` hiện và chạy |
| c5 | 3:39 (2,4s) | npm install express socket chấm ai-âu. **[Đọc lệnh rõ]** | Dòng `npm install express socket.io`, thanh tiến trình chạy |

### S20 — Thư viện và cấu trúc | 3:43–3:51

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 3:43 (4,6s) | Express giúp xây máy chủ Web; socket.io hỗ trợ giao tiếp thời gian thực. **[Giải thích]** | Hai thẻ: Express (icon server) và Socket.IO (icon tia chớp), mô tả ngắn |
| c2 | 3:47 (3,6s) | Cấu trúc gồm server.js và thư mục public chứa index.html. **[Rõ, chậm]** | Cây thư mục vẽ dần: synclab/ → server.js, public/ → index.html |

### S21 — Code server: khởi tạo | 3:52–4:06

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 3:52 (4,2s) | Bước 2: xây dựng Server. Tạo file server.js và viết đoạn code sau. **[Hướng dẫn]** | Code panel trượt vào, dòng 1–3 sáng |
| c2 | 3:56 (4,0s) | Khởi tạo Express và HTTP Server để Socket.IO dùng cùng máy chủ. **[Giải thích code, bình tĩnh]** | Highlight dòng 1–8 (`require`, `express()`, `createServer`, `new Server`) |
| c3 | 4:00 (5,1s) | sharedData lưu nội dung ghi chú và số phiên bản – trạng thái chung của ứng dụng. **[Nhấn "trạng thái chung"]** | Highlight khối `sharedData { content, version }`; callout "trạng thái chung" |

### S22 — Code server: kết nối và phát sự kiện | 4:07–4:30

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 4:07 (6,5s) | Khi Client kết nối, Server gửi trạng thái hiện tại bằng sync-state, để người mới thấy dữ liệu mới nhất. **[Giải thích]** | Highlight `io.on("connection")` + `socket.emit("sync-state", sharedData)`; mũi tên sang Client mới |
| c2 | 4:14 (7,2s) | Khi nhận update-data, Server kiểm tra, cập nhật nội dung và tăng phiên bản, để chặn dữ liệu sai kiểu hoặc quá dài. **[Giải thích, nhấn "kiểm tra"]** | Highlight `socket.on("update-data")`, 2 dòng `if`, `sharedData.content`, `version++` |
| c3 | 4:21 (4,7s) | Hàm emit của io phát data-updated đến tất cả Client, gồm cả người vừa gửi. **[Nhấn "tất cả"]** | Highlight `io.emit("data-updated", sharedData)`; 3 mũi tên tỏa ra 3 client |
| c4 | 4:26 (3,7s) | Đây là bước giúp mọi trình duyệt nhận cùng một trạng thái. **[Kết ý, chắc giọng]** | 3 khung client đồng loạt đổi nội dung, nhãn "cùng trạng thái" |

### S23 — Giao diện Client | 4:31–4:42

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 4:31 (3,9s) | Bước 3: xây dựng giao diện Client. Tạo file public/index.html. **[Hướng dẫn]** | Code panel HTML trượt vào |
| c2 | 4:35 (3,8s) | Giao diện gồm ô nhập, nút Gửi cập nhật và dòng số phiên bản. **[Giải thích]** | Mockup UI: textarea, nút xanh "Gửi cập nhật", "Phiên bản dữ liệu: 0" |
| c3 | 4:39 (2,8s) | Client gọi hàm io để tạo kết nối với Server. **[Giải thích]** | Highlight `const socket = io();` |

### S24 — Code client | 4:43–4:56

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 4:43 (8,3s) | Khi nhận sync-state, trình duyệt hiển thị dữ liệu hiện tại; khi nhận data-updated, giao diện tự cập nhật nội dung và số phiên bản. **[Giải thích, nhịp đều]** | Highlight 2 handler `sync-state` và `data-updated`; mũi tên từ sự kiện sang textarea và badge |
| c2 | 4:51 (4,5s) | Khi nhấn Gửi cập nhật, Client phát update-data kèm nội dung lên Server. **[Rõ, kết ý]** | Highlight `addEventListener("click")` + `socket.emit("update-data", content.value)` |

### S25 — Hoàn thành demo | 4:57–5:05

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 4:57 (4,5s) | Chúng ta đã hoàn thành ứng dụng đồng bộ dữ liệu thời gian thực cơ bản. **[Chắc giọng, chốt mốc]** | Sơ đồ 3 lớp: Client ↔ Server ↔ Client, dấu ✓ xanh, nhãn "Demo hoàn tất" |
| c2 | 5:01 (3,1s) | Hai trình duyệt giờ đây chia sẻ cùng một ghi chú. **[Kết ý]** | Hai khung A/B cùng hiện một nội dung, đường nối về Server |

---

## PHẦN 5 — CHẠY THỬ VÀ TÍCH HỢP (5:06–6:35)

### S26 — Chạy thử | 5:06–5:19

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 5:06 (5,1s) | Bây giờ, hãy kiểm tra kết quả. Tại Terminal, chạy node, file server chấm giây-ét. **[Hướng dẫn]** | Terminal hiện `node server.js`, log "SyncLab đang chạy tại http://localhost:3000" |
| c2 | 5:11 (3,6s) | Sau đó, mở trình duyệt truy cập localhost, cổng ba nghìn. **[Rõ]** | Thanh địa chỉ gõ `http://localhost:3000`, trang tải |
| c3 | 5:14 (3,2s) | Mở thêm một tab hoặc trình duyệt khác cùng địa chỉ. **[Rõ]** | Tab 2 mở cùng URL; badge "Đã kết nối máy chủ" xanh ở cả hai |

### S27 — Demo cập nhật | 5:20–5:34

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 5:20 (6,0s) | Ở trình duyệt thứ nhất, nhập: "Đây là dữ liệu cập nhật từ người dùng A", rồi nhấn Gửi cập nhật. **[Tự nhiên, như thao tác thật]** | A gõ câu, con trỏ nhấp nháy, click nút; hiệu ứng click |
| c2 | 5:26 (5,0s) | Ngay lập tức, trình duyệt thứ hai nhận nội dung mới mà không cần tải lại trang. **[Nhấn "ngay lập tức"]** | B đổi nội dung tức thì; nhãn "không reload" |
| c3 | 5:31 (2,8s) | Số phiên bản cũng tăng sau mỗi lần cập nhật. **[Chỉ dẫn quan sát]** | Badge phiên bản 0 → 1 ở cả A và B, đếm nhảy |

### S28 — Phía sau | 5:35–5:53

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 5:35 (2,0s) | Vậy điều gì đã xảy ra phía sau? **[Tò mò, chuyển ý]** | Màn hình tối lại, chỉ còn 3 nút A/B/Server |
| c2 | 5:37 (7,2s) | Client A gửi update-data lên Server. Server cập nhật dữ liệu, tăng phiên bản và phát data-updated đến mọi Client. **[Giải thích tuần tự]** | Animation 4 bước: gói update-data → server xử lý → version++ → tỏa data-updated |
| c3 | 5:44 (3,4s) | Client B nhận sự kiện và đổi nội dung trên giao diện. **[Rõ]** | B cập nhật textarea, badge nhảy |
| c4 | 5:47 (4,5s) | Đó là luồng đồng bộ thời gian thực, có thể ứng dụng vào nhiều hệ thống. **[Kết ý, mở rộng]** | Sơ đồ thu nhỏ sang góc, 4 icon hệ thống thực tế hiện mờ |

### S29 — Ứng dụng thực tế | 5:54–6:12

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 5:54 (6,3s) | Trong thực tế, cơ chế này dùng cho quản lý công việc, khi nhiều người theo dõi trạng thái nhiệm vụ. **[Gần gũi, ví dụ]** | Thẻ 1: bảng Kanban, 3 avatar cùng cập nhật |
| c2 | 6:00 (8,1s) | Website bán hàng cập nhật đơn hàng, tồn kho; quản lý lớp học cập nhật danh sách, kết quả; ứng dụng trò chuyện gửi nhận tin nhắn. **[Rõ, liệt kê có nhịp]** | 3 thẻ hiện so le: đơn hàng → "Đang giao"; bảng điểm cập nhật; khung chat có bong bóng mới |
| c3 | 6:09 (3,4s) | Trong giáo dục, học sinh cùng làm bài nhóm trực tuyến. **[Rõ, kết thúc liệt kê]** | Thẻ 4: 3 học sinh cùng sửa một tài liệu, nội dung đồng bộ |

### S30 — Giới hạn | 6:13–6:35

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 6:13 (4,3s) | Lưu ý: ví dụ này lưu dữ liệu trong RAM, khởi động lại Server sẽ mất. **[Cảnh báo, nhấn rõ]** | Callout amber "Dữ liệu trong RAM"; server restart → khối dữ liệu biến mất |
| c2 | 6:17 (3,7s) | Hệ thống thực tế cần MySQL hoặc PostgreSQL để lưu lâu dài. **[Giải thích]** | Mũi tên từ Server xuống Database (MySQL/PostgreSQL), nhãn "lưu trữ lâu dài" |
| c3 | 6:22 (5,5s) | Cần thêm xác thực người dùng, kiểm tra quyền, xử lý mất kết nối và kiểm soát xung đột. **[Liệt kê có nhịp]** | 4 icon: shield-check, lock, wifi-off, git-merge hiện lần lượt |
| c4 | 6:27 (7,8s) | Quan trọng: Socket.IO truyền nhanh nhưng không tự đảm bảo nhất quán. Điều đó phụ thuộc logic xử lý và lưu trữ phía Server. **[Nhấn mạnh, chậm]** | Tách 2 lớp: "truyền nhanh" (Socket.IO) ≠ "nhất quán" (logic Server); dấu ≠ giữa hai khối |

---

## PHẦN 6 — ƯU ĐIỂM, HẠN CHẾ, TỔNG KẾT (6:36–7:49)

### S31 — Ưu điểm | 6:36–6:54

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 6:36 (2,9s) | Đồng bộ thời gian thực mang lại nhiều lợi ích. **[Tổng kết, chắc giọng]** | Tiêu đề "Ưu điểm", 3 ô trống |
| c2 | 6:39 (4,8s) | Thứ nhất, dữ liệu cập nhật gần như tức thì, nâng cao trải nghiệm người dùng. **[Nhịp đều]** | Ô 1 sáng: icon tia chớp + "cập nhật tức thì" |
| c3 | 6:44 (5,0s) | Thứ hai, nhiều Client cùng theo dõi một trạng thái mà không cần tải lại trang. **[Rõ]** | Ô 2: nhiều client quanh 1 khối dữ liệu |
| c4 | 6:49 (4,4s) | Thứ ba, Socket.IO giúp xây ứng dụng tương tác thời gian thực dễ dàng. **[Rõ, kết ý]** | Ô 3: icon phát sóng + code `socket.on` thu nhỏ |

### S32 — Hạn chế | 6:55–7:13

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 6:55 (4,6s) | Thứ nhất, quản lý nhiều kết nối đồng thời có thể gây áp lực lên máy chủ. **[Cảnh báo vừa, không hù dọa]** | Cột "Hạn chế"; nhiều đường nối dồn vào server, thanh tải tăng |
| c2 | 7:00 (4,3s) | Thứ hai, cần cơ chế phục hồi khi mất kết nối hoặc xung đột dữ liệu. **[Rõ]** | Đường nối đứt, icon wifi-off + mũi tên phục hồi |
| c3 | 7:04 (5,1s) | Thứ ba, nhiều máy chủ cần thêm giải pháp chia sẻ trạng thái và phân phối sự kiện. **[Rõ]** | 2 server, cần adapter trung gian để chia sẻ trạng thái |
| c4 | 7:09 (3,5s) | Khi số người dùng tăng, chi phí hạ tầng cũng tăng theo. **[Kết ý]** | Biểu đồ số kết nối tăng, kèm icon máy chủ nhân bản |

### S33 — Tổng kết | 7:15–7:26

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 7:15 (7,9s) | Tóm lại, chúng ta đã hiểu đồng bộ thời gian thực, phân biệt HTTP và WebSocket, nắm Client – Server và Event trong Socket.IO. **[Tổng kết, cô đọng]** | 3 dòng tổng kết hiện so le, mỗi dòng kèm icon nhỏ |
| c2 | 7:23 (3,6s) | Đồng thời, chúng ta đã biết cách xử lý xung đột dữ liệu. **[Chắc giọng]** | Dòng thứ 4 + chip Node.js / Socket.IO |

### S34 — Bài tập và kết thúc | 7:27–7:49

| Cue | Thời gian | Lời thoại | Hình ảnh |
|---|---|---|---|
| c1 | 7:27 (8,8s) | Bài tập: phát triển SyncLab thành bảng quản lý công việc, nhiều người thêm, sửa, cập nhật trạng thái; lưu vào MySQL và kiểm soát phiên bản. **[Hướng dẫn, khuyến khích]** | Thẻ bài tập: 3 gạch đầu dòng + icon database, version |
| c2 | 7:36 (6,8s) | Hy vọng bài học giúp các bạn hiểu rõ cách xây dựng ứng dụng Web thời gian thực. Cảm ơn các bạn đã theo dõi! **[Thân thiện, ấm]** | Thầy Minh mỉm cười, gật đầu; nền chuyển sky |
| c3 | 7:43 (5,6s) | Hẹn gặp lại trong bài học tiếp theo. AN TECH ACADEMY – HỌC CÔNG NGHỆ, LÀM CHỦ TƯƠNG LAI! **[Năng lượng, chốt thương hiệu]** | Wordmark + tagline, gạch chân amber vẽ dần |

---

## Ghi chú sản xuất

- Khoảng nghỉ giữa cue: 0,22 s; đuôi cảnh: 1,10 s; crossfade 0,30 s.
- Tính toán: 421,6 s audio + 37,4 s đuôi − 9,9 s crossfade + 11,7 s gap = **460,8 s ≈ 7:40,7**.
- Phụ đề lấy từ đúng lời thoại đã đọc, tối đa 2 dòng, không hiển thị phiên âm.
- Cue đang giảng để highlight code: S21c2/c3, S22c1–c3, S23c2/c3, S24c1/c2 (khớp `tools/plan_cues.py`).
