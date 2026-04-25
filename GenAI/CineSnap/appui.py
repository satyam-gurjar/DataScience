import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
import time
import re

load_dotenv()

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineExtract · AI Movie Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --gold:      #D4AF37;
    --gold-dim:  #A8882A;
    --cream:     #F5EFE0;
    --ink:       #0E0C0A;
    --charcoal:  #1A1714;
    --card-bg:   #1E1B17;
    --border:    rgba(212,175,55,0.25);
    --text-muted:#8A7F72;
    --red-accent:#C0392B;
}

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--ink) !important;
    color: var(--cream) !important;
}

.stApp {
    background: var(--ink) !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--charcoal); }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 3px; }

/* ── Hero Header ── */
.hero-wrapper {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%; transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse, rgba(212,175,55,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold);
    border: 1px solid var(--border);
    padding: 0.3rem 1rem;
    border-radius: 2px;
    margin-bottom: 1.2rem;
    background: rgba(212,175,55,0.06);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: var(--cream);
    margin: 0 0 0.6rem;
}
.hero-title span {
    color: var(--gold);
    font-style: italic;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: var(--text-muted);
    max-width: 480px;
    margin: 0 auto 0.5rem;
    line-height: 1.6;
}
.divider-gold {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem auto;
}

/* ── Input Card ── */
.input-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    border-radius: 6px 6px 0 0;
}
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.8rem;
}

/* ── Textarea Styling ── */
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    caret-color: var(--gold) !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease !important;
    resize: vertical !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
    font-style: italic;
}

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dim) 100%) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(212,175,55,0.4) !important;
    background: linear-gradient(135deg, #E0C04A 0%, var(--gold) 100%) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Result Card ── */
.result-wrapper {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-top: 1.5rem;
}
.result-header {
    background: linear-gradient(90deg, rgba(212,175,55,0.12), transparent);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.result-header-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: 0.02em;
}
.result-body {
    padding: 1.5rem 1.8rem;
}

/* ── Info Fields ── */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.info-field {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(212,175,55,0.12);
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
    transition: border-color 0.2s;
}
.info-field:hover {
    border-color: rgba(212,175,55,0.3);
}
.field-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 0.35rem;
}
.field-value {
    font-size: 0.95rem;
    font-weight: 400;
    color: var(--cream);
    line-height: 1.5;
}
.field-value.null-value {
    color: var(--text-muted);
    font-style: italic;
    font-size: 0.88rem;
}
.cast-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.3rem;
}
.cast-pill {
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.2);
    color: var(--gold);
    font-size: 0.8rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-weight: 500;
}

/* ── Summary Block ── */
.summary-block {
    background: linear-gradient(135deg, rgba(212,175,55,0.06), rgba(212,175,55,0.02));
    border-left: 3px solid var(--gold);
    border-radius: 0 4px 4px 0;
    padding: 1.2rem 1.5rem;
    margin-top: 0.5rem;
}
.summary-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.5rem;
}
.summary-text {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-style: italic;
    color: var(--cream);
    line-height: 1.8;
}

/* ── Example Pills ── */
.example-section {
    margin-top: 1rem;
}
.example-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
}
.example-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.example-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--text-muted);
    font-size: 0.8rem;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'DM Sans', sans-serif;
}
.example-pill:hover {
    border-color: var(--gold-dim);
    color: var(--gold);
    background: rgba(212,175,55,0.07);
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    gap: 2rem;
    padding: 1rem 0;
    border-top: 1px solid var(--border);
    margin-top: 1.5rem;
}
.stat-item { text-align: center; }
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
}
.stat-label {
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 0.2rem;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--gold) !important;
}

/* ── Alert ── */
.stAlert {
    background: rgba(192,57,43,0.12) !important;
    border: 1px solid rgba(192,57,43,0.3) !important;
    border-radius: 4px !important;
    color: #E8A09A !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2.5rem 1rem;
    color: var(--text-muted);
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
}
.footer span { color: var(--gold-dim); }

