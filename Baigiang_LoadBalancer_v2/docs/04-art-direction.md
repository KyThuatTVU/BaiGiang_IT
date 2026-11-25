# 04 · Art direction — Bài 12: Load Balancer

## Bảng màu

| Vai trò | Mã | Dùng ở đâu |
|---|---|---|
| Nền chính | `#F7F9FC` | Toàn bộ nền, lưới blueprint mờ |
| Chữ chính | `#12203A` (navy) | Tiêu đề, nhãn, card CTA |
| Thông tin | `#64748B` (muted) | Phụ đề cảnh, chú thích |
| Nhấn chính | `#2F6BFF` (blue) | Hành động, server đang chọn, tiêu đề phụ |
| Nhấn phụ | `#F5A524` (amber) | Nét vẽ tay, chip thứ tự, điểm nhấn |
| Xác nhận | `#22A06B` (green) | OK, hồi phục, chip đúng |
| Cảnh báo | `#E5484D` (red) | Quá tải, timeout, lỗi |
| Phụ trợ | `#0D9488` (teal) | LB, health probe, luồng dữ liệu |
| Viền | `#E2E8F0` | Đường kẻ, khung card |

Tỉ lệ 60–30–10: nền sáng chiếm ~60%, chữ/card trung tính ~30%, màu nhấn ~10%. Không dùng gradient làm nền chính; chỉ gradient rất nhẹ ở vòng trang trí góc phải.

## Typography

| Thành phần | Font | Cỡ |
|---|---|---|
| Tiêu đề cảnh | Be Vietnam Pro Bold | 56 px |
| Tiêu đề phụ | Be Vietnam Pro SemiBold | 44 px |
| Nội dung | Be Vietnam Pro Regular/Medium | 29–30 px |
| Nhãn nhỏ, chú thích | Be Vietnam Pro Medium | 22–23 px |
| Số liệu nổi bật | Plus Jakarta Sans ExtraBold | 58 px |
| Code | JetBrains Mono | 25 px |
| Phụ đề | Be Vietnam Pro Medium | 28 px |

Ghi chú: prompt gợi ý Quicksand cho tiêu đề; máy không có Quicksand nên dùng Be Vietnam Pro (hỗ trợ tiếng Việt đầy đủ). Một bộ font dùng xuyên suốt, không trộn font serif.

## Layout 1920×1080

- Lề trái 96 px; tiêu đề cảnh ở y ≈ 100–190; eyebrow ở góc phải trên.
- Vùng nội dung y 230–820; vùng nhân vật x 1560–1920, chân ở y 1020.
- Phụ đề: card navy góc trái dưới (x 96, y 940–1050), rộng tối đa 1180 px, thanh amber 6 px bên trái, chữ trắng 28 px, tối đa 2 dòng.
- Không đặt chữ quan trọng dưới y 820 (trừ phụ đề) và không đè vùng nhân vật.

## Hình khối

- Bo góc card 22–26 px; chip 999 px; nút 24 px.
- Viền 2 px màu `#E2E8F0`; bóng đổ mềm `0 10 30 rgba(18,32,58,0.06)`.
- Icon Lucide, nét 2 px, tô một màu; kích thước 34–44 px.
- Sơ đồ dùng hình học rõ: lục giác cho LB, card cho server, trụ cho database, mũi tên 3–4 px.

## Nét vẽ tay

- Nét marker màu amber, dày 5–7 px, đầu/cuối tự nhiên, có dao động nhẹ để không giống đường kẻ kỹ thuật.
- Thời lượng vẽ 0,5–0,9 giây, chạy đúng lúc lời giảng nhấn.
- Chỉ dùng để gạch chân từ khóa, khoanh thành phần đang nói, nối quan hệ. Sơ đồ kỹ thuật vẫn vẽ bằng nét thẳng chính xác.

## Nhân vật An

- Kích thước 360×560, vẽ gấp đôi rồi thu nhỏ (khử răng cưa).
- Áo xanh `#2F6BFF`, quần navy, kính đen, tóc đen, bảng tên "AN" amber.
- Pose: đứng giới thiệu, chỉ trái, chỉ phải, suy nghĩ, vẫy tay, viết.
- Đặt cố định góc phải dưới; không cắt đầu, không che phụ đề.

## Chuyển động

- Easing ease-out bậc ba cho mọi phần tử xuất hiện.
- Gói tin chạy theo đường gấp khúc 0,8–1,2 giây; không teleport.
- Card hiện bằng fade + dịch lên 12 px trong 0,4 giây.
- Chuyển cảnh xfade 0,4 giây, không hiệu ứng mạnh.
- Icon không rung lắc liên tục; chỉ nhấp nháy nhẹ khi đang được nói tới.
