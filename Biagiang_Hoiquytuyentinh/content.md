\# HỌC LẬP TRÌNH CÙNG AN

\# BÀI GIẢNG: HỒI QUY TUYẾN TÍNH VÀ ỨNG DỤNG



\*\*Thương hiệu:\*\* An Tech Academy  

\*\*Chủ đề:\*\* Machine Learning – Supervised Learning  

\*\*Đối tượng:\*\* Người mới học lập trình, dữ liệu và trí tuệ nhân tạo  

\*\*Mục tiêu:\*\* Hiểu bản chất, đọc được công thức, tự tính một ví dụ đơn giản, biết đánh giá mô hình và nhận diện các tình huống nên hoặc không nên sử dụng hồi quy tuyến tính.



\---



\## 1. Mở đầu: Vì sao chúng ta cần hồi quy tuyến tính?



Học lập trình cùng An. Hãy tưởng tượng một cửa hàng muốn ước tính doanh thu của ngày mai, một người mua nhà muốn tham khảo giá căn nhà dựa trên diện tích, hoặc một trang thương mại điện tử muốn dự đoán số lượng sản phẩm có thể bán trong tuần tới. Những bài toán này có điểm chung: chúng ta có dữ liệu trong quá khứ và muốn dùng dữ liệu đó để ước tính một giá trị số trong tương lai hoặc cho một trường hợp mới.



Thay vì đoán theo cảm tính, chúng ta có thể xây dựng một mô hình toán học để tìm mối liên hệ giữa các yếu tố đầu vào và kết quả. Một trong những phương pháp nền tảng, dễ hiểu và thường được dùng làm bước khởi đầu trong học máy là \*\*hồi quy tuyến tính (Linear Regression)\*\*.



Ví dụ, khi diện tích nhà tăng thì giá nhà thường có xu hướng tăng. Tuy nhiên, giá nhà không chỉ phụ thuộc vào diện tích. Vị trí, số phòng, chất lượng xây dựng, pháp lý và nhiều yếu tố khác cũng có thể ảnh hưởng. Hồi quy tuyến tính giúp mô hình hóa mối quan hệ này ở mức độ phù hợp với dữ liệu, chứ không khẳng định rằng diện tích là nguyên nhân duy nhất quyết định giá nhà.



!\[Đồ thị minh họa dữ liệu và đường hồi quy](img/01\_khai\_niem\_duong\_hoi\_quy.png)



\*Hình 1. Các chấm xanh là những quan sát thực tế; đường đỏ biểu diễn xu hướng tuyến tính mà mô hình ước lượng. Dữ liệu trong hình chỉ nhằm minh họa.\*



\## 2. Hồi quy tuyến tính là gì?



\*\*Hồi quy tuyến tính\*\* là một phương pháp thống kê và học máy có giám sát, được sử dụng để mô hình hóa mối quan hệ giữa một biến kết quả dạng số và một hoặc nhiều biến đầu vào. Từ dữ liệu đã có, mô hình ước lượng các hệ số sao cho giá trị dự đoán nằm gần các giá trị quan sát theo một tiêu chí tối ưu, thường là tổng bình phương phần dư nhỏ nhất.



Nói đơn giản: mô hình quan sát nhiều cặp dữ liệu đầu vào – kết quả, học ra một công thức, sau đó dùng công thức đó để dự đoán kết quả cho dữ liệu mới.



\### 2.1. Một số thuật ngữ cần nắm



| Thuật ngữ | Ý nghĩa | Ví dụ |

|---|---|---|

| Biến đầu vào (feature, X) | Thông tin mô hình sử dụng để dự đoán | Diện tích nhà, số phòng ngủ |

| Biến mục tiêu (target, Y) | Giá trị mà mô hình cần dự đoán | Giá nhà |

| Dữ liệu huấn luyện (training data) | Dữ liệu dùng để mô hình học hệ số | Các căn nhà đã biết diện tích và giá |

| Giá trị thực tế (y) | Kết quả được quan sát trong dữ liệu | Giá bán thực tế |

| Giá trị dự đoán (ŷ) | Kết quả do mô hình tạo ra | Giá nhà mô hình ước tính |

| Hệ số (coefficient) | Mức độ và chiều liên hệ mà mô hình ước lượng | Mức thay đổi dự đoán khi X tăng một đơn vị |

| Phần dư (residual) | Chênh lệch giữa thực tế và dự đoán | `e = y - ŷ` |



\### 2.2. Hồi quy khác phân loại như thế nào?



Hồi quy thường dự đoán \*\*một giá trị số liên tục\*\*, chẳng hạn giá nhà, doanh thu, nhiệt độ hoặc lượng tiêu thụ điện. Phân loại (Classification) thường dự đoán \*\*một nhãn hoặc nhóm\*\*, chẳng hạn email là spam hay không spam, khách hàng có rời bỏ dịch vụ hay không.



Ví dụ: dự đoán một căn nhà có giá 2,1 tỷ đồng là bài toán hồi quy. Dự đoán căn nhà thuộc nhóm giá thấp, trung bình hay cao là bài toán phân loại nếu đầu ra được định nghĩa thành các nhãn đó.



!\[So sánh hồi quy và phân loại](img/10\_hoi\_quy\_vs\_phan\_loai.png)



\*Hình 2. Hồi quy ước lượng một đại lượng số; phân loại gán đối tượng vào một nhãn hoặc nhóm.\*



> Ghi nhớ: Không phải cứ dự đoán là hồi quy. Hãy nhìn vào kiểu kết quả cần dự đoán: số liên tục thường là hồi quy; nhãn hoặc lớp thường là phân loại.



\## 3. Hiểu đường hồi quy và mối quan hệ giữa các biến



