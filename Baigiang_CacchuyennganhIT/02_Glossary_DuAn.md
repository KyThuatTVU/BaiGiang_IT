# GLOSSARY DỰ ÁN — KHÁM PHÁ CÁC CHUYÊN NGÀNH CNTT

*AN TECH ACADEMY · MASTER DESIGN & VOICE STANDARD 2.2 (mục 3) · Bản trình Cổng A · 12/11/2026*

## Nguyên tắc áp dụng

- AI **đề xuất** cách đọc kèm nguồn; **người duyệt chốt** trước khi tạo voice (3.1). AI không nghe được audio nên không tự ghi "Đã nghe".
- Trạng thái vòng đời: **Đề xuất → Đã duyệt → Đã nghe**. Toàn bộ bảng dưới đây đã được người dùng duyệt ở **Cổng A ngày 12/11/2026** ("Duyệt Cổng A, chọn giọng nữ Việt Nam"); chưa mục nào ở "Đã nghe". "Đã nghe" chỉ được gán sau khi người (hoặc quy trình nghe thật) kiểm tra bản render (3.4).
- Mỗi thuật ngữ ghi rõ đọc tiếng Anh hay Việt hóa và giữ nhất quán toàn video/series.
- Chữ phiên âm cho TTS **không** xuất hiện trên phụ đề/màn hình (3.3); kịch bản ba cột đã tách sẵn.
- **Master Glossary:** chưa tồn tại trong workspace (đã kiểm tra 12/11/2026). Theo yêu cầu "quy tắc hoàn toàn mới, không sao chép dự án cũ", dự án này không kế thừa glossary cũ; Master Glossary sẽ được tạo từ các thuật ngữ đầu tiên được duyệt của dự án này.

## Chú giải nguồn

- **[TD]** IPA chuẩn theo từ điển Cambridge/Oxford — nguồn tham chiếu đề xuất; chưa đối chiếu trực tiếp trong phiên này; người duyệt có thể yêu cầu kiểm chứng lại.
- **[CC]** Quy ước đọc phổ biến của cộng đồng công nghệ / cách đọc tên chính thức; kèm liên kết nếu có.
- **[KD]** Kiến thức chuyên môn ổn định, đã rà soát trong phiên 12/11/2026 (phân loại ngôn ngữ / runtime / thư viện / framework / engine).
- Cột "Người duyệt": để trống chờ người dùng chốt ở Cổng A.

## Chính sách đọc đề xuất cho dự án

