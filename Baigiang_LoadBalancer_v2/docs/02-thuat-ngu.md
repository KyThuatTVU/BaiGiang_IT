# 02 · Bảng thuật ngữ CNTT — Bài 12: Load Balancer

Quy tắc: lần đầu xuất hiện nói kèm nghĩa Việt ("Load Balancer, tức bộ cân bằng tải"), các lần sau dùng tên gốc.
**Chưa từ nào được nghe kiểm.** Cột "cách đọc đề xuất" là phiên âm tiếng Việt để người thu đọc thống nhất; người thu xác nhận khi ghi âm.

| Thuật ngữ | Nhóm | Nghĩa tiếng Việt (giải thích lần đầu) | Cách đọc đề xuất | Nguồn / trạng thái | Cách viết khi thu | Đã nghe kiểm |
|---|---|---|---|---|---|---|
| Load Balancer | Kiến trúc | Bộ cân bằng tải, chia request cho nhiều server | "lâu be-lần-sơ" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Client | Kiến trúc | Máy khách / trình duyệt của người dùng | "clai-ần" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Server | Kiến trúc | Máy chủ | "sơ-vờ" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Backend | Kiến trúc | Phần máy chủ xử lý nghiệp vụ | "béc-ken" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Database | Dữ liệu | Cơ sở dữ liệu | "đây-ta-bây" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Request | Web | Yêu cầu gửi từ client lên server | "ri-quét" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Response | Web | Phản hồi từ server về client | "ri-spon" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| CPU | Phần cứng | Bộ xử lý trung tâm | "xê-pê-u" | CẦN XÁC MINH | Viết hoa, đọc từng chữ | Chưa |
| RAM | Phần cứng | Bộ nhớ tạm | "ram" | CẦN XÁC MINH | Viết hoa | Chưa |
| HTTP | Giao thức | Giao thức truyền tải web | "hát-tê-tê-pê" | CẦN XÁC MINH | Viết hoa, đọc từng chữ | Chưa |
| Endpoint | Web/API | Điểm cuối nhận request | "en-đi-poi-ần" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Health Check | Vận hành | Kiểm tra định kỳ server còn sống | "hen-chờ chék" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Timeout | Vận hành | Hết thời gian chờ phản hồi | "taim-ao" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Round Robin | Thuật toán | Luân phiên theo thứ tự | "rao-đờ rao-bin" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Weighted Round Robin | Thuật toán | Luân phiên có trọng số | "quây-tịt rao-đờ rao-bin" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Least Connections | Thuật toán | Chọn server ít kết nối nhất | "li-xtờ kơ-nék-sần" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| IP Hash | Thuật toán | Băm địa chỉ IP để giữ phiên | "ai-pi hash" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| IP | Mạng | Địa chỉ mạng của thiết bị | "ai-pi" | CẦN XÁC MINH | Viết hoa | Chưa |
| Horizontal Scaling | Kiến trúc | Mở rộng theo chiều ngang, thêm máy | "hô-ri-zon-tồ skây-ling" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Reverse Proxy | Kiến trúc | Proxy đứng trước backend | "ri-vợt prốc-xi" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Nginx | Công cụ | Web server / reverse proxy phổ biến | "en-gin-ích" (engine-x) | Quy ước phổ biến, chưa nghe kiểm | Giữ nguyên | Chưa |
| HAProxy | Công cụ | Load balancer/proxy mã nguồn mở | "hát-ây prốc-xi" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| AWS Elastic Load Balancing | Cloud | Dịch vụ cân bằng tải của Amazon | "ây đắp-liu ét · i-lát-tích lâu be-lần-sing" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Google Cloud Load Balancing | Cloud | Dịch vụ cân bằng tải của Google | "gu-gồ clao lâu be-lần-sing" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Node.js | Công cụ | Nền tảng chạy JavaScript phía server | "nốt chấm jây-ét" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| Express | Công cụ | Framework web cho Node.js | "ích-prét" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| SQL | Dữ liệu | Ngôn ngữ truy vấn cơ sở dữ liệu | "ét-quy-en" | CẦN XÁC MINH (có nhiều cách đọc) | Viết hoa, thống nhất một cách | Chưa |
| Session | Web | Phiên đăng nhập của người dùng | "séc-sần" | CẦN XÁC MINH | Giữ nguyên | Chưa |
| 502 | Mã lỗi | Lỗi gateway khi backend không phản hồi | "năm linh hai" | CẦN XÁC MINH | Giữ nguyên số | Chưa |
| Cache / Message Queue / CDN | Outro | Bộ nhớ đệm / hàng đợi / mạng phân phối nội dung | "két · mé-sịt quơ · xê-đê-en" | CẦN XÁC MINH | Giữ nguyên | Chưa |

## Thống nhất cách đọc

- Acronym đọc rời từng chữ: CPU, RAM, HTTP, IP, AWS, CDN.
- Tên sản phẩm đọc liền: Nginx, HAProxy, Express, Node.js.
- "Load Balancer" luôn đọc hai từ, không nuốt âm cuối.
- Nếu người thu chọn cách đọc khác, ghi lại một lần và dùng thống nhất cả video.
