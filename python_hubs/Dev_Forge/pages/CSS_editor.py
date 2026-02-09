# theme_studio_app2_simple.py
import streamlit as st
from textwrap import dedent
import json

st.set_page_config(page_title="UI Theme Builder — Palettes + Overlay", layout="wide")

# ============================================================
# PALETTES (6 examples)
# Palette structure: bg, surface, surface2, border, text, muted, accent, good, warn, bad
# ============================================================
PALETTES = {
    "blush": {
        "bg": "#fff4f6",
        "surface": "#ffffff",
        "surface2": "#ffe9ee",
        "border": "#f2c7d2",
        "text": "#2a1020",
        "muted": "#7b4b61",
        "accent": "#d9467a",
        "good": "#16a34a",
        "warn": "#f59e0b",
        "bad": "#ef4444",
    },
    "atomic": {
        "bg": "#061019",
        "surface": "#0b1b2a",
        "surface2": "#081523",
        "border": "#1a3550",
        "text": "#eaf6ff",
        "muted": "#8bb3cf",
        "accent": "#22d3ee",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#fb7185",
    },
    "ink": {
        "bg": "#0b0f19",
        "surface": "#121a2b",
        "surface2": "#0e1524",
        "border": "#22314f",
        "text": "#eef2ff",
        "muted": "#97a6c7",
        "accent": "#8b5cf6",
        "good": "#34d399",
        "warn": "#fbbf24",
        "bad": "#f87171",
    },
    "bold": {
        "bg": "#0b0b0b",
        "surface": "#111111",
        "surface2": "#151515",
        "border": "#2a2a2a",
        "text": "#f9fafb",
        "muted": "#a3a3a3",
        "accent": "#3b82f6",
        "good": "#22c55e",
        "warn": "#f59e0b",
        "bad": "#ef4444",
    },
    "vintage": {
        "bg": "#fbf5e8",
        "surface": "#fffdf7",
        "surface2": "#f7e7c9",
        "border": "#d9c6a5",
        "text": "#2a241a",
        "muted": "#6a5b44",
        "accent": "#b45309",
        "good": "#15803d",
        "warn": "#d97706",
        "bad": "#b91c1c",
    },
    "universal gray": {
        "bg": "#f3f4f6",
        "surface": "#ffffff",
        "surface2": "#f8fafc",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "good": "#16a34a",
        "warn": "#f59e0b",
        "bad": "#ef4444",
    },


}

FONTS = {
    "system": "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
    "inter-like": "Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
    "serif": "ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif",
    "mono": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    "comic": "'Comic Sans MS','Chalkboard SE','Comic Neue',cursive,sans-serif",
}

OVERLAY_TYPES = ["None", "Glass", "Matte", "Faded"]
OVERLAY_LEVELS = ["Low", "Medium", "High"]  # used when overlay != None


