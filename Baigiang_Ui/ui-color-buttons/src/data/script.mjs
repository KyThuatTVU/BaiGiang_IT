// Kịch bản: "Thiết kế màu sắc và chuẩn hóa hệ thống nút bấm trong giao diện website"
// Cue là đơn vị đồng bộ giữa giọng đọc, hình ảnh và phụ đề.

export const scenes = [
  {
    id: 'intro',
    type: 'intro',
    part: null,
    title: 'Màu sắc & hệ thống nút bấm',
    cues: [
      { id: 'intro-1', say: 'Cùng là website, có trang nhìn rất chuyên nghiệp, nhưng cũng có trang khiến người dùng rối mắt ngay từ giây đầu tiên. Vì sao?', sfx: 'error' },
      { id: 'intro-2', say: 'Khác biệt không nằm ở logo hay ảnh đẹp. Nó nằm ở hai thứ nền tảng: một bảng màu có nguyên tắc, và một hệ thống nút bấm nhất quán.', sfx: 'whoosh' },
      { id: 'intro-3', say: 'Năm phút tới, chúng ta sẽ mổ xẻ đúng hai thứ đó, trên cùng một website bán hàng.', sfx: 'chime' }
    ]
  },
  {
    id: 'goals',
    type: 'goals',
    part: null,
    title: 'Bạn sẽ học được gì',
    cues: [
      { id: 'goals-1', say: 'Bạn sẽ nắm quy tắc 60–30–10, biết chọn màu theo mục đích, và chuẩn hóa nút bấm từ kích thước đến từng trạng thái.', sfx: 'pop' },
      { id: 'goals-2', say: 'Đi kèm là một ví dụ xuyên suốt: Shop Xanh, một website bán hàng công nghệ.', sfx: 'chime' }
    ]
  },
  {
    id: 'div1',
    type: 'divider',
    part: 1,
    title: 'Màu sắc',
    cues: [
      { id: 'div1-1', say: 'Phần một. Màu sắc và nguyên tắc phối màu.', sfx: 'riser' }
    ]
  },
  {
    id: 'why',
    type: 'why',
    part: 1,
    title: 'Màu sắc làm ba việc',
    cues: [
      { id: 'why-1', say: 'Màu sắc làm ba việc cùng lúc. Một: tạo phân cấp. Màu đậm và màu nhạt cho mắt biết đâu là tiêu đề, đâu là nội dung, đâu là hành động.', sfx: 'marker' },
      { id: 'why-2', say: 'Hai: màu là thương hiệu. Chỉ cần nhìn bảng màu và kiểu chữ, người dùng đã nhận ra bạn là ai.', sfx: 'chime' },
      { id: 'why-3', say: 'Ba: màu hướng sự chú ý. Một nút cam giữa nền trắng sẽ được nhìn thấy trước mọi thứ khác.', sfx: 'pop' }
    ]
  },
  {
    id: 'rule',
    type: 'rule',
    part: 1,
    title: 'Quy tắc 60–30–10',
    cues: [
      { id: 'rule-1', say: 'Đây là quy tắc 60–30–10. Nó không phải công thức bắt buộc, mà là tỷ lệ định hướng cho cảm nhận thị giác.', sfx: 'marker' },
      { id: 'rule-2', say: 'Sáu mươi phần trăm là màu chủ đạo: nền lớn và các vùng chính. Với Shop Xanh, đó là trắng và xanh rất nhạt.', sfx: 'pop' },
      { id: 'rule-3', say: 'Ba mươi phần trăm là màu phụ: chia khu vực, tạo chiều sâu. Ở đây là xanh dương của thanh điều hướng và các khối nội dung.', sfx: 'pop' },
      { id: 'rule-4', say: 'Mười phần trăm còn lại là màu nhấn: nút mua hàng, khuyến mãi, thông tin quan trọng. Ít thôi, nhưng phải nổi.', sfx: 'success' },
      { id: 'rule-5', say: 'Đừng đếm từng pixel. Hãy nhìn tổng thể: nền chiếm phần lớn, màu phụ vừa phải, màu nhấn thật tiết chế.', sfx: 'whoosh' }
    ]
  },
  {
    id: 'wheel',
    type: 'wheel',
    part: 1,
    title: 'Xây bảng màu',
    cues: [
      { id: 'wheel-1', say: 'Vậy lấy màu từ đâu? Từ bánh xe màu. Phối đơn sắc dùng các sắc độ của một màu. Phối tương đồng dùng những màu nằm cạnh nhau.', sfx: 'marker' },
      { id: 'wheel-2', say: 'Phối bổ sung lấy hai màu đối diện, tạo tương phản mạnh. Chọn cách nào là tùy mục đích của website.', sfx: 'chime' },
      { id: 'wheel-3', say: 'Giáo dục: xanh dương, trắng, xanh lá. Thương mại điện tử: nền trung tính, một màu nhấn thật nổi. Công nghệ: xanh dương, cyan, tím.', sfx: 'pop' }
    ]
  },
  {
    id: 'div2',
    type: 'divider',
    part: 2,
    title: 'Hệ thống nút bấm',
    cues: [
      { id: 'div2-1', say: 'Phần hai. Chuẩn hóa hệ thống nút bấm.', sfx: 'riser' }
    ]
  },
  {
    id: 'anatomy',
    type: 'anatomy',
    part: 2,
    title: 'Giải phẫu một nút bấm',
    cues: [
      { id: 'anatomy-1', say: 'Một nút bấm không phải hình chữ nhật tô màu. Nó là một bộ thông số.', sfx: 'pop' },
      { id: 'anatomy-2', say: 'Chiều cao trên desktop từ bốn mươi đến bốn mươi tám pixel. Trên mobile, vùng chạm phải từ bốn mươi bốn pixel trở lên.', sfx: 'marker' },
      { id: 'anatomy-3', say: 'Bo góc chọn một hệ thống: sáu, tám hoặc mười hai pixel, và dùng nhất quán. Chữ dùng đúng font của website, cùng cỡ, cùng độ đậm.', sfx: 'click' },
      { id: 'anatomy-4', say: 'Khoảng đệm ngang và khoảng cách giữa các nút cũng theo bội số: tám, mười hai, mười sáu pixel.', sfx: 'marker' }
    ]
  },
  {
    id: 'types',
    type: 'types',
    part: 2,
    title: 'Bốn loại nút',
    cues: [
      { id: 'types-1', say: 'Bốn loại nút, bốn vai trò. Primary cho hành động chính. Secondary cho hành động phụ. Outline cho lựa chọn nhẹ. Danger cho việc nguy hiểm như xóa dữ liệu.', sfx: 'click' },
      { id: 'types-2', say: 'Quy tắc vàng: mỗi màn hình chỉ nên có một nút primary thật sự nổi bật.', sfx: 'success' }
    ]
  },
  {
    id: 'states',
    type: 'states',
    part: 2,
    title: 'Sáu trạng thái của nút',
    cues: [
      { id: 'states-1', say: 'Trạng thái mới là thứ tạo cảm giác chuyên nghiệp. Default là bình thường. Hover khi rê chuột: đổi màu nhẹ và nâng lên một chút.', sfx: 'hover' },
      { id: 'states-2', say: 'Active khi nhấn: tối hơn và lún xuống. Focus khi dùng bàn phím: phải có viền rõ ràng để biết mình đang ở đâu.', sfx: 'click' },
      { id: 'states-3', say: 'Disabled khi không thể thao tác: giảm tương phản nhưng vẫn đọc được. Loading khi đang xử lý: giữ nguyên kích thước, thay chữ bằng vòng xoay.', sfx: 'error' },
      { id: 'states-4', say: 'Mỗi trạng thái phải khác nhau đủ rõ, và phải nhất quán trên toàn bộ hệ thống.', sfx: 'pop' }
    ]
  },
  {
    id: 'mistakes',
    type: 'mistakes',
    part: 2,
    title: 'Ba lỗi thường gặp',
    cues: [
      { id: 'mistakes-1', say: 'Đây là ba lỗi thường gặp. Một: quá nhiều màu nhấn, mắt không biết nhìn đâu. Hai: mỗi nút một chiều cao, một bo góc. Ba: chữ và nền quá gần nhau, thiếu tương phản.', sfx: 'error' },
      { id: 'mistakes-2', say: 'Cả ba đều sửa được bằng cùng một cách: đưa tất cả về một hệ thống.', sfx: 'whoosh' }
    ]
  },
  {
    id: 'makeover',
    type: 'makeover',
    part: 2,
    title: 'Cải tiến giao diện',
    cues: [
      { id: 'makeover-1', say: 'Áp dụng 60–30–10, chọn một màu nhấn, và chuẩn hóa toàn bộ nút bấm.', sfx: 'whoosh' },
      { id: 'makeover-2', say: 'Kết quả: cùng nội dung, nhưng rõ ràng, dễ đọc và đáng tin hơn.', sfx: 'success' }
    ]
  },
  {
    id: 'recap',
    type: 'recap',
    part: 2,
    title: 'Ba điều mang về',
    cues: [
      { id: 'recap-1', say: 'Ba điều mang về. Phối màu có nguyên tắc. Dùng màu để phân cấp thông tin. Và biến nút bấm thành một hệ thống nhất quán.', sfx: 'pop' },
      { id: 'recap-2', say: 'Hãy bắt đầu từ bảng màu, rồi mới đi đến từng chi tiết.', sfx: 'chime' }
    ]
  },
  {
    id: 'quiz',
    type: 'quiz',
    part: null,
    title: 'Kiểm tra nhanh',
    cues: [
      { id: 'quiz-1', say: 'Câu một: quy tắc phối màu trong bài dùng tỷ lệ nào? Ba giây, mời bạn chọn.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-1a', say: 'Đáp án: 60–30–10. Nền 60, màu phụ 30, màu nhấn 10.', sfx: 'success' },
      { id: 'quiz-2', say: 'Câu hai: màu nhấn 10 phần trăm dùng để làm gì? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-2a', say: 'Đáp án: hướng mắt vào hành động chính, ví dụ nút mua hàng.', sfx: 'success' },
      { id: 'quiz-3', say: 'Câu ba: trạng thái nào xuất hiện khi rê chuột lên nút? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-3a', say: 'Đáp án: Hover. Nhấn là Active, dùng bàn phím là Focus.', sfx: 'success' }
    ]
  },
  {
    id: 'outro',
    type: 'outro',
    part: null,
    title: 'Nhất quán trong từng chi tiết',
    cues: [
      { id: 'outro-1', say: 'Một giao diện đẹp không chỉ nằm ở màu sắc bắt mắt, mà ở sự nhất quán trong từng chi tiết. Hãy bắt đầu từ bảng màu và hệ thống nút bấm, để website của bạn chuyên nghiệp hơn mỗi ngày.', sfx: 'chime' }
    ]
  }
];