Trong biểu đồ phân tán (scatter plot), mỗi chấm thể hiện một quan sát. Trục X biểu diễn biến đầu vào; trục Y biểu diễn biến kết quả. Nếu các điểm có xu hướng đi lên từ trái sang phải, mối liên hệ tuyến tính có xu hướng dương. Nếu chúng đi xuống, mối liên hệ có xu hướng âm. Nếu các điểm phân tán mà không thể hiện xu hướng đường thẳng rõ ràng, một mô hình tuyến tính đơn giản có thể không mô tả tốt dữ liệu.



!\[Ba dạng xu hướng tuyến tính](img/02\_he\_so\_goc\_va\_chieu\_tuong\_quan.png)



\*Hình 3. Hệ số góc dương biểu thị xu hướng tăng; hệ số góc âm biểu thị xu hướng giảm; hệ số góc gần 0 biểu thị đường hồi quy gần nằm ngang. Hệ số gần 0 không có nghĩa là hai biến hoàn toàn không có bất kỳ mối quan hệ nào; chúng có thể có quan hệ phi tuyến.\*



Cần phân biệt \*\*mối liên hệ (association)\*\* với \*\*quan hệ nhân quả (causation)\*\*. Nếu dữ liệu cho thấy diện tích và giá nhà có xu hướng đi cùng nhau, điều đó không chứng minh rằng chỉ cần tăng diện tích là giá nhà sẽ tăng đúng theo hệ số của mô hình. Những yếu tố khác có thể đồng thời tác động đến cả hai biến.



\## 4. Công thức hồi quy tuyến tính đơn biến



Hồi quy tuyến tính đơn biến sử dụng \*\*một biến đầu vào\*\* để dự đoán một biến kết quả. Mô hình tổng thể thường được biểu diễn như sau:



\\\[

Y = \\beta\_0 + \\beta\_1X + \\varepsilon

\\]



Sau khi ước lượng hệ số từ dữ liệu mẫu, công thức dự đoán được viết:



\\\[

\\hat{y} = b\_0 + b\_1x

\\]



Trong đó:



\- `x`: giá trị đầu vào.

\- `ŷ` (đọc là y mũ): giá trị mà mô hình dự đoán.

\- `b₀`: hệ số chặn (intercept), là giá trị dự đoán của Y khi X bằng 0.

\- `b₁`: hệ số góc (slope), cho biết giá trị dự đoán của Y thay đổi trung bình bao nhiêu khi X tăng một đơn vị.

\- `β₀`, `β₁`: hệ số của mô hình tổng thể; `b₀`, `b₁` là các hệ số ước lượng từ dữ liệu mẫu.

\- `ε`: sai số ngẫu nhiên trong mô hình tổng thể.



Trong dữ liệu đã quan sát, phần dư của một điểm thường được tính là:



\\\[

e\_i = y\_i - \\hat{y}\_i

\\]



\*\*Lưu ý quan trọng:\*\* `ε` và `e` không hoàn toàn đồng nghĩa. `ε` là thành phần sai số trong mô hình tổng thể, còn `e` là phần dư tính được từ dữ liệu sau khi đã ước lượng mô hình.



\### 4.1. Đọc hệ số chặn và hệ số góc



Giả sử mô hình có dạng `ŷ = 0,5 + 0,02x`, trong đó X là diện tích tính bằng mét vuông và Y là giá nhà tính bằng tỷ đồng. Khi đó, hệ số góc `0,02` có nghĩa là: trong phạm vi dữ liệu và theo mô hình này, diện tích tăng thêm 1 m² gắn với mức tăng trung bình ước lượng 0,02 tỷ đồng, tương đương 20 triệu đồng, trong giá trị dự đoán.



Hệ số chặn `0,5` là giá trị mô hình dự đoán khi diện tích bằng 0 m². Trong bài toán giá nhà, trường hợp này không có ý nghĩa thực tế. Hệ số chặn vẫn cần thiết về mặt toán học, nhưng không phải lúc nào cũng có cách diễn giải thực tế hữu ích.



\### 4.2. Quan sát tương tác của đường hồi quy



Hãy quan sát đường thẳng bên dưới. Các điểm có thể nằm phía trên hoặc phía dưới đường. Mô hình không cần đi qua tất cả các điểm; nhiệm vụ của nó là tìm đường phù hợp nhất với xu hướng chung theo tiêu chí đã chọn.



\*\*Công thức chuẩn của đường hồi quy:\*\*



\\\[

\\hat{y} = b\_0 + b\_1x

\\]



\## 5. Mô hình tìm đường thẳng phù hợp như thế nào?



Một đường thẳng bất kỳ cũng có thể được vẽ xuyên qua biểu đồ, nhưng không phải đường nào cũng phù hợp. Hồi quy tuyến tính thông thường sử dụng \*\*phương pháp bình phương tối thiểu (Ordinary Least Squares – OLS)\*\* để chọn hệ số.



Với mỗi quan sát, mô hình tính giá trị dự đoán `ŷᵢ`, sau đó lấy giá trị thực tế `yᵢ` trừ đi giá trị dự đoán để thu được phần dư:



\\\[

e\_i = y\_i - \\hat{y}\_i

\\]



OLS chọn các hệ số để tối thiểu hóa tổng bình phương phần dư:



\\\[

SSE = \\sum\_{i=1}^{n}(y\_i - \\hat{y}\_i)^2

\\]



Tại sao lại bình phương phần dư?



1\. Nếu chỉ cộng phần dư có dấu, sai số dương và âm có thể triệt tiêu nhau. Bình phương làm cho các giá trị đều không âm.

2\. Sai số có độ lớn lớn sẽ bị phạt mạnh hơn sai số nhỏ.

