# 🤖 AI Assistant

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

A powerful, locally-running AI Assistant built with Python — no cloud, no subscriptions, fully private. Runs on your machine using local AI models via Ollama.

---

## ✨ Features

- 🧠 **Local AI** — runs entirely on your machine using Ollama (no API key needed)
- 💬 **Conversational memory** — remembers context within a session
- ⚙️ **Configurable models** — swap between `llama3`, `mistral`, `gemma` and more
- 🔧 **Modular codebase** — clean separation with `main.py`, `chatbot.py`, `config.py`, `utils.py`
- 🚀 **Fast responses** — optimized for low-latency local inference
- 🔒 **100% Private** — your conversations never leave your device

---

## 🗂️ Project Structure

```
ai-assistant/
├── main.py          ← Entry point, CLI interface
├── chatbot.py       ← Core chat logic & AI interaction
├── config.py        ← Model config, settings
├── utils.py         ← Helper functions
├── requirements.txt ← Dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai) installed locally

### 1. Clone the repo
```bash
git clone https://github.com/hardiekk/ai-assistant.git
cd ai-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Pull an AI model via Ollama
```bash
ollama pull llama3
```

### 4. Run the assistant
```bash
python main.py
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python 3.11 | Core language |
| Ollama | Local LLM runtime |
| LLaMA 3 / Mistral | AI model |
| Rich / Colorama | Terminal UI |

---

## 🔮 Roadmap

- [ ] Voice input/output support
- [ ] Web UI interface
- [ ] Multi-model switching on the fly
- [ ] Persistent conversation history
- [ ] Plugin/tool system (web search, calculator)

---

## 👨‍💻 Author

**Kunal Kakde** — [@hardiekk](https://github.com/hardiekk)

> Building AI products that actually ship. 🚀

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
