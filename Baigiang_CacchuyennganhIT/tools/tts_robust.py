import json, os, subprocess, time

MAU = "D:/Edit/Baigiang_CacchuyennganhIT/mau"
ITEMS = {
    "b_f4": {"rate": "-5%", "variants": ["và thư viện React", "và thư viện ri-ác", "và thư viện Ri-ác", "thư viện React"]},
    "s10a": {"rate": "+10%", "variants": ["Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử", "Ví dụ: bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử.", "bạn vừa xem một chiếc điện thoại trên trang thương mại điện tử"]},
}
ROUNDS = 10
state_path = f"{MAU}/tts_state.json"
state = json.load(open(state_path)) if os.path.exists(state_path) else {}

for rnd in range(ROUNDS):
    pending = [k for k in ITEMS if k not in state]
    if not pending:
        break
    for k in pending:
        v = ITEMS[k]["variants"][rnd % len(ITEMS[k]["variants"])]
        p = f"{MAU}/{k}.mp3"
        try:
            subprocess.run(["python", "-m", "edge_tts", "--voice", "vi-VN-HoaiMyNeural", f"--rate={ITEMS[k]['rate']}", "--text", v, "--write-media", p], capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            pass
        ok = os.path.exists(p) and os.path.getsize(p) > 0
        print(f"[{time.strftime('%H:%M:%S')}] round{rnd} {k} variant{rnd % len(ITEMS[k]['variants'])} {'OK' if ok else 'FAIL'}", flush=True)
        if ok:
            state[k] = {"variant": v, "round": rnd}
            json.dump(state, open(state_path, "w"), ensure_ascii=False, indent=2)
        else:
            if os.path.exists(p):
                os.remove(p)
    if [k for k in ITEMS if k not in state]:
        time.sleep(60)
print("ROBUST_DONE", json.dumps(state, ensure_ascii=False))