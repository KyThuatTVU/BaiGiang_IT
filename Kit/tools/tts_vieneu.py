# -*- coding: utf-8 -*-
"""TTS giọng clone cục bộ (VieNeu-TTS) -> WAV 48 kHz.

Dùng từ code khác:  import tts_vieneu;  tts_vieneu.synth(text, "out.wav")
CLI một câu:        python tts_vieneu.py --text "Xin chào" --out test.wav
CLI manifest:       python tts_vieneu.py --manifest manifest.json --out <thư mục>
Env: VIENEU_REF (file giọng mẫu), VIENEU_PRECISION (int8|fp32), VIENEU_THREADS.
"""
import json, os, sys, time

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.environ.get("VIENEU_REF", KIT + "/cache/ref_voice/ref_final.wav")
PREC = os.environ.get("VIENEU_PRECISION", "int8")
THREADS = int(os.environ.get("VIENEU_THREADS", "8"))

_tts = None


def _clear_proxy():
    os.environ["HF_HUB_OFFLINE"] = "1"
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
              "http_proxy", "https_proxy", "all_proxy", "no_proxy"):
        os.environ.pop(k, None)


def engine():
    global _tts
    if _tts is None:
        _clear_proxy()
        from vieneu import Vieneu
        t0 = time.time()
        _tts = Vieneu(precision=PREC, threads=THREADS)
        _tts.encode_reference(REF)
        print(f"VieNeu ready ({PREC}, {time.time() - t0:.0f}s)", flush=True)
    return _tts


def synth(text, out, retries=2):
    if os.path.exists(out) and os.path.getsize(out) > 20000:
        return out
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    tmp = out + ".tmp.wav"
    for rnd in range(retries + 1):
        wav = engine().infer(text, ref_audio=REF)
        if len(wav) >= 48000 * 0.3:
            engine().save(wav, tmp)
            os.replace(tmp, out)
            return out
        print(f"VieNeu short r{rnd}: {text}", flush=True)
    raise RuntimeError("VieNeu synth fail: " + text)


def main():
    args = sys.argv[1:]
    if "--text" in args:
        text = args[args.index("--text") + 1]
        out = args[args.index("--out") + 1] if "--out" in args else "vieneu_test.wav"
        synth(text, out)
        print("OK", out, flush=True)
        return
    if "--manifest" in args:
        man = json.load(open(args[args.index("--manifest") + 1], encoding="utf-8"))
        outdir = args[args.index("--out") + 1]
        os.makedirs(outdir, exist_ok=True)
        state_p = outdir + "/state.json"
        state = json.load(open(state_p, encoding="utf-8")) if os.path.exists(state_p) else {}
        for c in man:
            p = synth(c["say"], f"{outdir}/{c['id']}.wav")
            state[c["id"]] = {"bytes": os.path.getsize(p)}
            json.dump(state, open(state_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("OK", c["id"], os.path.getsize(p), flush=True)
        return
    print(__doc__)


if __name__ == "__main__":
    main()
