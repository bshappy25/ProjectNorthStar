# -*- coding: utf-8 -*-
"""
DevForge – Admin Tools + Code Card Export
Boomer-proof. Pretty. Safe.
"""

import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

# =====================
# CONFIG
# =====================

st.set_page_config(page_title="DevForge Admin", page_icon="🛠️", layout="wide")

TOOLS_DIR = Path("tools")
TOOLS_DIR.mkdir(exist_ok=True)

ADMIN_CODE = "Bshapp"

# =====================
# SESSION STATE INIT
# =====================

defaults = {
    "palm_taps": 0,
    "show_admin_box": False,
    "admin_unlocked": False,
    "current_tool": None,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# =====================
# CODE → JPEG EXPORT
# =====================

def code_to_jpeg(code: str, bg="#FDF1F0", fg="#3A1A1A"):
    font_size = 20
    padding = 30
    max_width = 80

    wrapped = []
    for line in code.splitlines():
        wrapped.extend(textwrap.wrap(line, max_width) or [""])

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except:
        font = ImageFont.load_default()

    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    line_height = d.textbbox((0, 0), "Ag", font=font)[3] + 6

    width = max(d.textbbox((0, 0), line, font=font)[2] for line in wrapped) + padding * 2
    height = line_height * len(wrapped) + padding * 2

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in wrapped:
        draw.text((padding, y), line, font=font, fill=fg)
        y += line_height

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# =====================
# DELETE TOOL
# =====================

def delete_tool(name):
    path = TOOLS_DIR / f"{name}.html"
    if path.exists():
        path.unlink()
        st.session_state["current_tool"] = None
        st.success(f"🗑️ {name} deleted.")

# =====================
# HEADER + PALM ID
# =====================

left, right = st.columns([0.88, 0.12], vertical_alignment="center")

with left:
    st.title("🛠️ DevForge")

with right:
    if st.button("✋", help="Palm ID (tap 3x)"):
        st.session_state["palm_taps"] += 1
        if st.session_state["palm_taps"] >= 3:
            st.session_state["show_admin_box"] = True

# =====================
# ADMIN GATE
# =====================

if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
    st.markdown("### 🔐 Palm ID – Admin Access")
    code_try = st.text_input("Admin Code", type="password", placeholder="Enter code…")

    colA, colB = st.columns(2)
    with colA:
        if st.button("Unlock"):
            if code_try == ADMIN_CODE:
                st.session_state["admin_unlocked"] = True
                st.success("Admin unlocked.")
            else:
                st.error("Incorrect code.")
    with colB:
        if st.button("Reset"):
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False

if st.session_state["admin_unlocked"]:
    st.caption("✅ Palm ID: unlocked")

st.divider()

# =====================
# TOOL PICKER (DEMO)
# =====================

tools = [p.stem for p in TOOLS_DIR.glob("*.html")]
tool = st.selectbox("Select tool", tools or ["(none)"])

st.session_state["current_tool"] = tool if tool != "(none)" else None

# =====================
# CODE CARD
# =====================

demo_code = """def hello_world():
    print("Hello, DevForge 👋")
"""

st.markdown(
    """
    <style>
    .code-card {
        background:#FDF1F0;
        border:2px solid #E7B3AE;
        border-radius:18px;
        padding:24px;
        font-family:monospace;
        white-space:pre;
        color:#3A1A1A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"<div class='code-card'>{demo_code}</div>", unsafe_allow_html=True)

# =====================
# EXPORT OPTIONS
# =====================

jpeg_bytes = code_to_jpeg(demo_code)

col1, col2 = st.columns([0.8, 0.2])

with col2:
    st.download_button(
        "📸 Export JPEG",
        data=jpeg_bytes,
        file_name="code_card.jpg",
        mime="image/jpeg",
    )

# =====================
# DELETE (ADMIN ONLY)
# =====================

if st.session_state["admin_unlocked"] and st.session_state["current_tool"]:
    st.divider()
    st.markdown("### ⚠️ Admin Tools")

    colA, colB = st.columns([0.85, 0.15])
    with colB:
        if st.button("❌", help="Delete tool"):
            delete_tool(st.session_state["current_tool"])
