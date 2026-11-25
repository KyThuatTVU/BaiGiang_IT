# STORYBOARD — CỔNG A

Nguyên tắc chung: nền giấy sáng #F6F8FB, thương hiệu góc trên trái, chip chương góc trên phải, dải tiến trình vàng; nhân vật An đứng bên trái hoặc phải, không che nội dung; phụ đề trong dải navy đáy khung (tối đa 2 dòng).

Ký hiệu chuyển động: **IN** = xuất hiện (fade/rise), **TYPE** = chữ chạy từng ký tự, **DRAW** = nét bút dạ vẽ dần, **POP** = bật chip, **SWAP** = thay ảnh tại chỗ.

---

## S01 — Hero
- Bố cục: tiêu đề động 3 dòng "BẢO VỆ / MÃ NGUỒN / & KIỂM SOÁT TRUY CẬP" bên trái; 3 chip vũ khí (Apache, .htaccess, Front Controller) xếp dọc dưới tiêu đề; thẻ ảnh image1 bên phải.
- Ảnh: **image1** — minh hoạ .htaccess bảo vệ hệ thống, có nét bút khoanh amber quanh tài liệu .htaccess.
- Nhịp: tiêu đề IN 0,0–0,6 s → gạch chân DRAW 0,5–1,1 s → chip POP lần lượt 0,7/0,95/1,2 s → ảnh trượt vào + sheen quét 1,0–1,8 s.
- Nhân vật: An vẫy tay (wave), quay nhẹ sang ảnh.
- SFX: whoosh (mở cảnh), pop ×3, marker (gạch chân), chime cuối cảnh.
- Phụ đề: 2 câu hook.

## S02 — DevTools / Network
- Bố cục: khung browser giả lập (URL example.com/products) chiếm trái; cột phải: thẻ "Nguyên tắc vàng", keycap F12, hàng chip HTML/CSS/JS/API.
- Ảnh: **image5** — screenshot Network của OWASP Juice Shop; khoanh tròn amber tab Network, chip nhãn "Network" gắn phía trên.
- Nhịp: browser IN 0,0–0,8 → ảnh hiện + khoanh tab 0,8–1,7 → chữ "mở DevTools" và keycap 2,4 → dải quét xanh chạy dọc bảng request ở cue 2 → 4 chip bay lên từ mép dưới browser.
- Nhân vật: An chỉ trái (point_left).
- SFX: whoosh, marker (khoanh), tick ×2 (dải quét), pop ×4 (chip), chime.
- Phụ đề: 2 câu.

## S03 — Lộ thư mục nội bộ
- Bố cục: thanh URL lớn `https://example.com/backend/config/` → khung listing giả lập "Index of /backend/config/" → 4 thẻ rủi ro xếp dọc bên phải (mã nguồn, cấu hình, dữ liệu, bàn đạp).
- Ảnh: **image6** — cây thư mục dự án, khoanh đỏ vùng `index.php`/thư mục lõi; chú thích "Cấu trúc thư mục thực tế".
- Nhịp: URL TYPE → listing trượt lên (mỗi dòng: database.php 4.1K, ../, .env 1.2K) → image6 IN + DRAW vòng đỏ → 4 thẻ rủi ro POP so le → chip cảnh báo amber.
- Nhân vật: An đứng phải, pose present.
- SFX: click (từng ký tự URL), whoosh, marker (vòng đỏ), thud (thẻ rủi ro), chime.
- Phụ đề: 3 câu.

## S04 — Apache & .htaccess
- Bố cục: hàng 3 node Trình duyệt → Apache → PHP có gói dữ liệu chạy dọc đường nối; panel code `.htaccess` tối bên phải đang TYPE; ảnh VS Code thật phía dưới trái (image2), chip điều kiện AllowOverride / mod_rewrite.
- Ảnh: **image2** — cửa sổ VS Code chứa .htaccess thực tế, đóng khung + nhãn "VS Code thực tế".
- Nhịp: node POP 0,2/0,45/0,7 → gói dữ liệu chạy 0,4–2,2 → code TYPE theo cue 2 → ảnh IN kèm sheen → chip POP.
- Nhân vật: An trái, pose present.
- SFX: pop ×3, whoosh, click (gói dữ liệu), chime.
- Phụ đề: 2 câu.

## S05 — 403 & chặn thư mục
- Bố cục: thẻ listing giả "Index of /frontend/assets/" (css/, js/, images/, config.php, .env) bị gạch đỏ lần lượt; ảnh 403 isometric bên phải; tem "403 FORBIDDEN" bật ra; 2 chip kết luận.
- Ảnh: **image7** — minh hoạ 403 Forbidden 3D isometric (từ tài liệu gốc), khoanh đỏ nét tay.
- Nhịp: listing IN → từng dòng gạch đỏ theo cue 1 → ảnh IN + khoanh 403 → tem 403 bật (thud) → chip Directory Listing: OFF / Require all denied → 403.
- Nhân vật: An trái dưới, present.
- SFX: whoosh, marker (gạch dòng), deny (âm rơi), thud (tem), chime.
- Phụ đề: 2 câu, câu chốt "Require all denied → 403 Forbidden".

