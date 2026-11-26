HỌC LẬP TRÌNH CÙNG AN

BÀI GIẢNG: THUẬT TOÁN SVD VÀ ỨNG DỤNG TRONG HỆ THỐNG LỌC CỘNG TÁC (COLLABORATIVE FILTERING)

Bài giảng chuyên ngành CNTT

&#x20;Machine Learning – Recommender Systems



1\. Mục tiêu bài học

Trong bài học này, chúng ta sẽ tìm hiểu thuật toán SVD (Singular Value Decomposition – Phân rã giá trị suy biến), một phương pháp đại số tuyến tính được ứng dụng trong hệ thống gợi ý sản phẩm.



Sau bài học, người học cần hiểu được:

\- SVD là gì và tại sao cần sử dụng SVD.

\- Ma trận người dùng – sản phẩm (User-Item Matrix) hoạt động như thế nào.

\- Cách SVD phân rã ma trận thành những thành phần nhỏ hơn.

\- Cách SVD tìm ra những đặc điểm sở thích tiềm ẩn của người dùng.

\- Cách kết hợp SVD với Collaborative Filtering để dự đoán mức độ yêu thích sản phẩm.

\- Cách ứng dụng thuật toán vào một website bán hàng hoặc nhà hàng thực tế.

2\. Đặt vấn đề: Tại sao cần thuật toán SVD?

Hãy tưởng tượng chúng ta đang xây dựng một website bán hàng trực tuyến. Hệ thống có hàng nghìn người dùng và hàng nghìn sản phẩm.



Mỗi người dùng có sở thích khác nhau. Có người thường xuyên mua điện thoại, có người thích laptop, có người quan tâm đến phụ kiện công nghệ.



Vấn đề đặt ra là:



Làm thế nào để hệ thống biết một người dùng có thể thích sản phẩm nào, kể cả khi họ chưa từng xem hoặc mua sản phẩm đó?



Một cách đơn giản là dựa vào lịch sử đánh giá hoặc hành vi mua hàng của những người dùng khác có sở thích tương tự.



Đây chính là ý tưởng của Collaborative Filtering – Lọc cộng tác.













































9





























Tuy nhiên, nếu số lượng người dùng và sản phẩm quá lớn, ma trận dữ liệu sẽ rất rộng và thưa. Phần lớn người dùng chỉ tương tác với một số ít sản phẩm.



Đây là lúc SVD phát huy tác dụng: giúp hệ thống tìm ra những yếu tố sở thích tiềm ẩn từ dữ liệu tương tác đã có.

3\. Tìm hiểu Collaborative Filtering – Lọc cộng tác

3.1. Collaborative Filtering là gì?

Collaborative Filtering là phương pháp gợi ý sản phẩm dựa trên hành vi và sở thích của nhiều người dùng.



Nguyên lý cơ bản:



Nếu hai người dùng có lịch sử đánh giá hoặc mua hàng tương tự nhau, hệ thống có thể dự đoán rằng họ sẽ tiếp tục quan tâm đến những sản phẩm tương tự.



Ví dụ:

\- Người A thích iPhone, MacBook và AirPods.

\- Người B cũng thích iPhone và MacBook.

\- Người B chưa từng đánh giá AirPods.

\- Hệ thống có thể đề xuất AirPods cho người B vì người có sở thích tương tự là A đã đánh giá cao sản phẩm này.

















medium.com





3.2. Ma trận người dùng – sản phẩm

Để máy tính xử lý dữ liệu, chúng ta biểu diễn hành vi người dùng dưới dạng ma trận.



Giả sử có 4 người dùng và 5 sản phẩm. Người dùng đánh giá sản phẩm theo thang điểm từ 1 đến 5.



Ta có ma trận sau:

Ma trận đánh giá sản phẩm



Hàng là người dùng, cột là sản phẩm. Dấu ? là chưa có đánh giá.

Người dùng	iPhone	Samsung	MacBook	AirPods	Chuột

A	5	4	5	5	?

B	5	4	4	?	2

C	1	2	?	1	5

