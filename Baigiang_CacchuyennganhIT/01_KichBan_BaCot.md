# KỊCH BẢN BA CỘT — KHÁM PHÁ CÁC CHUYÊN NGÀNH CNTT

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.2 · Bản trình Cổng A · 12/11/2026*
*Nguồn nội dung: NoidungcacchuyennganhIT.docx (người dùng cung cấp). Thời lượng mục tiêu: ~7 phút (ước lượng từ số âm tiết; sẽ đo thực tế trên audio ở bước mẫu).*

## Quy ước cột

- **Cột 1 – Chữ hiển thị / phụ đề:** đúng lời người xem nghe; mỗi cue tối đa 2 dòng, mỗi dòng ≤ 42 ký tự; ngắt theo cụm nghĩa, không cắt rời thuật ngữ. Đây là nguồn để xuất file .srt (6.2).
- **Cột 2 – Chữ cho TTS:** tối ưu cách đọc, dấu câu, ngắt nghỉ; áp dụng phiên âm đề xuất của Glossary (02_Glossary_DuAn.md). Phiên âm KHÔNG bao giờ xuất hiện ở cột 1 hay trên màn hình (3.3).
- **Cột 3 – Chỉ dẫn diễn xuất:** nhãn nội bộ (4.2, 4.3), ánh xạ sang điều khiển thực của edge-tts (rate theo phân đoạn + dấu câu/ngắt câu) tại bước mẫu; không lọt vào audio/phụ đề.
- Chính sách phiên âm (đề xuất, chờ duyệt): viết tắt và tên ký hiệu → đọc tên chữ cái tiếng Anh phiên âm Việt; từ công nghệ có cách đọc tiếng Anh ổn định → phiên âm Việt hóa; chức danh nghề nghiệp tiếng Anh → giữ nguyên chính tả, kiểm tra ở voice mẫu, có phương án phiên âm dự phòng trong glossary.
- Khoảng nghỉ: `…` = nghỉ ngắn ~0,4 s; `[nghỉ 1 s]`, `[nghỉ 3 s]` = điểm dừng có chủ đích (4.4). Thời gian cảnh là ước lượng, chốt lại sau khi đo audio.
- Quy ước tổng hợp (phát hiện 12/11/2026, xem 00 mục 2b): khi đưa chữ vào edge-tts, thay `…` bằng `,` (dấu "…" gây lỗi NoAudioReceived); bỏ nhãn `[nghỉ …]` và thay bằng khoảng lặng chèn bằng ffmpeg; tổng hợp theo từng câu/cue rồi ghép. Một số chuỗi chữ gây lỗi cứng (ví dụ "Sờ" hoa, "tử,") → mỗi cue phải dùng chuỗi/biến thể đã thử OK trong bảng preflight trước khi render toàn bộ.

---

## PHẦN 1 — MỞ ĐẦU (0:00 – 0:35)

### S01 · 0:00–0:08 · Cold open (hook)
*Mục tiêu cảnh: giữ chân người xem bằng câu hỏi nghịch lý "một ứng dụng = cả đội ngũ".*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Để một ứng dụng mua sắm trực tuyến<br>đến tay bạn, cần bao nhiêu người phía sau? | Để một ứng dụng mua sắm trực tuyến đến tay bạn, cần bao nhiêu người phía sau? | Tò mò, lên giọng cuối câu hỏi; nhịp nhanh vừa |
| Không chỉ một lập trình viên đâu —<br>mà là cả một đội ngũ. | Không chỉ một lập trình viên đâu… mà là cả một đội ngũ. | Dí dỏm nhẹ ở "đâu"; nhấn "cả một đội ngũ" |
| Mỗi người một vai trò rất khác nhau. | Mỗi người một vai trò rất khác nhau. | Nhấn "rất khác nhau" |

### S02 · 0:08–0:20 · Chào + nhận diện thương hiệu
*Mục tiêu cảnh: chào sáng tạo theo chủ đề, nhắc tên An Tech Academy, nêu lợi ích video.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Xin chào các bạn!<br>Chào mừng đến với An Tech Academy — | Xin chào các bạn! Chào mừng đến với An Tech A-ca-đê-my… | Năng lượng tốt, thân thiện |
| nơi chúng ta cùng khám phá công nghệ<br>theo cách dễ hiểu và thực tế nhất. | nơi chúng ta cùng khám phá công nghệ theo cách dễ hiểu, và thực tế nhất. | Bình tĩnh, rõ ràng |
| Hôm nay, chúng ta sẽ mở tấm bản đồ<br>sáu chuyên ngành của Công nghệ thông tin, | Hôm nay, chúng ta sẽ mở tấm bản đồ sáu chuyên ngành của Công nghệ thông tin,… | Tạo mong đợi, nhấn "sáu chuyên ngành" |
| để bạn tìm ra con đường phù hợp với mình. | để bạn tìm ra con đường phù hợp với mình. | Chắc giọng, ấm áp |

