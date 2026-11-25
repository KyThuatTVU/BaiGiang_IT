# 00 · Hồ sơ phân tích — Bài 12: Load Balancer

## Bước 0 — Khai báo năng lực công cụ

| Việc | Trạng thái | Ghi chú |
|---|---|---|
| Render video 1920×1080, 30 fps | Làm được | PIL vẽ từng khung + ffmpeg encode/xfade |
| Sơ đồ, icon, code panel vector | Làm được | Vẽ bằng code, một bộ icon Lucide cục bộ |
| Hiệu ứng "vẽ tay" | Làm được một phần | Nét marker theo quỹ đạo + reveal, không phải nét cọ thật |
| Phụ đề burn-in | Làm được | SRT cũng được xuất kèm bản dựng |
| SFX, nhạc nền | Làm được | Tổng hợp bằng code, không phải thư viện thu |
| Thu giọng người miền Nam | KHÔNG | Bản mẫu dùng Edge `vi-VN-NamMinhNeural` tạm, đã khai báo |
| Nghe kiểm phát âm / cảm xúc | KHÔNG | Sẽ ghi "Chưa thể xác minh", nhờ bạn nghe |
| Đồng bộ tiếng–hình–phụ đề | Kiểm được bằng số liệu | Đo độ dài cue và offset, không kiểm bằng tai |

## 7.1 Phân tích

**Người học sau video hiểu/làm được:**
- Giải thích Load Balancer là gì và vì sao cần nó khi traffic tăng.
- Kể được 4 thành phần cơ bản: Client → Load Balancer → Backend → Database.
- Phân biệt 4 thuật toán: Round Robin, Weighted RR, Least Connections, IP Hash.
- Hiểu Health Check loại server lỗi khỏi nhóm phục vụ.
- Biết ví dụ thực tế (Nginx, HAProxy, AWS ELB) và giới hạn của Load Balancer.

**Kiến thức trọng tâm:** vai trò điều phối (không xử lý nghiệp vụ), luồng request, thuật toán chọn server, health check. **Lược bỏ:** TLS termination, OSI layer 4/7 chuyên sâu, sticky session chi tiết, giá dịch vụ cloud, cấu hình Nginx nâng cao.

**Hình ảnh:** tài liệu gốc không kèm ảnh chụp; cảnh S02 dùng 3 ảnh minh họa AI (đám đông mua sắm, server quá nhiệt, màn hình cảnh báo) — đã ghi rõ là hình minh họa, không phải ảnh chụp hệ thống thật. Các cảnh còn lại dùng sơ đồ vector tự dựng.

**Ví dụ thực tế:** cao điểm 12/12; trạm thu phí nhiều làn; trang chi tiết điện thoại; Nginx reverse proxy với dải IP nội bộ.

**Thời lượng dự kiến:** ~5 phút (28 cue, 10 cảnh). Chốt lại sau khi thu giọng thật.

## Hồ sơ dự án

- Dự án mới: `D:\Edit\Baigiang_LoadBalancer_v2`
- Bản cũ 4:50: `D:\Edit\Baigiang_LoadBalancer` — **giữ nguyên, không sửa**
- Mẫu 30–45 giây: S01–S03, ghép từ timeline thật của bản mẫu
- Prompt áp dụng: `D:\Edit\AnTechAcademy_PromptSanXuatVideo_v1.md`

## Giới hạn đã biết

- Bản mẫu dùng giọng Edge tạm (không phải giọng miền Nam cuối cùng) để duyệt hình, nhịp, phụ đề.
- Chưa thể xác minh phát âm thuật ngữ, cảm xúc và độ đồng bộ bằng tai.
