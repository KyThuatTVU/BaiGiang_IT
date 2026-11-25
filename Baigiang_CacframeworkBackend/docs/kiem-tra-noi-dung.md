# Kiểm tra kỹ thuật — Ngôn ngữ, runtime, framework, thư viện

Phạm vi rà soát: 21 cảnh, 64 cue thoại, toàn bộ code panel và nhãn trên hình. Mục tiêu: không nhầm lẫn giữa **ngôn ngữ lập trình**, **môi trường thực thi (runtime)**, **framework**, **thư viện**, **ORM** và **nền tảng**.

## 1. Bảng phân loại

| Tên | Phân loại đúng | Ghi chú kiểm chứng |
|---|---|---|
| JavaScript | Ngôn ngữ lập trình | Chạy trên trình duyệt và trên Node.js |
| TypeScript | Ngôn ngữ (superset của JavaScript) | Biên dịch về JavaScript; không phải framework |
| Node.js | Môi trường thực thi (runtime) | Xây trên V8 + libuv; **không phải framework** |
| Express | Framework web (tối giản) | Chạy trên Node.js |
| NestJS | Framework | TypeScript, DI, module; chạy trên Node.js |
| Fastify | Framework web | Tối ưu throughput/độ trễ ở mức thiết kế |
| Python | Ngôn ngữ lập trình | — |
| Django | Framework full-stack | ORM, admin, auth, bảo mật tích hợp |
| Flask | Micro-framework | Nhẹ, tự lắp thành phần |
| FastAPI | Framework API | Type hints, OpenAPI/Swagger tự sinh, async |
| PHP | Ngôn ngữ lập trình | Chạy qua PHP-FPM/OPcache trên server |
| Laravel | Framework full-stack | Eloquent ORM, routing, middleware, auth, queue |
| Symfony | Framework + bộ component tái sử dụng | Nhiều thành phần được framework khác dùng lại |
| CodeIgniter | Framework nhẹ | Ít cấu hình, dễ tiếp cận |
| Java | Ngôn ngữ lập trình | Chạy trên JVM |
| Spring Boot | Framework | Auto-configuration, embedded server, hệ sinh thái Spring |
| Quarkus | Framework | Cloud-native, container-first, hỗ trợ native image |
| Micronaut | Framework | Khởi động nhanh, ít bộ nhớ, microservices |
| C# | Ngôn ngữ lập trình | — |
| .NET | Nền tảng/runtime | CLR, thư viện chuẩn, đa nền tảng từ .NET Core |
| ASP.NET Core | Framework web | Chạy trên .NET, đa nền tảng |
| Entity Framework Core | ORM | Ánh xạ đối tượng ↔ database, không phải framework web |
| Minimal APIs | Kiểu API trong ASP.NET Core | Không phải framework riêng |
| Go (Golang) | Ngôn ngữ lập trình | Goroutine, channel |
| Gin | Framework web | Định tuyến, middleware |
| Echo | Framework web | Đầy đủ tính năng |
| Fiber | Framework web | API phong cách Express, chạy trên fasthttp |
| `net/http` | Thư viện chuẩn | Không phải framework |
| Ruby | Ngôn ngữ lập trình | — |
| Rails | Framework full-stack | Convention over Configuration |
| Sinatra | Micro-framework/DSL | Route tối giản |
| bcrypt | Thư viện băm mật khẩu | Có salt, chủ động chậm |
| JWT | Chuẩn token + thư viện triển khai | Không phải framework |
| REST API | Kiến trúc/phong cách API | Không phải công nghệ cụ thể |
| HTTP | Giao thức | Request/response |

## 2. Các điểm đã sửa hoặc siết lại

1. **Node.js** — loại bỏ mọi cách nói ngầm coi là framework; cue `langfw-4` và `js-4` nói thẳng “môi trường thực thi, không phải framework”, kèm hình 4 khay phân loại.
2. **.NET vs ASP.NET Core** — hình ghi .NET là nền tảng, ASP.NET Core là framework; không gộp hai khái niệm.
3. **Spring Boot** — dùng “tự cấu hình” theo nghĩa auto-configuration, không nói “tự viết code”.
4. **Symfony** — mô tả là framework kiêm bộ component, tránh gọi là “thư viện”.
5. **Sinatra** — gọi là micro-framework/DSL, không xếp ngang framework full-stack.
6. **TypeScript** — trong hình có nhãn “superset của JavaScript”; lời thoại chỉ nói “cặp đôi phổ biến”, không gọi TS là framework.
7. **EF Core** — ghi rõ là ORM, không phải framework web.
8. **Minimal APIs** — ghi rõ là kiểu API trong ASP.NET Core.

