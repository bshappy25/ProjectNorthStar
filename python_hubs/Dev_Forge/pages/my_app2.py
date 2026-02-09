# ============================================================
# my_app2.py — SAFE TOP SECTION (ORDER MATTERS)
# ============================================================

import streamlit as st
from pathlib import Path
from textwrap import dedent
import json
import re

st.set_page_config(
    page_title="UI Theme Builder — Palettes + Overlay",
    layout="wide"
)

# ============================================================
# GUARDED GLOBALS (must exist before use)
# ============================================================

# Always guarantee PALETTES exists before any .update()
PALETTES = globals().get("PALETTES")
if not isinstance(PALETTES, dict):
    PALETTES = {}

# Session-safe storage key names
CUSTOM_PALETTES_KEY = "custom_palettes_app2"
CUSTOM_PALETTES_PATH = Path("custom_palettes_app2.json")

# ============================================================
# CUSTOM PALETTE STORAGE HELPERS (NO session_state YET)
# ============================================================

def _slug(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 _-]", "", s)
    return s[:48].strip() or "custom"

def _load_custom_palettes() -> dict:
    if CUSTOM_PALETTES_PATH.exists():
        try:
            data = json.loads(CUSTOM_PALETTES_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def _save_custom_palettes(palettes: dict) -> None:
    CUSTOM_PALETTES_PATH.write_text(
        json.dumps(palettes, indent=2),
        encoding="utf-8"
    )

# ============================================================
# STREAMLIT-SAFE MERGE (CALL ONLY AFTER FIRST RENDER)
# ============================================================

def merge_custom_palettes_into_PALETTES():
    """
    Safe to call AFTER Streamlit has initialized.
    Never call this at import time.
    """
    if CUSTOM_PALETTES_KEY not in st.session_state:
        st.session_state[CUSTOM_PALETTES_KEY] = _load_custom_palettes()

    for k, v in st.session_state[CUSTOM_PALETTES_KEY].items():
        if isinstance(v, dict):
            PALETTES.setdefault(k, v)

# ============================================================
# 🚨 DO NOT CALL merge_custom_palettes_into_PALETTES() HERE
# ============================================================

# ----------------------------
# 1) EXTEND PALETTES
# ----------------------------
PALETTES.update({
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
    # science-lean teal/blue-green options
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
})

# ----------------------------
# 2) CUSTOM PALETTE STORAGE
# ----------------------------
CUSTOM_PALETTES_PATH = Path("custom_palettes_app2.json")

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

def merge_custom_palettes_into_PALETTES() -> None:
    st.session_state.setdefault("custom_palettes_app2", _load_custom_palettes())
    for k, v in st.session_state["custom_palettes_app2"].items():
        if isinstance(v, dict) and all(x in v for x in ("bg","surface","surface2","border","text","muted","accent","good","warn","bad")):
            PALETTES.setdefault(k, v)

# IMPORTANT: call this ONCE right after PALETTES definition
merge_custom_palettes_into_PALETTES()

# ----------------------------
# 3) AGGRESSIVE OVERLAYS (replace your lists)
# ----------------------------
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
OVERLAY_LEVELS = ["Low", "Medium", "High", "Extreme"]

# ----------------------------
# 4) AGGRESSIVE overlay_params() (replace your function)
# Returns: (bg_alpha, border_alpha, blur_px, text_opacity, sheen_strength, noise_opacity, scanline_opacity, grid_opacity, glow_strength, shadow_boost, edge_strength)
# ----------------------------
def overlay_params(overlay_type: str, level: str):
    if overlay_type == "None":
        return 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.00, 0.0

    base = {
        "Glass":       (0.10, 0.30, 12, 0.45, 0.16, 0.00, 0.00, 0.00, 0.08, 1.00, 0.06),
        "Frost":       (0.09, 0.26, 16, 0.40, 0.14, 0.06, 0.00, 0.00, 0.10, 1.05, 0.08),
        "Matte":       (0.20, 0.22,  3, 0.30, 0.10, 0.02, 0.00, 0.00, 0.00, 1.15, 0.00),
        "Faded":       (0.08, 0.18,  8, 0.28, 0.08, 0.03, 0.00, 0.00, 0.00, 1.00, 0.00),
        "Noise":       (0.14, 0.20,  0, 0.18, 0.00, 0.12, 0.00, 0.00, 0.00, 1.05, 0.00),
        "Scanlines":   (0.12, 0.20,  0, 0.18, 0.00, 0.04, 0.16, 0.00, 0.04, 1.10, 0.00),
        "Grid":        (0.12, 0.22,  0, 0.18, 0.00, 0.02, 0.00, 0.16, 0.00, 1.05, 0.00),
        "Glow":        (0.10, 0.26, 10, 0.32, 0.12, 0.00, 0.00, 0.00, 0.22, 1.00, 0.00),
        "ShadowHeavy": (0.24, 0.18,  0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.55, 0.00),
        "NeonEdge":    (0.12, 0.34,  8, 0.22, 0.10, 0.00, 0.00, 0.00, 0.14, 1.10, 0.22),
    }.get(overlay_type, (0.10, 0.30, 12, 0.45, 0.16, 0.00, 0.00, 0.00, 0.08, 1.00, 0.06))

    mult = {
        "Low":     (0.85, 0.85, 0.80, 0.80, 0.85, 0.75, 0.75, 0.75, 0.75, 0.95, 0.75),
        "Medium":  (1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00),
        "High":    (1.15, 1.15, 1.25, 1.25, 1.15, 1.25, 1.25, 1.25, 1.25, 1.15, 1.25),
        "Extreme": (1.30, 1.30, 1.60, 1.55, 1.30, 1.60, 1.60, 1.60, 1.60, 1.25, 1.55),
    }.get(level, (1.00,)*11)

    out = []
    for i, v in enumerate(base):
        if i == 2:  # blur_px int
            out.append(int(round(v * mult[i])))
        else:
            out.append(float(v) * float(mult[i]))
    # clamp
    out[0] = min(max(out[0], 0.00), 0.35)  # bg alpha
    out[1] = min(max(out[1], 0.00), 0.65)  # border alpha
    out[3] = min(max(out[3], 0.00), 0.80)  # text opacity
    out[5] = min(out[5], 0.22)             # noise
    out[6] = min(out[6], 0.28)             # scanlines
    out[7] = min(out[7], 0.24)             # grid
    out[8] = min(out[8], 0.35)             # glow
    out[10] = min(out[10], 0.35)           # edge
    return tuple(out)

# ----------------------------
# 5) PATCH build_css() to use new overlay vars (add these to :root and pseudo layers)
# ---- add vars: --ov_noise, --ov_scan, --ov_grid, --ov_glow, --ov_shadow_boost, --ov_edge
# ---- add in overlay-card box-shadow extras + background overlays
# ----------------------------
# In build_css(), inside :root add:
#   --ov_noise: {cfg["ov_noise"]};
#   --ov_scan: {cfg["ov_scan"]};
#   --ov_grid: {cfg["ov_grid"]};
#   --ov_glow: {cfg["ov_glow"]};
#   --ov_shadow_boost: {cfg["ov_shadow_boost"]};
#   --ov_edge: {cfg["ov_edge"]};
#
# Then replace .overlay-card with:
#   box-shadow: 0 10px 28px rgba(0,0,0, calc(0.10 * var(--ov_shadow_boost))),
#               0 0 calc(18px * var(--ov_glow)) color-mix(in srgb, var(--accent) 65%, transparent),
#               0 0 0 calc(2px * var(--ov_edge)) color-mix(in srgb, var(--accent) 60%, transparent);
#
# And add these layers:
#   .overlay-card:after {  (noise + scanlines + grid)
# ----------------------------

# Drop-in CSS fragment you can paste into your build_css() output (replace overlay-card section):
OVERLAY_CSS_PATCH = """
    .overlay-card{
      background: var(--ov_bg);
      border: 1px solid var(--ov_border);
      border-radius: var(--radius);
      padding: 18px;
      backdrop-filter: blur(var(--ov_blur));
      -webkit-backdrop-filter: blur(var(--ov_blur));
      position: relative;
      overflow: hidden;
      box-shadow:
        0 10px 28px rgba(0,0,0, calc(0.10 * var(--ov_shadow_boost))),
        0 0 calc(18px * var(--ov_glow)) color-mix(in srgb, var(--accent) 65%, transparent),
        0 0 0 calc(2px * var(--ov_edge)) color-mix(in srgb, var(--accent) 60%, transparent);
    }

    .overlay-card:before{
      content:"";
      position:absolute;
      inset:0;
      background: linear-gradient(
        135deg,
        rgba(255,255,255,var(--ov_sheen)) 0%,
        rgba(255,255,255,0.05) 35%,
        rgba(255,255,255,0.00) 62%
      );
      pointer-events:none;
      mix-blend-mode: screen;
    }

    .overlay-card:after{
      content:"";
      position:absolute;
      inset:0;
      pointer-events:none;
      background:
        /* GRID */
        repeating-linear-gradient(0deg, rgba(255,255,255,var(--ov_grid)) 0 1px, transparent 1px 36px),
        repeating-linear-gradient(90deg, rgba(255,255,255,var(--ov_grid)) 0 1px, transparent 1px 36px),
        /* SCANLINES */
        repeating-linear-gradient(0deg, rgba(0,0,0,var(--ov_scan)) 0 1px, transparent 1px 5px),
        /* NOISE (cheap) */
        radial-gradient(circle at 10% 10%, rgba(255,255,255,var(--ov_noise)) 0 1px, transparent 2px),
        radial-gradient(circle at 30% 70%, rgba(255,255,255,var(--ov_noise)) 0 1px, transparent 2px),
        radial-gradient(circle at 70% 20%, rgba(255,255,255,var(--ov_noise)) 0 1px, transparent 2px),
        radial-gradient(circle at 90% 90%, rgba(255,255,255,var(--ov_noise)) 0 1px, transparent 2px);
      background-size: 36px 36px, 36px 36px, auto, 120px 120px;
      mix-blend-mode: overlay;
      opacity: 1;
    }
"""

# ----------------------------
# 6) CUSTOM PALETTE MAKER UI (paste INSIDE your sidebar, near Palette select)
# ----------------------------
def custom_palette_maker_ui():
    st.session_state.setdefault("custom_palettes_app2", _load_custom_palettes())
    customs = st.session_state["custom_palettes_app2"]

    with st.expander("🧪 Make your own palette (saved)", expanded=False):
        base_name = st.selectbox("Start from", options=sorted(PALETTES.keys()), index=0)
        base = PALETTES[base_name].copy()

        name = st.text_input("Name", value=f"{base_name} custom")
        c1, c2 = st.columns(2, gap="medium")

        with c1:
            bg = st.color_picker("bg", base["bg"])
            surface = st.color_picker("surface", base["surface"])
            surface2 = st.color_picker("surface2", base["surface2"])
            border = st.color_picker("border", base["border"])
            text = st.color_picker("text", base["text"])

        with c2:
            muted = st.color_picker("muted", base["muted"])
            accent = st.color_picker("accent", base["accent"])
            good = st.color_picker("good", base["good"])
            warn = st.color_picker("warn", base["warn"])
            bad = st.color_picker("bad", base["bad"])

        candidate = {
            "bg": bg, "surface": surface, "surface2": surface2, "border": border,
            "text": text, "muted": muted, "accent": accent,
            "good": good, "warn": warn, "bad": bad,
        }

        key = _slug(name)

        colA, colB, colC = st.columns([1,1,1], gap="small")
        with colA:
            if st.button("💾 Save", use_container_width=True):
                customs[key] = candidate
                _save_custom_palettes(customs)
                st.success(f"Saved: {key}")
        with colB:
            if st.button("➕ Add to palette list", use_container_width=True):
                PALETTES[key] = candidate
                st.success(f"Added to PALETTES: {key}")
        with colC:
            if st.button("🧹 Reset", use_container_width=True):
                st.rerun()

        st.caption("Saved palettes persist in `custom_palettes_app2.json` next to this app.")

        if customs:
            st.divider()
            pick = st.selectbox("Saved palettes", options=sorted(customs.keys()))
            st.code(json.dumps(customs[pick], indent=2), language="json")

            d1, d2 = st.columns(2)
            with d1:
                if st.button("Use selected now"):
                    PALETTES[pick] = customs[pick]
                    st.session_state.cfg["palette"] = pick
                    st.session_state.cfg.update(customs[pick])
                    st.success(f"Now using: {pick}")

            with d2:
                if st.button("Delete selected"):
                    customs.pop(pick, None)
                    _save_custom_palettes(customs)
                    st.warning(f"Deleted: {pick}")
                    st.rerun()

# ============================================================
# EXACT WIRING YOU MUST DO (2 lines)
# ============================================================
# A) Right after your Palette select in the sidebar, call:
#     custom_palette_maker_ui()
#
# B) In your Save block AND live preview block, replace:
#     bg_a, border_a, blur_px, text_op, sheen = overlay_params(...)
#    with:
#     bg_a, border_a, blur_px, text_op, sheen, ov_noise, ov_scan, ov_grid, ov_glow, ov_shadow_boost, ov_edge = overlay_params(...)
#    and include these in export_cfg / live_cfg:
#     "ov_noise": ov_noise,
#     "ov_scan": ov_scan,
#     "ov_grid": ov_grid,
#     "ov_glow": ov_glow,
#     "ov_shadow_boost": ov_shadow_boost,
#     "ov_edge": ov_edge,
#
# Then paste OVERLAY_CSS_PATCH into your build_css() output, replacing the old overlay-card CSS section.
# ============================================================