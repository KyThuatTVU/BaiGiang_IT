# 02 — GLOSSARY & BẢNG PHÁT ÂM

Quy trình theo mục 3.2 và 15.3. Cột **Đã nghe kiểm tra** chỉ được đánh "Có" sau khi nghe file audio thực tế — hiện toàn bộ là **Chưa**.

## 1. Quy tắc chung

- Lời thoại hiển thị giữ đúng tên công nghệ, không phiên âm lên phụ đề.
- Bản viết cho TTS (cột 5) chỉ thay thế khi ký hiệu/code dễ bị đọc sai; phụ đề vẫn hiển thị dạng gốc nếu đọc được tự nhiên.
- Với tên sự kiện (`update-data`, `sync-state`, `data-updated`), giữ nguyên dạng có gạch nối; TTS đọc từng từ tiếng Anh.
- Acronym chọn **một** cách đọc và giữ nguyên toàn video.

## 2. Bảng thuật ngữ

| Thuật ngữ | Nhóm | Cách đọc chốt | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn | Đã nghe kiểm tra |
|---|---|---|---|---|---|---|
| Node.js | Runtime | nốt chấm giây-ét | Không đọc "nốt-đờ" | node chấm giây-ét | Tên chính thức nodejs.org | Chưa |
| npm | Công cụ | en-pi-em | Đọc từng chữ cái | en-pi-em | Tài liệu npm | Chưa |
| Express | Web framework | ích-prét | Trọng âm âm tiết 2 | ích-prét | expressjs.com | Chưa |
| Socket.IO | Thư viện realtime | só-ckịt chấm ai-âu | Không đọc "socket i-o" rời rạc | só-ckịt chấm ai-âu | socket.io | Chưa |
| WebSocket | Giao thức | uép-só-ckịt | Trọng âm "uép" | uép-só-ckịt | RFC 6455 | Chưa |
| HTTP | Giao thức | hát-tê-tê-pê | Đọc từng chữ cái | hát-tê-tê-pê | RFC 9110 | Chưa |
| Request – Response | Kiến trúc | ri-quét – ri-spón | Giữ nhịp ngắt giữa hai từ | ri-quét, ri-spón | MDN | Chưa |
| API | Giao tiếp | ây-pi-ai | Thống nhất, không đọc "a-pi" | ây-pi-ai | — | Chưa |
| Client | Kiến trúc | cờ-lai-ần | Trọng âm âm tiết 1 | cờ-lai-ần | — | Chưa |
| Server | Kiến trúc | sơ-vờ | Không đọc "séc-vờ" | sơ-vờ | — | Chưa |
| Event | Khái niệm | i-vèn | Trọng âm âm tiết 2 | i-vèn | — | Chưa |
| Polling | Kỹ thuật | pô-ling | Nhấn "pô" | pô-ling | MDN | Chưa |
| Real-time | Khái niệm | ri-ồn-taim | Đọc liền, không tách | ri-ồn-taim | — | Chưa |
| Data | Khái niệm | đây-ta | — | đây-ta | — | Chưa |
| Synchronization | Khái niệm | sinh-krờ-nai-dây-sần | Chậm hơn câu thường | sinh-krờ-nai-dây-sần | — | Chưa |
| Conflict Resolution | Khái niệm | còn-flịch rè-dô-lu-sần | Ngắt giữa hai từ | còn-flịch, rè-dô-lu-sần | — | Chưa |
| Last Write Wins | Kỹ thuật | lát rai quần | Đọc rõ "wins" | lát rai quần | — | Chưa |
| LWW | Acronym | eo-đắp-bờ-liu | Đọc tên chữ cái | eo-đắp-bờ-liu | — | Chưa |
| Optimistic Locking | Kỹ thuật | óp-ti-mít-tịch ló-king | Không đọc "op-ti-mis-tic" kiểu Pháp | óp-ti-mít-tịch ló-king | — | Chưa |
| OT | Acronym (Operational Transformation) | âu-ti | Nói rõ trong hình là Operational Transformation | âu-ti | — | Chưa |
| CRDT | Acronym (Conflict-free Replicated Data Type) | xê-a-đi-ti | Nói rõ trong hình | xê-a-đi-ti | — | Chưa |
| JSON | Định dạng | giây-sần | Không đọc "giôn" | giây-sần | — | Chưa |
| RAM | Phần cứng | ram | Đọc như từ "ram", không đánh vần | ram | — | Chưa |
| Terminal | Công cụ | tơ-mi-nồ | Trọng âm âm tiết 1 | tơ-mi-nồ | — | Chưa |
| localhost | Mạng | lâu-câu-hốt | — | lâu-câu-hốt | — | Chưa |
| cổng 3000 | Số | cổng ba nghìn | Không đọc "ba không không không" | cổng ba nghìn | — | Chưa |
| MySQL | CSDL | mai-ét-kiu-en | — | mai-ét-kiu-en | mysql.com | Chưa |
| PostgreSQL | CSDL | pốt-grét-xờ-quy-en | Không đọc "post-gre-sql" | pốt-grét-xờ-quy-en | postgresql.org | Chưa |
| SyncLab | Tên ứng dụng | sính-láp | Tên riêng trong bài | sính-láp | Nội dung bài | Chưa |
| server.js | Tên file | sơ-vờ chấm giây-ét | — | sơ-vờ chấm giây-ét | — | Chưa |
| index.html | Tên file | in-đếch chấm hát-tê-em-eo | — | in-đếch chấm hát-tê-em-eo | — | Chưa |
| update-data | Sự kiện | úp-đết đây-ta | Giữ gạch nối khi hiển thị | úp-đết đây-ta | Mã nguồn bài | Chưa |
| sync-state | Sự kiện | sình-stây | — | sình-stây | Mã nguồn bài | Chưa |
| data-updated | Sự kiện | đây-ta úp-đết-tịt | — | đây-ta úp-đết-tịt | Mã nguồn bài | Chưa |
| sharedData | Biến | seo đây-ta | Không đọc "shared data" | seo đây-ta | Mã nguồn bài | Chưa |
| io | Đối tượng | ai-âu | Chỉ đọc khi nhắc "đối tượng io" | ai-âu | Mã nguồn bài | Chưa |
| io.emit() | Hàm | ai-âu chấm i-mít | **Lời thoại dùng "hàm emit của đối tượng io"** | (không dùng ký hiệu) | Mã nguồn bài | Chưa |
| socket.on() | Hàm | só-ckịt chấm on | Lời thoại dùng "lắng nghe sự kiện" | (không dùng ký hiệu) | Mã nguồn bài | Chưa |
| io() | Hàm | ai-âu | Lời thoại dùng "gọi hàm io" | (không dùng ký hiệu) | Mã nguồn bài | Chưa |
| require() | Hàm | ri-quai-ơ | Chỉ xuất hiện trên hình, không đọc | — | — | — |
| console.log | Hàm | côn-sâu chấm lóc | Không đọc trong lời thoại | — | — | — |