### S03 · 0:20–0:35 · Mục tiêu học tập + bản đồ 6 nhóm
*Mục tiêu cảnh: nêu mục tiêu đo được (7.2) và lộ trình 6 nhóm.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Sau video này, bạn sẽ phân biệt được<br>sáu nhóm chuyên ngành, | Sau video này, bạn sẽ phân biệt được sáu nhóm chuyên ngành,… | Rõ ràng, mạch lạc |
| kể được vài vị trí nghề nghiệp tiêu biểu<br>của mỗi nhóm, | kể được vài vị trí nghề nghiệp tiêu biểu của mỗi nhóm,… | Liệt kê có nhịp |
| và tự đối chiếu sở thích của mình<br>với từng hướng đi. | và tự đối chiếu sở thích của mình với từng hướng đi. | Nhấn "tự đối chiếu" |
| Sáu nhóm đó là: Công nghệ phần mềm;<br>Khoa học dữ liệu và Trí tuệ nhân tạo; | Sáu nhóm đó là: Công nghệ phần mềm; Khoa học dữ liệu và Trí tuệ nhân tạo; | Đọc chậm vừa, tách bạch từng tên |
| An toàn thông tin; Hệ thống thông tin;<br>Mạng máy tính và Điện toán đám mây; | An toàn thông tin; Hệ thống thông tin; Mạng máy tính và Điện toán đám mây; | Giữ nhịp liệt kê |
| cùng Đồ họa máy tính và<br>Phát triển trò chơi. Bắt đầu nhé! | cùng Đồ họa máy tính và Phát triển trò chơi. [nghỉ 1 s] Bắt đầu nhé! | Tăng nhịp nhẹ, hào hứng ở câu chốt |

---

## PHẦN 2 — SÁU CHUYÊN NGÀNH (0:35 – 5:35)

### S04 · 0:35–0:47 · CNPM — định nghĩa
*Mục tiêu cảnh: định nghĩa Công nghệ phần mềm bằng chuỗi vòng đời + ví dụ sản phẩm.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Đầu tiên: Công nghệ phần mềm. | Đầu tiên: Công nghệ phần mềm. | Chuyển phần, nhấn tên chuyên ngành |
| Đây là lĩnh vực nghiên cứu, phân tích,<br>thiết kế, xây dựng, kiểm thử | Đây là lĩnh vực nghiên cứu, phân tích, thiết kế, xây dựng, kiểm thử,… | Định nghĩa: chậm ~0,95×, chắc giọng |
| và bảo trì sản phẩm phần mềm. | và bảo trì sản phẩm phần mềm. | Giữ nhịp định nghĩa |
| Nói dễ hiểu: muốn biến ý tưởng như<br>website bán hàng, ứng dụng đặt đồ ăn, | Nói dễ hiểu: muốn biến ý tưởng như oép-sai-tờ bán hàng, ứng dụng đặt đồ ăn,… | Gần gũi, tự nhiên |
| hay phần mềm quản lý sinh viên<br>thành sản phẩm chạy được, | hay phần mềm quản lý sinh viên thành sản phẩm chạy được,… | Nhấn "chạy được" |
| bạn cần Công nghệ phần mềm. | bạn cần Công nghệ phần mềm. | Chắc giọng |

### S05 · 0:47–1:02 · CNPM — ba hướng lập trình
*Mục tiêu cảnh: phân biệt Frontend / Backend / Full-stack kèm công nghệ đúng phân loại.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Trong đó có ba hướng lập trình phổ biến. | Trong đó có ba hướng lập trình phổ biến. | Dẫn nhập, nhấn "ba hướng" |
| Frontend Developer xây dựng giao diện<br>người dùng trực tiếp nhìn thấy, | Frontend Developer xây dựng giao diện người dùng trực tiếp nhìn thấy,… | Giải thích bình tĩnh |
| với HTML, CSS, JavaScript<br>và thư viện React. | với Ếch Ti Em En, Si Ét Ét, Gia-vơ Sờ-críp, và thư viện Ri-ác. | Thuật ngữ: chậm ~0,95×, tách bạch |
| Backend Developer xử lý nghiệp vụ<br>phía máy chủ: đăng nhập, đơn hàng, | Backend Developer xử lý nghiệp vụ phía máy chủ: đăng nhập, đơn hàng,… | Liệt kê có nhịp, rõ ràng |
| thanh toán, kết nối cơ sở dữ liệu;<br>công nghệ thường gặp là Node.js, Java, | thanh toán, kết nối cơ sở dữ liệu;… công nghệ thường gặp là Nâu-đờ chấm Giây Ét, Gia-vơ,… | Tiếp nhịp liệt kê |
| PHP, Python và C#. | Pi Ếch Pi, Pai-thơn, và Si Sáp. | Thuật ngữ: chậm, tách bạch |
| Full-stack Developer làm được cả hai phía. | Full-stack Developer làm được cả hai phía. | Nhấn "cả hai phía" |

### S06 · 1:02–1:14 · CNPM — Tester & QA
*Mục tiêu cảnh: vai trò kiểm thử; vì sao chất lượng quan trọng.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Bên cạnh lập trình viên còn có<br>Software Tester và QA Engineer — | Bên cạnh lập trình viên còn có Software Tester và Kiu Ây Engineer… | Giới thiệu vai trò mới |
| người kiểm thử, săn lỗi và giữ chất lượng<br>phần mềm trước khi đến tay người dùng. | người kiểm thử, săn lỗi, và giữ chất lượng phần mềm trước khi đến tay người dùng. | Nhấn "săn lỗi", dí dỏm nhẹ |
| Sản phẩm tốt không chỉ chạy được,<br>mà còn phải chạy đúng. | Sản phẩm tốt không chỉ chạy được… mà còn phải chạy đúng. | Nhấn đối lập "chạy được / chạy đúng"; nghỉ ngắn |
| Một lỗi nhỏ lọt ra ngoài<br>cũng có thể làm hỏng trải nghiệm | Một lỗi nhỏ lọt ra ngoài cũng có thể làm hỏng trải nghiệm… | Cảnh báo nhẹ |
| của hàng nghìn người dùng. | của hàng nghìn người dùng. | Chắc giọng |

