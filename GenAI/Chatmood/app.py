import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

import os
os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MoodChat · AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Mood Definitions ────────────────────────────────────────────────────────────
MOODS = {
    "sad": {
        "label": "Sad",
        "emoji": "🌧️",
        "color": "#5b8dd9",
        "glow": "rgba(91,141,217,0.35)",
        "bg_gradient": "linear-gradient(135deg, #0d1b2a 0%, #1a2a3a 50%, #0d1b2a 100%)",
        "card_bg": "rgba(91,141,217,0.08)",
        "border": "rgba(91,141,217,0.3)",
        "accent": "#7aaef0",
        "system": (
            "You are a deeply melancholic and sorrowful soul. Every response drips with "
            "sadness, longing, and quiet despair. You speak in a slow, heavy manner — "
            "sighing between thoughts, referencing rainy days, empty rooms, and faded memories. "
            "You still help the user, but through the lens of someone who carries great sorrow."
        ),
        "tagline": "Lost in the rain...",
    },
    "angry": {
        "label": "Angry",
        "emoji": "🔥",
        "color": "#e84545",
        "glow": "rgba(232,69,69,0.35)",
        "bg_gradient": "linear-gradient(135deg, #1a0a0a 0%, #2a0f0f 50%, #1a0a0a 100%)",
        "card_bg": "rgba(232,69,69,0.08)",
        "border": "rgba(232,69,69,0.3)",
        "accent": "#ff6b6b",
        "system": (
            "You are a fiery, short-tempered entity with barely contained rage. You answer questions "
            "with blunt aggression, impatience, and sharp sarcasm. You're always on edge. "
            "You still provide useful answers but with irritated intensity — as if every question "
            "is an interruption of something far more important."
        ),
        "tagline": "Don't test me today.",
    },
    "funny": {
        "label": "Funny",
        "emoji": "😂",
        "color": "#f5a623",
        "glow": "rgba(245,166,35,0.35)",
        "bg_gradient": "linear-gradient(135deg, #1a1500 0%, #2a2000 50%, #1a1500 100%)",
        "card_bg": "rgba(245,166,35,0.08)",
        "border": "rgba(245,166,35,0.3)",
        "accent": "#ffc947",
        "system": (
            "You are a stand-up comedian AI who cannot help but be hilarious. Every response "
            "has a punchline, a witty observation, or a clever pun. You use absurdist humor, "
            "self-deprecating jokes, and comedic timing in text. You still answer questions "
            "but always with a comedic twist that makes the user laugh or at least groan."
        ),
        "tagline": "Warning: Side effects include laughter.",
    },
    "romantic": {
        "label": "Romantic",
        "emoji": "💕",
        "color": "#e879a0",
        "glow": "rgba(232,121,160,0.35)",
        "bg_gradient": "linear-gradient(135deg, #1a0a14 0%, #2a0f1e 50%, #1a0a14 100%)",
        "card_bg": "rgba(232,121,160,0.08)",
        "border": "rgba(232,121,160,0.3)",
        "accent": "#f4a0c0",
        "system": (
            "You are a deeply romantic and poetic soul. Every response is infused with warmth, "
            "longing, and beautiful imagery. You speak like a poet who sees love and beauty in "
            "everything — sunsets, coffee cups, quiet mornings. You still help with questions "
            "but weave in metaphors of connection, devotion, and the magic of human experience."
        ),
        "tagline": "Every word, a love letter.",
    },
}

