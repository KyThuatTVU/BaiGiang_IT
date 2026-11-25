# Storyboard — Tích hợp API thanh toán ngân hàng vào website thương mại điện tử

**Bài:** `Biagiang_ThanhToanTheNH` (thư mục hiện có; tên gốc người dùng đặt thiếu chữ "g")  
**Nguồn:** `content.md` 12 phần · **Yêu cầu:** `notes.md` — khoảng 7 phút  
**Định dạng:** 1920×1080, 30 fps, H.264 CRF 18, audio AAC 192 kbps, −14 LUFS, TP ≤ −1 dBTP  
**Giọng:** clone cục bộ VieNeu (`Kit/cache/ref_voice/ref_final.wav`), một giọng nam xuyên suốt  
**Hình:** nền tối tech, vector phẳng, icon Lucide line, nhân vật An, nét bút tay, SFX tổng hợp; **không nhạc nền** (theo mẫu V13 đã duyệt)  
**Thời lượng dự kiến:** 6:55–7:05 sau khi đo TTS thực tế (script hiện ước 6:59,8 ở 4 từ/giây)

## Nguyên tắc sản xuất

- Mỗi cảnh một ý; hình ảnh giải thích luồng, không lặp slide chữ.
- Thuật ngữ hiển thị tiếng Anh; lời đọc tiếng Việt hoặc tiếng Anh đã kiểm (xem `docs/00_terms.md`).
- Mã trạng thái (`PENDING_PAYMENT`, `PAID`, `TIMEOUT`…) hiển thị trên sơ đồ, không đọc mã.
- Ảnh trong `img/` chỉ dùng tham khảo nội dung; sơ đồ, QR, bảng, code đều dựng lại bằng vector/code để đúng kỹ thuật (MASTER 12.4–12.5).
- An xuất hiện toàn bộ cảnh, góc phải dưới, nhỏ lại ở cảnh code; không che nội dung.
- Nét bút tay chỉ dùng để khoanh từ khóa, vẽ mũi tên luồng, gạch chân — đồng bộ tiếng bút.
- Không khẳng định ngân hàng cụ thể nào hỗ trợ API nào nếu chưa kiểm tài liệu; ví dụ đều ghi "ví dụ minh họa".

## Timeline tổng

| Cảnh | Nội dung | Bắt đầu | Ước lượng |
|---|---|---|---|
| S01 | Hook + lời chào | 0:00 | 28 s |
| S02 | API ngân hàng là gì | 0:28 | 40 s |
| S03 | Điều kiện cấp API và bộ thông tin | 1:08 | 38 s |
| S04 | Năm nhóm API ngân hàng | 1:46 | 42 s |
| S05 | Năm thành phần hệ thống | 2:28 | 21 s |
| S06 | Luồng thanh toán tám bước | 2:49 | 51 s |
| S07 | Return URL và Webhook | 3:40 | 30 s |
| S08 | Xác thực OAuth và bảo mật khóa | 4:10 | 34 s |
| S09 | Database orders và payments | 4:44 | 28 s |
| S10 | Ba bước code Node.js | 5:12 | 44 s |
| S11 | Trạng thái, trùng lặp, đối soát | 5:56 | 37 s |
| S12 | Tổng kết + lời kết | 6:32 | 28 s |

---

## S01 — Hook + lời chào (0:00–0:28)

**Mục tiêu:** tạo tò mò về đơn hàng "đã chuyển khoản nhưng vẫn chờ thanh toán"; nhận diện AN TECH ACADEMY.

**Hình ảnh:** thẻ đơn hàng checkout bên trái (Điện thoại thông minh · SP001 · 15.000.000 ₫ · trạng thái "Chờ thanh toán"); bên phải là điện thoại ngân hàng với chip "Biến động số dư +15.000.000 ₫"; nhân viên nhỏ với đồng hồ; An đứng present bên phải. Header thương hiệu xuất hiện.

**Chuyển động:** thẻ đơn trượt lên; chip tiền vào pop; nét bút khoanh "Chờ thanh toán"; dấu hỏi mờ dần; camera zoom nhẹ.

