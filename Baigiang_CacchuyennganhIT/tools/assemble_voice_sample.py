import json, re, subprocess, sys
from fractions import Fraction

MAU = "D:/Edit/Baigiang_CacchuyennganhIT/mau"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

TEXTS = {
    "segA1": ("+10%", "Xin chào các bạn! Chào mừng đến với An Tech A-ca-đê-my, nơi chúng ta cùng khám phá công nghệ theo cách dễ hiểu, và thực tế nhất."),
    "segA2": ("+10%", "Hôm nay, chúng ta sẽ mở tấm bản đồ sáu chuyên ngành của Công nghệ thông tin, để bạn tìm ra con đường phù hợp với mình."),
    "segB1": ("-5%", "với Ếch Ti Em En, Si Ét Ét, Gia-vơ Sờ-críp, và thư viện Ri-ác."),
    "segB2": ("-5%", "Công nghệ thường gặp là Nâu-đờ chấm Giây Ét, Gia-vơ, Pi Ếch Pi, Pai-thơn, và Si Sáp."),
    "segC_dinhnghia": ("-5%", "Đây là lĩnh vực nghiên cứu, phân tích, thiết kế, xây dựng, kiểm thử, và bảo trì sản phẩm phần mềm."),
}

def syl(text):
    n = 0
    for tok in text.split():
        tok = re.sub(r"[^\wÀ-ỹ-]", "", tok, flags=re.UNICODE)
        if not tok:
            continue
        n += len(tok.split("-")) if "-" in tok else 1
    return n

def dur(path):
    r = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", r.stderr)
    h, mi, s = m[-1]
    return int(h) * 3600 + int(mi) * 60 + float(s)

for k in TEXTS:
    import os
    p = f"{MAU}/{k}.mp3"
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        print(f"MISSING {k}")
        sys.exit(1)

rows = []
GAPS = {"segB1": 0.0, "segC_dinhnghia": 0.2}
for k, (rate, text) in TEXTS.items():
    d = dur(f"{MAU}/{k}.mp3")
    n = syl(text)
    speech_d = d - GAPS.get(k, 0.0)
    rows.append({"seg": k, "rate": rate, "dur_s": round(d, 2), "speech_s": round(speech_d, 2), "syllables": n, "syl_per_s": round(n / speech_d, 2)})

for name, sec in [("sil03", 0.3), ("sil05", 0.5)]:
    subprocess.run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(sec), "-q:a", "9", f"{MAU}/{name}.mp3"], capture_output=True)

parts = ["segA1", "sil03", "segA2", "sil05", "segB1", "sil03", "segB2"]
with open(f"{MAU}/voice_concat.txt", "w") as f:
    for p in parts:
        f.write(f"file '{MAU}/{p}.mp3'\n")
subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", f"{MAU}/voice_concat.txt", "-c", "copy", f"{MAU}/voice_sample.mp3"], capture_output=True)
total = dur(f"{MAU}/voice_sample.mp3")
speech = sum(r["speech_s"] for r in rows[:4])
syls = sum(r["syllables"] for r in rows[:4])
out = {"segments": rows, "voice_sample_total_s": round(total, 2), "speech_s": round(speech, 2), "overall_syl_per_s": round(syls / speech, 2)}
with open(f"{MAU}/voice_measurements.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False, indent=2))
print("ASSEMBLE_DONE")