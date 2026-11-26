# CỔNG A — STORYBOARD & KỊCH BẢN KHÓA
## Bài: Thuật toán SVD và ứng dụng trong lọc cộng tác — AN TECH ACADEMY

**Ngày lập:** 2026-11-25 · **Trạng thái:** chờ duyệt Cổng A (chưa dựng mẫu)
**Nguồn nội dung:** `content.md` (13 mục + 5 câu hỏi) · **Yêu cầu riêng:** `note.md` — video khoảng 7 phút, dùng `img/anhbia.png` làm ảnh bìa
**Chuẩn áp dụng:** MASTER DESIGN & VOICE STANDARD 2.3 + `D:\Edit\AGENTS.md`

---

## 1. Hồ sơ bài giảng

| Hạng mục | Nội dung |
|---|---|
| Chủ đề | Machine Learning — Recommender Systems: SVD và lọc cộng tác |
| Đối tượng | Người mới học lập trình, dữ liệu và AI; đã biết Python cơ bản |
| Mục tiêu | Hiểu SVD là gì; đọc được A = UΣVᵀ; hiểu ma trận User-Item và yếu tố tiềm ẩn; biết quy trình dự đoán, Top-N; chạy được mô hình Surprise; biết ưu/nhược, Cold Start, RMSE/MAE; phân biệt SVD và Collaborative Filtering |
| Thời lượng dự kiến | ~7:00–7:20 (khoảng 1.350 từ lời đọc; chốt bằng đo TTS ở Cổng B/full) |
| Giọng đọc | Clone VieNeu mặc định (`Kit/tools/tts_vieneu.py`, ref `ref_final.wav`) |
| Nhân vật | Giáo viên An toàn bộ cảnh (MASTER XVIII), 6 tư thế, không che nội dung |
| Âm thanh | Giọng + SFX tổng hợp (whoosh/pop/tick/bút/chime), **không nhạc nền** theo chuỗi bài gần nhất |
| Hình ảnh | 13/13 ảnh trong `img/` được dùng (12 ảnh minh họa + ảnh bìa), qua photo card kính |
| Lời chào | Có mở đầu + lời kết theo mặc định `AGENTS.md` (mẫu S01/S11 bài API) |

---

## 2. Art direction & bảng màu

Kế thừa đúng hệ hình ảnh **AI & Data** đã duyệt ở bài Hồi quy tuyến tính (bản v4):

- Nền: navy tối `#0A101C → #0D1626`, lưới be sữa rất mờ trôi chậm, ngoặc HUD 4 góc cyan/violet quét nhẹ.
- Chữ chính `#ECF1F9`, chữ phụ `#94A3B8`, nhãn viền trắng be sữa.
- Accent theo chức năng: **cyan `#38BDF8`** (dữ liệu, ma trận), **violet `#A78BFA`** (mô hình, yếu tố tiềm ẩn), **amber `#F59E0B`** (từ khóa, công thức), **emerald `#34D399`** (kết quả dự đoán, gợi ý). Đỏ `#E5484D` chỉ dùng ở cảnh Cold Start/lưu ý.
- Card: nền `#111A2D`, viền trắng alpha 28–34, vạch accent sáng phía trên; không gradient cầu vồng, không glow tràn.
- Font: Be Vietnam Pro (tiêu đề/nội dung), Plus Jakarta Sans (số liệu), JetBrains Mono (công thức, code).
- Hình ảnh: photo card kính — ảnh chụp màn hình/giao diện → `contain` (nền mờ tối, đúng tỉ lệ); ảnh bìa → `cover` toàn khung ở S01.
- Nhân vật An: đứng phải (`x≈1620–1680`), scale 0.66–0.82, pose theo cảnh (wave/present/point_left/point_right/write), mấp máy môi khi đang nói.

Vì sao tối: chủ đề ma trận/gợi ý thuộc nhóm AI & Data; nền tối làm nổi ma trận, công thức và ảnh giao diện sáng; đồng thời giữ nhất quán series bài giảng gần nhất.

---

## 3. Bảng thuật ngữ và cách thể hiện trong lời đọc

Nguyên tắc: **một giọng Việt** (clone), thuật ngữ nói theo tiếng Việt hoặc giữ nguyên tiếng Anh nhưng không chuyển giọng; chữ tiếng Anh vẫn hiển thị trên màn hình. Các từ rủi ro sẽ kiểm bằng sampler ~20 s ở Cổng B.

