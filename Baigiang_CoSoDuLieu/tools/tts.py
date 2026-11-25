import json, os, subprocess, sys, wave, time
import edge_tts

VOICE = os.environ.get('TTS_VOICE', 'vi-VN-NamMinhNeural')
TEMPO = 0.96          # đọc chậm hơn một chút, giữ nguyên cao độ
OUT = 'build/voice'
WAV = os.path.join(OUT, 'wav')
os.makedirs(WAV, exist_ok=True)

FF = subprocess.run(['node', '-e', "console.log(require('ffmpeg-static'))"],
                    capture_output=True, text=True).stdout.strip()


def decode(mp3, wav):
    subprocess.run([FF, '-y', '-v', 'error', '-i', mp3,
                    '-filter:a', f'atempo={TEMPO},loudnorm=I=-19:TP=-2:LRA=7',
                    '-ar', '48000', '-ac', '2', wav], check=True)
    with wave.open(wav, 'rb') as w:
        return w.getnframes() / w.getframerate()


def one(cue):
    cid = cue['id']
    mp3 = os.path.join(OUT, cid + '.mp3')
    wav = os.path.join(WAV, cid + '.wav')
    meta = os.path.join(OUT, cid + '.json')
    if os.path.exists(meta) and os.path.exists(wav):
        return
    last = None
    for attempt in range(6):
        try:
            r = subprocess.run([sys.executable, '-m', 'edge_tts', '--voice', VOICE,
                                '--text', cue['say'], '--write-media', mp3],
                               capture_output=True, text=True, timeout=90)
            if r.returncode != 0 or not os.path.exists(mp3) or os.path.getsize(mp3) < 2000:
                raise RuntimeError((r.stderr or '').strip().splitlines()[-1:] or 'no audio')
            dur = decode(mp3, wav)
            with open(meta, 'w', encoding='utf-8') as f:
                json.dump({'id': cid, 'say': cue['say'], 'dur': round(dur, 3), 'words': []},
                          f, ensure_ascii=False, indent=1)
            print(f"OK {cid} {dur:.2f}s", flush=True)
            return
        except Exception as e:
            last = e
            print(f"retry {cid} ({attempt + 1}): {e}", file=sys.stderr, flush=True)
            time.sleep(4 + attempt * 4)
    raise RuntimeError(f'TTS failed: {cid}: {last}')


def main():
    data = json.load(open('build/script.json', encoding='utf-8'))
    cues = [c for s in data['scenes'] for c in s['cues']]
    sel = sys.argv[1:]
    if sel:
        cues = [c for c in cues if c['id'] in sel]
    for c in cues:
        one(c)
        time.sleep(0.3)
    print('done', len(cues))


if __name__ == '__main__':
    main()
