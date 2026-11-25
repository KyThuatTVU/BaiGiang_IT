BÀI GIẢNG: TÍCH HỢP API THANH TOÁN NGÂN HÀNG VÀO HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ

AN TECH ACADEMY · LẬP TRÌNH BACKEND · API INTEGRATION













































14





























Chủ đề: Doanh nghiệp kết nối hệ thống bán hàng với ngân hàng để tự động hóa quy trình thanh toán, xác nhận giao dịch và cập nhật trạng thái đơn hàng.



Mục tiêu bài học: Sau bài này, người học hiểu được cách ngân hàng cung cấp API cho doanh nghiệp, cách website kết nối với ngân hàng, cách xử lý logic đơn hàng sau thanh toán và cách lập trình một quy trình thanh toán thực tế bằng Node.js, Express và MySQL.



PHẦN 1. NHẬN ĐỊNH: BẠN HIỂU ĐÚNG HAY CHƯA?

Tôi đánh giá nhận định của bạn đúng về bản chất, nhưng cần điều chỉnh một điểm quan trọng về quy trình cấp API của ngân hàng.



Bạn đang hình dung quy trình như sau:

1\. Doanh nghiệp đăng ký và mở tài khoản tại ngân hàng.

2\. Ngân hàng cấp API Key hoặc thông tin xác thực API cho doanh nghiệp.

3\. Lập trình viên sử dụng thông tin đó để kết nối website với ngân hàng.

4\. Khi khách hàng đặt hàng, hệ thống tạo giao dịch thanh toán.

5\. Ngân hàng xử lý giao dịch và phản hồi kết quả.

6\. Website căn cứ vào kết quả để cập nhật trạng thái đơn hàng.

Đây là mô hình tư duy đúng.



Tuy nhiên, cần phân biệt:



Mở tài khoản doanh nghiệp không đồng nghĩa với việc tự động được cấp API thanh toán.



Trên thực tế, tùy ngân hàng và dịch vụ đăng ký, doanh nghiệp có thể cần:

\- Có tài khoản thanh toán doanh nghiệp.

\- Đăng ký sử dụng dịch vụ API hoặc dịch vụ thanh toán trực tuyến.

\- Ký hợp đồng hoặc thỏa thuận cung cấp dịch vụ.

\- Hoàn thành quy trình xác minh doanh nghiệp.

\- Được ngân hàng cấp thông tin tích hợp môi trường thử nghiệm (Sandbox/UAT).

\- Hoàn thành kiểm thử và được phê duyệt sử dụng môi trường chính thức (Production).

Ngoài ra, không phải ngân hàng nào cũng chỉ cấp một chuỗi gọi là API Key. Có thể có Client ID, Client Secret, Access Token, khóa ký số, chứng thư số hoặc cơ chế xác thực khác.



Một điểm rất quan trọng: Ngân hàng không nên chỉ được gọi từ trình duyệt của khách hàng. Backend của doanh nghiệp mới là thành phần chịu trách nhiệm giao tiếp với ngân hàng và xác minh kết quả thanh toán.



Đây chính là nội dung chúng ta sẽ đi sâu trong bài học.

PHẦN 2. API NGÂN HÀNG LÀ GÌ? DOANH NGHIỆP SỬ DỤNG ĐỂ LÀM GÌ?

2.1. Khái niệm API ngân hàng

API ngân hàng (Banking API) là giao diện lập trình ứng dụng do ngân hàng cung cấp, cho phép các hệ thống phần mềm bên ngoài kết nối và sử dụng một số dịch vụ ngân hàng thông qua Internet.



Thay vì nhân viên phải đăng nhập vào Internet Banking để kiểm tra từng giao dịch, hệ thống phần mềm có thể tự động gửi yêu cầu đến ngân hàng, nhận dữ liệu phản hồi và thực hiện nghiệp vụ tương ứng.



Ví dụ, một doanh nghiệp kinh doanh điện thoại có website bán hàng. Khách hàng đặt mua một chiếc điện thoại trị giá 15.000.000 đồng.



Nếu chưa tích hợp API thanh toán:

\- Khách hàng chuyển khoản vào tài khoản ngân hàng của doanh nghiệp.

\- Nhân viên mở ứng dụng ngân hàng kiểm tra tiền vào.

\- Nhân viên đối chiếu nội dung chuyển khoản.

\- Nhân viên quay lại website xác nhận đơn hàng.

\- Bộ phận kho mới bắt đầu chuẩn bị giao hàng.

Nếu đã tích hợp API thanh toán:

\- Website tự động tạo yêu cầu thanh toán.

\- Khách hàng thực hiện chuyển khoản hoặc thanh toán trực tuyến.

\- Ngân hàng xử lý giao dịch.

\- Hệ thống nhận thông báo giao dịch thành công.

\- Backend xác minh giao dịch.

\- Website tự động cập nhật đơn hàng đã thanh toán.

Đây chính là giá trị lớn nhất của việc tích hợp API ngân hàng: Tự động hóa quy trình thanh toán và đồng bộ dữ liệu giữa ngân hàng với hệ thống doanh nghiệp.

2.2. Một số loại API ngân hàng thường gặp

Không phải API ngân hàng nào cũng có chức năng giống nhau. Khi triển khai dự án thực tế, lập trình viên cần phân biệt các nhóm sau:





















1\. Payment Gateway API – API cổng thanh toán



Cho phép website khởi tạo giao dịch thanh toán, chuyển khách hàng sang trang thanh toán hoặc ứng dụng ngân hàng và nhận kết quả giao dịch.



Ví dụ: thanh toán đơn hàng bằng thẻ, tài khoản hoặc QR.



























2\. QR Payment API – API thanh toán QR



Hỗ trợ tạo thông tin thanh toán hoặc mã QR gắn với số tiền và mã đơn hàng. Khách hàng dùng ứng dụng ngân hàng quét mã để thanh toán.



























3\. Transaction Notification API – API thông báo biến động số dư



Ngân hàng gửi thông tin giao dịch phát sinh vào tài khoản doanh nghiệp để hệ thống tự động ghi nhận và đối soát.



























4\. Virtual Account API – API tài khoản định danh



Hỗ trợ tạo hoặc sử dụng tài khoản định danh để nhận diện tiền khách hàng chuyển vào tương ứng với từng đơn hàng.



























5\. Transfer API – API chuyển tiền



Cho phép hệ thống gửi yêu cầu chuyển tiền hoặc chi hộ theo quyền hạn và quy trình xác thực được ngân hàng cấp.







Ví dụ thực tế: VietinBank Open API có các nhóm dịch vụ như chuyển tiền trong nước, thông báo biến động số dư, VietQR Pay và tài khoản định danh. BIDV cũng cung cấp gói Payment Gateway với các API khởi tạo và vấn tin giao dịch. 