/* ── Responsive ── */
@media (max-width: 768px) {
    .info-grid { grid-template-columns: 1fr; }
    .stats-bar { gap: 1rem; }
    .input-card { padding: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)


# ── LLM & Prompt Setup ────────────────────────────────────────────────────────
@st.cache_resource
def get_chain():
    model = ChatMistralAI(model="mistral-small-latest")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are a professional Movie Information Extraction Assistant.

Your task:
Extract useful structured information from a movie paragraph and present it in a clean format.

Rules:
- Do NOT add explanations
- Do NOT add extra commentary
- Follow the exact format below precisely
- If information is missing -> write NULL
- Keep summary short (2-3 lines max)
- Do NOT guess unknown facts

Output Format (use these exact labels):

Movie Title:
Release Year:
Genre:
Director:
Main Cast:
Setting/Location:
Plot:
Themes:
Ratings:
Notable Features:

Short Summary:
"""),
        ("human", "Extract information from this paragraph:\n\n{paragraph}")
    ])
    return prompt | model


# ── Parse Output ──────────────────────────────────────────────────────────────
def parse_response(text: str) -> dict:
    fields = {
        "Movie Title": None, "Release Year": None, "Genre": None,
        "Director": None, "Main Cast": None, "Setting/Location": None,
        "Plot": None, "Themes": None, "Ratings": None,
        "Notable Features": None, "Short Summary": None,
    }
    pattern = r"(?:Movie Title|Release Year|Genre|Director|Main Cast|Setting/Location|Plot|Themes|Ratings|Notable Features|Short Summary)\s*:\s*"
    keys = list(fields.keys())
    for i, key in enumerate(keys):
        next_key = keys[i + 1] if i + 1 < len(keys) else None
        if next_key:
            match = re.search(
                rf"{re.escape(key)}\s*:\s*(.*?)(?={re.escape(next_key)}\s*:)",
                text, re.DOTALL | re.IGNORECASE
            )
        else:
            match = re.search(rf"{re.escape(key)}\s*:\s*(.*?)$", text, re.DOTALL | re.IGNORECASE)
        if match:
            val = match.group(1).strip().strip("*").strip()
            fields[key] = val if val.upper() != "NULL" and val else None
    return fields


def render_field(label, value, wide=False):
    is_null = value is None or value.upper() == "NULL" if value else True
    if label == "Main Cast" and not is_null:
        actors = [a.strip() for a in re.split(r",|and ", value) if a.strip()]
        pills = "".join(f'<span class="cast-pill">{a}</span>' for a in actors)
        return f"""
        <div class="info-field">
            <div class="field-label">{label}</div>
            <div class="cast-pills">{pills}</div>
        </div>"""
    display = value if not is_null else "Not mentioned"
    cls = "field-value" if not is_null else "field-value null-value"
    return f"""
    <div class="info-field">
        <div class="field-label">{label}</div>
        <div class="{cls}">{display}</div>
    </div>"""


# ── Example Paragraphs ────────────────────────────────────────────────────────
EXAMPLES = [
    "Interstellar (2014)",
    "The Dark Knight (2008)",
    "Parasite (2019)",
    "Inception (2010)",
]

EXAMPLE_TEXTS = {
    "Interstellar (2014)": "Interstellar is a visually stunning science fiction epic directed by Christopher Nolan. Released in 2014, the film stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, and Michael Caine. The story revolves around a group of astronauts who travel through a wormhole near Saturn in search of a new home for humanity as Earth faces environmental collapse. The movie was widely appreciated for its emotional depth, scientific accuracy, and Hans Zimmer's powerful soundtrack. It holds a rating of 8.6 on IMDb and is often considered one of the greatest sci-fi films of the 21st century.",
    "The Dark Knight (2008)": "The Dark Knight is a 2008 superhero film directed by Christopher Nolan and starring Christian Bale as Bruce Wayne/Batman alongside Heath Ledger as the iconic Joker. Also starring Aaron Eckhart, Maggie Gyllenhaal, and Gary Oldman, the film is set in Gotham City and follows Batman's battle against the anarchic Joker. It received critical acclaim for Ledger's performance and won two Academy Awards. The film holds a 9.0 rating on IMDb and grossed over $1 billion worldwide.",
    "Parasite (2019)": "Parasite is a 2019 South Korean black comedy thriller written and directed by Bong Joon-ho. The film stars Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik, and Park So-dam. The story follows the Kim family, who are all unemployed, and their cunning plan to infiltrate and exploit the wealthy Park family. Parasite made history by becoming the first non-English language film to win the Academy Award for Best Picture. It holds a 8.5 rating on IMDb and is praised for its sharp social commentary on class inequality.",
    "Inception (2010)": "Inception is a 2010 science fiction action film written and directed by Christopher Nolan. The film stars Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy, Ken Watanabe, and Cillian Murphy. DiCaprio plays Dom Cobb, a thief who specializes in entering people's dreams to steal secrets. The movie features groundbreaking visual effects, particularly the famous rotating hallway scene. It holds an 8.8 rating on IMDb and grossed over $836 million worldwide. Hans Zimmer composed the iconic score.",
}


# ── Session State ─────────────────────────────────────────────────────────────
if "paragraph" not in st.session_state:
    st.session_state.paragraph = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "extractions_done" not in st.session_state:
    st.session_state.extractions_done = 0


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">🎬 &nbsp; AI-Powered · Cinema Intelligence</div>
    <h1 class="hero-title">Cine<span>Extract</span></h1>
    <p class="hero-sub">Drop any movie paragraph. Instantly extract cast, plot, themes, ratings & more.</p>
    <div class="divider-gold"></div>
</div>
""", unsafe_allow_html=True)