| Thuật ngữ | Nhóm | Lời đọc dự kiến | Trên màn hình | Đã kiểm chứng |
|---|---|---|---|---|
| SVD | Viết tắt | "S-V-D" (3 chữ cái) — **A/B/C ở sampler**: "SVD" / "S-V-D" / đọc từng chữ kiểu Anh | SVD | Chưa |
| Singular Value Decomposition | Đại số | giữ nguyên tiếng Anh ở lần đầu, sau đó dùng "SVD" | Singular Value Decomposition | Chưa |
| Phân rã giá trị suy biến | Đại số | "phân rã giá trị suy biến" | Phân rã giá trị suy biến | Chưa |
| Collaborative Filtering | Gợi ý | giữ nguyên tiếng Anh; nghĩa "lọc cộng tác" | Collaborative Filtering · Lọc cộng tác | Chưa |
| User-Item Matrix | Gợi ý | "ma trận người dùng – sản phẩm" (ưu tiên), nhắc "User-Item Matrix" một lần | User-Item Matrix | Chưa |
| Ma trận thưa | Dữ liệu | "ma trận thưa" | Ma trận thưa (sparse) | Chưa |
| Latent factors | Gợi ý | "yếu tố tiềm ẩn" | Latent factors | Chưa |
| Matrix Factorization | Gợi ý | "phân rã ma trận" | Matrix Factorization | Chưa |
| U · Σ · Vᵀ | Ký hiệu | "U", "Sigma", "V chuyển vị" | U · Σ · Vᵀ | Chưa |
| R̂ | Ký hiệu | "R mũ" | R̂ = U_k Σ_k V_kᵀ | Chưa |
| μ · b_u · b_i · p_u · q_i | Ký hiệu | "mu", "b-u", "b-i", "p-u", "q-i" | μ, b_u, b_i, p_u, q_i | Chưa |
| Top-N | Gợi ý | "Top N" | Top-N | Chưa |
| RMSE | Đánh giá | "R-M-S-E" (từng chữ cái) | RMSE | Chưa |
| MAE | Đánh giá | "M-A-E" (từng chữ cái) | MAE | Chưa |
| Precision@K · Recall@K · F1@K | Đánh giá | "Precision, Recall và F1" | Precision@K · Recall@K · F1@K | Chưa |
| Cold Start | Gợi ý | giữ nguyên tiếng Anh | Cold Start | Chưa |
| Popularity-Based Filtering | Gợi ý | "gợi ý theo độ phổ biến" (không đọc cụm Anh) | Popularity-Based Filtering | Chưa |
| Surprise · scikit-surprise | Thư viện | "Surprise", "scikit-surprise" | Surprise · scikit-surprise | Chưa |
| pandas · pip install | Công cụ | giữ nguyên tiếng Anh | pandas · pip install | Chưa |
| Python · Flask | Công nghệ | giữ nguyên | Python · Flask | Chưa |
| Node.js · Express · MySQL | Công nghệ | giữ nguyên | Node.js · Express · MySQL | Chưa |
| API · JSON · GET | Web | "API", "JSON", "GET" | API · JSON · GET | Chưa |
| AirPods | Sản phẩm | giữ nguyên | AirPods | Chưa |

**Kế hoạch kiểm:** sampler Cổng B gồm 3 biến thể "SVD" + 16 thuật ngữ rủi ro (Collaborative Filtering, User-Item Matrix, latent factors, Sigma, V chuyển vị, RMSE, MAE, Cold Start, Surprise, scikit-surprise, Top N, Flask, Node.js, AirPods, R mũ, b-u/q-i). Người dùng nghe và chốt trước khi sản xuất full. Không tự nhận đã kiểm phát âm khi chưa nghe.

---

## 4. Kế hoạch dùng 13 ảnh trong `img/`

Đã xem toàn bộ 13 ảnh. Vị trí dùng và lưu ý trung thực:

