#!/bin/bash
cd "D:/Edit/Baigiang_CacchuyennganhIT/mau" || exit 1
gen(){ echo "[$(date +%H:%M:%S)] TRY $1"; timeout 60 python -m edge_tts --voice vi-VN-HoaiMyNeural --rate="$2" --text "$3" --write-media "$1" 2>/dev/null; if [ -s "$1" ]; then echo "OK $1"; else echo "FAIL $1"; rm -f "$1"; fi; }
gen b_f3.mp3 "-5%" "Gia-vơ sờ-críp,"
[ -s b_f3.mp3 ] || gen b_f3.mp3 "-5%" "sờ-críp,"
sleep 10
gen b_f4.mp3 "-5%" "và thư viện React"
[ -s b_f4.mp3 ] || gen b_f4.mp3 "-5%" "và thư viện Ri-ắc"
sleep 10
gen s10a.mp3 "+10%" "Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử"
[ -s s10a.mp3 ] || { gen a_f1.mp3 "+10%" "bạn vừa xem một chiếc điện thoại"; sleep 10; gen a_f2.mp3 "+10%" "trên trang thương mại điện tử"; }
echo BATCH4_DONE