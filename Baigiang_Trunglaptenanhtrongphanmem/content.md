An Tech Academy – Bài giảng: Xử lý trùng lặp tên file Avatar trong phần mềm

Chủ đề: Hai người dùng cùng có ảnh đại diện tên 1.jpg nhưng nội dung khác nhau. Làm thế nào để hệ thống lưu trữ, phân biệt và truy xuất đúng ảnh?



Công nghệ: HTML, CSS, PHP, MySQL

Thời lượng đề xuất: 15–20 phút

Đối tượng: Học viên đã biết cơ bản về lập trình web.

Học lập trình cùng An!



Mục tiêu bài học

Sau bài học, học viên có thể:

1\. Giải thích vì sao hai file cùng tên có thể gây ghi đè khi lưu trong cùng một thư mục.

2\. Phân biệt tên file, đường dẫn file, ID người dùng và nội dung file.

3\. Thiết kế cách lưu ảnh theo người dùng và tạo tên file mới.

4\. Tạo biểu mẫu HTML, định dạng giao diện bằng CSS.

5\. Dùng PHP tiếp nhận, kiểm tra và lưu file upload.

6\. Dùng MySQL lưu đường dẫn ảnh và truy xuất theo tài khoản.

7\. Nhận biết các vấn đề bảo mật cơ bản khi xử lý file upload.

1\. Dẫn nhập: Đặt vấn đề

Hãy tưởng tượng chúng ta đang xây dựng một phần mềm quản lý người dùng. User A tải lên ảnh đại diện có tên 1.jpg. User B cũng tải lên một ảnh có tên 1.jpg. Tuy nhiên, ảnh của A là ảnh chân dung, còn ảnh của B là ảnh một chú mèo. Hai file cùng tên nhưng nội dung hoàn toàn khác nhau.



Câu hỏi đặt ra: Làm thế nào để hệ thống biết ảnh nào thuộc về A, ảnh nào thuộc về B? Nếu lập trình viên chỉ dựa vào tên file để lưu và truy xuất, hệ thống có thể ghi đè file hoặc hiển thị nhầm ảnh.



Đây là tình huống phổ biến trong các website có chức năng đăng ký tài khoản, cập nhật hồ sơ, quản lý nhân sự, mạng xã hội và thương mại điện tử.

2\. Bản chất: Tên file không phải định danh duy nhất

2.1. File được xác định bằng tên và vị trí

Tên 1.jpg chỉ là tên file. Khi lưu trữ trong hệ thống file, vị trí của file cũng rất quan trọng.



Ví dụ:

D:/Website/UserA/1.jpg

D:/Website/UserB/1.jpg

Hai file có cùng tên nhưng nằm trong hai thư mục khác nhau, vì vậy chúng là hai đối tượng lưu trữ khác nhau.



Có thể hình dung thư mục như ngăn tủ, tên file như tên món đồ, đường dẫn như địa chỉ ngăn tủ và user\_id như mã nhận diện chủ sở hữu.



Nguyên tắc: Tên file có thể trùng nhau ở những thư mục khác nhau. Đường dẫn đầy đủ xác định vị trí của file.

2.2. Khi hai file cùng tên được lưu vào cùng thư mục

Giả sử dự án chỉ có một thư mục:

project/

└── uploads/

&#x20;   └── 1.jpg

Quá trình xảy ra:

1\. User A tải 1.jpg lên.

2\. PHP lưu file tại uploads/1.jpg.

3\. User B tải một file khác cũng tên 1.jpg.

4\. Chương trình tiếp tục lưu vào uploads/1.jpg.

5\. Nếu thao tác lưu cho phép thay thế file hiện có, ảnh A có thể bị ghi đè bởi ảnh B.



Vấn đề không phải là hai người dùng đặt tên giống nhau. Vấn đề là chương trình dùng cùng một vị trí lưu trữ cho hai file khác nhau.

3\. Thiết kế giải pháp

3.1. Tạo thư mục riêng theo ID người dùng

Thay vì lưu mọi ảnh vào một thư mục chung, có thể tổ chức:

uploads/

├── user\_101/

│   └── 1.jpg

└── user\_205/

&#x20;   └── 1.jpg