## 3. Điểm phát âm rủi ro cao (ưu tiên nghe lại — mục 15.3)

1. `io` / `io.emit` / `emit` — dễ bị đọc thành "i-o" hoặc "e-mit". Đã chuyển sang lời nói tự nhiên.
2. `Socket.IO` — dễ đọc rời thành "socket chấm i o".
3. `localhost:3000` — dễ đọc "ba không không không".
4. `sync-state` / `data-updated` — dễ nuốt phụ âm cuối.
5. `CRDT` — dễ đọc thành "cờ-rờ-đờ-tờ".
6. `Node.js` — dễ đọc "nốt chấm giốt".
7. `PostgreSQL` — dễ đọc sai hoàn toàn.
8. Từ **"năm"** trong "cứ năm giây một lần" — đã thêm "một lần" để tránh nhầm với "năm" (year).

## 4. Thuật ngữ chỉ xuất hiện trên hình (không đọc)

`require`, `http.createServer`, `app.use`, `express.static`, `new Server`, `socket.emit`, `typeof`, `disconnect`, `addEventListener`, `getElementById`, `textContent`, `.value`, CSS `border-radius`, `DOCTYPE`, `meta charset`, `viewport`.

Nguyên tắc: hình hiển thị đúng ký hiệu; lời thoại chỉ nói ý nghĩa. Không đọc từng dòng code.
