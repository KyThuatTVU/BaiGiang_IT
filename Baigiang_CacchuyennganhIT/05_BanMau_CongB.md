# BẢN MẪU CỔNG B — KHÁM PHÁ CÁC CHUYÊN NGÀNH CNTT

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.2 · 12/11/2026*
*Trạng thái: ĐÃ DUYỆT 12/11/2026 ("Duyệt Cổng B, chạy preflight và sản xuất toàn bộ") — 4 mặc định a–d được chấp nhận. Đang sản xuất toàn bộ.*

## 1. Danh mục mẫu

| Mẫu | File | Nội dung |
| --- | --- | --- |
| Voice sample 20–30 s | mau/voice_sample.mp3 | 28,8 s: chào + dẫn (+10%) → liệt kê công nghệ Frontend/Backend (−5%), phiên âm đúng glossary đã duyệt |
| Tham chiếu định nghĩa chậm | mau/segC_dinhnghia.mp3 | Định nghĩa Công nghệ phần mềm, rate −5% |
| Probe chức danh tiếng Anh | mau/probe_jobtitles.mp3 | Frontend Developer, Backend Developer, Data Scientist, Penetration Tester, Business Analyst (rate +0%) — để người nghe chốt giữ chính tả Anh hay phiên âm |
| Style frame icon | mau/frames/frame_icon.png | S25: năm thẻ sản phẩm, icon Lucide teal |
| Style frame sơ đồ | mau/frames/frame_diagram.png | S10: luồng lịch sử → mô hình → gợi ý, tím AI |
| Style frame typography | mau/frames/frame_type.png | S03: checklist mục tiêu + bản đồ 6 nhóm + specimen 3 font |
| Mood board đúng/sai | mau/frames/frame_moodboard.png | Đối chiếu chuẩn 5.6 (ví dụ SAI cố ý, không dùng trong video) |
| Motion sample 10–15 s | mau/motion_sample_S10.mp4 | 12,8 s, 1080p30 H.264/AAC: S10 cues a–c có voice đồng bộ; reveal ≤200 ms, connector vẽ theo lời, chấm data-flow, highlight khối đang nói, chip kết luận hiện trong khoảng giữ tĩnh ≥1,5 s, phụ đề 2 dòng ≤42 ký tự |

## 2. Số đo nhịp giọng (đo bằng ffmpeg, không ước lượng)

| Phân đoạn | Rate | Thời lượng (s) | Âm tiết | Âm tiết/giây |
| --- | --- | --- | --- | --- |
| segA1 chào | +10% | 8,18 | 30 | 3,67 |
| segA2 dẫn | +10% | 6,43 | 27 | 4,20 |
| segB1 thuật ngữ FE | −5% | 5,95 | 17 | 2,86 |
| segB2 thuật ngữ BE | −5% | 7,03 | 20 | 2,84 |
| segC định nghĩa | −5% | 8,59 | 21 | 2,50 |

Voice sample tổng 28,82 s (đạt khổ 20–30 s). Nhịp dẫn ~3,7–4,2 âm tiết/s; thuật ngữ ~2,9; định nghĩa ~2,5 — đúng chủ đích "dẫn nhanh vừa, định nghĩa chậm". Loudness mẫu chưa chuẩn hoá: voice −18,85 LUFS/−2,42 dBTP; motion −18,50 LUFS/−2,93 dBTP; bản toàn bộ chuẩn hoá −14 LUFS/−1 dBTP.

## 3. Đã kiểm tra bằng công cụ (0.4)

- Phụ đề: 0 dòng >42 ký tự trên 153 cue (script kiểm tra tự động); khung motion render đúng 2 dòng.
- Tương phản màu: tính bằng script, đạt 4.5:1 cho mọi cặp chữ/nền (04).
- Font/icon: đã tải, kèm giấy phép OFL/ISC; render thử thấy dấu tiếng Việt đầy đủ, icon đúng nét (đã xem ảnh).
- Motion: đã xem khung ở 5 thời điểm (reveal đầu, giữa luồng, reveal khối 3, chốt, giữ tĩnh) — bố cục đúng; chuyển động đúng danh mục cho phép của 04; thời lượng 12,8 s đạt khổ 10–15 s.
- Thông số xuất: 1920×1080, 30 fps, H.264 + AAC (ffmpeg xác nhận trên motion_sample_S10.mp4).
- Loudness: đo bằng ffmpeg loudnorm, ghi ở mục 2; bản mẫu chưa chuẩn hoá −14 LUFS — bản toàn bộ sẽ chuẩn hoá ở bước xuất.

## 4. Chưa kiểm tra được bằng công cụ — cần người (0.4)

- Phát âm từng thuật ngữ và độ tự nhiên/biểu cảm của giọng nữ HoaiMy: AI không nghe được audio → người dùng nghe voice sample + probe và kết luận; glossary chỉ chuyển "Đã nghe" khi người dùng xác nhận.
- Độ mượt mối ghép 0,2 s trong segC (xem mục 5d).
- Cảm nhận nhịp +10%/−5% có đúng "dẫn nhanh vừa, định nghĩa chậm" hay không.

## 5. Điều chỉnh phát sinh ở bước mẫu — cần duyệt tại Cổng B

a) **Giữ phiên âm đã duyệt, chỉnh dấu câu khi tổng hợp:** voice sample dùng đúng phiên âm Cổng A ("Ếch Ti Em En", "Si Ét Ét", "Gia-vơ Sờ-críp", "Ri-ác") trong một câu liền mạch. Dịch vụ edge-tts có cửa sổ xấu vài phút từ chối gần như mọi chuỗi; dấu "…" luôn lỗi → thay ","; một số cue cần bỏ dấu câu cuối để ổn định. Đề xuất: glossary thêm cột "chuỗi TTS đã kiểm tra" (chữ hiển thị không đổi); người dùng nghe mẫu để xác nhận cách đọc.
b) **Preflight trước sản xuất toàn bộ:** chạy thử từng cue (153 cue) bằng runner retry round-robin biến thể, giãn cách 60 s; lập bảng chuỗi đã kiểm tra trước khi render. Thời gian TTS tăng đáng kể do cửa sổ xấu (đã quan sát cửa sổ xấu ~10 phút trong bước mẫu) — công bố trung thực: tổng thời gian sản xuất dài hơn ước lượng ban đầu.
c) **Nhạc nền:** chưa chọn nguồn có quyền xác minh → đề xuất mặc định KHÔNG nhạc nền cho bản nháp đầu tiên (chỉ voice), hoặc người dùng cung cấp nguồn royalty-free kèm giấy phép để ghép ở bản sau.
d) **Mối ghép trong segC:** định nghĩa ghép 2 nửa đã kiểm tra với nghỉ 0,2 s (chuỗi liền mạch lỗi ở cửa sổ thử); nếu người nghe thấy gắt, preflight sẽ tìm chuỗi liền mạch OK ở bước sản xuất. segB1 và s10a là câu liền mạch, không mối ghép.

## 6. Cách duyệt

Trả lời "Duyệt Cổng B" kèm lựa chọn cho mục 5 (a–d), hoặc liệt kê sửa đổi. Sau khi duyệt mới chạy preflight + sản xuất toàn bộ; rồi bản nháp → Cổng C.