# -*- coding: utf-8 -*-
"""
Code Library - DevForge

Copy/paste ready code snippets for rapid development

- Glassy UI components
- PDF generators
- Session state patterns
- Form builders
"""

import streamlit as st

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(page_title="Code Library", page_icon="📚", layout="wide")

# =====================
# THEME
# =====================

is_science = st.session_state.get("dev_theme", "science") == "science"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"

NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

st.markdown(
    f"""
<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --border: {BORDER};
  --text: {TEXT};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

.code-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 15px 0;
  backdrop-filter: blur(10px);
}}
</style>
""",
    unsafe_allow_html=True,
)

# =====================
# SNIPPETS (SAFE STRINGS)
# =====================

code_glassy_card = (
    "import streamlit as st\n\n"
    "# GLASSY CARD CSS\n"
    "st.markdown(\n"
    '    "<style>\\n"\n'
    '    ".glassy-card{background:rgba(255,255,255,0.08);border:1px solid rgba(120,255,220,0.3);'
    "border-radius:16px;padding:20px;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);}\\n"
    '    "</style>",\n'
    "    unsafe_allow_html=True\n"
    ")\n\n"
    "# USAGE\n"
    "st.markdown(\n"
    '    "<div class=\\"glassy-card\\"><h3>Your Title</h3><p>Your content here</p></div>",\n'
    "    unsafe_allow_html=True\n"
    ")\n"
)

code_theme = (
    "import streamlit as st\n\n"
    "NEUTRAL_BG = \"#f2f2f2\"\n"
    "NEUTRAL_CARD = \"rgba(230, 230, 230, 0.7)\"\n"
    "NEUTRAL_BORDER = \"rgba(207, 207, 207, 0.5)\"\n"
    "NEUTRAL_TEXT = \"#000000\"\n\n"
    "SCI_BG = \"#061B15\"\n"
    "SCI_CARD = \"rgba(255,255,255,0.08)\"\n"
    "SCI_BORDER = \"rgba(120,255,220,0.3)\"\n"
    "SCI_TEXT = \"rgba(255,255,255,0.92)\"\n"
    "SCI_ACCENT = \"#14B8A6\"\n\n"
    "is_science = st.session_state.get(\"dev_theme\", \"science\") == \"science\"\n"
    "BG = SCI_BG if is_science else NEUTRAL_BG\n"
    "CARD = SCI_CARD if is_science else NEUTRAL_CARD\n"
    "BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER\n"
    "TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT\n\n"
    "st.markdown(\n"
    "    f\"\"\"\n"
    "    <style>\n"
    "    :root {{ --bg:{BG}; --card:{CARD}; --border:{BORDER}; --text:{TEXT}; }}\n"
    "    div[data-testid='stAppViewContainer']{{ background-color:var(--bg)!important; }}\n"
    "    input,textarea,select{{ background-color:var(--card)!important; color:var(--text)!important; border:1px solid var(--border)!important; }}\n"
    "    </style>\n"
    "    \"\"\",\n"
    "    unsafe_allow_html=True\n"
    ")\n"
)

code_ticker = (
    "import streamlit as st\n\n"
    "st.markdown(\n"
    "    \"\"\"\n"
    "    <style>\n"
    "    .ticker{position:fixed;bottom:0;left:0;right:0;background-color:rgba(255,255,255,0.08);"
    "border-top:1px solid rgba(120,255,220,0.3);padding:8px 20px;text-align:center;font-size:0.85rem;"
    "font-weight:700;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);z-index:999;}\n"
    "    </style>\n"
    "    <div class='ticker'>YOUR MESSAGE • We are L.E.A.D. 🌟</div>\n"
    "    \"\"\",\n"
    "    unsafe_allow_html=True\n"
    ")\n\n"
    "st.markdown(\"<div style='height:60px'></div>\", unsafe_allow_html=True)\n"
)

code_session = (
    "import streamlit as st\n\n"
    "if \"my_data\" not in st.session_state:\n"
    "    st.session_state[\"my_data\"] = {\"name\":\"\", \"count\":0, \"items\":[]}\n\n"
    "current_name = st.session_state[\"my_data\"][\"name\"]\n"
    "st.session_state[\"my_data\"][\"count\"] += 1\n"
)

code_pdf = (
    "import io\n"
    "import streamlit as st\n"
    "from reportlab.pdfgen import canvas\n"
    "from reportlab.lib.pagesizes import letter\n"
    "from reportlab.lib.units import inch\n\n"
    "def generate_pdf(title, content):\n"
    "    buf = io.BytesIO()\n"
    "    c = canvas.Canvas(buf, pagesize=letter)\n"
    "    w, h = letter\n"
    "    c.setFont('Helvetica-Bold', 18)\n"
    "    c.drawString(0.75*inch, h-0.75*inch, title)\n"
    "    c.setFont('Helvetica', 12)\n"
    "    y = h - 1.2*inch\n"
    "    for line in content.split('\\\\n'):\n"
    "        c.drawString(0.75*inch, y, line)\n"
    "        y -= 0.2*inch\n"
    "    c.save()\n"
    "    return buf.getvalue()\n\n"
    "pdf_bytes = generate_pdf('My Title', 'Line 1\\\\nLine 2\\\\nLine 3')\n"
    "st.download_button('Download PDF', data=pdf_bytes, file_name='document.pdf', mime='application/pdf')\n"
)

code_form = (
    "import streamlit as st\n"
    "from datetime import date\n\n"
    "col1, col2 = st.columns(2)\n"
    "with col1:\n"
    "    name = st.text_input('Name')\n"
    "    grade = st.selectbox('Grade', ['K','1','2','3','4','5'])\n"
    "with col2:\n"
    "    chosen_date = st.date_input('Date', value=date.today())\n"
    "    subject = st.selectbox('Subject', ['Math','Science','ELA'])\n"
)

# =====================
# UI
# =====================

st.title("📚 Code Library")
st.markdown("### Copy/Paste Ready Components")
st.caption("These snippets are stored as safe strings and shown with st.code() so this page always parses.")
st.divider()

st.markdown("## 🎨 Glassy UI Components")
with st.expander("🔲 Glassy Card Container", expanded=False):
    st.code(code_glassy_card, language="python")

with st.expander("🎨 Theme Variable System", expanded=False):
    st.code(code_theme, language="python")

with st.expander("📊 Bottom Ticker Bar", expanded=False):
    st.code(code_ticker, language="python")

st.divider()

st.markdown("## 💾 Session State Patterns")
with st.expander("🔄 Initialize Session State", expanded=False):
    st.code(code_session, language="python")

st.divider()

st.markdown("## 📄 PDF Generation (ReportLab)")
with st.expander("📝 Basic PDF with ReportLab", expanded=False):
    st.code(code_pdf, language="python")

st.divider()

st.markdown("## 📝 Form Patterns")
with st.expander("🔘 Multi-Column Form Layout", expanded=False):
    st.code(code_form, language="python")

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)