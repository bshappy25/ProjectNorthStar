import streamlit as st
from dataclasses import dataclass, asdict

# ============================================================
# UI CSS SELECTOR — Streamlit In-App Theme Builder
# - Pick colors / presets
# - Preview multiple components
# - Export reusable code blocks (CSS + Python)
# ============================================================

st.set_page_config(page_title="UI CSS Selector", page_icon="🎨", layout="wide")

# ---------------------------
# Presets (easy starting points)
# ---------------------------
PRESETS = {
    "Neutral Light (DOE-friendly)": {
        "bg": "#F3F4F6",
        "panel": "#FFFFFF",
        "border": "#D1D5DB",
        "text": "#111827",
        "muted": "#6B7280",
        "accent": "#2563EB",
        "accent_text": "#FFFFFF",
        "success": "#16A34A",
        "warning": "#F59E0B",
        "danger": "#DC2626",
        "shadow": "0 10px 20px rgba(0,0,0,0.08)",
        "radius": 18,
    },
    "Science Mode (Cool Lab)": {
        "bg": "#ECFEFF",
        "panel": "#FFFFFF",
        "border": "#A7F3D0",
        "text": "#0F172A",
        "muted": "#334155",
        "accent": "#0EA5E9",
        "accent_text": "#FFFFFF",
        "success": "#22C55E",
        "warning": "#F97316",
        "danger": "#EF4444",
        "shadow": "0 14px 26px rgba(2,132,199,0.12)",
        "radius": 20,
    },
    "Dark Neon (Arcade)": {
        "bg": "#0B1020",
        "panel": "#0F172A",
        "border": "#1F2A44",
        "text": "#E5E7EB",
        "muted": "#9CA3AF",
        "accent": "#A855F7",
        "accent_text": "#0B1020",
        "success": "#34D399",
        "warning": "#FBBF24",
        "danger": "#FB7185",
        "shadow": "0 16px 32px rgba(168,85,247,0.12)",
        "radius": 22,
    },
    "Warm Pastel (Calm)": {
        "bg": "#FFF7ED",
        "panel": "#FFFFFF",
        "border": "#FED7AA",
        "text": "#1F2937",
        "muted": "#6B7280",
        "accent": "#F97316",
        "accent_text": "#111827",
        "success": "#10B981",
        "warning": "#EAB308",
        "danger": "#EF4444",
        "shadow": "0 12px 24px rgba(249,115,22,0.10)",
        "radius": 18,
    },
}

# ---------------------------
# Theme model
# ---------------------------
@dataclass
class ThemeTokens:
    bg: str
    panel: str
    border: str
    text: str
    muted: str
    accent: str
    accent_text: str
    success: str
    warning: str
    danger: str
    shadow: str
    radius: int


def theme_to_css_vars(t: ThemeTokens) -> str:
    return f"""
:root {{
  --bg: {t.bg};
  --panel: {t.panel};
  --border: {t.border};
  --text: {t.text};
  --muted: {t.muted};
  --accent: {t.accent};
  --accentText: {t.accent_text};
  --success: {t.success};
  --warning: {t.warning};
  --danger: {t.danger};
  --shadow: {t.shadow};
  --radius: {t.radius}px;
}}
""".strip()