user\_101 là thư mục của tài khoản có ID 101; user\_205 là thư mục của tài khoản có ID 205. Hai file 1.jpg không xung đột vì nằm ở hai đường dẫn khác nhau.



Hạn chế: Nếu cùng một người tải lên nhiều file cùng tên vào thư mục của họ, file vẫn có thể bị ghi đè.

3.2. Tạo tên file duy nhất

Một cách phổ biến là không dùng tên gốc làm tên lưu trữ. Hệ thống tạo tên mới bằng UUID hoặc chuỗi ngẫu nhiên.

Người dùng	Tên gốc	Tên lưu trên máy chủ

A	1.jpg	a83f91c2.jpg

B	1.jpg	d71b42e9.jpg

C	1.jpg	f9216a37.jpg





Ví dụ cấu trúc kết hợp:

uploads/

├── user\_101/

│   └── a83f91c2d45e7890a12b34c56d78ef90.jpg

└── user\_205/

&#x20;   └── d71b42e9a12c34f567890abcdef12345.jpg

Khuyến nghị: Kết hợp thư mục theo user\_id với tên file ngẫu nhiên. Cách này giúp hạn chế xung đột tên và dễ quản lý dữ liệu.

4\. Thiết kế cơ sở dữ liệu MySQL

4.1. Phân biệt nơi lưu ảnh và nơi lưu thông tin

Có hai thành phần:

\- File storage: Lưu dữ liệu hình ảnh thực tế, ví dụ JPG, PNG, WEBP.

\- MySQL: Lưu thông tin người dùng và đường dẫn tới ảnh.

MySQL không nhất thiết phải lưu toàn bộ dữ liệu ảnh dưới dạng BLOB. Với avatar thông thường, có thể lưu file trên máy chủ và lưu đường dẫn trong cơ sở dữ liệu.



4.2. Tạo cơ sở dữ liệu và bảng users

CREATE DATABASE avatar\_demo

CHARACTER SET utf8mb4

COLLATE utf8mb4\_unicode\_ci;



USE avatar\_demo;



CREATE TABLE users (

&#x20;   id INT AUTO\_INCREMENT PRIMARY KEY,

&#x20;   username VARCHAR(100) NOT NULL,

&#x20;   avatar\_path VARCHAR(255) DEFAULT NULL

);

Giải thích:

\- id: Mã định danh duy nhất của người dùng.

\- username: Tên tài khoản.

\- avatar\_path: Đường dẫn ảnh đại diện.

Thêm dữ liệu mẫu:

INSERT INTO users (username)

VALUES ('user\_a'), ('user\_b');

MySQL tự tạo ID nhờ AUTO\_INCREMENT.

4.3. Lưu đường dẫn ảnh

Ví dụ User A có ID 1, ảnh được lưu tại:

uploads/user\_1/a83f91c2.jpg

Cập nhật cơ sở dữ liệu:

UPDATE users

SET avatar\_path = 'uploads/user\_1/a83f91c2.jpg'

WHERE id = 1;

User B có ID 2:

UPDATE users

SET avatar\_path = 'uploads/user\_2/d71b42e9.jpg'

WHERE id = 2;

Bảng dữ liệu lúc này có dạng:

id	username	avatar\_path

1	user\_a	uploads/user\_1/a83f91c2.jpg

2	user\_b	uploads/user\_2/d71b42e9.jpg





Điểm mấu chốt: MySQL lưu mối liên hệ giữa tài khoản và đường dẫn ảnh. PHP dùng ID để truy vấn đường dẫn tương ứng.

5\. Thực hành HTML, CSS và PHP

5.1. Cấu trúc dự án

avatar-demo/

├── uploads/

├── database.php

├── index.php

├── upload.php

└── style.css

\- uploads/: Thư mục lưu ảnh.

\- database.php: Kết nối MySQL bằng PDO.

\- index.php: Hiển thị tài khoản và biểu mẫu upload.

\- upload.php: Xử lý file tải lên.

\- style.css: Thiết kế giao diện.

5.2. Kết nối PHP với MySQL – database.php

<?php



$host = 'localhost';

$dbname = 'avatar\_demo';

$username = 'root';

$password = '';



