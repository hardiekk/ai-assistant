print("RUNNING NEW AETHER UI BUILD")

import gradio as gr
from chatbot import ChatBot
from stt import transcribe_audio
from voice import text_to_speech_file
from utils import list_saved_sessions

bot = ChatBot()

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700;800&display=swap');

:root {
    --bg-1: #070b14;
    --bg-2: #0f172a;
    --panel: rgba(15, 23, 42, 0.78);
    --panel-2: rgba(30, 41, 59, 0.72);
    --border: rgba(148, 163, 184, 0.18);
    --text: #e5eefc;
    --muted: #94a3b8;
    --primary: #8b5cf6;
    --accent: #22c55e;
    --cyan: #22d3ee;
}

html, body, .gradio-container {
    background:
        radial-gradient(circle at 15% 20%, rgba(139, 92, 246, 0.18), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(34, 211, 238, 0.12), transparent 26%),
        linear-gradient(135deg, var(--bg-1), var(--bg-2)) !important;
    color: var(--text) !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 1220px !important;
    margin: 0 auto !important;
    padding: 20px 14px 28px !important;
    font-family: 'Sora', sans-serif !important;
}

#hero {
    background: linear-gradient(135deg, rgba(139,92,246,0.16), rgba(34,211,238,0.08));
    border: 1px solid rgba(139,92,246,0.24);
    border-radius: 28px;
    padding: 24px 24px 18px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.32);
    margin-bottom: 16px;
}

#hero h1 {
    margin: 0 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #c4b5fd, #67e8f9, #86efac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#hero-sub {
    color: var(--muted) !important;
    margin-top: 4px !important;
    font-size: 0.98rem !important;
}

#status-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(139,92,246,0.22);
    border-radius: 18px;
    padding: 10px 14px;
    text-align: center;
    color: #ddd6fe !important;
    font-weight: 600;
}

.shell {
    gap: 16px !important;
}

.sidebar-panel, .main-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 24px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.28);
}

.sidebar-panel {
    padding: 16px;
}

.main-panel {
    padding: 18px;
}

.panel-title {
    color: #f8fafc !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
}

.quick-grid {
    gap: 8px !important;
}

.quick-btn button {
    background: rgba(139,92,246,0.12) !important;
    border: 1px solid rgba(139,92,246,0.28) !important;
    color: #ddd6fe !important;
    border-radius: 999px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    transition: all 0.18s ease !important;
}
.quick-btn button:hover {
    transform: translateY(-1px);
    background: rgba(139,92,246,0.2) !important;
}

.control-btn button {
    border-radius: 16px !important;
    font-weight: 700 !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    background: rgba(255,255,255,0.04) !important;
    color: var(--text) !important;
}
.control-btn button:hover {
    background: rgba(255,255,255,0.08) !important;
}

#chat-wrap {
    border: 1px solid rgba(139,92,246,0.16);
    border-radius: 22px;
    overflow: hidden;
}

#chatbot {
    background: rgba(2, 6, 23, 0.36) !important;
    border-radius: 20px !important;
    min-height: 460px !important;
}

#chatbot .message {
    border-radius: 18px !important;
    padding: 12px 14px !important;
}
#chatbot .message.user {
    background: linear-gradient(135deg, #7c3aed, #14b8a6) !important;
    color: white !important;
}
#chatbot .message.bot {
    background: rgba(255,255,255,0.06) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

#input-card {
    margin-top: 14px;
    background: var(--panel-2);
    border: 1px solid rgba(148,163,184,0.14);
    border-radius: 20px;
    padding: 14px;
}

#message-box textarea,
#audio-box,
#status-box textarea,
#sessions-box textarea {
    background: rgba(255,255,255,0.05) !important;
    color: var(--text) !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    border-radius: 16px !important;
}

#message-box textarea:focus,
#status-box textarea:focus,
#sessions-box textarea:focus {
    border-color: rgba(139,92,246,0.55) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important;
}

#send-btn button {
    background: linear-gradient(90deg, #8b5cf6, #22c55e) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    font-weight: 800 !important;
    min-height: 50px !important;
    box-shadow: 0 10px 28px rgba(139,92,246,0.3);
}
#send-btn button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 30px rgba(139,92,246,0.42);
}

#status-box textarea {
    text-align: center !important;
    font-weight: 600 !important;
}

#audio-output {
    margin-top: 14px;
}

#footer-note {
    text-align: center;
    color: rgba(148,163,184,0.8) !important;
    font-size: 0.82rem !important;
    margin-top: 16px !important;
}