3\. Với bài toán hồi quy tuyến tính OLS tiêu chuẩn, nghiệm có thể được tìm bằng công thức đại số hoặc các thuật toán số.



!\[Minh họa phần dư và bình phương tối thiểu](img/04\_binh\_phuong\_toi\_thieu.png)



\*Hình 4. Đường thẳng được chọn sao cho tổng bình phương các khoảng cách theo phương Y giữa điểm quan sát và giá trị trên đường là nhỏ nhất.\*



Không nên hiểu hình vẽ là mô hình đang tối thiểu hóa khoảng cách vuông góc từ điểm đến đường thẳng. OLS tối thiểu hóa \*\*phần dư theo chiều của biến Y\*\*.



\## 6. Ví dụ tính toán hoàn chỉnh: dự đoán giá nhà theo diện tích



Để hiểu cách các hệ số được tạo ra, ta sử dụng một bộ dữ liệu giả định gồm năm căn nhà. `X` là diện tích (m²), `Y` là giá bán (tỷ đồng). Các con số dưới đây chỉ là dữ liệu học tập, không đại diện cho giá thị trường thực tế.



| Căn nhà | Diện tích X (m²) | Giá thực tế Y (tỷ đồng) |

|---:|---:|---:|

| 1 | 60 | 1,55 |

| 2 | 70 | 1,72 |

| 3 | 80 | 2,05 |

| 4 | 90 | 2,15 |

| 5 | 100 | 2,48 |



\### Bước 1. Tính giá trị trung bình



\\\[

\\bar{x} = \\frac{60+70+80+90+100}{5}=80

\\]



\\\[

\\bar{y} = \\frac{1,55+1,72+2,05+2,15+2,48}{5}=1,99

\\]



\### Bước 2. Tính hệ số góc `b₁`



Công thức:



\\\[

b\_1 = \\frac{\\sum (x\_i-\\bar{x})(y\_i-\\bar{y})}{\\sum (x\_i-\\bar{x})^2}

\\]



Với bộ dữ liệu trên:



\\\[

\\sum (x\_i-\\bar{x})(y\_i-\\bar{y}) = 22,9

\\]



\\\[

\\sum (x\_i-\\bar{x})^2 = 1000

\\]



Do đó:



\\\[

b\_1 = \\frac{22,9}{1000}=0,0229

\\]



\### Bước 3. Tính hệ số chặn `b₀`



\\\[

b\_0 = \\bar{y} - b\_1\\bar{x}

\\]



\\\[

b\_0 = 1,99 - (0,0229 \\times 80)=0,158

\\]



\### Bước 4. Viết phương trình hồi quy



\\\[

\\boxed{\\hat{y}=0,158+0,0229x}

\\]



Diễn giải: trong bộ dữ liệu giả định này, cứ tăng 1 m² diện tích thì giá nhà \*\*được mô hình ước lượng tăng trung bình 0,0229 tỷ đồng\*\*, tương đương 22,9 triệu đồng. Đây là mô tả theo mô hình, không phải quy luật áp dụng cho mọi căn nhà.



\### Bước 5. Dự đoán căn nhà rộng 85 m²



Thay `x = 85` vào công thức:



\\\[

\\hat{y}=0,158+(0,0229\\times85)=2,1045

\\]



Mô hình dự đoán giá căn nhà 85 m² khoảng \*\*2,1045 tỷ đồng\*\* (xấp xỉ 2,10 tỷ đồng).



\### Bước 6. So sánh thực tế với dự đoán



| Diện tích (m²) | Giá thực tế (y) | Giá dự đoán (ŷ) | Phần dư (y − ŷ) |

|---:|---:|---:|---:|

| 60 | 1,550 | 1,532 | 0,018 |

| 70 | 1,720 | 1,761 | -0,041 |

| 80 | 2,050 | 1,990 | 0,060 |

| 90 | 2,150 | 2,219 | -0,069 |

| 100 | 2,480 | 2,448 | 0,032 |



!\[Các giá trị thực tế, dự đoán và phần dư](img/03\_phan\_du\_residual.png)



\*Hình 5. Phần dư dương nghĩa là mô hình dự đoán thấp hơn thực tế; phần dư âm nghĩa là mô hình dự đoán cao hơn thực tế.\*



Đây là cách đọc sai số ở từng quan sát. Để đánh giá toàn bộ mô hình, chúng ta cần thêm các chỉ số tổng hợp.



\## 7. Hồi quy tuyến tính đa biến



Trong thực tế, kết quả thường chịu ảnh hưởng bởi nhiều yếu tố. Giá nhà có thể liên quan đến diện tích, số phòng ngủ, vị trí, tuổi công trình và khoảng cách đến trung tâm. Khi sử dụng từ hai biến đầu vào trở lên, ta có \*\*hồi quy tuyến tính đa biến (Multiple Linear Regression)\*\*.



Công thức tổng quát:



\\\[

\\hat{y}=b\_0+b\_1x\_1+b\_2x\_2+\\cdots+b\_px\_p

\\]



Trong đó:



\- `x₁, x₂, …, xₚ` là các biến đầu vào.

\- `b₁, b₂, …, bₚ` là các hệ số tương ứng.

\- `b₀` là hệ số chặn.



!\[Sơ đồ các yếu tố đầu vào của hồi quy đa biến](img/06\_so\_do\_hoi\_quy\_da\_bien.png)



\*Hình 6. Nhiều đặc trưng cùng được đưa vào mô hình để dự đoán một kết quả.\*



