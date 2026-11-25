# -*- coding: utf-8 -*-
"""Manifest Cổng A v2 — bản rút gọn mục tiêu 7:40, giọng NamMinh +18%."""
SCENES = [
 ("S01","P1","Mở đầu thương hiệu",[
   ("S01c1","Xin chào các bạn! Chào mừng các bạn đến với An Tech Academy – nơi cùng nhau học công nghệ và làm chủ tương lai."),
   ("S01c2","Hôm nay chúng ta cùng tìm hiểu cách ứng dụng hiện đại chia sẻ dữ liệu theo thời gian thực.")]),
 ("S02","P1","Tình huống ba người dùng",[
   ("S02c1","Hãy tưởng tượng một nhóm sinh viên cùng làm việc trên một bảng ghi chú trực tuyến. Bạn A vừa cập nhật nội dung, nhưng bạn B vẫn thấy dữ liệu cũ, còn bạn C phải tải lại trang.")]),
 ("S03","P1","Câu hỏi và tên bài toán",[
   ("S03c1","Vậy làm sao để mọi người thấy dữ liệu mới ngay khi có người cập nhật, mà không cần tải lại trang?"),
   ("S03c2","Đây chính là bài toán đồng bộ dữ liệu thời gian thực – Real-time Data Synchronization.")]),
 ("S04","P1","Lộ trình bài học",[
   ("S04c1","Bài học hôm nay gồm bốn phần: cơ chế hoạt động, truyền dữ liệu giữa Client và Server, xử lý xung đột và thực hành với Node.js, Socket.IO.")]),
 ("S05","P2","Định nghĩa",[
   ("S05c1","Đồng bộ dữ liệu thời gian thực là gì?"),
   ("S05c2","Đây là cơ chế giúp nhiều thiết bị nhận thay đổi dữ liệu gần như ngay lập tức khi có người cập nhật.")]),
 ("S06","P2","Luồng đồng bộ",[
   ("S06c1","Khi A thay đổi ghi chú, hệ thống nhận dữ liệu, xử lý tại máy chủ và gửi cập nhật đến những người đang kết nối."),
   ("S06c2","Nhờ vậy, ai đang mở ứng dụng cũng thấy bản mới nhất.")]),
 ("S07","P2","HTTP Request – Response",[
   ("S07c1","Có hai cơ chế truyền thông phổ biến. Thứ nhất là HTTP Request – Response."),
   ("S07c2","Với HTTP, trình duyệt gửi yêu cầu, máy chủ trả kết quả. Muốn biết dữ liệu đổi chưa, phải gửi yêu cầu mới.")]),
 ("S08","P2","Polling",[
   ("S08c1","Ví dụ, cứ năm giây một lần, website gọi API để kiểm tra dữ liệu. Cách này gọi là Polling.")]),
 ("S09","P2","WebSocket",[
   ("S09c1","Thứ hai là WebSocket – kết nối hai chiều giữa Client và Server."),
   ("S09c2","Sau khi kết nối, hai bên gửi dữ liệu cho nhau mà không cần yêu cầu HTTP mới cho từng lần cập nhật.")]),
 ("S10","P2","Socket.IO",[
   ("S10c1","Trong bài thực hành, chúng ta dùng Socket.IO – thư viện giao tiếp thời gian thực theo sự kiện."),
   ("S10c2","Socket.IO thường dùng WebSocket khi có thể, kèm cơ chế dự phòng.")]),
 ("S11","P2","Bốn bước",[
   ("S11c1","Quy trình gồm bốn bước."),
   ("S11c2","Client kết nối đến Server."),
   ("S11c3","Người dùng thực hiện thao tác cập nhật dữ liệu."),
   ("S11c4","Server tiếp nhận và xử lý dữ liệu."),
   ("S11c5","Server phát sự kiện đến các Client liên quan để cập nhật giao diện.")]),
 ("S12","P2","Server trung tâm",[
   ("S12c1","Server là trung tâm tiếp nhận và phân phối dữ liệu để mọi thiết bị cùng nhìn một trạng thái chung."),
   ("S12c2","Nếu không có máy chủ, mỗi trình duyệt chỉ thấy dữ liệu riêng của nó.")]),
 ("S13","P3","Ba khái niệm",[
   ("S13c1","Trước khi viết code, chúng ta cần nắm ba khái niệm.")]),
 ("S14","P3","Client – Server",[
   ("S14c1","Một là Client – Server."),
   ("S14c2","Client là phía người dùng, như trình duyệt trên máy tính hoặc điện thoại. Server nhận yêu cầu, xử lý và gửi kết quả trở lại.")]),
 ("S15","P3","Event và bảng sự kiện",[
   ("S15c1","Hai là Event. Trong Socket.IO, ta gửi và lắng nghe sự kiện."),
   ("S15c2","update-data: người dùng muốn cập nhật dữ liệu."),
   ("S15c3","sync-state: gửi trạng thái dữ liệu hiện tại."),
   ("S15c4","data-updated: báo dữ liệu vừa cập nhật."),
   ("S15c5","Nhờ vậy, hệ thống trao đổi dữ liệu linh hoạt.")]),
 ("S16","P3","Xung đột dữ liệu",[
   ("S16c1","Ba là xử lý xung đột – Conflict Resolution. Hai người cùng sửa một tài liệu gần như cùng lúc. Hệ thống chọn nội dung nào?")]),
 ("S17","P3","Last Write Wins",[
   ("S17c1","Một cách đơn giản là Last Write Wins – LWW: áp dụng bản cập nhật cuối theo thứ tự xác định, ví dụ thứ tự Server nhận.")]),
 ("S18","P3","Optimistic Locking",[
   ("S18c1","Cách khác là Optimistic Locking, dùng phiên bản dữ liệu để kiểm tra."),
   ("S18c2","Nếu dữ liệu đã đổi từ lúc người dùng đọc, hệ thống từ chối cập nhật và yêu cầu tải lại. OT và CRDT là kỹ thuật nâng cao, sẽ học ở bài sau.")]),
 ("S19","P4","Mục tiêu và khởi tạo",[
   ("S19c1","Bây giờ, chúng ta sẽ xây dựng ứng dụng SyncLab."),
   ("S19c2","Mục tiêu: khu vực ghi chú dùng chung. Khi A nhập và nhấn Gửi, trình duyệt B nhận thay đổi gần như ngay lập tức."),
   ("S19c3","Bước 1: khởi tạo dự án. Tạo thư mục synclab, mở Terminal và chạy các lệnh."),
   ("S19c4","npm init, gạch ngang y."),
   ("S19c5","npm install express socket chấm ai-âu.")]),
 ("S20","P4","Thư viện và cấu trúc",[
   ("S20c1","Express giúp xây máy chủ Web; socket.io hỗ trợ giao tiếp thời gian thực."),
   ("S20c2","Cấu trúc gồm server.js và thư mục public chứa index.html.")]),
 ("S21","P4","Code server: khởi tạo",[
   ("S21c1","Bước 2: xây dựng Server. Tạo file server.js và viết đoạn code sau."),
   ("S21c2","Khởi tạo Express và HTTP Server để Socket.IO dùng cùng máy chủ."),
   ("S21c3","sharedData lưu nội dung ghi chú và số phiên bản – trạng thái chung của ứng dụng.")]),
 ("S22","P4","Code server: kết nối và phát sự kiện",[
   ("S22c1","Khi Client kết nối, Server gửi trạng thái hiện tại bằng sync-state, để người mới thấy dữ liệu mới nhất."),
   ("S22c2","Khi nhận update-data, Server kiểm tra, cập nhật nội dung và tăng phiên bản, để chặn dữ liệu sai kiểu hoặc quá dài."),
   ("S22c3","Hàm emit của io phát data-updated đến tất cả Client, gồm cả người vừa gửi."),
   ("S22c4","Đây là bước giúp mọi trình duyệt nhận cùng một trạng thái.")]),
 ("S23","P4","Giao diện Client",[
   ("S23c1","Bước 3: xây dựng giao diện Client. Tạo file public/index.html."),
   ("S23c2","Giao diện gồm ô nhập, nút Gửi cập nhật và dòng số phiên bản."),
   ("S23c3","Client gọi hàm io để tạo kết nối với Server.")]),
 ("S24","P4","Code client",[
   ("S24c1","Khi nhận sync-state, trình duyệt hiển thị dữ liệu hiện tại; khi nhận data-updated, giao diện tự cập nhật nội dung và số phiên bản."),
   ("S24c2","Khi nhấn Gửi cập nhật, Client phát update-data kèm nội dung lên Server.")]),
 ("S25","P4","Hoàn thành demo",[
   ("S25c1","Chúng ta đã hoàn thành ứng dụng đồng bộ dữ liệu thời gian thực cơ bản."),
   ("S25c2","Hai trình duyệt giờ đây chia sẻ cùng một ghi chú.")]),
 ("S26","P5","Chạy thử",[
   ("S26c1","Bây giờ, hãy kiểm tra kết quả. Tại Terminal, chạy node, file server chấm giây-ét."),
   ("S26c2","Sau đó, mở trình duyệt truy cập localhost, cổng ba nghìn."),
   ("S26c3","Mở thêm một tab hoặc trình duyệt khác cùng địa chỉ.")]),
 ("S27","P5","Demo cập nhật",[
   ("S27c1","Ở trình duyệt thứ nhất, nhập: \"Đây là dữ liệu cập nhật từ người dùng A\", rồi nhấn Gửi cập nhật."),
   ("S27c2","Ngay lập tức, trình duyệt thứ hai nhận nội dung mới mà không cần tải lại trang."),
   ("S27c3","Số phiên bản cũng tăng sau mỗi lần cập nhật.")]),
 ("S28","P5","Phía sau",[
   ("S28c1","Vậy điều gì đã xảy ra phía sau?"),
   ("S28c2","Client A gửi update-data lên Server. Server cập nhật dữ liệu, tăng phiên bản và phát data-updated đến mọi Client."),
   ("S28c3","Client B nhận sự kiện và đổi nội dung trên giao diện."),
   ("S28c4","Đó là luồng đồng bộ thời gian thực, có thể ứng dụng vào nhiều hệ thống.")]),
 ("S29","P5","Ứng dụng thực tế",[
   ("S29c1","Trong thực tế, cơ chế này dùng cho quản lý công việc, khi nhiều người theo dõi trạng thái nhiệm vụ."),
   ("S29c2","Website bán hàng cập nhật đơn hàng, tồn kho; quản lý lớp học cập nhật danh sách, kết quả; ứng dụng trò chuyện gửi nhận tin nhắn."),
   ("S29c3","Trong giáo dục, học sinh cùng làm bài nhóm trực tuyến.")]),
 ("S30","P5","Giới hạn",[
   ("S30c1","Lưu ý: ví dụ này lưu dữ liệu trong RAM, khởi động lại Server sẽ mất."),
   ("S30c2","Hệ thống thực tế cần MySQL hoặc PostgreSQL để lưu lâu dài."),
   ("S30c3","Cần thêm xác thực người dùng, kiểm tra quyền, xử lý mất kết nối và kiểm soát xung đột."),
   ("S30c4","Quan trọng: Socket.IO truyền nhanh nhưng không tự đảm bảo nhất quán. Điều đó phụ thuộc logic xử lý và lưu trữ phía Server.")]),
 ("S31","P6","Ưu điểm",[
   ("S31c1","Đồng bộ thời gian thực mang lại nhiều lợi ích."),
   ("S31c2","Thứ nhất, dữ liệu cập nhật gần như tức thì, nâng cao trải nghiệm người dùng."),
   ("S31c3","Thứ hai, nhiều Client cùng theo dõi một trạng thái mà không cần tải lại trang."),
   ("S31c4","Thứ ba, Socket.IO giúp xây ứng dụng tương tác thời gian thực dễ dàng.")]),
 ("S32","P6","Hạn chế",[
   ("S32c1","Thứ nhất, quản lý nhiều kết nối đồng thời có thể gây áp lực lên máy chủ."),
   ("S32c2","Thứ hai, cần cơ chế phục hồi khi mất kết nối hoặc xung đột dữ liệu."),
   ("S32c3","Thứ ba, nhiều máy chủ cần thêm giải pháp chia sẻ trạng thái và phân phối sự kiện."),
   ("S32c4","Khi số người dùng tăng, chi phí hạ tầng cũng tăng theo.")]),
 ("S33","P6","Tổng kết",[
   ("S33c1","Tóm lại, chúng ta đã hiểu đồng bộ thời gian thực, phân biệt HTTP và WebSocket, nắm Client – Server và Event trong Socket.IO."),
   ("S33c2","Đồng thời, chúng ta đã biết cách xử lý xung đột dữ liệu.")]),
 ("S34","P6","Bài tập và kết thúc",[
   ("S34c1","Bài tập: phát triển SyncLab thành bảng quản lý công việc, nhiều người thêm, sửa, cập nhật trạng thái; lưu vào MySQL và kiểm soát phiên bản."),
   ("S34c2","Hy vọng bài học giúp các bạn hiểu rõ cách xây dựng ứng dụng Web thời gian thực. Cảm ơn các bạn đã theo dõi!"),
   ("S34c3","Hẹn gặp lại trong bài học tiếp theo. AN TECH ACADEMY – HỌC CÔNG NGHỆ, LÀM CHỦ TƯƠNG LAI!")]),
]

