# 04 — Art direction & phân loại hình ảnh

## 1. Bảng màu (chốt, không đổi giữa các cảnh)

| Vai trò | Màu | Hex |
|---|---|---|
| Nền | trắng xanh rất nhạt | `#F7F9FC` |
| Chữ chính / khối đậm | navy | `#12203A` |
| Nhấn chính (API, request) | xanh dương | `#2F6BFF` |
| Nhấn phụ (response, DB) | teal | `#0D9488` |
| Điểm nhấn / marker | hổ phách | `#F5A524` |
| Lỗi / DELETE | đỏ | `#E5484D` |
| Thành công / GET | xanh lá | `#22A06B` |
| Nền code | navy đậm | `#0F172A` |

Quy tắc 60-30-10: nền sáng ~60%, navy/chữ ~30%, xanh dương + hổ phách ~10%. Không dùng neon, không gradient cầu vồng, không glow tràn.

**Bảng accent công nghệ (v3, dùng lẫn nhau):** xanh dương `#2F6BFF`, indigo `#4F46E5`, cyan `#06B6D4`, tím `#8B5CF6`, xanh terminal `#10B981`, teal `#0D9488`, hổ phách đậm `#B45309`, xanh trời `#0EA5E9`. Tông lạnh + xanh terminal là chủ đạo; đã bỏ coral/cam/hồng để hình đọc đúng chất công nghệ. Accent dùng cho chip, viền icon, vạch đầu thẻ, nét nối, chấm nền — luân phiên giữa các phần tử nhưng nền/chữ vẫn giữ 60-30.

**Dải terminal (v3):** thẻ navy `#0F172A` bo góc, 3 chấm đèn cyan/hổ phách/xanh terminal, dòng lệnh `› METHOD /path STATUS` bằng JetBrains Mono. Dùng làm điểm nhấn "API đang chạy thật": `GET /api/mon-an 200 OK`, `GET /api/menu 200 OK`, `POST /orders 201 Created`.

## 2. Typography

- Tiêu đề: **Be Vietnam Pro Bold** (56/44 px).
- Nội dung: **Be Vietnam Pro** (30/26 px), tiếng Việt đủ dấu.
- Nhãn/số: **Plus Jakarta Sans** (24–28 px, 600–700).
- Code/URL: **JetBrains Mono** (25 px).
- Phụ đề: Be Vietnam Pro Medium 28, card navy góc trái dưới, tối đa 2 dòng.

## 3. Icon & nét

- Một bộ **Lucide line icon** duy nhất (92 icon, stroke 1.6, đầu nét tròn), tô màu theo vai trò.
- Nét vẽ tay: marker hổ phách 6 px, hơi lượn, dùng cho: khoanh ổ cắm, gạch chân URL, mũi tên request, đóng khung "API".
- Không emoji, không icon 3D/nhựa, không đổ bóng dày.

## 4. Bố cục

- Vùng an toàn 5%; giáo viên An đứng phải (1660, 1020), không che nội dung; khi có code chuyển An nhỏ hơn hoặc ẩn.
- Mỗi cảnh một trọng tâm; tối đa 2 nhóm chuyển động cùng lúc.
- Card bo 18 px, viền `#E2E8F0` 2 px, bóng mờ nhẹ.

## 5. Nhân vật giáo viên

- "An": vector phẳng 2D, áo sơ mi xanh, quần navy, thẻ tên AN, tóc đen ngắn. Dùng lại `character.py` của bài Load Balancer (cùng vũ trụ hình ảnh AN TECH), 6 tư thế: idle / present / point_left / point_right / think / wave / write.
- Không đổi trang phục, khuôn mặt, tỷ lệ giữa các cảnh; nhép miệng khi đang nói, chớp mắt chu kỳ 3,4 s.

## 6. Xử lý ảnh người dùng

Ảnh được đưa vào dưới dạng **card bo góc + Ken Burns nhẹ (zoom 1,0→1,08)**, có nhãn tiếng Việt; ảnh chứa chữ tiếng Anh (hand-drawn, vector) sẽ được phủ nhãn tiếng Việt hoặc crop để tránh người học đọc nhầm.
Ảnh giao diện (Postman, Thunder Client) giữ nguyên tỷ lệ, crop bỏ viền, **không** chồng chữ lên vùng JSON.

