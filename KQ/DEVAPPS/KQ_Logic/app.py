# python_hubs/KQ_Logic/app.py
# KQ Logic — PRIVATE Shell Hub (safe scaffold)
# Purpose: container + navigation only (no heavy logic yet)

import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="KQ Logic (Private)",
    page_icon="☯️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# THEME CSS (Light/Dark + Adaptive Text)
# NOTE: Streamlit can't set <html data-theme="..."> directly,
# but we support:
#   - Auto (prefers-color-scheme)
#   - Manual toggle via session_state that swaps CSS variables
# -----------------------------
THEME_CSS = r"""
<style>
/* --- DevForge Theme Maker (Light/Dark + Adaptive Text) --- */
:root{
  color-scheme: light dark;

  --bg: #f3f4f6;
  --card: #ffffff;
  --border: #d1d5db;

  --text: #111827;
  --muted: #6b7280;

  --accent: #2563eb;
  --accent2: #16a34a;

  --shadow: 0 10px 30px rgba(0,0,0,.08);
  --focus: 0 0 0 3px rgba(37,99,235,.25);
}

/* Auto Dark mode (only when no manual override is set) */
@media (prefers-color-scheme: dark){
  :root{
    --bg: #0b0f19;
    --card: #0f172a;
    --border: #22314a;

    --text: #e5e7eb;
    --muted: #9ca3af;

    --accent: #60a5fa;
    --accent2: #34d399;

    --shadow: 0 10px 30px rgba(0,0,0,.45);
    --focus: 0 0 0 3px rgba(96,165,250,.30);
  }
}

/* App chrome */
html, body, .stApp{
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* Typography */
h1,h2,h3,h4,h5,h6, p, li, label, span, div{
  color: var(--text);
}

/* Links */
a{ color: var(--accent) !important; }
a:hover{ filter: brightness(1.05); }

/* Cards / panels */
.kq-card{
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  border-radius: 18px;
  padding: 16px;
}

/* Small muted text */
.kq-muted{ color: var(--muted); }

/* Sidebar polish */
section[data-testid="stSidebar"]{
  background: var(--card) !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] *{
  color: var(--text) !important;
}

/* Buttons */
.stButton > button{
  border-radius: 14px !important;
  padding: 0.55rem 0.9rem !important;
  border: 1px solid transparent !important;
}
.stButton > button:focus{
  box-shadow: var(--focus) !important;
}

/* Select / inputs */
[data-baseweb="select"] > div,
.stTextInput input,
.stTextArea textarea{
  background: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}

/* Remove top padding a bit */
.block-container{
  padding-top: 1.2rem;
}
</style>
"""

# -----------------------------
# MANUAL THEME OVERRIDE (optional)
# -----------------------------
LIGHT_OVERRIDES = {
    "--bg": "#f3f4f6",
    "--card": "#ffffff",
    "--border": "#d1d5db",
    "--text": "#111827",
    "--muted": "#6b7280",
    "--accent": "#2563eb",
    "--accent2": "#16a34a",
    "--shadow": "0 10px 30px rgba(0,0,0,.08)",
    "--focus": "0 0 0 3px rgba(37,99,235,.25)",
}

DARK_OVERRIDES = {
    "--bg": "#0b0f19",
    "--card": "#0f172a",
    "--border": "#22314a",
    "--text": "#e5e7eb",
    "--muted": "#9ca3af",
    "--accent": "#60a5fa",
    "--accent2": "#34d399",
    "--shadow": "0 10px 30px rgba(0,0,0,.45)",
    "--focus": "0 0 0 3px rgba(96,165,250,.30)",
}


def _apply_manual_theme(mode: str) -> None:
    """
    mode: 'auto' | 'light' | 'dark'
    Auto = rely on prefers-color-scheme.
    Light/Dark = inject CSS variable overrides.
    """
    if mode not in ("auto", "light", "dark"):
        mode = "auto"

    if mode == "auto":
        return

    overrides = LIGHT_OVERRIDES if mode == "light" else DARK_OVERRIDES
    css_lines = [":root{"]
    for k, v in overrides.items():
        css_lines.append(f"  {k}: {v};")
    css_lines.append("}")
    st.markdown(f"<style>{''.join(css_lines)}</style>", unsafe_allow_html=True)


