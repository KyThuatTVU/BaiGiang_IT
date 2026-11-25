# 00 — Hồ sơ phân tích bài giảng API

**Dự án:** AN TECH ACADEMY — "API là gì và nó chạy như thế nào"
**Nguồn:** `Baigiang_API/NoidungAPI.docx` (15 phần, bài đầy đủ)
**Đối tượng:** sinh viên CNTT, người mới học lập trình web
**Thời lượng mục tiêu:** 4:50–5:10 (11 cảnh)
**Khung:** 16:9 Full HD 1920×1080 · 30 fps
**Định dạng đầu ra:** MP4 H.264 + AAC, phụ đề SRT kèm theo

---

## 1. Mục tiêu học tập

Sau video, người học:

1. Phát biểu được API là gì và ví von "bồi bàn" đúng bản chất (API ≠ toàn bộ backend).
2. Phân biệt API – Endpoint – Route – Request – Response.
3. Đọc được một HTTP request/response đơn giản (method, URL, headers, body, status code).
4. Nêu được 4 method CRUD và các mã trạng thái hay gặp (200/201/400/401/404/500).
5. Hiểu JSON là định dạng trao đổi và cách `JSON.stringify` / `JSON.parse`.
6. Hình dung được luồng Express + Fetch từ một ví dụ tối giản.

## 2. Kiến thức trọng tâm (giữ)

- API là **giao diện giao tiếp**, không phải bộ não xử lý.
- Mapping nhà hàng: khách = Client, bồi bàn = API, phiếu = Request, bếp = Backend, món = Response, quầy = Endpoint, kho = Database.
- Endpoint = địa chỉ; HTTP method = hành động.
- Request 4 phần; Response 3 phần (status, headers, body).
- JSON + status code là "ngôn ngữ chung".
- Frontend không cần biết backend lưu dữ liệu ở đâu.

## 3. Phần lược bỏ để vừa 5 phút

Toàn bộ Phần 9 (CRUD code đầy đủ), Phần 11 (MySQL chi tiết, CREATE TABLE, mysql2), Phần 12.2–12.5 (JWT, phân quyền, CORS code), Phần 15 (bài tập). Chỉ nhắc tên ở phần tổng kết để gợi bài sau.

## 4. Kiểm kê 16 ảnh người dùng cung cấp

| # | File | Nội dung | Dùng ở cảnh | Đánh giá theo Clean Visual System 2.3 |
|---|---|---|---|---|
| 1 | `waiter_order.png` | Bồi bàn ghi order tại bàn (ảnh thật, ánh sáng ấm) | S01, S04 | **Đạt** — ảnh thật đúng ngữ cảnh, dùng làm neo ví dụ |
| 2 | `chef_cook.png` | Đầu bếp nấu trong bếp (ảnh thật) | S04 | **Đạt** — ảnh thật, rõ "nhà bếp" |
| 3 | `kitchen_rush.png` | Bếp đông, nhiều khay món | S04 (nền phụ) | **Đạt có điều kiện** — hơi rối, chỉ dùng crop nhỏ |
| 4 | `fe_be_db.png` | Sơ đồ Frontend – API – Server – Database | S02 | **Cần sửa nhẹ** — đúng ý nhưng có logo "thunkable"; sẽ crop bỏ footer |
| 5 | `handdrawn_cycle.png` | Vòng Diner → Waiter → Kitchen → Food | S04 (nền minh họa) | **Đạt** — nét tay hợp motif marker; chữ tiếng Anh sẽ che bằng nhãn tiếng Việt |
| 6 | `order_flow_flat.png` | Infographic phẳng 4 bước gọi món | S04 (thay thế/zoombie) | **Đạt** — vector phẳng, đúng phong cách |
| 7 | `waiter_chef_flat.png` | Vector bồi bàn + bếp, màn hình "NEW ORDER" | S06 (request đi vào bếp) | **Đạt** — vector sạch, có yếu tố "phiếu → bếp" |
| 8 | `postman_get.png` | Postman gửi GET, xem JSON | S09 | **Đạt** — ảnh giao diện thật, cần crop bỏ viền |
| 9 | `thunder_client.png` | Thunder Client trong VS Code | S09 | **Đạt** — UI thật |
| 10 | `rest_cards.png` | 5 endpoint GET/POST/PUT/DELETE kèm JSON | S05/S07 (chỉ crop 1–2 thẻ) | **Cần sửa** — chữ tiếng Anh do AI tạo; chỉ dùng như "bối cảnh", không đọc chi tiết |
| 11 | `fetch_code.png` | Đoạn fetch() + nhãn REST/HTTP/JSON | S09 | **Cần sửa** — code AI có chữ nhỏ; thay bằng code tự dựng, ảnh chỉ làm nền mờ |
| 12 | `client_server_yellow.png` | APP A (Client) ⇄ APP B (Server) | S02 | **Đạt** — tối giản, đúng chiều request/response; sẽ Việt hóa nhãn |
| 13 | `api_neon.png` | APP – API – BACKEND neon | S03 (nền thoáng) | **Tiết chế** — neon trái quy chuẩn; dùng rất nhỏ hoặc bỏ |
| 14 | `neon_restaurant.png` | Nhà hàng API retro neon | (dự phòng) | **Loại khỏi bản chính** — neon/glow mạnh, sai art direction |
| 15 | `http_deep_dive.png` | HTTP/1.1 neon + status code | (dự phòng) | **Loại khỏi bản chính** — cùng lý do; status code sẽ tự dựng |
| 16 | `cartoon_cycle.png` | Customer–Waiter–Chef hoạt hình trẻ con | (dự phòng) | **Loại** — lệch tông người lớn, trùng nội dung ảnh 5 |

**Quyết định:** dùng 12 ảnh (1–12), trong đó ảnh 4/10/11 chỉ dùng một phần; loại 13–16 khỏi bản chính (nếu bạn muốn giữ, nói rõ — tôi sẽ chèn tiết chế). Các thành phần cần chính xác (URL, JSON, status code, code Express) **tự dựng bằng vector/chữ thật**, không để AI vẽ chữ.

## 5. Ví dụ thực tế dùng xuyên suốt

- Ứng dụng đặt món ăn (hook) → nhà hàng (analogy) → website bán laptop (endpoint, product ID).
- Một luồng duy nhất: `GET /api/products` → JSON danh sách sản phẩm.

## 6. Cấu trúc 11 cảnh

| Cảnh | Nội dung | Thời lượng dự kiến |
|---|---|---|
| S01 | Intro + hook đặt món | 0:00–0:16 |
| S02 | Vấn đề Frontend ↔ Backend | 0:16–0:44 |
| S03 | API là gì + ổ cắm điện | 0:44–1:18 |
| S04 | Nhà hàng: API = bồi bàn | 1:18–1:56 |
| S05 | Endpoint & cấu trúc URL | 1:56–2:26 |
| S06 | Request: 4 thành phần | 2:26–2:56 |
| S07 | HTTP method + status code | 2:56–3:30 |
| S08 | Response & JSON | 3:30–3:56 |
| S09 | Thực chiến Express + Fetch | 3:56–4:30 |
| S10 | Lỗi hay gặp + tổng kết | 4:30–4:58 |
| S11 | Outro thương hiệu | 4:58–5:06 |
