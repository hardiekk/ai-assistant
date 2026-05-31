"""
config.py — Central Configuration

WHY THIS FILE EXISTS:
  In production systems, you never hardcode settings inside your logic.
  This file is the single source of truth for all configurable values.
  When you add a web UI or voice interface later, they all share this config.

DESIGN DECISION:
  Using a dataclass gives us type hints (great for learning what each value should be)
  and makes config readable like an object: config.MODEL_NAME instead of a dict.
"""

from dataclasses import dataclass, field
from pathlib import Path

# ── Project root: the folder where this file lives ──────────────────────────
BASE_DIR = Path(__file__).parent


@dataclass
class Config:
    # ── Ollama / LLM settings ────────────────────────────────────────────────
    OLLAMA_BASE_URL: str = "http://localhost:11434"   # Default Ollama server
    MODEL_NAME: str = "llama3.2"                      # Change to any model you have pulled
    TEMPERATURE: float = 0.7                          # 0 = deterministic, 1 = creative
    MAX_CONTEXT_MESSAGES: int = 20                    # Keeps memory from growing forever

    # ── Paths ────────────────────────────────────────────────────────────────
    CHAT_HISTORY_DIR: Path = BASE_DIR / "chat_history"
    LOGS_DIR: Path = BASE_DIR / "logs"
    LOG_FILE: Path = BASE_DIR / "logs" / "assistant.log"

    # ── UI / UX ──────────────────────────────────────────────────────────────
    APP_NAME: str = "AI Assistant"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Your Name"

    # ── Commands the user can type ───────────────────────────────────────────
    CMD_HELP: str = "/help"
    CMD_CLEAR: str = "/clear"
    CMD_EXIT: str = "/exit"
    CMD_HISTORY: str = "/history"
    CMD_SAVE: str = "/save"

    def __post_init__(self):
        """Create directories if they don't exist yet."""
        self.CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Singleton: import `config` anywhere in the project
config = Config()