# -----------------------------
# SESSION STATE
# -----------------------------
defaults = {
    "kq_theme": "auto",         # auto | light | dark
    "kq_area": "Home",          # nav selection
    "kq_pin": "",               # optional private PIN input (not required)
    "kq_unlocked": True,        # default True (no gate by default)
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -----------------------------
# APPLY CSS
# -----------------------------
st.markdown(THEME_CSS, unsafe_allow_html=True)
_apply_manual_theme(st.session_state["kq_theme"])

# -----------------------------
# SIDEBAR (PRIVATE HUB NAV)
# -----------------------------
with st.sidebar:
    st.markdown("## ☯️ KQ Logic")
    st.caption("Private operating layer — shell hub")

    # Theme toggle
    st.markdown("### Theme")
    st.session_state["kq_theme"] = st.radio(
        "Theme mode",
        options=["auto", "light", "dark"],
        horizontal=True,
        index=["auto", "light", "dark"].index(st.session_state["kq_theme"]),
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Optional privacy gate (disabled by default)
    # If you want this ON later: set kq_unlocked=False by default and compare to a local secret.
    with st.expander("🔒 Privacy (optional)", expanded=False):
        st.caption("Not required. Keep OFF unless you need it.")
        st.session_state["kq_unlocked"] = st.toggle("Enable local unlock gate", value=not (st.session_state.get("kq_unlocked") is False))
        if st.session_state["kq_unlocked"] is False:
            st.session_state["kq_pin"] = st.text_input("Enter PIN", type="password")
            st.info("Gate placeholder only — wire to secrets later.")

    st.markdown("---")

    st.markdown("### Areas")
    st.session_state["kq_area"] = st.selectbox(
        "Navigate",
        options=[
            "Home",
            "Energy",
            "Rings",
            "Identity",
            "Symbols",
            "Logs",
            "Settings",
        ],
        index=[
            "Home",
            "Energy",
            "Rings",
            "Identity",
            "Symbols",
            "Logs",
            "Settings",
        ].index(st.session_state["kq_area"]),
        label_visibility="collapsed",
    )

# -----------------------------
# TOP HEADER
# -----------------------------
left, right = st.columns([0.82, 0.18], vertical_alignment="center")
with left:
    st.title("KQ Logic (Private)")
    st.markdown('<div class="kq-muted">Shell hub only — logic comes later.</div>', unsafe_allow_html=True)

with right:
    st.markdown(
        f"""
        <div class="kq-card" style="padding:10px 12px;">
          <div style="font-weight:700;">Mode</div>
          <div class="kq-muted">{st.session_state["kq_theme"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# -----------------------------
# MAIN CONTENT (PLACEHOLDER PAGES)
# -----------------------------
area = st.session_state["kq_area"]

def card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="kq-card">
          <div style="font-size:1.15rem;font-weight:800;margin-bottom:6px;">{title}</div>
          <div class="kq-muted" style="line-height:1.5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if area == "Home":
    colA, colB = st.columns([0.6, 0.4], vertical_alignment="top")
    with colA:
        card(
            "Purpose",
            "This app is a private container for KQ operating logic. "
            "No demos, no explanations, no pressure. Just scaffolding.",
        )
        st.markdown("")
        card(
            "Rules",
            "• Containment over expression<br>"
            "• Logic over narrative<br>"
            "• Low-energy safe<br>"
            "• One file = one idea",
        )
    with colB:
        card(
            "Next Safe Build",
            "Add *empty* modules one at a time:<br>"
            "modules/energy.py<br>"
            "modules/rings.py<br>"
            "modules/identity.py<br>"
            "modules/symbols.py",
        )

elif area == "Energy":
    card(
        "Energy",
        "Placeholder. Later: Low / Mid / High states with allowed actions and recovery rules.",
    )
    st.markdown("")
    st.info("No logic yet. Add it when you’re calm, not when you’re wired.")

elif area == "Rings":
    card(
        "Rings",
        "Placeholder. Later: scope boundaries (today/week/season/year) + deferral rules.",
    )

elif area == "Identity":
    card(
        "Identity",
        "Placeholder. Later: roles/modes/states — switches, not stories.",
    )

elif area == "Symbols":
    card(
        "Symbols",
        "Placeholder. Later: color/icon mapping as anchors (not aesthetics).",
    )

elif area == "Logs":
    card(
        "Logs",
        "Placeholder. Later: a simple text log that records state changes and decisions.",
    )
    st.markdown("")
    st.text_area("Scratch (local only)", height=200, placeholder="Drop notes here. No structure required.")

elif area == "Settings":
    card(
        "Settings",
        "Placeholder. Later: export/import config, local preferences, and safe reset.",
    )
    st.markdown("")
    st.write("Theme:", st.session_state["kq_theme"])
    st.write("Area:", st.session_state["kq_area"])

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("")
st.markdown('<div class="kq-muted">Private hub • stable shell • no coupling to DevForge</div>', unsafe_allow_html=True)