## S06 — FilesMatch
- Bố cục: panel code tối `.htaccess` với `<FilesMatch "(?i)\.(env|sql|log|bak|ini|sh)$">` + `Require all denied`; 6 chip đuôi tệp bị gạch; thẻ kem "Bí mật nên nằm ngoài DocumentRoot".
- Nhịp: code TYPE → chip regex và ý nghĩa POP → 6 chip đuôi tệp POP rồi gạch đỏ lần lượt → thẻ kem IN.
- Nhân vật: An phải, present.
- SFX: click, marker ×6, pop, chime.
- Phụ đề: 2 câu.

## S07 — URL Rewrite
- Bố cục: thanh địa chỉ morph từ URL dài (`/frontend/pages/about/index.html`) → `/about/`; chip giải thích `→ frontend/pages/about/index.html`; sơ đồ luồng Apache thay thế ảnh chân dung code.
- Ảnh: **image8** — VS Code RewriteRule (nửa đầu cảnh) → **SWAP** sang **image3** — flowchart xử lý RewriteRule (nửa sau), nhãn "Luồng xử lý của Apache".
- Nhịp: URL dài bị gạch đỏ → URL ngắn hiện + dấu check teal → 2 thẻ so sánh "Rewrite nội bộ" vs "Redirect 301" POP → ảnh đổi tại cue 2.
- Nhân vật: An phải, present.
- SFX: whoosh, tick, pop ×2, chime.
- Phụ đề: 2 câu.

## S08 — Front Controller
- Bố cục: 6 chip tệp rời (login.php, register.php, products.php…) co cụm vào hub tròn `index.php`; 5 route toả ra (/ , /about/, /contact/, /api/settings, /admin/ — route admin màu đỏ); sơ đồ image4 bên phải; 3 chip nhiệm vụ (Đọc URL, Kiểm quyền, Gọi xử lý).
- Ảnh: **image4** — sơ đồ Front Controller (Entry Point → Application → Router → Controller → Helpers/Repositories/Models/View).
- Nhịp: chip rời IN → DRAW đường nối vào hub → hub POP → route toả POP lần lượt → sơ đồ IN → chip nhiệm vụ.
- Nhân vật: An trái, present.
- SFX: pop ×6, whoosh, chime.
- Phụ đề: 2 câu.

## S09 — Whitelist & 404
- Bố cục: panel code PHP sáng TYPE khai báo `$routes`; thẻ "Danh sách được phép" (/, /about/, /contact/ ✓; /admin/ ✗ + gạch đỏ); tem 404 nghiêng.
- Nhịp: code TYPE → thẻ whitelist IN → từng route tick → /admin/ gạch → tem 404 bật (thud) → 2 chip ghi chú.
- Nhân vật: An phải, point_left.
- SFX: click, pop, marker, thud, chime.
- Phụ đề: 1 câu dài chia 2 dòng.

## S10 — public / private
- Bố cục: thẻ cây thư mục 2 khối PUBLIC (xanh mint) / PRIVATE (hồng nhạt); mũi tên DocumentRoot; flow 5 bước dọc; chip 403 và 404 đặt cạnh bước tương ứng.
- Nhịp: thẻ IN → folder POP so le (2 public, 4 private) → mũi tên DRAW + chip DocumentRoot → 5 bước flow POP tuần tự → 403 (bước Kiểm luật) → 404 (bước Router).
- Nhân vật: An trái, present.
- SFX: whoosh, pop ×7, chime.
- Phụ đề: 2 câu.

## S11 — Tóm tắt & quiz
- Bố cục: 3 thẻ tóm tắt (DevTools / .htaccess / Whitelist) → khối quiz "Dòng nào tắt danh sách thư mục?" với 3 đáp án A/B/C; đáp án B sáng teal + dấu check + chip "Đáp án: B".
- Nhịp: 3 thẻ POP 0,2/0,5/0,8 → quiz IN → A/C hiện → B highlight sau "Suy nghĩ hai giây" → chip đáp án.
- Nhân vật: An phải, present.
- SFX: pop ×3, tick, chime, success (khi lộ đáp án).
- Phụ đề: 2 câu.

## S12 — Outro
- Bố cục: lockup "AN TECH ACADEMY — Học công nghệ cùng An", câu định vị "Bảo mật không phải che giấu, mà là kiểm soát đúng chỗ.", 2 chip CTA (dựng WebShield trên XAMPP; gõ thử URL lạ), chip bài kế tiếp.
- Nhịp: lockup IN + gạch chân DRAW → câu định vị IN theo dòng → chip POP → sheen quét.
- Nhân vật: An vẫy tay (wave), scale lớn hơn cảnh nội dung.
- SFX: chime mở, pop, success cuối.
- Phụ đề: 2 câu kết.

---

## Bảng dùng ảnh gốc (đủ 8/8)

| Ảnh | Cảnh | Vai trò trong ngữ cảnh |
|---|---|---|
| image1 | S01 | Minh hoạ .htaccess như "lá chắn" — mở bài |
| image2 | S04 | Cửa sổ VS Code thật của .htaccess — chứng minh tệp luật |
| image3 | S07 | Flowchart Apache xử lý RewriteRule — giải thích luồng |
| image4 | S08 | Sơ đồ Front Controller — kiến trúc một cửa |
| image5 | S02 | Screenshot Network tab — dẫn chứng DevTools thấy request |
| image6 | S03 | Cây thư mục dự án — minh hoạ lộ cấu trúc |
| image7 | S05 | 403 Forbidden isometric — kết quả chặn thư mục |
| image8 | S07 | Code RewriteRule trong VS Code — mở đầu cảnh rewrite |
