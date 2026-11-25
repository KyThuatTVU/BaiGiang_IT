import asyncio, edge_tts, traceback
async def run(tag, text, **kw):
    try:
        c = edge_tts.Communicate(text, 'vi-VN-NamMinhNeural', **kw)
        data=b''; words=0
        async for ch in c.stream():
            if ch['type']=='audio': data+=ch['data']
            elif ch['type']=='WordBoundary': words+=1
        print(tag, len(data), words)
    except Exception as e:
        print(tag, 'FAIL', repr(e))
        traceback.print_exc()
async def main():
    await run('a', 'Xin chào, đây là bài kiểm tra giọng đọc.')
    await run('b', 'Xin chào các bạn', boundary='WordBoundary')
asyncio.run(main())
