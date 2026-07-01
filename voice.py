import asyncio
import os
import tempfile
from typing import Optional

import edge_tts

def text_to_speech_file(text: str) -> Optional[str]:
    text = (text or "").strip()
    if not text:
        return None

    async def _run():
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        communicate = edge_tts.Communicate(text=text, voice="en-US-AriaNeural")
        await communicate.save(path)
        return path

    try:
        return asyncio.run(_run())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(_run())
        finally:
            loop.close()
    except Exception:
        return None
