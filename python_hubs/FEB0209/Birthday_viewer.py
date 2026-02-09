# python_hubs/Dev_Forge/pages/Birthday_viewer.py
# ============================================================
# 🎂 Birthday Viewer — Fail-Proof HTML Viewer + Paste Uploader
# - Any user can add HTML (paste)
# - Admin (Palm ID) can delete HTML tools
# - Palette-based "CSS editor" that generates a polished birthday HTML
# - Abort/Reset button to clear draft + restore locked view
#
# NOTE:
# This app focuses on RELIABLE viewing inside Streamlit iframe.
# External images can fail due to iframe/CORS; this uses a link-first hero.
# ============================================================

from __future__ import annotations

from pathlib import Path
import html as _html
import re
import streamlit as st
import streamlit.components.v1 as components


# -----------------------------
# CONFIG
# -----------------------------
APP_TITLE = "🎂 Birthday Viewer"
PAGE_ICON = "🎂"
ADMIN_CODE = "Bshapp"  # your Palm ID code

# Store birthday HTMLs here
# (This keeps the page self-contained inside DevForge/pages)
TOOLS_DIR = Path(__file__).resolve().parent / "teacher_tools" / "birthdays"
TOOLS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")


# -----------------------------
# HELPERS
# -----------------------------
def safe_stem(name: str) -> str:
    """Filename stem sanitizer for .html"""
    stem = Path(name).stem.strip()
    stem = stem.replace(" ", "_")
    stem = re.sub(r"[^A-Za-z0-9_\-]+", "", stem)
    return stem[:60] if stem else "birthday_card"


def unique_path(base_stem: str) -> Path:
    """Avoid overwrite by appending _1, _2..."""
    p = TOOLS_DIR / f"{base_stem}.html"
    if not p.exists():
        return p
    n = 1
    while True:
        cand = TOOLS_DIR / f"{base_stem}_{n}.html"
        if not cand.exists():
            return cand
        n += 1


def list_html_tools() -> list[str]:
    return sorted([p.name for p in TOOLS_DIR.glob("*.html")])


def load_html(filename: str) -> str:
    p = TOOLS_DIR / filename
    return p.read_text(encoding="utf-8", errors="replace")


def save_html(filename_hint: str, content: str) -> Path:
    stem = safe_stem(filename_hint)
    dest = unique_path(stem)
    dest.write_text(content, encoding="utf-8")
    return dest


def delete_html(filename: str) -> bool:
    p = TOOLS_DIR / filename
    if p.exists():
        p.unlink()
        return True
    return False


def reset_all():
    for k in [
        "selected_tool",
        "viewer_height",
        "safe_mode",
        "draft_mode",
        "draft_title",
        "draft_subtitle",
        "draft_date",
        "draft_link",
        "draft_emoji",
        "draft_button_text",
        "draft_note",
        "draft_filename",
        "palette_key",
        "draft_html_custom",
        "confirm_delete",
        "palm_taps",
        "show_admin_box",
        "admin_unlocked",
    ]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()


# -----------------------------
# SESSION STATE DEFAULTS
# -----------------------------
defaults = {
    "selected_tool": None,
    "viewer_height": 900,
    "safe_mode": True,
    "draft_mode": "Template",
    "draft_title": "Ariel: The People’s Princess. 02.09.1990",
    "draft_subtitle": "A People’s Princess",
    "draft_date": "02.09.1990",
    "draft_link": "https://imgur.com/a/9IqbQtd",
    "draft_emoji": "✨👸🏻✨",
    "draft_button_text": "RAW ↗",
    "draft_note": "Opens Imgur in a new tab",
    "draft_filename": "Birthday_Card.html",
    "palette_key": "Frosty Lavender (White/Purple)",
    "draft_html_custom": "",
    "confirm_delete": False,
    "palm_taps": 0,
    "show_admin_box": False,
    "admin_unlocked": False,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)


