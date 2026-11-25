# CỔNG A — STORYBOARD & KỊCH BẢN KHÓA
## Bài: Hồi quy tuyến tính và ứng dụng — AN TECH ACADEMY

**Ngày lập:** 2026-11-25 · **Trạng thái:** chờ duyệt Cổng A (chưa dựng mẫu)
**Nguồn nội dung:** `content.md` (17 mục) · **Yêu cầu riêng:** `note.md` — video khoảng 7 phút
**Chuẩn áp dụng:** MASTER DESIGN & VOICE STANDARD 2.3 + `D:\Edit\AGENTS.md`

---

## 1. Hồ sơ bài giảng

| Hạng mục | Nội dung |
|---|---|
| Chủ đề | Machine Learning — Supervised Learning: hồi quy tuyến tính |
| Đối tượng | Người mới học lập trình, dữ liệu và AI |
| Mục tiêu | Hiểu bản chất; đọc được công thức; tự tính ví dụ 5 căn nhà; biết đánh giá mô hình; nhận diện khi nào nên/không nên dùng |
| Thời lượng dự kiến | 7:10–7:25 (khoảng 1.280 từ lời đọc, đo thực tế sẽ chốt ở Cổng B/full) |
| Giọng đọc | Clone VieNeu mặc định (`Kit/tools/tts_vieneu.py`, ref `ref_final.wav`) — không hỏi lại |
| Nhân vật | Giáo viên An, 7 tư thế, có mặt toàn bộ cảnh (MASTER XVIII) |
| Âm thanh | Giọng + SFX tổng hợp (whoosh/pop/tick/bút/chime), **không nhạc nền** theo chuỗi bài gần nhất |
| Hình ảnh | 11/11 ảnh trong `img/` đều được dùng qua photo card kính (contain/cover) |
| Lời chào | Có mở đầu + lời kết theo mặc định `AGENTS.md` (mẫu S01/S11 bài API) |

**Art direction (AI & Data):** nền navy tối `#0B1220 → #0E1A2E`, lưới mờ, vệt sáng chuyển động nhẹ.
Chữ chính `#ECF1F9`, phụ `#94A3B8`. Accent theo chức năng: cyan `#22D3EE` (dữ liệu), violet `#8B5CF6` (mô hình), amber `#F59E0B` (từ khóa/nhấn), emerald `#34D399` (kết quả đúng), đỏ `#E5484D` (cảnh báo, chỉ dùng ở cảnh giới hạn).
Thẻ/card: nền `#16213A`, viền + gradient accent sáng (~45% xuống ~16%), không trùng màu nền; chữ số dùng Plus Jakarta Sans, code/công thức dùng JetBrains Mono.
Font: Be Vietnam Pro (tiêu đề/nội dung), Plus Jakarta Sans (số liệu), JetBrains Mono (code/công thức) — đúng bộ font Kit.

---

## 2. Bảng thuật ngữ và cách thể hiện trong lời đọc

Nguyên tắc: **một giọng Việt**, không chuyển giọng Anh; thuật ngữ nói bằng tiếng Việt, chữ tiếng Anh giữ trên màn hình. Từ rủi ro sẽ kiểm bằng sampler ngắn ở Cổng B.

