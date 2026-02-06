"""
BSChapp — v1 Streamlit App (Mobile-safe)
Teacher-first. Print-first. Admin-blind.

- Optional signature (top-right)
- Mobile download buttons (works in Safari + in-app browsers)
- Template path auto-resolve (materials/ OR materials/materials/)
- Offline editor download button (if offline_editor.html exists)
- No AI. No analytics. No accounts.
"""

import os
from pathlib import Path
from datetime import date
import streamlit as st


# =====================
# PATHS
# =====================
REPO_ROOT = Path(__file__).resolve().parents[1]  # project root
OUTPUT_DIR = REPO_ROOT / "generated_artifacts"

TEMPLATES_RAW = {
    "Exit Ticket": "materials/exit_tickets/exit_ticket_v1.html",
    "Worksheet": "materials/worksheets/worksheet_v1.html",
    "Lesson Plan": "materials/lesson_plans/lesson_plan_v1.html",
    "PBIS Reflective Note": "materials/pbis/pbis_reflective_note_v1.html",
    "Photo Evidence": "materials/evidence/photo_evidence_v1.html",
}

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
def ensure_dir(dirpath: Path) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)

def resolve_template_path(rel_path: str) -> Path:
    """
    Supports both:
      materials/...
      materials/materials/...
    """
    p1 = REPO_ROOT / rel_path
    if p1.exists():
        return p1

    # auto-try double materials
    if rel_path.startswith("materials/"):
        p2 = REPO_ROOT / ("materials/" + rel_path)
        if p2.exists():
            return p2

    return p1  # return primary for error messaging

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")

def populate_safe_fields(html: str, title: str = "", standards: str = "") -> str:
    # Safe, minimal fill: first two occurrences only
    html = html.replace("__________________________", title or "__________________________", 1)
    html = html.replace("__________________________", standards or "__________________________", 1)
    return html

def inject_signature(html: str, signature: str) -> str:
    if not signature:
        return html
    sig = SIGNATURE_HTML.format(signature=signature)
    return html.replace("<body>", f"<body>\n{sig}", 1)

def generate_files(selected_names, title: str, standards: str, signature: str):
    ensure_dir(OUTPUT_DIR)
    today = date.today().isoformat()
    outputs = []

    for display_name in selected_names:
        rel = TEMPLATES_RAW[display_name]
        template_path = resolve_template_path(rel)

        if not template_path.exists():
            raise FileNotFoundError(
                f"Missing template: {rel}\nTried: {template_path}"
            )

        html = load_text(template_path)
        html = populate_safe_fields(html, title, standards)
        html = inject_signature(html, signature)

        filename = f"{display_name.replace(' ', '_').lower()}_{today}.html"
        out_path = OUTPUT_DIR / filename
        save_text(out_path, html)
        outputs.append(out_path)

    return outputs

def find_offline_editor() -> Path | None:
    # Try a few common locations
    candidates = [
        REPO_ROOT / "offline_editor.html",
        REPO_ROOT / "materials" / "offline_editor.html",
        REPO_ROOT / "python_hubs" / "offline_editor.html",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


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

# ---------- OFFLINE MODE ----------
st.markdown("### Offline Mode (NYC subway-safe)")
st.caption("Download once. Use with no service. Then come back online to sign + download.")

offline_path = find_offline_editor()
if offline_path:
    st.download_button(
        label="Download Offline Editor (HTML)",
        data=load_text(offline_path),
        file_name="offline_editor.html",
        mime="text/html",
        use_container_width=True
    )
else:
    st.info("Offline editor not found yet. Add `offline_editor.html` at the repo root to enable this button.")

st.divider()

# ---------- INPUTS ----------
lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional)")
signature = st.text_input("Signature (optional)", placeholder="Your name, initials, or leave blank")
st.caption("Signature appears top-right on all generated documents (cosmetic only).")

st.divider()

# ---------- SELECT ----------
st.markdown("### Select materials to generate")
st.caption("Most teachers generate all of these daily.")
selected_templates = st.multiselect("", list(TEMPLATES_RAW.keys()), default=list(TEMPLATES_RAW.keys()))

st.divider()

# ---------- GENERATE ----------
if st.button("Generate Materials"):
    try:
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

            st.warning(
                "If you opened this inside Facebook/Messenger: tap ••• → **Open in Safari/Chrome** for best printing."
            )

            st.markdown("### Download your files (mobile-safe)")
            for p in outputs:
                st.code(p.name, language="text")
                st.download_button(
                    label=f"Download {p.name}",
                    data=load_text(p),
                    file_name=p.name,
                    mime="text/html",
                    use_container_width=True
                )

            st.info("After downloading: open the HTML → Share → Print (Letter).")
    except Exception as e:
        st.error("Generation failed.")
        st.exception(e)

st.divider()
st.caption("BSChapp v1 • Teacher-First • Print-First • Admin-Blind • No AI • No analytics • No accounts")