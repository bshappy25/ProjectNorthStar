# pages/CSS_Editor.py
"""
DevForge — CSS Editor (Bulletproof Hybrid)

Preserves:
1) Override editor (session_state["custom_css"]) with Apply / Reset
2) Theme maker with premade palettes + minimal customization
   -> generates a safe :root variable block compatible with DevForge base CSS

No files. No exports. No JSON. No overlays. Commit-safe.
"""

from __future__ import annotations
import streamlit as st


# ---------------------------
# Session defaults (safe)
# ---------------------------
st.session_state.setdefault("custom_css", "")


# ---------------------------
# Simple palettes (hex only = bulletproof)
# ---------------------------
PALETTES = {
    "Universal Gray": {
        "bg": "#f3f4f6",
        "card": "#ffffff",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "accent2": "#16a34a",
    },
    "Science": {
        "bg": "#061B15",
        "card": "#0b2a22",
        "border": "#2bd4b7",
        "text": "#f9fafb",
        "muted": "#b6e7dd",
        "accent": "#14B8A6",
        "accent2": "#2F5BEA",
    },
    "Ink Violet": {
        "bg": "#0b0f19",
        "card": "#111a2b",
        "border": "#334a7a",
        "text": "#eef2ff",
        "muted": "#97a6c7",
        "accent": "#8b5cf6",
        "accent2": "#22d3ee",
    },
    "Blush": {
        "bg": "#fff4f6",
        "card": "#ffffff",
        "border": "#f2c7d2",
        "text": "#2a1020",
        "muted": "#7b4b61",
        "accent": "#d9467a",
        "accent2": "#2563eb",
    },
    "Bold": {
        "bg": "#0b0b0b",
        "card": "#111111",
        "border": "#2a2a2a",
        "text": "#f9fafb",
        "muted": "#a3a3a3",
        "accent": "#3b82f6",
        "accent2": "#f59e0b",
    },
}


# ---------------------------
# Helpers (defined BEFORE UI)
# ---------------------------
def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = (h or "").strip().lstrip("#")
    if len(h) == 3:  # #abc -> #aabbcc
        h = "".join([c * 2 for c in h])
    if len(h) != 6:
        return (17, 24, 39)  # fallback
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        return (17, 24, 39)

def _is_dark(hex_bg: str) -> bool:
    r, g, b = _hex_to_rgb(hex_bg)
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return lum < 130

def _vars_block(p: dict) -> str:
    # Keep this strictly to DevForge variables you already use
    return f"""
/* --- DevForge Theme Maker (generated) --- */
:root {{
  --bg: {p["bg"]};
  --card: {p["card"]};
  --border: {p["border"]};
  --text: {p["text"]};
  --muted: {p["muted"]};
  --accent: {p["accent"]};
  --accent2: {p["accent2"]};
}}
""".strip()


# ---------------------------
# UI
# ---------------------------
st.title("🎨 CSS Editor")
st.caption("Overrides + Theme Maker (simple, commit-safe).")

tab_overrides, tab_theme = st.tabs(["✍️ Overrides", "🎛️ Theme Maker"])


# ---------------------------
# Tab 1: Overrides (preserved behavior)
# ---------------------------
with tab_overrides:
    st.subheader("App-wide CSS Overrides")
    st.caption("This writes to `st.session_state['custom_css']` (DevForge injects it after base CSS).")

    current = st.session_state.get("custom_css", "")

    edited = st.text_area(
        "Custom CSS",
        value=current,
        height=360,
        placeholder="/* Paste overrides here */\n.dev-card{ border-color: var(--accent) !important; }\n",
        key="css_editor_override_text",
    )

    c1, c2, c3 = st.columns([1, 1, 2.6])

    with c1:
        if st.button("Apply", type="primary", use_container_width=True):
            st.session_state["custom_css"] = (edited or "").strip()
            st.success("Applied.")
            st.rerun()

    with c2:
        if st.button("Reset", use_container_width=True):
            st.session_state["custom_css"] = ""
            st.success("Reset.")
            st.rerun()

    with c3:
        st.caption("Preview")
        st.markdown(
            """
            <div class="dev-card">
              <h3>Preview Card</h3>
              <p class="muted">If your overrides affect <code>.dev-card</code>, badges, buttons, you’ll see it here.</p>
              <span class="badge badge-accent">Accent</span>
              <span class="badge badge-accent2">Accent2</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------
# Tab 2: Theme Maker (premade palettes + minimal customization)
# ---------------------------
with tab_theme:
    st.subheader("Theme Maker (Premade Palettes)")
    st.caption("Pick a palette, optionally tweak a few colors, then Replace or Append into overrides.")

    pal_name = st.selectbox("Palette", list(PALETTES.keys()), index=0)
    base = PALETTES[pal_name].copy()

    # Minimal customization: just BG + Accent (and auto text/muted if you want)
    colA, colB, colC = st.columns([1, 1, 1])

    with colA:
        bg = st.color_picker("Background (bg)", base["bg"])
    with colB:
        accent = st.color_picker("Accent", base["accent"])
    with colC:
        accent2 = st.color_picker("Accent2", base["accent2"])

    auto = st.toggle("Auto text/muted for readability", value=True)

    # Build final palette (hex-only)
    out = base
    out["bg"] = bg
    out["accent"] = accent
    out["accent2"] = accent2

    if auto:
        if _is_dark(out["bg"]):
            out["text"] = "#f9fafb"
            out["muted"] = "#a3a3a3"
            out["card"] = "#111827"   # safe dark surface
            out["border"] = "#334155" # safe dark border
        else:
            out["text"] = "#111827"
            out["muted"] = "#6b7280"
            out["card"] = "#ffffff"
            out["border"] = "#d1d5db"

    theme_css = _vars_block(out)

    st.markdown("**Generated CSS (copy/paste if you want):**")
    st.code(theme_css, language="css")

    b1, b2, b3 = st.columns([1, 1, 2.6])

    with b1:
        if st.button("Replace Overrides", type="primary", use_container_width=True):
            st.session_state["custom_css"] = theme_css
            st.success("Overrides replaced with theme variables.")
            st.rerun()

    with b2:
        if st.button("Append to Overrides", use_container_width=True):
            cur = (st.session_state.get("custom_css", "") or "").strip()
            joiner = "\n\n" if cur else ""
            st.session_state["custom_css"] = cur + joiner + theme_css
            st.success("Theme variables appended.")
            st.rerun()

    with b3:
        st.caption("Preview")
        st.markdown(
            """
            <div class="dev-card">
              <h3>Theme Preview</h3>
              <p class="muted">This preview uses your DevForge variables: <code>--bg</code>, <code>--card</code>, <code>--accent</code>.</p>
              <span class="badge badge-accent">Accent</span>
              <span class="badge badge-accent2">Accent2</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Bottom spacer so DevForge ticker doesn’t overlap
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)