"""
BSChapp — v1 Streamlit App (Freeze Candidate)
Teacher-first • Print-first • Boomer-proof iPhone flow

Goals (per S-answers):
- Simple editing (S1B) for other teachers (S2B)
- Final output as PDF downloads (S3/S10)
- Tap-to-print behavior (iPhone Files/Safari) supported via PDF
- Minimal UI: a few fields + buttons (S5 A/B)
- Claude placeholder window exists but is non-functional (S6/S8)
- Offline mode removed (S9A)

No AI. No analytics. No accounts.
"""

import io
from datetime import date
import streamlit as st

# ReportLab (installed in your environment)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

BSCL_BLUE = (0.184, 0.357, 0.918)  # subtle blue for signature only

ARTIFACTS = [
    "Exit Ticket",
    "Worksheet",
    "Lesson Plan",
    "PBIS Reflective Note",
    "Photo Evidence"
]

DEFAULT_PROMPTS = {
    "Exit Ticket": "Prompt:\n\nStudent Response:",
    "Worksheet": "Do Now:\n\nSection A:\n\nSection B:\n\nSection C:\n\nExit Ticket:",
    "Lesson Plan": "Teacher Objective:\n\nStudent Objective:\n\nDo Now:\n\nProcedure:\n\nCFU:\n\nDifferentiation:\n\nExit Ticket:",
    "PBIS Reflective Note": "What happened (facts):\n\nPBIS focus:\n- Engage in Safety:\n- Learn to Earn:\n- Do the Right Thing:\n- Placeholder:\n- My Goal Point:\n\nPlan (next time I will):\n\nRepair/Restart:",
    "Photo Evidence": "Artifact Type:\n\nEvidence Summary (Teacher):\n\nStudent Objective:\n\nNotes:"
}


# =========================
# PDF ENGINE (boomer-proof)
# =========================
def _wrap_lines(text: str, max_chars: int):
    # Simple wrap by character count (reliable, not pretty, but stable)
    out = []
    for para in (text or "").split("\n"):
        if not para:
            out.append("")
            continue
        line = para
        while len(line) > max_chars:
            cut = line[:max_chars]
            out.append(cut)
            line = line[max_chars:]
        out.append(line)
    return out


def build_pdf_bytes(
    artifact_name: str,
    lesson_title: str,
    standard_tags: str,
    signature: str,
    body_text: str
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter

    margin = 0.75 * inch
    x0 = margin
    y = h - margin

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, y, artifact_name)
    y -= 0.32 * inch

    c.setFont("Helvetica", 12)
    c.drawString(x0, y, f"Date: {date.today().isoformat()}")
    y -= 0.22 * inch

    if lesson_title:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x0, y, "Lesson/Topic:")
        c.setFont("Helvetica", 12)
        c.drawString(x0 + 1.2 * inch, y, lesson_title)
        y -= 0.22 * inch

    if standard_tags:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x0, y, "Standards:")
        c.setFont("Helvetica", 12)
        c.drawString(x0 + 1.2 * inch, y, standard_tags)
        y -= 0.22 * inch

    # Signature (top-right, subtle blue)
    if signature:
        c.setFillColorRGB(*BSCL_BLUE)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawRightString(w - margin, h - margin + 0.05 * inch, f"✍️ {signature}")
        c.setFillColorRGB(0, 0, 0)

    # Divider line
    y -= 0.08 * inch
    c.setLineWidth(1.2)
    c.line(x0, y, w - margin, y)
    y -= 0.25 * inch

    # Body content box
    c.setFont("Helvetica", 12)

    # Conservative wrapping to avoid overflow
    max_chars = 95
    lines = _wrap_lines(body_text, max_chars=max_chars)

    line_h = 14.5
    bottom = margin

    for ln in lines:
        if y <= bottom + 0.6 * inch:
            c.showPage()
            y = h - margin
            # repeat signature on new page
            if signature:
                c.setFillColorRGB(*BSCL_BLUE)
                c.setFont("Helvetica-Bold", 11.5)
                c.drawRightString(w - margin, h - margin + 0.05 * inch, f"✍️ {signature}")
                c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 12)

        c.drawString(x0, y, ln)
        y -= line_h

    # Footer note (admin-blind statement)
    c.setFont("Helvetica-Oblique", 9.5)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(
        x0,
        margin - 0.25 * inch,
        "BSChapp v1 • Teacher-owned • Print-first • No tracking • Admin-blind by default"
    )

    c.save()
    return buf.getvalue()


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="BSChapp v1", layout="centered")

st.title("🧩 BSChapp v1")
st.caption("Teacher-first • Print-first • Boomer-proof iPhone flow (PDF download)")

st.markdown(
    """
**How it works**
1) Pick a document  
2) Edit the text (simple)  
3) Download PDF → tap to print / share  
"""
)

# Super-simple inputs (S5 A/B)
lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional)")
signature = st.text_input("Signature (optional)", placeholder="Initials / name (cosmetic only)")

st.divider()

artifact = st.selectbox("Choose a document", ARTIFACTS)

# Minimal editor: one big box (works for boomers)
st.markdown("### Edit content")
body = st.text_area(
    "Simple editor (no formatting needed)",
    value=DEFAULT_PROMPTS.get(artifact, ""),
    height=340
)

# Claude placeholder (S6/S8)
with st.expander("Claude Window (placeholder — coming soon)"):
    st.caption("This will later provide structured generation / rewrites. For now it’s a placeholder.")
    st.text_area("Claude output will appear here later.", value="", height=140, disabled=False)

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Preview (on-screen)", use_container_width=True):
        st.markdown("### Preview")
        st.write(f"**{artifact}**")
        if lesson_title:
            st.write(f"**Lesson/Topic:** {lesson_title}")
        if standard_tags:
            st.write(f"**Standards:** {standard_tags}")
        st.write("---")
        st.write(body if body else "(empty)")

with col2:
    # Generate PDF bytes every run (fast enough; avoids state bugs)
    pdf_bytes = build_pdf_bytes(
        artifact_name=artifact,
        lesson_title=lesson_title.strip(),
        standard_tags=standard_tags.strip(),
        signature=signature.strip(),
        body_text=body
    )
    filename = f"{artifact.replace(' ', '_').lower()}_{date.today().isoformat()}.pdf"

    st.download_button(
        "Download PDF (tap to print)",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )

st.info(
    "iPhone tip: After download → open the PDF in Files/Safari → Share → Print.\n"
    "No one edits HTML. This is the boomer-proof path."
)

st.divider()
st.caption("No accounts • No analytics • No admin access • v1 freeze candidate")