# ============================================================
# Simple utility: decide light vs dark based on hex bg
# ============================================================
def hex_to_rgb(hex_color: str):
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def relative_luminance(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    # quick perceptual luminance (0..255)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def is_dark_bg(hex_color: str) -> bool:
    return relative_luminance(hex_color) < 130  # threshold works well for UI


# ============================================================
# Overlay mapping
# ============================================================
def overlay_params(overlay_type: str, level: str):
    """
    Returns: (bg_alpha, border_alpha, blur_px, text_opacity, sheen_strength)
    """
    if overlay_type == "None":
        return 0.0, 0.0, 0, 0.0, 0.0

    if overlay_type == "Glass":
        # blur-heavy, translucent
        if level == "Low":
            return 0.07, 0.22, 10, 0.30, 0.12
        if level == "Medium":
            return 0.10, 0.30, 12, 0.45, 0.16
        return 0.14, 0.38, 14, 0.60, 0.20

    if overlay_type == "Matte":
        # little blur, more solid
        if level == "Low":
            return 0.14, 0.22, 2, 0.22, 0.08
        if level == "Medium":
            return 0.20, 0.30, 3, 0.32, 0.10
        return 0.26, 0.38, 4, 0.40, 0.12

    # Faded
    # gentle wash / very subtle border
    if level == "Low":
        return 0.05, 0.16, 6, 0.22, 0.06
    if level == "Medium":
        return 0.08, 0.20, 8, 0.30, 0.08
    return 0.11, 0.24, 10, 0.38, 0.10


# ============================================================
# CSS builder (kept intentionally small + reusable)
# ============================================================
def build_css(cfg: dict) -> str:
    return dedent(f"""
    :root {{
      --bg: {cfg["bg"]};
      --surface: {cfg["surface"]};
      --surface2: {cfg["surface2"]};
      --border: {cfg["border"]};

      --text: {cfg["text"]};
      --muted: {cfg["muted"]};

      --accent: {cfg["accent"]};
      --good: {cfg["good"]};
      --warn: {cfg["warn"]};
      --bad: {cfg["bad"]};

      --radius: {cfg["radius"]}px;
      --pad: {cfg["pad"]}px;
      --font: {cfg["font_family"]};
      --font_weight: {cfg["font_weight"]};

      --shadow: 0 {cfg["shadow_y"]}px {cfg["shadow_blur"]}px rgba(0,0,0,{cfg["shadow_alpha"]});

      /* overlay */
      --ov_bg: rgba(255,255,255,{cfg["ov_bg_alpha"]});
      --ov_border: rgba(120,255,220,{cfg["ov_border_alpha"]});
      --ov_blur: {cfg["ov_blur"]}px;
      --ov_text_opacity: {cfg["ov_text_opacity"]};
      --ov_sheen: {cfg["ov_sheen"]};
      --ov_text_color: rgba(255,255,255,{cfg["ov_text_alpha"]});
      --ov_text_shadow: rgba(0,0,0,{cfg["ov_text_shadow_alpha"]});

      /* ticker */
      --ticker_on: {1 if cfg["ticker_enabled"] else 0};
      --ticker_bg: rgba(255,255,255,{cfg["ticker_alpha"]});
      --ticker_border: rgba(120,255,220,{cfg["ticker_border_alpha"]});
      --ticker_blur: {cfg["ticker_blur"]}px;
      --ticker_size: {cfg["ticker_size"]}rem;
    }}

    html, body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      font-weight: var(--font_weight);
    }}

    [data-testid="stAppViewContainer"] {{
      background: var(--bg);
    }}
    [data-testid="stHeader"] {{
      background: transparent;
    }}

    .block-container {{
      padding-top: 1.25rem;
      padding-bottom: 2.6rem;
    }}

    /* ====== SIMPLE PREVIEW COMPONENTS ====== */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: var(--pad);
      box-shadow: var(--shadow);
    }}

    .row {{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:12px;
      border: 1px solid var(--border);
      background: var(--surface2);
      border-radius: calc(var(--radius) - 2px);
      padding: 10px 12px;
    }}

    .badge {{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid color-mix(in srgb, var(--accent) 35%, var(--border));
      background: color-mix(in srgb, var(--accent) 12%, var(--surface));
      font-weight: 900;
      font-size: 0.85rem;
      white-space: nowrap;
    }}

    .btn {{
      appearance:none;
      border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--border));
      background: linear-gradient(180deg, var(--accent), color-mix(in srgb, var(--accent) 70%, black));
      color: white;
      border-radius: calc(var(--radius) - 2px);
      padding: 10px 12px;
      font-weight: 900;
      cursor: pointer;
      box-shadow: var(--shadow);
    }}

    .muted {{ color: var(--muted); }}

    /* ====== OVERLAY CARD (glassy/matte/faded) ====== */
    .overlay-card {{
      background: var(--ov_bg);
      border: 1px solid var(--ov_border);
      border-radius: var(--radius);
      padding: 18px;
      backdrop-filter: blur(var(--ov_blur));
      -webkit-backdrop-filter: blur(var(--ov_blur));
      position: relative;
      overflow: hidden;
    }}

    .overlay-card:before {{
      content: "";
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
    }}

    .overlay-text {{
      position:absolute;
      inset:0;
      display:flex;
      align-items:center;
      justify-content:center;
      text-align:center;
      padding: 16px;
      opacity: var(--ov_text_opacity);
      color: var(--ov_text_color);
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-weight: 900;
      text-shadow: 0 2px 10px var(--ov_text_shadow);
      pointer-events:none;
    }}

    /* ====== TICKER ====== */
    .ticker {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--ticker_bg);
      border-top: 1px solid var(--ticker_border);
      padding: 8px 20px;
      text-align: center;
      font-size: var(--ticker_size);
      font-weight: 900;
      letter-spacing: 0.06em;
      backdrop-filter: blur(var(--ticker_blur));
      -webkit-backdrop-filter: blur(var(--ticker_blur));
      z-index: 9999;
    }}
    .ticker-spacer {{ height: 64px; }}
    """).strip()


def streamlit_snippet(css_text: str, ticker_on: bool, ticker_text: str) -> str:
    return dedent(f"""
    import streamlit as st

    THEME_CSS = r\"\"\"{css_text}\"\"\"
    st.markdown(f"<style>{{THEME_CSS}}</style>", unsafe_allow_html=True)

    # Optional ticker
    if {bool(ticker_on)}:
        st.markdown(
            \"\"\"<div class='ticker'>{ticker_text}</div><div class='ticker-spacer'></div>\"\"\",
            unsafe_allow_html=True
        )
    """).strip()


# ============================================================
# State defaults
# ============================================================
if "cfg" not in st.session_state:
    # Start with universal gray
    base = PALETTES["universal gray"].copy()
    st.session_state.cfg = {
        "palette": "universal gray",
        **base,

        "radius": 18,
        "pad": 14,
        "shadow_y": 8,
        "shadow_blur": 24,
        "shadow_alpha": 0.12,

        "font_key": "system",
        "font_family": FONTS["system"],
        "font_weight": 900,  # default bold on

        "auto_contrast": True,   # auto sets text/muted based on bg
        "bold_text": True,       # easier switch for weight

        "overlay_type": "Glass",
        "overlay_level": "Medium",

        "ticker_enabled": True,
        "ticker_text": "YOUR MESSAGE • We are L.E.A.D. 🌟",
        "ticker_size": 0.85,
        "ticker_alpha": 0.08,
        "ticker_border_alpha": 0.30,
        "ticker_blur": 10,

        # export "saved" pack (generated only when user presses Save)
        "saved": None,
    }

cfg = st.session_state.cfg


# ============================================================
# Sidebar — palette-first builder
# ============================================================
with st.sidebar:
    st.title("🎨 UI Theme Builder")
    st.caption("Palette-first. Simple. Save → Export blocks.")

    # Palette select
    palette_name = st.selectbox("Palette", list(PALETTES.keys()), index=list(PALETTES.keys()).index(cfg["palette"]))
    if palette_name != cfg["palette"]:
        cfg["palette"] = palette_name
        cfg.update(PALETTES[palette_name])

    st.divider()

    # Overlay
    cfg["overlay_type"] = st.selectbox("Overlay", OVERLAY_TYPES, index=OVERLAY_TYPES.index(cfg["overlay_type"]))
    if cfg["overlay_type"] == "None":
        cfg["overlay_level"] = "Low"  # ignored
        st.caption("Overlay disabled.")
    else:
        cfg["overlay_level"] = st.radio("Overlay intensity", OVERLAY_LEVELS, horizontal=True,
                                        index=OVERLAY_LEVELS.index(cfg["overlay_level"]))

    st.divider()

    # Fonts + bold
    cfg["font_key"] = st.selectbox("Font", list(FONTS.keys()), index=list(FONTS.keys()).index(cfg["font_key"]))
    cfg["font_family"] = FONTS[cfg["font_key"]]
    cfg["bold_text"] = st.toggle("Bold text", value=bool(cfg["bold_text"]))
    cfg["font_weight"] = 900 if cfg["bold_text"] else 500

    st.divider()

    # Auto contrast
    cfg["auto_contrast"] = st.toggle("Auto light/dark contrast", value=bool(cfg["auto_contrast"]))
    if cfg["auto_contrast"]:
        if is_dark_bg(cfg["bg"]):
            cfg["text"] = "#f9fafb"
            cfg["muted"] = "#a3a3a3"
        else:
            # keep palette text but ensure it's readable
            # (palette already sets text/muted; this is a gentle guard)
            cfg["text"] = cfg["text"] if cfg["text"] else "#111827"
            cfg["muted"] = cfg["muted"] if cfg["muted"] else "#6b7280"

    st.divider()

    # Ticker
    cfg["ticker_enabled"] = st.toggle("Ticker", value=bool(cfg["ticker_enabled"]))
    cfg["ticker_text"] = st.text_input("Ticker text", cfg["ticker_text"])
    cfg["ticker_size"] = st.slider("Ticker size (rem)", 0.75, 1.10, float(cfg["ticker_size"]), 0.01)

    st.divider()

    # Small shape controls (kept minimal)
    with st.expander("Advanced (optional)", expanded=False):
        cfg["radius"] = st.slider("Radius", 0, 28, int(cfg["radius"]))
        cfg["shadow_alpha"] = st.slider("Shadow alpha", 0.00, 0.30, float(cfg["shadow_alpha"]), 0.01)

    st.divider()

    # SAVE / EXPORT
    save = st.button("💾 Save + Build Outputs", use_container_width=True)
    if save:
        # map overlay → params
        bg_a, border_a, blur_px, text_op, sheen = overlay_params(cfg["overlay_type"], cfg["overlay_level"])

        # overlay text alpha/shadow alpha depend on background darkness
        dark = is_dark_bg(cfg["bg"])
        ov_text_alpha = 0.70 if dark else 0.55
        ov_text_shadow_alpha = 0.40 if dark else 0.25

        export_cfg = {
            **cfg,
            "ov_bg_alpha": bg_a,
            "ov_border_alpha": border_a,
            "ov_blur": blur_px,
            "ov_text_opacity": text_op,
            "ov_sheen": sheen,
            "ov_text_alpha": ov_text_alpha,
            "ov_text_shadow_alpha": ov_text_shadow_alpha,
        }

        css_text = build_css(export_cfg)
        snippet = streamlit_snippet(css_text, export_cfg["ticker_enabled"], export_cfg["ticker_text"])
        theme_json = json.dumps(export_cfg, indent=2)

        cfg["saved"] = {
            "css": css_text,
            "snippet": snippet,
            "json": theme_json,
            "export_cfg": export_cfg,
        }
        st.success("Saved. Outputs are ready in the Export panel →")


# ============================================================
# Build live CSS (preview uses current cfg values, not only saved)
# ============================================================
bg_a, border_a, blur_px, text_op, sheen = overlay_params(cfg["overlay_type"], cfg["overlay_level"])
dark = is_dark_bg(cfg["bg"])
ov_text_alpha = 0.70 if dark else 0.55
ov_text_shadow_alpha = 0.40 if dark else 0.25

live_cfg = {
    **cfg,
    "ov_bg_alpha": bg_a,
    "ov_border_alpha": border_a,
    "ov_blur": blur_px,
    "ov_text_opacity": 0.0 if cfg["overlay_type"] == "None" else text_op,
    "ov_sheen": 0.0 if cfg["overlay_type"] == "None" else sheen,
    "ov_text_alpha": ov_text_alpha,
    "ov_text_shadow_alpha": ov_text_shadow_alpha,
}

live_css = build_css(live_cfg)
st.markdown(f"<style>{live_css}</style>", unsafe_allow_html=True)

# Ticker render
if cfg["ticker_enabled"]:
    st.markdown(
        f"<div class='ticker'>{cfg['ticker_text']}</div><div class='ticker-spacer'></div>",
        unsafe_allow_html=True
    )

# ============================================================
# Main UI (simple preview + export panel)
# ============================================================
st.title("UI Theme Builder")
st.caption("Palette-based • Overlay presets • Save to generate export blocks")

preview_col, export_col = st.columns([1.05, 0.95], gap="large")

with preview_col:
    st.subheader("Preview (simple)")

    overlay_label = "NONE" if cfg["overlay_type"] == "None" else f"{cfg['overlay_type'].upper()} • {cfg['overlay_level'].upper()}"

    st.markdown(
        f"""
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
            <div>
              <div style="font-size:1.05rem; font-weight:900;">{cfg["palette"].title()} UI</div>
              <div class="muted" style="margin-top:4px;">Auto contrast: {"ON" if cfg["auto_contrast"] else "OFF"} • Font: {cfg["font_key"]}</div>
            </div>
            <span class="badge">{overlay_label}</span>
          </div>

          <div style="height:12px;"></div>

          <div class="row">
            <div>
              <div style="font-weight:900;">Primary action</div>
              <div class="muted" style="font-size:0.9rem;">A clean row for dashboards/logs</div>
            </div>
            <button class="btn">Do it</button>
          </div>

          <div style="height:12px;"></div>

          <div class="overlay-card">
            <div class="overlay-text">UI OVERLAY</div>
            <div style="font-weight:900;">Overlay Panel</div>
            <div class="muted" style="margin-top:4px;">Glassy / Matte / Faded depending on your preset.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.info("Tip: hit **Save + Build Outputs** in the sidebar to generate copy/paste blocks + downloads.")

with export_col:
    st.subheader("Export")
    saved = cfg.get("saved")

    if not saved:
        st.markdown(
            "<div class='card'><div style='font-weight:900;'>Nothing saved yet.</div>"
            "<div class='muted' style='margin-top:6px;'>Press <b>Save + Build Outputs</b> to generate export code.</div></div>",
            unsafe_allow_html=True,
        )
    else:
        tab1, tab2, tab3 = st.tabs(["theme.css", "Streamlit snippet", "theme.json"])

        with tab1:
            st.code(saved["css"], language="css")
            st.download_button("Download theme.css", saved["css"], file_name="theme.css", mime="text/css")

        with tab2:
            st.code(saved["snippet"], language="python")
            st.download_button("Download snippet.py", saved["snippet"], file_name="theme_snippet.py", mime="text/plain")

        with tab3:
            st.code(saved["json"], language="json")
            st.download_button("Download theme.json", saved["json"], file_name="theme.json", mime="application/json")


st.divider()
st.markdown(
    """
**How you reuse it in any other Streamlit app (fast):**
1) Copy the **Streamlit snippet** output into the top of your app  
2) Or inject `theme.css` via `st.markdown("<style>...</style>", unsafe_allow_html=True)`  
3) Keep `theme.json` presets per tool if you want palette consistency
"""
)