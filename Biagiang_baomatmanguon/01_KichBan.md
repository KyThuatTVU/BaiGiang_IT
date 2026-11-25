# KỊCH BẢN — CỔNG A

> 24 cue / 12 cảnh. Thoại dưới đây là **bản đọc** (đã bỏ phiên âm thay thế; xem `02_Glossary.md`).
> Rate: tốc độ tương đối của edge-tts. Pause: khoảng lặng sau câu (giây) cộng thêm 0,3 s gap chuẩn.

## Cách kể chuyện

- Xưng "mình" – gọi "các bạn", giọng vui, có câu đố và phép so sánh đời thường (rèm che cửa kính, nhật ký ở quán cà phê).
- Mỗi cảnh mở bằng một câu dẫn ngắn, chốt bằng một câu "đắt" để nhớ.
- Không đọc code theo kiểu chính tả: đọc ý nghĩa của dòng lệnh, chỉ nhắc đúng tên lệnh.
- Quiz ở cảnh 11 có khoảng "Suy nghĩ hai giây…" để người học kịp chọn.

---

## S01 — Hook: "bộ đồ lòng" của website

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S01c1 | +8% | 0,20 | Xin chào các bạn! Chào mừng quay lại với An Tech Academy — học công nghệ cùng An. Hôm nay mình có một câu đố nhỏ dành cho bạn. |
| S01c2 | +10% | 0,25 | Chỉ cần gõ thêm vài chữ vào thanh địa chỉ, bạn có thể nhìn thấy nguyên bộ đồ lòng của một website. Nghe như ảo thuật, nhưng đây là chuyện thật. |
| S01c3 | +6% | 0,30 | Thủ phạm là một lỗi cấu hình rất phổ biến: để lộ mã nguồn và cấu trúc thư mục. Hôm nay, chúng ta sẽ chặn nó bằng ba vũ khí: Apache, tệp htaccess và mô hình Front Controller. |

Sắc thái: câu 2 nhanh – tò mò; câu 3 chậm lại, xuống giọng ở "ba vũ khí".

## S02 — DevTools nhìn thấy gì?

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S02c1 | +8% | 0,20 | Đầu tiên, hãy mở mắt của trình duyệt. Nhấn F12, hoặc tổ hợp Ctrl Shift I, các bạn sẽ gặp DevTools — công cụ có sẵn trong Chrome, Edge và Firefox. |
| S02c2 | +6% | 0,35 | Mở tab Network, bạn thấy mọi tệp trình duyệt tải về, cả những phản hồi API. Nguyên tắc vàng là: thứ gì đã gửi xuống trình duyệt, thì người dùng đều xem được. Ẩn JavaScript bằng vài dòng lệnh khác gì lấy rèm che cửa kính — mà rèm lại trong suốt. |

Sắc thái: câu chốt "rèm lại trong suốt" nhấn mạnh, hơi châm biếm nhẹ.

## S03 — Rủi ro thật: máy chủ lộ thư mục

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S03c1 | +7% | 0,25 | Nhưng phần nghiêm trọng nằm ở máy chủ. PHP chạy trên server, người dùng chỉ nhận HTML hoặc JSON, không thấy code. Vấn đề là cấu trúc thư mục vẫn có thể bị lộ nếu cấu hình sai. |
| S03c2 | +6% | 0,25 | Thử gõ thẳng đường dẫn tới thư mục config, hoặc tệp BookingService.php. Nếu cấu hình sai, bạn có thể thấy danh sách tệp, tải cả file cấu hình và file SQL chứa cơ sở dữ liệu. |
| S03c3 | +8% | 0,30 | Hệ quả là lộ mã nguồn, lộ cấu hình, lộ dữ liệu, rồi thành bàn đạp cho kẻ tấn công. Không phải thấy tên thư mục là hack được ngay, nhưng để lộ tài nguyên nhạy cảm là rủi ro phải dẹp. |

Sắc thái: đây là đoạn "căng" nhất — giọng trầm hơn, câu cuối dứt khoát.

## S04 — Apache và tệp .htaccess

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S04c1 | +7% | 0,20 | Vậy ai là người gác cửa? Chính là Apache — máy chủ web mã nguồn mở: nhận yêu cầu HTTP, xác định tài nguyên rồi trả phản hồi. Apache phục vụ tệp tĩnh và phối hợp với PHP để chạy ứng dụng. |
| S04c2 | +5% | 0,30 | Vũ khí nhỏ mà quyền lực là tệp htaccess. Đặt ngay trong thư mục cần bảo vệ, nó đổi luật ở cấp thư mục mà không cần sờ cấu hình tổng. Nhưng nhớ: máy chủ phải bật AllowOverride và mod rewrite. |

Sắc thái: câu hỏi mở đầu háo hức; "nhưng nhớ" hạ giọng cảnh báo.

## S05 — Tắt danh sách & chặn thư mục

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S05c1 | +7% | 0,20 | Luật đầu tiên, dễ mà nhiều bạn quên: tắt Directory Listing bằng dòng Options trừ Indexes. Khi mở một thư mục không có tệp mặc định, máy chủ sẽ im lặng, thay vì khoe hết danh sách tệp bên trong. |
| S05c2 | +6% | 0,35 | Nhưng cẩn thận: tắt danh sách không chặn được từng tệp. Biết đúng tên tệp vẫn vào được — nhiều bạn mới học Apache nhầm chỗ này. Muốn chặn hẳn cả thư mục, dùng Require all denied: mọi yêu cầu sẽ nhận 403 Forbidden. |

