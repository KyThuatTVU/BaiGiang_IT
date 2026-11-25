# Storyboard — Ngôn ngữ lập trình & Framework Backend

Khung hình 1920×1080. Mọi cảnh dùng chung: brand **AN TECH ACADEMY** góc trái trên, nhãn **BACKEND · LANGUAGES & FRAMEWORKS** góc phải trên, thanh tiến trình mảnh dưới đáy, dải phụ đề giữa dưới. Chuyển cảnh bằng whoosh + wipe mềm; không dùng hiệu ứng nhấp nháy mạnh.

> Đây là storyboard đã duyệt trước khi dựng. Mốc thời gian trong từng mục là ước lượng lúc lập kế hoạch; **mốc chính xác của bản dựng cuối** nằm trong [loi-thoai.md](loi-thoai.md) và `build/subtitles.srt` (tổng 8:30.3).

## 1. `intro` — Backend, bộ não phía sau giao diện · 0:00.0 – 0:26.2

**Bố cục:** trái 55% là cửa sổ trình duyệt “NOVA SHOP” mở form đăng nhập; phải 45% là tủ server 3 tầng đèn nháy và trụ database. Đường nét đứt nối form → server → DB. Thầy chibi đứng góc phải dưới, tay chỉ.

**Nhịp:**
- 0:00.1 — form hiện, email và mật khẩu được “gõ” tự động (mật khẩu hiển thị dấu chấm), con trỏ nhấn **Đăng nhập**, vòng pulse lan ra; chime chào.
- 0:09.8 — camera lùi, tiêu đề lớn **NGÔN NGỮ & FRAMEWORK BACKEND**, phụ đề “Từ một cú click đến database”; packet sáng chạy dọc đường nối.
- 0:17.2 — bảy huy hiệu ngôn ngữ bay vào quỹ đạo quanh tiêu đề; thầy vẫy tay; chime.
- 0:24.5 — wipe sang cảnh lộ trình.

## 2. `goals` — Bốn chặng trên lộ trình · 0:26.5 – 0:42.2

**Bố cục:** con đường nét đứt uốn lượn từ trái sang phải, 4 thẻ mốc đánh số 01–04: “Backend là gì”, “Ngôn ngữ vs Framework”, “Bảy hệ sinh thái”, “So sánh & chọn”. Thầy đứng đầu đường.

**Nhịp:** 0:26.7 cả 4 thẻ trượt lên theo nhịp pop; thẻ đang nói phóng to nhẹ. 0:36.1 một chip quiz “3 câu hỏi nhanh” nảy ra với tia sét, thầy nháy mắt.

## 3. `div1` — Chương 01 · 0:42.6 – 0:45.1

Nền gradient xanh dương → cyan, số **01** cỡ lớn mờ, tiêu đề **BACKEND LÀ GÌ?** trượt vào, lưới mảnh và mũi tên quét ngang. Riser ngắn.

## 4. `backend` — Backend làm việc gì? · 0:45.4 – 1:26.0

**Bố cục:** dải trên là mockup shop thu nhỏ với 5 điểm nóng: đăng nhập, tìm kiếm, giỏ hàng, đặt hàng, thanh toán. Giữa màn hình là chuỗi 5 nút: **Người dùng → Frontend → API → Backend → Database**. Dưới cùng là 3 chip trách nhiệm: Xác thực, Nghiệp vụ, Truy vấn.

**Nhịp:**
- 0:45.5 — mockup shop hiện, từng hotspot sáng lên theo lời kể; click.
- 0:54.8 — packet HTTP chạy từ Frontend qua API vào Backend, rồi xuống DB và quay lại; data blip.
- 1:05.1 — nhãn lớn: API = cửa ngõ, Backend = bộ não, Database = trí nhớ dài hạn; marker.
- 1:12.9 — tách đôi màn hình: trái “Frontend: hiển thị”, phải “Backend: quyết định – kiểm tra – ghi nhớ”; pop.
- 1:19.2 — server chuyển đỏ, chữ **SẬP**, rồi khởi động lại xanh; tiếng error để nhấn tầm quan trọng.

