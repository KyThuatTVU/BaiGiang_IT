# -*- coding: utf-8 -*-
"""Sinh manifest full (30 cue) + sample (8 cue) cho bài API."""
import json, os

ROOT = "D:/Edit/Baigiang_API"
FULL = ROOT + "/mau"

# id, scene, say, subs
CUES = [
    ("S01c1", "S01", "Chào các bạn! Chào mừng đến với An Tech Academy.",
     ["Chào các bạn!", "Chào mừng đến với An Tech Academy."]),
    ("S01c2", "S01", "Bạn bấm đặt món trên app, hai giây sau đã có thông báo xác nhận. Vậy ai đã nói chuyện với nhà bếp?",
     ["Bấm đặt món trên app, hai giây sau đã có xác nhận.", "Ai đã nói chuyện với nhà bếp?"]),
    ("S01c3", "S01", "Câu trả lời là API. Năm phút nữa, bạn sẽ hiểu nó là gì và chạy như thế nào.",
     ["Câu trả lời là API.", "Năm phút nữa, bạn sẽ hiểu nó chạy thế nào."]),

    ("S02c1", "S02", "Frontend là mặt tiền: nút bấm, danh sách sản phẩm. Backend là phía sau: xử lý nghiệp vụ, tính toán, lưu dữ liệu.",
     ["Frontend là mặt tiền: nút bấm, danh sách sản phẩm.", "Backend xử lý, tính toán, lưu dữ liệu."]),
    ("S02c2", "S02", "Hai bên ở hai thế giới khác nhau. Không có quy tắc chung, mỗi màn hình phải chép cứng dữ liệu. Đổi một cái giá là sửa cả chục chỗ.",
     ["Không có quy tắc chung, mỗi màn hình chép cứng dữ liệu.", "Đổi một cái giá là sửa cả chục chỗ."]),
    ("S02c3", "S02", "Nên cần một quầy giao dịch chung: bên này gửi yêu cầu, bên kia trả kết quả. Quầy đó chính là API.",
     ["Cần một quầy giao dịch chung:", "gửi yêu cầu — trả kết quả. Đó là API."]),

    ("S03c1", "S03", "API, viết tắt của Application Programming Interface, tiếng Việt là giao diện lập trình ứng dụng. Nghe to tát, nhưng hiểu đơn giản là bộ quy tắc để hai phần mềm nói chuyện.",
     ["API — Application Programming Interface.", "Bộ quy tắc để hai phần mềm nói chuyện."]),
    ("S03c2", "S03", "Giống ổ cắm điện trong nhà. Bạn cắm phích là có điện, không cần biết nhà máy điện xây thế nào. API chính là ổ cắm giữa các hệ thống.",
     ["Giống ổ cắm điện: cắm phích là có điện,", "không cần biết nhà máy điện xây thế nào."]),
    ("S03c3", "S03", "Ba đặc điểm: có quy tắc chung, có đầu vào và đầu ra, và giấu phần xử lý bên trong. Một API có thể phục vụ web, app điện thoại và app quản trị cùng lúc.",
     ["Có quy tắc chung, có đầu vào — đầu ra,", "và giấu phần xử lý bên trong."]),

    ("S04c1", "S04", "Dễ nhất là ví dụ nhà hàng. Bạn là khách, tức Client. Anh bồi bàn là API. Phiếu gọi món là Request. Nhà bếp là Backend. Món bưng ra là Response.",
     ["Khách = Client · Bồi bàn = API · Phiếu = Request",
      "Bếp = Backend · Món bưng ra = Response"]),
    ("S04c2", "S04", "Bạn gọi cơm gà. Bồi bàn ghi phiếu, chuyển xuống bếp. Bếp kiểm tra nguyên liệu, nấu chín, trao lại. Bồi bàn bưng ra bàn cho bạn.",
     ["Bồi bàn ghi phiếu, chuyển xuống bếp.", "Bếp nấu xong, bồi bàn bưng ra."]),
    ("S04c3", "S04", "Nhớ kỹ: anh bồi bàn không nấu ăn. API cũng không tự xử lý nghiệp vụ. Nó là người đưa thư: đúng người, đúng món, đúng lúc.",
     ["Bồi bàn không nấu ăn — API không tự xử lý nghiệp vụ.", "Nó là người đưa thư: đúng người, đúng món."]),

    ("S05c1", "S05", "Endpoint là địa chỉ cụ thể để gửi yêu cầu. Nhà hàng có nhiều quầy: quầy món ăn, quầy đồ uống. API có nhiều endpoint: sản phẩm, đơn hàng, người dùng.",
     ["Endpoint là địa chỉ cụ thể để gửi yêu cầu.", "API có nhiều endpoint: sản phẩm, đơn hàng, người dùng."]),
    ("S05c2", "S05", "Bóc một địa chỉ nhé: https là giao thức, example chấm com là tên miền, api là khu vực API, products là tài nguyên, còn số 1 là mã sản phẩm.",
     ["https = giao thức · example.com = tên miền", "api/products = tài nguyên · 1 = mã sản phẩm"]),
    ("S05c3", "S05", "Một API gồm nhiều endpoint. Endpoint là cái cửa; HTTP method là việc bạn muốn làm ở cái cửa đó.",
     ["Endpoint là cái cửa.", "HTTP method là việc bạn muốn làm ở cửa đó."]),

    ("S06c1", "S06", "Request là lá phiếu gửi đi. Nó có bốn phần: method, URL, headers và body.",
     ["Request là lá phiếu gửi đi.", "Bốn phần: method · URL · headers · body."]),
    ("S06c2", "S06", "Method là hành động. URL là địa chỉ. Headers là giấy tờ tùy thân, ví dụ token đăng nhập. Body là nội dung, thường là JSON.",
     ["Method = hành động · URL = địa chỉ", "Headers = giấy tờ · Body = nội dung (JSON)"]),
    ("S06c3", "S06", "Nhìn một request thật: POST tới api products, Content-Type là application JSON, body gồm tên, giá, số lượng. Bếp đọc phiếu là biết phải nấu gì.",
     ["POST /api/products · Content-Type: application/json", "Body: tên, giá, số lượng"]),

    ("S07c1", "S07", "Bốn method quen thuộc: GET lấy dữ liệu, POST tạo mới, PUT cập nhật toàn bộ, DELETE xóa. Chỉ sửa một trường? Dùng PATCH.",
     ["GET lấy · POST tạo · PUT thay thế · DELETE xóa", "Chỉ sửa một trường: PATCH"]),
    ("S07c2", "S07", "Bốn thao tác đó chính là CRUD: Create, Read, Update, Delete.",
     ["Đó chính là CRUD:", "Create · Read · Update · Delete"]),
    ("S07c3", "S07", "Server trả mã trạng thái: 200 là OK, 201 đã tạo, 400 gửi sai, 401 chưa đăng nhập, 404 không tìm thấy, 500 server lỗi. Nhìn mã là biết chuyện gì.",
     ["200 OK · 201 Created · 400 sai · 401 chưa đăng nhập", "404 không thấy · 500 server lỗi"]),

    ("S08c1", "S08", "Response cũng ba phần: mã trạng thái, headers và body. Body thường là JSON, văn bản dễ đọc cho cả người lẫn máy.",
     ["Response: status · headers · body.", "Body thường là JSON — dễ đọc cho người và máy."]),
    ("S08c2", "S08", "JSON có string, number, boolean, null, object và array. Danh sách sản phẩm là một array gồm nhiều object.",
     ["JSON: string · number · boolean · null · object · array", "Danh sách = array các object"]),
    ("S08c3", "S08", "JavaScript có JSON điểm stringify để đóng gói, và JSON điểm parse để mở ra. Gửi đi thì stringify, nhận về thì parse.",
     ["JSON.stringify để đóng gói", "JSON.parse để mở ra"]),

    ("S09c1", "S09", "Thực chiến với Node.js và Express.js. Khai báo app, bật express json, viết route app get cho api products, rồi trả về res json. Chưa tới hai chục dòng.",
     ["Node.js + Express.js: app.get(\"/api/products\")", "res.json(...) — chưa tới 20 dòng"]),
    ("S09c2", "S09", "Chạy node server điểm js, mở localhost 3000 trên api products là thấy danh sách. Thử POST bằng Postman hoặc Thunder Client, vì trình duyệt chỉ gửi GET.",
     ["Mở localhost:3000/api/products là thấy JSON.", "Thử POST bằng Postman hoặc Thunder Client."]),
    ("S09c3", "S09", "Phía frontend, Fetch API gọi endpoint, await response json, rồi đổ dữ liệu lên giao diện. Frontend không cần biết bên kia dùng MySQL hay mảng tạm.",
     ["fetch(endpoint) → await response.json()", "Frontend không cần biết backend lưu ở đâu."]),

    ("S10c1", "S10", "Vài lỗi hay gặp: quên bật express json nên body rỗng; quên cấu hình CORS nên trình duyệt chặn; và tin dữ liệu frontend mà không kiểm tra ở backend.",
     ["Quên express.json → body rỗng.", "Quên CORS → trình duyệt chặn."]),
    ("S10c2", "S10", "Nhớ ba điều: API là cầu nối, endpoint là địa chỉ, method cộng status code là ngôn ngữ chung. Request đi, response về, JSON ở giữa.",
     ["API = cầu nối · Endpoint = địa chỉ", "Method + status code = ngôn ngữ chung"]),
    ("S10c3", "S10", "Hiểu API là bạn đã mở cửa bước sang backend. Còn RESTful, xác thực JWT và bảo mật API, mình sẽ nói ở bài sau.",
     ["Hiểu API là mở cửa bước sang backend.", "RESTful, JWT và bảo mật API — bài sau."]),

    ("S11c1", "S11", "Cảm ơn các bạn đã theo dõi An Tech Academy. Hiểu công nghệ, làm chủ tương lai!",
     ["Cảm ơn các bạn đã theo dõi An Tech Academy.", "Hiểu công nghệ, làm chủ tương lai!"]),
    ("S11c2", "S11", "Nhớ theo dõi kênh và để lại câu hỏi nha. Hẹn gặp lại ở bài tiếp theo.",
     ["Nhớ theo dõi kênh và để lại câu hỏi nha.", "Hẹn gặp lại!"]),
]

SAMPLE_IDS = ["S01c1", "S01c2", "S01c3", "S04c1", "S04c2"]
SAMPLE = [row for row in CUES if row[0] in SAMPLE_IDS]


def build(rows, path):
    out = []
    for i, (cid, sid, text, subs) in enumerate(rows):
        prev = rows[i - 1] if i else None
        pause = 0.18
        if prev and prev[1] != sid:
            pause = 0.45
        out.append({
            "id": cid, "scene": sid, "rate": "+18%", "shift": 0.0,
            "pause_after": pause, "text": text, "say": text, "subs": subs,
        })
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(os.path.basename(path), len(out), "cues", sum(len(r[2]) for r in rows), "chars")


if __name__ == "__main__":
    os.makedirs(FULL, exist_ok=True)
    build(CUES, FULL + "/manifest.json")
    build(SAMPLE, FULL + "/manifest_sample.json")
