# Bảng thuật ngữ & phát âm

**Bài giảng:** Cá nhân hóa người dùng và các thuật toán trong hệ thống gợi ý sản phẩm
**Thương hiệu:** AN TECH ACADEMY · Recommender Systems

> Mục đích: thống nhất cách gọi và cách đọc trước khi tổng hợp giọng đọc (TTS), tránh phát âm sai thuật ngữ.
> Cột "Văn bản TTS" là chuỗi đã nạp vào `cue.tts` trong `src/data/script.mjs`; cột "Hiển thị/Phụ đề" là `cue.say`.
> Nguyên tắc: từ viết tắt đọc tách từng chữ cái; công thức đọc thành lời; số hiệu sản phẩm đọc thành số tiếng Việt.

---

## 1. Giới hạn công cụ (công bố trung thực)

- **Giọng đọc:** Edge TTS **không có giọng nam miền Nam**. Hai giọng tiếng Việt hiện có: `vi-VN-NamMinhNeural` (nam, miền Bắc) và `vi-VN-HoaiMyNeural` (nữ, miền Bắc). Bản mẫu dùng **NamMinhNeural**, tốc độ **+18%** (≈1.18x), giảm tốc ở công thức (+6%…+12%). Yêu cầu "nam miền Nam, 1.15–1.2x" **chưa đáp ứng đúng chất giọng vùng miền**; phương án thay thế: ElevenLabs/Azure Custom Neural Voice (pipeline không phụ thuộc nhà cung cấp). Sẽ xin ý kiến trước khi làm bản đầy đủ.
- **Kiểm tra phát âm:** công cụ hiện tại **không nghe được âm thanh**. Chỉ kiểm tra lập trình được (độ dài, RMS, clipping, khớp mốc phụ đề). Phát âm cảm quan **chưa thể xác minh** bằng máy; cần người nghe duyệt bản mẫu. Bảng dưới là *chủ đích phát âm*, không phải kết quả nghe kiểm chứng.

---

## 2. Thuật ngữ chuyên môn

| Hiển thị / Phụ đề | Thuật ngữ gốc | Nghĩa ngắn gọn | Văn bản TTS (cách đọc) |
|---|---|---|---|
| Hệ thống gợi ý | Recommender System | Hệ thống đề xuất sản phẩm phù hợp từng người | "Hệ thống gợi ý — Recommender System" |
| Hồ sơ sở thích | User Profile | Tập đặc trưng sở thích suy ra từ hành vi | "hồ sơ sở thích — User Profile" |
| Cá nhân hóa | Personalization | Điều chỉnh nội dung theo từng người | "cá nhân hóa" |
| Lọc độ phổ biến | Popularity-based Filtering | Xếp hạng theo số đông (xem/mua/đánh giá) | "lọc độ phổ biến" |
| Lọc cộng tác | Collaborative Filtering | Học từ người có gu giống nhau | "lọc cộng tác — Collaborative Filtering" |
| User-Based | User-Based CF | Tìm **người** giống bạn | "User-Based" (giữ tiếng Anh) |
| Item-Based | Item-Based CF | Tìm **sản phẩm** giống món đã thích | "Item-Based" (giữ tiếng Anh) |
| KNN | K-Nearest Neighbors | K láng giềng gần nhất | "K N N" (tách chữ) |
| Độ tương đồng cosin | Cosine Similarity | Đo góc giữa hai vector | "Cosine Similarity" |
| Tương quan Pearson | Pearson Correlation | Đo tương đồng tuyến tính có trừ trung bình | "Pearson" |
| SVD | Singular Value Decomposition | Phân rã giá trị suy biến | "S V D" (tách chữ) |
| Yếu tố tiềm ẩn | Latent Factors | Chiều ẩn tóm tắt gu (hệ ĐH, cấu hình, camera) | "yếu tố tiềm ẩn — Latent Factors" |
| Phân rã ma trận | Matrix Factorization | Học U, V từ ô đã biết | "Matrix Factorization" |
| FunkSVD | FunkSVD | Biến thể MF tối ưu bằng gradient descent | "Funk S V D" |
| Lọc nội dung | Content-Based Filtering | Học từ chính thuộc tính sản phẩm | "lọc nội dung — Content-Based Filtering" |
| TF-IDF | Term Frequency – Inverse Document Frequency | Trọng số từ: TF×IDF | "T F I D F" (tách chữ) |
| TF | Term Frequency | Tần suất từ trong một mô tả | "T F" |
| IDF | Inverse Document Frequency | Nghịch đảo tần suất tài liệu chứa từ | "I D F" |
| Feature-Based Similarity | Feature-Based Similarity | Tương đồng trên thuộc tính số/danh mục | "Feature-Based Similarity" |
| Hybrid | Hybrid Recommender | Kết hợp nhiều phương pháp | "hybrid" |
| Weighted Hybrid | Weighted | Trộn điểm theo trọng số | "Weighted" |
| Switching Hybrid | Switching | Chọn một phương pháp theo lượng dữ liệu | "Switching" |
| Cascade Hybrid | Cascade | Lọc nối tiếp theo tầng | "Cascade" |
| Khởi đầu lạnh | Cold Start | Người/món mới chưa có dữ liệu | "khởi đầu lạnh" |
| Dữ liệu thưa | Data Sparsity | Ma trận quá ít ô được đánh giá | "dữ liệu thưa" |
| Quá chuyên biệt | Over-specialization | Gợi ý na ná món đã xem, khó bất ngờ | "gợi ý cứ na ná món đã xem" |

