# -*- coding: utf-8 -*-
import json, os, glob

FULL = "D:/Edit/Baigiang_Apriori/mau/full"
sp = FULL + "/tts_state.json"
state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
for f in glob.glob(FULL + "/tts_state_s*.json"):
    state.update(json.load(open(f, encoding="utf-8")))
json.dump(state, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

manifest = json.load(open(FULL + "/manifest.json", encoding="utf-8"))
ids = [c["id"] for c in manifest]
miss = [i for i in ids if i not in state or not os.path.exists(f"{FULL}/audio/{i}.mp3")]
print("MERGE total", len(state), "expected", len(ids), "missing", len(miss), miss[:15])
print("TOTAL_DUR", round(sum(state[i]["dur"] for i in ids if i in state), 2))
