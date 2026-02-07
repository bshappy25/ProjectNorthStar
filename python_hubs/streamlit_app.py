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

BSCL_BLUE = "#2F5BEA"


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


def build_pdf_bytes(artifact, lesson_title, standard_tags, signature, body_text) -> bytes:
    # Only call when REPORTLAB_OK is True
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter
    margin = 0.75 * inch
    x0 = margin
    y = h - margin

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, y, artifact)
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

    # Signature top-right
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


def build_html(artifact, lesson_title, standard_tags, signature, body_text) -> str:
    # Offline/iPhone fallback: download HTML then Print → Save as PDF
    title_line = f"<div style='font-size:20pt;font-weight:900'>{artifact}</div>"
    meta = f"<div style='margin-top:8px'>Date: {date.today().isoformat()}</div>"
    lt = f"<div><b>Lesson/Topic:</b> {lesson_title}</div>" if lesson_title else ""
    stags = f"<div><b>Standards:</b> {standard_tags}</div>" if standard_tags else ""
    sig = f"<div style='position:fixed;top:24px;right:28px;color:{BSCL_BLUE};font-weight:800'>✍️ {signature}</div>" if signature else ""
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
{sig}
{title_line}
{meta}
{lt}
{stags}
<hr/>
<div>{body}</div>
</body></html>"""


# ================= UI =================
st.set_page_config(page_title="BSChapp v1", layout="centered")
st.title("🧩 BSChapp v1")
st.caption("Boomer-proof: edit → preview → download → tap to print")

lesson_title = st.text_input("Lesson / Topic Title (optional)")
standard_tags = st.text_input("Standard Tags (optional)")
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
        body_text=body
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
        body_text=body
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