| Ảnh | Nội dung ảnh | Cảnh | Chế độ / kích thước | Thời điểm (ước tính) | Lưu ý |
|---|---|---|---|---|---|
| anhbia.png (1672×941) | Ảnh bìa bài giảng: tiêu đề SVD, bảng đánh giá An–Bình–Chi–Dũng, công thức A=UΣVᵀ, robot AI, khung gợi ý | S01 | cover toàn khung → thu về photo card | 0:00–0:20 | Ảnh người dùng cung cấp; chữ trên ảnh khớp nội dung bài |
| 7.jpg (16:9) | Website LUMA có sidebar "Personalized Recommendations" | S02 | contain 880×495 | 0:20–0:47 | Ảnh giao diện mẫu, tiếng Anh |
| 3.jpg (1280×896) | Carousel "Personalized Recommendations for You", nhãn Best Match/Trending | S02 | contain 700×490 | 0:20–0:47 | **Mockup do người dùng cung cấp, chữ trong ảnh bị lỗi** ("Best Mach", "Al lew") — chỉ dùng minh họa bố cục, không đọc chữ, có caption "Ảnh minh họa giao diện" |
| 2.jpg (1000×800) | Lọc cộng tác: user A và B giống sở thích, gợi ý tai nghe cho B | S04 | contain 760×608 | 1:12–1:42 | Ảnh minh họa tiếng Anh (Recostream) |
| 4.jpg (1024×768) | Lưới user – ratings – item với mũi tên đỏ | S05 | contain 780×585 | 1:42–2:08 | Ảnh minh họa tiếng Anh |
| 10.jpg (16:9) | User-Based CF với phim: hai người dùng tương tự | S06 | contain 800×450 | 2:08–2:30 | Ảnh minh họa tiếng Anh |
| 1.jpg (3311×1293) | Sơ đồ User-Item Rating Matrix → Collaborative Filtering Model (Prediction, Top-N) | S07 | contain 1160×455 | 2:30–3:00 | Sơ đồ kỹ thuật đúng quan hệ; chữ nhỏ, không yêu cầu đọc hết |
| 12.jpg (850×498) | Matrix factorization: ô known/unknown → user latent factors × item latent factors | S09 | contain 780×457 | 3:31–4:04 | Ảnh minh họa tiếng Anh; khớp trực tiếp ý "phân rã phần đã biết" |
| 6.jpg (574×333) | Sơ đồ người dùng A–D, vật phẩm a–d, mũi tên gợi ý | S11 | contain 760×440 | 4:28–4:58 | **Nhãn tiếng Trung**; lời đọc chỉ nói quan hệ người–vật phẩm, không đọc nhãn |
| 5.jpg (1024×683) | Laptop hiển thị "Recommended for you" (T-shirt, Headphones, Tote bag, Sneakers) | S13 | contain 640×427 | 5:29–6:12 | Watermark nhỏ "Reesert.Oam" — không đọc |
| 11.jpg (640×640) | Kiến trúc e-commerce microservices: Users → Ingress → Frontend (React) → ML Service (Python); Backend API (Node.js) → PostgreSQL, Redis | S15 | contain 520×520 | 6:38–7:06 | **Kiến trúc trong ảnh khác ví dụ trong content** (React/PostgreSQL/Redis thay vì HTML/MySQL/Flask). Lời đọc bám theo ảnh ở mức tổng quát: Frontend, Backend Node.js, cơ sở dữ liệu quan hệ, cache, ML Service Python — không đọc chi tiết lệch |
| 8.jpg (620×620) | Modal "You might also like these" + tùy chọn AI-personalized (best sellers, recently viewed, frequently bought together), badge "Increase CTR by 30%" | S16 | contain 500×500 | 7:06–7:34 | **Con số "30%" là nội dung ảnh minh họa, không phải số liệu đã kiểm chứng** — không đọc |
| 9.jpg (2048×1536) | Lọc cộng tác: 4 sản phẩm, 3 người dùng, mũi tên tương tác | S17 | contain 720×540 | 7:34–7:56 | Ảnh minh họa tiếng Anh |

Tổng: **13/13 ảnh được dùng**, không bỏ trống ảnh nào; ảnh có chữ lỗi/claim chỉ dùng làm minh họa bố cục và đều có ghi chú trên màn hình.

---

## 5. Storyboard 18 cảnh (thời gian ước tính, chốt sau khi đo TTS)