try {

&#x20;   $pdo = new PDO(

&#x20;       "mysql:host=$host;dbname=$dbname;charset=utf8mb4",

&#x20;       $username,

&#x20;       $password

&#x20;   );



&#x20;   $pdo->setAttribute(

&#x20;       PDO::ATTR\_ERRMODE,

&#x20;       PDO::ERRMODE\_EXCEPTION

&#x20;   );



} catch (PDOException $e) {

&#x20;   exit("Không thể kết nối cơ sở dữ liệu!");

}

PDO (PHP Data Objects) là giao diện giúp PHP làm việc với cơ sở dữ liệu. Prepared Statements cho phép truyền dữ liệu vào câu truy vấn an toàn hơn, góp phần phòng tránh SQL Injection.

5.3. Tạo biểu mẫu HTML – index.php

<?php

session\_start();

require 'database.php';



// Chỉ dùng để minh họa trên máy cá nhân.

// Trong hệ thống thật, ID phải đến từ phiên đăng nhập đã xác thực.

if (!isset($\_SESSION\['user\_id'])) {

&#x20;   $\_SESSION\['user\_id'] = 1;

}



$userId = $\_SESSION\['user\_id'];



$stmt = $pdo->prepare(

&#x20;   "SELECT \* FROM users WHERE id = ?"

);

$stmt->execute(\[$userId]);

$user = $stmt->fetch(PDO::FETCH\_ASSOC);

?>



<!DOCTYPE html>

<html lang="vi">

<head>

&#x20;   <meta charset="UTF-8">

&#x20;   <title>Quản lý Avatar</title>

&#x20;   <link rel="stylesheet" href="style.css">

</head>

<body>

<div class="container">

&#x20;   <h2>Thông tin tài khoản</h2>



&#x20;   <?php if ($user): ?>

&#x20;       <?php if ($user\['avatar\_path']): ?>

&#x20;           <img

&#x20;               src="<?= htmlspecialchars(

&#x20;                   $user\['avatar\_path'],

&#x20;                   ENT\_QUOTES,

&#x20;                   'UTF-8'

&#x20;               ) ?>"

&#x20;               class="avatar"

&#x20;               alt="Ảnh đại diện"

&#x20;           >

&#x20;       <?php else: ?>

&#x20;           <div class="no-avatar">

&#x20;               Chưa có ảnh đại diện

&#x20;           </div>

&#x20;       <?php endif; ?>



&#x20;       <h3>

&#x20;           <?= htmlspecialchars($user\['username']) ?>

&#x20;       </h3>



&#x20;       <form

&#x20;           action="upload.php"

&#x20;           method="POST"

&#x20;           enctype="multipart/form-data"

&#x20;       >

&#x20;           <input

&#x20;               type="file"

&#x20;               name="avatar"

&#x20;               accept="image/jpeg,image/png,image/webp"

&#x20;               required

&#x20;           >

&#x20;           <button type="submit">Cập nhật ảnh</button>

&#x20;       </form>

&#x20;   <?php endif; ?>

</div>

</body>

</html>

Giải thích các thuộc tính quan trọng:

\- action="upload.php": Gửi dữ liệu đến file PHP xử lý.

\- method="POST": Gửi dữ liệu bằng phương thức POST.

\- enctype="multipart/form-data": Cho phép gửi dữ liệu file.

\- type="file": Cho phép chọn file từ thiết bị.

\- name="avatar": Tên trường mà PHP dùng để nhận file trong $\_FILES\['avatar'].

Nếu thiếu multipart/form-data, biểu mẫu sẽ không gửi file theo cách upload thông thường.

5.4. Thiết kế CSS – style.css

\* {

&#x20;   box-sizing: border-box;

}



body {

&#x20;   font-family: Arial, sans-serif;

&#x20;   background: #f1f5f9;

&#x20;   margin: 0;

&#x20;   padding: 40px 20px;

}



.container {

&#x20;   max-width: 450px;

&#x20;   margin: auto;

&#x20;   padding: 30px;

&#x20;   text-align: center;

&#x20;   background: white;

&#x20;   border-radius: 16px;

&#x20;   box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);

}