| Thuật ngữ | Nhóm | Lời đọc dự kiến | Trên màn hình | Đã kiểm chứng |
|---|---|---|---|---|
| Linear Regression | ML | "hồi quy tuyến tính" (có nhắc "Linear Regression" ở câu mở) | Linear Regression | Chưa (nghe ở Cổng B) |
| Machine Learning | ML | "Machine Learning" (giữ nguyên) | Machine Learning | Chưa |
| Supervised Learning | ML | "Supervised Learning" (giữ nguyên) | Supervised Learning | Chưa |
| Feature / X | ML | "Feature", "biến đầu vào X" | Feature (X) | Chưa |
| Target / Y | ML | "Target", "biến mục tiêu Y" | Target (Y) | Chưa |
| Training data | ML | "Training data", "dữ liệu huấn luyện" | Training data | Chưa |
| Coefficient | ML | "Coefficient", "hệ số" | Coefficient | Chưa |
| Residual | ML | "Residual", "phần dư" | Residual · e = y − ŷ | Chưa |
| OLS | Thống kê | "phương pháp bình phương tối thiểu, OLS" | OLS | Chưa |
| SSE | Thống kê | "tổng bình phương phần dư" | SSE | Chưa |
| MAE | Đánh giá | "MAE" + nghĩa "sai số tuyệt đối trung bình" | MAE | Chưa |
| MSE | Đánh giá | "MSE" | MSE | Chưa |
| RMSE | Đánh giá | "RMSE" + nghĩa "căn bậc hai của MSE" | RMSE | Chưa |
| R² | Đánh giá | "R bình phương" | R² | Chưa |
| ŷ | Ký hiệu | "y mũ" | ŷ | Chưa |
| β₀, β₁, ε | Ký hiệu | "beta không", "beta một", "epsilon" | β₀, β₁, ε | Chưa |
| Multiple Linear Regression | ML | "hồi quy tuyến tính đa biến" | Multiple Linear Regression | Chưa |
| Polynomial Regression | ML | "hồi quy đa thức, Polynomial Regression" | Polynomial Regression | Chưa |
| scikit-learn / pandas / CSV | Công cụ | giữ nguyên tiếng Anh | scikit-learn, pandas, CSV | Chưa |
| Overfitting | ML | "quá khớp" | Overfitting | Chưa |
| Data Leakage | ML | "rò rỉ dữ liệu" | Data Leakage | Chưa |

Kế hoạch kiểm: sampler ~12 s gồm MAE, MSE, RMSE, R², scikit-learn, pandas, CSV, Supervised Learning — gửi kèm mẫu Cổng B để người dùng nghe và chốt cách đọc trước khi sản xuất full.

---

## 3. Kế hoạch dùng 11 ảnh trong `img/`

Đã xem toàn bộ ảnh. Tóm tắt nội dung và vị trí dùng:

| Ảnh | Nội dung ảnh | Cảnh dùng | Chế độ | Thời điểm (ước tính) |
|---|---|---|---|---|
| 01_khai_niem_duong_hoi_quy | 20 căn nhà (chấm xanh) + đường hồi quy đỏ; ghi chú "minh họa giả định" | S02 | contain, card phải | 0:28–0:43 |
| 02_he_so_goc_va_chieu_tuong_quan | 3 panel: góc dương, góc âm, không xu hướng rõ | S05 | contain, card rộng | 1:31–1:54 |
| 03_phan_du_residual | 5 căn nhà: thực tế, dự đoán, phần dư có nhãn; phương trình 0,158 + 0,0229x | S09 | contain, card phải | 3:35–3:54 |
| 04_binh_phuong_toi_thieu | OLS 2 bước: đo phần dư dọc; cột bình phương phần dư (bộ điểm khác ví dụ nhà) | S07 | contain, card phải | 2:22–2:49 |
| 05_cac_dang_hoi_quy | 3 dạng: đơn biến, đa biến (màu X₂), đa thức (parabol) | S11 | contain, card rộng | 4:14–4:31 |
| 06_so_do_hoi_quy_da_bien | 3 đầu vào (diện tích, số phòng, khoảng cách) → mô hình → giá dự đoán | S10 | contain, card phải | 3:56–4:14 |
| 07_quy_trinh_xay_dung_mo_hinh | Quy trình 6 bước có mũi tên | S12 | contain, card rộng | 4:31–4:52 |
| 08_danh_gia_mae_rmse | Trái: y so với ŷ; phải: cột sai số tuyệt đối (hình sơ đồ: cả 6 mẫu lệch đúng 1 đơn vị) | S14 | contain, card phải | 5:15–5:45 |
| 09_chia_train_test | Thanh 80% train / 20% test, chú thích tỷ lệ chỉ là ví dụ | S13 | contain, card trên | 4:54–5:12 |
| 10_hoi_quy_vs_phan_loai | Trái hồi quy (số liên tục); phải phân loại 3 nhóm A/B/C | S04 | contain, card trái | 1:12–1:31 |
| 11_poster_tong_quan | Poster 8 khối tổng quan, có nhân vật An; chữ nhỏ khi thu nhỏ | S16 | contain, card phải, phóng to vừa | 6:15–6:36 |

