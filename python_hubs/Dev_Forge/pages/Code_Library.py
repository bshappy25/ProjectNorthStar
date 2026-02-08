# -*- coding: utf-8 -*-
"""
DevForge – Block Library (Production Grade)
Universal Gray • Admin Gate • JPEG/PNG Export
"""

import streamlit as st
from pathlib import Path
import json, io, zipfile, textwrap, datetime
from PIL import Image, ImageDraw, ImageFont

# =====================
# CONFIG
# =====================

st.set_page_config(page_title="DevForge Blocks", page_icon="🧱", layout="wide")

BLOCKS_DIR = Path("blocks")
EXPORT_DIR = Path("exports")
BLOCKS_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

ADMIN_CODE = "Bshapp"

# =====================
# SESSION STATE
# =====================

for k, v in {
    "palm_taps": 0,
    "show_admin_box": False,
    "admin_unlocked": False,
    "confirm_delete": False,
}.items():
    st.session_state.setdefault(k, v)

# =====================
# CSS (UNIVERSAL GRAY)
# =====================

st.markdown(
    """<style>
:root {
  --bg:#f3f4f6;--surface:#fff;--surface2:#f8fafc;--border:#d1d5db;
  --text:#111827;--muted:#6b7280;--accent:#2563eb;
  --radius:18px;--pad:14px;--shadow:0 8px 24px rgba(0,0,0,.12);
  --font:'Comic Sans MS','Chalkboard SE','Comic Neue',cursive,sans-serif;
}
html,body,[data-testid="stAppViewContainer"]{
  background:var(--bg);color:var(--text);
  font-family:var(--font);font-weight:900;
}
.card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:var(--pad);
  box-shadow:var(--shadow);
  margin-bottom:16px;
}
.row{
  display:flex;justify-content:space-between;align-items:center;gap:12px;
  border:1px solid var(--border);
  background:var(--surface2);
  border-radius:14px;padding:10px 12px;
}
.badge{
  padding:6px 10px;border-radius:999px;
  border:1px solid var(--border);
  background:#e5edff;font-size:.8rem;
}
.code{
  background:#fdfdfd;border:1px dashed var(--border);
  border-radius:14px;padding:14px;white-space:pre;
  font-family:monospace;font-size:.9rem;
}
</style>""",
    unsafe_allow_html=True,
)

# =====================
# IMAGE EXPORT
# =====================

def block_to_image(code, bg="#ffffff", fg="#111827", fmt="JPEG"):
    padding = 28
    font_size = 20
    wrap = 88

    lines = []
    for l in code.splitlines():
        lines += textwrap.wrap(l, wrap) or [""]

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except:
        font = ImageFont.load_default()

    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    lh = d.textbbox((0, 0), "Ag", font=font)[3] + 6

    w = max(d.textbbox((0, 0), l, font=font)[2] for l in lines) + padding * 2
    h = lh * len(lines) + padding * 2

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    y = padding
    for l in lines:
        draw.text((padding, y), l, font=font, fill=fg)
        y += lh

    buf = io.BytesIO()
    img.save(buf, format=fmt, quality=95)
    return buf.getvalue()

# =====================
# DATA
# =====================

def load_blocks():
    blocks = []
    for p in BLOCKS_DIR.glob("*.json"):
        blocks.append(json.loads(p.read_text()))
    return sorted(blocks, key=lambda x: x["created"], reverse=True)

def save_block(data):
    (BLOCKS_DIR / f"{data['id']}.json").write_text(json.dumps(data, indent=2))

def delete_block(block_id):
    p = BLOCKS_DIR / f"{block_id}.json"
    if p.exists():
        p.unlink()

# =====================
# HEADER + PALM ID
# =====================

left, right = st.columns([0.9, 0.1])
with left:
    st.title("🧱 DevForge Blocks")
with right:
    if st.button("✋", help="Palm ID (tap 3x)"):
        st.session_state.palm_taps += 1
        if st.session_state.palm_taps >= 3:
            st.session_state.show_admin_box = True

# =====================
# ADMIN GATE
# =====================

if st.session_state.show_admin_box and not st.session_state.admin_unlocked:
    st.markdown("### 🔐 Admin Access")
    code = st.text_input("Admin Code", type="password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Unlock") and code == ADMIN_CODE:
            st.session_state.admin_unlocked = True
            st.success("Admin unlocked")
    with c2:
        if st.button("Reset"):
            st.session_state.palm_taps = 0
            st.session_state.show_admin_box = False

if st.session_state.admin_unlocked:
    st.caption("✅ Palm ID unlocked")

st.divider()

# =====================
# CREATE BLOCK
# =====================

with st.expander("➕ Create New Block", expanded=False):
    title = st.text_input("Block title")
    tags = st.text_input("Tags (comma separated)")
    code = st.text_area("Code", height=180)
    if st.button("Save block"):
        data = {
            "id": title.lower().replace(" ", "_"),
            "title": title,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "code": code,
            "created": datetime.datetime.utcnow().isoformat(),
        }
        save_block(data)
        st.success("Block saved")

# =====================
# BLOCK LIST
# =====================

blocks = load_blocks()

for b in blocks:
    with st.container():
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)

        st.markdown(
            f"<div class='row'><strong>{b['title']}</strong>"
            f"<span class='badge'>{', '.join(b['tags'])}</span></div>",
            unsafe_allow_html=True,
        )

        st.markdown(f"<div class='code'>{b['code']}</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.download_button(
                "📸 JPEG",
                block_to_image(b["code"], fmt="JPEG"),
                f"{b['id']}.jpg",
                "image/jpeg",
            )
        with c2:
            st.download_button(
                "🖼️ PNG",
                block_to_image(b["code"], fmt="PNG"),
                f"{b['id']}.png",
                "image/png",
            )
        with c3:
            st.download_button(
                "📋 Copy",
                f"```python\n{b['code']}\n```",
                f"{b['id']}.md",
            )
        with c4:
            if st.session_state.admin_unlocked:
                if st.button("❌ Delete", key=b["id"]):
                    delete_block(b["id"])
                    st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# =====================
# EXPORT ALL
# =====================

if blocks:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for b in blocks:
            z.writestr(f"{b['id']}.md", b["code"])
    st.download_button("📦 Export all blocks (ZIP)", buf.getvalue(), "blocks.zip")