.avatar {

&#x20;   width: 140px;

&#x20;   height: 140px;

&#x20;   border-radius: 50%;

&#x20;   object-fit: cover;

&#x20;   border: 4px solid #2563eb;

}



.no-avatar {

&#x20;   padding: 50px 10px;

&#x20;   background: #e2e8f0;

&#x20;   border-radius: 50%;

}



input {

&#x20;   display: block;

&#x20;   width: 100%;

&#x20;   margin: 20px 0;

}



button {

&#x20;   padding: 12px 25px;

&#x20;   border: none;

&#x20;   border-radius: 8px;

&#x20;   color: white;

&#x20;   background: #2563eb;

&#x20;   cursor: pointer;

}



button:hover {

&#x20;   background: #1d4ed8;

}

border-radius: 50% tạo khung hình tròn. object-fit: cover giúp ảnh lấp đầy khung mà không bị kéo méo tỷ lệ. Ảnh có thể bị cắt bớt phần rìa để vừa khung.

5.5. Xử lý upload bằng PHP – upload.php

Bước 1: Xác định người dùng đang đăng nhập.

<?php

session\_start();

require 'database.php';



$userId = $\_SESSION\['user\_id'] ?? null;



if (!$userId) {

&#x20;   exit("Bạn chưa đăng nhập!");

}

Session giúp duy trì trạng thái đăng nhập giữa các yêu cầu. Trong thực tế, không được lấy ID chủ sở hữu từ dữ liệu do trình duyệt tự gửi lên mà không xác thực. Người dùng có thể sửa dữ liệu gửi lên. ID phải được lấy từ phiên đăng nhập đã được máy chủ xác thực.



Bước 2: Kiểm tra file được gửi lên.

if (

&#x20;   !isset($\_FILES\['avatar']) ||

&#x20;   $\_FILES\['avatar']\['error'] !== UPLOAD\_ERR\_OK

) {

&#x20;   exit("Upload thất bại!");

}



$file = $\_FILES\['avatar'];

PHP cung cấp biến toàn cục $\_FILES để chứa thông tin file upload.

Thuộc tính	Ý nghĩa

name	Tên file gốc do người dùng gửi

type	MIME type do trình duyệt cung cấp, không nên tin cậy tuyệt đối

tmp\_name	Đường dẫn file tạm trên máy chủ

error	Mã trạng thái upload

size	Dung lượng file tính bằng byte





Bước 3: Kiểm tra dung lượng.

if ($file\['size'] > 5 \* 1024 \* 1024) {

&#x20;   exit("Ảnh vượt quá giới hạn 5 MiB!");

}

Giới hạn dung lượng giúp giảm nguy cơ người dùng tải lên file quá lớn, gây tốn dung lượng và tài nguyên máy chủ. Ngoài kiểm tra trong code, cần cấu hình upload\_max\_filesize và post\_max\_size trong PHP.



Bước 4: Kiểm tra MIME type thực tế.

$finfo = new finfo(FILEINFO\_MIME\_TYPE);

$mime = $finfo->file($file\['tmp\_name']);



$allowed = \[

&#x20;   'image/jpeg' => 'jpg',

&#x20;   'image/png'  => 'png',

&#x20;   'image/webp' => 'webp'

];



if (!isset($allowed\[$mime])) {

&#x20;   exit("Định dạng ảnh không hợp lệ!");

}



if (@getimagesize($file\['tmp\_name']) === false) {

&#x20;   exit("Nội dung file không phải ảnh hợp lệ!");

}

Không nên chỉ dựa vào đuôi .jpg hoặc thuộc tính accept của HTML. Người dùng có thể đổi tên một file không phải ảnh thành hinh.jpg. Vì vậy, máy chủ cần kiểm tra nội dung thực tế. finfo xác định MIME type dựa trên nội dung file; getimagesize() bổ sung bước kiểm tra khả năng nhận diện ảnh.



Bước 5: Tạo tên file mới.

$newName = bin2hex(random\_bytes(16))

&#x20;        . '.' . $allowed\[$mime];

random\_bytes(16) tạo 16 byte ngẫu nhiên. bin2hex() chuyển chúng thành chuỗi hexadecimal. Kết quả là tên file mới, không phụ thuộc tên gốc người dùng gửi lên.



