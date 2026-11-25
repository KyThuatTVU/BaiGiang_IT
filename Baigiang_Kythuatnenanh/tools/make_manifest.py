# -*- coding: utf-8 -*-
"""Manifest 29 cue cho bài giảng "Kỹ thuật nén ảnh trong website" (~5 phút).
say = bản tối ưu cho TTS (phiên âm thuật ngữ CNTT); subs = phụ đề hiển thị đúng chính tả.
rate/shift tạo nhịp: câu hỏi & câu đùa nhanh + cao hơn, định nghĩa chậm + trầm hơn.
"""
import json, os

ROOT = "D:/Edit/Baigiang_Kythuatnenanh"
OUT = ROOT + "/mau/manifest.json"

PRON = [
    # dài trước, ngắn sau
    ("Lossless Compression", "lót-lít com-pờ-ré-sần"),
    ("Lossy Compression", "lót-xi com-pờ-ré-sần"),
    ("Image Compression", "i-mịch com-pờ-ré-sần"),
    ("An Tech Academy", "An Tếch A-ca-đê-mi"),
    ("withoutEnlargement", "gu-i-dao en-lát-mần"),
    ("ImageMagick", "i-mịch ma-gích"),
    ("TinyPNG", "tai-ni pê-en-gờ"),
    ("Squoosh", "sờ-quút"),
    ("npm install", "en-pi-em in-sto"),
    ("Node.js", "nốt giây-ét"),
    ("product.webp", "pro-đớt guép-pê"),
    ("product.jpg", "pro-đớt chây-pê-gờ"),
    ("srcset", "sooc-sét"),
    ("loading", "lô-đinh"),
    ("CDN", "xê-đi-en"),
    ("JPEG", "giây-pê-gờ"),
    ("WebP", "guép-pê"),
    ("webp", "guép-pê"),
    ("PNG", "pê-en-gờ"),
    ("AVIF", "ây-víp"),
    ("SVG", "ét-vi-giờ"),
    ("RAW", "ro"),
    ("Sharp", "sáp"),
    ("sharp", "sáp"),
    ("MB", "mê-ga-bai"),
    ("KB", "ki-lô-bai"),
    ("pixel", "pích-xồ"),
    ("resize", "ri-sai"),
    ("quality", "quoa-li-ti"),
    ("toFile", "tu-phai"),
    ("lazy", "lây-zi"),
    ("src", "ét-xờ-xê"),
    ("width", "uých"),
    ("height", "hai-tờ"),
]