### Phân loại & quyết định

| Nhóm | Ảnh | Quyết định |
|---|---|---|
| Ảnh thật đúng ngữ cảnh | waiter_order, chef_cook, kitchen_rush | Dùng (kitchen_rush chỉ crop nhỏ) |
| Sơ đồ/vector phẳng | fe_be_db, order_flow_flat, handdrawn_cycle, waiter_chef_flat, client_server_yellow | Dùng; crop bỏ logo/footer; phủ nhãn Việt |
| UI thật | postman_get, thunder_client | Dùng làm bằng chứng thao tác |
| Ảnh AI có chữ/code | rest_cards, fetch_code | Chỉ dùng 1 phần/nền mờ; nội dung kỹ thuật tự dựng |
| Neon/glow | api_neon, neon_restaurant, http_deep_dive | **Không dùng bản chính** (trái Clean Visual System). Có thể chèn 1 nhịp rất ngắn nếu bạn yêu cầu. |
| Hoạt hình trẻ con | cartoon_cycle | **Không dùng** (lệch đối tượng, trùng nội dung ảnh 5) |

### Hình minh hoạ IT tự dựng (v3)

Không dùng ảnh AI cho phần kỹ thuật — vẽ vector bằng PIL để giữ nét sạch, đúng chuyên ngành:

- **Cửa sổ IDE tối** (`code_window`): thanh tiêu đề + 3 chấm đèn, số dòng, code tô màu cú pháp (keyword hổ phách, string xanh terminal, lời gọi cyan). Dùng ở S01 (`app.js — đặt món`) và S03 (`GET /api/menu`).
- **Tủ rack server** (`server_rack`): 3 tầng, khe máy, đèn LED cyan nhấp nháy theo nhịp. Dùng ở S04 cạnh sơ đồ nhà hàng, nhãn `SERVER · BACKEND`.
- **Dải terminal** (`code_strip`): dòng lệnh `› METHOD /path STATUS` — S01, S03, S04.
- **Nền mạch in** (`bg_tech`): vệt mạch vuông góc + pad hàn + dải nhị phân mờ ở rìa + quầng indigo/cyan, alpha thấp để không tranh chữ.

## 7. Chuyển động (v3 — vui tươi + công nghệ)

- Vào cảnh: fade + scale 0,96→1 trong 0,5 s.
- Sơ đồ: thành phần xuất hiện tuần tự theo lời; connector là **nét đứt chạy** đúng chiều dữ liệu; gói request là chấm tròn có đuôi.
- Icon: đặt trong **đĩa màu** (nền tint + viền accent), bật vào kiểu sticker (overshoot ~5% + nghiêng ±7° rồi về thẳng).
- Chip/nhãn: bật vào có overshoot nhẹ, nghiêng ±4° khi xuất hiện; mỗi chip một màu accent.
- Hiệu ứng điểm nhấn: **sparkle 4 cánh** nhấp nháy quanh vật thể chính; **confetti** giấy màu bung ra ở khoảnh khắc chốt (badge API, ổ cắm, món ăn về bàn).
- Nền: lớp mạch in + nhị phân mờ (v3), 6 chấm màu trôi chậm, không chồng lên vùng chữ.
- Code/URL: highlight nền hổ phách nhạt đúng dòng đang nói, không nhảy dòng.
- Chuyển cảnh (v3): xfade 0,4 s + whoosh, luân phiên `fade → smoothleft → pixelize → circleopen → hlslice → radial → hblur`; đã thử từng hiệu ứng với ffmpeg hiện tại, tất cả chạy được.
- Giới hạn: particle là hình học vẽ bằng PIL (không physics thật), tất định theo thời gian — không random mỗi frame.

## 8. Giới hạn đã biết

- Đây là motion graphics 2D dựng bằng frame (PIL) + ffmpeg, không phải 3D/cinematic. Không có camera 3D thật, không particle phức tạp.
- Hiệu ứng vẽ tay là **stroke reveal** mô phỏng nét marker, không phải hand-tracking thật.
- Chữ trên ảnh AI (rest_cards, fetch_code) không được dùng làm nội dung dạy; mọi URL/code/status code hiển thị đều do renderer vẽ.
