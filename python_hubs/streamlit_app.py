import io
from datetime import date
import streamlit as st

# ============================================================
# BSChapp v1 — FREEZE BUILD
# - Universal neutral gray by default (Science is NOT default)
# - Science Mode = impactful blue-green UI + NGSS + 5E emblems
# - Palm ID: 🌴 tap 3x → unlock admin code box (code: "Bshapp")
# - Boomer-proof rails + simple editor + PDF download (HTML fallback)
# ============================================================

# -----------------------------
# PDF engine (ReportLab)
# -----------------------------
REPORTLAB_OK = True
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
except Exception:
    REPORTLAB_OK = False

# =====================
# RIGID RAILS
# =====================
GRADE_BANDS = ["HS", "MS", "5", "4", "3", "2", "1", "K"]

# Science is NOT default. Default = "Select…" which keeps neutral UI.
SUBJECTS = ["Select…", "Science", "Math", "ELA"]

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

GENERIC_UNITS = {
    "Math": ["Unit A", "Unit B", "Unit C"],
    "ELA": ["Unit A", "Unit B", "Unit C"],
    "Select…": ["Unit A"],
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

# =====================
# THEME TOKENS
# =====================

# UNIVERSAL NEUTRAL (DEFAULT)
NEUTRAL_BG = "#f2f2f2"          # app background
NEUTRAL_CARD = "#e6e6e6"        # ALL boxes
NEUTRAL_BORDER = "#cfcfcf"
NEUTRAL_TEXT = "#000000"        # true black
NEUTRAL_MUTED = "#1f1f1f"
NEUTRAL_ACCENT = "#5a5a5a"

# SCIENCE MODE (ONLY EXCEPTION)
SCI_BG = "#061B15"
SCI_CARD = "#0f2a22"
SCI_BORDER = "#14b8a6"
SCI_TEXT = "#ffffff"
SCI_MUTED = "#d1fae5"
SCI_ACCENT = "#14b8a6"
SCI_ACCENT2 = "#2F5BEA"
# Science mode (impactful blue-green)
SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.06)"
SCI_BORDER = "rgba(120,255,220,0.24)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.74)"
SCI_ACCENT = "#14B8A6"      # blue-green
SCI_ACCENT2 = "#2F5BEA"     # bridge blue (also used for signature)

# Emblems (text-only = reliable)
NGSS_EMBLEM = "NGSS"
FIVE_E_EMBLEM = "5E"

# Admin code (Palm ID unlock)
ADMIN_CODE = "Bshapp"


# =====================
# HELPERS
# =====================
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

    # Science emblems top-right
    if subject == "Science":
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(w - margin, y + 2, f"[{NGSS_EMBLEM}]  [{FIVE_E_EMBLEM}]")

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
        c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Lesson/Topic:")
        c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, lesson_title)
        y -= 0.22 * inch

    # Standards
    if standard_tags:
        c.setFont("Helvetica-Bold", 12); c.drawString(x0, y, "Standards:")
        c.setFont("Helvetica", 12); c.drawString(x0 + 1.2 * inch, y, standard_tags)
        y -= 0.22 * inch

    # Signature top-right (bridge blue)
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

            # repeat emblems + signature on new pages
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
        f"<div style='position:fixed;top:24px;right:28px;color:{SCI_ACCENT2};font-weight:800'>✍️ {signature}</div>"
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


# =====================
# SESSION STATE DEFAULTS
# =====================
if "subject_mode" not in st.session_state:
    st.session_state["subject_mode"] = "Select…"   # NOT science by default
if "palm_taps" not in st.session_state:
    st.session_state["palm_taps"] = 0
if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = False
if "show_admin_box" not in st.session_state:
    st.session_state["show_admin_box"] = False

# =====================
# STREAMLIT UI
# =====================
st.set_page_config(page_title="BSChapp v1", layout="centered")

# Determine theme based on subject selection
is_science = (st.session_state["subject_mode"] == "Science")

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_ACCENT if is_science else NEUTRAL_ACCENT

