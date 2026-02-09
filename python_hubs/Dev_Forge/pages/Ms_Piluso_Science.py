# pages/Ms_Piluso_Science.py
from __future__ import annotations

import io
import textwrap
from datetime import date
from pathlib import Path
from typing import Dict, Tuple, List

import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# PAGE CONFIG (top of file, once)
# ============================================================
st.set_page_config(
    page_title="Ms. Piluso Science Tools",
    page_icon="🔬",
    layout="wide",
)

# ============================================================
# NGSS STANDARDS DATABASE
# ============================================================
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

SENTENCE_STARTERS = {
    "Engage": [
        "Today we’re investigating…",
        "What do you notice? What do you wonder?",
        "Based on the phenomenon, I predict… because…",
    ],
    "Explore": [
        "We tested… by…",
        "The data shows…",
        "A pattern I observed was…",
    ],
    "Explain": [
        "My claim is…",
        "My evidence is…",
        "My reasoning is…",
    ],
    "Elaborate": [
        "This concept also applies to…",
        "A real-world example is…",
        "If we change ___, then ___ because…",
    ],
    "Evaluate": [
        "I can demonstrate understanding by…",
        "One misconception I had was… now I think…",
        "A strong answer would include…",
    ],
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

# ============================================================
# SESSION STATE
# ============================================================
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

lesson = st.session_state["piluso_lesson"]


# ============================================================
# IMAGE EXPORT HELPERS
# ============================================================
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


def safe_val(x: str) -> str:
    x = (x or "").strip()
    return x if x else "N/a"


def generate_sci_block_jpeg(
    title: str,
    lines: list[tuple[str, bool]],
    *,
    width: int = 1200,
    body_bg: str = "#EEF2F7",     # neutral light
    header_bg: str = "#0F2A3D",   # deep blue
    body_text: str = "#111827",   # near black
    header_text: str = "#F9FAFB", # near white
) -> io.BytesIO:
    pad_x = 60
    pad_y = 48
    header_h = 120

    font_body = _load_font(34, bold=False)
    font_bold = _load_font(36, bold=True)
    font_header = _load_font(44, bold=True)

    wrap_width_chars = 52
    wrapper = textwrap.TextWrapper(width=wrap_width_chars, break_long_words=False, replace_whitespace=False)

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
    draw.text((pad_x, 30), title, fill=header_text, font=font_header)

    y = header_h + pad_y
    for txt, is_bold in wrapped:
        font = font_bold if is_bold else font_body
        draw.text((pad_x, y), txt, fill=body_text, font=font)
        y += line_h

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return buf


# ============================================================
# HEADER (NO GLOBAL CSS INJECTION)
# ============================================================
st.title("🔬 Ms. Piluso Science")
st.markdown("### NGSS + New Visions Curriculum Builder")
st.video("https://www.youtube.com/watch?v=9l2MVsYVxlE")
st.divider()

# ============================================================
# STEP 1: NGSS STANDARD
# ============================================================
st.markdown("### 📋 Step 1: Select NGSS Standard")

col1, col2 = st.columns([1, 2], gap="large")
with col1:
    domain = st.selectbox(
        "NGSS Domain",
        options=list(NGSS_STANDARDS.keys()),
        format_func=lambda x: f"{x}: {NGSS_STANDARDS[x]['title']}",
    )

with col2:
    if domain:
        standards_dict = NGSS_STANDARDS[domain]["standards"]
        selected_standard = st.selectbox(
            "Specific Standard",
            options=list(standards_dict.keys()),
            format_func=lambda x: f"{x}: {standards_dict[x]}",
        )
        lesson["ngss"] = selected_standard

st.divider()

# ============================================================
# STEP 2: NEW VISIONS (optional)
# ============================================================
st.markdown("### 📚 Step 2: New Visions Curriculum (Optional)")

nv_branch = st.selectbox("New Visions Branch", options=["None"] + list(NEW_VISIONS_UNITS.keys()))
if nv_branch != "None":
    nv_unit = st.selectbox("Unit", options=NEW_VISIONS_UNITS[nv_branch])
    lesson["nv_unit"] = nv_unit

st.divider()

# ============================================================
# STEP 3: 5E — WHEEL SELECTOR + ONE PANEL AT A TIME
# (no custom component; uses query params so clicking works)
# ============================================================
st.markdown("### 🔄 Step 3: Build 5E Lesson")

# Wheel image path (you add this file)
WHEEL_IMG = Path("python_hubs/Dev_Forge/assets/ms_piluso/5e_wheel.png")

# Query param phase
q = st.query_params
current_phase = q.get("phase", "Engage")
if current_phase not in FIVE_E_PHASES:
    current_phase = "Engage"

# Render wheel + clickable hotspots (links set ?phase=...)
wheel_left, wheel_right = st.columns([1.05, 1.2], gap="large")

with wheel_left:
    if WHEEL_IMG.exists():
        st.image(str(WHEEL_IMG), caption="5E Model", use_container_width=True)
    else:
        st.warning("Missing wheel image. Add: python_hubs/Dev_Forge/assets/ms_piluso/5e_wheel.png")

    # Click targets: simple buttons (reliable) + optional links
    bcols = st.columns(5)
    phases = ["Engage", "Explore", "Explain", "Elaborate", "Evaluate"]
    for i, ph in enumerate(phases):
        with bcols[i]:
            if st.button(ph, use_container_width=True, type="primary" if ph == current_phase else "secondary"):
                st.query_params["phase"] = ph
                st.rerun()

with wheel_right:
    st.subheader(current_phase)
    st.caption(FIVE_E_PHASES[current_phase])

    show_starters = st.toggle("Show sentence starters", value=True)
    if show_starters:
        starters = SENTENCE_STARTERS.get(current_phase, [])
        if starters:
            st.markdown("**Sentence starters:**")
            st.write("\n".join([f"• {s}" for s in starters]))

    key = current_phase.lower()
    lesson[key] = st.text_area(
        f"{current_phase} (what students do / say)",
        value=lesson.get(key, ""),
        height=180,
        placeholder=f"Describe {key} activities…",
    )

st.divider()

# ============================================================
# STEP 4: DETAILS
# ============================================================
st.markdown("### ✏️ Step 4: Lesson Details")

cA, cB = st.columns(2, gap="large")
with cA:
    lesson["objective"] = st.text_area(
        "Student Objective",
        value=lesson.get("objective", ""),
        placeholder="Students will be able to…",
        height=110,
    )

with cB:
    lesson["materials"] = st.text_area(
        "Materials Needed",
        value=lesson.get("materials", ""),
        placeholder="List materials, tech, handouts…",
        height=110,
    )

lesson["notes"] = st.text_area(
    "Teacher Notes / Differentiation",
    value=lesson.get("notes", ""),
    placeholder="Notes, modifications, extensions…",
    height=110,
)

lesson["accommodations"] = st.text_area(
    "Accommodations / Modifications",
    value=lesson.get("accommodations", ""),
    placeholder="IEP/504 supports: visuals, sentence starters, extended time, breaks, reduced choices...",
    height=110,
)

st.divider()

# ============================================================
# PREVIEW
# ============================================================
st.markdown("### 👁️ Preview")

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
""".strip()

st.text_area("Lesson Preview", value=preview_text, height=420, disabled=True)

st.divider()

# ============================================================
# SCI-BLOCK JPEG EXPORT (same output idea)
# ============================================================
st.markdown("### 🖼️ Export SCI-BLOCK (JPEG)")

ngss_pick = safe_val(lesson.get("ngss"))
today_str = date.today().isoformat()
header_title = f"SCI-BLOCK • {today_str} • {ngss_pick}"

img_lines: List[Tuple[str, bool]] = [
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

st.divider()

# ============================================================
# EXPORT OPTIONS
# ============================================================
st.markdown("### 🚀 Export")

e1, e2, e3 = st.columns(3, gap="large")

with e1:
    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.info("Copy the preview text manually (Streamlit clipboard is browser-based).")

with e2:
    if st.button("📄 Export to BSChapp", use_container_width=True, type="primary"):
        st.success("✅ Ready to paste into BSChapp v2 ‘Lesson Plan’ artifact!")

with e3:
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
        st.query_params.clear()
        st.rerun()

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