API Portal+1





Lưu ý cho lập trình viên: Nếu mục tiêu của doanh nghiệp là tự động xác nhận khách hàng đã chuyển khoản thành công hay chưa, cần lựa chọn giải pháp có khả năng thông báo giao dịch hoặc đối soát giao dịch. Chỉ tạo được mã QR không có nghĩa là hệ thống đã biết khách hàng thanh toán thành công.



PHẦN 3. MÔ HÌNH HOẠT ĐỘNG THỰC TẾ – HÃY HÌNH DUNG MỘT ĐƠN HÀNG

3.1. Ví dụ: Khách hàng mua điện thoại trên website

Giả sử chúng ta xây dựng website bán điện thoại.



Khách hàng lựa chọn:





















Điện thoại thông minh



Sản phẩm: SP001

15.000.000 ₫

Thanh toán chuyển khoản







Mã đơn hàng



DH20261124001



Tổng thanh toán



15.000.000 VNĐ



Trạng thái

Chờ thanh toán





Khi khách hàng nhấn nút Thanh toán ngay, hệ thống bắt đầu thực hiện quy trình.

3.2. Sơ đồ tổng quan quá trình thanh toán

















developer.casso.vn





Hãy chia hệ thống thành 5 thành phần:

Thành phần	Nhiệm vụ

Customer	Người mua hàng

Frontend	Giao diện website

Backend	Xử lý nghiệp vụ đơn hàng

Bank API	Kết nối ngân hàng hoặc nhà cung cấp thanh toán

Database	Lưu đơn hàng và giao dịch



3.3. Luồng hoạt động chi tiết

1\. Khách hàng tạo đơn hàng

&#x20;  

&#x20;  Frontend gửi yêu cầu đến Backend với danh sách sản phẩm, số lượng và phương thức thanh toán.

2\. Backend tính tiền và lưu đơn hàng

&#x20;  

&#x20;  Backend tự tính tổng tiền dựa trên dữ liệu sản phẩm trong Database, không tin số tiền do Frontend gửi lên. Đơn hàng được lưu ở trạng thái PENDING\_PAYMENT.

3\. Backend gọi API ngân hàng

&#x20;  

&#x20;  Backend gửi mã đơn hàng, số tiền, nội dung thanh toán và thông tin định danh đối tác tới ngân hàng hoặc cổng thanh toán.

4\. Ngân hàng trả về thông tin thanh toán

&#x20;  

&#x20;  Hệ thống nhận URL thanh toán hoặc dữ liệu QR tùy theo dịch vụ đang tích hợp.

5\. Khách hàng thực hiện thanh toán

&#x20;  

&#x20;  Khách hàng quét mã QR hoặc xác thực giao dịch bằng ứng dụng ngân hàng.

6\. Ngân hàng thông báo kết quả

&#x20;  

&#x20;  Ngân hàng hoặc cổng thanh toán gửi thông báo đến địa chỉ Webhook/IPN của Backend.

7\. Backend xác minh giao dịch

&#x20;  

&#x20;  Kiểm tra chữ ký, mã giao dịch, số tiền, mã đơn hàng và trạng thái giao dịch.

8\. Cập nhật trạng thái đơn hàng

&#x20;  

&#x20;  Nếu hợp lệ, Backend cập nhật thanh toán thành công, ghi nhận giao dịch và chuyển đơn hàng sang bước xử lý tiếp theo.



Đặc biệt, cần hiểu rõ sự khác biệt giữa hai luồng:

\- Return URL: Đưa khách hàng quay lại website sau khi thanh toán.

\- Webhook/IPN: Kênh máy chủ ngân hàng hoặc cổng thanh toán thông báo kết quả cho máy chủ doanh nghiệp.

Không nên chỉ dựa vào việc khách hàng được chuyển về trang Thanh toán thành công để xác nhận đơn hàng. Tài liệu VNPAY mô tả IPN là luồng giao tiếp server-to-server và yêu cầu kiểm tra tính toàn vẹn dữ liệu trước khi cập nhật kết quả. 

Cổng thanh toán VNPAY+1





PHẦN 4. API KEY NGÂN HÀNG – LẬP TRÌNH VIÊN NHẬN ĐƯỢC NHỮNG GÌ?

Đây là phần liên quan trực tiếp đến nhận định ban đầu của bạn.

4.1. API Key là gì?

API Key là một dạng thông tin xác thực được sử dụng để nhận diện hoặc cấp quyền truy cập cho ứng dụng khi gọi API.



Tuy nhiên, trong hệ thống ngân hàng, API Key có thể chỉ là một thành phần của cơ chế xác thực.



Ví dụ, ngân hàng có thể cấp cho doanh nghiệp bộ thông tin minh họa sau:

BỘ THÔNG TIN TÍCH HỢP API

Ví dụ minh họa



CLIENT ID

merchant\_abc\_001





CLIENT SECRET



••••••••••••••••••••••



API BASE URL (UAT)



https://sandbox.example-bank.vn/api



SIGNING KEY / CERTIFICATE



merchant-private-key.pem



Các giá trị trên hoàn toàn giả lập, không phải thông tin đăng nhập của ngân hàng thật.



Các thành phần có thể bao gồm:

Thông tin	Ý nghĩa

Client ID	Định danh ứng dụng doanh nghiệp

Client Secret	Bí mật dùng trong quá trình xác thực

API Key	Khóa truy cập API nếu nhà cung cấp sử dụng

Access Token	Token tạm thời để gọi API

Signing Key	Khóa ký dữ liệu giao dịch

Certificate	Chứng thư số phục vụ xác thực hoặc mã hóa

Merchant ID	Mã định danh đơn vị chấp nhận thanh toán

Terminal ID	Mã định danh điểm giao dịch, nếu có



Ví dụ tài liệu VietinBank có mô tả phương thức kết nối RESTful qua HTTPS, JSON, client-id, client-secret, và trong một số phương thức sử dụng OAuth2/OIDC. Tài liệu cũng nêu yêu cầu đăng ký PID/MID, khai báo IP và chứng thư số đối với dịch vụ QR cụ thể. 

developer.vietinbank.vn+1



4.2. Tại sao ngân hàng phải cấp những thông tin này?

Hãy tưởng tượng ngân hàng có hàng nghìn doanh nghiệp cùng kết nối hệ thống.



Ngân hàng cần biết:

\- Ai đang gửi yêu cầu?

\- Yêu cầu đó thuộc doanh nghiệp nào?

\- Doanh nghiệp có được phép sử dụng chức năng này không?

