"""
DevForge - Developer Productivity Hub

Your personal Streamlit development assistant

Features:
- Quick Start Templates
- Code Library (copy/paste components)
- ABC Branch Generator (architecture decisions)
- Ms. Piluso Science Page (NGSS + New Visions)
- Placeholder Apps (my_app1 / my_app2)

Connected to BSChapp v2 ecosystem
We are L.E.A.D.
"""

from __future__ import annotations

from datetime import date

import streamlit as st

# ============================================================
# CONFIG
# ============================================================

APP_TITLE = "DevForge - Developer Hub"
APP_ICON = "🔧"

ADMIN_CODE = "Bshapp"  # PALM ID (Admin Gate)

# ============================================================
# SESSION STATE (SAFE INIT)
# ============================================================

def ss_init(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

# Core shared state
ss_init("dev_theme", "science")   # science | neutral | pink
ss_init("signature", "")          # developer name / signature (shared w/ BSChapp)
ss_init("notes", "")              # quick scratch notes

# PALM ID admin gate state
ss_init("palm_taps", 0)
ss_init("show_admin_box", False)
ss_init("admin_unlocked", False)

# ============================================================
# THEMES
# ============================================================

NEUTRAL = {
    "BG": "#f2f2f2",
    "CARD": "rgba(230, 230, 230, 0.7)",
    "BORDER": "rgba(207, 207, 207, 0.5)",
    "TEXT": "#000000",
    "MUTED": "#1f1f1f",
    "ACCENT": "#5a5a5a",
    "ACCENT2": "#2F5BEA",
}

SCIENCE = {
    "BG": "#061B15",
    "CARD": "rgba(255,255,255,0.08)",
    "BORDER": "rgba(120,255,220,0.3)",
    "TEXT": "rgba(255,255,255,0.92)",
    "MUTED": "rgba(255,255,255,0.74)",
    "ACCENT": "#14B8A6",
    "ACCENT2": "#2F5BEA",
}

# Fun Pink theme (only shows under PALM ID gate)
PINK = {
    "BG": "#140914",
    "CARD": "rgba(255, 192, 203, 0.10)",
    "BORDER": "rgba(255, 105, 180, 0.35)",
    "TEXT": "rgba(255,255,255,0.92)",
    "MUTED": "rgba(255,255,255,0.72)",
    "ACCENT": "#FF4DA6",
    "ACCENT2": "#FFB3D9",
}

def get_theme_dict(theme_key: str) -> dict:
    if theme_key == "neutral":
        return NEUTRAL
    if theme_key == "pink":
        return PINK
    return SCIENCE

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

T = get_theme_dict(st.session_state["dev_theme"])

# ============================================================
# CSS / UI
# ============================================================

st.markdown(
    f"""
<style>
:root {{
  --bg: {T["BG"]};
  --card: {T["CARD"]};
  --border: {T["BORDER"]};
  --text: {T["TEXT"]};
  --muted: {T["MUTED"]};
  --accent: {T["ACCENT"]};
  --accent2: {T["ACCENT2"]};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

.block-container {{
  padding-top: 1.15rem;
  padding-bottom: 4.5rem;
}}

section[data-testid="stSidebar"] {{
  background-color: transparent !important;
}}

section[data-testid="stSidebar"],
div[data-testid="stExpander"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextArea"] > div,
div[data-testid="stSelectbox"] > div,
.stCodeBlock {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

small, .stCaption, .muted {{
  color: var(--muted) !important;
}}

input, textarea, select {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}

button {{
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  color: var(--text) !important;
  font-weight: 800 !important;
}}

button[kind="primary"] {{
  border: 2px solid var(--accent) !important;
  font-weight: 900 !important;
}}

.dev-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 14px 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}}

.dev-card h3 {{
  margin-top: 0;
  color: var(--accent) !important;
  font-weight: 950;
}}

.badge {{
  display: inline-block;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-weight: 950;
  background: var(--card);
  backdrop-filter: blur(10px);
  font-size: 0.85rem;
  margin: 4px 6px 4px 0;
}}

.badge-accent {{
  border-color: var(--accent);
  color: var(--accent) !important;
}}

.badge-accent2 {{
  border-color: var(--accent2);
  color: var(--accent2) !important;
}}

.hr {{
  height: 1px;
  background: var(--border);
  margin: 14px 0;
}}

.ticker {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--card);
  border-top: 1px solid var(--border);
  padding: 8px 18px;
  text-align: center;
  font-size: 0.85rem;
  font-weight: 850;
  color: var(--muted);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 999;
}}

.kicker {{
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.9;
}}

.callout {{
  border-left: 4px solid var(--accent);
  padding: 10px 14px;
  margin: 10px 0;
  background: rgba(0,0,0,0.06);
  border-radius: 10px;
}}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# TICKER
# ============================================================

st.markdown(
    "<div class='ticker'>DEVFORGE • Developer Productivity Hub • We are L.E.A.D. 🔧</div>",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR (WITH PALM ID + THEMES)
# ============================================================

with st.sidebar:
    st.title("🔧 DevForge")
    st.caption("Developer Productivity Hub")

    st.divider()

    # =========================
    # PALM ID (Admin Gate)
    # =========================
    left, right = st.columns([0.86, 0.14], vertical_alignment="center")
    with left:
        st.markdown("#### PALM ID")
        st.caption("Tap the palm 3× to open admin gate.")
    with right:
        if st.button("🤚", help="Palm ID (tap 3x)", key="palm_btn"):
            st.session_state["palm_taps"] += 1
            if st.session_state["palm_taps"] >= 3:
                st.session_state["show_admin_box"] = True

    if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
        st.markdown("**Palm ID:** enter admin code")
        code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...", key="admin_code_try")
        cA, cB = st.columns([0.6, 0.4])
        with cA:
            if st.button("Unlock", key="unlock_btn"):
                if code_try == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    st.success("Admin override unlocked.")
                else:
                    st.error("Incorrect code.")
        with cB:
            if st.button("Reset", key="reset_palm_btn"):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False

    if st.session_state["admin_unlocked"]:
        st.caption("✅ Palm ID: unlocked")

    st.divider()

    # =========================
    # THEME TOGGLE
    # =========================
    theme_options = ["Science", "Neutral"]
    # Pink option only under PALM ID (as requested)
    if st.session_state["admin_unlocked"]:
        theme_options.append("Pink")

    current = st.session_state["dev_theme"]
    idx = 0
    if current == "neutral":
        idx = 1
    if current == "pink":
        idx = 2 if "Pink" in theme_options else 0

    theme_choice = st.radio(
        "Dev Theme",
        theme_options,
        index=idx,
        horizontal=True,
        key="theme_choice_radio",
    )

    choice_map = {"Science": "science", "Neutral": "neutral", "Pink": "pink"}
    chosen_theme = choice_map[theme_choice]
    if chosen_theme != st.session_state["dev_theme"]:
        st.session_state["dev_theme"] = chosen_theme
        st.rerun()

    st.divider()

    # =========================
    # QUICK STATS
    # =========================
    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")

    sig = st.session_state.get("signature", "")
    if sig:
        st.write(f"**Dev:** {sig}")
    else:
        st.caption("No signature (set in BSChapp)")

    st.divider()

    # =========================
    # NAV HINTS (Multipage)
    # =========================
    st.subheader("🗺️ Pages")
    st.caption("Your pages folder drives navigation automatically.")
    st.markdown(
        """
- **ABC_Generator.py**
- **Code_Library.py**
- **Ms_Piluso_Science.py**
- **my_app1.py**
- **my_app2.py**
"""
    )

    st.divider()

    # =========================
    # DEV NOTES
    # =========================
    st.subheader("📝 Scratch Notes")
    st.session_state["notes"] = st.text_area(
        "Notes",
        value=st.session_state.get("notes", ""),
        height=110,
        placeholder="Quick notes while you build...",
        label_visibility="collapsed",
    )

    st.divider()

    # =========================
    # ADMIN TOOLS (ONLY WHEN UNLOCKED)
    # =========================
    if st.session_state["admin_unlocked"]:
        st.subheader("🧰 Admin Tools")
        st.caption("Visible only when Palm ID is unlocked.")

        if st.button("Reset Theme to Science", use_container_width=True):
            st.session_state["dev_theme"] = "science"
            st.rerun()

        if st.button("Clear Scratch Notes", use_container_width=True):
            st.session_state["notes"] = ""
            st.rerun()

        if st.button("Lock Admin Gate", use_container_width=True):
            st.session_state["admin_unlocked"] = False
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False
            st.rerun()

    st.caption("Connected to Project North Star")

# ============================================================
# MAIN CONTENT (HOME)
# ============================================================

st.title("🔧 DevForge - Developer Hub")
st.markdown("### Your Streamlit Development Assistant")

st.markdown(
    """
<div class='dev-card'>
<div class='kicker'>SYSTEM OVERVIEW</div>
<h3>🎯 Quick Start</h3>
<p>DevForge helps you build Streamlit apps faster with:</p>
<ul>
<li><strong>Ms. Piluso Science Page</strong> - NGSS + New Visions curriculum tools + SCI-BLOCK exports</li>
<li><strong>Code Library</strong> - Copy/paste UI components and patterns</li>
<li><strong>ABC Generator</strong> - Make architecture decisions quickly</li>
<li><strong>my_app1 / my_app2</strong> - sandbox pages for experiments</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# FEATURE GRID
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
<div class='dev-card'>
<h3>🔬 Science Tools</h3>
<p>NGSS-aligned lesson planning</p>
<p>New Visions integration</p>
<p>5E framework builder + accommodations</p>
<br>
<p><strong>→ Open “Ms_Piluso_Science” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class='dev-card'>
<h3>📚 Code Library</h3>
<p>Glassy UI components</p>
<p>PDF + Image export patterns</p>
<p>Session state patterns</p>
<br>
<p><strong>→ Open “Code_Library” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
<div class='dev-card'>
<h3>⚡ ABC Framework</h3>
<p><strong>A</strong> - Architecture</p>
<p><strong>B</strong> - Build pattern</p>
<p><strong>C</strong> - Code style</p>
<p><strong>S</strong> - Style selection</p>
<br>
<p><strong>→ Open “ABC_Generator” page</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# DEVFORGE "DIVISION" (Primary vs Tester Apps)
# ============================================================

st.markdown("## 🧭 Primary Apps vs Tester Apps")

st.markdown(
    """
<div class='dev-card'>
<h3>Primary Apps</h3>
<ul>
  <li><strong>Ms_Piluso_Science</strong> — production lesson builder</li>
  <li><strong>Code_Library</strong> — canonical snippets (copy/paste)</li>
  <li><strong>ABC_Generator</strong> — build decisions + starter structures</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='dev-card'>
<h3>Tester Apps</h3>
<p class='muted'>Use these to experiment without risking your core pages.</p>
<ul>
  <li><strong>my_app1</strong> — small UI blocks / forms</li>
  <li><strong>my_app2</strong> — export experiments, widgets, layouts</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# QUICK REFERENCE
# ============================================================

st.markdown("## 🚀 Quick Reference")

with st.expander("📋 Common Tasks", expanded=False):
    st.markdown(
        """
**Create new science lesson**
1) Open **Ms_Piluso_Science**
2) Select NGSS standard
3) Fill 5E + Materials + Notes + Accommodations
4) Export SCI-BLOCK.jpeg and/or copy the preview