Ví dụ về diễn giải: nếu hệ số của diện tích là 0,02 tỷ đồng/m², thì khi các biến đầu vào khác được giữ cố định, diện tích tăng 1 m² gắn với mức tăng ước lượng 0,02 tỷ đồng trong giá dự đoán. Cụm từ \*\*“giữ các biến khác cố định”\*\* rất quan trọng khi diễn giải hệ số đa biến.



Hồi quy đa biến không tự động chứng minh tác động nhân quả. Hệ số có thể bị ảnh hưởng bởi biến bị bỏ sót, cách thu thập dữ liệu, tương quan mạnh giữa các biến và các sai lệch khác.



\## 8. Hồi quy đa thức: khi xu hướng không phải đường thẳng



Không phải mọi quan hệ đều là đường thẳng. Có trường hợp Y tăng nhanh lúc đầu rồi chậm lại, hoặc thay đổi theo hình cong. Một cách mở rộng là tạo thêm đặc trưng như `x²`, `x³` rồi đưa chúng vào mô hình:



\\\[

\\hat{y}=b\_0+b\_1x+b\_2x^2

\\]



Mô hình này thường được gọi là \*\*hồi quy đa thức (Polynomial Regression)\*\*. Đường dự đoán có thể cong theo X, nhưng mô hình vẫn tuyến tính theo các hệ số `b₀`, `b₁`, `b₂`. Vì vậy, nó vẫn có thể được ước lượng bằng phương pháp hồi quy tuyến tính trên các đặc trưng đã biến đổi.



!\[So sánh hồi quy đơn biến, đa biến và đa thức](img/05\_cac\_dang\_hoi\_quy.png)



\*Hình 7. Ba dạng mô hình. Hình đa biến dùng màu để gợi ý rằng một biến đầu vào nữa cũng góp phần giải thích kết quả.\*



Tăng bậc đa thức quá cao có thể khiến mô hình bám sát nhiễu trong dữ liệu huấn luyện và dự đoán kém trên dữ liệu mới. Cần đánh giá trên dữ liệu chưa dùng để huấn luyện, không chọn độ phức tạp chỉ vì đường cong trông khớp hơn.



\## 9. Quy trình xây dựng một mô hình hồi quy tuyến tính



Một dự án thực tế thường trải qua các bước sau:



1\. \*\*Xác định bài toán:\*\* cần dự đoán giá trị nào, tại thời điểm nào, cho đối tượng nào? Chọn biến mục tiêu phù hợp.

2\. \*\*Thu thập dữ liệu:\*\* lấy dữ liệu có nguồn gốc rõ ràng, đủ liên quan và phản ánh tình huống cần dự đoán.

3\. \*\*Làm sạch dữ liệu:\*\* xử lý giá trị thiếu, kiểu dữ liệu sai, bản ghi trùng, đơn vị không thống nhất và ngoại lệ bất thường. Không xóa ngoại lệ một cách máy móc; cần xác minh đó là lỗi hay trường hợp thực tế.

4\. \*\*Khám phá dữ liệu:\*\* thống kê mô tả, vẽ biểu đồ phân tán, xem phân phối và mối liên hệ giữa các biến.

5\. \*\*Chia dữ liệu:\*\* tách dữ liệu huấn luyện và kiểm tra trước khi đánh giá cuối cùng. Với dữ liệu theo thời gian, nên chia theo thứ tự thời gian thay vì xáo trộn ngẫu nhiên.

6\. \*\*Huấn luyện:\*\* dùng tập huấn luyện để ước lượng các hệ số của mô hình.

7\. \*\*Đánh giá:\*\* tính MAE, MSE, RMSE, R² và xem xét phần dư. So sánh với một mô hình cơ sở đơn giản.

8\. \*\*Triển khai và theo dõi:\*\* đưa mô hình vào quy trình ứng dụng, theo dõi sai số khi có dữ liệu mới và đánh giá lại khi bối cảnh thay đổi.



!\[Quy trình xây dựng mô hình hồi quy](img/07\_quy\_trinh\_xay\_dung\_mo\_hinh.png)



\*Hình 8. Quy trình từ dữ liệu thô đến mô hình được triển khai và theo dõi.\*



\### 9.1. Vì sao cần tách train và test?



Nếu dùng cùng một tập dữ liệu để huấn luyện rồi báo cáo kết quả, chúng ta có nguy cơ đánh giá quá lạc quan. Mô hình cần được kiểm tra trên những quan sát mà nó chưa dùng để học. Một cách chia thường gặp là 80% dữ liệu cho huấn luyện và 20% cho kiểm tra, nhưng đây chỉ là ví dụ; tỷ lệ phù hợp phụ thuộc vào quy mô và đặc điểm dữ liệu.



!\[Ví dụ chia tập huấn luyện và kiểm tra](img/09\_chia\_train\_test.png)



\*Hình 9. Minh họa tỷ lệ 80/20. Với dữ liệu chuỗi thời gian, không nên tùy tiện trộn dữ liệu tương lai vào tập huấn luyện.\*



\## 10. Các chỉ số đánh giá mô hình



Không nên chỉ nhìn vào một con số rồi kết luận mô hình tốt hay xấu. Mỗi chỉ số thể hiện một góc nhìn khác nhau về sai số và mức độ giải thích dữ liệu.



\### 10.1. MAE – Mean Absolute Error



MAE là sai số tuyệt đối trung bình:



\\\[

MAE=\\frac{1}{n}\\sum\_{i=1}^{n}|y\_i-\\hat{y}\_i|

\\]



MAE cho biết trung bình độ lớn sai lệch giữa giá trị thực tế và dự đoán. Đơn vị của MAE giống đơn vị biến mục tiêu. Ví dụ, nếu giá nhà được tính bằng tỷ đồng thì MAE cũng có đơn vị tỷ đồng.



\### 10.2. MSE – Mean Squared Error



