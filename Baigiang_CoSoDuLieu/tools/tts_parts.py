"""Tổng hợp giọng đọc theo PHẦN (8 request), rồi cắt thành từng cảnh.

Edge TTS giới hạn tần suất theo request, nên gộp toàn bộ lời thoại của một phần
vào một lần gọi, dùng WordBoundary để căn từng cue, sau đó cắt WAV theo cảnh.
"""
import asyncio, json, os, re, subprocess, sys, unicodedata, wave, random
import numpy as np
import edge_tts

VOICE = os.environ.get('TTS_VOICE', 'vi-VN-NamMinhNeural')
TEMPO = 0.96
OUT = 'build/voice/scenes'
PARTS = 'build/voice/parts'
os.makedirs(OUT, exist_ok=True)
os.makedirs(PARTS, exist_ok=True)
FF = subprocess.run(['node', '-e', "console.log(require('ffmpeg-static'))"],
                    capture_output=True, text=True).stdout.strip()


def norm(w):
    w = unicodedata.normalize('NFC', w).lower()
    return re.sub(r'[^\wàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+', '', w)


def decode(src, dst):
    subprocess.run([FF, '-y', '-v', 'error', '-i', src,
                    '-filter:a', f'atempo={TEMPO},loudnorm=I=-19:TP=-2:LRA=7',
                    '-ar', '48000', '-ac', '2', dst], check=True)
    with wave.open(dst, 'rb') as w:
        return w.getnframes() / w.getframerate()


async def synth(text, mp3):
    comm = edge_tts.Communicate(text, VOICE, boundary='WordBoundary')
    words, data = [], 0
    with open(mp3, 'wb') as f:
        async for ch in comm.stream():
            if ch['type'] == 'audio':
                f.write(ch['data'])
                data += len(ch['data'])
            elif ch['type'] == 'WordBoundary':
                words.append({'w': ch['text'], 't': ch['offset'] / 1e7 / TEMPO,
                              'd': ch['duration'] / 1e7 / TEMPO})
    if data < 4000:
        raise RuntimeError('empty audio')
    return words


def find_cue(words, pos, toks, limit=260):
    n = len(words)
    first = toks[0]
    for j in range(pos, min(n, pos + limit)):
        if norm(words[j]['w']) != first:
            continue
        k, jj, good = 1, j + 1, 0
        while k < min(3, len(toks)) and jj < n and jj - j <= 7:
            if norm(words[jj]['w']) == toks[k]:
                good += 1
                k += 1
            jj += 1
        if good >= min(2, len(toks) - 1):
            return j
    for j in range(pos, min(n, pos + limit)):
        if norm(words[j]['w']) == first:
            return j
    return -1


def cue_spans(cues, words):
    starts = []
    pos = 0
    for c in cues:
        toks = [norm(t) for t in c['say'].split() if norm(t)]
        j = find_cue(words, pos, toks) if toks else -1
        if j < 0:
            j = min(pos, max(0, len(words) - 1))
        starts.append(j)
        pos = j + 1
    spans = []
    for i, (c, a) in enumerate(zip(cues, starts)):
        st = words[a]['t'] if a < len(words) else 0
        if i + 1 < len(cues):
            b = starts[i + 1]
            en = (words[b - 1]['t'] + words[b - 1]['d']) if b > 0 else st + 1
        else:
            en = (words[-1]['t'] + words[-1]['d']) if words else st + 1
        if en <= st:
            en = st + 0.4
        spans.append({'id': c['id'], 'start': round(st, 3), 'end': round(en + 0.02, 3)})
    return spans


def read_wav(path):
    with wave.open(path, 'rb') as w:
        params = w.getparams()
        arr = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2')
    return params, arr.reshape(-1, params.nchannels)


def write_wav(path, params, arr):
    with wave.open(path, 'wb') as w:
        w.setparams(params)
        w.writeframes(arr.astype('<i2').tobytes())


async def synth_retry(text, mp3, label):
    for attempt in range(6):
        try:
            return await asyncio.wait_for(synth(text, mp3), timeout=420)
        except Exception as e:
            print(f"retry {label} ({attempt + 1}): {type(e).__name__}", flush=True)
            await asyncio.sleep(150 + attempt * 60 + random.random() * 20)
    return None


async def do_part(key, scenes):
    mp3 = os.path.join(PARTS, f'p{key}.mp3')
    wavp = os.path.join(PARTS, f'p{key}.wav')
    text = ' '.join(c['say'] for sc in scenes for c in sc['cues'])
    print(f"part {key}: {len(scenes)} scenes, {len(text)} chars", flush=True)
    words = await synth_retry(text, mp3, f'p{key}')
    if not words:
        return False
    decode(mp3, wavp)
    params, audio = read_wav(wavp)
    total = audio.shape[0] / params.framerate
    all_cues = [c for sc in scenes for c in sc['cues']]
    spans = cue_spans(all_cues, words)

    pos = 0
    prev_end = 0.0
    for sc in scenes:
        k = len(sc['cues'])
        myspans = spans[pos:pos + k]
        pos += k
        st = max(prev_end + 0.08, myspans[0]['start'] - 0.28) if prev_end else max(0, myspans[0]['start'] - 0.28)
        en = min(total, myspans[-1]['end'] + 0.5)
        a = int(st * params.framerate) * params.nchannels
        b = int(en * params.framerate) * params.nchannels
        seg = audio[a:b].copy()
        path = os.path.join(OUT, sc['id'] + '.wav')
        write_wav(path, params, seg)
        dur = seg.shape[0] / params.nchannels / params.framerate
        rel = [{'id': s['id'], 'start': round(max(0, s['start'] - st), 3),
                'end': round(min(dur, s['end'] - st), 3)} for s in myspans]
        with open(os.path.join(OUT, sc['id'] + '.json'), 'w', encoding='utf-8') as f:
            json.dump({'id': sc['id'], 'dur': round(dur, 3), 'cues': rel, 'part': key}, f, ensure_ascii=False, indent=1)
        print(f"  OK {sc['id']} {dur:.2f}s", flush=True)
        prev_end = en
    return True


async def main():
    data = json.load(open('build/script.json', encoding='utf-8'))
    groups = {}
    for sc in data['scenes']:
        groups.setdefault(sc.get('part') or 0, []).append(sc)
    only = sys.argv[1:]
    print('cooldown 180s before first request...', flush=True)
    await asyncio.sleep(180)
    for key in sorted(groups):
        if only and str(key) not in only:
            continue
        ok = await do_part(key, groups[key])
        if not ok:
            print(f'PART {key} FAILED', flush=True)
            return
        await asyncio.sleep(110 + random.random() * 30)
    print('done parts', len(groups), flush=True)


asyncio.run(main())