**Chữ trên màn hình:** `AN TECH ACADEMY` · `TÍCH HỢP THANH TOÁN · NGÂN HÀNG` · `Thanh toán tự động` · `Chờ thanh toán`.

**Lời đọc:**
1. Xin chào các bạn! Chào mừng đến với An Tech Academy.
2. Hôm nay, chúng ta sẽ nối website bán hàng với ngân hàng.
3. Khách đã chuyển khoản, mà đơn hàng vẫn báo chờ thanh toán?
4. Nhân viên phải mở ứng dụng ngân hàng, dò từng giao dịch mỗi ngày?
5. Đó là lúc API thanh toán ngân hàng phát huy tác dụng.
6. Chúng ta sẽ đi từ khái niệm, đến luồng xử lý và code Node.js.
7. Kèm theo webhook, bảo mật và cách chống xử lý trùng.

**SFX:** whoosh mở; pop thẻ đơn; tick khi khoanh; thud nhẹ khi chip tiền vào; không SFX dày.

---

## S02 — API ngân hàng là gì (0:28–1:08)

**Mục tiêu:** hiểu API ngân hàng là giao diện lập trình; thấy khác biệt thủ công và tự động.

**Hình ảnh:** hai cột "Chưa tích hợp" và "Đã tích hợp". Cột trái: nhân viên → app ngân hàng → đối chiếu → website, có đồng hồ và dấu Ba chấm. Cột phải: Frontend → Backend → Bank API → Webhook về Backend → Database; dòng tiền 15.000.000 ₫. An chỉ sang cột phải.

**Chuyển động:** hai cột hiện lần lượt; mũi tên vẽ tay; packet chạy một chiều; dấu ✓ xuất hiện ở cột tự động.

**Chữ trên màn hình:** `API NGÂN HÀNG` · `Giao diện lập trình ứng dụng` · `Thủ công` / `Tự động` · `15.000.000 ₫` · `PENDING → PAID`.

**Lời đọc:**
1. API ngân hàng là giao diện lập trình do ngân hàng cung cấp.
2. Nó cho phép phần mềm bên ngoài gọi dịch vụ ngân hàng qua Internet.
3. Ví dụ, khách đặt mua một chiếc điện thoại giá mười lăm triệu đồng.
4. Chưa tích hợp, nhân viên phải kiểm tra biến động số dư, rồi đối chiếu nội dung chuyển khoản.
5. Sau đó quay lại website xác nhận, kho mới bắt đầu giao hàng.
6. Đã tích hợp, website tự tạo giao dịch, ngân hàng xử lý và thông báo về máy chủ.
7. Backend xác minh, rồi tự cập nhật đơn đã thanh toán.
8. Giá trị lớn nhất là tự động hóa và đồng bộ dữ liệu.
9. Mỗi ngày hàng trăm đơn, nhân viên không thể dò thủ công.

**SFX:** whoosh chuyển cột; tick khi đối chiếu; chime nhẹ khi PAID; marker khi gạch chân "tự động".

---

## S03 — Điều kiện cấp API và bộ thông tin (1:08–1:46)

**Mục tiêu:** sửa hiểu nhầm "mở tài khoản là có API"; biết quy trình đăng ký và bộ thông tin xác thực; biết bí mật chỉ nằm ở Backend.

**Hình ảnh:** pipeline 5 bước: Tài khoản doanh nghiệp → Đăng ký dịch vụ → Hợp đồng & xác minh → Sandbox/UAT → Production. Dưới là thẻ "BỘ THÔNG TIN TÍCH HỢP": `CLIENT ID merchant_abc_001`, `CLIENT SECRET ••••`, `SIGNING KEY merchant-private-key.pem`, `MERCHANT ID`; huy hiệu khóa "CHỈ BACKEND"; thẻ trình duyệt bị gạch đỏ.

**Chuyển động:** pipeline vẽ từng bước; thẻ thông tin trượt lên; dấu đỏ X trên JavaScript trình duyệt; An viết gạch chân "CHỈ BACKEND".

**Chữ trên màn hình:** `ĐIỀU KIỆN CẤP API` · `Sandbox / UAT` · `Production` · `Client ID · Client Secret · Signing Key · Merchant ID` · `KHÔNG đặt trong JavaScript`.

