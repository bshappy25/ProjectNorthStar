# “””
Code Library - DevForge

Copy/paste ready code snippets for rapid development

- Glassy UI components
- PDF generators
- Session state patterns
- Form builders
  “””

import streamlit as st

# =====================

# PAGE CONFIG

# =====================

st.set_page_config(
page_title=“Code Library”,
page_icon=“📚”,
layout=“wide”
)

# =====================

# THEME

# =====================

is_science = st.session_state.get(“dev_theme”, “science”) == “science”

SCI_BG = “#061B15”
SCI_CARD = “rgba(255,255,255,0.08)”
SCI_BORDER = “rgba(120,255,220,0.3)”
SCI_TEXT = “rgba(255,255,255,0.92)”

NEUTRAL_BG = “#f2f2f2”
NEUTRAL_CARD = “rgba(230, 230, 230, 0.7)”
NEUTRAL_BORDER = “rgba(207, 207, 207, 0.5)”
NEUTRAL_TEXT = “#000000”

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

st.markdown(f”””

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
  font-size: 1.1rem;
  margin-bottom: 10px;
}}
</style>

“””, unsafe_allow_html=True)

# =====================

# HEADER

# =====================

st.title(“📚 Code Library”)
st.markdown(”### Copy/Paste Ready Components”)

st.caption(“Click ‘Copy Code’ below each snippet”)

st.divider()

# =====================

# GLASSY UI COMPONENTS

# =====================

st.markdown(”## 🎨 Glassy UI Components”)

# Component 1: Basic Glassy Card

with st.expander(“🔲 Glassy Card Container”, expanded=False):
st.markdown(”**Use case:** Content sections, feature cards”)

```
code_glassy_card = '''
```

# GLASSY CARD CSS

st.markdown(”””

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

“””, unsafe_allow_html=True)

# USAGE

st.markdown(”””

<div class='glassy-card'>
<h3>Your Title</h3>
<p>Your content here</p>
</div>
""", unsafe_allow_html=True)
'''

```
st.code(code_glassy_card, language="python")
st.caption("✅ Copy this entire block")
```

# Component 2: Theme Variables

with st.expander(“🎨 Theme Variable System”, expanded=False):
st.markdown(”**Use case:** Consistent theming across app”)

```
code_theme = '''
```

# THEME SETUP

NEUTRAL_BG = “#f2f2f2”
NEUTRAL_CARD = “rgba(230, 230, 230, 0.7)”
NEUTRAL_BORDER = “rgba(207, 207, 207, 0.5)”
NEUTRAL_TEXT = “#000000”

SCI_BG = “#061B15”
SCI_CARD = “rgba(255,255,255,0.08)”
SCI_BORDER = “rgba(120,255,220,0.3)”
SCI_TEXT = “rgba(255,255,255,0.92)”
SCI_ACCENT = “#14B8A6”

# APPLY THEME

is_science = st.session_state.get(“theme_mode”) == “science”
BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

# INJECT CSS

st.markdown(f”””

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
  backdrop-filter: blur(10px) !important;
}}
</style>

“””, unsafe_allow_html=True)
‘’’

```
st.code(code_theme, language="python")
```

# Component 3: Ticker

with st.expander(“📊 Bottom Ticker Bar”, expanded=False):
st.markdown(”**Use case:** Persistent footer with branding”)

```
code_ticker = '''
```

# TICKER CSS + HTML

st.markdown(”””

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
  z-index: 999;
}
</style>

<div class='ticker'>YOUR MESSAGE • We are L.E.A.D. 🌟</div>
""", unsafe_allow_html=True)

# Add padding at bottom so ticker doesn’t cover content

st.markdown(”<div style='height:60px'></div>”, unsafe_allow_html=True)
‘’’

```
st.code(code_ticker, language="python")
```

st.divider()

# =====================

# SESSION STATE PATTERNS

# =====================

st.markdown(”## 💾 Session State Patterns”)

with st.expander(“🔄 Initialize Session State”, expanded=False):
st.markdown(”**Use case:** Set up persistent data”)

```
code_session = '''
```

# INITIALIZE SESSION STATE

if “my_data” not in st.session_state:
st.session_state[“my_data”] = {
“name”: “”,
“count”: 0,
“items”: []
}

# ACCESS

current_name = st.session_state[“my_data”][“name”]

# UPDATE

st.session_state[“my_data”][“count”] += 1

# SHARE ACROSS PAGES

# All pages in multipage app can access st.session_state

‘’’

```
st.code(code_session, language="python")
```

with st.expander(“🔗 Cross-App Data Sharing”, expanded=False):
st.markdown(”**Use case:** Share signature between BSChapp and DevForge”)

```
code_cross = '''
```

# IN BSCHAPP (sets signature)

signature = st.text_input(“Signature”)
st.session_state[“signature”] = signature

# IN DEVFORGE (reads signature)

teacher_name = st.session_state.get(“signature”, “Unknown”)
st.write(f”Welcome, {teacher_name}!”)

# FALLBACK PATTERN

value = st.session_state.get(“key”, “default_value”)
‘’’

```
st.code(code_cross, language="python")
```

st.divider()

# =====================

# PDF GENERATION

# =====================

st.markdown(”## 📄 PDF Generation (ReportLab)”)

with st.expander(“📝 Basic PDF with ReportLab”, expanded=False):
st.markdown(”**Use case:** Generate downloadable PDFs”)

```
code_pdf = '''
```

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_pdf(title, content):
“”“Generate simple PDF”””
buf = io.BytesIO()
c = canvas.Canvas(buf, pagesize=letter)
w, h = letter

```
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
```

# USAGE IN STREAMLIT

pdf_bytes = generate_pdf(“My Title”, “Line 1\nLine 2\nLine 3”)

st.download_button(
“Download PDF”,
data=pdf_bytes,
file_name=“document.pdf”,
mime=“application/pdf”
)
‘’’

```
st.code(code_pdf, language="python")
```

st.divider()

# =====================

# FORM PATTERNS

# =====================

st.markdown(”## 📝 Form Patterns”)

with st.expander(“🔘 Multi-Column Form Layout”, expanded=False):
st.markdown(”**Use case:** Compact forms”)

```
code_form = '''
```

# TWO-COLUMN LAYOUT

col1, col2 = st.columns(2)

with col1:
name = st.text_input(“Name”)
grade = st.selectbox(“Grade”, [“K”, “1”, “2”, “3”, “4”, “5”])

with col2:
date = st.date_input(“Date”)
subject = st.selectbox(“Subject”, [“Math”, “Science”, “ELA”])

# THREE-COLUMN LAYOUT

col1, col2, col3 = st.columns(3)

with col1:
st.button(“Option A”)
with col2:
st.button(“Option B”)
with col3:
st.button(“Option C”)
‘’’

```
st.code(code_form, language="python")
```

with st.expander(“✅ Form with Validation”, expanded=False):
st.markdown(”**Use case:** Required fields, error handling”)

```
code_validation = '''
```

# FORM WITH VALIDATION

with st.form(“my_form”):
name = st.text_input(“Name (required)”)
email = st.text_input(“Email (required)”)
notes = st.text_area(“Notes (optional)”)

```
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
        # Process data...
```

‘’’

```
st.code(code_validation, language="python")
```

st.divider()

# =====================

# UTILITY SNIPPETS

# =====================

st.markdown(”## 🔧 Utility Functions”)

with st.expander(“📅 Date Helpers”, expanded=False):
code_date = ‘’’
from datetime import date, timedelta

# TODAY

today = date.today()
today_str = today.isoformat()  # “2024-02-07”

# FORMATTED

formatted = today.strftime(”%B %d, %Y”)  # “February 07, 2024”

# CALCULATE DATES

tomorrow = today + timedelta(days=1)
week_ago = today - timedelta(weeks=1)

# IN STREAMLIT

st.write(f”Today: {today_str}”)
date_input = st.date_input(“Select Date”, value=today)
‘’’

```
st.code(code_date, language="python")
```

with st.expander(“💾 File I/O Helpers”, expanded=False):
code_file = ‘’’
from pathlib import Path
import json

# READ TEXT FILE

def load_text(filepath):
return Path(filepath).read_text(encoding=‘utf-8’)

# WRITE TEXT FILE

def save_text(filepath, content):
Path(filepath).write_text(content, encoding=‘utf-8’)

# JSON SAVE/LOAD

def save_json(filepath, data):
with open(filepath, ‘w’) as f:
json.dump(data, f, indent=2)

def load_json(filepath):
with open(filepath, ‘r’) as f:
return json.load(f)

# CREATE DIRECTORY

Path(“my_folder”).mkdir(exist_ok=True)

# LIST FILES

html_files = list(Path(“folder”).glob(”*.html”))
‘’’

```
st.code(code_file, language="python")
```

st.divider()

# =====================

# QUICK REFERENCE

# =====================

st.markdown(”## 📖 Quick Reference”)

with st.expander(“🎨 Color Palette (BSChapp v2)”, expanded=False):
st.markdown(”””
**Neutral Theme:**
- Background: `#f2f2f2`
- Card: `rgba(230, 230, 230, 0.7)`
- Border: `rgba(207, 207, 207, 0.5)`
- Text: `#000000`

```
**Science Theme:**
- Background: `#061B15`
- Card: `rgba(255,255,255,0.08)`
- Border: `rgba(120,255,220,0.3)`
- Text: `rgba(255,255,255,0.92)`
- Accent: `#14B8A6` (teal)
- Accent2: `#2F5BEA` (blue - for signatures)
""")
```

with st.expander(“⌨️ Common Streamlit Widgets”, expanded=False):
st.markdown(”””
```python
# Text input
name = st.text_input(“Label”, placeholder=“hint”)

```
# Text area
notes = st.text_area("Label", height=200)

# Selectbox
choice = st.selectbox("Pick one", ["A", "B", "C"])

# Multiselect
choices = st.multiselect("Pick many", ["A", "B", "C"])

# Radio
option = st.radio("Choose", ["X", "Y", "Z"])

# Checkbox
agree = st.checkbox("I agree")

# Button
if st.button("Click me"):
    st.write("Clicked!")

# File uploader
file = st.file_uploader("Upload", type=["pdf", "png"])

# Download button
st.download_button("Download", data=content, file_name="file.txt")
```
""")
```

st.markdown(”<div style='height:60px'></div>”, unsafe_allow_html=True)