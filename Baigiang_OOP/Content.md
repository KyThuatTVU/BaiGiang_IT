BÀI GIẢNG: LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP) VỚI JAVA

An Tech Academy

&#x20;Thời lượng: 5–7 phút

&#x20;Ngôn ngữ: Java

10

1\. Mở đầu – Giới thiệu bài học

Học lập trình cùng An!



Xin chào các bạn, chào mừng các bạn đã quay trở lại với An Tech Academy.



Trong lập trình, khi xây dựng một phần mềm, chúng ta không chỉ quan tâm đến việc viết code sao cho chương trình chạy được, mà còn phải tổ chức mã nguồn như thế nào để dễ quản lý, dễ mở rộng và dễ bảo trì.



Và đó chính là lý do chúng ta cần tìm hiểu về lập trình hướng đối tượng, hay còn gọi là OOP – Object-Oriented Programming.



Trong bài học hôm nay, chúng ta sẽ tìm hiểu khái niệm OOP, bốn tính chất quan trọng nhất, thông qua ngôn ngữ Java, đồng thời khám phá cách OOP được ứng dụng trong những dự án phần mềm thực tế.

2\. Lập trình hướng đối tượng là gì?

medium.com

Các bạn hãy tưởng tượng chúng ta đang xây dựng một phần mềm quản lý sinh viên.



Mỗi sinh viên sẽ có những thông tin như: mã sinh viên, họ tên, tuổi, email. Đồng thời, sinh viên cũng có những hành động như đăng ký môn học, xem điểm và cập nhật thông tin.



Thay vì viết tất cả dữ liệu và chức năng một cách rời rạc, lập trình hướng đối tượng cho phép chúng ta gom những thông tin và hành động có liên quan vào một đối tượng.



Trong Java, chúng ta có hai khái niệm quan trọng:

\- Class – Lớp: Là bản thiết kế để tạo ra các đối tượng.

\- Object – Đối tượng: Là một thực thể cụ thể được tạo ra từ lớp.

Ví dụ:

class SinhVien {

&#x20;   String hoTen;

&#x20;   int tuoi;



&#x20;   void hienThiThongTin() {

&#x20;       System.out.println(hoTen + " - " + tuoi);

&#x20;   }

}



public class Main {

&#x20;   public static void main(String\[] args) {

&#x20;       SinhVien sv = new SinhVien();



&#x20;       sv.hoTen = "Nguyen Van An";

&#x20;       sv.tuoi = 20;



&#x20;       sv.hienThiThongTin();

&#x20;   }

}





Ở đây, SinhVien là lớp, còn sv là một đối tượng được tạo ra từ lớp đó.



Đây chính là nền tảng đầu tiên của lập trình hướng đối tượng.

3\. Bốn tính chất quan trọng của OOP

Đây là nội dung trọng tâm của bài học. Lập trình hướng đối tượng có bốn tính chất cơ bản: Đóng gói, Kế thừa, Đa hình và Trừu tượng.

Tính chất 1: Đóng gói (Encapsulation)







docs.telusko.com





Đóng gói có nghĩa là chúng ta bảo vệ dữ liệu bên trong đối tượng, không cho phép bên ngoài truy cập và thay đổi tùy ý.



Ví dụ, trong phần mềm quản lý ngân hàng, số dư tài khoản không nên được thay đổi trực tiếp từ bên ngoài.



Java minh họa:

class TaiKhoan {

&#x20;   private double soDu;



&#x20;   public void napTien(double tien) {

&#x20;       if (tien > 0) {

&#x20;           soDu += tien;

&#x20;       }

&#x20;   }



&#x20;   public double getSoDu() {

&#x20;       return soDu;

&#x20;   }

}





Ở đây, private giúp bảo vệ số dư tài khoản. Muốn thay đổi số dư, chúng ta phải thông qua phương thức napTien().



Ý nghĩa: Đảm bảo dữ liệu an toàn, hạn chế sai sót và kiểm soát cách truy cập dữ liệu.

Tính chất 2: Kế thừa (Inheritance)





docs.telusko.com





Kế thừa cho phép một lớp con sử dụng lại những thuộc tính và phương thức của lớp cha.



Ví dụ, trong một hệ thống quản lý nhân sự, chúng ta có lớp NhanVien. Từ lớp này, có thể tạo ra các lớp NhanVienFullTime và NhanVienPartTime.



Java minh họa:

class NhanVien {

&#x20;   String hoTen;



&#x20;   void lamViec() {

&#x20;       System.out.println("Nhan vien dang lam viec");

&#x20;   }

}



class NhanVienIT extends NhanVien {

&#x20;   void lapTrinh() {

&#x20;       System.out.println("Dang lap trinh Java");

&#x20;   }

}





Ở đây, NhanVienIT kế thừa từ NhanVien thông qua từ khóa extends.



Nhờ vậy, lớp nhân viên IT có thể sử dụng thuộc tính hoTen và phương thức lamViec() mà không cần viết lại.



Ý nghĩa: Tái sử dụng mã nguồn, giảm trùng lặp và dễ mở rộng hệ thống.