D	2	1	2	?	5





Nhìn vào bảng, chúng ta có thể nhận thấy:

\- A và B có xu hướng thích các thiết bị công nghệ cao.

\- C và D có xu hướng quan tâm đến những sản phẩm khác.

\- Một số sản phẩm chưa được người dùng đánh giá.

Vấn đề: Làm thế nào dự đoán những ô còn thiếu trong ma trận?



Một trong những cách giải quyết là sử dụng SVD.

4\. Thuật toán SVD là gì?

SVD là viết tắt của Singular Value Decomposition, tiếng Việt gọi là phân rã giá trị suy biến.



Đây là thuật toán trong đại số tuyến tính, cho phép phân rã một ma trận dữ liệu ban đầu thành ba ma trận thành phần.





\\(A=U\\Sigma V^{\\mathsf T}\\)



\\(A=\\begin{bmatrix}4\&1\&2\&0\\\\1\&4\&0\&2\\\\2\&0\&4\&1\\\\0\&2\&1\&4\\end{bmatrix}\\)





















\\(A\_{2}=\\begin{bmatrix}3\&0,5\&3\&0,5\\\\0,5\&3\&0,5\&3\\\\3\&0,5\&3\&0,5\\\\0,5\&3\&0,5\&3\\end{bmatrix}\\)\\(\\text{error}=\\lVert A-A\_{2}\\rVert=3,162\\)









Gửi góp ý



Về bản chất, SVD giúp chúng ta biểu diễn một ma trận phức tạp thông qua các thành phần có cấu trúc đơn giản hơn.



Trong hệ thống gợi ý, điều quan trọng không chỉ là giảm kích thước dữ liệu mà còn là tìm ra các yếu tố tiềm ẩn (Latent Factors) thể hiện sở thích của người dùng và đặc điểm của sản phẩm.

4.1. Công thức SVD

Với ma trận dữ liệu A, SVD phân rã thành ba ma trận:

\\\[

A=U\\Sigma V^{T}

\\]



Trong đó:

Thành phần	Ý nghĩa

A	Ma trận dữ liệu ban đầu

U	Ma trận thể hiện các vector đặc trưng của hàng

Σ	Ma trận đường chéo chứa các giá trị suy biến

Vᵀ	Ma trận chuyển vị của các vector đặc trưng cột



Hãy hiểu đơn giản:

\- U giúp biểu diễn mối quan hệ giữa người dùng và các yếu tố tiềm ẩn.

\- Σ thể hiện mức độ quan trọng của từng yếu tố.

\- Vᵀ giúp biểu diễn mối quan hệ giữa sản phẩm và các yếu tố tiềm ẩn.

Trong bài toán gợi ý, các yếu tố tiềm ẩn có thể đại diện cho những sở thích mà hệ thống tự học được từ dữ liệu, chẳng hạn như xu hướng thích thiết bị cao cấp, thiết bị phục vụ học tập hoặc phụ kiện.



Lưu ý: Đây là những yếu tố toán học tiềm ẩn, không phải nhãn sở thích được con người định nghĩa sẵn.

5\. Ví dụ thực tế: Sử dụng SVD để gợi ý sản phẩm

Bây giờ chúng ta sẽ đi vào ví dụ cụ thể.



Giả sử website bán hàng có 4 người dùng:

\- An

\- Bình

\- Chi

\- Dũng

Và 4 sản phẩm:

\- iPhone

\- Samsung

\- MacBook

\- Chuột máy tính

Dữ liệu đánh giá:

Người dùng	iPhone	Samsung	MacBook	Chuột

An	5	4	5	1

Bình	5	4	4	2

Chi	1	2	1	5

Dũng	2	1	2	5



Nhận xét: An và Bình có xu hướng thích điện thoại, laptop. Trong khi đó, Chi và Dũng có xu hướng đánh giá cao chuột máy tính.

5.1. Bước 1 – Tạo ma trận dữ liệu

Chuyển bảng đánh giá thành ma trận:

