// Kịch bản bài giảng: "Cơ sở dữ liệu và ứng dụng trong thực tế"
// Mỗi scene gồm các cue (câu thuyết minh). Cue là đơn vị đồng bộ giữa giọng đọc và hình ảnh.

export const scenes = [
  {
    id: 'intro',
    type: 'coldopen',
    part: null,
    title: 'Cơ sở dữ liệu và ứng dụng trong thực tế',
    cues: [
      { id: 'intro-1', say: 'Chào các bạn. Chào mừng đến với bài giảng Cơ sở dữ liệu và ứng dụng trong thực tế.', sfx: 'boot' },
      { id: 'intro-2', say: 'Hôm nay, chúng ta sẽ đi từ những khái niệm nền tảng nhất, cho đến thiết kế sơ đồ ERD, và viết những câu truy vấn SQL thật sự.', sfx: 'whoosh' },
      { id: 'intro-3', say: 'Mục tiêu là: sau bài học, các bạn có thể đọc hiểu một cơ sở dữ liệu, thiết kế được mô hình dữ liệu cho một cửa hàng, và tự viết truy vấn để lấy ra thông tin mình cần.' }
    ]
  },
  {
    id: 'objectives',
    type: 'objectives',
    part: null,
    title: 'Mục tiêu bài học',
    cues: [
      { id: 'obj-1', say: 'Bài giảng gồm bảy phần, đi theo một lộ trình rõ ràng.', sfx: 'whoosh' },
      { id: 'obj-2', say: 'Phần một và hai: hiểu cơ sở dữ liệu là gì, hệ quản trị cơ sở dữ liệu là gì, và các thành phần của một bảng.' },
      { id: 'obj-3', say: 'Phần ba và bốn: ba loại mối quan hệ, và cách chuyển một bài toán thực tế thành sơ đồ ERD.' },
      { id: 'obj-4', say: 'Phần năm, sáu và bảy: ngôn ngữ SQL, sáu bài toán truy vấn trên dữ liệu cửa hàng điện thoại, và phần tổng kết, ôn tập.', sfx: 'sparkle' }
    ]
  },
  {
    id: 'div1',
    type: 'divider',
    part: 1,
    title: 'Giới thiệu cơ sở dữ liệu',
    cues: [
      { id: 'div1-1', say: 'Phần một. Giới thiệu cơ sở dữ liệu.', sfx: 'riser' }
    ]
  },
  {
    id: 'db-concept',
    type: 'dbconcept',
    part: 1,
    title: 'Cơ sở dữ liệu là gì?',
    cues: [
      { id: 'dbc-1', say: 'Hãy bắt đầu bằng câu hỏi đơn giản: cơ sở dữ liệu là gì?' },
      { id: 'dbc-2', say: 'Cơ sở dữ liệu là một tập hợp dữ liệu được tổ chức có cấu trúc, lưu trữ trên máy tính, và được quản lý để nhiều người có thể truy cập, tìm kiếm và cập nhật một cách hiệu quả.', sfx: 'chime' },
      { id: 'dbc-3', say: 'Ví dụ: danh sách sinh viên, hóa đơn bán hàng, hay lịch sử giao dịch ngân hàng, đều có thể được lưu trong cơ sở dữ liệu.' },
      { id: 'dbc-4', say: 'Điểm quan trọng là: dữ liệu ở đây không phải một mớ hỗn độn, mà có cấu trúc rõ ràng, và các phần tử có quan hệ với nhau.' }
    ]
  },
  {
    id: 'data-info',
    type: 'datainfo',
    part: 1,
    title: 'Dữ liệu và thông tin',
    cues: [
      { id: 'di-1', say: 'Nhiều bạn nhầm lẫn giữa dữ liệu và thông tin. Dữ liệu là những sự kiện thô, chưa qua xử lý. Ví dụ: một con số, một ngày tháng, một mã đơn hàng.' },
      { id: 'di-2', say: 'Thông tin là kết quả sau khi dữ liệu được xử lý, tổng hợp, và đặt trong ngữ cảnh.', sfx: 'chime' },
      { id: 'di-3', say: 'Cùng một tập dữ liệu, nhưng khi ta tính tổng doanh thu theo tháng, ta có thông tin để ra quyết định. Dữ liệu là nguyên liệu, còn thông tin là sản phẩm.' }
    ]
  },
  {
    id: 'why-db',
    type: 'whydb',
    part: 1,
    title: 'Vì sao cần cơ sở dữ liệu?',
    cues: [
      { id: 'why-1', say: 'Vậy tại sao phải dùng cơ sở dữ liệu, thay vì lưu bằng file Excel hay sổ sách?' },
      { id: 'why-2', say: 'Khi dữ liệu lớn dần, cách lưu file truyền thống bộc lộ bốn vấn đề: dư thừa dữ liệu, dữ liệu không nhất quán, tìm kiếm chậm, và không thể chia sẻ an toàn cho nhiều người.', sfx: 'whoosh' },
      { id: 'why-3', say: 'Cơ sở dữ liệu giải quyết bằng bốn cách: chuẩn hóa cấu trúc để giảm dư thừa, dùng ràng buộc để đảm bảo nhất quán, dùng chỉ mục để tìm nhanh, và phân quyền để kiểm soát truy cập.', sfx: 'sparkle' },
      { id: 'why-4', say: 'Đặc biệt, nhiều người có thể làm việc cùng lúc, mà không ghi đè lên dữ liệu của nhau.' }
    ]
  },
  {
    id: 'shop',
    type: 'shop',
    part: 1,
    title: 'Bài toán: cửa hàng điện thoại',
    cues: [
      { id: 'shop-1', say: 'Hãy hình dung một cửa hàng điện thoại, với khoảng một nghìn hai trăm sản phẩm, ba trăm tám mươi khách hàng, và hơn năm nghìn hóa đơn mỗi năm.', sfx: 'whoosh' },
      { id: 'shop-2', say: 'Nếu lưu bằng file rời rạc, mỗi nhân viên giữ một bản Excel, thì việc đồng bộ gần như không thể: giá cũ, tồn kho sai, khách hàng bị trùng.' },
      { id: 'shop-3', say: 'Với cơ sở dữ liệu, tất cả nằm trong một nguồn dữ liệu duy nhất. Bán một chiếc điện thoại, tồn kho tự giảm, hóa đơn được ghi lại, doanh thu cập nhật ngay.', sfx: 'success' },
      { id: 'shop-4', say: 'Đó là lý do gần như mọi ứng dụng hiện đại đều có một cơ sở dữ liệu phía sau.' }
    ]
  },
  {
    id: 'dbms',
    type: 'dbms',
    part: 1,
    title: 'Hệ quản trị cơ sở dữ liệu',
    cues: [
      { id: 'dbms-1', say: 'Cơ sở dữ liệu là dữ liệu. Còn phần mềm dùng để tạo, quản lý và truy vấn dữ liệu đó, gọi là hệ quản trị cơ sở dữ liệu, viết tắt là DBMS.' },
      { id: 'dbms-2', say: 'Bốn hệ quản trị phổ biến nhất hiện nay: MySQL, mã nguồn mở, rất phổ biến với ứng dụng web; SQL Server của Microsoft; PostgreSQL, mạnh về tính chuẩn và khả năng mở rộng; và Oracle, thường dùng trong hệ thống lớn như ngân hàng, tài chính.', sfx: 'whoosh' },
      { id: 'dbms-3', say: 'Điểm chung: cả bốn đều dùng ngôn ngữ SQL để làm việc với dữ liệu. Học tốt SQL, các bạn có thể chuyển đổi giữa chúng khá dễ dàng.' },
      { id: 'dbms-4', say: 'Ngoài truy vấn, DBMS còn lo bảo mật, sao lưu, phục hồi, và xử lý nhiều người dùng cùng lúc.' }
    ]
  },
  {
    id: 'div2',
    type: 'divider',
    part: 2,
    title: 'Các thành phần của cơ sở dữ liệu',
    cues: [
      { id: 'div2-1', say: 'Phần hai. Các thành phần của cơ sở dữ liệu.', sfx: 'riser' }
    ]
  },
  {
    id: 'table-anatomy',
    type: 'tableanatomy',
    part: 2,
    title: 'Bảng, dòng và cột',
    cues: [
      { id: 'ta-1', say: 'Bây giờ, hãy mổ xẻ một cơ sở dữ liệu để xem bên trong có gì. Đơn vị cơ bản nhất là bảng, hay table.' },
      { id: 'ta-2', say: 'Bảng SinhVien có bốn cột: MaSV, HoTen, Lop, Email. Mỗi cột là một thuộc tính, hay còn gọi là trường, field.', sfx: 'chime' },
      { id: 'ta-3', say: 'Mỗi dòng là một bản ghi, record, đại diện cho một đối tượng cụ thể. Ở đây, mỗi dòng là một sinh viên.' },
      { id: 'ta-4', say: 'Cột quy định kiểu dữ liệu và ý nghĩa. Dòng chứa các giá trị thực tế. Toàn bộ các dòng tạo thành dữ liệu của bảng.' }
    ]
  },
  {
    id: 'primary-key',
    type: 'primarykey',
    part: 2,
    title: 'Khóa chính',
    cues: [
      { id: 'pk-1', say: 'Trong bốn cột đó, MaSV có một vai trò đặc biệt: nó là khóa chính, primary key.', sfx: 'chime' },
      { id: 'pk-2', say: 'Khóa chính là một cột, hoặc một tổ hợp cột, xác định duy nhất mỗi bản ghi trong bảng. Không được trùng, và không được để trống.' },
      { id: 'pk-3', say: 'Vì sao cần? Vì tên có thể trùng. Có hai bạn cùng tên Nguyễn Văn An, cùng lớp. Nếu không có mã định danh, hệ thống không biết đang cập nhật hồ sơ của ai.', sfx: 'error' },
      { id: 'pk-4', say: 'Nhờ MaSV, mỗi sinh viên là duy nhất. Khóa chính thường là mã, số căn cước, hoặc một mã do hệ thống sinh ra.' }
    ]
  },
  {
    id: 'foreign-key',
    type: 'foreignkey',
    part: 2,
    title: 'Khóa ngoại',
    cues: [
      { id: 'fk-1', say: 'Nếu khóa chính định danh bản ghi trong bảng của nó, thì khóa ngoại tạo cầu nối giữa hai bảng.' },
      { id: 'fk-2', say: 'Cột MaLop trong bảng SinhVien là khóa ngoại, tham chiếu đến khóa chính MaLop của bảng Lop.', sfx: 'chime' },
      { id: 'fk-3', say: 'Ràng buộc khóa ngoại đảm bảo: không thể gán một sinh viên vào lớp không tồn tại. Thử nhập MaLop là DA99, hệ thống sẽ từ chối.', sfx: 'error' },
      { id: 'fk-4', say: 'Nhờ vậy, dữ liệu luôn liên kết đúng, và ta có thể truy vấn chéo giữa các bảng.' }
    ]
  },
  {
    id: 'div3',
    type: 'divider',
    part: 3,
    title: 'Các loại mối quan hệ',
    cues: [
      { id: 'div3-1', say: 'Phần ba. Các loại mối quan hệ.', sfx: 'riser' }
    ]
  },
  {
    id: 'rel-1-1',
    type: 'rel11',
    part: 3,
    title: 'Quan hệ một-một',
    cues: [
      { id: 'r11-1', say: 'Có ba loại mối quan hệ chính. Thứ nhất, một-một. Một sinh viên có đúng một hồ sơ cá nhân, và mỗi hồ sơ thuộc về đúng một sinh viên.', sfx: 'whoosh' },
      { id: 'r11-2', say: 'Trong mô hình, ta đặt khóa ngoại MaSV vào bảng HoSo, kèm ràng buộc duy nhất, để mỗi sinh viên chỉ có tối đa một hồ sơ.' },
      { id: 'r11-3', say: 'Quan hệ một-một thường dùng để tách những thông tin ít dùng, hoặc nhạy cảm, sang một bảng riêng.' }
    ]
  },
  {
    id: 'rel-1-n',
    type: 'rel1n',
    part: 3,
    title: 'Quan hệ một-nhiều',
    cues: [
      { id: 'r1n-1', say: 'Thứ hai, một-nhiều. Một lớp có nhiều sinh viên, nhưng mỗi sinh viên chỉ thuộc một lớp.', sfx: 'whoosh' },
      { id: 'r1n-2', say: 'Cách hiện thực rất gọn: đặt khóa ngoại ở phía nhiều. Cột MaLop nằm trong bảng SinhVien.', sfx: 'chime' },
      { id: 'r1n-3', say: 'Đây là quan hệ phổ biến nhất trong thực tế: khách hàng và hóa đơn, danh mục và sản phẩm, nhân viên và hợp đồng.' }
    ]
  },
  {
    id: 'rel-n-n',
    type: 'relnn',
    part: 3,
    title: 'Quan hệ nhiều-nhiều',
    cues: [
      { id: 'rnn-1', say: 'Thứ ba, nhiều-nhiều. Một sinh viên đăng ký nhiều môn học, và một môn học có nhiều sinh viên.', sfx: 'whoosh' },
      { id: 'rnn-2', say: 'Không thể đặt khóa ngoại trực tiếp, vì mỗi ô chỉ chứa một giá trị. Giải pháp là tạo một bảng trung gian, ở đây là DangKy.', sfx: 'chime' },
      { id: 'rnn-3', say: 'Bảng DangKy chứa hai khóa ngoại: MaSV và MaMH, và hai cột này cùng tạo thành khóa chính. Mỗi dòng là một lần đăng ký.' },
      { id: 'rnn-4', say: 'Nhìn lại, quan hệ nhiều-nhiều đã được tách thành hai quan hệ một-nhiều. Đây là kỹ thuật các bạn sẽ dùng rất nhiều khi thiết kế.', sfx: 'success' }
    ]
  },
  {
    id: 'div4',
    type: 'divider',
    part: 4,
    title: 'Thiết kế cơ sở dữ liệu và sơ đồ ERD',
    cues: [
      { id: 'div4-1', say: 'Phần bốn. Thiết kế cơ sở dữ liệu và sơ đồ ERD.', sfx: 'riser' }
    ]
  },
  {
    id: 'erd-concepts',
    type: 'erdconcepts',
    part: 4,
    title: 'Thực thể, thuộc tính, quan hệ',
    cues: [
      { id: 'erdc-1', say: 'Để thiết kế cơ sở dữ liệu, ta dùng sơ đồ thực thể liên kết, gọi tắt là ERD.' },
      { id: 'erdc-2', say: 'Ba thành phần chính: thực thể, là đối tượng cần quản lý, ví dụ khách hàng; thuộc tính, là thông tin mô tả thực thể, ví dụ họ tên, số điện thoại; và mối quan hệ, là sự liên kết giữa các thực thể.', sfx: 'chime' },
      { id: 'erdc-3', say: 'Trong ký pháp kinh điển, thực thể là hình chữ nhật, thuộc tính là hình elip, quan hệ là hình thoi. Trong thực tế, ta thường dùng dạng bảng gọn hơn, nhưng ý nghĩa không đổi.' },
      { id: 'erdc-4', say: 'Một thực thể sẽ trở thành một bảng. Một thuộc tính trở thành một cột. Khóa chính đảm bảo định danh, còn khóa ngoại hiện thực mối quan hệ.' }
    ]
  },
  {
    id: 'erd-analysis',
    type: 'erdanalysis',
    part: 4,
    title: 'Phân tích bài toán bán hàng',
    cues: [
      { id: 'erda-1', say: 'Bài toán: xây dựng cơ sở dữ liệu quản lý bán hàng cho một cửa hàng điện thoại.', sfx: 'whoosh' },
      { id: 'erda-2', say: 'Bước một, phân tích yêu cầu. Cửa hàng cần quản lý khách hàng, sản phẩm, nhân viên, hóa đơn, và chi tiết từng hóa đơn.' },
      { id: 'erda-3', say: 'Từ các danh từ trong yêu cầu, ta xác định thực thể: KhachHang, SanPham, NhanVien, HoaDon. Và vì một hóa đơn có nhiều sản phẩm, với số lượng và đơn giá riêng, ta cần thêm ChiTietHoaDon.', sfx: 'chime' },
      { id: 'erda-4', say: 'Bước hai: xác định thuộc tính và khóa chính cho từng thực thể. Bước ba: xác định quan hệ và số lượng giữa chúng.' },
      { id: 'erda-5', say: 'Một khách hàng có nhiều hóa đơn. Một nhân viên lập nhiều hóa đơn. Một hóa đơn có nhiều chi tiết. Và mỗi chi tiết ứng với một sản phẩm.' }
    ]
  },
  {
    id: 'erd-build',
    type: 'erdbuild',
    part: 4,
    title: 'Sơ đồ ERD cửa hàng điện thoại',
    cues: [
      { id: 'erdb-1', say: 'Đây là sơ đồ ERD hoàn chỉnh: năm thực thể, với khóa chính màu vàng và khóa ngoại màu xanh.', sfx: 'whoosh' },
      { id: 'erdb-2', say: 'KhachHang một-nhiều HoaDon qua MaKH. NhanVien một-nhiều HoaDon qua MaNV.', sfx: 'chime' },
      { id: 'erdb-3', say: 'HoaDon một-nhiều ChiTietHoaDon. SanPham một-nhiều ChiTietHoaDon. Và ChiTietHoaDon có khóa chính ghép: MaHD cộng với MaSP.', sfx: 'chime' },
      { id: 'erdb-4', say: 'Lưu ý: DonGia được lưu trong chi tiết hóa đơn, để giữ đúng giá tại thời điểm bán, kể cả sau này sản phẩm đổi giá.', sfx: 'sparkle' },
      { id: 'erdb-5', say: 'Thiết kế này tránh lặp dữ liệu, và đảm bảo mỗi thông tin chỉ được lưu ở một nơi hợp lý.' }
    ]
  },
  {
    id: 'div5',
    type: 'divider',
    part: 5,
    title: 'Ngôn ngữ SQL cơ bản',
    cues: [
      { id: 'div5-1', say: 'Phần năm. Ngôn ngữ SQL cơ bản.', sfx: 'riser' }
    ]
  },
  {
    id: 'sql-groups',
    type: 'sqlgroups',
    part: 5,
    title: 'Năm nhóm lệnh SQL',
    cues: [
      { id: 'sqlg-1', say: 'SQL là ngôn ngữ chuẩn để làm việc với cơ sở dữ liệu quan hệ. Các lệnh được chia thành năm nhóm.' },
      { id: 'sqlg-2', say: 'DDL, ngôn ngữ định nghĩa dữ liệu: CREATE tạo, ALTER sửa cấu trúc, DROP xóa.', sfx: 'chime' },
      { id: 'sqlg-3', say: 'DML, ngôn ngữ thao tác dữ liệu: INSERT thêm, UPDATE cập nhật, DELETE xóa bản ghi.' },
      { id: 'sqlg-4', say: 'DQL, ngôn ngữ truy vấn: SELECT. Đây là nhóm lệnh các bạn sẽ dùng nhiều nhất.', sfx: 'chime' },
      { id: 'sqlg-5', say: 'DCL, ngôn ngữ điều khiển truy cập: GRANT cấp quyền, REVOKE thu hồi quyền. Và TCL, điều khiển giao dịch: COMMIT xác nhận, ROLLBACK hoàn tác.' },
      { id: 'sqlg-6', say: 'Nắm được năm nhóm này, các bạn đã có bản đồ tổng thể về SQL.', sfx: 'sparkle' }
    ]
  },
  {
    id: 'sql-create',
    type: 'sqlcreate',
    part: 5,
    title: 'DDL: tạo bảng',
    cues: [
      { id: 'sqlc-1', say: 'Hãy tạo bảng SinhVien. CREATE TABLE, tên bảng, sau đó là danh sách cột trong ngoặc.', sfx: 'whoosh' },
      { id: 'sqlc-2', say: 'MaSV kiểu VARCHAR mười ký tự, và ghi PRIMARY KEY ngay sau khai báo.', sfx: 'type' },
      { id: 'sqlc-3', say: 'HoTen dùng NVARCHAR một trăm, để lưu được tiếng Việt có dấu. Lop là VARCHAR hai mươi. Email là VARCHAR một trăm.' },
      { id: 'sqlc-4', say: 'Chạy lệnh, hệ quản trị trả về thông báo tạo bảng thành công. Cấu trúc đã sẵn sàng, nhưng bảng chưa có dữ liệu.', sfx: 'success' }
    ]
  },
  {
    id: 'sql-insert',
    type: 'sqlinsert',
    part: 5,
    title: 'DML và DQL',
    cues: [
      { id: 'sqli-1', say: 'Thêm một bản ghi bằng INSERT INTO, theo sau là tên bảng và danh sách giá trị, đúng thứ tự các cột.', sfx: 'type' },
      { id: 'sqli-2', say: 'Chuỗi tiếng Việt có dấu nên đặt sau chữ N, ví dụ N Nguyễn Văn An. Đây là cách SQL Server hiểu đó là chuỗi Unicode.', sfx: 'chime' },
      { id: 'sqli-3', say: 'Để xem dữ liệu, dùng SELECT dấu sao FROM SinhVien. Dấu sao nghĩa là lấy tất cả các cột.' },
      { id: 'sqli-4', say: 'Kết quả là một bảng tạm, gọi là result set. Lưu ý: câu lệnh SELECT không làm thay đổi dữ liệu gốc.', sfx: 'success' }
    ]
  },
  {
    id: 'div6',
    type: 'divider',
    part: 6,
    title: 'Bài toán truy vấn thực tế',
    cues: [
      { id: 'div6-1', say: 'Phần sáu. Các bài toán truy vấn thực tế.', sfx: 'riser' }
    ]
  },
  {
    id: 'shop-schema',
    type: 'shopschema',
    part: 6,
    title: 'Dữ liệu cửa hàng điện thoại',
    cues: [
      { id: 'ss-1', say: 'Giờ chúng ta vận dụng vào cơ sở dữ liệu cửa hàng điện thoại vừa thiết kế. Đây là dữ liệu mẫu.', sfx: 'whoosh' },
      { id: 'ss-2', say: 'Bảng SanPham có năm sản phẩm, với giá từ tám triệu đến ba mươi hai triệu. KhachHang có bốn khách. HoaDon và ChiTietHoaDon ghi lại các lần mua.' },
      { id: 'ss-3', say: 'Mỗi bài toán dưới đây sẽ đi theo bốn bước: đọc đề, phân tích, viết SQL, và đọc kết quả.' }
    ]
  },
  {
    id: 'q1',
    type: 'queryAll',
    part: 6,
    title: 'Bài toán 1: Toàn bộ sản phẩm',
    cues: [
      { id: 'q1-1', say: 'Bài toán một: hiển thị toàn bộ danh sách sản phẩm để kiểm kê.', sfx: 'whoosh' },
      { id: 'q1-2', say: 'Phân tích: cần tất cả các cột, của tất cả các dòng, trong bảng SanPham.' },
      { id: 'q1-3', say: 'Câu lệnh: SELECT dấu sao FROM SanPham. Không có điều kiện, nên lấy toàn bộ năm dòng.', sfx: 'type' },
      { id: 'q1-4', say: 'Kết quả trả về đủ năm sản phẩm, đúng thứ tự các cột trong bảng.', sfx: 'success' }
    ]
  },
  {
    id: 'q2',
    type: 'queryPrice',
    part: 6,
    title: 'Bài toán 2: Sản phẩm trên 10 triệu',
    cues: [
      { id: 'q2-1', say: 'Bài toán hai: tìm những sản phẩm có giá trên mười triệu, để đưa vào nhóm cao cấp.', sfx: 'whoosh' },
      { id: 'q2-2', say: 'Phân tích: lọc theo cột DonGia, dùng mệnh đề WHERE với điều kiện lớn hơn mười triệu. Đơn giá tính bằng đồng.' },
      { id: 'q2-3', say: 'SELECT dấu sao FROM SanPham, WHERE DonGia lớn hơn mười triệu.', sfx: 'type' },
      { id: 'q2-4', say: 'Ba sản phẩm thỏa điều kiện: iPhone 15 Pro Max, Galaxy S24 Ultra và Xiaomi 14. Hai dòng còn lại bị loại, vì giá không lớn hơn mười triệu.', sfx: 'success' }
    ]
  },
  {
    id: 'q3',
    type: 'queryCustomers',
    part: 6,
    title: 'Bài toán 3: Khách đã mua hàng',
    cues: [
      { id: 'q3-1', say: 'Bài toán ba: liệt kê khách hàng đã từng mua hàng, mỗi người một lần.', sfx: 'whoosh' },
      { id: 'q3-2', say: 'Phân tích: thông tin khách nằm ở bảng KhachHang, nhưng việc mua hàng nằm ở bảng HoaDon. Cần nối hai bảng qua MaKH. Dùng DISTINCT để loại trùng.' },
      { id: 'q3-3', say: 'SELECT DISTINCT cột HoTen, FROM KhachHang, INNER JOIN HoaDon, ON MaKH bằng nhau.', sfx: 'type' },
      { id: 'q3-4', say: 'Kết quả chỉ còn những khách có hóa đơn. Khách chưa mua hàng không xuất hiện, vì INNER JOIN chỉ giữ các dòng khớp ở cả hai bảng.', sfx: 'success' }
    ]
  },
  {
    id: 'q4',
    type: 'queryRevenue',
    part: 6,
    title: 'Bài toán 4: Tổng doanh thu',
    cues: [
      { id: 'q4-1', say: 'Bài toán bốn: tính tổng doanh thu của cửa hàng.', sfx: 'whoosh' },
      { id: 'q4-2', say: 'Phân tích: doanh thu của một dòng chi tiết bằng số lượng nhân đơn giá. Tổng doanh thu là tổng của tất cả các dòng.' },
      { id: 'q4-3', say: 'SELECT SUM của SoLuong nhân DonGia, FROM ChiTietHoaDon.', sfx: 'type' },
      { id: 'q4-4', say: 'Kết quả: hai trăm mười lăm triệu đồng. Hàm SUM gộp nhiều dòng thành một giá trị duy nhất.', sfx: 'success' }
    ]
  },
  {
    id: 'q5',
    type: 'queryQty',
    part: 6,
    title: 'Bài toán 5: Số lượng đã bán',
    cues: [
      { id: 'q5-1', say: 'Bài toán năm: thống kê số lượng đã bán của từng sản phẩm.', sfx: 'whoosh' },
      { id: 'q5-2', say: 'Phân tích: cần nhóm các dòng theo sản phẩm, rồi cộng số lượng trong mỗi nhóm. Đó là GROUP BY.' },
      { id: 'q5-3', say: 'SELECT MaSP, SUM SoLuong, FROM ChiTietHoaDon, GROUP BY MaSP.', sfx: 'type' },
      { id: 'q5-4', say: 'iPhone 15 Pro Max dẫn đầu với bốn chiếc. Nhóm theo mã sản phẩm giúp tổng hợp chính xác từng mặt hàng.', sfx: 'success' }
    ]
  },
  {
    id: 'q6',
    type: 'queryJoin',
    part: 6,
    title: 'Bài toán 6: Kết hợp nhiều bảng',
    cues: [
      { id: 'q6-1', say: 'Bài toán sáu, cũng là bài tổng hợp: in ra bảng kê chi tiết, gồm tên khách hàng, tên nhân viên, tên sản phẩm, số lượng và thành tiền.', sfx: 'whoosh' },
      { id: 'q6-2', say: 'Phân tích: thông tin nằm rải ở bốn bảng. Ta nối HoaDon với KhachHang, NhanVien, rồi ChiTietHoaDon, rồi SanPham, tất cả bằng INNER JOIN.' },
      { id: 'q6-3', say: 'Câu lệnh nối bốn bảng, và tính thành tiền bằng SoLuong nhân DonGia.', sfx: 'type' },
      { id: 'q6-4', say: 'Kết quả là một bảng kê đầy đủ, đúng như hóa đơn in cho khách. Đây là sức mạnh của mô hình quan hệ: dữ liệu tách nhỏ để tránh trùng lặp, nhưng vẫn ghép lại được khi cần.', sfx: 'success' }
    ]
  },
  {
    id: 'div7',
    type: 'divider',
    part: 7,
    title: 'Tổng kết và ôn tập',
    cues: [
      { id: 'div7-1', say: 'Phần bảy. Tổng kết và câu hỏi ôn tập.', sfx: 'riser' }
    ]
  },
  {
    id: 'summary',
    type: 'summary',
    part: 7,
    title: 'Tổng kết',
    cues: [
      { id: 'sum-1', say: 'Chúng ta đã đi qua toàn bộ nền tảng. Hãy chốt lại những ý quan trọng nhất.', sfx: 'whoosh' },
      { id: 'sum-2', say: 'Cơ sở dữ liệu là dữ liệu có cấu trúc, được quản lý bởi DBMS. Dữ liệu là nguyên liệu, thông tin là kết quả sau xử lý.', sfx: 'chime' },
      { id: 'sum-3', say: 'Bảng gồm cột và dòng. Khóa chính định danh duy nhất, khóa ngoại liên kết các bảng.' },
      { id: 'sum-4', say: 'Ba loại quan hệ: một-một, một-nhiều, nhiều-nhiều. Quan hệ nhiều-nhiều cần bảng trung gian.' },
      { id: 'sum-5', say: 'ERD giúp chuyển bài toán thực tế thành mô hình dữ liệu. Và SQL là công cụ để tạo, cập nhật và truy vấn.' },
      { id: 'sum-6', say: 'Quy trình thực tế: hiểu yêu cầu, thiết kế ERD, tạo bảng, nhập dữ liệu, rồi truy vấn.', sfx: 'success' }
    ]
  },
  {
    id: 'quiz',
    type: 'quiz',
    part: 7,
    title: 'Câu hỏi ôn tập',
    cues: [
      { id: 'quiz-intro', say: 'Đến phần tự kiểm tra. Năm câu hỏi trắc nghiệm, các bạn hãy chọn đáp án trước khi đáp án hiện ra nhé.', sfx: 'whoosh' },
      { id: 'quiz-1', say: 'Câu một: thành phần nào xác định duy nhất mỗi bản ghi trong bảng? A, khóa ngoại. B, khóa chính. C, chỉ mục. D, khóa ghép.' },
      { id: 'quiz-1a', say: 'Đáp án đúng là B, khóa chính. Khóa chính không được trùng và không được để trống.', sfx: 'success' },
      { id: 'quiz-2', say: 'Câu hai: quan hệ giữa Lop và SinhVien là loại nào? A, một-một. B, một-nhiều. C, nhiều-nhiều. D, không xác định.' },
      { id: 'quiz-2a', say: 'Đáp án đúng là B. Một lớp có nhiều sinh viên, mỗi sinh viên thuộc một lớp.', sfx: 'success' },
      { id: 'quiz-3', say: 'Câu ba: lệnh nào thuộc nhóm DDL? A, INSERT. B, SELECT. C, CREATE TABLE. D, COMMIT.' },
      { id: 'quiz-3a', say: 'Đáp án đúng là C. CREATE TABLE định nghĩa cấu trúc bảng, nên thuộc DDL.', sfx: 'success' },
      { id: 'quiz-4', say: 'Câu bốn: để lọc sản phẩm có giá trên mười triệu, dùng mệnh đề nào? A, GROUP BY. B, ORDER BY. C, WHERE. D, HAVING.' },
      { id: 'quiz-4a', say: 'Đáp án đúng là C, WHERE. HAVING dùng để lọc sau khi nhóm, còn WHERE lọc từng dòng.', sfx: 'success' },
      { id: 'quiz-5', say: 'Câu năm: quan hệ nhiều-nhiều được xử lý bằng cách nào? A, thêm khóa ngoại vào một bảng. B, tạo bảng trung gian chứa hai khóa ngoại. C, gộp hai bảng làm một. D, dùng khóa chính ghép trong bảng gốc.' },
      { id: 'quiz-5a', say: 'Đáp án đúng là B. Bảng trung gian chứa hai khóa ngoại, và chúng tạo thành khóa chính ghép.', sfx: 'success' },
      { id: 'quiz-end', say: 'Nếu các bạn trả lời đúng từ bốn câu trở lên, các bạn đã nắm khá chắc phần nền tảng.', sfx: 'sparkle' }
    ]
  },
  {
    id: 'outro',
    type: 'outro',
    part: 7,
    title: 'Kết thúc bài giảng',
    cues: [
      { id: 'out-1', say: 'Cơ sở dữ liệu không chỉ là một môn học, mà là nền móng của mọi hệ thống phần mềm. Hiểu dữ liệu, bạn hiểu cách hệ thống vận hành.' },
      { id: 'out-2', say: 'Hãy thực hành ngay: cài MySQL hoặc PostgreSQL, tạo bảng SinhVien, và thử viết những truy vấn đầu tiên.', sfx: 'chime' },
      { id: 'out-3', say: 'Cảm ơn các bạn đã theo dõi. Chúc các bạn học tốt, và hẹn gặp lại ở bài giảng tiếp theo.', sfx: 'sparkle' }
    ]
  }
];