\- Dữ liệu giao dịch có bị chỉnh sửa trong quá trình truyền tải không?

\- Yêu cầu có thực sự đến từ hệ thống hợp lệ không?

Thông tin xác thực giúp ngân hàng nhận diện ứng dụng và kiểm soát quyền truy cập.

4.3. Quy trình xác thực API bằng Access Token

Một số API ngân hàng sử dụng OAuth 2.0.

















blog.octo.com





Quy trình minh họa:

1\. Backend gửi Client ID và Client Secret đến máy chủ xác thực của ngân hàng.

2\. Ngân hàng kiểm tra thông tin.

3\. Nếu hợp lệ, ngân hàng trả về Access Token.

4\. Backend sử dụng Access Token để gọi API thanh toán.

5\. Khi Token hết hạn, Backend lấy Token mới theo quy định của ngân hàng.

Ví dụ code Node.js:

const axios = require("axios");



async function getBankAccessToken() {

&#x20;   const response = await axios.post(

&#x20;       process.env.BANK\_TOKEN\_URL,

&#x20;       new URLSearchParams({

&#x20;           grant\_type: "client\_credentials"

&#x20;       }),

&#x20;       {

&#x20;           auth: {

&#x20;               username: process.env.BANK\_CLIENT\_ID,

&#x20;               password: process.env.BANK\_CLIENT\_SECRET

&#x20;           },

&#x20;           headers: {

&#x20;               "Content-Type":

&#x20;                   "application/x-www-form-urlencoded"

&#x20;           }

&#x20;       }

&#x20;   );



&#x20;   return response.data.access\_token;

}





Đây là ví dụ theo OAuth 2.0 Client Credentials. Cấu trúc thực tế phải tuân theo tài liệu của ngân hàng; có ngân hàng yêu cầu xác thực bằng Header, chữ ký số, mTLS hoặc các tham số bổ sung.

4.4. Lưu API Key ở đâu?

Nguyên tắc bảo mật bắt buộc

Tuyệt đối không đưa Client Secret, Private Key hoặc API Key bí mật vào JavaScript chạy trên trình duyệt.



Không được viết:

// KHÔNG AN TOÀN

const BANK\_SECRET = "my-secret-key";



fetch("https://bank-api.example.com/payment", {

&#x20;   headers: {

&#x20;       "X-API-KEY": BANK\_SECRET

&#x20;   }

});





Bởi vì người dùng có thể mở Developer Tools, xem mã nguồn hoặc kiểm tra Network để lấy thông tin bí mật.



Cách đúng là lưu thông tin trong biến môi trường của Backend:

BANK\_BASE\_URL=https://sandbox.example-bank.vn

BANK\_CLIENT\_ID=your\_client\_id

BANK\_CLIENT\_SECRET=your\_client\_secret

BANK\_MERCHANT\_ID=your\_merchant\_id

BANK\_WEBHOOK\_SECRET=your\_webhook\_secret





Backend mới được quyền đọc các biến này.

const bankClientId = process.env.BANK\_CLIENT\_ID;

const bankSecret = process.env.BANK\_CLIENT\_SECRET;





Trong môi trường thật, cần bổ sung quản lý Secret an toàn, giới hạn quyền truy cập, xoay vòng khóa, không ghi thông tin bí mật vào log và sử dụng HTTPS.



PHẦN 5. THỰC HÀNH XÂY DỰNG HỆ THỐNG THANH TOÁN BẰNG NODE.JS

Bây giờ chúng ta sẽ chuyển từ lý thuyết sang lập trình.



Thay vì chỉ mô tả API hoạt động như thế nào, chúng ta sẽ xây dựng một mô hình mô phỏng hệ thống bán hàng tích hợp thanh toán ngân hàng.

5.1. Công nghệ sử dụng

Công nghệ	Vai trò

HTML, CSS, JavaScript	Giao diện khách hàng

Node.js	Môi trường chạy Backend

Express.js	Xây dựng REST API

MySQL	Lưu đơn hàng và giao dịch

Axios	Gửi HTTP Request đến nhà cung cấp

dotenv	Quản lý biến môi trường

Bank API	Xử lý thanh toán



















github.com





5.2. Thiết kế cấu trúc dự án

payment-system/

│

├── config/

│   └── database.js

│

├── controllers/

│   ├── orderController.js

│   └── paymentController.js

│

├── services/

│   └── bankService.js

│

├── routes/

│   ├── orderRoutes.js

│   └── paymentRoutes.js

│

├── middlewares/

│   └── errorHandler.js

│

├── public/

│   ├── index.html

│   ├── payment.html

│   └── js/

│       └── app.js

│

├── .env

├── .gitignore

└── server.js





Chúng ta chia thành các tầng rõ ràng:

\- Routes: Tiếp nhận yêu cầu HTTP.

\- Controllers: Xử lý nghiệp vụ.

\- Services: Giao tiếp với ngân hàng.

\- Database: Lưu trữ dữ liệu.

\- Frontend: Hiển thị kết quả cho khách hàng.

5.3. Thiết kế Database

Trước khi viết API, cần thiết kế cơ sở dữ liệu.



Bảng orders – Quản lý đơn hàng

CREATE TABLE orders (

&#x20;   id BIGINT AUTO\_INCREMENT PRIMARY KEY,



&#x20;   order\_code VARCHAR(50) NOT NULL UNIQUE,



&#x20;   customer\_id BIGINT,



&#x20;   total\_amount DECIMAL(15,2) NOT NULL,



&#x20;   payment\_status ENUM(

&#x20;       'PENDING',

&#x20;       'PAID',

&#x20;       'FAILED',

&#x20;       'EXPIRED',

&#x20;       'REFUNDED'

&#x20;   ) DEFAULT 'PENDING',



&#x20;   order\_status ENUM(

&#x20;       'NEW',

&#x20;       'PROCESSING',

&#x20;       'SHIPPING',

&#x20;       'COMPLETED',

&#x20;       'CANCELLED'

&#x20;   ) DEFAULT 'NEW',



&#x20;   created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,



&#x20;   updated\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

&#x20;       ON UPDATE CURRENT\_TIMESTAMP

);





Bảng payments – Quản lý giao dịch thanh toán

