# -*- coding: utf-8 -*-
"""Dựng audio video mẫu: voice NamMinh + SFX, chuẩn hóa −14 LUFS, rồi ghép video."""
import json, os, re, subprocess, sys, wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sample_render as SR

MAU = SR.MAU
AUD = SR.AUD
SFXD = SR.SFXD
FF = SR.FF
SR_RATE = 48000

def decode(path):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-f", "f32le", "-ac", "1",
                        "-ar", str(SR_RATE), "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)

def write_wav(path, x, sr=SR_RATE):
    x = np.clip(x, -1.0, 1.0)
    pcm = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())

def read_wav(path):
    with wave.open(path, "rb") as w:
        assert w.getsampwidth() == 2
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return x.astype(np.float64) / 32768.0

def build_voice():
    n = int((SR.TOTAL + 0.5) * SR_RATE)
    voice = np.zeros(n)
    for sid in SR.SAMPLE:
        s = SR.SC[sid]
        for c, st in zip(s["cues"], s["starts"]):
            x = decode(f"{AUD}/{c['id']}.mp3")
            i = int(round((SR.GSTART[sid] + st) * SR_RATE))
            voice[i:i + len(x)] += x
    write_wav(MAU + "/voice_raw.wav", voice)
    subprocess.run([FF, "-y", "-v", "error", "-i", MAU + "/voice_raw.wav",
                    "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-ar", str(SR_RATE), "-ac", "1",
                    MAU + "/voice_norm.wav"], check=True)
    print("VOICE_NORM done", flush=True)
    return read_wav(MAU + "/voice_norm.wav")

def sfx_events():
    s2 = SR.SC["S02"]
    s6 = SR.SC["S06"]
    tA = SR.phrase_t("S02", 0, "Bạn A vừa cập nhật")
    tB = SR.phrase_t("S02", 0, "nhưng bạn B vẫn thấy")
    tC = SR.phrase_t("S02", 0, "còn bạn C phải tải lại")
    t_sync = s6["starts"][1] - 0.15
    return [
        ("S01", "chime", 0.25),
        ("S01", "pen", 1.02),
        ("S02", "whoosh", 0.45),
        ("S02", "pop", tA),
        ("S02", "buzz", tB),
        ("S02", "click", tC),
        ("S06", "pop", 0.20),
        ("S06", "click", 2.60),
        ("S06", "whoosh", 4.10),
        ("S06", "chime", t_sync),
    ]

def mix():
    voice = build_voice()
    n = len(voice)
    sfx = np.zeros(n)
    for sid, name, local in sfx_events():
        x = read_wav(f"{SFXD}/{name}.wav")
        i = int(round((SR.GSTART[sid] + local) * SR_RATE))
        j = min(n, i + len(x))
        sfx[i:j] += x[:j - i]
    out = voice + sfx
    peak = np.max(np.abs(out))
    lim = 10 ** (-1.5 / 20)
    if peak > lim:
        out *= lim / peak
    write_wav(MAU + "/mix.wav", out)
    print(f"MIX done peak={peak:.3f} scaled={peak > lim}", flush=True)
    two_pass()

def measure(path=MAU + "/mix_norm.wav"):
    r = subprocess.run([FF, "-hide_banner", "-i", path,
                        "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]+\}", r.stderr, re.S)
    rep = json.loads(m.group(0)) if m else {}
    json.dump(rep, open(MAU + "/audio_report.json", "w", encoding="utf-8"), indent=1)
    print("LUFS", rep.get("input_i"), "TP", rep.get("input_tp"), flush=True)
    return rep

def two_pass():
    rep = measure(MAU + "/mix.wav")
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11"
          f":measured_I={rep['input_i']}:measured_LRA={rep['input_lra']}"
          f":measured_TP={rep['input_tp']}:measured_thresh={rep['input_thresh']}"
          f":offset={rep['target_offset']}:linear=true")
    subprocess.run([FF, "-y", "-v", "error", "-i", MAU + "/mix.wav", "-af", af,
                    "-ar", str(SR_RATE), "-ac", "1", MAU + "/mix_norm.wav"], check=True)
    print("TWO_PASS done", flush=True)

def assemble():
    durs = [SR.SC[s]["dur"] for s in SR.SAMPLE]
    off1 = durs[0] - SR.XF
    off2 = off1 + durs[1] - SR.XF
    cmd = [FF, "-y", "-v", "error",
           "-i", SVID0("S01"), "-i", SVID0("S02"), "-i", SVID0("S06"),
           "-filter_complex",
           f"[0:v][1:v]xfade=transition=fade:duration={SR.XF}:offset={off1:.3f}[a];"
           f"[a][2:v]xfade=transition=fade:duration={SR.XF}:offset={off2:.3f}[v]",
           "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-an", MAU + "/_silent.mp4"]
    subprocess.run(cmd, check=True)
    subprocess.run([FF, "-y", "-v", "error", "-i", MAU + "/_silent.mp4", "-i", MAU + "/mix_norm.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", MAU + "/sample_congB.mp4"],
                   check=True)
    print("ASSEMBLE done", flush=True)

def SVID0(sid):
    return f"{SR.SVID}/{sid}.mp4"

if __name__ == "__main__":
    args = sys.argv[1:]
    mix()
    measure()
    if "--no-assemble" not in args:
        assemble()
