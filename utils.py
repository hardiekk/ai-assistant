"""
utils.py — Utility / Helper Functions

WHY THIS FILE EXISTS:
  Utility functions are small, reusable helpers that don't belong to any
  specific class. Keeping them here avoids repeating code across files and
  makes future features (web UI, voice) easy to reuse them.

  Think of this as your "toolbelt".
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import config


# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logger(name: str = "ai_assistant") -> logging.Logger:
    """
    Create and configure a logger.

    WHY: Logging is how professional apps track what happened without
    printing everything to the terminal. You can later review logs to
    debug problems or understand usage patterns.

    Outputs to:
      - Terminal (INFO level and above)
      - Log file  (DEBUG level and above — everything)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if called twice
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — verbose, for debugging
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Stream handler — only warnings+ in terminal so the UI stays clean
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = setup_logger()


# ── Chat history persistence ──────────────────────────────────────────────────

def save_chat_history(messages: list[dict], session_id: str) -> Path:
    """
    Save the current conversation to a JSON file.

    WHY JSON: It's human-readable, easy to parse, and you can later build
    a web UI that loads and displays past conversations.

    Args:
        messages:   List of {"role": ..., "content": ...} dicts.
        session_id: Unique ID for this session (used as filename).

    Returns:
        Path to the saved file.
    """
    filename = config.CHAT_HISTORY_DIR / f"{session_id}.json"

    payload = {
        "session_id": session_id,
        "saved_at": datetime.now().isoformat(),
        "model": config.MODEL_NAME,
        "message_count": len(messages),
        "messages": messages,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    logger.info(f"Chat saved → {filename}")
    return filename


def load_chat_history(session_id: str) -> Optional[list[dict]]:
    """
    Load a past conversation from disk.

    Returns None if the file doesn't exist.
    """
    filename = config.CHAT_HISTORY_DIR / f"{session_id}.json"

    if not filename.exists():
        logger.warning(f"History file not found: {filename}")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"Chat loaded ← {filename}")
    return data.get("messages", [])


def list_saved_sessions() -> list[str]:
    """Return a list of saved session IDs (filenames without extension)."""
    files = sorted(config.CHAT_HISTORY_DIR.glob("*.json"), reverse=True)
    return [f.stem for f in files]


# ── Session ID generation ─────────────────────────────────────────────────────

def generate_session_id() -> str:
    """
    Create a unique session ID based on the current timestamp.

    Example output: "session_20250531_143022"

    WHY: Each chat session gets its own file. Timestamps make them
    chronologically sortable.
    """
    return datetime.now().strftime("session_%Y%m%d_%H%M%S")


# ── Terminal formatting helpers ───────────────────────────────────────────────

class Colors:
    """
    ANSI escape codes for terminal colors.

    WHY: Colors make the UI scannable and professional-looking without
    any external libraries. They work in most modern terminals.
    """
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foreground colors
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"


def cprint(text: str, color: str = "", bold: bool = False, end: str = "\n"):
    """Shorthand for printing colored text."""
    prefix = (Colors.BOLD if bold else "") + color
    print(f"{prefix}{text}{Colors.RESET}", end=end)


def print_divider(char: str = "─", width: int = 60, color: str = Colors.GRAY):
    """Print a horizontal divider line."""
    cprint(char * width, color=color)


def format_timestamp(iso_string: str) -> str:
    """Convert an ISO timestamp to a human-friendly string."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except ValueError:
        return iso_string