CREATE TABLE payments (

&#x20;   id BIGINT AUTO\_INCREMENT PRIMARY KEY,



&#x20;   order\_id BIGINT NOT NULL,



&#x20;   transaction\_code VARCHAR(100),



&#x20;   provider VARCHAR(50),



&#x20;   amount DECIMAL(15,2) NOT NULL,



&#x20;   payment\_method VARCHAR(30),



&#x20;   status ENUM(

&#x20;       'PENDING',

&#x20;       'SUCCESS',

&#x20;       'FAILED'

&#x20;   ) DEFAULT 'PENDING',



&#x20;   provider\_transaction\_id VARCHAR(100),



&#x20;   paid\_at DATETIME,



&#x20;   created\_at TIMESTAMP DEFAULT CURRENT\_TIMESTAMP,



&#x20;   FOREIGN KEY (order\_id) REFERENCES orders(id),



&#x20;   UNIQUE KEY unique\_provider\_transaction (

&#x20;       provider,

&#x20;       provider\_transaction\_id

&#x20;   )

);





Tại sao cần hai bảng riêng biệt?



Bởi vì một đơn hàng có thể phát sinh nhiều lần thử thanh toán.



Ví dụ:

\- Lần 1: Khách hàng thanh toán thất bại.

\- Lần 2: Khách hàng thử lại.

\- Lần 3: Khách hàng thanh toán thành công.

Nếu chỉ lưu trạng thái trong bảng orders, chúng ta sẽ mất lịch sử các lần giao dịch.



Vì vậy, orders quản lý đơn hàng, còn payments quản lý từng lần thanh toán.

5.4. Bước 1 – Khách hàng tạo đơn hàng

Frontend gửi yêu cầu:

async function createOrder() {

&#x20;   const response = await fetch("/api/orders", {

&#x20;       method: "POST",

&#x20;       headers: {

&#x20;           "Content-Type": "application/json"

&#x20;       },

&#x20;       body: JSON.stringify({

&#x20;           productId: 1,

&#x20;           quantity: 1

&#x20;       })

&#x20;   });



&#x20;   const result = await response.json();



&#x20;   console.log(result);

}





Backend tiếp nhận:

const express = require("express");

const router = express.Router();



router.post("/", async (req, res) => {

&#x20;   try {

&#x20;       const { productId, quantity } = req.body;



&#x20;       // Backend phải kiểm tra sản phẩm

&#x20;       // và lấy giá từ Database.



&#x20;       const product = await getProduct(productId);



&#x20;       if (!product || quantity < 1) {

&#x20;           return res.status(400).json({

&#x20;               message: "Dữ liệu đơn hàng không hợp lệ"

&#x20;           });

&#x20;       }



&#x20;       const totalAmount =

&#x20;           Number(product.price) \* quantity;



&#x20;       const orderCode =

&#x20;           "DH" + Date.now();



&#x20;       // Lưu đơn hàng vào MySQL

&#x20;       await saveOrder({

&#x20;           orderCode,

&#x20;           totalAmount,

&#x20;           paymentStatus: "PENDING"

&#x20;       });



&#x20;       res.json({

&#x20;           success: true,

&#x20;           orderCode,

&#x20;           amount: totalAmount

&#x20;       });



&#x20;   } catch (error) {

&#x20;       res.status(500).json({

&#x20;           message: "Không thể tạo đơn hàng"

&#x20;       });

&#x20;   }

});



module.exports = router;





Trong ví dụ trên, getProduct() và saveOrder() là các hàm truy vấn MySQL cần triển khai trong dự án. Phần quan trọng là Backend tự lấy giá sản phẩm, không nhận tổng tiền do Frontend tự quyết định.

5.5. Bước 2 – Backend khởi tạo yêu cầu thanh toán

Đây là bước quan trọng nhất.



Sau khi đơn hàng được tạo, Backend sẽ gửi yêu cầu sang ngân hàng.



Ví dụ dữ liệu gửi đi:

{

&#x20;   "merchantId": "MERCHANT001",

&#x20;   "orderId": "DH20261124001",

&#x20;   "amount": 15000000,

&#x20;   "currency": "VND",

&#x20;   "description": "Thanh toan don hang DH20261124001",

&#x20;   "returnUrl": "https://shop.example.com/payment/result",

&#x20;   "notifyUrl": "https://api.example.com/webhooks/bank"

}





Đây là cấu trúc minh họa, không phải JSON chuẩn dùng chung cho mọi ngân hàng.



Code Backend:

const axios = require("axios");



async function createBankPayment(order) {



&#x20;   const token = await getBankAccessToken();



&#x20;   const payload = {

&#x20;       merchantId: process.env.BANK\_MERCHANT\_ID,



&#x20;       orderId: order.order\_code,



&#x20;       amount: Number(order.total\_amount),



&#x20;       currency: "VND",



&#x20;       description:

&#x20;           `Thanh toan don hang ${order.order\_code}`,



&#x20;       returnUrl:

&#x20;           process.env.PAYMENT\_RETURN\_URL,



&#x20;       notifyUrl:

&#x20;           process.env.PAYMENT\_WEBHOOK\_URL

&#x20;   };



&#x20;   const response = await axios.post(

&#x20;       `${process.env.BANK\_BASE\_URL}/payments`,

&#x20;       payload,

&#x20;       {

&#x20;           headers: {

&#x20;               Authorization: `Bearer ${token}`,

&#x20;               "Content-Type": "application/json"

&#x20;           }

&#x20;       }

&#x20;   );



&#x20;   return response.data;

}



module.exports = {

&#x20;   createBankPayment

};





Giả sử ngân hàng phản hồi:

{

&#x20;   "success": true,

&#x20;   "transactionId": "BANK123456789",

&#x20;   "paymentUrl": "https://sandbox.example-bank.vn/pay/123",

&#x20;   "status": "PENDING"

}





Backend sẽ lưu mã giao dịch và trả paymentUrl về Frontend.



Điểm cần nhớ: Endpoint /payments, tên trường dữ liệu và cách xác thực trong đoạn code trên là ví dụ thiết kế. Khi tích hợp thật, phải thay bằng endpoint và chữ ký theo tài liệu kỹ thuật của ngân hàng.

5.6. Bước 3 – Frontend chuyển khách hàng đến trang thanh toán

Sau khi nhận được đường dẫn thanh toán:

async function payOrder(orderCode) {



&#x20;   const response = await fetch(

&#x20;       `/api/payments/${orderCode}`,

&#x20;       {

&#x20;           method: "POST"

&#x20;       }

&#x20;   );



&#x20;   const result = await response.json();



&#x20;   if (result.success) {

&#x20;       window.location.href =

&#x20;           result.paymentUrl;

&#x20;   }

}





Lúc này, khách hàng được chuyển đến giao diện thanh toán của nhà cung cấp.













































14























Khách hàng thực hiện xác thực theo hướng dẫn của ngân hàng.



Website của doanh nghiệp không được tự ý thu thập mật khẩu Internet Banking, mã PIN hoặc OTP của khách hàng. Việc xác thực thanh toán phải diễn ra trên kênh được ngân hàng hoặc đơn vị thanh toán kiểm soát.

