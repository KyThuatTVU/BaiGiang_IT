# Lời thoại đầy đủ (bản duyệt kịch bản)

**Bài giảng:** Cá nhân hóa người dùng và các thuật toán trong hệ thống gợi ý sản phẩm · AN TECH ACADEMY

> Đây là toàn bộ lời thoại sẽ đọc ở bản đầy đủ (23 cảnh, 64 cue). Mốc thời gian từng cue sẽ chốt sau khi tổng hợp giọng đọc đầy đủ; bản mẫu 3 cảnh đầu có mốc thật ở `docs/loi-thoai.md`.
> Chỉ dẫn diễn xuất nằm trong comment của `src/data/script.mjs`, không đọc. Số liệu minh họa nhất quán từ `catalog.mjs`.

## Vì sao website biết bạn thích gì?  
`intro` · Mở đầu/Kết

- **intro-1**: Chào mừng các bạn đến với An Tech Academy – nơi công nghệ được giải thích bằng những ví dụ trực quan và dễ hiểu.
- **intro-2**: Lướt vài chiếc Samsung, web liền gợi ý máy cấu hình cao. Sao nó biết bạn thích gì?
- **intro-3**: Hôm nay, cùng bóc tách hệ thống gợi ý sản phẩm và các thuật toán đứng sau.

## Lộ trình bài học  
`goals` · Mở đầu/Kết

- **goals-1**: Năm chặng: cá nhân hóa, lọc phổ biến, lọc cộng tác với KNN và SVD, lọc nội dung với TF-IDF, rồi hybrid kết hợp.
- **goals-2**: Một website bán điện thoại, ba người dùng A, B, C xuyên suốt. Cuối bài có ba câu hỏi nhanh.

## Cá nhân hóa người dùng  
`div1` · Phần 1

- **div1-1**: Phần một: Cá nhân hóa người dùng.

## Từ hành vi đến hồ sơ sở thích  
`personalization` · Phần 1

- **pers-1**: Cá nhân hóa là điều chỉnh nội dung cho từng người, nhờ Hệ thống gợi ý — Recommender System.
- **pers-2**: Mỗi lượt xem, tìm kiếm, đánh giá, mua hàng được ghi lại thành hồ sơ sở thích — User Profile.
- **pers-3**: Dữ liệu đi vào, hệ thống học sở thích, trả ra danh sách gợi ý đúng gu của bạn.

## Ma trận Người dùng – Sản phẩm  
`matrix` · Phần 1

- **mat-1**: Dữ liệu xếp thành ma trận Người dùng – Sản phẩm: hàng là người, cột là máy, ô là điểm đánh giá.
- **mat-2**: Ô trống là chưa tương tác, không phải điểm không. Ma trận này rất thưa.
- **mat-3**: Hệ thống dự đoán ô trống, rồi chọn sản phẩm điểm cao nhất để gợi ý.

## Lọc độ phổ biến  
`div2` · Phần 2

- **div2-1**: Phần hai: Lọc độ phổ biến.

## Xếp hạng theo mức độ phổ biến  
`popularity` · Phần 2

- **pop-1**: Cách đơn giản nhất: xếp hạng theo độ phổ biến — lượt xem, lượt mua, điểm đánh giá, tần suất tương tác.
- **pop-2**: Galaxy S24 một nghìn lượt mua, iPhone 15 bảy trăm năm mươi, Xiaomi 14 năm trăm. Nhiều lượt mua hơn, xếp trên.
- **pop-3**: Galaxy S24 dẫn đầu, được chọn để gợi ý. Nhanh, dễ làm, không cần dữ liệu cá nhân.

## Ưu điểm và hạn chế  
`poplimit` · Phần 2

- **popl-1**: Ưu điểm: luôn có kết quả, kể cả người mới như C. Nhưng ai cũng nhận một danh sách giống nhau.
- **popl-2**: Người thích iPhone vẫn bị gợi ý Samsung bán chạy. Đó là số đông, không phải cá nhân hóa. Ta cần lọc cộng tác.

## Lọc cộng tác  
`div3` · Phần 3

- **div3-1**: Phần ba: Lọc cộng tác — Collaborative Filtering.

