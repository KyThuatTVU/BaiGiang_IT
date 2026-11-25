import asyncio, edge_tts
async def run(voice, text):
    try:
        c = edge_tts.Communicate(text, voice, boundary='WordBoundary')
        n=0
        async for ch in c.stream():
            if ch['type']=='audio': n+=len(ch['data'])
        print(voice, 'OK', n, flush=True)
        return True
    except Exception as e:
        print(voice, 'FAIL', type(e).__name__, flush=True)
        return False
async def main():
    for v in ['vi-VN-NamMinhNeural','en-US-EmmaMultilingualNeural','vi-VN-HoaiMyNeural']:
        for i in range(2):
            await run(v, 'Xin chào, đây là bài kiểm tra.')
            await asyncio.sleep(1)
asyncio.run(main())
