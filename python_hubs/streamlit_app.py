import io
from datetime import date
import streamlit as st

# Try PDF engine (ReportLab). If missing on Streamlit Cloud, we fallback to HTML.
REPORTLAB_OK = True
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
except Exception:
    REPORTLAB_OK = False

# =====================
# RIGID RAILS (Boomer-proof)
# =====================
GRADE_BANDS = ["HS", "MS", "5", "4", "3", "2", "1", "K"]

SUBJECTS = ["Science"]  # rigid for now

SCIENCE_BRANCHES = [
    "Earth & Space Science",
    "Life Science",
    "Physical Science"
]

SCIENCE_UNITS = {
    "Earth & Space Science": [
        "Weather & Climate",
        "Water Cycle & Watersheds",
        "Plate Tectonics",
        "Rocks & Minerals",
        "Earth Systems Interactions",
        "Space Systems"
    ],
    "Life Science": [
        "Cells & Body Systems",
        "Genetics & Traits",
        "Ecosystems",
        "Natural Selection & Adaptations",
        "Human Impacts on Ecosystems"
    ],
    "Physical Science": [
        "Matter & Its Interactions",
        "Chemical Reactions",
        "Forces & Motion",
        "Energy",
        "Waves",
        "Electricity & Magnetism"
    ]
}

# =====================
# ARTIFACTS
# =====================
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

# UI colors
BSCL_BLUE = "#2F5BEA"
SCIENCE_GREEN = "#2E7D32"  # Science Mode accent

# Emblems (text-only, reliable)
NGSS_EMBLEM = "NGSS"
FIVE_E_EMBLEM = "5E"


def wrap_lines(text: str, max_chars: int = 95):
    out = []
    for para in (text or "").split("\n"):
        if para == "":
            out.append("")
            continue
        line = para
        while len(line) > max_chars:
            out.append(line[:max_chars])
            line = line[max_chars:]
        out.append(line)
    return out


def build_pdf_bytes(
    artifact,
    lesson_title,
    standard_tags,
    signature,
    body_text,
    grade_band,
    subject,
    science_branch,
    unit
) -> bytes:
    # Only call when REPORTLAB_OK is True
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter
    margin = 0.75 * inch
    x0 = margin
    y = h - margin

    # Header title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, y, artifact)

    # Emblems top-right (always for science mode)
    # keep simple: text badges
    badge_text = f"[{NGSS_EMBLEM}]  [{FIVE_E_EMBLEM}]"
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(w - margin, y + 2, badge_text)

    y -= 0.32 * inch

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(x0, y, f"Date: {date.today().isoformat()}")
    y -= 0.22 * inch

    # Rigid rails
    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Grade Band:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, grade_band)
    y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Subject:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, subject)
    y -= 0.22 * inch

    if science_branch:
        c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Branch:")
        c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, science_branch)
        y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Unit:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, unit)
    y -= 0.22 * inch

    # Lesson/topic
    if lesson_title:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x0, y, "Lesson/Topic:")
        c.setFont("Helvetica", 12)
        c.drawString(x0 + 1.2 * inch, y, lesson_title)
        y -= 0.22 * inch

    # Standards
    if standard_tags:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x0, y, "Standards:")
        c.setFont("Helvetica", 12)
        c.drawString(x0 + 1.2 * inch, y, standard_tags)
        y -= 0.22 * inch

    # Signature top-right (blue bridge)
    if signature:
        c.setFillColorRGB(0.184, 0.357, 0.918)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawRightString(w - margin, h - margin + 0.05 * inch, f"✍️ {signature}")
        c.setFillColorRGB(0, 0, 0)

    # Divider
    y -= 0.08 * inch
    c.setLineWidth(1.2)
    c.line(x0, y, w - margin, y)
    y -= 0.25 * inch

    # Body
    c.setFont("Helvetica", 12)
    lines = wrap_lines(body_text, max_chars=95)
    line_h = 14.5
    bottom = margin

    for ln in lines:
        if y <= bottom + 0.6 * inch:
            c.showPage()
            y = h - margin

            # repeat emblems + signature on new page
            c.setFont("Helvetica-Bold", 11)
            c.drawRightString(w - margin, y + 2, badge_text)

            if signature:
                c.setFillColorRGB(0.184, 0.357, 0.918)
                c.setFont("Helvetica-Bold", 11.5)
                c.drawRightString(w - margin, h - margin + 0.05 * inch, f"✍️ {signature}")
                c.setFillColorRGB(0, 0, 0)

            c.setFont("Helvetica", 12)

        c.drawString(x0, y, ln)
        y -= line_h

    # Footer
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawString(
        x0,
        margin - 0.25 * inch,
        "BSChapp v1 • Teacher-owned • Print-first • No tracking • Admin-blind by default"
    )

    c.save()
    return buf.getvalue()


