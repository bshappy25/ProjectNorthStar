# python_hubs/FEB0209/Birthday_viewer.py
# ============================================================
# 🎂 Birthday Viewer — Glassy HTML Link Card Generator + Viewer
# - Paste HTML (creates .html in teacher_tools/)
# - OR use quick "Birthday Card Builder" (no HTML needed)
# - Preview inside an iframe (safe mode toggle)
# ============================================================

from __future__ import annotations

from pathlib import Path
import html as _html
import re
import streamlit as st
import streamlit.components.v1 as components

APP_TITLE = "🎂 Birthday Viewer"
APP_ICON = "🎂"

APP_DIR = Path(__file__).resolve().parent
TOOLS_DIR = APP_DIR / "teacher_tools"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Page config + glassy polish
# -------------------------------
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

GLASS_CSS = """
<style>
  /* Background */
  .stApp {
    background:
      radial-gradient(circle at 18% 18%, rgba(255,255,255,.96), rgba(255,255,255,0) 56%),
      radial-gradient(circle at 82% 14%, rgba(222,210,255,.72), rgba(255,255,255,0) 60%),
      radial-gradient(circle at 62% 88%, rgba(196,230,255,.55), rgba(255,255,255,0) 62%),
      radial-gradient(circle at 16% 86%, rgba(238,226,255,.58), rgba(255,255,255,0) 60%),
      linear-gradient(135deg, #fbfbff 0%, #f2f4ff 45%, #efe7ff 100%);
  }

  /* Main content width feel */
  .block-container { padding-top: 1.2rem; padding-bottom: 2.2rem; }

  /* Sidebar glass */
  section[data-testid="stSidebar"] {
    background: rgba(255,255,255,.62) !important;
    border-right: 1px solid rgba(92,80,140,.12);
    backdrop-filter: blur(10px);
  }

  /* Cards / expanders feel */
  div[data-testid="stExpander"] > details {
    border-radius: 14px;
    border: 1px solid rgba(92,80,140,.14);
    background: rgba(255,255,255,.66);
    box-shadow: 0 18px 46px rgba(60,40,110,.07);
  }

  /* Inputs */
  .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 12px !important;
  }

  /* Buttons */
  .stButton button {
    border-radius: 999px !important;
    font-weight: 800 !important;
    padding: .6rem 1.0rem !important;
  }
</style>
"""
st.markdown(GLASS_CSS, unsafe_allow_html=True)

st.title("🎂 Birthday Viewer")
st.caption(f"Tools folder: `{TOOLS_DIR}`")

# -------------------------------
# Helpers
# -------------------------------
def safe_stem(name: str) -> str:
    """Sanitize filename stem for safe saving."""
    stem = Path(name).stem.strip().replace(" ", "_")
    stem = re.sub(r"[^A-Za-z0-9_\-]+", "", stem)
    return stem[:60] if stem else "birthday_card"

def next_available_path(directory: Path, base_stem: str, suffix: str = ".html") -> Path:
    p = directory / f"{base_stem}{suffix}"
    if not p.exists():
        return p
    n = 1
    while True:
        cand = directory / f"{base_stem}_{n}{suffix}"
        if not cand.exists():
            return cand
        n += 1