Ghi chú trung thực:
- **08** là hình **sơ đồ** (cả 6 mẫu đều lệch đúng 1,0). Lời đọc không dùng nó làm số liệu thật; trên hình có chip "Hình minh họa: cả 6 mẫu lệch đúng 1 đơn vị".
- **04** minh họa OLS bằng **bộ điểm khác** ví dụ 5 căn nhà; caption ghi rõ "Bộ điểm minh họa khác ví dụ giá nhà".
- **11** là poster nhiều chữ; ở khung 16:9 chữ nhỏ sẽ không đọc được trên điện thoại — chỉ dùng làm tổng quan, lời đọc điểm tên 6 lĩnh vực, không yêu cầu người học đọc chữ trong ảnh.
- **06** có nhãn "Khoảng cách trung tâm (X₃)" sát mép trái trong ảnh gốc; không cắt, chấp nhận như ảnh người dùng cung cấp.

---

## 4. Storyboard 18 cảnh (thời gian là ước tính, chốt lại sau khi đo TTS)

| # | Thời gian | Lời đọc (tóm tắt) | Hình ảnh / chữ trên màn hình | Chuyển động + SFX | Mục tiêu |
|---|---|---|---|---|---|
| S01 | 0:00–0:19 | Chào + 3 tình huống cần dự đoán số | Tiêu đề "Hồi quy tuyến tính"; 3 thẻ câu hỏi (doanh thu, giá nhà, nhu cầu); An; logo | Thẻ pop + whoosh; An present | Tạo tò mò, nhận diện thương hiệu |
| S02 | 0:19–0:43 | Định nghĩa + học công thức từ dữ liệu | 3 bullet: học có giám sát · đầu vào → kết quả số · học từ dữ liệu; ảnh 01; underline "Linear Regression" | Photo card trượt vào; nét bút marker; An point_left | Hiểu bản chất |
| S03 | 0:43–1:12 | 7 thuật ngữ cốt lõi | Lưới 7 thẻ thuật ngữ; dải e = y − ŷ; nhấn "Residual" | Thẻ hiện lần lượt + pop; khoanh tay "Residual" | Nắm từ vựng trước khi vào công thức |
| S04 | 1:12–1:31 | Hồi quy vs phân loại | 2 cột HỒI QUY / PHÂN LOẠI; ví dụ 2,1 tỷ và 3 nhóm giá; ảnh 10 | Photo card; chip so sánh; An point_left | Phân biệt đúng loại bài toán |
| S05 | 1:31–1:54 | Scatter, dấu hệ số góc, tương quan ≠ nhân quả | Ảnh 02; 3 nhãn "+", "−", "≈ 0"; chip "Tương quan không chứng minh nhân quả" | Khoanh từng panel theo cue; An point_right | Đọc xu hướng trên biểu đồ |
| S06 | 1:54–2:22 | Công thức tổng thể và công thức dự đoán | Bảng công thức Y = β₀ + β₁X + ε; ŷ = b₀ + b₁x; chú thích chặn/góc; ví dụ 0,5 + 0,02x | Viết công thức từng nét; gạch chân; An write | Đọc và hiểu công thức |
| S07 | 2:22–2:49 | OLS, phần dư dọc, bình phương, SSE | 3 bước; ảnh 04; công thức SSE; ghi chú "phần dư theo chiều Y" | Photo card; cột bình phương mọc lên; An point_left | Hiểu vì sao bình phương |
| S08 | 2:49–3:25 | Ví dụ 5 căn nhà: trung bình, b1, b0 | Bảng 5 dòng; pipeline số: x̄=80, ȳ=1,99, Σ=22,9, Σ=1000, b₁=0,0229, b₀=0,158 | Số hiện theo cue; tick; An write | Tự tính được hệ số |
| S09 | 3:25–3:54 | Phương trình, dự đoán 85 m², đọc phần dư | Banner ŷ = 0,158 + 0,0229x; thẻ 85 m² → 2,1045 tỷ; ảnh 03; chip phần dư | Ảnh 03 trượt vào; chip +0,018… −0,069; An point_right | Áp dụng và đọc sai số |
| S10 | 3:54–4:14 | Đa biến, "giữ các biến khác cố định" | Công thức b₀ + b₁x₁ + … + b_p x_p; ảnh 06; callout giữ cố định | Photo card; callout sáng; An point_right | Hiểu hệ số đa biến |
| S11 | 4:14–4:31 | Đa thức, vẫn tuyến tính theo hệ số, cảnh báo bậc cao | Ảnh 05; công thức b₀ + b₁x + b₂x²; chip "bậc cao dễ quá khớp" | Photo card; chip cảnh báo; An point_left | Mở rộng mô hình đúng chỗ |
| S12 | 4:31–4:52 | Quy trình 6 bước | Ảnh 07; 6 chip bước sáng theo cue; chip "kiểm ngoại lệ" | Ảnh 07; chip tuần tự; An present | Nắm quy trình thực tế |
| S13 | 4:52–5:12 | Vì sao chia train/test, 80/20, chuỗi thời gian | Ảnh 09; 2 thẻ 80/20; icon đồng hồ + ghi chú chia theo thời gian | Photo card; thẻ màu; An point_left | Tránh đánh giá lạc quan |
| S14 | 5:12–5:45 | MAE, MSE, RMSE, R²; số của ví dụ; cảnh báo 5 mẫu | 4 công thức; ảnh 08; chip 0,044 · 0,0477 · 0,9787; caveat | Photo card; chip kết quả; An point_left | Biết đọc chỉ số đánh giá |
| S15 | 5:45–6:15 | Giả định, giới hạn, 5 hiểu lầm | 8 thẻ "cần biết" + 5 thẻ "KHÔNG ĐÚNG" gạch chéo bằng nét vẽ; không dùng ảnh | Thẻ hiện theo cue; gạch chéo hand-drawn; An present | Dùng mô hình có trách nhiệm |
| S16 | 6:15–6:36 | 6 lĩnh vực ứng dụng | Ảnh 11 (poster) + 6 chip lĩnh vực; ghi chú kiểm định theo ngành | Photo card; chip tuần tự; An point_right | Liên hệ thực tế |
| S17 | 6:36–6:56 | Python + scikit-learn | Code card: LinearRegression, fit, coef_, intercept_, predict; caveat 10 dòng | Gõ code + tick; An write | Biết quy trình API thư viện |
| S18 | 6:56–7:21 | Tổng kết 3 ý, câu hỏi, cảm ơn, hẹn bài sau | 3 thẻ tổng kết; câu hỏi; logo + "Hẹn gặp lại" | Thẻ + chime; logo pop; An wave | Củng cố và kết bài |

