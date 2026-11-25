# -*- coding: utf-8 -*-
"""Sinh manifest full + sample cho Load Balancer v2."""
import json, os

ROOT = "D:/Edit/Baigiang_LoadBalancer_v2"
FULL = ROOT + "/mau"

CUES = [
    ("S01c1", "S01", "Chào các bạn! Chào mừng đến với An Tech Academy. Thử tưởng tượng: 5.000 người cùng bấm mua một chiếc điện thoại trong đúng một giây — website của bạn có sập không?",
     ["Chào các bạn! Chào mừng đến với An Tech Academy.",
      "5.000 người cùng mua một chiếc điện thoại trong một giây — web có sập không?"]),
    ("S01c2", "S01", "Câu trả lời nằm ở Load Balancer. Xem xong clip này, bạn sẽ biết cách giữ hệ thống đứng vững khi truy cập tăng gấp hàng chục lần.",
     ["Câu trả lời nằm ở Load Balancer.",
      "Giữ hệ thống đứng vững khi truy cập tăng gấp hàng chục lần."]),
    ("S02c1", "S02", "Bạn là kỹ sư của một sàn thương mại điện tử. Ngày 12/12, chương trình giảm giá bắt đầu. Chỉ trong vài phút, 5.000 người truy cập cùng lúc, dồn hết request vào một server duy nhất.",
     ["Bạn là kỹ sư sàn thương mại điện tử. Ngày 12/12, giảm giá bắt đầu.",
      "5.000 người truy cập cùng lúc, dồn hết request vào một server."]),
    ("S02c2", "S02", "CPU vọt lên, RAM đầy, thời gian phản hồi kéo dài. Khách bấm mua mà trang quay mãi, có người còn bị lỗi thanh toán. Một server khỏe đến mấy cũng có giới hạn.",
     ["CPU vọt lên, RAM đầy, trang quay mãi. Khách còn bị lỗi thanh toán.",
      "Một server khỏe đến mấy cũng có giới hạn."]),
    ("S02c3", "S02", "Vậy làm sao để cả hệ thống cùng gánh việc, thay vì để một chú server oằn lưng? Đó chính là lúc Load Balancer phát huy tác dụng.",
     ["Vậy làm sao để cả hệ thống cùng gánh việc?",
      "Đó chính là lúc Load Balancer phát huy tác dụng."]),
    ("S03c1", "S03", "Load Balancer — hay bộ cân bằng tải — là thành phần đứng trước các server. Nó nhận request từ người dùng rồi quyết định chia cho server nào phía sau.",
     ["Load Balancer — bộ cân bằng tải — đứng trước các server.",
      "Nó nhận request và quyết định chia cho server nào phía sau."]),
    ("S03c2", "S03", "Hãy hình dung một trạm thu phí cao tốc. Xe đến rất đông; nếu chỉ mở một làn thì kẹt cứng. Nhưng khi có nhiều làn và một nhân viên điều phối, từng xe sẽ được hướng vào làn đang trống.",
     ["Giống trạm thu phí cao tốc: xe rất đông, một làn thì kẹt cứng.",
      "Nhiều làn và một nhân viên điều phối sẽ hướng xe vào làn trống."]),
    ("S03c3", "S03", "Load Balancer cũng vậy. Nó không làm nghiệp vụ bán hàng, không thay server xử lý đơn. Nó chỉ giỏi một việc: điều phối để hệ thống nhanh và ổn định hơn.",
     ["Load Balancer không làm nghiệp vụ bán hàng, không thay server xử lý đơn.",
      "Nó chỉ giỏi điều phối để hệ thống nhanh và ổn định hơn."]),
    ("S04c1", "S04", "Một mô hình cơ bản có bốn thành phần. Client là người dùng với điện thoại hoặc trình duyệt. Load Balancer là cửa ngõ tiếp nhận kết nối.",
     ["Mô hình cơ bản có bốn thành phần.",
      "Client là người dùng; Load Balancer là cửa ngõ tiếp nhận kết nối."]),
    ("S04c2", "S04", "Backend Server xử lý nghiệp vụ: đăng nhập, tìm sản phẩm, giỏ hàng, đặt hàng. Database lưu tài khoản, sản phẩm, tồn kho và đơn hàng.",
     ["Backend Server xử lý đăng nhập, tìm sản phẩm, giỏ hàng, đặt hàng.",
      "Database lưu tài khoản, sản phẩm, tồn kho và đơn hàng."]),
    ("S04c3", "S04", "Bốn lớp nối thành một luồng: Client gửi request, Load Balancer điều phối, Backend xử lý, Database trả dữ liệu. Load Balancer đứng giữa nhưng không thay server làm việc.",
     ["Client gửi request, Load Balancer điều phối, Backend xử lý, Database trả dữ liệu.",
      "Load Balancer đứng giữa nhưng không thay server làm việc."]),
    ("S05c1", "S05", "Khi bạn mở trang chi tiết một chiếc điện thoại, trình duyệt gửi một HTTP request. Request đến Load Balancer trước, rồi được chuyển đến một backend phù hợp — ví dụ Server 01.",
     ["Khi mở trang chi tiết điện thoại, trình duyệt gửi một HTTP request.",
      "Load Balancer nhận trước, rồi chuyển đến backend phù hợp — ví dụ Server 01."]),
    ("S05c2", "S05", "Server xử lý, truy vấn Database, rồi trả kết quả về cho bạn. Request tiếp theo có thể sang Server 02, rồi Server 03. ",
     ["Server xử lý, truy vấn Database, rồi trả kết quả về.",
      "Request tiếp theo có thể sang Server 02, rồi Server 03."]),
    ("S05c3", "S05", "Thay vì nâng cấp CPU, RAM cho một máy, ta thêm nhiều máy để tăng sức chịu tải. Đó là Horizontal Scaling — mở rộng hệ thống theo chiều ngang.",
     ["Thêm nhiều máy để tăng sức chịu tải: đó là Horizontal Scaling.",
      "Mở rộng hệ thống theo chiều ngang."]),
    ("S06c1", "S06", "Vậy Load Balancer dựa vào đâu để chọn server? Câu trả lời nằm ở các thuật toán cân bằng tải. Có bốn cách phổ biến.",
     ["Vậy Load Balancer dựa vào đâu để chọn server?",
      "Câu trả lời nằm ở các thuật toán cân bằng tải. Có bốn cách phổ biến."]),
    ("S06c2", "S06", "Đầu tiên là Round Robin — luân phiên theo thứ tự. Request 1 sang Server 01, request 2 sang 02, request 3 sang 03, rồi quay lại 01. Hợp khi các server cấu hình giống nhau.",
     ["Round Robin — luân phiên: request 1 sang Server 01, 2 sang 02, 3 sang 03, rồi quay lại 01.",
      "Hợp khi các server cấu hình giống nhau."]),
    ("S06c3", "S06", "Thứ hai là Weighted Round Robin — có trọng số. Server mạnh hơn nhận nhiều request hơn. Ví dụ Server 01 trọng số 3, hai server còn lại trọng số 1.",
     ["Weighted Round Robin — có trọng số. Server mạnh nhận nhiều request hơn.",
      "Ví dụ Server 01 trọng số 3, hai server còn lại trọng số 1."]),
    ("S07c1", "S07", "Thứ ba là Least Connections — chọn server đang ít kết nối nhất. Server 01 giữ 100 kết nối, Server 02 giữ 30, Server 03 chỉ có 10. Request tiếp theo sẽ ưu tiên Server 03.",
     ["Least Connections — chọn server đang ít kết nối nhất.",
      "S01 giữ 100 kết nối, S02 giữ 30, S03 chỉ có 10: request tiếp theo ưu tiên S03."]),
    ("S07c2", "S07", "Thứ tư là IP Hash — băm địa chỉ IP để cùng một người dùng thường về cùng một server. Tiện cho việc giữ phiên đăng nhập, nhưng không đảm bảo tuyệt đối khi danh sách server thay đổi.",
     ["IP Hash — băm địa chỉ IP để cùng người dùng thường về cùng một server.",
      "Tiện giữ phiên đăng nhập, nhưng không đảm bảo tuyệt đối khi server thay đổi."]),
    ("S08c1", "S08", "Còn một cơ chế cực quan trọng: Health Check. Load Balancer định kỳ gọi vào một endpoint, ví dụ /health, để hỏi từng server: còn sống không?",
     ["Health Check — Load Balancer định kỳ gọi vào /health.",
      "Nó hỏi từng server: còn sống không?"]),
    ("S08c2", "S08", "Giả sử Server 02 đột nhiên lỗi. Nếu vẫn nhận request, khách sẽ gặp lỗi. Health Check phát hiện, tạm ngắt Server 02 và chuyển request sang Server 01, 03. Khi 02 được sửa và trả lời khỏe trở lại, nó được đưa vào nhóm phục vụ.",
     ["Server 02 lỗi: nếu vẫn nhận request, khách sẽ gặp lỗi.",
      "Health Check tạm ngắt Server 02, chuyển request sang 01 và 03."]),
    ("S08c3", "S08", "Nhờ vậy, một máy chủ gặp sự cố không kéo cả website chết theo.",
     ["Khi Server 02 khỏe lại, nó được đưa vào nhóm phục vụ.",
      "Một máy chủ gặp sự cố không kéo cả website chết theo."]),
    ("S09c1", "S09", "Trong thực tế, Load Balancer có thể là phần mềm như Nginx, HAProxy, hoặc dịch vụ đám mây như AWS Elastic Load Balancing, Google Cloud Load Balancing.",
     ["Load Balancer có thể là Nginx, HAProxy, hoặc dịch vụ đám mây.",
      "Ví dụ AWS Elastic Load Balancing, Google Cloud Load Balancing."]),
    ("S09c2", "S09", "Với Node.js và Express, Nginx thường đứng làm Reverse Proxy: nhận request rồi chuyển đến nhóm backend 192.168.1.101, 102, 103.",
     ["Với Node.js và Express, Nginx thường làm Reverse Proxy.",
      "Nhận request rồi chuyển đến nhóm backend 192.168.1.101, 102, 103."]),
    ("S09c3", "S09", "Nhưng Load Balancer không chữa được mọi bệnh. Database quá tải, câu SQL chậm hay thanh toán lỗi thì website vẫn chậm. Còn phải lo phiên đăng nhập và tránh đặt hàng trùng.",
     ["Nhưng Load Balancer không chữa được mọi bệnh.",
      "Database quá tải, SQL chậm hay thanh toán lỗi thì web vẫn chậm."]),
    ("S10c1", "S10", "Tóm lại: Load Balancer nhận request và chia cho nhiều server; bốn thuật toán chính là Round Robin, Weighted Round Robin, Least Connections và IP Hash; Health Check giúp loại bỏ server gặp lỗi.",
     ["Load Balancer chia request cho nhiều server.",
      "Bốn thuật toán: Round Robin, Weighted Round Robin, Least Connections, IP Hash."]),
    ("S10c2", "S10", "Hiểu Load Balancer là bước đầu để thiết kế hệ thống chịu tải lớn. Phía sau còn cache, message queue, database scaling — rất nhiều thứ thú vị.",
     ["Health Check loại bỏ server gặp lỗi.",
      "Hiểu Load Balancer là bước đầu để thiết kế hệ thống chịu tải lớn."]),
    ("S10c3", "S10", "Cảm ơn các bạn đã theo dõi An Tech Academy. Nhớ theo dõi kênh và để lại câu hỏi nha. Hẹn gặp lại ở bài tiếp theo!",
     ["Cảm ơn các bạn đã theo dõi An Tech Academy.",
      "Nhớ theo dõi kênh và hẹn gặp lại ở bài tiếp theo!"]),
]