\\\[

MSE=\\frac{1}{n}\\sum\_{i=1}^{n}(y\_i-\\hat{y}\_i)^2

\\]



MSE bình phương sai số trước khi lấy trung bình, vì vậy sai số lớn có ảnh hưởng mạnh hơn. Đơn vị của MSE là bình phương đơn vị của biến mục tiêu, nên thường khó diễn giải trực tiếp hơn MAE.



\### 10.3. RMSE – Root Mean Squared Error



\\\[

RMSE=\\sqrt{\\frac{1}{n}\\sum\_{i=1}^{n}(y\_i-\\hat{y}\_i)^2}

\\]



RMSE là căn bậc hai của MSE. Chỉ số này có cùng đơn vị với biến mục tiêu và vẫn nhạy với các sai số lớn.



\### 10.4. R² – Hệ số xác định



\\\[

R^2=1-\\frac{\\sum (y\_i-\\hat{y}\_i)^2}{\\sum(y\_i-\\bar{y})^2}

\\]



R² cho biết mức độ mô hình giải thích biến thiên của Y so với mô hình cơ sở luôn dự đoán bằng trung bình của Y, trên tập dữ liệu đang xét. Với mô hình có hệ số chặn và đánh giá trên dữ liệu huấn luyện theo OLS, R² thường nằm trong khoảng 0 đến 1. Trên tập kiểm tra, R² có thể âm nếu mô hình dự đoán còn tệ hơn cách dự đoán đơn giản bằng trung bình của tập tham chiếu.



\*\*R² = 0,85 không có nghĩa mô hình dự đoán đúng 85% số lần.\*\* Nó cũng không chứng minh mô hình có quan hệ nhân quả. Cần đọc R² cùng MAE/RMSE, phần dư và mục tiêu nghiệp vụ.



!\[Minh họa so sánh thực tế, dự đoán và sai số](img/08\_danh\_gia\_mae\_rmse.png)



\*Hình 10. Điểm càng gần đường y = ŷ thì dự đoán càng sát; biểu đồ cột thể hiện độ lớn sai số tuyệt đối ở từng mẫu.\*



\### 10.5. Các chỉ số trên ví dụ giá nhà



Với năm quan sát giả định ở phần 6, mô hình có các kết quả trên chính bộ dữ liệu minh họa:



\- MAE = \*\*0,044 tỷ đồng\*\*, tương đương khoảng 44 triệu đồng.

\- RMSE ≈ \*\*0,0477 tỷ đồng\*\*, tương đương khoảng 47,7 triệu đồng.

\- R² ≈ \*\*0,9787\*\*.



Các chỉ số này được tính trên đúng năm điểm đã dùng để minh họa phép tính. Vì số mẫu rất ít và không có tập kiểm tra độc lập, \*\*không được xem đây là bằng chứng mô hình có thể dự đoán giá nhà ngoài thực tế với độ chính xác cao\*\*.



\## 11. Những giả định và giới hạn cần biết



Hồi quy tuyến tính hữu ích vì dễ hiểu và dễ diễn giải, nhưng không phải bài toán nào cũng phù hợp. Khi dùng mô hình, cần xem xét:



\- \*\*Tính tuyến tính:\*\* mối quan hệ trung bình cần được mô tả hợp lý bằng dạng tuyến tính theo các hệ số. Nếu có đường cong rõ rệt, cần biến đổi đặc trưng hoặc cân nhắc mô hình khác.

\- \*\*Tính độc lập của sai số:\*\* sai số giữa các quan sát không nên phụ thuộc có hệ thống vào nhau. Đây là vấn đề đáng chú ý với dữ liệu theo thời gian hoặc dữ liệu theo nhóm.

\- \*\*Phương sai sai số tương đối ổn định:\*\* nếu độ phân tán phần dư tăng hoặc giảm mạnh theo X hay theo giá trị dự đoán, suy luận thống kê có thể bị ảnh hưởng.

\- \*\*Ngoại lệ và điểm có ảnh hưởng lớn:\*\* một số điểm bất thường có thể kéo đường hồi quy thay đổi đáng kể. Cần kiểm tra nguyên nhân trước khi quyết định xử lý.

\- \*\*Đa cộng tuyến:\*\* trong hồi quy đa biến, các biến đầu vào tương quan tuyến tính rất mạnh có thể khiến việc diễn giải từng hệ số trở nên không ổn định.

\- \*\*Biến bị bỏ sót và dữ liệu sai lệch:\*\* thiếu yếu tố quan trọng, dữ liệu đại diện không tốt hoặc quy trình ghi nhận không nhất quán sẽ làm chất lượng mô hình giảm.

\- \*\*Ngoại suy:\*\* dự đoán quá xa vùng dữ liệu đã quan sát thường rủi ro. Đường thẳng khớp trong khoảng 50–150 m² không có nghĩa nó đáng tin khi áp dụng cho căn nhà 1.000 m².

\- \*\*Rò rỉ dữ liệu (data leakage):\*\* không được để thông tin chỉ có sau thời điểm cần dự đoán lọt vào biến đầu vào hoặc quá trình tiền xử lý.



Đối với suy luận thống kê cổ điển, giả định sai số phân phối chuẩn thường được dùng để xây dựng một số kiểm định và khoảng tin cậy trong mẫu nhỏ. Điều đó không có nghĩa mọi ứng dụng dự đoán đều bắt buộc phần dư phải chuẩn tuyệt đối; mục tiêu dự đoán và mục tiêu suy luận cần được phân biệt.



\## 12. Ứng dụng hồi quy tuyến tính trong thực tế



\### 12.1. Thương mại điện tử và bán lẻ



