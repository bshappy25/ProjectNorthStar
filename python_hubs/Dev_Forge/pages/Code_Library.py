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

st.set_page_config(
    page_title="Code Library",
    page_icon="📚",
    layout="wide",
)

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

.snippet-title {{
  font-weight: 900;
  font-size: 1.05rem;
  margin-bottom: 10px;
}}
</style>
""",
    unsafe_allow_html=True,
)

# =====================
# SNIPPETS (ALL AS STRINGS)
# =====================

code_glassy_card = r'''import streamlit as st

# GLASSY CARD CSS
st.markdown("""
<style>
.glassy-card {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(120,255,220,0.3);
  border-radius: 16px;
  padding: 20px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# USAGE
st.markdown("""
<div class='glassy-card'>
  <h3>Your Title</h3>
  <p>Your content here</p>
</div>
""", unsafe_allow_html=True)
'''

code_theme = r'''import streamlit as st

# THEME SETUP
NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_ACCENT = "#14B8A6"

# APPLY THEME
is_science = st.session_state.get("dev_theme", "science") == "science"
BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

# INJECT CSS
st.markdown(f"""
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

input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
}}
</style>
""", unsafe_allow_html=True)
'''

code_ticker = r'''import streamlit as st

# TICKER CSS + HTML
st.markdown("""
<style>
.ticker {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(255,255,255,0.08);
  border-top: 1px solid rgba(120,255,220,0.3);
  padding: 8px 20px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 700;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 999;
}
</style>
<div class='ticker'>YOUR MESSAGE • We are L.E.A.D. 🌟</div>
""", unsafe_allow_html=True)

# Bottom padding so the ticker doesn't cover content
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
'''

code_session = r'''import streamlit as st

# INITIALIZE SESSION STATE
if "my_data" not in st.session_state:
    st.session_state["my_data"] = {
        "name": "",
        "count": 0,
        "items": []
    }

# ACCESS
current_name = st.session_state["my_data"]["name"]

# UPDATE
st.session_state["my_data"]["count"] += 1

# NOTE:
# All pages in a multipage app can access st.session_state
'''

code_cross = r'''import streamlit as st

# IN BSCHAPP (sets signature)
signature = st.text_input("Signature")
st.session_state["signature"] = signature

# IN DEVFORGE (reads signature)
teacher_name = st.session_state.get("signature", "Unknown")
st.write(f"Welcome, {teacher_name}!")

# FALLBACK PATTERN
value = st.session_state.get("key", "default_value")
'''

code_pdf = r'''import io
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_pdf(title: str, content: str) -> bytes:
    """Generate simple PDF bytes."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75 * inch, h - 0.75 * inch, title)

    # Content
    c.setFont("Helvetica", 12)
    y = h - 1.2 * inch
    for line in content.split("\\n"):
        c.drawString(0.75 * inch, y, line)
        y -= 0.2 * inch

    c.save()
    return buf.getvalue()

pdf_bytes = generate_pdf("My Title", "Line 1\\nLine 2\\nLine 3")

st.download_button(
    "Download PDF",
    data=pdf_bytes,
    file_name="document.pdf",
    mime="application/pdf",
)
'''

code_form = r'''import streamlit as st
from datetime import date

# TWO-COLUMN LAYOUT
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    grade = st.selectbox("Grade", ["K", "1", "2", "3", "4", "5"])

with col2:
    chosen_date = st.date_input("Date", value=date.today())
    subject = st.selectbox("Subject", ["Math", "Science", "ELA"])

# THREE-COLUMN LAYOUT
col1, col2, col3 = st.columns(3)

with col1:
    st.button("Option A")
with col2:
    st.button("Option B")
with col3:
    st.button("Option C")
'''

code_validation = r'''import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name (required)")
    email = st.text_input("Email (required)")
    notes = st.text_area("Notes (optional)")
    submitted = st.form_submit_button("Submit")

if submitted:
    errors = []

    if not name:
        errors.append("Name is required")
    if not email:
        errors.append("Email is required")
    elif "@" not in email:
        errors.append("Invalid email format")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("Form submitted successfully!")
'''

code_date = r'''from datetime import date, timedelta
import streamlit as st

today = date.today()
today_str = today.isoformat()
formatted = today.strftime("%B %d, %Y")

tomorrow = today + timedelta(days=1)
week_ago = today - timedelta(weeks=1)

st.write(f"Today: {today_str}")
st.write(f"Formatted: {formatted}")
st.write(f"Tomorrow: {tomorrow.isoformat()}")
st.write(f"Week ago: {week_ago.isoformat()}")
'''

code_file = r'''from pathlib import Path
import json

def load_text(filepath: str) -> str:
    return Path(filepath).read_text(encoding="utf-8")

def save_text(filepath: str, content: str) -> None:
    Path(filepath).write_text(content, encoding="utf-8")

def save_json(filepath: str, data) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

Path("my_folder").mkdir(exist_ok=True)
html_files = list(Path("folder").glob("*.html"))
'''

# =====================
# HEADER UI
# =====================

st.title("📚 Code Library")
st.markdown("### Copy/Paste Ready Components")
st.caption("Snippets are safe strings — paste them into your app and edit as needed.")
st.divider()

# =====================
# GLASSY UI COMPONENTS
# =====================

st.markdown("## 🎨 Glassy UI Components")

with st.expander("🔲 Glassy Card Container", expanded=False):
    st.markdown("**Use case:** Content sections, feature cards")
    st.code(code_glassy_card, language="python")

with st.expander("🎨 Theme Variable System", expanded=False):
    st.markdown("**Use case:** Consistent theming across app")
    st.code(code_theme, language="python")

with st.expander("📊 Bottom Ticker Bar", expanded=False):
    st.markdown("**Use case:** Persistent footer with branding")
    st.code(code_ticker, language="python")

st.divider()

# =====================
# SESSION STATE PATTERNS
# =====================

st.markdown("## 💾 Session State Patterns")

with st.expander("🔄 Initialize Session State", expanded=False):
    st.markdown("**Use case:** Set up persistent data")
    st.code(code_session, language="python")

with st.expander("🔗 Cross-App Data Sharing", expanded=False):
    st.markdown("**Use case:** Share signature between BSChapp and DevForge")
    st.code(code_cross, language="python")

st.divider()

# =====================
# PDF GENERATION
# =====================

st.markdown("## 📄 PDF Generation (ReportLab)")

with st.expander("📝 Basic PDF with ReportLab", expanded=False):
    st.markdown("**Use case:** Generate downloadable PDFs")
    st.code(code_pdf, language="python")

st.divider()

# =====================
# FORM PATTERNS
# =====================

st.markdown("## 📝 Form Patterns")

with st.expander("🔘 Multi-Column Form Layout", expanded=False):
    st.markdown("**Use case:** Compact forms")
    st.code(code_form, language="python")

with st.expander("✅ Form with Validation", expanded=False):
    st.markdown("**Use case:** Required fields, error handling")
    st.code(code_validation, language="python")

st.divider()

# =====================
# UTILITY SNIPPETS
# =====================

st.markdown("## 🔧 Utility Functions")

with st.expander("📅 Date Helpers", expanded=False):
    st.code(code_date, language="python")

with st.expander("💾 File I/O Helpers", expanded=False):
    st.code(code_file, language="python")

st.divider()

# =====================
# QUICK REFERENCE
# =====================

st.markdown("## 📖 Quick Reference")

with st.expander("🎨 Color Palette (BSChapp v2)", expanded=False):
    st.markdown(
        """
**Neutral Theme**
- Background: `#f2f2f2`
- Card: `rgba(230, 230, 230, 0.7)`
- Border: `rgba(207, 207, 207, 0.5)`
- Text: `#000000`

**Science Theme**
- Background: `#061B15`
- Card: `rgba(255,255,255,0.08)`
- Border: `rgba(120,255,220,0.3)`
- Text: `rgba(255,255,255,0.92)`
- Accent: `#14B8A6`
- Accent2: `#2F5BEA`
"""
    )

with st.expander("⌨️ Common Streamlit Widgets", expanded=False):
    st.markdown(
        """
```python
name = st.text_input("Label", placeholder="hint")
notes = st.text_area("Label", height=200)
choice = st.selectbox("Pick one", ["A", "B", "C"])
choices = st.multiselect("Pick many", ["A", "B", "C"])
option = st.radio("Choose", ["X", "Y", "Z"])
agree = st.checkbox("I agree")

if st.button("Click me"):
    st.write("Clicked!")

file = st.file_uploader("Upload", type=["pdf", "png"])

st.download_button("Download", data="hello", file_name="file.txt")

“””
)

st.markdown(””, unsafe_allow_html=True

