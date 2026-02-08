# -*- coding: utf-8 -*-
"""
DevForge – Block Library (Production Grade)
Universal Gray • Admin Gate • Color-Coded Blocks • Bannered JPEG/PNG Export
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
# COLOR SEMANTICS (YOUR CONTRACT)
# =====================

ROLE_META = {
    "Unassigned (Light Grey)": {
        "key": "unassigned",
        "hex": "#E5E7EB",
        "label": "UNASSIGNED",
        "hint": "Neutral / placeholder / read-only info.",
    },
    "Overrides • Access • Gateways (Green)": {
        "key": "gateway",
        "hex": "#22C55E",
        "label": "GATEWAY",
        "hint": "Overrides, access panels, gateways.",
    },
    "Clears • Resets • Reboots • CLOCK IT (Red)": {
        "key": "terminal",
        "hex": "#EF4444",
        "label": "RESET/CLOCK",
        "hint": "Clears, resets, reboots, end-operation codes.",
    },
    "Uploads • Downloads • In-app Mods (Light Blue)": {
        "key": "transfer",
        "hex": "#60A5FA",
        "label": "TRANSFER",
        "hint": "Uploads/downloads + safe in-app modifications.",
    },
    "CSS • UI Changes (Yellow)": {
        "key": "ui",
        "hex": "#F59E0B",
        "label": "UI/CSS",
        "hint": "CSS/UI-only changes (presentation layer).",
    },
    "Full Ops • Major Sections (Purple)": {
        "key": "ops",
        "hex": "#A855F7",
        "label": "OPERATIONS",
        "hint": "Full operations, major sections, core workflows.",
    },
}

CODE_FORMATS = ["python", "html", "css", "javascript", "json", "markdown", "text"]

def now_utc_date():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")

# =====================
# SESSION STATE
# =====================

for k, v in {
    "palm_taps": 0,
    "show_admin_box": False,
    "admin_unlocked": False,
}.items():
    st.session_state.setdefault(k, v)

# =====================
# CSS (UNIVERSAL GRAY + ROLE COLORS)
# =====================

st.markdown(
    """<style>
