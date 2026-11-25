# 06 · Phiếu thu giọng — Bài 12: Load Balancer

**Không cần phòng thu.** Thu bằng điện thoại hoặc tai nghe ở phòng yên tĩnh, giọng Nam miền Nam tự nhiên, trẻ, rõ, thân thiện. Không cố giọng phát thanh viên. Tốc độ nhanh hơn nói chuyện thường một chút (khoảng 1,15–1,25 lần), chỗ in đậm thì nhấn nhẹ, hết câu nghỉ ngắn.

## Cách thu

1. Mỗi cue thu thành **một file riêng**, đặt tên đúng: `S01c1`, `S01c2`, `S02c1`, … (đuôi `.wav`, `.m4a` hay `.mp3` đều được).
2. Bấm ghi, im 1 giây, đọc, im 1 giây rồi dừng. Sai thì thu lại cả câu, không cần cắt ghép.
3. Mỗi cue 1–2 bản là đủ; giữ bản đọc tự nhiên nhất.
4. Bỏ file vào thư mục `D:\Edit\Baigiang_LoadBalancer_v2\mau\ghi_am\`.
5. Thu 6 cue mẫu trước (`S01c1`, `S01c2`, `S02c1`, `S02c2`, `S03c1`, `S03c2`) để thay giọng tạm trong video mẫu; 22 cue còn lại thu sau khi mẫu được duyệt.
6. Không tự thêm nhạc, không khử ồn mạnh, không nén; giữ file gốc.

## Thứ tự đọc

### S01 — Mở đầu
- **S01c1** — Chào các bạn! Chào mừng đến với An Tech Academy. Thử tưởng tượng: **5.000 người** cùng bấm mua một chiếc điện thoại trong đúng một giây — website của bạn có sập không?
- **S01c2** — Câu trả lời nằm ở **Load Balancer**. Xem xong clip này, bạn sẽ biết cách giữ hệ thống đứng vững khi truy cập tăng gấp hàng chục lần.

### S02 — Vấn đề
- **S02c1** — Bạn là kỹ sư của một sàn thương mại điện tử. Ngày **12/12**, chương trình giảm giá bắt đầu. Chỉ trong vài phút, **5.000 người** truy cập cùng lúc, dồn hết request vào **một server duy nhất**.
- **S02c2** — CPU vọt lên, RAM đầy, thời gian phản hồi kéo dài. Khách bấm mua mà **trang quay mãi**, có người còn bị lỗi thanh toán. Một server khỏe đến mấy cũng có **giới hạn**.
- **S02c3** — Vậy làm sao để cả hệ thống cùng gánh việc, thay vì để một chú server oằn lưng? Đó chính là lúc **Load Balancer** phát huy tác dụng.

### S03 — Khái niệm
- **S03c1** — **Load Balancer** — hay **bộ cân bằng tải** — là thành phần đứng trước các server. Nó nhận request từ người dùng rồi quyết định chia cho server nào phía sau.
- **S03c2** — Hãy hình dung một **trạm thu phí cao tốc**. Xe đến rất đông; nếu chỉ mở một làn thì kẹt cứng. Nhưng khi có nhiều làn và một nhân viên điều phối, từng xe sẽ được hướng vào làn đang trống.
- **S03c3** — Load Balancer cũng vậy. Nó **không làm nghiệp vụ bán hàng**, không thay server xử lý đơn. Nó chỉ giỏi một việc: **điều phối** để hệ thống nhanh và ổn định hơn.

### S04 — Kiến trúc
- **S04c1** — Một mô hình cơ bản có **bốn thành phần**. **Client** là người dùng với điện thoại hoặc trình duyệt. **Load Balancer** là cửa ngõ tiếp nhận kết nối.
- **S04c2** — **Backend Server** xử lý nghiệp vụ: đăng nhập, tìm sản phẩm, giỏ hàng, đặt hàng. **Database** lưu tài khoản, sản phẩm, tồn kho và đơn hàng.
- **S04c3** — Bốn lớp nối thành một luồng: Client gửi request, Load Balancer điều phối, Backend xử lý, Database trả dữ liệu. Load Balancer đứng giữa nhưng **không thay server làm việc**.

### S05 — Luồng request
- **S05c1** — Khi bạn mở trang chi tiết một chiếc điện thoại, trình duyệt gửi một **HTTP request**. Request đến Load Balancer trước, rồi được chuyển đến một backend phù hợp — ví dụ **Server 01**.
- **S05c2** — Server xử lý, truy vấn Database, rồi trả kết quả về cho bạn. Request tiếp theo có thể sang **Server 02**, rồi **Server 03**.
- **S05c3** — Thay vì nâng cấp CPU, RAM cho một máy, ta thêm nhiều máy để tăng sức chịu tải. Đó là **Horizontal Scaling** — mở rộng hệ thống theo chiều ngang.

### S06 — Thuật toán 1–2
- **S06c1** — Vậy Load Balancer dựa vào đâu để chọn server? Câu trả lời nằm ở các **thuật toán cân bằng tải**. Có **bốn cách** phổ biến.
- **S06c2** — Đầu tiên là **Round Robin** — luân phiên theo thứ tự. Request 1 sang Server 01, request 2 sang 02, request 3 sang 03, rồi **quay lại 01**. Hợp khi các server cấu hình giống nhau.
- **S06c3** — Thứ hai là **Weighted Round Robin** — có trọng số. Server mạnh hơn nhận nhiều request hơn. Ví dụ Server 01 trọng số **3**, hai server còn lại trọng số **1**.

### S07 — Thuật toán 3–4
- **S07c1** — Thứ ba là **Least Connections** — chọn server đang ít kết nối nhất. Server 01 giữ **100** kết nối, Server 02 giữ **30**, Server 03 chỉ có **10**. Request tiếp theo sẽ ưu tiên **Server 03**.
- **S07c2** — Thứ tư là **IP Hash** — băm địa chỉ IP để cùng một người dùng thường về cùng một server. Tiện cho việc giữ phiên đăng nhập, nhưng **không đảm bảo tuyệt đối** khi danh sách server thay đổi.

### S08 — Health Check
- **S08c1** — Còn một cơ chế **cực quan trọng**: **Health Check**. Load Balancer định kỳ gọi vào một endpoint, ví dụ **/health**, để hỏi từng server: còn sống không?
- **S08c2** — Giả sử **Server 02** đột nhiên lỗi. Nếu vẫn nhận request, khách sẽ gặp lỗi. Health Check phát hiện, **tạm ngắt Server 02** và chuyển request sang Server 01, 03. Khi 02 được sửa và trả lời khỏe trở lại, nó được **đưa vào nhóm phục vụ**.
- **S08c3** — Nhờ vậy, một máy chủ gặp sự cố **không kéo cả website chết theo**.

### S09 — Thực tế
- **S09c1** — Trong thực tế, Load Balancer có thể là phần mềm như **Nginx**, **HAProxy**, hoặc dịch vụ đám mây như **AWS Elastic Load Balancing**, **Google Cloud Load Balancing**.
- **S09c2** — Với **Node.js** và **Express**, Nginx thường đứng làm **Reverse Proxy**: nhận request rồi chuyển đến nhóm backend **192.168.1.101, 102, 103**.
- **S09c3** — Nhưng Load Balancer **không chữa được mọi bệnh**. Database quá tải, câu SQL chậm hay thanh toán lỗi thì website vẫn chậm. Còn phải lo **phiên đăng nhập** và **tránh đặt hàng trùng**.

### S10 — Tổng kết
- **S10c1** — Tóm lại: Load Balancer nhận request và chia cho nhiều server; bốn thuật toán chính là **Round Robin**, **Weighted Round Robin**, **Least Connections** và **IP Hash**; Health Check giúp loại bỏ server gặp lỗi.
- **S10c2** — Hiểu Load Balancer là **bước đầu** để thiết kế hệ thống chịu tải lớn. Phía sau còn **cache**, **message queue**, **database scaling** — rất nhiều thứ thú vị.
- **S10c3** — Cảm ơn các bạn đã theo dõi An Tech Academy. Nhớ theo dõi kênh và để lại câu hỏi nha. **Hẹn gặp lại ở bài tiếp theo!**

## Cách đọc một số từ

- Load Balancer: "lâu be-lần-sơ" (đọc liền, rõ hai từ).
- Nginx: "en-gin-ích"; HAProxy: "hát-ây prốc-xi"; Express: "ích-prét"; Node.js: "nốt chấm jây-ét".
- Round Robin: "rao-đờ rao-bin"; Least Connections: "li-xtờ kơ-nék-sần"; IP Hash: "ai-pi hash".
- 12/12: "ngày mười hai, tháng mười hai"; 192.168.1.101: "một chín hai, chấm, một sáu tám, chấm, một, chấm, một linh một".
- Nếu bạn quen đọc cách khác, cứ đọc tự nhiên và ghi chú lại; em sẽ thống nhất toàn bài theo cách của bạn.

## Sau khi thu

Gửi file vào `mau\ghi_am\`; em sẽ cắt khoảng lặng, chuẩn hóa mức, đo lại độ dài từng cue và dựng hình khớp đúng file thật. Bản mẫu hiện tại đang dùng giọng Edge tạm để duyệt bố cục — giọng của bạn sẽ thay vào khi có file.
