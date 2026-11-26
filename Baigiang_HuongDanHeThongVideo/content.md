# Hệ Thống Sản Xuất Video Bài Giảng Tự Động Trên Terminal

## Cảnh 1: Chào mừng đến với AN TECH Video Engine [hieu_ung: intro]
- mô_tả: Tự động hóa sản xuất video bài giảng Full HD chỉ bằng Terminal — 100% offline, 0đ chi phí API
- ảnh: 1.jpg | Dây chuyền sản xuất video tự động 100% offline
- 100% Chạy Offline | Không cần Agent, không tốn API key
- Giọng Clone VieNeu | Đọc tiếng Việt & thuật ngữ chuẩn xác
- 8 Hiệu Ứng Động | Không cứng nhắc như slide truyền thống
- Chuẩn MASTER 2.3 | Tự động -14 LUFS, đóng logo & QA
> Xin chào các bạn! Chào mừng các bạn quay trở lại với AN TECH ACADEMY, nền tảng kiến thức công nghệ thực chiến.
> Trong video hôm nay, chúng ta sẽ khám phá một hệ thống sản xuất video bài giảng tự động chạy ngay trên Terminal.
> Điểm đặc biệt nhất: toàn bộ quy trình hoạt động 100% offline trên máy tính cá nhân, hoàn toàn không tốn API key.
> Chỉ từ một file ghi chú Markdown và thư mục ảnh, bạn có thể xuất ra video Full HD có giọng clone, nhân vật và hiệu ứng động.
> Video bạn đang xem ngay lúc này cũng được dựng trực tiếp bằng chính hệ thống đó!

## Cảnh 2: Vấn đề của cách làm video truyền thống [hieu_ung: va_cham]
- mô_tả: Vì sao làm video bài giảng thủ công hoặc viết code rời rạc luôn tốn công sức?
- trái: Viết code cứng | Mỗi bài giảng mới phải viết lại hàng trăm dòng Python vẽ từng cảnh
- phải: Chạy lệnh rời rạc | Tách rời 5 bước: đọc giọng, vẽ khung hình, cân âm lượng, gắn logo, kiểm tra lỗi
- cảnh_báo: Quá phụ thuộc vào thao tác tay, dễ quên đóng logo hoặc lệch chuẩn âm thanh!
- Chỉnh sửa chậm | Đổi một dòng chữ phải sửa sâu trong code
- Lỗi phát âm lặp lại | Thuật ngữ tiếng Anh phải nhắc lại mỗi bài mới
- Thiếu tính đồng bộ | Mỗi bài dễ lệch màu sắc và cỡ chữ
> Trước khi có hệ thống này, việc tạo một video bài giảng kỹ thuật tốn rất nhiều công sức lặp đi lặp lại.
> Khó khăn thứ nhất là viết code cứng: cứ sang một chủ đề mới lại phải ngồi viết lại hàng trăm dòng code dựng cảnh từ đầu.
> Khó khăn thứ hai là năm công đoạn từ tạo giọng đọc, dựng khung hình, ghép âm thanh đến đóng logo đều nằm rời rạc.
> Chỉ cần sơ suất một bước, video rất dễ bị lệch âm lượng, thiếu logo thương hiệu hoặc phát âm sai thuật ngữ tiếng Anh.
> Mỗi lần muốn sửa nhẹ một câu thoại hay đổi hiệu ứng một cảnh, người làm lại phải chờ chạy lại gần như toàn bộ.
> Đó là lý do chúng ta cần đóng gói mọi quy tắc chuẩn hóa thành một bộ máy tự vận hành duy nhất.

