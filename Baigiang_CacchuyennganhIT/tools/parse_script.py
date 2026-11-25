import json, os, re

ROOT = "D:/Edit/Baigiang_CacchuyennganhIT"
src = open(ROOT + "/01_KichBan_BaCot.md", encoding="utf-8").read()
scenes = re.split(r"^### (S\d\d) · ", src, flags=re.M)
manifest = []
for i in range(1, len(scenes), 2):
    sid = scenes[i]
    body = scenes[i + 1]
    n = 0
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0].startswith("Chữ hiển thị") or set(cells[0]) <= {"-", " "}:
            continue
        n += 1
        subs = [s.strip() for s in cells[0].split("<br>")]
        tts = cells[1].replace("…", ",")
        pause = 0.0
        m = re.search(r"\[nghỉ (\d+) s\]", tts)
        if m:
            pause = float(m.group(1))
            tts = tts.replace(m.group(0), "")
        tts = re.sub(r",\s*,", ",", tts)
        tts = re.sub(r"\s+", " ", tts).strip()
        direction = cells[2]
        rate = "-5%" if any(k in direction for k in ["Thuật ngữ", "Định nghĩa", "chậm"]) else "+10%"
        manifest.append({"id": f"{sid}c{n}", "scene": sid, "rate": rate, "text": tts, "subs": subs, "pause_after": pause, "direction": direction})
os.makedirs(ROOT + "/mau/full", exist_ok=True)
json.dump(manifest, open(ROOT + "/mau/full/manifest.json", "w"), ensure_ascii=False, indent=1)
bad = [c["id"] for c in manifest for l in c["subs"] if len(l) > 42]
print("cues:", len(manifest), "scenes:", len({c['scene'] for c in manifest}), "slow:", sum(c["rate"] == "-5%" for c in manifest), "pauses:", [(c["id"], c["pause_after"]) for c in manifest if c["pause_after"]], "sub_violations:", bad)