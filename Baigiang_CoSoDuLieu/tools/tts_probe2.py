import asyncio, edge_tts
async def main():
    try:
        c = edge_tts.Communicate('Xin chào các bạn, đây là bài giảng cơ sở dữ liệu.', 'vi-VN-NamMinhNeural')
        await c.save('build/voice/test4.mp3')
        print('save OK')
    except Exception as e:
        print('save FAIL', e)
asyncio.run(main())
