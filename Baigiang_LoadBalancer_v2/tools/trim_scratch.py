# -*- coding: utf-8 -*-
"""Cắt im lặng voice tạm sample, xuất WAV 48k và cập nhật tts_state_sample."""
import json, os, shutil, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_human_prep import decode, trim, SR

FULL = "D:/Edit/Baigiang_LoadBalancer_v2/mau"
AUD = FULL + "/audio_sample"
SRC = AUD + "/edge_src"
MAN = FULL + "/manifest_sample.json"
STATE = FULL + "/tts_state_sample.json"


def main():
    st_name = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "sample"
    if st_name == "full":
        AUD, MAN, STATE = FULL + "/audio", FULL + "/manifest.json", FULL + "/tts_state.json"
    else:
        AUD, MAN, STATE = (FULL + "/audio_sample", FULL + "/manifest_sample.json",
                           FULL + "/tts_state_sample.json")
    SRC = AUD + "/edge_src"
    os.makedirs(SRC, exist_ok=True)
    man = json.load(open(MAN, encoding="utf-8"))
    st = json.load(open(STATE, encoding="utf-8"))
    old = new = 0.0
    for c in man:
        cid = c["id"]
        mp3, wav = f"{AUD}/{cid}.mp3", f"{AUD}/{cid}.wav"
        src = mp3 if os.path.exists(mp3) else (wav if os.path.exists(wav) else None)
        if not src:
            print(cid, "MISSING")
            continue
        x = decode(src)
        old += len(x) / SR
        y, lead, tail = trim(x)
        y = y - np.mean(y)
        f = int(0.008 * SR)
        if f * 2 < len(y):
            y[:f] *= np.linspace(0, 1, f)
            y[-f:] *= np.linspace(1, 0, f)
        tmp = wav + ".tmp"
        with wave.open(tmp, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.clip(y * 32767, -32768, 32767).astype("<i2").tobytes())
        os.replace(tmp, wav)
        d = len(y) / SR
        new += d
        st[cid]["dur"] = round(d, 3)
        st[cid]["trimmed"] = True
        if os.path.exists(mp3):
            shutil.move(mp3, f"{SRC}/{cid}.mp3")
        print(f"{cid} {len(x)/SR:.2f}->{d:.2f}s", flush=True)
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"TRIM_DONE {old:.1f}->{new:.1f}s")


if __name__ == "__main__":
    main()