def birthday_link_card_html(
    title: str,
    subtitle: str,
    emoji_text: str,
    link_title: str,
    button_text: str,
    url: str,
    note: str,
) -> str:
    # Minimal, mobile-friendly HTML card (no external deps)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_html.escape(title)}</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}

    :root{{
      --lav-0:#fbfbff; --lav-1:#f2f4ff; --lav-2:#efe7ff;
      --ink: rgba(30,30,40,.78);
      --muted: rgba(40,40,60,.52);
      --stroke: rgba(92,80,140,.12);
      --btnA:#6b5cff; --btnB:#7b3ff2;
    }}

    body{{
      font-family: Georgia, serif;
      min-height:100vh;
      padding:18px;
      background:
        radial-gradient(circle at 18% 18%, rgba(255,255,255,.96), rgba(255,255,255,0) 56%),
        radial-gradient(circle at 82% 14%, rgba(222,210,255,.72), rgba(255,255,255,0) 60%),
        radial-gradient(circle at 62% 88%, rgba(196,230,255,.55), rgba(255,255,255,0) 62%),
        radial-gradient(circle at 16% 86%, rgba(238,226,255,.58), rgba(255,255,255,0) 60%),
        linear-gradient(135deg, var(--lav-0) 0%, var(--lav-1) 45%, var(--lav-2) 100%);
    }}

    .wrap{{
      max-width: 980px;
      margin: 0 auto;
      border-radius: 22px;
      overflow: hidden;
      background: rgba(255,255,255,.72);
      border: 1px solid var(--stroke);
      box-shadow: 0 28px 90px rgba(50,35,90,.16), 0 0 0 1px rgba(255,255,255,.35) inset;
      backdrop-filter: blur(10px);
    }}

    header{{
      text-align:center;
      padding: 30px 18px;
      background:
        radial-gradient(circle at 20% 30%, rgba(255,255,255,.90), rgba(255,255,255,0) 58%),
        radial-gradient(circle at 85% 22%, rgba(210,195,255,.55), rgba(255,255,255,0) 60%),
        linear-gradient(135deg, rgba(246,248,255,.92), rgba(232,225,255,.88), rgba(214,232,255,.84));
      border-bottom: 1px solid rgba(130,110,190,.10);
    }}

    h1{{
      font-size: clamp(22px, 6vw, 44px);
      color: #ffffff;
      text-shadow: 0 2px 10px rgba(88,66,140,.22), 0 16px 46px rgba(120,90,190,.16);
      margin-bottom: 8px;
    }}

    .sub{{
      font-size: clamp(14px, 3.6vw, 18px);
      color: rgba(255,255,255,.92);
      font-style: italic;
    }}

    main{{ padding: 22px 14px 30px; }}

    .hero{{
      position: relative;
      margin: 0 auto;
      width: min(980px, 100%);
      border-radius: 24px;
      padding: 24px 16px;
      background:
        radial-gradient(circle at 20% 25%, rgba(255,255,255,.92), rgba(255,255,255,0) 56%),
        radial-gradient(circle at 85% 20%, rgba(214,201,255,.38), rgba(255,255,255,0) 60%),
        radial-gradient(circle at 60% 90%, rgba(186,225,255,.30), rgba(255,255,255,0) 58%),
        linear-gradient(135deg, rgba(255,255,255,.78), rgba(235,230,255,.60));
      border: 1px solid rgba(120,95,190,.14);
      box-shadow: 0 24px 74px rgba(60,40,110,.14), 0 0 0 1px rgba(255,255,255,.35) inset;
      overflow:hidden;
    }}

    .hero::before{{
      content:"";
      position:absolute;
      inset:-60px;
      background: radial-gradient(circle at 50% 40%,
        rgba(255,255,255,.85) 0%,
        rgba(210,195,255,.34) 40%,
        rgba(180,220,255,.22) 62%,
        rgba(120,90,190,.10) 78%,
        rgba(0,0,0,0) 100%);
      filter: blur(28px);
      opacity:.85;
      animation: glowPulse 3.6s ease-in-out infinite;
      pointer-events:none;
    }}

    .hero::after{{
      content:"";
      position:absolute;
      inset:0;
      pointer-events:none;
      background:
        radial-gradient(circle at 12% 26%, rgba(255,255,255,.85) 0 2px, rgba(255,255,255,0) 4px),
        radial-gradient(circle at 22% 62%, rgba(255,255,255,.75) 0 2px, rgba(255,255,255,0) 4px),
        radial-gradient(circle at 55% 40%, rgba(255,255,255,.80) 0 2px, rgba(255,255,255,0) 4px),
        radial-gradient(circle at 78% 68%, rgba(255,255,255,.78) 0 2px, rgba(255,255,255,0) 4px);
      opacity:.55;
      animation: twinkle 2.6s ease-in-out infinite;
      mix-blend-mode: screen;
    }}

    @keyframes glowPulse{{0%,100%{{opacity:.72;transform:scale(1)}}50%{{opacity:1;transform:scale(1.02)}}}}
    @keyframes twinkle{{0%,100%{{opacity:.40}}50%{{opacity:.72}}}}

    .stack{{
      position:relative;
      z-index:2;
      display:grid;
      gap: 14px;
      justify-items:center;
      padding: 10px 6px;
      text-align:center;
    }}

    .emoji-link{{
      font-size: clamp(42px, 10vw, 68px);
      line-height: 1;
      text-decoration:none;
      filter: drop-shadow(0 12px 24px rgba(0,0,0,.16));
      transition: transform .15s ease;
      -webkit-tap-highlight-color: transparent;
      user-select:none;
    }}
    .emoji-link:hover{{transform:scale(1.03)}}
    .emoji-link:active{{transform:scale(.96)}}

    .link-title{{
      font-size: clamp(18px, 4.6vw, 28px);
      font-weight: 800;
      color: var(--ink);
      text-shadow: 0 1px 0 rgba(255,255,255,.55);
    }}

    .btn{{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      width: min(520px, 92%);
      min-height: 62px;
      padding: 16px 22px;
      border-radius: 999px;
      font-size: clamp(18px, 4.6vw, 22px);
      font-weight: 900;
      letter-spacing: .6px;
      color:#fff;
      text-decoration:none;
      background: linear-gradient(135deg, var(--btnA), var(--btnB));
      box-shadow: 0 16px 38px rgba(107,92,255,.26), 0 0 0 1px rgba(255,255,255,.18) inset;
      transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
      -webkit-tap-highlight-color: transparent;
      user-select:none;
    }}
    .btn:hover{{transform: translateY(-1px); box-shadow: 0 20px 44px rgba(123,63,242,.30); filter:saturate(1.05)}}
    .btn:active{{transform: translateY(1px) scale(.985); box-shadow: 0 12px 30px rgba(107,92,255,.22)}}

    .note{{font-size: 14px; color: var(--muted); font-style: italic;}}

    @media (max-width: 430px){{
      body{{padding:12px}}
      .hero{{padding:22px 14px}}
      .stack{{gap:12px}}
    }}

    @media (prefers-reduced-motion: reduce){{
      .hero::before, .hero::after{{animation:none}}
      .emoji-link, .btn{{transition:none}}
    }}
  </style>
