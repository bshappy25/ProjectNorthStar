from __future__ import annotations

from datetime import date
# pages/home.py  (drop-in replacement for main content area)

import streamlit as st

# Assume T (theme dict) and other shared vars are accessible via session_state or import
# For standalone testing, you can re-define minimal T here if needed

st.markdown(
    """
    <div style="text-align: center; padding: 80px 20px 60px; background: linear-gradient(135deg, var(--bg), rgba(20,184,166,0.08)); border-radius: 0 0 32px 32px; margin: -20px -40px 40px;">
        <h1 style="font-size: 4.2rem; margin: 0; letter-spacing: -0.02em; background: linear-gradient(90deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔧 DevForge
        </h1>
        <p class="kicker" style="font-size: 1.5rem; margin: 16px 0 32px; opacity: 0.95;">
            Your Personal Streamlit Forge — Build Faster, Smarter, Beautifully
        </p>
        <div style="animation: pulse 4s infinite ease-in-out;">
            <span class="badge badge-accent" style="font-size: 1.1rem; padding: 10px 24px;">We are L.E.A.D.</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add subtle load animation to CSS if not already present (extend your <style> block in entry file)
st.markdown(
    """
    <style>
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    .animate-fade { animation: fadeInUp 1.2s ease-out forwards; }
    .glow-hover:hover { box-shadow: 0 0 30px rgba(var(--accent-rgb), 0.4); transition: box-shadow 0.4s; }
    </style>
    """,
    unsafe_allow_html=True
)

# Feature showcase — staggered cards with animation delay
cols = st.columns([1, 1.2, 1])
with cols[0]:
    st.markdown(
        f"""
        <div class='dev-card glow-hover animate-fade' style='animation-delay: 0.2s;'>
            <h3>🔬 Science Forge</h3>
            <p>NGSS + New Visions lessons • 5E builder • SCI-BLOCK exports</p>
            <span class='badge badge-accent'>Core Production</span>
        </div>
        """, unsafe_allow_html=True
    )

with cols[1]:
    st.markdown(
        f"""
        <div class='dev-card glow-hover animate-fade' style='animation-delay: 0.5s; transform: translateY(-12px);'>
            <h3>📚 Code Arsenal</h3>
            <p>Glassy components • Export patterns • Session mastery</p>
            <span class='badge badge-accent'>Canonical Snippets</span>
        </div>
        """, unsafe_allow_html=True
    )

with cols[2]:
    st.markdown(
        f"""
        <div class='dev-card glow-hover animate-fade' style='animation-delay: 0.8s;'>
            <h3>⚡ ABC Engine</h3>
            <p>Architecture • Build • Code • Style decisions — instant starters</p>
            <span class='badge badge-accent'>Decision Accelerator</span>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("<div class='hr' style='margin: 60px 0;'></div>", unsafe_allow_html=True)

# Enhanced CTA with pulse + gradient
st.markdown(
    f"""
    <div class='dev-card' style='text-align:center; background: linear-gradient(135deg, rgba(20,184,166,0.18), rgba(47,91,234,0.14)); animation: pulse 6s infinite;'>
        <h3 style='font-size: 2.4rem; margin-bottom: 16px;'>Ready to Forge?</h3>
        <p style='font-size: 1.2rem; margin: 0 0 24px;'>Launch from sidebar — prototype safely in sandboxes — scale to production.</p>
        <div>
            <span class='badge badge-accent'>NGSS Power</span>
            <span class='badge badge-accent2'>UI Mastery</span>
            <span class='badge badge-accent'>Architecture Clarity</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Retain your quick reference expanders and current state preview below, perhaps in columns for better flow

# ============================================================
# CONFIG & CONSTANTS
# ============================================================

APP_TITLE = "DevForge - Developer Hub"
APP_ICON = "🔧"
ADMIN_CODE = "Bshapp"  # PALM ID admin gate code

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def ss_init(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

ss_init("dev_theme", "science")    # science | neutral | pink
ss_init("signature", "")
ss_init("notes", "")
ss_init("palm_taps", 0)
ss_init("show_admin_box", False)
ss_init("admin_unlocked", False)

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
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

T = get_theme_dict(st.session_state["dev_theme"])

# ============================================================
# CUSTOM CSS (Glassmorphism + Ticker)
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
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='ticker'>DEVFORGE • Developer Productivity Hub • We are L.E.A.D. 🔧</div>", unsafe_allow_html=True)

# ============================================================
# PALM ID ADMIN GATE
# ============================================================

with st.sidebar:
    st.title("🔧 DevForge")
    st.caption("Developer Productivity Hub")
    st.divider()

    # PALM ID trigger
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
            if st.button("Unlock", key="unlock_btn", use_container_width=True):
                if code_try == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    st.success("Admin override unlocked.")
                else:
                    st.error("Incorrect code.")
        with cB:
            if st.button("Reset", key="reset_palm_btn", use_container_width=True):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False

    if st.session_state["admin_unlocked"]:
        st.caption("✅ Palm ID: unlocked")

    st.divider()

    # Theme selector (Pink only visible when unlocked)
    theme_options = ["Science", "Neutral"]
    if st.session_state["admin_unlocked"]:
        theme_options.append("Pink")

    current = st.session_state.get("dev_theme", "science")
    idx = {"science": 0, "neutral": 1, "pink": 2}.get(current, 0)

    theme_choice = st.radio("Dev Theme", theme_options, index=idx, horizontal=True, key="theme_radio")
    choice_map = {"Science": "science", "Neutral": "neutral", "Pink": "pink"}
    selected = choice_map[theme_choice]
    if selected != st.session_state["dev_theme"]:
        st.session_state["dev_theme"] = selected
        st.rerun()

    st.divider()

    # Quick session info
    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")
    sig = st.session_state.get("signature", "")
    st.write(f"**Dev:** {sig or 'Not set'}")

    st.divider()

    # Scratch notes
    st.subheader("📝 Scratch Notes")
    st.session_state["notes"] = st.text_area(
        "Notes", value=st.session_state["notes"], height=110,
        placeholder="Quick notes while you build...", label_visibility="collapsed"
    )

    st.divider()

    # Admin tools (only when unlocked)
    if st.session_state["admin_unlocked"]:
        st.subheader("🧰 Admin Tools")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Reset Theme", use_container_width=True):
                st.session_state["dev_theme"] = "science"
                st.rerun()
        with c2:
            if st.button("Clear Notes", use_container_width=True):
                st.session_state["notes"] = ""
                st.rerun()
        if st.button("Lock Admin Gate", use_container_width=True):
            st.session_state["admin_unlocked"] = False
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False
            st.rerun()

# ============================================================
# DYNAMIC NAVIGATION (core improvement)
# ============================================================

home = st.Page(__file__, title="DevForge Home", icon="🔧", default=True)  # self-reference for home

core_pages = [
    st.Page("pages/Ms_Piluso_Science.py", title="Ms. Piluso Science", icon="🔬"),
    st.Page("pages/Code_Library.py",      title="Code Library",      icon="📚"),
    st.Page("pages/ABC_Generator.py",     title="ABC Generator",     icon="⚡"),
]

sandbox_pages = [
    st.Page("pages/my_app1.py", title="Sandbox 1", icon="🧪"),
    st.Page("pages/my_app2.py", title="Sandbox 2", icon="🧪"),
]

admin_pages = []
if st.session_state.get("admin_unlocked", False):
    admin_pages = [
        st.Page("pages/Teacher_Tools.py", title="Teacher Tools (Extended)", icon="🧰"),
        # Add future admin-only pages here — no core file edits required
    ]

sections = {
    "Home": [home],
    "Core Tools": core_pages,
    "Sandboxes": sandbox_pages,
}
if admin_pages:
    sections["Admin Extras"] = admin_pages

pg = st.navigation(sections, position="sidebar")
pg.run()