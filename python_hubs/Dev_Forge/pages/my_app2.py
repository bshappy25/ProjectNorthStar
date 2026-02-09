# ============================================================
# PALETTES (extended) + AGGRESSIVE OVERLAYS + CUSTOM MAKER
# Drop-in block: paste below your existing PALETTES/FONTS defs.
# Requires: import json, re
# ============================================================

import json, re
from pathlib import Path
import streamlit as st

# ---------- storage ----------
CUSTOM_PALETTES_PATH = Path("custom_palettes.json")

def _load_custom_palettes() -> dict:
    if CUSTOM_PALETTES_PATH.exists():
        try:
            data = json.loads(CUSTOM_PALETTES_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def _save_custom_palettes(palettes: dict) -> None:
    CUSTOM_PALETTES_PATH.write_text(json.dumps(palettes, indent=2), encoding="utf-8")

def _slug(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 _-]", "", s)
    return s[:48].strip() or "custom"

def _is_hex(c: str) -> bool:
    return bool(re.fullmatch(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", (c or "").strip()))

# ---------- more palettes ----------
PALETTES.update({
    # Soft neutrals / “easy to look at”
    "paper": {
        "bg": "#f5f5f5",
        "surface": "#ffffff",
        "surface2": "#eeeeee",
        "border": "#d6d6d6",
        "text": "#111111",
        "muted": "#444444",
        "accent": "#111111",
        "good": "#0a7a2f",
        "warn": "#b45309",
        "bad": "#b91c1c",
    },
    "cloud": {
        "bg": "#f7f8fb",
        "surface": "#ffffff",
        "surface2": "#f1f3f7",
        "border": "#d7dbe5",
        "text": "#0f172a",
        "muted": "#475569",
        "accent": "#111827",
        "good": "#15803d",
        "warn": "#b45309",
        "bad": "#b91c1c",
    },
    "stone": {
        "bg": "#f2f2f2",
        "surface": "#ffffff",
        "surface2": "#eaeaea",
        "border": "#cfcfcf",
        "text": "#111111",
        "muted": "#3f3f3f",
        "accent": "#111111",
        "good": "#166534",
        "warn": "#a16207",
        "bad": "#991b1b",
    },

    # Science-ish / teal-blue-green lean
    "aqua_lab": {
        "bg": "#031b1f",
        "surface": "#062a30",
        "surface2": "#042227",
        "border": "#0c3a41",
        "text": "#e6fffb",
        "muted": "#7dd3cf",
        "accent": "#2dd4bf",
        "good": "#34d399",
        "warn": "#fbbf24",
        "bad": "#fb7185",
    },
    "ocean_mint": {
        "bg": "#06222a",
        "surface": "#0b2f38",
        "surface2": "#07252c",
        "border": "#124754",
        "text": "#e8fffb",
        "muted": "#93c5bd",
        "accent": "#38bdf8",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#f97316",
    },

    # High-contrast “dashboard” looks
    "terminal": {
        "bg": "#050505",
        "surface": "#0b0b0b",
        "surface2": "#111111",
        "border": "#2b2b2b",
        "text": "#eaeaea",
        "muted": "#a3a3a3",
        "accent": "#22c55e",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#ef4444",
    },
    "night_vision": {
        "bg": "#020a05",
        "surface": "#05110a",
        "surface2": "#041009",
        "border": "#0b2417",
        "text": "#d1fae5",
        "muted": "#6ee7b7",
        "accent": "#10b981",
        "good": "#34d399",
        "warn": "#fbbf24",
        "bad": "#fb7185",
    },

    # Warm / cozy
    "latte": {
        "bg": "#f7f0e6",
        "surface": "#fffaf3",
        "surface2": "#efe3d3",
        "border": "#d6c3aa",
        "text": "#2b2116",
        "muted": "#6b4f3a",
        "accent": "#8b5e34",
        "good": "#166534",
        "warn": "#b45309",
        "bad": "#b91c1c",
    },
    "copper": {
        "bg": "#1b0f0a",
        "surface": "#25140d",
        "surface2": "#1f120c",
        "border": "#4a2a1a",
        "text": "#fff7ed",
        "muted": "#fdba74",
        "accent": "#fb923c",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#f87171",
    },

    # Punchy / playful
    "neon_mango": {
        "bg": "#0a0a0a",
        "surface": "#101010",
        "surface2": "#141414",
        "border": "#2a2a2a",
        "text": "#fff7ed",
        "muted": "#fed7aa",
        "accent": "#f59e0b",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#ef4444",
    },
    "arcade_ice": {
        "bg": "#070a18",
        "surface": "#0e1430",
        "surface2": "#0a1026",
        "border": "#2a3a7a",
        "text": "#eef2ff",
        "muted": "#a5b4fc",
        "accent": "#60a5fa",
        "good": "#34d399",
        "warn": "#fbbf24",
        "bad": "#fb7185",
    },
})

# ---------- aggressive overlays ----------
OVERLAY_TYPES = [
    "None",
    "Glass",
    "Frost",
    "Matte",
    "Faded",
    "Noise",
    "Scanlines",
    "Grid",
    "Glow",
    "ShadowHeavy",
    "NeonEdge",
]

OVERLAY_LEVELS = ["Low", "Medium", "High", "Extreme"]  # more aggressive

_OVERLAY_PRESETS = {
    # Each preset returns CSS vars that your theme can use.
    # We keep it variable-based so it applies “across all components”.
    "None": dict(
        pane_alpha=1.00, blur_px=0, sat=1.00, contrast=1.00, brighten=1.00,
        noise_opacity=0.00, line_opacity=0.00, grid_opacity=0.00,
        glow=0.00, shadow=0.18, edge=0.00
    ),
    "Glass": dict(
        pane_alpha=0.78, blur_px=10, sat=1.25, contrast=1.05, brighten=1.05,
        noise_opacity=0.00, line_opacity=0.00, grid_opacity=0.00,
        glow=0.10, shadow=0.20, edge=0.06
    ),
    "Frost": dict(
        pane_alpha=0.72, blur_px=16, sat=1.20, contrast=1.08, brighten=1.06,
        noise_opacity=0.04, line_opacity=0.00, grid_opacity=0.00,
        glow=0.12, shadow=0.22, edge=0.08
    ),
    "Matte": dict(
        pane_alpha=0.92, blur_px=0, sat=0.98, contrast=1.03, brighten=1.00,
        noise_opacity=0.02, line_opacity=0.00, grid_opacity=0.00,
        glow=0.00, shadow=0.25, edge=0.00
    ),
    "Faded": dict(
        pane_alpha=0.88, blur_px=2, sat=0.85, contrast=0.98, brighten=1.06,
        noise_opacity=0.03, line_opacity=0.00, grid_opacity=0.00,
        glow=0.00, shadow=0.18, edge=0.00
    ),
    "Noise": dict(
        pane_alpha=0.90, blur_px=0, sat=1.00, contrast=1.02, brighten=1.00,
        noise_opacity=0.10, line_opacity=0.00, grid_opacity=0.00,
        glow=0.00, shadow=0.22, edge=0.00
    ),
    "Scanlines": dict(
        pane_alpha=0.88, blur_px=0, sat=1.05, contrast=1.06, brighten=1.00,
        noise_opacity=0.04, line_opacity=0.18, grid_opacity=0.00,
        glow=0.06, shadow=0.25, edge=0.00
    ),
    "Grid": dict(
        pane_alpha=0.90, blur_px=0, sat=1.02, contrast=1.04, brighten=1.00,
        noise_opacity=0.02, line_opacity=0.00, grid_opacity=0.16,
        glow=0.00, shadow=0.22, edge=0.00
    ),
    "Glow": dict(
        pane_alpha=0.82, blur_px=8, sat=1.20, contrast=1.06, brighten=1.04,
        noise_opacity=0.00, line_opacity=0.00, grid_opacity=0.00,
        glow=0.22, shadow=0.18, edge=0.00
    ),
    "ShadowHeavy": dict(
        pane_alpha=0.96, blur_px=0, sat=1.00, contrast=1.02, brighten=1.00,
        noise_opacity=0.00, line_opacity=0.00, grid_opacity=0.00,
        glow=0.00, shadow=0.40, edge=0.00
    ),
    "NeonEdge": dict(
        pane_alpha=0.86, blur_px=6, sat=1.28, contrast=1.10, brighten=1.02,
        noise_opacity=0.00, line_opacity=0.00, grid_opacity=0.00,
        glow=0.14, shadow=0.20, edge=0.20
    ),
}

_LEVEL_MULT = {
    "Low":     dict(a=1.00, blur=0.70, fx=0.70),
    "Medium":  dict(a=1.00, blur=1.00, fx=1.00),
    "High":    dict(a=0.98, blur=1.35, fx=1.35),
    "Extreme": dict(a=0.96, blur=1.85, fx=1.85),
}

def overlay_vars(overlay_type: str, overlay_level: str) -> dict:
    base = _OVERLAY_PRESETS.get(overlay_type, _OVERLAY_PRESETS["None"]).copy()
    mult = _LEVEL_MULT.get(overlay_level, _LEVEL_MULT["Medium"])
    # alpha a little lower at stronger levels to “feel” more overlay-y
    base["pane_alpha"] = max(0.60, min(1.00, base["pane_alpha"] * mult["a"]))
    base["blur_px"] = int(round(base["blur_px"] * mult["blur"]))
    for k in ["sat", "contrast", "brighten", "noise_opacity", "line_opacity", "grid_opacity", "glow", "shadow", "edge"]:
        base[k] = float(base[k]) * float(mult["fx"])
    # clamp a few
    base["noise_opacity"] = min(base["noise_opacity"], 0.22)
    base["line_opacity"] = min(base["line_opacity"], 0.28)
    base["grid_opacity"] = min(base["grid_opacity"], 0.24)
    base["glow"] = min(base["glow"], 0.35)
    base["shadow"] = min(base["shadow"], 0.55)
    base["edge"] = min(base["edge"], 0.35)
    return base

def build_theme_css(palette: dict, font_family: str, overlay_type: str, overlay_level: str) -> str:
    ov = overlay_vars(overlay_type, overlay_level)

    # NOTE: Overlay is applied via CSS variables + pseudo backgrounds
    # so it can hit “all components” consistently.
    return f"""
<style>
:root {{
  --bg:{palette["bg"]};
  --surface:{palette["surface"]};
  --surface2:{palette["surface2"]};
  --border:{palette["border"]};
  --text:{palette["text"]};
  --muted:{palette["muted"]};
  --accent:{palette["accent"]};
  --good:{palette["good"]};
  --warn:{palette["warn"]};
  --bad:{palette["bad"]};

  --font:{font_family};

  --pane-alpha:{ov["pane_alpha"]};
  --blur-px:{ov["blur_px"]}px;
  --sat:{ov["sat"]};
  --contrast:{ov["contrast"]};
  --brighten:{ov["brighten"]};
  --noise-op:{ov["noise_opacity"]};
  --line-op:{ov["line_opacity"]};
  --grid-op:{ov["grid_opacity"]};
  --glow:{ov["glow"]};
  --shadow:{ov["shadow"]};
  --edge:{ov["edge"]};
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
}}

[data-testid="stHeader"], [data-testid="stToolbar"] {{
  background: transparent !important;
}}

[data-testid="stSidebar"] {{
  background: color-mix(in srgb, var(--bg) 85%, #fff 15%) !important;
}}

:where(.stButton>button, .stTextInput input, .stTextArea textarea, .stSelectbox select,
       .stMultiSelect, .stNumberInput input, .stDateInput input, .stTimeInput input) {{
  font-family: var(--font) !important;
}}

:where(.stButton>button) {{
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  background: color-mix(in srgb, var(--surface2) 70%, var(--surface) 30%) !important;
  box-shadow: 0 6px 18px rgba(0,0,0,var(--shadow)) !important;
}}

:where(.stButton>button:hover) {{
  border-color: color-mix(in srgb, var(--border) 50%, var(--accent) 50%) !important;
  transform: translateY(-1px);
}}

:where(.block-container) {{
  padding-top: 1rem;
}}

:where(div[data-testid="stMarkdownContainer"], label, p, span, div) {{
  color: var(--text);
}}

:where(.stCaption, small, .stMarkdown p small) {{
  color: var(--muted) !important;
}}

:where(div[data-testid="stMetric"]) {{
  background: color-mix(in srgb, var(--surface) 78%, var(--bg) 22%) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px;
  padding: 10px 12px;
}}

:where(section.main, [data-testid="stSidebar"]) {{
  /* Core overlay: affects every pane */
  -webkit-backdrop-filter: blur(var(--blur-px)) saturate(var(--sat)) contrast(var(--contrast)) brightness(var(--brighten));
  backdrop-filter: blur(var(--blur-px)) saturate(var(--sat)) contrast(var(--contrast)) brightness(var(--brighten));
}}

:where(section.main) {{
  position: relative;
}}
:where(section.main)::before {{
  content:"";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    /* GRID */
    repeating-linear-gradient(0deg, rgba(255,255,255,var(--grid-op)) 0 1px, transparent 1px 36px),
    repeating-linear-gradient(90deg, rgba(255,255,255,var(--grid-op)) 0 1px, transparent 1px 36px),
    /* SCANLINES */
    repeating-linear-gradient(0deg, rgba(0,0,0,var(--line-op)) 0 1px, transparent 1px 5px);
  mix-blend-mode: overlay;
  opacity: 1;
}}

:where(section.main)::after {{
  content:"";
  position: fixed;
  inset: 0;
  pointer-events: none;
  /* NOISE (cheap CSS noise approximation) */
  background-image:
    radial-gradient(circle at 10% 10%, rgba(255,255,255,var(--noise-op)) 0 1px, transparent 2px),
    radial-gradient(circle at 30% 70%, rgba(255,255,255,var(--noise-op)) 0 1px, transparent 2px),
    radial-gradient(circle at 70% 20%, rgba(255,255,255,var(--noise-op)) 0 1px, transparent 2px),
    radial-gradient(circle at 90% 90%, rgba(255,255,255,var(--noise-op)) 0 1px, transparent 2px);
  background-size: 120px 120px;
  opacity: 1;
}}

/* Surfaces: unify look */
:where(.stContainer, div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"]) {{
  background: rgba(255,255,255,var(--pane-alpha)) !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,var(--shadow)) !important;
}}

:where(div[data-testid="stExpander"] details) {{
  background: transparent !important;
}}

:where(.stAlert) {{
  border-radius: 14px !important;
}}

:where(a) {{
  color: color-mix(in srgb, var(--accent) 70%, var(--text) 30%) !important;
  text-decoration: none;
}}
:where(a:hover) {{
  text-decoration: underline;
}}

/* Neon Edge (subtle, controlled by --edge and --glow) */
:where(.stContainer, div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stExpander"]) {{
  box-shadow:
    0 10px 28px rgba(0,0,0,var(--shadow)),
    0 0 calc(18px * var(--glow)) color-mix(in srgb, var(--accent) 60%, transparent),
    0 0 0 calc(2px * var(--edge)) color-mix(in srgb, var(--accent) 55%, transparent) !important;
}}
</style>
"""

# ---------- custom palette maker UI ----------
def palette_custom_maker_ui(base_palette_name: str = "universal gray") -> None:
    """
    Call inside your Streamlit app to enable:
    - build a custom palette
    - save to custom_palettes.json
    - load & delete customs
    - merge into PALETTES at runtime
    """
    st.session_state.setdefault("custom_palettes", _load_custom_palettes())

    with st.expander("🎛️ Custom Palette Maker", expanded=False):
        colA, colB = st.columns([1, 1], gap="medium")

        with colA:
            st.caption("Start from an existing palette, then tweak.")
            base = st.selectbox("Base palette", options=sorted(PALETTES.keys()), index=sorted(PALETTES.keys()).index(base_palette_name) if base_palette_name in PALETTES else 0)
            base_obj = PALETTES[base].copy()

            name = st.text_input("Custom palette name", value=f"{base} + custom")
            st.markdown("**Colors** (hex like `#f3f4f6`)")

            def cp(key, default):
                return st.color_picker(key, value=base_obj.get(key, default))

            bg = cp("bg", "#f3f4f6")
            surface = cp("surface", "#ffffff")
            surface2 = cp("surface2", "#f8fafc")
            border = cp("border", "#d1d5db")
            text = cp("text", "#111827")
            muted = cp("muted", "#6b7280")
            accent = cp("accent", "#2563eb")
            good = cp("good", "#16a34a")
            warn = cp("warn", "#f59e0b")
            bad = cp("bad", "#ef4444")

            candidate = {
                "bg": bg, "surface": surface, "surface2": surface2, "border": border,
                "text": text, "muted": muted, "accent": accent,
                "good": good, "warn": warn, "bad": bad,
            }

            ok = all(_is_hex(v) for v in candidate.values())
            if not ok:
                st.error("One or more colors are not valid hex codes.")

            if st.button("💾 Save custom palette", type="primary", disabled=not ok):
                key = _slug(name)
                st.session_state["custom_palettes"][key] = candidate
                _save_custom_palettes(st.session_state["custom_palettes"])
                st.success(f"Saved as: {key}")

        with colB:
            st.caption("Manage saved palettes")
            customs = st.session_state["custom_palettes"]
            if customs:
                pick = st.selectbox("Saved custom palettes", options=sorted(customs.keys()))
                st.code(json.dumps(customs[pick], indent=2), language="json")

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("➕ Add to PALETTES for this session"):
                        PALETTES[pick] = customs[pick]
                        st.success(f"Added `{pick}` to PALETTES (runtime).")

                with c2:
                    if st.button("🗑️ Delete saved palette"):
                        customs.pop(pick, None)
                        _save_custom_palettes(customs)
                        st.session_state["custom_palettes"] = customs
                        st.warning(f"Deleted `{pick}`. Rerun app to refresh list.")
            else:
                st.info("No saved custom palettes yet. Create one on the left.")

# ---------- optional helper: ensure customs auto-merge ----------
def merge_custom_palettes_into_PALETTES() -> None:
    st.session_state.setdefault("custom_palettes", _load_custom_palettes())
    for k, v in st.session_state["custom_palettes"].items():
        if isinstance(v, dict) and all(x in v for x in ("bg","surface","surface2","border","text","muted","accent","good","warn","bad")):
            PALETTES.setdefault(k, v)

# ============================================================
# USAGE (example)
# ============================================================
# merge_custom_palettes_into_PALETTES()
# palette_name = st.selectbox("Palette", options=sorted(PALETTES.keys()))
# font_key = st.selectbox("Font", options=sorted(FONTS.keys()))
# overlay_type = st.selectbox("Overlay", options=OVERLAY_TYPES, index=0)
# overlay_level = st.selectbox("Overlay Strength", options=OVERLAY_LEVELS, index=1)
# st.markdown(build_theme_css(PALETTES[palette_name], FONTS[font_key], overlay_type, overlay_level), unsafe_allow_html=True)
# palette_custom_maker_ui(base_palette_name=palette_name)