Nhịp: mỗi cảnh 17–36 s, 5–8 cue; cảnh công thức/ví dụ dài hơn để có thời gian quan sát; không cắt cảnh liên tục.

---

## 5. Kịch bản lời đọc khóa (115 cue, ~1.280 từ)

Từ viết theo cách đọc; số thập phân đọc bằng lời; ký hiệu đọc bằng tên ("y mũ", "R bình phương").

### S01 — Hook + lời chào
- `s01c1` Xin chào các bạn! Chào mừng đến với An Tech Academy.
- `s01c2` Hôm nay chúng ta cùng tìm hiểu hồi quy tuyến tính, Linear Regression.
- `s01c3` Một cửa hàng muốn ước tính doanh thu của ngày mai.
- `s01c4` Một người mua nhà muốn biết căn nhà này khoảng bao nhiêu tiền.
- `s01c5` Ta đều có dữ liệu trong quá khứ, và cần ước lượng một con số.

### S02 — Hồi quy tuyến tính là gì
- `s02c1` Hồi quy tuyến tính là một phương pháp học có giám sát, Supervised Learning.
- `s02c2` Nó mô hình hóa quan hệ giữa biến đầu vào và một kết quả dạng số.
- `s02c3` Từ dữ liệu đã có, mô hình học ra một công thức.
- `s02c4` Rồi dùng công thức đó để dự đoán cho trường hợp mới.
- `s02c5` Đây là một trong những bước khởi đầu quen thuộc của Machine Learning.
- `s02c6` Ví dụ, diện tích tăng thì giá thường tăng; nhưng còn vị trí, pháp lý và nhiều yếu tố khác.

### S03 — Thuật ngữ cốt lõi
- `s03c1` Trước khi đi tiếp, ta chốt vài thuật ngữ.
- `s03c2` Feature, hay biến đầu vào X, là thông tin dùng để dự đoán; ví dụ diện tích nhà.
- `s03c3` Target, biến mục tiêu Y, là thứ cần dự đoán; ví dụ giá nhà.
- `s03c4` Training data, dữ liệu huấn luyện, là các cặp X và Y đã biết.
- `s03c5` y là giá trị thực tế. ŷ, đọc là y mũ, là giá trị mô hình dự đoán.
- `s03c6` Coefficient, hệ số, cho biết mức và chiều của mối liên hệ.
- `s03c7` Residual, phần dư, là chênh lệch giữa thực tế và dự đoán.