:root{
  --bg:#f3f4f6;--surface:#ffffff;--surface2:#f8fafc;--border:#d1d5db;
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
  position:relative;
}
.cardbar{
  height:10px;
  border-radius:12px;
  margin:-6px -6px 12px -6px;
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
.badge2{
  padding:6px 10px;border-radius:999px;
  border:1px solid var(--border);
  background:#f1f5f9;font-size:.8rem;color:var(--muted);
}
.code{
  background:#fdfdfd;border:1px dashed var(--border);
  border-radius:14px;padding:14px;white-space:pre-wrap;
  font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size:.92rem;
  overflow:auto;
}
.smallmuted{color:var(--muted); font-size:.85rem;}
.hr{height:1px;background:rgba(0,0,0,.06);margin:12px 0;}
</style>""",
    unsafe_allow_html=True,
)

# =====================
# IMAGE EXPORT (WITH BANNER + META BOX)
# =====================

def _safe_font(mono=True, size=20):
    # Prefer a mono font for code rendering
    try:
        if mono:
            return ImageFont.truetype("DejaVuSansMono.ttf", size)
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

def block_to_image(
    code: str,
    *,
    title: str = "DevForge Block",
    role_color: str = "#E5E7EB",
    code_format: str = "text",
    date_str: str = "",
    fmt: str = "JPEG",
    bg: str = "#FFFFFF",
    fg: str = "#111827",
):
    """
    Produces a bannered image:
    - Top banner: title (left) + meta box (right: date + format)
    - Colored role stripe under banner
    - Code body
    """
    padding = 28
    font_size = 20
    wrap = 92

    if not date_str:
        date_str = now_utc_date()

    # Wrap code
    lines = []
    for l in code.splitlines():
        lines += textwrap.wrap(l, wrap) or [""]

    mono = _safe_font(mono=True, size=font_size)
    ui = _safe_font(mono=False, size=18)
    ui_bold = _safe_font(mono=False, size=22)

    # Measure line height
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    lh = d.textbbox((0, 0), "Ag", font=mono)[3] + 7

    # Measure code width
    code_w = 0
    for l in lines:
        code_w = max(code_w, d.textbbox((0, 0), l, font=mono)[2])

    # Banner sizing
    banner_h = 88
    stripe_h = 10
    meta_w = 240

    # Total image size
    w = max(code_w + padding * 2, 920)
    w = w + meta_w  # space for meta box on right without squeezing title
    h = banner_h + stripe_h + (lh * max(1, len(lines))) + padding * 2 + 10

    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    # Banner background
    banner_bg = "#F8FAFC"
    banner_border = "#D1D5DB"
    draw.rounded_rectangle((14, 14, w - 14, 14 + banner_h), radius=18, fill=banner_bg, outline=banner_border, width=2)

    # Title text (left)
    title_x = 34
    title_y = 24
    draw.text((title_x, title_y), title, font=ui_bold, fill="#111827")
    draw.text((title_x, title_y + 34), "DevForge • Bannered Export", font=ui, fill="#6B7280")

    # Meta box (right)
    box_x2 = w - 34
    box_x1 = box_x2 - meta_w
    box_y1 = 26
    box_y2 = 14 + banner_h - 12
    draw.rounded_rectangle((box_x1, box_y1, box_x2, box_y2), radius=16, fill="#FFFFFF", outline=banner_border, width=2)

    # Meta contents
    draw.text((box_x1 + 16, box_y1 + 10), f"DATE: {date_str}", font=ui, fill="#111827")
    draw.text((box_x1 + 16, box_y1 + 34), f"FORMAT: {code_format.lower()}", font=ui, fill="#111827")
    draw.text((box_x1 + 16, box_y1 + 58), f"EXPORT: {fmt.upper()}", font=ui, fill="#6B7280")

    # Role stripe
    stripe_y1 = 14 + banner_h + 8
    draw.rounded_rectangle((14, stripe_y1, w - 14, stripe_y1 + stripe_h), radius=10, fill=role_color, outline=None)

    # Code area background
    code_top = stripe_y1 + stripe_h + 16
    code_left = 14
    code_right = w - 14
    code_bottom = h - 14
    draw.rounded_rectangle((code_left, code_top, code_right, code_bottom), radius=18, fill="#FFFFFF", outline=banner_border, width=2)

    # Code text
    y = code_top + 18
    x = code_left + 22
    for l in lines:
        draw.text((x, y), l, font=mono, fill=fg)
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
        try:
            blocks.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            # Skip malformed files safely
            continue
    return sorted(blocks, key=lambda x: x.get("created", ""), reverse=True)

def save_block(data):
    (BLOCKS_DIR / f"{data['id']}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

def delete_block(block_id):
    p = BLOCKS_DIR / f"{block_id}.json"
    if p.exists():
        p.unlink()

def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    keep = []
    for ch in s:
        if ch.isalnum() or ch in ("_", "-"):
            keep.append(ch)
        elif ch.isspace():
            keep.append("_")
    out = "".join(keep).strip("_")
    return out or f"block_{int(datetime.datetime.utcnow().timestamp())}"

# =====================
# HEADER + PALM ID
# =====================

left, right = st.columns([0.9, 0.1])
with left:
    st.title("🧱 DevForge Blocks")
    st.caption("Production-grade block library • Role colors • Bannered exports • Admin-gated delete")
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
        if st.button("Reset Palm"):
            st.session_state.palm_taps = 0
            st.session_state.show_admin_box = False

if st.session_state.admin_unlocked:
    st.caption("✅ Palm ID unlocked (Delete enabled)")

st.divider()

# =====================
# SIDEBAR FILTERS
# =====================

with st.sidebar:
    st.header("Filters")
    role_filter = st.selectbox("Role", ["All"] + list(ROLE_META.keys()), index=0)
    fmt_filter = st.selectbox("Code format", ["All"] + CODE_FORMATS, index=0)
    query = st.text_input("Search title/tags")

# =====================
# CREATE BLOCK
# =====================

with st.expander("➕ Create New Block", expanded=False):
    cA, cB = st.columns([0.62, 0.38])
    with cA:
        title = st.text_input("Block title", placeholder="e.g., Upload Panel v1")
        tags = st.text_input("Tags (comma separated)", placeholder="e.g., upload, portal, v1")
    with cB:
        role_name = st.selectbox(
            "Role color",
            list(ROLE_META.keys()),
            index=0,
            help="Your contract: green gateway, red reset/clock, blue transfer, yellow ui/css, purple ops, grey unassigned.",
        )
        code_format = st.selectbox("Code format", CODE_FORMATS, index=0)

    code = st.text_area("Code", height=220)

    c1, c2 = st.columns([0.5, 0.5])
    with c1:
        if st.button("Save block"):
            if not (title or "").strip():
                st.error("Block title is required.")
            else:
                meta = ROLE_META[role_name]
                data = {
                    "id": slugify(title),
                    "title": title.strip(),
                    "tags": [t.strip() for t in (tags or "").split(",") if t.strip()],
                    "code": code or "",
                    "role_name": role_name,
                    "role_key": meta["key"],
                    "role_hex": meta["hex"],
                    "code_format": (code_format or "text").lower(),
                    "created": datetime.datetime.utcnow().isoformat(),
                }
                save_block(data)
                st.success("Block saved")
    with c2:
        st.markdown(
            f"<div class='smallmuted'><b>Role meaning:</b> {ROLE_META[role_name]['hint']}</div>",
            unsafe_allow_html=True,
        )

# =====================
# BLOCK LIST
# =====================

blocks = load_blocks()

def _matches(b):
    # role filter
    if role_filter != "All" and b.get("role_name") != role_filter:
        return False
    # format filter
    if fmt_filter != "All" and (b.get("code_format") or "").lower() != fmt_filter:
        return False
    # query filter
    q = (query or "").strip().lower()
    if q:
        hay = " ".join([
            (b.get("title") or ""),
            " ".join(b.get("tags") or []),
            (b.get("role_name") or ""),
            (b.get("code_format") or ""),
        ]).lower()
        if q not in hay:
            return False
    return True

filtered = [b for b in blocks if _matches(b)]

st.subheader(f"Library ({len(filtered)} shown / {len(blocks)} total)")

# One optional system rule: only one red block per tool view
# (Not enforced here — this is a library; you enforce it when assembling tools.)

for b in filtered:
    role_hex = b.get("role_hex", "#E5E7EB")
    role_name = b.get("role_name", "Unassigned (Light Grey)")
    code_format = (b.get("code_format") or "text").lower()

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='cardbar' style='background:{role_hex};'></div>", unsafe_allow_html=True)

        tags_txt = ", ".join(b.get("tags") or []) or "—"
        st.markdown(
            f"<div class='row'>"
            f"<div>"
            f"<div style='font-size:1.05rem; font-weight:900;'>{b.get('title','(untitled)')}</div>"
            f"<div class='smallmuted'>{b.get('created','')[:19].replace('T',' ')}</div>"
            f"</div>"
            f"<div style='display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;'>"
            f"<span class='badge2'>{role_name}</span>"
            f"<span class='badge'>{code_format}</span>"
            f"<span class='badge2'>{tags_txt}</span>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(f"<div class='code'>{(b.get('code') or '').replace('<','&lt;').replace('>','&gt;')}</div>", unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns([0.18, 0.18, 0.22, 0.22, 0.20])

        with c1:
            st.download_button(
                "📸 JPEG",
                block_to_image(
                    b.get("code", ""),
                    title=b.get("title", "DevForge Block"),
                    role_color=role_hex,
                    code_format=code_format,
                    date_str=now_utc_date(),
                    fmt="JPEG",
                ),
                f"{b.get('id','block')}.jpg",
                "image/jpeg",
            )
        with c2:
            st.download_button(
                "🖼️ PNG",
                block_to_image(
                    b.get("code", ""),
                    title=b.get("title", "DevForge Block"),
                    role_color=role_hex,
                    code_format=code_format,
                    date_str=now_utc_date(),
                    fmt="PNG",
                ),
                f"{b.get('id','block')}.png",
                "image/png",
            )
        with c3:
            md = f"```{code_format}\n{b.get('code','')}\n```"
            st.download_button(
                "📋 Copy (MD)",
                md,
                f"{b.get('id','block')}.md",
                "text/markdown",
            )
        with c4:
            st.download_button(
                "💾 Raw code",
                b.get("code", ""),
                f"{b.get('id','block')}.{('txt' if code_format=='text' else code_format)}",
                "text/plain",
            )
        with c5:
            if st.session_state.admin_unlocked:
                if st.button("❌ Delete", key=f"del_{b.get('id','block')}"):
                    delete_block(b.get("id", ""))
                    st.rerun()
            else:
                st.caption("Delete is admin-only")

        st.markdown("</div>", unsafe_allow_html=True)

# =====================
# EXPORT ALL
# =====================

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

if blocks:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for b in blocks:
            fmt = (b.get("code_format") or "text").lower()
            ext = "txt" if fmt == "text" else fmt
            z.writestr(f"{b.get('id','block')}.{ext}", b.get("code", ""))
            # Also include a markdown wrapper for easy paste into docs
            z.writestr(f"{b.get('id','block')}.md", f"```{fmt}\n{b.get('code','')}\n```")
    st.download_button("📦 Export all blocks (ZIP)", buf.getvalue(), "devforge_blocks.zip")
else:
    st.info("No blocks yet. Create your first block above.")