**Use sandbox**
1) Open **my_app1** or **my_app2**
2) Paste a UI block or feature idea
3) Once stable, move it into a primary page

**Make architecture decision**
1) Open **ABC_Generator**
2) Answer A, B, C, S
3) Use the recommended structure + starter code
"""
    )

with st.expander("🧱 Recommended Page Pattern", expanded=False):
    st.markdown(
        """
**Keep each page stable**
- Each page should start with:
  - `import streamlit as st`
  - `st.set_page_config(...)`
  - theme read: `st.session_state.get("dev_theme", "science")`
- No smart quotes. Only normal quotes: `"` and `'`

**Sharing state across pages**
- `st.session_state["dev_theme"]`
- `st.session_state["signature"]`
- Any shared objects should be dicts with safe init.
"""
    )

with st.expander("🔒 PALM ID Notes", expanded=False):
    st.markdown(
        """
**PALM ID gate**
- Tap 🤚 three times
- Enter admin code
- Unlock reveals:
  - **Pink** theme option (fun)
  - Admin tools (reset notes / lock gate)

If you ever get stuck, lock gate + reset theme to Science.
"""
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# STATUS / DEBUG (SAFE)
# ============================================================

st.markdown("## 🧩 Current State")

cA, cB = st.columns([0.55, 0.45])

with cA:
    st.markdown(
        """