def build_html(
    artifact,
    lesson_title,
    standard_tags,
    signature,
    body_text,
    grade_band,
    subject,
    science_branch,
    unit
) -> str:
    # HTML fallback: download then Print → Save as PDF
    title_line = f"<div style='font-size:20pt;font-weight:900'>{artifact}</div>"
    meta = f"<div style='margin-top:8px'>Date: {date.today().isoformat()}</div>"

    rails = f"""
    <div><b>Grade Band:</b> {grade_band}</div>
    <div><b>Subject:</b> {subject}</div>
    <div><b>Branch:</b> {science_branch}</div>
    <div><b>Unit:</b> {unit}</div>
    """

    lt = f"<div><b>Lesson/Topic:</b> {lesson_title}</div>" if lesson_title else ""
    stags = f"<div><b>Standards:</b> {standard_tags}</div>" if standard_tags else ""

    sig = (
        f"<div style='position:fixed;top:24px;right:28px;color:{BSCL_BLUE};font-weight:800'>✍️ {signature}</div>"
        if signature else ""
    )

    emblems = f"<div style='position:fixed;top:24px;left:28px;font-weight:900'>[{NGSS_EMBLEM}] [{FIVE_E_EMBLEM}]</div>"

    body = (body_text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    body = body.replace("\n", "<br/>")

    return f"""<!doctype html>
<html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>BSChapp v1</title>
<style>
@page {{ size: Letter; margin: 0.75in; }}
body {{ font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; font-size: 13pt; }}
hr {{ border:none; border-top:2px solid #000; margin: 14px 0; }}
</style>
</head>
<body>
{emblems}
{sig}
{title_line}
{meta}
{rails}
{lt}
{stags}
<hr/>
<div>{body}</div>
</body></html>"""


# ================= UI =================
st.set_page_config(page_title="BSChapp v1", layout="centered")

# Science Mode UI (green accent)
st.markdown(f"""
<style>
/* science mode accent */
div[data-testid="stAppViewContainer"] {{
  background: #ffffff;
}}
/* Make primary buttons green-ish (best-effort, Streamlit UI varies) */
button[kind="primary"] {{
  border: 2px solid {SCIENCE_GREEN} !important;
}}
</style>
""", unsafe_allow_html=True)

st.title("🧩 BSChapp v1")
st.caption("Boomer-proof: select rails → edit → preview → download → tap to print")

# REQUIRED rails
st.divider()
st.markdown("### Required selections (rigid)")
grade_band = st.selectbox("Grade Band (required)", GRADE_BANDS, index=0)
subject = st.selectbox("Subject (required)", SUBJECTS, index=0)

science_branch = None
unit = None
if subject == "Science":
    science_branch = st.selectbox("Science Branch (required)", SCIENCE_BRANCHES, index=0)
    unit = st.selectbox("Unit (required)", SCIENCE_UNITS[science_branch], index=0)
else:
    unit = st.selectbox("Unit (required)", ["General"], index=0)

st.info(f"Science Mode: [{NGSS_EMBLEM}] + [{FIVE_E_EMBLEM}] enabled (auto).")

# Optional headers
lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional) — comma separated")
signature = st.text_input("Signature (optional)", placeholder="Initials / name (cosmetic only)")

st.divider()
artifact = st.selectbox("Choose a document", ARTIFACTS)

st.markdown("### Edit content")
body = st.text_area("Simple editor", value=DEFAULT_PROMPTS.get(artifact, ""), height=340)

with st.expander("Claude Window (placeholder — coming soon)"):
    st.caption("Reserved space for future structured generation. (No AI in v1.)")
    st.text_area("Claude output will appear here later.", value="", height=140)

st.divider()

st.markdown("### Preview")
st.write(f"**{artifact}**")
st.write(f"**Grade Band:** {grade_band}  |  **Subject:** {subject}")
if science_branch:
    st.write(f"**Science Branch:** {science_branch}  |  **Unit:** {unit}")
else:
    st.write(f"**Unit:** {unit}")
if lesson_title:
    st.write(f"**Lesson/Topic:** {lesson_title}")
if standard_tags:
    st.write(f"**Standards:** {standard_tags}")
st.write("---")
st.write(body)

st.divider()

today = date.today().isoformat()

if REPORTLAB_OK:
    pdf_bytes = build_pdf_bytes(
        artifact=artifact,
        lesson_title=lesson_title.strip(),
        standard_tags=standard_tags.strip(),
        signature=signature.strip(),
        body_text=body,
        grade_band=grade_band,
        subject=subject,
        science_branch=science_branch or "",
        unit=unit or ""
    )
    filename = f"{artifact.replace(' ', '_').lower()}_{today}.pdf"
    st.download_button(
        "Download PDF (tap to print)",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.warning("PDF engine not installed yet. Add `reportlab` to requirements.txt to enable PDF downloads.")
    html = build_html(
        artifact=artifact,
        lesson_title=lesson_title.strip(),
        standard_tags=standard_tags.strip(),
        signature=signature.strip(),
        body_text=body,
        grade_band=grade_band,
        subject=subject,
        science_branch=science_branch or "",
        unit=unit or ""
    )
    filename = f"{artifact.replace(' ', '_').lower()}_{today}.html"
    st.download_button(
        "Download HTML (then Print → Save as PDF)",
        data=html,
        file_name=filename,
        mime="text/html",
        use_container_width=True
    )
    st.info("iPhone: after download → open HTML → Share → Print → pinch-out → Save/Share PDF.")

st.caption("BSChapp v1 • Teacher-owned • No tracking • Admin-blind by default")