\\\[

R=

\\begin{bmatrix}

5\&4\&5\&1\\\\

5\&4\&4\&2\\\\

1\&2\&1\&5\\\\

2\&1\&2\&5

\\end{bmatrix}

\\]



Đây là dữ liệu đầu vào của ví dụ minh họa.

5.2. Bước 2 – Phân rã ma trận bằng SVD

Hệ thống tiến hành phân rã ma trận R thành ba thành phần U, Σ và Vᵀ.



Thay vì xử lý toàn bộ ma trận ban đầu, ta có thể giữ lại một số lượng nhỏ các yếu tố tiềm ẩn quan trọng.



Ví dụ, giữ lại 2 yếu tố tiềm ẩn:

\- Yếu tố 1: Xu hướng yêu thích thiết bị công nghệ như điện thoại và laptop.

\- Yếu tố 2: Xu hướng yêu thích phụ kiện máy tính.

Đây chỉ là cách diễn giải trực quan cho ví dụ; thuật toán không tự đặt tên cho hai yếu tố này.

5.3. Bước 3 – Tái tạo ma trận đánh giá

Sau khi giữ lại các yếu tố quan trọng, hệ thống tính toán ma trận xấp xỉ:

\\\[

\\hat{R}=U\_k\\Sigma\_kV\_k^T

\\]



Trong đó k là số yếu tố tiềm ẩn được giữ lại.



Ma trận tái tạo cho phép ước lượng mức độ yêu thích của người dùng đối với những sản phẩm họ chưa đánh giá.

5.4. Bước 4 – Dự đoán và gợi ý

Giả sử người dùng An chưa từng đánh giá sản phẩm AirPods.



Hệ thống sử dụng mô hình đã học để tính điểm dự đoán cho sản phẩm đó.



Nếu điểm dự đoán cao, sản phẩm có thể được đưa vào danh sách gợi ý.

















hostadvice.com





Điểm quan trọng: SVD không trực tiếp chọn sản phẩm. Nó giúp xây dựng mô hình dự đoán điểm đánh giá. Sau đó, hệ thống sắp xếp các sản phẩm chưa được tương tác theo điểm dự đoán và chọn ra Top-N sản phẩm để gợi ý.

6\. Đi sâu vào cách SVD dự đoán điểm đánh giá

Để hiểu rõ hơn, chúng ta hãy xem hệ thống thực sự làm gì khi người dùng chưa đánh giá một sản phẩm.

6.1. Tình huống cụ thể

Giả sử An đã đánh giá:

\- iPhone: 5 điểm.

\- Samsung: 4 điểm.

\- MacBook: 5 điểm.

\- Chuột máy tính: 1 điểm.

An chưa từng đánh giá AirPods.



Trong khi đó, Bình có sở thích khá giống An và đã đánh giá AirPods ở mức 5 điểm.



Hệ thống không đơn giản sao chép điểm của Bình cho An. Thay vào đó, SVD học các yếu tố tiềm ẩn từ toàn bộ lịch sử tương tác của nhiều người dùng.

















vishalsahu290.medium.com





6.2. Quá trình dự đoán diễn ra như thế nào?

Có thể hình dung quy trình gồm 5 bước:

1\. Thu thập dữ liệu

&#x20;  

&#x20;  Hệ thống lấy lịch sử đánh giá, mua hàng hoặc tương tác của người dùng.

2\. Xây dựng ma trận

&#x20;  

&#x20;  Biểu diễn dữ liệu dưới dạng ma trận User-Item.

3\. Huấn luyện mô hình SVD

&#x20;  

&#x20;  Tìm các vector đặc trưng tiềm ẩn cho người dùng và sản phẩm.

4\. Dự đoán điểm

&#x20;  

&#x20;  Tính toán mức độ yêu thích của An đối với AirPods.

5\. Xếp hạng và gợi ý

&#x20;  

&#x20;  So sánh điểm dự đoán của các sản phẩm chưa được đánh giá, sau đó chọn Top 5 hoặc Top 10.

6.3. Công thức dự đoán điểm

