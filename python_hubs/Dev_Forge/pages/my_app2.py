# theme_studio_app2.py
import streamlit as st
from textwrap import dedent
import json

st.set_page_config(page_title="Theme Studio (App 2) — Glass + Ticker", layout="wide")

# ============================================================
# CSS GENERATOR
# ============================================================
def build_css(v: dict) -> str:
    return dedent(f"""
    /* ==========================================================
       THEME STUDIO (APP 2) — CSS SELECTOR + GLASS OVERLAY + TICKER
       Copy/paste safe • One-file • Streamlit-ready
       ========================================================== */

    :root {{
      --bg: {v["bg"]};
      --surface: {v["surface"]};
      --surface2: {v["surface2"]};
      --border: {v["border"]};

      --text: {v["text"]};
      --muted: {v["muted"]};

      --accent: {v["accent"]};
      --accent2: {v["accent2"]};
      --good: {v["good"]};
      --warn: {v["warn"]};
      --bad: {v["bad"]};

      --radius: {v["radius"]}px;
      --pad: {v["pad"]}px;

      --shadow: 0 {v["shadow_y"]}px {v["shadow_blur"]}px rgba(0,0,0,{v["shadow_alpha"]});
      --font: {v["font_family"]};

      /* --- glass layer controls --- */
      --glass_bg: rgba(255,255,255,{v["glass_alpha"]});
      --glass_border: rgba(120,255,220,{v["glass_border_alpha"]});
      --glass_blur: {v["glass_blur"]}px;
      --glass_text: rgba(255,255,255,{v["overlay_text_alpha"]});
      --glass_text_shadow: rgba(0,0,0,{v["overlay_shadow_alpha"]});

      /* --- ticker controls --- */
      --ticker_bg: rgba(255,255,255,{v["ticker_alpha"]});
      --ticker_border: rgba(120,255,220,{v["ticker_border_alpha"]});
      --ticker_blur: {v["ticker_blur"]}px;
      --ticker_size: {v["ticker_size"]}rem;
      --ticker_pad_y: {v["ticker_pad_y"]}px;
      --ticker_pad_x: {v["ticker_pad_x"]}px;
    }}

    html, body {{
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
    }}

    /* --- Streamlit frame polish --- */
    .block-container {{
      padding-top: 1.35rem;
      padding-bottom: 2.6rem;
    }}

    /* Prevent Streamlit default backgrounds from fighting your theme */
    [data-testid="stAppViewContainer"] {{
      background: var(--bg);
    }}
    [data-testid="stHeader"] {{
      background: transparent;
    }}

    /* ---------- base primitives ---------- */
    .ts-wrap {{ background: transparent; color: var(--text); font-family: var(--font); }}

    .ts-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: var(--pad);
    }}

    .ts-card--alt {{
      background: var(--surface2);
    }}

    .ts-title {{
      font-weight: 900;
      letter-spacing: 0.02em;
      margin: 0 0 8px 0;
    }}

    .ts-muted {{
      color: var(--muted);
    }}

    .ts-row {{
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      border-radius: calc(var(--radius) - 2px);
      border: 1px solid var(--border);
      background: var(--surface2);
    }}

    .ts-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: var(--surface);
      font-weight: 900;
      font-size: 0.85rem;
      white-space: nowrap;
    }}

    .ts-pill--accent {{
      border-color: color-mix(in srgb, var(--accent) 35%, var(--border));
      background: color-mix(in srgb, var(--accent) 12%, var(--surface));
    }}

    .ts-pill--good {{
      border-color: color-mix(in srgb, var(--good) 35%, var(--border));
      background: color-mix(in srgb, var(--good) 12%, var(--surface));
    }}

    .ts-pill--warn {{
      border-color: color-mix(in srgb, var(--warn) 35%, var(--border));
      background: color-mix(in srgb, var(--warn) 12%, var(--surface));
    }}

    .ts-pill--bad {{
      border-color: color-mix(in srgb, var(--bad) 35%, var(--border));
      background: color-mix(in srgb, var(--bad) 12%, var(--surface));
    }}

    .ts-btn {{
      appearance: none;
      border: 1px solid color-mix(in srgb, var(--accent) 45%, var(--border));
      background: linear-gradient(180deg,
        color-mix(in srgb, var(--accent) 18%, var(--surface)),
        color-mix(in srgb, var(--accent) 10%, var(--surface))
      );
      color: var(--text);
      border-radius: calc(var(--radius) - 2px);
      padding: 10px 12px;
      font-weight: 900;
      cursor: pointer;
      box-shadow: var(--shadow);
      transition: transform 120ms ease, filter 120ms ease;
    }}

    .ts-btn:hover {{
      transform: translateY(-1px);
      filter: brightness(1.03);
    }}

    .ts-btn--solid {{
      border-color: color-mix(in srgb, var(--accent) 70%, var(--border));
      background: linear-gradient(180deg, var(--accent), color-mix(in srgb, var(--accent) 70%, black));
      color: #ffffff;
    }}

    .ts-btn--ghost {{
      background: transparent;
      box-shadow: none;
    }}

    .ts-input {{
      width: 100%;
      padding: 10px 12px;
      border-radius: calc(var(--radius) - 2px);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      outline: none;
    }}

    .ts-input:focus {{
      border-color: color-mix(in srgb, var(--accent) 65%, var(--border));
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 18%, transparent);
    }}

    .ts-alert {{
      border-radius: var(--radius);
      border: 1px solid var(--border);
      padding: 12px;
      background: var(--surface);
    }}

    .ts-alert--good {{
      border-color: color-mix(in srgb, var(--good) 40%, var(--border));
      background: color-mix(in srgb, var(--good) 10%, var(--surface));
    }}

    .ts-alert--warn {{
      border-color: color-mix(in srgb, var(--warn) 40%, var(--border));
      background: color-mix(in srgb, var(--warn) 10%, var(--surface));
    }}

    .ts-alert--bad {{
      border-color: color-mix(in srgb, var(--bad) 40%, var(--border));
      background: color-mix(in srgb, var(--bad) 10%, var(--surface));
    }}

    /* ==========================================================
       GLASS OVERLAY (glassy / faded / laminated)
       ========================================================== */
    .glassy-card {{
      background: var(--glass_bg);
      border: 1px solid var(--glass_border);
      border-radius: var(--radius);
      padding: 20px;
      backdrop-filter: blur(var(--glass_blur));
      -webkit-backdrop-filter: blur(var(--glass_blur));
      position: relative;
      overflow: hidden;
    }}

    /* laminated sheen */
    .glassy-card:before {{
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(
        135deg,
        rgba(255,255,255,0.20) 0%,
        rgba(255,255,255,0.07) 35%,
        rgba(255,255,255,0.00) 62%
      );
      pointer-events: none;
      mix-blend-mode: screen;
    }}

    /* text overlay */
    .glassy-overlay-text {{
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 18px;
      color: var(--glass_text);
      font-weight: 900;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      text-shadow: 0 2px 10px var(--glass_text_shadow);
      pointer-events: none;
      opacity: {v["overlay_opacity"]};
    }}

    /* ==========================================================
       TICKER (fixed bottom)
       ========================================================== */
    .ticker {{
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background-color: var(--ticker_bg);
      border-top: 1px solid var(--ticker_border);
      padding: var(--ticker_pad_y) var(--ticker_pad_x);
      text-align: center;
      font-size: var(--ticker_size);
      font-weight: 900;
      letter-spacing: 0.06em;
      backdrop-filter: blur(var(--ticker_blur));
      -webkit-backdrop-filter: blur(var(--ticker_blur));
      z-index: 9999;
    }}

    .ticker-spacer {{
      height: 64px;
    }}
    """).strip()