### S07 · 1:14–1:25 · CNPM — hợp với ai
*Mục tiêu cảnh: đối chiếu sở thích người học với chuyên ngành.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Nhóm này hợp với bạn nếu bạn thích<br>lập trình, tư duy logic | Nhóm này hợp với bạn nếu bạn thích lập trình, tư duy logic,… | Gần gũi, tâm tình |
| và muốn tự tay làm ra sản phẩm công nghệ<br>dùng được trong thực tế. | và muốn tự tay làm ra sản phẩm công nghệ dùng được trong thực tế. [nghỉ 1 s] | Nhấn "tự tay"; nghỉ chuyển cảnh |

### S08 · 1:25–1:37 · KHDL&AI — dữ liệu ở khắp nơi
*Mục tiêu cảnh: dữ liệu thô ≠ giá trị; cần phân tích.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Chuyên ngành thứ hai: Khoa học dữ liệu<br>và Trí tuệ nhân tạo. | Chuyên ngành thứ hai: Khoa học dữ liệu, và Trí tuệ nhân tạo. | Chuyển phần, nhấn tên |
| Mỗi lần bạn tìm kiếm trên Google,<br>xem video trên YouTube hay mua hàng | Mỗi lần bạn tìm kiếm trên Gu-gồ, xem video trên Du-túp, hay mua hàng… | Ví dụ đời thường, nhịp nhanh vừa |
| trực tuyến, hệ thống đều ghi nhận dữ liệu. | trực tuyến, hệ thống đều ghi nhận dữ liệu. | Giữ nhịp |
| Nhưng dữ liệu thô chưa tự có giá trị — | Nhưng dữ liệu thô chưa tự có giá trị… | Nhấn "chưa tự", nghỉ ngắn |
| phải phân tích, xử lý và khai thác nó. | phải phân tích, xử lý, và khai thác nó. | Chắc giọng |

### S09 · 1:37–1:50 · KHDL&AI — phân biệt DS và AI
*Mục tiêu cảnh: phân biệt hai khái niệm, không đồng nhất.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Khoa học dữ liệu dùng thống kê, lập trình<br>và thuật toán | Khoa học dữ liệu dùng thống kê, lập trình và thuật toán,… | Định nghĩa: chậm, rõ |
| để tìm xu hướng, quy luật<br>và thông tin hữu ích từ dữ liệu. | để tìm xu hướng, quy luật, và thông tin hữu ích từ dữ liệu. | Nhấn "xu hướng, quy luật" |
| Trí tuệ nhân tạo đi xa hơn:<br>xây dựng hệ thống biết học từ dữ liệu | Trí tuệ nhân tạo đi xa hơn: xây dựng hệ thống biết học từ dữ liệu,… | Tạo mong đợi |
| để thực hiện những nhiệm vụ thông minh. | để thực hiện những nhiệm vụ thông minh. | Chắc giọng |
| Khoa học dữ liệu thiên về<br>phân tích và giải thích; | Khoa học dữ liệu thiên về phân tích và giải thích;… | Đối chiếu, tách bạch |
| AI thiên về dạy máy tự học<br>để thực hiện nhiệm vụ. | Ây Ai thiên về dạy máy tự học để thực hiện nhiệm vụ. | Nhấn "tự học" |

### S10 · 1:50–2:03 · KHDL&AI — ví dụ hệ thống gợi ý
*Mục tiêu cảnh: luồng dữ liệu thật: lịch sử → mô hình → gợi ý.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Ví dụ: bạn vừa xem một chiếc điện thoại<br>trên trang thương mại điện tử, | Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử,… | Gần gũi, kể chuyện |
| hệ thống phân tích lịch sử<br>tìm kiếm và mua hàng, | hệ thống phân tích lịch sử tìm kiếm và mua hàng,… | Nhấn "lịch sử" |
| để gợi ý những sản phẩm hợp sở thích bạn. | để gợi ý những sản phẩm hợp sở thích bạn. | Nhấn "hợp sở thích bạn" |
| Đó chính là hệ thống gợi ý sản phẩm —<br>một ứng dụng rất đời thường của AI. | Đó chính là hệ thống gợi ý sản phẩm… một ứng dụng rất đời thường của Ây Ai. | Kết luận chắc giọng, dí dỏm nhẹ |

### S11 · 2:03–2:15 · KHDL&AI — công nghệ, nghề nghiệp, hợp với ai
*Mục tiêu cảnh: gọi tên stack và vị trí nghề nghiệp đúng phân loại.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Công nghệ thường gặp: Python, SQL, Pandas,<br>Scikit-learn, TensorFlow và PyTorch. | Công nghệ thường gặp: Pai-thơn, Ét Kiu En, Pan-đợz, Sai-kit Lơn, Ten-sơ-phờ-lâu, và Pai Thoóc. | Thuật ngữ: chậm ~0,95×, tách bạch |
| Vị trí nghề nghiệp: Data Analyst,<br>Data Scientist, | Vị trí nghề nghiệp: Data Analyst, Data Scientist,… | Liệt kê rõ nhịp |
| Machine Learning Engineer, AI Engineer. | Machine Learning Engineer, Ây Ai Engineer. | Giữ nhịp liệt kê |
| Hợp với bạn nếu bạn thích toán, thống kê<br>và tò mò cách máy tính học hỏi, dự đoán. | Hợp với bạn nếu bạn thích toán, thống kê, và tò mò cách máy tính học hỏi, dự đoán. [nghỉ 1 s] | Tâm tình; nhấn "học hỏi, dự đoán"; nghỉ chuyển cảnh |

