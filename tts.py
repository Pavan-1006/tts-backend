import asyncio
import edge_tts

VOICE = "en-IN-PrabhatNeural"  # Indian male voice

async def _text_to_mp3_async(text, output_path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def text_to_mp3(text, output_path):
    asyncio.run(_text_to_mp3_async(text, output_path))
