# 00 — HỒ SƠ DỰ ÁN: ĐỒNG BỘ DỮ LIỆU THỜI GIAN THỰC

**Series:** An Tech Academy — Bài giảng công nghệ
**Bài:** Đồng bộ dữ liệu thời gian thực với Node.js và Socket.IO
**Quy chuẩn áp dụng:** MASTER DESIGN & VOICE STANDARD 2.3
**Trạng thái:** Cổng C — **bản đầy đủ đã dựng** (`mau/full/full.mp4`, 7:30,8) — chờ bạn nghiệm thu
**Ngày lập:** 2026-11-13

---

## 1. Đầu vào

| Nguồn | Đường dẫn | Vai trò |
|---|---|---|
| Quy chuẩn sản xuất | `D:/Edit/MASTER_DESIGN_VOICE_STANDARD_2.3.md` | Ràng buộc bắt buộc |
| Nội dung bài giảng | `D:/Edit/Baigiang_dongbodulieu/Noidungdongbodulieu.docx` | Lời thoại gốc, code, quiz |
| Pipeline tham chiếu | `D:/Edit/Baigiang_Apriori/tools/*` | TTS edge-tts, render PIL, assemble ffmpeg |

## 2. Đối tượng và mục tiêu

- **Người học:** sinh viên CNTT năm 2–3, đã biết HTML/CSS/JavaScript cơ bản, chưa từng làm ứng dụng realtime.
- **Sau bài học, người học có thể:**
  1. Phân biệt HTTP request–response, Polling và WebSocket.
  2. Giải thích vai trò trung tâm của Server trong đồng bộ trạng thái.
  3. Đọc hiểu và chạy được ứng dụng SyncLab tối giản với Express + Socket.IO.
  4. Nhận diện 3 vấn đề production: lưu RAM, xác thực/quyền, xung đột dữ liệu.

## 3. Phạm vi và đầu ra

| Hạng mục | Nội dung |
|---|---|
| Thời lượng đích | **7:40** (6 phần) — đã cắt nội dung để đạt, xem §6 |
| Thời lượng thực tế | **7:30,8** (87 cue, 34 cảnh, 6.631 ký tự; audio lời thoại 6:51,6) — xem §6 |
| Định dạng | MP4 H.264 High 1920×1080, 30 fps, AAC 48 kHz mono, 22,9 MB |
| Phụ đề | **Burn cứng trong hình** + file `full.srt` (111 đoạn, tối đa 2 dòng) |
| Tài nguyên kèm | Kịch bản, glossary, storyboard, art direction, `manifest.json` (87 cue), `timeline.json` |

## 4. Cổng duyệt (bắt buộc)

| Cổng | Nội dung | Trạng thái |
|---|---|---|
| **A** | Hồ sơ, kịch bản, glossary, storyboard, art direction | Đã chốt (cắt 7:40, 34 cảnh) |
| **B** | Video mẫu 30–45 s (voice + visual + SFX + phụ đề + nhân vật) | **Đã duyệt** 2026-11-13 (`mau/sample_congB.mp4`, 32,4 s) |
| **C** | Full draft + bảng nghiệm thu | **Đã dựng** — chờ bạn nghiệm thu (`mau/full/full.mp4`) |

## 5. Ma trận năng lực công cụ (trung thực)

| Hạng mục | Khả thi | Công cụ / cách làm | Giới hạn phải nêu |
|---|---|---|---|
| Giọng nam **miền Nam** | **KHÔNG** | edge-tts chỉ có `vi-VN-NamMinhNeural` (nam, giọng Bắc) và `vi-VN-HoaiMyNeural` (nữ) | §7 — đã chốt dùng giọng Bắc, ghi rõ ngoại lệ |
| Giọng nam Bắc +18% | Có | edge-tts `vi-VN-NamMinhNeural`, rate +18% | Đã dùng cho 3 bài trước |
| Nhân vật giáo viên | Có (mức 2D, **đã render thử ở Cổng B**) | Vector vẽ bằng PIL, 3 pose dùng thực tế (D/C/G) + vẫy tay, idle 2 px, chớp mắt 4,2 s | Không phải rig 3D/xương, không lip-sync; miệng chỉ 3 biến thể đổi theo nhịp |
| Hiệu ứng vẽ tay | Có (**đã render thử**: gạch chân S01, connector S06) | Progressive polyline | Chỉ nét vector, không mô phỏng mực loang |
| SFX | Có (**đã tổng hợp 7 file WAV**) | Tổng hợp bằng numpy → WAV 48 kHz | SFX đơn giản (bút, pop, click, chime, whoosh, buzz, key) |
| Nhạc nền | Không dùng | — | Tránh lấn voice; có thể bổ sung nếu bạn yêu cầu |
| Code highlight theo cue | Có | Render code panel + nền dòng sáng | Code tĩnh, không gõ từng ký tự; **chưa render thử** |
| Giao diện mô phỏng | Có (**đã render thử**: 3 khung trình duyệt S02) | Mockup dựng bằng code PIL | Không phải quay màn hình thật |
| Kiểm tra phát âm bằng tai | **KHÔNG** | Không có công cụ nghe | Các mục phát âm để "Chưa xác minh" đến khi bạn nghe |

