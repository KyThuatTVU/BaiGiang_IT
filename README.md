# Video bài giảng — Cơ sở dữ liệu và ứng dụng trong thực tế

Dự án video giáo dục 16:9 (1920×1080, 25 fps) được dựng hoàn toàn bằng HTML/CSS/SVG + engine
render theo từng khung hình, thuyết minh tiếng Việt, nhạc nền và hiệu ứng sinh bằng code.
Không dùng slideshow ảnh tĩnh: mỗi cảnh có chuyển động, gõ SQL theo từng ký tự, sơ đồ ERD
hiện dần, bảng kết quả truy vấn và phụ đề đồng bộ theo cue.

## Nội dung

| Phần | Chủ đề | Cảnh |
|---|---|---|
| Mở đầu | Tiêu đề, mục tiêu bài học | intro, objectives |
| 1 | CSDL là gì, dữ liệu vs thông tin, vì sao cần CSDL, DBMS | 6 cảnh |
| 2 | Bảng/dòng/cột, khóa chính, khóa ngoại | 3 cảnh |
| 3 | Quan hệ 1—1, 1—N, N—N | 3 cảnh |
| 4 | Thực thể/thuộc tính/quan hệ, phân tích, ERD cửa hàng | 3 cảnh |
| 5 | Năm nhóm lệnh SQL, CREATE TABLE, INSERT/SELECT | 3 cảnh |
| 6 | 6 bài toán truy vấn trên dữ liệu cửa hàng | 7 cảnh |
| 7 | Tổng kết, 5 câu trắc nghiệm, lời kết | 3 cảnh |

Tài liệu chi tiết:

- [Nội dung bài giảng](docs/noi-dung-bai-giang.md)
- [Storyboard & danh sách hình ảnh](docs/storyboard.md)
- [Dữ liệu & ERD](docs/du-lieu-erd.md)
- [Lời thoại đầy đủ](docs/loi-thoai.md)
- [Kiểm tra thuật ngữ, SQL, nhất quán](docs/qa-kiem-tra.md)
- Phụ đề: `build/captions.srt`

## Cấu trúc dự án

```
src/
  index.html          trang render 1920×1080
  styles.css          hệ thống hình ảnh (navy/cyan, font, bảng, ERD, quiz…)
  app.js              engine cảnh + đồ họa động, gọi window.renderFrame(t)
  timeline.js         timeline sinh tự động (window.__TIMELINE)
  data/script.mjs     kịch bản 36 cảnh, 131 cue thuyết minh, quiz, parts
assets/fonts          Be Vietnam Pro + JetBrains Mono (woff2, có tiếng Việt)
tools/
  tts_cues.py         tổng hợp giọng theo từng cue (Edge TTS), có resume
  build-timeline.mjs  dựng timeline, phụ đề, sự kiện SFX
  build-audio.py      nhạc nền ambient + ducking + SFX + trộn
  render.mjs          render frame → ffmpeg → MP4 (AAC 192k)
  preview.mjs         chụp still từng cảnh để QA bố cục
  export-srt.mjs      xuất phụ đề SRT
  build-docs.mjs      sinh storyboard + lời thoại từ script/timeline
build/                đầu ra trung gian (voice, previews, audio, video…)
```

## Yêu cầu môi trường

- Windows 10/11, Node.js ≥ 20, Python ≥ 3.10.
- Microsoft Edge cài tại `C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`.
- `npm install` (playwright-core, ffmpeg-static).
- Python: `pip install edge-tts numpy` (cần mạng cho Edge TTS).

## Quy trình dựng video

```bash
# 0. Sinh script.json từ kịch bản
node tools/export-script.mjs

# 1. Thuyết minh (resume được: chạy lại sẽ bỏ qua cue đã có)
python tools/tts_cues.py

# 2. Timeline + phụ đề + sự kiện âm thanh
node tools/build-timeline.mjs

# 3. Trộn giọng đọc, nhạc nền, SFX
python tools/build-audio.py

# 4. Phụ đề SRT
node tools/export-srt.mjs

# 5. Render video đầy đủ
node tools/render.mjs --out build/video/co-so-du-lieu.mp4

# 5b. Hoặc render 3 đoạn song song (nhanh hơn), rồi ghép và mux audio
node tools/render.mjs --from 0 --to 350 --out build/video/seg1.mp4 --mute
node tools/render.mjs --from 350 --to 700 --out build/video/seg2.mp4 --mute
node tools/render.mjs --from 700 --to 1050.8 --out build/video/seg3.mp4 --mute
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\n" > build/video/segments.txt
ffmpeg -f concat -safe 0 -i build/video/segments.txt -c copy build/video/video-only.mp4
ffmpeg -i build/video/video-only.mp4 -i build/audio/mix.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest build/video/co-so-du-lieu.mp4

# Render thử một đoạn (ví dụ 0–60 giây)
node tools/render.mjs --from 0 --to 60 --out build/video/test-60s.mp4

# 6. Cập nhật storyboard/lời thoại kèm thời lượng thật
node tools/build-docs.mjs
```

