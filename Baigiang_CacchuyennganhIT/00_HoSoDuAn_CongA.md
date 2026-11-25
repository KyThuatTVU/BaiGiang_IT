# HỒ SƠ DỰ ÁN — CỔNG A
## Video bài giảng: Khám phá các chuyên ngành CNTT — đâu là con đường dành cho bạn?

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.2 · 12/11/2026 · Trạng thái: CỔNG A ĐÃ DUYỆT (12/11/2026) — đang tạo bản mẫu Cổng B*

## 1. Tiếp nhận yêu cầu (Giai đoạn 1)

| Hạng mục | Giá trị |
| --- | --- |
| Thương hiệu | AN TECH ACADEMY |
| Nguồn nội dung | NoidungcacchuyennganhIT.docx (người dùng cung cấp, đã đọc toàn văn) |
| Quy chuẩn áp dụng | MASTER DESIGN & VOICE STANDARD 2.2 (bản mới, tự đủ; không kế thừa quy tắc/dự án cũ theo yêu cầu người dùng) |
| Đối tượng học | Học sinh, sinh viên, người đang tìm hiểu ngành CNTT; kiến thức đầu vào: không yêu cầu |
| Thời lượng mục tiêu | ~7 phút (ước lượng hiện tại 6:30–6:55; đo thật ở bước mẫu) |
| Khung hình / nền tảng | 16:9 · 1920×1080 · 30 fps · MP4 H.264/AAC (đề xuất YouTube) |
| Loudness mục tiêu | −14 LUFS, true peak ≤ −1 dBTP (đề xuất 6.1) |
| Tài nguyên người dùng cung cấp | File nội dung docx; chưa có logo, nhạc, voice chỉ định |

## 2. Báo cáo khả thi — công cụ đã kiểm tra thật ngày 12/11/2026

| Công cụ | Phiên bản / đường dẫn | Đã kiểm tra bằng cách nào |
| --- | --- | --- |
| TTS edge-tts | 7.3.1, chạy `python -m edge_tts` (Python 3.14.4) | `--list-voices`: chỉ có vi-VN-NamMinhNeural (nam), vi-VN-HoaiMyNeural (nữ) |
| ffmpeg | 7.1 (binary imageio-ffmpeg trong site-packages Python) | `-version`, `-encoders`: có libx264 và AAC |
| moviepy / Pillow / numpy | 2.2.1 / 11.3.0 / 2.4.4 | `pip list` |
| Dựng khung hình HTML/CSS → PNG | Headless Microsoft Edge | Xuất thử khung 1920×1080 và đã xem ảnh kết quả |
| Tải font | Google Fonts reachable | HTTP 200, trả 3 URL font cho Be Vietnam Pro |
| Xem trước tương tác | browser-use MCP | có sẵn trong phiên |

### Làm được / làm một phần / không làm được (0.4)

- **Làm được:** nghiên cứu–kịch bản–glossary–storyboard; sơ đồ/mockup/icon tự dựng SVG/HTML/CSS; TTS tiếng Việt theo phân đoạn với rate riêng; ghép video, chuyển cảnh, highlight, data-flow bằng chuỗi khung PNG + ffmpeg; phụ đề .srt + đốt phụ đề; đo loudness/true peak bằng ffmpeg; kiểm tra tương phản màu bằng script (đã làm).
- **Làm một phần:** diễn xuất giọng — edge-tts không nhận SSML, chỉ điều khiển rate/volume/pitch theo đoạn + dấu câu/ngắt câu; không thể hứa "diễn xuất chuyên nghiệp". Chuyển động — reveal/flow/parallax 2D làm được; morph, 3D thật, camera 3D thì không. Đồng bộ phụ đề — đối chiếu bằng công cụ (đo thời lượng audio, waveform) nhưng rà cuối vẫn cần người.
- **Không làm được:** nghe audio để tự xác nhận phát âm/biểu cảm (không có công cụ nghe); đảm bảo giọng nam miền Nam bằng edge-tts (voice nam duy nhất là NamMinh, thường được cảm nhận là giọng Bắc); dùng nhạc khi chưa xác nhận quyền.

### 2b. Giới hạn vận hành edge-tts (phát hiện thật 12/11/2026, ~80 phép thử) + quy ước tổng hợp