\- Dự đoán doanh thu theo ngày hoặc theo tuần dựa trên lịch sử bán hàng, giá bán, chương trình khuyến mãi và mùa vụ.

\- Ước lượng nhu cầu sản phẩm để hỗ trợ lập kế hoạch tồn kho.

\- Phân tích mối liên hệ giữa mức giảm giá và số lượng bán.



\### 12.2. Bất động sản



\- Ước tính giá tham khảo dựa trên diện tích, số phòng, tuổi công trình và vị trí.

\- Phân tích yếu tố nào liên hệ mạnh với giá trong một bộ dữ liệu cụ thể.

\- Hỗ trợ tạo giá tham khảo, nhưng không thay thế thẩm định pháp lý và đánh giá thực địa.



\### 12.3. Tài chính và kinh doanh



\- Ước lượng doanh thu, chi phí hoặc lợi nhuận dựa trên các yếu tố đầu vào.

\- Phân tích xu hướng chi tiêu, nhu cầu vốn hoặc một số chỉ số kinh doanh.

\- Trong tài chính, cần thận trọng với biến động thị trường, dữ liệu chuỗi thời gian và rủi ro thay đổi chế độ; mô hình tuyến tính đơn giản không đảm bảo dự đoán giá tài sản chính xác.



\### 12.4. Giáo dục



\- Ước lượng điểm số dựa trên số giờ học, tỷ lệ tham dự và kết quả đánh giá trước đó.

\- Phân tích mối liên hệ giữa thời lượng học và kết quả học tập.

\- Không nên dùng kết quả dự đoán đơn lẻ để kết luận năng lực hay đưa ra quyết định bất lợi cho người học.



\### 12.5. Y tế và chăm sóc sức khỏe



\- Nghiên cứu, ước lượng một chỉ số liên tục như huyết áp hoặc thời gian hồi phục dựa trên các biến được phép sử dụng trong nghiên cứu.

\- Hỗ trợ phân tích dữ liệu ở cấp độ nghiên cứu hoặc vận hành.

\- Không dùng một mô hình hồi quy đơn giản thay cho chẩn đoán, chỉ định hoặc đánh giá chuyên môn của nhân viên y tế.



\### 12.6. Nông nghiệp và năng lượng



\- Ước lượng sản lượng dựa trên lượng mưa, diện tích canh tác, loại giống và các điều kiện liên quan.

\- Dự đoán nhu cầu điện dựa trên lịch sử tiêu thụ, thời tiết và thời điểm.

\- Những bài toán có mùa vụ, xu hướng dài hạn hoặc quan hệ phi tuyến có thể cần mô hình chuỗi thời gian hay mô hình khác phù hợp hơn.



!\[Poster tổng quan các lĩnh vực ứng dụng](img/11\_poster\_tong\_quan.png)



\*Hình 11. Hình tổng hợp minh họa các lĩnh vực có thể khai thác mô hình dự đoán. Khi triển khai thật, cần lựa chọn dữ liệu, phương pháp và quy trình kiểm định phù hợp từng ngành.\*



\## 13. Thực hành bằng Python và scikit-learn



Trong dự án thực tế, lập trình viên thường sử dụng thư viện để huấn luyện mô hình thay vì tự tính từng hệ số bằng tay. Ví dụ dưới đây sử dụng `pandas` để đọc dữ liệu, `scikit-learn` để chia dữ liệu và huấn luyện, sau đó tính các chỉ số đánh giá.



\### 13.1. Cài đặt thư viện



```bash

pip install pandas scikit-learn matplotlib

```



\### 13.2. Cấu trúc dữ liệu đầu vào



Tạo file `du\_lieu\_nha.csv` có tối thiểu hai cột như sau. Bộ dữ liệu 10 dòng dưới đây giúp ví dụ chia tập kiểm tra có hai quan sát; đây vẫn chỉ là dữ liệu minh họa, chưa đủ để đánh giá một mô hình dùng trong thực tế.



```csv

dien\_tich\_m2,gia\_ty

50,1.32

60,1.55

70,1.72

80,2.05

90,2.15

100,2.48

110,2.55

120,2.85

130,3.05

140,3.30

```



\### 13.3. Huấn luyện và đánh giá mô hình



```python

import pandas as pd

from math import sqrt

from sklearn.model\_selection import train\_test\_split

from sklearn.linear\_model import LinearRegression

from sklearn.metrics import mean\_absolute\_error, mean\_squared\_error, r2\_score



\# 1. Đọc dữ liệu

\# Mỗi dòng là một căn nhà; các cột phải có đúng tên trong file CSV.

df = pd.read\_csv("du\_lieu\_nha.csv")



\# 2. Chọn đặc trưng đầu vào X và biến mục tiêu y

X = df\[\["dien\_tich\_m2"]]

y = df\["gia\_ty"]



\# 3. Chia dữ liệu thành tập huấn luyện và tập kiểm tra

\# random\_state giúp kết quả chia có thể tái lập.

\# Với dữ liệu theo thời gian, cần chia theo thời gian thay vì xáo trộn ngẫu nhiên.

X\_train, X\_test, y\_train, y\_test = train\_test\_split(

&#x20;   X, y, test\_size=0.2, random\_state=42

)



\# 4. Khởi tạo và huấn luyện mô hình

model = LinearRegression()

model.fit(X\_train, y\_train)



\# 5. Dự đoán trên tập kiểm tra

predictions = model.predict(X\_test)



\# 6. Đánh giá

mae = mean\_absolute\_error(y\_test, predictions)

mse = mean\_squared\_error(y\_test, predictions)

rmse = sqrt(mse)

r2 = r2\_score(y\_test, predictions)



print("Intercept (b0):", model.intercept\_)

print("Coefficient (b1):", model.coef\_\[0])

print("MAE:", mae)

print("MSE:", mse)

print("RMSE:", rmse)

print("R2:", r2)



\# 7. Dự đoán một căn nhà mới rộng 85 m2

new\_house = pd.DataFrame({"dien\_tich\_m2": \[85]})

predicted\_price = model.predict(new\_house)\[0]

print("Giá dự đoán (tỷ đồng):", predicted\_price)

```



