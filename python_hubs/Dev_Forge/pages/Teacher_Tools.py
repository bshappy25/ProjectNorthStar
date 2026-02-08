import re
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

"""
TEACHER TOOLS HUB — VIP TV MODE (FULL FILE)
Futuristic TV interface for HTML teaching tools

- Glassy sidebar + TV overlay
- Browse + Search + (optional) Favorites
- Admin "PALM ID" gate (tap 3x) → unlock Upload + Delete
- Upload .html (admin only) + paste/save (safe)
- Delete bad tools (admin only) with confirm
- Hard cap: 25 tools (prevents repo chaos)
- Does NOT modify your saved tools (views them as-is)
"""

# =====================
# CONFIG
# =====================

TOOLS_DIR = Path("teacher_tools")
TOOLS_DIR.mkdir(exist_ok=True)

MAX_TOOLS = 25
ADMIN_CODE = "Bshapp"  # your Palm ID code

# Theme: neutral + science
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

def _init_state():
    ss = st.session_state
    ss.setdefault("theme_mode", "neutral")
    ss.setdefault("current_tool", None)

    # Add/Paste
    ss.setdefault("new_tool_name", "")
    ss.setdefault("html_input", "")

    # Browse
    ss.setdefault("tool_search", "")
    ss.setdefault("fav_tools", set())

    # Admin gate
    ss.setdefault("palm_taps", 0)
    ss.setdefault("show_admin_box", False)
    ss.setdefault("admin_unlocked", False)
    ss.setdefault("admin_code_try", "")

    # Safety confirmations
    ss.setdefault("confirm_delete", False)

_init_state()

# =====================
# HELPERS
# =====================

def list_tools():
    """Return tool stems for all .html files in teacher_tools/"""
    return sorted([p.stem for p in TOOLS_DIR.glob("*.html")])

def tool_path(stem: str) -> Path:
    return TOOLS_DIR / f"{stem}.html"

def load_tool(stem: str) -> str:
    p = tool_path(stem)
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    return ""

def save_tool(name: str, html_code: str) -> Path:
    """Save as <name>.html (no edits to content)."""
    p = tool_path(name)
    p.write_text(html_code, encoding="utf-8")
    return p

def safe_stem(name: str) -> str:
    """Keep letters, numbers, underscores, hyphens; convert spaces to underscores."""
    stem = Path(name).stem.strip()
    stem = stem.replace(" ", "_")
    stem = re.sub(r"[^A-Za-z0-9_\-]+", "", stem)
    stem = stem[:60] if stem else "uploaded_tool"
    return stem

def next_available_stem(base: str) -> str:
    """Avoid overwrite: base, base_1, base_2 ..."""
    base = safe_stem(base)
    if not tool_path(base).exists():
        return base
    n = 1
    while True:
        cand = f"{base}_{n}"
        if not tool_path(cand).exists():
            return cand
        n += 1

def delete_tool(stem: str):
    p = tool_path(stem)
    if p.exists():
        p.unlink()
    if st.session_state.get("current_tool") == stem:
        st.session_state["current_tool"] = None

def cap_tools_guard():
    tools = list_tools()
    if len(tools) >= MAX_TOOLS:
        return True, f"Tool cap reached ({MAX_TOOLS}). Delete one to add more."
    return False, ""

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="Teacher Tools Hub (VIP)",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================
# THEME SELECTION
# =====================

is_science = st.session_state["theme_mode"] == "science"

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT
MUTED = SCI_MUTED if is_science else NEUTRAL_MUTED
ACCENT = SCI_ACCENT if is_science else "#2563eb"

# =====================
# CSS — VIP GLASS + TV
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
  --radius: 18px;
}}

/* App background */
div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
  background-color: var(--card) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border-right: 1px solid var(--border) !important;
}}

/* Text */
h1,h2,h3,h4,h5,h6,p,span,label,div {{
  color: var(--text) !important;
}}

/* Inputs */
input, textarea, select {{
  background-color: rgba(255,255,255,0.35) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

/* Code box */
textarea {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Courier New", monospace !important;
  font-size: 13px !important;
}}

/* Buttons */
button {{
  background-color: rgba(255,255,255,0.28) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-weight: 800 !important;
}}
button[kind="primary"] {{
  border: 2px solid rgba(20,184,166,0.45) !important;
  background: linear-gradient(135deg, rgba(20,184,166,0.25), rgba(20,184,166,0.12)) !important;
}}

/* Bottom ticker */
.ticker {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background-color: var(--card);
  border-top: 1px solid var(--border);
  padding: 8px 18px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--muted);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 9999;
}}