- **Breaker nhất quán:** dấu "…" → `NoAudioReceived` ở mọi thời điểm → thay bằng "," khi tổng hợp.
- **Phần còn lại là cửa sổ thời gian của service:** có các cửa sổ "xấu" vài phút mà gần như mọi chuỗi lỗi (kể chuỗi từng OK), xen cửa sổ "tốt" mà hầu hết chuỗi OK. Bằng chứng: "Sờ-críp" hoa lỗi suốt 14:16–14:46 nhưng OK lúc 14:49; "sờ" thường OK 14:38 nhưng lỗi 14:49. Các kết luận trung gian ("breaker cứng theo từng chuỗi", "văn bản dài gây lỗi", "chặn theo nhịp gọi") đều đã bị bác bỏ bằng phép thử đối chứng; chuỗi dài ~230 ký tự OK (test_long).
- **Quy ước tổng hợp:** theo từng câu/cue; runner retry round-robin biến thể (giữ nguyên chữ, bỏ dấu câu cuối, hoa/thường phiên âm, chính tả Anh) giãn cách 60 s để vượt cửa sổ xấu; khoảng nghỉ chèn bằng ffmpeg; không retry mù một chuỗi trong cửa sổ xấu.
- **Hệ quả sản xuất:** preflight thử 153 cue trước khi render toàn bộ, lập bảng "chuỗi TTS đã kiểm tra" bổ sung vào 01; thời gian TTS tăng đáng kể do cửa sổ xấu — công bố ở Cổng B.
- Số đo nhịp thực tế (đo ffmpeg trên voice sample, đếm âm tiết = token tách khoảng trắng, token phiên âm gạch nối đếm từng phần):

| Phân đoạn | Rate | Thời lượng (s) | Số âm tiết | Âm tiết/giây |
| --- | --- | --- | --- | --- |
| segA1 (chào) | +10% | 8,18 | 30 | 3,67 |
| segA2 (dẫn) | +10% | 6,43 | 27 | 4,20 |
| segB1 (thuật ngữ FE) | −5% | 5,95 | 17 | 2,86 |
| segB2 (thuật ngữ BE) | −5% | 7,03 | 20 | 2,84 |
| segC (định nghĩa) | −5% | 8,59 (lời 8,39) | 21 | 2,50 |
| **voice_sample tổng** | | **28,82** | 94 | 3,41 (trung bình phần lời) |

- Loudness mẫu (chưa chuẩn hoá): voice_sample −18,85 LUFS / −2,42 dBTP; motion_sample −18,50 LUFS / −2,93 dBTP. Bản toàn bộ sẽ chuẩn hoá −14 LUFS / −1 dBTP ở bước xuất.

## 3. Quyết định [CẦN CHỐT] — đề xuất của AI, chờ người dùng duyệt

| # | Hạng mục | Đề xuất | Ghi chú / phương án khác |
| --- | --- | --- | --- |
| 1 | Giọng đọc | **ĐÃ CHỐT 12/11/2026: vi-VN-HoaiMyNeural (nữ, edge-tts)** — người dùng chọn rõ "giọng nữ Việt Nam", xác nhận lệch mặc định nam miền Nam của 4.1 | Khóa cho series: edge-tts 7.3.1 · voice vi-VN-HoaiMyNeural · rate dẫn +10% (≈1,1×), định nghĩa/thuật ngữ −5% (≈0,95×); số đo âm tiết/giây thực tế ghi ở mục 2b sau khi đo mẫu |
| 2 | Nhân vật dẫn chuyện | Không dùng | Đúng mặc định 5.4 |
| 3 | Quicksand | Bỏ; wordmark dùng Plus Jakarta Sans Bold | Giữ 3 font theo 2.1 |
| 4 | Bộ icon | Lucide (ISC) | Thay thế: Phosphor/Tabler |
| 5 | Bảng màu | Như 04_ArtDirection_BangMau.md (đã tính tương phản) | Màu thương hiệu đề xuất #2563EB |
| 6 | Công cụ TTS + dựng | edge-tts + HTML/PNG + ffmpeg/moviepy | Như mục 2 |
| 7 | Khung hình / nền tảng | 16:9 1080p30, YouTube | Đổi nếu người dùng muốn nền tảng khác |
| 8 | Nhạc nền | Instrumental royalty-free, ducking −20 dB; nguồn chốt ở Cổng B kèm giấy phép | Nếu chưa có quyền: không nhạc |
| 9 | Thay đổi so với docx gốc | Intro 55 s → ~35 s (cold open + chào + mục tiêu); thêm mục tiêu đo được S03, câu hỏi tự kiểm tra dừng 3 s S30, cảnh nhấn ủy quyền pentest S14; rút gọn vài câu cho khổ phụ đề | Giữ toàn bộ ý và thứ tự 6 chuyên ngành của docx; chi tiết ở ghi chú cuối 01_KichBan_BaCot.md |

