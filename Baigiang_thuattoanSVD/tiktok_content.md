# Content TikTok — Bài giảng SVD (bản 7:41,97)

Nguồn: `mau/full/svd_full_v1.mp4` (1920×1080, 18 cảnh, 108 cue).
Mốc thời gian lấy từ `mau/full/timeline.json`.

---

## 1. Caption chính (đăng kèm video đầy đủ)

Vừa xem iPhone xong, app đã gợi ý ốp lưng, tai nghe, sạc dự phòng?
Không phải app nghe lén. Đó là một bài toán ma trận có tên SVD — Singular Value Decomposition, hay phân rã giá trị suy biến.

Trong 7 phút:
• Vì sao ma trận người dùng – sản phẩm phần lớn là ô trống
• A = UΣVᵀ thực chất nói điều gì
• Cách hệ thống đoán An sẽ cho AirPods 4,8 điểm (số minh họa)
• Code Python với Surprise: fit, predict, Top-N
• RMSE, Cold Start và phân biệt SVD với lọc cộng tác

Xem hết rồi thử 5 câu hỏi ở cuối bài. Lưu lại để ôn phỏng vấn!
Theo dõi AN TECH ACADEMY để học thuật toán theo cách dễ hiểu.
Bạn muốn bài tiếp theo về Cold Start hay Matrix Factorization? Comment nhé.

#hoclaptrinh #machinelearning #thuattoan #SVD #recommendersystem #AI #congnghe #sinhvienIT #hoclaptrinhcungAn #antecacademy #devviet

---

## 2. Caption ngắn để A/B test

**A — tò mò**
App không nghe lén bạn đâu. Nó chỉ đang… nhân ma trận. 7 phút để hiểu SVD — thuật toán đứng sau mọi ô "gợi ý cho bạn".
#hoclaptrinh #SVD #machinelearning #congnghe #antecacademy

**B — phỏng vấn**
Câu hỏi phỏng vấn: "Hệ thống gợi ý hoạt động thế nào?" — Trả lời gọn bằng SVD, ma trận User-Item và vài dòng Python. Video có code chạy được.
#hoclaptrinh #it #phongvanIT #SVD #recommendersystem #antecacademy

**C — học tập**
Học SVD không cần quá giỏi toán: chỉ cần hiểu "tách gu người dùng thành vài trục, rồi nhân lại để đoán ô trống". Ví dụ 4 người dùng + code Surprise ở cuối video.
#hoclaptrinh #thuattoan #machinelearning #sinhvienIT #SVD #antecacademy

---

## 3. Hook 3 giây & chữ trên bìa

Hook (nói hoặc chữ to đầu video):
- "App không nghe lén bạn — nó đang giải một bài toán ma trận."
- "Vì sao vừa xem một món, web đã biết bạn sắp mua gì?"
- "SVD: công thức trông đáng sợ, ý tưởng chỉ có một câu."

Chữ trên bìa:
- Dòng 1: VÌ SAO APP BIẾT BẠN SẮP MUA GÌ?
- Dòng 2: SVD trong 7 phút
- Góc: AN TECH ACADEMY

---

## 4. Comment ghim + comment mốc thời gian

**Ghim:**
Công thức A = UΣVᵀ trông đáng sợ, nhưng thực chất là: tách gu người dùng thành vài "trục sở thích", rồi nhân lại để đoán các ô còn trống. Bạn muốn bài tiếp theo về Cold Start hay Matrix Factorization?

**Mốc thời gian (đăng ngay dưới video):**
00:00 Mở đầu
00:47 Ma trận toàn ô trống
02:34 SVD là gì — A = UΣVᵀ
03:44 Dự đoán An / AirPods 4,8
04:37 Code Python với Surprise
05:16 Đánh giá bằng RMSE
06:22 Cold Start
06:52 Lọc cộng tác vs SVD

---

## 5. Kế hoạch series 3 clip ngắn cắt từ video gốc

| Clip | Nội dung | Cắt từ | Độ dài |
|---|---|---|---|
| 1 | Ma trận toàn ô trống → vì sao cần mô hình | 00:47,7 – 01:07,0 | ~19 s |
| 2 | SVD là gì, công thức A = UΣVᵀ | 02:34,9 – 03:02,3 | ~27 s |
| 3 | 20 dòng code Surprise + dự đoán AirPods | 04:37,3 – 05:16,1 | ~39 s |

- Mỗi clip thêm 2 giây tiêu đề đầu và 3 giây CTA cuối ("Full 7 phút ở video ghim").
- Clip 1 có thể nối thêm 03:44,7 – 04:06,3 (điểm dự đoán 4,8) nếu muốn kết bằng con số.
- Nếu đăng dọc: dùng khung 9:16 nền mờ, giữ nguyên hình 16:9 ở giữa; không crop vì sẽ mất chữ trong khung.

---

## 6. Ghi chú khi đăng

- Video gốc 16:9 → TikTok sẽ có viền trên/dưới; chấp nhận được khi đăng bài giảng, hoặc đăng kèm series clip dọc.
- 7:41 là độ dài dài cho TikTok; ưu tiên đăng 1 clip ngắn/ngày (clip 1 → 2 → 3) rồi dẫn về video đầy đủ.
- Trả lời bình luận trong 30 phút đầu; ghim comment câu hỏi để tăng tương tác.
- Không dùng số liệu 4,8 / 4,6 như kết quả thực nghiệm — luôn ghi rõ "số minh họa".