SAMPLE = [
    ("S01c1", "S01", "Chào các bạn! Chào mừng đến với An Tech Academy. 5.000 người cùng mua hàng trong một giây — web có sập không?",
     ["Chào các bạn! Chào mừng đến với An Tech Academy.",
      "5.000 người cùng mua hàng trong một giây — web có sập không?"]),
    ("S01c2", "S01", "Câu trả lời là Load Balancer — cách giữ hệ thống đứng vững khi truy cập tăng vọt.",
     ["Câu trả lời là Load Balancer.",
      "Cách giữ hệ thống đứng vững khi truy cập tăng vọt."]),
    ("S02c1", "S02", "Ngày 12/12, 5.000 người truy cập cùng lúc, dồn hết request vào một server.",
     ["Ngày 12/12, 5.000 người truy cập cùng lúc,",
      "dồn hết request vào một server."]),
    ("S02c2", "S02", "CPU vọt lên, RAM đầy, trang quay mãi. Một server khỏe đến mấy cũng có giới hạn.",
     ["CPU vọt lên, RAM đầy, trang quay mãi.",
      "Một server khỏe đến mấy cũng có giới hạn."]),
    ("S03c1", "S03", "Load Balancer đứng trước các server, nhận request rồi chia đều cho phía sau.",
     ["Load Balancer đứng trước các server,",
      "nhận request rồi chia đều cho phía sau."]),
    ("S03c2", "S03", "Giống trạm thu phí: nhiều làn, một nhân viên điều phối.",
     ["Giống trạm thu phí:", "nhiều làn, một nhân viên điều phối."]),
]


def build(rows, path, sample=False):
    out = []
    for i, (cid, sid, text, subs) in enumerate(rows):
        prev = rows[i - 1] if i else None
        pause = 0.20
        if prev and prev[1] != sid:
            pause = 0.50
        out.append({
            "id": cid, "scene": sid,
            "rate": "+10%" if not sample else "+8%",
            "shift": 0.0, "pause_after": pause,
            "text": text, "say": text, "subs": subs,
        })
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(os.path.basename(path), len(out), "cues", sum(len(r[2]) for r in rows), "chars")


if __name__ == "__main__":
    os.makedirs(FULL, exist_ok=True)
    build([(a, b, c, d) for a, b, c, d in CUES], FULL + "/manifest.json")
    build(SAMPLE, FULL + "/manifest_sample.json", True)
