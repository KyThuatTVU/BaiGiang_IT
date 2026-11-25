# 04 — ART DIRECTION, NHÂN VẬT, SFX

Áp dụng Clean Visual System (mục XII) + nhân vật giáo viên, vẽ tay, SFX (mục XVIII).

## 1. Định hướng

- Phong cách: **flat 2D editorial, kỹ thuật, sạch**. Nền sáng, nhiều khoảng trắng, phân cấp rõ.
- Chủ đề Backend/Networking → màu thông tin xanh dương, màu nhấn **teal** cho "realtime/đồng bộ".
- Không gradient, không neon, không glow, không icon bóng nhựa, không ảnh AI.
- Toàn bộ chữ, bảng, sơ đồ, code, giao diện **render bằng code** (PIL) — không dùng ảnh sinh sẵn chứa chữ.

## 2. Bảng màu (giới hạn)

| Vai trò | Hex | Dùng cho |
|---|---|---|
| Navy | `#0B2A5B` | banner, header bảng, áo blazer nhân vật, nền code |
| Blue | `#2F6FD0` | icon, mũi tên, nét vẽ kỹ thuật |
| Teal | `#0F9D8F` | nhấn "realtime/đồng bộ", trạng thái kết nối, cà vạt nhân vật |
| Sky | `#EAF1F9` | nền toàn video |
| Ice | `#D9E7F7` | card, hàng bảng xen kẽ, vùng tô nhạt |
| Amber | `#F5C45E` | gạch chân, khoanh từ khóa, badge nhấn |
| Cream | `#FCEFD2` | callout ghi chú |
| Ink | `#0E1B33` | chữ chính |
| Muted | `#4A5B72` | chữ phụ, phần tử bị loại |
| Green | `#1F8A4C` | ✓, đạt |
| Red | `#C0392B` | ✗, cảnh báo |
| Code bg | `#0B1B33` | nền code panel |
| Code line | `#123A6E` | dòng đang giảng |

Không dùng quá 3 màu nhấn trong một cảnh. Màu phải mang nghĩa: teal = đồng bộ/kết nối, amber = điểm cần nhớ, đỏ = lỗi/bị từ chối.

## 3. Typography

| Thành phần | Font | Cỡ |
|---|---|---|
| Tiêu đề cảnh | Plus Jakarta Sans 800 | 54–56 px |
| Phụ đề banner | Be Vietnam Pro Medium | 29–30 px |
| Tiêu đề khối | Be Vietnam Pro SemiBold | 34 px |
| Nội dung | Be Vietnam Pro Regular/Medium | 30 px |
| Chú thích, nhãn bảng | Be Vietnam Pro Medium | 24–26 px |
| Số liệu/badge | Plus Jakarta Sans 800 | 42–58 px |
| Code | JetBrains Mono | 22–23 px |
| Wordmark | Plus Jakarta Sans 800 | 78 px |
| Phụ đề | Be Vietnam Pro Medium | 30 px, tối đa 2 dòng |

## 4. Layout

- Vùng an toàn: 96 px hai bên, 54 px trên/dưới.
- Banner navy cao ~150 px, kết thúc y≈216; nội dung y 260–980; phụ đề đáy 1026.
- Wordmark 21 px góc trên trái mọi cảnh nội dung.
- Code panel: x 96–1460, y 260–980; nhân vật thu nhỏ bên phải.
- Không đặt chữ quan trọng sát mép hoặc sau nhân vật.

## 5. Nhân vật giáo viên — "Thầy Minh"

Character sheet cố định, dùng **cùng một tham số** cho mọi cảnh (vẽ bằng hàm `draw_teacher(pose, t)`):

| Thuộc tính | Giá trị |
|---|---|
| Giới thiệu | Nam, 30–34 tuổi, người dẫn bài giảng |
| Tóc | Đen `#1B1B1F`, ngắn, rẽ phải, không kính |
| Da | `#F0C4A0`, tai đơn giản |
| Áo | Sơ mi trắng `#FFFFFF`, blazer navy `#0B2A5B`, cà vạt teal `#0F9D8F` |
| Quần / giày | `#22304A` / `#2A2118` |
| Tỷ lệ | 5,5 đầu; cao 430 px ở 1080p (đầu–chân) |
| Nét | Viền 3 px màu `#0A1A33` ở 60% opacity; không gradient |
| Mắt | 2 chấm + chớp mỗi 4,2 s (0,12 s) |
| Miệng | 3 biến thể: cười nhẹ, trung tính, mở khi nhấn mạnh |
| Idle | Nhấp nhô 2 px chu kỳ 4 s; đầu nghiêng ±2° |

**Pose (4):**

1. `D` — đứng giảng, tay phải mở về phía bảng.
2. `C` — chỉ tay phải lên/ngang về đối tượng đang nói.
3. `V` — tay phải cầm bút, tay trái chống hông (dùng khi có nét vẽ).
4. `G` — hai tay mở, lòng bàn tay hướng người học (giải thích).

**Vị trí:** mặc định x 1560–1880, chân y 1010. Cảnh code (S21–S24) và cảnh chạy thử (S26): scale 0,55, đặt x 1660–1880, đỉnh y 470 — không che panel.