---

## 3. Công thức — đọc thành lời

| Hiển thị | Văn bản TTS | Ghi chú |
|---|---|---|
| `A = UΣVᵀ` | "A bằng U nhân Xích-ma nhân V chuyển vị" | Σ đọc "Xích-ma"; Vᵀ đọc "V chuyển vị". Giảm tốc +6%. |
| `Score = 0.5·S_CF + 0.3·S_CB + 0.2·S_POP` | "Score bằng không phẩy năm nhân điểm cộng tác, cộng không phẩy ba nhân điểm nội dung, cộng không phẩy hai nhân điểm phổ biến" | Giảm tốc +8%. Nhấn mạnh **chuẩn hóa trước khi trộn**. |
| `0.5×0.9 + 0.3×0.8 + 0.2×0.5 = 0.79` | "không phẩy năm nhân không phẩy chín, cộng không phẩy ba nhân không phẩy tám, cộng không phẩy hai nhân không phẩy năm, bằng không phẩy bảy chín" | Số hạng đã chuẩn hóa về [0,1]. |
| `r̂(A,I5) = Σ sim·r / Σ sim` (KNN) | "trung bình có trọng số theo độ tương đồng" | k=1, láng giềng D → dự đoán = 5.0. |

---

## 4. Tên riêng, sản phẩm, đơn vị

| Hiển thị | Văn bản TTS | Ghi chú |
|---|---|---|
| An Tech Academy | "An Tech Academy" | Câu chào thương hiệu giữ nguyên văn. |
| Galaxy S24 | "Galaxy S hai bốn" | |
| Galaxy A55 | "Galaxy A năm năm" | |
| iPhone 15 | "iPhone mười lăm" | |
| iPhone 15 Pro | "iPhone mười lăm Pro" | |
| Xiaomi 14 | "Xiaomi mười bốn" | |
| Samsung / Apple / Xiaomi | giữ nguyên | |
| RAM 12GB | "RAM mười hai ghi-ga" | |
| ROM 256GB | "ROM hai trăm năm sáu ghi-ga" | |
| pin 5000mAh | "pin năm nghìn mi-li-am-pe giờ" | |
| pin 5000 (rút gọn) | "pin năm nghìn" | |

---

## 5. Quy ước phát âm đã áp dụng trong script

1. **Viết tắt tách chữ cái** bằng khoảng trắng: `K N N`, `S V D`, `T F I D F`, `T F`, `I D F` — tránh TTS đọc dính thành một từ.
2. **Ký hiệu toán đọc thành lời**: `Σ`→"Xích-ma", `Vᵀ`→"V chuyển vị", `=`→"bằng", `×`/`·`→"nhân", `+`→"cộng".
3. **Số hiệu sản phẩm đọc số tiếng Việt**: S24→"S hai bốn", A55→"A năm năm", 15→"mười lăm", 14→"mười bốn".
4. **Số thập phân**: dấu `.` đọc "phẩy" (0.5→"không phẩy năm").
5. **Giảm tốc cục bộ** bằng `cue.rate` ở cue công thức/nền tảng: mat-1 `+12%`, svd-2 `+6%`, w-2 `+8%` (mặc định `+18%`).
6. **Chỉ dẫn diễn xuất** đặt trong comment, **không** đưa vào văn bản đọc.

> Trạng thái kiểm chứng: các chuyển đổi trên đã nạp vào `cue.tts`. Bản mẫu (intro/personalization/matrix) chưa chứa thuật ngữ viết tắt khó; các chuyển đổi KNN/SVD/TF-IDF/công thức sẽ được nghe kiểm chứng ở bản đầy đủ **sau khi có người duyệt âm thanh**.