\*\*Cảnh báo về ví dụ mã:\*\* Mười dòng dữ liệu vẫn quá ít để kết luận mô hình có khả năng dự đoán tổng quát. Nếu tập kiểm tra chỉ có một quan sát thì R² không thể được diễn giải có ý nghĩa và một số thư viện sẽ trả về giá trị không xác định. Mã nhằm minh họa quy trình API của scikit-learn. Khi làm dự án, cần tập dữ liệu đủ lớn, chia tập hợp lý và đánh giá trên dữ liệu đại diện.



\### 13.4. Giải thích các lệnh quan trọng



\- `LinearRegression()` tạo mô hình hồi quy tuyến tính.

\- `model.fit(X\_train, y\_train)` ước lượng hệ số từ dữ liệu huấn luyện.

\- `model.coef\_` trả về hệ số của các đặc trưng.

\- `model.intercept\_` trả về hệ số chặn.

\- `model.predict(...)` tạo dự đoán cho dữ liệu đầu vào mới.

\- `mean\_absolute\_error`, `mean\_squared\_error`, `r2\_score` tính các chỉ số tương ứng.



Trong hồi quy tuyến tính OLS tiêu chuẩn, không bắt buộc phải chuẩn hóa dữ liệu chỉ để mô hình chạy. Tuy nhiên, chuẩn hóa có thể hữu ích trong một số quy trình xử lý hoặc khi dùng các biến thể có regularization như Ridge và Lasso.



\## 14. So sánh nhanh: khi nào nên cân nhắc hồi quy tuyến tính?



| Tình huống | Mức độ phù hợp | Lý do |

|---|---|---|

| Dự đoán giá trị số, xu hướng khá tuyến tính | Phù hợp để thử đầu tiên | Dễ huấn luyện, dễ diễn giải |

| Cần giải thích chiều và mức liên hệ của các biến | Có ích | Hệ số có thể diễn giải khi điều kiện mô hình phù hợp |

| Quan hệ có dạng cong rõ rệt | Cần mở rộng hoặc chọn mô hình khác | Đường thẳng đơn giản có thể bỏ sót cấu trúc |

| Dữ liệu có ngoại lệ mạnh | Cần kiểm tra kỹ | OLS nhạy với một số điểm có ảnh hưởng lớn |

| Dự đoán nhãn như spam/không spam | Không phải lựa chọn hồi quy phù hợp | Đây là bài toán phân loại |

| Dự báo chuỗi thời gian có mùa vụ và xu hướng phức tạp | Có thể chưa đủ | Cần đặc trưng thời gian hoặc mô hình chuỗi thời gian phù hợp |



\## 15. Những hiểu lầm thường gặp



\*\*Hiểu lầm 1: Đường hồi quy phải đi qua tất cả các điểm.\*\* Không đúng. Đường hồi quy được chọn để tối ưu tiêu chí tổng thể, không phải để đi qua từng quan sát.



\*\*Hiểu lầm 2: R² càng cao thì mô hình chắc chắn càng tốt.\*\* Không đúng. R² cao trên tập huấn luyện có thể đi cùng overfitting, rò rỉ dữ liệu hoặc dữ liệu không đại diện. Cần đánh giá trên dữ liệu chưa thấy và xem xét sai số theo ngữ cảnh.



\*\*Hiểu lầm 3: Hệ số dương chứng minh X gây ra Y.\*\* Không đúng. Hệ số thể hiện mối liên hệ có điều kiện theo mô hình; muốn kết luận nhân quả cần thiết kế nghiên cứu và giả định phù hợp.



\*\*Hiểu lầm 4: Tăng dữ liệu luôn làm mô hình chính xác hơn.\*\* Chỉ tăng số lượng không đủ. Dữ liệu phải đúng, liên quan, đại diện và được thu thập đúng thời điểm.



\*\*Hiểu lầm 5: Có thể dự đoán thật xa ngoài vùng dữ liệu.\*\* Rất rủi ro. Mô hình có thể hoạt động ổn trong vùng quan sát nhưng sai lệch lớn khi ngoại suy.



\## 16. Bài tập củng cố



\### Bài tập 1 – Nhận diện bài toán



Một hệ thống cần dự đoán doanh thu ngày mai là 35 triệu đồng. Đây là bài toán hồi quy hay phân loại? Giải thích.



\### Bài tập 2 – Đọc hệ số



Một mô hình có phương trình `ŷ = 1,2 + 0,03x`, trong đó X là số giờ học và Y là điểm dự đoán.



1\. Hệ số chặn là bao nhiêu?

2\. Hệ số góc là bao nhiêu?

3\. Theo mô hình, số điểm dự đoán thay đổi thế nào khi số giờ học tăng thêm một giờ?

4\. Dự đoán điểm khi học 10 giờ.



\### Bài tập 3 – Tính phần dư



Một mẫu có giá trị thực tế `y = 2,4` và giá trị dự đoán `ŷ = 2,1`. Hãy tính phần dư và diễn giải dấu của phần dư.



\### Bài tập 4 – Lựa chọn chỉ số



Trong trường hợp doanh nghiệp muốn hạn chế những dự đoán sai lệch rất lớn, nên chú ý chỉ số nào hơn giữa MAE và RMSE? Vì sao?



\### Bài tập 5 – Thiết kế dữ liệu