## 6. Thời lượng — đã chốt: cắt về 7:40

File gốc ghi 7:40 nhưng lời thoại thuần đã dài 8.218 ký tự (≈ 8:42 audio). Bạn đã chọn **cắt nội dung về 7:40**.

| Nguồn | Ký tự | Ước tính |
|---|---|---|
| Lời thoại thuần trong .docx | 8.218 | ≈ 8:42 audio |
| Kịch bản v1 (thêm lời dẫn code) | 9.075 | ≈ 9:37 audio → 10:27 video |
| **Kịch bản v2 (đã cắt, đang trình)** | **6.631** | **421,6 s audio → 7:40,7 video** |

Tính: 421,6 s audio + 34 × 1,10 s đuôi cảnh − 33 × 0,30 s crossfade + 53 × 0,22 s gap = 460,8 s.
Calibration: bài Apriori, 6.162 ký tự → 391,7 s audio, cùng giọng NamMinh +18%.

> **Số đo thực sau khi render đủ 87 cue (2026-11-13):** lời thoại **411,61 s** (6:51,6) → 16,11 ký tự/giây toàn bài; cộng 53 khoảng nghỉ 0,22 s, 34 đuôi cảnh 1,10 s, trừ 33 crossfade 0,30 s → video **450,77 s = 7:30,8**. Cao hơn dự phóng 6:38–6:52 là do các cue dài có tốc độ đọc chậm hơn mẫu; vẫn thấp hơn mốc 7:40 khoảng 9 s. Bạn đã chốt **giữ +18 %**.

**Đã cắt 8 nhóm nội dung** (chi tiết ở `01_KichBan_BaCot.md` §0b): cảnh ẩn dụ cuộc gọi, cảnh riêng OT/CRDT (gộp 1 câu vào S18), dẫn nhập dài, 4 thẻ ứng dụng → 1 cảnh 3 cue, câu lặp trong phần code, câu dẫn ưu/nhược, mô tả demo lặp, tổng kết 2 câu → 2 câu ngắn.

**Không cắt:** định nghĩa, HTTP/Polling/WebSocket, 4 bước, 3 khái niệm, LWW, Optimistic Locking, toàn bộ code, cảnh báo RAM, câu "truyền nhanh ≠ nhất quán", bài tập.

## 7. Giọng đọc — đã chốt: NamMinh (Bắc) +18 %, ngoại lệ có khai báo

Chuẩn 2.3 §4.1 yêu cầu giọng nam miền Nam. Toolchain hiện tại **không đáp ứng**:

- `edge-tts`: chỉ 1 giọng nam tiếng Việt — NamMinh, **giọng Bắc**.
- Windows SAPI trên máy: chỉ có David/Zira (tiếng Anh).
- Chưa cài engine khác (Piper, FPT.AI, Viettel, Zalo).

**Quyết định của bạn:** dùng **`vi-VN-NamMinhNeural`, rate +18 %** — giọng nam Bắc đã kiểm chứng qua 3 bài trước, chấp nhận lệch vùng miền, ghi rõ ngoại lệ trong hồ sơ và bảng nghiệm thu.

