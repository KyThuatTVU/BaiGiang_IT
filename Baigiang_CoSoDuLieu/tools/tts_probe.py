import asyncio, edge_tts, os
async def run(tag, **kw):
    try:
        c = edge_tts.Communicate('Xin chào các bạn, đây là bài giảng cơ sở dữ liệu.', 'vi-VN-NamMinhNeural', **kw)
        data = b''
        words = 0
        async for ch in c.stream():
            if ch['type'] == 'audio': data += ch['data']
            elif ch['type'] == 'WordBoundary': words += 1
        print(tag, 'bytes', len(data), 'words', words)
    except Exception as e:
        print(tag, 'FAIL', type(e).__name__, e)
async def main():
    await run('default')
    await run('rate-4', rate='-4%')
    await run('pitch-2', pitch='-2Hz')
    await run('both', rate='-4%', pitch='-2Hz')
asyncio.run(main())
