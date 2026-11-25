import asyncio, edge_tts
async def one(i, rate, pitch):
    try:
        c = edge_tts.Communicate(f'Đây là câu kiểm tra số {i}.', 'vi-VN-NamMinhNeural', rate=rate, pitch=pitch, boundary='WordBoundary')
        n=0
        async for ch in c.stream():
            if ch['type']=='audio': n+=len(ch['data'])
        print(i, 'OK', n, flush=True)
    except Exception as e:
        print(i, 'FAIL', type(e).__name__, flush=True)
async def main():
    for i in range(1,5):
        await one(i, '-4%', '-2Hz')
        await asyncio.sleep(1.0)
asyncio.run(main())