Bước 6: Tạo thư mục riêng theo user\_id.

$folder = \_\_DIR\_\_ . "/uploads/user\_" . $userId . "/";



if (!is\_dir($folder) \&\&

&#x20;   !mkdir($folder, 0755, true)) {

&#x20;   exit("Không thể tạo thư mục!");

}

\_\_DIR\_\_ là đường dẫn thư mục chứa file PHP hiện tại. is\_dir() kiểm tra thư mục đã tồn tại chưa. mkdir() tạo thư mục nếu cần. Quyền 0755 là quyền truy cập thường dùng trên hệ thống Unix/Linux; cần điều chỉnh theo môi trường triển khai.



Bước 7: Di chuyển file vào vị trí chính thức.

$path = $folder . $newName;



if (!move\_uploaded\_file($file\['tmp\_name'], $path)) {

&#x20;   exit("Không thể lưu file!");

}

PHP thường nhận file vào thư mục tạm trước. move\_uploaded\_file() chuyển file upload hợp lệ từ vị trí tạm đến thư mục lưu trữ của ứng dụng.



Bước 8: Lưu đường dẫn vào MySQL.

$relativePath =

&#x20;   "uploads/user\_" . $userId . "/" . $newName;



$stmt = $pdo->prepare(

&#x20;   "UPDATE users

&#x20;    SET avatar\_path = ?

&#x20;    WHERE id = ?"

);



$stmt->execute(\[$relativePath, $userId]);



echo "Cập nhật ảnh đại diện thành công!";

avatar\_path lưu đường dẫn tương đối để ứng dụng có thể truy xuất ảnh. WHERE id = ? đảm bảo cập nhật đúng tài khoản đã xác định. Prepared Statement giúp truyền tham số an toàn hơn.

5.6. File upload.php hoàn chỉnh

<?php

session\_start();

require 'database.php';



// 1. Xác định người dùng

$userId = $\_SESSION\['user\_id'] ?? null;



if (!$userId) {

&#x20;   exit("Bạn chưa đăng nhập!");

}



// 2. Kiểm tra file upload

if (

&#x20;   !isset($\_FILES\['avatar']) ||

&#x20;   $\_FILES\['avatar']\['error'] !== UPLOAD\_ERR\_OK

) {

&#x20;   exit("Upload thất bại!");

}



$file = $\_FILES\['avatar'];



// 3. Kiểm tra dung lượng

if ($file\['size'] > 5 \* 1024 \* 1024) {

&#x20;   exit("Ảnh vượt quá 5 MiB!");

}



// 4. Kiểm tra MIME type

$finfo = new finfo(FILEINFO\_MIME\_TYPE);

$mime = $finfo->file($file\['tmp\_name']);



$allowed = \[

&#x20;   'image/jpeg' => 'jpg',

&#x20;   'image/png'  => 'png',

&#x20;   'image/webp' => 'webp'

];



if (!isset($allowed\[$mime])) {

&#x20;   exit("Định dạng ảnh không hợp lệ!");

}



if (@getimagesize($file\['tmp\_name']) === false) {

&#x20;   exit("Nội dung file không phải ảnh hợp lệ!");

}



// 5. Tạo tên file duy nhất

$newName = bin2hex(random\_bytes(16))

&#x20;        . '.' . $allowed\[$mime];



// 6. Tạo thư mục theo user\_id

$folder = \_\_DIR\_\_ . "/uploads/user\_" . $userId . "/";



if (!is\_dir($folder) \&\&

&#x20;   !mkdir($folder, 0755, true)) {

&#x20;   exit("Không thể tạo thư mục!");

}



// 7. Di chuyển file

$path = $folder . $newName;



if (!move\_uploaded\_file($file\['tmp\_name'], $path)) {

&#x20;   exit("Không thể lưu file!");

}



// 8. Lưu đường dẫn vào MySQL

$relativePath =

&#x20;   "uploads/user\_" . $userId . "/" . $newName;