/* VIP badge */
.vip-badge {{
  display:inline-flex;
  gap:10px;
  align-items:center;
  padding: 8px 12px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.22);
  box-shadow: 0 12px 28px rgba(0,0,0,0.10);
}}

.vip-dot {{
  width:10px; height:10px;
  border-radius: 999px;
  background: var(--accent);
  box-shadow: 0 0 18px rgba(20,184,166,0.55);
}}

</style>
""",
    unsafe_allow_html=True,
)

# =====================
# TICKER
# =====================

st.markdown(
    "<div class='ticker'>TEACHER TOOLS HUB • We are L.E.A.D. • VIP TV MODE 📺</div>",
    unsafe_allow_html=True,
)

# =====================
# SIDEBAR (VIP NAV)
# =====================

with st.sidebar:
    # Top row: title left, Palm ID button right (tap 3x)
    left, right = st.columns([0.84, 0.16], vertical_alignment="center")
    with left:
        st.title("📺 Teacher Tools")
        st.caption("VIP viewing • upload • preview (HTML)")

    with right:
        if st.button("🌴", help="Palm ID (tap 3x)", use_container_width=True):
            st.session_state["palm_taps"] += 1
            if st.session_state["palm_taps"] >= 3:
                st.session_state["show_admin_box"] = True
                st.session_state["palm_taps"] = 3  # clamp

    # Gate UI
    if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
        st.markdown("**Palm ID:** enter admin code")
        st.session_state["admin_code_try"] = st.text_input(
            "Admin Code",
            type="password",
            placeholder="Enter code…",
            value=st.session_state.get("admin_code_try", ""),
        )
        colA, colB = st.columns([0.6, 0.4])
        with colA:
            if st.button("Unlock", type="primary", use_container_width=True):
                if st.session_state["admin_code_try"] == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    st.success("Admin override unlocked.")
                else:
                    st.error("Incorrect code.")
        with colB:
            if st.button("Reset", use_container_width=True):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False
                st.session_state["admin_code_try"] = ""

    if st.session_state["admin_unlocked"]:
        st.caption("🌴 Palm ID: **unlocked**")

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

    # Search
    st.subheader("📂 Your Tools")
    st.session_state["tool_search"] = st.text_input(
        "Search",
        placeholder="type to filter…",
        value=st.session_state.get("tool_search", ""),
    )

    # Tool list (max 25)
    tools_all = list_tools()
    q = st.session_state["tool_search"].strip().lower()

    # favorites first
    favs = st.session_state.get("fav_tools", set())
    tools_filtered = [t for t in tools_all if (q in t.lower())]
    tools_favs = [t for t in tools_filtered if t in favs]
    tools_rest = [t for t in tools_filtered if t not in favs]
    tools = tools_favs + tools_rest

    if not tools_all:
        st.info("No tools yet. Add one in **Add/Paste** or **Upload**.")
    else:
        for t in tools:
            is_active = st.session_state["current_tool"] == t
            icon = "📺" if is_active else "📄"
            star = "⭐" if t in favs else "☆"
            cols = st.columns([0.82, 0.18], vertical_alignment="center")
            with cols[0]:
                if st.button(
                    f"{icon} {t}",
                    key=f"tool_{t}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state["current_tool"] = t
                    st.session_state["confirm_delete"] = False
                    st.rerun()
            with cols[1]:
                if st.button(star, key=f"fav_{t}", help="favorite"):
                    if t in favs:
                        favs.remove(t)
                    else:
                        favs.add(t)
                    st.session_state["fav_tools"] = favs
                    st.rerun()

    st.caption(f"Limit: **{len(tools_all)}/{MAX_TOOLS}** tools")

# =====================
# MAIN WINDOW — VIP TABS
# =====================

st.markdown(
    """
<div class="vip-badge">
  <div class="vip-dot"></div>
  <div style="font-weight:900; letter-spacing:0.10em;">VIP VIEWING CONSOLE</div>
  <div style="opacity:0.75; font-weight:800;">Preview • Upload • Delete</div>
</div>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs(["📺 Preview", "➕ Add/Paste", "⬆️ Upload (Admin)", "🛠️ Admin"])