## Học từ những người giống bạn  
`cfintro` · Phần 3

- **cf-1**: Ý tưởng đẹp: người có gu giống nhau sẽ thích món giống nhau. Chỉ cần biết ai thích gì, không cần hiểu sản phẩm.
- **cf-2**: Hai hướng: User-Based tìm người giống bạn; Item-Based tìm sản phẩm giống món bạn đã thích.
- **cf-3**: Cả hai cần thước đo độ tương đồng. Và đây là lúc KNN bước vào.

## KNN — K láng giềng gần nhất  
`knn` · Phần 3

- **knn-1**: KNN tìm K người dùng giống bạn nhất, đo bằng Cosine Similarity hoặc Pearson trên các ô cùng đánh giá.
- **knn-2**: A và D cùng chấm Galaxy S24 năm điểm, Galaxy A55 bốn điểm. Vector gần trùng nhau, độ tương đồng rất cao.
- **knn-3**: D chấm Xiaomi 14 năm điểm, A chưa. Vì D giống A, hệ thống dự đoán A thích Xiaomi 14 và đưa vào gợi ý.
- **knn-4**: Đo tương đồng khác với dự đoán điểm. Từ láng giềng, lấy trung bình có trọng số theo độ giống để suy ô thiếu.
- **knn-5**: Item-Based đổi trục: tìm sản phẩm được cùng nhóm người đánh giá giống nhau, thay vì tìm người giống nhau.

## SVD — Phân rã ma trận  
`svd` · Phần 3

- **svd-1**: SVD nén cả ma trận thành vài yếu tố tiềm ẩn — Latent Factors — như gu hệ điều hành, mức cấu hình, camera.
- **svd-2**: Công thức: A = UΣVᵀ. U là đặc trưng người dùng, V là đặc trưng sản phẩm, Σ là trọng số yếu tố tiềm ẩn.
- **svd-3**: Giữ vài yếu tố quan trọng, tái tạo ma trận xấp xỉ. Ô trống giờ có giá trị dự đoán — như A với Xiaomi 14.
- **svd-4**: Chọn ô điểm cao để gợi ý. Nhưng đây là minh họa: SVD nguyên bản cần ma trận đầy đủ.
- **svd-5**: Thực tế dùng Matrix Factorization như FunkSVD: chỉ học ô đã biết, không lấp số không vào ô trống.

## Dữ liệu thưa & khởi đầu lạnh  
`cflimits` · Phần 3

- **cfl-1**: KNN và SVD gặp hai bài toán khó: dữ liệu thưa và khởi đầu lạnh.
- **cfl-2**: Thưa: quá ít ô được đánh giá, khó tìm láng giềng tin cậy. Lạnh: người mới như C chưa có gì, lọc cộng tác bó tay.
- **cfl-3**: KNN dễ giải thích nhưng nặng khi dữ liệu lớn. SVD dự đoán tốt hơn trên dữ liệu thưa, nhưng khó diễn giải.

## Lọc nội dung  
`div4` · Phần 4

- **div4-1**: Phần bốn: Lọc nội dung — Content-Based Filtering.

## TF-IDF — Biến mô tả thành vector  
`tfidf` · Phần 4

- **tf-1**: Lọc nội dung nhìn vào chính sản phẩm. Biến mô tả thành vector đặc trưng bằng TF-IDF.
- **tf-2**: TF đo từ xuất hiện nhiều trong mô tả. IDF giảm trọng số từ xuất hiện ở khắp nơi.
- **tf-3**: Kết quả: từ khóa đặc trưng như RAM 12GB, pin 5000 nổi lên; từ chung chung chìm xuống. Mỗi sản phẩm thành một vector.

## Cosine Similarity — Đo góc giữa hai vector  
`cosine` · Phần 4

- **cos-1**: So sánh bằng Cosine Similarity: đo góc giữa vector sở thích và vector sản phẩm. Góc càng nhỏ, càng giống.
- **cos-2**: A thích RAM 12GB, ROM 256GB, pin 5000mAh. Hệ thống tìm máy có thuộc tính gần nhất — như Xiaomi 14 — rồi gợi ý.
- **cos-3**: Với dữ liệu số và danh mục, dùng thêm Feature-Based Similarity. Không cần người khác, hợp người mới có vài lượt xem.
- **cos-4**: Hạn chế: gợi ý cứ na ná món đã xem, khó bất ngờ. Thích Samsung dễ bị nhốt trong thế giới Samsung.