## 4. Mục tiêu học tập (7.2 — đo được)

Sau video, người học có thể:
1. **Phân biệt** 6 nhóm chuyên ngành CNTT theo vai trò cốt lõi (kiểm tra bằng bảng ánh xạ S29).
2. **Kể tên** ít nhất 2 vị trí nghề nghiệp và 2 công nghệ tiêu biểu của mỗi nhóm.
3. **Tự ghép** sở thích cá nhân với một nhóm chuyên ngành phù hợp (điểm dừng S30).
4. **Nêu** nguyên tắc "kiểm thử xâm nhập chỉ trong phạm vi được cho phép" và 3 hành trang học tập (nền tảng, thực hành, học hỏi liên tục).

Mật độ: mỗi cảnh một ý chính; ≤ 3–4 khái niệm mới mỗi 5 phút (mỗi chuyên ngành ~50 s gồm định nghĩa + ví dụ + nghề nghiệp).

## 5. Dàn ý và phân bổ thời gian (ước lượng)

| Phần | Cảnh | Thời gian | Nội dung |
| --- | --- | --- | --- |
| 1. Mở đầu | S01–S03 | 0:00–0:35 | Cold open, chào + thương hiệu, mục tiêu + bản đồ 6 nhóm |
| 2. Sáu chuyên ngành | S04–S27 | 0:35–5:35 | Mỗi nhóm ~50 s: định nghĩa → ví dụ/luồng → nghề nghiệp + công nghệ → hợp với ai |
| 3. Chọn chuyên ngành | S28–S31 | 5:35–6:25 | Không có "tốt nhất"; ánh xạ sở thích; tự kiểm tra 3 s; đừng chọn chỉ vì lương |
| 4. Tổng kết + outro | S32–S34 | 6:25–7:00 | 3 hành trang; câu hỏi mở + khuyến khích; chào thương hiệu |

## 6. Ghi chú chính xác chuyên môn (7.3, 7.4)

- Phân loại đã rà ngày 12/11/2026 (kiến thức ổn định, không phụ thuộc phiên bản): JavaScript/Java/PHP/Python/C#/C++ là ngôn ngữ; SQL là ngôn ngữ truy vấn; HTML là chuẩn đánh dấu, CSS là chuẩn định kiểu; Node.js là runtime; React, Pandas, Scikit-learn là thư viện; TensorFlow, PyTorch là framework; Unity, Unreal Engine là game engine; Blender là phần mềm 3D. Kịch bản và chip trên màn hình không gọi chung các nhóm này là "ngôn ngữ".
- Video không dạy phiên bản cụ thể của công nghệ nào → không cần chốt phiên bản; nếu bản sửa thêm nội dung phụ thuộc phiên bản sẽ đối chiếu nguồn chính thức và ghi ngày kiểm tra.
- Không số liệu/benchmark/mức lương tự đặt; ví dụ là minh họa định tính có ghi chú trong kịch bản.
- An toàn: không demo code thật, không khóa/mật khẩu/dữ liệu thật; pentest chỉ mô tả khái niệm + nhấn phạm vi được cho phép (S14).

## 7. Giới hạn còn tồn tại (thông báo trung thực theo 0.4)

