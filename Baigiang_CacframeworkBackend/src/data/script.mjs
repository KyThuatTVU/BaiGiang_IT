// Kịch bản: "Khám phá các ngôn ngữ lập trình và framework phổ biến trong Backend"
// Mỗi cue là một đơn vị đồng bộ giữa giọng đọc, hình ảnh và phụ đề.

export const scenes = [
  {
    id: 'intro',
    type: 'intro',
    part: null,
    title: 'Backend — bộ não phía sau giao diện',
    cues: [
      { id: 'intro-1', say: 'Chào bạn! Tôi là An Tech Academy. Nghĩ đăng nhập chỉ là gõ email, mật khẩu rồi bấm nút? Ồ không — sau cú click là cả một hệ thống đang quay.', sfx: 'chime' },
      { id: 'intro-2', say: 'Một website bán hàng, một app ngân hàng hay app đặt xe, tất cả đều cần Backend — phần não nằm sau giao diện.', sfx: 'whoosh' },
      { id: 'intro-3', say: 'Hôm nay chúng ta mổ xẻ Backend, bảy ngôn ngữ phổ biến nhất và framework đi kèm, để bạn biết chúng chạy ở đâu và chọn cái nào cho đúng.', sfx: 'chime' }
    ]
  },
  {
    id: 'goals',
    type: 'goals',
    part: null,
    title: 'Bốn chặng trên lộ trình',
    cues: [
      { id: 'goals-1', say: 'Lộ trình bốn chặng: hiểu Backend là gì, phân biệt ngôn ngữ với framework, đi qua bảy hệ sinh thái, rồi so sánh và chọn công nghệ cho dự án thật.', sfx: 'pop' },
      { id: 'goals-2', say: 'Cuối bài có ba câu hỏi nhanh. Chuẩn bị tinh thần đi, vì phần sau hơi bánh cuốn đấy.', sfx: 'chime' }
    ]
  },
  {
    id: 'div1',
    type: 'divider',
    part: 1,
    title: 'Backend là gì?',
    cues: [
      { id: 'div1-1', say: 'Phần một: Backend là gì?', sfx: 'riser' }
    ]
  },
  {
    id: 'backend',
    type: 'backend',
    part: 1,
    title: 'Backend làm việc gì?',
    cues: [
      { id: 'backend-1', say: 'Thử tưởng tượng bạn mở trang bán hàng. Bạn đăng nhập, tìm sản phẩm, thêm vào giỏ, đặt hàng rồi thanh toán. Mọi thao tác đều mượt trên màn hình.', sfx: 'click' },
      { id: 'backend-2', say: 'Giao diện chỉ là phần nổi. Mỗi cú click tạo ra HTTP request gửi lên server. Backend tiếp nhận, xử lý nghiệp vụ, xác thực người dùng, truy vấn database rồi trả kết quả.', sfx: 'data' },
      { id: 'backend-3', say: 'Mô hình là: người dùng, frontend, API, backend, database. API là cửa ngõ, backend là bộ não, database là trí nhớ dài hạn.', sfx: 'marker' },
      { id: 'backend-4', say: 'Frontend lo những gì bạn thấy. Backend lo những gì phải quyết định, phải kiểm tra và phải ghi nhớ.', sfx: 'pop' },
      { id: 'backend-5', say: 'Điều thú vị: bạn không bao giờ nhìn thấy backend. Chỉ thấy nó nhanh, ổn định — hoặc thấy nó sập.', sfx: 'error' }
    ]
  },
  {
    id: 'flow',
    type: 'flow',
    part: 1,
    title: 'Một yêu cầu đi qua hệ thống',
    cues: [
      { id: 'flow-1', say: 'Theo dõi một lần đăng nhập. Người dùng nhập email, mật khẩu. Frontend không tự quyết định, nó đóng gói thành HTTP request gửi đến API.', sfx: 'data' },
      { id: 'flow-2', say: 'Backend nhận request, kiểm tra dữ liệu, tìm tài khoản trong database và so sánh mật khẩu đã băm. Nếu khớp, nó tạo access token.', sfx: 'marker' },
      { id: 'flow-3', say: 'Rồi trả response về frontend. Thành công thì chuyển trang; sai mật khẩu thì báo lỗi. Cả quá trình thường chưa đến một giây, và bạn không hề thấy.', sfx: 'success' }
    ]
  },
  {
    id: 'div2',
    type: 'divider',
    part: 2,
    title: 'Ngôn ngữ vs Framework',
    cues: [
      { id: 'div2-1', say: 'Phần hai: ngôn ngữ khác framework ở đâu?', sfx: 'riser' }
    ]
  },
  {
    id: 'langfw',
    type: 'langfw',
    part: 2,
    title: 'Phân biệt ngôn ngữ, runtime, framework',
    cues: [
      { id: 'langfw-1', say: 'Đây là chỗ nhiều bạn nhầm. Ngôn ngữ lập trình là công cụ viết mã và xây logic: JavaScript, Python, PHP, Java, C#, Go, Ruby. Nó là nguyên liệu và dụng cụ.', sfx: 'marker' },
      { id: 'langfw-2', say: 'Framework là bộ khung: cung cấp cấu trúc, thư viện và quy ước để dựng ứng dụng nhanh hơn, có tổ chức hơn. Nó giống giàn giáo và bản thiết kế thi công.', sfx: 'click' },
      { id: 'langfw-3', say: 'Điểm mấu chốt: framework luôn được xây trên một ngôn ngữ cụ thể. Express thuộc JavaScript, Laravel thuộc PHP, Spring Boot thuộc Java. Nó không phải ngôn ngữ độc lập.', sfx: 'pop' },
      { id: 'langfw-4', say: 'Node.js là môi trường thực thi JavaScript phía server, không phải framework. Xếp bốn thẻ: JavaScript là ngôn ngữ, Node.js là runtime, Express là framework, bcrypt là thư viện.', sfx: 'chime' }
    ]
  },
  {
    id: 'div3',
    type: 'divider',
    part: 3,
    title: 'Bảy hệ sinh thái',
    cues: [
      { id: 'div3-1', say: 'Phần ba: bảy hệ sinh thái Backend.', sfx: 'riser' }
    ]
  },
  {
    id: 'js',
    type: 'js',
    part: 3,
    title: 'JavaScript & TypeScript',
    cues: [
      { id: 'js-1', say: 'Bắt đầu với JavaScript và TypeScript — cặp đôi phổ biến nhất của web. Node.js đưa JavaScript ra khỏi trình duyệt để chạy trên server. Một ngôn ngữ dùng được cả hai phía.', sfx: 'pop' },
      { id: 'js-2', say: 'Có ba framework đáng chú ý. Express tối giản, linh hoạt, phổ biến để dựng REST API. NestJS cấu trúc rõ ràng, TypeScript mạnh, dependency injection, module hóa. Fastify tối ưu hiệu năng và tốc độ.', sfx: 'click' },
      { id: 'js-3', say: 'Điểm mạnh: chung ngôn ngữ với frontend, cộng đồng cực lớn, thư viện đủ mọi thứ. Hợp với thương mại điện tử, hệ thống quản lý, API mobile và ứng dụng thời gian thực.', sfx: 'chime' },
      { id: 'js-4', say: 'Nhớ nhé: Node.js không phải framework, mà là môi trường thực thi.', sfx: 'success' }
    ]
  },
  {
    id: 'python',
    type: 'python',
    part: 3,
    title: 'Python',
    cues: [
      { id: 'python-1', say: 'Python nổi tiếng vì dễ đọc, dễ học và mạnh trong xử lý dữ liệu. Ở Backend, ba cái tên tiêu biểu là Django, Flask và FastAPI.', sfx: 'pop' },
      { id: 'python-2', say: 'Django đầy đủ: ORM, trang quản trị, xác thực, bảo mật. Flask nhẹ, linh hoạt, bạn tự lắp từng mảnh. FastAPI hiện đại: type hints, tự sinh tài liệu API, hỗ trợ bất đồng bộ.', sfx: 'marker' },
      { id: 'python-3', say: 'Mạnh nhất ở hệ sinh thái AI và khoa học dữ liệu. Hợp với hệ thống quản lý, REST API, dịch vụ dữ liệu và ứng dụng AI cần backend.', sfx: 'chime' },
      { id: 'python-4', say: 'Chọn Django khi cần nhanh và đầy đủ; Flask khi muốn kiểm soát tối đa; FastAPI khi ưu tiên API hiện đại và hiệu năng.', sfx: 'success' }
    ]
  },
  {
    id: 'php',
    type: 'php',
    part: 3,
    title: 'PHP',
    cues: [
      { id: 'php-1', say: 'PHP vẫn là lực lượng đáng gờm, nhất là website doanh nghiệp và hệ thống nội dung. Laravel là ngôi sao lớn nhất: Eloquent, routing, middleware, xác thực, hàng đợi — gần như có sẵn.', sfx: 'pop' },
      { id: 'php-2', say: 'Symfony mạnh về mô-đun và các thành phần tái sử dụng, rất hợp hệ thống lớn. CodeIgniter nhẹ, đơn giản, dễ tiếp cận người mới.', sfx: 'marker' },
      { id: 'php-3', say: 'Chi phí triển khai thấp, hosting phổ biến, nhiều lập trình viên. Vẫn là lựa chọn thực dụng cho website doanh nghiệp, quản trị, thương mại điện tử và CMS.', sfx: 'chime' }
    ]
  },
  {
    id: 'java',
    type: 'java',
    part: 3,
    title: 'Java',
    cues: [
      { id: 'java-1', say: 'Java là trụ cột doanh nghiệp, nơi ổn định quan trọng hơn tốc độ viết code. Spring Boot phổ biến nhất: tự cấu hình, máy chủ nhúng, hệ sinh thái khổng lồ.', sfx: 'pop' },
      { id: 'java-2', say: 'Quarkus hướng tới cloud native, tối ưu cho container và biên dịch native. Micronaut tập trung khởi động nhanh và ít bộ nhớ. Cả hai đều nhắm đến microservices hiện đại.', sfx: 'marker' },
      { id: 'java-3', say: 'Vì thế Java thường nằm trong ngân hàng, hệ thống giao dịch, phần mềm doanh nghiệp và microservices quy mô lớn.', sfx: 'chime' }
    ]
  },
  {
    id: 'csharp',
    type: 'csharp',
    part: 3,
    title: 'C# & .NET',
    cues: [
      { id: 'csharp-1', say: 'C# và nền tảng .NET mạnh trong thế giới Microsoft, nhưng .NET hiện đại đã chạy đa nền tảng. ASP.NET Core dùng để xây web API và ứng dụng web hiệu năng cao.', sfx: 'pop' },
      { id: 'csharp-2', say: 'Entity Framework Core là ORM giúp làm việc với database bằng đối tượng thay vì SQL thủ công. Minimal APIs dựng HTTP API gọn nhẹ chỉ với vài dòng.', sfx: 'marker' },
      { id: 'csharp-3', say: 'C# phổ biến trong quản lý doanh nghiệp, quản lý nhân sự, web API và hệ thống nội bộ — nơi cần tích hợp sâu với hệ sinh thái Microsoft.', sfx: 'chime' }
    ]
  },
  {
    id: 'go',
    type: 'go',
    part: 3,
    title: 'Go (Golang)',
    cues: [
      { id: 'go-1', say: 'Go được thiết kế cho sự đơn giản và xử lý đồng thời. Goroutine chạy hàng nghìn tác vụ nhẹ cùng lúc, nên Go hợp với dịch vụ cần xử lý nhiều request.', sfx: 'pop' },
      { id: 'go-2', say: 'Trong hệ sinh thái Go, Gin nhẹ và phổ biến, Echo đầy đủ tính năng, Fiber có cú pháp gần Express. Bạn cũng có thể dùng thư viện chuẩn net/http.', sfx: 'data' },
      { id: 'go-3', say: 'Go thường xuất hiện trong microservices, dịch vụ hiệu năng cao và hệ thống chịu tải lớn.', sfx: 'chime' }
    ]
  },
  {
    id: 'ruby',
    type: 'ruby',
    part: 3,
    title: 'Ruby',
    cues: [
      { id: 'ruby-1', say: 'Ruby nổi bật với triết lý lập trình vui vẻ và tốc độ phát triển. Rails đưa quy ước hơn cấu hình thành thương hiệu: đặt tên đúng, Rails lo phần còn lại.', sfx: 'pop' },
      { id: 'ruby-2', say: 'Sinatra là lựa chọn tối giản cho API nhỏ hoặc dịch vụ nội bộ. Rails hợp với web application, nền tảng dịch vụ và sản phẩm khởi nghiệp cần ra mắt nhanh.', sfx: 'click' },
      { id: 'ruby-3', say: 'Đánh đổi: hiệu năng thuần không phải điểm mạnh nhất, nhưng thời gian phát triển rất đáng nể.', sfx: 'chime' }
    ]
  },
  {
    id: 'compare',
    type: 'compare',
    part: 4,
    title: 'So sánh bảy hệ sinh thái',
    cues: [
      { id: 'compare-1', say: 'Đặt bảy hệ sinh thái cạnh nhau: JavaScript mạnh web; Python về API, AI, dữ liệu; PHP về web doanh nghiệp; Java về hệ thống lớn; C# về web và Microsoft; Go về hiệu năng; Ruby về tốc độ phát triển.', sfx: 'whoosh' },
      { id: 'compare-2', say: 'Đừng tìm framework tốt nhất. Câu trả lời là: không có. Mỗi công cụ sinh ra cho một bài toán.', sfx: 'marker' },
      { id: 'compare-3', say: 'Hãy cân nhắc quy mô, yêu cầu nghiệp vụ, hiệu năng, đội ngũ, hệ sinh thái thư viện và khả năng bảo trì.', sfx: 'chime' },
      { id: 'compare-4', say: 'Một chi tiết thực tế: chọn công nghệ đội bạn giỏi nhanh hơn chọn công nghệ đang hot nhưng không ai biết dùng.', sfx: 'success' }
    ]
  },
  {
    id: 'choose',
    type: 'choose',
    part: 4,
    title: 'Chọn công nghệ theo bài toán',
    cues: [
      { id: 'choose-1', say: 'Vậy chọn thế nào? Đừng theo trend. Hãy hỏi năm câu: quy mô, hiệu năng, đội ngũ, hệ sinh thái và chi phí bảo trì.', sfx: 'pop' },
      { id: 'choose-2', say: 'Dự án nhỏ cần REST API nhanh: Express hoặc FastAPI là đủ, ít nghi thức, triển khai nhanh.', sfx: 'click' },
      { id: 'choose-3', say: 'Hệ thống quản lý nhiều nghiệp vụ: Laravel, Django, NestJS hoặc ASP.NET Core — chọn theo đội ngũ và hệ sinh thái.', sfx: 'marker' },
      { id: 'choose-4', say: 'Doanh nghiệp lớn: Spring Boot hoặc ASP.NET Core, tùy kiến trúc, bảo mật và năng lực đội ngũ.', sfx: 'success' }
    ]
  },
  {
    id: 'login',
    type: 'login',
    part: 5,
    title: 'Backend hoạt động thật',
    cues: [
      { id: 'login-1', say: 'Giờ xem backend hoạt động thật, không còn sơ đồ. Bên trái là form đăng nhập; bên phải là API Node.js dùng Express, bcrypt để băm mật khẩu và JWT để cấp token.', sfx: 'pop' },
      { id: 'login-2', say: 'Frontend gửi POST /login kèm email, mật khẩu. Backend kiểm tra dữ liệu, tìm người dùng trong database, so sánh mật khẩu bằng bcrypt. Mật khẩu gốc không bao giờ lưu dạng văn bản thuần.', sfx: 'data' },
      { id: 'login-3', say: 'Nếu khớp, server ký JWT access token có thời hạn và trả về kèm thông tin người dùng. Nếu sai, trả lỗi 401 — không tiết lộ tài khoản có tồn tại hay không.', sfx: 'click' },
      { id: 'login-4', say: 'Frontend nhận response, lưu token an toàn và chuyển hướng. Cả quá trình vài trăm mili giây, nhưng có đủ xác thực, phân quyền và bảo mật.', sfx: 'success' }
    ]
  },
  {
    id: 'recap',
    type: 'recap',
    part: 6,
    title: 'Năm điều mang về',
    cues: [
      { id: 'recap-1', say: 'Tóm lại. Backend xử lý nghiệp vụ phía máy chủ. Ngôn ngữ là công cụ viết mã. Framework là bộ khung. Mỗi ngôn ngữ có nhiều framework, thế mạnh riêng. Lựa chọn dựa trên bài toán thật.', sfx: 'pop' },
      { id: 'recap-2', say: 'Đừng học framework trước khi hiểu ngôn ngữ. Đừng chọn công nghệ trước khi hiểu dự án. Đó là thứ tự đúng.', sfx: 'chime' }
    ]
  },
  {
    id: 'quiz',
    type: 'quiz',
    part: 6,
    title: 'Kiểm tra nhanh',
    cues: [
      { id: 'quiz-1', say: 'Câu một: Node.js là ngôn ngữ lập trình hay môi trường thực thi? Ba giây, mời bạn chọn.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-1a', say: 'Đáp án: môi trường thực thi. Node.js chạy JavaScript, còn ngôn ngữ là JavaScript.', sfx: 'success' },
      { id: 'quiz-2', say: 'Câu hai: framework nào thường được dùng trong hệ sinh thái Java? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-2a', say: 'Đáp án: Spring Boot. Quarkus và Micronaut cho nhu cầu cloud native.', sfx: 'success' },
      { id: 'quiz-3', say: 'Câu ba: framework nào phù hợp để xây API bằng Python? Ba giây.', sfx: 'whoosh', hold: 3 },
      { id: 'quiz-3a', say: 'Đáp án: FastAPI. Flask và Django cũng được, nhưng FastAPI tối ưu cho API hiện đại.', sfx: 'success' }
    ]
  },
  {
    id: 'outro',
    type: 'outro',
    part: 6,
    title: 'Chọn đúng công cụ',
    cues: [
      { id: 'outro-1', say: 'Backend chính là bộ não phía sau mỗi ứng dụng web. Hiểu ngôn ngữ và framework sẽ giúp bạn chọn đúng công nghệ, và xây những hệ thống mạnh mẽ, chuyên nghiệp hơn. Hẹn gặp bạn ở bài tiếp theo.', sfx: 'chime' }
    ]
  }
];

export const totalCues = scenes.reduce((a, s) => a + s.cues.length, 0);
