"""
chatbot.py — Core Chatbot Engine

WHY THIS FILE EXISTS:
  This is the "brain" of the assistant. It handles:
    - Communicating with the Ollama API
    - Maintaining conversation memory
    - Formatting messages

  DESIGN DECISION — Separation of Concerns:
    chatbot.py knows NOTHING about the terminal UI. It only deals with
    messages and the LLM. This means in Version 2, you can plug this same
    class into a Streamlit web app or a voice interface without rewriting it.

  This pattern is called the "Core/Shell" architecture:
    Core  = chatbot.py  (pure logic, no I/O)
    Shell = main.py     (handles all user interaction)
"""

import json
import time
import urllib.error
import urllib.request
from typing import Generator, Optional

from config import config
from utils import logger, save_chat_history, generate_session_id


class Message:
    """
    A single chat message.

    WHY A CLASS: Gives us dot-access (msg.role, msg.content) and
    makes it easy to add metadata later (timestamps, token counts, etc.)
    """

    ROLE_USER      = "user"
    ROLE_ASSISTANT = "assistant"
    ROLE_SYSTEM    = "system"

    def __init__(self, role: str, content: str):
        self.role    = role
        self.content = content
        self.timestamp = time.time()

    def to_dict(self) -> dict:
        """Convert to the format Ollama's API expects."""
        return {"role": self.role, "content": self.content}

    def __repr__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"Message(role={self.role!r}, content={preview!r})"


class ChatBot:
    """
    The main chatbot class.

    Responsibilities:
      1. Hold the system prompt (personality / instructions)
      2. Store the conversation history (session memory)
      3. Send messages to Ollama and get responses
      4. Save/load history

    SCALABILITY NOTE:
      To add PDF chat later, you just add a method `load_pdf_context(path)`
      that appends the PDF text to the system prompt. The rest stays the same.
    """

    SYSTEM_PROMPT = """You are a helpful, knowledgeable AI assistant running locally on the user's machine.

Your personality:
- Clear and concise — no unnecessary fluff
- Friendly but professional
- Honest about uncertainty — say "I don't know" when appropriate
- Proactive — suggest follow-up questions or improvements when useful

Technical context:
- You are powered by Ollama running locally (no internet required)
- The user is an engineering student learning AI development
- Encourage good coding practices and learning when relevant

Keep responses focused. Use markdown formatting (headers, code blocks, lists)
when it improves clarity."""

    def __init__(self):
        self.session_id: str = generate_session_id()
        self.messages: list[Message] = []          # Full history this session
        self._context_window: list[Message] = []   # Trimmed window sent to API
        self.is_connected: bool = False

        logger.info(f"ChatBot initialized | session={self.session_id} | model={config.MODEL_NAME}")

    # ── Connection check ──────────────────────────────────────────────────────

    def check_connection(self) -> bool:
        """
        Verify Ollama is running and the model is available.

        WHY: Give users a clear error message instead of a confusing crash
        when they forget to start Ollama.
        """
        try:
            req = urllib.request.Request(
                f"{config.OLLAMA_BASE_URL}/api/tags",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())

            # Check if our model is available
            available_models = [m["name"] for m in data.get("models", [])]
            model_available = any(
                config.MODEL_NAME in m for m in available_models
            )

            if not model_available:
                logger.warning(
                    f"Model '{config.MODEL_NAME}' not found. "
                    f"Available: {available_models}"
                )
                return False

            self.is_connected = True
            logger.info(f"Connected to Ollama | model={config.MODEL_NAME}")
            return True

        except (urllib.error.URLError, OSError) as e:
            logger.error(f"Cannot reach Ollama: {e}")
            self.is_connected = False
            return False

    # ── Message management ────────────────────────────────────────────────────

    def _build_context(self) -> list[dict]:
        """
        Build the message list to send to the API.

        WHY TRIMMING: LLMs have a context window limit (max tokens they can
        handle). Keeping all messages would eventually hit this limit and
        cause errors. We keep the most recent N messages.

        The system prompt is always included at the start.
        """
        # Always start with the system prompt
        context = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        # Trim to the last N messages to stay within context limits
        recent = self.messages[-config.MAX_CONTEXT_MESSAGES:]
        context.extend(msg.to_dict() for msg in recent)

        return context

    def add_message(self, role: str, content: str) -> Message:
        """Add a message to history and return it."""
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        logger.debug(f"Message added | role={role} | chars={len(content)}")
        return msg

    # ── Core API call ─────────────────────────────────────────────────────────

    def send_message(self, user_input: str) -> Generator[str, None, None]:
        """
        Send a user message to Ollama and stream the response.

        WHY STREAMING: Streaming shows tokens as they arrive, so users see
        the response being typed out — feels much more responsive than
        waiting for the full answer.

        This is a Python *generator* function (uses `yield`).
        The caller receives one token chunk at a time.

        Args:
            user_input: The raw text the user typed.

        Yields:
            str: Individual text chunks from the model.

        Raises:
            ConnectionError: If Ollama is not reachable.
            RuntimeError:    If the API returns an unexpected response.
        """
        # 1. Store the user's message
        self.add_message(Message.ROLE_USER, user_input)

        # 2. Build the context window (trimmed history)
        context = self._build_context()

        # 3. Build the API request payload
        payload = json.dumps({
            "model": config.MODEL_NAME,
            "messages": context,
            "stream": True,              # Enable streaming
            "options": {
                "temperature": config.TEMPERATURE,
            },
        }).encode("utf-8")

        # 4. Make the HTTP request
        req = urllib.request.Request(
            url=f"{config.OLLAMA_BASE_URL}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        full_response = ""  # Accumulate the full response

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                # Stream the response line by line
                for raw_line in response:
                    line = raw_line.decode("utf-8").strip()
                    if not line:
                        continue

                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Extract the text token
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        full_response += token
                        yield token  # ← Send to the caller immediately

                    # Check if this is the last chunk
                    if chunk.get("done", False):
                        break

        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {config.OLLAMA_BASE_URL}. "
                "Is Ollama running? Try: `ollama serve`"
            ) from e

        # 5. Store the complete assistant response
        if full_response:
            self.add_message(Message.ROLE_ASSISTANT, full_response)
            logger.info(f"Response received | chars={len(full_response)}")

    # ── History management ────────────────────────────────────────────────────

    def save_session(self) -> Optional[str]:
        """Save current session to disk. Returns the file path as a string."""
        if not self.messages:
            return None

        messages_dicts = [m.to_dict() for m in self.messages]
        path = save_chat_history(messages_dicts, self.session_id)
        return str(path)

    def clear_history(self):
        """Clear in-memory conversation history (does not delete saved files)."""
        self.messages.clear()
        self.session_id = generate_session_id()   # Fresh session
        logger.info("Conversation history cleared")

    # ── Stats ─────────────────────────────────────────────────────────────────

    @property
    def message_count(self) -> int:
        return len(self.messages)

    @property
    def turn_count(self) -> int:
        """Number of complete user↔assistant exchanges."""
        return sum(1 for m in self.messages if m.role == Message.ROLE_USER)