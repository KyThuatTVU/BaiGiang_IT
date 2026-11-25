# GLOSSARY PHÁT ÂM — CỔNG A

Cách xử lý: thuật ngữ tiếng Anh trong **phụ đề/hình** giữ nguyên chính tả; trong **chuỗi TTS** thay bằng phiên âm tiếng Việt để edge-tts đọc đúng âm, không đọc rời từng ký tự.

> Trạng thái kiểm: cột "Nghe" ghi **chưa kiểm** cho mọi mục — người dựng không có khả năng nghe lại. Cột "Văn bản" xác nhận chuỗi thay thế đã nằm trong manifest và khớp ngữ cảnh.

| Thuật ngữ | Chuỗi TTS dùng | Ghi chú | Văn bản | Nghe |
|---|---|---|---|---|
| An Tech Academy | An Tếch A-ca-đê-mi | Tên kênh, đọc 3 lần trong bài | ✔ | chưa kiểm |
| Apache | A-pa-chê | Nhấn âm 2 | ✔ | chưa kiểm |
| .htaccess | hờ-tắc-xét | Không đọc dấu chấm | ✔ | chưa kiểm |
| DevTools | đép-tút | Gộp thành 1 từ | ✔ | chưa kiểm |
| F12 | ép mười hai | Tránh đọc "ép-một-hai" | ✔ | chưa kiểm |
| Ctrl + Shift + I | cần-trố, sịp ai | Đọc tên phím | ✔ | chưa kiểm |
| Network (tab) | nết-uốc | Kèm chữ "tab" phía trước | ✔ | chưa kiểm |
| JavaScript | ja-va-sờ-cờ-ríp | 4 âm tiết | ✔ | chưa kiểm |
| PHP | pê-hát-pê | Đọc từng chữ cái theo âm Việt | ✔ | chưa kiểm |
| JSON | dây-sần | Cách gọi phổ biến miền Nam | ✔ | chưa kiểm |
| HTML | HTML | edge-tts đọc chữ cái tiếng Anh ổn | ✔ | chưa kiểm |
| API | API | Giữ nguyên | ✔ | chưa kiểm |
| SQL | ét-kiu-el | — | ✔ | chưa kiểm |
| BookingService.php | Bu-king Sờ-vịt chấm pê-hát-pê | Tên tệp ví dụ trong bài | ✔ | chưa kiểm |
| config (thư mục) | con-phích | — | ✔ | chưa kiểm |
| server | sờ-vờ | Giữ từ tiếng Anh phổ thông | ✔ | chưa kiểm |
| AllowOverride | A-lao-âu-vơ-rai | Nhấn "âu" | ✔ | chưa kiểm |
| mod_rewrite | mót ri-rait | Bỏ gạch dưới | ✔ | chưa kiểm |
| Directory Listing | Đai-rếch-tơ-ri lít-ting | — | ✔ | chưa kiểm |
| Options -Indexes | Ốp-sần, trừ in-đếch-sờ | Đọc "trừ" thay dấu trừ | ✔ | chưa kiểm |
| Require all denied | Ri-quai-ơ o đì-nai | "all" đọc "o" | ✔ | chưa kiểm |
| 403 Forbidden | bốn không ba, pho-bít-đần | Số đọc rời | ✔ | chưa kiểm |
| FilesMatch | Phai-sờ-mách | — | ✔ | chưa kiểm |
| DocumentRoot | Đốc-kiu-mần-rút | — | ✔ | chưa kiểm |
| URL Rewrite | u-rờ-el ri-rait | — | ✔ | chưa kiểm |
| RewriteEngine On | Ri-rait-en-gin on | "On" đọc "on" | ✔ | chưa kiểm |
| RewriteRule | ri-rait ru (`S07c2` đọc "quy tắc") | Tránh đọc cả từ ở câu nhanh | ✔ | chưa kiểm |
| Front Controller | Phờ-rông Con-trô-lơ | — | ✔ | chưa kiểm |
| index.php | in-đếch chấm pê-hát-pê | — | ✔ | chưa kiểm |
| include | in-clu-đờ | — | ✔ | chưa kiểm |
| Whitelist Routing | Quai-lít rao-ting | — | ✔ | chưa kiểm |
| 404 Not Found | bốn không bốn, nót phao | — | ✔ | chưa kiểm |
| public / private | pấp-lịch / private | "private" đọc như tiếng Anh | ✔ | chưa kiểm |
| Router | rao-tơ | — | ✔ | chưa kiểm |
| XAMPP | zăm | Cách gọi quen thuộc | ✔ | chưa kiểm |
| frontend, routes, storage, env | phờ-rôn-en, rút, sto-rịch, en-vờ | — | ✔ | chưa kiểm |

## Từ không đổi trong TTS

Chrome, Edge, Firefox, HTTP, pages, login, register, products, orders, about, assets, app, route, rewrite — các từ này edge-tts xử lý chấp nhận được; nếu người nghe phát hiện sai ở Cổng C, sẽ bổ sung phiên âm riêng theo từng cue.

## Quy ước số & ký hiệu

- `403`, `404`, `301`: đọc rời từng chữ số ("bốn không ba"…).
- `F12`, `Ctrl Shift I`: đọc tên phím.
- `-Indexes`: đọc "trừ Indexes" (không đọc "gạch ngang").
- Dấu `→` trong phụ đề chỉ để hiển thị, không xuất hiện trong chuỗi TTS.
