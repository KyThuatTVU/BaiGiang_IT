# Storyboard — Cá nhân hóa & thuật toán hệ thống gợi ý sản phẩm

**Thương hiệu:** AN TECH ACADEMY · **Khung:** 1920×1080 @25fps · **Engine:** render tất định `window.renderFrame(t)`
**Bảng màu:** AI/Data (indigo #4F46E5, violet #7C3AED, cyan #06B6D4, teal #14B8A6, amber #F59E0B) trên nền sáng.
**Font:** Quicksand (tiêu đề), Be Vietnam Pro (thân), Plus Jakarta Sans (nhãn/số), JetBrains Mono (code).

> Mốc thời gian chính xác từng cue nằm ở `docs/loi-thoai.md` (sinh tự động từ timeline thật).
> Bảng dưới mô tả **bố cục + chuyển động + chữ trên màn hình** cho mỗi cảnh. Cảnh mẫu đã dựng; cảnh còn lại dựng sau khi duyệt mẫu.
> Mọi chuyển động suy ra từ `t` (không CSS animation) → khung hình lặp lại được, đồng bộ giọng đọc.

---

## Mẫu (đã dựng, 42.9s)

### `intro` · 0.0–13.7s · Mở đầu
- **Bố cục:** trái = eyebrow thương hiệu + hero title 2 dòng "HỆ THỐNG / GỢI Ý SẢN PHẨM" + sub + 4 chip (Personalization / Recommender System / KNN·SVD / Hybrid) + nhân vật giáo viên; phải = cửa sổ trình duyệt "NOVA SHOP".
- **Motion:** camera zoom nhẹ 1→1.018; title fade-trượt từng dòng; chip hiện lần lượt; con trỏ chuột lướt qua 3 thẻ Samsung (cue1) làm thẻ "hot"; dải "Gợi ý cho bạn" trượt lên (cue1→2); giáo viên vẫy tay → chỉ.
- **Chữ:** hero, sub, chip; shop: "Đang xem · Samsung cấu hình cao", thẻ Galaxy S24/A55/Xiaomi 14, rec Galaxy S24 98% / Xiaomi 14 95%.
- **Cue:** intro-1 chào thương hiệu (chime); intro-2 hook lướt Samsung (whoosh); intro-3 dẫn vào (chime).

### `personalization` · 14.0–28.2s · Phần 1
- **Bố cục:** pipeline 4 nút ngang: **Hành vi** (DỮ LIỆU ĐẦU VÀO: xem/tìm kiếm/nhấn chọn/đánh giá/mua) → **Hồ sơ sở thích** (USER PROFILE: chip Samsung/Cấu hình cao/Pin 5000mAh/RAM 12GB) → **Hệ thống gợi ý** (RECOMMENDER SYSTEM: KNN·SVD·TF-IDF) → **Danh sách gợi ý** (KẾT QUẢ ĐẦU RA: Galaxy S24 98%, Xiaomi 14 95%).
- **Motion:** các nút fade-trượt lần lượt; **packet** (chấm dữ liệu) chạy dọc link nối giữa các nút theo cue; chip hồ sơ bật lần lượt (cue2); rec trượt ra (cue3).
- **Cue:** pers-1 định nghĩa + Recommender System (marker); pers-2 hành vi→User Profile (data); pers-3 luồng vào→ra (success).

### `matrix` · 28.6–42.3s · Phần 1
- **Bố cục:** lưới ma trận 4 hàng (A,B,C,D) × 5 cột (I1…I5) + thẻ chú giải phải (CÁCH ĐỌC MA TRẬN; callout "≠ Ô trống KHÔNG phải điểm 0"; thanh sparsity; chip dự đoán).
- **Motion:** ô filled hiện lần lượt (cue1); ô trống viền đỏ nhấp nháy + hàng C khoanh (cue2); thanh sparsity chạy 0→60%; ô A×I5 đổi "?"→"5.0" viền cyan (cue3).
- **Chữ:** giá trị đúng catalog; "?" cho ô trống; "60% ô trống"; "Dự đoán ô trống → chọn điểm cao".
- **Cue:** mat-1 cấu trúc ma trận (marker, +12%); mat-2 ô trống≠0 + thưa (click); mat-3 dự đoán→gợi ý (pop).

---

## Phần còn lại (dựng sau duyệt mẫu)

### `goals` · Mở đầu · Lộ trình
- 5 thẻ chặng ngang (Cá nhân hóa / Phổ biến / Cộng tác KNN·SVD / Nội dung TF-IDF / Hybrid) + dải persona A,B,C. Thẻ bật lần lượt; camera pan nhẹ. Cue goals-1 (pop), goals-2 (chime).

### `div1…div5` · Divider phần
- Nền tối indigo/violet, số phần lớn, tiêu đề phần, gạch chân scribble. Zoom-out 1.04→1.0. Cue divN-1 (riser). Đổi chrome sang dark.

### `popularity` · Phần 2 · Xếp hạng phổ biến
- Bảng xếp hạng 3 cột dọc (I1/I3/I5) với thanh lượt mua 1000/750/500 + nhãn lượt xem/đánh giá; thanh mọc theo cue2; vương miện/huy hiệu #1 cho I1 (cue3). Camera zoom vào #1.
- Cue pop-1 tiêu chí (marker); pop-2 số liệu (data); pop-3 chọn I1 (success).

### `poplimit` · Phần 2 · Ưu/nhược
- Hai cột: trái "Ưu: luôn có kết quả (kể cả C)" xanh; phải "Nhược: ai cũng một danh sách" đỏ; mô phỏng 3 persona A,B,C nhận **cùng** list Samsung; dấu ≠ giữa "số đông" và "cá nhân hóa". Cue popl-1 (click), popl-2 (error).

### `cfintro` · Phần 3 · Ý tưởng lọc cộng tác
- Đồ thị người–sản phẩm: nút A,B,D nối tới món đã thích; highlight cặp A–D "gu giống nhau"; hai nhánh User-Based / Item-Based tách trục. Cue cf-1 (marker), cf-2 (click), cf-3 (pop).

### `knn` · Phần 3 · KNN
- Trái: vector A và D trên ô cùng đánh giá (I1=5,I2=4) → chồng khít, nhãn cosine=1.00; phải: ô A×I5 "?"→5.0 suy từ D; thanh K=1; công thức trung bình trọng số. Chuyển trục Item-Based ở cue5.
- Cue knn-1 định nghĩa+cosine/Pearson (marker); knn-2 vector A,D (data); knn-3 dự đoán I5 (success); knn-4 đo≠dự đoán (click); knn-5 item-based (pop).

### `svd` · Phần 3 · SVD
- Ma trận A tách thành 3 khối U · Σ · Vᵀ (animation tách/khối trượt); Σ hiện vài thanh latent (hệ ĐH/cấu hình/camera); tái tạo A≈UΣVᵀ lấp ô trống; nhãn "SVD gốc cần ma trận đầy đủ" → "FunkSVD chỉ học ô đã biết". Giảm tốc cue2.
- Cue svd-1 latent (marker); svd-2 công thức (data,+6%); svd-3 tái tạo (sparkle); svd-4 giới hạn SVD gốc (click); svd-5 MF/FunkSVD (marker).

### `cflimits` · Phần 3 · Thưa & lạnh
- Hai thẻ vấn đề: "Dữ liệu thưa" (ma trận lỗ chỗ) và "Khởi đầu lạnh" (persona C trống); bảng so KNN vs SVD (dễ giải thích/nặng vs dự đoán tốt/khó diễn giải). Cue cfl-1 (error), cfl-2 (click), cfl-3 (pop).

### `tfidf` · Phần 4 · TF-IDF
- Mô tả sản phẩm → tách từ; thanh TF (từ trong mô tả) và IDF (nghịch đảo số tài liệu); từ khóa đặc trưng (RAM 12GB, pin 5000) nổi lên, từ chung chìm; mỗi sản phẩm thành vector. Cue tf-1 (marker), tf-2 (data), tf-3 (sparkle).

### `cosine` · Phần 4 · Cosine
- Hai vector (sở thích A vs sản phẩm) trên mặt phẳng, góc θ kẹp giữa; góc nhỏ→giống; ví dụ RAM12/ROM256/pin5000 → khớp Xiaomi 14; nhãn Feature-Based; thẻ hạn chế over-specialization. Cue cos-1 (marker), cos-2 (data), cos-3 (click), cos-4 (error).

### `weighted` · Phần 5 · Weighted
- Ba nguồn điểm (S_CF .9 / S_CB .8 / S_POP .5) chảy vào bộ trộn với trọng số .5/.3/.2; thanh chuẩn hóa về [0,1] trước; kết quả 0.79 hiện lớn. Giảm tốc cue2. Cue w-1 (marker), w-2 (data,+8%), w-3 (success), w-4 chuẩn hóa (click).

### `switching` · Phần 5 · Switching
- Công tắc 3 nhánh theo lượng dữ liệu: C mới→Popularity; có lịch sử xem→Content-Based; đủ tương tác→SVD/KNN; đèn nhánh sáng theo cue. Cue sw-1 (marker), sw-2 (data), sw-3 (success).

### `cascade` · Phần 5 · Cascade
- 4 tầng nối tiếp: Ứng viên → SVD → Content-Based → Xếp hạng top5; danh sách ứng viên lọc dần qua từng tầng; bảng chốt "Weighted trộn / Switching chọn một / Cascade nối tiếp". Cue ca-1 (marker), ca-2 (data), ca-3 (click), ca-4 (success).

### `recap` · Phần 6 · Năm điều mang về
- 5 thẻ tóm tắt (cá nhân hóa/phổ biến/cộng tác/nội dung/hybrid) bật lần lượt; camera pan. Cue rec-1 (pop), rec-2 (chime).

### `quiz` · Phần 6 · Kiểm tra nhanh
- 3 câu hỏi, mỗi câu: thẻ câu hỏi + vòng đếm ngược 3s (hold) + 3 lựa chọn; hết hold tô đáp án đúng, mờ đáp án sai + giải thích. Cue q1/q2/q3 (whoosh, hold 3) + q1a/q2a/q3a (success).

### `outro` · Phần 6 · Kết
- Câu kết thương hiệu lớn + scribble; chip tổng kết; giáo viên vẫy tay; logo AN TECH; fade trắng cuối. Cue out-1 (chime) — giữ nguyên văn câu kết.

---

## Quy ước chuyển động toàn cục
- **Transition cảnh:** fade-in 0.55s / fade-out 0.5s + sweep màu ngang đầu cảnh; cảnh trước chồng mờ 0.42s.
- **Camera:** mỗi cảnh có `cam(t)` zoom/pan nhẹ (≤2%) tạo chiều sâu, không giật.
- **Nền:** mesh gradient trôi chậm + hạt float parallax; không nền tĩnh đơn sắc.
- **Phụ đề:** đáy màn hình, fade theo từng cue, nền gradient mờ để dễ đọc.
- **Progress:** thanh tiến trình + timecode góc phải; chip phần đổi theo cảnh.