Sắc thái: "im lặng" thả chậm; "Biết đúng tên tệp vẫn vào được" nhấn cảnh báo.

## S06 — FilesMatch: chặn theo phần mở rộng

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S06c1 | +7% | 0,20 | Còn tệp nhạy cảm rải rác? Dùng FilesMatch chặn theo phần mở rộng: env, sql, log, bak, ini, sh. Cờ i trong ngoặc giúp so khớp không phân biệt hoa thường. |
| S06c2 | +6% | 0,30 | Nhưng đừng chỉ tin vào phần mở rộng. Bí mật an toàn nhất là cất ngoài DocumentRoot. Đừng để tệp env như cuốn nhật ký bỏ quên trên bàn cà phê. |

Sắc thái: liệt kê nhanh 6 đuôi tệp; câu so sánh cuối có nụ cười trong giọng.

## S07 — Giấu đường dẫn vật lý

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S07c1 | +7% | 0,20 | Luật thứ ba: giấu đường dẫn vật lý bằng URL Rewrite. Người dùng thấy địa chỉ about gọn gàng, còn Apache âm thầm phục vụ tệp nằm sâu trong frontend, pages, about. |
| S07c2 | +6% | 0,35 | Cần RewriteEngine On và module mod rewrite. Quy tắc khớp about, thay bằng đường dẫn thật, cờ L để dừng xử lý. Và đừng lẫn rewrite nội bộ với chuyển hướng 301: một cái giữ nguyên địa chỉ, một cái bắt trình duyệt đổi sang địa chỉ mới. |

Sắc thái: "âm thầm" kéo chậm; vế so sánh 301 đọc rõ từng vế.

## S08 — Front Controller: một cửa duy nhất

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S08c1 | +9% | 0,20 | Giờ đến phần hay nhất: Front Controller. Thay vì mỗi chức năng một tệp riêng như login, register, products, orders, mọi yêu cầu đều đi qua một cửa duy nhất: tệp index.php. |
| S08c2 | +7% | 0,35 | Cửa đó đọc URL, xác định route, kiểm tra quyền, gọi đúng chức năng rồi trả kết quả. Muốn thêm kiểm tra đăng nhập hay phân quyền? Chỉ sửa một chỗ. Và tuyệt đối không đưa đường dẫn người dùng nhập thẳng vào include. |

Sắc thái: mở đầu hào hứng nhất bài; câu cuối cảnh báo dứt khoát.

## S09 — Whitelist Routing → 404

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S09c1 | +7% | 0,30 | Cách an toàn là Whitelist Routing: khai báo trước danh sách route được phép. Có trong danh sách thì chạy, không có thì trả 404 Not Found. 404 ở đây không đáng buồn — nó là dấu hiệu hệ thống đang làm đúng: không có cửa thì không mở. |

Sắc thái: câu cuối là "punchline" — chậm, rõ, pha hài.

## S10 — Tách public / private

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S10c1 | +6% | 0,25 | Ghép tất cả lại: tách rõ public và private. Frontend, assets, index.php là công khai; app, config, routes, storage, env là nội bộ. Mấu chốt là trỏ DocumentRoot thẳng vào thư mục public, thay vì ném cả mã nguồn ra vùng công khai rồi cầu nguyện htaccess che giúp. |
| S10c2 | +6% | 0,30 | Luồng chạy: trình duyệt gửi yêu cầu, Apache kiểm tra luật, chuyển vào front controller, router xác định route, xử lý rồi trả kết quả. Sai luật thì 403, sai route thì 404. |

Sắc thái: "rồi cầu nguyện htaccess che giúp" — hài nhẹ, không lố.

## S11 — Tóm ba ý + quiz

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S11c1 | +8% | 0,20 | Tóm gọn ba ý. Một: DevTools thấy mọi thứ gửi xuống trình duyệt. Hai: htaccess chặn thư mục, chặn tệp, đổi URL ngay tại máy chủ. Ba: Front Controller cùng whitelist chỉ mở đúng cửa cần mở. |
| S11c2 | +9% | 0,30 | Thử thách nhanh nhé: dòng nào tắt danh sách thư mục? A, Require all denied. B, Options trừ Indexes. C, RewriteEngine On. Suy nghĩ hai giây... Đáp án là B. Nếu bạn chọn đúng, xin chúc mừng! |

Sắc thái: đọc A/B/C chậm rãi, ngắt rõ; "Đáp án là B" bật lên.

## S12 — Kết

| Cue | Rate | Pause | Lời |
|---|---|---|---|
| S12c1 | +7% | 0,10 | Bảo mật không phải là che giấu, mà là kiểm soát đúng chỗ. Hãy thử dựng lại WebShield trên XAMPP, gõ một đường dẫn lạ xem chuyện gì xảy ra. Cảm ơn các bạn đã học cùng An Tech Academy, hẹn gặp ở bài tiếp theo! |

Sắc thái: ấm, chậm, kết bằng nụ cười.

---

## Ghi chú hậu kỳ

- Khoảng nghỉ giữa cue: 0,30 s; đuôi cảnh: 1,0 s trước khi chuyển (xfade 0,3 s chồng lấn).
- Pitch shift hậu kỳ: +0,5 semitone ở cue cao hứng (S01c2, S08c1), +0,2–0,7 semitone rải đều; không vượt ±1 semitone để tránh méo formant.
- Phụ đề: tối đa 2 dòng, chuẩn hoá theo `subs` trong `mau/manifest.json`.
