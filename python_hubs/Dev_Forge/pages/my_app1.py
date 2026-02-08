# app1_signature.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="App 1 — Signature", layout="wide")

# ============================================================
# APP 1 — SIGNATURE THEME (your CSS block, cleaned + ready)
# ============================================================
THEME_CSS = r""":root {
  --bg: #f3f4f6;
  --surface: #ffffff;
  --surface2: #f8fafc;
  --border: #d1d5db;

  --text: #111827;
  --muted: #6b7280;

  --accent: #2563eb;
  --good: #16a34a;
  --warn: #f59e0b;
  --bad: #ef4444;

  --radius: 26px;
  --pad: 14px;
  --font: 'Comic Sans MS','Chalkboard SE','Comic Neue',cursive,sans-serif;
  --font_weight: 900;

  --shadow: 0 8px 24px rgba(0,0,0,0.12);

  /* overlay */
  --ov_bg: rgba(255,255,255,0.1);
  --ov_border: rgba(120,255,220,0.3);
  --ov_blur: 12px;
  --ov_text_opacity: 0.45;
  --ov_sheen: 0.16;
  --ov_text_color: rgba(255,255,255,0.55);
  --ov_text_shadow: rgba(0,0,0,0.25);

  /* ticker */
  --ticker_bg: rgba(255,255,255,0.08);
  --ticker_border: rgba(120,255,220,0.3);
  --ticker_blur: 10px;
  --ticker_size: 1.06rem;
}

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-weight: var(--font_weight);
}

[data-testid="stAppViewContainer"] { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }

.block-container {
  padding-top: 1.25rem;
  padding-bottom: 2.6rem;
}

/* ====== SIMPLE COMPONENTS ====== */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--pad);
  box-shadow: var(--shadow);
}

.row {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  border: 1px solid var(--border);
  background: var(--surface2);
  border-radius: calc(var(--radius) - 2px);
  padding: 10px 12px;
}

.badge {
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
}

.btn {
  appearance:none;
  border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--border));
  background: linear-gradient(180deg, var(--accent), color-mix(in srgb, var(--accent) 70%, black));
  color: white;
  border-radius: calc(var(--radius) - 2px);
  padding: 10px 12px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: var(--shadow);
}

.muted { color: var(--muted); }

/* ====== OVERLAY CARD ====== */
.overlay-card {
  background: var(--ov_bg);
  border: 1px solid var(--ov_border);
  border-radius: var(--radius);
  padding: 18px;
  backdrop-filter: blur(var(--ov_blur));
  -webkit-backdrop-filter: blur(var(--ov_blur));
  position: relative;
  overflow: hidden;
}

.overlay-card:before {
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
}

.overlay-text {
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
}

/* ====== TICKER ====== */
.ticker {
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
}
.ticker-spacer { height: 64px; }
"""

st.markdown(f"<style>{THEME_CSS}</style>", unsafe_allow_html=True)

# ============================================================
# TICKER (toggle + message)
# ============================================================
with st.sidebar:
    st.title("App 1 — Signature")
    st.caption("Signature UI scaffold using your theme.css block.")
    show_ticker = st.toggle("Show ticker", value=True)
    ticker_text = st.text_input("Ticker text", "NGSS Aligned")

if show_ticker:
    st.markdown(
        f"<div class='ticker'>{ticker_text}</div><div class='ticker-spacer'></div>",
        unsafe_allow_html=True
    )

# ============================================================
# APP 1 SIGNATURE LAYOUT (simple, reusable, clean)
# ============================================================
st.title("Signature App 1")
st.caption("A clean, branded scaffold you can paste into your repo and build on.")

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.subheader("Preview Panel")

    st.markdown(
        """
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
            <div>
              <div style="font-size:1.05rem; font-weight:900;">Teacher Tool — App 1</div>
              <div class="muted" style="margin-top:4px;">Signature layout with card / row / badge / overlay.</div>
            </div>
            <span class="badge">Signature</span>
          </div>

          <div style="height:12px;"></div>

          <div class="row">
            <div>
              <div style="font-weight:900;">Status</div>
              <div class="muted" style="font-size:0.9rem;">Ready for your tool content</div>
            </div>
            <button class="btn">Run</button>
          </div>

          <div style="height:12px;"></div>

          <div class="overlay-card">
            <div class="overlay-text">LAMINATED</div>
            <div style="font-weight:900;">Overlay Zone</div>
            <div class="muted" style="margin-top:4px;">
              Put mission text, mode labels, or “AI usage” banners here.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
          <div style="font-weight:900; margin-bottom:6px;">Notes</div>
          <div class="muted">This file is meant to be your App 1 “signature shell.” Replace the inner HTML blocks with your actual tool UI.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.subheader("Drop-in Blocks (for other apps)")

    st.markdown(
        "<div class='card'><div style='font-weight:900;'>Copy/paste snippets</div>"
        "<div class='muted' style='margin-top:6px;'>Use these in any Streamlit file.</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.code(
        dedent(f"""
        import streamlit as st

        THEME_CSS = r\"\"\"{THEME_CSS}\"\"\"
        st.markdown(f"<style>{{THEME_CSS}}</style>", unsafe_allow_html=True)

        # ticker (optional)
        st.markdown("<div class='ticker'>NGSS Aligned</div><div class='ticker-spacer'></div>", unsafe_allow_html=True)
        """).strip(),
        language="python",
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.code(
        dedent("""
        st.markdown(
          "<div class='overlay-card'>"
          "<div class='overlay-text'>LAMINATED</div>"
          "<div style='font-weight:900;'>Overlay Zone</div>"
          "<div class='muted' style='margin-top:4px;'>Your content</div>"
          "</div>",
          unsafe_allow_html=True
        )
        """).strip(),
        language="python",
    )