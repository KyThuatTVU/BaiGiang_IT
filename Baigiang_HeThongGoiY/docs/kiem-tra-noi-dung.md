# Kiểm tra chuyên môn & độ chính xác nội dung

**Bài giảng:** Cá nhân hóa người dùng và các thuật toán trong hệ thống gợi ý sản phẩm
**Đối chiếu:** MASTER PROMPT (5 phần nội dung bắt buộc, 7 mục tiêu) + `MASTER_DESIGN_VOICE_STANDARD_2.0.md`

> Nguyên tắc: chính xác > phát âm > dễ hiểu > chất lượng nghe nhìn. Mọi số liệu là **GIẢ ĐỊNH để minh họa**, không phải kết quả thực nghiệm. Không coi ô chưa tương tác là điểm 0.

---

## 1. Đối chiếu 7 mục tiêu học tập

| # | Mục tiêu | Cảnh đảm nhiệm | Trạng thái |
|---|---|---|---|
| 1 | Hiểu cá nhân hóa là gì | personalization, matrix | ✅ Có trong mẫu |
| 2 | Phân biệt các phương pháp lọc | popularity, cfintro, tfidf, recap | ✅ Đủ cảnh |
| 3 | KNN trong lọc cộng tác | knn (user/item-based, K, cosine/Pearson) | ✅ Đủ cảnh |
| 4 | SVD & dự đoán điểm | svd (A=UΣVᵀ, latent, tái tạo) | ✅ Đủ cảnh |
| 5 | TF-IDF & Cosine trong lọc nội dung | tfidf, cosine | ✅ Đủ cảnh |
| 6 | Phân biệt Weighted/Switching/Cascade | weighted, switching, cascade, ca-3 | ✅ Đủ cảnh |
| 7 | Xây hệ thống kết hợp thực tế | cascade, ca-4, recap | ✅ Đủ cảnh |

## 2. Đối chiếu 5 phần nội dung bắt buộc

**Phần 1 — Cá nhân hóa:** thu thập hành vi (xem/tìm kiếm/click/đánh giá/mua) → User Profile → danh sách gợi ý.
→ `personalization` (pipeline 4 nút: Hành vi → Hồ sơ → Hệ thống gợi ý → Danh sách). ✅

**Phần 2 — Lọc phổ biến:** ví dụ lượt mua 1000/750/500; ưu/nhược; cùng một danh sách cho mọi người.
→ `popularity` (I1=1000, I3=750, I5=500), `poplimit` (người mới C vẫn có kết quả; ai cũng nhận list giống nhau; thích iPhone vẫn bị gợi ý Samsung). ✅

**Phần 3 — Lọc cộng tác:**
- KNN user-based & item-based, K láng giềng, cosine/Pearson. → `knn`. ✅
- **Phân biệt đo tương đồng ≠ dự đoán điểm.** → `knn-4` nói rõ. ✅
- SVD: ma trận User-Item, ô thiếu, latent factors, A=UΣVᵀ, tái tạo, dự đoán. → `svd-1..3`. ✅
- **Phân biệt SVD nguyên bản ≠ Matrix Factorization/biến thể tối ưu.** → `svd-4` (SVD gốc cần ma trận đầy đủ) + `svd-5` (FunkSVD chỉ học ô đã biết). ✅
- **Không coi ô thiếu = 0.** → `mat-2`, `svd-5`, `q1a`. ✅
- Dữ liệu thưa & khởi đầu lạnh. → `cflimits`. ✅

**Phần 4 — Lọc nội dung:**
- TF-IDF: vai trò TF/IDF, trích từ khóa. → `tfidf`. ✅
- Cosine Similarity: góc giữa vector; ví dụ RAM 12GB/ROM 256GB/pin 5000mAh. → `cosine`, `cos-2`. ✅
- Feature-based cho số/danh mục. → `cos-3`. ✅
- Hạn chế over-specialization. → `cos-4`. ✅

**Phần 5 — Hybrid:**
- Weighted: `Score = 0.5·S_CF + 0.3·S_CB + 0.2·S_POP`; **chuẩn hóa trước**. → `weighted`, `w-4`. ✅
- Switching: mới→Popularity, có lịch sử xem→Content-Based, đủ tương tác→CF. → `switching`, `sw-2`. ✅
- Cascade 4 bước: ứng viên→SVD→Content-Based→xếp hạng top 5. → `cascade`, `ca-2`. ✅
- **Phân biệt rõ 3 chiến lược.** → `ca-3` ("Weighted trộn điểm, Switching chọn một, Cascade lọc nối tiếp. Đừng nhầm là một."). ✅