5.7. Bước 4 – Ngân hàng gửi Webhook về Backend

Đây là phần rất đáng chú ý.



Webhook là cơ chế cho phép một hệ thống chủ động gửi dữ liệu đến một URL của hệ thống khác khi có sự kiện xảy ra.



Ví dụ:



Khách hàng vừa thanh toán thành công 15.000.000 đồng.



Thay vì Backend liên tục hỏi ngân hàng:

\- Đơn hàng đã thanh toán chưa?

\- Đã nhận được tiền chưa?

\- Giao dịch thành công chưa?

Ngân hàng hoặc cổng thanh toán có thể chủ động gửi thông báo đến hệ thống doanh nghiệp.

















fundl.us





Ví dụ dữ liệu Webhook:

{

&#x20;   "transactionId": "BANK123456789",

&#x20;   "orderId": "DH20261124001",

&#x20;   "amount": 15000000,

&#x20;   "currency": "VND",

&#x20;   "status": "SUCCESS",

&#x20;   "paidAt": "2026-11-24T10:30:00+07:00"

}





Backend xây dựng endpoint nhận thông báo:

router.post(

&#x20;   "/webhooks/bank",

&#x20;   async (req, res) => {



&#x20;       try {

&#x20;           const payment = req.body;



&#x20;           // 1. Xác minh chữ ký

&#x20;           // 2. Kiểm tra mã đơn hàng

&#x20;           // 3. Kiểm tra số tiền

&#x20;           // 4. Kiểm tra giao dịch đã xử lý chưa

&#x20;           // 5. Cập nhật trạng thái



&#x20;           res.json({

&#x20;               success: true,

&#x20;               message: "Received"

&#x20;           });



&#x20;       } catch (error) {

&#x20;           res.status(400).json({

&#x20;               success: false

&#x20;           });

&#x20;       }

&#x20;   }

);





Đây mới là khung minh họa. Trong hệ thống thật, không được bỏ qua bước xác minh chữ ký và đối chiếu dữ liệu.

5.8. Bước 5 – Xác minh giao dịch và cập nhật đơn hàng

Giả sử có người gửi một yêu cầu giả mạo đến:

POST /webhooks/bank





Với nội dung:

{

&#x20;   "orderId": "DH20261124001",

&#x20;   "amount": 15000000,

&#x20;   "status": "SUCCESS"

}





Nếu Backend chỉ kiểm tra status === SUCCESS thì kẻ tấn công có thể giả mạo thông báo để đánh dấu đơn hàng đã thanh toán dù ngân hàng chưa nhận được tiền.



Đây là một lỗi bảo mật nghiêm trọng.



Backend cần xác minh:

1\. Chữ ký thông báo có hợp lệ không?

2\. Mã giao dịch có tồn tại và đúng nhà cung cấp không?

3\. Mã đơn hàng có tồn tại không?

4\. Số tiền thanh toán có khớp không?

5\. Tiền tệ có đúng không?

6\. Giao dịch có bị xử lý trước đó không?

7\. Trạng thái giao dịch có thực sự là thành công không?

Ví dụ code xử lý nghiệp vụ:

async function handleSuccessfulPayment(data) {



&#x20;   const connection = await db.getConnection();



&#x20;   try {

&#x20;       await connection.beginTransaction();



&#x20;       // Tìm đơn hàng

&#x20;       const \[orders] = await connection.execute(

&#x20;           `SELECT \* FROM orders

&#x20;            WHERE order\_code = ?

&#x20;            FOR UPDATE`,

&#x20;           \[data.orderId]

&#x20;       );



&#x20;       if (orders.length === 0) {

&#x20;           throw new Error("Không tìm thấy đơn hàng");

&#x20;       }



&#x20;       const order = orders\[0];



&#x20;       // Kiểm tra số tiền

&#x20;       if (

&#x20;           Number(order.total\_amount) !==

&#x20;           Number(data.amount)

&#x20;       ) {

&#x20;           throw new Error("Sai số tiền thanh toán");

&#x20;       }



&#x20;       // Không xử lý lại đơn đã thanh toán

&#x20;       if (order.payment\_status === "PAID") {

&#x20;           await connection.rollback();

&#x20;           return;

&#x20;       }



&#x20;       // Lưu giao dịch

&#x20;       await connection.execute(

&#x20;           `UPDATE payments

&#x20;            SET status = 'SUCCESS',

&#x20;                provider\_transaction\_id = ?,

&#x20;                paid\_at = NOW()

&#x20;            WHERE order\_id = ?

&#x20;              AND status = 'PENDING'`,

&#x20;           \[

&#x20;               data.transactionId,

&#x20;               order.id

&#x20;           ]

&#x20;       );



&#x20;       // Cập nhật đơn hàng

&#x20;       await connection.execute(

&#x20;           `UPDATE orders

&#x20;            SET payment\_status = 'PAID',

&#x20;                order\_status = 'PROCESSING'

&#x20;            WHERE id = ?`,

&#x20;           \[order.id]

&#x20;       );



&#x20;       await connection.commit();



&#x20;   } catch (error) {



&#x20;       await connection.rollback();

&#x20;       throw error;



&#x20;   } finally {

&#x20;       connection.release();

&#x20;   }

}





Đây là ví dụ để giảng dạy nguyên tắc giao dịch Database. Khi triển khai thực tế cần bổ sung kiểm tra bản ghi giao dịch, đối chiếu trạng thái đã xác minh từ ngân hàng, xử lý giao dịch trùng lặp bằng mã định danh duy nhất và đảm bảo cập nhật đúng một lần.



Một nguyên tắc cực kỳ quan trọng: Không được đánh dấu đơn hàng đã thanh toán chỉ vì khách hàng nói rằng họ đã chuyển tiền. Phải có bằng chứng giao dịch hợp lệ từ ngân hàng hoặc nhà cung cấp thanh toán.



PHẦN 6. WEBHOOK VÀ POLLING – HAI CÁCH KIỂM TRA THANH TOÁN

Hai cơ chế này rất dễ bị nhầm lẫn.





















Webhook

Chủ động thông báo

Ngân hàng gửi kết quả về Backend khi có sự kiện.























Polling

Chủ động truy vấn

Backend định kỳ gọi API hỏi trạng thái giao dịch.





Ví dụ Polling:

async function checkPaymentStatus(transactionId) {



&#x20;   const token = await getBankAccessToken();



&#x20;   const response = await axios.get(

&#x20;       `/transactions/${transactionId}`,

&#x20;       {

&#x20;           headers: {

&#x20;               Authorization: `Bearer ${token}`

&#x20;           }

&#x20;       }

&#x20;   );



&#x20;   return response.data.status;

}





