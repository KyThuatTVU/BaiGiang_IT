# -*- coding: utf-8 -*-
"""Sinh manifest 24 cue cho bài giảng Bảo vệ mã nguồn (~5 phút).
say = bản tối ưu cho TTS (phiên âm thuật ngữ); subs = phụ đề hiển thị đúng chính tả."""
import json, os

ROOT = "D:/Edit/Biagiang_baomatmanguon"
OUT = ROOT + "/mau/manifest.json"

PRON = [
    ("An Tech Academy", "An Tếch A-ca-đê-mi"),
    ("BookingService.php", "Bu-king Sờ-vịt chấm pê-hát-pê"),
    ("Require all denied", "Ri-quai-ơ o đì-nai"),
    ("Directory Listing", "Đai-rếch-tơ-ri lít-ting"),
    ("Whitelist Routing", "Quai-lít rao-ting"),
    ("Front Controller", "Phờ-rông Con-trô-lơ"),
    ("DocumentRoot", "Đốc-kiu-mần-rút"),
    ("AllowOverride", "A-lao-âu-vơ-rai"),
    ("RewriteEngine On", "Ri-rait-en-gin on"),
    ("RewriteRule", "Ri-rait-run"),
    ("RewriteCond", "Ri-rait-còn"),
    ("FilesMatch", "Phai-sờ-mách"),
    ("FileMatch", "Phai-sờ-mách"),
    ("Options -Indexes", "Ốp-sần, trừ in-đếch-sờ"),
    ("Options trừ Indexes", "Ốp-sần, trừ in-đếch-sờ"),
    ("htaccess", "hờ-tắc-xét"),
    ("DevTools", "đép-tút"),
    ("Apache", "A-pa-chê"),
    ("mod rewrite", "mót ri-rait"),
    ("index.php", "in-đếch chấm pê-hát-pê"),
    ("403 Forbidden", "bốn không ba, pho-bít-đần"),
    ("404 Not Found", "bốn không bốn, nót phao"),
    ("XAMPP", "zăm"),
    ("MySQL", "mai ét-kiu-el"),
    ("PHP", "pê-hát-pê"),
    ("JSON", "dây-sần"),
    ("F12", "ép mười hai"),
    ("Ctrl Shift I", "cần-trố, sịp ai"),
    ("SQL", "ét-kiu-el"),
    (".env", "chấm en-vờ"),
    ("env", "en-vờ"),
    ("JavaScript", "ja-va-sờ-cờ-ríp"),
    ("SQL", "ét-kiu-el"),
    ("Network", "nết-uốc"),
    ("URL Rewrite", "u-rờ-el ri-rait"),
    ("URL", "u-rờ-el"),
    ("about", "ơ-bao"),
    ("include", "in-clu-đờ"),
    ("public", "pấp-lịch"),
    ("assets", "át-sét"),
    ("routes", "rút"),
    ("storage", "sto-rịch"),
    ("config", "con-phích"),
    ("frontend", "phờ-rôn-en"),
    ("router", "rao-tơ"),
    ("Router", "rao-tơ"),
    ("documentroot", "đốc-kiu-mần-rút"),
]

