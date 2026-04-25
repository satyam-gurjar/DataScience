import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
import time
import re
import json

load_dotenv()

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineSnap",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Master CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;0,700;1,300;1,600&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --gold:        #D4AF37;
    --gold-dim:    #A8882A;
    --gold-glow:   rgba(212,175,55,0.15);
    --cream:       #F0E8D5;
    --ink:         #080706;
    --deep:        #0D0B09;
    --card:        #131109;
    --card2:       #181410;
    --border:      rgba(212,175,55,0.18);
    --border2:     rgba(212,175,55,0.08);
    --muted:       #7A6F5E;
    --muted2:      #4A4236;
    --red:         #E05252;
    --green:       #52C97A;
    --blue:        #5298C9;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background: var(--ink) !important;
    color: var(--cream) !important;
}
.stApp { background: var(--ink) !important; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 4px; }

/* ── FIXED SPLIT LAYOUT ── */
.split-container {
    display: flex;
    height: calc(100vh - 180px);
    gap: 0;
    overflow: hidden;
    border: 1px solid var(--border);
    border-radius: 10px;
    margin: 0 1rem;
}
.split-left {
    width: 50%;
    min-width: 50%;
    overflow-y: auto;
    border-right: 1px solid var(--border);
    padding: 2rem;
    background: var(--deep);
    scrollbar-width: thin;
    scrollbar-color: var(--gold-dim) transparent;
}
.split-right {
    width: 50%;
    overflow-y: auto;
    padding: 2rem;
    background: var(--ink);
    scrollbar-width: thin;
    scrollbar-color: var(--gold-dim) transparent;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 2rem 1rem 1.5rem;
    position: relative;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold-dim), transparent);
}
.hero-eyebrow {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.7rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3.2rem,6vw,5rem);
    font-weight: 700;
    color: var(--cream);
    line-height: 1;
    margin: 0;
    letter-spacing: -0.01em;
}
.hero-title em { color: var(--gold); font-style: italic; }
.hero-desc {
    margin-top: 0.6rem;
    font-size: 1.1rem;
    color: var(--cream);
    font-weight: 700;
}

/* ── INPUT MODE TOGGLE ── */
.mode-toggle {
    display: flex;
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 1.2rem;
}
.mode-btn {
    flex: 1;
    text-align: center;
    padding: 0.65rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--muted);
    border: none;
    background: transparent;
}
.mode-btn.active {
    background: linear-gradient(135deg, var(--gold), var(--gold-dim));
    color: var(--ink);
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border2) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.2rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem !important; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 5px !important;
    color: var(--cream) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.1rem !important;
    caret-color: var(--gold) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--muted) !important;
    font-style: italic;
}

/* ── BUTTON ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--gold), var(--gold-dim)) !important;
    color: var(--ink) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(212,175,55,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(212,175,55,0.4) !important;
}

/* ── SECTION LABEL ── */
.slabel {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── RESULT CARDS ── */
.rcard {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.rcard:hover { border-color: var(--border); }
.rcard-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 0.4rem;
}
.rcard-value {
    font-size: 1.05rem;
    color: var(--cream);
    line-height: 1.6;
}
.rcard-null { color: var(--muted); font-style: italic; font-size: 0.85rem; }

/* ── MOVIE TITLE BANNER ── */
.movie-banner {
    background: linear-gradient(135deg, rgba(212,175,55,0.1) 0%, rgba(212,175,55,0.03) 100%);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.movie-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--gold-dim), var(--gold), var(--gold-dim));
}
.movie-banner-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1.1;
}
.movie-banner-meta {
    font-size: 0.82rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── SCORE RING ── */
.score-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px; height: 64px;
    border-radius: 50%;
    border: 2px solid var(--gold);
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gold);
    background: rgba(212,175,55,0.06);
    box-shadow: 0 0 16px rgba(212,175,55,0.15);
}

