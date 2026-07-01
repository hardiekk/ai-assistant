import os
import speech_recognition as sr

def transcribe_audio(audio_path: str) -> str:
    if not audio_path or not os.path.exists(audio_path):
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return (text or "").strip()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"[Speech recognition service error: {e}]"
    except Exception as e:
        return f"[Audio processing error: {e}]"
