```python
from __future__ import annotations

import streamlit as st

# ============================================================
# MS. PILUSO SCIENCE PAGE (Priority #2)
# ============================================================

st.title("🔬 Ms. Piluso Science - NGSS Lesson Builder")
st.markdown("### New Visions Curriculum Integration + 5E Framework")

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "ngss_standard" not in st.session_state:
    st.session_state["ngss_standard"] = ""
if "lesson_title" not in st.session_state:
    st.session_state["lesson_title"] = ""
if "grade_level" not in st.session_state:
    st.session_state["grade_level"] = "6th Grade"
if "engage" not in st.session_state:
    st.session_state["engage"] = ""
if "explore" not in st.session_state:
    st.session_state["explore"] = ""
if "explain" not in st.session_state:
    st.session_state["explain"] = ""
if "elaborate" not in st.session_state:
    st.session_state["elaborate"] = ""
if "evaluate" not in st.session_state:
    st.session_state["evaluate"] = ""
if "materials" not in st.session_state:
    st.session_state["materials"] = ""
if "accommodations" not in st.session_state:
    st.session_state["accommodations"] = ""
if "teacher_notes" not in st.session_state:
    st.session_state["teacher_notes"] = ""

# ============================================================
# NGSS STANDARDS DATABASE (MS = Middle School)
# ============================================================

NGSS_STANDARDS = {
    "MS-PS1-1": "Develop models to describe atomic composition of simple molecules and extended structures",
    "MS-PS1-2": "Analyze and interpret data on properties of substances before and after interaction",
    "MS-PS1-3": "Gather and make sense of information to describe synthetic materials",
    "MS-PS1-4": "Develop a model that predicts and describes changes in particle motion",
    "MS-PS2-1": "Apply Newton's Third Law to design a solution to a problem",
    "MS-PS2-2": "Plan an investigation to provide evidence that the change in motion depends on forces",
    "MS-PS3-1": "Construct and interpret graphical displays of data to describe relationships of kinetic energy",
    "MS-PS3-2": "Develop a model to describe that when arrangement of objects changes, energy changes",
    "MS-LS1-1": "Conduct an investigation to provide evidence that living things are made of cells",
    "MS-LS1-2": "Develop and use a model to describe the function of a cell as a whole",
    "MS-LS1-3": "Use argument supported by evidence for how the body is a system of interacting subsystems",
    "MS-LS2-1": "Analyze and interpret data to provide evidence for effects of resource availability",
    "MS-LS2-2": "Construct an explanation that predicts patterns of interactions among organisms",
    "MS-ESS1-1": "Develop and use a model of the Earth-sun-moon system",
    "MS-ESS1-2": "Develop and use a model to describe the role of gravity in the motions within galaxies",
    "MS-ESS2-1": "Develop a model to describe the cycling of Earth's materials",
    "MS-ESS3-1": "Construct a scientific explanation based on evidence for how unequal heating of Earth",
}

# ============================================================
# TOP SECTION: LESSON BASICS
# ============================================================

st.markdown(
    """
<div class='dev-card animate-fade'>
<div class='kicker'>STEP 1</div>
<h3>📋 Lesson Basics</h3>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([0.65, 0.35])

with col1:
    st.session_state["lesson_title"] = st.text_input(
        "Lesson Title", 
        value=st.session_state["lesson_title"],
        placeholder="e.g., Chemical Reactions and Energy Transfer"
    )

with col2:
    st.session_state["grade_level"] = st.selectbox(
        "Grade Level",
        ["6th Grade", "7th Grade", "8th Grade"],
        index=["6th Grade", "7th Grade", "8th Grade"].index(st.session_state["grade_level"])
    )

# NGSS Standard Selection
ngss_options = [""] + list(NGSS_STANDARDS.keys())
current_index = 0
if st.session_state["ngss_standard"] in ngss_options:
    current_index = ngss_options.index(st.session_state["ngss_standard"])

st.session_state["ngss_standard"] = st.selectbox(
    "NGSS Standard",
    ngss_options,
    index=current_index,
    format_func=lambda x: f"{x} - {NGSS_STANDARDS.get(x, 'Select a standard')}" if x else "Select a standard"
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# 5E FRAMEWORK BUILDER
# ============================================================

st.markdown(
    """
<div class='dev-card'>
<div class='kicker'>STEP 2</div>
<h3>🎯 5E Framework</h3>
<p class='muted'>Engage → Explore → Explain → Elaborate → Evaluate</p>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎪 Engage", "🔍 Explore", "💡 Explain", "🚀 Elaborate", "✅ Evaluate"])

with tab1:
    st.markdown("**Hook students' attention and assess prior knowledge**")
    st.session_state["engage"] = st.text_area(
        "Engage Activities",
        value=st.session_state["engage"],
        height=150,
        placeholder="e.g., Show video of chemical reaction, ask students what they observe...",
        label_visibility="collapsed"
    )

with tab2:
    st.markdown("**Students investigate and gather data**")
    st.session_state["explore"] = st.text_area(
        "Explore Activities",
        value=st.session_state["explore"],
        height=150,
        placeholder="e.g., Lab activity: students mix baking soda and vinegar, measure temperature change...",
        label_visibility="collapsed"
    )

with tab3:
    st.markdown("**Introduce formal terms, definitions, and explanations**")
    st.session_state["explain"] = st.text_area(
        "Explain Activities",
        value=st.session_state["explain"],
        height=150,
        placeholder="e.g., Direct instruction on endothermic vs exothermic reactions, energy diagrams...",
        label_visibility="collapsed"
    )

with tab4:
    st.markdown("**Students apply concepts in new situations**")
    st.session_state["elaborate"] = st.text_area(
        "Elaborate Activities",
        value=st.session_state["elaborate"],
        height=150,
        placeholder="e.g., Design experiment to test hand warmers or cold packs...",
        label_visibility="collapsed"
    )

with tab5:
    st.markdown("**Assess student understanding**")
    st.session_state["evaluate"] = st.text_area(
        "Evaluate Activities",
        value=st.session_state["evaluate"],
        height=150,
        placeholder="e.g., Exit ticket: Explain why ice melting is endothermic...",
        label_visibility="collapsed"
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# MATERIALS & ACCOMMODATIONS
# ============================================================

st.markdown(
    """
<div class='dev-card'>
<div class='kicker'>STEP 3</div>
<h3>📦 Materials & Accommodations</h3>
</div>
""",
    unsafe_allow_html=True,
)

colA, colB = st.columns(2)

with colA:
    st.markdown("**Materials List**")
    st.session_state["materials"] = st.text_area(
        "Materials",
        value=st.session_state["materials"],
        height=200,
        placeholder="• Baking soda\n• Vinegar\n• Thermometers\n• Beakers...",
        label_visibility="collapsed"
    )

with colB:
    st.markdown("**Accommodations & Differentiation**")
    st.session_state["accommodations"] = st.text_area(
        "Accommodations",
        value=st.session_state["accommodations"],
        height=200,
        placeholder="• ELL: Provide vocabulary cards with visuals\n• IEP: Extended time for lab write-up\n• Advanced: Research real-world applications...",
        label_visibility="collapsed"
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# TEACHER NOTES
# ============================================================

st.markdown(
    """
<div class='dev-card'>
<h3>📝 Teacher Notes</h3>
<p class='muted'>Planning notes, timing, common misconceptions, etc.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.session_state["teacher_notes"] = st.text_area(
    "Teacher Notes",
    value=st.session_state["teacher_notes"],
    height=120,
    placeholder="e.g., Allow 15 min for Explore. Watch for safety with vinegar. Common mistake: students confuse temp change with heat...",
    label_visibility="collapsed"
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# EXPORT & PREVIEW
# ============================================================

st.markdown("## 📄 Export & Preview")

cX, cY = st.columns([0.5, 0.5])

with cX:
    if st.button("📋 Copy Lesson Plan to Clipboard", use_container_width=True):
        lesson_text = f"""
MS. PILUSO SCIENCE - LESSON PLAN
{'='*50}

LESSON TITLE: {st.session_state['lesson_title']}
GRADE LEVEL: {st.session_state['grade_level']}
NGSS STANDARD: {st.session_state['ngss_standard']}
{NGSS_STANDARDS.get(st.session_state['ngss_standard'], '')}

{'='*50}
5E FRAMEWORK
{'='*50}

ENGAGE:
{st.session_state['engage']}

EXPLORE:
{st.session_state['explore']}

EXPLAIN:
{st.session_state['explain']}

ELABORATE:
{st.session_state['elaborate']}

EVALUATE:
{st.session_state['evaluate']}

{'='*50}
MATERIALS:
{st.session_state['materials']}

ACCOMMODATIONS:
{st.session_state['accommodations']}

TEACHER NOTES:
{st.session_state['teacher_notes']}
"""
        st.code(lesson_text, language=None)
        st.success("✅ Lesson plan ready! Copy from box above.")

with cY:
    if st.button("🔄 Clear All Fields", use_container_width=True):
        st.session_state["lesson_title"] = ""
        st.session_state["ngss_standard"] = ""
        st.session_state["engage"] = ""
        st.session_state["explore"] = ""
        st.session_state["explain"] = ""
        st.session_state["elaborate"] = ""
        st.session_state["evaluate"] = ""
        st.session_state["materials"] = ""
        st.session_state["accommodations"] = ""
        st.session_state["teacher_notes"] = ""
        st.rerun()

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)