def ensure_defaults():
    if "theme" in st.session_state:
        return

    st.session_state.theme = {
        # Theme
        "bg": "#f3f4f6",
        "surface": "#ffffff",
        "surface2": "#f8fafc",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "accent2": "#22c55e",
        "good": "#16a34a",
        "warn": "#f59e0b",
        "bad": "#ef4444",
        "radius": 18,
        "pad": 14,
        "shadow_y": 8,
        "shadow_blur": 24,
        "shadow_alpha": 0.12,
        "font_family": "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",

        # Glass overlay
        "glass_alpha": 0.10,
        "glass_border_alpha": 0.30,
        "glass_blur": 10,
        "overlay_opacity": 0.55,
        "overlay_text_alpha": 0.75,
        "overlay_shadow_alpha": 0.35,

        # Ticker
        "ticker_enabled": True,
        "ticker_text": "YOUR MESSAGE • We are L.E.A.D. 🌟",
        "ticker_alpha": 0.08,
        "ticker_border_alpha": 0.30,
        "ticker_blur": 10,
        "ticker_size": 0.85,
        "ticker_pad_y": 8,
        "ticker_pad_x": 20,
    }


# ============================================================
# APP START
# ============================================================
ensure_defaults()
t = st.session_state.theme

# -----------------------------
# SIDEBAR: selector controls
# -----------------------------
with st.sidebar:
    st.title("🎛️ Theme Studio (App 2)")
    st.caption("Glassy overlay + ticker adjuster. Export code blocks for other apps.")

    st.subheader("Core Surfaces")
    t["bg"] = st.color_picker("Background", t["bg"])
    t["surface"] = st.color_picker("Surface", t["surface"])
    t["surface2"] = st.color_picker("Surface (Alt)", t["surface2"])
    t["border"] = st.color_picker("Border", t["border"])

    st.subheader("Text")
    t["text"] = st.color_picker("Text", t["text"])
    t["muted"] = st.color_picker("Muted", t["muted"])

    st.subheader("Semantic Colors")
    t["accent"] = st.color_picker("Accent", t["accent"])
    t["accent2"] = st.color_picker("Accent 2", t["accent2"])
    t["good"] = st.color_picker("Good", t["good"])
    t["warn"] = st.color_picker("Warn", t["warn"])
    t["bad"] = st.color_picker("Bad", t["bad"])

    st.subheader("Shape & Depth")
    t["radius"] = st.slider("Radius", 0, 32, int(t["radius"]))
    t["pad"] = st.slider("Padding", 8, 24, int(t["pad"]))
    t["shadow_y"] = st.slider("Shadow Y", 0, 20, int(t["shadow_y"]))
    t["shadow_blur"] = st.slider("Shadow Blur", 0, 50, int(t["shadow_blur"]))
    t["shadow_alpha"] = st.slider("Shadow Alpha", 0.00, 0.40, float(t["shadow_alpha"]), 0.01)

    st.subheader("Font")
    preset = st.selectbox("Font preset", ["System", "Inter-like", "Serif", "Mono", "Comic-ish"], index=0)
    if preset == "System":
        t["font_family"] = "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif"
    elif preset == "Inter-like":
        t["font_family"] = "Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif"
    elif preset == "Serif":
        t["font_family"] = "ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif"
    elif preset == "Mono":
        t["font_family"] = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
    else:
        t["font_family"] = "'Comic Sans MS','Chalkboard SE','Comic Neue',cursive,sans-serif"

    st.divider()
    st.subheader("🧊 Glass Overlay (laminated)")
    t["glass_alpha"] = st.slider("Glass background alpha", 0.00, 0.30, float(t["glass_alpha"]), 0.01)
    t["glass_border_alpha"] = st.slider("Glass border alpha", 0.00, 0.80, float(t["glass_border_alpha"]), 0.01)
    t["glass_blur"] = st.slider("Glass blur (px)", 0, 30, int(t["glass_blur"]))
    t["overlay_opacity"] = st.slider("Overlay text opacity", 0.00, 1.00, float(t["overlay_opacity"]), 0.01)
    t["overlay_text_alpha"] = st.slider("Overlay text alpha", 0.00, 1.00, float(t["overlay_text_alpha"]), 0.01)
    t["overlay_shadow_alpha"] = st.slider("Overlay shadow alpha", 0.00, 1.00, float(t["overlay_shadow_alpha"]), 0.01)

    st.divider()
    st.subheader("📣 Ticker Adjuster")
    t["ticker_enabled"] = st.toggle("Enable ticker", value=bool(t["ticker_enabled"]))
    t["ticker_text"] = st.text_input("Ticker text", t["ticker_text"])
    t["ticker_alpha"] = st.slider("Ticker background alpha", 0.00, 0.30, float(t["ticker_alpha"]), 0.01)
    t["ticker_border_alpha"] = st.slider("Ticker border alpha", 0.00, 0.80, float(t["ticker_border_alpha"]), 0.01)
    t["ticker_blur"] = st.slider("Ticker blur (px)", 0, 30, int(t["ticker_blur"]))
    t["ticker_size"] = st.slider("Ticker font size (rem)", 0.70, 1.20, float(t["ticker_size"]), 0.01)
    t["ticker_pad_y"] = st.slider("Ticker padding Y (px)", 4, 16, int(t["ticker_pad_y"]))
    t["ticker_pad_x"] = st.slider("Ticker padding X (px)", 8, 40, int(t["ticker_pad_x"]))

    st.divider()
    if st.button("Reset to defaults"):
        st.session_state.pop("theme", None)
        st.rerun()