## Phương pháp kết hợp  
`div5` · Phần 5

- **div5-1**: Phần năm: Hybrid — kết hợp để mạnh hơn.

## Weighted Hybrid — Trộn điểm theo trọng số  
`weighted` · Phần 5

- **w-1**: Mỗi phương pháp mạnh một kiểu. Hybrid kết hợp chúng. Cách một: Weighted — trộn điểm theo trọng số.
- **w-2**: Score = 0.5·S_CF + 0.3·S_CB + 0.2·S_POP. Ba nguồn điểm đi vào một bộ kết hợp.
- **w-3**: Xiaomi 14 cho A: 0.5×0.9 + 0.3×0.8 + 0.2×0.5 = 0.79. Đó là điểm xếp hạng cuối.
- **w-4**: Bắt buộc chuẩn hóa điểm về cùng thang đo trước khi trộn. Nếu không, trọng số mất ý nghĩa.

## Switching Hybrid — Đổi phương pháp theo dữ liệu  
`switching` · Phần 5

- **sw-1**: Cách hai: Switching — chọn phương pháp tùy lượng dữ liệu. Không trộn, mà chuyển.
- **sw-2**: Người mới như C: ưu tiên phổ biến. Có lịch sử xem: dùng nội dung. Đủ tương tác: chuyển sang SVD hoặc KNN.
- **sw-3**: Nhờ vậy, hệ thống luôn có phương án phù hợp ở mỗi giai đoạn của người dùng.

## Cascade Hybrid — Lọc theo tầng  
`cascade` · Phần 5

- **ca-1**: Cách ba: Cascade — xếp phương pháp thành tầng, tầng trước tinh chỉnh cho tầng sau.
- **ca-2**: Bước một: lọc ứng viên. Bước hai: SVD dự đoán. Bước ba: nội dung đo tương đồng. Bước bốn: xếp hạng, chọn năm sản phẩm.
- **ca-3**: Ba bản chất: Weighted trộn điểm, Switching chọn một, Cascade lọc nối tiếp. Đừng nhầm là một.
- **ca-4**: Hệ thống thực tế thường kết hợp cả ba: chuyển theo dữ liệu, lọc tầng, rồi trộn điểm ra danh sách cuối.

## Năm điều mang về  
`recap` · Phần 6

- **rec-1**: Cá nhân hóa biến hành vi thành hồ sơ. Phổ biến nhanh nhưng đại trà. Cộng tác học từ người giống bạn. Nội dung học từ sản phẩm.
- **rec-2**: Hybrid kết hợp tất cả: chính xác và linh hoạt. Hiểu bản chất thuật toán, bạn sẽ chọn đúng cách kết hợp.

## Kiểm tra nhanh  
`quiz` · Phần 6

- **q1**: Câu một: ô trống trong ma trận nghĩa là gì? Ba giây. _(giữ 3s đếm ngược)_
- **q1a**: Đáp án: chưa tương tác, không phải điểm không. Lấp số không sẽ làm sai dự đoán.
- **q2**: Câu hai: người mới chưa có lịch sử, ưu tiên phương pháp nào? Ba giây. _(giữ 3s đếm ngược)_
- **q2a**: Đáp án: lọc phổ biến — cách Switching Hybrid xử lý khởi đầu lạnh.
- **q3**: Câu ba: chiến lược nào trộn điểm theo trọng số? Ba giây. _(giữ 3s đếm ngược)_
- **q3a**: Đáp án: Weighted Hybrid. Nhớ chuẩn hóa điểm trước khi trộn.

## Từ dữ liệu đến gợi ý thông minh  
`outro` · Phần 6

- **out-1**: Từ dữ liệu đến thuật toán, từ thuật toán đến những gợi ý thông minh. Cảm ơn các bạn đã theo dõi An Tech Academy!