| # | Thời gian | Lời đọc (tóm tắt) | Hình ảnh / chữ trên màn hình | Chuyển động + SFX | Mục tiêu |
|---|---|---|---|---|---|
| S01 | 0:00–0:20 | Chào; câu hỏi "vì sao web gợi ý đúng thứ mình vừa xem?"; giới thiệu SVD + lọc cộng tác; 3 mục tiêu | Ảnh bìa toàn khung → thu về card; tiêu đề "Thuật toán SVD" + "Lọc cộng tác"; 3 chip mục tiêu; An wave | Cover zoom nhẹ; whoosh; card trượt; An vào | Tạo tò mò, nhận diện thương hiệu |
| S02 | 0:20–0:47 | Gợi ý có mặt khắp nơi; hàng nghìn người dùng/sản phẩm; mỗi người tương tác rất ít | Ảnh 7 (LUMA) + ảnh 3 (carousel); nhãn "Trang chủ", "Trong trang sản phẩm"; chip "Đúng người · đúng lúc" | Hai photo card lần lượt; pop; An present | Đặt vấn đề thực tế |
| S03 | 0:47–1:12 | Dữ liệu thành bảng hàng×cột; phần lớn ô trống → ma trận thưa; câu hỏi dự đoán ô trống | Lưới ma trận 8×14 tự dựng, phần lớn ô xám, vài ô điểm sáng; ô "?" amber phóng to | Lưới hiện dần; ô "?" pop + khoanh marker | Hiểu vì sao cần mô hình |
| S04 | 1:12–1:42 | Dựa vào người giống mình; ví dụ An/Bình/AirPods | Ảnh 2; thẻ nguyên lý "Người giống nhau → thích sản phẩm giống nhau"; chip AirPods | Photo card; marker gạch chân; An point_left | Hiểu ý tưởng lọc cộng tác |
| S05 | 1:42–2:08 | Nối user–item thành mạng hành vi; hai cách user-based / item-based; cần cách dự đoán | Ảnh 4; hai nhãn "Dựa trên người dùng" / "Dựa trên sản phẩm"; mũi tên nối | Ảnh hiện; chip hai cách; An point_left | Hiểu CF hoạt động |
| S06 | 2:08–2:30 | Ví dụ phim: hai người xem 3 phim giống nhau → gợi ý phim còn lại | Ảnh 10; flow chip "User 1 ≈ User 2 → phim mới" | Photo card; chip tuần tự; An point_right | Ví dụ trực quan |
| S07 | 2:30–3:00 | Ma trận User-Item; hàng/cột/ô; ví dụ 4 người × 4 sản phẩm; mục tiêu điền ô thiếu | Ảnh 1 (sơ đồ rộng) + bảng 4×4 tự dựng (An/Bình/Chi/Dũng × iPhone/Samsung/MacBook/Chuột); ô "?" | Ảnh trượt; bảng số hiện theo cue; tick; An present | Hiểu cấu trúc dữ liệu |
| S08 | 3:00–3:31 | SVD là gì; A = UΣVᵀ; nghĩa U, Σ, Vᵀ | Công thức lớn JetBrains Mono; 3 thẻ U/Σ/Vᵀ; nhãn kích thước (người dùng × tiềm ẩn, …) | Công thức viết dần; 3 thẻ pop; marker | Nắm công thức |
| S09 | 3:31–4:04 | Yếu tố tiềm ẩn là gì; giữ k yếu tố; phân rã phần đã biết → suy ra phần chưa biết | Ảnh 12; 3 chip "đã biết" (vàng) / "chưa biết" (xám) / "suy ra" (cam); callout "hệ thống tự học, không phải nhãn người đặt" | Photo card; chip lần lượt; An point_right | Hiểu bản chất tiềm ẩn |
| S10 | 4:04–4:28 | Trở lại bảng 4×4; hai nhóm sở thích; giữ 2 yếu tố (thiết bị / phụ kiện); lưu ý diễn giải | Bảng lớn 4×4, hàng An–Bình tô cyan, Chi–Dũng tô violet; 2 thẻ "Yếu tố 1 · thiết bị", "Yếu tố 2 · phụ kiện" | Hàng tô màu theo cue; thẻ pop; An write | Nối ví dụ với lý thuyết |
| S11 | 4:28–4:58 | R̂ = U_kΣ_kV_kᵀ; lấp ô trống; ví dụ điểm An/AirPods 4,8, Sony 4,6; ghi chú minh họa | Ảnh 6; công thức R̂; 2 chip điểm dự đoán; caveat "Số liệu minh họa" | Photo card; công thức; chip pop; An point_left | Hiểu tái tạo & dự đoán |
| S12 | 4:58–5:29 | Quy trình 5 bước; công thức r̂ = μ + b_u + b_i + q_iᵀp_u; nghĩa từng thành phần | 5 chip bước (thu thập → ma trận → huấn luyện → dự đoán → Top-N); card công thức; 5 nhãn nghĩa | Chip tuần tự + tick; công thức hiện; marker từng số hạng | Nắm quy trình & công thức |
| S13 | 5:29–6:12 | Surprise; pip install; dữ liệu 3 cột; khởi tạo SVD; fit/predict; hàm Top-N; lưu ý Surprise SVD ≠ SVD thường | Code card (JetBrains Mono): import, ratings, SVD(n_factors=2, n_epochs=100, lr_all=0.005, reg_all=0.02), fit, predict, recommend; ảnh 5 nhỏ cuối cảnh | Gõ code + tick; ảnh 5 trượt vào; caveat | Biết triển khai thực tế |
| S14 | 6:12–6:38 | RMSE, MAE; bảng 3 mô hình 0,95/0,78/0,62; RMSE thấp chưa chắc Top-N tốt | 2 card công thức; bảng 3 dòng (minh họa); highlight mô hình C; chip Precision/Recall/F1 | Card + bảng hiện; marker khoanh C; caveat | Biết đánh giá mô hình |
| S15 | 6:38–7:06 | Kiến trúc tham khảo; Frontend, Backend Node.js, ML Service Python, DB, cache; API recommendations; JSON | Ảnh 11; card `GET /api/recommendations/An`; JSON mẫu; luồng mũi tên | Photo card; JSON gõ dần; An present | Hiểu tích hợp hệ thống |
| S16 | 7:06–7:34 | Ưu/nhược; Cold Start; 4 cách xử lý | 2 cột Ưu điểm / Hạn chế; callout Cold Start; 4 chip giải pháp; ảnh 8 nhỏ | Thẻ hiện theo cue; callout amber; ảnh 8 trượt; An point_left | Dùng đúng ngữ cảnh |
| S17 | 7:34–7:56 | CF là phương pháp; SVD là kỹ thuật; quan hệ; không phải CF nào cũng dùng SVD | Ảnh 9; bảng so sánh 2 cột CF / SVD; câu chốt underline | Photo card; bảng hiện; marker gạch chân | Phân biệt khái niệm |
| S18 | 7:56–8:20 | Tổng kết 3 ý; câu hỏi sản phẩm mới; cảm ơn, theo dõi kênh, hẹn bài sau | 3 thẻ tổng kết; thẻ câu hỏi; logo An Tech + "Hẹn gặp lại" | Thẻ pop; chime; logo pop; An wave | Củng cố & kết bài |