### S12 · 2:15–2:27 · ATTT — đặt vấn đề
*Mục tiêu cảnh: hậu quả mất an toàn thông tin → nhu cầu bảo vệ.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Thứ ba: An toàn thông tin. | Thứ ba: An toàn thông tin. | Chuyển phần, nhấn tên |
| Thử tưởng tượng tài khoản ngân hàng<br>bị đánh cắp, | Thử tưởng tượng tài khoản ngân hàng bị đánh cắp,… | Nghiêm túc, nhấn từng viễn cảnh |
| thông tin khách hàng bị rò rỉ,<br>hay hệ thống máy chủ bị tấn công — | thông tin khách hàng bị rò rỉ, hay hệ thống máy chủ bị tấn công… | Giữ nhịp nghiêm túc |
| hậu quả sẽ nghiêm trọng thế nào? | hậu quả sẽ nghiêm trọng thế nào? | Lên giọng câu hỏi; nghỉ ngắn |
| An toàn thông tin hướng đến giải quyết<br>chính những vấn đề đó. | An toàn thông tin hướng đến giải quyết chính những vấn đề đó. | Chắc giọng |

### S13 · 2:27–2:40 · ATTT — công việc thực tế
*Mục tiêu cảnh: vòng việc bảo mật + ví dụ pentest có ủy quyền.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Người làm bảo mật tìm lỗ hổng,<br>kiểm tra sức phòng thủ của hệ thống, | Người làm bảo mật tìm lỗ hổng, kiểm tra sức phòng thủ của hệ thống,… | Giải thích bình tĩnh |
| giám sát hoạt động đáng ngờ<br>và xây giải pháp ngăn tấn công. | giám sát hoạt động đáng ngờ, và xây giải pháp ngăn tấn công. | Nhấn "ngăn tấn công" |
| Ví dụ, chuyên gia kiểm thử xâm nhập<br>có thể được doanh nghiệp giao | Ví dụ, chuyên gia kiểm thử xâm nhập có thể được doanh nghiệp giao,… | Kể chuyện, rõ ràng |
| dò tìm điểm yếu của website<br>trước khi hacker kịp khai thác. | dò tìm điểm yếu của oép-sai-tờ trước khi hacker kịp khai thác. | Nhấn "trước khi" |
| Họ cũng diễn tập ứng phó sự cố<br>để doanh nghiệp không bị động | Họ cũng diễn tập ứng phó sự cố, để doanh nghiệp không bị động… | Bổ sung |
| khi tấn công thật xảy ra. | khi tấn công thật xảy ra. | Chắc giọng |

### S14 · 2:40–2:52 · ATTT — nguyên tắc ủy quyền
*Mục tiêu cảnh: nhấn ranh giới pháp lý/đạo đức của kiểm thử xâm nhập (7.4).*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Một nguyên tắc bắt buộc:<br>mọi hoạt động kiểm thử xâm nhập | Một nguyên tắc bắt buộc: mọi hoạt động kiểm thử xâm nhập,… | Cảnh báo: nhấn rõ mức độ quan trọng |
| chỉ được thực hiện trong phạm vi<br>được cho phép. | chỉ được thực hiện trong phạm vi được cho phép. | Chậm, chắc, nhấn "được cho phép" |
| Bảo mật là bảo vệ hệ thống,<br>không phải tấn công tùy tiện. | Bảo mật là bảo vệ hệ thống… không phải tấn công tùy tiện. | Đối lập rõ; nghỉ ngắn |

### S15 · 2:52–3:05 · ATTT — nghề nghiệp, kiến thức, hợp với ai
*Mục tiêu cảnh: gọi tên vị trí và kiến thức nền.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Vị trí phổ biến: Security Analyst,<br>Penetration Tester, Security Engineer. | Vị trí phổ biến: Security Analyst, Penetration Tester, Security Engineer. | Liệt kê rõ nhịp |
| Kiến thức nền: mạng máy tính,<br>hệ điều hành, Linux, mã hóa dữ liệu | Kiến thức nền: mạng máy tính, hệ điều hành, Li-nợks, mã hóa dữ liệu,… | Thuật ngữ chậm, tách bạch |
| và bảo mật ứng dụng. | và bảo mật ứng dụng. | Giữ nhịp |
| Hợp với bạn nếu bạn cẩn thận,<br>thích khám phá | Hợp với bạn nếu bạn cẩn thận, thích khám phá,… | Gần gũi |
| và muốn bảo vệ các hệ thống công nghệ. | và muốn bảo vệ các hệ thống công nghệ. [nghỉ 1 s] | Nhấn "bảo vệ"; nghỉ chuyển cảnh |

