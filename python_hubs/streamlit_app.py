"""
BSChapp — Phase 1 Streamlit UI
Teacher-first demo.
No AI. No analytics. No admin logic.
"""

import os
from datetime import date
import streamlit as st

# ===== CONFIG =====
TEMPLATES = {
    "Exit Ticket": "materials/exit_tickets/exit_ticket_v1.html",
    "Worksheet": "materials/worksheets/worksheet_v1.html",
    "Lesson Plan": "materials/lesson_plans/lesson_plan_v1.html",
    "PBIS Reflective Note": "materials/pbis/pbis_reflective_note_v1.html",
    "Photo Evidence": "materials/evidence/photo_evidence_v1.html",
}

OUTPUT_DIR = "generated_artifacts"

# ===== HELPERS =====
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_output(content, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def populate_safe_fields(content, title="", standards=""):
    # Only touch the first two placeholder lines (safe fields)
    content = content.replace("__________________________", title or "__________________________", 1)
    content = content.replace("__________________________", standards or "__________________________", 1)
    return content

def generate_files(selected, title, standards):
    today = date.today().isoformat()
    ensure_dir(OUTPUT_DIR)
    outputs = []

    for name in selected:
        template_path = TEMPLATES[name]
        html = load_template(template_path)
        html = populate_safe_fields(html, title=title, standards=standards)

        filename = f"{name.replace(' ', '_').lower()}_{today}.html"
        out_path = os.path.join(OUTPUT_DIR, filename)
        save_output(html, out_path)
        outputs.append(out_path)

    return outputs

# ===== STREAMLIT UI =====
st.set_page_config(
    page_title="BSChapp — Teacher Material Generator",
    layout="centered"
)

st.title("🧩 BSChapp")
st.subheader("Teacher-First Material Generator (Phase 1)")

st.markdown(
    """
**What this does**
- Generates print-ready classroom materials
- No accounts, no tracking, no admin access
- Files are teacher-owned and ready to print
"""
)

st.divider()

lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional)")

st.markdown("### Select materials to generate:")
selected_templates = st.multiselect(
    "",
    list(TEMPLATES.keys()),
    default=list(TEMPLATES.keys())
)

st.divider()

if st.button("Generate Materials"):
    if not selected_templates:
        st.warning("Select at least one material.")
    else:
        outputs = generate_files(
            selected_templates,
            lesson_title.strip(),
            standard_tags.strip()
        )

        st.success("Materials generated!")
        st.markdown("**Files created:**")
        for path in outputs:
            st.code(path, language="text")

        st.info(
            "Open a file → Print (Letter, B/W). "
            "These are safe, Phase-1 demo outputs."
        )

st.divider()

st.caption(
    "BSChapp • Teacher-First • Print-First • Admin-Blind by Default\n"
    "Phase 1 demo — no AI, no analytics, no storage."
)