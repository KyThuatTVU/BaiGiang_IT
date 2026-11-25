# 07 — Nghiệm thu bản mẫu (Cổng B)

Ngày dựng: 2026-11-23. Mẫu gồm **S01 (mở đầu)** + **S04 (ẩn dụ nhà hàng)**, dùng đúng chữ đã khóa ở Cổng A.

## 1. Tệp bàn giao

| Tệp | Nội dung |
|---|---|
| `mau/sample_draft.mp4` | Bản mẫu có tiếng, phụ đề cháy sẵn, **38,4 s**, 1920×1080 @30fps |
| `mau/sample.srt` | Phụ đề rời, 5 cue, sinh từ thời lượng voice đo được |
| `mau/sample_timeline.json` | Mốc bắt đầu/thời lượng từng cue |
| `mau/sample_voice.wav` | Track voice + SFX (không nhạc nền), trước loudnorm |
| `mau/qa_sample/` | Ảnh trích từ video để đối chiếu bố cục (v1; `v2_*.jpg` hiệu ứng mới; `v3_*.jpg` bảng màu công nghệ; `v4_*.jpg` thêm hình minh hoạ IT) |

## 2. Timeline mẫu

| Cue | Cảnh | Bắt đầu | Dài | Chữ (đã khóa) |
|---|---|---|---|---|
| S01c1 | S01 | 0,00 | 3,46 | "Chào các bạn! Chào mừng đến với An Tech Academy." |
| S01c2 | S01 | 3,94 | 5,27 | "Bạn bấm đặt món trên app, hai giây sau đã có thông báo xác nhận. Vậy ai đã nói chuyện với nhà bếp?" |
| S01c3 | S01 | 9,69 | 4,98 | "Câu trả lời là API. Năm phút nữa, bạn sẽ hiểu nó là gì và chạy như thế nào." |
| S04c1 | S04 | 15,67 | 11,88 | "Dễ nhất là ví dụ nhà hàng. Bạn là khách, tức Client. Anh bồi bàn là API. …" |
| S04c2 | S04 | 28,30 | 9,05 | "Bạn gọi cơm gà. Bồi bàn ghi phiếu, chuyển xuống bếp. …" |

Tổng thoại 34,64 s; video 38,36 s (đệm chuyển cảnh); nằm trong khung 30–45 s.

## 3. Kết quả kiểm tra kỹ thuật (đã chạy, có số liệu)

| Hạng mục | Kết quả |
|---|---|
| Render frame | S01 482 frame, S04 680 frame, không lỗi |
| Encode + xfade | 2 cảnh, fade 0,4 s, video 38,36 s |
| Loudness | −14,41 LUFS, true peak −0,93 dBTP |
| Nhạc nền | Đã gỡ hoàn toàn; đoạn đuôi video RMS = 0,000 (chỉ còn voice + SFX) |
| Voice trong mix | Đủ 5/5 cue, RMS mỗi đoạn 0,099–0,109; không có cue câm |
| Phụ đề | 5/5 cue, mốc khớp timeline đo được |
| Hiệu ứng v2 | Icon đĩa màu bật kiểu sticker, sparkle 4 cánh, confetti ở badge / ổ cắm / món về bàn, connector nét đứt chạy, chấm trôi nền, chip nhiều màu |
| Màu công nghệ v3 | Accent chuyển sang indigo `#4F46E5`, cyan `#06B6D4`, tím `#8B5CF6`, xanh terminal `#10B981`; bỏ coral/cam/hồng. Thêm dải terminal `GET /api/mon-an 200 OK` (S01), `GET /api/menu 200 OK` (S03), `POST /orders 201 Created` (S04). Washi tape xanh dương/cyan, mapping chip 6 màu công nghệ |
| Hình minh hoạ IT v4 | Cửa sổ IDE tối có syntax color (S01 `app.js — đặt món`, S03 `GET /api/menu`), tủ rack server 3 tầng đèn LED nhấp nháy (S04), nền mạch in + dải nhị phân mờ (`bg_tech`) |
| Chuyển cảnh v3 | Đã thử riêng từng hiệu ứng với ffmpeg hiện tại: `fade`, `smoothleft`, `pixelize`, `circleopen`, `hlslice`, `radial`, `hblur` — tất cả chạy được; bản full luân phiên 7 kiểu |
| Ngắt dòng phụ đề | Sửa lỗi nối dòng: mỗi `subs` xuống dòng riêng, không còn dính "…Request Bếp…" |

## 4. Ảnh người dùng dùng trong mẫu

- `waiter_order` — polaroid S01 + thẻ tròn "BỒI BÀN" ở S04.
- `chef_cook` — polaroid S01 + thẻ tròn "NHÀ BẾP" ở S04.