def app_css(t: ThemeTokens) -> str:
    # This CSS styles BOTH: overall page and demo components
    return f"""
<style>
{theme_to_css_vars(t)}

html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
}}

* {{
  box-sizing: border-box;
}}

.block {{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 16px;
}}

.h1 {{
  font-weight: 900;
  letter-spacing: .02em;
  font-size: 1.35rem;
  margin: 0 0 6px 0;
}}

.muted {{
  color: var(--muted);
  font-size: 0.95rem;
}}

.row {{
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}}

.pill {{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.35);
  color: var(--text);
  font-weight: 700;
}}

.pill.success {{
  border-color: color-mix(in srgb, var(--success) 55%, var(--border));
}}
.pill.warning {{
  border-color: color-mix(in srgb, var(--warning) 55%, var(--border));
}}
.pill.danger {{
  border-color: color-mix(in srgb, var(--danger) 55%, var(--border));
}}

.card {{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px;
  box-shadow: var(--shadow);
  min-width: 220px;
}}

.cardTitle {{
  font-weight: 900;
  margin-bottom: 6px;
}}

.btn {{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding: 10px 14px;
  border-radius: calc(var(--radius) - 6px);
  border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--border));
  background: var(--accent);
  color: var(--accentText);
  font-weight: 900;
  text-decoration: none;
  cursor: pointer;
  user-select: none;
}}

.btn.secondary {{
  background: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}}

.btn:hover {{
  filter: brightness(0.98);
}}

.alert {{
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 12px 14px;
  font-weight: 800;
}}

.alert.success {{
  border-color: color-mix(in srgb, var(--success) 60%, var(--border));
  background: color-mix(in srgb, var(--success) 10%, var(--panel));
}}
.alert.warning {{
  border-color: color-mix(in srgb, var(--warning) 60%, var(--border));
  background: color-mix(in srgb, var(--warning) 10%, var(--panel));
}}
.alert.danger {{
  border-color: color-mix(in srgb, var(--danger) 60%, var(--border));
  background: color-mix(in srgb, var(--danger) 10%, var(--panel));
}}

.table {{
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}}
.tr {{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}}
.td {{
  padding: 10px 12px;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}}
.td:first-child {{
  border-left: 1px solid var(--border);
  border-top-left-radius: var(--radius);
  border-bottom-left-radius: var(--radius);
  font-weight: 900;
}}
.td:last-child {{
  border-right: 1px solid var(--border);
  border-top-right-radius: var(--radius);
  border-bottom-right-radius: var(--radius);
  color: var(--muted);
  font-weight: 700;
}}
</style>
""".strip()


# ---------------------------
# Session state init
# ---------------------------
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "Neutral Light (DOE-friendly)"
if "theme" not in st.session_state:
    st.session_state.theme = PRESETS[st.session_state.theme_name].copy()

# ---------------------------
# Sidebar controls
# ---------------------------
with st.sidebar:
    st.markdown("## 🎨 UI CSS Selector")
    st.caption("Pick a preset, then tweak tokens. Export code blocks for other apps.")

    theme_name = st.selectbox(
        "Preset",
        list(PRESETS.keys()),
        index=list(PRESETS.keys()).index(st.session_state.theme_name),
    )

    if theme_name != st.session_state.theme_name:
        st.session_state.theme_name = theme_name
        st.session_state.theme = PRESETS[theme_name].copy()

    st.divider()
    st.markdown("### Tokens")

    t = st.session_state.theme
    t["bg"] = st.color_picker("Background (bg)", t["bg"])
    t["panel"] = st.color_picker("Panel (panel)", t["panel"])
    t["border"] = st.color_picker("Border (border)", t["border"])
    t["text"] = st.color_picker("Text (text)", t["text"])
    t["muted"] = st.color_picker("Muted (muted)", t["muted"])
    t["accent"] = st.color_picker("Accent (accent)", t["accent"])
    t["accent_text"] = st.color_picker("Accent Text (accent_text)", t["accent_text"])

    st.markdown("### Status Colors")
    t["success"] = st.color_picker("Success", t["success"])
    t["warning"] = st.color_picker("Warning", t["warning"])
    t["danger"] = st.color_picker("Danger", t["danger"])

    st.markdown("### Shape / Shadow")
    t["radius"] = st.slider("Radius (px)", 8, 30, int(t["radius"]))
    shadow_mode = st.selectbox(
        "Shadow strength",
        ["Soft", "Medium", "Bold", "Off"],
        index=1,
    )
    if shadow_mode == "Soft":
        t["shadow"] = "0 10px 20px rgba(0,0,0,0.08)"
    elif shadow_mode == "Medium":
        t["shadow"] = "0 14px 26px rgba(0,0,0,0.10)"
    elif shadow_mode == "Bold":
        t["shadow"] = "0 18px 36px rgba(0,0,0,0.14)"
    else:
        t["shadow"] = "none"

    st.divider()
    if st.button("Reset to preset"):
        st.session_state.theme = PRESETS[st.session_state.theme_name].copy()
        st.rerun()

# ---------------------------
# Build current theme + inject CSS
# ---------------------------
theme = ThemeTokens(**st.session_state.theme)
st.markdown(app_css(theme), unsafe_allow_html=True)