## Cảnh 3: So sánh Cách cũ và Hệ thống Kit mới [hieu_ung: so_sanh]
- mô_tả: Chuyển từ viết code theo từng bài sang kiến trúc đọc dữ liệu dùng chung
- trước: Phải nhờ Agent viết mới hàng trăm dòng code cho từng bài
- trước: Tự gõ tay từng lệnh FFmpeg, ghép âm thanh và đóng logo
- trước: Bố cục tĩnh giống slide, khó thêm hiệu ứng đồng bộ
- trước: Quên kiểm tra ảnh trong img/ hoặc thiếu bước QA âm thanh
- sau: Toàn bộ luật MASTER 2.3 đã đóng gói sẵn trong thư mục Kit
- sau: Mỗi bài chỉ cần duy nhất 1 file content.md và thư mục img/
- sau: Gõ đúng 1 lệnh Terminal tự chạy trọn gói từ A đến Z
- sau: Sửa 1 cảnh render lại trong vài giây nhờ bộ nhớ Cache thông minh
> Hãy nhìn sự khác biệt rõ rệt giữa quy trình cũ và hệ thống AN TECH Video Engine mới.
> Với cách làm cũ, mỗi bài giảng giống như việc bạn phải xây lại một căn bếp mới chỉ để nấu một món ăn mới.
> Với cách làm mới, chúng ta xây sẵn một dây chuyền dùng chung duy nhất đặt gọn trong thư mục Kit.
> Toàn bộ quy tắc thương hiệu, bảng màu, cỡ chữ, vị trí logo và chuẩn âm thanh đều được cài đặt sẵn trong mã nguồn.
> Mỗi khi làm bài giảng mới, bạn không cần đụng vào một dòng code Python nào nữa, mà chỉ cần chuẩn bị nội dung văn bản.
> Từ đó, một câu lệnh Terminal duy nhất sẽ điều phối toàn bộ dây chuyền để xuất ra file MP4 hoàn chỉnh.

## Cảnh 4: Kiến trúc thư mục Kit và Thư mục bài giảng [hieu_ung: anh_dong]
- mô_tả: Mọi tài nguyên dùng chung nằm tại Kit; mỗi bài giảng chỉ chứa nội dung riêng biệt
- ảnh: 2.jpg | Kho lõi Kit: Chuẩn màu, Phát âm, Nhân vật, SFX & Templates
- ảnh: 3.jpg | Thư mục bài giảng gọn nhẹ: content.md, notes.md và img/
> Toàn bộ hệ thống được tổ chức tách bạch thành hai khu vực cực kỳ gọn gàng và dễ quản lý.
> Khu vực thứ nhất là thư mục Kit — đây là bộ não trung tâm chứa tất cả quy chuẩn và hiệu ứng dùng chung.
> Bên trong Kit có file cấu hình chuẩn standard_2_3.json quy định độ phân giải, font chữ, màu sắc và thông số logo.
> Ngay bên cạnh là từ điển pronunciation.json giúp tự động chuyển các từ tiếng Anh như Python, ChatGPT hay Terminal sang cách đọc chuẩn.
> Khu vực thứ hai là thư mục của từng bài giảng riêng lẻ, bên trong chỉ gồm file content.md, file notes.md và thư mục img/.
> Nhờ tách biệt rõ ràng như vậy, bạn chỉ cần chỉnh sửa một lần trong Kit là toàn bộ các bài giảng về sau đều tự động đẹp theo.