try {

&#x20;   $stmt = $pdo->prepare(

&#x20;       "UPDATE users

&#x20;        SET avatar\_path = ?

&#x20;        WHERE id = ?"

&#x20;   );



&#x20;   $stmt->execute(\[$relativePath, $userId]);



&#x20;   echo "Cập nhật ảnh thành công!";



} catch (PDOException $e) {

&#x20;   if (is\_file($path)) {

&#x20;       unlink($path);

&#x20;   }



&#x20;   exit("Không thể cập nhật dữ liệu!");

}

Đây là mã thực hành minh họa. Khi triển khai thực tế cần bổ sung CSRF token, giới hạn chiều rộng và chiều cao ảnh, xử lý ảnh cũ, ghi log lỗi ở phía máy chủ và cấu hình thư mục upload không cho thực thi mã PHP. Cũng cần có cơ chế xử lý trường hợp lưu file thành công nhưng cập nhật database thất bại.

6\. Truy xuất đúng ảnh đại diện

Đây là phần cốt lõi của bài học. Lưu được file chưa có nghĩa là hệ thống biết phải hiển thị file nào.



Khi User A đăng nhập với ID 1, PHP truy vấn:

SELECT avatar\_path

FROM users

WHERE id = 1;

MySQL trả về:

uploads/user\_1/a83f91c2.jpg

Khi User B đăng nhập với ID 2:

SELECT avatar\_path

FROM users

WHERE id = 2;

MySQL trả về:

uploads/user\_2/d71b42e9.jpg



Cần hiểu rõ hai công việc:

1\. PHP truy vấn MySQL để lấy đường dẫn ảnh của người dùng.

2\. Trình duyệt gửi yêu cầu HTTP đến đường dẫn đó để tải ảnh về và hiển thị.

MySQL không tự đi tìm file ảnh trong thư mục. PHP lấy đường dẫn từ MySQL; trình duyệt dùng đường dẫn để tải tài nguyên từ máy chủ.

7\. Phân biệt trùng tên file và trùng nội dung file

Hai file cùng tên chưa chắc có nội dung giống nhau. Ngược lại, hai file khác tên vẫn có thể chứa dữ liệu byte giống hệt nhau.



Ví dụ:

1.jpg

avatar.png

photo.webp

Nếu muốn kiểm tra hai file có dữ liệu byte giống hệt nhau không, có thể dùng SHA-256:

$hashA = hash\_file('sha256', 'uploads/1.jpg');

$hashB = hash\_file('sha256', 'uploads/avatar.png');



if ($hashA === $hashB) {

&#x20;   echo "Hai file có dữ liệu giống hệt nhau!";

} else {

&#x20;   echo "Hai file có dữ liệu khác nhau!";

}

SHA-256 tạo ra một giá trị băm đại diện cho dữ liệu đầu vào. Nếu hai file có nội dung byte giống hệt nhau thì giá trị băm giống nhau. Tuy nhiên, hai ảnh nhìn giống nhau nhưng được nén, đổi kích thước hoặc chuyển định dạng có thể có hash khác nhau.



Muốn phát hiện ảnh gần giống nhau về mặt thị giác, có thể tìm hiểu perceptual hashing (pHash, aHash, dHash) hoặc kỹ thuật xử lý ảnh. Đây là bài toán khác với trùng tên file.



8\. Những sai lầm cần tránh

Sai lầm	Hậu quả

Lưu mọi ảnh bằng tên gốc vào cùng thư mục	Có thể ghi đè file

Chỉ lưu tên file trong MySQL	Không đủ thông tin xác định vị trí

Chỉ tin vào đuôi JPG	Có thể nhận file giả dạng ảnh

Lấy user\_id từ dữ liệu gửi lên mà không xác thực	Có thể cập nhật ảnh của người khác

Không giới hạn dung lượng	Tốn tài nguyên máy chủ

Không xử lý ảnh cũ	Tăng dung lượng lưu trữ

Nghĩ tên ngẫu nhiên đồng nghĩa với bảo mật	File vẫn có thể bị truy cập nếu đường dẫn công khai bị lộ





Đối với tài liệu cá nhân hoặc ảnh nhạy cảm, nên lưu file ngoài thư mục công khai và cho tải thông qua endpoint PHP có kiểm tra quyền truy cập. Tên file ngẫu nhiên không thay thế cho cơ chế phân quyền.

