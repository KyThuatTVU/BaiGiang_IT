# 01 — Kịch bản lời thoại (bản khóa Cổng A)

Quy ước: `[tag]` là chỉ dẫn diễn xuất, không đọc. `say` là bản cho TTS (giữ nguyên chữ đã khóa). `subs` là phụ đề hiển thị (tối đa 2 dòng, ngắt theo cụm nghĩa).
Giọng: nam, đọc nhanh 1,18 lần, xuống giọng cuối câu, nhấn từ khóa IN HOA.

---

## S01 — Intro (0:00–0:16)

**S01c1** `[Thân thiện, năng lượng]`
say: "Chào các bạn! Chào mừng đến với An Tech Academy."
subs: Chào các bạn! / Chào mừng đến với An Tech Academy.
(~3,3s)

**S01c2** `[Tò mò, kể chuyện]`
say: "Bạn bấm đặt món trên app, hai giây sau đã có thông báo xác nhận. Vậy ai đã nói chuyện với nhà bếp?"
subs: Bấm đặt món trên app, hai giây sau đã có xác nhận. / Ai đã nói chuyện với nhà bếp?
(~6,5s)

**S01c3** `[Nhấn mạnh, dẫn vào bài]`
say: "Câu trả lời là API. Năm phút nữa, bạn sẽ hiểu nó là gì và chạy như thế nào."
subs: Câu trả lời là API. / Năm phút nữa, bạn sẽ hiểu nó chạy thế nào.
(~5s)

## S02 — Vấn đề (0:16–0:44)

**S02c1** `[Giải thích bình tĩnh]`
say: "Frontend là mặt tiền: nút bấm, danh sách sản phẩm. Backend là phía sau: xử lý nghiệp vụ, tính toán, lưu dữ liệu."
subs: Frontend là mặt tiền: nút bấm, danh sách sản phẩm. / Backend xử lý, tính toán, lưu dữ liệu.
(~7s)

**S02c2** `[Nhấn mạnh vấn đề, hơi dí dỏm]`
say: "Hai bên ở hai thế giới khác nhau. Không có quy tắc chung, mỗi màn hình phải chép cứng dữ liệu. Đổi một cái giá là sửa cả chục chỗ."
subs: Không có quy tắc chung, mỗi màn hình chép cứng dữ liệu. / Đổi một cái giá là sửa cả chục chỗ.
(~8s)

**S02c3** `[Chốt ý]`
say: "Nên cần một quầy giao dịch chung: bên này gửi yêu cầu, bên kia trả kết quả. Quầy đó chính là API."
subs: Cần một quầy giao dịch chung: / gửi yêu cầu — trả kết quả. Đó là API.
(~6s)

## S03 — API là gì (0:44–1:18)

**S03c1** `[Định nghĩa, chắc giọng]`
say: "API, viết tắt của Application Programming Interface, tiếng Việt là giao diện lập trình ứng dụng. Nghe to tát, nhưng hiểu đơn giản là bộ quy tắc để hai phần mềm nói chuyện."
subs: API — Application Programming Interface. / Bộ quy tắc để hai phần mềm nói chuyện.
(~10s)

**S03c2** `[Ví dụ gần gũi]`
say: "Giống ổ cắm điện trong nhà. Bạn cắm phích là có điện, không cần biết nhà máy điện xây thế nào. API chính là ổ cắm giữa các hệ thống."
subs: Giống ổ cắm điện: cắm phích là có điện, / không cần biết nhà máy điện xây thế nào.
(~8,5s)

**S03c3** `[Liệt kê, nhấn từng ý]`
say: "Ba đặc điểm: có quy tắc chung, có đầu vào và đầu ra, và giấu phần xử lý bên trong. Một API có thể phục vụ web, app điện thoại và app quản trị cùng lúc."
subs: Có quy tắc chung, có đầu vào — đầu ra, / và giấu phần xử lý bên trong.
(~9,5s)

## S04 — Nhà hàng (1:18–1:56)

