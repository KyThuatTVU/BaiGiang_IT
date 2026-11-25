import asyncio, hashlib, os, sys
import edge_tts
import edge_tts.communicate as comm
from edge_tts import Communicate

OUT = os.path.dirname(os.path.abspath(__file__)) + "/../mau/demo30/voice_lab"
os.makedirs(OUT, exist_ok=True)

comm.escape = lambda s: s  # allow raw SSML tags through

VI = "vi-VN-NamMinhNeural"
CASES = {
    "p1_plain": "Đây là MySQL. Đây là Node.js và API.",
    "p2_lang": "Đây là <lang xml:lang='en-US'>MySQL</lang>. Đây là <lang xml:lang='en-US'>Node.js</lang> và <lang xml:lang='en-US'>API</lang>.",
    "p3_voice": "Đây là <voice name='en-US-EmmaMultilingualNeural'>MySQL</voice>. Đây là <voice name='en-US-EmmaMultilingualNeural'>Node.js</voice> và <voice name='en-US-EmmaMultilingualNeural'>API</voice>.",
    "p4_emma_vi": "Đây là MySQL. Đây là Node.js và API.",
}

async def synth(tag, text, voice):
    path = f"{OUT}/{tag}.mp3"
    c = Communicate(text, voice, rate="+12%")
    with open(path, "wb") as f:
        async for chunk in c.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
    size = os.path.getsize(path)
    h = hashlib.md5(open(path, "rb").read()).hexdigest()[:10]
    print(tag, size, h)

async def main():
    for tag, text in CASES.items():
        voice = "en-US-EmmaMultilingualNeural" if tag == "p4_emma_vi" else VI
        try:
            await synth(tag, text, voice)
        except Exception as e:
            print(tag, "FAIL", repr(e))

asyncio.run(main())
