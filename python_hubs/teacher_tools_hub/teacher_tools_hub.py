import os
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# =====================
# CONFIG
# =====================
TOOLS_DIR = "teacher_tools"
Path(TOOLS_DIR).mkdir(exist_ok=True)

ADMIN_CODE = "Bshapp"  # PALM ID code

# Theme tokens (keep simple + stable)
NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"
NEUTRAL_MUTED = "#1f1f1f"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
SCI_MUTED = "rgba(255,255,255,0.74)"
SCI_ACCENT = "#14B8A6"

# =====================
# SESSION STATE
# =====================
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "neutral"

if "current_tool" not in st.session_state:
    st.session_state["current_tool"] = None

if "html_input" not in st.session_state:
    st.session_state["html_input"] = ""

# PALM ID state
if "palm_taps" not in st.session_state:
    st.session_state["palm_taps"] = 0
if "show_admin_box" not in st.session_state:
    st.session_state["show_admin_box"] = False
if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = False


# =====================
# HELPERS
# =====================
def list_tools():
    return sorted([p.stem for p in Path(TOOLS_DIR).glob("*.html")])

def save_tool(name: str, html_code: str):
    fp = Path(TOOLS_DIR) / f"{name}.html"
    fp.write_text(html_code, encoding="utf-8")
    return fp

def load_tool(name: str) -> str:
    fp = Path(TOOLS_DIR) / f"{name}.html"
    return fp.read_text(encoding="utf-8") if fp.exists() else ""

def delete_tool(name: str):
    """EASY X (Delete Tool) — Admin only"""
    fp = Path(TOOLS_DIR) / f"{name}.html"
    if fp.exists():
        fp.unlink()
        st.session_state["current_tool"] = None
        st.success(f"🗑️ {name} deleted.")


# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Teacher Tools Hub",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# THEME
# =====================
is_science = st.session_state["theme_mode"] == "science"

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_ACCENT if is_science else "#4b5563"