**S04c1** `[Kể chuyện, chậm vừa]`
say: "Dễ nhất là ví dụ nhà hàng. Bạn là khách, tức Client. Anh bồi bàn là API. Phiếu gọi món là Request. Nhà bếp là Backend. Món bưng ra là Response."
subs: Khách = Client · Bồi bàn = API · Phiếu = Request / Bếp = Backend · Món bưng ra = Response
(~11s)

**S04c2** `[Kể chuyện]`
say: "Bạn gọi cơm gà. Bồi bàn ghi phiếu, chuyển xuống bếp. Bếp kiểm tra nguyên liệu, nấu chín, trao lại. Bồi bàn bưng ra bàn cho bạn."
subs: Bồi bàn ghi phiếu, chuyển xuống bếp. / Bếp nấu xong, bồi bàn bưng ra.
(~8,5s)

**S04c3** `[Nhấn mạnh, cảnh báo nhẹ]`
say: "Nhớ kỹ: anh bồi bàn không nấu ăn. API cũng không tự xử lý nghiệp vụ. Nó là người đưa thư: đúng người, đúng món, đúng lúc."
subs: Bồi bàn không nấu ăn — API không tự xử lý nghiệp vụ. / Nó là người đưa thư: đúng người, đúng món.
(~8s)

## S05 — Endpoint & URL (1:56–2:26)

**S05c1** `[Giải thích]`
say: "Endpoint là địa chỉ cụ thể để gửi yêu cầu. Nhà hàng có nhiều quầy: quầy món ăn, quầy đồ uống. API có nhiều endpoint: sản phẩm, đơn hàng, người dùng."
subs: Endpoint là địa chỉ cụ thể để gửi yêu cầu. / API có nhiều endpoint: sản phẩm, đơn hàng, người dùng.
(~8,5s)

**S05c2** `[Bóc tách từng phần]`
say: "Bóc một địa chỉ nhé: https là giao thức, example chấm com là tên miền, api là khu vực API, products là tài nguyên, còn số 1 là mã sản phẩm."
subs: https = giao thức · example.com = tên miền / api/products = tài nguyên · 1 = mã sản phẩm
(~9s)

**S05c3** `[Chốt]`
say: "Một API gồm nhiều endpoint. Endpoint là cái cửa; HTTP method là việc bạn muốn làm ở cái cửa đó."
subs: Endpoint là cái cửa. / HTTP method là việc bạn muốn làm ở cửa đó.
(~6s)

## S06 — Request (2:26–2:56)

**S06c1** `[Giải thích nhanh]`
say: "Request là lá phiếu gửi đi. Nó có bốn phần: method, URL, headers và body."
subs: Request là lá phiếu gửi đi. / Bốn phần: method · URL · headers · body.
(~5,5s)

**S06c2** `[Giải thích, nhấn từng phần]`
say: "Method là hành động. URL là địa chỉ. Headers là giấy tờ tùy thân, ví dụ token đăng nhập. Body là nội dung, thường là JSON."
subs: Method = hành động · URL = địa chỉ / Headers = giấy tờ · Body = nội dung (JSON)
(~8,5s)

**S06c3** `[Ví dụ cụ thể]`
say: "Nhìn một request thật: POST tới api products, Content-Type là application JSON, body gồm tên, giá, số lượng. Bếp đọc phiếu là biết phải nấu gì."
subs: POST /api/products · Content-Type: application/json / Body: tên, giá, số lượng
(~9,5s)

## S07 — Method + Status (2:56–3:30)

**S07c1** `[Liệt kê, nhịp đều]`
say: "Bốn method quen thuộc: GET lấy dữ liệu, POST tạo mới, PUT cập nhật toàn bộ, DELETE xóa. Chỉ sửa một trường? Dùng PATCH."
subs: GET lấy · POST tạo · PUT thay thế · DELETE xóa / Chỉ sửa một trường: PATCH
(~8,5s)

**S07c2** `[Chốt]`
say: "Bốn thao tác đó chính là CRUD: Create, Read, Update, Delete."
subs: Đó chính là CRUD: / Create · Read · Update · Delete
(~4,5s)

