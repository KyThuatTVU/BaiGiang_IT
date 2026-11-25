# 05 — Thiết kế SFX (không nhạc nền)

SFX **tự tổng hợp bằng numpy** (không bản quyền), ngắn, sạch; voice là lớp nổi nhất (SFX 0,25–0,55). **Không dùng nhạc nền.** Không chèn SFX cho mọi chuyển động nhỏ.

| Thời điểm | Hành động trên hình | SFX | Mức |
|---|---|---|---|
| S01 mở đầu | logo/tên thương hiệu hiện | chime | 0,45 |
| S01 c2 | 2 polaroid trượt vào | whoosh | 0,40 |
| S01 c3 | badge "API" bật | pop | 0,50 |
| S02 c1 | 2 khối Frontend/Backend hiện | pop ×2 | 0,40 |
| S02 c2 | thẻ giá lặp 4 nơi + gạch đỏ | deny | 0,35 |
| S02 c3 | khung "1 quầy chung" vẽ | marker 0,7 | 0,30 |
| S03 c1 | URL chữ API định nghĩa hiện | pop | 0,40 |
| S03 c2 | ổ cắm được khoanh marker | marker 0,6 | 0,32 |
| S03 c3 | 3 chip đặc điểm hiện lần lượt | pop ×3 | 0,35 |
| S04 c1 | bảng mapping 6 dòng hiện | pop ×2 | 0,35 |
| S04 c2 | phiếu bay sang bếp, đĩa bay về | whoosh ×2 | 0,40 |
| S04 c3 | câu chốt "không nấu ăn" | thud nhẹ | 0,30 |
| S05 c2 | 5 nhãn URL trượt xuống | tick ×5 | 0,30 |
| S05 c3 | gạch chân "ENDPOINT" | marker 0,6 | 0,30 |
| S06 c1 | phiếu request 4 dòng hiện | pop | 0,40 |
| S06 c3 | JSON body highlight | tick | 0,30 |
| S07 c1 | 5 method hiện | tick ×5 | 0,28 |
| S07c3 | dải status code hiện | pop ×2 | 0,35 |
| S08 c1 | response card hiện | pop | 0,40 |
| S08 c3 | mũi tên stringify/parse | whoosh nhẹ | 0,30 |
| S09 c1 | code hiện + highlight dòng | tick/click | 0,30 |
| S09 c2 | "200 OK" hiện | success | 0,45 |
| S10 c1 | 3 thẻ lỗi gạch chéo | deny ×3 | 0,35 |
| S10 c2 | 3 điều nhớ hiện | chime | 0,40 |
| S11 | logo kết | chime | 0,45 |

Quy tắc: SFX chỉ phát khi có hành động tương ứng; không tiếng gõ phím nếu không có cảnh code; không tiếng marker nếu không có nét vẽ; mỗi cảnh tối đa 3 SFX.