Trong hệ thống gợi ý sử dụng Matrix Factorization, điểm dự đoán thường được tính bằng:

\\\[

\\hat r\_{ui}=\\mu+b\_u+b\_i+q\_i^Tp\_u

\\]



Trong đó:

\- \\(\\hat r\_{ui}\\): Điểm dự đoán của người dùng u đối với sản phẩm i.

\- \\(\\mu\\): Điểm đánh giá trung bình toàn hệ thống.

\- \\(b\_u\\): Độ lệch đánh giá của người dùng.

\- \\(b\_i\\): Độ lệch đánh giá của sản phẩm.

\- \\(p\_u\\): Vector đặc trưng tiềm ẩn của người dùng.

\- \\(q\_i\\): Vector đặc trưng tiềm ẩn của sản phẩm.

Hai vector \\(p\_u\\) và \\(q\_i\\) được học trong quá trình huấn luyện mô hình.



Phần tích vô hướng \\(q\_i^Tp\_u\\) thể hiện mức độ tương thích giữa sở thích tiềm ẩn của người dùng và đặc điểm tiềm ẩn của sản phẩm.



Ví dụ minh họa kết quả dự đoán:

Sản phẩm	Điểm dự đoán

AirPods	4.8

Tai nghe Sony	4.6

Bàn phím cơ	3.2

Chuột gaming	2.1



Kết quả minh họa



Hệ thống có thể ưu tiên gợi ý AirPods và tai nghe Sony cho An.



Lưu ý: Các điểm trên chỉ nhằm minh họa kết quả, không phải kết quả thực nghiệm của bộ dữ liệu phía trên.

7\. Thực hành: Xây dựng mô hình SVD bằng Python

Bây giờ chúng ta chuyển từ lý thuyết sang lập trình.



Thay vì chỉ nói thuật toán hoạt động như thế nào, hãy xem cách một lập trình viên có thể triển khai nó trong một dự án thực tế.

7.1. Chuẩn bị môi trường

Sử dụng thư viện Surprise, một thư viện Python hỗ trợ xây dựng hệ thống gợi ý dựa trên dữ liệu đánh giá.



Cài đặt:

pip install scikit-surprise pandas





7.2. Chuẩn bị dữ liệu

Tạo một tập dữ liệu gồm ba trường:

\- user\_id: Mã người dùng.

\- product\_id: Mã sản phẩm.

\- rating: Điểm đánh giá.

Ví dụ:

ratings = \[    ("An", "iPhone", 5),    ("An", "Samsung", 4),    ("An", "MacBook", 5),    ("An", "Chuột", 1),    ("Binh", "iPhone", 5),    ("Binh", "Samsung", 4),    ("Binh", "MacBook", 4),    ("Binh", "AirPods", 5),    ("Chi", "iPhone", 1),    ("Chi", "Samsung", 2),    ("Chi", "Chuột", 5),    ("Chi", "AirPods", 1),    ("Dung", "iPhone", 2),    ("Dung", "MacBook", 2),    ("Dung", "Chuột", 5),    ("Dung", "AirPods", 2),]







Đây là dữ liệu lịch sử. Những sản phẩm chưa xuất hiện trong lịch sử của một người dùng sẽ là đối tượng cần dự đoán.

7.3. Xây dựng và huấn luyện mô hình

import pandas as pdfrom surprise import Datasetfrom surprise import Readerfrom surprise import SVD# Chuyển dữ liệu thành DataFramedf = pd.DataFrame(    ratings,    columns=\["user\_id", "product\_id", "rating"])# Khai báo thang điểmreader = Reader(rating\_scale=(1, 5))# Đưa dữ liệu vào Surprisedata = Dataset.load\_from\_df(    df\[\["user\_id", "product\_id", "rating"]],    reader)# Sử dụng toàn bộ dữ liệu để huấn luyện minh họatrainset = data.build\_full\_trainset()# Khởi tạo mô hình SVDmodel = SVD(    n\_factors=2,    n\_epochs=100,    lr\_all=0.005,    reg\_all=0.02,    random\_state=42)# Huấn luyệnmodel.fit(trainset)print("Huấn luyện hoàn tất!")