# ---------------------
# TAB: PREVIEW
# ---------------------
with tabs[0]:
    if not st.session_state["current_tool"]:
        st.markdown(
            """
            <div style="text-align:center; padding: 40px 10px;">
              <h1 style="margin:0; font-size:2.2rem;">📺 Teacher Tools Hub</h1>
              <p style="margin-top:8px; font-weight:800; opacity:0.75;">
                Pick a tool from the sidebar to view it in VIP TV mode.
              </p>
              <p style="opacity:0.75;">
                Tip: ⭐ favorite your daily drivers so they stay on top.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        tool_name = st.session_state["current_tool"]
        tool_html = load_tool(tool_name)

        # Header row with actions
        hcol1, hcol2, hcol3 = st.columns([0.64, 0.18, 0.18], vertical_alignment="center")
        with hcol1:
            st.markdown(f"## 📺 {tool_name}")
            st.caption("Viewing in Futuristic TV Mode • (tool content is not edited)")

        # Quick actions (safe)
        with hcol2:
            if st.button("🔄 Refresh Preview", use_container_width=True):
                st.rerun()
        with hcol3:
            # Screenshot guidance (replaces “save png”)
            st.button("📸 Screenshot Mode", use_container_width=True, help="Use device screenshot / Smart Select")

        # Optional: admin delete button (small X)
        if st.session_state.get("admin_unlocked"):
            dcolA, dcolB = st.columns([0.85, 0.15], vertical_alignment="center")
            with dcolB:
                if st.button("✖", help="Delete tool (admin)", use_container_width=True):
                    st.session_state["confirm_delete"] = True

            if st.session_state.get("confirm_delete"):
                st.warning("Delete this tool file? This cannot be undone (repo backup recommended).")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Confirm Delete", type="primary", use_container_width=True):
                        delete_tool(tool_name)
                        st.session_state["confirm_delete"] = False
                        st.success(f"Deleted: {tool_name}")
                        st.rerun()
                with c2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state["confirm_delete"] = False
                        st.rerun()

        if not tool_html.strip():
            st.error("Tool file is empty or missing.")
        else:
            escaped = html.escape(tool_html, quote=True)

            # VIP TV wrapper (responsive; avoids crushed layouts)
            combined = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  :root {{
    --border: {BORDER};
    --accent: {ACCENT};
  }}
  html, body {{
    height: 100%;
    margin: 0;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  }}

  /* fill the visible area nicely */
  .tv-frame {{
    position: relative;
    width: 100%;
    height: min(86vh, 980px);
    border: 3px solid var(--border);
    border-radius: 20px;
    overflow: hidden;
    background: rgba(0,0,0,0.05);
    box-shadow:
      0 0 40px rgba(20,184,166,0.20),
      inset 0 0 60px rgba(20,184,166,0.06);
  }}

  /* scan lines */
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
    z-index: 3;
    animation: scanlines 8s linear infinite;
  }}

  @keyframes scanlines {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(4px); }}
  }}

  /* glow vignette */
  .tv-frame::after {{
    content: '';
    position: absolute;
    top: -55%;
    left: -55%;
    width: 210%;
    height: 210%;
    background: radial-gradient(circle, rgba(20,184,166,0.12) 0%, transparent 55%);
    pointer-events: none;
    z-index: 2;
    animation: glow 4s ease-in-out infinite alternate;
  }}

  @keyframes glow {{
    0% {{ opacity: 0.22; }}
    100% {{ opacity: 0.62; }}
  }}

  /* inner bevel */
  .bevel {{
    position:absolute;
    inset:0;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.10);
    pointer-events:none;
    z-index: 4;
  }}

  .screen {{
    position: relative;
    z-index: 5;
    width: 100%;
    height: 100%;
    background: rgba(255,255,255,0.06);
  }}

  iframe {{
    width: 100%;
    height: 100%;
    border: 0;
    background: white;
  }}

  /* top label */
  .label {{
    position:absolute;
    top: 10px; left: 12px;
    z-index: 6;
    padding: 8px 10px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(0,0,0,0.18);
    color: rgba(255,255,255,0.88);
    font-weight: 800;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    font-size: 12px;
    backdrop-filter: blur(10px);
  }}
</style>
</head>
<body>
  <div class="tv-frame">
    <div class="label">VIP PREVIEW</div>
    <div class="bevel"></div>
    <div class="screen">
      <iframe
        sandbox="allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin"
        srcdoc="{escaped}">
      </iframe>
    </div>
  </div>
</body>
</html>
"""
            # Height should match the max-ish frame; Streamlit needs a fixed px.
            components.html(combined, height=1020, scrolling=False)

# ---------------------
# TAB: ADD/PASTE
# ---------------------
with tabs[1]:
    st.subheader("➕ Add New Tool (Paste HTML)")
    st.caption("Copy → Paste → Save. This does NOT modify any existing tools.")

    cap_hit, cap_msg = cap_tools_guard()
    if cap_hit:
        st.error(cap_msg)
    else:
        tool_name_raw = st.text_input(
            "Tool Name",
            placeholder="e.g., Evidence Capture v1",
            value=st.session_state.get("new_tool_name", ""),
            key="new_tool_name",
        )

        html_code = st.text_area(
            "HTML Code",
            placeholder="Paste your complete HTML code here…",
            height=320,
            value=st.session_state.get("html_input", ""),
            key="html_input",
        )

        c1, c2, c3 = st.columns([0.33, 0.33, 0.34])
        with c1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state["html_input"] = ""
                st.rerun()
        with c2:
            if st.button("🧪 Quick Validate", use_container_width=True):
                s = (html_code or "").lower()
                if "<html" not in s or "<body" not in s:
                    st.warning("This may not be a complete HTML document (missing <html> or <body>). It can still work, but full files are safer.")
                else:
                    st.success("Looks like a full HTML document.")
        with c3:
            if st.button("💾 Save", type="primary", use_container_width=True):
                if not tool_name_raw.strip():
                    st.error("Enter a tool name!")
                elif not html_code.strip():
                    st.error("Paste HTML code!")
                else:
                    safe_name = next_available_stem(tool_name_raw.strip())
                    save_tool(safe_name, html_code)
                    st.session_state["current_tool"] = safe_name
                    st.session_state["html_input"] = ""
                    st.session_state["new_tool_name"] = ""
                    st.success(f"✅ Saved: {safe_name}.html")
                    st.rerun()

# ---------------------
# TAB: UPLOAD (ADMIN)
# ---------------------
with tabs[2]:
    st.subheader("⬆️ Upload HTML Tool (Admin only)")
    st.caption("Upload a .html file directly into teacher_tools/ (safe naming, no overwrite).")

    if not st.session_state.get("admin_unlocked"):
        st.info("Palm ID required. Tap 🌴 3x in the sidebar, then enter admin code.")
    else:
        cap_hit, cap_msg = cap_tools_guard()
        if cap_hit:
            st.error(cap_msg)
        else:
            up = st.file_uploader("Upload .html file", type=["html"], accept_multiple_files=False)
            if up is not None:
                base = safe_stem(up.name)
                stem = next_available_stem(base)
                dest = tool_path(stem)
                dest.write_bytes(up.getbuffer())
                st.session_state["current_tool"] = stem
                st.success(f"✅ Uploaded: {dest.name}")
                st.rerun()

# ---------------------
# TAB: ADMIN
# ---------------------
with tabs[3]:
    st.subheader("🛠️ Admin Controls")
    st.caption("Delete bad tools safely. (Viewing is always available; destructive actions are locked.)")

    if not st.session_state.get("admin_unlocked"):
        st.info("Palm ID required. Tap 🌴 3x in the sidebar, then enter admin code.")
    else:
        st.success("Admin unlocked.")
        tools = list_tools()

        st.markdown("### 🧹 Cleanup")
        if not tools:
            st.info("No tools to manage yet.")
        else:
            pick = st.selectbox("Select a tool to delete", options=["(choose)"] + tools)
            if pick != "(choose)":
                st.warning("Deleting removes the .html file from teacher_tools/. Your repo backup is your safety net.")
                colA, colB = st.columns(2)
                with colA:
                    if st.button("✖ Delete Selected", type="primary", use_container_width=True):
                        delete_tool(pick)
                        st.success(f"Deleted: {pick}")
                        st.rerun()
                with colB:
                    if st.button("Reset Palm Gate", use_container_width=True):
                        st.session_state["palm_taps"] = 0
                        st.session_state["show_admin_box"] = False
                        st.session_state["admin_unlocked"] = False
                        st.session_state["admin_code_try"] = ""
                        st.success("Palm gate reset.")
                        st.rerun()

# Bottom padding so ticker doesn't cover content
st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)