# ── Main Layout ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📝 &nbsp; Movie Paragraph</div>', unsafe_allow_html=True)

    paragraph = st.text_area(
        label="paragraph_input",
        label_visibility="collapsed",
        placeholder="Paste any movie description here — from Wikipedia, IMDb, reviews, or your own writing…",
        value=st.session_state.paragraph,
        height=220,
        key="para_input"
    )

    # Example selector
    st.markdown("""
    <div class="example-section">
        <div class="example-label">⚡ Quick Examples</div>
    </div>""", unsafe_allow_html=True)

    ex_cols = st.columns(len(EXAMPLES))
    for i, ex in enumerate(EXAMPLES):
        with ex_cols[i]:
            if st.button(ex.split(" (")[0], key=f"ex_{i}", use_container_width=True):
                st.session_state.paragraph = EXAMPLE_TEXTS[ex]
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    extract_btn = st.button("✦ &nbsp; Extract Intelligence", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── How It Works ──
    st.markdown("""
    <div style="margin-top: 1.5rem; padding: 1.2rem 1.5rem;
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 6px;">
        <div class="section-label" style="margin-bottom:0.8rem">⚙ &nbsp; How It Works</div>
        <div style="display:flex; flex-direction:column; gap:0.6rem;">
            <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                <span style="color:var(--gold); font-size:0.8rem; margin-top:2px;">①</span>
                <span style="color:var(--text-muted); font-size:0.88rem; line-height:1.5">Paste any movie paragraph from any source</span>
            </div>
            <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                <span style="color:var(--gold); font-size:0.8rem; margin-top:2px;">②</span>
                <span style="color:var(--text-muted); font-size:0.88rem; line-height:1.5">Mistral AI extracts structured intelligence via LangChain</span>
            </div>
            <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                <span style="color:var(--gold); font-size:0.8rem; margin-top:2px;">③</span>
                <span style="color:var(--text-muted); font-size:0.88rem; line-height:1.5">Get cast, plot, themes, ratings & a sharp summary instantly</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Right Column: Results ─────────────────────────────────────────────────────
with right_col:
    use_paragraph = st.session_state.paragraph if st.session_state.paragraph else paragraph

    if extract_btn:
        if not use_paragraph.strip():
            st.error("⚠ Please enter a movie paragraph before extracting.")
        else:
            with st.spinner("Analysing with Mistral AI…"):
                try:
                    chain = get_chain()
                    start = time.time()
                    response = chain.invoke({"paragraph": use_paragraph})
                    elapsed = round(time.time() - start, 1)
                    st.session_state.result = {
                        "raw": response.content,
                        "parsed": parse_response(response.content),
                        "elapsed": elapsed,
                    }
                    st.session_state.extractions_done += 1
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    if st.session_state.result:
        data = st.session_state.result["parsed"]
        elapsed = st.session_state.result["elapsed"]
        title = data.get("Movie Title") or "Movie"

        st.markdown(f"""
        <div class="result-wrapper">
            <div class="result-header">
                <span style="font-size:1.2rem">🎞</span>
                <span class="result-header-title">{title}</span>
                <span style="margin-left:auto; font-size:0.72rem; color:var(--text-muted);">
                    ⚡ {elapsed}s
                </span>
            </div>
            <div class="result-body">
        """, unsafe_allow_html=True)

        # Grid fields
        grid_fields = [
            "Movie Title", "Release Year", "Genre", "Director",
            "Main Cast", "Setting/Location", "Ratings", "Themes"
        ]
        grid_html = '<div class="info-grid">'
        for f in grid_fields:
            grid_html += render_field(f, data.get(f))
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)

        # Plot
        plot_val = data.get("Plot")
        if plot_val:
            st.markdown(f"""
            <div style="margin-bottom:1rem">
                <div class="field-label" style="margin-bottom:0.4rem">🎭 &nbsp; Plot</div>
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(212,175,55,0.12);
                            border-radius:4px; padding:1rem; font-size:0.93rem;
                            line-height:1.75; color:var(--cream);">{plot_val}</div>
            </div>""", unsafe_allow_html=True)

        # Notable Features
        notable = data.get("Notable Features")
        if notable:
            st.markdown(f"""
            <div style="margin-bottom:1rem">
                <div class="field-label" style="margin-bottom:0.4rem">✨ &nbsp; Notable Features</div>
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(212,175,55,0.12);
                            border-radius:4px; padding:1rem; font-size:0.93rem;
                            line-height:1.75; color:var(--cream);">{notable}</div>
            </div>""", unsafe_allow_html=True)

        # Summary
        summary = data.get("Short Summary")
        if summary:
            st.markdown(f"""
            <div class="summary-block">
                <div class="summary-label">✦ &nbsp; Short Summary</div>
                <div class="summary-text">"{summary}"</div>
            </div>""", unsafe_allow_html=True)

        # Stats Bar
        filled = sum(1 for v in data.values() if v and v.upper() != "NULL")
        total = len(data)
        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">{filled}</div>
                <div class="stat-label">Fields found</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total fields</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{round(filled/total*100)}%</div>
                <div class="stat-label">Completeness</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{elapsed}s</div>
                <div class="stat-label">Extract time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Raw toggle
        with st.expander("🔍 Raw Model Output"):
            st.code(st.session_state.result["raw"], language=None)

    else:
        st.markdown("""
        <div style="height:380px; display:flex; flex-direction:column;
                    align-items:center; justify-content:center;
                    border: 1px dashed rgba(212,175,55,0.2);
                    border-radius:6px;
                    background: rgba(212,175,55,0.02);">
            <div style="font-size:3rem; margin-bottom:1rem; opacity:0.4">🎬</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.2rem;
                        color:var(--text-muted); font-style:italic; text-align:center;
                        max-width:260px; line-height:1.7;">
                Your extracted results will appear here
            </div>
            <div style="margin-top:0.8rem; font-size:0.75rem;
                        color:rgba(138,127,114,0.5); letter-spacing:0.1em;">
                PASTE A PARAGRAPH & CLICK EXTRACT
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <span>LangChain · Mistral AI · Streamlit</span> &nbsp;·&nbsp; CineExtract © 2025
</div>
""", unsafe_allow_html=True)