Xem trước bố cục không cần giọng đọc: `node tools/preview.mjs [scene-id …]`
→ ảnh PNG trong `build/previews/`.

## Giọng đọc

- Mặc định: `vi-VN-NamMinhNeural` — nam, giọng Bắc chuẩn, rõ ràng; phù hợp thuật ngữ CNTT.
- Edge TTS **không có giọng nam miền Nam** cho `vi-VN`; yêu cầu "giọng nam miền Nam" không thể
  đáp ứng tuyệt đối bằng dịch vụ miễn phí này. Có thể đổi giọng bằng biến môi trường:

  ```bash
  TTS_VOICE=vi-VN-HoaiMyNeural python tools/tts_cues.py
  ```

  hoặc thay hàm `synth()` trong `tools/tts_cues.py` bằng nhà cung cấp khác (ElevenLabs,
  Azure Speech custom voice…) nếu có giọng nam miền Nam được cấp phép. Toàn bộ pipeline còn lại
  không phụ thuộc nhà cung cấp TTS: mỗi cue là một file WAV, timeline tự căn theo thời lượng file.

- Tốc độ: đọc tự nhiên, sau đó áp `atempo=0.96` (chậm nhẹ 4%) và `loudnorm` cho đồng đều.
- Nếu Edge TTS báo `NoAudioReceived` (giới hạn tạm thời theo IP), script tự retry và có thể
  chạy lại bất cứ lúc nào để tiếp tục.

## Âm thanh

- Nhạc nền ambient/tech (A minor, pad + pulse + pluck) sinh bằng numpy, tự động duck −82% theo
  giọng đọc (block 50 ms, attack 0.12 s, release 0.8 s).
- SFX: boot, whoosh, chime, sparkle, success, error, riser, keyboard click. Tiếng gõ phím chỉ
  xuất hiện trong các cue có `sfx: 'type'`.
- Trộn tại 48 kHz stereo, normalize đỉnh 0.89, soft-limit tanh, xuất WAV + M4A AAC 192 kbps.

## Ghi chú kỹ thuật

- Render tất định: mọi chuyển động là hàm của thời gian `t`, không dùng CSS animation hay
  requestAnimationFrame; nhờ vậy frame nào cũng tái lập được và A/V khớp tuyệt đối.
- Mỗi cảnh có lead-in/lead-out riêng; cue bắt đầu đúng mốc trong file thoại của cảnh.
- Phụ đề ưu tiên cắt tại dấu câu, tối đa ~75 ký tự mỗi dòng; thời gian chia theo độ dài từ.
- Video: H.264 High, CRF 18, yuv420p, faststart; audio AAC 192 kbps.
- Thời lượng thực tế: 17 phút 31 giây. Render tuần tự ~12–16 fps; có thể chia 3 đoạn
  `--mute`, ghép video rồi mux `build/audio/mix.wav` một lần để còn khoảng 10 phút.

## Trạng thái

- [x] Kịch bản 36 cảnh / 131 cue; dữ liệu cửa hàng nhất quán
- [x] Engine cảnh, đồ họa động, ERD, SQL typing, quiz tương tác
- [x] Preview 36 cảnh và sửa lỗi bố cục
- [x] Tổng hợp giọng đọc đầy đủ (131/131 cue, 36 cảnh)
- [x] Timeline 17:31, audio mix, phụ đề SRT 326 dòng
- [x] Render MP4 cuối — `build/video/co-so-du-lieu.mp4` (17:30, 1920×1080, 25 fps, 127 MB)
- [x] QA video cuối: panel quiz, chuyển cảnh, phụ đề, mức âm lượng; ảnh tổng hợp tại
  `build/video/contact-sheet.png`
