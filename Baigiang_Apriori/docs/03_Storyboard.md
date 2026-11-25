# 03 — STORYBOARD (23 cảnh)

Thời lượng chính xác lấy từ `mau/full/timeline.json` sau khi render voice; dưới đây là ước tính.

| # | Cảnh | Nội dung thị giác | Chuyển động | Mục tiêu sư phạm | ~giây |
|---|---|---|---|---|---|
| 1 | S01 Hook | Thẻ "Điện thoại" + giỏ hàng → thẻ gợi ý 3 món (ốp lưng, kính, tai nghe); dải "10.000 hoá đơn" | Sản phẩm trượt vào, mũi tên vẽ dần, chấm dữ liệu chạy | Tạo câu hỏi: gợi ý từ đâu? | 14 |
| 2 | S02 Wordmark | AN TECH ACADEMY + tagline | Fade + gạch chân vàng vẽ | Nhận diện thương hiệu | 6 |
| 3 | S03 Mục tiêu | 3 dòng ✓ + 3 chip thuật ngữ | Hiện so le | Nêu lộ trình | 16 |
| 4 | S04 Định nghĩa | Câu định nghĩa lớn + 3 từ khoá tập mục / phổ biến / luật | Từ khoá tô sáng lần lượt | Hiểu Apriori là gì | 14 |
| 5 | S05 Dữ liệu | Bảng 10 giao dịch, icon sản phẩm | Từng hàng hiện 120 ms | Thấy dữ liệu đầu vào | 16 |
| 6 | S06 Support | Công thức + ví dụ 6/10 = 60% | Công thức hiện, số nhảy | Nắm công thức | 15 |
| 7 | S07 Số liệu | 4 thanh Support + 3 thanh cặp | Thanh chạy từ 0 | Đọc số liệu | 17 |
| 8 | S08 Cắt tỉa | Cây: Bơ+Trứng 10% → nhánh bị gạch đỏ | Nhánh mờ dần + dấu ✗ | Hiểu nguyên lý | 17 |
| 9 | S09 Pipeline | 4 thẻ bước theo ảnh + mũi tên | Tuần tự, badge bật | Tổng quan thuật toán | 16 |
| 10 | S10 1-itemset | Bảng 4 món + thanh %, ngưỡng 40% | Hàng Bơ chuyển xám | Cắt tỉa bước 1 | 14 |
| 11 | S11 2-itemset | 3 cặp ứng viên, 1 đạt | Dấu ✓/✗ hiện | Cắt tỉa bước 2 | 15 |
| 12 | S12 Luật | 2 thẻ Cream: BM→Sữa, Sữa→BM | Thẻ trượt vào | Chuyển từ tập sang luật | 10 |
| 13 | S13 Confidence | Công thức + 2 phép tính | Số liệu đếm lên | Hiểu chiều suy diễn | 16 |
| 14 | S14 Lift | Công thức + 3 mốc 1,25 / =1 / <1 | Thang 3 mốc | Hiểu liên kết thật | 22 |
| 15 | S15 Code setup | Code panel `pip`, `transactions`, `TransactionEncoder` | Dòng sáng theo cue | Thấy dữ liệu → bảng nhị phân | 20 |
| 16 | S16 Code apriori | `apriori(...)`, `association_rules(...)` | Highlight dòng | Chạy thuật toán | 20 |
| 17 | S17 Code recommend | Hàm `recommend` + kết quả Sữa | Highlight + kết quả | Nối kết quả với gợi ý | 15 |
| 18 | S18 Kiến trúc | Frontend — Flask/API — Backend + bảng luật | Luồng một chiều | Hiểu kiến trúc | 16 |
| 19 | S19 API | Request GET + JSON response | Hai khung hiện, mũi tên | Hiểu hợp đồng API | 15 |
| 20 | S20 JS/UI | Hàm fetch + mockup khối "Có thể bạn cũng thích" | Khối gợi ý hiện | Hiểu phía giao diện | 15 |
| 21 | S21 Lưu ý | Callout vàng "mô hình minh hoạ" + 2 gạch đầu dòng | Fade | Tránh hiểu sai | 12 |
| 22 | S22 Ưu/nhược | 2 cột ✓ / ! | Cột hiện lần lượt | Đánh giá công cụ | 18 |
| 23 | S23 Tổng kết | 3 điều cần nhớ + lời kết | Fade + wordmark | Củng cố | 18 |

## Đồng bộ
- Mỗi hàng/cột/thẻ chỉ xuất hiện tại cue tương ứng trong `manifest.json`.
- Code highlight đúng dòng khi lời giảng nhắc tham số.
- Phụ đề lấy từ trường `subs`, tối đa 2 dòng, không che bảng/code.