Nhịp: 18 cảnh, 22–43 s/cảnh, 5–8 cue; cảnh công thức/code dài hơn để có thời gian đọc; không cắt cảnh liên tục. Tổng ước tính ~7:20; nếu đo TTS vượt 7:45 sẽ cắt gọn cue ở S12–S13 (ghi rõ khi báo cáo).

---

## 6. Kịch bản lời đọc khóa (~1.350 từ, 108 cue)

Quy ước: số thập phân đọc bằng lời ("bốn phẩy tám"); ký hiệu đọc bằng tên ("R mũ", "V chuyển vị"); chỉ dẫn diễn xuất trong ngoặc vuông là chỉ dẫn sản xuất, không đọc.

### S01 — Lời chào + ảnh bìa
- `s01c1` [Thân thiện, năng lượng] Xin chào các bạn! Chào mừng đến với An Tech Academy.
- `s01c2` [Tò mò] Bạn đã bao giờ tự hỏi: vì sao vừa xem một món hàng, trang web đã gợi ý thêm hàng loạt sản phẩm tương tự?
- `s01c3` [Dừng ngắn] Đằng sau những ô gợi ý đó thường là một thuật toán mang tên SVD.
- `s01c4` [Giới thiệu] Hôm nay, chúng ta cùng tìm hiểu SVD, và ứng dụng của nó trong lọc cộng tác, Collaborative Filtering.
- `s01c5` [Chắc giọng] Sau bài học, bạn sẽ hiểu bản chất, đọc được công thức, và chạy được một mô hình gợi ý đơn giản bằng Python.

### S02 — Gợi ý có mặt khắp nơi
- `s02c1` [Kể chuyện] Những mục như "dành riêng cho bạn" hay "có thể bạn cũng thích" đã trở nên quen thuộc.
- `s02c2` Chúng xuất hiện trên trang chủ, trong trang sản phẩm, và cả trong khung giỏ hàng.
- `s02c3` [Nhấn] Mục tiêu rất rõ: đưa đúng sản phẩm đến đúng người, trước khi người đó phải tự tìm.
- `s02c4` Nhưng làm được điều này không hề đơn giản.
- `s02c5` Một website có thể có hàng nghìn người dùng và hàng nghìn sản phẩm; mỗi người chỉ tương tác với một phần rất nhỏ.

### S03 — Ma trận thưa và câu hỏi trung tâm
- `s03c1` Hãy hình dung toàn bộ lượt xem, lượt mua và đánh giá được ghi lại thành một bảng.
- `s03c2` Mỗi hàng là một người dùng, mỗi cột là một sản phẩm.
- `s03c3` [Giải thích bình tĩnh] Phần lớn các ô trong bảng đều trống, vì một người chỉ từng xem hoặc mua vài món.
- `s03c4` [Nhấn] Câu hỏi trung tâm là: dự đoán những ô còn trống đó.
- `s03c5` Nói cách khác: đoán xem người dùng sẽ thích sản phẩm nào, dù họ chưa từng tương tác với nó.

### S04 — Lọc cộng tác là gì
- `s04c1` Cách tự nhiên nhất là dựa vào những người có sở thích giống nhau.
- `s04c2` Nếu hai người cùng thích điện thoại và laptop giống nhau, hệ thống có thể đoán họ sẽ còn thích thêm những món giống nhau.
- `s04c3` [Chắc giọng] Đó chính là lọc cộng tác, Collaborative Filtering.
- `s04c4` Ví dụ: An thích iPhone, MacBook và AirPods. Bình cũng thích iPhone và MacBook, nhưng chưa đánh giá AirPods.
- `s04c5` Hệ thống có thể đề xuất AirPods cho Bình, vì An, người có sở thích tương tự, đã đánh giá cao món này.

### S05 — Lọc cộng tác hoạt động thế nào
- `s05c1` Trong lọc cộng tác, mỗi người dùng được nối với những sản phẩm họ đã xem, mua hoặc đánh giá.
- `s05c2` Những đường nối dày lên thành một mạng các hành vi.
- `s05c3` Có hai cách tiếp cận quen thuộc: dựa trên người dùng, và dựa trên sản phẩm.
- `s05c4` Cách dựa trên người dùng: tìm những người giống mình, rồi xem họ thích gì.
- `s05c5` Cách dựa trên sản phẩm: tìm những sản phẩm thường xuất hiện cùng nhau.
- `s05c6` [Chuyển ý] Nhưng cả hai cách đều cần một thứ: cách so sánh và dự đoán đủ mạnh.

