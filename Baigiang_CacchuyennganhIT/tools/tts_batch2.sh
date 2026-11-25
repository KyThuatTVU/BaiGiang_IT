#!/bin/bash
cd "D:/Edit/Baigiang_CacchuyennganhIT/mau" || exit 1
FF="C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
gen(){ for i in 1 2 3; do python -m edge_tts --voice vi-VN-HoaiMyNeural --rate="$2" --text "$3" --write-media "$1" 2>/dev/null; if [ -s "$1" ]; then echo "OK $1"; return 0; fi; sleep 20; done; echo "FAIL $1"; return 1; }
join(){ "$FF" -y -i "concat:$1|$2" -acodec copy "$3" 2>/dev/null && [ -s "$3" ] && echo "OK $3 (joined)"; }

gen segB1.mp3 "-5%" "với Ếch Ti Em En, Si Ét Ét, Gia-vơ Sờ-críp, và thư viện Ri-ác." || {
  gen b1a.mp3 "-5%" "với Ếch Ti Em En, Si Ét Ét, Gia-vơ Sờ-críp," && \
  gen b1b.mp3 "-5%" "và thư viện Ri-ác." && join b1a.mp3 b1b.mp3 segB1.mp3; }
sleep 20
gen segC_dinhnghia.mp3 "-5%" "Đây là lĩnh vực nghiên cứu, phân tích, thiết kế, xây dựng, kiểm thử, và bảo trì sản phẩm phần mềm." || {
  gen c1.mp3 "-5%" "Đây là lĩnh vực nghiên cứu, phân tích, thiết kế, xây dựng, kiểm thử," && \
  gen c2.mp3 "-5%" "và bảo trì sản phẩm phần mềm." && join c1.mp3 c2.mp3 segC_dinhnghia.mp3; }
sleep 20
gen s10a.mp3 "+10%" "Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử,"
sleep 20
gen s10b.mp3 "+10%" "hệ thống phân tích lịch sử tìm kiếm và mua hàng,"
sleep 20
gen s10c.mp3 "+10%" "để gợi ý những sản phẩm hợp sở thích bạn."
sleep 20
gen s10d.mp3 "+10%" "Đó chính là hệ thống gợi ý sản phẩm, một ứng dụng rất đời thường của Ây Ai."
echo BATCH2_DONE