## Cảnh 5: Quy trình 4 bước tự tay xuất video [hieu_ung: quy_trinh]
- mô_tả: Từ ý tưởng thô đến video thành phẩm chỉ qua 4 bước mạch lạc, không cần API key
- ảnh: 4.jpg | Tự động tổng hợp giọng clone VieNeu và chuẩn hóa âm thanh offline
- Soạn bài ChatGPT | Dán Prompt mẫu tạo content.md và ảnh 1.jpg, 2.jpg...
- Lưu vào thư mục | Bỏ content.md và các ảnh đúng tên vào thư mục img/
- Kiểm tra & Preview | Chạy lệnh check rồi preview 30 giây kiểm tra bố cục
- Xuất video Full | Gõ lệnh render tự động đóng logo và in bảng QA
> Khi bạn tự làm bài giảng lần sau, toàn bộ quy trình chỉ gói gọn trong bốn bước tuần tự rất dễ nhớ.
> Bước một: bạn mở ChatGPT, dán bộ Prompt mẫu có sẵn và nhập tên chủ đề cùng thời lượng mong muốn.
> ChatGPT sẽ tự chia sẵn các cảnh theo đúng cú pháp Markdown, chọn sẵn hiệu ứng động và liệt kê danh sách ảnh cần tạo.
> Bước hai: bạn dán nội dung vào file content.md và lưu các bức ảnh đúng số thứ tự 1.jpg, 2.jpg vào thư mục img/.
> Bước ba: mở Terminal chạy lệnh check để kiểm tra thiếu ảnh hay phát âm, sau đó chạy preview xuất nhanh bản nháp 30 giây.
> Bước bốn: khi mọi thứ đã ưng ý, bạn gõ đúng một lệnh render để máy tự động hoàn tất toàn bộ video và đóng logo.
> Không cần gọi API tốn phí, không phải chờ thao tác trung gian, mọi thứ hoàn toàn nằm trong tầm kiểm soát của bạn.

## Cảnh 6: Thực hành bộ lệnh Terminal cốt lõi [hieu_ung: code]
- mô_tả: Chỉ cần nhớ 3 lệnh chính check, preview, render cùng các cờ mở rộng cực tiện lợi
```powershell
# 1. Quet thu muc img/ tao anh luoi danh so de tra cuu nhanh
python D:\Edit\Kit\tools\build.py scan Baigiang_Moi

# 2. Kiem tra content.md, doi chieu anh thieu va xem phien am
python D:\Edit\Kit\tools\build.py check Baigiang_Moi

# 3. Xuat nhanh ban mau 30 giay (hoac sua rieng 1 canh --scene)
python D:\Edit\Kit\tools\build.py preview Baigiang_Moi --scene s02

# 4. Xuat video FULL + tu dong chuan -14 LUFS + dong logo + QA
python D:\Edit\Kit\tools\build.py render Baigiang_Moi --theme dark_cyan
```
> Bây giờ hãy nhìn trực tiếp vào bốn câu lệnh ngắn gọn trên cửa sổ PowerShell này.
> Đầu tiên, lệnh scan giúp gom toàn bộ ảnh trong thư mục img/ thành một tấm ảnh lưới có đánh số sẵn để bạn tra cứu cực nhanh.
> Tiếp theo, lệnh check phân tích file content.md trong một giây, báo ngay nếu có ảnh nào bị thiếu hoặc ảnh nào chưa dùng tới.
> Lệnh preview giúp bạn xem trước ba mươi giây đầu tiên, đặc biệt khi thêm cờ scene s02, máy chỉ dựng lại đúng cảnh số hai trong vài giây.
> Cuối cùng, lệnh render kích hoạt toàn bộ dây chuyền sản xuất, tự động đánh số phiên bản mới mà không bao giờ ghi đè bản cũ.
> Trong suốt quá trình chạy, Terminal luôn in rõ tiến độ từng bước từ một đến sáu để bạn dễ dàng theo dõi.