st.markdown(f"""
<style>
:root {{
  --bg:{BG};
  --card:{CARD};
  --border:{BORDER};
  --text:{TEXT};
  --muted:{MUTED};
  --accent:{ACCENT};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

.block-container {{
  padding-top: 1.2rem;
}}

h1, h2, h3, h4, h5, h6,
p, span, label, div {{
  color: var(--text) !important;
}}

input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
}}

.card {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px;
  padding: 14px;
}}

.small-muted {{
  color: var(--muted) !important;
  font-size: 0.95rem;
}}

.badge {{
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-weight: 900;
  background-color: var(--card);
}}

.badge-accent {{
  border-color: var(--accent);
}}

button {{
  color: var(--text) !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
}}
</style>
""", unsafe_allow_html=True)

div[data-testid="stAppViewContainer"] {{
  background: var(--bg);
  color: var(--text);
}}

h1, h2, h3, p, label, div {{ color: var(--text); }}

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
  display:inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-weight: 900;
  letter-spacing: 0.02em;
  background: rgba(255,255,255,0.04);
}}

.badge-accent {{
  border-color: var(--accent);
}}

</style>
""", unsafe_allow_html=True)

# Header row with Palm ID on the right
left, right = st.columns([0.88, 0.12], vertical_alignment="center")
with left:
    st.title("🧩 BSChapp v1")
    st.caption("Default: universal neutral gray • Science: blue-green Science Mode")
with right:
    # Palm ID: tap 3x to show admin code box
    if st.button("🌴", help="Palm ID (tap 3x)"):
        st.session_state["palm_taps"] += 1
        if st.session_state["palm_taps"] >= 3:
            st.session_state["show_admin_box"] = True

# Admin gate
if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
    st.markdown("<div class='card'><b>Palm ID:</b> enter admin code</div>", unsafe_allow_html=True)
    code_try = st.text_input("Admin Code", type="password", placeholder="Enter code…")
    if st.button("Unlock Admin"):
        if code_try == ADMIN_CODE:
            st.session_state["admin_unlocked"] = True
            st.success("Admin override unlocked.")
        else:
            st.error("Incorrect code.")
elif st.session_state["admin_unlocked"]:
    st.markdown("<div class='card'><b>Admin Override:</b> unlocked</div>", unsafe_allow_html=True)

st.divider()

# Subject drives theme (Science not default)
st.markdown("### Subject Mode (required)")
subject_mode = st.selectbox("Select subject", SUBJECTS, index=SUBJECTS.index(st.session_state["subject_mode"]), key="subject_mode")

st.divider()

# Required rails
st.markdown("### Required selections (rigid)")
grade_band = st.selectbox("Grade Band (required)", GRADE_BANDS, index=0)

science_branch = ""
unit = ""

if subject_mode == "Science":
    science_branch = st.selectbox("Science Branch (required)", SCIENCE_BRANCHES, index=0)
    unit = st.selectbox("Unit (required)", SCIENCE_UNITS[science_branch], index=0)
else:
    unit_list = GENERIC_UNITS.get(subject_mode, ["Unit A"])
    unit = st.selectbox("Unit (required)", unit_list, index=0)

# Science emblems (auto)
if subject_mode == "Science":
    st.markdown(
        f"<div class='card'><span class='badge badge-accent'>[{NGSS_EMBLEM}]</span> "
        f"<span class='badge badge-accent'>[{FIVE_E_EMBLEM}]</span> "
        f"<span class='small-muted' style='margin-left:10px;'>Science Mode active</span></div>",
        unsafe_allow_html=True
    )
else:
    st.markdown("<div class='card'><span class='small-muted'>Neutral mode active</span></div>", unsafe_allow_html=True)

# Optional headers
lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standards (optional) — comma separated")
signature = st.text_input("Signature (optional)", placeholder="Initials / name (cosmetic only)")

st.divider()

artifact = st.selectbox("Choose a document", ARTIFACTS)

st.markdown("### Edit content")
body = st.text_area("Simple editor", value=DEFAULT_PROMPTS.get(artifact, ""), height=340)

with st.expander("Claude Window (placeholder — coming soon)"):
    st.caption("Reserved space for future structured generation. (No AI in v1.)")
    st.text_area("Claude output will appear here later.", value="", height=140)

st.divider()

# Preview
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

# Block download until subject selected (boomer rail)
if subject_mode == "Select…":
    st.warning("Select a subject to enable download.")
else:
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

st.caption("BSChapp v1 • Teacher-owned • No tracking • Admin-blind by default • FREEZE")