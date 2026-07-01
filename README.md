# 🤖 AI Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.x-orange?style=for-the-badge&logo=gradio&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black?style=for-the-badge)
![Voice](https://img.shields.io/badge/Voice-STT_%2B_TTS-purple?style=for-the-badge&logo=microphone)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A fully local, voice-enabled AI assistant with a browser UI — powered by Ollama, Gradio, and Edge TTS.**

[Features](#-features) · [Demo](#-demo) · [Quick Start](#-quick-start) · [Tech Stack](#️-tech-stack) · [Roadmap](#-roadmap)

</div>

---

## 🎯 What Is This?

A **locally-running AI assistant** that you can talk to — by voice or by typing — right from your browser. No API keys. No subscriptions. No data leaving your machine.

Built with:
- 🧠 **Ollama** for private, on-device LLM inference
- 🎙️ **Speech-to-Text** so you can speak your questions
- 🔊 **Edge TTS** so the assistant talks back in a natural voice
- 🖥️ **Gradio** for a clean, shareable browser interface

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Local AI** | Runs 100% on your machine via Ollama — no API key needed |
| 🎙️ **Voice Input (STT)** | Speak your question — Google Speech Recognition transcribes it |
| 🔊 **Voice Output (TTS)** | Replies are spoken aloud using Microsoft Edge TTS (Aria Neural) |
| 💬 **Chat Memory** | Remembers the full conversation context within a session |
| 🌐 **Browser UI** | Gradio-powered web interface — works on any device on your network |
| ⚙️ **Swappable Models** | Switch between `llama3`, `mistral`, `gemma`, `phi3` and more |
| 🔒 **100% Private** | All data stays on your device — zero telemetry |
| 🔧 **Modular Code** | Clean separation: `app.py`, `bot.py`, `stt.py`, `voice.py`, `config.py` |

---

## 🖥️ Demo

> Launch the app and open the browser UI to chat by text or voice.

```
🌐 Running on http://127.0.0.1:7860
```

The interface supports:
- **Text input** — type your message and press Send
- **Audio input** — record or upload a `.wav`/`.mp3` file
- **Audio output** — the assistant's reply plays back automatically
- **Chat history** — full conversation visible in the UI

---

## 📂 Project Structure

```
ai-assistant/
├── app.py           ← Gradio UI + chat orchestration
├── bot.py           ← Core AI chat logic (Ollama integration)
├── stt.py           ← Speech-to-Text (Google Speech Recognition)
├── voice.py         ← Text-to-Speech (Edge TTS, Aria Neural)
├── config.py        ← Model name, settings
├── requirements.txt ← All dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai) installed and running
- `ffmpeg` installed (required by `pydub` for audio processing)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
```

### 1. Clone the repo

```bash
git clone https://github.com/hardiekk/ai-assistant.git
cd ai-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull an AI model via Ollama

```bash
ollama pull llama3
# or try: ollama pull mistral | ollama pull gemma | ollama pull phi3
```

### 5. Run the assistant

```bash
python app.py
```

Then open your browser at **http://127.0.0.1:7860** 🎉

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| **Python 3.9+** | Core language |
| **Gradio 4.x** | Browser-based UI framework |
| **Ollama** | Local LLM runtime (llama3, mistral, etc.) |
| **edge-tts** | Microsoft Edge Neural TTS for voice output |
| **SpeechRecognition** | Google Speech API for audio-to-text |
| **pydub** | Audio file processing |

---

## ⚙️ Configuration

Edit `config.py` to change the model or voice:

```python
MODEL_NAME = "llama3"      # Any model pulled via ollama
VOICE_NAME = "en-US-AriaNeural"  # Any Edge TTS voice
```

Available Edge TTS voices: run `edge-tts --list-voices` in your terminal.

---

## 🐛 Known Issues & Fixes

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: gradio` | Run `pip install -r requirements.txt` inside your `.venv` |
| `ImportError: HfFolder` | Pin `huggingface-hub<1.0`: `pip install huggingface-hub==0.34.3` |
| `TypeError: unsupported operand types` in `voice.py` | Ensure Python 3.9+ is active in your venv |
| No audio output | Make sure `ffmpeg` is installed and on your PATH |
| Ollama not responding | Run `ollama serve` in a separate terminal before launching the app |

---

## 🔮 Roadmap

- [x] Voice input (STT via Google Speech Recognition)
- [x] Voice output (TTS via Edge TTS)
- [x] Browser UI via Gradio
- [x] Conversational memory (session history)
- [ ] Persistent chat history (save to file)
- [ ] Groq API support for cloud-speed inference
- [ ] Multi-model switching live in the UI
- [ ] Hugging Face Spaces deployment
- [ ] Plugin system (web search, calculator, file reader)
- [ ] Dark mode + custom UI theme

---

## 🚢 Deployment

This app runs locally by design. For sharing:

**Gradio public link (temporary, 72h):**
```python
# In app.py, change:
demo.launch(share=True)
```

**Hugging Face Spaces (recommended for persistent hosting):**
1. Push this repo to a HF Space
2. Add a `README.md` with `sdk: gradio`
3. Set any required environment variables in the Space settings

---

## 👨‍💻 Author

**Kunal Kakde** — [@hardiekk](https://github.com/hardiekk)

> Building AI products that actually ship. 🚀

Feel free to open an issue, star the repo ⭐, or reach out!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
