import os
import sys

sys.path.insert(0, r"D:\Edit\Kit\tools")
import tts_vieneu

OUT_DIR = r"D:\Edit\Baigiang_Trunglaptenanhtrongphanmem\mau\sample\audio"
os.makedirs(OUT_DIR, exist_ok=True)

cues = [
    ("c01", "Xin chào các bạn! Chào mừng đến với AN TECH ACADEMY, nền tảng kiến thức công nghệ thực chiến."),
    ("c02", "Hãy tưởng tượng chúng ta đang xây dựng một ứng dụng quản lý người dùng."),
    ("c03", "Người dùng A tải lên ảnh đại diện tên 1.jpg là ảnh chân dung của mình."),
    ("c04", "Cùng lúc đó, người dùng B cũng tải lên một ảnh tên 1.jpg, nhưng lại là ảnh một chú mèo dễ thương."),
    ("c05", "Nếu hệ thống chỉ lưu theo tên file vào một thư mục chung, chuyện gì sẽ xảy ra?"),
    ("c06", "Đúng vậy, ảnh của người dùng A sẽ bị ảnh của người dùng B ghi đè hoàn toàn!"),
]

print("Bắt đầu sinh 6 audio cues cho video mẫu Cổng B...")
for cid, text in cues:
    out_wav = os.path.join(OUT_DIR, f"{cid}.wav")
    print(f"Generating {cid}: {text[:30]}...")
    tts_vieneu.synth(text, out_wav)
    print(f"-> {out_wav} ({os.path.getsize(out_wav)} bytes)")

print("Hoàn tất sinh audio mẫu Cổng B!")
