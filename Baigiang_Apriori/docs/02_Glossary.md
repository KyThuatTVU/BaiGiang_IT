# 02 — BẢNG THUẬT NGỮ VÀ CÁCH ĐỌC

Quy tắc: cột **Bản TTS** là chữ đưa vào edge-tts (phiên âm Việt để giọng đọc tự nhiên); cột **Hiển thị** là chữ trên màn hình/phụ đề. Không để phiên âm xuất hiện trên hình.

| Thuật ngữ | Nhóm | Cách đọc chốt | Bản TTS | Hiển thị | Trạng thái |
|---|---|---|---|---|---|
| Apriori | Thuật toán | a-pri-o-ri | A-pri-o-ri | Apriori | Chờ nghe lại |
| Support | Chỉ số | súp-pọt | sấp-pọt | Support | Chờ nghe lại |
| Confidence | Chỉ số | con-fi-đần | con-fi-đần | Confidence | Chờ nghe lại |
| Lift | Chỉ số | líp | líp | Lift | Chờ nghe lại |
| itemset | Khái niệm | ai-tầm-sét | ai-tầm-sét | itemset | Chờ nghe lại |
| transaction | Dữ liệu | tờ-ranh-dắc-sần | tờ-ranh-dắc-sần | transaction | Chờ nghe lại |
| TransactionEncoder | Lớp thư viện | tờ-ranh-dắc-sần en-cô-đờ | tờ-ranh-dắc-sần en-cô-đờ | TransactionEncoder | Chờ nghe lại |
| pandas | Thư viện | pan-đát | pan-đát | pandas | Chờ nghe lại |
| mlxtend | Thư viện | em-lờ-ích-ten | em-lờ-ích-ten | mlxtend | Chờ nghe lại |
| Flask | Framework | phờ-lát | phờ-lát | Flask | Chờ nghe lại |
| Python | Ngôn ngữ | pai-thờn | pai-thờn | Python | Chờ nghe lại |
| API | Giao tiếp | ây-pi-ai | ây-pi-ai | API | Chờ nghe lại |
| JSON | Định dạng | giây-sần | giây-sần | JSON | Chờ nghe lại |
| Frontend | Kiến trúc | phờ-ron-en | phờ-ron-en | Frontend | Chờ nghe lại |
| Backend | Kiến trúc | bếch-en | bếch-en | Backend | Chờ nghe lại |
| endpoint /recommend | Giao tiếp | ri-cô-men | ri-cô-men | /recommend | Chờ nghe lại |
| fetch | Web API | phét | phét | fetch | Chờ nghe lại |
| min_support | Tham số | min sấp-pọt | min sấp-pọt | min_support | Chờ nghe lại |
| one-hot / nhị phân | Dữ liệu | (nói "bảng nhị phân") | — | One-hot (1/0) | Đạt (không đọc thuật ngữ Anh) |
| association_rules | Hàm | (nói "hàm tạo luật kết hợp") | — | association_rules | Đạt (tránh đọc sai) |
| FP-Growth | Thuật toán | ép-pi grâu-th | ép-pi grâu-th | FP-Growth | Chờ nghe lại |
| T1…T10 | Nhãn | tê một … tê mười | — | T1…T10 | Đạt |
| 60% | Số liệu | sáu mươi phần trăm | sáu mươi phần trăm | 60% | Đạt |
| 1,25 | Số liệu | một phẩy hai lăm | một phẩy hai lăm | 1,25 | Đạt |

**Giới hạn:** edge-tts không có từ điển phát âm; cách đọc chỉ kiểm chứng được bằng việc nghe lại. Sau khi người dùng duyệt mẫu, nếu có từ đọc sai, sửa cột Bản TTS và render lại đúng cue đó (ghi timestamp).
