# HỒ SƠ DỰ ÁN — CỔNG A

## 1. Thông tin bài giảng

| Mục | Nội dung |
|---|---|
| Kênh | An Tech Academy — "Học công nghệ cùng An" |
| Chủ đề | Bảo vệ mã nguồn & kiểm soát truy cập ứng dụng web |
| Nguồn nội dung | `Noidung.docx` (bài "Web Shield") — bám đúng thuật ngữ, đoạn code, luồng xử lý |
| Thời lượng mục tiêu | 5:00 – 5:30 (12 cảnh, 24 cue thoại) |
| Định dạng | 1920×1080, 30 fps, H.264 + AAC 48 kHz, loudness −14 LUFS / TP −1 dB |
| Giọng | `vi-VN-NamMinhNeural`, tăng tốc 5–10% theo cue, nhấn nhá bằng pause + pitch shift nhẹ |
| Nhân vật | Giáo viên An — vector phẳng 2D cố định, đứng dạy suốt video (7 tư thế, mấp máy môi) |
| Hình ảnh từ file gốc | Dùng đủ 8/8 ảnh nhúng trong `Noidung.docx` |

## 2. Mục tiêu học tập

1. Nhận diện rủi ro lộ mã nguồn/cấu trúc thư mục qua DevTools & URL trực tiếp.
2. Hiểu vai trò Apache và tệp `.htaccess` khi bật `AllowOverride`.
3. Áp dụng `Options -Indexes`, `Require all denied`, `FilesMatch` đúng ngữ cảnh.
4. Phân biệt rewrite nội bộ và redirect 301; viết `RewriteRule` cơ bản.
5. Hiểu Front Controller + whitelist routing; tách `public/` – `private/` với `DocumentRoot`.

## 3. Phân bổ cảnh (đã chốt)

| Cảnh | Nội dung | Ảnh gốc | Thời lượng dự kiến |
|---|---|---|---|
| S01 | Hook: "gõ vài chữ thấy bộ đồ lòng website" | image1 | ~28 s |
| S02 | DevTools → tab Network | image5 | ~27 s |
| S03 | Rủi ro lộ thư mục nội bộ | image6 | ~40 s |
| S04 | Apache & `.htaccess` | image2 | ~30 s |
| S05 | `Options -Indexes` + `Require all denied` → 403 | image7 | ~33 s |
| S06 | `FilesMatch` theo phần mở rộng | — | ~27 s |
| S07 | URL Rewrite vs Redirect 301 | image8, image3 | ~33 s |
| S08 | Front Controller — một cửa `index.php` | image4 | ~36 s |
| S09 | Whitelist routing → 404 | — | ~25 s |
| S10 | Kiến trúc public/private + DocumentRoot | — | ~32 s |
| S11 | Tóm 3 ý + quiz | — | ~30 s |
| S12 | Outro, CTA | — | ~20 s |

## 4. Quy trình 3 cổng

| Cổng | Nội dung | Trạng thái |
|---|---|---|
| A | Kịch bản, glossary, storyboard, art direction (5 tài liệu trong thư mục này) | Hoàn tất, trình duyệt |
| B | Mẫu 30–45 giây (giọng + hình) để duyệt cảm giác | Gộp vào bản nháp đầy đủ theo yêu cầu "làm bài giảng ~5 phút" của người dùng |
| C | Bản nháp đầy đủ → góp ý có timestamp → bản cuối | Chờ |

## 5. Giới hạn năng lực — công bố trước (bắt buộc)

- **Giọng đọc**: edge-tts chỉ điều khiển được `--rate`; tham số `--pitch` lỗi `NoAudioReceived` trên máy này. Cảm xúc thực hiện bằng: tốc độ từng câu, khoảng nghỉ, và dịch cao độ hậu kỳ bằng ffmpeg (±0,2–0,7 semitone). Đây **không phải** TTS biểu cảm thật; không thể cam kết "giống người thật 100%".
- **Không nghe được audio**: người dựng không có khả năng nghe/kiểm âm. Mọi nhận định về độ truyền cảm, ngắt nghỉ, phát âm là **chưa kiểm chứng bằng tai**; chỉ kiểm bằng văn bản thay thế (glossary) và thời lượng file.
- **Dịch vụ TTS không ổn định**: edge-tts trả rỗng nhiều lần; có retry 5 vòng, đổi dấu câu. Các cue có thể lệch tông rất nhẹ giữa lần ghép — cần người nghe xác nhận ở Cổng C.
- **Hình ảnh**: 8 ảnh gốc được đặt trong khung thống nhất + chú thích + nét bút dạ; không tạo ảnh AI mới, không dùng icon 3D nhựa. Hình minh hoạ UI (browser, code panel) là vector tự dựng, không phải ảnh chụp thật.
- **Nội dung kỹ thuật**: code minh hoạ rút gọn từ tài liệu gốc; đúng cú pháp Apache/PHP nhưng là ví dụ giảng dạy, chưa chạy thử trên XAMPP trong khuôn khổ dự án này.

## 6. Rủi ro & phương án

| Rủi ro | Ảnh hưởng | Xử lý |
|---|---|---|
| TTS fail kéo dài | Trễ tiến độ | Retry + variant dấu câu; đã sinh đủ 24/24 trước khi render audio |
| Tổng thời lượng vượt 5:30 | Sai yêu cầu | Rate theo cue; nếu vượt sẽ cắt cue phụ, không cắt nội dung lõi |
| Chữ trên hình nhỏ khi xem mobile | Khó đọc | Cỡ chữ tối thiểu 19–20 px ở 1080p, phụ đề 2 dòng |
| Phát âm thuật ngữ sai | Mất uy tín | Glossary thay thế phiên âm; người dùng duyệt ở Cổng B/C |

## 7. Cấu trúc thư mục

```
Biagiang_baomatmanguon/
├─ Noidung.docx, image1..8.jpeg      # nguồn gốc
├─ 00..04_*.md                        # hồ sơ Cổng A (tài liệu này)
├─ assets/fonts, assets/icons*        # font + icon Lucide
├─ tools/                             # pipeline: core, character, sfx,
│                                     #   make_manifest, tts, scenes_web,
│                                     #   render_full, audio_full, assemble_full
└─ mau/                               # manifest, audio, frames, scene_mp4, probe, log
```
