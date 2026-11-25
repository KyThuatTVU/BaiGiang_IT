# -*- coding: utf-8 -*-
"""Manifest 26 cue cho bài giảng Load Balancer (~5 phút).
say = bản tối ưu cho TTS (phiên âm thuật ngữ CNTT); subs = phụ đề hiển thị đúng chính tả.
rate/shift tạo nhịp điệu: câu hỏi & câu đùa nhanh + cao hơn, định nghĩa chậm + trầm hơn."""
import json, os

ROOT = "D:/Edit/Baigiang_LoadBalancer"
OUT = ROOT + "/mau/manifest.json"

PRON = [
    # dài trước, ngắn sau
    ("Weighted Round Robin", "quây-tịt rao rô-bin"),
    ("Least Connections", "lít cơ-néc-sần"),
    ("Horizontal Scaling", "hô-ri-dôn-tồ sờ-kei-ling"),
    ("Load Balancer", "Lâu Ba-lăn-sơ"),
    ("Load balancing", "Lâu Ba-lăn-sing"),
    ("Health Check", "hen chéc"),
    ("Round Robin", "rao rô-bin"),
    ("IP Hash", "ai-pi hát"),
    ("Backend Server", "béc-en sơ-vơ"),
    ("Server 01", "sơ-vơ không một"),
    ("Server 02", "sơ-vơ không hai"),
    ("Server 03", "sơ-vơ không ba"),
    ("An Tech Academy", "An Tếch A-ca-đê-mi"),
    ("Server", "sơ-vơ"),
    ("Backend", "béc-en"),
    ("Client", "cờ-lai-ần"),
    ("Request", "Ri-quét"),
    ("request", "ri-quét"),
    ("Database", "đây-ta-bây"),
    ("endpoint", "en-đờ-po-en"),
    ("upstream", "ắp-strim"),
    ("location", "lô-cây-sần"),
    ("Nginx", "en-gin-ích"),
    ("HAProxy", "hát-prô-xi"),
    ("HTTP", "hát-tê-tê-pê"),
    ("CPU", "xê-pê-u"),
    ("SQL", "ét-kiu-el"),
    ("IP", "ai-pi"),
    ("RAM", "ram"),
]

