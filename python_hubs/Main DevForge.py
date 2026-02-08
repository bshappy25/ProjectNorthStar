# """
DevForge - Developer Productivity Hub

Your personal Streamlit development assistant

Features:

- Quick Start Templates
- Code Library (copy/paste components)
- ABC Branch Generator (architecture decisions)
- Ms. Piluso Science Page (NGSS + New Visions)

Connected to BSChapp v2 ecosystem
We are L.E.A.D.
# """

import streamlit as st
from datetime import date

# =====================
# SESSION STATE SETUP
# =====================

if "dev_theme" not in st.session_state:
    st.session_state["dev_theme"] = "science"  # Default to science for Ms. Piluso

if "signature" not in st.session_state:
    st.session_state["signature"] = ""  # Pull from BSChapp if available

# =====================
# THEME (GLASSY)
# =====================

NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"
NEUTRAL_MUTED = "#1f1f1f"
NEUTRAL_ACCENT = "#5a5a5a"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.74)"
SCI_ACCENT = "#14B8A6"
SCI_ACCENT2 = "#2F5BEA"

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="DevForge - Developer Hub",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Determine theme
is_science = st.session_state["dev_theme"] == "science"
BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_ACCENT if is_science else NEUTRAL_ACCENT

# =====================
# GLASSY UI STYLES
# =====================

st.markdown(
    f"""
<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --border: {BORDER};
  --text: {TEXT};
  --muted: {MUTED};
  --accent: {ACCENT};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

.block-container {{
  padding-top: 1.2rem;
}}

section[data-testid="stSidebar"],
div[data-testid="stExpander"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextArea"] > div,
div[data-testid="stSelectbox"] > div,
.stCodeBlock {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}}

button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-weight: 700 !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
  font-weight: 900 !important;
}}

.dev-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 15px 0;
}}
</style>
""",
    unsafe_allow_html=True,
)

# =====================
# TICKER
# =====================

st.markdown(
    "<div class='ticker'>DEVFORGE • Developer Productivity Hub • We are L.E.A.D. 🔧</div>",
    unsafe_allow_html=True,
)

# =====================
# SIDEBAR
# =====================

with st.sidebar:
    st.title("🔧 DevForge")
    st.caption("Developer Productivity Hub")

    st.divider()

    theme_choice = st.radio(
        "Dev Theme",
        ["Science", "Neutral"],
        index=0 if is_science else 1,
        horizontal=True,
    )

    if theme_choice.lower() != st.session_state["dev_theme"]:
        st.session_state["dev_theme"] = theme_choice.lower()
        st.rerun()

    st.divider()

    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")

    if st.session_state.get("signature"):
        st.write(f"**Dev:** {st.session_state['signature']}")
    else:
        st.caption("No signature (set in BSChapp)")

    st.divider()

    st.subheader("🗺️ Pages")
    st.markdown(
        """
- **Home** - Quick start  
- **Ms. Piluso Science** - NGSS tools  
- **Code Library** - Copy/paste  
- **ABC Generator** - Architecture
"""
    )

    st.divider()
    st.caption("Connected to Project North Star")

# =====================
# MAIN CONTENT
# =====================

st.title("🔧 DevForge - Developer Hub")
st.markdown("### Your Streamlit Development Assistant")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='dev-card'>🔬 Science Tools</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='dev-card'>📚 Code Library</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='dev-card'>⚡ ABC Framework</div>", unsafe_allow_html=True)

st.divider()

with st.expander("⚙️ Dev Settings", expanded=False):
    st.json(
        {
            "theme": st.session_state["dev_theme"],
            "signature": st.session_state.get("signature", "Not set"),
            "date": date.today().isoformat(),
            "ecosystem": "Project North Star",
        }
    )

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)