# id, scene, rate, semitone, pause_after, text (hiển thị), subs (2 dòng)
CUES = [
    ("S01c1", "S01", "+8%", 0.5, 0.20,
     "Xin chào các bạn! Chào mừng quay lại với An Tech Academy — học công nghệ cùng An. Hôm nay mình có một câu đố nhỏ dành cho bạn.",
     ["Xin chào các bạn! Chào mừng quay lại với An Tech Academy",
      "— học công nghệ cùng An. Hôm nay mình có một câu đố nhỏ."]),
    ("S01c2", "S01", "+10%", 0.7, 0.25,
     "Chỉ cần gõ thêm vài chữ vào thanh địa chỉ, bạn có thể nhìn thấy nguyên bộ đồ lòng của một website. Nghe như ảo thuật, nhưng đây là chuyện thật.",
     ["Chỉ cần gõ thêm vài chữ vào thanh địa chỉ,",
      "bạn có thể nhìn thấy nguyên bộ đồ lòng của một website."]),
    ("S01c3", "S01", "+6%", 0.0, 0.30,
     "Thủ phạm là một lỗi cấu hình rất phổ biến: để lộ mã nguồn và cấu trúc thư mục. Hôm nay, chúng ta sẽ chặn nó bằng ba vũ khí: Apache, tệp htaccess và mô hình Front Controller.",
     ["Thủ phạm là lỗi cấu hình để lộ mã nguồn và cấu trúc thư mục.",
      "Cách chặn: Apache, tệp .htaccess và Front Controller."]),

    ("S02c1", "S02", "+8%", 0.3, 0.20,
     "Đầu tiên, hãy mở mắt của trình duyệt. Nhấn F12, hoặc tổ hợp Ctrl Shift I, các bạn sẽ gặp DevTools — công cụ có sẵn trong Chrome, Edge và Firefox.",
     ["Đầu tiên, hãy mở mắt của trình duyệt: nhấn F12",
      "hoặc Ctrl + Shift + I để mở DevTools."]),
    ("S02c2", "S02", "+6%", 0.0, 0.35,
     "Mở tab Network, bạn thấy mọi tệp trình duyệt tải về, cả những phản hồi API. Nguyên tắc vàng là: thứ gì đã gửi xuống trình duyệt, thì người dùng đều xem được. Ẩn JavaScript bằng vài dòng lệnh khác gì lấy rèm che cửa kính — mà rèm lại trong suốt.",
     ["Mở tab Network: mọi tệp gửi xuống trình duyệt đều hiện ra.",
      "Ẩn JavaScript để bảo mật khác gì rèm trong suốt che cửa kính."]),

    ("S03c1", "S03", "+7%", 0.2, 0.25,
     "Nhưng phần nghiêm trọng nằm ở máy chủ. PHP chạy trên server, người dùng chỉ nhận HTML hoặc JSON, không thấy code. Vấn đề là cấu trúc thư mục vẫn có thể bị lộ nếu cấu hình sai.",
     ["Nhưng phần nghiêm trọng nằm ở máy chủ: PHP chỉ trả kết quả,",
      "cấu trúc thư mục vẫn có thể bị lộ nếu cấu hình sai."]),
    ("S03c2", "S03", "+6%", 0.0, 0.25,
     "Thử gõ thẳng đường dẫn tới thư mục config, hoặc tệp BookingService.php. Nếu cấu hình sai, bạn có thể thấy danh sách tệp, tải cả file cấu hình và file SQL chứa cơ sở dữ liệu.",
     ["Gõ thẳng đường dẫn tới thư mục config hay BookingService.php:",
      "có thể thấy danh sách tệp, tải cả cấu hình và file SQL."]),
    ("S03c3", "S03", "+8%", 0.4, 0.30,
     "Hệ quả là lộ mã nguồn, lộ cấu hình, lộ dữ liệu, rồi thành bàn đạp cho kẻ tấn công. Không phải thấy tên thư mục là hack được ngay, nhưng để lộ tài nguyên nhạy cảm là rủi ro phải dẹp.",
     ["Lộ mã nguồn, lộ cấu hình, lộ dữ liệu — thành bàn đạp tấn công.",
      "Thấy tên thư mục chưa chắc hack được, nhưng lộ là rủi ro phải dẹp."]),

    ("S04c1", "S04", "+7%", 0.2, 0.20,
     "Vậy ai là người gác cửa? Chính là Apache — máy chủ web mã nguồn mở: nhận yêu cầu HTTP, xác định tài nguyên rồi trả phản hồi. Apache phục vụ tệp tĩnh và phối hợp với PHP để chạy ứng dụng.",
     ["Người gác cửa là Apache: nhận yêu cầu HTTP,",
      "xác định tài nguyên và trả phản hồi cho trình duyệt."]),
    ("S04c2", "S04", "+5%", 0.0, 0.30,
     "Vũ khí nhỏ mà quyền lực là tệp htaccess. Đặt ngay trong thư mục cần bảo vệ, nó đổi luật ở cấp thư mục mà không cần sờ cấu hình tổng. Nhưng nhớ: máy chủ phải bật AllowOverride và mod rewrite.",
     ["Tệp .htaccess đổi luật ngay tại thư mục cần bảo vệ.",
      "Điều kiện: bật AllowOverride và module mod_rewrite."]),

    ("S05c1", "S05", "+7%", 0.2, 0.20,
     "Luật đầu tiên, dễ mà nhiều bạn quên: tắt Directory Listing bằng dòng Options trừ Indexes. Khi mở một thư mục không có tệp mặc định, máy chủ sẽ im lặng, thay vì khoe hết danh sách tệp bên trong.",
     ["Tắt Directory Listing bằng: Options -Indexes",
      "Mở thư mục trống, máy chủ không còn khoe danh sách tệp."]),
    ("S05c2", "S05", "+6%", 0.0, 0.35,
     "Nhưng cẩn thận: tắt danh sách không chặn được từng tệp. Biết đúng tên tệp vẫn vào được — nhiều bạn mới học Apache nhầm chỗ này. Muốn chặn hẳn cả thư mục, dùng Require all denied: mọi yêu cầu sẽ nhận 403 Forbidden.",
     ["Tắt danh sách không chặn được từng tệp nếu biết đúng tên.",
      "Chặn cả thư mục: Require all denied → 403 Forbidden."]),

    ("S06c1", "S06", "+7%", 0.2, 0.20,
     "Còn tệp nhạy cảm rải rác? Dùng FilesMatch chặn theo phần mở rộng: env, sql, log, bak, ini, sh. Cờ i trong ngoặc giúp so khớp không phân biệt hoa thường.",
     ["Dùng FilesMatch chặn tệp nhạy cảm: .env, .sql, .log, .bak…",
      "Cờ (?i) giúp so khớp không phân biệt hoa thường."]),
    ("S06c2", "S06", "+6%", 0.0, 0.30,
     "Nhưng đừng chỉ tin vào phần mở rộng. Bí mật an toàn nhất là cất ngoài DocumentRoot. Đừng để tệp env như cuốn nhật ký bỏ quên trên bàn cà phê.",
     ["Đừng chỉ tin vào phần mở rộng: hãy để tệp bí mật",
      "ngoài DocumentRoot — như nhật ký đừng bỏ quên ở quán cà phê."]),

    ("S07c1", "S07", "+7%", 0.3, 0.20,
     "Luật thứ ba: giấu đường dẫn vật lý bằng URL Rewrite. Người dùng thấy địa chỉ about gọn gàng, còn Apache âm thầm phục vụ tệp nằm sâu trong frontend, pages, about.",
     ["URL Rewrite giấu đường dẫn vật lý: /about/ →",
      "frontend/pages/about/index.html (người dùng không thấy)."]),
    ("S07c2", "S07", "+6%", 0.0, 0.35,
     "Cần RewriteEngine On và module mod rewrite. Quy tắc khớp about, thay bằng đường dẫn thật, cờ L để dừng xử lý. Và đừng lẫn rewrite nội bộ với chuyển hướng 301: một cái giữ nguyên địa chỉ, một cái bắt trình duyệt đổi sang địa chỉ mới.",
     ["RewriteRule ^about/?$ → frontend/pages/about/index.html [L]",
      "Rewrite nội bộ giữ URL; chuyển hướng 301 thì đổi URL."]),

    ("S08c1", "S08", "+9%", 0.6, 0.20,
     "Giờ đến phần hay nhất: Front Controller. Thay vì mỗi chức năng một tệp riêng như login, register, products, orders, mọi yêu cầu đều đi qua một cửa duy nhất: tệp index.php.",
     ["Front Controller: mọi yêu cầu đi qua một cửa duy nhất",
      "là index.php, thay vì login.php, products.php, orders.php…"]),
    ("S08c2", "S08", "+7%", 0.2, 0.35,
     "Cửa đó đọc URL, xác định route, kiểm tra quyền, gọi đúng chức năng rồi trả kết quả. Muốn thêm kiểm tra đăng nhập hay phân quyền? Chỉ sửa một chỗ. Và tuyệt đối không đưa đường dẫn người dùng nhập thẳng vào include.",
     ["Index.php đọc URL → xác định route → kiểm tra quyền → xử lý.",
      "Không lấy đường dẫn người dùng nhập đưa thẳng vào include!"]),

    ("S09c1", "S09", "+7%", 0.3, 0.30,
     "Cách an toàn là Whitelist Routing: khai báo trước danh sách route được phép. Có trong danh sách thì chạy, không có thì trả 404 Not Found. 404 ở đây không đáng buồn — nó là dấu hiệu hệ thống đang làm đúng: không có cửa thì không mở.",
     ["Whitelist Routing: chỉ chạy route đã khai báo trước.",
      "Đường dẫn lạ → 404. Không có cửa thì không mở."]),

    ("S10c1", "S10", "+6%", 0.0, 0.25,
     "Ghép tất cả lại: tách rõ public và private. Frontend, assets, index.php là công khai; app, config, routes, storage, env là nội bộ. Mấu chốt là trỏ DocumentRoot thẳng vào thư mục public, thay vì ném cả mã nguồn ra vùng công khai rồi cầu nguyện htaccess che giúp.",
     ["Tách rõ PUBLIC (frontend, assets, index.php) và",
      "PRIVATE (app, config, routes, storage, .env)."]),
    ("S10c2", "S10", "+6%", 0.0, 0.30,
     "Luồng chạy: trình duyệt gửi yêu cầu, Apache kiểm tra luật, chuyển vào front controller, router xác định route, xử lý rồi trả kết quả. Sai luật thì 403, sai route thì 404.",
     ["Luồng: trình duyệt → Apache → Front Controller → Router → xử lý.",
      "Sai luật: 403. Sai route: 404."]),

    ("S11c1", "S11", "+8%", 0.4, 0.20,
     "Tóm gọn ba ý. Một: DevTools thấy mọi thứ gửi xuống trình duyệt. Hai: htaccess chặn thư mục, chặn tệp, đổi URL ngay tại máy chủ. Ba: Front Controller cùng whitelist chỉ mở đúng cửa cần mở.",
     ["1. DevTools thấy mọi thứ gửi xuống trình duyệt.",
      "2. .htaccess chặn thư mục, chặn tệp, đổi URL.  3. Whitelist route."]),
    ("S11c2", "S11", "+9%", 0.5, 0.30,
     "Thử thách nhanh nhé: dòng nào tắt danh sách thư mục? A, Require all denied. B, Options trừ Indexes. C, RewriteEngine On. Suy nghĩ hai giây... Đáp án là B. Nếu bạn chọn đúng, xin chúc mừng!",
     ["Dòng nào tắt danh sách thư mục? A. Require all denied",
      "B. Options -Indexes   C. RewriteEngine On  → Đáp án: B"]),

    ("S12c1", "S12", "+7%", 0.2, 0.10,
     "Bảo mật không phải là che giấu, mà là kiểm soát đúng chỗ. Hãy thử dựng lại WebShield trên XAMPP, gõ một đường dẫn lạ xem chuyện gì xảy ra. Cảm ơn các bạn đã học cùng An Tech Academy, hẹn gặp ở bài tiếp theo!",
     ["Bảo mật là kiểm soát đúng chỗ, không phải che giấu.",
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