### S04 — Hồi quy khác phân loại thế nào
- `s04c1` Hồi quy dự đoán một số liên tục: giá nhà, doanh thu, nhiệt độ.
- `s04c2` Phân loại dự đoán một nhãn: spam hay không spam, rời bỏ hay ở lại.
- `s04c3` Dự đoán căn nhà giá hai phẩy một tỷ là hồi quy.
- `s04c4` Xếp căn nhà vào nhóm giá thấp, trung bình, cao là phân loại.
- `s04c5` Hãy nhìn vào kiểu kết quả cần dự đoán.

### S05 — Đường hồi quy và dấu hệ số góc
- `s05c1` Trên biểu đồ phân tán, mỗi chấm là một quan sát.
- `s05c2` Điểm đi lên từ trái sang phải: hệ số góc dương.
- `s05c3` Đi xuống: hệ số góc âm.
- `s05c4` Gần nằm ngang: hệ số góc gần không, nhưng chưa chắc hai biến không liên quan.
- `s05c5` Có thể chúng có quan hệ phi tuyến.
- `s05c6` Và tương quan không chứng minh nhân quả.
- `s05c7` Một yếu tố khác có thể tác động lên cả hai biến.

### S06 — Công thức đơn biến
- `s06c1` Mô hình tổng thể: Y bằng beta không, cộng beta một X, cộng sai số epsilon.
- `s06c2` Sau khi ước lượng từ dữ liệu mẫu, ta được công thức dự đoán.
- `s06c3` ŷ bằng b không, cộng b một nhân x.
- `s06c4` b không là hệ số chặn: giá trị dự đoán khi X bằng không.
- `s06c5` b một là hệ số góc: Y thay đổi bao nhiêu khi X tăng một đơn vị.
- `s06c6` Ví dụ, ŷ bằng không phẩy năm, cộng không phẩy không hai nhân x.
- `s06c7` Diện tích tăng một mét vuông, giá dự đoán tăng khoảng hai mươi triệu.

### S07 — Bình phương tối thiểu (OLS)
- `s07c1` Một đường thẳng nào cũng vẽ được, nhưng không phải đường nào cũng phù hợp.
- `s07c2` Hồi quy tuyến tính thường dùng phương pháp bình phương tối thiểu, OLS.
- `s07c3` Với mỗi điểm, phần dư là thực tế trừ dự đoán, đo theo chiều dọc.
- `s07c4` Nếu cộng có dấu, sai số dương và âm triệt tiêu nhau.
- `s07c5` Vì vậy OLS bình phương từng phần dư rồi cộng lại.
- `s07c6` Sai số lớn bị phạt mạnh hơn sai số nhỏ.
- `s07c7` Mô hình chọn bộ hệ số làm tổng bình phương phần dư nhỏ nhất.

### S08 — Ví dụ tính tay: từ dữ liệu đến hệ số
- `s08c1` Cùng tính tay với năm căn nhà giả định.
- `s08c2` Diện tích: sáu mươi, bảy mươi, tám mươi, chín mươi và một trăm mét vuông.
- `s08c3` Giá tương ứng: một phẩy năm lăm; một phẩy bảy hai; hai phẩy không năm; hai phẩy mười lăm; hai phẩy bốn tám, đơn vị tỷ đồng.
- `s08c4` Trung bình diện tích là tám mươi; trung bình giá là một phẩy chín chín.
- `s08c5` Tổng tích độ lệch là hai mươi hai phẩy chín.
- `s08c6` Tổng bình phương độ lệch diện tích là một nghìn.
- `s08c7` Vậy b một bằng hai mươi hai phẩy chín chia một nghìn, tức không phẩy không hai hai chín.
- `s08c8` b không bằng một phẩy chín chín, trừ không phẩy không hai hai chín nhân tám mươi, ra không phẩy một năm tám.