9\. Ứng dụng thực tế

\- Mạng xã hội: Quản lý avatar và ảnh người dùng.

\- Quản lý nhân sự: Lưu ảnh hồ sơ nhân viên.

\- Thương mại điện tử: Quản lý ảnh sản phẩm của nhiều nhà bán hàng.

\- Giáo dục: Lưu ảnh học viên, giáo viên và nhân viên.

Trong hệ thống lớn, có thể sử dụng dịch vụ lưu trữ bên ngoài như Amazon S3 hoặc Cloudinary. Nguyên tắc định danh chủ sở hữu và lưu thông tin đường dẫn hoặc khóa đối tượng trong cơ sở dữ liệu vẫn được áp dụng.

10\. Tổng kết

Có ba điều học viên cần ghi nhớ:

1\. Tránh ghi đè: Dùng thư mục riêng và tên file lưu trữ duy nhất.

2\. Xác định chủ sở hữu: Dùng user\_id để liên kết tài khoản với file.

3\. Truy xuất chính xác: Lưu avatar\_path trong MySQL và truy vấn theo ID người dùng đã xác thực.

Tên file không đồng nghĩa với định danh của file. Một hệ thống tốt phải tổ chức dữ liệu khoa học, quản lý đúng chủ sở hữu và truy xuất đúng tài nguyên.

11\. Bài tập thực hành

Đề bài: Xây dựng website quản lý ảnh đại diện cho ít nhất 3 tài khoản.



Yêu cầu:

1\. Tạo bảng users trong MySQL.

2\. Mỗi tài khoản có ID riêng.

3\. Cho phép người dùng tải ảnh đại diện.

4\. Tự động tạo tên file mới.

5\. Tạo thư mục riêng theo người dùng.

6\. Lưu đường dẫn ảnh vào MySQL.

7\. Khi đăng nhập, hiển thị đúng ảnh.

8\. Thử cho cả ba tài khoản tải lên file cùng tên 1.jpg.

Câu hỏi tư duy:

\- Nếu 1.000 người dùng cùng tải lên 1.jpg, hệ thống xử lý như thế nào?

\- Nếu một người thay đổi ảnh đại diện 10 lần, file cũ cần được xử lý ra sao?

\- Nếu người dùng cố thay đổi user\_id trong yêu cầu upload, hệ thống có bị ảnh hưởng không?

\- Nếu hai file có tên khác nhau nhưng nội dung byte giống hệt nhau, làm thế nào để phát hiện?

12\. Lời kết video

Vậy là trong bài học hôm nay, chúng ta đã tìm hiểu cách xử lý vấn đề trùng lặp tên file trong phần mềm, từ nguyên nhân, cách tổ chức thư mục, thiết kế cơ sở dữ liệu cho đến thực hành bằng HTML, CSS, PHP và MySQL.



Hy vọng sau bài học này, các bạn không chỉ biết cách viết một chức năng upload hình ảnh mà còn hiểu được cách một hệ thống thực sự quản lý và truy xuất dữ liệu.



Cảm ơn các bạn đã theo dõi bài giảng. Hẹn gặp lại các bạn trong những bài học tiếp theo tại An Tech Academy – Cùng bạn chinh phục công nghệ!

Gợi ý phân cảnh video

Cảnh	Nội dung	Hình thức

1	Giới thiệu vấn đề	Hai avatar cùng tên 1.jpg

2	Bản chất tên file	Minh họa hai thư mục

3	Lỗi ghi đè	Mô phỏng upload

4	Giải pháp	Sơ đồ thư mục theo user\_id

5	MySQL	Minh họa bảng dữ liệu

6	HTML/CSS	Quay màn hình viết giao diện

7	PHP	Giải thích từng công đoạn code

8	Truy xuất	PHP → MySQL → ảnh

9	SHA-256	So sánh dữ liệu file

10	Tổng kết	Sơ đồ toàn hệ thống





Định hướng giảng dạy: Không đọc code liên tục. Hãy cho học viên thấy vấn đề, dự đoán lỗi, giải thích nguyên nhân, sau đó mới viết code để khắc phục. Trọng tâm là mối quan hệ giữa user\_id, file\_path, hệ thống file và MySQL.