CPS, GAP, TAIL, XFADE = 15.73, 0.22, 1.10, 0.30

def build():
    out, t = [], 0.0
    for sid, part, title, cues in SCENES:
        start = t
        rows = []
        for i,(cid,text) in enumerate(cues):
            if i: t += GAP
            d = len(text)/CPS
            rows.append((cid, t-start, d, text))
            t += d
        out.append((sid, part, title, start, t-start, rows))
        t += TAIL
    total = t - TAIL + 1.10 - XFADE*(len(SCENES)-1)
    return out, total

def emit(scenes, total, out_dir):
    import json
    manifest, timeline = [], {"total": round(total, 3), "scenes": [], "params":
                             {"cps": CPS, "gap": GAP, "tail": TAIL, "xfade": XFADE}}
    for sid, part, title, st, dur, rows in scenes:
        timeline["scenes"].append({"id": sid, "part": part, "title": title,
                                   "start": round(st, 3), "dur": round(dur, 3),
                                   "cues": [{"id": cid, "offset": round(off, 3),
                                             "dur": round(d, 3)} for cid, off, d, _ in rows]})
        for cid, _off, _d, text in rows:
            manifest.append({"id": cid, "scene": sid, "text": text, "rate": "+18%"})
    with open(out_dir + "/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    with open(out_dir + "/timeline.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    import os, sys
    scenes, total = build()
    def mmss(s): return f"{int(s//60)}:{int(s%60):02d}"
    for sid, part, title, st, dur, rows in scenes:
        print(f"{sid} {mmss(st)}-{mmss(st+dur)} ({dur:5.1f}s) {title}")
        for cid, off, d, text in rows:
            print(f"    {cid} +{off:5.1f} {d:4.1f}s {text[:60]}")
    n=sum(len(s[5]) for s in scenes); ch=sum(len(c[3]) for s in scenes for c in s[5])
    print(f"TOTAL video {mmss(total)} ({total:.1f}s) scenes={len(scenes)} cues={n} chars={ch} audio_est={ch/CPS:.1f}")
    if "--emit" in sys.argv:
        out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        emit(scenes, total, out)
        print(f"EMITTED {out}/manifest.json + timeline.json")