### S09 — Phương trình, dự đoán và phần dư
- `s09c1` Phương trình hồi quy: ŷ bằng không phẩy một năm tám, cộng không phẩy không hai hai chín x.
- `s09c2` Căn nhà tám mươi lăm mét vuông được dự đoán khoảng hai phẩy một không bốn lăm tỷ.
- `s09c3` So sánh với thực tế, ta có phần dư ở từng điểm.
- `s09c4` Phần dư dương: mô hình dự đoán thấp hơn thực tế.
- `s09c5` Phần dư âm: mô hình dự đoán cao hơn thực tế.
- `s09c6` Đây là dữ liệu học tập, không phải giá thị trường.
- `s09c7` Và sai số này chỉ mô tả mô hình, không phải quy luật cho mọi căn nhà.

### S10 — Hồi quy tuyến tính đa biến
- `s10c1` Thực tế, giá nhà còn phụ thuộc số phòng, vị trí và tuổi công trình.
- `s10c2` Từ hai biến đầu vào trở lên, ta có hồi quy tuyến tính đa biến.
- `s10c3` Công thức thêm b hai x hai, cho đến b p x p.
- `s10c4` Mỗi hệ số cho biết mức thay đổi khi một biến tăng, các biến khác giữ cố định.
- `s10c5` Cụm giữ các biến khác cố định rất quan trọng khi diễn giải.

### S11 — Hồi quy đa thức
- `s11c1` Không phải quan hệ nào cũng là đường thẳng.
- `s11c2` Có thể thêm x bình phương, x lập phương vào mô hình.
- `s11c3` Đó là hồi quy đa thức, Polynomial Regression.
- `s11c4` Đường dự đoán cong, nhưng mô hình vẫn tuyến tính theo hệ số.
- `s11c5` Bậc quá cao dễ bám nhiễu, nên phải kiểm tra trên dữ liệu chưa thấy.

### S12 — Quy trình xây dựng mô hình
- `s12c1` Một dự án thực tế thường đi qua sáu bước.
- `s12c2` Thu thập dữ liệu; làm sạch và khám phá.
- `s12c3` Chia train, test; huấn luyện mô hình.
- `s12c4` Đánh giá hiệu suất; dự đoán và theo dõi.
- `s12c5` Dữ liệu phải đúng nguồn và đại diện cho tình huống cần dự đoán.
- `s12c6` Đừng xóa ngoại lệ máy móc: cần biết đó là lỗi hay trường hợp thật.
- `s12c7` Khi quan hệ thay đổi, phải huấn luyện lại.

### S13 — Vì sao chia train và test
- `s13c1` Nếu học và chấm điểm trên cùng một tập, kết quả sẽ lạc quan.
- `s13c2` Vì vậy chia dữ liệu thành tập huấn luyện và tập kiểm tra.
- `s13c3` Ví dụ tám mươi phần trăm để học, hai mươi phần trăm để kiểm tra.
- `s13c4` Tỷ lệ chỉ là ví dụ, phụ thuộc quy mô và đặc điểm dữ liệu.
- `s13c5` Dữ liệu chuỗi thời gian phải chia theo thời gian, không trộn tương lai vào quá khứ.

### S14 — Các chỉ số đánh giá
- `s14c1` Đừng chỉ nhìn một con số rồi kết luận mô hình tốt hay xấu.
- `s14c2` MAE là sai số tuyệt đối trung bình, cùng đơn vị với biến mục tiêu.
- `s14c3` MSE bình phương sai số trước khi lấy trung bình, nên sai số lớn bị phạt mạnh.
- `s14c4` RMSE là căn bậc hai của MSE.
- `s14c5` R bình phương cho biết mức mô hình giải thích biến thiên của Y.
- `s14c6` Với năm điểm trên, MAE khoảng không phẩy không bốn bốn tỷ.
- `s14c7` RMSE khoảng không phẩy không bốn bảy bảy; R bình phương khoảng không phẩy chín bảy tám bảy.
- `s14c8` Nhưng chỉ năm mẫu, không có tập kiểm tra: đây không phải bằng chứng dự đoán thực tế.