Một ứng dụng muốn dự đoán giá thuê nhà. Hãy đề xuất ít nhất bốn biến đầu vào có thể thu thập hợp pháp và hợp lý. Nêu một rủi ro khi dữ liệu không đại diện.



\### Đáp án gợi ý



1\. Bài tập 1: Hồi quy, vì kết quả cần dự đoán là một giá trị số liên tục (doanh thu).

2\. Bài tập 2: `b₀ = 1,2`; `b₁ = 0,03`; khi X tăng 1 giờ, điểm dự đoán tăng 0,03 điểm theo mô hình; với 10 giờ, `ŷ = 1,2 + 0,03 × 10 = 1,5`.

3\. Bài tập 3: `e = 2,4 − 2,1 = 0,3`. Phần dư dương nghĩa là dự đoán thấp hơn thực tế 0,3 đơn vị.

4\. Bài tập 4: RMSE nhạy hơn với sai số lớn do bình phương sai số; tuy nhiên cần xem cả đơn vị, phân phối sai số và chi phí thực tế.

5\. Bài tập 5: Có thể gồm diện tích, số phòng, khu vực, khoảng cách tới điểm tiện ích, tình trạng nội thất, tuổi công trình. Rủi ro: dữ liệu chỉ thu thập ở khu vực trung tâm sẽ không đại diện cho nhà ở ngoại thành.



\## 17. Tổng kết bài học



Hồi quy tuyến tính là một phương pháp nền tảng để mô hình hóa mối quan hệ giữa biến đầu vào và một kết quả dạng số. Ở dạng đơn biến, mô hình có một biến đầu vào và một hệ số góc; ở dạng đa biến, mô hình kết hợp nhiều đặc trưng. Phương pháp bình phương tối thiểu thường được dùng để tìm các hệ số sao cho tổng bình phương phần dư nhỏ nhất.



Để xây dựng mô hình tốt, người làm dữ liệu không chỉ cần biết công thức. Cần hiểu dữ liệu, chia tập huấn luyện và kiểm tra đúng cách, đọc các chỉ số MAE/MSE/RMSE/R², kiểm tra phần dư, nhận diện giới hạn và đánh giá mô hình trong đúng bối cảnh sử dụng.



\*\*Thông điệp cuối:\*\* Hồi quy tuyến tính không phải công cụ đoán tương lai một cách tuyệt đối. Nó là công cụ giúp chúng ta đưa ra ước lượng có cơ sở từ dữ liệu, hiểu xu hướng và hỗ trợ quyết định tốt hơn.



\---



\## 18. Bảng thuật ngữ Anh – Việt dùng khi giảng dạy



| Thuật ngữ | Cách hiểu tiếng Việt |

|---|---|

| Linear Regression | Hồi quy tuyến tính |

| Machine Learning | Học máy |

| Supervised Learning | Học có giám sát |

| Feature | Đặc trưng / biến đầu vào |

| Target | Biến mục tiêu |

| Prediction | Dự đoán |

| Intercept | Hệ số chặn |

| Slope | Hệ số góc |

| Coefficient | Hệ số |

| Residual | Phần dư |

| Ordinary Least Squares (OLS) | Bình phương tối thiểu thông thường |

| Scatter Plot | Biểu đồ phân tán |

| Training Set | Tập huấn luyện |

| Test Set | Tập kiểm tra |

| Overfitting | Quá khớp |

| Data Leakage | Rò rỉ dữ liệu |

| Mean Absolute Error (MAE) | Sai số tuyệt đối trung bình |

| Mean Squared Error (MSE) | Sai số bình phương trung bình |

| Root Mean Squared Error (RMSE) | Căn bậc hai của sai số bình phương trung bình |

| Coefficient of Determination (R²) | Hệ số xác định |

| Multiple Linear Regression | Hồi quy tuyến tính đa biến |

| Polynomial Regression | Hồi quy đa thức |



\## Danh mục hình minh họa



1\. `01\_khai\_niem\_duong\_hoi\_quy.png` – Dữ liệu quan sát và đường hồi quy.

2\. `02\_he\_so\_goc\_va\_chieu\_tuong\_quan.png` – Xu hướng dương, âm và gần như không có xu hướng tuyến tính.

3\. `03\_phan\_du\_residual.png` – Giá trị thực tế, dự đoán và phần dư.

4\. `04\_binh\_phuong\_toi\_thieu.png` – Cách OLS tối thiểu hóa tổng bình phương phần dư.

5\. `05\_cac\_dang\_hoi\_quy.png` – Hồi quy đơn biến, đa biến và đa thức.

6\. `06\_so\_do\_hoi\_quy\_da\_bien.png` – Nhiều biến đầu vào kết hợp để dự đoán một kết quả.

7\. `07\_quy\_trinh\_xay\_dung\_mo\_hinh.png` – Quy trình xây dựng và triển khai mô hình.

8\. `08\_danh\_gia\_mae\_rmse.png` – So sánh giá trị thực tế, dự đoán và sai số.

9\. `09\_chia\_train\_test.png` – Minh họa tập huấn luyện và tập kiểm tra.

10\. `10\_hoi\_quy\_vs\_phan\_loai.png` – Phân biệt hồi quy với phân loại.

11\. `11\_poster\_tong\_quan.png` – Poster tổng quan các lĩnh vực ứng dụng.



\*\*Gợi ý sử dụng:\*\* Mỗi hình nằm ngay sau phần giải thích liên quan. Có thể chèn trực tiếp vào slide, tài liệu học tập hoặc video. Các ví dụ số trong bài được xây dựng để giảng dạy, không phải dữ liệu thị trường hay dữ liệu nghiên cứu thực tế.