</head>

<body>
  <div class="wrap">
    <header>
      <h1>{_html.escape(title)}</h1>
      <div class="sub">{_html.escape(subtitle)}</div>
    </header>

    <main>
      <div class="hero">
        <div class="stack">
          <a class="emoji-link" href="{_html.escape(url)}" target="_blank" rel="noopener noreferrer"
             aria-label="Open birthday gallery link">{_html.escape(emoji_text)}</a>

          <div class="link-title">{_html.escape(link_title)}</div>

          <a class="btn" href="{_html.escape(url)}" target="_blank" rel="noopener noreferrer">{_html.escape(button_text)} ↗</a>

          <div class="note">{_html.escape(note)}</div>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
"""

# -------------------------------
# Sidebar: Add / Create
# -------------------------------
with st.sidebar:
    st.header("Controls")

    with st.expander("➕ Add HTML (paste)", expanded=False):
        st.caption("Paste a full HTML file. We'll save it into `teacher_tools/` and it will appear in the dropdown.")
        filename = st.text_input("File name (no extension needed)", value="Birthday_Card")
        pasted = st.text_area("Paste HTML here", height=220, placeholder="<!doctype html> ...")
        colA, colB = st.columns([0.6, 0.4])
        with colA:
            save_paste = st.button("Save pasted HTML", type="primary", use_container_width=True)
        with colB:
            clear_paste = st.button("Clear", use_container_width=True)

        if clear_paste:
            st.session_state["__paste_clear__"] = True
            st.rerun()

        if save_paste:
            if not pasted.strip():
                st.error("Paste HTML first.")
            else:
                stem = safe_stem(filename)
                dest = next_available_path(TOOLS_DIR, stem, ".html")
                try:
                    dest.write_text(pasted, encoding="utf-8")
                    st.success(f"Saved: {dest.name}")
                    st.session_state["current_tool"] = dest.name
                    st.rerun()
                except Exception as e:
                    st.error("Could not save file.")
                    st.exception(e)

    with st.expander("🎁 Birthday Card Builder (no HTML)", expanded=True):
        st.caption("Fill these fields and generate a polished link-card HTML automatically.")
        person = st.text_input("Name", value="Ariel")
        date_str = st.text_input("Birthday (MM.DD.YYYY)", value="02.09.1990")
        subtitle = st.text_input("Subtitle line", value="A People's Princess")
        emoji_text = st.text_input("Emoji text link", value="✨👸🏻✨")
        url = st.text_input("Link (Imgur/Drive/etc.)", value="https://imgur.com/a/9IqbQtd")
        link_title = st.text_input("Center title", value="Open Ariel — A People’s Princess")
        button_text = st.text_input("Button text", value="RAW")
        note = st.text_input("Note under button", value="Opens in a new tab")

        gen_name = st.text_input("Output file name", value="Ariel_Principal_LinkCard")

        if st.button("Generate HTML card", type="primary", use_container_width=True):
            title = f"{person}: The People’s Princess. {date_str}"
            html_doc = birthday_link_card_html(
                title=title,
                subtitle=subtitle,
                emoji_text=emoji_text,
                link_title=link_title,
                button_text=button_text,
                url=url,
                note=note,
            )
            stem = safe_stem(gen_name)
            dest = next_available_path(TOOLS_DIR, stem, ".html")
            try:
                dest.write_text(html_doc, encoding="utf-8")
                st.success(f"Generated: {dest.name}")
                st.session_state["current_tool"] = dest.name
                st.rerun()
            except Exception as e:
                st.error("Could not write generated file.")
                st.exception(e)

    st.divider()
    st.subheader("Viewer")
    height = st.slider("Viewer height", 520, 1600, 980, 40)
    safe_mode = st.toggle("Safe mode (recommended)", value=True)
    st.caption("Safe mode locks down scripts/forms/popups in the iframe.")

# -------------------------------
# Main: choose + preview
# -------------------------------
tools = sorted([p.name for p in TOOLS_DIR.glob("*.html")])

if not tools:
    st.warning("No .html files found yet.")
    st.markdown("**Fix:** add files into `python_hubs/FEB0209/teacher_tools/` or use the builder in the sidebar.")
    st.stop()

default_idx = 0
current = st.session_state.get("current_tool")
if current in tools:
    default_idx = tools.index(current)

tool_name = st.selectbox("Choose a card/tool", tools, index=default_idx)

tool_path = TOOLS_DIR / tool_name
try:
    raw_html = tool_path.read_text(encoding="utf-8", errors="replace")
except Exception as e:
    st.error(f"Could not read file: `{tool_path}`")
    st.exception(e)
    st.stop()

escaped = _html.escape(raw_html, quote=True)

if safe_mode:
    sandbox = "allow-same-origin"
else:
    sandbox = "allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin"

viewer_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  html, body {{
    margin:0; padding:0; height:100%;
    background: transparent;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }}
  .frame {{
    width:100%;
    height:100vh;
    max-height:{height}px;
    border: 1px solid rgba(92,80,140,0.18);
    border-radius: 18px;
    overflow:hidden;
    background: rgba(255,255,255,0.58);
    box-shadow: 0 26px 70px rgba(60,40,110,0.12);
    backdrop-filter: blur(10px);
  }}
  iframe {{
    width:100%;
    height:100%;
    border:0;
    background: white;
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