## 3. Tuyên bố đã tránh

- Không nói framework nào “nhanh nhất”, “tốt nhất”, “bảo mật nhất”.
- Không đưa con số benchmark thật. Thanh so sánh khởi động Quarkus/Micronaut có nhãn **“minh họa, không phải benchmark”**.
- Không nói “PHP đã chết” hay “Java chỉ cho ngân hàng”; chỉ nêu định hướng thế mạnh và ví dụ điển hình.
- Không nói “Node.js là framework”, “React là framework backend”, “JWT là framework”.
- Không khẳng định một ngôn ngữ chỉ dùng được một loại ứng dụng.

## 4. Kiểm tra bảo mật của ví dụ đăng nhập

| Yêu cầu | Cách thể hiện trong video |
|---|---|
| Không dùng mật khẩu thật | Form chỉ hiển thị `••••••••`; JSON minh họa cũng che mật khẩu |
| Không lưu plaintext | Lời thoại nói rõ “mật khẩu gốc không bao giờ lưu dạng văn bản thuần”; hình chỉ có `password_hash` |
| So sánh an toàn | `bcrypt.compare(password, user.password_hash)` |
| Token | `jwt.sign({ sub: user.id }, SECRET, { expiresIn: '15m' })`, nhấn mạnh token có thời hạn |
| Chống dò tài khoản | Sai email hoặc sai mật khẩu đều trả 401 với thông báo chung |
| Không lộ secret | Code panel dùng `process.env.JWT_SECRET`, không in giá trị |

## 5. Đối chiếu với brief

| Yêu cầu brief | Trạng thái |
|---|---|
| Giải thích Backend, ví dụ thương mại điện tử, 5 bước | Đạt — cảnh `intro`, `backend` |
| Mô hình User → Frontend → API → Backend → Database | Đạt — cảnh `backend` |
| Animation một request đăng nhập | Đạt — cảnh `flow` và `login` |
| Phân biệt ngôn ngữ vs framework, phép so sánh | Đạt — cảnh `langfw` |
| 7 hệ sinh thái, logo, code, kiến trúc, use case | Đạt — cảnh `js` → `ruby`, mỗi hệ một cảnh riêng |
| Bảng so sánh + tiêu chí + 3 kịch bản | Đạt — cảnh `compare`, `choose` |
| Mô phỏng 8 bước + ví dụ Express/bcrypt/JWT an toàn | Đạt — cảnh `login` |
| Tổng kết 5 điểm + 3 quiz có đếm ngược + câu kết | Đạt — cảnh `recap`, `quiz`, `outro` |
| Lời chào “Tôi là An Tech Academy” | Đạt — cue `intro-1` (nói “Mình là An Tech Academy”) |
| Giọng Nam | **Chưa đạt tuyệt đối** — Edge TTS chỉ có `vi-VN-NamMinhNeural` (miền Bắc); cần dịch vụ khác nếu bắt buộc giọng Nam |
| Tốc độ 1.15–1.25x | Đạt — +22% |
| Không đọc danh sách công nghệ | Đạt — mỗi hệ có lý do, thế mạnh, bài toán |

## 6. Nguồn tham chiếu

Tài liệu chính thức của: nodejs.org, expressjs.com, docs.nestjs.com, fastify.dev, djangoproject.com, flask.palletsprojects.com, fastapi.tiangolo.com, php.net, laravel.com, symfony.com, codeigniter.com, spring.io, quarkus.io, micronaut.io, dotnet.microsoft.com, go.dev, gin-gonic.com, echo.labstack.com, gofiber.io, ruby-lang.org, rubyonrails.org, sinatrarb.com. Các nhận định về “thế mạnh” là tổng hợp định hướng thiết kế và mức phổ biến, không phải kết quả benchmark.