footer { display: none !important; }
"""

QUICK_PROMPTS = [
    "Explain this simply",
    "Summarize in 3 bullets",
    "Give step by step solution",
    "Write Python code",
]

def check_status():
    if bot.check_connection():
        return "🟢 Ollama connected and ready"
    return "🔴 Ollama not connected — run `ollama serve`"

def build_reply(user_text: str) -> str:
    chunks = []
    for token in bot.send_message(user_text):
        chunks.append(token)
    return "".join(chunks).strip()

def chat_submit(message, audio_input, history):
    try:
        history = history or []
        user_text = (message or "").strip()

        if not user_text and audio_input:
            user_text = transcribe_audio(audio_input)

        if not user_text:
            return history, "", None, "⚠️ Type a message or record/upload audio."

        assistant_reply = build_reply(user_text)
        audio_file = text_to_speech_file(assistant_reply)

        history = history + [(user_text, assistant_reply)]
        return history, "", audio_file, "✨ Response generated"
    except Exception as e:
        return history, "", None, f"❌ Error: {e}"

def use_quick_prompt(prompt_text):
    return prompt_text

def clear_chat():
    bot.clear_history()
    return [], "", None, "🧹 Conversation cleared"

def save_current_session():
    path = bot.save_session()
    if path:
        return f"💾 Session saved: {path}"
    return "⚠️ Nothing to save yet."

def show_saved_sessions():
    sessions = list_saved_sessions()
    if not sessions:
        return "No saved sessions found."
    return "\n".join(f"{i+1}. {sid}" for i, sid in enumerate(sessions[:20]))

with gr.Blocks(
    title="Aether — Local AI",
    css=CUSTOM_CSS,
    theme=gr.themes.Base(),
) as demo:

    with gr.Column(elem_id="hero"):
        gr.Markdown("# ✦ Aether")
        gr.Markdown(
            "A private local AI assistant with chat, voice input, voice output, and session memory.",
            elem_id="hero-sub",
        )

    with gr.Row():
        status_box = gr.Markdown(check_status(), elem_id="status-card")

    with gr.Row(elem_classes="shell"):
        with gr.Column(scale=1, min_width=250, elem_classes="sidebar-panel"):
            gr.Markdown("### Quick Actions", elem_classes="panel-title")

            with gr.Column(elem_classes="quick-grid"):
                chip_btns = [
                    gr.Button(p, elem_classes="quick-btn", size="sm")
                    for p in QUICK_PROMPTS
                ]

            gr.Markdown("### Controls", elem_classes="panel-title")
            clear_btn = gr.Button("🧹 Clear Chat", elem_classes="control-btn")
            save_btn = gr.Button("💾 Save Session", elem_classes="control-btn")
            refresh_btn = gr.Button("🔄 Check Ollama", elem_classes="control-btn")

            gr.Markdown("### Sessions", elem_classes="panel-title")
            sessions_box = gr.Textbox(
                label="Saved Session IDs",
                lines=8,
                interactive=False,
                elem_id="sessions-box",
            )
            load_sessions_btn = gr.Button("Refresh Sessions", elem_classes="control-btn")

        with gr.Column(scale=3, min_width=720, elem_classes="main-panel"):
            with gr.Column(elem_id="chat-wrap"):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=460,
                    elem_id="chatbot",
                )

            with gr.Column(elem_id="input-card"):
                text_input = gr.Textbox(
                    label="Message",
                    placeholder="Ask Aether anything...",
                    lines=2,
                    elem_id="message-box",
                )

                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="Voice Input",
                    elem_id="audio-box",
                )

                with gr.Row():
                    send_btn = gr.Button("✦ Send", elem_id="send-btn")
                    status_message = gr.Textbox(
                        value="Ready.",
                        interactive=False,
                        show_label=False,
                        elem_id="status-box",
                    )

            audio_output = gr.Audio(
                label="Assistant Voice Output",
                type="filepath",
                autoplay=True,
                elem_id="audio-output",
            )

    gr.Markdown(
        "Runs locally with Ollama + Gradio",
        elem_id="footer-note",
    )

    send_btn.click(
        fn=chat_submit,
        inputs=[text_input, audio_input, chatbot],
        outputs=[chatbot, text_input, audio_output, status_message],
        api_name=False,
    )
    text_input.submit(
        fn=chat_submit,
        inputs=[text_input, audio_input, chatbot],
        outputs=[chatbot, text_input, audio_output, status_message],
        api_name=False,
    )
    clear_btn.click(
        fn=clear_chat,
        inputs=[],
        outputs=[chatbot, text_input, audio_output, status_message],
        api_name=False,
    )
    save_btn.click(
        fn=save_current_session,
        inputs=[],
        outputs=[status_message],
        api_name=False,
    )
    refresh_btn.click(
        fn=check_status,
        inputs=[],
        outputs=[status_box],
        api_name=False,
    )
    load_sessions_btn.click(
        fn=show_saved_sessions,
        inputs=[],
        outputs=[sessions_box],
        api_name=False,
    )

    for chip in chip_btns:
        chip.click(
            fn=use_quick_prompt,
            inputs=[chip],
            outputs=[text_input],
            api_name=False,
        )

if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_api=False,
    )