**Lời đọc:**
1. Nhưng mở tài khoản doanh nghiệp chưa đủ để có API thanh toán.
2. Doanh nghiệp phải đăng ký dịch vụ, ký hợp đồng và hoàn tất xác minh.
3. Ngân hàng cấp môi trường thử nghiệm sandbox để lập trình viên kiểm thử.
4. Kiểm thử đạt, mới được phê duyệt sang môi trường chính thức.
5. Bộ thông tin thường gồm Client ID, Client Secret, khóa ký và chứng thư số.
6. Tùy ngân hàng, có thể thêm API Key, Access Token hoặc Merchant ID.
7. Điểm quan trọng: không nhúng bí mật vào JavaScript chạy trên trình duyệt.
8. Chỉ Backend được giữ và sử dụng thông tin xác thực.
9. Mỗi ngân hàng có tài liệu và quy trình riêng.

**SFX:** tick theo 5 bước; pop thẻ; deny nhẹ khi gạch đỏ; marker.

---

## S04 — Năm nhóm API ngân hàng (1:46–2:28)

**Mục tiêu:** phân biệt 5 nhóm API; hiểu QR chỉ để thu tiền, không tự xác nhận.

**Hình ảnh:** 5 ô icon: `Payment Gateway` (credit-card), `QR Payment` (scan), `Transaction Notification` (message-circle), `Virtual Account` (wallet), `Transfer API` (banknote). Mỗi ô có mô tả 1 dòng. Thẻ cảnh báo bên dưới: "QR ≠ đã thanh toán" + mũi tên sang "Thông báo giao dịch / Đối soát". An đứng present.

**Chuyển động:** 5 ô hiện lần lượt theo lời; ô đang nói sáng lên; thẻ cảnh báo rung nhẹ 1 lần; dấu ≠ vẽ tay.

**Chữ trên màn hình:** `5 NHÓM API` · tên 5 nhóm · `QR ≠ xác nhận thanh toán` · `Cần Notification hoặc Đối soát`.

**Lời đọc:**
1. Có năm nhóm API ngân hàng thường gặp.
2. Nhóm một: cổng thanh toán, tạo giao dịch và chuyển khách sang trang thanh toán.
3. Nhóm hai: thanh toán QR, sinh mã gắn với số tiền và mã đơn hàng.
4. Nhóm ba: thông báo biến động số dư, gửi giao dịch về hệ thống doanh nghiệp.
5. Nhóm bốn: tài khoản định danh, giúp nhận diện tiền chuyển vào của từng đơn.
6. Nhóm năm: API chuyển tiền, cho phép chi hộ theo quyền được cấp.
7. Lưu ý rất quan trọng: chỉ tạo được mã QR không có nghĩa là đã biết khách thanh toán.
8. Muốn tự xác nhận, phải có thông báo giao dịch hoặc chức năng đối soát.
9. Chọn đúng nhóm API theo nhu cầu, đừng chỉ nhìn vào tên gọi.

**SFX:** pop từng ô; tick khi ô sáng; deny nhẹ ở "QR ≠"; whoosh sang thẻ cảnh báo.

---

## S05 — Năm thành phần hệ thống (2:28–2:49)

**Mục tiêu:** thấy Backend là trung tâm, chỉ Backend gọi ngân hàng.

**Hình ảnh:** hàng 5 khối: Customer (user) → Frontend (monitor) → Backend (server) → Bank API (building-2) → Database (database). Đường Frontend–Backend hai chiều; Backend–Bank hai chiều; Backend–Database hai chiều; Customer chỉ nối Frontend.

**Chuyển động:** các khối pop theo thứ tự; connector vẽ dần; nhãn "chỉ Backend" xuất hiện trên đường Backend–Bank; An chỉ tay vào Backend.

**Chữ trên màn hình:** `5 THÀNH PHẦN` · `Customer · Frontend · Backend · Bank API · Database` · `Backend = trung tâm`.

**Lời đọc:**
1. Hãy chia hệ thống thành năm thành phần.
2. Customer là người mua hàng.
3. Frontend là giao diện website.
4. Backend xử lý nghiệp vụ đơn hàng.
5. Bank API nối tới ngân hàng hoặc nhà cung cấp thanh toán.
6. Database lưu đơn hàng và giao dịch.
7. Backend là trung tâm, và là thành phần duy nhất gọi ngân hàng.

