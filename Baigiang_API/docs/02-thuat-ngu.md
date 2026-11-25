# 02 — Bảng thuật ngữ & phát âm

Cách đọc dưới đây là **quy ước thống nhất trong video** (chuẩn phổ biến của lập trình viên Việt Nam), không phải phiên âm IPA. Edge TTS đọc chữ Latin theo tiếng Anh; cột "viết cho TTS" chỉ dùng khi cần ép cách đọc, **không bao giờ hiện lên phụ đề**.
Trạng thái "nghe kiểm": **Chưa** — phiên này không có khả năng nghe/phân tích audio.

| Thuật ngữ | Nhóm | Nghĩa tiếng Việt (giải thích lần đầu) | Cách đọc chọn | Viết cho TTS | Nghe kiểm |
|---|---|---|---|---|---|
| API | Giao tiếp | Giao diện lập trình ứng dụng | ây-pi-ai | API | Chưa |
| Endpoint | Giao tiếp | Địa chỉ cụ thể của API | en-đi-poi | Endpoint | Chưa |
| Route | Express | Định nghĩa đường dẫn + method trong backend | rao | Route | Chưa |
| Request | Giao tiếp | Yêu cầu gửi đến server | ri-quét | Request | Chưa |
| Response | Giao tiếp | Kết quả server trả về | ri-spon | Response | Chưa |
| HTTP | Giao thức | Giao thức truyền tải siêu văn bản | hát-tê-tê-pê | HTTP | Chưa |
| HTTPS | Giao thức | HTTP mã hóa bằng TLS | hát-tê-tê-pê-ét | HTTPS | Chưa |
| Method | Giao thức | Phương thức hành động | me-thợt | method | Chưa |
| GET / POST / PUT / PATCH / DELETE | Giao thức | Lấy / tạo / thay thế / sửa một phần / xóa | đọc tiếng Anh | GET, POST, PUT, PATCH, DELETE | Chưa |
| Header | Request | Phần thông tin bổ sung | hê-đờ | header | Chưa |
| Body | Request | Phần nội dung dữ liệu | bo-đi | body | Chưa |
| Params | Request | Tham số trong đường dẫn | pa-ram | params | Chưa |
| Query | Request | Tham số sau dấu hỏi trên URL | quơ-ri | query | Chưa |
| JSON | Dữ liệu | JavaScript Object Notation | jây-sơn | JSON | Chưa |
| Status Code | Response | Mã trạng thái HTTP | sta-tợt cốt | status code | Chưa |
| CRUD | Dữ liệu | Create, Read, Update, Delete | crớt | CRUD | Chưa |
| REST / RESTful | Kiến trúc | Phong cách thiết kế API resource-centric | rét / rét-phu | REST, RESTful | Chưa |
| Node.js | Runtime | Môi trường chạy JavaScript phía server | nốt chấm gít | Node.js | Chưa |
| Express.js | Framework | Framework web trên Node.js | ích-prét chấm gít | Express.js | Chưa |
| Fetch API | JavaScript | Hàm gửi HTTP request có sẵn | phét-chờ ây-pi-ai | Fetch API | Chưa |
| MySQL | Database | Hệ quản trị CSDL quan hệ | mai-ét-quy-en | MySQL | Chưa |
| Postman | Công cụ | Công cụ gửi request kiểm thử API | pốt-mần | Postman | Chưa |
| Thunder Client | Công cụ | Extension kiểm thử API trong VS Code | thăn-đờ clai-ần | Thunder Client | Chưa |
| CORS | Bảo mật | Cơ chế chia sẻ tài nguyên khác origin | co | CORS | Chưa |
| JWT | Bảo mật | JSON Web Token | giây-đắp-liu-ti | JWT | Chưa |
| URL | Web | Địa chỉ tài nguyên | u-er-el | URL | Chưa |
| localhost:3000 | Web | Máy cục bộ, cổng 3000 | lô-cồ-hốt ba nghìn | localhost:3000 | Chưa |
| Token | Bảo mật | Chuỗi xác thực | tốc-kần | token | Chưa |
| Client / Server | Kiến trúc | Bên gửi yêu cầu / bên phục vụ | clai-ần / sơ-vờ | client, server | Chưa |
| Frontend / Backend | Kiến trúc | Phần giao diện / phần máy chủ | phờ-ron-en / béc-en | frontend, backend | Chưa |
| Database | Dữ liệu | Cơ sở dữ liệu | đây-ta-bây | database | Chưa |
| JSON.stringify / JSON.parse | JavaScript | Đóng gói / mở chuỗi JSON | string-ghi-phai / pác | JSON.stringify, JSON.parse | Chưa |

## Nguyên tắc áp dụng

1. Lần đầu xuất hiện: nói tên gốc + giải thích tiếng Việt ngay trong câu (đã viết sẵn trong kịch bản).
2. Về sau chỉ dùng tên gốc, không dịch lại (tránh "giao diện lập trình ứng dụng" lặp 5 lần).
3. Acronym chọn **một** cách đọc, thống nhất toàn video: API = ây-pi-ai; JSON = jây-sơn; CRUD = crớt.
4. Chữ hiển thị trên màn hình luôn viết đúng chính tả gốc (API, JSON, POST...), phụ đề cũng vậy.
5. Sau khi render, cần nghe lại các cue: S03c1 (API, Application Programming Interface), S06c3 (Content-Type), S07c3 (chuỗi mã), S09c1–c2 (Node.js, Express.js, Postman), S09c3 (Fetch API). Chưa nghe kiểm trong phiên này.