### S06 — Ví dụ dựa trên người dùng
- `s06c1` Một ví dụ dễ thấy là gợi ý phim.
- `s06c2` Hai người cùng xem và thích ba bộ phim giống nhau; họ được xem là người dùng tương tự.
- `s06c3` Một người trong số đó đã xem thêm một bộ phim khác.
- `s06c4` Hệ thống có thể gợi ý bộ phim đó cho người còn lại.
- `s06c5` Đây là lọc cộng tác dựa trên người dùng, ở dạng đơn giản nhất.

### S07 — Ma trận người dùng – sản phẩm
- `s07c1` Để máy tính xử lý, ta biểu diễn dữ liệu thành ma trận người dùng – sản phẩm, User-Item Matrix.
- `s07c2` Hàng là người dùng; cột là sản phẩm; mỗi ô là điểm đánh giá.
- `s07c3` Ví dụ với bốn người: An, Bình, Chi, Dũng; và bốn sản phẩm: iPhone, Samsung, MacBook, Chuột.
- `s07c4` An và Bình cho điểm cao điện thoại và laptop; Chi và Dũng lại thích chuột hơn.
- `s07c5` [Nhấn] Mục tiêu của mô hình gợi ý là điền vào các ô còn thiếu.
- `s07c6` Và SVD là một kỹ thuật giúp làm việc đó.

### S08 — SVD là gì
- `s08c1` [Chậm, rõ] SVD là viết tắt của Singular Value Decomposition, tức phân rã giá trị suy biến.
- `s08c2` Đây là một kỹ thuật trong đại số tuyến tính.
- `s08c3` Với ma trận dữ liệu A, SVD phân rã A thành tích của ba ma trận: A bằng U, nhân Sigma, nhân V chuyển vị.
- `s08c4` U mô tả quan hệ giữa người dùng với các yếu tố tiềm ẩn.
- `s08c5` Sigma là ma trận đường chéo, cho biết mỗi yếu tố quan trọng đến mức nào.
- `s08c6` V chuyển vị mô tả quan hệ giữa sản phẩm với các yếu tố tiềm ẩn.

### S09 — Yếu tố tiềm ẩn
- `s09c1` [Giải thích] "Tiềm ẩn" nghĩa là hệ thống tự học ra, không phải nhãn do con người đặt trước.
- `s09c2` Ta có thể hiểu mỗi yếu tố như một trục sở thích: chẳng hạn, thích thiết bị công nghệ, hoặc thích phụ kiện.
- `s09c3` SVD cho phép giữ lại một số ít yếu tố quan trọng nhất.
- `s09c4` Những ô đã biết giúp tìm ra các vector tiềm ẩn của người dùng và sản phẩm.
- `s09c5` Từ đó, nhân chúng với nhau để ước lượng những ô còn trống.
- `s09c6` [Chốt ý] Đây chính là ý tưởng cốt lõi: phân rã phần đã biết, để suy ra phần chưa biết.

### S10 — Ví dụ số
- `s10c1` Trở lại bảng đánh giá của An, Bình, Chi, Dũng.
- `s10c2` An và Bình thích iPhone, Samsung và MacBook; Chi và Dũng thích chuột.
- `s10c3` Hãy giữ lại hai yếu tố tiềm ẩn.
- `s10c4` Yếu tố thứ nhất có thể hiểu là xu hướng thích thiết bị; yếu tố thứ hai là xu hướng thích phụ kiện.
- `s10c5` [Lưu ý] Đây là cách diễn giải để dễ hiểu; thuật toán không tự đặt tên cho các yếu tố.

### S11 — Tái tạo ma trận và dự đoán
- `s11c1` Sau khi giữ lại k yếu tố, hệ thống tính ma trận xấp xỉ R mũ.
- `s11c2` R mũ bằng U con k, nhân Sigma con k, nhân V chuyển vị con k.
- `s11c3` Ma trận xấp xỉ lấp những ô trống bằng điểm dự đoán.
- `s11c4` Các ô đã có vẫn được tái tạo gần đúng; sai số càng nhỏ càng tốt.
- `s11c5` Với An, hệ thống có thể dự đoán AirPods khoảng bốn phẩy tám, tai nghe Sony khoảng bốn phẩy sáu.
- `s11c6` [Lưu ý] Các điểm này chỉ để minh họa; kết quả thực tế phụ thuộc dữ liệu và cách huấn luyện.

### S12 — Quy trình và công thức dự đoán
- `s12c1` Có thể hình dung quy trình gồm năm bước.
- `s12c2` Một: thu thập dữ liệu tương tác. Hai: xây dựng ma trận người dùng – sản phẩm.
- `s12c3` Ba: huấn luyện mô hình để tìm vector tiềm ẩn. Bốn: dự đoán điểm cho sản phẩm chưa tương tác.
- `s12c4` Năm: xếp hạng và chọn Top N sản phẩm để gợi ý.
- `s12c5` [Chậm] Trong nhiều hệ thống, điểm dự đoán có dạng: r mũ bằng mu, cộng b-u, cộng b-i, cộng q-i chuyển vị nhân p-u.
- `s12c6` Mu là trung bình chung; b-u và b-i là độ lệch của người dùng và sản phẩm; p-u và q-i là hai vector tiềm ẩn.
- `s12c7` Tích vô hướng q-i chuyển vị nhân p-u đo mức độ tương thích giữa sở thích người dùng và đặc điểm sản phẩm.