So sánh:

Tiêu chí	Webhook	Polling

Cách hoạt động	Ngân hàng gửi thông báo	Backend hỏi ngân hàng

Thời điểm	Khi có sự kiện	Theo chu kỳ

Độ trễ	Thường thấp	Phụ thuộc chu kỳ

Số lượng request	Theo sự kiện	Có thể nhiều

Ứng dụng	Nhận kết quả thanh toán	Kiểm tra trạng thái, đối soát



Trong thực tế, hệ thống tốt thường kết hợp cả hai: Webhook là luồng thông báo chính, còn API truy vấn trạng thái và đối soát là phương án bổ trợ khi thông báo bị thất lạc hoặc chưa nhận được.

PHẦN 7. XỬ LÝ CÁC TÌNH HUỐNG THỰC TẾ TRONG THANH TOÁN

Một bài toán thanh toán thực tế không chỉ có hai trạng thái thành công và thất bại. Lập trình viên cần nghĩ đến những tình huống xảy ra trong quá trình vận hành.

7.1. Các tình huống có thể xảy ra

SUCCESS

Thanh toán thành công



Khách hàng thanh toán đúng số tiền, ngân hàng xác nhận giao dịch. Hệ thống cập nhật đơn hàng đã thanh toán.

FAILED

Thanh toán thất bại



Khách hàng không đủ tiền, ngân hàng từ chối giao dịch hoặc giao dịch bị lỗi. Đơn hàng vẫn chưa được xác nhận thanh toán.

PENDING

Đang chờ thanh toán



Khách hàng đã tạo yêu cầu nhưng chưa hoàn tất giao dịch. Hệ thống chưa được phép xác nhận đơn hàng.

TIMEOUT

Quá thời gian chờ



Backend gọi ngân hàng nhưng không nhận được phản hồi trong thời gian quy định. Không được mặc định đây là giao dịch thất bại vì ngân hàng có thể đã xử lý giao dịch.

DUPLICATE

Thông báo giao dịch bị gửi lặp



Ngân hàng gửi lại Webhook do chưa nhận được phản hồi trước đó. Backend phải nhận diện giao dịch đã xử lý để không cộng tiền hoặc cập nhật đơn hàng nhiều lần.

7.2. Vì sao phải chống xử lý giao dịch trùng lặp?

Giả sử khách hàng thanh toán một đơn hàng 15 triệu đồng.



Ngân hàng gửi Webhook thành công lần đầu. Backend cập nhật đơn hàng.



Nhưng do lỗi mạng, ngân hàng không nhận được phản hồi HTTP 200. Ngân hàng gửi lại Webhook lần thứ hai.



Nếu Backend xử lý cả hai lần như hai giao dịch mới, hệ thống có thể gây ra những lỗi nghiêm trọng như:

\- Ghi nhận doanh thu hai lần.

\- Trừ tồn kho hai lần.

\- Gửi hai email xác nhận.

\- Tạo hai yêu cầu giao hàng.

Để khắc phục, sử dụng provider\_transaction\_id hoặc một mã định danh giao dịch duy nhất và ràng buộc UNIQUE trong Database.



Ví dụ:

ALTER TABLE payments

ADD UNIQUE KEY unique\_transaction\_id (

&#x20;   provider,

&#x20;   provider\_transaction\_id

);





Ngoài ra, cần sử dụng cơ chế xử lý idempotency (tính bất biến khi thực hiện lặp lại). Nghĩa là một giao dịch dù được gửi đến nhiều lần vẫn chỉ tạo ra một kết quả nghiệp vụ duy nhất.

7.3. Bảo mật Webhook

Webhook là một điểm tiếp nhận dữ liệu quan trọng. Vì vậy, cần bảo vệ nó cẩn thận.

















creativesoftware.com





Các biện pháp cần thực hiện:

Biện pháp	Mục đích

HTTPS	Mã hóa dữ liệu truyền tải

HMAC/RSA Signature	Xác minh tính toàn vẹn và nguồn gốc dữ liệu

IP Whitelist	Giới hạn địa chỉ IP được phép gửi thông báo nếu nhà cung cấp hỗ trợ

Timestamp	Kiểm tra thời gian gửi, chống phát lại

Nonce/Transaction ID	Phát hiện yêu cầu trùng lặp

Idempotency	Ngăn xử lý nghiệp vụ nhiều lần

Database Transaction	Đảm bảo cập nhật dữ liệu nhất quán



Ví dụ minh họa xác minh HMAC-SHA256:

const crypto = require("crypto");



function verifySignature(

&#x20;   rawBody,

&#x20;   receivedSignature

) {

&#x20;   const secret = process.env.BANK\_WEBHOOK\_SECRET;



&#x20;   const expectedSignature =

&#x20;       crypto

&#x20;           .createHmac("sha256", secret)

&#x20;           .update(rawBody)

&#x20;           .digest("hex");



&#x20;   if (

&#x20;       typeof receivedSignature !== "string" ||

&#x20;       !/^\[a-f0-9]{64}$/i.test(receivedSignature)

&#x20;   ) {

&#x20;       return false;

&#x20;   }



&#x20;   const expected = Buffer.from(

&#x20;       expectedSignature,

&#x20;       "hex"

&#x20;   );



&#x20;   const received = Buffer.from(

&#x20;       receivedSignature,

&#x20;       "hex"

&#x20;   );



&#x20;   return crypto.timingSafeEqual(

&#x20;       expected,

&#x20;       received

&#x20;   );

}





Lưu ý: Đoạn code trên chỉ minh họa một phương pháp HMAC. Cần đọc chính xác tài liệu ngân hàng để biết thuật toán, dữ liệu cần ký, cách chuẩn hóa JSON, encoding và tên Header. Một số ngân hàng dùng RSA hoặc chữ ký số thay vì HMAC.



Với Express, nếu nhà cung cấp yêu cầu ký trên nội dung HTTP nguyên bản, phải cấu hình express.raw() cho Webhook trước khi JSON parser làm thay đổi cách biểu diễn dữ liệu.



Ví dụ:

app.post(

&#x20;   "/webhooks/bank",

&#x20;   express.raw({ type: "application/json" }),

&#x20;   bankWebhookHandler

);



app.use(express.json());





7.4. Vì sao phải có chức năng đối soát giao dịch?

Hãy tưởng tượng:

\- Ngân hàng đã nhận tiền của khách hàng.

\- Nhưng đường truyền bị lỗi.

\- Webhook không thể gửi đến Backend.

\- Website vẫn hiển thị đơn hàng chưa thanh toán.