## 5. `flow` — Một yêu cầu đi qua hệ thống · 1:26.3 – 1:51.4

**Bố cục:** 6 trạm ngang: Nhập liệu → `POST /login` → API → Xác thực → Database → Response. Panel JSON request phía trên, response phía dưới; đồng hồ mili giây bên phải.

**Nhịp:** 1:26.4 packet rời trình duyệt, đi qua từng trạm theo lời kể; 1:34.5 trạm Xác thực sáng, so sánh hash; 1:42.4 response 200 quay về, đồng hồ dừng dưới 1 giây, dấu check xanh. Mật khẩu trong JSON luôn là `"••••••••"`.

## 6. `div2` — Chương 02 · 1:51.7 – 1:54.9

Nền tím → xanh, số **02**, tiêu đề **NGÔN NGỮ vs FRAMEWORK**, hai icon đối lập: búa + vật liệu bên trái, giàn giáo + bản vẽ bên phải.

## 7. `langfw` — Phân biệt ngôn ngữ, runtime, framework · 1:55.3 – 2:34.3

**Bố cục:** trái là hộp dụng cụ với 7 chip ngôn ngữ; phải là giàn giáo công trình. Giữa là 4 khay dán nhãn: **NGÔN NGỮ / RUNTIME / FRAMEWORK / THƯ VIỆN**.

**Nhịp:** 1:55.4 hộp dụng cụ mở, 7 chip xếp hàng; 2:05.7 giàn giáo dựng lên, từng thanh khớp vào; 2:15.6 quy tắc “framework luôn thuộc một ngôn ngữ” hiện dưới dạng công thức `Express ∈ JavaScript`, `Laravel ∈ PHP`, `Spring Boot ∈ Java`; 2:24.9 bốn thẻ bay vào khay: JavaScript → NGÔN NGỮ, Node.js → RUNTIME, Express → FRAMEWORK, bcrypt → THƯ VIỆN, mỗi thẻ có dấu check và chime.

## 8. `div3` — Chương 03 · 2:34.6 – 2:37.6

Nền tối chuyển sáng, số **03**, tiêu đề **BẢY HỆ SINH THÁI BACKEND**, 7 logo xếp vòng cung. Riser.

## 9. `js` — JavaScript & TypeScript · 2:38.0 – 3:14.0

**Bố cục:** panel vàng JS bên trái, chip TS cạnh đó; giữa là vòng **Node.js** gắn nhãn **RUNTIME**; phải là 3 thẻ framework Express / NestJS / Fastify; dưới là code panel và dải use-case.

**Nhịp:** 2:38.1 Node.js nâng JavaScript ra khỏi biểu tượng trình duyệt, mũi tên “server-side”; 2:47.9 ba thẻ framework lật mở kèm mô tả một dòng; 2:59.1 code highlight `const express = require('express')` + `app.get('/api/products', ...)`; 3:09.6 con dấu đỏ **“Node.js ≠ framework”** đóng xuống, success.

## 10. `python` — Python · 3:14.3 – 3:50.8

**Bố cục:** logo Python lớn bên trái; ba thẻ Django / Flask / FastAPI xếp bậc thang; phải là code FastAPI và mockup Swagger UI tự sinh.

**Nhịp:** 3:14.4 thẻ Django mở ra các khối ORM, Admin, Auth, Security; 3:22.8 Flask hiện các mảnh ghép tự lắp, FastAPI hiện type hints + nút “/docs”; 3:34.0 chip AI / Data science / REST API sáng lên; 3:43.1 bảng “chọn theo nhu cầu” trượt vào.

## 11. `php` — PHP · 3:51.1 – 4:19.2

**Bố cục:** nền chàm; logo PHP + chữ “PHP 8”; Laravel là thẻ lớn nhất với danh sách Eloquent, Routing, Middleware, Auth, Queue; Symfony và CodeIgniter là hai thẻ phụ.

**Nhịp:** 3:51.3 Laravel mở khóa từng thành phần; 4:02.1 sơ đồ component của Symfony và thẻ “nhẹ, dễ học” của CodeIgniter; 4:09.9 code `Route::get('/shop', ...)` + use-case CMS / e-commerce / admin.

