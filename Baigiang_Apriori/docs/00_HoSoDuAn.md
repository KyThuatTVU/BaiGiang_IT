# 00 — HỒ SƠ DỰ ÁN: BÀI GIẢNG APRIORI (AN TECH ACADEMY)

**Chuẩn áp dụng:** MASTER DESIGN & VOICE STANDARD 2.2
**Nguồn nội dung:** `Noidung_apriori.docx`
**Ảnh tham chiếu phong cách:** infographic bảng dữ liệu Apriori (navy – xanh nhạt – vàng kem)
**Định dạng:** 1920×1080, 30 fps, H.264 + AAC, MP4
**Thời lượng mục tiêu:** 7–8 phút
**Giọng đọc:** `vi-VN-NamMinhNeural`, rate +18% (nam miền Bắc — ngoại lệ được người dùng chốt, lệch mặc định 4.1)

## 1. Đối tượng và mục tiêu
- Sinh viên CNTT, người học lập trình và khai phá dữ liệu.
- Sau video, người học: (1) hiểu nguyên lý Apriori và cắt tỉa; (2) đọc đúng Support, Confidence, Lift; (3) chạy được ví dụ Python và hình dung luồng đưa gợi ý lên website.

## 2. Quyết định nội dung quan trọng
Bộ dữ liệu minh hoạ được **thiết kế lại thành 10 giao dịch** thay vì 5 giao dịch trong file Word, vì:
- File Word có mâu thuẫn: dữ liệu 5 giao dịch cho Confidence Bánh mì → Sữa = 3/4 = 75%, nhưng lời thoại viết "ba giao dịch chứa Bánh mì và cả ba đều chứa Sữa" (thực tế 4 giao dịch chứa Bánh mì).
- Ảnh tham chiếu ghi Sữa+Trứng 60% và Bánh mì→Trứng 75%, trong khi dữ liệu trong ảnh chỉ cho 40% và 50%.

Bộ 10 giao dịch mới giữ **đúng các con số headline** của cả hai nguồn nhưng đúng số học:

| T | Sản phẩm |
|---|---|
| T1 | Sữa, Bánh mì, Trứng |
| T2 | Sữa, Bánh mì |
| T3 | Sữa, Bánh mì, Bơ |
| T4 | Sữa, Bánh mì, Trứng |
| T5 | Sữa, Bánh mì |
| T6 | Sữa, Bánh mì |
| T7 | Sữa, Trứng |
| T8 | Sữa, Bơ |
| T9 | Trứng |
| T10 | Trứng, Bơ |

Kết quả kiểm chứng bằng code:
- Support 1 món: Sữa 80%, Bánh mì 60%, Trứng 50%, Bơ 30%.
- Support cặp: Bánh mì+Sữa 60%; Sữa+Trứng 30%; Bánh mì+Trứng 20%; Sữa+Bơ 20%; Bánh mì+Bơ 10%; Trứng+Bơ 10%.
- Ngưỡng 40% → 4 tập 1 phần tử + 1 cặp phổ biến.
- Luật: Bánh mì→Sữa (conf 100%, lift 1,25); Sữa→Bánh mì (conf 75%, lift 1,25).

Ghi chú này phải được nêu khi duyệt Cổng A: **dữ liệu là ví dụ mô phỏng**, không phải kết quả thực nghiệm.

## 3. Cổng duyệt
- **Cổng A:** kịch bản + glossary + storyboard + art direction (tài liệu 01–04).
- **Cổng B:** video mẫu 40 giây (intro + bảng số liệu + chuyển động) để duyệt voice và visual.
- **Cổng C:** bản nháp đầy đủ + bảng nghiệm thu.

## 4. Giới hạn công cụ (công bố trước)
- TTS edge-tts không hỗ trợ SSML/điều khiển cảm xúc; diễn xuất chỉ đạt được bằng chọn câu, dấu câu, tốc độ từng cue.
- Không có công cụ nghe để thẩm định phát âm; cách đọc được chốt bằng phiên âm Việt trong bản TTS và cần người dùng nghe lại.
- Hình minh hoạ sản phẩm dùng icon Lucide + hình vector tự dựng, không dùng ảnh AI.

## 5. Trạng thái sản xuất (cập nhật 2026-11-13)
- Kịch bản: 69 cue, 23 cảnh S01–S23.
- Renderer: PIL 1920×1080/30fps + ffmpeg; icon Lucide raster hoá bằng Edge headless.
- **Mẫu Cổng B:** `mau/full/sample_draft.mp4` — 38,9 giây (S01 + S02 + S10), loudness −14,4 LUFS, TP −0,9 dB.
- Phát âm thử: `mau/full/preflight_terms.mp3` — 55,1 giây, 8 thuật ngữ (Apriori, transaction, Support, Confidence, Lift, Flask, JSON, mlxtend) kèm mốc thời gian trong `preflight_terms.txt`.
- Phụ đề mẫu: `mau/full/sample.srt`.
- TTS toàn bộ: 69/69 cue, tổng 427,70 giây (7:07) — đúng khung 7–8 phút; `full.srt` + `full_timeline.json` đã sinh.
- Cổng B đã được người dùng duyệt ngày 2026-11-13.

## 6. Bảng nghiệm thu Cổng C (cập nhật 2026-11-13)
- Bản dựng: `mau/full/full_draft.mp4` — 7:07,70; 1920×1080, 30 fps, H.264 High; AAC 48 kHz mono 130 kbps; −14,45 LUFS, true peak −0,86 dB; 19,4 MB.
- Phụ đề: `mau/full/full.srt` — 69 khối, khối cuối kết thúc 00:07:06,600.

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| Kiến thức và ví dụ | Đạt | Support 80/60/50/30%, BM+Sữa 60%, conf 100%/75%, lift 1,25 — đã đối chiếu số học với 10 giao dịch |
| Thuật ngữ và phát âm | Chưa xác minh | Không có công cụ nghe; cần người dùng kiểm tra `preflight_terms.mp3` |
| Giọng đọc và cảm xúc | Chưa xác minh | edge-tts không SSML; cần người dùng nghe bản đầy đủ |
| Hình ảnh và icon | Đạt | Contact sheet 23 cảnh `mau/qa/full_sheet.png` + 5 ảnh phóng to; không cắt chữ, không chồng lớp |
| Sơ đồ, code, giao diện | Đạt | Code panel đúng API mlxtend/Flask; bảng số liệu khớp kịch bản |
| Đồng bộ hình – tiếng | Đạt | Cùng một timeline sinh audio + phụ đề; video 427,70 s ≈ audio 427,71 s; spot-check 400 s khớp S22c4 |
| Phụ đề | Đạt | 69 khối, không lẫn phiên âm TTS; tối đa 2 dòng/khối |
| Định dạng và file xuất | Đạt | Thông số ghi ở trên; màu full-range (yuvj420p) |
| Dữ liệu | Đạt (có công bố) | 10 giao dịch là ví dụ mô phỏng, đã nêu trong video (S21) và hồ sơ |