1. Audio mẫu (voice sample, probe chức danh, audio S10 cho motion sample) được tạo ở giai đoạn 3; phát âm/biểu cảm vẫn chờ người nghe xác nhận — AI không nghe được audio.
2. AI không nghe được audio → phát âm và biểu cảm bắt buộc người nghe kiểm tra sau render; trạng thái glossary "Đã nghe" chỉ do người gán.
3. Giọng đã chốt là **nữ (HoaiMy)** theo lựa chọn rõ ràng của người dùng ở Cổng A — lệch mặc định nam miền Nam của 4.1 đã được xác nhận; không còn là giới hạn mở.
4. Diễn xuất TTS giới hạn ở rate + dấu câu; không tuyên bố diễn xuất chuyên nghiệp.
5. Thời lượng và đồng bộ phụ đề hiện là ước lượng từ số âm tiết (1.713 âm tiết, 153 cue); chốt sau khi đo audio.
6. Chuyển động là 2D reveal/flow dựng bằng chuỗi khung; không morph/3D thật.
7. Font đã tải 12/11/2026 (Plus Jakarta Sans var, Be Vietnam Pro 4 weight, JetBrains Mono var; giấy phép OFL kèm trong assets/fonts/) và đã render thử thành công; icon Lucide 1.72.0 (ISC) đã tải — xem nhật ký tài sản ở 04.

## 8. Quy trình còn lại (mục 8)

- **Cổng A: ĐÃ DUYỆT 12/11/2026** (người dùng: "Duyệt Cổng A, chọn giọng nữ Việt Nam"). Kịch bản, glossary, storyboard, bảng màu và các quyết định mục 3 được duyệt; glossary chuyển trạng thái "Đã duyệt".
- **Giai đoạn 3 – bản mẫu:** voice sample 20–30 s (intro + đoạn thuật ngữ); style frames (cảnh icon, cảnh sơ đồ, cảnh typography + bảng màu, mood board đúng/sai); motion sample 10–15 s (reveal sơ đồ + data-flow).
- **Cổng B: ĐÃ DUYỆT 12/11/2026** (người dùng: "Duyệt Cổng B, chạy preflight và sản xuất toàn bộ"). Chấp nhận 4 mặc định: giữ phiên âm như mẫu; preflight 153 cue; không nhạc nền; chấp nhận mối ghép 0,2 s segC. Hồ sơ chốt: voice vi-VN-HoaiMyNeural, rate +10%/−5%, icon Lucide 1.72.0, font OFL, bảng màu 04, loudness đích −14 LUFS/−1 dBTP.
- **Giai đoạn 5–6:** sản xuất toàn bộ theo storyboard; xuất bản nháp; kiểm tra theo checklist mục 10, ghi lỗi theo timestamp.
- **Cổng C: ĐÃ GỬI BẢN NHÁP 12/11/2026 — CHỜ DUYỆT.** Draft `mau/full/draft.mp4` (666,43 s; −14,41 LUFS/−1,37 dBTP); hồ sơ + checklist §10 + giới hạn: 06_BanNhap_CongC.md; kiểm tra máy ALL_OK (mau/full/qa_report.json). Phát âm/biểu cảm chờ tai người nghe.
- **Giai đoạn 8 – bàn giao:** MP4 cuối + thông số xuất, .srt rời, glossary đã chốt, nhật ký tài sản, danh sách hạng mục đã kiểm tra, giới hạn còn lại.

## 9. Danh mục hồ sơ Cổng A

| File | Nội dung |
| --- | --- |
| 00_HoSoDuAn_CongA.md | File này: yêu cầu, khả thi, quyết định chờ chốt, mục tiêu, dàn ý, giới hạn |
| 01_KichBan_BaCot.md | Kịch bản 3 cột, 34 cảnh / 153 cue phụ đề, ghi chú thay đổi so với docx |
| 02_Glossary_DuAn.md | 72 thuật ngữ, cách đọc đề xuất + nguồn, chính sách phiên âm |
| 03_Storyboard.md | Shot list 7 cột cho 34 cảnh, tự rà theo 5.8 |
| 04_ArtDirection_BangMau.md | Phong cách, font, icon, bảng màu + tương phản đã tính, chuyển động, nhật ký tài sản |

**Cách duyệt:** trả lời "Duyệt Cổng A" kèm lựa chọn cho mục 3 (đặc biệt dòng 1 về giọng), hoặc liệt kê sửa đổi theo mã cảnh / mục từ. Sau khi duyệt, AI mới tạo bản mẫu voice + visual.