## 12. `java` — Java · 4:19.6 – 4:45.5

**Bố cục:** logo Java bên trái, Spring Boot là khối trung tâm 3 tầng: Auto-configuration / Embedded server / Ecosystem; Quarkus và Micronaut hai thẻ bên phải.

**Nhịp:** 4:19.7 ba tầng Spring Boot dựng lên; 4:29.5 hai thanh “khởi động” so sánh Quarkus/Micronaut với nhãn rõ **“minh họa, không phải benchmark”**; 4:38.9 code `@RestController` và chip ngân hàng / giao dịch / microservices.

## 13. `csharp` — C# & .NET · 4:45.8 – 5:13.6

**Bố cục:** vòng tròn **.NET** ở giữa (CLR, cross-platform), ASP.NET Core bên trái, EF Core bên phải, Minimal APIs phía dưới.

**Nhịp:** 4:46.0 vòng .NET vẽ ra, chip “Windows / Linux / macOS”; 4:56.0 EF Core nối thanh database, hiện `DbContext` thay cho SQL thủ công; 5:04.6 code Minimal API `app.MapGet("/hello", ...)` và chip doanh nghiệp / nhân sự / nội bộ.

## 14. `go` — Go · 5:14.0 – 5:38.5

**Bố cục:** logo Go + lưới 1.000 chấm tượng trưng goroutine; ba thẻ Gin / Echo / Fiber; code panel bên phải.

**Nhịp:** 5:14.1 lưới chấm bật sáng theo đợt, vài chấm chạy song song; 5:23.8 ba thẻ framework hiện, ghi chú `net/http` là thư viện chuẩn; 5:33.0 code `r.GET("/ping", ...)` + chip microservices / tải cao / độ trễ thấp.

## 15. `ruby` — Ruby · 5:38.8 – 6:04.1

**Bố cục:** viên ngọc Ruby bên trái, Rails là bệ phóng ở giữa với khẩu hiệu **Convention over Configuration**, Sinatra là thẻ nhỏ bên phải.

**Nhịp:** 5:38.9 dòng lệnh `rails new shop` chạy, các thư mục scaffold tự sinh; 5:48.8 Sinatra hiện route 3 dòng; 5:58.3 chip “ra mắt nhanh” và ghi chú đánh đổi hiệu năng thuần.

## 16. `compare` — So sánh bảy hệ sinh thái · 6:04.5 – 6:38.0

**Bố cục:** bảng 7 hàng × 4 cột: Hệ sinh thái / Ngôn ngữ / Framework tiêu biểu / Thế mạnh – bài toán. Header dính trên, hàng trượt vào lần lượt.

**Nhịp:** 6:04.6 hàng 1–2 vào; 6:17.2 bảng mờ đi, dòng lớn **KHÔNG CÓ FRAMEWORK TỐT NHẤT**; 6:23.6 sáu chip tiêu chí: quy mô, nghiệp vụ, hiệu năng, đội ngũ, hệ sinh thái, bảo trì; 6:30.9 thẻ trích dẫn “chọn công nghệ đội bạn giỏi”.

## 17. `choose` — Chọn công nghệ theo bài toán · 6:38.4 – 7:05.6

**Bố cục:** trái là 5 câu hỏi tiêu chí; phải là cây quyết định 3 nhánh.

**Nhịp:** 6:38.5 5 chip tiêu chí; 6:46.5 nhánh “REST API nhỏ” → Express / FastAPI; 6:52.4 nhánh “quản lý nhiều nghiệp vụ” → Laravel / Django / NestJS / ASP.NET Core; 6:59.5 nhánh “doanh nghiệp lớn” → Spring Boot / ASP.NET Core. Packet chạy theo nhánh được chọn.

## 18. `login` — Backend hoạt động thật · 7:05.9 – 7:45.2

**Bố cục:** trái 55% là form đăng nhập thật (email, mật khẩu che dấu, nút); phải 45% là code editor Express + bcrypt + JWT, nền tối. Dưới cùng là 8 chấm bước.

