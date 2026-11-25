# 06 — Bản nháp Cổng C (chờ duyệt)

Ngày gửi: 12/11/2026 · Dự án: Bài giảng "Các chuyên ngành IT" · AN TECH ACADEMY
Quy trình: MASTER DESIGN & VOICE STANDARD 2.2 — Giai đoạn 6→7 (Cổng C). **Dừng tại đây chờ người dùng duyệt; chưa bàn giao bản cuối.**

## 1. Bản nháp và thông số xuất (đã đo bằng ffmpeg/loudnorm)

| Hạng mục | Giá trị đo được |
| --- | --- |
| File nháp | `mau/full/draft.mp4` (21,9 MB) |
| Thời lượng | 666,43 s ≈ 11 phút 06 giây (153 cue / 34 cảnh) |
| Khung hình | 1920×1080, 30 fps, H.264 (yuv420p), AAC 192 kbps 48 kHz |
| Loudness | −14,41 LUFS · true peak −1,37 dBTP · LRA 3,9 (mục tiêu −14 / ≤−1: đạt) |
| Chuyển cảnh | crossfade fade 300 ms × 33 ranh giới, nhất quán toàn video |
| Phụ đề | đốt vào video (dải ≤2 dòng × ≤42 ký tự) + `mau/full/full_video.srt` rời, 153 mục |
| Đồng bộ | ranh giới cảnh khớp tuyệt đối audio–video; onset trong cảnh lệch ≤32 ms (lượng hoá centisecond của ffmpeg); stream audio dài hơn video 0,08 s do padding AAC (nằm trong đuôi im lặng) |
| Nhạc nền / SFX | không dùng (quyết định Cổng B: chưa xác minh quyền) |

Kiểm tra máy (`tools/qa.py` → `mau/full/qa_report.json`): specs ✓, loudness ✓, A/V ✓, SRT–manifest–timeline ✓ (153/153, không overlap, không lọt nhãn), đếm frame 34 cảnh ✓, cỡ chữ nhỏ nhất 28 px ✓. **ALL_OK.**

Frame đối chứng trích từ chính draft: `mau/full/qa_frames/` (mid_S05, mid_S16, mid_S30, mid_S34, xfade_S12_S13, xfade_true_mid).

## 2. Checklist §10 (Đạt / Chưa đạt / Chưa thể xác minh)

### A. Nội dung và sư phạm
- Đạt — kiến thức đã duyệt Cổng A; mục tiêu học tập đo được (00_HoSoDuAn).
- Đạt — giải thích bản chất + ví dụ (S10 gợi ý sản phẩm, S24 parallax mạng, S16 cầu nối HTTT); mô phỏng đúng ngữ cảnh.
- Đạt — phiên bản công nghệ + ngày kiểm tra ghi trong 00/01; demo không chứa mật khẩu/khoá API/dữ liệu thật; pentest chỉ trong phạm vi cho phép (thẻ quy tắc S14).
- Đạt — tổng kết S32 + câu hỏi củng cố S30/S33.

### B. Phát âm và giọng đọc
- Đạt — Glossary dự án duyệt Cổng A (02_Glossary_DuAn); giọng nữ vi-VN-HoaiMyNeural, dẫn +10%, định nghĩa −5%.
- Đạt (máy) — nhãn diễn xuất/chữ phiên âm không lọt phụ đề; text TTS = đúng chữ kịch bản (2 cue chỉ đổi dấu câu, mục 4).
- **Chưa thể xác minh** — nghe kiểm tra phát âm thuật ngữ, biểu cảm, nuốt chữ/trọng âm: AI không tự nghe được (§0.4, §9). Cần tai người nghe draft, đặc biệt các thuật ngữ glossary (Ba Đê, AI, API, Node.js, React…).

### C. Hình ảnh và chuyển động
- Đạt — 34 cảnh khác bố cục (card/chu trình/bản đồ/parallax/phone/outro); đã xem frame đại diện mọi cảnh + frame draft.
- Đạt — sơ đồ đúng nội dung duyệt; không chữ méo; icon cùng bộ Lucide 1.72.0 nét 1.6; không bóng nhựa/3D giả; không dùng hình AI.
- Đạt — bảng màu giới hạn theo chuyên ngành, tương phản tính ở 04 §4; reveal ≤200 ms, giữ tĩnh ≥1,5 s sau sơ đồ; S30 nghỉ 3 s thật.