12 ảnh còn lại (sơ đồ API, Postman, Thunder Client, REST, fetch…) dành cho các cảnh S02–S11; phân loại "đạt / cần sửa / loại" giữ nguyên như `00-ho-so-phan-tich.md` mục 4.

## 5. Những gì **chưa thể xác minh** (cần bạn xem/nghe)

- **Phát âm** từng chữ: tôi không có khả năng nghe lại file audio.
- **Độ dí dỏm, nhịp nhanh "vừa đủ"**: chỉ chỉnh được bằng dấu câu và tốc độ, không nghe kiểm.
- **Phụ đề khớp cảm nhận** khi xem (mốc thời gian đúng theo file voice, nhưng cảm giác đọc có thể lệch).
- **Màu/độ nét trên màn hình của bạn**: QA bằng ảnh trích, không xem trực tiếp trên máy bạn.

## 6. Giọng đọc — giới hạn đã công bố

Mẫu dùng **Edge TTS `vi-VN-NamMinhNeural`, rate +18%** — giọng nam phổ thông tổng hợp, **không phải giọng nam miền Nam thu thật**, không có tham số cảm xúc. Đây là bản tạm để duyệt nhịp và hình.

Để đạt yêu cầu "giọng hay, dí dỏm":
1. Bạn thu theo phiếu trong `06-script-thu.md` (điện thoại cũng được), đặt vào `mau/ghi_am/`; tôi trim và render lại.
2. Hoặc cấp token Viettel `hcm-minhquan` để tôi chạy giọng nam miền Nam.

## 7. Ghi chú hình đã biết

- Trong 0,4 s chuyển cảnh, hai badge cảnh chồng mờ lên nhau — bản chất của crossfade, chỉ thấy khi dừng hình.
- Đĩa cơm gà kết thúc nằm trong thẻ KHÁCH (đúng ẩn dụ "món về tới khách"), hơi chạm viền dưới thẻ.
- Confetti bung quanh chip "cơm gà của bạn đây!" (phía trên thẻ KHÁCH), không phủ lên chữ trên thẻ.
- Bản full sẽ luân phiên 7 kiểu chuyển cảnh (fade → smoothleft → pixelize → circleopen → hlslice → radial → hblur) thay vì chỉ fade; mẫu 2 cảnh chỉ có 1 mốc nên vẫn là fade.
- S03 chưa nằm trong mẫu (để giữ 38 s) nhưng đã áp cùng hệ: icon đĩa màu 3 dòng đặc điểm, sparkle quanh ổ cắm, confetti, dải terminal + cửa sổ `GET /api/menu` góc trái dưới (đã canh không chạm phụ đề).
- Nền mạch in/nhị phân cố ý rất mờ (alpha thấp) để giữ quy tắc 60-30-10; khi xem video ở tốc độ thật gần như chỉ cảm nhận texture, không tranh chữ.

## 8. Cổng B — cần bạn duyệt

Nếu mẫu đạt, tôi sản xuất **full 11 cảnh, 32 cue, ~5 phút** theo cùng hệ hình. Ước tính: TTS ~10 phút, render ~25–35 phút, encode/mux ~5 phút — chạy nền, có log.

Bạn trả lời một trong ba:
1. **Duyệt mẫu** → tôi chạy full.
2. **Sửa chỗ X** (nêu cụ thể) → tôi chỉ sửa đúng chỗ đó rồi dựng lại mẫu.
3. **Đổi giọng trước** → bạn thu file hoặc cấp token, tôi làm lại voice rồi mới chạy full.

## 9. Bản full 11 cảnh — kết quả (2026-11-23)

- File: `mau/full_draft.mp4` — **4:52,87**, 1920×1080 @30fps, H.264 + AAC mono 48 kHz, 26,2 MB.
- Voice: Edge `vi-VN-NamMinhNeural` +18% (vẫn là giọng tạm, chưa phải giọng nam thật); 32/32 cue đủ, không thiếu file.
- Phụ đề: `mau/full.srt` 32 dòng, cue cuối kết thúc 4:51,84 (trước khi hết hình 1 s).
- Loudness: đo −20,15 LUFS đầu vào → **−14,52 LUFS**, true peak −0,84 dBTP (mục tiêu −14 / −1).
- Chuyển cảnh: 10 mốc luân phiên fade → smoothleft → pixelize → circleopen → hlslice → radial → hblur → … (chu kỳ 7).
- Đồng bộ: audio đặt theo `starts` của timeline; clip mỗi cảnh chừa 0,4 s đệm đúng bằng xfade nên không trôi mốc (đã kiểm bằng tổng duration 292,86 s khớp tổng timeline).
- QA ảnh trích: `mau/qa_full/t8…t288.jpg` — 11 cảnh đúng thứ tự, không khung đen, phụ đề không đè chữ chính.
- Vẫn **chưa thể xác minh bằng tai**: phát âm, độ dí dỏm, cảm giác nhịp — cần bạn nghe lại.
