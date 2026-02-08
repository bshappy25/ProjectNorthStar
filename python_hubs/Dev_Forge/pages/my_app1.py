# signature_overlay_spine.py
# BASIC SPINE: Signature Overlay Layer (Streamlit)
# Purpose: Drop this "overlay layer" at the top of ANY Streamlit/HTML-heavy app.
# Next step: we’ll add your CSS theme block + palette/overlay presets.

import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Signature Overlay Spine", layout="wide")

# ============================================================
# 0) SETTINGS (edit these per app)
# ============================================================
APP_TITLE = "Teacher Tool"
SUBTITLE = "Signature Overlay Layer"
DEFAULT_TICKER = "NGSS Aligned"
DEFAULT_OVERLAY_TEXT = "SIGNATURE"
DEFAULT_MODE = "NORMAL"  # e.g., NORMAL / SCIENCE / SAFE / RAPID

# ============================================================
# 1) VERY BASIC BASE CSS (minimal, safe)
#    (We’ll replace/expand this with your full CSS in the next step.)
# ============================================================
BASE_CSS = """
.sig-wrap{position:relative;}
.sig-topbar{
  position:sticky; top:0; z-index:1000;
  display:flex; gap:12px; align-items:center; justify-content:space-between;
  padding:10px 12px; border-radius:14px;
  border:1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
}
.sig-left{display:flex; flex-direction:column; gap:2px;}
.sig-title{font-weight:900; letter-spacing:0.02em;}
.sig-sub{opacity:0.7; font-size:0.9rem;}
.sig-pill{
  display:inline-flex; align-items:center; gap:8px;
  padding:6px 10px; border-radius:999px;
  border:1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.70);
  font-weight:800; font-size:0.85rem; white-space:nowrap;
}
.sig-overlay-card{
  position:relative; overflow:hidden;
  margin-top:12px;
  border-radius:18px;
  border:1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.70);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  padding:18px;
}
.sig-overlay-text{
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  text-align:center;
  padding:18px;
  font-weight:900;
  letter-spacing:0.18em;
  text-transform:uppercase;
  opacity:0.18;
  pointer-events:none;
}
.sig-ticker{
  position:fixed; left:0; right:0; bottom:0; z-index:9999;
  padding:8px 20px; text-align:center;
  font-weight:900; letter-spacing:0.06em;
  border-top:1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.78);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
}
.sig-ticker-spacer{height:64px;}
"""

st.markdown(f"<style>{BASE_CSS}</style>", unsafe_allow_html=True)

# ============================================================
# 2) OVERLAY CONTROLS (simple, optional)
# ============================================================
with st.sidebar:
    st.title("Signature Overlay")
    st.caption("This is the basic spine. Next step: replace BASE_CSS with your theme.")
    show_topbar = st.toggle("Show top bar", value=True)
    show_overlay_card = st.toggle("Show overlay card", value=True)
    show_ticker = st.toggle("Show ticker", value=True)

    mode = st.text_input("Mode label", DEFAULT_MODE)
    overlay_text = st.text_input("Overlay text", DEFAULT_OVERLAY_TEXT)
    ticker_text = st.text_input("Ticker text", DEFAULT_TICKER)

# ============================================================
# 3) OVERLAY LAYER (drop-in)
#    Put this block at the TOP of your app, before your tool UI.
# ============================================================
st.markdown("<div class='sig-wrap'>", unsafe_allow_html=True)

if show_topbar:
    st.markdown(
        dedent(f"""
        <div class="sig-topbar">
          <div class="sig-left">
            <div class="sig-title">{APP_TITLE}</div>
            <div class="sig-sub">{SUBTITLE}</div>
          </div>
          <div style="display:flex; gap:10px; align-items:center;">
            <span class="sig-pill">MODE: {mode}</span>
            <span class="sig-pill">SIGN</span>
          </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

if show_overlay_card:
    st.markdown(
        dedent(f"""
        <div class="sig-overlay-card">
          <div class="sig-overlay-text">{overlay_text}</div>
          <div style="font-weight:900; margin-bottom:6px;">Overlay Zone</div>
          <div style="opacity:0.75;">
            Put any one-liner here: classroom rule, AI usage, safety, NGSS, PBIS, etc.
          </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 4) YOUR HTML APP AREA (placeholder)
#    Replace this section with your actual HTML app.
# ============================================================
st.markdown("### Your App Content (placeholder)")
st.caption("Drop your existing HTML-heavy app below this line.")

demo_left, demo_right = st.columns([1, 1], gap="large")
with demo_left:
    st.text_area("Example log / text input", "Left side content...\n\n(Replace with your actual app)", height=260)

with demo_right:
    st.markdown(
        """
        <div style="border-radius:18px; border:1px dashed rgba(0,0,0,0.25); padding:16px; background: rgba(255,255,255,0.5);">
          <div style="font-weight:900; margin-bottom:6px;">Right-side preview</div>
          <div style="opacity:0.75;">This is where your HTML preview/output would go.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 5) TICKER (fixed bottom)
# ============================================================
if show_ticker:
    st.markdown(
        f"<div class='sig-ticker'>{ticker_text}</div><div class='sig-ticker-spacer'></div>",
        unsafe_allow_html=True
    )