# =====================
# GLOBAL CSS
# =====================
st.markdown(
    f"""
<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --border: {BORDER};
  --text: {TEXT};
  --muted: {MUTED};
  --accent: {ACCENT};
}}

/* App background */
div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

/* Sidebar glass */
section[data-testid="stSidebar"] {{
  background-color: var(--card) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border-right: 1px solid var(--border) !important;
}}

/* Inputs */
input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

textarea {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Courier New", monospace !important;
  font-size: 13px !important;
}}

/* Buttons */
button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-weight: 750 !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--border) !important;
  background: linear-gradient(135deg, rgba(20,184,166,0.20), rgba(20,184,166,0.08)) !important;
}}

/* Bottom ticker */
.ticker {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background-color: var(--card);
  border-top: 1px solid var(--border);
  padding: 8px 20px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--muted);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 999;
}}
</style>
""",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='ticker'>TEACHER TOOLS HUB • We are L.E.A.D. • Futuristic Interface 📺</div>",
    unsafe_allow_html=True,
)

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.title("📺 Teacher Tools")
    st.caption("Copy → Paste → Save → View")

    st.divider()

    theme_choice = st.radio(
        "Theme",
        ["Neutral", "Science"],
        index=0 if st.session_state["theme_mode"] == "neutral" else 1,
        horizontal=True,
    )
    if theme_choice.lower() != st.session_state["theme_mode"]:
        st.session_state["theme_mode"] = theme_choice.lower()
        st.rerun()

    st.divider()

    st.subheader("📂 Your Tools")
    tools = list_tools()
    if not tools:
        st.info("No tools yet. Add one below 👇")
    else:
        for tool in tools:
            is_active = (st.session_state["current_tool"] == tool)
            if st.button(
                f"{'📺 ' if is_active else '📄 '}{tool}",
                key=f"tool_{tool}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["current_tool"] = tool
                st.rerun()

    st.divider()

    with st.expander("➕ Add New Tool", expanded=False):
        tool_name = st.text_input("Tool Name", placeholder="e.g., Uranium", key="new_tool_name")
        html_code = st.text_area("HTML Code", placeholder="Paste full HTML here…", height=260, key="html_input")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state["html_input"] = ""
                st.rerun()
        with c2:
            if st.button("💾 Save", use_container_width=True, type="primary"):
                if not tool_name.strip():
                    st.error("Enter a tool name.")
                elif not html_code.strip():
                    st.error("Paste HTML code.")
                else:
                    save_tool(tool_name.strip(), html_code)
                    st.session_state["current_tool"] = tool_name.strip()
                    st.session_state["html_input"] = ""
                    st.success(f"✅ {tool_name.strip()} saved!")
                    st.rerun()

    st.divider()
    st.caption("Admin tools are locked behind 🌴 Palm ID.")


# =====================
# HEADER + PALM ID (Admin Gate)
# =====================
left, right = st.columns([0.88, 0.12], vertical_alignment="center")

with left:
    st.markdown(
        """
<div style="padding:6px 2px;">
  <div style="font-size:2.2rem; font-weight:900; line-height:1;">📺 TEACHER TOOLS HUB</div>
  <div style="color:var(--muted); font-weight:800;">Futuristic TV interface for HTML teaching tools</div>
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    if st.button("🌴", help="Palm ID (tap 3x)"):
        st.session_state["palm_taps"] += 1
        if st.session_state["palm_taps"] >= 3:
            st.session_state["show_admin_box"] = True

# Gate UI (only appears after 3 taps)
if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
    st.markdown("**Palm ID:** enter admin code")
    code_try = st.text_input("Admin Code", type="password", placeholder="Enter code…")

    colA, colB = st.columns([0.6, 0.4])
    with colA:
        if st.button("Unlock", type="primary"):
            if code_try == ADMIN_CODE:
                st.session_state["admin_unlocked"] = True
                st.success("Admin override unlocked.")
            else:
                st.error("Incorrect code.")
    with colB:
        if st.button("Reset"):
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False

# Optional tiny badge
if st.session_state["admin_unlocked"]:
    st.caption("🌴 Palm ID: unlocked")

st.divider()

# =====================
# MAIN: VIEWING PORTAL WINDOW (Original)
# =====================
if st.session_state["current_tool"]:
    tool_name = st.session_state["current_tool"]

    # Row: tool title + EASY X (admin only)
    colT, colX = st.columns([0.85, 0.15], vertical_alignment="center")
    with colT:
        st.markdown(
            f"""
<div style="margin: 6px 0 8px;">
  <div style="font-size:1.8rem; font-weight:900;">📺 {tool_name}</div>
  <div style="color:var(--muted); font-weight:800;">Viewing in Futuristic TV Mode</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with colX:
        if st.session_state.get("admin_unlocked") and st.session_state.get("current_tool"):
            if st.button("✖", help="EASY X (Delete tool)", type="secondary", use_container_width=True):
                delete_tool(st.session_state["current_tool"])
                st.rerun()

    tool_html = load_tool(tool_name)

    if tool_html:
        escaped = html.escape(tool_html, quote=True)

        combined = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {{
    --border: {BORDER};
  }}

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
      0 0 40px rgba(20,184,166,0.2),
      inset 0 0 60px rgba(20,184,166,0.05);
  }}

  .tv-frame::before {{
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

  .tv-frame::after {{
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
    else:
        st.error(f"Tool file not found: {tool_name}.html")

else:
    st.markdown(
        """
<div style='text-align:center; padding:48px 12px;'>
  <div style='font-size:3rem; font-weight:900;'>📺 PORTAL</div>
  <div style='font-size:1.2rem; color:var(--muted); font-weight:800; margin-top:10px;'>
    Pick a tool from the sidebar to view it in TV mode.
  </div>
  <div style='margin-top:24px; padding:18px; max-width:720px; margin-left:auto; margin-right:auto;
              background:var(--card); border:1px solid var(--border); border-radius:18px;'>
    <div style='font-weight:900; font-size:1.05rem;'>Quick Start</div>
    <ol style='text-align:left; line-height:2; margin:12px auto 0; max-width:560px;'>
      <li>Open <b>➕ Add New Tool</b> in the sidebar</li>
      <li>Paste your full HTML</li>
      <li>Press <b>💾 Save</b></li>
      <li>Select the tool to view it</li>
    </ol>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# bottom spacing for fixed ticker
st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)