**SFX:** pop từng khối; whoosh theo connector; chime nhẹ khi hoàn tất sơ đồ.

---

## S06 — Luồng thanh toán tám bước (2:49–3:40)

**Mục tiêu:** nắm toàn bộ luồng; nhớ Backend tự tính tiền; nhớ bước xác minh trước khi cập nhật.

**Hình ảnh:** 8 bước xếp 2 hàng 4 cột, mỗi bước một chip số + icon. Bước 2 phóng to: `total = product.price × quantity` với nguồn `Database`, dấu X trên "tin giá từ client". Bước 6: mũi tên từ Bank vào Backend nhãn `Webhook / IPN`. Bước 7: khiên "verify signature". Bước 8: `payment_status = PAID`, `order_status = PROCESSING`.

**Chuyển động:** từng bước sáng theo lời; packet chạy theo mũi tên; bước 2 có highlight amber; bước 7 nhấp khiên; bước 8 chime + đổi trạng thái.

**Chữ trên màn hình:** `LUỒNG 8 BƯỚC` · `Backend tự tính tiền` · `PENDING_PAYMENT` · `Webhook / IPN` · `Verify` · `PAID → PROCESSING`.

**Lời đọc:**
1. Khi khách nhấn nút Thanh toán, luồng xử lý bắt đầu.
2. Bước một: Frontend gửi danh sách sản phẩm, số lượng và phương thức thanh toán.
3. Bước hai: Backend tự tính tiền từ dữ liệu trong Database.
4. Không tin số tiền do Frontend gửi lên, vì client có thể sửa.
5. Đơn hàng được lưu ở trạng thái chờ thanh toán.
6. Bước ba: Backend gửi mã đơn, số tiền và nội dung sang ngân hàng.
7. Bước bốn: ngân hàng trả về URL thanh toán hoặc dữ liệu QR.
8. Bước năm: khách quét mã và xác thực trong ứng dụng ngân hàng.
9. Bước sáu: ngân hàng gọi Webhook hoặc IPN về máy chủ doanh nghiệp.
10. Bước bảy: Backend kiểm tra chữ ký, mã giao dịch, số tiền và trạng thái.
11. Bước tám: hợp lệ thì cập nhật đã thanh toán và chuyển đơn sang xử lý.
12. Nếu bước bảy thất bại, tuyệt đối không cập nhật đơn hàng.

**SFX:** tick từng bước; thud ở bước 2; whoosh request/response; chime bước 8; deny nếu bước 7 thất bại (nhánh minh họa).

---

## S07 — Return URL và Webhook (3:40–4:10)

**Mục tiêu:** phân biệt kênh trình duyệt và kênh máy chủ; không xác nhận đơn từ Return URL.

**Hình ảnh:** hai làn. Làn trên: Customer Browser → Return URL (amber, nhãn "chỉ hiển thị"). Làn dưới: Bank Server → Webhook/IPN → Backend (violet, nhãn "bằng chứng giao dịch"). Thẻ đỏ: "Không xác nhận từ Return URL" với dấu X.

**Chuyển động:** làn trên vẽ trước, làn dưới vẽ sau; packet chạy; dấu X đỏ trên thẻ; An chỉ vào làn dưới.

**Chữ trên màn hình:** `RETURN URL` · `chỉ hiển thị` · `WEBHOOK / IPN` · `server → server` · `không phải bằng chứng`.

**Lời đọc:**
1. Cần phân biệt hai khái niệm rất dễ nhầm: Return URL và Webhook.
2. Return URL chỉ đưa trình duyệt của khách quay về website.
3. Nó phục vụ hiển thị kết quả, không phải bằng chứng thanh toán.
4. Webhook hay IPN là kênh máy chủ ngân hàng gọi thẳng máy chủ doanh nghiệp.
5. Không xác nhận đơn chỉ vì khách đã quay về trang thành công.
6. Kẻ giả mạo hoàn toàn có thể tự mở địa chỉ đó.
7. Hãy xác minh dữ liệu từ ngân hàng trước khi cập nhật.

