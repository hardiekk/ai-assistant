"""
main.py — Application Entry Point & Terminal UI

WHY THIS FILE EXISTS:
  This is the "shell" of the Core/Shell architecture.
  It handles EVERYTHING the user sees and types:
    - Welcome screen
    - Input prompt
    - Rendering the AI's streamed response
    - Processing commands (/help, /clear, /exit, /history, /save)
    - Error messages

  DESIGN DECISION:
    main.py knows about the terminal. chatbot.py does NOT.
    This clean boundary means you can replace main.py with a
    Streamlit app (Version 2) or a voice interface (Version 3)
    while chatbot.py stays exactly the same.

USAGE:
    python main.py
"""

import sys
import shutil
import time

from chatbot import ChatBot
from config import config
from utils import (
    Colors, cprint, print_divider,
    list_saved_sessions, format_timestamp, logger,
)


# ── Welcome Screen ────────────────────────────────────────────────────────────

def print_welcome():
    """
    Print the welcome banner.

    WHY: First impressions matter. A clean welcome screen tells the user
    the app is working, shows the version, and lists available commands.
    """
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    width = min(terminal_width, 72)

    print()
    cprint("=" * width, color=Colors.CYAN)
    cprint(f"  🤖  {config.APP_NAME}  v{config.VERSION}", color=Colors.CYAN, bold=True)
    cprint(f"  Powered by Ollama · Model: {config.MODEL_NAME}", color=Colors.GRAY)
    cprint("=" * width, color=Colors.CYAN)
    print()
    cprint("  Commands:", color=Colors.YELLOW, bold=True)
    cprint(f"  {config.CMD_HELP:<12} Show this help message", color=Colors.GRAY)
    cprint(f"  {config.CMD_CLEAR:<12} Clear conversation history", color=Colors.GRAY)
    cprint(f"  {config.CMD_HISTORY:<12} List saved sessions", color=Colors.GRAY)
    cprint(f"  {config.CMD_SAVE:<12} Save current session now", color=Colors.GRAY)
    cprint(f"  {config.CMD_EXIT:<12} Exit the assistant", color=Colors.GRAY)
    print()
    cprint("  Type your message and press Enter to chat.", color=Colors.GREEN)
    print_divider(width=width)
    print()


def print_help():
    """Print the help screen (same as welcome but called mid-session)."""
    print()
    cprint("  📖  Help", color=Colors.YELLOW, bold=True)
    print_divider()
    cprint(f"  {config.CMD_HELP:<14} Show this message", color=Colors.GRAY)
    cprint(f"  {config.CMD_CLEAR:<14} Clear history & start fresh", color=Colors.GRAY)
    cprint(f"  {config.CMD_HISTORY:<14} Show saved chat sessions", color=Colors.GRAY)
    cprint(f"  {config.CMD_SAVE:<14} Save session to chat_history/", color=Colors.GRAY)
    cprint(f"  {config.CMD_EXIT:<14} Exit (auto-saves session)", color=Colors.GRAY)
    print()
    cprint("  Tips:", color=Colors.YELLOW, bold=True)
    cprint("  • Ask follow-up questions — the assistant remembers context", color=Colors.GRAY)
    cprint("  • Ask for code, explanations, summaries, or creative writing", color=Colors.GRAY)
    cprint("  • Change the model in config.py (e.g. mistral, codellama)", color=Colors.GRAY)
    print()


# ── Command Handlers ──────────────────────────────────────────────────────────

def handle_clear(bot: ChatBot):
    """Clear conversation memory and start a fresh session."""
    bot.clear_history()
    print()
    cprint("  ✓ Conversation cleared. Starting fresh session.", color=Colors.GREEN)
    cprint(f"  Session ID: {bot.session_id}", color=Colors.GRAY)
    print()


def handle_history():
    """Display a list of saved sessions."""
    sessions = list_saved_sessions()
    print()
    if not sessions:
        cprint("  No saved sessions found.", color=Colors.YELLOW)
    else:
        cprint(f"  💾  Saved Sessions ({len(sessions)})", color=Colors.CYAN, bold=True)
        print_divider()
        for i, session_id in enumerate(sessions[:10], 1):
            # Session IDs look like "session_20250531_143022"
            # We can parse the date from the ID
            parts = session_id.split("_")
            if len(parts) == 3:
                date_str = parts[1]
                time_str = parts[2]
                readable = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}  {time_str[:2]}:{time_str[2:4]}"
                cprint(f"  {i:2}. {readable}  ({session_id})", color=Colors.GRAY)
            else:
                cprint(f"  {i:2}. {session_id}", color=Colors.GRAY)
    print()


def handle_save(bot: ChatBot):
    """Manually save the current session."""
    print()
    path = bot.save_session()
    if path:
        cprint(f"  ✓ Session saved → {path}", color=Colors.GREEN)
    else:
        cprint("  Nothing to save — conversation is empty.", color=Colors.YELLOW)
    print()