**Nhịp:**
- 7:06.0 form và code hiện; đường nối request–response giữa hai nửa.
- 7:16.1 dòng `bcrypt.compare(...)` sáng, DB flash truy vấn, packet data.
- 7:26.7 nhánh sai: badge **401**, dòng `res.status(401)` sáng, thông báo chung “Sai email hoặc mật khẩu” (không lộ tài khoản tồn tại).
- 7:36.8 nhánh đúng: badge **200**, `jwt.sign(...)` sáng, token bay về trình duyệt, chuyển trang; success.
- 8 chấm bước lần lượt đổi màu: nhận request → kiểm tra → tìm user → so hash → ký JWT → trả response → lưu token → chuyển hướng.

## 19. `recap` — Năm điều mang về · 7:45.6 – 8:03.9

5 ô xếp zigzag: Backend = nghiệp vụ máy chủ; Ngôn ngữ = công cụ viết mã; Framework = bộ khung; mỗi ngôn ngữ nhiều framework; chọn theo bài toán. Banner **Hiểu công cụ — chọn đúng công nghệ**; thầy vẫy tay.

## 20. `quiz` — Kiểm tra nhanh · 8:04.2 – 8:43.1

Ba thẻ câu hỏi nối tiếp, mỗi thẻ có 2 lựa chọn A/B và vòng đếm ngược 3 giây.

| Thời điểm | Nội dung | Hành vi |
|---|---|---|
| 8:04.3 | Node.js là ngôn ngữ hay môi trường thực thi? | Vòng 3→2→1, tick mỗi giây |
| 8:13.3 | Đáp án: môi trường thực thi | Đáp án B sáng xanh, giải thích 1 dòng |
| 8:18.3 | Framework nào thuộc hệ sinh thái Java? | Đếm ngược 3 giây |
| 8:26.0 | Đáp án: Spring Boot | Giải thích Quarkus/Micronaut |
| 8:30.2 | Framework nào hợp xây API bằng Python? | Đếm ngược 3 giây |
| 8:37.7 | Đáp án: FastAPI | Ghi chú Flask/Django cũng được |

Lựa chọn hiển thị: Q1 **A. Ngôn ngữ lập trình / B. Môi trường thực thi**; Q2 **A. Laravel / B. Spring Boot**; Q3 **A. FastAPI / B. Ruby on Rails**. Mỗi câu chỉ có một đáp án đúng, không gây tranh cãi.

## 21. `outro` — Chọn đúng công cụ · 8:43.5 – 8:55.5

Câu kết hiện như được viết lên bảng: **“Backend chính là bộ não phía sau mỗi ứng dụng web.”** Ba chip: Hiểu backend / Phân biệt công cụ / Chọn theo bài toán. Logo AN TECH ACADEMY, dòng “Hẹn gặp ở bài tiếp theo”, fade trắng.

## Danh sách asset

**Logo/thương hiệu (vector):** JavaScript, TypeScript, Node.js, Express, NestJS, Fastify, Python, Django, Flask, FastAPI, PHP, Laravel, Symfony, CodeIgniter, Java, Spring Boot, Quarkus, Micronaut, .NET, C#, Go, Gin, Echo, Fiber, Ruby, Rails, Sinatra. Ưu tiên bộ Simple Icons (CC0); thương hiệu không có trong bộ sẽ dùng emblem cách điệu cùng màu, không tự vẽ lại logo sai.

**Mockup UI:** shop NOVA, form đăng nhập, Swagger UI, admin dashboard mini.

**Sơ đồ:** 5 nút User→Frontend→API→Backend→DB; 6 trạm request; 4 khay phân loại; bảng so sánh 7 hàng; cây quyết định 3 nhánh; 8 bước đăng nhập.

**Nhân vật:** thầy chibi 4 dáng — vẫy, chỉ, giải thích, nhìn xuống.

**Code panel:** Express, FastAPI, Laravel, Spring Boot, Minimal API, Gin, Rails, Sinatra, Express + bcrypt + JWT.