/* ── PILL ── */
.pill {
    display: inline-block;
    background: rgba(212,175,55,0.08);
    border: 1px solid rgba(212,175,55,0.2);
    color: var(--gold);
    font-size: 0.75rem;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    margin: 0.2rem 0.15rem;
    font-weight: 500;
}
.pill-blue {
    background: rgba(82,152,201,0.1);
    border-color: rgba(82,152,201,0.3);
    color: #7BB8E0;
}
.pill-green {
    background: rgba(82,201,122,0.1);
    border-color: rgba(82,201,122,0.3);
    color: #7BE0A0;
}
.pill-red {
    background: rgba(224,82,82,0.1);
    border-color: rgba(224,82,82,0.3);
    color: #E08A8A;
}

/* ── WHY WATCH ── */
.why-card {
    background: linear-gradient(135deg, rgba(212,175,55,0.07), rgba(212,175,55,0.02));
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.why-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border2);
}
.why-item:last-child { border-bottom: none; }
.why-icon { font-size: 1.1rem; margin-top: 1px; flex-shrink: 0; }
.why-text { font-size: 0.9rem; color: var(--cream); line-height: 1.55; }

/* ── VERDICT BADGE ── */
.verdict {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.2rem;
    border-radius: 25px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
}
.verdict-watch { background: rgba(82,201,122,0.15); border: 1px solid rgba(82,201,122,0.35); color: #7BE0A0; }
.verdict-maybe { background: rgba(212,175,55,0.12); border: 1px solid rgba(212,175,55,0.3); color: var(--gold); }
.verdict-skip  { background: rgba(224,82,82,0.12); border: 1px solid rgba(224,82,82,0.3); color: #E08A8A; }

/* ── TRIVIA / FUN FACTS ── */
.trivia-item {
    background: var(--card2);
    border-left: 3px solid var(--gold);
    border-radius: 0 5px 5px 0;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    color: var(--cream);
    line-height: 1.6;
}

/* ── CONTENT WARNINGS ── */
.warn-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(224,82,82,0.06);
    border: 1px solid rgba(224,82,82,0.15);
    border-radius: 4px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #E0B0B0;
}

/* ── SIMILAR MOVIES ── */
.similar-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
}
.similar-card {
    background: var(--card);
    border: 1px solid var(--border2);
    border-radius: 5px;
    padding: 0.8rem;
    text-align: center;
    transition: all 0.2s;
}
.similar-card:hover { border-color: var(--border); transform: translateY(-2px); }
.similar-card-title { font-size: 0.8rem; font-weight: 600; color: var(--cream); }
.similar-card-year { font-size: 0.7rem; color: var(--muted); margin-top: 0.2rem; }

/* ── PROGRESS BAR ── */
.prog-bar-wrap { margin-bottom: 0.7rem; }
.prog-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
.prog-bar-track {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 4px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--gold-dim), var(--gold));
}

/* ── SUMMARY QUOTE ── */
.summary-quote {
    border-left: 3px solid var(--gold);
    padding: 1rem 1.4rem;
    background: rgba(212,175,55,0.04);
    border-radius: 0 6px 6px 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-style: italic;
    color: var(--cream);
    line-height: 1.9;
    margin-bottom: 1rem;
}

/* ── EMPTY STATE ── */
.empty-state {
    height: 100%;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
}
.empty-icon {
    font-size: 3.5rem;
    opacity: 0.25;
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 0.2; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(1.05); }
}
.empty-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    font-style: italic;
    color: var(--muted);
    text-align: center;
    max-width: 240px;
    line-height: 1.7;
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.2rem 0;
}

/* ── EXAMPLE CHIPS ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.75rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover { border-color: var(--gold-dim); color: var(--gold); }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    color: var(--cream) !important;
    border-radius: 5px !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── SCROLLBAR FOR SPLIT ── */
.split-left::-webkit-scrollbar,
.split-right::-webkit-scrollbar { width: 3px; }
.split-left::-webkit-scrollbar-thumb,
.split-right::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 1.5rem;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    color: var(--muted2);
    border-top: 1px solid var(--border2);
    margin-top: 1rem;
}

