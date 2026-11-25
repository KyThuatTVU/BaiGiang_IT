# HỒ SƠ DỰ ÁN — CỔNG A
## Video bài giảng: Bên trong một dự án phát triển phần mềm

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.3 · 18/11/2026 · Trạng thái: CỔNG A ĐÃ DUYỆT (18/11/2026); BẢN MẪU CỔNG B ĐÃ DỰNG XONG 22:12 18/11/2026 (mau/sample_draft.mp4, 41,2s) — CHỜ NGƯỜI DÙNG DUYỆT*

## 1. Tiếp nhận yêu cầu (Giai đoạn 1)

| Hạng mục | Giá trị |
| --- | --- |
| Thương hiệu | AN TECH ACADEMY — "Học công nghệ cùng An" |
| Nguồn nội dung | Noidung.docx (đã đọc toàn văn 532 đoạn; trích xuất noidung_full.txt) |
| Quy chuẩn | MASTER DESIGN & VOICE STANDARD 2.3 (bắt buộc: nhân vật giáo viên đứng giảng, hiệu ứng vẽ tay, SFX — mục XVIII) |
| Yêu cầu riêng của người dùng | ~7 phút; nội dung sinh động; hiệu ứng đẹp, chuyên nghiệp; âm thanh hiệu ứng đẹp; animation mượt, "bóng bẩy" hiểu là **trau chuốt, hoàn thiện cao**, KHÔNG phải icon nhựa 3D (quy chuẩn XII cấm phong cách bóng nhựa mặc định) |
| Đối tượng học | Sinh viên CNTT, người mới học lập trình Web; không yêu cầu kiến thức đầu vào |
| Thời lượng mục tiêu | ~7 phút (ước lượng kịch bản hiện tại 6:20–7:00; đo thật ở Cổng B) |
| Khung hình / nền tảng | 16:9 · 1920×1080 · 30 fps · MP4 H.264/AAC |
| Loudness mục tiêu | −14 LUFS, true peak ≤ −1 dBTP |
| Tài nguyên | Docx nội dung; font + bộ icon Lucide tái sử dụng từ dự án trước (cùng workspace, đã có giấy phép OFL/Lucide) |

## 2. Rút gọn nội dung cho 7 phút (bản gốc ước lượng >20 phút)

Giữ đủ mạch sư phạm: khái niệm → cơ cấu 17 vị trí → 6 giai đoạn dự án → phối hợp → công cụ → định hướng người mới → bài tập → quiz → tổng kết.

| Phần gốc | Xử lý |
| --- | --- |
| 1. Lời chào | Giữ, rút gọn còn ~30 giây |
| 2. Dự án phần mềm là gì | Giữ khái niệm + ví dụ website bán hàng; danh sách 8 chức năng rút còn 5 chức năng chính trên màn hình (đủ 8 icon, lời đọc 5) |
| 2.2–2.3 | Gộp: vì sao nhiều vị trí + phân biệt công ty/dự án, 1 cảnh |
| 3. 17 vị trí | Giữ đủ 17 vị trí; CEO/CTO/Sponsor ~35s; PM/PO/BA ~60s; 3 Lead ~12s; 8 vị trí phát triển ~85s. Bớt danh sách liệt kê dài (công nghệ FE/BE chỉ nêu đại diện) |
| 4. 6 giai đoạn | Giữ đủ 6 giai đoạn + kết quả mỗi giai đoạn; ví dụ đăng nhập (data-flow) giữ làm animation trọng tâm |
| 5. Quy trình phối hợp | Giữ chuỗi yêu cầu thanh toán (10 bước rút còn chuỗi 6 mắt xích trên màn hình) |
| 6. Công cụ | Giữ 6 công cụ (Jira, Figma, Git/GitHub, Postman, VS Code, Docker); lời đọc 5, VS Code hiện trên lưới icon |
| 7. Người mới bắt đầu | Giữ lời khuyên + 3 hướng; thêm câu "có thể đổi hướng" |
| 8. Thực hành | Giữ bài tập nhóm 8 người / website nhà hàng / 8 tuần, rút gọn |
| 9. Quiz 8 câu | **Rút còn 2 câu** (Câu 1 và Câu 5 gốc) để vừa 7 phút; 6 câu còn lại không đưa vào video |
| 10. Tổng kết | Giữ 3 ý chính + thông điệp + lời mời theo dõi |
| Nguồn ảnh tham khảo trong docx (spaceo.ca, storexio.ae…) | Không tải/dùng lại (quyền sử dụng chưa xác minh); thay bằng sơ đồ/mockup tự dựng |

