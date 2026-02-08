"""
my_app2.py — Simplified HTML Viewer (DevForge Tester App)

Includes:
- PORTAL Viewing Window (TV frame + scanlines + glow)
- PALM ID Admin Gate (tap 3x → password unlock)
- EASY X Delete Tool (admin-only delete selected HTML tool)

Expected folder:
- tools_html/   (contains .html files)
"""

from __future__ import annotations

import html
from pathlib import Path
from datetime import date

import streamlit as st
import streamlit.components.v1 as components


# =====================
# CONFIG
# =====================

TOOLS_DIR = Path(__file__).parent / "tools_html"   # put your .html files here
TOOLS_DIR.mkdir(exist_ok=True)

ADMIN_CODE = "Bshapp"  # PALM ID code


# =====================
# HELPERS
# =====================

def list_tools() -> list[str]:
    return sorted([p.stem for p in TOOLS_DIR.glob("*.html")])


def load_tool(tool_name: str) -> str | None:
    p = TOOLS_DIR / f"{tool_name}.html"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="ignore")
    return None


def delete_tool(tool_name: str) -> bool:
    p = TOOLS_DIR / f"{tool_name}.html"
    if p.exists():
        p.unlink()
        return True
    return False


def portal_view(tool_html: str, border: str = "rgba(20,184,166,0.65)") -> None:
    """
    Render the HTML in a "portal" TV-style frame using sandboxed iframe + srcdoc.
    """
    escaped = html.escape(tool_html, quote=True)

    combined = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {{ --border: {border}; }}

  body {{
    margin: 0;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  }}

  .tv-frame {{
    position: relative;
    width: 100%;
    height: 820px;
    border: 3px solid var(--border);
    border-radius: 20px;
    overflow: hidden;
    background: rgba(0,0,0,0.05);
    box-shadow:
      0 0 40px rgba(20,184,166,0.20),
      inset 0 0 60px rgba(20,184,166,0.05);
  }}

  .tv-frame:before {{
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(255,255,255,0.03) 2px,
      rgba(255,255,255,0.03) 4px
    );
    pointer-events: none;
    z-index: 2;
    animation: scanlines 8s linear infinite;
  }}

  @keyframes scanlines {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(4px); }}
  }}

  .tv-frame:after {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(20,184,166,0.12) 0%, transparent 55%);
    pointer-events: none;
    z-index: 1;
    animation: glow 4s ease-in-out infinite alternate;
  }}

  @keyframes glow {{
    0% {{ opacity: 0.25; }}
    100% {{ opacity: 0.65; }}
  }}

  .screen {{
    position: relative;
    z-index: 3;
    width: 100%;
    height: 100%;
  }}

  iframe {{
    width: 100%;
    height: 100%;
    border: 0;
    background: white;
  }}
</style>
</head>
<body>
  <div class="tv-frame">
    <div class="screen">
      <iframe
        sandbox="allow-scripts allow-forms allow-popups allow-modals allow-downloads"
        srcdoc="{escaped}">
      </iframe>
    </div>
  </div>
</body>
</html>
"""
    components.html(combined, height=860, scrolling=False)


# =====================
# SESSION STATE (PALM ID)
# =====================

if "palm_taps" not in st.session_state:
    st.session_state["palm_taps"] = 0

if "show_admin_box" not in st.session_state:
    st.session_state["show_admin_box"] = False

if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = False

if "current_tool" not in st.session_state:
    st.session_state["current_tool"] = None


# =====================
# PAGE CONFIG
# =====================

st.set_page_config(page_title="My App 2 — HTML Viewer", page_icon="🖥️", layout="wide")


# =====================
# HEADER + PALM ID UI
# =====================

left, right = st.columns([0.88, 0.12], vertical_alignment="center")

with left:
    st.title("🖥️ My App 2 — Simplified HTML Viewer")
    st.caption("Portal viewer for your local HTML tools (tools_html/*.html)")

with right:
    if st.button("🖐️", help="Palm ID (tap 3x)"):
        st.session_state["palm_taps"] += 1
        if st.session_state["palm_taps"] >= 3:
            st.session_state["show_admin_box"] = True
        st.rerun()

# Gate UI (only appears after 3 taps)
if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
    st.markdown("**Palm ID:** enter admin code")
    code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...")
    colA, colB = st.columns([0.6, 0.4])

    with colA:
        if st.button("Unlock"):
            if code_try == ADMIN_CODE:
                st.session_state["admin_unlocked"] = True
                st.success("Admin override unlocked.")
                st.rerun()
            else:
                st.error("Incorrect code.")

    with colB:
        if st.button("Reset"):
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False
            st.session_state["admin_unlocked"] = False
            st.rerun()

# Optional tiny badge if unlocked
if st.session_state["admin_unlocked"]:
    st.caption("🖐️ Palm ID: unlocked")


st.divider()


# =====================
# TOOL SELECTOR
# =====================

tools = list_tools()

topL, topR = st.columns([0.72, 0.28], vertical_alignment="center")

with topL:
    st.subheader("📁 Tools Folder")
    st.caption(f"Path: {TOOLS_DIR} • {len(tools)} file(s) found • {date.today().isoformat()}")

with topR:
    st.markdown("**Current tool**")
    if tools:
        default_idx = 0
        if st.session_state["current_tool"] in tools:
            default_idx = tools.index(st.session_state["current_tool"])
        picked = st.selectbox("Select HTML tool", tools, index=default_idx, label_visibility="collapsed")
        st.session_state["current_tool"] = picked
    else:
        st.session_state["current_tool"] = None
        st.info("Add .html files into tools_html/")

st.divider()


# =====================
# EASY X (Delete Tool) — ADMIN ONLY
# =====================

def _render_delete_ui():
    st.markdown("### 🧨 EASY X (Delete Tool)")
    st.caption("Admin-only: deletes the currently selected HTML file from tools_html/")

    if not st.session_state.get("current_tool"):
        st.warning("No tool selected.")
        return

    tool_name = st.session_state["current_tool"]
    colA, colB = st.columns([0.85, 0.15], vertical_alignment="center")
    with colA:
        st.markdown(f"**Selected:** `{tool_name}.html`")
    with colB:
        if st.button("✖", help="Delete tool"):
            ok = delete_tool(tool_name)
            if ok:
                st.session_state["current_tool"] = None
                st.success(f"✅ {tool_name}.html deleted.")
            else:
                st.error("File not found.")
            st.rerun()


# show delete UI only when unlocked AND something is selected
if st.session_state.get("admin_unlocked") and st.session_state.get("current_tool"):
    with st.expander("🧨 Admin Tools", expanded=False):
        _render_delete_ui()


# =====================
# PORTAL VIEW
# =====================

st.subheader("🌀 PORTAL — Viewing Window")

if not st.session_state.get("current_tool"):
    st.info("Pick a tool on the right, or add .html files into tools_html/")
else:
    tool_html = load_tool(st.session_state["current_tool"])
    if tool_html:
        portal_view(tool_html, border="rgba(20,184,166,0.65)")
    else:
        st.error(f"Tool file not found: {st.session_state['current_tool']}.html")

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)