# -----------------------------
# PALETTES (template generator)
# -----------------------------
PALETTES = {
    "Frosty Lavender (White/Purple)": {
        "page_bg": "radial-gradient(circle at 20% 20%, rgba(255,255,255,0.95), rgba(255,255,255,0) 55%),"
                   "radial-gradient(circle at 80% 10%, rgba(225,214,255,0.55), rgba(255,255,255,0) 60%),"
                   "radial-gradient(circle at 60% 90%, rgba(186,225,255,0.45), rgba(255,255,255,0) 55%),"
                   "linear-gradient(135deg, #f7f8ff 0%, #eef2ff 40%, #f3f4ff 100%)",
        "container_bg": "rgba(255,255,255,0.70)",
        "header_bg": "linear-gradient(135deg, rgba(245,247,255,0.95) 0%, rgba(232,225,255,0.92) 55%, rgba(214,232,255,0.88) 100%)",
        "hero_bg": "radial-gradient(circle at 20% 25%, rgba(255,255,255,0.92), rgba(255,255,255,0) 55%),"
                   "radial-gradient(circle at 85% 20%, rgba(214,201,255,0.35), rgba(255,255,255,0) 60%),"
                   "radial-gradient(circle at 60% 90%, rgba(186,225,255,0.30), rgba(255,255,255,0) 58%),"
                   "linear-gradient(135deg, rgba(255,255,255,0.70), rgba(235,230,255,0.55))",
        "button_bg": "linear-gradient(135deg, #6b5cff, #7b3ff2)",
        "text_dark": "rgba(40, 40, 60, 0.74)",
        "note": "rgba(40, 40, 60, 0.50)",
        "shadow": "0 20px 70px rgba(60, 40, 110, 0.14)",
    },
    "Icy Blue (White/Blue)": {
        "page_bg": "radial-gradient(circle at 25% 20%, rgba(255,255,255,0.95), rgba(255,255,255,0) 55%),"
                   "radial-gradient(circle at 80% 15%, rgba(180,220,255,0.60), rgba(255,255,255,0) 60%),"
                   "linear-gradient(135deg, #f8fbff 0%, #edf6ff 45%, #f4f8ff 100%)",
        "container_bg": "rgba(255,255,255,0.72)",
        "header_bg": "linear-gradient(135deg, rgba(245,252,255,0.98), rgba(220,240,255,0.90))",
        "hero_bg": "radial-gradient(circle at 20% 25%, rgba(255,255,255,0.92), rgba(255,255,255,0) 55%),"
                   "radial-gradient(circle at 80% 20%, rgba(160,210,255,0.32), rgba(255,255,255,0) 60%),"
                   "linear-gradient(135deg, rgba(255,255,255,0.70), rgba(220,245,255,0.45))",
        "button_bg": "linear-gradient(135deg, #4f8cff, #3b5bdb)",
        "text_dark": "rgba(20, 25, 35, 0.74)",
        "note": "rgba(20, 25, 35, 0.50)",
        "shadow": "0 20px 70px rgba(20, 60, 120, 0.14)",
    },
    "Rose Gold (Warm)": {
        "page_bg": "linear-gradient(135deg, #fff7f3 0%, #ffe9e1 50%, #fff8fb 100%)",
        "container_bg": "rgba(255,255,255,0.78)",
        "header_bg": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
        "hero_bg": "linear-gradient(135deg, rgba(246,211,101,0.25), rgba(253,160,133,0.18))",
        "button_bg": "linear-gradient(135deg, #667eea, #764ba2)",
        "text_dark": "rgba(40, 30, 30, 0.72)",
        "note": "rgba(40, 30, 30, 0.50)",
        "shadow": "0 20px 70px rgba(120, 70, 70, 0.14)",
    },
}