**Giới hạn phải nêu:** nhân vật là hình vector 2D đổi pose + idle, **không** phải rig xương, không lip-sync, không walk-cycle. Không tuyên bố "nhân vật chuyển động 3D".

## 6. Hiệu ứng vẽ tay

| Hành động | Nét | Thời lượng | Dùng ở |
|---|---|---|---|
| Gạch chân từ khóa | Amber 6 px | 0,45–0,60 s | S01, S03, S34 |
| Khoanh khái niệm | Blue 5 px | 0,50 s | S05, S16 |
| Vẽ mũi tên | Blue 5 px | 0,35–0,60 s | S06, S09, S28 |
| Vẽ khung/bảng | Navy 4 px | 0,40 s | S11, S15 |
| Gạch chéo | Red 5 px | 0,30 s | S03 (reload), S18 (✗) |

Quy tắc: tối đa 2 nét/cảnh; nét mượt, ease-out; bắt đầu/kết thúc tự nhiên; **không** dùng vẽ tay cho số liệu hoặc code (code hiển thị đúng font, không "viết tay").

## 7. Icon

- Bộ duy nhất: **Lucide** (ISC), stroke 2, viewBox 24, tô 1 màu theo ngữ nghĩa.
- Cần chuẩn bị: `users`, `monitor`, `smartphone`, `server`, `database`, `globe`, `wifi`, `wifi-off`, `arrow-right`, `arrow-left-right`, `refresh-cw`, `layers`, `link`, `git-branch`, `git-merge`, `shield-check`, `lock`, `triangle-alert`, `circle-check`, `clock`, `terminal`, `code-xml`, `mouse-pointer-click`, `pen-line`, `zap`, `radio`, `messages-square`, `list-checks`, `graduation-cap`, `book-open`, `square-kanban`, `shopping-cart`, `school`, `message-circle`, `rotate-ccw`, `x`, `equal-not`, `panel-top`, `square-stack`.
- Không emoji, không trộn bộ khác, không icon 3D.

## 8. Chuyển động

- Reveal: fade + scale 0,9→1 trong 200 ms, ease-out.
- Hàng bảng/thẻ: so le 120 ms.
- Connector: vẽ nét 600 ms; đầu mũi tên hiện khi nét đủ.
- Chấm dữ liệu: chạy 0,9 s/chặng, dừng 0,2 s ở node.
- Banner: trượt lên 12 px + fade 300 ms.
- Chuyển cảnh: crossfade 300 ms. Không zoom, không rung, không nhấp nháy.
- Code highlight: đổi nền dòng, **không** nhấp nháy, **không** gõ từng ký tự (trừ 2 lệnh terminal ở S19/S26).

## 9. SFX (tổng hợp, không bản quyền)

| File | Mô tả | Thời lượng | Mức |
|---|---|---|---|
| `pen.wav` | Nhiễu lọc 1,2–3,5 kHz, envelope ngắn | 180 ms | −26 dBFS |
| `pop.wav` | Sine 660→440 Hz | 120 ms | −26 dBFS |
| `click.wav` | Transient + noise 2 ms | 60 ms | −24 dBFS |
| `chime.wav` | Hợp âm 523/659/784 Hz | 500 ms | −28 dBFS |
| `whoosh.wav` | Nhiễu quét tần số | 350 ms | −28 dBFS |
| `buzz.wav` | Saw 140 Hz, ngắn (✗, cảnh báo) | 180 ms | −30 dBFS |
| `key.wav` | Chuỗi click 40 ms (gõ lệnh) | 40 ms | −30 dBFS |

Quy tắc:
- Voice là lớp ưu tiên cao nhất; SFX không bao giờ phát khi đang đọc thuật ngữ.
- Tối đa 1 SFX mỗi 1,5 s; không phát SFX cho mọi chuyển động nhỏ.
- Không có nhạc nền (mặc định). Nếu bạn muốn nhạc, phải ≤ −32 LUFS và không lấn voice.
- SFX phải khớp hành động: `key.wav` chỉ khi có gõ lệnh, `pen.wav` chỉ khi có nét vẽ.

## 10. Âm thanh tổng

- Voice chuẩn hóa −14 LUFS, true peak ≤ −1 dBTP.
- SFX đặt dưới voice ≥ 10 dB.
- Không clipping; kiểm tra từng đoạn nối cue.

## 11. Quy tắc hình ảnh AI

- **Không dùng ảnh AI** trong video này. Sơ đồ, code, giao diện, biểu tượng đều dựng bằng code.
- Nếu sau này cần ảnh nền/không khí, chỉ dùng texture trừu tượng không chữ, và phải ghi rõ nguồn.

## 12. Checklist trước khi dựng

- [ ] Bảng màu và font đã chốt.
- [ ] Bộ icon Lucide đủ, cùng stroke.
- [ ] Character sheet 4 pose đã render thử và duyệt.
- [ ] Nét vẽ tay khớp cue.
- [ ] SFX có file thật, đã đo mức.
- [ ] Visual sample 30–45 s có: icon, sơ đồ, typography, chuyển động mẫu.