# -----------------------------
# Apply theme CSS live
# -----------------------------
css_text = build_css(t)
st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)

# Ticker render (if enabled)
if t["ticker_enabled"]:
    st.markdown(
        f"<div class='ticker'>{t['ticker_text']}</div><div class='ticker-spacer'></div>",
        unsafe_allow_html=True
    )

# -----------------------------
# Main layout
# -----------------------------
st.title("Theme Studio — App 2")
st.caption("Glassy laminated overlay + ticker adjuster + reusable export blocks.")

left, right = st.columns([1.15, 0.85], gap="large")

# -----------------------------
# Preview column
# -----------------------------
with left:
    st.subheader("Live Preview")

    st.markdown(
        f"""
        <div class="ts-wrap">

          <div class="ts-card">
            <div class="ts-title">Base Card</div>
            <div class="ts-muted">Standard surface + border + shadow.</div>

            <div style="height:10px"></div>

            <div class="ts-row">
              <div>
                <div style="font-weight:900">Row Item</div>
                <div class="ts-muted" style="font-size:0.9rem">Secondary line</div>
              </div>
              <div class="ts-pill ts-pill--accent">⭐ Accent</div>
            </div>

            <div style="height:10px"></div>

            <div style="display:flex; gap:10px; flex-wrap:wrap">
              <button class="ts-btn">Button</button>
              <button class="ts-btn ts-btn--solid">Primary</button>
              <button class="ts-btn ts-btn--ghost">Ghost</button>
              <span class="ts-pill ts-pill--good">✅ Good</span>
              <span class="ts-pill ts-pill--warn">⚠️ Warn</span>
              <span class="ts-pill ts-pill--bad">⛔ Bad</span>
            </div>

            <div style="height:12px"></div>

            <input class="ts-input" placeholder="Input focus ring preview" />

            <div style="height:12px"></div>

            <div class="ts-alert ts-alert--good"><b>Success:</b> Positive alert panel.</div>
            <div style="height:10px"></div>
            <div class="ts-alert ts-alert--warn"><b>Warning:</b> Caution alert panel.</div>
            <div style="height:10px"></div>
            <div class="ts-alert ts-alert--bad"><b>Error:</b> Error alert panel.</div>
          </div>

          <div style="height:14px"></div>

          <div class="ts-card ts-card--alt">
            <div class="ts-title">Glassy / Laminated Demo</div>
            <div class="ts-muted">This is your laminated glass overlay with centered text.</div>
            <div style="height:10px"></div>

            <div class="glassy-card">
              <div class="glassy-overlay-text">GLASSY • FADED • LAMINATED</div>
              <h3 style="margin:0 0 6px 0;">Your Title</h3>
              <p style="margin:0;" class="ts-muted">
                Your content here. Overlay text sits above without blocking clicks.
              </p>
            </div>

            <div style="height:12px"></div>

            <div class="ts-row">
              <div style="font-weight:900">Ticker Status</div>
              <div class="ts-pill ts-pill--good">{"ON" if t["ticker_enabled"] else "OFF"}</div>
            </div>
          </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Export column
# -----------------------------
with right:
    st.subheader("Export Blocks")

    tab1, tab2, tab3 = st.tabs(["theme.css", "Streamlit snippet", "theme.json"])

    with tab1:
        st.caption("Reusable CSS you can inject into other apps.")
        st.code(css_text, language="css")
        st.download_button("Download theme.css", data=css_text, file_name="theme.css", mime="text/css")

    with tab2:
        st.caption("Paste this into any other Streamlit app (top of file).")
        snippet = dedent(f"""
        import streamlit as st

        THEME_CSS = r\"\"\"{css_text}\"\"\"
        st.markdown(f"<style>{{THEME_CSS}}</style>", unsafe_allow_html=True)

        # Ticker (optional)
        if {bool(t["ticker_enabled"])}:
            st.markdown(
                \"\"\"<div class='ticker'>{t["ticker_text"]}</div><div class='ticker-spacer'></div>\"\"\",
                unsafe_allow_html=True
            )
        """).strip()
        st.code(snippet, language="python")
        st.download_button("Download streamlit_snippet.py", data=snippet, file_name="streamlit_snippet.py", mime="text/plain")

    with tab3:
        st.caption("Theme preset data (store and load per app).")
        st.code(json.dumps(t, indent=2), language="json")
        st.download_button("Download theme.json", data=json.dumps(t, indent=2), file_name="theme.json", mime="application/json")


st.divider()
st.markdown(
    """
**Use your glass overlay anywhere**
```python
st.markdown(
  "<div class='glassy-card'><div class='glassy-overlay-text'>TEXT</div><h3>Title</h3><p>Content</p></div>",
  unsafe_allow_html=True
)