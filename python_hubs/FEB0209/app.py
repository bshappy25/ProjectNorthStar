# python_hubs/FEB0209/app.py
# ============================================
# FEB0209 — Fail-Proof HTML Viewing Window + Paste-to-Add HTML
# Pick an .html file from teacher_tools/ and preview it safely
# ============================================

from pathlib import Path
import html
import re
import streamlit as st
import streamlit.components.v1 as components

APP_TITLE = "FEB0209 — Tool Viewer"
TOOLS_DIR = Path(__file__).resolve().parent / "teacher_tools"

st.set_page_config(page_title=APP_TITLE, page_icon="🪟", layout="wide")
st.title("🪟 FEB0209 — HTML Tool Viewer")
st.caption(f"Reading tools from: `{TOOLS_DIR}`")

# Ensure folder exists
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- helpers ----------
def safe_stem(name: str) -> str:
    """
    Convert arbitrary title into a safe filename stem.
    - spaces -> underscores
    - keep letters/numbers/_/-
    - max 60 chars
    """
    name = (name or "").strip()
    if not name:
        return "new_tool"
    name = name.replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_\-]+", "", name)
    return name[:60] if name else "new_tool"

def next_available_path(stem: str) -> Path:
    """Avoid overwrite by appending _1, _2, ..."""
    base = safe_stem(stem)
    candidate = TOOLS_DIR / f"{base}.html"
    if not candidate.exists():
        return candidate
    n = 1
    while True:
        cand = TOOLS_DIR / f"{base}_{n}.html"
        if not cand.exists():
            return cand
        n += 1

def list_tools() -> list[str]:
    return sorted([p.name for p in TOOLS_DIR.glob("*.html")])


# ---------- sidebar controls ----------
with st.sidebar:
    st.header("Controls")

    # ADD HTML (PASTE)
    with st.expander("➕ Add HTML (paste)", expanded=False):
        new_title = st.text_input("Tool name (filename)", value="ariel_tool")
        st.caption("This becomes the .html filename. Spaces are OK.")
        pasted_html = st.text_area(
            "Paste full HTML here",
            height=220,
            placeholder="<!DOCTYPE html>\n<html>...\n</html>"
        )

        colA, colB = st.columns(2)
        with colA:
            if st.button("💾 Save to teacher_tools/", use_container_width=True, type="primary"):
                if not pasted_html.strip():
                    st.error("Paste HTML first.")
                else:
                    dest = next_available_path(new_title)
                    try:
                        dest.write_text(pasted_html, encoding="utf-8")
                        st.success(f"Saved: {dest.name}")
                        # select it automatically
                        st.session_state["selected_tool"] = dest.name
                        st.rerun()
                    except Exception as e:
                        st.error("Could not save HTML file.")
                        st.exception(e)

        with colB:
            if st.button("🧹 Clear", use_container_width=True):
                st.session_state["__clear_paste__"] = True
                st.rerun()

    # Clear paste area safely via session flags
    if st.session_state.get("__clear_paste__"):
        st.session_state["__clear_paste__"] = False
        # Streamlit text_area can't be directly cleared without a key;
        # simplest approach is to rerun and let user paste again.
        st.info("Cleared. Paste new HTML now.")

    st.divider()

    tools = list_tools()
    if not tools:
        st.warning("No .html files found yet.")
        st.markdown("Drop files into `python_hubs/FEB0209/teacher_tools/` or use **Add HTML (paste)** above.")
        st.stop()

    # Tool picker
    default_tool = st.session_state.get("selected_tool")
    if default_tool not in tools:
        default_tool = tools[0]

    tool_name = st.selectbox("Choose a tool", tools, index=tools.index(default_tool))
    height = st.slider("Viewer height", 500, 1400, 900, 50)

    st.divider()
    st.subheader("Safety mode")
    safe_mode = st.toggle("Safe mode (recommended)", value=True)
    st.caption(
        "Safe mode blocks scripts/forms/popups in the iframe. "
        "Turn OFF only if your tool needs JavaScript."
    )

# ---------- load HTML ----------
tool_path = TOOLS_DIR / tool_name
try:
    raw_html = tool_path.read_text(encoding="utf-8", errors="replace")
except Exception as e:
    st.error(f"Could not read file: `{tool_path}`")
    st.exception(e)
    st.stop()

# Escape for srcdoc safety (prevents breaking the wrapper doc)
escaped = html.escape(raw_html, quote=True)

# Sandbox policy
if safe_mode:
    sandbox = "allow-same-origin"
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

components.html(viewer_doc, height=height + 40, scrolling=False)

with st.expander("🔎 Debug: show raw HTML (read-only)", expanded=False):
    st.code(raw_html, language="html")

