"""
BSChapp — v1 Streamlit App
Teacher-first. Print-first. Admin-blind.

v1 additions:
- Optional signature
- Signature rendered top-right on all generated documents
- Mobile-safe downloads (works better in Safari + in-app browsers)
- No storage, no tracking, no identity enforcement
"""

import os
from datetime import date
import streamlit as st

# =====================
# CONFIG
# =====================
TEMPLATES = {
    "Exit Ticket": "materials/exit_tickets/exit_ticket_v1.html",
    "Worksheet": "materials/worksheets/worksheet_v1.html",
    "Lesson Plan": "materials/lesson_plans/lesson_plan_v1.html",
    "PBIS Reflective Note": "materials/pbis/pbis_reflective_note_v1.html",
    "Photo Evidence": "materials/evidence/photo_evidence_v1.html",
}

OUTPUT_DIR = "generated_artifacts"

SIGNATURE_HTML = """
<div style="
  position:fixed;
  top:0.5in;
  right:0.6in;
  font-size:11.5pt;
  font-weight:700;
  color:#2F5BEA;
  z-index:9999;
">
  ✍️ {signature}
</div>
"""

# =====================
# HELPERS
# =====================
def ensure_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def load_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_output(content: str, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def inject_signature(html: str, signature: str) -> str:
    if not signature:
        return html
    signature_block = SIGNATURE_HTML.format(signature=signature)
    return html.replace("<body>", f"<body>\n{signature_block}", 1)

def populate_safe_fields(html: str, title: str = "", standards: str = "") -> str:
    # Safe, minimal fill: first two blank slots only
    html = html.replace("__________________________", title or "__________________________", 1)
    html = html.replace("__________________________", standards or "__________________________", 1)
    return html

def generate_files(selected, title: str, standards: str, signature: str):
    today = date.today().isoformat()
    ensure_dir(OUTPUT_DIR)
    outputs = []

    for name in selected:
        template_path = TEMPLATES[name]
        html = load_template(template_path)
        html = populate_safe_fields(html, title, standards)
        html = inject_signature(html, signature)

        filename = f"{name.replace(' ', '_').lower()}_{today}.html"
        out_path = os.path.join(OUTPUT_DIR, filename)
        save_output(html, out_path)

        outputs.append(out_path)

    return outputs

# =====================
# STREAMLIT UI
# =====================
st.set_page_config(page_title="BSChapp v1", layout="centered")

st.title("🧩 BSChapp")
st.subheader("Teacher-First Material Generator")

st.markdown(
    """
**What this does**
- Generates print-ready classroom materials  
- No accounts, no tracking, no admin access  
- Files are teacher-owned and ready to print  
"""
)

st.divider()

# ---------- INPUTS ----------
lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional)")

signature = st.text_input(
    "Signature (optional)",
    placeholder="Your name, initials, or leave blank"
)
st.caption("Signature appears top-right on all generated documents (cosmetic only).")

st.divider()

# ---------- MATERIAL SELECT ----------
st.markdown("### Select materials to generate")
st.caption("Most teachers generate all of these daily.")

selected_templates = st.multiselect(
    "",
    list(TEMPLATES.keys()),
    default=list(TEMPLATES.keys())
)

st.divider()

# ---------- GENERATE ----------
if st.button("Generate Materials"):
    if not selected_templates:
        st.warning("Select at least one material.")
    else:
        outputs = generate_files(
            selected_templates,
            lesson_title.strip(),
            standard_tags.strip(),
            signature.strip()
        )

        st.success("Materials generated!")

        # Mobile/in-app browser advice
        st.warning(
            "If you opened this inside Facebook/Messenger: tap ••• and choose **Open in Safari/Chrome** for best printing."
        )

        st.markdown("### Download your files (mobile-safe)")
        for path in outputs:
            filename = os.path.basename(path)

            # Show just the filename (cleaner than server path)
            st.code(filename, language="text")

            # Download button = best behavior on iPhone + in-app browsers
            with open(path, "r", encoding="utf-8") as f:
                st.download_button(
                    label=f"Download {filename}",
                    data=f.read(),
                    file_name=filename,
                    mime="text/html",
                    use_container_width=True
                )

        st.info(
            "After downloading, open the HTML file → Share → Print (Letter). "
            "Signature is cosmetic only and not stored."
        )

st.divider()

st.caption(
    "BSChapp v1 • Teacher-First • Print-First • Admin-Blind\n"
    "No AI • No analytics • No accounts"
)