Giải thích các tham số:

Tham số	Ý nghĩa

n\_factors=2	Sử dụng 2 yếu tố tiềm ẩn

n\_epochs=100	Huấn luyện qua 100 vòng

lr\_all=0.005	Tốc độ học

reg\_all=0.02	Hệ số điều chuẩn

random\_state=42	Cố định ngẫu nhiên để dễ tái lập



Ở đây, mô hình Surprise SVD là phương pháp phân rã ma trận được tối ưu trực tiếp trên các đánh giá đã biết, không phải thao tác lấy ma trận có ô trống rồi điền số 0 và áp dụng SVD thông thường.

7.4. Dự đoán sản phẩm cho người dùng

Đây là phần quan trọng nhất:

\# Dự đoán điểm của An đối với AirPodsprediction = model.predict("An", "AirPods")print("Người dùng:", prediction.uid)print("Sản phẩm:", prediction.iid)print("Điểm dự đoán:", round(prediction.est, 2))







Trong đó:

\- An là người dùng cần gợi ý.

\- AirPods là sản phẩm chưa được An đánh giá.

\- prediction.est là điểm đánh giá mà mô hình dự đoán.

7.5. Xây dựng chức năng gợi ý Top 5

Không chỉ dự đoán một sản phẩm, chúng ta cần dự đoán nhiều sản phẩm rồi sắp xếp theo mức độ phù hợp.

def recommend\_products(user\_id, df, model, top\_n=5):    # Danh sách tất cả sản phẩm    all\_products = df\["product\_id"].unique()    # Sản phẩm người dùng đã đánh giá    rated\_products = df\[        df\["user\_id"] == user\_id    ]\["product\_id"].tolist()    recommendations = \[]    for product in all\_products:        # Bỏ qua sản phẩm đã đánh giá        if product in rated\_products:            continue        # Dự đoán điểm        predicted\_rating = model.predict(            user\_id,            product        ).est        recommendations.append({            "product": product,            "score": predicted\_rating        })    # Sắp xếp giảm dần theo điểm dự đoán    recommendations.sort(        key=lambda x: x\["score"],        reverse=True    )    return recommendations\[:top\_n]result = recommend\_products("An", df, model)for item in result:    print(        item\["product"],        round(item\["score"], 2)    )























roartheme.co





Khi chạy chương trình, hệ thống sẽ đưa ra danh sách các sản phẩm An chưa đánh giá, sắp xếp theo điểm dự đoán từ cao xuống thấp.



Vì tập dữ liệu chỉ có 5 sản phẩm nên kết quả tối đa sẽ là một vài sản phẩm, không nhất thiết đủ 5 sản phẩm. Trong dự án thực tế, danh sách sản phẩm có thể lên đến hàng nghìn hoặc hàng triệu mặt hàng.



Một lưu ý khi thực hành: Bộ dữ liệu này rất nhỏ, chỉ dùng để minh họa cách lập trình. Muốn đánh giá chính xác chất lượng mô hình, cần có dữ liệu lớn hơn và chia tập huấn luyện, kiểm thử riêng biệt.

8\. Ứng dụng SVD trong một dự án thực tế

Hãy liên hệ với một website bán hàng mà chúng ta đang xây dựng.



Giả sử hệ thống có kiến trúc:

\- Frontend: HTML, CSS, JavaScript.

\- Backend: Node.js và Express.js.

\- Database: MySQL.

\- AI Service: Python và Flask.

\- Recommendation Engine: SVD.

















dev.to





8.1. Luồng hoạt động của hệ thống

Người dùng truy cập website



Xem sản phẩm, mua hàng, đánh giá





Backend Node.js / Express



Ghi nhận và xử lý hành vi người dùng





MySQL Database



Lưu lịch sử tương tác và đánh giá





Python – SVD Recommendation Engine



Huấn luyện, dự đoán và xếp hạng sản phẩm





Trả danh sách sản phẩm gợi ý



