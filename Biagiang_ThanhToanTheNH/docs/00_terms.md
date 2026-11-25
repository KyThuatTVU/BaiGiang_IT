# Bảng thuật ngữ — Tích hợp API thanh toán ngân hàng

Quy tắc chung: thuật ngữ tiếng Anh **hiển thị nguyên chữ** trên màn hình; lời đọc dùng tiếng Việt hoặc tiếng Anh đã kiểm. Phụ đề bám lời đọc thực tế, không hiển thị phiên âm.

| Thuật ngữ | Nhóm | Hiển thị | Lời đọc dự kiến | Cách xử lý | Trạng thái |
|---|---|---|---|---|---|
| API | Giao tiếp | API | "API" (giữ nguyên tiếng Anh) | Câu đầu có thể "Ây pi ai" nếu TTS đọc rời | Đã duyệt ở V13 (bài API) |
| Banking API | Giao tiếp | Banking API | "API ngân hàng" | Nói tiếng Việt, hiển thị tiếng Anh | Chưa kiểm — kiểm ở mẫu |
| Client ID | Xác thực | Client ID | "Client ID" | Giữ tiếng Anh | Chưa kiểm — kiểm ở mẫu |
| Client Secret | Xác thực | Client Secret | "Client Secret" | Giữ tiếng Anh | Chưa kiểm — kiểm ở mẫu |
| Access Token | Xác thực | Access Token | "Access Token" | Giữ tiếng Anh | Chưa kiểm — kiểm ở mẫu |
| OAuth 2.0 | Xác thực | OAuth 2.0 | "OAuth 2.0" | Thử take; nếu sai đọc "ô-ót hai chấm không" | Chưa kiểm — kiểm ở mẫu |
| Sandbox | Môi trường | Sandbox | "sandbox" | Giữ tiếng Anh | Chưa kiểm — kiểm ở mẫu |
| UAT | Môi trường | UAT | Không đọc | Chỉ hiển thị cạnh Sandbox | — |
| Production | Môi trường | Production | "môi trường chính thức" | Nói tiếng Việt | — |
| Payment Gateway | Thanh toán | Payment Gateway | "cổng thanh toán" | Nói tiếng Việt, hiển thị tiếng Anh | — |
| QR Payment | Thanh toán | QR Payment | "thanh toán QR" | Nói tiếng Việt | — |
| Transaction Notification | Thanh toán | Transaction Notification | "thông báo biến động số dư" | Nói tiếng Việt | — |
| Virtual Account | Thanh toán | Virtual Account | "tài khoản định danh" | Nói tiếng Việt | — |
| Transfer API | Thanh toán | Transfer API | "API chuyển tiền" | Nói tiếng Việt | — |
| Webhook | Tích hợp | Webhook | "Webhook" | Thử take; nếu sai đọc "web-húc" | Chưa kiểm — kiểm ở mẫu |
| IPN | Tích hợp | IPN | "IPN" (i-pi-en) | Thử take; nếu sai đọc "i-pi-en" | Chưa kiểm — kiểm ở mẫu |
| Return URL | Tích hợp | Return URL | "Return URL" | Thử take; nếu sai đọc "ri-tần u-a-el" | Chưa kiểm — kiểm ở mẫu |
| Payment URL | Tích hợp | paymentUrl | "payment URL" | Thử take; nếu sai đọc "đường dẫn thanh toán" | Chưa kiểm — kiểm ở mẫu |
| Endpoint | Tích hợp | Endpoint | "endpoint" | Thử take; nếu sai đọc "địa chỉ API" | Chưa kiểm — kiểm ở mẫu |
| HTTPS | Bảo mật | HTTPS | "HTTPS" | Thử take; nếu sai đọc "hát-ti-ti-pi-ét" | Chưa kiểm — kiểm ở mẫu |
| HMAC-SHA256 | Bảo mật | HMAC-SHA256 | "HMAC-SHA256" | Thử take; nếu sai đọc "chữ ký HMAC" | Chưa kiểm — kiểm ở mẫu |
| JSON | Dữ liệu | JSON | "JSON" | Thử take; nếu sai đọc "giây-sần" | Chưa kiểm — kiểm ở mẫu |
| Node.js | Runtime | Node.js | "Node.js" | Giữ tiếng Anh | Đã duyệt ở V13 |
| Express | Framework | Express | "Express" | Chỉ hiển thị; có thể không đọc | Chưa kiểm — kiểm ở mẫu |
| MySQL | Database | MySQL | "MySQL" | Giữ tiếng Anh | Đã duyệt ở V13 (người dùng nghe) |
| Database | Database | Database | "cơ sở dữ liệu" | Nói tiếng Việt | — |
| Idempotency | Nghiệp vụ | Idempotency | "tính bất biến khi lặp lại" | Nói tiếng Việt, hiển thị tiếng Anh | — |
| provider | Database | provider | "nhà cung cấp" | Nói tiếng Việt | — |
| transaction / rollback | Database | transaction, rollback | "transaction", "rollback" | Thử take; nếu sai đọc "giao dịch", "hoàn tác" | Chưa kiểm — kiểm ở mẫu |
| PENDING_PAYMENT, PAID, PROCESSING | Trạng thái | PENDING_PAYMENT, PAID, PROCESSING | Không đọc mã trạng thái | Hiển thị mã; lời đọc nói "chờ thanh toán", "đã thanh toán", "đang xử lý" | — |
| PENDING, EXPIRED, TIMEOUT, DUPLICATE | Trạng thái | PENDING, EXPIRED, TIMEOUT, DUPLICATE | Không đọc mã trạng thái | Hiển thị mã; lời đọc nói tiếng Việt | — |
| VNPAY, VietinBank, BIDV, NAPAS, VietQR | Tham chiếu | Logo/chữ trên slide | Không đọc | Chỉ xuất hiện ở slide tham khảo, không đọc tên | — |

## Kế hoạch kiểm phát âm

1. Ở mẫu 30–45 s: thu take cho các từ rủi ro (Webhook, Return URL, OAuth 2.0, Client ID/Secret).
2. Chạy ASR bằng `Kit/tools/qa_voice.py`, đối chiếu từng thuật ngữ; người dùng nghe và chốt.
3. Từ nào ASR/người nghe xác nhận sai: đổi cách viết trong `script.json` (không đổi chữ hiển thị), thu lại cue đó.
4. Chỉ đánh dấu "Đạt" sau khi nghe thực tế; các mục còn lại ghi "Chưa xác minh".
