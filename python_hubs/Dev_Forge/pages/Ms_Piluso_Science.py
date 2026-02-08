"""
Ms. Piluso Science - Phase 2 Department Tool

NGSS-aligned lesson planning with New Visions curriculum integration
5E framework auto-builder
Science Mode glassy UI

Quick export to BSChapp v2 format
"""

import streamlit as st
from datetime import date

from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# =====================
# NGSS STANDARDS DATABASE
# =====================

NGSS_STANDARDS = {
    "MS-ESS1": {
        "title": "Earth’s Place in the Universe",
        "standards": {
            "MS-ESS1-1": "Develop and use a model of the Earth-sun-moon system",
            "MS-ESS1-2": "Develop and use a model to describe the role of gravity",
            "MS-ESS1-3": "Analyze and interpret data to determine scale properties of objects in the solar system",
            "MS-ESS1-4": "Construct a scientific explanation based on evidence from rock strata",
        },
    },
    "MS-ESS2": {
        "title": "Earth’s Systems",
        "standards": {
            "MS-ESS2-1": "Develop a model to describe the cycling of Earth’s materials",
            "MS-ESS2-2": "Construct an explanation based on evidence for how geoscience processes have changed Earth’s surface",
            "MS-ESS2-3": "Analyze and interpret data on the distribution of fossils and rocks",
            "MS-ESS2-4": "Develop a model to describe the cycling of water through Earth’s systems",
            "MS-ESS2-5": "Collect data to provide evidence for how the motions and complex interactions of air masses result in changes in weather",
            "MS-ESS2-6": "Develop and use a model to describe how unequal heating and rotation of the Earth cause patterns of atmospheric and oceanic circulation",
        },
    },
    "MS-ESS3": {
        "title": "Earth and Human Activity",
        "standards": {
            "MS-ESS3-1": "Construct a scientific explanation based on evidence for how the uneven distributions of Earth’s mineral, energy, and groundwater resources are the result of past and current geoscience processes",
            "MS-ESS3-2": "Analyze and interpret data on natural hazards to forecast future catastrophic events",
            "MS-ESS3-3": "Apply scientific principles to design a method for monitoring and minimizing a human impact on the environment",
            "MS-ESS3-4": "Construct an argument supported by evidence for how increases in human population and per-capita consumption of natural resources impact Earth’s systems",
            "MS-ESS3-5": "Ask questions to clarify evidence of the factors that have caused the rise in global temperatures over the past century",
        },
    },
}

FIVE_E_PHASES = {
    "Engage": "Hook students’ interest and activate prior knowledge",
    "Explore": "Students actively investigate and gather data",
    "Explain": "Students explain their understanding and teacher clarifies",
    "Elaborate": "Students apply concepts in new contexts",
    "Evaluate": "Assess student understanding and learning",
}

NEW_VISIONS_UNITS = {
    "Earth Science": [
        "Unit 1: Plate Tectonics",
        "Unit 2: Rocks & Minerals",
        "Unit 3: Earth’s History",
        "Unit 4: Weather & Climate",
        "Unit 5: Water Systems",
        "Unit 6: Space Systems",
    ],
    "Life Science": [
        "Unit 1: Cells & Systems",
        "Unit 2: Genetics",
        "Unit 3: Evolution",
        "Unit 4: Ecosystems",
    ],
    "Physical Science": [
        "Unit 1: Matter",
        "Unit 2: Energy",
        "Unit 3: Forces & Motion",
        "Unit 4: Waves",
    ],
}

# =====================
# SESSION STATE
# =====================

if "piluso_lesson" not in st.session_state:
    st.session_state["piluso_lesson"] = {
        "ngss": "",
        "nv_unit": "",
        "engage": "",
        "explore": "",
        "explain": "",
        "elaborate": "",
        "evaluate": "",
        "objective": "",
        "materials": "",
        "notes": "",
        "accommodations": "",
    }

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="Ms. Piluso Science Tools",
    page_icon="🔬",
    layout="wide",
)

# =====================
# THEME (SCIENCE MODE)
# =====================

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.74)"
SCI_ACCENT = "#14B8A6"

st.markdown(
    f"""
<style>
:root {{
  --bg: {SCI_BG};
  --card: {SCI_CARD};
  --border: {SCI_BORDER};
  --text: {SCI_TEXT};
  --muted: {SCI_MUTED};
  --accent: {SCI_ACCENT};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

div[data-testid="stExpander"],
input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  color: var(--text) !important;
  font-weight: 700 !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
}}

.sci-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 15px 0;
  backdrop-filter: blur(10px);
}}

.badge {{
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--accent);
  background: var(--card);
  color: var(--accent) !important;
  font-weight: 900;
  font-size: 0.85rem;
  margin: 5px;
}}
</style>
""",
    unsafe_allow_html=True,
)

# =====================
# IMAGE EXPORT HELPERS
# =====================