## 3. Báo cáo khả thi — công cụ đã kiểm tra thật ngày 18/11/2026

| Công cụ | Kết quả kiểm tra |
| --- | --- |
| edge-tts (python -m edge_tts) | `--list-voices`: chỉ vi-VN-NamMinhNeural (nam), vi-VN-HoaiMyNeural (nữ) |
| ffmpeg 7.1 (imageio-ffmpeg) | Binary tồn tại; libx264/AAC đã xác minh ở dự án trước, dùng lại cùng binary |
| moviepy / Pillow / numpy | Import OK (Python 3.14) |
| Headless Microsoft Edge | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` tồn tại; pipeline HTML/CSS→PNG đã chạy thật ở 3 dự án trước |
| python-docx | Đọc đủ 532 đoạn |

### Làm được / làm một phần / không làm được

- **Làm được:** kịch bản–glossary–storyboard; nhân vật giáo viên SVG 2D nhất quán với cử chỉ tay/đổi tư thế theo cảnh; hiệu ứng vẽ tay (stroke reveal: gạch chân, khoanh, mũi tên, sơ đồ từng bước); sơ đồ tổ chức, data-flow đăng nhập, timeline 6 giai đoạn, mockup UI, quiz tương tác — tất cả dựng SVG/HTML/CSS có kiểm soát; SFX **tự tổng hợp** (whoosh, pop, click, tiếng bút, chime đúng) bằng numpy → không bản quyền; nhạc nền tự soạn dạng pad/pluck nhẹ, âm lượng thấp; TTS theo cue với rate riêng; phụ đề SRT đốt vào video; đo loudness/true peak.
- **Làm một phần:** diễn xuất giọng — edge-tts không SSML, chỉ rate/volume/pitch + dấu câu/ngắt câu; chuyển động là 2D/2.5D (reveal, parallax, data-flow, camera pan/zoom trên khung phẳng), **không phải 3D thật**; nhân vật là animation 2D theo tư thế (không phải rig xương đầy đủ).
- **Không làm được:** tự nghe audio để xác nhận phát âm/biểu cảm (không có công cụ nghe) → mục "Đã nghe" chỉ gán khi người dùng nghe; giọng nam miền Nam chuẩn — NamMinh thường được cảm nhận là giọng Bắc (đã gặp ở dự án HeThongGoiY/Apriori, người dùng đã chấp nhận giọng này ở các dự án đó); nhạc/SFX "đẹp" mức điện ảnh — chỉ tổng hợp được âm sạch, đơn giản, đúng thời điểm.

## 4. Quyết định [CẦN CHỐT] — đề xuất của AI, chờ người dùng duyệt

| # | Hạng mục | Đề xuất | Phương án khác |
| --- | --- | --- | --- |
| 1 | Giọng đọc | **vi-VN-NamMinhNeural (nam)** đúng mặc định 4.1; rate dẫn +5%, định nghĩa/thuật ngữ 0% (chậm hơn để rõ); disclose: chất giọng thường cảm nhận là Bắc, không phải Nam | HoaiMy (nữ) như dự án Chuyên ngành IT |
| 2 | Nhân vật giáo viên | **Bắt buộc theo 2.3**: nhân vật "An" — nam, vector phẳng 2D, áo sơ mi xanh navy + thẻ tên, kiểu tóc ngắn; nhất quán mọi cảnh; 5 tư thế (đứng giảng, chỉ trái, chỉ phải, trình bày 2 tay, suy nghĩ); cử chỉ khớp lời giảng | Không có phương án bỏ (quy chuẩn bắt buộc) |
| 3 | Phong cách | Clean flat 2D, nền sáng giấy #F6F8FB; navy #1B2A4A + xanh #2563EB (30%) + amber #F59E0B (10%); icon Lucide nét 2px; vẽ tay nét marker amber; đổ bóng rất nhẹ, không glow/neon | Nền tối (không khuyến nghị: chủ đề tổ chức/con người hợp nền sáng) |
| 4 | Nhạc nền + SFX | Nhạc nền tự soạn (pad + pluck, ~−26 LUFS dưới voice); SFX tổng hợp: bút viết, pop, whoosh, click, chime đúng, ding quiz | Không nhạc nền, chỉ SFX |
| 5 | Quiz | 2 câu (1 và 5 bản gốc), mỗi câu 2 giây chờ | Giữ 8 câu → vượt 7 phút, phải cắt phần khác |
| 6 | Nội dung cắt | Như bảng mục 2 | Giữ nguyên văn → ~20 phút |

## 5. Quy trình cổng

- **Cổng A (hiện tại):** duyệt hồ sơ + kịch bản + glossary + storyboard + art direction. Chưa render gì.
- **Cổng B:** mẫu 30–45 giây (intro + đoạn thuật ngữ + animation sơ đồ + nhân vật + vẽ tay + SFX) → duyệt voice & visual.
- **Cổng C:** bản nháp toàn video → phản hồi theo timestamp → sửa → bản cuối + bảng nghiệm thu trung thực.

## 6. Nhật ký Cổng B (18/11/2026)

- Mẫu gồm 3 cảnh / 4 cue: M1 intro (S01c2), M2 sơ đồ 4 nhóm (S04c1), M3 luồng đăng nhập (S10c1+S10c2). Cue chào mừng S01c1 chuyển về bản full: giữ 5 cue thì mẫu dài 48,7s, vượt khung 30–45s của chuẩn (riêng lời đọc đã 44,5s).
- TTS: 3/5 cue đầu fail hàng loạt (kể cả control test) → cửa sổ dịch vụ edge-tts xấu; retry giãn cách 60s với biến thể chỉ đổi dấu câu đã đủ 5/5 (S10c1 trúng ở vòng 5). Không sửa chữ đã duyệt.
- Sửa lỗi đồng bộ: lịch hiện hình đổi từ mốc giây cố định sang tỉ lệ theo độ dài cue thật; offset audio bỏ số trừ xfade (frames đệm +0,3s/c cảnh nên xfade đặt cảnh k đúng tại cumulative total); nhạc nền thêm fade in 0,6s / out 1,2s; nhân vật dời lên vạch sân khấu y=920 để không bị dải phụ đề 2 dòng che chân.
- Đo đạc thật: draft 41,17s (khung 30–45s đạt); loudness cuối −14,67 LUFS, TP −0,93 dBTP, LRA 3,6; RMS voice trong cửa sổ cue 0,10–0,115 so với khoảng lặng trước cue 0,02–0,03 (nhạc nền) → voice đặt đúng offset video; SRT 4 cue khớp offset cảnh 0 / 9,28 / 19,76 / 26,94s.
- QA thị giác: đã xem frame thật của draft tại 4,0 / 12,0 / 18,2 / 24,0 / 31,0 / 39,5s — khớp lời giảng, không chồng lấn.
- CHƯA kiểm tra: nghe thử audio (công cụ không nghe được) — phát âm, ngữ điệu, cảm xúc giọng NamMinh chờ người dùng nghe; chất giọng cảm nhận là Bắc.
## 7. Nhật ký Cổng C — bản nháp full (19/11/2026)

- File: `mau/full_draft.mp4` — 7:34,43; 1920×1080 30fps H.264; AAC 48 kHz mono 173 kbps; 27 MB. Phụ đề: `mau/full.srt` (44 cue), text đầy đủ: `mau/full_timeline.json`.
- Voice: 44/44 cue, vi-VN-NamMinhNeural. 4 cue bị dịch vụ từ chối suốt 4 vòng retry (S05c3, S11c1, S15c2, S17c1) được ghép từ 2–3 cụm ngắn cùng giọng, khoảng lặng 0,18s giữa cụm — có thể nghe hơi gãy nhịp ở các mối nối.
- Loudness cuối: **−15,0 LUFS** (chuẩn −14 ±1), TP **−1,13 dBTP** (≤ −1), LRA 2,9. Mix voice+SFX peak 0,918 trước chuẩn hoá.
- Sửa trong QA: dải phụ đề dài trước chỉ hiện 2 dòng đầu → paging 2 dòng theo tiến độ cue; S02 giá/nhãn; S03 chip dự án; S06 nhãn "PM xử lý"; S07 backlog; S10 nhóm công nghệ backend; S13 (sửa lần 2) dòng sáu giai đoạn trước đây chỉ hiện ở cue 2, để trống ~6s → nay hiện dần ngay từ cue 1; S14 xếp lại hàng relay; S17 outro tắt dần chip trước logo.
- QA thị giác trên file cuối: frame tại 32 / 141 / 263 / 292 / 352 / 435s — phụ đề khớp lời, không chồng lấn; S13 tại 292s xác nhận đã hết nhịp trống.
- CHƯA kiểm tra (không có công cụ nghe): phát âm thuật ngữ, ngữ điệu/cảm xúc NamMinh, độ hoà nhạc nền, tiếng pop/whoosh thực tế. Chưa thử phát trên thiết bị/di động. Một số phụ đề rút gọn (ví dụ S15c2 bỏ "khi tích lũy thêm kiến thức", "để") — chủ ý.