Backend nhận dữ liệu và hiển thị trên website





8.2. Ví dụ API thực tế

Backend có thể cung cấp một API:

GET /api/recommendations/An





Python xử lý việc dự đoán và trả về dữ liệu JSON:

{

&#x20; "user\_id": "An",

&#x20; "recommendations": \[

&#x20;   {

&#x20;     "product\_id": "P001",

&#x20;     "predicted\_rating": 4.8

&#x20;   },

&#x20;   {

&#x20;     "product\_id": "P002",

&#x20;     "predicted\_rating": 4.6

&#x20;   }

&#x20; ]

}





Frontend nhận dữ liệu, sau đó sử dụng product\_id để lấy thông tin sản phẩm như tên, giá, hình ảnh và hiển thị cho người dùng.



Như vậy, SVD không cần trực tiếp quản lý giao diện, giỏ hàng hay thanh toán. Nó đảm nhiệm phần phân tích dữ liệu và dự đoán sở thích.

9\. Ưu điểm và hạn chế của SVD

Ưu điểm	Hạn chế

Khám phá được sở thích tiềm ẩn	Cần dữ liệu tương tác để học

Giảm số chiều dữ liệu	Cần thời gian huấn luyện

Dự đoán được sản phẩm chưa đánh giá	Khó xử lý người dùng mới

Có thể cá nhân hóa gợi ý	Chất lượng phụ thuộc dữ liệu

Phù hợp với dữ liệu tương tác lớn	Cần cập nhật mô hình khi dữ liệu thay đổi



9.1. Vấn đề Cold Start

Đây là một vấn đề quan trọng trong hệ thống gợi ý.



Cold Start xảy ra khi hệ thống chưa có đủ dữ liệu về người dùng hoặc sản phẩm mới.



Ví dụ:



Một khách hàng vừa đăng ký tài khoản, chưa xem, chưa mua và chưa đánh giá bất kỳ sản phẩm nào.



Lúc này, SVD không có đủ dữ liệu lịch sử để xác định sở thích của khách hàng.



Một số phương án xử lý:

\- Sử dụng Popularity-Based Filtering: Gợi ý sản phẩm phổ biến.

\- Sử dụng thông tin danh mục và thuộc tính sản phẩm.

\- Thu thập sở thích ban đầu thông qua lựa chọn của người dùng.

\- Kết hợp nhiều phương pháp gợi ý để bổ sung dữ liệu.

















linkedin.com





10\. Đánh giá hiệu quả thuật toán SVD

Một hệ thống gợi ý không thể chỉ chạy được là xem như thành công. Chúng ta phải đánh giá xem mô hình dự đoán có chính xác hay không.



Hai chỉ số thường được sử dụng là RMSE và MAE.



RMSE (Root Mean Squared Error): Đo căn bậc hai của trung bình bình phương sai số giữa điểm thực tế và điểm dự đoán.

\\\[

RMSE=\\sqrt{\\frac{1}{n}\\sum\_{i=1}^{n}(r\_i-\\hat r\_i)^2}

\\]



MAE (Mean Absolute Error): Đo trung bình giá trị tuyệt đối của sai số.

\\\[

MAE=\\frac{1}{n}\\sum\_{i=1}^{n}|r\_i-\\hat r\_i|

\\]



Ví dụ:

Mô hình	RMSE

Mô hình A	0.95

Mô hình B	0.78

Mô hình C	0.62



Mô hình C tốt hơn theo RMSE

Vì RMSE càng thấp thì sai số dự đoán trên tập kiểm thử càng nhỏ.



Tuy nhiên, RMSE thấp chưa chắc đồng nghĩa với việc danh sách gợi ý Top-N tốt. Nếu muốn đánh giá chất lượng gợi ý, chúng ta còn có thể sử dụng Precision@K, Recall@K và F1@K.

11\. Phân biệt SVD và Collaborative Filtering

Đây là phần người học cần đặc biệt ghi nhớ vì hai thuật ngữ này thường bị nhầm lẫn.