### S13 — Thực hành với Python
- `s13c1` Lý thuyết là vậy. Giờ hãy xem một lập trình viên triển khai thế nào.
- `s13c2` Thư viện Surprise trong Python hỗ trợ xây dựng hệ thống gợi ý từ dữ liệu đánh giá.
- `s13c3` Cài đặt bằng pip install scikit-surprise và pandas.
- `s13c4` Dữ liệu chỉ cần ba cột: mã người dùng, mã sản phẩm, và điểm đánh giá.
- `s13c5` [Quy trình] Ta khởi tạo mô hình SVD với hai yếu tố tiềm ẩn, một trăm vòng huấn luyện, tốc độ học không phẩy không không năm, và hệ số điều chuẩn không phẩy không hai.
- `s13c6` Gọi fit để huấn luyện; gọi predict để dự đoán điểm của An cho AirPods.
- `s13c7` Hàm gợi ý sẽ duyệt các sản phẩm chưa được đánh giá, dự đoán điểm, sắp xếp giảm dần và lấy Top N.
- `s13c8` [Lưu ý] SVD của Surprise là phương pháp phân rã ma trận tối ưu trên các đánh giá đã biết; nó không điền số 0 vào ô trống rồi chạy SVD thông thường.

### S14 — Đánh giá hiệu quả
- `s14c1` Một mô hình chạy được chưa chắc đã tốt. Ta cần đo sai số dự đoán.
- `s14c2` RMSE là căn bậc hai của trung bình bình phương sai số.
- `s14c3` MAE là trung bình giá trị tuyệt đối của sai số.
- `s14c4` [Ví dụ] Ba mô hình minh họa có RMSE lần lượt không phẩy chín mươi lăm, không phẩy bảy mươi tám, và không phẩy sáu mươi hai.
- `s14c5` Theo RMSE, mô hình thứ ba tốt nhất, vì sai số thấp nhất.
- `s14c6` Tuy vậy, RMSE thấp chưa chắc danh sách Top N đã tốt; khi cần, ta đánh giá thêm bằng Precision, Recall và F1.

### S15 — Tích hợp vào hệ thống thực tế
- `s15c1` Trong một dự án thật, mô hình gợi ý thường đứng sau một kiến trúc như thế này.
- `s15c2` Frontend hiển thị sản phẩm; Backend xử lý nghiệp vụ; cơ sở dữ liệu lưu lịch sử tương tác.
- `s15c3` Một dịch vụ Machine Learning bằng Python đảm nhiệm việc huấn luyện và dự đoán; thêm cache để tăng tốc.
- `s15c4` Khi người dùng mở trang, Backend gọi dịch vụ gợi ý, ví dụ: GET /api/recommendations/An.
- `s15c5` Dịch vụ trả về JSON gồm mã sản phẩm và điểm dự đoán.
- `s15c6` Backend dùng mã đó để lấy tên, giá, hình ảnh và hiển thị danh sách gợi ý.
- `s15c7` [Chốt ý] SVD không quản lý giao diện, giỏ hàng hay thanh toán; nó chỉ phụ trách phân tích dữ liệu và dự đoán sở thích.

### S16 — Ưu điểm, hạn chế và Cold Start
- `s16c1` Vậy khi nào nên dùng SVD?
- `s16c2` Ưu điểm: khám phá sở thích tiềm ẩn, giảm số chiều dữ liệu, dự đoán được sản phẩm chưa đánh giá.
- `s16c3` Hạn chế: cần dữ liệu tương tác để học, cần thời gian huấn luyện, và chất lượng phụ thuộc dữ liệu.
- `s16c4` [Nhấn] Một vấn đề quan trọng là Cold Start.
- `s16c5` Cold Start xảy ra khi người dùng hoặc sản phẩm mới chưa có đủ dữ liệu tương tác.
- `s16c6` Khi đó, SVD không có đủ lịch sử để suy ra sở thích.
- `s16c7` Cách xử lý: tạm dùng gợi ý theo độ phổ biến, khai thác thông tin danh mục, hoặc hỏi sở thích ban đầu khi đăng ký.
- `s16c8` Và thường kết hợp nhiều phương pháp để bù dữ liệu.

### S17 — Phân biệt SVD và lọc cộng tác
- `s17c1` Cuối cùng, phân biệt hai khái niệm dễ nhầm.
- `s17c2` Collaborative Filtering là phương pháp giải bài toán gợi ý, dựa trên hành vi của nhiều người dùng.
- `s17c3` SVD là một kỹ thuật phân rã ma trận, giúp tìm cấu trúc tiềm ẩn trong dữ liệu.
- `s17c4` [Chốt] Nói ngắn: lọc cộng tác là phương pháp; SVD là công cụ có thể dùng bên trong phương pháp đó.
- `s17c5` Không phải mọi hệ thống lọc cộng tác đều dùng SVD; còn có cách dựa trên người dùng hoặc dựa trên sản phẩm.