### S15 — Giả định, giới hạn, hiểu lầm
- `s15c1` Có vài giả định và giới hạn cần biết.
- `s15c2` Quan hệ trung bình phải gần tuyến tính; sai số không phụ thuộc hệ thống vào nhau.
- `s15c3` Ngoại lệ mạnh có thể kéo đường hồi quy lệch hẳn.
- `s15c4` Đa cộng tuyến làm hệ số khó diễn giải; dữ liệu rò rỉ làm kết quả ảo.
- `s15c5` Ngoại suy quá xa vùng dữ liệu rất rủi ro.
- `s15c6` Đường hồi quy không cần đi qua mọi điểm.
- `s15c7` R bình phương cao chưa chắc mô hình tốt; nó không phải tỷ lệ dự đoán đúng.
- `s15c8` Và nhiều dữ liệu hơn chưa chắc tốt hơn nếu dữ liệu sai hoặc không đại diện.

### S16 — Ứng dụng thực tế
- `s16c1` Hồi quy tuyến tính có mặt ở nhiều ngành.
- `s16c2` Thương mại điện tử dự báo doanh thu và nhu cầu tồn kho.
- `s16c3` Bất động sản ước tính giá; tài chính phân tích chi phí, lợi nhuận.
- `s16c4` Giáo dục ước lượng điểm số; y tế hỗ trợ nghiên cứu chỉ số liên tục.
- `s16c5` Nông nghiệp và năng lượng dự báo sản lượng, nhu cầu điện.
- `s16c6` Mỗi ngành vẫn cần dữ liệu và quy trình kiểm định phù hợp.

### S17 — Thực hành Python và scikit-learn
- `s17c1` Trong thực tế, ta dùng thư viện thay vì tính tay.
- `s17c2` Pandas đọc tệp CSV; scikit-learn chia dữ liệu và huấn luyện.
- `s17c3` LinearRegression, rồi model.fit để học hệ số.
- `s17c4` model.coef và model.intercept cho hệ số góc và hệ số chặn.
- `s17c5` model.predict dự đoán giá căn nhà tám mươi lăm mét vuông.
- `s17c6` Nhưng mười dòng dữ liệu vẫn quá ít để kết luận mô hình tổng quát.

### S18 — Tổng kết và lời kết
- `s18c1` Tóm lại: hồi quy tuyến tính mô hình hóa quan hệ giữa đầu vào và kết quả số.
- `s18c2` OLS chọn hệ số để tổng bình phương phần dư nhỏ nhất.
- `s18c3` Muốn đánh giá đúng, hãy chia train test và đọc MAE, RMSE, R bình phương.
- `s18c4` Câu hỏi cho bạn: với dữ liệu của mình, bạn sẽ chọn biến mục tiêu nào?
- `s18c5` Cảm ơn các bạn đã theo dõi. Hãy theo dõi kênh An Tech Academy để học tiếp.
- `s18c6` Hẹn gặp lại ở bài giảng tiếp theo!

---

## 6. Kế hoạch Cổng B — mẫu 30–45 s

**Nội dung mẫu:** S01 (toàn bộ, ~19 s) + S02 (toàn bộ, ~24 s) + 3–5 s đầu S03 để lộ thẻ thuật ngữ → mục tiêu 42–45 s.
Mẫu thể hiện đủ: lời chào An Tech Academy · thuật ngữ CNTT (Linear Regression, Supervised Learning, Feature/Target) · photo card ảnh 01 + nét bút + nhân vật An + SFX + caption + màu sắc/typography.
Kèm **sampler phát âm 12 s** (một giọng clone): "Supervised Learning. Linear Regression. MAE. MSE. RMSE. R bình phương. scikit-learn. pandas. CSV." để người dùng chốt cách đọc trước khi sản xuất full.
Chưa dựng full ở Cổng A.

---

## 7. Điểm cần người dùng duyệt ở Cổng A

1. Thời lượng ~7:10–7:25 và nhịp 18 cảnh (có thể gộp S12+S13 nếu thấy dài).
2. Không nhạc nền, chỉ giọng + SFX (theo chuỗi bài gần nhất).
3. Giọng clone mặc định; sampler phát âm gửi kèm Cổng B.
4. Kế hoạch dùng 11/11 ảnh như mục 3 (đặc biệt ảnh 11 poster thu nhỏ, ảnh 08 là sơ đồ).
5. Phạm vi mẫu Cổng B: S01 + S02 + mở đầu S03.

Sau khi duyệt Cổng A, tôi dựng mẫu Cổng B (chưa đụng bản full), gửi kèm sampler phát âm và bảng trạng thái trung thực.
