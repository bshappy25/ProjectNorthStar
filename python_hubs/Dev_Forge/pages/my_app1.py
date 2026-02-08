"""
My App 1 — Signature Maker (DevForge)
Creates a reusable "signature bridge" snippet you can paste into other Streamlit apps.
Also exports the snippet as a JPG "code block" (light aqua) with name + date.
"""

import io
import os
from datetime import date

import streamlit as st
from PIL import Image, ImageDraw, ImageFont


# -----------------------------
# Helpers: fonts + code-to-JPG
# -----------------------------
def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    bold_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    regular_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    candidates = bold_candidates if bold else regular_candidates
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def code_block_to_jpeg(
    title: str,
    subtitle: str,
    code: str,
    bg_rgb=(201, 245, 243),        # light aqua
    header_rgb=(7, 77, 73),        # darker teal
    text_rgb=(9, 55, 52),          # deep teal
) -> bytes:
    W = 1400
    pad = 70
    header_h = 120

    font_header = _load_font(54, bold=True)
    font_sub = _load_font(34, bold=False)
    font_mono = _load_font(34, bold=False)

    tmp = Image.new("RGB", (W, 10), bg_rgb)
    dtmp = ImageDraw.Draw(tmp)
    max_text_w = W - 2 * pad - 70

    # Wrap code lines nicely
    lines = []
    for raw in code.splitlines():
        if raw.strip() == "":
            lines.append("")
            continue
        words = raw.split(" ")
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if dtmp.textlength(test, font=font_mono) <= max_text_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

    line_h = int(font_mono.size * 1.45)
    body_h = line_h * (len(lines) + 4)
    H = header_h + body_h + pad

    img = Image.new("RGB", (W, H), bg_rgb)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, W, header_h], fill=header_rgb)
    draw.text((pad, 30), title, font=font_header, fill=(240, 255, 254))

    # Subtitle
    draw.text((pad, header_h + 20), subtitle, font=font_sub, fill=text_rgb)

    # Code box
    box_y0 = header_h + 80
    box_x0 = pad
    box_x1 = W - pad
    box_y1 = H - pad
    box_bg = (230, 255, 254)
    draw.rounded_rectangle(
        [box_x0, box_y0, box_x1, box_y1],
        radius=28,
        fill=box_bg,
        outline=(120, 210, 205),
        width=4,
    )

    # Draw code
    x = box_x0 + 35
    y = box_y0 + 30
    for ln in lines:
        draw.text((x, y), ln, font=font_mono, fill=(20, 45, 45))
        y += line_h

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def signature_snippet(signature_value: str) -> str:
    # This snippet is intentionally minimal + paste-safe
    safe = signature_value.replace("\\", "\\\\").replace('"', '\\"')
    return f'''# DevForge Signature Bridge (paste into any Streamlit app)
import streamlit as st

# Shared signature across pages/apps
if "signature" not in st.session_state:
    st.session_state["signature"] = "{safe}"

sig = st.text_input("Signature", value=st.session_state.get("signature", ""))
st.session_state["signature"] = sig

# Read anywhere:
# dev_name = st.session_state.get("signature", "")
'''


# -----------------------------
# Streamlit page
# -----------------------------
st.set_page_config(page_title="Signature Maker", page_icon="✍️", layout="wide")

st.title("✍️ Signature Maker")
st.caption("Set a shared signature and export a paste-ready snippet (plus a code-block JPG).")

# Session defaults
if "signature" not in st.session_state:
    st.session_state["signature"] = ""

colA, colB = st.columns([1, 1])

with colA:
    st.subheader("1) Set signature")
    sig = st.text_input("Signature", value=st.session_state["signature"], placeholder="e.g., Ms. Piluso")
    st.session_state["signature"] = sig

    st.markdown("**Quick actions**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Use today's date tag"):
            st.session_state["signature"] = (st.session_state["signature"] + f" • {date.today().isoformat()}").strip()
            st.rerun()
    with c2:
        if st.button("Clear"):
            st.session_state["signature"] = ""
            st.rerun()

with colB:
    st.subheader("2) Output snippet")
    snippet = signature_snippet(st.session_state["signature"])
    st.code(snippet, language="python")

    # Download .py snippet
    st.download_button(
        "⬇️ Download snippet .py",
        data=snippet.encode("utf-8"),
        file_name="signature_bridge.py",
        mime="text/x-python",
        use_container_width=True,
    )

st.divider()

st.subheader("3) Export the snippet as a code-block JPG")
snippet_name = st.text_input("Snippet name (for the image header)", value="SIGNATURE SNIPPET")
today_str = date.today().isoformat()

img_title = f"{snippet_name.upper()} • {today_str}"
img_sub = "DevForge • paste-ready Streamlit snippet"

jpeg_bytes = code_block_to_jpeg(
    title=img_title,
    subtitle=img_sub,
    code=snippet,
    bg_rgb=(201, 245, 243),      # light aqua
    header_rgb=(7, 77, 73),      # darker teal
    text_rgb=(9, 55, 52),        # hunter-ish green text
)

st.image(jpeg_bytes, caption="Preview (JPG)")
st.download_button(
    "⬇️ Download code-block JPG",
    data=jpeg_bytes,
    file_name="SIGNATURE_BLOCK.jpeg",
    mime="image/jpeg",
    use_container_width=True,
)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)