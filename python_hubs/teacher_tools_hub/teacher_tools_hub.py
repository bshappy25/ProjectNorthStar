"""
TEACHER TOOLS HUB

Futuristic TV interface for HTML teaching tools

- Glassy sidebar for tool management
- Copy/paste HTML -> instant publish
- Transparent screen overlay (TV effect)
- We are L.E.A.D.
"""

import streamlit as st
import os
from pathlib import Path

# =====================
# CONFIG
# =====================

TOOLS_DIR = "teacher_tools"
Path(TOOLS_DIR).mkdir(exist_ok=True)

# Theme: Glassy UI (matches BSChapp v2)

NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"
NEUTRAL_MUTED = "#1f1f1f"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.74)"
SCI_ACCENT = "#14B8A6"
# =====================

# SESSION STATE

# =====================

if “theme_mode” not in st.session_state:
st.session_state[“theme_mode”] = “neutral”
if “current_tool” not in st.session_state:
st.session_state[“current_tool”] = None
if “html_input” not in st.session_state:
st.session_state[“html_input”] = “”

# =====================

# HELPERS

# =====================

def list_tools():
“”“Get all .html files in teacher_tools/”””
tools = []
for f in Path(TOOLS_DIR).glob(”*.html”):
tools.append(f.stem)
return sorted(tools)

def save_tool(name, html_code):
“”“Save HTML code as .html file”””
filename = f”{name}.html”
filepath = Path(TOOLS_DIR) / filename
with open(filepath, ‘w’, encoding=‘utf-8’) as f:
f.write(html_code)
return filepath

def load_tool(name):
“”“Load HTML code from file”””
filepath = Path(TOOLS_DIR) / f”{name}.html”
if filepath.exists():
with open(filepath, ‘r’, encoding=‘utf-8’) as f:
return f.read()
return “”

# =====================

# PAGE CONFIG

# =====================

st.set_page_config(
page_title=“Teacher Tools Hub”,
page_icon=“📺”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

# =====================

# THEME SELECTION

# =====================

is_science = st.session_state[“theme_mode”] == “science”

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED

# =====================

# GLASSY UI + TV OVERLAY

# =====================

st.markdown(f”””

<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --border: {BORDER};
  --text: {TEXT};
  --muted: {MUTED};
}}

/* Background */
div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

/* GLASSY TEXTURE - Sidebar */
section[data-testid="stSidebar"] {{
  background-color: var(--card) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-right: 1px solid var(--border) !important;
}}

/* All text */
h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

/* Inputs - GLASSY */
input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

textarea {{
  font-family: 'Courier New', monospace !important;
  font-size: 13px !important;
}}

/* Buttons - GLASSY */
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
  border: 2px solid var(--border) !important;
  background: linear-gradient(135deg, rgba(20,184,166,0.2), rgba(20,184,166,0.1)) !important;
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

/* FUTURISTIC TV SCREEN OVERLAY */
.tv-frame {{
  position: relative;
  width: 100%;
  height: calc(100vh - 120px);
  border: 3px solid var(--border);
  border-radius: 20px;
  overflow: hidden;
  background: rgba(0,0,0,0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 
    0 0 40px rgba(20,184,166,0.2),
    inset 0 0 60px rgba(20,184,166,0.05);
}}

/* Scan line effect */
.tv-frame::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.03) 2px,
    rgba(255,255,255,0.03) 4px
  );
  pointer-events: none;
  z-index: 2;
  animation: scanlines 8s linear infinite;
}}

@keyframes scanlines {{
  0% {{ transform: translateY(0); }}
  100% {{ transform: translateY(4px); }}
}}

/* Glow effect */
.tv-frame::after {{
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(20,184,166,0.1) 0%,
    transparent 50%
  );
  pointer-events: none;
  z-index: 1;
  animation: glow 4s ease-in-out infinite alternate;
}}

@keyframes glow {{
  0% {{ opacity: 0.3; }}
  100% {{ opacity: 0.6; }}
}}

/* Screen content */
.tv-screen {{
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 3;
}}
</style>

“””, unsafe_allow_html=True)

# =====================

# TICKER

# =====================

st.markdown(
“<div class='ticker'>TEACHER TOOLS HUB • We are L.E.A.D. • Futuristic Interface 📺</div>”,
unsafe_allow_html=True
)

# =====================

# SIDEBAR

# =====================