## Cảnh 7: Sức mạnh Render đa nhân và Đổi màu linh hoạt [hieu_ung: anh_dong]
- mô_tả: Tận dụng tối đa CPU đa nhân, bộ nhớ Cache thông minh và hệ thống Theme đổi màu tức thì
- ảnh: 5.jpg | Render đa nhân CPU kết hợp 8 hiệu ứng chuyển động mượt mà
- ảnh: 6.jpg | Đổi toàn bộ giao diện màu sắc tức thì qua file standard_2_3.json
> Điều làm nên sự khác biệt của hệ thống này nằm ở tốc độ xử lý và khả năng tùy biến giao diện cực kỳ linh hoạt.
> Nhờ cơ chế Cache giọng đọc thông minh, nếu bạn sửa màu sắc hay chỉnh sửa bố cục một cảnh, máy sẽ giữ nguyên file âm thanh cũ.
> Quá trình vẽ khung hình được chia đều cho nhiều nhân CPU chạy song song, giúp dựng hàng nghìn khung hình Full HD rất nhanh chóng.
> Các bức ảnh minh họa trong img/ đều được áp dụng chuyển động thu phóng mượt mà kết hợp khung kính hiện đại thay vì dán ảnh tĩnh.
> Đặc biệt, khi muốn đổi phong cách màu sắc cho các video mới, bạn chỉ cần sửa mã màu trong file standard_2_3.json.
> Hoặc chỉ cần thêm cờ theme dark_purple hay midnight_emerald trên Terminal là toàn bộ video tự khoác lên diện mạo mới ngay lập tức.

## Cảnh 8: Các thông số kiểm định chuẩn phát sóng [hieu_ung: dem_so]
- mô_tả: Mọi video xuất ra đều trải qua bước QA tự động cuối cùng trước khi bàn giao
- 100% | Vận hành Offline hoàn toàn trên máy
- 0đ | Chi phí API key định kỳ hàng tháng
- 8 | Mẫu hiệu ứng Animation sáng tạo sẵn có
- -14 LUFS | Chuẩn âm lượng phát sóng tự động
> Ở bước cuối cùng của tiến trình, hệ thống tự động thực hiện kiểm định chất lượng theo đúng tiêu chuẩn MASTER 2.3.
> Hệ thống hoạt động 100% offline trên máy tính cá nhân với chi phí API key bằng không đồng.
> Kho giao diện tích hợp sẵn 8 mẫu hiệu ứng chuyển động đa dạng: từ mở đầu, va chạm, so sánh, gõ code đến bảng đếm số liệu.
> Toàn bộ âm thanh giọng nói cùng hiệu ứng SFX tổng hợp được chuẩn hóa hai lượt về đúng mức âm 14 LUFS và đỉnh âm chuẩn phát sóng.
> Khi kết thúc, màn hình Terminal in ra bảng kết quả chi tiết từng hạng mục Đạt hay Cần sửa kèm đường dẫn trực tiếp tới file video.
> Bạn cũng nhận được bộ ảnh stills đại diện cho từng cảnh để liếc nhanh bố cục chỉ trong vài giây.

## Cảnh 9: Sẵn sàng tự chủ sản xuất bài giảng [hieu_ung: outro]
- mô_tả: Ba nguyên tắc vàng giúp bạn vận hành hệ thống trơn tru cho hàng trăm bài giảng tiếp theo
- Soạn chuẩn cú pháp | Dùng Prompt mẫu tạo content.md và đặt tên ảnh khớp 100%
- Kiểm tra trước khi xuất | Luôn chạy lệnh check và preview để tinh chỉnh nhanh
- Nâng cấp ngay trong Kit | Chỉnh màu, thêm phát âm hay hiệu ứng tại một nơi duy nhất
> Như vậy là bạn đã nắm trọn toàn bộ cách vận hành hệ thống sản xuất video bài giảng tự động trên Terminal.
> Hãy nhớ ba nguyên tắc vàng: soạn nội dung đúng cú pháp Markdown, luôn chạy lệnh check và preview trước khi xuất bản đầy đủ.
> Và bất cứ khi nào muốn nâng cấp giao diện hay thêm từ phát âm mới, bạn chỉ cần cập nhật đúng một chỗ trong thư mục Kit.
> Toàn bộ tài liệu hướng dẫn chi tiết cùng mẫu Prompt cho ChatGPT đã được lưu sẵn ngay trong thư mục dự án này.
> Cảm ơn các bạn đã theo dõi AN TECH ACADEMY! Đừng quên đăng ký kênh và hẹn gặp lại trong những bài giảng công nghệ thực chiến tiếp theo!