def handle_exit(bot: ChatBot):
    """Save session and exit gracefully."""
    print()
    cprint("  Saving session...", color=Colors.GRAY)
    path = bot.save_session()
    if path:
        cprint(f"  ✓ Saved → {path}", color=Colors.GREEN)

    turns = bot.turn_count
    cprint(
        f"\n  Goodbye! 👋  You had {turns} exchange{'s' if turns != 1 else ''} this session.",
        color=Colors.CYAN,
        bold=True,
    )
    print()
    sys.exit(0)


# ── Connection Check ──────────────────────────────────────────────────────────

def check_ollama(bot: ChatBot) -> bool:
    """
    Verify Ollama is running before entering the chat loop.
    Prints a friendly error if it isn't.
    """
    cprint("  Connecting to Ollama...", color=Colors.GRAY, end="\r")

    if bot.check_connection():
        cprint(f"  ✓ Connected  →  {config.MODEL_NAME}                ", color=Colors.GREEN)
        print()
        return True

    # Connection failed — print helpful instructions
    print()
    cprint("  ✗ Cannot connect to Ollama", color=Colors.RED, bold=True)
    print_divider()
    cprint("  Make sure Ollama is installed and running:", color=Colors.YELLOW)
    print()
    cprint("  1. Install Ollama:  https://ollama.ai", color=Colors.GRAY)
    cprint(f"  2. Pull the model:  ollama pull {config.MODEL_NAME}", color=Colors.GRAY)
    cprint("  3. Start server:    ollama serve", color=Colors.GRAY)
    cprint("  4. Run this again:  python main.py", color=Colors.GRAY)
    print()
    return False


# ── Response Renderer ─────────────────────────────────────────────────────────

def render_streaming_response(bot: ChatBot, user_input: str):
    """
    Stream the assistant's response to the terminal token by token.

    WHY STREAMING MATTERS:
      Instead of waiting 5-10 seconds for a complete answer, the user sees
      text appearing immediately. This is how ChatGPT and Claude feel "fast".
      Under the hood, we're printing each token as it arrives from the API.
    """
    print()
    cprint("  Assistant", color=Colors.CYAN, bold=True)
    print_divider()
    print("  ", end="", flush=True)

    try:
        col = 2  # Track column position for soft word-wrap
        for token in bot.send_message(user_input):
            print(token, end="", flush=True)

            # Simple soft word-wrap at ~70 chars
            col += len(token)
            if "\n" in token:
                print("  ", end="", flush=True)
                col = 2

        print("\n")  # Clean newline after response

    except ConnectionError as e:
        print()
        cprint(f"\n  ✗ Connection Error: {e}", color=Colors.RED)
        print()
        logger.error(f"Connection error during chat: {e}")

    except KeyboardInterrupt:
        # User pressed Ctrl+C mid-response
        print()
        cprint("\n  [Response interrupted]", color=Colors.YELLOW)
        print()


# ── Main Chat Loop ────────────────────────────────────────────────────────────

def chat_loop(bot: ChatBot):
    """
    The main interactive loop.

    HOW IT WORKS:
      1. Show a prompt
      2. Read user input
      3. Check if it's a command (starts with /)
      4. If not, send to the AI and render the response
      5. Repeat forever until /exit or Ctrl+C
    """
    while True:
        try:
            # ── Input prompt ─────────────────────────────────────────────────
            print_divider()
            cprint("  You", color=Colors.GREEN, bold=True)
            user_input = input("  › ").strip()

            # Skip empty input
            if not user_input:
                continue

            logger.debug(f"User input: {user_input[:80]}")

            # ── Command routing ───────────────────────────────────────────────
            if user_input.lower() == config.CMD_EXIT:
                handle_exit(bot)                    # Saves and exits

            elif user_input.lower() == config.CMD_HELP:
                print_help()

            elif user_input.lower() == config.CMD_CLEAR:
                handle_clear(bot)

            elif user_input.lower() == config.CMD_HISTORY:
                handle_history()

            elif user_input.lower() == config.CMD_SAVE:
                handle_save(bot)

            elif user_input.startswith("/"):
                # Unknown command
                cprint(
                    f"\n  Unknown command '{user_input}'. Type {config.CMD_HELP} for help.\n",
                    color=Colors.YELLOW,
                )

            else:
                # ── Normal chat message ───────────────────────────────────────
                render_streaming_response(bot, user_input)

        except KeyboardInterrupt:
            # Ctrl+C — treat as /exit
            print()
            cprint("\n  Ctrl+C detected.", color=Colors.YELLOW)
            handle_exit(bot)

        except EOFError:
            # Piped input finished (e.g. echo "hello" | python main.py)
            handle_exit(bot)


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    """
    Application entry point.

    Sequence:
      1. Create the ChatBot instance
      2. Print the welcome screen
      3. Verify Ollama connection
      4. Start the chat loop
    """
    bot = ChatBot()

    print_welcome()

    if not check_ollama(bot):
        sys.exit(1)   # Exit with error code if Ollama not available

    chat_loop(bot)


if __name__ == "__main__":
    main()