### D. Thương hiệu và trình bày
- Đạt — wordmark AN TECH ACADEMY + tagline (S02/S34); intro cold open, outro đúng khung.
- Đạt — font nhất quán (Plus Jakarta Sans / Be Vietnam Pro / JetBrains Mono); chữ nhỏ nhất 28 px (đã sửa mockup phone 20→28 px, mục 4).
- Đạt — vùng an toàn 5%; dải phụ đề không che nội dung.

### E. Âm thanh và phụ đề
- Đạt — loudness đo đạt mục tiêu; không clipping (TP −1,37); không nhạc nên không có vấn đề voice/nhạc.
- Đạt (văn bản + đồng bộ đo) — phụ đề đúng chữ kịch bản/TTS, .srt khớp timeline ≤32 ms. **Chưa thể xác minh**: đối chiếu bằng tai lần cuối.

### F. Quy trình và bản quyền
- Đạt — Cổng A duyệt 12/11, Cổng B duyệt 12/11 (00 §8); Cổng C đang chờ.
- Đạt — nhật ký tài sản 04 §7 đầy đủ: font SIL OFL, icon ISC pinned 1.72.0, không nhạc/SFX, không logo bên thứ ba, không hình AI.
- Đạt — giới hạn còn lại liệt kê tại mục 5.

## 3. Việc đã kiểm tra bằng máy (tuyên bố đúng phạm vi §0.4)

specs/loudness/đồng bộ/SRT/frame/cỡ chữ: đo thật, kết quả mục 1. Phát âm/biểu cảm: **chưa** kiểm tra bằng tai — không tuyên bố đạt.

## 4. Sửa lỗi trong sản xuất (đã áp dụng vào draft)

| Vị trí | Lỗi | Cách sửa |
| --- | --- | --- |
| S30 (nền tối) | dải phụ đề trong suốt bị hỏng alpha → nền trắng chữ trắng | fill đặc (30,41,59) cho cảnh tối |
| S05 / S29 / S13 / S16 / S33 | chữ cắt/thiếu, connector lệch | nới rộng sprite, auto-fit nhãn, chỉnh toạ độ |
| S01 / S10 | tiêu đề mockup phone 20 px < MUST 28 px | nâng 28 px + nới khung phone |
| TTS S20c4 / S25c1 | service không trả audio với text gốc | biến thể dấu câu (thêm/bớt dấu phẩy cuối); giữ nguyên từng chữ |
| Toàn video | audio dài hơn timeline 0,65 s (padding MP3) | cắt đuôi im lặng mỗi cảnh đúng timeline; khớp tuyệt đối |
| Toàn video | TP −0,77 sau AAC (vượt −1) | loudnorm TP đích −1,5 chừa headroom → −1,37 |

Không còn lỗi máy phát hiện trên draft. Lỗi nghe/nhìn thêm (nếu có) ghi theo mẫu: timestamp — mô tả — cách sửa.

## 5. Giới hạn còn tồn tại (thông báo trung thực)

1. AI không nghe được audio: phát âm thuật ngữ, biểu cảm, ngắt nghỉ cần người nghe xác nhận ở Cổng C.
2. Onset phụ đề trong cảnh lệch tối đa 32 ms so với voice (không nhận biết được bằng mắt/thường); ranh giới cảnh khớp tuyệt đối.
3. Không nhạc nền/SFX theo quyết định Cổng B (chưa xác minh quyền) — chủ đích, không phải thiếu sót.
4. Icon "briefing" không tồn tại trong Lucide 1.72.0 → thay briefcase (ghi nhật ký).
5. Mẫu Cổng B (S10) còn tiêu đề phone 20 px; bản toàn bộ nâng 28 px để đúng MUST §2.2 — lệch nhỏ so với mẫu đã duyệt, chủ đích tuân thủ.
6. Hai cue TTS dùng biến thể dấu câu; ngữ điệu cuối câu có thể khác nhẹ bản đọc lý tưởng.

## 6. Chờ duyệt Cổng C

Xem `mau/full/draft.mp4` (kèm .srt nếu cần). Phản hồi theo timestamp giúp sửa đúng chỗ; phần đã duyệt không sửa tùy tiện. Sau khi duyệt → Giai đoạn 8: bàn giao bản cuối + thông số xuất + .srt + glossary + nhật ký tài sản + checklist.