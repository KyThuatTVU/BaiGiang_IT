"""Tổng hợp giọng đọc theo từng cue, ghép thành file cảnh.

- Edge TTS: vi-VN-NamMinhNeural, rate +10% (1.10x), loudnorm.
- Câu hỏi quiz có `hold`: chèn im lặng 3 giây để đếm ngược.
- Span lấy trực tiếp từ độ dài file WAV, không lệch cue.
- Lưu build/voice/cues/<id>.wav và build/voice/scenes/<id>.wav|.json để chạy tiếp.
"""
import asyncio, json, os, random, subprocess, sys, wave
import numpy as np
import edge_tts

VOICE = os.environ.get('TTS_VOICE', 'vi-VN-NamMinhNeural')
RATE = os.environ.get('TTS_RATE', '+10%')
GAP = 0.30
PAD_HEAD = 0.12
PAD_TAIL = 0.38
OUT = 'build/voice/scenes'
CUES = 'build/voice/cues'
os.makedirs(OUT, exist_ok=True)
os.makedirs(CUES, exist_ok=True)
FF = subprocess.run(['node', '-e', "console.log(require('ffmpeg-static'))"],
                    capture_output=True, text=True).stdout.strip()

SILENCE = 0.008


def read_wav(path):
    with wave.open(path, 'rb') as w:
        params = w.getparams()
        arr = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2')
    return params, arr.reshape(-1, params.nchannels)


def write_wav(path, params, arr):
    with wave.open(path, 'wb') as w:
        w.setparams(params)
        w.writeframes(arr.astype('<i2').tobytes())


def trim(arr, sr):
    mono = np.abs(arr.astype(np.int32)).max(axis=1) / 32768.0
    idx = np.where(mono > SILENCE)[0]
    if len(idx) == 0:
        return arr
    a = max(0, idx[0] - int(sr * 0.05))
    b = min(arr.shape[0], idx[-1] + int(sr * 0.09))
    return arr[a:b]


def decode(mp3, wav):
    subprocess.run([FF, '-y', '-v', 'error', '-i', mp3,
                    '-filter:a', 'loudnorm=I=-19:TP=-2:LRA=7',
                    '-ar', '48000', '-ac', '2', wav], check=True)
    params, arr = read_wav(wav)
    arr = trim(arr, params.framerate)
    write_wav(wav, params, arr)
    return params, arr


async def synth(text, mp3):
    data = 0
    with open(mp3, 'wb') as f:
        async for ch in edge_tts.Communicate(text, VOICE, rate=RATE).stream():
            if ch['type'] == 'audio':
                f.write(ch['data'])
                data += len(ch['data'])
    if data < 3000:
        raise RuntimeError('empty audio')


async def synth_retry(text, mp3, label, max_attempts=24):
    for attempt in range(max_attempts):
        try:
            await asyncio.wait_for(synth(text, mp3), timeout=120)
            return True
        except Exception as e:
            print(f"  retry {label} ({attempt + 1}): {type(e).__name__}", flush=True)
            if attempt == max_attempts - 1:
                return False
            await asyncio.sleep(2.0 + attempt * 1.0 + random.random())
    return False


async def ensure_cue(cue):
    mp3 = os.path.join(CUES, cue['id'] + '.mp3')
    wav = os.path.join(CUES, cue['id'] + '.wav')
    if os.path.exists(wav) and os.path.getsize(wav) > 44100:
        try:
            params, arr = read_wav(wav)
            if arr.shape[0] / params.framerate > 0.4:
                return params, arr
        except Exception:
            pass
    ok = await synth_retry(cue['say'], mp3, cue['id'])
    if not ok:
        return None, None
    params, arr = decode(mp3, wav)
    await asyncio.sleep(1.0 + random.random() * 0.8)
    return params, arr


async def main():
    data = json.load(open('build/script.json', encoding='utf-8'))
    args = sys.argv[1:]
    only = set(args)
    scenes = [s for s in data['scenes'] if not only or s['id'] in only]
    total = sum(len(s['cues']) for s in scenes)
    done = 0
    for sc in scenes:
        out_json = os.path.join(OUT, sc['id'] + '.json')
        if os.path.exists(out_json):
            print(f"skip {sc['id']}", flush=True)
            done += len(sc['cues'])
            continue
        params = None
        pieces, spans = [], []
        t = PAD_HEAD
        for cue in sc['cues']:
            params, arr = await ensure_cue(cue)
            done += 1
            if arr is None:
                print(f"FAILED cue {cue['id']} ({done}/{total}) — rerun to resume", flush=True)
                return 1
            dur = arr.shape[0] / params.framerate
            spans.append({'id': cue['id'], 'start': round(t, 3), 'end': round(t + dur, 3)})
            pieces.append(arr)
            gap = GAP + float(cue.get('hold', 0))
            pieces.append(np.zeros((int(gap * params.framerate), params.nchannels), dtype='<i2'))
            t += dur + gap
            print(f"  cue {cue['id']} {dur:.2f}s ({done}/{total})", flush=True)
        pieces.pop()
        pieces.append(np.zeros((int(PAD_TAIL * params.framerate), params.nchannels), dtype='<i2'))
        audio = np.concatenate(pieces)
        dur = audio.shape[0] / params.framerate
        write_wav(os.path.join(OUT, sc['id'] + '.wav'), params, audio)
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump({'id': sc['id'], 'dur': round(dur, 3), 'cues': spans,
                       'part': sc.get('part')}, f, ensure_ascii=False, indent=1)
        print(f"SCENE {sc['id']} {dur:.2f}s", flush=True)
        await asyncio.sleep(0.5)
    print(f'done {len(scenes)} scenes / {total} cues', flush=True)
    return 0


sys.exit(asyncio.run(main()))