### S16 · 3:05–3:17 · HTTT — định nghĩa
*Mục tiêu cảnh: HTTT = công nghệ + dữ liệu + quản lý; khác CNPM ở trọng tâm.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Thứ tư: Hệ thống thông tin —<br>lĩnh vực kết hợp công nghệ, dữ liệu | Thứ tư: Hệ thống thông tin… lĩnh vực kết hợp công nghệ, dữ liệu,… | Chuyển phần, nhấn tên |
| và hoạt động quản lý của doanh nghiệp. | và hoạt động quản lý của doanh nghiệp. | Rõ ràng |
| Khác với việc tập trung viết code<br>để tạo sản phẩm, | Khác với việc tập trung viết code để tạo sản phẩm,… | Đối chiếu, nghỉ ngắn |
| ở đây công nghệ được dùng để giải<br>các bài toán quản lý và vận hành thực tế. | ở đây công nghệ được dùng để giải các bài toán quản lý và vận hành thực tế. | Nhấn "quản lý và vận hành" |

### S17 · 3:17–3:30 · HTTT — ví dụ nhân sự + Business Analyst
*Mục tiêu cảnh: luồng quy trình nghiệp vụ → tài liệu → đội phát triển.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Ví dụ: một công ty muốn xây<br>hệ thống quản lý nhân sự. | Ví dụ: một công ty muốn xây hệ thống quản lý nhân sự. | Kể chuyện, gần gũi |
| Trước khi lập trình, phải tìm hiểu<br>quy trình tuyển dụng, chấm công, | Trước khi lập trình, phải tìm hiểu quy trình tuyển dụng, chấm công,… | Liệt kê chậm vừa, tách bạch |
| tính lương, phân quyền và quản lý hồ sơ. | tính lương, phân quyền, và quản lý hồ sơ. | Giữ nhịp liệt kê |
| Người phân tích và chuyển các yêu cầu đó<br>thành tài liệu cho đội phát triển | Người phân tích và chuyển các yêu cầu đó thành tài liệu cho đội phát triển,… | Nhấn "chuyển thành tài liệu" |
| chính là Business Analyst —<br>chuyên viên phân tích nghiệp vụ. | chính là Business Analyst… chuyên viên phân tích nghiệp vụ. | Định nghĩa chắc giọng |

### S18 · 3:30–3:42 · HTTT — vai trò khác + kiến thức
*Mục tiêu cảnh: mở rộng vị trí nghề nghiệp và bộ kiến thức nền.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Ngoài ra còn có System Analyst,<br>Database Administrator | Ngoài ra còn có System Analyst, Database Administrator,… | Liệt kê rõ nhịp |
| và chuyên viên triển khai hệ thống ERP. | và chuyên viên triển khai hệ thống I A Pi. | Viết tắt: tách chữ cái |
| Kiến thức quan trọng gồm SQL,<br>cơ sở dữ liệu, UML, BPMN, | Kiến thức quan trọng gồm Ét Kiu En, cơ sở dữ liệu, Du Em En, Bi Pi Em En,… | Viết tắt: chậm, tách bạch |
| phân tích nghiệp vụ và thiết kế hệ thống. | phân tích nghiệp vụ, và thiết kế hệ thống. | Chắc giọng |

### S19 · 3:42–3:55 · HTTT — hợp với ai
*Mục tiêu cảnh: đối chiếu sở thích phân tích / cầu nối.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Hợp với bạn nếu bạn thích<br>phân tích vấn đề, | Hợp với bạn nếu bạn thích phân tích vấn đề,… | Tâm tình |
| tìm hiểu cách doanh nghiệp vận hành,<br>và làm cầu nối giữa người sử dụng | tìm hiểu cách doanh nghiệp vận hành, và làm cầu nối giữa người sử dụng,… | Nhấn "cầu nối" |
| với đội ngũ lập trình. | với đội ngũ lập trình. [nghỉ 1 s] | Nghỉ chuyển cảnh |

### S20 · 3:55–4:07 · Mạng & Cloud — đặt vấn đề
*Mục tiêu cảnh: bài toán kết nối quy mô lớn → vai trò người làm mạng.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Thứ năm: Mạng máy tính<br>và Điện toán đám mây. | Thứ năm: Mạng máy tính, và Điện toán đám mây. | Chuyển phần, nhấn tên |
| Một trường đại học với hàng nghìn<br>máy tính, hệ thống Wi-Fi, máy chủ | Một trường đại học với hàng nghìn máy tính, hệ thống Oai Fai, máy chủ,… | Nhấn quy mô "hàng nghìn" |
| và phần mềm quản lý — làm sao tất cả<br>kết nối, trao đổi dữ liệu và chạy ổn định? | và phần mềm quản lý… làm sao tất cả kết nối, trao đổi dữ liệu, và chạy ổn định? | Lên giọng câu hỏi |
| Đó là nhiệm vụ của người làm mạng. | Đó là nhiệm vụ của người làm mạng. | Chắc giọng |

### S21 · 4:07–4:20 · Mạng & Cloud — công việc + kiến thức
*Mục tiêu cảnh: phạm vi công việc quản trị hạ tầng.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Họ thiết kế, cấu hình, triển khai<br>và bảo trì mạng nội bộ, máy chủ | Họ thiết kế, cấu hình, triển khai, và bảo trì mạng nội bộ, máy chủ,… | Liệt kê có nhịp |
| và thiết bị kết nối. | và thiết bị kết nối. | Giữ nhịp |
| Kiến thức nền gồm TCP/IP, DNS, DHCP,<br>Linux, Windows Server, ảo hóa | Kiến thức nền gồm Ti Si Pi trên Ai Pi, Đi En Ét, Đi Ây Si Pi, Li-nợks, Win-đâu-zơ Sơ-vờ, ảo hóa,… | Giao thức: chậm ~0,9×, tách bạch |
| và quản trị hệ thống. | và quản trị hệ thống. | Chắc giọng |

