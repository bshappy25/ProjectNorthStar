# pages/CSS_Editor.py
"""
DevForge — CSS Editor (Hybrid, Simple)

Keeps v1 functionality:
- Edit + apply Streamlit CSS overrides via st.session_state["custom_css"]

Adds v2 ease-of-use:
- Premade palettes (CSS variables)
- Light customization (tweak a few key colors)
- One-click "Add to Overrides" or "Replace Overrides"
"""

from __future__ import annotations

import streamlit as st

# ---------------------------
# Premade Palettes (simple)
# ---------------------------
PALETTES = {
    "Universal Gray": {
        "bg": "#f3f4f6",
        "card": "rgba(255,255,255,0.92)",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "accent2": "#16a34a",
    },
    "Science Glass": {
        "bg": "#061B15",
        "card": "rgba(255,255,255,0.08)",
        "border": "rgba(120,255,220,0.30)",
        "text": "rgba(255,255,255,0.92)",
        "muted": "rgba(255,255,255,0.74)",
        "accent": "#14B8A6",
        "accent2": "#2F5BEA",
    },
    "Ink Violet": {
        "bg": "#0b0f19",
        "card": "rgba(255,255,255,0.07)",
        "border": "rgba(139,92,246,0.35)",
        "text": "rgba(255,255,255,0.92)",
        "muted": "rgba(255,255,255,0.72)",
        "accent": "#8b5cf6",
        "accent2": "#22d3ee",
    },
    "Blush": {
        "bg": "#fff4f6",
        "card": "rgba(255,255,255,0.92)",
        "border": "#f2c7d2",
        "text": "#2a1020",
        "muted": "#7b4b61",
        "accent": "#d9467a",
        "accent2": "#2563eb",
    },
    "Bold": {
        "bg": "#0b0b0b",
        "card": "rgba(255,255,255,0.06)",
        "border": "rgba(255,255,255,0.14)",
        "text": "rgba(255,255,255,0.92)",
        "muted": "rgba(255,255,255,0.65)",
        "accent": "#3b82f6",
        "accent2": "#f59e0b",
    },
}

def css_vars_block(p: dict) -> str:
    """Returns a small :root variable block compatible with DevForge base CSS."""
    return f"""
/* --- DevForge Palette Variables (generated) --- */
:root {{
  --bg: {p["bg"]};
  --card: {p["card"]};
  --border: {p["border"]};
  --text: {p["text"]};
  --muted: {p["muted"]};
  --accent: {p["accent"]};
  --accent2: {p["accent2"]};
}}
/* Optional: quick emphasis tweaks */
.dev-card h3 {{ color: var(--accent) !important; }}
.badge-accent {{ border-color: var(--accent) !important; color: var(--accent) !important; }}
.badge-accent2 {{ border-color: var(--accent2) !important; color: var(--accent2) !important; }}
""".strip()

# ---------------------------
# Page UI
# ---------------------------
st.title("🎨 CSS Editor (Hybrid)")
st.caption("Simple palettes + customization → writes into DevForge custom_css overrides.")

tab_quick, tab_palette = st.tabs(["✍️ Quick Overrides", "🎛️ Palette Builder"])

# ---------------------------
# TAB 1: Quick Overrides (v1 functionality)
# ---------------------------
with tab_quick:
    st.subheader("App-wide CSS Overrides")
    st.caption("This is the active override text DevForge injects after the base theme.")

    current_css = st.session_state.get("custom_css", "")
    edited_css = st.text_area(
        "Custom CSS",
        value=current_css,
        height=360,
        placeholder="/* Paste overrides here. */\n.dev-card { border-color: var(--accent) !important; }\n",
        key="css_editor_text",
    )

    c1, c2, c3 = st.columns([1, 1, 2.5])

    with c1:
        if st.button("Apply", type="primary", use_container_width=True):
            st.session_state["custom_css"] = (edited_css or "").strip()
            st.success("Applied to session_state['custom_css'].")
            st.rerun()

    with c2:
        if st.button("Reset", use_container_width=True):
            st.session_state.pop("custom_css", None)
            st.success("Removed custom_css.")
            st.rerun()

    with c3:
        st.caption("Preview block")
        st.markdown(
            """
            <div class="dev-card">
              <h3>Preview Card</h3>
              <p class="muted">If your overrides target <code>.dev-card</code>, buttons, badges, etc. you'll see changes.</p>
              <span class="badge badge-accent">Accent</span>
              <span class="badge badge-accent2">Accent2</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------
# TAB 2: Palette Builder (easy mode)
# ---------------------------
with tab_palette:
    st.subheader("Premade Palettes + Simple Customization")
    st.caption("Pick a palette → optionally tweak a few colors → add into your overrides.")

    # Choose palette
    pal_name = st.selectbox("Palette", list(PALETTES.keys()), index=0)
    base = PALETTES[pal_name].copy()

    # Light customization
    st.markdown("**Optional tweaks** (keep it simple):")
    colA, colB, colC = st.columns(3)

    with colA:
        base["bg"] = st.color_picker("BG", value=_safe_hex(base["bg"]) if isinstance(base["bg"], str) and base["bg"].startswith("#") else "#111111")
        base["accent"] = st.color_picker("Accent", value=_safe_hex(base["accent"]))
    with colB:
        base["text"] = st.color_picker("Text", value=_safe_hex(base["text"]) if isinstance(base["text"], str) and base["text"].startswith("#") else "#ffffff")
        base["accent2"] = st.color_picker("Accent2", value=_safe_hex(base["accent2"]))
    with colC:
        # border/card may be rgba; keep as text edits (simple + flexible)
        base["card"] = st.text_input("Card (rgba or hex)", value=str(base["card"]))
        base["border"] = st.text_input("Border (rgba or hex)", value=str(base["border"]))

    palette_css = css_vars_block(base)

    st.markdown("**Generated CSS**")
    st.code(palette_css, language="css")

    b1, b2, b3 = st.columns([1, 1, 2.5])

    with b1:
        if st.button("Replace Overrides with Palette", type="primary", use_container_width=True):
            st.session_state["custom_css"] = palette_css
            st.success("custom_css replaced with generated palette CSS.")
            st.rerun()

    with b2:
        if st.button("Append Palette to Overrides", use_container_width=True):
            current = st.session_state.get("custom_css", "").strip()
            joiner = "\n\n" if current else ""
            st.session_state["custom_css"] = current + joiner + palette_css
            st.success("Palette CSS appended to custom_css.")
            st.rerun()

    with b3:
        st.caption("Preview block")
        st.markdown(
            """
            <div class="dev-card">
              <h3>Palette Preview</h3>
              <p class="muted">This uses DevForge variables: <code>--bg</code>, <code>--card</code>, <code>--accent</code>.</p>
              <span class="badge badge-accent">Accent</span>
              <span class="badge badge-accent2">Accent2</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# bottom spacing so ticker doesn't overlap
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# ---------------------------
# Helpers
# ---------------------------
def _safe_hex(x: str) -> str:
    """Return a safe hex string for color_picker; fallback if input is rgba."""
    if isinstance(x, str) and x.startswith("#") and len(x) in (4, 7):
        return x
    return "#2563eb"