# id, scene, rate, semitone, pause_after, text (hiển thị), subs (2 dòng)
CUES = [
    ("S01c1", "S01", "+15%", 1.0, 0.25,
     "Chào các bạn! Chào mừng đến với An Tech Academy. Mình hỏi thật nhé: mười hai giờ đêm mười hai tháng mười hai, cả sàn thương mại điện tử giảm giá, bạn có đoán được chuyện gì xảy ra không?",
     ["Chào các bạn! Chào mừng đến với An Tech Academy.",
      "12 giờ đêm 12/12, cả sàn giảm giá — chuyện gì sẽ xảy ra?"]),

    ("S01c2", "S01", "+13%", 0.5, 0.20,
     "Một ngày, một trăm mười nghìn lượt truy cập. Cao điểm, năm nghìn người cùng lúc. Ai cũng bấm mua, ai cũng sợ hết hàng.",
     ["110.000 lượt truy cập một ngày. Cao điểm:",
      "5.000 người cùng lúc — ai cũng bấm mua."]),

    ("S01c3", "S01", "+11%", 0.3, 0.35,
     "Và rồi, web sập. Không phải vì hết hàng, mà vì máy chủ không kham nổi. Cứu tinh của chúng ta hôm nay là Load Balancer.",
     ["Và rồi web sập — không phải vì hết hàng,",
      "mà vì máy chủ không kham nổi. Cứu tinh: Load Balancer."]),

    ("S02c1", "S02", "+10%", 0.0, 0.25,
     "Nhìn màn hình này: CPU leo dốc, RAM đầy, thời gian phản hồi kéo dài. Một máy chủ phải gánh năm nghìn kết nối cùng lúc, nghe thôi đã thấy mệt.",
     ["CPU leo dốc, RAM đầy, phản hồi kéo dài.",
      "Một máy chủ gánh 5.000 kết nối — nghe thôi đã mệt."]),

    ("S02c2", "S02", "+12%", 0.2, 0.35,
     "Khách vào không được, bấm thanh toán thì báo lỗi. Mỗi giây chậm là một đơn hàng bay mất. Thêm CPU, thêm RAM ư? Đỡ được một chút, rồi lại chạm trần. Câu hỏi đặt ra: làm sao phục vụ hàng nghìn người mà không bắt một máy chủ gánh hết?",
     ["Khách không vào được, thanh toán báo lỗi.",
      "Nâng cấp một máy? Đỡ chút rồi chạm trần — cần cách khác."]),

    ("S03c1", "S03", "+8%", -0.2, 0.30,
     "Load Balancer, tức bộ cân bằng tải, là nhân viên điều phối đứng trước cửa hệ thống. Nó nhận mọi yêu cầu, rồi chia việc cho nhiều máy chủ phía sau.",
     ["Load Balancer là 'nhân viên điều phối' trước cửa hệ thống:",
      "nhận yêu cầu và chia việc cho nhiều máy chủ phía sau."]),

    ("S03c2", "S03", "+13%", 0.7, 0.35,
     "Giống siêu thị ngày sale: một quầy thì xếp hàng dài, mở thêm quầy và có người chỉ khách vào quầy trống, ai cũng nhanh hơn. Nhưng nhớ nhé, nó chỉ điều phối, không tự bán hàng đâu.",
     ["Như siêu thị ngày sale: mở thêm quầy và có người",
      "chỉ khách vào quầy trống. Nó điều phối, không bán hàng."]),

    ("S04c1", "S04", "+7%", -0.3, 0.30,
     "Kiến trúc chuẩn gồm bốn lớp. Một, Client là người dùng. Hai, Load Balancer là cửa ngõ. Ba, các Backend Server xử lý nghiệp vụ. Bốn, Database lưu dữ liệu.",
     ["Kiến trúc 4 lớp: Client → Load Balancer",
      "→ các Backend Server → Database."]),

    ("S04c2", "S04", "+10%", 0.0, 0.30,
     "Một request đi từ trình duyệt, qua Load Balancer, xuống Server 01, truy vấn Database rồi trả kết quả về. Request tiếp theo sang Server 02, rồi 03. Không máy nào phải gồng một mình. Mô hình bốn lớp này là nền móng của rất nhiều hệ thống thật.",
     ["Trình duyệt → Load Balancer → Server 01 → Database → trả kết quả.",
      "Request sau sang Server 02, 03. Không máy nào gồng một mình."]),

    ("S05c1", "S05", "+9%", 0.0, 0.25,
     "Đây là Horizontal Scaling, mở rộng theo chiều ngang. Thay vì mua một siêu máy chủ đắt gấp mười, bạn thêm vài máy chủ bình thường, chạy song song.",
     ["Horizontal Scaling: thêm nhiều máy chủ bình thường",
      "thay vì mua một siêu máy chủ đắt gấp mười."]),

    ("S05c2", "S05", "+14%", 0.8, 0.35,
     "Một máy ốm thì hai máy còn chạy. Hệ thống vừa khỏe hơn, vừa rẻ hơn, lại dễ nâng cấp từng bước. Quá hợp lý còn gì!",
     ["Một máy ốm, hai máy vẫn chạy.",
      "Khỏe hơn, rẻ hơn, dễ nâng cấp từng bước."]),

    ("S06c1", "S06", "+10%", 0.2, 0.25,
     "Vậy chia việc kiểu gì? Thuật toán đầu tiên dễ như phát bài: Round Robin. Request một về Server 01, hai về 02, ba về 03, bốn quay lại 01.",
     ["Round Robin — chia lần lượt như phát bài:",
      "01 → 02 → 03 → quay lại 01."]),

    ("S06c2", "S06", "+14%", 0.8, 0.35,
     "Cứ xoay vòng đều đặn, hết vòng lại quay về đầu. Hợp khi ba máy cấu hình như nhau. Nhưng nếu Server 01 khỏe hơn hẳn, chia đều kiểu này là bắt nó chạy chậm lại cho công bằng. Nghe sai sai đúng không?",
     ["Hợp khi các máy cấu hình như nhau.",
      "Máy khỏe hơn mà chia đều — nghe sai sai đúng không?"]),

    ("S07c1", "S07", "+9%", 0.2, 0.25,
     "Thế là có Weighted Round Robin, luân phiên có trọng số. Máy khỏe nhận nhiều việc hơn. Server 01 trọng số ba, hai máy còn lại trọng số một.",
     ["Weighted Round Robin — máy khỏe nhận nhiều việc hơn:",
      "Server 01 w=3, Server 02 w=1, Server 03 w=1."]),

    ("S07c2", "S07", "+14%", 0.9, 0.35,
     "Nghĩa là trong năm request, Server 01 nhận ba, hai bạn còn lại mỗi bạn một. Đúng sức, đúng việc, khỏi cãi nhau!",
     ["5 request: Server 01 nhận 3, hai máy kia mỗi máy 1.",
      "Đúng sức, đúng việc — khỏi cãi nhau."]),

    ("S08c1", "S08", "+9%", 0.1, 0.25,
     "Nhưng có lúc request nặng nhẹ khác nhau. Lúc đó Least Connections phát huy: nhìn xem máy nào đang rảnh nhất.",
     ["Least Connections: chọn máy đang ít kết nối nhất.",
      "Request nặng nhẹ khác nhau thì cách này rất hợp."]),

    ("S08c2", "S08", "+13%", 0.7, 0.35,
     "Server 01 đang giữ một trăm kết nối, Server 02 ba mươi, Server 03 chỉ mười. Request tiếp theo đi đâu? Chắc chắn về Server 03. Ai rảnh thì làm, quá công bằng. Đây là lúc chữ cân bằng có ý nghĩa thật sự.",
     ["Server 01: 100 kết nối, Server 02: 30, Server 03: 10.",
      "Request tiếp theo → Server 03. Ai rảnh thì làm."]),

    ("S09c1", "S09", "+8%", 0.0, 0.30,
     "Còn IP Hash thì băm địa chỉ IP của khách để chọn máy chủ. Cùng một IP thường vào cùng một máy, rất tiện cho giỏ hàng và phiên đăng nhập.",
     ["IP Hash: băm địa chỉ IP để chọn máy chủ.",
      "Cùng IP → cùng máy: tiện cho giỏ hàng, phiên đăng nhập."]),

    ("S09c2", "S09", "+11%", 0.3, 0.35,
     "Nhưng đừng thần thánh hóa nó. Đổi cấu hình, thêm bớt máy chủ, khách có thể nhảy sang máy khác. Không có thuật toán nào hoàn hảo cho mọi bài toán.",
     ["Nhưng đổi cấu hình hay thêm bớt máy chủ,",
      "khách có thể nhảy máy. Không thuật toán nào hoàn hảo."]),

    ("S10c1", "S10", "+13%", 0.6, 0.25,
     "Khoan đã, lỡ một máy chủ chết thì sao? Load Balancer vẫn chia đều vào cái máy đã tắt à? Không đâu, nó có Health Check.",
     ["Lỡ một máy chủ chết thì sao?",
      "Load Balancer có Health Check để xử lý chuyện này."]),

    ("S10c2", "S10", "+10%", 0.1, 0.40,
     "Định kỳ gọi vào endpoint health. Máy trả lời hai trăm thì khỏe, im lặng hoặc lỗi thì bị gạch tên khỏi danh sách. Sửa xong, vượt qua kiểm tra, lại được quay về đội.",
     ["Định kỳ gọi GET /health: trả 200 là khỏe.",
      "Lỗi hoặc im lặng → gạch tên. Sửa xong → quay lại đội."]),

    ("S11c1", "S11", "+9%", 0.0, 0.25,
     "Trong thực tế, Nginx, HAProxy hay cloud load balancer đều làm được. Nhìn cấu hình Nginx này: khai báo upstream gồm ba địa chỉ backend.",
     ["Nginx, HAProxy hay cloud đều cân bằng tải được.",
      "Cấu hình Nginx: upstream gồm 3 địa chỉ backend."]),

    ("S11c2", "S11", "+8%", -0.2, 0.40,
     "Server block lắng nghe cổng tám mươi, location gốc chuyển tiếp vào upstream. Thế là xong một tầng cân bằng tải gọn gàng.",
     ["server { listen 80; location / { proxy_pass ... } }",
      "Một tầng cân bằng tải gọn gàng chỉ với vài dòng."]),

    ("S12c1", "S12", "+10%", 0.0, 0.30,
     "Nhưng này, Load Balancer không phải cây đũa thần. Database quá tải, câu SQL chậm, cổng thanh toán lỗi, thì web vẫn ì ạch như thường.",
     ["Load Balancer không phải cây đũa thần:",
      "Database quá tải, SQL chậm, thanh toán lỗi → vẫn ì ạch."]),

    ("S12c2", "S12", "+9%", -0.2, 0.35,
     "Còn phải lo phiên đăng nhập dùng chung, dữ liệu đồng bộ giữa các server, và chống đặt hàng trùng. Cân bằng tải chỉ là một mảnh ghép.",
     ["Còn phải lo phiên đăng nhập, đồng bộ dữ liệu,",
      "chống đặt hàng trùng. Cân bằng tải chỉ là một mảnh ghép."]),

    ("S12c3", "S12", "+13%", 0.8, 0.30,
     "Tóm lại: một cửa ngõ, nhiều máy chủ, bốn thuật toán, một cơ chế health check. Hiểu rồi thì hệ thống của bạn sẽ thở đều hơn hẳn. Cảm ơn các bạn đã học cùng An Tech Academy, hẹn gặp ở bài tiếp theo!",
     ["Một cửa ngõ · nhiều máy chủ · bốn thuật toán · health check.",
      "Cảm ơn các bạn — hẹn gặp ở bài tiếp theo!"]),
]


def apply_pron(t):
    for a, b in PRON:
        if a in t:
            t = t.replace(a, b)
    return t


def main():
    out = []
    for cid, scene, rate, semi, pause, text, subs in CUES:
        out.append({
            "id": cid, "scene": scene, "rate": rate, "shift": semi,
            "pause_after": pause, "text": text,
            "say": apply_pron(text), "subs": subs,
        })
    os.makedirs(ROOT + "/mau", exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    words = sum(len(c["text"].split()) for c in out)
    print(f"MANIFEST {len(out)} cues, {words} words, scenes={len(set(c['scene'] for c in out))}")


if __name__ == "__main__":
    main()