# id, scene, rate, semitone, pause_after, text (hiển thị), subs (tối đa 2 dòng)
CUES = [
    ("S01c1", "S01", "+15%", 1.0, 0.25,
     "Chào các bạn! Chào mừng đến với An Tech Academy. Thử tưởng tượng: trang web bán điện thoại có ba mươi tấm ảnh, mỗi tấm năm MB. Đợi mãi… mà ảnh vẫn chưa hiện ra.",
     ["Chào các bạn! Chào mừng đến với An Tech Academy.",
      "Trang web 30 ảnh, mỗi ảnh 5 MB — đợi mãi ảnh chưa hiện."]),

    ("S01c2", "S01", "+13%", 0.5, 0.20,
     "Cộng lại là một trăm năm mươi MB cho một trang chủ. Trên mạng di động, chậm khỏi bàn. Khách chờ lâu, họ bỏ đi — đơn hàng đi theo.",
     ["30 × 5 MB = 150 MB cho một trang chủ.",
      "Mạng di động càng chậm — khách bỏ đi, đơn hàng đi theo."]),

    ("S01c3", "S01", "+12%", 0.4, 0.35,
     "Hôm nay mình học cách làm ảnh nhẹ đi mà mắt vẫn thấy đẹp. Tên chuyên môn: nén ảnh — Image Compression. Bắt đầu nhé!",
     ["Hôm nay: làm ảnh nhẹ đi mà mắt vẫn thấy đẹp.",
      "Tên chuyên môn: nén ảnh — Image Compression."]),

    ("S02c1", "S02", "+10%", 0.0, 0.25,
     "Vì sao phải nén? Ảnh nặng quyết định tốc độ tải trang, tốn băng thông, tốn chỗ lưu trữ. Băng thông và máy chủ đều là chi phí thật của người làm web.",
     ["Vì sao phải nén? Ảnh nặng quyết định tốc độ tải trang,",
      "tốn băng thông, tốn lưu trữ — mỗi MB đều có chi phí."]),

    ("S02c2", "S02", "+9%", -0.1, 0.40,
     "Và quan trọng nhất: trải nghiệm. Trang thương mại điện tử tải chậm là trang khó bán hàng. Các bạn đã bao giờ bỏ đi vì chờ quá lâu chưa?",
     ["Quan trọng nhất: trải nghiệm.",
      "Trang tải chậm là trang khó bán hàng."]),

    ("S03c1", "S03", "+8%", -0.2, 0.30,
     "Nén ảnh là quá trình giảm dung lượng hình ảnh bằng cách loại bỏ hoặc tổ chức lại thông tin theo một thuật toán. Giống dọn vali: vẫn đủ đồ, xếp khéo nên nhẹ hơn.",
     ["Nén ảnh: giảm dung lượng bằng cách loại bỏ hoặc",
      "tổ chức lại thông tin theo một thuật toán."]),

    ("S03c2", "S03", "+10%", 0.0, 0.35,
     "Ví dụ: ảnh sản phẩm năm MB, sau khi nén còn ba trăm năm mươi KB — giảm chín mươi ba phần trăm. Số liệu giả định thôi nhé, thực tế còn tùy ảnh và mức nén.",
     ["Ví dụ: 5 MB → 350 KB, giảm khoảng 93%.",
      "(Số liệu giả định để minh họa — thực tế tùy ảnh.)"]),

    ("S03c3", "S03", "+9%", 0.0, 0.40,
     "Dung lượng nhỏ hơn là tải nhanh hơn, ít tốn băng thông, ít tốn chỗ lưu trữ, khách ở lại lâu hơn. Một mũi tên trúng bốn đích.",
     ["Tải nhanh hơn · ít băng thông · ít lưu trữ ·",
      "khách ở lại lâu hơn — một mũi tên trúng bốn đích."]),

    ("S04c1", "S04", "+8%", -0.1, 0.30,
     "Có hai trường phái. Thứ nhất: nén mất dữ liệu — Lossy Compression. Nó chủ động vứt chi tiết mắt người khó thấy, đổi lấy dung lượng nhỏ hơn nhiều. JPEG là ví dụ quen thuộc.",
     ["Nén mất dữ liệu (Lossy): bỏ chi tiết mắt khó thấy",
      "để đổi lấy dung lượng nhỏ hơn nhiều. Ví dụ: JPEG."]),

    ("S04c2", "S04", "+9%", 0.1, 0.30,
     "Cùng một ảnh hoàng hôn: để chất lượng chín mươi, file khoảng sáu trăm mười tám KB; hạ còn năm mươi, chỉ còn một trăm chín mươi tư KB — giảm hơn ba lần. Nhưng nén quá tay, ảnh bắt đầu nhòe và xuất hiện nhiễu.",
     ["Cùng ảnh: quality 90 ≈ 618 KB → quality 50 ≈ 194 KB.",
      "Giảm hơn ba lần — nhưng bắt đầu nhòe, xuất hiện nhiễu."]),

    ("S04c3", "S04", "+12%", 0.6, 0.40,
     "Dấu vết đặc trưng: những ô vuông tám nhân tám pixel và vệt lỗi quanh vùng chuyển màu. Chữ và nét mảnh mà nén mạnh là răng cưa ngay. Nhớ nhé!",
     ["Đặc trưng JPEG: ô vuông 8×8 pixel, lỗi vùng chuyển màu.",
      "Chữ và nét mảnh nén mạnh → răng cưa ngay."]),

    ("S05c1", "S05", "+8%", -0.1, 0.25,
     "Thứ hai: nén không mất dữ liệu — Lossless Compression. Nén mà không vứt chi tiết nào, khôi phục lại y nguyên bản gốc. PNG là đại diện tiêu biểu.",
     ["Nén không mất dữ liệu (Lossless): không vứt chi tiết,",
      "khôi phục y nguyên bản gốc. Đại diện: PNG."]),

    ("S05c2", "S05", "+10%", 0.1, 0.40,
     "Nhờ vậy, PNG giữ nét chữ sắc, giữ nền trong suốt — như logo sư tử này — nên hợp logo, icon, ảnh chụp màn hình. Đổi lại, file thường nặng hơn JPEG và WebP.",
     ["PNG: nét chữ sắc, nền trong suốt → hợp logo, icon,",
      "ảnh chụp màn hình. Đổi lại: file nặng hơn JPEG, WebP."]),

    ("S06c1", "S06", "+9%", 0.0, 0.25,
     "Trên website nên dùng định dạng nào? JPEG nhẹ, hợp ảnh chụp. PNG nét, có nền trong suốt. WebP cân bằng, hỗ trợ cả hai kiểu nén. AVIF là định dạng mới, nén rất tốt.",
     ["JPEG: nhẹ, hợp ảnh chụp · PNG: nét, nền trong suốt",
      "WebP: cân bằng · AVIF: định dạng mới, nén rất tốt."]),

    ("S06c2", "S06", "+11%", 0.3, 0.45,
     "Ví dụ: JPEG một trăm hai mươi tám KB, PNG năm trăm mười hai, WebP bảy mươi tám, AVIF bốn mươi lăm KB. Nhưng đây là số liệu của một infographic, không phải chân lý cho mọi ảnh.",
     ["JPEG 128 KB · PNG 512 KB · WebP 78 KB · AVIF 45 KB.",
      "Số liệu từ infographic — ảnh khác, kết quả khác."]),

    ("S07c1", "S07", "+9%", 0.0, 0.30,
     "Chọn nhanh: ảnh chụp, sản phẩm, banner — JPEG hoặc WebP. Logo, icon, nền trong suốt — PNG hoặc SVG. Ảnh bản đồ, chữ nhỏ — đừng nén mạnh kiểu JPEG, chữ sẽ vỡ.",
     ["Ảnh chụp, sản phẩm → JPEG/WebP. Logo, icon → PNG/SVG.",
      "Ảnh bản đồ, chữ nhỏ → tránh JPEG nén mạnh."]),

    ("S07c2", "S07", "+11%", 0.3, 0.40,
     "Còn RAW? Đó là ảnh gốc để chỉnh sửa, chưa dành cho web: nặng và trình duyệt không đọc được. Xuất sang JPEG hoặc WebP trước khi đăng.",
     ["RAW: ảnh gốc để chỉnh sửa, chưa dành cho web.",
      "Xuất sang JPEG/WebP trước khi đăng."]),

    ("S08c1", "S08", "+10%", 0.0, 0.25,
     "Làm thử nhé. Có Squoosh nén trực tuyến, TinyPNG, ImageMagick cho dòng lệnh. Còn dân Node.js thì có Sharp — nén ngay trên máy chủ, rất nhanh.",
     ["Công cụ: Squoosh, TinyPNG, ImageMagick.",
      "Dân Node.js: Sharp — nén ngay trên máy chủ."]),

    ("S08c2", "S08", "+8%", -0.2, 0.30,
     "Cài bằng npm install sharp. Đọc ảnh product.jpg, resize về chiều rộng tám trăm pixel, không phóng lớn ảnh nhỏ, chuyển WebP chất lượng tám mươi, lưu ra product.webp.",
     ["npm install sharp → đọc product.jpg, resize 800px,",
      "chuyển WebP quality 80 → lưu product.webp."]),

    ("S08c3", "S08", "+9%", 0.0, 0.40,
     "Giải nghĩa: sharp mở ảnh; resize đổi kích thước; withoutEnlargement chặn phóng to; webp chọn định dạng; quality tám mươi là mức nén; toFile lưu kết quả.",
     ["sharp · resize · withoutEnlargement · webp ·",
      "quality 80 · toFile — ảnh nhẹ hơn, sẵn sàng lên web."]),

    ("S09c1", "S09", "+10%", 0.0, 0.25,
     "Ảnh nhẹ rồi, hiển thị cho khôn ngoan. Thẻ img cần src, alt, width, và đặc biệt là loading bằng lazy: khoan tải, đợi khách cuộn gần tới hãy tải.",
     ["Thẻ img: src, alt, width, loading=\"lazy\".",
      "lazy = khoan tải, đợi khách cuộn gần tới."]),

    ("S09c2", "S09", "+11%", 0.3, 0.40,
     "Khai báo width và height để trang không nhảy khi ảnh tải xong. Ảnh lớn thì dùng srcset để trình duyệt tự chọn kích thước phù hợp.",
     ["width + height: trang không nhảy khi ảnh tải xong.",
      "srcset: trình duyệt tự chọn kích thước phù hợp."]),

    ("S10c1", "S10", "+10%", 0.0, 0.25,
     "Nén ảnh có mặt khắp nơi: thương mại điện tử nén ảnh sản phẩm cho trang danh sách mượt; tin tức tối ưu ảnh bài viết.",
     ["Thương mại điện tử: nén ảnh sản phẩm, trang mượt hơn.",
      "Tin tức: tối ưu ảnh bài viết."]),

    ("S10c2", "S10", "+9%", 0.0, 0.35,
     "Du lịch giảm thư viện ảnh lớn — như hồ núi này. Giáo dục tối ưu ảnh khóa học. Hễ có ảnh trên web là có chỗ cho nén ảnh.",
     ["Du lịch: giảm thư viện ảnh. Giáo dục: ảnh khóa học.",
      "Hễ có ảnh trên web — là có chỗ cho nén ảnh."]),

    ("S11c1", "S11", "+9%", 0.0, 0.30,
     "Vài lưu ý. Đừng nén quá tay, ảnh vỡ thì đẹp mấy cũng vô nghĩa. Resize đúng kích thước hiển thị, đừng tải ảnh bốn nghìn pixel về khung ba trăm.",
     ["Đừng nén quá tay — ảnh vỡ thì đẹp mấy cũng vô nghĩa.",
      "Resize đúng kích thước hiển thị thực tế."]),

    ("S11c2", "S11", "+10%", 0.1, 0.40,
     "Khai báo width, height, dùng lazy loading. Cân nhắc CDN hoặc dịch vụ tối ưu ảnh. Cân bằng giữa dung lượng và chất lượng — đó là nghệ thuật, không phải phép tính.",
     ["width, height + lazy loading. Cân nhắc CDN / dịch vụ",
      "tối ưu ảnh. Cân bằng dung lượng ↔ chất lượng."]),

    ("S12c1", "S12", "+9%", 0.0, 0.30,
     "Tóm lại, bốn điều. Một: nén ảnh giảm dung lượng, tăng tốc tải. Hai: Lossy cho ảnh chụp, Lossless cho logo và nền trong suốt.",
     ["1. Nén ảnh giảm dung lượng, tăng tốc tải.",
      "2. Lossy (JPEG) cho ảnh chụp · Lossless (PNG) cho logo."]),

    ("S12c2", "S12", "+10%", 0.0, 0.30,
     "Ba: WebP và AVIF là lựa chọn hiện đại, nhớ kiểm tra trình duyệt. Bốn: Sharp, lazy loading và CDN giúp website nhẹ như lông hồng.",
     ["3. WebP/AVIF: hiện đại, nhớ kiểm tra trình duyệt hỗ trợ.",
      "4. Sharp + lazy loading + CDN = website nhẹ."]),

    ("S12c3", "S12", "+12%", 0.6, 0.30,
     "Không phải nén càng nhỏ càng tốt, mà là cân bằng giữa dung lượng, chất lượng và trải nghiệm. Cảm ơn các bạn đã học cùng An Tech Academy. Hẹn gặp ở bài tiếp theo!",
     ["Không phải nén càng nhỏ càng tốt — mà là cân bằng",
      "dung lượng, chất lượng, trải nghiệm. Hẹn gặp lại!"]),
]

