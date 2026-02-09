from __future__ import annotations
from datetime import date
import streamlit as st

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def ss_init(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss_init("dev_theme", "science")   # science | neutral | pink
ss_init("signature", "")          # developer name / signature
ss_init("notes", "")              # quick scratch notes
ss_init("palm_taps", 0)
ss_init("show_admin_box", False)
ss_init("admin_unlocked", False)
ss_init("custom_css", "")         # For CSS Editor: stores user-edited CSS overrides

ADMIN_CODE = "Bshapp"  # PALM ID admin gate code

# ============================================================
# THEME DEFINITIONS
# ============================================================

NEUTRAL = {
    "BG": "#f2f2f2", "CARD": "rgba(230,230,230,0.7)", "BORDER": "rgba(207,207,207,0.5)",
    "TEXT": "#000000", "MUTED": "#1f1f1f", "ACCENT": "#5a5a5a", "ACCENT2": "#2F5BEA",
}

SCIENCE = {
    "BG": "#061B15", "CARD": "rgba(255,255,255,0.08)", "BORDER": "rgba(120,255,220,0.3)",
    "TEXT": "rgba(255,255,255,0.92)", "MUTED": "rgba(255,255,255,0.74)",
    "ACCENT": "#14B8A6", "ACCENT2": "#2F5BEA",
}

PINK = {
    "BG": "#140914", "CARD": "rgba(255,192,203,0.10)", "BORDER": "rgba(255,105,180,0.35)",
    "TEXT": "rgba(255,255,255,0.92)", "MUTED": "rgba(255,255,255,0.72)",
    "ACCENT": "#FF4DA6", "ACCENT2": "#FFB3D9",
}

def get_theme_dict(theme_key: str) -> dict:
    return PINK if theme_key == "pink" else NEUTRAL if theme_key == "neutral" else SCIENCE

# ============================================================
# PAGE CONFIG & THEME APPLICATION
# ============================================================

st.set_page_config(
    page_title="DevForge - Developer Hub",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

T = get_theme_dict(st.session_state["dev_theme"])

# ============================================================
# CUSTOM CSS (Base + User Overrides from CSS Editor)
# ============================================================

base_css = f"""
<style>
:root {{
  --bg: {T["BG"]};
  --card: {T["CARD"]};
  --border: {T["BORDER"]};
  --text: {T["TEXT"]};
  --muted: {T["MUTED"]};
  --accent: {T["ACCENT"]};
  --accent2: {T["ACCENT2"]};
  --accent-rgb: 20,184,166;  /* For glow effects; adjust per theme if needed */
}}
div[data-testid="stAppViewContainer"] {{ background-color: var(--bg) !important; }}
.block-container {{ padding-top: 1.15rem; padding-bottom: 4.5rem; }}
section[data-testid="stSidebar"] {{ background-color: transparent !important; }}
section[data-testid="stSidebar"], div[data-testid="stExpander"], div[data-testid="stTextInput"] > div,
div[data-testid="stTextArea"] > div, div[data-testid="stSelectbox"] > div, .stCodeBlock {{
  background-color: var(--card) !important; border: 1px solid var(--border) !important;
  border-radius: 14px !important; backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
}}
h1,h2,h3,h4,h5,h6,p,span,label,div {{ color: var(--text) !important; }}
small,.stCaption,.muted {{ color: var(--muted) !important; }}
input,textarea,select,button {{
  background-color: var(--card) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; border-radius: 10px !important;
  backdrop-filter: blur(10px) !important; -webkit-backdrop-filter: blur(10px) !important;
}}
button[kind="primary"] {{ border: 2px solid var(--accent) !important; font-weight: 900 !important; }}
.dev-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px;
  padding: 20px; margin: 14px 0; backdrop-filter: blur(10px); box-shadow: 0 4px 14px rgba(0,0,0,0.12); }}
.dev-card h3 {{ margin-top: 0; color: var(--accent) !important; font-weight: 950; }}
.badge {{ display: inline-block; padding: 6px 12px; border-radius: 999px; border: 1px solid var(--border);
  font-weight: 950; background: var(--card); backdrop-filter: blur(10px); font-size: 0.85rem; margin: 4px 6px 4px 0; }}
.badge-accent {{ border-color: var(--accent); color: var(--accent) !important; }}
.badge-accent2 {{ border-color: var(--accent2); color: var(--accent2) !important; }}
.hr {{ height: 1px; background: var(--border); margin: 14px 0; }}
.ticker {{ position: fixed; bottom: 0; left: 0; right: 0; background-color: var(--card);
  border-top: 1px solid var(--border); padding: 8px 18px; text-align: center; font-size: 0.85rem;
  font-weight: 850; color: var(--muted); backdrop-filter: blur(10px); z-index: 999; }}
.kicker {{ font-size: 0.95rem; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.9; }}
.callout {{ border-left: 4px solid var(--accent); padding: 10px 14px; margin: 10px 0;
  background: rgba(0,0,0,0.06); border-radius: 10px; }}
/* Animation Keyframes for Wow Factor */
@keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} }}
.animate-fade {{ animation: fadeInUp 1.2s ease-out forwards; }}
.glow-hover:hover {{ box-shadow: 0 0 30px rgba(var(--accent-rgb), 0.4); transition: box-shadow 0.4s; }}
</style>
"""

# Append user-custom CSS from session state (from CSS Editor)
custom_css = st.session_state.get("custom_css", "")
st.markdown(base_css + custom_css, unsafe_allow_html=True)

st.markdown("<div class='ticker'>DEVFORGE • Developer Productivity Hub • We are L.E.A.D. 🔧</div>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR (PALM ID, Theme, Notes, Admin Tools)
# ============================================================

with st.sidebar:
    st.title("🔧 DevForge")
    st.caption("Developer Productivity Hub")
    st.divider()

    # PALM ID Gate
    left, right = st.columns([0.86, 0.14])
    with left:
        st.markdown("#### PALM ID")
        st.caption("Tap the palm 3× to open admin gate.")
    with right:
        if st.button("🤚", help="Palm ID (tap 3x)"):
            st.session_state["palm_taps"] += 1
            if st.session_state["palm_taps"] >= 3:
                st.session_state["show_admin_box"] = True

    if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
        st.markdown("**Palm ID:** enter admin code")
        code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...")
        cA, cB = st.columns([0.6, 0.4])
        with cA:
            if st.button("Unlock", use_container_width=True):
                if code_try == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    st.success("Admin override unlocked.")
                else:
                    st.error("Incorrect code.")
        with cB:
            if st.button("Reset", use_container_width=True):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False

    if st.session_state["admin_unlocked"]:
        st.caption("✅ Palm ID: unlocked")

    st.divider()

    # Theme Toggle
    theme_options = ["Science", "Neutral"]
    if st.session_state["admin_unlocked"]:
        theme_options.append("Pink")
    current = st.session_state["dev_theme"]
    idx = {"science": 0, "neutral": 1, "pink": 2}.get(current, 0)
    theme_choice = st.radio("Dev Theme", theme_options, index=idx, horizontal=True)
    choice_map = {"Science": "science", "Neutral": "neutral", "Pink": "pink"}
    if choice_map[theme_choice] != current:
        st.session_state["dev_theme"] = choice_map[theme_choice]
        st.rerun()

    st.divider()

    # Session Info
    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")
    st.write(f"**Dev:** {st.session_state.get('signature', 'Not set')}")

    st.divider()

    # Scratch Notes
    st.subheader("📝 Scratch Notes")
    st.session_state["notes"] = st.text_area(
        "Notes", value=st.session_state["notes"], height=110,
        placeholder="Quick notes while you build...", label_visibility="collapsed"
    )

    st.divider()

    # Admin Tools
    if st.session_state["admin_unlocked"]:
        st.subheader("🧰 Admin Tools")
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

# ============================================================
# DYNAMIC NAVIGATION
# ============================================================

home_page = st.Page("pages/home.py", title="DevForge Home", icon="🔧", default=True)

core_pages = [
    st.Page("pages/Ms_Piluso_Science.py", title="Ms. Piluso Science", icon="🔬"),
    st.Page("pages/Code_Library.py", title="Code Library", icon="📚"),
    st.Page("pages/ABC_Generator.py", title="ABC Generator", icon="⚡"),
]

sandbox_pages = [
    st.Page("pages/my_app1.py", title="Sandbox 1", icon="🧪"),
    st.Page("pages/my_app2.py", title="Sandbox 2", icon="🧪"),
]

admin_pages = [
    st.Page("pages/Teacher_Tools.py", title="Teacher Tools", icon="🧰"),
    st.Page("pages/CSS_Editor.py", title="CSS Editor", icon="🎨"),
]

sections = {
    "Home": [home_page],
    "Core Tools": core_pages,
    "Sandboxes": sandbox_pages,
}

if st.session_state.get("admin_unlocked", False):
    sections["Admin Extras"] = admin_pages

pg = st.navigation(sections)
pg.run()