1. **Viết tắt & tên ký hiệu** (HTML, CSS, SQL, QA, AI, IT, ERP, UML, BPMN, DNS, DHCP, TCP/IP, C#, C++): đọc tên chữ cái tiếng Anh, phiên âm Việt để TTS đọc ổn định. Riêng SQL chọn đọc từng chữ cái (không đọc "sequel"), giữ nhất quán series.
2. **Từ công nghệ / tên riêng có cách đọc tiếng Anh ổn định**: phiên âm Việt hóa (giữ trọng âm), để giọng Việt đọc nhất quán, tránh TTS tự đoán.
3. **Chức danh nghề nghiệp tiếng Anh**: giữ nguyên chính tả trong bản TTS; kiểm tra ở voice mẫu; nếu đọc sai thì thay bằng phiên âm dự phòng ghi ở cột ghi chú.
4. Mọi phiên âm là **đề xuất**; hiệu chỉnh sau khi nghe voice mẫu (Cổng B) và ghi lại vào hồ sơ dự án.

---

## A. Ngôn ngữ lập trình & ngôn ngữ truy vấn

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| JavaScript | Ngôn ngữ | Tiếng Anh /ˈdʒɑːvəskrɪpt/ ≈ "gia-vơ-sờ-críp" | Trọng âm 1; phân biệt với Java | Gia-vơ Sờ-críp | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Java | Ngôn ngữ | /ˈdʒɑːvə/ ≈ "gia-vơ" | Trọng âm 1; không nhầm JavaScript | Gia-vơ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| PHP | Ngôn ngữ | Từng chữ cái P-H-P /piː eɪtʃ piː/ | Đọc chữ cái, không đọc thành từ | Pi Ếch Pi | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Python | Ngôn ngữ | /ˈpaɪθɑːn/ ≈ "pai-thơn" | Trọng âm 1; /θ/ là "th" thổi nhẹ, không phải "t" | Pai-thơn | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| C# | Ngôn ngữ | "C sharp" /siː ʃɑːp/ ≈ "si sáp" | Không đọc "xê thăng"; thống nhất toàn series | Si Sáp | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| C++ | Ngôn ngữ | "C plus plus" /siː plʌs plʌs/ ≈ "si plớt plớt" | Phương án khác "xê cộng cộng" — chọn 1, giữ nhất quán | Si Plớt Plớt | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| SQL | Ngôn ngữ truy vấn | Từng chữ cái S-Q-L /ɛs kjuː ɛl/ ≈ "ét kiu en" | Chọn đọc chữ cái (không "sequel"); nhất quán series | Ét Kiu En | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |

## B. Runtime, thư viện, framework, engine, phần mềm

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| Node.js | Runtime JavaScript | "node" /noʊd/ + ".js" = "chấm giây ét" | **Runtime**, không phải ngôn ngữ [KD] | Nâu-đờ chấm Giây Ét | [CC]+[KD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| React | Thư viện UI | /riˈækt/ ≈ "ri-ác" | Trọng âm 2; **thư viện**, không gọi là framework [KD] | Ri-ác | [TD]+[KD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Pandas | Thư viện Python | /ˈpændəz/ ≈ "pan-đợz" | Trọng âm 1 | Pan-đợz | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Scikit-learn | Thư viện ML | "sai-kit lơn" /ˈsaɪkɪt lɜːrn/ | Tên ghép SciPy + toolkit; đọc liền "sai-kit" | Sai-kit Lơn | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| TensorFlow | Framework ML | /ˈtɛnsərfləʊ/ ≈ "ten-sơ-phờ-lâu" | Trọng âm 1 | Ten-sơ-phờ-lâu | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| PyTorch | Framework ML | "pai-thoóc" /ˈpaɪtɔːrtʃ/ | "torch" đọc như từ tiếng Anh | Pai Thoóc | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Unity | Game engine | /ˈjuːnəti/ ≈ "du-nơ-ti" | Trọng âm 1; engine, không phải ngôn ngữ [KD] | Du-nơ-ti | [TD]+[KD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Unreal Engine | Game engine | /ʌnˈriːl ˈɛndʒɪn/ ≈ "ăn-riêu en-gin" | Trọng âm "riêu" | Ăn-riêu En-gin | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Blender | Phần mềm 3D | /ˈblɛndər/ ≈ "blen-đờ" | Trọng âm 1 | Blen-đờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |

## C. Viết tắt & ký hiệu

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| HTML | Chuẩn đánh dấu | Chữ cái Anh H-T-M-L ≈ "ếch ti em en" | Không đọc thành từ | Ếch Ti Em En | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| CSS | Chuẩn định kiểu | Chữ cái Anh C-S-S ≈ "si ét ét" | | Si Ét Ét | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| QA | Chất lượng | Chữ cái Anh Q-A /kjuː eɪ/ ≈ "kiu ây" | | Kiu Ây | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| AI | Lĩnh vực | Chữ cái Anh A-I /eɪ aɪ/ ≈ "ây ai" | Nhất quán toàn series | Ây Ai | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| IT | Lĩnh vực | Chữ cái Anh I-T ≈ "ai ti" | | Ai Ti | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| ERP | Hệ thống quản trị | Chữ cái Anh E-R-P ≈ "i a pi" | | I A Pi | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| UML | Ngôn ngữ mô hình | Chữ cái Anh U-M-L ≈ "du em en" | | Du Em En | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| BPMN | Ký hiệu quy trình | Chữ cái Anh B-P-M-N ≈ "bi pi em en" | | Bi Pi Em En | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| DNS | Giao thức/dịch vụ | Chữ cái Anh D-N-S ≈ "đi en ét" | | Đi En Ét | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| DHCP | Giao thức | Chữ cái Anh D-H-C-P ≈ "đi ây si pi" | Không đọc "díp" | Đi Ây Si Pi | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| TCP/IP | Bộ giao thức | "T-C-P trên I-P" ≈ "ti si pi trên ai pi" | Dấu "/" đọc là "trên" | Ti Si Pi trên Ai Pi | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| 3D | Đồ họa | Việt hóa "ba đê" | Nhất quán với "mô hình 3D", "3D Artist" | Ba Đê | [CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Wi-Fi | Mạng không dây | /ˈwaɪfaɪ/ ≈ "oai-fai" | | Oai Fai | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |

## D. Kiến trúc & khái niệm (từ tiếng Anh xuất hiện trên màn hình)

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| Frontend | Kiến trúc | /ˈfrʌntɛnd/ ≈ "phờ-ront-en" | Trọng âm 1; phân biệt Backend | Phờ-ront-en | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Backend | Kiến trúc | /ˈbækɛnd/ ≈ "bắc-en" | Trọng âm 1 | Bắc-en | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Full-stack | Kiến trúc | /fʊl stæk/ ≈ "phun stắc" | | Phun Stắc | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Data Science | Lĩnh vực | /ˈdeɪtə ˈsaɪəns/ ≈ "đây-tơ sai-ơn-xờ" | Trên màn hình ưu tiên tiếng Việt "Khoa học dữ liệu" | Đây-tơ Sai-ơn-xờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Artificial Intelligence | Lĩnh vực | /ˌɑːrtɪˈfɪʃəl ɪnˈtɛlɪdʒəns/ | Lời thoại dùng tiếng Việt "Trí tuệ nhân tạo"; chỉ đọc tiếng Anh nếu hiện chữ Anh | (đọc tiếng Việt trong lời) | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Cybersecurity | Lĩnh vực | /ˌsaɪbərsɪˈkjʊərəti/ ≈ "sai-bơ-si-kiu-rơ-ti" | Lời thoại dùng "An toàn thông tin" | Sai-bơ-si-kiu-rơ-ti | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Cloud Computing | Lĩnh vực | /klaʊd kəmˈpjuːtɪŋ/ ≈ "clau-đờ cơm-piu-tinh" | Lời thoại dùng "Điện toán đám mây" | Clau-đờ Cơm-piu-tinh | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| hacker | Từ thông dụng | /ˈhækər/ ≈ "hắc-cờ" | | Hắc-cờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| website | Từ thông dụng | /ˈwɛbsaɪt/ ≈ "oép-sai-tờ" | | Oép-sai-tờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Internet | Từ thông dụng | /ˈɪntərnɛt/ ≈ "in-tơ-nét" | | In-tơ-nét | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| code | Từ thông dụng | /koʊd/ ≈ "câu-đờ" | Trong lời có thể thay bằng "mã lệnh" nếu người duyệt muốn thuần Việt | Câu-đờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |

## E. Tên riêng & thương hiệu

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| Google | Thương hiệu | /ˈɡuːɡəl/ ≈ "gu-gồ" | | Gu-gồ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| YouTube | Thương hiệu | /ˈjuːtjuːb/ ≈ "du-túp" | | Du-túp | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Amazon Web Services | Thương hiệu | /ˈæməzɒn wɛb ˈsɜːrvɪsɪz/ ≈ "a-ma-dơn oép sơ-vi-xìz" | Viết tắt AWS nếu dùng: "ây đắp-bơ-liu ét" | A-ma-dơn Oép Sơ-vi-xìz | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Microsoft | Thương hiệu | /ˈmaɪkrəsɒft/ ≈ "mai-crơ-sóft" | | Mai-crơ-sóft | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Azure | Thương hiệu | /ˈæʒər/ ≈ "æ-dờ" (Mỹ); phương án /əˈʒʊər/ | /ʒ/ nằm giữa "gi" và "d"; **chốt sau nghe mẫu**; xem nguồn [CC] | Æ-dờ | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Google Cloud | Thương hiệu | "gu-gồ clau-đờ" | | Gu-gồ Clau-đờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Windows Server | Hệ điều hành | /ˈwɪndoʊz ˈsɜːrvər/ ≈ "win-đâu-zơ sơ-vờ" | | Win-đâu-zơ Sơ-vờ | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Linux | Hệ điều hành | /ˈlɪnəks/ ≈ "li-nợks" | Phương án "li-núc" — chọn 1, nhất quán | Li-nợks | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| An Tech Academy | Thương hiệu riêng | "An Tech A-ca-đê-my"; "Tech" /tɛk/ ≈ "tếch" | Viết hoa thống nhất mọi tài sản (1.1) | An Tech A-ca-đê-my | Quy tắc 1.1 · người dùng duyệt 12/11/2026 | Đã duyệt |

Nguồn [CC] cho Azure: thảo luận cộng đồng devops xác nhận /ˈæʒər/ là cách đọc Mỹ phổ biến — https://www.reddit.com/r/devops/comments/1aj2cne/why_do_so_many_people_mispronounce_azure/ ; đối chiếu thêm https://www.reddit.com/r/namenerds/comments/1u4cjfh/i_dont_even_know_how_to_pronounce_my_own_sons_name/ (snippet nêu /ˈæʒ.ər/). Đây là nguồn cộng đồng, không phải phát ngôn chính thức Microsoft; người duyệt chốt.

## F. Chức danh nghề nghiệp (giữ chính tả tiếng Anh trong TTS; kiểm tra ở voice mẫu)

| Thuật ngữ | Nhóm | Cách đọc đề xuất | Trọng âm / ghi chú | Cách viết cho TTS | Nguồn · Người duyệt | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- |
| Frontend Developer | Chức danh | Tiếng Anh | Phiên âm dự phòng: Phờ-ront-en Đì-ve-lớp-phờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Backend Developer | Chức danh | Tiếng Anh | Dự phòng: Bắc-en Đì-ve-lớp-phờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Full-stack Developer | Chức danh | Tiếng Anh | Dự phòng: Phun Stắc Đì-ve-lớp-phờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Software Tester | Chức danh | Tiếng Anh | /ˈsɒftweər ˈtɛstər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| QA Engineer | Chức danh | Tiếng Anh, QA đọc chữ cái | Dự phòng: Kiu Ây En-gi-nia | Giữ nguyên | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Data Analyst | Chức danh | Tiếng Anh | /ˈdeɪtə ˈænəlɪst/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Data Scientist | Chức danh | Tiếng Anh | /ˈdeɪtə ˈsaɪəntɪst/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Machine Learning Engineer | Chức danh | Tiếng Anh | /məˈʃiːn ˈlɜːrnɪŋ ˌɛndʒɪˈnɪər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| AI Engineer | Chức danh | Tiếng Anh, AI đọc chữ cái | Dự phòng: Ây Ai En-gi-nia | Giữ nguyên | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Security Analyst | Chức danh | Tiếng Anh | /sɪˈkjʊərəti ˈænəlɪst/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Penetration Tester | Chức danh | Tiếng Anh | /ˌpɛnɪˈtreɪʃən ˈtɛstər; dự phòng: Pe-ni-trây-sần Tét-tờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Security Engineer | Chức danh | Tiếng Anh | Dự phòng: Si-kiu-rơ-ti En-gi-nia | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Business Analyst | Chức danh | Tiếng Anh | /ˈbɪznɪs ˈænəlɪst/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| System Analyst | Chức danh | Tiếng Anh | /ˈsɪstəm ˈænəlɪst/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Database Administrator | Chức danh | Tiếng Anh | /ˈdeɪtəbeɪs ədˈmɪnɪstreɪtər/; dự phòng: Đây-tơ-bây-ớt Át-mi-ni-stry-tờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Network Engineer | Chức danh | Tiếng Anh | /ˈnɛtwɜːrk ˌɛndʒɪˈnɪər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| System Administrator | Chức danh | Tiếng Anh | /ˈsɪstəm ədˈmɪnɪstreɪtər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Cloud Engineer | Chức danh | Tiếng Anh | /klaʊd ˌɛndʒɪˈnɪər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| IT Support | Chức danh | Tiếng Anh, IT đọc chữ cái | Dự phòng: Ai Ti Sớp-pót | Giữ nguyên | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Game Developer | Chức danh | Tiếng Anh | /ɡeɪm dɪˈvɛləpər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Game Designer | Chức danh | Tiếng Anh | /ɡeɪm dɪˈzaɪnər/ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |
| 3D Artist | Chức danh | "ba đê" + Artist tiếng Anh | Dự phòng: Ba Đê Át-tít | Giữ nguyên | [TD]+[CC] · người dùng duyệt 12/11/2026 | Đã duyệt |
| Graphics Programmer | Chức danh | Tiếng Anh | /ˈɡræfɪks ˈproʊɡræmər/; dự phòng: Grá-phích Prâu-gram-mờ | Giữ nguyên | [TD] · người dùng duyệt 12/11/2026 | Đã duyệt |

---

## Việc cần người duyệt chốt ở Cổng A — ĐÃ HOÀN TẤT 12/11/2026

1. Cách đọc đề xuất đã được duyệt nguyên khối ở Cổng A; các mục nhạy cảm (SQL đọc chữ cái, C# "si sáp", Azure "æ-dờ", Linux "li-nợks", C++ "si plớt plớt") giữ nguyên đề xuất và sẽ nghe kiểm tra ở bản mẫu.
2. Chính sách phiên âm 3 nhóm ở đầu file: đã duyệt.
3. Sau Cổng B (nghe voice mẫu), hiệu chỉnh phiên âm nào TTS đọc chưa đạt và ghi trạng thái mới; chỉ người nghe thật mới gán "Đã nghe".