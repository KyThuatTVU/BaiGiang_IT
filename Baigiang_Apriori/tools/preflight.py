import json, os, subprocess, sys

ROOT = "D:/Edit/Baigiang_Apriori"
FULL = ROOT + "/mau/full"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"

TERMS = [
    ("S03c2", "Apriori — thuật toán"),
    ("S03c3", "giao dịch (transaction)"),
    ("S06c1", "Support"),
    ("S14c2", "Confidence"),
    ("S15c1", "Lift"),
    ("S18c1", "Flask"),
    ("S18c3", "JSON"),
    ("S23c2", "mlxtend"),
]

state = json.load(open(FULL + "/tts_state.json", encoding="utf-8"))
man = {c["id"]: c for c in json.load(open(FULL + "/manifest.json", encoding="utf-8"))}

missing = [cid for cid, _ in TERMS if cid not in state or not os.path.exists(FULL + "/audio/" + cid + ".mp3")]
if missing:
    sys.exit("MISSING " + ",".join(missing))

sil = FULL + "/pf_sil.mp3"
subprocess.run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.7",
                "-c:a", "libmp3lame", "-b:a", "48k", sil], check=True, capture_output=True)
lst = FULL + "/pf_list.txt"
lines = []
for cid, _ in TERMS:
    lines.append("file '" + FULL + "/audio/" + cid + ".mp3'")
    lines.append("file '" + sil + "'")
open(lst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
out = FULL + "/preflight_terms.mp3"
subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "libmp3lame", "-b:a", "96k", out],
               check=True, capture_output=True)

with open(FULL + "/preflight_terms.txt", "w", encoding="utf-8") as f:
    t = 0.0
    for cid, label in TERMS:
        d = state[cid]["dur"]
        f.write(f"{t:6.2f}s  {cid}  {label}  ({d:.2f}s)\n")
        t += d + 0.7
print("PREFLIGHT_DONE", out, f"{t:.2f}s")