def _load_font(size: int, bold: bool = False):
    """
    Tries to load a sane default font. Falls back to PIL default if unavailable.
    Bold uses DejaVuSans-Bold if present.
    """
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


def generate_sci_block_jpeg(
    title: str,
    lines: list[tuple[str, bool]],
    *,
    width: int = 1200,
    body_bg: str = "#D9F2E6",     # light green
    header_bg: str = "#0B3D2E",   # darker green
    body_text: str = "#1B4D3E",   # hunter green
    header_text: str = "#E9FFF5", # very light mint
) -> io.BytesIO:
    """
    Creates a JPEG with a dark header band + body content.
    `lines` is a list of (text, is_bold).
    """
    pad_x = 60
    pad_y = 48
    header_h = 120

    font_body = _load_font(34, bold=False)
    font_bold = _load_font(36, bold=True)
    font_header = _load_font(44, bold=True)

    wrap_width_chars = 52  # tuned for 1200px with 34-36px font
    wrapper = textwrap.TextWrapper(width=wrap_width_chars, break_long_words=False, replace_whitespace=False)

    # Wrap lines
    wrapped: list[tuple[str, bool]] = []
    for txt, is_bold in lines:
        if txt.strip() == "":
            wrapped.append(("", is_bold))
            continue
        for wline in wrapper.wrap(txt):
            wrapped.append((wline, is_bold))

    line_h = 46  # stable spacing
    body_h = pad_y * 2 + line_h * max(1, len(wrapped))
    height = header_h + body_h

    img = Image.new("RGB", (width, height), body_bg)
    draw = ImageDraw.Draw(img)

    # Header band
    draw.rectangle([0, 0, width, header_h], fill=header_bg)
    draw.text((pad_x, 30), title, fill=header_text, font=font_header)

    # Body text
    y = header_h + pad_y
    for txt, is_bold in wrapped:
        font = font_bold if is_bold else font_body
        draw.text((pad_x, y), txt, fill=body_text, font=font)
        y += line_h

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf


def safe_val(x: str) -> str:
    x = (x or "").strip()
    return x if x else "N/a"


# =====================
# HEADER
# =====================

st.title("🔬 Ms. Piluso Science - Phase 2")
st.markdown("### NGSS + New Visions Curriculum Builder")

