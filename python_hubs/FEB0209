# python_hubs/FEB0209/app.py
# ============================================
# FEB0209 — Fail-Proof HTML Viewing Window
# Pick an .html file from teacher_tools/ and preview it safely
# ============================================

from pathlib import Path
import html
import streamlit as st
import streamlit.components.v1 as components

APP_TITLE = "FEB0209 — Tool Viewer"
TOOLS_DIR = Path(__file__).resolve().parent / "teacher_tools"

st.set_page_config(page_title=APP_TITLE, page_icon="🪟", layout="wide")
st.title("🪟 FEB0209 — HTML Tool Viewer")
st.caption(f"Reading tools from: `{TOOLS_DIR}`")

# Ensure folder exists
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# List tools
tools = sorted([p.name for p in TOOLS_DIR.glob("*.html")])

if not tools:
    st.warning("No .html files found yet.")
    st.markdown("**Fix:** drop files into `python_hubs/FEB0209/teacher_tools/` and refresh.")
    st.stop()

# Controls
with st.sidebar:
    st.header("Controls")
    tool_name = st.selectbox("Choose a tool", tools, index=0)
    height = st.slider("Viewer height", 500, 1400, 900, 50)

    st.divider()
    st.subheader("Safety mode")
    safe_mode = st.toggle("Safe mode (recommended)", value=True)
    st.caption(
        "Safe mode blocks scripts/forms/popups in the iframe. "
        "Turn OFF only if your tool needs JavaScript."
    )

# Load HTML bytes (fail-proof)
tool_path = TOOLS_DIR / tool_name
try:
    raw_html = tool_path.read_text(encoding="utf-8", errors="replace")
except Exception as e:
    st.error(f"Could not read file: `{tool_path}`")
    st.exception(e)
    st.stop()

# Always escape for srcdoc safety
escaped = html.escape(raw_html, quote=True)

# Sandbox policy
# Safe mode: no scripts/forms/popups
# Unsafe mode: allow scripts/forms/popups/modals/downloads (still isolated in iframe)
if safe_mode:
    sandbox = "allow-same-origin"  # keep it very locked down
else:
    sandbox = "allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin"

# Build a tight viewer document
viewer_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  html, body {{
    margin:0; padding:0; height:100%;
    background:#f3f4f6; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }}
  .frame {{
    width:100%;
    height:100vh;
    max-height:{height}px;
    border: 2px solid #d1d5db;
    border-radius: 16px;
    overflow:hidden;
    background:#fff;
    box-shadow: 0 12px 28px rgba(0,0,0,0.10);
  }}
  iframe {{
    width:100%;
    height:100%;
    border:0;
    background:#fff;
  }}
</style>
</head>
<body>
  <div class="frame">
    <iframe sandbox="{sandbox}" srcdoc="{escaped}"></iframe>
  </div>
</body>
</html>
"""

# Render
components.html(viewer_doc, height=height + 40, scrolling=False)

# Optional raw preview (debug)
with st.expander("🔎 Debug: show raw HTML (read-only)", expanded=False):
    st.code(raw_html, language="html")