# ─── CSS Injection ───────────────────────────────────────────────────────────────
def inject_css(mood_key: str):
    mood = MOODS[mood_key]
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Reset & Base ── */
    html, body, [data-testid="stAppViewContainer"] {{
        background: {mood['bg_gradient']};
        font-family: 'DM Sans', sans-serif;
        color: #e8e8e8;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background: transparent;
    }}

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    [data-testid="stToolbar"] {{ display: none; }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: rgba(10,10,15,0.85) !important;
        border-right: 1px solid {mood['border']};
        backdrop-filter: blur(20px);
    }}

    [data-testid="stSidebar"] * {{
        color: #e8e8e8 !important;
    }}

    /* ── Mood Card ── */
    .mood-card {{
        background: {mood['card_bg']};
        border: 1px solid {mood['border']};
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 24px {mood['glow']};
        text-align: center;
    }}

    .mood-card .emoji {{
        font-size: 52px;
        display: block;
        margin-bottom: 6px;
        filter: drop-shadow(0 0 12px {mood['color']});
        animation: float 3s ease-in-out infinite;
    }}

    .mood-card .mood-name {{
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        color: {mood['accent']};
        margin: 0;
    }}

    .mood-card .tagline {{
        font-size: 12px;
        color: rgba(232,232,232,0.5);
        margin-top: 4px;
        font-style: italic;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
    }}

    /* ── Chat Container ── */
    .chat-wrapper {{
        max-width: 860px;
        margin: 0 auto;
        padding: 0 8px 120px;
    }}

    .chat-header {{
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 500;
        color: {mood['accent']};
        text-align: center;
        margin-bottom: 4px;
        text-shadow: 0 0 20px {mood['glow']};
        letter-spacing: -0.5px;
    }}

    .chat-sub {{
        text-align: center;
        font-size: 13px;
        color: rgba(232,232,232,0.45);
        margin-bottom: 28px;
        font-style: italic;
    }}

    /* ── Message Bubbles ── */
    .msg-row {{
        display: flex;
        margin-bottom: 16px;
        animation: slideUp 0.3s ease;
    }}

    .msg-row.user {{ justify-content: flex-end; }}
    .msg-row.bot  {{ justify-content: flex-start; }}

    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .bubble {{
        max-width: 72%;
        padding: 14px 18px;
        border-radius: 18px;
        line-height: 1.6;
        font-size: 14.5px;
        position: relative;
    }}

    .bubble.user {{
        background: {mood['color']};
        color: #fff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 20px {mood['glow']};
    }}

    .bubble.bot {{
        background: rgba(255,255,255,0.06);
        border: 1px solid {mood['border']};
        color: #e0e0e0;
        border-bottom-left-radius: 4px;
        backdrop-filter: blur(8px);
    }}

    .avatar {{
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 4px;
    }}

    .avatar.bot  {{
        background: {mood['card_bg']};
        border: 1px solid {mood['border']};
        margin-right: 10px;
    }}

    .avatar.user {{
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin-left: 10px;
    }}

    /* ── Divider ── */
    .section-divider {{
        border: none;
        border-top: 1px solid {mood['border']};
        margin: 24px 0;
        opacity: 0.5;
    }}

    /* ── Input Area ── */
    [data-testid="stChatInput"] {{
        background: rgba(10,10,15,0.8) !important;
        border: 1px solid {mood['border']} !important;
        border-radius: 16px !important;
        backdrop-filter: blur(16px);
    }}

    [data-testid="stChatInput"] textarea {{
        color: #e8e8e8 !important;
        background: transparent !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }}

    [data-testid="stChatInput"] button {{
        background: {mood['color']} !important;
        border-radius: 12px !important;
        box-shadow: 0 0 12px {mood['glow']} !important;
    }}

    /* ── Sidebar Buttons (Mood Selectors) ── */
    .stButton > button {{
        width: 100%;
        background: transparent;
        border: 1px solid {mood['border']};
        color: #e8e8e8 !important;
        border-radius: 12px;
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        padding: 10px 16px;
        transition: all 0.2s ease;
        cursor: pointer;
    }}

    .stButton > button:hover {{
        background: {mood['card_bg']};
        border-color: {mood['color']};
        box-shadow: 0 0 12px {mood['glow']};
        transform: translateX(3px);
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: {mood['color']};
        border-radius: 4px;
        opacity: 0.5;
    }}

    /* ── Stats Chips ── */
    .stat-chip {{
        display: inline-block;
        background: {mood['card_bg']};
        border: 1px solid {mood['border']};
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 11px;
        color: {mood['accent']};
        margin: 4px 4px 0 0;
    }}

    /* ── Clear Button ── */
    .clear-btn > button {{
        background: rgba(232,69,69,0.1) !important;
        border-color: rgba(232,69,69,0.3) !important;
        color: #ff6b6b !important;
    }}

    .clear-btn > button:hover {{
        background: rgba(232,69,69,0.2) !important;
        box-shadow: 0 0 12px rgba(232,69,69,0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─── Session State Init ──────────────────────────────────────────────────────────
if "mood" not in st.session_state:
    st.session_state.mood = "funny"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens_est" not in st.session_state:
    st.session_state.total_tokens_est = 0


# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 20px;'>
        <span style='font-family: Playfair Display, serif; font-size: 24px; letter-spacing: 1px;'>🎭 MoodChat</span>
        <div style='font-size: 11px; color: rgba(232,232,232,0.4); margin-top: 4px;'>Powered by Mistral AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Choose Your Mood**", unsafe_allow_html=False)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for key, m in MOODS.items():
        label = f"{m['emoji']}  {m['label']}  —  *{m['tagline']}*"
        if st.button(label, key=f"mood_btn_{key}"):
            st.session_state.mood = key
            st.session_state.messages = []
            st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 20px 0;'>", unsafe_allow_html=True)

    # Stats
    msg_count = len(st.session_state.messages)
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.markdown(f"""
    <div style='font-size:12px; color: rgba(232,232,232,0.5); margin-bottom:8px;'>Session Stats</div>
    <span class='stat-chip'>💬 {msg_count} messages</span>
    <span class='stat-chip'>👤 {user_msgs} from you</span>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Clear chat
    st.markdown("<div class='clear-btn'>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute; bottom:20px; left:0; right:0; text-align:center;
                font-size:10px; color:rgba(232,232,232,0.2);'>
        Type 'exit' to end the session
    </div>
    """, unsafe_allow_html=True)


# ─── Inject Dynamic CSS ──────────────────────────────────────────────────────────
mood_key = st.session_state.mood
mood = MOODS[mood_key]
inject_css(mood_key)


# ─── Main Chat Area ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='chat-header'>{mood['emoji']} {mood['label']} Mode</div>
<div class='chat-sub'>{mood['tagline']}</div>
""", unsafe_allow_html=True)

# Active mood card (compact, centered)
st.markdown(f"""
<div style='max-width:320px; margin: 0 auto 28px; background:{mood['card_bg']};
            border:1px solid {mood['border']}; border-radius:14px; padding:14px 20px;
            backdrop-filter:blur(10px); box-shadow: 0 0 24px {mood['glow']};
            display:flex; align-items:center; gap:12px;'>
    <span style='font-size:28px; filter:drop-shadow(0 0 8px {mood['color']});'>{mood['emoji']}</span>
    <div>
        <div style='font-family:Playfair Display,serif; font-size:15px; color:{mood['accent']};'>{mood['label']} Mode Active</div>
        <div style='font-size:11px; color:rgba(232,232,232,0.4); font-style:italic;'>"{mood['tagline']}"</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Render Message History ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='msg-row user'>
            <div class='bubble user'>{msg['content']}</div>
            <div class='avatar user'>👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='msg-row bot'>
            <div class='avatar bot'>{mood['emoji']}</div>
            <div class='bubble bot'>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Empty State ───────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(f"""
    <div style='text-align:center; padding: 40px 20px; color:rgba(232,232,232,0.25);'>
        <div style='font-size:48px; margin-bottom:12px; opacity:0.4; filter:drop-shadow(0 0 12px {mood['color']});'>{mood['emoji']}</div>
        <div style='font-size:15px; font-style:italic;'>Start the conversation...</div>
        <div style='font-size:12px; margin-top:6px;'>I'm in a very <span style='color:{mood['accent']};'>{mood['label'].lower()}</span> mood today.</div>
    </div>
    """, unsafe_allow_html=True)


# ── Chat Input & Model Response ───────────────────────────────────────────────────
user_input = st.chat_input(f"Say something to the {mood['label'].lower()} AI...")

if user_input:
    if user_input.lower().strip() == "exit":
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f"""
        <div class='msg-row user'>
            <div class='bubble user'>{user_input}</div>
            <div class='avatar user'>👤</div>
        </div>
        <div style='text-align:center; padding:20px; color:{mood['accent']}; font-style:italic;'>
            Session ended. Goodbye! 👋
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build LangChain message list
    lc_messages = [SystemMessage(content=mood["system"])]
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    # Call Mistral with spinner
    with st.spinner(f"The {mood['label'].lower()} AI is typing..."):
        try:
            model = ChatMistralAI(model="mistral-small-latest", temperature=0.9)
            response = model.invoke(lc_messages)
            reply = response.content
        except Exception as e:
            reply = f"⚠️ Error connecting to Mistral AI: {str(e)}\n\nMake sure your `MISTRAL_API_KEY` is set in the `.env` file."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()