<div class='dev-card'>
<h3>System Status</h3>
<p><span class='badge badge-accent'>Theme</span> <strong>{theme}</strong></p>
<p><span class='badge badge-accent2'>Signature</span> <strong>{sig}</strong></p>
<p><span class='badge'>Admin</span> <strong>{admin}</strong></p>
</div>
""".format(
            theme=st.session_state["dev_theme"],
            sig=(st.session_state.get("signature") or "Not set"),
            admin=("Unlocked" if st.session_state["admin_unlocked"] else "Locked"),
        ),
        unsafe_allow_html=True,
    )

with cB:
    st.markdown(
        """
<div class='dev-card'>
<h3>Developer Notes</h3>
<p class='muted'>These are stored in session_state (temporary).</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.text_area(
        "Notes Preview",
        value=st.session_state.get("notes", ""),
        height=155,
        disabled=True,
        label_visibility="collapsed",
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# CTA
# ============================================================

st.markdown(
    """
<div class='dev-card' style='text-align:center; background: linear-gradient(135deg, rgba(20,184,166,0.12), rgba(47,91,234,0.10));'>
<h3>🎯 Ready to Build?</h3>
<p style='font-size:1.05rem;' class='muted'>
Open a page from the left sidebar (Streamlit Pages).
Use <strong>my_app1 / my_app2</strong> to prototype safely.
</p>
<div style='margin-top:18px;'>
<span class='badge badge-accent'>NGSS Tools</span>
<span class='badge badge-accent'>Code Snippets</span>
<span class='badge badge-accent'>Architecture Help</span>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# Bottom padding (keeps ticker from covering content)
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)