### S22 · 4:20–4:33 · Mạng & Cloud — điện toán đám mây
*Mục tiêu cảnh: khác biệt thuê tài nguyên vs tự mua máy chủ; lợi ích.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Ngày nay, thay vì tự đầu tư<br>toàn bộ máy chủ vật lý, | Ngày nay, thay vì tự đầu tư toàn bộ máy chủ vật lý,… | Đối chiếu, nghỉ ngắn |
| doanh nghiệp có thể dùng tài nguyên<br>điện toán từ các nền tảng đám mây | doanh nghiệp có thể dùng tài nguyên điện toán từ các nền tảng đám mây,… | Nhấn "đám mây" |
| như Amazon Web Services, Microsoft Azure<br>hay Google Cloud — | như A-ma-dơn Oép Sơ-vi-xìz, Mai-crơ-sóft Æ-dờ, hay Gu-gồ Clau-đờ… | Tên riêng: chậm, tách bạch |
| linh hoạt hơn và trả theo mức sử dụng. | linh hoạt hơn, và trả theo mức sử dụng. | Nhấn lợi ích |
| Đám mây cũng giúp đội ngũ kỹ thuật mở rộng<br>hệ thống trong vài phút | Đám mây cũng giúp đội ngũ kỹ thuật mở rộng hệ thống trong vài phút,… | Nhấn "vài phút" |
| thay vì vài tuần mua sắm phần cứng. | thay vì vài tuần mua sắm phần cứng. | Đối lập "phút / tuần" |

### S23 · 4:33–4:45 · Mạng & Cloud — nghề nghiệp + hợp với ai
*Mục tiêu cảnh: vị trí nghề nghiệp và đối chiếu sở thích hạ tầng.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Vị trí nghề nghiệp: Network Engineer,<br>System Administrator, Cloud Engineer | Vị trí nghề nghiệp: Network Engineer, System Administrator, Cloud Engineer,… | Liệt kê rõ nhịp |
| và IT Support. | và Ai Ti Support. | Giữ nhịp |
| Hợp với bạn nếu bạn thích tìm hiểu<br>cách Internet vận hành, | Hợp với bạn nếu bạn thích tìm hiểu cách In-tơ-nét vận hành,… | Gần gũi |
| cách máy chủ hoạt động<br>và cách các thiết bị kết nối với nhau. | cách máy chủ hoạt động, và cách các thiết bị kết nối với nhau. [nghỉ 1 s] | Nhấn "kết nối"; nghỉ chuyển cảnh |

### S24 · 4:45–4:57 · Đồ họa & Game — hook
*Mục tiêu cảnh: kết nối trải nghiệm chơi game với đội ngũ phía sau.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Cuối cùng: Đồ họa máy tính<br>và Phát triển trò chơi điện tử — | Cuối cùng: Đồ họa máy tính, và Phát triển trò chơi điện tử… | Chuyển phần, nhấn tên |
| nơi lập trình gặp mỹ thuật, sáng tạo<br>và công nghệ mô phỏng. | nơi lập trình gặp mỹ thuật, sáng tạo, và công nghệ mô phỏng. | Hào hứng vừa phải |
| Bạn từng chơi những trò chơi có nhân vật<br>chuyển động chân thực, | Bạn từng chơi những trò chơi có nhân vật chuyển động chân thực,… | Câu hỏi gợi hình ảnh |
| môi trường ba chiều sống động? | môi trường ba chiều sống động? | Lên giọng câu hỏi |
| Đằng sau là cả đội ngũ lập trình viên<br>và chuyên viên đồ họa. | Đằng sau là cả đội ngũ lập trình viên, và chuyên viên đồ họa. | Nhấn "cả đội ngũ" |

### S25 · 4:57–5:10 · Đồ họa & Game — sản phẩm
*Mục tiêu cảnh: phổ sản phẩm của lĩnh vực.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Người làm lĩnh vực này phát triển<br>trò chơi điện tử, mô hình 3D, hoạt hình, | Người làm lĩnh vực này phát triển trò chơi điện tử, mô hình Ba Đê, hoạt hình,… | Liệt kê có nhịp |
| mô phỏng kỹ thuật và các ứng dụng<br>thực tế ảo — | mô phỏng kỹ thuật, và các ứng dụng thực tế ảo… | Nhấn "thực tế ảo" |
| vừa cần code, vừa cần mắt thẩm mỹ. | vừa cần code, vừa cần mắt thẩm mỹ. | Nhấn đối lập "code / thẩm mỹ" |

### S26 · 5:10–5:22 · Đồ họa & Game — công nghệ + nghề nghiệp
*Mục tiêu cảnh: engine, ngôn ngữ, công cụ đúng phân loại.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Công nghệ phổ biến gồm Unity,<br>Unreal Engine, C#, C++, Blender | Công nghệ phổ biến gồm Du-nơ-ti, Ăn-riêu En-gin, Si Sáp, Si Plớt Plớt, Blen-đờ,… | Thuật ngữ: chậm ~0,95×, tách bạch |
| và các công cụ thiết kế đồ họa. | và các công cụ thiết kế đồ họa. | Giữ nhịp |
| Vị trí nghề nghiệp: Game Developer,<br>Game Designer, 3D Artist | Vị trí nghề nghiệp: Game Developer, Game Designer, Ba Đê Artist,… | Liệt kê rõ nhịp |
| và Graphics Programmer. | và Graphics Programmer. | Giữ nhịp |