# Thông tin cảnh cho storyboard: id, tiêu đề, phần, hình ảnh, chuyển động, chữ trên màn hình, SFX
SCENES = [
    ("S01", "Mở đầu — 30 ảnh, 150 MB", "Mở đầu",
     "Nền navy tối; ảnh loading_fast_slow (chia đôi Tải nhanh / Tải chậm); lưới 30 thumbnail sản phẩm mờ dần hiện; nhân vật An bên phải.",
     "30 thumbnail pop theo nhịp; bộ đếm 30 × 5 MB chạy tới 150 MB; thanh dung lượng đỏ đầy dần; Ken Burns nhẹ trên ảnh.",
     "AN TECH ACADEMY · NÉN ẢNH TRONG WEBSITE · 30 × 5 MB = 150 MB · Image Compression",
     "whoosh, pop ×3, riser nhẹ"),

    ("S02", "Vì sao website cần nén ảnh", "Vấn đề",
     "Ảnh imgix_score (Before/After, −96% dung lượng, −41% loading) khung lớn bên phải; ảnh shop_product_page khung nhỏ bên trái; 3 thẻ chi phí: tốc độ, băng thông, lưu trữ.",
     "Hai ảnh trượt vào; thẻ chi phí hiện lần lượt; nhãn 'trải nghiệm' nhấp nháy nhẹ khi nhắc.",
     "Tốc độ · Băng thông · Lưu trữ · Trải nghiệm",
     "whoosh, pop ×3, tick"),

    ("S03", "Nén ảnh là gì?", "Kiến thức nền",
     "Nền sáng; thẻ định nghĩa lớn; ảnh before_after_5mb (5 MB → 350 KB) bên phải; ảnh product_devices nhỏ phía dưới; thanh so sánh dung lượng; 4 chip lợi ích.",
     "Thanh 5 MB co về 350 KB; số % đếm tới 93%; 4 chip hiện lần lượt; nét marker gạch chân định nghĩa.",
     "NÉN ẢNH = GIẢM DUNG LƯỢNG · 5 MB → 350 KB (−93%, giả định)",
     "pop, chime, marker"),

    ("S04", "Nén mất dữ liệu (Lossy)", "Kiến thức nền",
     "Ảnh jpeg_quality_grid (100 → 50) bên trái, khung zoom vào ô 8×8; ảnh jpeg_artifacts_face + text_quality + cat_compression bên phải; thanh trượt quality 100 → 50.",
     "Slider quality kéo từ 100 xuống 50; ô 8×8 phóng to có viền cam; nhãn đỏ 'răng cưa' xuất hiện; ảnh mờ dần khi quality giảm.",
     "LOSSY · JPEG · Quality 90: 618 KB → 50: 194 KB · Ô 8×8 pixel",
     "whoosh, tick, error nhẹ"),

    ("S05", "Nén không mất dữ liệu (Lossless)", "Kiến thức nền",
     "Ảnh png_features bên trái; ảnh logo_transparent (JPG → trong suốt) bên phải với nền caro; thẻ 'khôi phục y nguyên'.",
     "Logo chuyển từ nền be sang nền trong suốt có animation caro; dấu check xanh; chip 'PNG' nảy nhẹ.",
     "LOSSLESS · PNG · Khôi phục y nguyên · Nền trong suốt",
     "pop, chime, success"),

    ("S06", "Bốn định dạng: JPEG, PNG, WebP, AVIF", "Phân tích",
     "Ảnh formats_4up là bằng chứng trung tâm; 4 thanh dung lượng chuẩn hóa (128/512/78/45 KB); chú thích nguồn infographic.",
     "Từng cột sáng lên khi được gọi tên; thanh dung lượng mọc dần; nhãn 'infographic' hiện kèm ghi chú.",
     "JPEG 128 KB · PNG 512 KB · WebP 78 KB · AVIF 45 KB (theo infographic)",
     "pop ×4, tick, whoosh"),

    ("S07", "Chọn định dạng theo mục đích", "Phân tích",
     "Ma trận 3 nhóm: ảnh chụp → JPEG/WebP; logo/icon → PNG/SVG; bản đồ/chữ nhỏ → PNG; thumbnail raw_vs_jpeg và elcapitan_sizes; ảnh map_jpeg_png crop.",
     "Ba cột hiện lần lượt, mũi tên nối nhóm → định dạng; ảnh map phóng to phần chữ bị vỡ.",
     "Ảnh chụp → JPEG/WebP · Logo → PNG/SVG · Bản đồ → PNG",
     "whoosh, pop ×3"),

    ("S08", "Thực hành: nén bằng Sharp", "Minh họa kỹ thuật",
     "Nền tối; panel code compress.js gõ từng ký tự; pipeline product.jpg → resize 800 → WebP 80 → product.webp; bảng giải thích 6 lệnh sáng theo lời giảng.",
     "Code typing đồng bộ; gói dữ liệu chạy qua pipeline; dung lượng giảm 5 MB → 350 KB (minh họa); từng dòng bảng highlight.",
     "compress.js · sharp().resize().webp({quality:80}).toFile()",
     "type, whoosh, tick ×6, chime"),

    ("S09", "Hiển thị ảnh thông minh trên HTML", "Minh họa kỹ thuật",
     "Panel HTML thẻ img; mock trình duyệt có đường cuộn; ảnh dưới màn hình mờ (chưa tải) rồi hiện khi đường cuộn đi qua; chip width/height giữ chỗ.",
     "loading=\"lazy\" được khoanh marker; ảnh lazy tải khi viewport chạm; khung giữ chỗ chống nhảy bố cục; srcset hiện 3 kích thước.",
     "<img src loading=\"lazy\" width height> · srcset",
     "type, pop, tick, whoosh"),

    ("S10", "Ứng dụng thực tế", "Ứng dụng",
     "Bốn thẻ: thương mại điện tử (shop_product_page crop), tin tức, du lịch (lake_dolomites), giáo dục — icon Lucide đồng nhất.",
     "Thẻ trượt lên lần lượt; ảnh Ken Burns nhẹ; dòng kết 'hễ có ảnh trên web…' gạch marker.",
     "E-commerce · Tin tức · Du lịch · Giáo dục",
     "pop ×4, whoosh"),

    ("S11", "Lưu ý khi nén ảnh", "Lưu ý",
     "Checklist 5 mục có icon; ảnh screenshot_guide (PNG vs JPG) khung nhỏ bên phải; biểu tượng cân bằng dung lượng ↔ chất lượng.",
     "Từng mục check hiện lần lượt; cán cân nghiêng về 'cân bằng'; mục sai bị gạch đỏ nhẹ.",
     "Đừng nén quá tay · Resize đúng · lazy + width/height · CDN · Cân bằng",
     "tick ×5, pop, chime"),

    ("S12", "Tổng kết & Outro", "Tổng kết",
     "4 thẻ tóm tắt; dải Before/After nhỏ từ imgix_score; logo chữ AN TECH ACADEMY; nhân vật An vẫy tay.",
     "4 thẻ hiện lần lượt; gạch marker cam dưới câu chốt; hiệu ứng sheen nhẹ; An vẫy.",
     "4 điều cần nhớ · Hiểu công nghệ, làm chủ tương lai!",
     "pop ×4, chime, success"),
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
    est = sum(len(c["text"].split()) / 3.1 + (0.3 + c["pause_after"]) for c in out) + 12
    print(f"EST_DURATION ~{int(est // 60)}:{est % 60:04.1f}")


if __name__ == "__main__":
    main()