**SFX:** whoosh làn trên; thud làn dưới; deny khi dấu X; marker gạch chân "server → server".

---

## S08 — Xác thực OAuth và bảo mật khóa (4:10–4:44)

**Mục tiêu:** hiểu luồng Client Credentials; biết nơi lưu bí mật.

**Hình ảnh:** sequence: Backend → Token Server (`Client ID + Client Secret`) → Access Token → Payment API (`Authorization: Bearer …`). Thẻ `.env` với `BANK_CLIENT_ID`, `BANK_CLIENT_SECRET`, `BANK_WEBHOOK_SECRET`. Thẻ trình duyệt bị gạch đỏ. Ba huy hiệu: HTTPS, xoay vòng khóa, không ghi log.

**Chuyển động:** mũi tên tuần tự; token rơi vào header; thẻ env fade; dấu X đỏ; An viết gạch chân "Backend".

**Chữ trên màn hình:** `OAUTH 2.0 · CLIENT CREDENTIALS` · `Client ID + Client Secret` · `Access Token` · `Authorization: Bearer` · `.env` · `HTTPS · Rotate keys · No logs`.

**Lời đọc:**
1. Nhiều ngân hàng dùng OAuth 2.0 để cấp quyền truy cập.
2. Backend gửi Client ID và Client Secret đến máy chủ xác thực.
3. Hợp lệ thì nhận về Access Token.
4. Token được gắn vào header khi gọi API thanh toán.
5. Khi hết hạn, Backend lấy token mới theo quy định.
6. Bí mật phải nằm trong biến môi trường của Backend.
7. Không đưa Client Secret, Private Key hay API Key vào mã trình duyệt.
8. Trong môi trường thật, cần HTTPS, xoay vòng khóa và giới hạn quyền.
9. Không ghi thông tin bí mật vào log hay mã nguồn công khai.

**SFX:** whoosh từng mũi tên; shimmer khi token xuất hiện; deny thẻ trình duyệt; marker.

---

## S09 — Database orders và payments (4:44–5:12)

**Mục tiêu:** hiểu vì sao tách hai bảng; nhớ khóa UNIQUE chống trùng.

**Hình ảnh:** hai thẻ schema. `orders`: id, order_code, total_amount, payment_status, order_status. `payments`: id, order_id, provider, provider_transaction_id, amount, status, paid_at. Liên kết 1:N. Bảng nhỏ 3 lần thử: FAILED → FAILED → SUCCESS. Huy hiệu `UNIQUE(provider, provider_transaction_id)`.

**Chuyển động:** hai thẻ trượt vào; đường 1:N vẽ; 3 dòng lần thử hiện; huy hiệu UNIQUE được khoanh.

**Chữ trên màn hình:** `ORDERS` · `PAYMENTS` · `1 đơn → N lần thử` · `UNIQUE(provider, provider_transaction_id)`.

**Lời đọc:**
1. Trước khi viết API, hãy thiết kế cơ sở dữ liệu.
2. Bảng orders quản lý đơn hàng và trạng thái thanh toán.
3. Bảng payments lưu từng lần thử thanh toán.
4. Một đơn có thể thất bại, thử lại rồi mới thành công.
5. Tách hai bảng giúp giữ đầy đủ lịch sử giao dịch.
6. Thêm ràng buộc duy nhất trên nhà cung cấp và mã giao dịch.
7. Đây là chốt chặn chống xử lý trùng ở tầng dữ liệu.

**SFX:** pop hai thẻ; thud khi liên kết; tick 3 lần thử; chime khi UNIQUE.

---

## S10 — Ba bước code Node.js (5:12–5:56)

**Mục tiêu:** thấy code tối thiểu của tạo đơn, tạo payment, nhận webhook; nhớ transaction.

**Hình ảnh:** ba thẻ code (JetBrains Mono, syntax màu), mỗi thẻ một bước, gõ dần:
1. `POST /api/orders` — lấy `product.price` từ DB, `totalAmount = price * quantity`, lưu `PENDING`.
2. `POST /api/payments` — `getBankAccessToken()`, payload `orderId`, `amount`, `returnUrl`, `notifyUrl`, gọi `POST /payments`.
3. `POST /webhooks/bank` — `verifySignature(rawBody)`, `SELECT ... FOR UPDATE`, kiểm tra amount/status, `UPDATE payments`, `UPDATE orders`, `commit`.
An nhỏ hơn (scale 0.55) bên phải, không che code.

