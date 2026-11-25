"""Tổng hợp giọng đọc theo từng cảnh (ít request hơn), trích timing từng từ.

- Mỗi cảnh: nối các câu thuyết minh thành một đoạn, gọi Edge TTS một lần.
- WordBoundary cho biết thời điểm từng từ -> ánh xạ ngược về từng cue.
- Nếu dịch vụ chặn (NoAudioReceived), tự chia cảnh thành nhiều đoạn ngắn hơn
  rồi ghép lại, timing cộng dồn theo từng đoạn.
- Hạ tốc độ 4% bằng atempo, chuẩn hóa loudness.
"""
import asyncio, json, os, subprocess, sys, wave, re, unicodedata, math, random
import edge_tts

VOICE = os.environ.get('TTS_VOICE', 'vi-VN-NamMinhNeural')
TEMPO = 0.96
GAP = 0.16
OUT = 'build/voice/scenes'
os.makedirs(OUT, exist_ok=True)
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
    words = []
    data = 0
    with open(mp3, 'wb') as f:
        async for ch in comm.stream():
            if ch['type'] == 'audio':
                f.write(ch['data'])
                data += len(ch['data'])
            elif ch['type'] == 'WordBoundary':
                words.append({'w': ch['text'],
                              't': ch['offset'] / 1e7 / TEMPO,
                              'd': ch['duration'] / 1e7 / TEMPO})
    if data < 2000:
        raise RuntimeError('empty audio')
    return words


def cue_spans(cues, words):
    """Ánh xạ mỗi cue sang đoạn thời gian trong audio dựa trên từ đầu tiên khớp."""
    spans = []
    pos = 0
    n = len(words)
    for i, c in enumerate(cues):
        toks = [norm(t) for t in c['say'].split() if norm(t)]
        first = toks[0] if toks else ''
        found = -1
        limit = min(n, pos + max(12, len(toks) * 3 + 8))
        for j in range(pos, limit):
            if norm(words[j]['w']) == first:
                found = j
                break
        if found < 0:
            spans.append(None)
            continue
        end = n
        if i + 1 < len(cues):
            nxt = [norm(t) for t in cues[i + 1]['say'].split() if norm(t)]
            nf = nxt[0] if nxt else ''
            lim2 = min(n, found + len(toks) * 4 + 14)
            for j in range(found + max(1, len(toks) - 3), lim2):
                if norm(words[j]['w']) == nf:
                    end = j
                    break
        spans.append((found, end))
        pos = found + 1
    out = []
    last_end = 0.0
    for c, sp in zip(cues, spans):
        if sp is None:
            out.append({'id': c['id'], 'start': last_end, 'end': last_end})
            continue
        a, b = sp
        st = words[a]['t'] if a < n else last_end
        en = (words[b - 1]['t'] + words[b - 1]['d']) if 0 < b <= n else st + 1
        if en <= st:
            en = st + 0.5
        out.append({'id': c['id'], 'start': st, 'end': en})
        last_end = en
    return out


def merge_wavs(files, dst, gap=GAP):
    out = wave.open(dst, 'wb')
    params = None
    for i, path in enumerate(files):
        with wave.open(path, 'rb') as r:
            if params is None:
                params = r.getparams()
                out.setparams(params)
            out.writeframes(r.readframes(r.getnframes()))
            if gap and i < len(files) - 1:
                out.writeframes(b'\x00' * int(params.framerate * gap) * params.nchannels * params.sampwidth)
    out.close()


def split_groups(cues, n):
    size = math.ceil(len(cues) / n)
    return [cues[i:i + size] for i in range(0, len(cues), size)]


async def synth_retry(text, mp3, tries, label):
    last = None
    for attempt in range(tries):
        try:
            return await asyncio.wait_for(synth(text, mp3), timeout=150)
        except Exception as e:
            last = e
            print(f"retry {label} ({attempt + 1}): {type(e).__name__}", flush=True)
            await asyncio.sleep(7 + attempt * 6 + random.random() * 3)
    print(f"chunk {label} failed: {last}", flush=True)
    return None


async def do_scene(sc):
    sid = sc['id']
    wav = os.path.join(OUT, sid + '.wav')
    meta = os.path.join(OUT, sid + '.json')
    if os.path.exists(wav) and os.path.exists(meta) and os.path.getsize(wav) > 20000:
        return True
    for nchunks in (1, 2, 3):
        parts, spans_all, cum, ok = [], [], 0.0, True
        groups = split_groups(sc['cues'], nchunks)
        for gi, group in enumerate(groups):
            text = ' '.join(c['say'] for c in group)
            mp3 = os.path.join(OUT, f'{sid}.p{gi}.mp3')
            pwav = os.path.join(OUT, f'{sid}.p{gi}.wav')
            words = await synth_retry(text, mp3, 3 if nchunks > 1 else 4, f'{sid} [{gi + 1}/{len(groups)}]')
            if not words:
                ok = False
                break
            dur = decode(mp3, pwav)
            spans = cue_spans(group, words)
            for sp in spans:
                sp['start'] += cum
                sp['end'] += cum
            spans_all += spans
            parts.append(pwav)
            cum += dur + GAP
        if ok:
            merge_wavs(parts, wav)
            with wave.open(wav, 'rb') as w:
                dur = w.getnframes() / w.getframerate()
            with open(meta, 'w', encoding='utf-8') as f:
                json.dump({'id': sid, 'dur': round(dur, 3), 'cues': spans_all,
                           'chunks': nchunks}, f, ensure_ascii=False, indent=1)
            for p in os.listdir(OUT):
                if p.startswith(sid + '.p'):
                    os.remove(os.path.join(OUT, p))
            print(f"OK {sid} {dur:.2f}s chunks={nchunks} cue0={spans_all[0]['start']:.2f}", flush=True)
            return True
    return False


async def main():
    data = json.load(open('build/script.json', encoding='utf-8'))
    scenes = data['scenes']
    sel = sys.argv[1:]
    if sel:
        scenes = [s for s in scenes if s['id'] in sel]
    failed = []
    for i, sc in enumerate(scenes):
        ok = await do_scene(sc)
        if not ok:
            failed.append(sc['id'])
        await asyncio.sleep(2.0 + random.random() * 1.5)
    print('done', len(scenes), 'failed', failed, flush=True)


asyncio.run(main())