# ---------------------------
# Main layout: Preview + Export
# ---------------------------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown(
        f"""
        <div class="block">
          <div class="h1">Preview — {st.session_state.theme_name}</div>
          <div class="muted">These are sample components that will react to your token changes.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # Component gallery
    st.markdown(
        """
        <div class="row">
          <div class="card">
            <div class="cardTitle">Card</div>
            <div class="muted">Panels, borders, text, shadow, radius.</div>
          </div>

          <div class="card">
            <div class="cardTitle">Pills</div>
            <div class="row" style="margin-top:8px">
              <span class="pill success">✅ Success</span>
              <span class="pill warning">⚠️ Warning</span>
              <span class="pill danger">🛑 Danger</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    st.markdown(
        """
        <div class="block">
          <div class="row">
            <a class="btn">Primary Button</a>
            <a class="btn secondary">Secondary Button</a>
            <span class="pill">🧠 Muted label demo</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    st.markdown(
        """
        <div class="row">
          <div class="alert success" style="flex:1">✅ Success alert — you can use this for “Saved / Exported”.</div>
          <div class="alert warning" style="flex:1">⚠️ Warning alert — “Check inputs”.</div>
          <div class="alert danger" style="flex:1">🛑 Danger alert — “Something failed”.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    st.markdown(
        """
        <div class="block">
          <div class="h1" style="font-size:1.05rem">Table-ish rows</div>
          <div class="muted">This is a common teacher-tool pattern (quick status rows).</div>
          <div style="margin-top:10px">
            <table class="table">
              <tr class="tr">
                <td class="td">PBIS Ticket Maker</td>
                <td class="td">Ready • Export OK</td>
              </tr>
              <tr class="tr">
                <td class="td">AI Storyboard</td>
                <td class="td">Draft • Needs Safari check</td>
              </tr>
              <tr class="tr">
                <td class="td">Image Ticker</td>
                <td class="td">Stable • Plug-in widget</td>
              </tr>
            </table>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="block">
          <div class="h1">Export Blocks</div>
          <div class="muted">Copy these into other apps. The tokens stay consistent across projects.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # 1) CSS VARS
    css_vars = theme_to_css_vars(theme)
    st.markdown("### 1) CSS Variables (drop into any HTML/CSS)")
    st.code(css_vars, language="css")

    # 2) Streamlit injector
    injector = f"""# --- UI THEME INJECTOR (Streamlit) ---
import streamlit as st

THEME_CSS = r\"\"\"<style>
{css_vars}

html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
}}
</style>\"\"\"

st.markdown(THEME_CSS, unsafe_allow_html=True)
"""
    st.markdown("### 2) Streamlit CSS Injector (minimal)")
    st.code(injector, language="python")

    # 3) A small helper module (paste as ui_theme.py)
    theme_dict = asdict(theme)
    module_block = f"""# ui_theme.py
# Reusable theme tokens for Streamlit/HTML injection.

THEME = {theme_dict}

def css_vars(theme: dict) -> str:
    return f\"\"\":root {{
  --bg: {{theme['bg']}};
  --panel: {{theme['panel']}};
  --border: {{theme['border']}};
  --text: {{theme['text']}};
  --muted: {{theme['muted']}};
  --accent: {{theme['accent']}};
  --accentText: {{theme['accent_text']}};
  --success: {{theme['success']}};
  --warning: {{theme['warning']}};
  --danger: {{theme['danger']}};
  --shadow: {{theme['shadow']}};
  --radius: {{theme['radius']}}px;
}}\"\"\"

def inject(st_module, theme: dict = None) -> None:
    t = theme or THEME
    st_module.markdown(
        "<style>" + css_vars(t) + "</style>",
        unsafe_allow_html=True
    )
"""
    st.markdown("### 3) Python Theme Module (drop into repo)")
    st.code(module_block, language="python")

    st.markdown("### Quick wiring tip")
    st.markdown(
        """
- Put this app in your repo as `tools/ui_css_selector_app.py`
- Put the exported module as `utils/ui_theme.py`
- In any Streamlit app: `from utils import ui_theme; ui_theme.inject(st)`
        """
    )