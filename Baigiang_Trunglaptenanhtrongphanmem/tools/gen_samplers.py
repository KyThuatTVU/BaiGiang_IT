import os
import sys

# Đảm bảo đường dẫn Kit
sys.path.insert(0, r"D:\Edit\Kit\tools")
import tts_vieneu

OUT_DIR = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem\mau\sample\samplers"
os.makedirs(OUT_DIR, exist_ok=True)

samples = [
    ("tech_raw", "Chúng ta sẽ sử dụng HTML, CSS, PHP và MySQL để xử lý hệ thống."),
    ("tech_phonetic", "Chúng ta sẽ sử dụng Át-ti-em-eo, Xi-ét-ét, Pi-ếch-pi và Mai-ét-kiu-eo để xử lý hệ thống."),
    ("uuid_raw", "Hệ thống có thể tạo tên file mới bằng chuỗi UUID ngẫu nhiên."),
    ("uuid_phonetic", "Hệ thống có thể tạo tên file mới bằng chuỗi Diu-diu-ai-đi ngẫu nhiên."),
    ("sha_raw", "Thuật toán SHA-256 giúp kiểm tra nội dung byte của hai file."),
    ("sha_phonetic", "Thuật toán Ét-hát-a hai năm sáu giúp kiểm tra nội dung bai của hai file."),
    ("pdo_raw", "Chúng ta sử dụng PDO và Prepared Statements để kết nối cơ sở dữ liệu."),
    ("pdo_phonetic", "Chúng ta sử dụng Pi-đi-ô và Pri-pe-đờ Stết-mân để kết nối cơ sở dữ liệu."),
]

print("Bắt đầu sinh samplers với VieNeu...")
for name, text in samples:
    out_wav = os.path.join(OUT_DIR, f"{name}.wav")
    print(f"Generating: {name}...")
    tts_vieneu.synth(text, out_wav)
    print(f"-> {out_wav} ({os.path.getsize(out_wav)} bytes)")

print("Hoàn tất sinh samplers!")