Lúc này, hệ thống có thể bị lệch dữ liệu giữa ngân hàng và doanh nghiệp.



Đối soát là quá trình so sánh dữ liệu giao dịch giữa hai hệ thống để phát hiện và xử lý chênh lệch.



Ví dụ:

Mã đơn	Website	Ngân hàng	Kết quả

DH001	Đã thanh toán	Đã nhận tiền	Khớp

DH002	Chờ thanh toán	Đã nhận tiền	Cần kiểm tra

DH003	Đã thanh toán	Chưa ghi nhận	Cần kiểm tra

DH004	Chờ thanh toán	Chưa nhận tiền	Khớp



Doanh nghiệp nên có tác vụ định kỳ gọi API truy vấn giao dịch hoặc sử dụng báo cáo đối soát từ ngân hàng để kiểm tra những trường hợp bất thường.



PHẦN 8. PHÂN BIỆT TÍCH HỢP API NGÂN HÀNG VÀ TÍCH HỢP CỔNG THANH TOÁN

Đây là phần rất cần thiết khi làm dự án thương mại điện tử.



Nhiều lập trình viên thường gọi tất cả những giải pháp thanh toán trực tuyến là API ngân hàng. Cách gọi này chưa chính xác.













































10























8.1. Kết nối trực tiếp với ngân hàng

Doanh nghiệp đăng ký sử dụng dịch vụ Open API hoặc sản phẩm thanh toán của ngân hàng.



Mô hình:

Website

&#x20;  |

&#x20;  v

Backend doanh nghiệp

&#x20;  |

&#x20;  v

Bank API

&#x20;  |

&#x20;  v

Ngân hàng

&#x20;  |

&#x20;  v

Xử lý giao dịch





Ưu điểm:

\- Có thể kết nối trực tiếp với dịch vụ ngân hàng.

\- Có khả năng sử dụng những nghiệp vụ ngân hàng được cấp quyền.

\- Phù hợp với doanh nghiệp cần tích hợp sâu vào hệ thống tài chính.

Hạn chế:

\- Phải đáp ứng điều kiện đăng ký của ngân hàng.

\- Từng ngân hàng có thể có tài liệu API khác nhau.

\- Cần triển khai xác thực và bảo mật theo yêu cầu riêng.

\- Công tác kiểm thử và vận hành có thể phức tạp.

8.2. Kết nối qua cổng thanh toán trung gian

Ví dụ doanh nghiệp đăng ký sử dụng dịch vụ của VNPAY.



Mô hình:

Website

&#x20;  |

&#x20;  v

Backend doanh nghiệp

&#x20;  |

&#x20;  v

VNPAY API

&#x20;  |

&#x20;  v

Ngân hàng / Đối tác thanh toán

&#x20;  |

&#x20;  v

Khách hàng thanh toán





Nhà cung cấp trung gian chịu trách nhiệm cung cấp các chức năng thanh toán theo phạm vi dịch vụ.



Ví dụ: VNPAY cung cấp tài liệu tích hợp gồm tạo URL thanh toán, Return URL và IPN. 

Cổng thanh toán VNPAY+1



8.3. So sánh hai mô hình

Tiêu chí	Kết nối ngân hàng	Cổng thanh toán

Đơn vị tích hợp	Ngân hàng	Nhà cung cấp thanh toán

Điều kiện	Theo ngân hàng	Theo nhà cung cấp

API	Theo từng ngân hàng	Theo nền tảng

Phương thức	Theo dịch vụ được cấp	Theo dịch vụ hỗ trợ

Xác thực	Theo ngân hàng	Theo nhà cung cấp

Đối soát	Theo sản phẩm ngân hàng	Theo nền tảng



Ví dụ để học viên dễ hiểu:



Nếu doanh nghiệp muốn nhận tiền vào tài khoản ngân hàng và tự động đối chiếu nội dung chuyển khoản, có thể nghiên cứu giải pháp thông báo biến động số dư, tài khoản định danh hoặc dịch vụ VietQR.



Nếu doanh nghiệp muốn khách hàng chọn nhiều phương thức thanh toán trên một giao diện tập trung, có thể nghiên cứu cổng thanh toán.



Hai mô hình có thể bổ trợ nhau, không nhất thiết loại trừ nhau.



PHẦN 9. SƠ ĐỒ TRẠNG THÁI ĐƠN HÀNG TRONG HỆ THỐNG THỰC TẾ

Đây là nội dung giúp lập trình viên hiểu rằng API thanh toán không đơn thuần là gửi một HTTP Request rồi nhận về một kết quả.



Thanh toán phải được kết nối với toàn bộ nghiệp vụ bán hàng.

















figviz.com





Có thể xây dựng quy trình:

&#x20;      TẠO ĐƠN HÀNG

&#x20;            |

&#x20;            v

&#x20;     PENDING\_PAYMENT

&#x20;            |

&#x20;      Khách thanh toán

&#x20;            |

&#x20;     +------+------+

&#x20;     |             |

&#x20;     v             v

&#x20;  SUCCESS        FAILED

&#x20;     |             |

&#x20;     v             v

&#x20;    PAID        Chờ thử lại

&#x20;     |

&#x20;     v

&#x20; PROCESSING

&#x20;     |

&#x20;     v

&#x20;  SHIPPING

&#x20;     |

&#x20;     v

&#x20; COMPLETED





Cần phân biệt hai loại trạng thái:

\- payment\_status: Trạng thái thanh toán.

\- order\_status: Trạng thái xử lý đơn hàng.

Ví dụ, khách hàng đã thanh toán thành công nhưng sản phẩm chưa được giao. Khi đó:

{

&#x20;   "payment\_status": "PAID",

&#x20;   "order\_status": "PROCESSING"

}





Không nên gộp hai trạng thái này thành một vì chúng biểu diễn hai nghiệp vụ khác nhau.



PHẦN 10. TRIỂN KHAI THỰC TẾ – LẬP TRÌNH VIÊN CẦN LÀM GÌ KHI DOANH NGHIỆP MUỐN TÍCH HỢP?

Giả sử bạn là Backend Developer của một công ty bán điện thoại.



Giám đốc yêu cầu:



"Tôi muốn khi khách hàng chuyển khoản thành công thì website tự động xác nhận đơn hàng, không cần nhân viên kiểm tra tài khoản ngân hàng nữa."



Bạn sẽ triển khai theo các bước sau.

Quy trình triển khai dự án

1\. Làm việc với doanh nghiệp

&#x20;  

&#x20;  Xác định ngân hàng đang sử dụng, nhu cầu thanh toán, loại tài khoản, khối lượng giao dịch và nghiệp vụ cần tự động hóa.

2\. Đăng ký dịch vụ với ngân hàng

