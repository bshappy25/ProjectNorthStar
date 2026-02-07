# “””
AI-Storyboard Portal Page for BSChapp v2

- Matches BSChapp v2 glassy aesthetic
- Adapts to Science/Neutral theme
- Passes teacher signature as username to HTML app
- Clean integration with Project North Star
  “””

import streamlit as st

# =====================

# THEME MATCHING

# =====================

# Match parent app theme

is_science = (st.session_state.get(“subject_mode”, “Select…”) == “Science”)

# UNIVERSAL NEUTRAL - GLASSY

NEUTRAL_BG = “#f2f2f2”  
NEUTRAL_CARD = “rgba(230, 230, 230, 0.7)”
NEUTRAL_BORDER = “rgba(207, 207, 207, 0.5)”
NEUTRAL_TEXT = “#000000”  
NEUTRAL_MUTED = “#1f1f1f”
NEUTRAL_ACCENT = “#5a5a5a”

# SCIENCE MODE - GLASSY

SCI_BG = “#061B15”
SCI_CARD = “rgba(255,255,255,0.08)”
SCI_BORDER = “rgba(120,255,220,0.3)”
SCI_TEXT = “rgba(255,255,255,0.92)”
SCI_MUTED = “rgba(255,255,255,0.74)”
SCI_ACCENT = “#14B8A6”

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_ACCENT if is_science else NEUTRAL_ACCENT

# =====================

# PAGE CONFIG

# =====================

st.set_page_config(
page_title=“AI-Storyboard Portal”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

# =====================

# GLASSY UI STYLES

# =====================

st.markdown(f”””

<style>
:root {{
  --bg:{BG};
  --card:{CARD};
  --border:{BORDER};
  --text:{TEXT};
  --muted:{MUTED};
  --accent:{ACCENT};
}}

/* Background */
div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

/* GLASSY TEXTURE */
.card,
div[data-testid="stExpander"],
button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

/* Text colors */
h1, h2, h3, h4, h5, h6,
p, span, label, div {{
  color: var(--text) !important;
}}

/* Portal frame - GLASSY */
.portal-frame {{
  background-color: var(--card);
  border: 2px solid var(--border);
  border-radius: 20px;
  padding: 20px;
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}}

.portal-header {{
  text-align: center;
  padding: 20px 0;
}}

.portal-title {{
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--text);
  margin-bottom: 10px;
}}

.portal-subtitle {{
  font-size: 1.1rem;
  color: var(--muted);
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

/* IFrame container - GLASSY border */
.iframe-container {{
  border: 3px solid var(--border);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  margin: 20px 0;
}}
</style>

“””, unsafe_allow_html=True)

# =====================

# TICKER

# =====================

st.markdown(
“<div class='ticker'>BSCHAPP v2 - We are L.E.A.D.</div>”,
unsafe_allow_html=True
)

# =====================

# PORTAL HEADER

# =====================

st.markdown(”””

<div class='portal-header'>
    <div class='portal-title'>🎬 AI-Storyboard Portal</div>
    <div class='portal-subtitle'>Project North Star • Interactive Story Creation</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =====================

# USER CONTEXT

# =====================

# Get teacher signature from main app session state

teacher_signature = st.session_state.get(“signature”, “”).strip()

if not teacher_signature:
st.warning(“💡 **Tip:** Set your signature on the main page to personalize the AI-Storyboard experience!”)
teacher_signature = “Teacher”  # Default fallback

# Display current user context

with st.expander(“🔧 Portal Settings”, expanded=False):
st.markdown(f”**Username for AI-Storyboard:** `{teacher_signature}`”)
st.caption(“This is pulled from your signature on the main BSChapp page.”)

```
theme_mode = "Science Mode (Blue-Green)" if is_science else "Neutral Mode (Gray)"
st.markdown(f"**Current Theme:** {theme_mode}")
```

st.divider()

# =====================

# EMBED AI-STORYBOARD

# =====================

# Build URL with username parameter

app_url = f”/html_apps/ai_storyboard.html?username={teacher_signature}”

# Info box

st.markdown(”””

<div class='portal-frame'>
<strong>📌 About AI-Storyboard:</strong><br>
Create interactive visual stories with AI assistance. Your signature passes as your username for a personalized experience.
</div>
""", unsafe_allow_html=True)

st.markdown(”<div style='height:20px'></div>”, unsafe_allow_html=True)

# Embed the HTML app

st.markdown(”<div class='iframe-container'>”, unsafe_allow_html=True)
st.components.v1.iframe(
src=app_url,
height=1000,
scrolling=True
)
st.markdown(”</div>”, unsafe_allow_html=True)

# =====================

# FOOTER PADDING

# =====================

st.markdown(”<div style='height:80px'></div>”, unsafe_allow_html=True)