Tiêu chí	Collaborative Filtering	SVD

Bản chất	Phương pháp gợi ý	Kỹ thuật phân rã ma trận

Mục đích	Gợi ý sản phẩm	Tìm cấu trúc tiềm ẩn trong dữ liệu

Đầu vào	Hành vi người dùng	Ma trận dữ liệu

Vai trò	Xác định sản phẩm cần gợi ý	Hỗ trợ dự đoán mức độ yêu thích

Quan hệ	Có thể sử dụng SVD	Có thể được sử dụng trong lọc cộng tác



Có thể hiểu đơn giản:



Collaborative Filtering là phương pháp giải quyết bài toán gợi ý sản phẩm, còn SVD là một kỹ thuật có thể được sử dụng để xây dựng mô hình dự đoán bên trong phương pháp đó.



Không phải mọi hệ thống Collaborative Filtering đều sử dụng SVD. Chúng ta còn có User-Based Collaborative Filtering, Item-Based Collaborative Filtering và nhiều phương pháp khác.



12\. Tổng kết bài học

Qua bài học này, chúng ta đã đi từ một vấn đề thực tế là làm thế nào để website hiểu sở thích khách hàng, đến cách sử dụng thuật toán SVD để giải quyết bài toán đó.



Điều quan trọng cần ghi nhớ:

1\. Dữ liệu tương tác của người dùng được biểu diễn thành ma trận User-Item.

2\. SVD giúp phân rã ma trận và tìm các yếu tố tiềm ẩn.

3\. Mô hình học mối quan hệ giữa người dùng và sản phẩm.

4\. Hệ thống sử dụng mô hình để dự đoán những đánh giá còn thiếu.

5\. Các sản phẩm có điểm dự đoán cao được ưu tiên đưa vào danh sách gợi ý.

Trong các website thương mại điện tử, nền tảng xem phim, nghe nhạc hoặc hệ thống quản lý nhà hàng, những kỹ thuật này đều có thể được ứng dụng để cá nhân hóa trải nghiệm người dùng.

13\. Câu hỏi kiểm tra kiến thức

Bài kiểm tra 5 câu

0/5 câu



Câu 1. SVD là viết tắt của thuật ngữ nào?



A. Singular Value Decomposition



B. System Value Database



C. Simple Vector Data



D. Software Version Development







Câu 2. Trong hệ thống gợi ý, ma trận User-Item biểu diễn điều gì?



A. Thông tin đăng nhập



B. Mối quan hệ tương tác giữa người dùng và sản phẩm



C. Cấu trúc giao diện website



D. Thông tin máy chủ







Câu 3. Tại sao chúng ta sử dụng SVD trong lọc cộng tác?



A. Để thiết kế giao diện



B. Để mã hóa mật khẩu



C. Để tìm yếu tố tiềm ẩn và dự đoán mức độ yêu thích



D. Để tăng tốc độ Internet







Câu 4. Nếu điểm dự đoán của một sản phẩm cao thì hệ thống thường làm gì?



A. Xóa sản phẩm



B. Ưu tiên đưa sản phẩm vào danh sách gợi ý



C. Khóa tài khoản



D. Xóa lịch sử đánh giá







Câu 5. Cold Start xảy ra khi nào?



A. Máy chủ bị mất điện



B. Người dùng hoặc sản phẩm mới chưa có đủ dữ liệu tương tác



C. Database có quá nhiều bảng



D. Website tải quá nhanh





Nộp bài và xem kết quả



Lời kết – An Tech Academy



Một hệ thống gợi ý thông minh không đơn giản là hiển thị những sản phẩm bán chạy nhất. Mục tiêu của nó là hiểu được mỗi người dùng có thể quan tâm đến điều gì, từ đó đưa ra những đề xuất phù hợp hơn.



SVD là một trong những kỹ thuật toán học giúp chúng ta tiến gần hơn đến mục tiêu đó.



Học lập trình không chỉ là học cách viết code, mà còn là hiểu cách những thuật toán phía sau vận hành và giải quyết các bài toán thực tế.

