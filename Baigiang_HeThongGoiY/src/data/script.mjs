// ============================================================
// KỊCH BẢN — "Cá nhân hóa người dùng & các thuật toán trong hệ thống gợi ý sản phẩm"
// AN TECH ACADEMY · Recommender Systems
// Mỗi cue = một đơn vị đồng bộ giọng đọc / hình ảnh / phụ đề.
// `say` = lời thoại hiển thị + phụ đề; `tts` = bản tối ưu phát âm (nếu khác).
// Chỉ dẫn diễn xuất đặt trong comment, KHÔNG đọc. Số liệu nhất quán từ catalog.mjs.
// Văn phong súc tích, tự nhiên; câu ngắn; giảm tốc ở công thức (cue.rate).
// ============================================================

export const scenes = [
  // ===================== MỞ ĐẦU =====================
  {
    id: 'intro', type: 'intro', part: null,
    title: 'Vì sao website biết bạn thích gì?',
    cues: [
      // [Năng lượng, thân thiện] — câu chào thương hiệu giữ nguyên văn
      { id: 'intro-1', say: 'Chào mừng các bạn đến với An Tech Academy – nơi công nghệ được giải thích bằng những ví dụ trực quan và dễ hiểu.', sfx: 'chime' },
      // [Tò mò]
      { id: 'intro-2', say: 'Lướt vài chiếc Samsung, web liền gợi ý máy cấu hình cao. Sao nó biết bạn thích gì?', sfx: 'whoosh' },
      // [Dẫn vào]
      { id: 'intro-3', say: 'Hôm nay, cùng bóc tách hệ thống gợi ý sản phẩm và các thuật toán đứng sau.', sfx: 'chime' }
    ]
  },
  {
    id: 'goals', type: 'goals', part: null,
    title: 'Lộ trình bài học',
    cues: [
      { id: 'goals-1', say: 'Năm chặng: cá nhân hóa, lọc phổ biến, lọc cộng tác với KNN và SVD, lọc nội dung với TF-IDF, rồi hybrid kết hợp.', sfx: 'pop', tts: 'Năm chặng: cá nhân hóa, lọc phổ biến, lọc cộng tác với K N N và S V D, lọc nội dung với T F I D F, rồi hybrid kết hợp.' },
      { id: 'goals-2', say: 'Một website bán điện thoại, ba người dùng A, B, C xuyên suốt. Cuối bài có ba câu hỏi nhanh.', sfx: 'chime' }
    ]
  },

  // ===================== PHẦN 1 =====================
  {
    id: 'div1', type: 'divider', part: 1, title: 'Cá nhân hóa người dùng',
    cues: [ { id: 'div1-1', say: 'Phần một: Cá nhân hóa người dùng.', sfx: 'riser' } ]
  },
  {
    id: 'personalization', type: 'personalization', part: 1,
    title: 'Từ hành vi đến hồ sơ sở thích',
    cues: [
      // [Giải thích bình tĩnh]
      { id: 'pers-1', say: 'Cá nhân hóa là điều chỉnh nội dung cho từng người, nhờ Hệ thống gợi ý — Recommender System.', sfx: 'marker' },
      // [Kể chuyện]
      { id: 'pers-2', say: 'Mỗi lượt xem, tìm kiếm, đánh giá, mua hàng được ghi lại thành hồ sơ sở thích — User Profile.', sfx: 'data' },
      // [Nhấn quy trình]
      { id: 'pers-3', say: 'Dữ liệu đi vào, hệ thống học sở thích, trả ra danh sách gợi ý đúng gu của bạn.', sfx: 'success' }
    ]
  },
  {
    id: 'matrix', type: 'matrix', part: 1,
    title: 'Ma trận Người dùng – Sản phẩm',
    cues: [
      // [Chậm, rõ — khái niệm nền]
      { id: 'mat-1', say: 'Dữ liệu xếp thành ma trận Người dùng – Sản phẩm: hàng là người, cột là máy, ô là điểm đánh giá.', sfx: 'marker', rate: '+12%' },
      { id: 'mat-2', say: 'Ô trống là chưa tương tác, không phải điểm không. Ma trận này rất thưa.', sfx: 'click' },
      { id: 'mat-3', say: 'Hệ thống dự đoán ô trống, rồi chọn sản phẩm điểm cao nhất để gợi ý.', sfx: 'pop' }
    ]
  },

  // ===================== PHẦN 2 =====================
  {
    id: 'div2', type: 'divider', part: 2, title: 'Lọc độ phổ biến',
    cues: [ { id: 'div2-1', say: 'Phần hai: Lọc độ phổ biến.', sfx: 'riser' } ]
  },
  {
    id: 'popularity', type: 'popularity', part: 2,
    title: 'Xếp hạng theo mức độ phổ biến',
    cues: [
      { id: 'pop-1', say: 'Cách đơn giản nhất: xếp hạng theo độ phổ biến — lượt xem, lượt mua, điểm đánh giá, tần suất tương tác.', sfx: 'marker' },
      { id: 'pop-2', say: 'Galaxy S24 một nghìn lượt mua, iPhone 15 bảy trăm năm mươi, Xiaomi 14 năm trăm. Nhiều lượt mua hơn, xếp trên.', sfx: 'data', tts: 'Galaxy S hai bốn một nghìn lượt mua, iPhone mười lăm bảy trăm năm mươi, Xiaomi mười bốn năm trăm. Nhiều lượt mua hơn, xếp trên.' },
      { id: 'pop-3', say: 'Galaxy S24 dẫn đầu, được chọn để gợi ý. Nhanh, dễ làm, không cần dữ liệu cá nhân.', sfx: 'success', tts: 'Galaxy S hai bốn dẫn đầu, được chọn để gợi ý. Nhanh, dễ làm, không cần dữ liệu cá nhân.' }
    ]
  },
  {
    id: 'poplimit', type: 'poplimit', part: 2,
    title: 'Ưu điểm và hạn chế',
    cues: [
      { id: 'popl-1', say: 'Ưu điểm: luôn có kết quả, kể cả người mới như C. Nhưng ai cũng nhận một danh sách giống nhau.', sfx: 'click' },
      { id: 'popl-2', say: 'Người thích iPhone vẫn bị gợi ý Samsung bán chạy. Đó là số đông, không phải cá nhân hóa. Ta cần lọc cộng tác.', sfx: 'error' }
    ]
  },

  // ===================== PHẦN 3 =====================
  {
    id: 'div3', type: 'divider', part: 3, title: 'Lọc cộng tác',
    cues: [ { id: 'div3-1', say: 'Phần ba: Lọc cộng tác — Collaborative Filtering.', sfx: 'riser' } ]
  },
  {
    id: 'cfintro', type: 'cfintro', part: 3,
    title: 'Học từ những người giống bạn',
    cues: [
      { id: 'cf-1', say: 'Ý tưởng đẹp: người có gu giống nhau sẽ thích món giống nhau. Chỉ cần biết ai thích gì, không cần hiểu sản phẩm.', sfx: 'marker' },
      { id: 'cf-2', say: 'Hai hướng: User-Based tìm người giống bạn; Item-Based tìm sản phẩm giống món bạn đã thích.', sfx: 'click' },
      { id: 'cf-3', say: 'Cả hai cần thước đo độ tương đồng. Và đây là lúc KNN bước vào.', sfx: 'pop', tts: 'Cả hai cần thước đo độ tương đồng. Và đây là lúc K N N bước vào.' }
    ]
  },
  {
    id: 'knn', type: 'knn', part: 3,
    title: 'KNN — K láng giềng gần nhất',
    cues: [
      { id: 'knn-1', say: 'KNN tìm K người dùng giống bạn nhất, đo bằng Cosine Similarity hoặc Pearson trên các ô cùng đánh giá.', sfx: 'marker', tts: 'K N N tìm K người dùng giống bạn nhất, đo bằng Cosine Similarity hoặc Pearson trên các ô cùng đánh giá.' },
      { id: 'knn-2', say: 'A và D cùng chấm Galaxy S24 năm điểm, Galaxy A55 bốn điểm. Vector gần trùng nhau, độ tương đồng rất cao.', sfx: 'data', tts: 'A và D cùng chấm Galaxy S hai bốn năm điểm, Galaxy A năm năm bốn điểm. Vector gần trùng nhau, độ tương đồng rất cao.' },
      { id: 'knn-3', say: 'D chấm Xiaomi 14 năm điểm, A chưa. Vì D giống A, hệ thống dự đoán A thích Xiaomi 14 và đưa vào gợi ý.', sfx: 'success', tts: 'D chấm Xiaomi mười bốn năm điểm, A chưa. Vì D giống A, hệ thống dự đoán A thích Xiaomi mười bốn và đưa vào gợi ý.' },
      { id: 'knn-4', say: 'Đo tương đồng khác với dự đoán điểm. Từ láng giềng, lấy trung bình có trọng số theo độ giống để suy ô thiếu.', sfx: 'click' },
      { id: 'knn-5', say: 'Item-Based đổi trục: tìm sản phẩm được cùng nhóm người đánh giá giống nhau, thay vì tìm người giống nhau.', sfx: 'pop' }
    ]
  },
  {
    id: 'svd', type: 'svd', part: 3,
    title: 'SVD — Phân rã ma trận',
    cues: [
      { id: 'svd-1', say: 'SVD nén cả ma trận thành vài yếu tố tiềm ẩn — Latent Factors — như gu hệ điều hành, mức cấu hình, camera.', sfx: 'marker', tts: 'S V D nén cả ma trận thành vài yếu tố tiềm ẩn — Latent Factors — như gu hệ điều hành, mức cấu hình, camera.' },
      // [Chậm — công thức]
      { id: 'svd-2', say: 'Công thức: A = UΣVᵀ. U là đặc trưng người dùng, V là đặc trưng sản phẩm, Σ là trọng số yếu tố tiềm ẩn.', sfx: 'data', rate: '+6%', tts: 'Công thức: A bằng U nhân Xích-ma nhân V chuyển vị. U là đặc trưng người dùng, V là đặc trưng sản phẩm, Xích-ma là trọng số yếu tố tiềm ẩn.' },
      { id: 'svd-3', say: 'Giữ vài yếu tố quan trọng, tái tạo ma trận xấp xỉ. Ô trống giờ có giá trị dự đoán — như A với Xiaomi 14.', sfx: 'sparkle', tts: 'Giữ vài yếu tố quan trọng, tái tạo ma trận xấp xỉ. Ô trống giờ có giá trị dự đoán — như A với Xiaomi mười bốn.' },
      { id: 'svd-4', say: 'Chọn ô điểm cao để gợi ý. Nhưng đây là minh họa: SVD nguyên bản cần ma trận đầy đủ.', sfx: 'click' },
      { id: 'svd-5', say: 'Thực tế dùng Matrix Factorization như FunkSVD: chỉ học ô đã biết, không lấp số không vào ô trống.', sfx: 'marker', tts: 'Thực tế dùng Matrix Factorization như Funk S V D: chỉ học ô đã biết, không lấp số không vào ô trống.' }
    ]
  },
  {
    id: 'cflimits', type: 'cflimits', part: 3,
    title: 'Dữ liệu thưa & khởi đầu lạnh',
    cues: [
      { id: 'cfl-1', say: 'KNN và SVD gặp hai bài toán khó: dữ liệu thưa và khởi đầu lạnh.', sfx: 'error', tts: 'K N N và S V D gặp hai bài toán khó: dữ liệu thưa và khởi đầu lạnh.' },
      { id: 'cfl-2', say: 'Thưa: quá ít ô được đánh giá, khó tìm láng giềng tin cậy. Lạnh: người mới như C chưa có gì, lọc cộng tác bó tay.', sfx: 'click' },
      { id: 'cfl-3', say: 'KNN dễ giải thích nhưng nặng khi dữ liệu lớn. SVD dự đoán tốt hơn trên dữ liệu thưa, nhưng khó diễn giải.', sfx: 'pop' }
    ]
  },

  // ===================== PHẦN 4 =====================
  {
    id: 'div4', type: 'divider', part: 4, title: 'Lọc nội dung',
    cues: [ { id: 'div4-1', say: 'Phần bốn: Lọc nội dung — Content-Based Filtering.', sfx: 'riser' } ]
  },
  {
    id: 'tfidf', type: 'tfidf', part: 4,
    title: 'TF-IDF — Biến mô tả thành vector',
    cues: [
      { id: 'tf-1', say: 'Lọc nội dung nhìn vào chính sản phẩm. Biến mô tả thành vector đặc trưng bằng TF-IDF.', sfx: 'marker', tts: 'Lọc nội dung nhìn vào chính sản phẩm. Biến mô tả thành vector đặc trưng bằng T F I D F.' },
      { id: 'tf-2', say: 'TF đo từ xuất hiện nhiều trong mô tả. IDF giảm trọng số từ xuất hiện ở khắp nơi.', sfx: 'data', tts: 'T F đo từ xuất hiện nhiều trong mô tả. I D F giảm trọng số từ xuất hiện ở khắp nơi.' },
      { id: 'tf-3', say: 'Kết quả: từ khóa đặc trưng như RAM 12GB, pin 5000 nổi lên; từ chung chung chìm xuống. Mỗi sản phẩm thành một vector.', sfx: 'sparkle', tts: 'Kết quả: từ khóa đặc trưng như RAM mười hai ghi-ga, pin năm nghìn nổi lên; từ chung chung chìm xuống. Mỗi sản phẩm thành một vector.' }
    ]
  },
  {
    id: 'cosine', type: 'cosine', part: 4,
    title: 'Cosine Similarity — Đo góc giữa hai vector',
    cues: [
      { id: 'cos-1', say: 'So sánh bằng Cosine Similarity: đo góc giữa vector sở thích và vector sản phẩm. Góc càng nhỏ, càng giống.', sfx: 'marker' },
      { id: 'cos-2', say: 'A thích RAM 12GB, ROM 256GB, pin 5000mAh. Hệ thống tìm máy có thuộc tính gần nhất — như Xiaomi 14 — rồi gợi ý.', sfx: 'data', tts: 'A thích RAM mười hai ghi-ga, ROM hai trăm năm sáu ghi-ga, pin năm nghìn mi-li-am-pe giờ. Hệ thống tìm máy có thuộc tính gần nhất — như Xiaomi mười bốn — rồi gợi ý.' },
      { id: 'cos-3', say: 'Với dữ liệu số và danh mục, dùng thêm Feature-Based Similarity. Không cần người khác, hợp người mới có vài lượt xem.', sfx: 'click' },
      { id: 'cos-4', say: 'Hạn chế: gợi ý cứ na ná món đã xem, khó bất ngờ. Thích Samsung dễ bị nhốt trong thế giới Samsung.', sfx: 'error' }
    ]
  },

  // ===================== PHẦN 5 =====================
  {
    id: 'div5', type: 'divider', part: 5, title: 'Phương pháp kết hợp',
    cues: [ { id: 'div5-1', say: 'Phần năm: Hybrid — kết hợp để mạnh hơn.', sfx: 'riser' } ]
  },
  {
    id: 'weighted', type: 'weighted', part: 5,
    title: 'Weighted Hybrid — Trộn điểm theo trọng số',
    cues: [
      { id: 'w-1', say: 'Mỗi phương pháp mạnh một kiểu. Hybrid kết hợp chúng. Cách một: Weighted — trộn điểm theo trọng số.', sfx: 'marker' },
      { id: 'w-2', say: 'Score = 0.5·S_CF + 0.3·S_CB + 0.2·S_POP. Ba nguồn điểm đi vào một bộ kết hợp.', sfx: 'data', rate: '+8%', tts: 'Score bằng không phẩy năm nhân điểm cộng tác, cộng không phẩy ba nhân điểm nội dung, cộng không phẩy hai nhân điểm phổ biến. Ba nguồn điểm đi vào một bộ kết hợp.' },
      { id: 'w-3', say: 'Xiaomi 14 cho A: 0.5×0.9 + 0.3×0.8 + 0.2×0.5 = 0.79. Đó là điểm xếp hạng cuối.', sfx: 'success', tts: 'Xiaomi mười bốn cho A: không phẩy năm nhân không phẩy chín, cộng không phẩy ba nhân không phẩy tám, cộng không phẩy hai nhân không phẩy năm, bằng không phẩy bảy chín. Đó là điểm xếp hạng cuối.' },
      { id: 'w-4', say: 'Bắt buộc chuẩn hóa điểm về cùng thang đo trước khi trộn. Nếu không, trọng số mất ý nghĩa.', sfx: 'click' }
    ]
  },
  {
    id: 'switching', type: 'switching', part: 5,
    title: 'Switching Hybrid — Đổi phương pháp theo dữ liệu',
    cues: [
      { id: 'sw-1', say: 'Cách hai: Switching — chọn phương pháp tùy lượng dữ liệu. Không trộn, mà chuyển.', sfx: 'marker' },
      { id: 'sw-2', say: 'Người mới như C: ưu tiên phổ biến. Có lịch sử xem: dùng nội dung. Đủ tương tác: chuyển sang SVD hoặc KNN.', sfx: 'data', tts: 'Người mới như C: ưu tiên phổ biến. Có lịch sử xem: dùng nội dung. Đủ tương tác: chuyển sang S V D hoặc K N N.' },
      { id: 'sw-3', say: 'Nhờ vậy, hệ thống luôn có phương án phù hợp ở mỗi giai đoạn của người dùng.', sfx: 'success' }
    ]
  },
  {
    id: 'cascade', type: 'cascade', part: 5,
    title: 'Cascade Hybrid — Lọc theo tầng',
    cues: [
      { id: 'ca-1', say: 'Cách ba: Cascade — xếp phương pháp thành tầng, tầng trước tinh chỉnh cho tầng sau.', sfx: 'marker' },
      { id: 'ca-2', say: 'Bước một: lọc ứng viên. Bước hai: SVD dự đoán. Bước ba: nội dung đo tương đồng. Bước bốn: xếp hạng, chọn năm sản phẩm.', sfx: 'data', tts: 'Bước một: lọc ứng viên. Bước hai: S V D dự đoán. Bước ba: nội dung đo tương đồng. Bước bốn: xếp hạng, chọn năm sản phẩm.' },
      { id: 'ca-3', say: 'Ba bản chất: Weighted trộn điểm, Switching chọn một, Cascade lọc nối tiếp. Đừng nhầm là một.', sfx: 'click' },
      { id: 'ca-4', say: 'Hệ thống thực tế thường kết hợp cả ba: chuyển theo dữ liệu, lọc tầng, rồi trộn điểm ra danh sách cuối.', sfx: 'success' }
    ]
  },

  // ===================== KẾT =====================
  {
    id: 'recap', type: 'recap', part: 6,
    title: 'Năm điều mang về',
    cues: [
      { id: 'rec-1', say: 'Cá nhân hóa biến hành vi thành hồ sơ. Phổ biến nhanh nhưng đại trà. Cộng tác học từ người giống bạn. Nội dung học từ sản phẩm.', sfx: 'pop' },
      { id: 'rec-2', say: 'Hybrid kết hợp tất cả: chính xác và linh hoạt. Hiểu bản chất thuật toán, bạn sẽ chọn đúng cách kết hợp.', sfx: 'chime' }
    ]
  },
  {
    id: 'quiz', type: 'quiz', part: 6,
    title: 'Kiểm tra nhanh',
    cues: [
      { id: 'q1', say: 'Câu một: ô trống trong ma trận nghĩa là gì? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'q1a', say: 'Đáp án: chưa tương tác, không phải điểm không. Lấp số không sẽ làm sai dự đoán.', sfx: 'success' },
      { id: 'q2', say: 'Câu hai: người mới chưa có lịch sử, ưu tiên phương pháp nào? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'q2a', say: 'Đáp án: lọc phổ biến — cách Switching Hybrid xử lý khởi đầu lạnh.', sfx: 'success' },
      { id: 'q3', say: 'Câu ba: chiến lược nào trộn điểm theo trọng số? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'q3a', say: 'Đáp án: Weighted Hybrid. Nhớ chuẩn hóa điểm trước khi trộn.', sfx: 'success' }
    ]
  },
  {
    id: 'outro', type: 'outro', part: 6,
    title: 'Từ dữ liệu đến gợi ý thông minh',
    cues: [
      { id: 'out-1', say: 'Từ dữ liệu đến thuật toán, từ thuật toán đến những gợi ý thông minh. Cảm ơn các bạn đã theo dõi An Tech Academy!', sfx: 'chime' }
    ]
  }
];

export const totalCues = scenes.reduce((a, s) => a + s.cues.length, 0);