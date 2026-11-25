# 04 — ART DIRECTION & BẢNG MÀU

## 1. Định hướng
Infographic dữ liệu, phẳng 2D, editorial — lấy đúng ngôn ngữ thị giác của ảnh tham chiếu (navy đậm + xanh nhạt + vàng kem) nhưng **không sao chép nội dung số liệu sai** trong ảnh.

## 2. Bảng màu (giới hạn 6 màu ngữ nghĩa)

| Vai trò | Hex | Dùng cho |
|---|---|---|
| Navy (nền thương hiệu) | `#0B2A5B` | banner tiêu đề, header bảng, code panel nền |
| Blue (màu thông tin) | `#2F6FD0` | icon, viền nhấn, thanh Support, mũi tên |
| Sky (nền chính) | `#EAF1F9` | nền toàn video |
| Ice (nền phụ) | `#D9E7F7` | card bước, hàng bảng xen kẽ, vùng tô nhạt |
| Amber (màu nhấn) | `#F5C45E` | số liệu nổi bật, gạch chân tiêu đề phụ, badge |
| Cream (nền nhấn) | `#FCEFD2` | thẻ luật kết hợp, callout ghi chú |
| Ink | `#0E1B33` | chữ chính |
| Muted | `#4A5B72` | chữ phụ, chú thích |
| Green | `#1F8A4C` | dấu ✓, kết quả đạt ngưỡng |
| Red | `#C0392B` | dấu ✗, giá trị bị loại |

Không dùng gradient, glow, neon. Bóng đổ: 1 lớp `rgba(11,42,91,0.10)`, lệch 6px.

## 3. Typography (theo mục 2.2)

| Thành phần | Font | Cỡ |
|---|---|---|
| Tiêu đề cảnh (trong banner) | Plus Jakarta Sans 800 | 56 px |
| Phụ đề banner | Be Vietnam Pro Medium | 30 px |
| Tiêu đề khối | Be Vietnam Pro SemiBold | 34 px |
| Nội dung, bảng | Be Vietnam Pro Regular/Medium | 30 px |
| Nhãn bảng, chú thích | Be Vietnam Pro Medium | 24–26 px |
| Số liệu nổi bật | Plus Jakarta Sans 800 | 52–64 px |
| Code | JetBrains Mono | 24–26 px |
| Phụ đề | Be Vietnam Pro Medium | 30 px, tối đa 2 dòng |

## 4. Layout
- Vùng an toàn 96 px hai bên, 54 px trên/dưới; banner kết thúc ở y≈216; nội dung y 260–980; phụ đề đáy 1026.
- Banner navy bo 26 px, tiêu đề trắng canh giữa, phụ đề vàng kem; wordmark "AN TECH ACADEMY" 22 px góc trên trái.
- Bảng: header navy, hàng cao 62 px, cột support canh phải; hàng đạt ngưỡng có nền Ice, hàng bị loại dùng chữ Muted + dấu ✗ đỏ.
- Thẻ bước 1–4 theo ảnh: số trong vòng navy, tiêu đề 28 px, nền Ice.
- Thẻ luật: nền Cream, viền trái Amber 6 px, dòng luật 34 px + Confidence/Lift 26 px.

## 5. Icon
- Một bộ duy nhất: **Lucide** (ISC), stroke 2, viewBox 24, render 1 màu theo ngữ nghĩa (blue/navy/green/red).
- Sản phẩm: `milk`, `sandwich`, `egg`, `package`.
- Chức năng: `database`, `filter`, `git-fork`, `link`, `receipt`, `bar-chart-3`, `code-xml`, `server`, `globe`, `lightbulb`, `target`, `refresh-cw`.
- Không emoji, không icon 3D, không trộn bộ khác.

## 6. Chuyển động
- Reveal phần tử: fade + scale 0.9→1 trong 200 ms, trễ theo cue.
- Bảng: từng hàng hiện so le 120 ms.
- Connector: vẽ nét 600 ms, đầu mũi tên hiện khi đủ nét, chấm dữ liệu chạy 0.9 s/lần.
- Banner: trượt lên 12 px + fade 300 ms.
- Chuyển cảnh: crossfade 300 ms; không zoom, không rung, không hiệu ứng nhấp nháy.
- Code: highlight dòng đang giảng bằng nền `#123A6E`, không nhấp nháy.

## 7. Quy tắc nội dung hình
- Mọi con số trên hình phải khớp bảng kiểm chứng trong `00_HoSoDuAn.md`.
- Không dùng chữ do AI tạo; toàn bộ chữ, bảng, code được render bằng code.
- Mỗi cảnh một thông điệp; nếu quá 3 nhóm thông tin thì tách cảnh.
