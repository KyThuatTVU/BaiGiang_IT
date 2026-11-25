# 05 · Thiết kế SFX — Bài 12: Load Balancer

Âm thanh tổng hợp bằng code (không dùng thư viện thu). Mức đặt dưới giọng đọc; toàn bộ mix qua loudnorm −14 LUFS.
**Chưa nghe kiểm trên loa thật.**

| Âm | Mô tả | Dùng khi | Gain |
|---|---|---|---|
| pop | Tiếng "bụp" ngắn, mềm | Card/chip xuất hiện, mở cảnh | 0,18–0,22 |
| whoosh | Gió lướt nhẹ | Chuyển ý, tab mới, sơ đồ hiện | 0,16 |
| tick | Tích tắc nhỏ | Gói tin nhảy server, probe, gõ code | 0,10–0,16 |
| marker | Nét bút sột soạt | Khi nét vẽ tay chạy | 0,14–0,16 |
| deny | Hai nốt đi xuống | Quá tải, lỗi, giới hạn | 0,18–0,24 |
| thud | Trầm ngắn | Server sập / TIMEOUT | 0,18–0,20 |
| success | Hai nốt đi lên | Hồi phục, hoàn tất | 0,16–0,20 |
| chime | Chuông nhẹ | Chốt ý, CTA | 0,12–0,16 |
| music | Pad ấm + pluck, vòng Am–F–C–G, 84 BPM | Nền toàn video | 0,55 × loop, không lời |

## Theo cảnh

| Cảnh | SFX |
|---|---|
| S01 | pop (0,3s), whoosh (cue 2), pop (cue 2 + 0,5s) |
| S02 | pop, deny + thud khi quá tải, marker khi gạch chân |
| S03 | pop, whoosh khi mở trạm thu phí, marker, chime chốt |
| S04 | pop, whoosh cue 2, tick gói tin |
| S05 | pop, tick ×2, whoosh scale-out, success |
| S06 | pop, whoosh đổi tab, tick ×5 mỗi thuật toán, whoosh sang WRR |
| S07 | pop, tick, whoosh IP Hash, tick, chime, marker điều kiện |
| S08 | pop, tick probe ×8, deny + thud khi S02 lỗi, success khi hồi phục |
| S09 | pop, whoosh, tick gõ code ×2, deny giới hạn, chime |
| S10 | pop, chime, success CTA, chime |

## Quy tắc

- Không đặt SFX dày hơn 1 âm/0,6 giây; ưu tiên im lặng khi giảng định nghĩa.
- SFX không che phụ âm cuối của từ; nếu trùng, dời muộn 0,1–0,2 giây.
- Nhạc nền vào 0,6 giây, ra 1,6 giây ở cuối; không dùng tiếng người trong nhạc.
- Nếu người thu thấy khó chịu ở đoạn nào, giảm gain 30% hoặc bỏ SFX đoạn đó (không đổi nhịp hình).
