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

import io
import textwrap
from datetime import date

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# =====================
# SESSION STATE SETUP
# =====================

if "dev_theme" not in st.session_state:
    st.session_state["dev_theme"] = "science"  # Default to science for Ms. Piluso

if "signature" not in st.session_state:
    st.session_state["signature"] = ""  # Pull from BSChapp if available

# NEW: NAV STATE (Primary vs Testers)
if "devforge_panel" not in st.session_state:
    st.session_state["devforge_panel"] = "Home (Primary)"

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
# TESTER HELPERS (SCI-BLOCK)
# =====================

def _load_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates = ["DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    else:
        candidates = ["DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def _safe(x: str) -> str:
    x = (x or "").strip()
    return x if x else "N/a"

def generate_sci_block_jpeg(header_title: str, lines: list[tuple[str, bool]]) -> io.BytesIO:
    width = 1200
    body_bg = "#D9F2E6"
    header_bg = "#0B3D2E"
    body_text = "#1B4D3E"
    header_text = "#E9FFF5"
    pad_x = 60
    pad_y = 48
    header_h = 120

    font_body = _load_font(34, bold=False)
    font_bold = _load_font(36, bold=True)
    font_header = _load_font(44, bold=True)

    wrapper = textwrap.TextWrapper(width=52, break_long_words=False)

    wrapped: list[tuple[str, bool]] = []
    for txt, is_bold in lines:
        if txt.strip() == "":
            wrapped.append(("", is_bold))
            continue
        for wline in wrapper.wrap(txt):
            wrapped.append((wline, is_bold))

    line_h = 46
    body_h = pad_y * 2 + line_h * max(1, len(wrapped))
    height = header_h + body_h

    img = Image.new("RGB", (width, height), body_bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, header_h], fill=header_bg)
    draw.text((pad_x, 30), header_title, fill=header_text, font=font_header)

    y = header_h + pad_y
    for txt, is_bold in wrapped:
        draw.text((pad_x, y), txt, fill=body_text, font=(font_bold if is_bold else font_body))
        y += line_h

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf

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

    # ===== DIVISION: Primary vs Tester Apps =====
    st.subheader("🧭 Navigation")

    st.caption("Primary Apps")
    primary_choice = st.radio(
        "Primary",
        ["Home (Primary)"],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Tester Apps (Sandbox)")
    tester_choice = st.radio(
        "Testers",
        ["Tester 1 — Simple Form", "Tester 2 — SCI-BLOCK", "Tester 3 — Scratchpad"],
        index=0 if st.session_state["devforge_panel"].startswith("Tester 1") else
              1 if st.session_state["devforge_panel"].startswith("Tester 2") else
              2 if st.session_state["devforge_panel"].startswith("Tester 3") else 0,
        label_visibility="collapsed",
    )

    # Decide active panel
    use_testers = st.checkbox("Use Tester Apps", value=st.session_state["devforge_panel"].startswith("Tester"))

    if use_testers:
        st.session_state["devforge_panel"] = tester_choice
    else:
        st.session_state["devforge_panel"] = primary_choice

    st.divider()
    st.caption("Connected to Project North Star")

# =====================
# MAIN ROUTER
# =====================

panel = st.session_state["devforge_panel"]

# =====================
# PRIMARY: HOME
# =====================

if panel == "Home (Primary)":
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

    st.markdown(
        """
<div class='dev-card' style='text-align:center; background: linear-gradient(135deg, rgba(20,184,166,0.1), rgba(47,91,234,0.1));'>
<h3>🎯 Ready to Build?</h3>
<p style='font-size:1.1rem;'>
Use the sidebar. Toggle "Use Tester Apps" when you want sandbox panels.
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

# =====================
# TESTER 1 — SIMPLE FORM
# =====================

elif panel == "Tester 1 — Simple Form":
    st.title("🧪 Tester 1 — Simple Form")
    st.caption("Quick plug-and-play form block")

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name")
        grade = st.selectbox("Grade", ["K", "1", "2", "3", "4", "5"])
    with c2:
        chosen_date = st.date_input("Date", value=date.today())
        subject = st.selectbox("Subject", ["Math", "Science", "ELA"])

    st.markdown("#### Output")
    st.code(
        {
            "name": name,
            "grade": grade,
            "date": chosen_date.isoformat(),
            "subject": subject,
        }
    )

# =====================
# TESTER 2 — SCI-BLOCK
# =====================

elif panel == "Tester 2 — SCI-BLOCK":
    st.title("🧪 Tester 2 — SCI-BLOCK")
    st.caption("Generate the exact SCI-BLOCK.jpeg artifact from typed content")

    std = st.text_input("Standard", value="MS-ESS1-1")
    d = st.date_input("Date", value=date.today())
    header = f"SCI-BLOCK • {d.isoformat()} • {std}"

    st.subheader("5E + Details")
    engage = st.text_area("Engage", value="Students will watch a video", height=90)
    explore = st.text_area("Explore", value="Students will gather data on freezing temps", height=90)
    explain = st.text_area("Explain", value="Students will call and response", height=90)
    elaborate = st.text_area("Elaborate", value="Students will make a brochure on water", height=90)
    evaluate = st.text_area("Evaluate", value="Students will look at other examples of brochures and rate them", height=90)

    materials = st.text_area("Materials", value="laptops and brochure materials", height=80)
    notes = st.text_area("Notes", value="some students need help with inputs", height=80)
    accom = st.text_area("Accommodations", value="N/a", height=80)

    lines = [
        ("5E Framework", True),
        (f"Engage: {_safe(engage)}", False),
        (f"Explore: {_safe(explore)}", False),
        (f"Explain: {_safe(explain)}", False),
        (f"Elaborate: {_safe(elaborate)}", False),
        (f"Evaluate: {_safe(evaluate)}", False),
        ("", False),
        ("Materials", True),
        (_safe(materials), False),
        ("", False),
        ("Notes", True),
        (_safe(notes), False),
        ("", False),
        ("Accommodations", True),
        (_safe(accom), False),
    ]

    buf = generate_sci_block_jpeg(header, lines)

    st.download_button(
        "📸 Download SCI-BLOCK.jpeg",
        data=buf,
        file_name="SCI-BLOCK.jpeg",
        mime="image/jpeg",
        use_container_width=True,
        type="primary",
    )

# =====================
# TESTER 3 — SCRATCHPAD
# =====================

elif panel == "Tester 3 — Scratchpad":
    st.title("🧪 Tester 3 — Scratchpad")
    st.caption("Paste anything here while prototyping. Nothing is persisted yet.")

    scratch = st.text_area("Scratch", height=260, placeholder="Paste code, notes, JSON, ideas...")
    st.markdown("#### Echo")
    st.code(scratch if scratch.strip() else "—")

# Bottom padding
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)