**Chuyển động:** code gõ theo cursor; highlight dòng đang nói; nhãn bước pop; transaction box vẽ quanh thẻ 3; dấu ✓/✗ ở verify.

**Chữ trên màn hình:** `BƯỚC 1 · TẠO ĐƠN` · `BƯỚC 2 · TẠO PAYMENT` · `BƯỚC 3 · WEBHOOK` · `VERIFY → TRANSACTION → UPDATE`.

**Lời đọc:**
1. Bước một: API tạo đơn hàng.
2. Backend lấy giá từ Database, tính tổng rồi lưu đơn.
3. Bước hai: tạo giao dịch thanh toán.
4. Backend lấy token, gửi mã đơn, số tiền, URL nhận kết quả.
5. Ngân hàng trả về payment URL để chuyển khách sang thanh toán.
6. Bước ba: nhận Webhook tại endpoint riêng.
7. Phải xác minh chữ ký trước khi đọc dữ liệu.
8. Mở transaction, khóa đơn hàng bằng FOR UPDATE.
9. Kiểm tra số tiền, trạng thái, rồi cập nhật bảng thanh toán và bảng đơn hàng.
10. Sai bất kỳ bước nào, rollback toàn bộ để giữ dữ liệu nhất quán.
11. Code trong bài là mô hình minh họa, không phải SDK của ngân hàng.

**SFX:** click gõ phím theo từng dòng; tick khi highlight; thud khi mở transaction; chime khi commit; deny nhánh lỗi.

---

## S11 — Trạng thái, trùng lặp, đối soát (5:56–6:32)

**Mục tiêu:** nhớ các trạng thái thực tế; hiểu timeout ≠ thất bại; hiểu idempotency; biết đối soát.

**Hình ảnh:** state machine `PENDING → PAID → PROCESSING → SHIPPING → COMPLETED`; nhánh `FAILED`, `EXPIRED`; thẻ amber `TIMEOUT ≠ FAILED`; thẻ `DUPLICATE → idempotency`; bảng đối soát 4 dòng DH001–DH004 (Khớp / Cần kiểm tra).

**Chuyển động:** trạng thái sáng theo lời; nhánh thất bại màu đỏ; timeout nhấp amber; bảng đối soát hiện từng dòng; dấu ✓/! theo kết quả.

**Chữ trên màn hình:** `PENDING · PAID · PROCESSING · SHIPPING · COMPLETED` · `FAILED · EXPIRED` · `TIMEOUT ≠ FAILED` · `DUPLICATE → idempotent` · `ĐỐI SOÁT`.

**Lời đọc:**
1. Thực tế không chỉ có thành công và thất bại.
2. Còn chờ thanh toán, hết hạn, quá thời gian chờ và giao dịch gửi lặp.
3. Timeout không có nghĩa là thất bại, vì ngân hàng có thể đã xử lý.
4. Gửi lặp phải nhận diện bằng mã giao dịch duy nhất.
5. Xử lý lặp lại vẫn chỉ tạo một kết quả. Đó là tính bất biến khi lặp lại.
6. Webhook cần HTTPS, chữ ký, thời gian gửi và giới hạn IP.
7. Cuối ngày, đối soát để tìm chênh lệch giữa website và ngân hàng.
8. Webhook có thể thất lạc, nên cần truy vấn trạng thái dự phòng.

**SFX:** tick theo trạng thái; deny nhánh FAILED; thud nhẹ timeout; tick bảng đối soát; chime kết thúc.

---

## S12 — Tổng kết + lời kết (6:32–7:00)

**Mục tiêu:** chốt 3 điều quan trọng; nhắc thương hiệu và bài sau.

**Hình ảnh:** 3 thẻ đánh số: `1. Tính tiền ở Backend` · `2. Xác minh chữ ký` · `3. Chống trùng + đối soát`. An chuyển pose wave; logo AN TECH ACADEMY hiện góc trái; dòng "Bài tiếp theo" mờ.

