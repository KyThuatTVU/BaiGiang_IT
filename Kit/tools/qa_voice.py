# -*- coding: utf-8 -*-
"""QA giọng thuyết minh: ASR + F0 + loudness. Không thay thế việc nghe của người duyệt.

Dùng: python qa_voice.py <audio|video> [--ref <wav>] [--json <out.json>]
Kết quả in ra: độ dài, loudness (LUFS/TP), F0 trung vị (Hz), tốc độ nói, transcript ASR.
"""
import json, os, re, subprocess, sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = ("C:/Users/ACER/AppData/Local/Python/pythoncore-3.14-64/Lib/"
      "site-packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
WHISPER = (r"C:\Users\ACER\.cache\huggingface\hub\models--Systran--faster-whisper-small"
           r"\snapshots\536b0662742c02347bc0e980a01041f333bce120")


def _clear_proxy():
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
              "http_proxy", "https_proxy", "all_proxy", "no_proxy"):
        os.environ.pop(k, None)


def load_audio(path, sr=16000):
    import numpy as np
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(sr), "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("decode fail: " + path)
    return np.frombuffer(r.stdout, dtype="<f4").astype("float32"), sr


def loudness(path):
    r = subprocess.run([FF, "-i", path, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        return {}
    d = json.loads(m[-1])
    return {"LUFS": float(d["input_i"]), "TP": float(d["input_tp"]), "LRA": float(d["input_lra"])}


def f0_stats(x, sr=16000):
    import librosa, numpy as np
    f, v, _ = librosa.pyin(x, fmin=70, fmax=350, sr=sr)
    v = v & (f > 0)
    if not v.any():
        return {}
    fv = f[v]
    return {"median": round(float(np.median(fv)), 1),
            "p10": round(float(np.percentile(fv, 10)), 1),
            "p90": round(float(np.percentile(fv, 90)), 1),
            "voiced_pct": round(float(v.mean() * 100), 1)}


def asr(x, sr=16000):
    import numpy as np, scipy.signal as ss
    from faster_whisper import WhisperModel
    _clear_proxy()
    model = WhisperModel(WHISPER, device="cpu", compute_type="int8", local_files_only=True)
    if sr != 16000:
        x = ss.resample_poly(x, 16000, sr).astype(np.float32)
    segs, _ = model.transcribe(x, language="vi", beam_size=5, temperature=0.0,
                               condition_on_previous_text=False, vad_filter=True)
    out = [{"t0": round(s.start, 2), "t1": round(s.end, 2), "text": s.text.strip()} for s in segs]
    return out


def run(path, ref=None):
    x, sr = load_audio(path)
    speech_s = len(x) / sr
    segs = asr(x, sr)
    words = sum(len(s["text"].split()) for s in segs)
    span = sum(s["t1"] - s["t0"] for s in segs)
    rep = {
        "file": path,
        "dur_s": round(speech_s, 2),
        "loudness": loudness(path),
        "f0": f0_stats(x, sr),
        "asr_words": words,
        "asr_speech_s": round(span, 2),
        "wpm": round(words / span * 60, 0) if span else None,
        "transcript": segs,
    }
    if ref and os.path.exists(ref):
        rx, rsr = load_audio(ref)
        rep["ref_f0"] = f0_stats(rx, rsr)
    return rep


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    path = args[0]
    ref = args[args.index("--ref") + 1] if "--ref" in args else None
    rep = run(path, ref)
    if "--json" in args:
        p = args[args.index("--json") + 1]
        json.dump(rep, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    brief = {k: rep[k] for k in ("dur_s", "loudness", "f0", "asr_words", "asr_speech_s", "wpm")}
    if "ref_f0" in rep:
        brief["ref_f0"] = rep["ref_f0"]
    print(json.dumps(brief, ensure_ascii=False, indent=1))
    for s in rep["transcript"]:
        print(f"[{s['t0']:6.2f}-{s['t1']:6.2f}] {s['text']}")


if __name__ == "__main__":
    main()
