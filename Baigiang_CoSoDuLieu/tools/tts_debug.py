import asyncio, logging, edge_tts
logging.basicConfig(level=logging.DEBUG)
async def main():
    c = edge_tts.Communicate('Xin chào các bạn.', 'vi-VN-NamMinhNeural')
    try:
        n=0
        async for ch in c.stream():
            if ch['type']=='audio': n+=len(ch['data'])
        print('OK', n)
    except Exception as e:
        print('ERR', repr(e))
asyncio.run(main())
