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

# Light neutral UI for all subjects; Science gets "Science Mode" UI.
SUBJECTS = ["Science", "Math", "ELA"]  # keep rigid

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

# Minimal generic units (placeholders) for non-science subjects for v1
GENERIC_UNITS = {
    "Math": ["Unit A", "Unit B", "Unit C"],
    "ELA": ["Unit A", "Unit B", "Unit C"],
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
NEUTRAL_BG = "#f3f4f6"      # light neutral gray
NEUTRAL_CARD = "#ffffff"    # white cards
NEUTRAL_BORDER = "rgba(0,0,0,0.10)"
NEUTRAL_TEXT = "#111827"
NEUTRAL_MUTED = "#4b5563"

SCI_BG = "#061B15"          # deep teal-black
SCI_CARD = "rgba(255,255,255,0.06)"
SCI_BORDER = "rgba(120,255,220,0.24)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.72)"
SCI_BLUE = "#2F5BEA"        # signature bridge blue
SCI_GREEN = "#14B8A6"       # blue-green accent
SCI_GREEN_2 = "#22C55E"     # secondary green accent

# Emblems (text-only for reliability)
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
    branch,
    unit
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter
    margin = 0.75 * inch
    x0 = margin
    y = h - margin

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, y, artifact)

    # Emblems (only for science)
    if subject == "Science":
        badge_text = f"[{NGSS_EMBLEM}]  [{FIVE_E_EMBLEM}]"
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(w - margin, y + 2, badge_text)

    y -= 0.32 * inch

    # Date
    c.setFont("Helvetica", 12)
    c.drawString(x0, y, f"Date: {date.today().isoformat()}")
    y -= 0.22 * inch

    # Rails
    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Grade Band:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, grade_band)
    y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Subject:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, subject)
    y -= 0.22 * inch

    if subject == "Science" and branch:
        c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Branch:")
        c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, branch)
        y -= 0.22 * inch

    c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Unit:")
    c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, unit)
    y -= 0.22 * inch

    # Lesson / Topic
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

            # repeat emblems (science) + signature on new page
            if subject == "Science":
                c.setFont("Helvetica-Bold", 11)
                c.drawRightString(w - margin, y + 2, f"[{NGSS_EMBLEM}]  [{FIVE_E_EMBLEM}]")

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
    branch,
    unit
) -> str:
    # HTML fallback: download then Print → Save as PDF
    title_line = f"<div style='font-size:20pt;font-weight:900'>{artifact}</div>"
    meta = f"<div style='margin-top:8px'>Date: {date.today().isoformat()}</div>"

    rails = f"""
    <div><b>Grade Band:</b> {grade_band}</div>
    <div><b>Subject:</b> {subject}</div>
    {"<div><b>Branch:</b> " + branch + "</div>" if subject=="Science" and branch else ""}
    <div><b>Unit:</b> {unit}</div>
    """

    lt = f"<div><b>Lesson/Topic:</b> {lesson_title}</div>" if lesson_title else ""
    stags = f"<div><b>Standards:</b> {standard_tags}</div>" if standard_tags else ""

    sig = (
        f"<div style='position:fixed;top:24px;right:28px;color:{SCI_BLUE};font-weight:800'>✍️ {signature}</div>"
        if signature else ""
    )

    emblems = ""
    if subject == "Science":
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

# First: collect subject quickly so we can theme the page
# We'll create a lightweight "pre-select" subject in session_state.
if "subject_mode" not in st.session_state:
    st.session_state["subject_mode"] = "Science"  # default to science for now (you can change)

# Theme tokens based on subject
is_science = (st.session_state["subject_mode"] == "Science")

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_GREEN if is_science else "#6b7280"
ACCENT2 = SCI_GREEN_2 if is_science else "#9ca3af"

# Global CSS: neutral gray vs science blue-green
st.markdown(f"""
<style>
:root {{
  --bg:{BG};
  --card:{CARD};
  --border:{BORDER};
  --text:{TEXT};
  --muted:{MUTED};
  --accent:{ACCENT};
  --accent2:{ACCENT2};
}}

div[data-testid="stAppViewContainer"] {{
  background: var(--bg);
  color: var(--text);
}}

.block-container {{
  padding-top: 1.2rem;
}}

h1, h2, h3, p, label, div {{
  color: var(--text);
}}

.small-muted {{
  color: var(--muted);
  font-size: 0.95rem;
}}

.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px 14px;
}}

.badge {{
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-weight: 800;
  letter-spacing: 0.02em;
  background: rgba(255,255,255,0.04);
}}

.badge-accent {{
  border-color: var(--accent);
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
}}

</style>
""", unsafe_allow_html=True)

st.title("🧩 BSChapp v1")

st.caption("Boomer-proof: select rails → edit → preview → download → tap to print")

# SUBJECT MODE selector (drives UI theme)
st.markdown("### Subject Mode")
subject_mode = st.selectbox("Select subject (required)", SUBJECTS, index=0, key="subject_mode")

st.divider()

# REQUIRED rails
st.markdown("### Required selections (rigid)")
grade_band = st.selectbox("Grade Band (required)", GRADE_BANDS, index=0)

science_branch = ""
unit = ""

if subject_mode == "Science":
    science_branch = st.selectbox("Science Branch (required)", SCIENCE_BRANCHES, index=0)
    unit = st.selectbox("Unit (required)", SCIENCE_UNITS[science_branch], index=0)
else:
    unit = st.selectbox("Unit (required)", GENERIC_UNITS.get(subject_mode, ["Unit A"]), index=0)

# Emblems shown only in science mode
if subject_mode == "Science":
    st.markdown(f"<div class='card'><span class='badge badge-accent'>[{NGSS_EMBLEM}]</span> <span class='badge badge-accent'>[{FIVE_E_EMBLEM}]</span> <span class='small-muted' style='margin-left:10px;'>Science Mode active (blue-green UI)</span></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='card'><span class='small-muted'>Neutral mode active (light gray UI)</span></div>", unsafe_allow_html=True)

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
st.write(f"**Grade Band:** {grade_band}  |  **Subject:** {subject_mode}")
if subject_mode == "Science":
    st.write(f"**Branch:** {science_branch}  |  **Unit:** {unit}")
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
        subject=subject_mode,
        branch=science_branch,
        unit=unit
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
        subject=subject_mode,
        branch=science_branch,
        unit=unit
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