from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

import streamlit as st

# ============================================================
# DEVFORGE OVERHAUL v2 (per DEV FORGE UPDATEv2.pdf)
# - Universal Gray = DEFAULT
# - Science = Green
# - Unlock Mode = Blush Pink (admin only)
# - Home = keep same
# - Core: Piluso Science, ABC, Code Library, NGSS Research Vault + add NACLI v2
# - Sandboxes: 1, 2
# - Admin: CSS Editor, Teacher Tools + add Home Editor
# ============================================================

# ============================================================
# FILESYSTEM PATHS & SETTINGS PERSISTENCE
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PAGES_DIR = APP_DIR / "pages"
SETTINGS_FILE = APP_DIR / ".devforge_settings.json"

def safe_read_json(path: Path, default: dict) -> dict:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default

def safe_write_json(path: Path, data: dict) -> None:
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        # Never crash the app due to filesystem issues
        pass

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def ss_init(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

# Load persisted settings first (so they become defaults)
persisted = safe_read_json(
    SETTINGS_FILE,
    default={
        "dev_theme": "universal",   # universal | science | unlock
        "signature": "",
        "notes": "",
        "custom_css": "",
        "palm_taps": 0,
        "admin_unlocked": False,
        "show_admin_box": False,
    },
)

ss_init("dev_theme", persisted.get("dev_theme", "universal"))
ss_init("signature", persisted.get("signature", ""))
ss_init("notes", persisted.get("notes", ""))
ss_init("custom_css", persisted.get("custom_css", ""))

ss_init("palm_taps", int(persisted.get("palm_taps", 0)))
ss_init("show_admin_box", bool(persisted.get("show_admin_box", False)))
ss_init("admin_unlocked", bool(persisted.get("admin_unlocked", False)))

# Small internal flags
ss_init("settings_dirty", False)
ss_init("last_save_ts", persisted.get("last_save_ts", ""))

ADMIN_CODE = "Bshapp"  # PALM ID admin gate code

def persist_now() -> None:
    payload = {
        "dev_theme": st.session_state.get("dev_theme", "universal"),
        "signature": st.session_state.get("signature", ""),
        "notes": st.session_state.get("notes", ""),
        "custom_css": st.session_state.get("custom_css", ""),
        "palm_taps": st.session_state.get("palm_taps", 0),
        "admin_unlocked": st.session_state.get("admin_unlocked", False),
        "show_admin_box": st.session_state.get("show_admin_box", False),
        "last_save_ts": datetime.now().isoformat(timespec="seconds"),
    }
    safe_write_json(SETTINGS_FILE, payload)
    st.session_state["last_save_ts"] = payload["last_save_ts"]
    st.session_state["settings_dirty"] = False

def mark_dirty() -> None:
    st.session_state["settings_dirty"] = True

# ============================================================
# THEME DEFINITIONS (UI OVERHAUL)
# ============================================================

@dataclass(frozen=True)
class Theme:
    BG: str
    CARD: str
    BORDER: str
    TEXT: str
    MUTED: str
    ACCENT: str
    ACCENT2: str
    ACCENT_RGB: str  # "r,g,b" for glow effects

UNIVERSAL = Theme(
    BG="#0b0f17",  # universal gray glass vibe
    CARD="rgba(200,200,200,0.10)",
    BORDER="rgba(220,220,220,0.16)",
    TEXT="rgba(255,255,255,0.92)",
    MUTED="rgba(255,255,255,0.70)",
    ACCENT="#BFC7D5",   # soft gray-blue accent
    ACCENT2="#7AA2FF",
    ACCENT_RGB="191,199,213",
)

SCIENCE = Theme(
    BG="#061B15",
    CARD="rgba(255,255,255,0.08)",
    BORDER="rgba(120,255,220,0.30)",
    TEXT="rgba(255,255,255,0.92)",
    MUTED="rgba(255,255,255,0.74)",
    ACCENT="#14B8A6",
    ACCENT2="#2F5BEA",
    ACCENT_RGB="20,184,166",
)

UNLOCK = Theme(
    BG="#140914",
    CARD="rgba(255,192,203,0.10)",
    BORDER="rgba(255,105,180,0.35)",
    TEXT="rgba(255,255,255,0.92)",
    MUTED="rgba(255,255,255,0.72)",
    ACCENT="#FF4DA6",
    ACCENT2="#FFB3D9",
    ACCENT_RGB="255,77,166",
)

def get_theme(theme_key: str, admin_unlocked: bool) -> Theme:
    # Unlock theme is admin-only
    if theme_key == "unlock" and admin_unlocked:
        return UNLOCK
    if theme_key == "science":
        return SCIENCE
    return UNIVERSAL  # universal gray default

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DevForge - Developer Hub",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

T = get_theme(st.session_state["dev_theme"], st.session_state["admin_unlocked"])

# ============================================================
# CUSTOM CSS (Base + User Overrides from CSS Editor)
# ============================================================

base_css = f"""
<style>
:root {{
  --bg: {T.BG};
  --card: {T.CARD};
  --border: {T.BORDER};
  --text: {T.TEXT};
  --muted: {T.MUTED};
  --accent: {T.ACCENT};
  --accent2: {T.ACCENT2};
  --accent-rgb: {T.ACCENT_RGB};
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

h1,h2,h3,h4,h5,h6,p,span,label,div {{
  color: var(--text) !important;
}}

small,.stCaption,.muted {{
  color: var(--muted) !important;
}}

input,textarea,select,button {{
  background-color: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
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

@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes pulse {{
  0%, 100% {{ transform: scale(1); }}
  50% {{ transform: scale(1.05); }}
}}

.animate-fade {{ animation: fadeInUp 1.0s ease-out forwards; }}

.glow-hover:hover {{
  box-shadow: 0 0 30px rgba(var(--accent-rgb), 0.38);
  transition: box-shadow 0.35s ease;
}}
</style>
"""

custom_css = st.session_state.get("custom_css", "")
st.markdown(base_css + custom_css, unsafe_allow_html=True)

# Footer ticker
theme_label = st.session_state["dev_theme"].upper()
lock_badge = " • 🔓 UNLOCKED" if st.session_state["admin_unlocked"] else ""
st.markdown(
    f"<div class='ticker'>DEVFORGE • Developer Productivity Hub • Theme: {theme_label}{lock_badge} • We are L.E.A.D. 🔧</div>",
    unsafe_allow_html=True,
)

# ============================================================
# DYNAMIC NAVIGATION (per DEVFORGE UPDATE v2)
# ============================================================

def P(name: str) -> str:
    return str(PAGES_DIR / name)

home_page = st.Page(
    P("home.py"),
    title="DevForge Home",
    icon="🔧",
    default=True,
)

core_pages = [
    st.Page(P("Ms_Piluso_Science.py"), title="Ms. Piluso Science", icon="🔬"),
    st.Page(P("Code_Library.py"), title="Code Library", icon="📚"),
    st.Page(P("ABC_Generator.py"), title="ABC Generator", icon="⚡"),
    st.Page(P("ngss_ms_research_vault_app.py"), title="NGSS Research Vault", icon="🗄️"),
    # ADD NEW: NACLI v2
    st.Page(P("Nacli_v2.py"), title="NACLI v2", icon="🧱"),
]

sandbox_pages = [
    st.Page(P("my_app1.py"), title="Sandbox 1", icon="🧪"),
    st.Page(P("my_app2.py"), title="Sandbox 2", icon="🧪"),
]

admin_pages = []
if st.session_state.get("admin_unlocked", False):
    admin_pages = [
        st.Page(P("Teacher_Tools.py"), title="Teacher Tools", icon="🧰"),
        st.Page(P("CSS_Editor.py"), title="CSS Editor", icon="🎨"),
        # ADD NEW: Home Editor
        st.Page(P("Home_Editor.py"), title="Home Editor", icon="🏠"),
    ]

sections = {
    "Home": [home_page],
    "Core Tools": core_pages,
    "Sandboxes": sandbox_pages,
}

if admin_pages:
    sections["Admin Extras"] = admin_pages

pg = st.navigation(sections, position="sidebar", expanded=True)

# ============================================================
# SIDEBAR CUSTOM CONTENT
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
            mark_dirty()
            if st.session_state["palm_taps"] >= 3:
                st.session_state["show_admin_box"] = True
                mark_dirty()

    if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
        st.markdown("**Palm ID:** enter admin code")
        code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...")
        cA, cB = st.columns([0.6, 0.4])
        with cA:
            if st.button("Unlock", use_container_width=True):
                if code_try == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    mark_dirty()
                    st.success("Admin override unlocked.")
                    st.rerun()
                else:
                    st.error("Incorrect code.")
        with cB:
            if st.button("Reset", use_container_width=True):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False
                mark_dirty()
                st.rerun()

    if st.session_state["admin_unlocked"]:
        st.caption("✅ Palm ID: unlocked")

    st.divider()

    # Theme Toggle (Universal Gray default; Unlock mode admin-only)
    theme_options = ["Universal", "Science"]
    if st.session_state["admin_unlocked"]:
        theme_options.append("Unlock Mode")

    current = st.session_state["dev_theme"]
    idx_map = {"universal": 0, "science": 1, "unlock": 2}
    idx = idx_map.get(current, 0)

    theme_choice = st.radio("Dev Theme", theme_options, index=idx, horizontal=True)
    choice_map = {"Universal": "universal", "Science": "science", "Unlock Mode": "unlock"}

    new_theme = choice_map[theme_choice]
    if new_theme != current:
        st.session_state["dev_theme"] = new_theme
        mark_dirty()
        st.rerun()

    st.divider()

    # Signature
    st.subheader("✍️ Signature")
    sig = st.text_input(
        "Dev name",
        value=st.session_state.get("signature", ""),
        placeholder="Set your dev signature…",
        label_visibility="collapsed",
    )
    if sig != st.session_state.get("signature", ""):
        st.session_state["signature"] = sig
        mark_dirty()

    st.divider()

    # Session Info
    st.subheader("📊 Session Info")
    st.write(f"**Date:** {date.today().isoformat()}")
    st.write(f"**Dev:** {st.session_state.get('signature', 'Not set')}")
    if st.session_state.get("last_save_ts"):
        st.caption(f"Last save: {st.session_state['last_save_ts']}")
    else:
        st.caption("Last save: (none)")

    st.divider()

    # Scratch Notes
    st.subheader("📝 Scratch Notes")
    notes_val = st.text_area(
        "Notes",
        value=st.session_state.get("notes", ""),
        height=120,
        placeholder="Quick notes while you build…",
        label_visibility="collapsed",
    )
    if notes_val != st.session_state.get("notes", ""):
        st.session_state["notes"] = notes_val
        mark_dirty()

    st.divider()

    # Settings Controls (adds real “hub” power)
    st.subheader("💾 Settings")
    a, b = st.columns(2)
    with a:
        if st.button("Save now", use_container_width=True, type="primary"):
            persist_now()
            st.success("Saved.")
    with b:
        if st.button("Reset local", use_container_width=True):
            # wipe file + reset keys
            try:
                if SETTINGS_FILE.exists():
                    SETTINGS_FILE.unlink()
            except Exception:
                pass
            for k in ["dev_theme", "signature", "notes", "custom_css", "palm_taps", "show_admin_box", "admin_unlocked"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    if st.session_state.get("settings_dirty", False):
        st.caption("⚠️ Unsaved changes")

    st.divider()

    # Admin Tools
    if st.session_state["admin_unlocked"]:
        st.subheader("🧰 Admin Tools")
        if st.button("Reset Theme to Universal", use_container_width=True):
            st.session_state["dev_theme"] = "universal"
            mark_dirty()
            st.rerun()

        if st.button("Clear Scratch Notes", use_container_width=True):
            st.session_state["notes"] = ""
            mark_dirty()
            st.rerun()

        if st.button("Lock Admin Gate", use_container_width=True):
            st.session_state["admin_unlocked"] = False
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False
            # If they were on unlock theme, knock them back to universal
            if st.session_state.get("dev_theme") == "unlock":
                st.session_state["dev_theme"] = "universal"
            mark_dirty()
            st.rerun()

    # Optional diagnostics (keep off by default for cleanliness)
    with st.expander("⚙️ Diagnostics", expanded=False):
        st.caption("Paths")
        st.code(f"APP_DIR = {APP_DIR}\nPAGES_DIR = {PAGES_DIR}\nSETTINGS_FILE = {SETTINGS_FILE}", language="text")
        st.caption("Theme key")
        st.code(st.session_state.get("dev_theme", "universal"), language="text")

# ============================================================
# RUN THE SELECTED PAGE
# ============================================================

# Auto-save lightly (optional): if you want, uncomment this to save whenever leaving the sidebar
# if st.session_state.get("settings_dirty", False):
#     persist_now()

pg.run()