export const quizData = [
  {
    q: 'Thành phần nào xác định duy nhất mỗi bản ghi trong bảng?',
    options: ['Khóa ngoại', 'Khóa chính', 'Chỉ mục', 'Khóa ghép'],
    answer: 1,
    explain: 'Khóa chính không trùng và không để trống.'
  },
  {
    q: 'Quan hệ giữa Lop và SinhVien là loại nào?',
    options: ['Một-một', 'Một-nhiều', 'Nhiều-nhiều', 'Không xác định'],
    answer: 1,
    explain: 'Một lớp có nhiều sinh viên, mỗi sinh viên thuộc một lớp.'
  },
  {
    q: 'Lệnh nào thuộc nhóm DDL?',
    options: ['INSERT', 'SELECT', 'CREATE TABLE', 'COMMIT'],
    answer: 2,
    explain: 'CREATE TABLE định nghĩa cấu trúc bảng.'
  },
  {
    q: 'Lọc sản phẩm có giá trên 10 triệu dùng mệnh đề nào?',
    options: ['GROUP BY', 'ORDER BY', 'WHERE', 'HAVING'],
    answer: 2,
    explain: 'WHERE lọc từng dòng trước khi nhóm.'
  },
  {
    q: 'Quan hệ nhiều-nhiều được xử lý bằng cách nào?',
    options: ['Thêm khóa ngoại vào một bảng', 'Tạo bảng trung gian chứa hai khóa ngoại', 'Gộp hai bảng làm một', 'Dùng khóa chính ghép trong bảng gốc'],
    answer: 1,
    explain: 'Bảng trung gian chứa hai khóa ngoại, tạo thành khóa chính ghép.'
  }
];

export const parts = [
  { n: 1, title: 'Giới thiệu cơ sở dữ liệu', en: 'FUNDAMENTALS' },
  { n: 2, title: 'Các thành phần của cơ sở dữ liệu', en: 'ANATOMY' },
  { n: 3, title: 'Các loại mối quan hệ', en: 'RELATIONSHIPS' },
  { n: 4, title: 'Thiết kế CSDL và sơ đồ ERD', en: 'DATA MODELING' },
  { n: 5, title: 'Ngôn ngữ SQL cơ bản', en: 'SQL BASICS' },
  { n: 6, title: 'Bài toán truy vấn thực tế', en: 'REAL QUERIES' },
  { n: 7, title: 'Tổng kết và ôn tập', en: 'REVIEW' }
];