Hệ quả phải nêu ở Cổng C:
- Video **không đạt** yêu cầu "giọng nam miền Nam" của §4.1; đạt các tiêu chí còn lại (nam, rõ, tốc độ 1,18× trong khoảng 1,15–1,25×).
- Nếu sau này có key FPT.AI/Viettel/Zalo hoặc bạn tự thu âm, có thể thay voice mà **không đổi hình**: manifest giữ nguyên id cue và độ dài ước tính, chỉ chạy lại TTS + đo lại thời lượng.
- Phát âm và cảm xúc **chưa được nghe kiểm tra** — sẽ ghi "Chưa xác minh" cho đến khi bạn nghe bản full.

## 8. Kiểm chứng nội dung chuyên môn

| Nội dung | Trạng thái | Ghi chú |
|---|---|---|
| Node.js = runtime, Express = web framework, Socket.IO = thư viện realtime | Đạt | Không gọi Socket.IO là giao thức |
| Socket.IO ưu tiên WebSocket, có fallback | Đạt | Đúng theo tài liệu chính thức |
| Polling = gọi lặp theo chu kỳ | Đạt | Đã sửa "mỗi năm giây" → "cứ năm giây một lần" |
| LWW / Optimistic Locking / OT / CRDT | Đạt | Mô tả đúng mức nhập môn |
| Code `server.js` | Đạt | Chạy được; validate kiểu chuỗi + giới hạn 2.000 ký tự |
| Code `index.html` | Đạt | Dùng `/socket.io/socket.io.js` do server phục vụ |
| **Code chưa kiểm tra version khi ghi** | Đạt (có ghi chú) | `version++` vô điều kiện → **không phải** Optimistic Locking. Kịch bản chỉ nói "tăng phiên bản", không tuyên bố demo đã cài Optimistic Locking; cần caption nhỏ ở S22: "bản demo chưa gửi/kiểm tra version khi ghi" |
| Dữ liệu lưu RAM, mất khi restart | Đạt | Đã cảnh báo ở P5 |
| Không có số liệu benchmark tự tạo | Đạt | Chỉ có hằng số trong code: 2000 ký tự, cổng 3000 |

## 9. Rủi ro

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Giọng không đúng vùng miền | Cao (đã chấp nhận) | §7 — dùng NamMinh Bắc, ghi ngoại lệ trong nghiệm thu |
| Ước tính 7:40,7 lệch so với audio thật | **Cao** | Đã đo Cổng B: 18,34 ký tự/giây → dự phóng 6:38–6:52; chờ bạn chốt tốc độ đọc/nội dung trước Cổng C |
| Thuật ngữ/code bị đọc sai | Cao | Glossary + bản viết TTS riêng + nghe lại sau render |
| 34 cảnh làm thời gian render dài | Trung bình | Render song song theo shard, tính frame theo ORDER đầy đủ |
| Nhân vật giáo viên trông "AI đại trà" | Trung bình | Vector phẳng tự dựng, 1 character sheet, không dùng ảnh AI |

## 10. Bảng nghiệm thu (số đo máy — phần nghe cảm nhận chưa xác minh)

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| Kiến thức và ví dụ | Chưa xác minh | Cần người duyệt nội dung |
| Thuật ngữ và phát âm | **Chưa xác minh** | Máy không nghe được; cần bạn nghe |
| Giọng đọc và cảm xúc | **Chưa xác minh** | NamMinh Bắc +18 %; cần bạn nghe |
| Hình ảnh và icon | Đã kiểm tra khung hình | 34/34 cảnh qua preview + 7 khung trích từ video cuối |
| Sơ đồ, code, giao diện | Đã kiểm tra khung hình | Đã sửa lỗi chồng chữ, glyph thiếu (`✕ ✓ ↻ ∪` thay bằng nét vẽ) |
| Đồng bộ hình – tiếng | Sơ bộ đạt | 111 đoạn phụ đề khớp mốc cue; không có khoảng lặng > 2,5 s |
| Phụ đề | Sơ bộ đạt | Burn + SRT; 111 đoạn, tối đa 2 dòng; kết thúc 7:29,7 |
| Định dạng và file xuất | **Đạt số đo** | 1920×1080, 30 fps, H.264 High; AAC 48 kHz mono; 450,77 s; 22,9 MB |
| Độ to | **Đạt số đo** | −14,86 LUFS; true peak **−0,96 dBTP** (đo trên MP4 cuối); LRA 3,3 |
| Nhạc nền | Không dùng | Theo lựa chọn mặc định |
