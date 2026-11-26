# -*- coding: utf-8 -*-
"""108 cue lời đọc bài SVD (Cổng A) — say đã phiên âm S-V-D / R-M-S-E / M-A-E."""
import math

RAW = [
    (1, [
        ("Xin chào các bạn! Chào mừng đến với An Tech Academy.", 0.45),
        ("Bạn đã bao giờ tự hỏi: vì sao vừa xem một món hàng, trang web đã gợi ý thêm hàng loạt sản phẩm tương tự?", 0.40),
        ("Đằng sau những ô gợi ý đó thường là một thuật toán mang tên Singular Value Decomposition.", 0.35),
        ("Hôm nay, chúng ta cùng tìm hiểu thuật toán này, và ứng dụng của nó trong lọc cộng tác, Collaborative Filtering.", 0.368),
        ("Sau bài học, bạn sẽ hiểu bản chất, đọc được công thức, và chạy được một mô hình gợi ý đơn giản bằng Python.", 0.45),
    ]),
    (2, [
        ("Những mục như \"dành riêng cho bạn\" hay \"có thể bạn cũng thích\" đã trở nên quen thuộc.", 0.35),
        ("Chúng xuất hiện trên trang chủ, trong trang sản phẩm, và cả trong khung giỏ hàng.", 0.30),
        ("Mục tiêu rất rõ: đưa đúng sản phẩm đến đúng người, trước khi người đó phải tự tìm.", 0.35),
        ("Nhưng làm được điều này không hề đơn giản.", 0.30),
        ("Một website có thể có hàng nghìn người dùng và hàng nghìn sản phẩm; mỗi người chỉ tương tác với một phần rất nhỏ.", 0.50),
    ]),
    (3, [
        ("Hãy hình dung toàn bộ lượt xem, lượt mua và đánh giá được ghi lại thành một bảng.", 0.30),
        ("Mỗi hàng là một người dùng, mỗi cột là một sản phẩm.", 0.30),
        ("Phần lớn các ô trong bảng đều trống, vì một người chỉ từng xem hoặc mua vài món.", 0.35),
        ("Câu hỏi trung tâm là: dự đoán những ô còn trống đó.", 0.35),
        ("Nói cách khác: đoán xem người dùng sẽ thích sản phẩm nào, dù họ chưa từng tương tác với nó.", 0.50),
    ]),
    (4, [
        ("Cách tự nhiên nhất là dựa vào những người có sở thích giống nhau.", 0.30),
        ("Nếu hai người cùng thích điện thoại và laptop giống nhau, hệ thống có thể đoán họ sẽ còn thích thêm những món giống nhau.", 0.35),
        ("Đó chính là lọc cộng tác, Collaborative Filtering.", 0.35),
        ("Ví dụ: An thích iPhone, MacBook và AirPods. Bình cũng thích iPhone và MacBook, nhưng chưa đánh giá AirPods.", 0.35),
        ("Hệ thống có thể đề xuất AirPods cho Bình, vì An, người có sở thích tương tự, đã đánh giá cao món này.", 0.50),
    ]),
    (5, [
        ("Trong lọc cộng tác, mỗi người dùng được nối với những sản phẩm họ đã xem, mua hoặc đánh giá.", 0.30),
        ("Những đường nối dày lên thành một mạng các hành vi.", 0.30),
        ("Có hai cách tiếp cận quen thuộc: dựa trên người dùng, và dựa trên sản phẩm.", 0.35),
        ("Cách dựa trên người dùng: tìm những người giống mình, rồi xem họ thích gì.", 0.30),
        ("Cách dựa trên sản phẩm: tìm những sản phẩm thường xuất hiện cùng nhau.", 0.35),
        ("Nhưng cả hai cách đều cần một thứ: cách so sánh và dự đoán đủ mạnh.", 0.45),
    ]),
    (6, [
        ("Một ví dụ dễ thấy là gợi ý phim.", 0.30),
        ("Hai người cùng xem và thích ba bộ phim giống nhau; họ được xem là người dùng tương tự.", 0.35),
        ("Một người trong số đó đã xem thêm một bộ phim khác.", 0.30),
        ("Hệ thống có thể gợi ý bộ phim đó cho người còn lại.", 0.35),
        ("Đây là lọc cộng tác dựa trên người dùng, ở dạng đơn giản nhất.", 0.45),
    ]),
    (7, [
        ("Để máy tính xử lý, ta biểu diễn dữ liệu thành ma trận người dùng – sản phẩm, User-Item Matrix.", 0.35),
        ("Hàng là người dùng; cột là sản phẩm; mỗi ô là điểm đánh giá.", 0.30),
        ("Ví dụ với bốn người: An, Bình, Chi, Dũng; và bốn sản phẩm: iPhone, Samsung, MacBook, Chuột.", 0.35),
        ("An và Bình cho điểm cao điện thoại và laptop; Chi và Dũng lại thích chuột hơn.", 0.35),
        ("Mục tiêu của mô hình gợi ý là điền vào các ô còn thiếu.", 0.35),
        ("Và S-V-D là một kỹ thuật giúp làm việc đó.", 0.45),
    ]),
    (8, [
        ("S-V-D là viết tắt của Singular Value Decomposition, tức phân rã giá trị suy biến.", 0.35),
        ("Đây là một kỹ thuật trong đại số tuyến tính.", 0.30),
        ("Với ma trận dữ liệu A, S-V-D phân rã A thành tích của ba ma trận: A bằng U, nhân Sigma, nhân V chuyển vị.", 0.40),
        ("U mô tả quan hệ giữa người dùng với các yếu tố tiềm ẩn.", 0.30),
        ("Sigma là ma trận đường chéo, cho biết mỗi yếu tố quan trọng đến mức nào.", 0.35),
        ("V chuyển vị mô tả quan hệ giữa sản phẩm với các yếu tố tiềm ẩn.", 0.50),
    ]),
    (9, [
        ("\"Tiềm ẩn\" nghĩa là hệ thống tự học ra, không phải nhãn do con người đặt trước.", 0.35),
        ("Ta có thể hiểu mỗi yếu tố như một trục sở thích: chẳng hạn, thích thiết bị công nghệ, hoặc thích phụ kiện.", 0.35),
        ("S-V-D cho phép giữ lại một số ít yếu tố quan trọng nhất.", 0.30),
        ("Những ô đã biết giúp tìm ra các vector tiềm ẩn của người dùng và sản phẩm.", 0.35),
        ("Từ đó, nhân chúng với nhau để ước lượng những ô còn trống.", 0.35),
        ("Đây chính là ý tưởng cốt lõi: phân rã phần đã biết, để suy ra phần chưa biết.", 0.50),
    ]),
    (10, [
        ("Trở lại bảng đánh giá của An, Bình, Chi, Dũng.", 0.30),
        ("An và Bình thích iPhone, Samsung và MacBook; Chi và Dũng thích chuột.", 0.35),
        ("Hãy giữ lại hai yếu tố tiềm ẩn.", 0.30),
        ("Yếu tố thứ nhất là xu hướng thích thiết bị; yếu tố thứ hai là thích phụ kiện.", 0.35),
        ("Đây là cách diễn giải; thuật toán không tự đặt tên cho yếu tố.", 0.50),
    ]),
    (11, [
        ("Sau khi giữ k yếu tố, hệ thống tính ma trận xấp xỉ R mũ.", 0.30),
        ("R mũ bằng U con k, nhân Sigma con k, nhân V chuyển vị con k.", 0.35),
        ("Ma trận xấp xỉ lấp những ô trống bằng điểm dự đoán.", 0.30),
        ("Các ô đã có được tái tạo gần đúng; sai số càng nhỏ càng tốt.", 0.35),
        ("Với An, hệ thống dự đoán AirPods khoảng bốn phẩy tám, Sony khoảng bốn phẩy sáu.", 0.35),
        ("Điểm này chỉ minh họa; kết quả thực tế phụ thuộc dữ liệu và huấn luyện.", 0.50),
    ]),
    (12, [
        ("Có thể hình dung quy trình gồm năm bước.", 0.30),
        ("Một: thu thập dữ liệu. Hai: xây dựng ma trận người dùng – sản phẩm.", 0.35),
        ("Ba: huấn luyện tìm vector tiềm ẩn. Bốn: dự đoán điểm cho sản phẩm chưa tương tác.", 0.35),
        ("Năm: xếp hạng và chọn Top N sản phẩm để gợi ý.", 0.35),
        ("Điểm dự đoán có dạng: r mũ bằng mu, cộng b-u, cộng b-i, cộng q-i chuyển vị nhân p-u.", 0.40),
        ("Mu là trung bình chung; b-u, b-i là độ lệch người dùng và sản phẩm; p-u, q-i là vector tiềm ẩn.", 0.35),
        ("Tích vô hướng q-i chuyển vị nhân p-u đo mức tương thích giữa người dùng và sản phẩm.", 0.50),
    ]),
    (13, [
        ("Lý thuyết là vậy. Giờ xem một lập trình viên triển khai thế nào.", 0.35),
        ("Thư viện Surprise hỗ trợ xây dựng hệ thống gợi ý từ dữ liệu đánh giá.", 0.35),
        ("Cài đặt bằng pip install scikit-surprise và pandas.", 0.35),
        ("Dữ liệu chỉ cần ba cột: mã người dùng, mã sản phẩm, điểm đánh giá.", 0.35),
        ("Ta khởi tạo S-V-D với hai yếu tố tiềm ẩn, một trăm vòng huấn luyện, tốc độ học không phẩy không không năm, điều chuẩn không phẩy không hai.", 0.40),
        ("Gọi fit để huấn luyện; gọi predict để dự đoán điểm của An cho AirPods.", 0.35),
        ("Hàm gợi ý duyệt sản phẩm chưa đánh giá, dự đoán điểm, sắp xếp giảm dần, lấy Top N.", 0.35),
        ("S-V-D của Surprise tối ưu trên các đánh giá đã biết; nó không điền số 0 rồi chạy S-V-D thông thường.", 0.50),
    ]),
    (14, [
        ("Mô hình chạy được chưa chắc đã tốt. Ta cần đo sai số dự đoán.", 0.35),
        ("R-M-S-E là căn bậc hai của trung bình bình phương sai số.", 0.35),
        ("M-A-E là trung bình giá trị tuyệt đối của sai số.", 0.35),
        ("Ba mô hình có R-M-S-E lần lượt: không phẩy chín lăm, không phẩy bảy tám, không phẩy sáu hai.", 0.40),
        ("Theo R-M-S-E, mô hình thứ ba tốt nhất, vì sai số thấp nhất.", 0.35),
        ("Tuy vậy, R-M-S-E thấp chưa chắc Top N đã tốt; có thể đánh giá thêm Precision, Recall, F1.", 0.50),
    ]),
    (15, [
        ("Trong dự án thật, mô hình gợi ý thường đứng sau kiến trúc như thế này.", 0.35),
        ("Frontend hiển thị; Backend xử lý nghiệp vụ; cơ sở dữ liệu lưu lịch sử tương tác.", 0.35),
        ("Dịch vụ Machine Learning bằng Python huấn luyện và dự đoán; thêm cache để tăng tốc.", 0.35),
        ("Khi người dùng mở trang, Backend gọi: GET /api/recommendations/An.", 0.35),
        ("Dịch vụ trả về JSON gồm mã sản phẩm và điểm dự đoán.", 0.35),
        ("Backend dùng mã đó để lấy tên, giá, hình ảnh và hiển thị danh sách.", 0.35),
        ("S-V-D không quản lý giao diện, giỏ hàng hay thanh toán; nó chỉ phân tích dữ liệu và dự đoán sở thích.", 0.50),
    ]),
    (16, [
        ("Vậy khi nào nên dùng S-V-D?", 0.30),
        ("Ưu điểm: khám phá sở thích tiềm ẩn, giảm số chiều, dự đoán sản phẩm chưa đánh giá.", 0.35),
        ("Hạn chế: cần dữ liệu tương tác, cần thời gian huấn luyện, chất lượng phụ thuộc dữ liệu.", 0.35),
        ("Một vấn đề quan trọng là Cold Start.", 0.35),
        ("Cold Start xảy ra khi người dùng hoặc sản phẩm mới chưa đủ dữ liệu.", 0.35),
        ("Khi đó S-V-D không đủ lịch sử để suy ra sở thích.", 0.35),
        ("Cách xử lý: dùng độ phổ biến, khai thác thông tin danh mục, hoặc hỏi sở thích ban đầu.", 0.40),
        ("Và thường kết hợp nhiều phương pháp.", 0.50),
    ]),
    (17, [
        ("Cuối cùng, phân biệt hai khái niệm dễ nhầm.", 0.30),
        ("Collaborative Filtering là phương pháp gợi ý dựa trên hành vi nhiều người dùng.", 0.35),
        ("S-V-D là kỹ thuật phân rã ma trận, tìm cấu trúc tiềm ẩn trong dữ liệu.", 0.35),
        ("Nói ngắn: lọc cộng tác là phương pháp; S-V-D là công cụ bên trong phương pháp đó.", 0.40),
        ("Không phải mọi hệ thống lọc cộng tác đều dùng S-V-D; còn user-based và item-based.", 0.50),
    ]),
    (18, [
        ("Ba ý quan trọng nhất.", 0.30),
        ("Một: dữ liệu tương tác được biểu diễn thành ma trận người dùng – sản phẩm.", 0.35),
        ("Hai: S-V-D phân rã ma trận để tìm các yếu tố tiềm ẩn.", 0.35),
        ("Ba: từ mô hình đã học, dự đoán điểm các ô trống và xếp hạng để gợi ý.", 0.40),
        ("Nếu sản phẩm mới hoàn toàn, chưa ai đánh giá, em xử lý thế nào?", 0.50),
        ("Cảm ơn các bạn đã theo dõi. Hãy theo dõi kênh An Tech Academy để không bỏ lỡ bài sau.", 0.40),
        ("Hẹn gặp lại các bạn trong bài giảng sau.", 0.50),
    ]),
]

DISPLAY = {"S-V-D": "SVD", "R-M-S-E": "RMSE", "M-A-E": "MAE"}


def mk_subs(say):
    t = say
    for k, v in DISPLAY.items():
        t = t.replace(k, v)
    t = t.strip()
    if len(t) <= 54:
        return [t]
    lines, cur = [], ""
    for w in t.split():
        trial = (cur + " " + w).strip()
        if cur and len(trial) > 60:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    if len(lines) <= 3:
        return lines
    mid = len(lines) // 2
    return [" ".join(lines[:mid]), " ".join(lines[mid:])]


CUES = []
for scene, items in RAW:
    for i, (say, pause) in enumerate(items, 1):
        CUES.append(dict(id=f"s{scene:02d}c{i}", scene=scene, pause=pause,
                         say=say, subs=mk_subs(say)))

SCENE_CUES = {}
for c in CUES:
    SCENE_CUES.setdefault(c["scene"], []).append(c)

if __name__ == "__main__":
    print(len(CUES), "cues", len(RAW), "scenes")
    print(sum(len(c["say"].split()) for c in CUES), "words")
    for c in CUES[:8]:
        print(c["id"], c["subs"])
