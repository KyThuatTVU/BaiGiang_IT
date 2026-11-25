# Giọng đọc — phương án dùng để xuất bản (2026-11-22)

## 1. Quyết định

Theo yêu cầu “dùng giọng như bình thường để làm video”, bản full dùng **Microsoft Edge TTS `vi-VN-NamMinhNeural`**, **không chỉnh pitch**, tốc độ theo từng cue (+8% đến +15%).

Đây là **fallback có ghi nhận**, không phải giọng nam Nam Bộ thật:
- Nguồn phát là tiếng Việt phổ thông (giọng Bắc), không phải Nam Bộ.
- Không dùng pitch-shift để giả giọng Nam.
- Giọng đọc ít nhấn nhá/hiếm cảm xúc hơn giọng người; chưa có bản thu người để so sánh.

Các hướng đã loại: Viettel `hcm-minhquan` (đúng giọng Nam nhưng demo hết lượt, API cần token — đã dừng), thu giọng người thật (người dùng không chọn thu file), FPT (không có nam Nam), V-TTS (CC BY-NC).

## 2. Sản xuất audio

- 29 cue / 12 cảnh; `tools/tts.py --no-shift` tạo MP3 từ manifest (rate +8…+15%, không pitch).
- Edge chèn im lặng cuối cue; `tools/trim_voices.py` cắt im lặng đầu/cuối (−45 dB, đệm 0,12 s), xuất WAV 48 kHz mono, cập nhật `tts_state.json`.
- Nói sau khi cắt: **281,4 s**; timeline video: **303,2 s (5:03,2)**, đạt 4:45–5:15.
- Mix: `tools/audio_full.py --tag full` (voice + SFX + nhạc nền, không dùng nhạc có bản quyền). Peak mix 0,818; loudness mix −19,9 LUFS, TP −1,75 dBFS.
- Ghép: xfade 12 cảnh (0,6 s chuyển cảnh) → `full_video.mp4` 5:03,20; `tools/mux_full.py` chuẩn hóa loudness + limiter rồi mux. **Kết quả đo bản cuối: −14,47 LUFS, TP −1,81 dBFS** (đạt ngưỡng TP ≤ −1).
- Phụ đề: `mau/full.srt` (29 cue), khớp timeline sau khi cắt.

## 3. Kiểm tra

- Đã kiểm tra: đủ 29 file, state đủ 29, SRT 29 cue, tổng thời lượng 5:03, mix không clipping.
- **Chưa xác minh bằng tai**: phát âm thuật ngữ, ngữ điệu, độ tự nhiên, nhất quán — công cụ không nghe thay người. Cần người nghe duyệt trước khi phát hành.
- Bản thu người (nếu sau này cần) vẫn dùng được bộ `mau/voice_human/script_thu.html` và `tools/voice_human_prep.py`; hiện chưa có file thu.
- Audio NamMinh cũ có pitch đã chuyển vào `mau/audio/legacy_namminh/`, không dùng.