**S07c3** `[Liệt kê mã, rõ ràng]`
say: "Server trả mã trạng thái: 200 là OK, 201 đã tạo, 400 gửi sai, 401 chưa đăng nhập, 404 không tìm thấy, 500 server lỗi. Nhìn mã là biết chuyện gì."
subs: 200 OK · 201 Created · 400 sai · 401 chưa đăng nhập / 404 không thấy · 500 server lỗi
(~9,5s)

## S08 — Response & JSON (3:30–3:56)

**S08c1** `[Giải thích]`
say: "Response cũng ba phần: mã trạng thái, headers và body. Body thường là JSON, văn bản dễ đọc cho cả người lẫn máy."
subs: Response: status · headers · body. / Body thường là JSON — dễ đọc cho người và máy.
(~7,5s)

**S08c2** `[Giải thích]`
say: "JSON có string, number, boolean, null, object và array. Danh sách sản phẩm là một array gồm nhiều object."
subs: JSON: string · number · boolean · null · object · array / Danh sách = array các object
(~7s)

**S08c3** `[Mẹo, dí dỏm nhẹ]`
say: "JavaScript có JSON điểm stringify để đóng gói, và JSON điểm parse để mở ra. Gửi đi thì stringify, nhận về thì parse."
subs: JSON.stringify để đóng gói / JSON.parse để mở ra
(~7,5s)

## S09 — Thực chiến (3:56–4:30)

**S09c1** `[Hướng dẫn, tự tin]`
say: "Thực chiến với Node.js và Express.js. Khai báo app, bật express json, viết route app get cho api products, rồi trả về res json. Chưa tới hai chục dòng."
subs: Node.js + Express.js: app.get("/api/products") / res.json(...) — chưa tới 20 dòng
(~10s)

**S09c2** `[Hướng dẫn]`
say: "Chạy node server điểm js, mở localhost 3000 trên api products là thấy danh sách. Thử POST bằng Postman hoặc Thunder Client, vì trình duyệt chỉ gửi GET."
subs: Mở localhost:3000/api/products là thấy JSON. / Thử POST bằng Postman hoặc Thunder Client.
(~9,5s)

**S09c3** `[Giải thích]`
say: "Phía frontend, Fetch API gọi endpoint, await response json, rồi đổ dữ liệu lên giao diện. Frontend không cần biết bên kia dùng MySQL hay mảng tạm."
subs: fetch(endpoint) → await response.json() / Frontend không cần biết backend lưu ở đâu.
(~9,5s)

## S10 — Lỗi + tổng kết (4:30–4:58)

**S10c1** `[Cảnh báo, nhấn vừa]`
say: "Vài lỗi hay gặp: quên bật express json nên body rỗng; quên cấu hình CORS nên trình duyệt chặn; và tin dữ liệu frontend mà không kiểm tra ở backend."
subs: Quên express.json → body rỗng. / Quên CORS → trình duyệt chặn.
(~9,5s)

**S10c2** `[Tổng kết chắc giọng]`
say: "Nhớ ba điều: API là cầu nối, endpoint là địa chỉ, method cộng status code là ngôn ngữ chung. Request đi, response về, JSON ở giữa."
subs: API = cầu nối · Endpoint = địa chỉ / Method + status code = ngôn ngữ chung
(~8,5s)

**S10c3** `[Mời bài sau]`
say: "Hiểu API là bạn đã mở cửa bước sang backend. Còn RESTful, xác thực JWT và bảo mật API, mình sẽ nói ở bài sau."
subs: Hiểu API là mở cửa bước sang backend. / RESTful, JWT và bảo mật API — bài sau.
(~7,5s)

## S11 — Outro (4:58–5:06)

**S11c1** `[Chắc, truyền cảm hứng]`
say: "Cảm ơn các bạn đã theo dõi An Tech Academy. Hiểu công nghệ, làm chủ tương lai!"
subs: Cảm ơn các bạn đã theo dõi An Tech Academy. / Hiểu công nghệ, làm chủ tương lai!
(~5s)

**S11c2** `[Thân thiện]`
say: "Nhớ theo dõi kênh và để lại câu hỏi nha. Hẹn gặp lại ở bài tiếp theo."
subs: Nhớ theo dõi kênh và để lại câu hỏi nha. / Hẹn gặp lại!
(~4,5s)