### S27 · 5:22–5:35 · Đồ họa & Game — hợp với ai
*Mục tiêu cảnh: đối chiếu sở thích sáng tạo + kỹ thuật.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Hợp với bạn nếu bạn vừa mê công nghệ,<br>vừa thích thiết kế hình ảnh | Hợp với bạn nếu bạn vừa mê công nghệ, vừa thích thiết kế hình ảnh,… | Gần gũi, hào hứng |
| và trò chơi điện tử. | và trò chơi điện tử. | Giữ nhịp |
| Sáng tạo ở đây không chỉ là vẽ đẹp —<br>mà còn làm cho thế giới ảo | Sáng tạo ở đây không chỉ là vẽ đẹp… mà còn làm cho thế giới ảo… | Nghỉ ngắn, tạo mong đợi |
| chuyển động đúng và mượt. | chuyển động đúng, và mượt. [nghỉ 1 s] | Nhấn "đúng và mượt"; nghỉ chuyển phần |

---

## PHẦN 3 — CHỌN CHUYÊN NGÀNH (5:35 – 6:25)

### S28 · 5:35–5:47 · Không có "tốt nhất"
*Mục tiêu cảnh: phá ngộ nhận "chuyên ngành hot nhất".*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Vậy đâu là chuyên ngành tốt nhất? | Vậy đâu là chuyên ngành tốt nhất? | Câu hỏi, lên giọng, nghỉ ngắn |
| Câu trả lời: không có chuyên ngành nào<br>tốt nhất cho tất cả mọi người. | Câu trả lời: không có chuyên ngành nào tốt nhất cho tất cả mọi người. | Chắc giọng, nhấn "không có" |
| Mỗi lĩnh vực có yêu cầu, đặc điểm<br>và cơ hội phát triển riêng. | Mỗi lĩnh vực có yêu cầu, đặc điểm, và cơ hội phát triển riêng. | Rõ ràng |
| Điều đáng chọn là chuyên ngành<br>phù hợp với bạn, | Điều đáng chọn là chuyên ngành phù hợp với bạn… | Nhấn "phù hợp với bạn" |
| không phải chuyên ngành "hot" nhất. | không phải chuyên ngành "hot" nhất. | Dí dỏm nhẹ ở "hot" |

### S29 · 5:47–6:05 · Bản đồ sở thích → chuyên ngành
*Mục tiêu cảnh: ghép nhanh sở thích với 6 nhóm (củng cố).*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Thích lập trình, xây ứng dụng?<br>Công nghệ phần mềm. | Thích lập trình, xây ứng dụng? Công nghệ phần mềm. | Hỏi–đáp nhanh, linh hoạt |
| Mê phân tích dữ liệu và AI?<br>Khoa học dữ liệu. | Mê phân tích dữ liệu và Ây Ai? Khoa học dữ liệu. | Giữ nhịp hỏi–đáp |
| Quan tâm bảo mật, phòng chống tấn công?<br>An toàn thông tin. | Quan tâm bảo mật, phòng chống tấn công? An toàn thông tin. | Giữ nhịp |
| Thích quy trình và bài toán quản lý?<br>Hệ thống thông tin. | Thích quy trình và bài toán quản lý? Hệ thống thông tin. | Giữ nhịp |
| Mê hạ tầng, máy chủ, kết nối mạng?<br>Mạng và đám mây. | Mê hạ tầng, máy chủ, kết nối mạng? Mạng và đám mây. | Giữ nhịp |
| Còn đam mê hình ảnh, thiết kế, trò chơi?<br>Đồ họa và game. | Còn đam mê hình ảnh, thiết kế, trò chơi? Đồ họa và game. | Chốt nhịp, hào hứng |

### S30 · 6:05–6:15 · Câu hỏi tự kiểm tra + điểm dừng
*Mục tiêu cảnh: người học tự đối chiếu (7.2); có 3 giây dừng thật trên video.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Bây giờ, dừng lại ba giây và tự hỏi: | Bây giờ, dừng lại ba giây và tự hỏi:… | Chậm lại, mời gọi |
| mình thích tạo ra sản phẩm,<br>phân tích dữ liệu, hay bảo vệ hệ thống? | mình thích tạo ra sản phẩm, phân tích dữ liệu, hay bảo vệ hệ thống? | Lên giọng lựa chọn; [nghỉ 3 s] sau câu |
| Câu trả lời chính là manh mối<br>đầu tiên của bạn. | [nghỉ 3 s] Câu trả lời chính là manh mối đầu tiên của bạn. | Ấm áp, chắc giọng |

### S31 · 6:15–6:25 · Lời khuyên: đừng chọn vì lương
*Mục tiêu cảnh: khuyến khích thực hành trước khi quyết định.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Và một lời khuyên quan trọng:<br>đừng chọn chuyên ngành chỉ vì nghe nói | Và một lời khuyên quan trọng: đừng chọn chuyên ngành chỉ vì nghe nói… | Cảnh báo nhẹ, nhấn "đừng" |
| lĩnh vực đó lương cao. | lĩnh vực đó lương cao. | Giữ nhịp cảnh báo |
| Hãy tìm hiểu bản chất công việc,<br>thử thực hành một dự án nhỏ, | Hãy tìm hiểu bản chất công việc, thử thực hành một dự án nhỏ,… | Khuyến khích, rõ ràng |
| rồi tự đánh giá xem mình<br>có thực sự phù hợp. | rồi tự đánh giá xem mình có thực sự phù hợp. [nghỉ 1 s] | Nhấn "thực sự phù hợp" |

