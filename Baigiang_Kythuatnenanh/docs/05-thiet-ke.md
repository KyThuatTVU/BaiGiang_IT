# Thiết kế hình ảnh & âm thanh — Kỹ thuật nén ảnh

## 1. Bảng màu

| Vai trò | Màu | Hex |
|---|---|---|
| Nền sáng (cảnh giảng) | trắng xanh | `#F6F8FB` |
| Nền tối (hook, code, outro) | navy | `#0B1322` → `#1B2A4A` |
| Chữ chính | ink | `#0F172A` |
| Nhấn chính | blue | `#2563EB` |
| Nhấn hành động / cảnh báo nhẹ | amber | `#F59E0B` |
| Trạng thái tốt / lossless | teal / green | `#0D9488` / `#16A34A` |
| Lỗi / nén quá tay | red | `#DC2626` |
| Đường viền, thẻ | border | `#E2E8F0` |

Nguyên tắc 60–30–10: ~60% nền sáng-trung tính, ~30% navy/blue (thẻ, tiêu đề, dải phụ đề), ~10% amber/teal làm nhấn.
Không gradient cầu vồng, không neon; bóng đổ rất nhẹ; không dùng 3D bóng nhựa.

## 2. Typography

- Tiêu đề cảnh: **Be Vietnam Pro Bold** 44–56 px.
- Nội dung: **Be Vietnam Pro Regular/Medium** 26–32 px.
- Số liệu, nhãn kỹ thuật: **Plus Jakarta Sans** 24–58 px.
- Code: **JetBrains Mono** 21–25 px trên nền `#0D1526`.
- Phụ đề: Be Vietnam Pro Medium 30 px, tối đa 2 dòng, dải navy đáy khung.
- Khoảng dòng 1,35; lề an toàn ≥ 5% (96 px ngang, 54 px dọc).

## 3. Icon & đồ họa

- Một bộ **Lucide** 92 icon (nét 1,6–2 px) trong toàn video, tô màu theo bảng màu; không emoji.
- Sơ đồ, pipeline, ma trận, bảng so sánh **tự dựng bằng PIL/vector**; không để AI sinh chữ/số.
- Ảnh người dùng: luôn đặt trong khung chứng cứ bo 16 px, viền `#D8E0EC`, nhãn nhỏ ghi nguồn khi cần.
- Ken Burns nhẹ (zoom 1,00→1,08) cho ảnh chứng cứ; không lặp cùng một bố cục ở hai cảnh liền nhau.

## 4. Nhân vật giáo viên "An"

- Vector phẳng 2D, áo sơ mi navy, thẻ tên AN, tóc ngắn — giữ nguyên toàn video (series An Tech).
- 6 tư thế: `present`, `point_left`, `point_right`, `think`, `write`, `wave`; mấp máy môi khi nói, nhìn theo nội dung.
- Đứng góc phải (hoặc trái ở S02) để không che code/sơ đồ/phụ đề; thu nhỏ ở cảnh code.
- Cử chỉ khớp lời: chỉ vào từ khóa khi nhấn mạnh, mở tay khi đặt câu hỏi, vẫy ở outro.

## 5. Chuyển động & chuyển cảnh

- Nền tảng: fade/rise 0,35–0,55 s cho thẻ; marker vẽ dần; số đếm tăng dần; thanh dung lượng co giãn.
- Cảnh code: gõ từng ký tự đồng bộ; gói dữ liệu chạy qua pipeline theo đúng chiều xử lý.
- Chuyển cảnh: xfade 0,3 s (mặc định), xen kẽ push nhẹ ở S04→S05, S08→S09; không dùng hiệu ứng mạnh.
- Mỗi khung hình chỉ một nhóm chuyển động chính để mắt kịp theo.

## 6. Âm thanh

- Voice: Edge TTS `vi-VN-NamMinhNeural`, rate +8…+15%, pitch-shift 0…+1,0 semitone theo cảm xúc câu.
- Nhạc nền: ambient tech sinh bằng numpy (A minor, pad + pulse), ducking −82% theo giọng, fade in/out.
- SFX theo hành động: whoosh (chuyển cảnh/thẻ), pop (xuất hiện), tick (chốt ý), type (gõ code), marker (nét vẽ), chime/success (kết), error nhẹ (cảnh báo nén quá tay).
- Voice luôn lớn nhất; SFX ngắn, sạch; không lặp một hiệu ứng cho mọi hành động.

## 7. Phụ đề

- Tiếng Việt đầy đủ, đúng thuật ngữ, tối đa 2 dòng/cue; cắt theo cụm nghĩa, không bẻ đôi thuật ngữ.
- Sinh trực tiếp từ `subs` trong manifest nên khớp nội dung đã duyệt; thời gian theo file thoại thật.

## 8. Nhịp cảnh dự kiến

| Cảnh | Nội dung | Nhịp |
|---|---|---|
| S01 | Hook | Nhanh, nhiều pop, câu hỏi |
| S02 | Vì sao | Trung bình, bằng chứng |
| S03 | Định nghĩa | Chậm, rõ |
| S04 | Lossy | Trung bình → nhấn cảnh báo |
| S05 | Lossless | Chậm, đối chiếu |
| S06 | 4 định dạng | Liệt kê có nhịp, highlight từng cột |
| S07 | Chọn định dạng | Dứt khoát, ma trận |
| S08 | Sharp | Chậm ở code, nhanh ở pipeline |
| S09 | HTML | Trung bình, thao tác |
| S10 | Ứng dụng | Nhanh, thẻ trượt |
| S11 | Lưu ý | Đều, checklist |
| S12 | Tổng kết | Chắc, tăng năng lượng, outro |
