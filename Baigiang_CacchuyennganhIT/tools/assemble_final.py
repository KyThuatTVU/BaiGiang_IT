import json, os, subprocess

MAU = "D:/Edit/Baigiang_CacchuyennganhIT/mau"
FF = "C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
state = json.load(open(f"{MAU}/tts_state.json"))
assert "b_f4" in state and "s10a" in state, state

for name, sec in [("sil012", 0.12), ("sil015", 0.15)]:
    subprocess.run([FF, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(sec), "-q:a", "9", f"{MAU}/{name}.mp3"], capture_output=True)

def concat(parts, out):
    lst = f"{MAU}/{out}.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{MAU}/{p}.mp3'\n")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{MAU}/{out}.mp3"], capture_output=True)
    assert os.path.getsize(f"{MAU}/{out}.mp3") > 0

concat(["bis_b1a1", "sil012", "mp_css_en", "sil012", "b_f3", "sil012", "b_f4"], "segB1")
if state["s10a"]["variant"].startswith("Ví dụ"):
    concat(["s10a"], "s10a_final")
else:
    concat(["fx_vidu", "sil015", "s10a"], "s10a_final")
os.replace(f"{MAU}/s10a_final.mp3", f"{MAU}/s10a.mp3")
print("FINAL_ASSEMBLE_DONE")