---

## PHẦN 4 — TỔNG KẾT & OUTRO (6:25 – 7:00)

### S32 · 6:25–6:40 · Ba hành trang
*Mục tiêu cảnh: tóm tắt 3 kiến thức cốt lõi (1.4).*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Tóm lại, Công nghệ thông tin<br>là một thế giới rộng lớn, | Tóm lại, Công nghệ thông tin là một thế giới rộng lớn,… | Tổng kết: chắc, cô đọng |
| mỗi chuyên ngành một vai trò quan trọng. | mỗi chuyên ngành một vai trò quan trọng. | Giữ nhịp tổng kết |
| Dù chọn con đường nào,<br>hãy nhớ ba hành trang: | Dù chọn con đường nào, hãy nhớ ba hành trang:… | Nhấn "ba hành trang", nghỉ ngắn |
| nền tảng kiến thức vững chắc,<br>khả năng thực hành, | nền tảng kiến thức vững chắc, khả năng thực hành,… | Liệt kê chậm, nhấn từng ý |
| và tinh thần học hỏi không ngừng. | và tinh thần học hỏi không ngừng. | Giữ nhịp |
| Công nghệ có thể đổi thay từng ngày,<br>nhưng tư duy và cách học mới là hành trang | Công nghệ có thể đổi thay từng ngày,… nhưng tư duy và cách học mới là hành trang… | Nghỉ ngắn trước đối lập |
| đi cùng bạn lâu dài. | đi cùng bạn lâu dài. | Truyền cảm hứng, chắc giọng |

### S33 · 6:40–6:50 · Câu hỏi gợi mở + khuyến khích thực hành
*Mục tiêu cảnh: một câu hỏi mở + hành động nhỏ khả thi (1.4).*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Bạn đang nghiêng về chuyên ngành nào? | Bạn đang nghiêng về chuyên ngành nào? | Câu hỏi mở, thân thiện |
| Hãy để lại câu trả lời,<br>và thử một dự án nhỏ đầu tiên | Hãy để lại câu trả lời, và thử một dự án nhỏ đầu tiên… | Khuyến khích |
| ngay tuần này nhé. | ngay tuần này nhé. | Dí dỏm nhẹ |

### S34 · 6:50–7:00 · Outro thương hiệu
*Mục tiêu cảnh: cảm ơn, nhắc thương hiệu, mời theo dõi bài tiếp theo.*

| Chữ hiển thị / phụ đề | Chữ cho TTS | Chỉ dẫn diễn xuất |
| --- | --- | --- |
| Cảm ơn bạn đã theo dõi bài giảng hôm nay. | Cảm ơn bạn đã theo dõi bài giảng hôm nay. | Ấm áp, biết ơn |
| Đừng quên theo dõi An Tech Academy<br>để cùng khám phá thêm nhiều kiến thức | Đừng quên theo dõi An Tech A-ca-đê-my để cùng khám phá thêm nhiều kiến thức… | Nhấn tên thương hiệu |
| công nghệ hữu ích. | công nghệ hữu ích. | Giữ nhịp |
| Xin chào và hẹn gặp lại<br>trong những bài học tiếp theo! | Xin chào, và hẹn gặp lại trong những bài học tiếp theo! | Tươi, dứt khoát |

---

## Ghi chú sản xuất kèm kịch bản

- **Ước lượng thời lượng:** ~1.710 âm tiết lời thoại; ở nhịp 4,5–4,8 âm tiết/giây (đã gồm tốc độ 1,05–1,1× phần dẫn và 0,9–0,95× phần định nghĩa) cộng ~26 s khoảng nghỉ có chủ đích → khoảng 6:30–6:55. Con số chính xác chỉ chốt sau khi đo audio thật ở bước mẫu (0.4).
- **Thay đổi có chủ đích so với docx gốc (trình duyệt ở Cổng A):** (1) intro rút từ 55 s còn ~35 s gồm cold open 8 s + chào 12 s + mục tiêu 15 s theo 1.3; (2) thêm mục tiêu học tập đo được ở S03 và câu hỏi tự kiểm tra có điểm dừng 3 s ở S30 theo 7.2; (3) tách ý "pentest phải được cho phép" thành cảnh nhấn mạnh S14 theo 7.4; (4) phân loại chính xác: React là thư viện, Node.js là runtime (ghi ở glossary/storyboard), không gọi chung là "ngôn ngữ"; (5) lời chào viết lại sáng tạo theo chủ đề theo 1.3, giữ tinh thần nội dung gốc; (6) một vài câu rút gọn cho vừa khổ phụ đề 2 dòng × 42 ký tự (6.2), không đổi ý.
- **Không có số liệu/benchmark tự đặt:** mọi ví dụ là minh họa định tính; không nêu mức lương cụ thể (7.3).
- **An toàn demo:** video không demo code thật; không hiển thị khóa/mật khẩu/dữ liệu thật; cảnh pentest chỉ mô tả khái niệm và nhấn phạm vi được cho phép (7.4).