with st.sidebar:
st.title(“📺 Teacher Tools”)
st.caption(“Futuristic Interface • HTML Tool Manager”)

```
st.divider()

# Theme toggle
theme_choice = st.radio(
    "Theme",
    ["Neutral", "Science"],
    index=0 if st.session_state["theme_mode"] == "neutral" else 1,
    horizontal=True
)
if theme_choice.lower() != st.session_state["theme_mode"]:
    st.session_state["theme_mode"] = theme_choice.lower()
    st.rerun()

st.divider()

# Tool List
st.subheader("📂 Your Tools")
tools = list_tools()

if not tools:
    st.info("No tools yet. Add one below! 👇")
else:
    for tool in tools:
        is_active = st.session_state["current_tool"] == tool
        button_type = "primary" if is_active else "secondary"
        
        if st.button(
            f"{'📺 ' if is_active else '📄 '}{tool}",
            key=f"tool_{tool}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state["current_tool"] = tool
            st.rerun()

st.divider()

# Add New Tool Section
with st.expander("➕ Add New Tool", expanded=False):
    st.caption("Copy HTML code → Paste → Save → View")
    
    tool_name = st.text_input(
        "Tool Name",
        placeholder="e.g., Evidence Capture v1",
        key="new_tool_name"
    )
    
    html_code = st.text_area(
        "HTML Code",
        placeholder="Paste your complete HTML code here...",
        height=300,
        key="html_input"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state["html_input"] = ""
            st.rerun()
    
    with col2:
        if st.button("💾 Save", use_container_width=True, type="primary"):
            if not tool_name:
                st.error("Enter a tool name!")
            elif not html_code.strip():
                st.error("Paste HTML code!")
            else:
                # Save tool
                save_tool(tool_name, html_code)
                st.session_state["current_tool"] = tool_name
                st.session_state["html_input"] = ""
                st.success(f"✅ {tool_name} saved!")
                st.rerun()

st.divider()
st.caption("📺 Futuristic TV Interface")
st.caption("Simple as Google Sites")
```

# =====================

# MAIN WINDOW

# =====================

if st.session_state[“current_tool”]:
tool_name = st.session_state[“current_tool”]

```
# Header
st.markdown(f"""
<div style='text-align:center; margin-bottom:20px;'>
    <h1 style='font-size:2.5rem; margin:0;'>📺 {tool_name}</h1>
    <p style='color:var(--muted); margin-top:5px;'>Viewing in Futuristic TV Mode</p>
</div>
""", unsafe_allow_html=True)

# TV Frame with tool
st.markdown("<div class='tv-frame'><div class='tv-screen'>", unsafe_allow_html=True)

# Load and display tool
tool_html = load_tool(tool_name)
if tool_html:
    st.components.v1.html(tool_html, height=800, scrolling=True)
else:
    st.error(f"Tool file not found: {tool_name}.html")

st.markdown("</div></div>", unsafe_allow_html=True)
```

else:
# Welcome screen
st.markdown(”””
<div style='text-align:center; padding:60px 20px;'>
<h1 style='font-size:3.5rem; margin-bottom:20px;'>📺 Teacher Tools Hub</h1>
<p style='font-size:1.3rem; color:var(--muted); margin-bottom:40px;'>
Futuristic Interface for HTML Teaching Tools
</p>
<div style='background:var(--card); border:1px solid var(--border); border-radius:20px; 
padding:40px; max-width:600px; margin:0 auto; backdrop-filter:blur(10px);'>
<h3 style='margin-top:0;'>🚀 Getting Started</h3>
<ol style='text-align:left; line-height:2;'>
<li><strong>Click “➕ Add New Tool”</strong> in the sidebar</li>
<li><strong>Paste your complete HTML code</strong></li>
<li><strong>Click “💾 Save”</strong> to publish</li>
<li><strong>View instantly</strong> in futuristic TV mode</li>
</ol>
<p style='margin-top:30px; color:var(--muted); font-size:0.95rem;'>
✨ <strong>Simple as Google Sites</strong> • Copy → Paste → Publish → View<br>
📺 <strong>Futuristic TV overlay</strong> • Scan lines + glow effects<br>
🎨 <strong>Glassy UI</strong> • Matches BSChapp v2 aesthetic
</p>
</div>
</div>
“””, unsafe_allow_html=True)

# Bottom padding for ticker

st.markdown(”<div style='height:60px'></div>”, unsafe_allow_html=True)