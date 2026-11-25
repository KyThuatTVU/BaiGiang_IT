# STORYBOARD — CỔNG A
## Bên trong một dự án phát triển phần mềm

*17 cảnh · 1920×1080 · 30fps · Mỗi cảnh: mục tiêu học tập, hình ảnh, chuyển động, chữ màn hình, SFX, tư thế giáo viên An. Thời gian dự kiến theo 01_KichBan; chốt lại theo audio thật.*

Quy ước chung: giáo viên An đứng góc trái dưới (hoặc phải tùy bố cục), cao ~380px, không che nội dung chính; cảnh sơ đồ/code thu nhỏ An còn ~240px. Nét vẽ tay màu amber xuất hiện ĐÚNG lúc lời nhắc từ khóa, kèm tiếng bút. Chuyển cảnh: crossfade 0.3s + whoosh nhẹ (không glitch).

| Cảnh | Thời gian | Mục tiêu học tập | Hình ảnh & chuyển động | Chữ màn hình | SFX | An |
| --- | --- | --- | --- | --- | --- | --- |
| S01 Intro | 0:00–0:24 | Nhận diện + tò mò | Nền sáng, logo chữ AN TECH ACADEMY hiện bằng stroke reveal; 3 icon câu hỏi (ý tưởng/chia việc/kiểm tra) pop lần lượt theo câu hỏi; An đứng cạnh bảng, tay trình bày | "Bên trong một dự án phát triển phần mềm" + tagline | chime thương hiệu nhẹ; pop ×3 | present → point |
| S02 Khái niệm | 0:24–0:48 | Hiểu định nghĩa dự án phần mềm | Thẻ định nghĩa 4 từ khóa (mục tiêu/thời gian/nguồn lực/phạm vi) gạch chân vẽ tay lần lượt; mockup website bán hàng điện thoại bên phải, 5 icon chức năng pop theo lời | Định nghĩa đầy đủ; nhãn chức năng | bút ×4; pop ×5 | point phải |
| S03 Công ty vs dự án | 0:48–1:12 | Phân biệt 2 khái niệm; hiểu vì sao chia việc | Tòa nhà công ty chứa 3 thẻ dự án (bán hàng/nhân sự/đặt lịch) slide vào; nửa dưới: 1 dev ôm 7 việc (icon chồng lên, rung nhẹ quá tải) → tách thành hàng ngang 5 thành viên | "Công ty ≠ Dự án"; "Chia theo chuyên môn" | whoosh; pop; click tách nhóm | think → present |
| S04 Bốn nhóm | 1:12–1:27 | Nhớ cơ cấu 4 nhóm | Sơ đồ 4 tầng vẽ dần bằng connector nét tay từ trên xuống; mỗi tầng 1 màu chức năng; chú thích "mô hình tham khảo" fade in | 4 nhãn nhóm | bút ×4; chime chốt | point trái |
| S05 Lãnh đạo | 1:27–1:53 | Vai trò CEO/CTO/Sponsor | 3 thẻ dọc lần lượt sáng đèn theo lời; thẻ CEO: icon chiến lược; CTO: 2 cặp lựa chọn công nghệ hiện dạng cân; Sponsor: icon ngân sách + khiên | CEO/CTO/Project Sponsor + 2 dòng vai trò mỗi thẻ | pop thẻ; click lựa chọn | point phải |
| S06 PM | 1:53–2:15 | 5 việc của PM | Bảng Kanban 3 cột (Cần làm/Đang làm/Xong); 5 task chip bay vào theo lời; 1 task đỏ "rủi ro" xuất hiện rồi được kéo sang xử lý; gạch chân câu chốt "không cần code giỏi nhất" | 5 đầu việc PM | whoosh task; click; bút gạch chân | present |
| S07 PO & BA | 2:15–2:42 | PO ưu tiên; BA làm rõ yêu cầu | Trái: Product Backlog 5 dòng, dòng ưu tiên kéo lên đầu (PO). Phải: bubble chat khách hàng → 3 câu hỏi BA pop → tài liệu SRS/Use Case/User Story hiện dạng trang giấy | Product Backlog; câu hỏi BA; tên tài liệu | pop bubble; bút; click kéo dòng | point trái/phải |
| S08 Ba Lead | 2:42–2:53 | Tech Lead/UI-UX Lead/QA Lead | 3 thẻ mini ngang, icon code/palette/checklist, sáng lần lượt | 3 chức danh + 1 vai trò | pop ×3 | present |
| S09 Designer→FE | 2:53–3:09 | Thiết kế thành giao diện chạy | Khung Figma (wireframe trang đăng nhập) bên trái morph-slide sang khung trình duyệt bên phải có màu; hàng icon HTML/CSS/JS/React hiện dưới | "Figma → Trình duyệt"; tên công nghệ | whoosh morph; pop icon | point phải |
| S10 Luồng đăng nhập | 3:09–3:32 | Hiểu FE↔BE↔DB qua API | **Animation trọng tâm**: nút Đăng nhập được click → gói dữ liệu (email + mật khẩu che ••••) chạy dọc connector FE→API→BE; BE sáng đèn kiểm tra → truy vấn DB (ống dữ liệu 2 chiều) → gói kết quả chạy ngược về FE → toast "Đăng nhập thành công". Mỗi bước sáng đúng lúc lời đọc bước đó; nhãn JSON hiện khi trả kết quả | FE / API / Backend / Database; "JSON" | click; whoosh gói tin ×2; chime thành công | point phải, thu nhỏ |
| S11 DB & QA | 3:32–3:48 | Bảng dữ liệu + kiểm thử | Trái: ERD mini 3 bảng Users/Products/Orders nối khóa (connector vẽ tay). Phải: checklist 3 ca kiểm thử tick xanh/đỏ dần; 1 bug đỏ → thẻ Bug Report bay sang dev | tên bảng; "Bug Report" | bút connector; tick; pop bug | point trái |
| S12 DevOps/Sec/Writer | 3:48–4:03 | Triển khai + bảo mật + tài liệu | Pipeline ngang: Code → Build → Test → Deploy, mũi tên chạy sáng dần đến icon máy chủ + ổ khóa HTTPS; 2 thẻ phụ Security (khiên, nhãn SQLi/XSS) và Writer (trang tài liệu) | CI/CD; HTTPS; SQL Injection; XSS | whoosh pipeline; click khóa; pop thẻ | present |
| S13 Sáu giai đoạn | 4:03–4:35 | Nhớ 6 giai đoạn + ai chủ trì | Timeline ngang 6 nút vẽ dần; mỗi nút: tên giai đoạn + chip kết quả + avatar vai trò chủ trì sáng theo lời S13c3; camera pan nhẹ trái→phải theo tiến độ | 6 tên giai đoạn; kết quả; vai trò | bút ×6; pop chip; whoosh pan | point trái, thu nhỏ |
| S14 Phối hợp + công cụ | 4:35–4:58 | Yêu cầu đi qua quy trình, không code ngay | Chuỗi relay 6 mắt xích (Khách hàng→BA→PM→Tech Lead→Dev+Design→QA→DevOps) gói yêu cầu "thanh toán" chạy từng chặng; sau đó lưới 6 icon công cụ pop (Jira/Figma/Git+GitHub/Postman/VS Code/Docker) | nhãn mắt xích; tên công cụ | whoosh chặng; pop ×6 | present → point |
| S15 Người mới + bài tập | 4:58–5:22 | Chọn hướng theo sở thích | 3 thẻ hướng (Frontend/Backend/BA) với icon sở thích; dưới: 8 avatar tròn xếp thành đội + thẻ đề bài "website nhà hàng · 8 tuần" | 3 hướng; đề bài tập | pop thẻ; chime đội hình | present |
| S16 Quiz | 5:22–5:43 | Củng cố 2 kiến thức | Thẻ câu hỏi lớn, 3 đáp án A/B/C; đồng hồ 2 giây chờ (không đọc); đáp án đúng viền xanh + khoanh vẽ tay, đáp án khác mờ đi; chuyển câu bằng slide ngang | câu hỏi + đáp án nguyên văn bản gốc | tick đồng hồ nhẹ; chime đúng ×2; whoosh chuyển câu | think → point |
| S17 Outro | 5:43–6:12 | Tổng kết 3 ý + thương hiệu | 3 chip tổng kết pop lần lượt; thông điệp chính hiện kinetic nhẹ; logo + tagline kết, An vẫy tay (pose wave) | 3 ý tóm tắt; AN TECH ACADEMY | chime ×3; chime outro | present → wave |

## Kiểm soát nhịp (16.2)

- S10 và S13 có điểm dừng quan sát (gói tin dừng 0.4s ở mỗi nút; timeline dừng 0.5s mỗi giai đoạn).
- Không cảnh tĩnh quá 8s: mọi cảnh đều có phần tử chuyển động theo lời.
- Không quá 3 nhóm chuyển động đồng thời; ưu tiên tuần tự.
- Chữ màn hình là từ khóa/nhãn, KHÔNG chép nguyên lời thoại (phụ đề riêng lớp dưới).