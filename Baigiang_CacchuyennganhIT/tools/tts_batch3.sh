#!/bin/bash
cd "D:/Edit/Baigiang_CacchuyennganhIT/mau" || exit 1
gen(){ echo "[$(date +%H:%M:%S)] TRY $1"; python -m edge_tts --voice vi-VN-HoaiMyNeural --rate="$2" --text "$3" --write-media "$1" 2>/dev/null; if [ -s "$1" ]; then echo "OK $1"; else echo "FAIL $1"; fi; }
sleep 30
gen bis_c2.mp3 "-5%" "và bảo trì sản phẩm phần mềm."
sleep 45
gen segB1.mp3 "-5%" "với Ếch Ti Em En, Si Ét Ét, Gia-vơ Sờ-críp, và thư viện Ri-ác."
sleep 45
gen segC_dinhnghia.mp3 "-5%" "Đây là lĩnh vực nghiên cứu, phân tích, thiết kế, xây dựng, kiểm thử, và bảo trì sản phẩm phần mềm."
sleep 45
gen test_long.mp3 "+10%" "Xin chào các bạn! Chào mừng đến với An Tech A-ca-đê-my, nơi chúng ta cùng khám phá công nghệ theo cách dễ hiểu, và thực tế nhất. Hôm nay, chúng ta sẽ mở tấm bản đồ sáu chuyên ngành của Công nghệ thông tin, để bạn tìm ra con đường phù hợp với mình."
sleep 45
gen test_ellipsis.mp3 "+10%" "Không chỉ một lập trình viên đâu… mà là cả một đội ngũ."
sleep 45
gen s10a.mp3 "+10%" "Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử,"
sleep 45
gen s10b.mp3 "+10%" "hệ thống phân tích lịch sử tìm kiếm và mua hàng,"
sleep 45
gen s10c.mp3 "+10%" "để gợi ý những sản phẩm hợp sở thích bạn."
sleep 45
gen s10d.mp3 "+10%" "Đó chính là hệ thống gợi ý sản phẩm, một ứng dụng rất đời thường của Ây Ai."
echo BATCH3_DONE