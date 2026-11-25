# AGENTS.md — D:\Edit

## Quy tắc chính (bắt buộc, không thay thế)

Trước khi làm bất kỳ video nào: **đọc và tuân thủ [`MASTER_DESIGN_VOICE_STANDARD_2.3.md`](MASTER_DESIGN_VOICE_STANDARD_2.3.md)** ở thư mục này.
Đó là quy chuẩn sản xuất chính thức của AN TECH ACADEMY: nhận diện thương hiệu, typography, phát âm, giọng đọc, hình ảnh, chuyển động, âm thanh, quy trình mẫu 30–45 s, checklist nghiệm thu, nhân vật giáo viên, vẽ tay và SFX.
File này **không chép lại và không thay đổi** quy chuẩn đó.

## Nhận bài mới

- Người dùng tự tạo thư mục bài (hoặc nhờ agent tạo) tại `D:\Edit\<TenBai>\` gồm:
  - `content.md` — nội dung/kịch bản gốc (`.md`, `.docx`, `.txt` đều được);
  - `notes.md` — tuỳ chọn: yêu cầu riêng (thời lượng, giọng, ngoại lệ được duyệt);
  - `img/` — ảnh/logo/sơ đồ người dùng cung cấp;
  - `AGENTS.md` — 3 dòng trỏ về `D:\Edit\AGENTS.md` và MASTER 2.3 (agent tạo nếu chưa có).
- Khi người dùng nói **"làm bài <tên bài>"**, agent quét đúng thư mục đó, đọc nội dung + `notes.md` + `img/` và bắt đầu quy trình; không hỏi lại vị trí.
- Dự án nhiều bài: `D:\Edit\<du-an>\bai\<ten-bai>\` cùng cấu trúc.
- Thiếu thông tin thiết yếu thì hỏi đúng một lần; không bịa nội dung, số liệu phải ghi "giả định".

## Quy trình

Theo mục X của MASTER 2.3: storyboard + bảng thuật ngữ → **mẫu 30–45 s (Cổng A/B)** → người dùng duyệt → sản xuất toàn bộ → QA → bàn giao kèm bảng trạng thái **Đạt / Cần sửa / Chưa xác minh**.
Bản đã duyệt không ghi đè; bản mới đặt tên phiên bản. Không tuyên bố đã kiểm tra những gì chưa thực sự kiểm.

## Mặc định khi sản xuất

- **Lời chào:** mọi bài mặc định có lời chào mở đầu (chào người xem, giới thiệu chủ đề và AN TECH ACADEMY) và lời kết (cảm ơn, nhắc theo dõi kênh, hẹn bài sau) — theo mẫu S01/S11 của bài API. Đưa vào storyboard ngay từ Cổng A; người dùng tắt bằng dòng "Không cần lời chào" trong `notes.md` của bài.
- **Ảnh minh họa trong `img/` (bắt buộc):** mọi bài phải đưa ảnh người dùng cung cấp trong `<bài>/img/` vào khung hình làm minh họa — không đọc nội dung rồi vẽ thay toàn bộ bằng code. Khi nhận bài: xem hết ảnh, ghi chú nội dung từng ảnh, và đưa kế hoạch dùng ảnh (cảnh nào · ảnh nào · thời điểm) vào storyboard Cổng A và mẫu 30–45 s Cổng B. Ảnh chụp màn hình/điện thoại → `cover`; sơ đồ/infographic → `contain` (nền mờ tối, khung đúng tỉ lệ) trong photo card kính — mẫu đã kiểm chứng: `Biagiang_ThanhToanTheNH\tools\demo_full.py`. Ảnh phải khớp lời đọc của cue đang nói. Checklist nghiệm thu có mục "ảnh trong `img/` đã dùng hết hoặc chọn lọc có lý do, hiển thị đúng cảnh"; ảnh thiếu/không phù hợp thì nói rõ và hỏi người dùng, không lặng lẽ bỏ qua và không báo hoàn thành khi ảnh còn bỏ trống.

## Phần riêng từng dự án

Ghi trong `<du-an>\AGENTS.md` (đường dẫn, bản mẫu, ngoại lệ được duyệt). Mẫu triển khai đã duyệt gần nhất: `Baigiang_API\tools\demo30.py` (chuyển động + SFX + nhân vật An).

## Kho dùng chung — `D:\Edit\Kit` (một nơi duy nhất để sửa)

- **Quy tắc:** `D:\Edit\MASTER_DESIGN_VOICE_STANDARD_2.3.md` (chuẩn chính) + file này (cách nhận bài).
- **Code chung:** `Kit\tools\` — `core.py` (khung hình, font, easing, nét bút tay), `demo20.py` (nền, card, chip, JSON, caption), `sfx.py` (âm thanh tổng hợp), `character.py` (nhân vật An), `tts.py` (Edge TTS), `prep_icons.py` (SVG→PNG, `icon_rgba`), `icons\` (logo React / Node.js / MySQL).
- **Font:** `Kit\assets\fonts`. **Icon:** `Kit\assets\icons` (SVG gốc), `Kit\assets\icons_black` (PNG đen), `Kit\assets\icons_png` (cache màu).
- **Logo bản quyền:** `Kit\assets\brand\logo_an_round.png` (ảnh gốc `logo_an.png`). Dán trong khung hình bằng `core.paste_brand(...)` / `core.brand_watermark(...)`; video đã render thì chạy `python Kit\tools\stamp_logo.py <video.mp4> --pos tr --dy 60 --size 150 --alpha 0.9` → xuất `<video>_logo.mp4`, giữ nguyên bản gốc.
- **Cache tự sinh:** `Kit\cache\` — không sửa tay.
- **Cách dùng:** đặt `PROJECT_ROOT` = thư mục dự án (mặc định `D:\Edit\Baigiang_API`) rồi `sys.path.insert(0, r"D:\Edit\Kit\tools")` trước khi import. Hướng dẫn chi tiết: `Kit\README.md`.
- **Mẫu triển khai đã duyệt:** `Baigiang_API\tools\demo30.py` (giữ trong dự án vì chứa nội dung bài) và video chuẩn hiện hành `Baigiang_API\mau\demo30_vieneu\api_pro_demo30_an.mp4` (V13, giọng clone + An + SFX); V11/V12 (Edge) giữ làm lịch sử.
- Dự án **không copy** code/font/icon từ Kit; chỉ viết code cảnh riêng của bài. Mọi yêu cầu chỉnh sửa code chung → sửa **trong Kit**, mọi dự án dùng ngay. Không sửa/di chuyển Kit khi chưa cập nhật mục này.

## Bảo mật

Không mở, in hoặc dò file token/credential (`.viettel_token*`, `.env`, khoá API). Không thử lại lệnh đã bị từ chối.