&#x20;  

&#x20;  Doanh nghiệp làm việc với ngân hàng để đăng ký Open API, QR Payment, Payment Gateway hoặc dịch vụ thông báo giao dịch phù hợp.

3\. Nhận tài liệu kỹ thuật

&#x20;  

&#x20;  Lập trình viên nhận API Documentation, thông tin môi trường UAT, cơ chế xác thực, danh sách Endpoint, mã lỗi và quy trình Webhook.

4\. Xây dựng Backend

&#x20;  

&#x20;  Tạo API tạo đơn hàng, tạo giao dịch thanh toán, nhận Webhook, xác minh giao dịch và cập nhật Database.

5\. Kiểm thử Sandbox/UAT

&#x20;  

&#x20;  Thử nghiệm thanh toán thành công, thất bại, timeout, giao dịch trùng lặp, sai số tiền và lỗi xác thực.

6\. Nghiệm thu và chuyển Production

&#x20;  

&#x20;  Hoàn thành kiểm thử, cấu hình thông tin chính thức, bảo vệ khóa bí mật, khai báo URL Webhook và triển khai hệ thống.

7\. Theo dõi và đối soát

&#x20;  

&#x20;  Giám sát giao dịch, lưu nhật ký, xử lý Webhook thất lạc và kiểm tra chênh lệch giữa ngân hàng với website.



Checklist trước khi đưa lên môi trường thật

\- \[ ] Có tài khoản và dịch vụ ngân hàng được phê duyệt.

\- \[ ] Có tài liệu API chính thức.

\- \[ ] Có thông tin xác thực Production.

\- \[ ] Backend bảo vệ thông tin bí mật.

\- \[ ] Có HTTPS và cấu hình Webhook.

\- \[ ] Xác minh chữ ký giao dịch.

\- \[ ] Có cơ chế chống xử lý trùng lặp.

\- \[ ] Có xử lý timeout và retry an toàn.

\- \[ ] Có chức năng đối soát.

\- \[ ] Có nhật ký giao dịch và cảnh báo lỗi.

PHẦN 11. BÀI TẬP THỰC HÀNH CHO HỌC VIÊN AN TECH ACADEMY

Để học viên thực sự hiểu bài, không nên chỉ yêu cầu đọc code. Hãy giao một bài tập xây dựng chức năng thanh toán hoàn chỉnh.

















medium.com





Đề tài: Xây dựng chức năng thanh toán trực tuyến cho website bán điện thoại.



Yêu cầu:

1\. Xây dựng chức năng đăng nhập và quản lý khách hàng.

2\. Xây dựng danh mục sản phẩm.

3\. Xây dựng giỏ hàng.

4\. Cho phép khách hàng tạo đơn hàng.

5\. Hỗ trợ phương thức thanh toán chuyển khoản ngân hàng.

6\. Sinh mã QR hoặc đường dẫn thanh toán theo nhà cung cấp.

7\. Tiếp nhận thông báo thanh toán qua Webhook.

8\. Tự động cập nhật trạng thái đơn hàng.

9\. Lưu lịch sử giao dịch.

10\. Xây dựng giao diện quản trị để nhân viên theo dõi thanh toán.

Yêu cầu nâng cao:

\- Chống giả mạo Webhook.

\- Chống xử lý giao dịch trùng lặp.

\- Tự động kiểm tra giao dịch quá hạn.

\- Xây dựng báo cáo doanh thu.

\- Xây dựng chức năng đối soát giao dịch.

Câu hỏi kiểm tra kiến thức

Bài kiểm tra nhanh

0/5 câu



1\. API Key hoặc Client Secret nên được lưu ở đâu?



JavaScript trên trình duyệt



Backend và hệ thống quản lý Secret



Local Storage của khách hàng







2\. Khi khách hàng được chuyển về trang thanh toán thành công, Backend có nên lập tức xác nhận đơn hàng không?



Có, vì khách hàng đã quay về



Không, cần xác minh kết quả giao dịch đáng tin cậy



Có, nếu URL chứa status=SUCCESS







3\. Webhook là gì?



Cơ chế hệ thống khác chủ động gửi sự kiện đến Backend



Một loại Database



Một ngôn ngữ lập trình







4\. Nếu ngân hàng gửi một Webhook hai lần, hệ thống cần làm gì?



Cộng doanh thu hai lần



Tạo hai đơn hàng



Nhận diện giao dịch trùng và không xử lý nghiệp vụ lần nữa







5\. Vì sao phải đối soát giao dịch?



Để thay đổi giao diện



Để phát hiện sai lệch giữa dữ liệu ngân hàng và website



Để tăng tốc độ tải trang





Nộp bài kiểm tra



PHẦN 12. TỔNG KẾT BÀI GIẢNG

Điều quan trọng nhất mà tôi muốn học viên ghi nhớ là:



Tích hợp API thanh toán không chỉ là kết nối website với ngân hàng. Đó là việc xây dựng một quy trình nghiệp vụ hoàn chỉnh giữa hệ thống bán hàng, máy chủ doanh nghiệp và hệ thống tài chính.



Một lập trình viên Backend giỏi cần hiểu được toàn bộ chu trình:

















contra.com





\- Khách hàng tạo đơn hàng.

\- Backend kiểm tra và tính toán số tiền.

\- Backend khởi tạo giao dịch thanh toán.

\- Ngân hàng hoặc cổng thanh toán xử lý giao dịch.

\- Webhook thông báo kết quả.

\- Backend xác minh tính hợp lệ.

\- Database cập nhật trạng thái.

\- Hệ thống bán hàng tiếp tục xử lý giao hàng và doanh thu.

Đó chính là cách một hệ thống thương mại điện tử chuyên nghiệp hoạt động.

TÀI LIỆU THAM KHẢO THỰC TẾ

Để bài giảng không chỉ dừng lại ở lý thuyết, học viên có thể tham khảo tài liệu dành cho lập trình viên của các đơn vị sau:



1\. VietinBank Open API



Tìm hiểu các API thông báo biến động số dư, VietQR Pay, tài khoản định danh và chuyển tiền.

Truy cập cổng VietinBank Open API



2\. BIDV Open API



Tìm hiểu API Payment Gateway, khởi tạo giao dịch và vấn tin trạng thái.

Tài liệu sản phẩm BIDV Payment Gateway



3\. VNPAY Developer



Tìm hiểu tích hợp cổng thanh toán, Return URL và IPN.

Hướng dẫn tích hợp VNPAY



4\. NAPAS Developer



Tìm hiểu hệ sinh thái thanh toán VietQR và các giải pháp thanh toán liên ngân hàng.

Cổng tài liệu NAPAS Developer