## 3. Kiểm chứng số liệu (nhất quán với `catalog.mjs`)

| Đại lượng | Giá trị | Kiểm chứng |
|---|---|---|
| Lượt mua phổ biến | I1=1000, I3=750, I5=500 | Đúng ví dụ đề bài. ✅ |
| Điểm phổ biến chuẩn hóa | 1.0 / 0.75 / 0.5 | = buys/1000. ✅ |
| Độ thưa ma trận | 60% | 20 ô, 8 filled (A2+B2+C0+D4), 12 trống → 12/20=60%. ✅ |
| KNN cosine(A,D) | 1.00 | Co-rated I1=5,I2=4 cho cả hai → vector trùng → cos=41/41=1.00. ✅ |
| KNN dự đoán A×I5 | 5.0 | k=1, trung bình trọng số = sim·r(D,I5)/sim = 5.0. ✅ (đã sửa từ 4.6) |
| Weighted I5/A | 0.79 | 0.5×0.9+0.3×0.8+0.2×0.5 = 0.45+0.24+0.10 = 0.79. ✅ |
| Cascade top | I1(0.95, đã sở hữu)→I5(0.88)→I2(0.74)→I4(0.52)→I3(0.38) | I1 owned nên gợi ý thực tế bắt đầu từ I5. ✅ |

> Lưu ý sư phạm: KNN cho 5.0, SVD/MF (cascade) cho 4.6 trên cùng ô A×I5 — **hai thuật toán khác nhau cho dự đoán khác nhau** là chủ đích, không phải mâu thuẫn. Cảnh matrix (mẫu) hiển thị 5.0 khớp KNN.

## 4. Điểm chính xác then chốt (đã rà)

1. **Ô trống ≠ 0** — nhấn ở mat-2, svd-5, q1a; không lấp 0 vào ô thiếu. ✅
2. **SVD gốc vs MF** — svd-4 nêu SVD gốc cần ma trận đầy đủ; svd-5 nêu FunkSVD học ô đã biết. Không đồng nhất hai khái niệm. ✅
3. **Đo tương đồng vs dự đoán điểm** — knn-4 tách bạch: cosine/Pearson đo giống; trung bình trọng số suy ô thiếu. ✅
4. **Chuẩn hóa trước khi trộn** — w-4 bắt buộc; các điểm weighted đã ở [0,1]. ✅
5. **3 hybrid khác bản chất** — ca-3 chốt rõ. ✅
6. **Số liệu giả định** — ghi rõ ở catalog + doc; không khẳng định thực nghiệm. ✅
7. **Câu chào/kết thương hiệu** — giữ nguyên văn theo đề (intro-1, out-1). ✅

## 5. Giới hạn & việc cần chốt trước bản đầy đủ

- **Giọng nam miền Nam:** Edge TTS không có → dùng NamMinh (Bắc) cho mẫu, công bố giới hạn, xin duyệt phương án giọng thay thế. ⚠️
- **Nghe kiểm chứng phát âm:** công cụ không nghe được → cần người duyệt bản mẫu/bản đầy đủ. Các mục "✅" trên là kiểm chứng **nội dung/số liệu**, không phải kiểm chứng **âm thanh cảm quan**. ⚠️
- **Thuật ngữ viết tắt (KNN/SVD/TF-IDF) & công thức:** chưa xuất hiện trong mẫu; sẽ nghe kiểm chứng ở bản đầy đủ. ⚠️
- **Số liệu KNN đã khóa** về giá trị đúng toán (cosine 1.00, dự đoán 5.0). Các builder cảnh full (popularity…quiz) sẽ dựng sau khi duyệt mẫu.

## 6. Kết luận

Nội dung kịch bản **bao phủ đủ 5 phần bắt buộc và 7 mục tiêu**, số liệu minh họa **nhất quán và đúng toán** ở các điểm đã kiểm. Các giới hạn về giọng đọc vùng miền và kiểm chứng âm thanh được **công bố trung thực**, không tự nhận đã hoàn thành khâu nghe duyệt.