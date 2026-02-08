
"""
DevForge - Developer Productivity Hub

Your personal Streamlit development assistant

Features:
- Quick Start Templates
- Code Library (copy/paste components)
- ABC Branch Generator (architecture decisions)
- Ms. Piluso Science Page (NGSS + New Visions)

Connected to BSChapp v2 ecosystem
We are L.E.A.D.
"""

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
    initial_sidebar_state="expanded",
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

/* Background */
div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

.block-container {{
  padding-top: 1.2rem;
}}

/* GLASSY TEXTURE */
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

/* Text colors */
h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

/* Inputs */
input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

/* Buttons */
button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  color: var(--text) !important;
  font-weight: 700 !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
  font-weight: 900 !important;
}}

/* Code blocks */
.stCodeBlock {{
  font-family: 'Courier New', monospace !important;
  font-size: 13px !important;
}}

/* Cards */
.dev-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 15px 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.dev-card h3 {{
  margin-top: 0;
  color: var(--accent) !important;
  font-weight: 900;
}}

/* Badge */
.badge {{
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-weight: 900;
  background: var(--card);
  backdrop-filter: blur(10px);
  font-size: 0.85rem;
  margin: 5px;
}}

.badge-accent {{
  border-color: var(--accent);
  color: var(--accent) !important;
}}

/* Ticker */
.ticker {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--card);
  border-top: 1px solid var(--border);
  padding: 8px 20px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--muted);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 999;
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

    # Theme toggle
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

    # Quick stats
    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")

    if st.session_state.get("signature"):
        st.write(f"**Dev:** {st.session_state['signature']}")
    else:
        st.caption("No signature (set in BSChapp)")

    st.divider()

    # Navigation helper
    st.subheader("🗺️ Pages")
    st.caption("Use sidebar to navigate:")
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

st.markdown(
    """
<div class='dev-card'>
<h3>🎯 Quick Start</h3>
<p>DevForge helps you build Streamlit apps faster with:</p>
<ul>
<li><strong>Ms. Piluso Science Page</strong> - NGSS + New Visions curriculum tools</li>
<li><strong>Code Library</strong> - Copy/paste glassy UI components</li>
<li><strong>ABC Generator</strong> - Make architecture decisions quickly</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
<div class='dev-card'>
<h3>🔬 Science Tools</h3>
<p>NGSS-aligned lesson planning</p>
<p>New Visions integration</p>
<p>5E framework builder</p>
<br>
<p><strong>→ See “Ms. Piluso Science” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class='dev-card'>
<h3>📚 Code Library</h3>
<p>Glassy UI components</p>
<p>PDF generators</p>
<p>Session state patterns</p>
<br>
<p><strong>→ See “Code Library” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
<div class='dev-card'>
<h3>⚡ ABC Framework</h3>
<p><strong>A</strong> - Architecture</p>
<p><strong>B</strong> - Build pattern</p>
<p><strong>C</strong> - Code style</p>
<br>
<p><strong>→ See “ABC Generator” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

st.divider()

# Quick reference
st.markdown("### 🚀 Quick Reference")

with st.expander("📋 Common Tasks", expanded=False):
    st.markdown(
        """
**Create new science lesson:**
1. Go to “Ms. Piluso Science” page
2. Select NGSS standard
3. Fill 5E framework
4. Export to BSChapp

**Copy glassy UI component:**
1. Go to "Code Library" page
2. Browse components
3. Click "Copy Code"
4. Paste into your app

**Make architecture decision:**
1. Go to "ABC Generator" page
2. Answer A, B, C questions
3. Get recommended structure
4. Generate starter code
"""
    )

with st.expander("🔗 Connected Apps", expanded=False):
    st.markdown(
        """
**DevForge connects to:**
- **BSChapp v2** - Shares signature, theme
- **Teacher Tools Hub** - HTML app testing
- **Project North Star** - Ecosystem data

**Session state shared:**
- `st.session_state["signature"]` - Developer name
- `st.session_state["dev_theme"]` - UI theme
- Future: shared student rosters, standards library
"""
    )

with st.expander("⚙️ Dev Settings", expanded=False):
    st.markdown("**Current Configuration:**")
    st.json(
        {
            "theme": st.session_state["dev_theme"],
            "signature": st.session_state.get("signature", "Not set"),
            "date": date.today().isoformat(),
            "ecosystem": "Project North Star",
        }
    )

st.divider()

# Call to action
st.markdown(
    """
<div class='dev-card' style='text-align:center; background: linear-gradient(135deg, rgba(20,184,166,0.1), rgba(47,91,234,0.1));'>
<h3>🎯 Ready to Build?</h3>
<p style='font-size:1.1rem;'>
Navigate to a page in the sidebar to start developing!
</p>
<div style='margin-top:20px;'>
<span class='badge badge-accent'>NGSS Tools</span>
<span class='badge badge-accent'>Code Snippets</span>
<span class='badge badge-accent'>Architecture Help</span>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# Bottom padding
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