def render_birthday_template(
    *,
    title: str,
    subtitle: str,
    link: str,
    emoji: str,
    button_text: str,
    note: str,
    palette_key: str,
) -> str:
    pal = PALETTES.get(palette_key, PALETTES["Frosty Lavender (White/Purple)"])

    # Link-first hero: reliable inside Streamlit iframe
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_html.escape(title)}</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{
      font-family: Georgia, serif;
      min-height:100vh;
      padding:16px;
      background:{pal["page_bg"]};
    }}
    .container{{
      max-width:1100px;
      margin:0 auto;
      border-radius:22px;
      overflow:hidden;
      background:{pal["container_bg"]};
      box-shadow: 0 18px 60px rgba(0,0,0,0.18);
      border:1px solid rgba(90,80,130,0.10);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }}
    .header{{
      padding:28px 18px;
      text-align:center;
      background:{pal["header_bg"]};
      position:relative;
      overflow:hidden;
    }}
    .header::before{{
      content:'👑';
      position:absolute;
      top:-18px; right:-12px;
      font-size:96px;
      opacity:0.12;
      transform: rotate(8deg);
    }}
    h1{{
      font-size: clamp(26px, 5.6vw, 46px);
      color:#fff;
      letter-spacing:0.2px;
      text-shadow: 0 2px 10px rgba(88, 66, 140, 0.25), 0 10px 35px rgba(120, 90, 190, 0.18);
      margin-bottom:8px;
      padding: 0 8px;
    }}
    .sparkle{{display:inline-block; animation:sparkle 2s infinite}}
    @keyframes sparkle{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.55;transform:scale(1.16)}}}}
    .subtitle{{
      font-size: clamp(14px, 3.6vw, 18px);
      color: rgba(255,255,255,0.92);
      font-style: italic;
    }}
    .image-section{{
      padding:22px 14px 30px;
      background: linear-gradient(to bottom, #fbfbff, #ffffff);
    }}
    .image-hero{{
      position:relative;
      width:min(100%, 980px);
      margin: 0 auto;
      border-radius:26px;
      padding: 26px 16px;
      background: {pal["hero_bg"]};
      box-shadow: {pal["shadow"]};
      border: 1px solid rgba(70, 60, 110, 0.10);
      overflow:hidden;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }}
    .image-hero::before{{
      content:"";
      position:absolute;
      inset:-40px;
      background: radial-gradient(circle at 50% 45%,
        rgba(255,255,255,0.85) 0%,
        rgba(210,195,255,0.35) 40%,
        rgba(180,220,255,0.22) 62%,
        rgba(120, 90, 190, 0.10) 78%,
        rgba(0,0,0,0) 100%);
      filter: blur(26px);
      opacity: 0.85;
      pointer-events:none;
      animation: glowPulse 3.5s ease-in-out infinite;
    }}
    @keyframes glowPulse{{0%,100%{{opacity:.70;transform:scale(1)}}50%{{opacity:1;transform:scale(1.02)}}}}
    .link-stack{{
      position:relative;
      z-index:2;
      display:grid;
      gap:14px;
      justify-items:center;
      text-align:center;
      padding: 6px 8px;
    }}
    .princess-link{{
      font-size: clamp(44px, 10vw, 70px);
      line-height:1;
      text-decoration:none;
      filter: drop-shadow(0 10px 22px rgba(0,0,0,0.16));
      transition: transform .15s ease, filter .15s ease;
      -webkit-tap-highlight-color: transparent;
      user-select:none;
    }}
    .princess-link:active{{transform:scale(0.96)}}
    .princess-link:hover{{transform:scale(1.03)}}
    .link-title{{
      font-size: clamp(18px, 4.6vw, 28px);
      font-weight: 800;
      color: {pal["text_dark"]};
      text-shadow: 0 1px 0 rgba(255,255,255,0.6);
      letter-spacing: 0.2px;
    }}
    .raw-btn{{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      width: min(520px, 92%);
      min-height: 62px;
      padding: 16px 22px;
      border-radius: 999px;
      font-size: clamp(18px, 4.6vw, 22px);
      font-weight: 900;
      letter-spacing: 0.6px;
      color:#fff;
      text-decoration:none;
      background: {pal["button_bg"]};
      box-shadow: 0 14px 34px rgba(107, 92, 255, 0.28);
      transition: transform .15s ease, box-shadow .15s ease;
      -webkit-tap-highlight-color: transparent;
      user-select:none;
    }}
    .raw-btn:hover{{transform: translateY(-1px)}}
    .raw-btn:active{{transform: translateY(1px) scale(0.985)}}
    .link-note{{
      font-size: 14px;
      color: {pal["note"]};
      font-style: italic;
    }}
    @media (prefers-reduced-motion: reduce){{
      .princess-link,.raw-btn{{transition:none}}
      .sparkle{{animation:none}}
      .image-hero::before{{animation:none}}
    }}
    /* Optional content area (kept minimal + safe) */
    .content{{
      padding: 0 18px 22px;
      max-width: 980px;
      margin: 0 auto;
    }}
    .mini{{
      margin-top: 14px;
      padding: 14px 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.65);
      border: 1px solid rgba(90,80,130,0.10);
      color: rgba(30,30,40,0.70);
      line-height: 1.6;
      font-size: 15px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1><span class="sparkle">✨</span> {_html.escape(title)} <span class="sparkle">✨</span></h1>
      <div class="subtitle">{_html.escape(subtitle)}</div>
    </div>

    <div class="image-section">
      <div class="image-hero">
        <div class="link-stack">
          <a class="princess-link" href="{_html.escape(link)}" target="_blank" rel="noopener noreferrer"
             aria-label="Open birthday gallery link">{_html.escape(emoji)}</a>
          <div class="link-title">Open Birthday Gallery</div>
          <a class="raw-btn" href="{_html.escape(link)}" target="_blank" rel="noopener noreferrer">{_html.escape(button_text)}</a>
          <div class="link-note">{_html.escape(note)}</div>
        </div>
      </div>
    </div>

    <div class="content">
      <div class="mini">
        Tip: This layout is <b>iframe-safe</b> inside Streamlit. If you want images, prefer hosting that returns a direct
        <code>.png/.jpg</code> URL (or keep it link-first like this).
      </div>
    </div>
  </div>
</body>
</html>
"""


# -----------------------------
# HEADER
# -----------------------------
st.title(APP_TITLE)
st.caption(f"Reading birthday HTML cards from: `{TOOLS_DIR}`")

# -----------------------------
# SIDEBAR CONTROLS
# -----------------------------
with st.sidebar:
    st.header("Controls")

    # Abort / Reset (prevents your “editor overlapping/bleeding” feeling)
    if st.button("🧯 Abort / Reset View", use_container_width=True):
        reset_all()

    st.divider()

    # Tool selection + viewer config
    tools = list_html_tools()
    if tools:
        # Keep selection stable
        default_index = 0
        if st.session_state.selected_tool in tools:
            default_index = tools.index(st.session_state.selected_tool)

        picked = st.selectbox("Choose a card", tools, index=default_index)
        st.session_state.selected_tool = picked
    else:
        st.info("No birthday .html cards yet. Add one below.")

    st.session_state.viewer_height = st.slider("Viewer height", 520, 1400, st.session_state.viewer_height, 20)

    st.divider()
    st.subheader("Safety mode")
    st.session_state.safe_mode = st.toggle("Safe mode (recommended)", value=st.session_state.safe_mode)
    st.caption("Safe mode blocks scripts/forms/popups in the iframe.")

    st.divider()
    st.subheader("➕ Add HTML (paste)")
    with st.expander("Open paste uploader", expanded=False):
        st.session_state.draft_filename = st.text_input("Filename (e.g., Benji_1994.html)", st.session_state.draft_filename)
        st.session_state.draft_html_custom = st.text_area(
            "Paste full HTML here",
            st.session_state.draft_html_custom,
            height=220,
            placeholder="<!DOCTYPE html> ...",
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save pasted HTML", use_container_width=True, disabled=not st.session_state.draft_html_custom.strip()):
                dest = save_html(st.session_state.draft_filename, st.session_state.draft_html_custom)
                st.success(f"Saved: {dest.name}")
                st.session_state.selected_tool = dest.name
                st.session_state.draft_html_custom = ""
                st.rerun()
        with c2:
            if st.button("🧹 Clear paste box", use_container_width=True):
                st.session_state.draft_html_custom = ""
                st.rerun()

    st.divider()
    st.subheader("🎨 Palette Generator (glassy polish)")
    st.caption("This does NOT change the Streamlit app UI. It generates a new birthday HTML card.")
    st.session_state.palette_key = st.selectbox("Choose a palette", list(PALETTES.keys()), index=list(PALETTES.keys()).index(st.session_state.palette_key))

    with st.expander("Build a new Birthday Card (template)", expanded=False):
        st.session_state.draft_title = st.text_input("Title (top)", st.session_state.draft_title)
        st.session_state.draft_subtitle = st.text_input("Subtitle (top)", st.session_state.draft_subtitle)
        st.session_state.draft_link = st.text_input("Link (Imgur/Drive/etc.)", st.session_state.draft_link)
        st.session_state.draft_emoji = st.text_input("Emoji (center link)", st.session_state.draft_emoji)
        st.session_state.draft_button_text = st.text_input("Button text", st.session_state.draft_button_text)
        st.session_state.draft_note = st.text_input("Small note", st.session_state.draft_note)
        st.session_state.draft_filename = st.text_input("Save as (filename)", st.session_state.draft_filename)

        gen_html = render_birthday_template(
            title=st.session_state.draft_title,
            subtitle=st.session_state.draft_subtitle,
            link=st.session_state.draft_link,
            emoji=st.session_state.draft_emoji,
            button_text=st.session_state.draft_button_text,
            note=st.session_state.draft_note,
            palette_key=st.session_state.palette_key,
        )

        st.code(gen_html[:1500] + ("\n...\n" if len(gen_html) > 1500 else ""), language="html")

        if st.button("✨ Generate & Save Card", use_container_width=True):
            dest = save_html(st.session_state.draft_filename, gen_html)
            st.success(f"Generated: {dest.name}")
            st.session_state.selected_tool = dest.name
            st.rerun()

    # -------------------------
    # ADMIN: PALM ID + DELETE
    # -------------------------
    st.divider()
    st.subheader("🔒 Admin (Delete cards)")

    # Palm tap gate
    colL, colR = st.columns([0.82, 0.18])
    with colR:
        if st.button("🌴", help="Palm ID (tap 3x)"):
            st.session_state.palm_taps += 1
            if st.session_state.palm_taps >= 3:
                st.session_state.show_admin_box = True

    if st.session_state.show_admin_box and not st.session_state.admin_unlocked:
        st.write("**Palm ID:** enter admin code")
        code_try = st.text_input("Admin Code", type="password", placeholder="Enter code…")
        a, b = st.columns(2)
        with a:
            if st.button("Unlock", use_container_width=True):
                if code_try == ADMIN_CODE:
                    st.session_state.admin_unlocked = True
                    st.success("Admin unlocked.")
                    st.rerun()
                else:
                    st.error("Incorrect code.")
        with b:
            if st.button("Reset", use_container_width=True):
                st.session_state.palm_taps = 0
                st.session_state.show_admin_box = False
                st.session_state.admin_unlocked = False
                st.rerun()

    if st.session_state.admin_unlocked:
        st.caption("Palm ID: unlocked")
        admin_tools = list_html_tools()
        if not admin_tools:
            st.info("Nothing to delete yet.")
        else:
            pick_del = st.selectbox("Select a card to delete", ["(choose)"] + admin_tools)
            if pick_del != "(choose)":
                st.warning("Deleting removes the .html file from the birthdays folder.")
                if st.button("🗑️ Delete Selected", type="primary", use_container_width=True):
                    ok = delete_html(pick_del)
                    if ok:
                        st.success(f"Deleted: {pick_del}")
                        # If you deleted the currently viewed tool, clear selection
                        if st.session_state.selected_tool == pick_del:
                            st.session_state.selected_tool = None
                        st.rerun()
                    else:
                        st.error("File not found.")


# -----------------------------
# MAIN VIEWER
# -----------------------------
tools_now = list_html_tools()
if not tools_now:
    st.info("Add a birthday card from the sidebar: **Add HTML (paste)** or **Palette Generator**.")
    st.stop()

selected = st.session_state.selected_tool or tools_now[0]
if selected not in tools_now:
    selected = tools_now[0]
    st.session_state.selected_tool = selected

# Load HTML
try:
    raw_html = load_html(selected)
except Exception as e:
    st.error(f"Could not read file: `{selected}`")
    st.exception(e)
    st.stop()

escaped = _html.escape(raw_html, quote=True)

# Sandbox
if st.session_state.safe_mode:
    sandbox = "allow-same-origin"  # locked down
else:
    sandbox = "allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin"

# Viewer wrapper (glassy)
height = st.session_state.viewer_height
viewer_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  html, body {{
    margin:0; padding:0; height:100%;
    background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.85), rgba(255,255,255,0) 55%),
                radial-gradient(circle at 80% 10%, rgba(225,214,255,0.35), rgba(255,255,255,0) 60%),
                linear-gradient(135deg, #f7f8ff 0%, #eef2ff 40%, #f3f4ff 100%);
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  }}
  .frame {{
    width: min(1200px, calc(100% - 24px));
    margin: 14px auto;
    height: {height}px;
    border-radius: 22px;
    overflow:hidden;
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(90,80,130,0.12);
    box-shadow: 0 18px 60px rgba(0,0,0,0.14);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }}
  iframe {{
    width:100%;
    height:100%;
    border:0;
    background:white;
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
