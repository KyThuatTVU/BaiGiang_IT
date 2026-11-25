# 01 · Kịch bản lời thoại — Bài 12: Load Balancer

28 cue, 10 cảnh. Chỉ dẫn trong ngoặc vuông là chỉ dẫn sản xuất, **không đọc thành tiếng**.
Phụ đề tách theo cụm nghĩa, tối đa 2 dòng; bản .srt được xuất cùng bản dựng.

| # | Cue | Cảnh | Diễn xuất | Lời thoại | Nghỉ sau |
|---|---|---|---|---|---|
| 1 | S01c1 | S01 | [Tò mò, năng lượng] | Chào các bạn! Chào mừng đến với An Tech Academy. Thử tưởng tượng: 5.000 người cùng bấm mua một chiếc điện thoại trong đúng một giây — website của bạn có sập không? | 0.2s |
| 2 | S01c2 | S01 | [Chắc giọng, hứa hẹn] | Câu trả lời nằm ở Load Balancer. Xem xong clip này, bạn sẽ biết cách giữ hệ thống đứng vững khi truy cập tăng gấp hàng chục lần. | 0.2s |
| 3 | S02c1 | S02 | [Kể chuyện, bình tĩnh] | Bạn là kỹ sư của một sàn thương mại điện tử. Ngày 12/12, chương trình giảm giá bắt đầu. Chỉ trong vài phút, 5.000 người truy cập cùng lúc, dồn hết request vào một server duy nhất. | 0.5s |
| 4 | S02c2 | S02 | [Nhấn mạnh sự cố, không hù dọa] | CPU vọt lên, RAM đầy, thời gian phản hồi kéo dài. Khách bấm mua mà trang quay mãi, có người còn bị lỗi thanh toán. Một server khỏe đến mấy cũng có giới hạn. | 0.2s |
| 5 | S02c3 | S02 | [Đặt câu hỏi, chuyển ý] | Vậy làm sao để cả hệ thống cùng gánh việc, thay vì để một chú server oằn lưng? Đó chính là lúc Load Balancer phát huy tác dụng. | 0.2s |
| 6 | S03c1 | S03 | [Giải thích bình tĩnh, định nghĩa chắc] | Load Balancer — hay bộ cân bằng tải — là thành phần đứng trước các server. Nó nhận request từ người dùng rồi quyết định chia cho server nào phía sau. | 0.5s |
| 7 | S03c2 | S03 | [Kể chuyện gần gũi, dí dỏm nhẹ] | Hãy hình dung một trạm thu phí cao tốc. Xe đến rất đông; nếu chỉ mở một làn thì kẹt cứng. Nhưng khi có nhiều làn và một nhân viên điều phối, từng xe sẽ được hướng vào làn đang trống. | 0.2s |
| 8 | S03c3 | S03 | [Nhấn mạnh "chỉ điều phối"] | Load Balancer cũng vậy. Nó không làm nghiệp vụ bán hàng, không thay server xử lý đơn. Nó chỉ giỏi một việc: điều phối để hệ thống nhanh và ổn định hơn. | 0.2s |
| 9 | S04c1 | S04 | [Giải thích, liệt kê rõ] | Một mô hình cơ bản có bốn thành phần. Client là người dùng với điện thoại hoặc trình duyệt. Load Balancer là cửa ngõ tiếp nhận kết nối. | 0.5s |
| 10 | S04c2 | S04 | [Giải thích bình tĩnh] | Backend Server xử lý nghiệp vụ: đăng nhập, tìm sản phẩm, giỏ hàng, đặt hàng. Database lưu tài khoản, sản phẩm, tồn kho và đơn hàng. | 0.2s |
| 11 | S04c3 | S04 | [Tổng hợp, chắc giọng] | Bốn lớp nối thành một luồng: Client gửi request, Load Balancer điều phối, Backend xử lý, Database trả dữ liệu. Load Balancer đứng giữa nhưng không thay server làm việc. | 0.2s |
| 12 | S05c1 | S05 | [Kể tình huống thực] | Khi bạn mở trang chi tiết một chiếc điện thoại, trình duyệt gửi một HTTP request. Request đến Load Balancer trước, rồi được chuyển đến một backend phù hợp — ví dụ Server 01. | 0.5s |
| 13 | S05c2 | S05 | [Bình tĩnh, rõ] | Server xử lý, truy vấn Database, rồi trả kết quả về cho bạn. Request tiếp theo có thể sang Server 02, rồi Server 03. | 0.2s |
| 14 | S05c3 | S05 | [Nhấn mạnh khái niệm, chậm lại] | Thay vì nâng cấp CPU, RAM cho một máy, ta thêm nhiều máy để tăng sức chịu tải. Đó là Horizontal Scaling — mở rộng hệ thống theo chiều ngang. | 0.2s |
| 15 | S06c1 | S06 | [Đặt câu hỏi, tăng nhịp nhẹ] | Vậy Load Balancer dựa vào đâu để chọn server? Câu trả lời nằm ở các thuật toán cân bằng tải. Có bốn cách phổ biến. | 0.5s |
| 16 | S06c2 | S06 | [Giải thích, nhịp đều như đếm] | Đầu tiên là Round Robin — luân phiên theo thứ tự. Request 1 sang Server 01, request 2 sang 02, request 3 sang 03, rồi quay lại 01. Hợp khi các server cấu hình giống nhau. | 0.2s |
| 17 | S06c3 | S06 | [Nhấn mạnh ví dụ 3:1:1, chậm] | Thứ hai là Weighted Round Robin — có trọng số. Server mạnh hơn nhận nhiều request hơn. Ví dụ Server 01 trọng số 3, hai server còn lại trọng số 1. | 0.2s |
| 18 | S07c1 | S07 | [Kể số liệu, chậm rõ] | Thứ ba là Least Connections — chọn server đang ít kết nối nhất. Server 01 giữ 100 kết nối, Server 02 giữ 30, Server 03 chỉ có 10. Request tiếp theo sẽ ưu tiên Server 03. | 0.5s |
| 19 | S07c2 | S07 | [Giải thích, lưu ý điều kiện] | Thứ tư là IP Hash — băm địa chỉ IP để cùng một người dùng thường về cùng một server. Tiện cho việc giữ phiên đăng nhập, nhưng không đảm bảo tuyệt đối khi danh sách server thay đổi. | 0.2s |
| 20 | S08c1 | S08 | [Nhấn mạnh "cực quan trọng", chậm] | Còn một cơ chế cực quan trọng: Health Check. Load Balancer định kỳ gọi vào một endpoint, ví dụ /health, để hỏi từng server: còn sống không? | 0.5s |
| 21 | S08c2 | S08 | [Kể sự cố, nhấn mạnh phục hồi] | Giả sử Server 02 đột nhiên lỗi. Nếu vẫn nhận request, khách sẽ gặp lỗi. Health Check phát hiện, tạm ngắt Server 02 và chuyển request sang Server 01, 03. Khi 02 được sửa và trả lời khỏe trở lại, nó được đưa vào nhóm phục vụ. | 0.2s |
| 22 | S08c3 | S08 | [Kết luận chắc] | Nhờ vậy, một máy chủ gặp sự cố không kéo cả website chết theo. | 0.2s |
| 23 | S09c1 | S09 | [Liệt kê tên, đọc chậm] | Trong thực tế, Load Balancer có thể là phần mềm như Nginx, HAProxy, hoặc dịch vụ đám mây như AWS Elastic Load Balancing, Google Cloud Load Balancing. | 0.5s |
| 24 | S09c2 | S09 | [Giải thích kỹ thuật, rõ] | Với Node.js và Express, Nginx thường đứng làm Reverse Proxy: nhận request rồi chuyển đến nhóm backend 192.168.1.101, 102, 103. | 0.2s |
| 25 | S09c3 | S09 | [Cảnh báo nhẹ, cân bằng] | Nhưng Load Balancer không chữa được mọi bệnh. Database quá tải, câu SQL chậm hay thanh toán lỗi thì website vẫn chậm. Còn phải lo phiên đăng nhập và tránh đặt hàng trùng. | 0.2s |
| 26 | S10c1 | S10 | [Tổng kết, đếm 4 thuật toán] | Tóm lại: Load Balancer nhận request và chia cho nhiều server; bốn thuật toán chính là Round Robin, Weighted Round Robin, Least Connections và IP Hash; Health Check giúp loại bỏ server gặp lỗi. | 0.5s |
| 27 | S10c2 | S10 | [Truyền cảm hứng] | Hiểu Load Balancer là bước đầu để thiết kế hệ thống chịu tải lớn. Phía sau còn cache, message queue, database scaling — rất nhiều thứ thú vị. | 0.2s |
| 28 | S10c3 | S10 | [Thân thiện, kết] | Cảm ơn các bạn đã theo dõi An Tech Academy. Nhớ theo dõi kênh và để lại câu hỏi nha. Hẹn gặp lại ở bài tiếp theo! | 0.2s |

## Cách đọc số và ký hiệu (dùng khi thu)

- `5.000` → "năm nghìn"; `110.000` → "một trăm mười nghìn".
- `12/12` → "ngày mười hai, tháng mười hai".
- `3 : 1 : 1` → "tỉ lệ ba, một, một".
- `192.168.1.101` → "một chín hai, chấm, một sáu tám, chấm, một, chấm, một linh một".
- `/health` → "đường dẫn health" hoặc "hép".
- `HTTP request` → "request HTTP"; không đọc rời từng chữ cái.
- Nhịp: nghỉ ngắn sau dấu chấm, nghỉ rõ hơn sau dấu hai chấm và trước ví dụ.

## Ghi chú

- Bản mẫu S01–S03 dùng 6 cue đầu (bỏ S02c3, S03c3 vì nằm ngoài 45 giây).
- Lời thoại hiển thị và lời thoại đọc giống nhau; chỉ tách dòng phụ đề theo cụm nghĩa.