**Chuyển động:** 3 thẻ pop lần lượt; gạch chân từng thẻ; logo pop; fade kết.

**Chữ trên màn hình:** `3 ĐIỀU CẦN NHỚ` · `AN TECH ACADEMY` · `Hẹn gặp lại`.

**Lời đọc:**
1. Tóm lại, tích hợp thanh toán không chỉ là một lời gọi HTTP.
2. Đó là cả quy trình: tạo đơn, tạo giao dịch, xác minh và cập nhật.
3. Hãy nhớ ba điều: tính tiền ở Backend, xác minh chữ ký, chống trùng.
4. Và luôn có đối soát cho những giao dịch bị thất lạc.
5. Cảm ơn các bạn đã theo dõi An Tech Academy.
6. Nhớ theo dõi kênh để không bỏ lỡ bài giảng tiếp theo.
7. Hẹn gặp lại các bạn!

**SFX:** pop 3 thẻ; chime thương hiệu; whoosh nhẹ kết.

---

## Cổng B — mẫu 40 giây

Mẫu lấy đúng lời và hình của các cảnh trên, không dựng nội dung mới:

| Thời gian | Nội dung | Cue |
|---|---|---|
| 0–8 s | Lời chào + chủ đề, header thương hiệu, thẻ đơn "Chờ thanh toán" | s0101–s0102 |
| 8–16 s | Định nghĩa API ngân hàng, sơ đồ website → API → ngân hàng | s0201–s0202 |
| 16–25 s | Backend tự tính tiền từ Database, lưu `PENDING_PAYMENT` | s0603–s0605 |
| 25–35 s | Webhook → verify chữ ký → `PAID`, `PROCESSING`, nhánh sai thì không cập nhật | s0610–s0612 |
| 35–39 s | Chip kết `AN TECH ACADEMY · TÍCH HỢP THANH TOÁN`, An wave | không lời |

Ghi chú triển khai (2026-11-24): đo TTS thực tế 9 cue + 1 cue nhánh lỗi (s0612) → mẫu dài 39,1 s, vẫn trong khung 30–45 s. Ảnh tĩnh duyệt tại `mau/congB_41s/stills/`.

Ghi chú v2 (2026-11-24): bản `mau/congB_41s/thanhtoan_congB_41s_v2.mp4` dán logo An Tech bản quyền cố định góc phải trên mọi khung hình (`core.brand_watermark`, 120 px, alpha 0,9); bản v1 giữ nguyên để đối chiếu.

Mẫu phải thể hiện: giọng clone, phát âm thuật ngữ, nền tối + icon + An, nét bút tay, SFX, typography, caption. Sau khi duyệt mẫu mới render toàn bộ 12 cảnh.

## Kế hoạch QA

- Đo thời lượng từng cue sau TTS; nếu lệch >10% so với ước lượng, chỉnh pause/hold, không cắt lời.
- ASR + nghe các cue có thuật ngữ rủi ro (Webhook, Return URL, OAuth, Client ID/Secret, FOR UPDATE, rollback).
- Kiểm tra caption khớp lời đọc; tối đa 2 dòng; không che code/sơ đồ.
- Kiểm tra đồng bộ nét bút – SFX – lời; không có SFX khi không có hành động.
- Đo loudness −14 LUFS, TP ≤ −1; kiểm tra clipping; voice nổi hơn SFX.
- Bảng nghiệm thu cuối dùng trạng thái Đạt / Cần sửa / Chưa xác minh; không tự đánh dấu Đạt khi chưa nghe/kiểm.

## Giới hạn đã biết

- Chưa có bản nghe thử ở bước storyboard; các ước lượng thời lượng là dự tính.
- Tên ngân hàng cụ thể (VietinBank, BIDV, VNPAY, NAPAS) chỉ xuất hiện dạng tham chiếu trên slide, không đọc và không khẳng định chi tiết dịch vụ khi chưa đối chiếu tài liệu chính thức.
- Code trong bài là mô hình giảng dạy, không phải SDK/endpoint thật của ngân hàng; cần thay theo tài liệu khi tích hợp thật.
- Giọng clone có watermark PerTh mặc định của VieNeu (không nghe thấy, giữ nguyên theo chuẩn V13).