### S18 — Tổng kết và lời kết
- `s18c1` [Tổng kết] Ba ý quan trọng nhất.
- `s18c2` Một: dữ liệu tương tác được biểu diễn thành ma trận người dùng – sản phẩm.
- `s18c3` Hai: SVD phân rã ma trận để tìm các yếu tố tiềm ẩn.
- `s18c4` Ba: từ mô hình đã học, hệ thống dự đoán điểm cho những ô còn trống và xếp hạng để gợi ý.
- `s18c5` [Câu hỏi] Nếu một sản phẩm mới hoàn toàn, chưa ai đánh giá, em sẽ xử lý thế nào?
- `s18c6` Cảm ơn các bạn đã theo dõi. Hãy nhấn theo dõi kênh An Tech Academy để không bỏ lỡ bài tiếp theo.
- `s18c7` Hẹn gặp lại các bạn trong bài giảng sau.

---

## 7. Kiểm chứng nội dung và giới hạn (ghi trung thực)

1. **Công thức:** A = UΣVᵀ và R̂ = U_kΣ_kV_kᵀ đúng chuẩn SVD; r̂_ui = μ + b_u + b_i + q_iᵀp_u là dạng biased matrix factorization phổ biến — trình bày là "trong nhiều hệ thống", không tuyệt đối hóa.
2. **Surprise SVD:** là Funk-SVD (SGD trên đánh giá đã biết, có bias), **không phải** SVD thông thường trên ma trận điền 0 — đã đưa vào lời đọc S13 và chip trên màn hình.
3. **Dữ liệu ví dụ:** điểm của An/Bình/Chi/Dũng là **giả định** theo `content.md`; điểm dự đoán 4,8 / 4,6 và bảng RMSE 0,95 / 0,78 / 0,62 là **số minh họa**, có caption "Số liệu minh họa" trên màn hình.
4. **Ảnh 3, 5, 8:** mockup AI có chữ lỗi / claim "30%" — chỉ dùng minh họa bố cục, không đọc chữ trong ảnh, có ghi chú khi hiển thị.
5. **Ảnh 11:** kiến trúc trong ảnh (React / PostgreSQL / Redis) khác ví dụ trong content (HTML / MySQL / Flask); lời đọc bám ảnh ở mức thành phần, không nhắc công nghệ lệch.
6. **Ảnh 6:** nhãn tiếng Trung — lời đọc chỉ nói quan hệ người dùng – vật phẩm.
7. **Phát âm:** chưa xác minh. Sẽ gửi sampler ở Cổng B; chỉ đánh dấu "đã kiểm" sau khi người dùng nghe và xác nhận.
8. **Thời lượng:** ước tính từ số từ; số thực tế chốt sau khi đo TTS (có thể cắt gọn S12–S13 nếu vượt 7:45).

---

## 8. Kế hoạch Cổng B (mẫu 30–45 s)

- **Nội dung mẫu:** S01 đầy đủ (chào + hook + mục tiêu) + S02 đầy đủ (2 photo card giao diện) + cue đầu S03 (ma trận thưa) — khoảng 38–44 s.
- **Thể hiện đủ:** lời chào An Tech, thuật ngữ SVD, ảnh bìa + 2 ảnh giao diện, 1 cảnh đồ họa ma trận tự dựng, nhân vật An, phụ đề, SFX, nhận diện.
- **Sampler thuật ngữ:** ~20 s, gồm 3 biến thể "SVD" + 16 từ rủi ro (mục 3).
- **Đầu ra:** `mau/congB/svd_congB_v1.mp4` (1920×1080, 30 fps), file stills kiểm tra, `sampler_thuat_ngu.m4a`; báo cáo đo loudness và thời lượng thực.
- **Chỉ sản xuất full sau khi người dùng duyệt mẫu** (Cổng B), theo MASTER X.

---

## 9. Bàn giao dự kiến (sau Cổng B)

- Video full: `mau/full/svd_full_v1.mp4` — 1920×1080, 30 fps, H.264 CRF18 + AAC 192k, loudnorm −14 LUFS.
- Code: `tools/full_cues.py`, `full_common.py`, `scenes_a/b/c.py`, `demo_full.py`, `demo_gateB.py` (kế thừa kiến trúc bài Hồi quy, không sửa Kit nếu không cần).
- QA: 12 frame trích từ MP4 cuối + bảng nghiệm thu Đạt / Cần sửa / Chưa xác minh; nêu rõ phần chưa nghe kiểm.
- Bản mẫu và bản full đánh số phiên bản, không ghi đè.

---

**Chờ duyệt Cổng A để dựng mẫu 30–45 s.**