st.markdown(
    """
<div class='sci-card'>
<span class='badge'>[NGSS]</span>
<span class='badge'>[5E]</span>
<span class='badge'>[New Visions]</span>
<p style='margin-top:15px; color:var(--muted);'>
Quick lesson planning for department-wide use. Export directly to BSChapp v2 format.
</p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# =====================
# NGSS STANDARD SELECTOR
# =====================

st.markdown("### 📋 Step 1: Select NGSS Standard")

col1, col2 = st.columns([1, 2])

with col1:
    domain = st.selectbox(
        "NGSS Domain",
        options=list(NGSS_STANDARDS.keys()),
        format_func=lambda x: f"{x}: {NGSS_STANDARDS[x]['title']}",
    )

with col2:
    selected_standard = ""
    if domain:
        standards_dict = NGSS_STANDARDS[domain]["standards"]
        selected_standard = st.selectbox(
            "Specific Standard",
            options=list(standards_dict.keys()),
            format_func=lambda x: f"{x}: {standards_dict[x]}",
        )
        st.session_state["piluso_lesson"]["ngss"] = selected_standard

st.divider()

# =====================
# NEW VISIONS UNIT
# =====================

st.markdown("### 📚 Step 2: New Visions Curriculum (Optional)")

nv_branch = st.selectbox(
    "New Visions Branch",
    options=["None"] + list(NEW_VISIONS_UNITS.keys()),
)

if nv_branch != "None":
    nv_unit = st.selectbox("Unit", options=NEW_VISIONS_UNITS[nv_branch])
    st.session_state["piluso_lesson"]["nv_unit"] = nv_unit
    st.info(f"**Placeholder:** Integration with {nv_unit} resources coming soon!")

st.divider()

# =====================
# 5E FRAMEWORK BUILDER
# =====================

st.markdown("### 🔄 Step 3: Build 5E Lesson")
st.caption("Fill out each phase of the 5E instructional model:")

for phase, description in FIVE_E_PHASES.items():
    with st.expander(f"**{phase}** - {description}", expanded=False):
        phase_key = phase.lower()
        content = st.text_area(
            f"{phase} Activities",
            value=st.session_state["piluso_lesson"].get(phase_key, ""),
            height=120,
            placeholder=f"Describe {phase.lower()} activities…",
            key=f"5e_{phase_key}",
        )
        st.session_state["piluso_lesson"][phase_key] = content

st.divider()

# =====================
# ADDITIONAL DETAILS
# =====================

st.markdown("### ✏️ Step 4: Lesson Details")

col1, col2 = st.columns(2)

with col1:
    objective = st.text_area(
        "Student Objective",
        value=st.session_state["piluso_lesson"].get("objective", ""),
        placeholder="Students will be able to…",
        height=100,
    )
    st.session_state["piluso_lesson"]["objective"] = objective

with col2:
    materials = st.text_area(
        "Materials Needed",
        value=st.session_state["piluso_lesson"].get("materials", ""),
        placeholder="List materials, tech, handouts…",
        height=100,
    )
    st.session_state["piluso_lesson"]["materials"] = materials

notes = st.text_area(
    "Teacher Notes / Differentiation",
    value=st.session_state["piluso_lesson"].get("notes", ""),
    placeholder="Notes, modifications, extensions…",
    height=100,
)
st.session_state["piluso_lesson"]["notes"] = notes

accom = st.text_area(
    "Accommodations / Modifications",
    value=st.session_state["piluso_lesson"].get("accommodations", ""),
    placeholder="IEP/504 supports: visuals, sentence starters, extended time, breaks, reduced choices...",
    height=100,
)
st.session_state["piluso_lesson"]["accommodations"] = accom

st.divider()

# =====================
# PREVIEW
# =====================

st.markdown("### 👁️ Preview")

lesson = st.session_state["piluso_lesson"]

preview_text = f"""
**NGSS Standard:** {lesson.get('ngss', '—')}
**New Visions Unit:** {lesson.get('nv_unit', 'N/A')}

**Student Objective:**
{lesson.get('objective', '—')}

**5E Framework:**
**Engage:** {lesson.get('engage', '—')}
**Explore:** {lesson.get('explore', '—')}
**Explain:** {lesson.get('explain', '—')}
**Elaborate:** {lesson.get('elaborate', '—')}
**Evaluate:** {lesson.get('evaluate', '—')}

**Materials:**
{lesson.get('materials', '—')}

**Notes:**
{lesson.get('notes', '—')}

**Accommodations:**
{lesson.get('accommodations', '—')}
"""

st.text_area("Lesson Preview", value=preview_text, height=420, disabled=True)

st.divider()

# =====================
# ✅ SCI-BLOCK JPEG EXPORT (INSERTED HERE)
# =====================

st.markdown("### 🖼️ Export SCI-BLOCK (JPEG)")

ngss_pick = safe_val(lesson.get("ngss"))
today_str = date.today().isoformat()
header_title = f"SCI-BLOCK • {today_str} • {ngss_pick}"

# lines: (text, is_bold)
img_lines: list[tuple[str, bool]] = [
    ("5E Framework", True),
    (f"Engage: {safe_val(lesson.get('engage'))}", False),
    (f"Explore: {safe_val(lesson.get('explore'))}", False),
    (f"Explain: {safe_val(lesson.get('explain'))}", False),
    (f"Elaborate: {safe_val(lesson.get('elaborate'))}", False),
    (f"Evaluate: {safe_val(lesson.get('evaluate'))}", False),
    ("", False),
    ("Materials", True),
    (safe_val(lesson.get("materials")), False),
    ("", False),
    ("Notes", True),
    (safe_val(lesson.get("notes")), False),
    ("", False),
    ("Accommodations", True),
    (safe_val(lesson.get("accommodations")), False),
]

jpeg_buf = generate_sci_block_jpeg(header_title, img_lines)

st.download_button(
    label="📸 Download SCI-BLOCK.jpeg",
    data=jpeg_buf,
    file_name="SCI-BLOCK.jpeg",
    mime="image/jpeg",
    use_container_width=True,
)

st.caption("Tip: Download, then drop the image into chat as your exemplar block.")

st.divider()

# =====================
# EXPORT OPTIONS
# =====================

st.markdown("### 🚀 Export")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.info("Copy the preview text above manually")

with col2:
    if st.button("📄 Export to BSChapp", use_container_width=True, type="primary"):
        st.success("✅ Ready to paste into BSChapp v2 ‘Lesson Plan’ artifact!")
        st.info("Navigate to BSChapp → Select ‘Lesson Plan’ → Paste content")

with col3:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state["piluso_lesson"] = {
            "ngss": "",
            "nv_unit": "",
            "engage": "",
            "explore": "",
            "explain": "",
            "elaborate": "",
            "evaluate": "",
            "objective": "",
            "materials": "",
            "notes": "",
            "accommodations": "",
        }
        st.rerun()

st.divider()

# =====================
# QUICK TIPS
# =====================

with st.expander("💡 Quick Tips for Ms. Piluso", expanded=False):
    st.markdown(
        """
**5E Framework quick cues**
- Engage: hook / phenomenon
- Explore: hands-on investigation
- Explain: student talk + teacher clarify
- Elaborate: apply in new context
- Evaluate: checks for understanding

**Export workflow**
1) Build lesson here
2) Export to BSChapp
3) Paste into Lesson Plan artifact
4) Add signature
5) Download PDF
"""
    )

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)