Tính chất 3: Đa hình (Polymorphism)





medium.com





Đa hình có nghĩa là cùng một phương thức nhưng có thể thể hiện những hành vi khác nhau tùy theo đối tượng.



Ví dụ, chúng ta có nhiều loại nhân viên. Khi gọi phương thức tinhLuong(), mỗi loại nhân viên sẽ có cách tính lương riêng.



Java minh họa:

class NhanVien {

&#x20;   void tinhLuong() {

&#x20;       System.out.println("Tinh luong nhan vien");

&#x20;   }

}



class NhanVienFullTime extends NhanVien {

&#x20;   @Override

&#x20;   void tinhLuong() {

&#x20;       System.out.println("Luong co dinh hang thang");

&#x20;   }

}



class NhanVienPartTime extends NhanVien {

&#x20;   @Override

&#x20;   void tinhLuong() {

&#x20;       System.out.println("Luong tinh theo gio");

&#x20;   }

}





Ở đây, cả hai lớp đều có phương thức tinhLuong(), nhưng cách thực hiện hoàn toàn khác nhau.



Đây là ví dụ về ghi đè phương thức – Method Overriding.



Ý nghĩa: Giúp chương trình linh hoạt, dễ mở rộng và xử lý nhiều loại đối tượng thông qua cùng một cách gọi.

Tính chất 4: Trừu tượng (Abstraction)







newsletter.francofernando.com





Trừu tượng là việc tập trung vào những chức năng cần thiết và ẩn đi cách thức triển khai phức tạp bên trong.



Ví dụ, khi thanh toán trực tuyến, người dùng chỉ cần chọn phương thức thanh toán và thực hiện giao dịch. Họ không cần biết hệ thống xử lý kết nối ngân hàng như thế nào.



Java minh họa:

interface ThanhToan {

&#x20;   void thanhToan(double soTien);

}



class ThanhToanMoMo implements ThanhToan {

&#x20;   public void thanhToan(double soTien) {

&#x20;       System.out.println("Thanh toan qua MoMo");

&#x20;   }

}



class ThanhToanThe implements ThanhToan {

&#x20;   public void thanhToan(double soTien) {

&#x20;       System.out.println("Thanh toan bang the");

&#x20;   }

}





Ở đây, ThanhToan định nghĩa chức năng chung, còn từng lớp sẽ triển khai cách thanh toán riêng.



Ý nghĩa: Giảm sự phức tạp, tách biệt chức năng và cách triển khai, giúp hệ thống dễ thay đổi.

4\. Ứng dụng OOP trong các dự án thực tế





7





Vậy lập trình hướng đối tượng được ứng dụng như thế nào trong những dự án thực tế?



Thực tế, OOP được sử dụng rất rộng rãi trong quá trình phát triển phần mềm.



Thứ nhất – Hệ thống quản lý nhà hàng.



Chúng ta có thể xây dựng các lớp như MonAn, BanAn, NhanVien, HoaDon, KhachHang. Mỗi lớp quản lý dữ liệu và chức năng riêng. Tính kế thừa và đa hình có thể hỗ trợ quản lý nhiều loại nhân viên hoặc phương thức thanh toán.



Thứ hai – Website thương mại điện tử.



Có thể xây dựng các lớp SanPham, KhachHang, GioHang, DonHang. Đóng gói giúp bảo vệ thông tin đơn hàng, còn trừu tượng giúp xây dựng nhiều phương thức thanh toán khác nhau.



Thứ ba – Hệ thống quản lý bệnh viện.



Các lớp như BenhNhan, BacSi, LichKham, DonThuoc giúp tổ chức dữ liệu rõ ràng, dễ quản lý và mở rộng.



Thứ tư – Ứng dụng ngân hàng.



Các đối tượng như TaiKhoan, GiaoDich, KhachHang giúp quản lý thông tin và nghiệp vụ tài chính một cách có tổ chức.



Điều quan trọng cần nhớ là OOP không chỉ dành riêng cho Java. Nó còn được ứng dụng trong nhiều ngôn ngữ như C++, C#, Python, PHP và nhiều công nghệ phát triển phần mềm khác.

5\. Tổng kết bài học



ibm.com



Như vậy, trong bài học hôm nay, chúng ta đã tìm hiểu những kiến thức quan trọng nhất của lập trình hướng đối tượng.



Hãy ghi nhớ bốn tính chất:

1\. Đóng gói: Bảo vệ dữ liệu.

2\. Kế thừa: Tái sử dụng mã nguồn.

3\. Đa hình: Một phương thức, nhiều cách thực hiện.

4\. Trừu tượng: Ẩn đi sự phức tạp, tập trung vào chức năng cần thiết.

OOP không đơn thuần là một cách viết code, mà còn là tư duy thiết kế phần mềm. Khi nắm vững những nguyên tắc này, các bạn sẽ có nền tảng tốt hơn để xây dựng những dự án lớn, chuyên nghiệp và dễ bảo trì.



Cảm ơn các bạn đã theo dõi bài giảng của An Tech Academy. Hẹn gặp lại các bạn trong những bài học lập trình tiếp theo!