/* ── ANIMATIONS ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)


# ── LLM Setup ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-latest")


def build_name_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
You are CineExtract Pro — a world-class cinema intelligence engine.

Given ONLY a movie name, produce a comprehensive JSON response with ALL of the following fields.
Respond ONLY with valid JSON — no markdown, no backticks, no extra text.

JSON Schema:
{{
  "movie_title": "string",
  "release_year": "string",
  "genre": ["array of genres"],
  "director": "string",
  "main_cast": ["array of actor names"],
  "setting_location": "string",
  "plot": "string (3-4 sentences)",
  "themes": ["array of themes"],
  "imdb_rating": "string (e.g. 8.6/10)",
  "rt_score": "string (e.g. 73%)",
  "audience_score": "string",
  "language": "string",
  "runtime": "string (e.g. 169 min)",
  "budget": "string",
  "box_office": "string",
  "awards": "string",
  "content_rating": "string (e.g. PG-13)",
  "content_warnings": ["array of content warnings e.g. violence, language, etc."],
  "short_summary": "string (2-3 elegant sentences)",
  "why_watch": ["array of 4-5 compelling reasons to watch this movie"],
  "watch_verdict": "MUST WATCH | WORTH WATCHING | CASUAL WATCH | SKIP",
  "verdict_reason": "string (1 sentence explaining verdict)",
  "best_watched": "string (e.g. With family, On a date night, Alone at night, etc.)",
  "mood_match": ["array of moods this film suits e.g. Thoughtful, Adventurous, etc."],
  "trivia": ["array of 3 interesting behind-the-scenes facts"],
  "similar_movies": [{{"title": "string", "year": "string"}}, ...],
  "streaming_note": "string (general streaming availability note)",
  "cinematographer": "string",
  "music_composer": "string",
  "notable_features": "string",
  "audience_vibe_scores": {{
    "action": 0,
    "emotion": 0,
    "humor": 0,
    "suspense": 0,
    "romance": 0
  }}
}}

All score values (action, emotion, humor, suspense, romance) must be integers between 0 and 10.
If any field is unknown, use null. Be accurate, detailed, and insightful.
"""),
        ("human", "Movie name: {movie_name}")
    ])


def build_paragraph_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
You are CineExtract Pro — a world-class cinema intelligence engine.

Given a movie paragraph, extract and enrich all information. 
Respond ONLY with valid JSON — no markdown, no backticks, no extra text.

JSON Schema:
{{
  "movie_title": "string",
  "release_year": "string",
  "genre": ["array"],
  "director": "string",
  "main_cast": ["array"],
  "setting_location": "string",
  "plot": "string",
  "themes": ["array"],
  "imdb_rating": "string",
  "rt_score": "string",
  "audience_score": "string",
  "language": "string",
  "runtime": "string",
  "budget": "string",
  "box_office": "string",
  "awards": "string",
  "content_rating": "string",
  "content_warnings": ["array"],
  "short_summary": "string",
  "why_watch": ["array of 4-5 compelling reasons"],
  "watch_verdict": "MUST WATCH | WORTH WATCHING | CASUAL WATCH | SKIP",
  "verdict_reason": "string",
  "best_watched": "string",
  "mood_match": ["array"],
  "trivia": ["array of 3 facts"],
  "similar_movies": [{{"title": "string", "year": "string"}}],
  "streaming_note": "string",
  "cinematographer": "string",
  "music_composer": "string",
  "notable_features": "string",
  "audience_vibe_scores": {{
    "action": 0,
    "emotion": 0,
    "humor": 0,
    "suspense": 0,
    "romance": 0
  }}
}}

All score values must be integers between 0 and 10.
If any field is unknown, use null. Enrich with your knowledge where the paragraph is incomplete.
"""),
        ("human", "Extract from this paragraph:\n\n{paragraph}")
    ])


# ── Helper: Parse JSON response ────────────────────────────────────────────────
def parse_json_response(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
    return {}


def v(data, key, fallback="—"):
    val = data.get(key)
    if val is None or val == "" or (isinstance(val, list) and len(val) == 0):
        return fallback
    return val


def pills_html(items, style="gold"):
    if not items or items == "—":
        return '<span class="rcard-null">Not available</span>'
    if isinstance(items, str):
        items = [items]
    css = {"gold": "pill", "blue": "pill pill-blue", "green": "pill pill-green", "red": "pill pill-red"}
    cls = css.get(style, "pill")
    return "".join(f'<span class="{cls}">{i}</span>' for i in items)


def prog_bar(label, value, max_val=10):
    pct = int((value / max_val) * 100) if value else 0
    return f"""
    <div class="prog-bar-wrap">
        <div class="prog-bar-label"><span>{label}</span><span>{value}/10</span></div>
        <div class="prog-bar-track"><div class="prog-bar-fill" style="width:{pct}%"></div></div>
    </div>"""


def verdict_html(verdict, reason):
    mapping = {
        "MUST WATCH": ("verdict-watch", "✦ MUST WATCH"),
        "WORTH WATCHING": ("verdict-maybe", "◈ WORTH WATCHING"),
        "CASUAL WATCH": ("verdict-maybe", "◇ CASUAL WATCH"),
        "SKIP": ("verdict-skip", "✕ SKIP"),
    }
    cls, label = mapping.get(str(verdict).upper().strip(), ("verdict-maybe", verdict))
    return f'<span class="verdict {cls}">{label}</span><div style="font-size:0.8rem;color:var(--muted);margin-top:0.5rem">{reason or ""}</div>'


# ── Session State ─────────────────────────────────────────────────────────────
for k, d in [("result", None), ("mode", "name"), ("movie_name", ""), ("paragraph", "")]:
    if k not in st.session_state:
        st.session_state[k] = d

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ &nbsp; AI Cinema Intelligence &nbsp; ✦</div>
    <div class="hero-title">Cine<em>Extract</em> Pro</div>
    <div class="hero-desc">Enter a movie name or paragraph — get everything you need to know before watching</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Split Layout ──────────────────────────────────────────────────────────────
# We simulate the split with st.columns but inject JS for independent scroll
left, right = st.columns(2, gap="large")

# ──────────────── LEFT PANEL ──────────────────────────────────────────────────
with left:
    # Mode Toggle
    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("🎬  Movie Name", key="btn_mode_name", use_container_width=True):
            st.session_state.mode = "name"
            st.session_state.result = None
    with mode_col2:
        if st.button("📝  Paragraph", key="btn_mode_para", use_container_width=True):
            st.session_state.mode = "paragraph"
            st.session_state.result = None

    st.markdown(f"""
    <div style="font-size:0.7rem; color:var(--muted); text-align:center; margin:-0.3rem 0 0.8rem;
                letter-spacing:0.08em;">
        Active mode: <span style="color:var(--gold); font-weight:600;">
        {'🎬 Movie Name' if st.session_state.mode == 'name' else '📝 Paragraph'}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── INPUT: Movie Name Mode ──
    if st.session_state.mode == "name":
        st.markdown('<div class="slabel">🎬 &nbsp; Movie Name</div>', unsafe_allow_html=True)
        movie_input = st.text_input(
            "movie_name_input",
            label_visibility="collapsed",
            placeholder="e.g.  Interstellar,  Parasite,  The Godfather…",
            value=st.session_state.movie_name,
            key="movie_name_field"
        )

        st.markdown("""
        <div class="slabel" style="margin-top:0.8rem">⚡ &nbsp; Quick Pick</div>
        <div class="chip-row">""", unsafe_allow_html=True)

        QUICK = ["Interstellar", "Inception", "Parasite", "The Dark Knight",
                 "The Godfather", "Dune", "Oppenheimer", "Whiplash"]
        cols = st.columns(4)
        for i, movie in enumerate(QUICK):
            with cols[i % 4]:
                if st.button(movie, key=f"quick_{i}", use_container_width=True):
                    st.session_state.movie_name = movie
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦ &nbsp; Analyse Movie", key="btn_extract_name", use_container_width=True):
            name = movie_input or st.session_state.movie_name
            if not name.strip():
                st.error("⚠ Please enter a movie name.")
            else:
                with st.spinner(f'Fetching intelligence on  \"{name}\"…'):
                    try:
                        model = get_model()
                        prompt = build_name_prompt()
                        chain = prompt | model
                        t0 = time.time()
                        resp = chain.invoke({"movie_name": name})
                        elapsed = round(time.time() - t0, 1)
                        parsed = parse_json_response(resp.content)
                        st.session_state.result = {"data": parsed, "elapsed": elapsed}
                        st.session_state.movie_name = name
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # ── INPUT: Paragraph Mode ──
    else:
        st.markdown('<div class="slabel">📝 &nbsp; Movie Paragraph</div>', unsafe_allow_html=True)
        para_input = st.text_area(
            "para_input",
            label_visibility="collapsed",
            placeholder="Paste any movie description from Wikipedia, IMDb, a review, or your own writing…",
            height=180,
            value=st.session_state.paragraph,
            key="para_field"
        )

        PARA_EXAMPLES = {
            "Interstellar": "Interstellar is a visually stunning science fiction epic directed by Christopher Nolan. Released in 2014, the film stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, and Michael Caine. The story revolves around a group of astronauts who travel through a wormhole near Saturn in search of a new home for humanity as Earth faces environmental collapse. The movie was widely appreciated for its emotional depth, scientific accuracy, and Hans Zimmer's powerful soundtrack. It holds a rating of 8.6 on IMDb.",
            "Parasite": "Parasite is a 2019 South Korean black comedy thriller directed by Bong Joon-ho, starring Song Kang-ho and Lee Sun-kyun. The film follows the Kim family who infiltrate a wealthy household through deception. It won the Palme d'Or at Cannes and became the first non-English film to win Best Picture at the Oscars. Its razor-sharp critique of class inequality made it a cultural phenomenon with an 8.5 IMDb rating.",
        }

        ex_c1, ex_c2 = st.columns(2)
        for i, (title, text) in enumerate(PARA_EXAMPLES.items()):
            with (ex_c1 if i == 0 else ex_c2):
                if st.button(f"📋 {title}", key=f"para_ex_{i}", use_container_width=True):
                    st.session_state.paragraph = text
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦ &nbsp; Extract Intelligence", key="btn_extract_para", use_container_width=True):
            para = para_input or st.session_state.paragraph
            if not para.strip():
                st.error("⚠ Please enter a movie paragraph.")
            else:
                with st.spinner("Analysing paragraph with Mistral AI…"):
                    try:
                        model = get_model()
                        prompt = build_paragraph_prompt()
                        chain = prompt | model
                        t0 = time.time()
                        resp = chain.invoke({"paragraph": para})
                        elapsed = round(time.time() - t0, 1)
                        parsed = parse_json_response(resp.content)
                        st.session_state.result = {"data": parsed, "elapsed": elapsed}
                        st.session_state.paragraph = para
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # ── About Section ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0.5rem 0;">
        <div class="slabel">🧠 &nbsp; What You Get</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.6rem;">
    """, unsafe_allow_html=True)

    features = [
        ("🎭", "Full Cast & Crew"), ("⭐", "Ratings & Scores"),
        ("📖", "Plot & Themes"), ("✦", "Why Watch?"),
        ("⚡", "Vibe Scores"), ("🎬", "Similar Movies"),
        ("⚠", "Content Warnings"), ("🎲", "Fun Trivia"),
    ]
    feat_html = ""
    for icon, label in features:
        feat_html += f"""
        <div style="display:flex; align-items:center; gap:0.5rem;
                    background:var(--card); border:1px solid var(--border2);
                    border-radius:4px; padding:0.5rem 0.7rem;">
            <span style="font-size:0.9rem">{icon}</span>
            <span style="font-size:0.75rem; color:var(--muted); font-weight:500">{label}</span>
        </div>"""
    st.markdown(feat_html + "</div></div>", unsafe_allow_html=True)


# ──────────────── RIGHT PANEL ─────────────────────────────────────────────────
with right:
    if not st.session_state.result:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎬</div>
            <div class="empty-text">Your cinema intelligence report will appear here</div>
            <div style="font-size:0.68rem; color:var(--muted2); letter-spacing:0.15em; text-transform:uppercase; margin-top:0.4rem;">
                Enter a movie name or paragraph
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        d = st.session_state.result["data"]
        elapsed = st.session_state.result["elapsed"]

        if not d:
            st.error("Could not parse the response. Please try again.")
        else:
            # Movie Banner
            genres = v(d, "genre", [])
            genre_str = " · ".join(genres[:3]) if isinstance(genres, list) else genres
            st.markdown(f"""
            <div class="movie-banner fade-in">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="movie-banner-title">{v(d, 'movie_title')}</div>
                        <div class="movie-banner-meta">
                            {v(d,'release_year')} &nbsp;·&nbsp; {genre_str} &nbsp;·&nbsp;
                            {v(d,'runtime')} &nbsp;·&nbsp; {v(d,'content_rating')}
                        </div>
                    </div>
                    <div style="text-align:center">
                        <div class="score-ring">{v(d,'imdb_rating','?').replace('/10','')}</div>
                        <div style="font-size:0.6rem; color:var(--muted); margin-top:0.3rem; letter-spacing:0.1em">IMDb</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 Overview", "✦ Why Watch", "📊 Ratings", "🎲 Trivia", "🎭 More"
            ])

            # ── Tab 1: Overview ──
            with tab1:
                # Summary
                summary = v(d, "short_summary")
                if summary != "—":
                    st.markdown(f'<div class="summary-quote">{summary}</div>', unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">🎬 Director</div>
                        <div class="rcard-value">{v(d,'director')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">📅 Release Year</div>
                        <div class="rcard-value">{v(d,'release_year')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">🌍 Language</div>
                        <div class="rcard-value">{v(d,'language')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">⏱ Runtime</div>
                        <div class="rcard-value">{v(d,'runtime')}</div>
                    </div>""", unsafe_allow_html=True)

                with col_b:
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">💰 Budget</div>
                        <div class="rcard-value">{v(d,'budget')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">🏆 Box Office</div>
                        <div class="rcard-value">{v(d,'box_office')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">🎵 Music</div>
                        <div class="rcard-value">{v(d,'music_composer')}</div>
                    </div>
                    <div class="rcard">
                        <div class="rcard-label">📷 Cinematographer</div>
                        <div class="rcard-value">{v(d,'cinematographer')}</div>
                    </div>""", unsafe_allow_html=True)

                # Cast
                cast = v(d, "main_cast", [])
                st.markdown(f"""
                <div class="rcard">
                    <div class="rcard-label">🎭 Main Cast</div>
                    <div style="margin-top:0.3rem">{pills_html(cast if cast != '—' else [], 'blue')}</div>
                </div>""", unsafe_allow_html=True)

                # Genres & Themes
                themes = v(d, "themes", [])
                st.markdown(f"""
                <div class="rcard">
                    <div class="rcard-label">🎨 Genres</div>
                    <div style="margin-top:0.3rem">{pills_html(genres if genres != '—' else [])}</div>
                </div>
                <div class="rcard">
                    <div class="rcard-label">💡 Themes</div>
                    <div style="margin-top:0.3rem">{pills_html(themes if themes != '—' else [], 'green')}</div>
                </div>""", unsafe_allow_html=True)

                # Plot
                plot = v(d, "plot")
                if plot != "—":
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">📖 Plot</div>
                        <div class="rcard-value" style="margin-top:0.3rem">{plot}</div>
                    </div>""", unsafe_allow_html=True)

                # Awards
                awards = v(d, "awards")
                if awards != "—":
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">🏅 Awards</div>
                        <div class="rcard-value">{awards}</div>
                    </div>""", unsafe_allow_html=True)

            # ── Tab 2: Why Watch ──
            with tab2:
                # Verdict
                verdict = v(d, "watch_verdict")
                reason = v(d, "verdict_reason", "")
                st.markdown(f"""
                <div style="text-align:center; margin-bottom:1.2rem;">
                    {verdict_html(verdict, reason)}
                </div>""", unsafe_allow_html=True)

                # Best Watched
                best = v(d, "best_watched")
                mood = v(d, "mood_match", [])
                if best != "—" or mood != "—":
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">🌙 Best Watched</div>
                        <div class="rcard-value">{best}</div>
                        <div style="margin-top:0.5rem">{pills_html(mood if mood != '—' else [], 'green')}</div>
                    </div>""", unsafe_allow_html=True)

                # Why Watch reasons
                why = v(d, "why_watch", [])
                if why != "—" and isinstance(why, list):
                    st.markdown("""
                    <div class="rcard-label" style="margin-bottom:0.4rem">✦ &nbsp; Reasons to Watch</div>
                    <div class="why-card">""", unsafe_allow_html=True)
                    icons = ["🎯", "🎨", "🧠", "❤️", "🌟"]
                    why_html = ""
                    for i, reason_item in enumerate(why[:5]):
                        icon = icons[i % len(icons)]
                        why_html += f"""
                        <div class="why-item">
                            <span class="why-icon">{icon}</span>
                            <span class="why-text">{reason_item}</span>
                        </div>"""
                    st.markdown(why_html + "</div>", unsafe_allow_html=True)

                # Content Warnings
                warnings = v(d, "content_warnings", [])
                if warnings != "—" and isinstance(warnings, list) and warnings:
                    st.markdown('<div class="rcard-label" style="margin:1rem 0 0.4rem">⚠ Content Warnings</div>',
                                unsafe_allow_html=True)
                    for w in warnings:
                        st.markdown(f'<div class="warn-item">⚠ &nbsp; {w}</div>', unsafe_allow_html=True)

                # Streaming
                streaming = v(d, "streaming_note")
                if streaming != "—":
                    st.markdown(f"""
                    <div class="rcard" style="margin-top:0.8rem">
                        <div class="rcard-label">📺 Where to Watch</div>
                        <div class="rcard-value">{streaming}</div>
                    </div>""", unsafe_allow_html=True)

            # ── Tab 3: Ratings ──
            with tab3:
                # Score cards
                r1, r2, r3 = st.columns(3)
                with r1:
                    imdb = v(d, "imdb_rating", "N/A")
                    st.markdown(f"""
                    <div style="text-align:center; padding:1rem;
                                background:var(--card); border:1px solid var(--border2); border-radius:6px;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:2.2rem;
                                    font-weight:700; color:var(--gold);">{imdb}</div>
                        <div style="font-size:0.65rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; margin-top:0.2rem">IMDb</div>
                    </div>""", unsafe_allow_html=True)
                with r2:
                    rt = v(d, "rt_score", "N/A")
                    st.markdown(f"""
                    <div style="text-align:center; padding:1rem;
                                background:var(--card); border:1px solid var(--border2); border-radius:6px;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:2.2rem;
                                    font-weight:700; color:#E87C53;">{rt}</div>
                        <div style="font-size:0.65rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; margin-top:0.2rem">Rotten Tomatoes</div>
                    </div>""", unsafe_allow_html=True)
                with r3:
                    aud = v(d, "audience_score", "N/A")
                    st.markdown(f"""
                    <div style="text-align:center; padding:1rem;
                                background:var(--card); border:1px solid var(--border2); border-radius:6px;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:2.2rem;
                                    font-weight:700; color:#7BE0A0;">{aud}</div>
                        <div style="font-size:0.65rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; margin-top:0.2rem">Audience Score</div>
                    </div>""", unsafe_allow_html=True)

                # Vibe Scores
                vibes = d.get("audience_vibe_scores")
                if vibes and isinstance(vibes, dict):
                    st.markdown("""
                    <div class="rcard" style="margin-top:1rem">
                        <div class="rcard-label" style="margin-bottom:0.8rem">🎯 &nbsp; Vibe Scores</div>
                    """, unsafe_allow_html=True)
                    vibe_labels = {
                        "action": "⚡ Action",
                        "emotion": "❤️ Emotion",
                        "humor": "😄 Humor",
                        "suspense": "😰 Suspense",
                        "romance": "💕 Romance",
                    }
                    bar_html = ""
                    for key, label in vibe_labels.items():
                        val = vibes.get(key, 0) or 0
                        bar_html += prog_bar(label, val)
                    st.markdown(bar_html + "</div>", unsafe_allow_html=True)

            # ── Tab 4: Trivia ──
            with tab4:
                trivia = v(d, "trivia", [])
                if trivia != "—" and isinstance(trivia, list):
                    st.markdown('<div class="rcard-label" style="margin-bottom:0.6rem">🎲 &nbsp; Behind the Scenes</div>',
                                unsafe_allow_html=True)
                    for fact in trivia:
                        st.markdown(f'<div class="trivia-item">🎬 &nbsp; {fact}</div>', unsafe_allow_html=True)

                # Notable Features
                notable = v(d, "notable_features")
                if notable != "—":
                    st.markdown(f"""
                    <div class="rcard" style="margin-top:1rem">
                        <div class="rcard-label">✨ Notable Features</div>
                        <div class="rcard-value" style="margin-top:0.3rem">{notable}</div>
                    </div>""", unsafe_allow_html=True)

                # Setting
                setting = v(d, "setting_location")
                if setting != "—":
                    st.markdown(f"""
                    <div class="rcard">
                        <div class="rcard-label">📍 Setting / Location</div>
                        <div class="rcard-value">{setting}</div>
                    </div>""", unsafe_allow_html=True)

            # ── Tab 5: More ──
            with tab5:
                # Similar Movies
                similar = v(d, "similar_movies", [])
                if similar != "—" and isinstance(similar, list) and similar:
                    st.markdown('<div class="rcard-label" style="margin-bottom:0.6rem">🎞 &nbsp; If You Liked This, Watch:</div>',
                                unsafe_allow_html=True)
                    sim_html = '<div class="similar-grid">'
                    for m in similar[:6]:
                        if isinstance(m, dict):
                            sim_html += f"""
                            <div class="similar-card">
                                <div style="font-size:1.2rem; margin-bottom:0.4rem">🎬</div>
                                <div class="similar-card-title">{m.get('title','?')}</div>
                                <div class="similar-card-year">{m.get('year','')}</div>
                            </div>"""
                    sim_html += "</div>"
                    st.markdown(sim_html, unsafe_allow_html=True)

                # Full JSON
                st.markdown('<div class="divider" style="margin:1rem 0"></div>', unsafe_allow_html=True)
                with st.expander("🔍 Raw JSON Data"):
                    st.json(d)

                # Stats
                filled = sum(1 for v_val in d.values()
                             if v_val is not None and v_val != "" and v_val != [] and v_val != {})
                total = len(d)
                st.markdown(f"""
                <div style="display:flex; gap:1rem; margin-top:1rem; flex-wrap:wrap;">
                    <div style="flex:1; text-align:center; background:var(--card);
                                border:1px solid var(--border2); border-radius:5px; padding:0.8rem;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:1.8rem;
                                    font-weight:700; color:var(--gold);">{filled}</div>
                        <div style="font-size:0.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.12em">Fields Found</div>
                    </div>
                    <div style="flex:1; text-align:center; background:var(--card);
                                border:1px solid var(--border2); border-radius:5px; padding:0.8rem;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:1.8rem;
                                    font-weight:700; color:var(--gold);">{round(filled/total*100)}%</div>
                        <div style="font-size:0.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.12em">Complete</div>
                    </div>
                    <div style="flex:1; text-align:center; background:var(--card);
                                border:1px solid var(--border2); border-radius:5px; padding:0.8rem;">
                        <div style="font-family:'Cormorant Garamond',serif; font-size:1.8rem;
                                    font-weight:700; color:var(--gold);">{elapsed}s</div>
                        <div style="font-size:0.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.12em">Analysis Time</div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    CineExtract Pro &nbsp;·&nbsp; Powered by <span style="color:var(--gold-dim)">LangChain · Mistral AI · Streamlit</span>
    &nbsp;·&nbsp; © 2025
</div>""", unsafe_allow_html=True)