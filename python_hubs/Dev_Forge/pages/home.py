# pages/home.py
"""
DevForge Home Page — 1:1 rebuild
Top to bottom:
1) Hero
2) Student Work Reel (Admin upload -> staged -> commit)
3) DevPage promotion
4) Instructions (how to use)
5) User entry (signature + quick notes)
6) Persistent ticker (only renders once)
7) Share link + QR (copy/email; QR if qrcode installed)
"""

import streamlit as st
from pathlib import Path
from textwrap import dedent
import base64, json, time, re, urllib.parse

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="DevForge — Home", layout="wide")

# Safety defaults (won't override hub logic)
st.session_state.setdefault("admin_unlocked", False)
st.session_state.setdefault("dev_theme", st.session_state.get("dev_theme", "science"))

# -----------------------------
# Storage: NOT repo unless you commit it
# -----------------------------
MEDIA_DIR = Path("devforge_media/home_reel")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = MEDIA_DIR / "index.json"

CUSTOM_QR_ENABLED = True  # will auto-disable if qrcode lib not present

# -----------------------------
# Helpers
# -----------------------------
def _load_index() -> list[str]:
    if INDEX_PATH.exists():
        try:
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def _save_index(items: list[str]) -> None:
    INDEX_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")

def _safe_ext(name: str) -> str:
    n = (name or "").lower()
    if n.endswith(".png"):
        return ".png"
    if n.endswith(".jpg") or n.endswith(".jpeg"):
        return ".jpg"
    return ""

def _data_uri_from_file(p: Path) -> str:
    ext = p.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def _slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9_-]", "", s)
    return s[:48] or "devforge"

def _render_ticker_once(text: str) -> None:
    """
    Avoid duplicate tickers across hub/pages.
    If another page already rendered it in this session, we skip.
    """
    if st.session_state.get("_devforge_ticker_rendered", False):
        return
    st.session_state["_devforge_ticker_rendered"] = True
    st.markdown(
        dedent(f"""
        <style>
          .devforge-ticker {{
            position: fixed;
            left: 0; right: 0; bottom: 0;
            z-index: 9999;
            padding: 10px 18px;
            text-align: center;
            font-weight: 900;
            letter-spacing: .08em;
            border-top: 1px solid rgba(255,255,255,0.22);
            background: rgba(255,255,255,0.10);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
          }}
          .devforge-ticker span {{
            display:inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.26);
            background: rgba(255,255,255,0.12);
          }}
          .devforge-ticker-spacer {{ height: 70px; }}
        </style>
        <div class="devforge-ticker"><span>{text}</span></div>
        <div class="devforge-ticker-spacer"></div>
        """).strip(),
        unsafe_allow_html=True,
    )

def _make_qr_png_bytes(data: str) -> bytes | None:
    """
    Returns PNG bytes for QR if qrcode is installed, else None.
    """
    global CUSTOM_QR_ENABLED
    if not CUSTOM_QR_ENABLED:
        return None
    try:
        import qrcode
        from io import BytesIO
        qr = qrcode.QRCode(version=None, box_size=8, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        CUSTOM_QR_ENABLED = False
        return None


# ============================================================
# 1) HERO (dedent prevents the “HTML showing as text” issue)
# ============================================================
st.markdown(
    dedent("""
    <style>
      .df-hero{
        text-align: center;
        padding: 4.2rem 1.5rem 2.25rem;
        background: linear-gradient(135deg, var(--bg), rgba(20,184,166,0.06));
        border-radius: 0 0 2rem 2rem;
        margin: -1.5rem -2rem 1.6rem;
        position: relative;
        overflow: hidden;
      }
      .df-title{
        font-size: 4.2rem;
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.05;
        display:flex;
        align-items:center;
        justify-content:center;
        gap: 14px;
      }
      .df-title .word{
        background: linear-gradient(90deg, var(--accent), var(--accent2, var(--accent)));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
      }
      .df-kicker{
        font-size: 1.35rem;
        margin: 1.1rem 0 1.2rem;
        opacity: 0.92;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }
      .df-badge{
        display:inline-flex;
        align-items:center;
        gap:8px;
        padding: 0.7rem 1.6rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.22);
        background: rgba(255,255,255,0.10);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        font-weight: 900;
        opacity: 0.95;
      }
      @keyframes dfPulse { 0%,100%{ transform: scale(1); } 50%{ transform: scale(1.03);} }
      .df-pulse{ animation: dfPulse 4.6s infinite ease-in-out; display:inline-block; }
    </style>

    <div class="df-hero">
      <div class="df-title">
        <span style="font-size:3.2rem;">🔧</span>
        <span class="word">DevForge</span>
      </div>
      <div class="df-kicker">Your Personal Streamlit Development Forge</div>
      <div class="df-pulse"><span class="df-badge">We are L.E.A.D.</span></div>
    </div>
    """).strip(),
    unsafe_allow_html=True
)

# ============================================================
# 2) STUDENT WORK REEL (smooth upload: staged -> commit)
# ============================================================
st.subheader("Student Work Reel")

reel_items = _load_index()

# Admin controls
if st.session_state.get("admin_unlocked", False):
    st.caption("Admin: Upload PNG/JPG → preview → Commit. (No repo edits; saves to devforge_media/home_reel/)")

    st.session_state.setdefault("_reel_staged_files", [])

    with st.form("reel_uploader_form", clear_on_submit=False):
        staged = st.file_uploader(
            "Add images (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="reel_uploader",
        )
        cA, cB = st.columns([1, 1])
        with cA:
            commit = st.form_submit_button("✅ Commit to Reel", use_container_width=True)
        with cB:
            clear_stage = st.form_submit_button("🧹 Clear Staging", use_container_width=True)

    if clear_stage:
        st.session_state["_reel_staged_files"] = []
        st.rerun()

    # Update staging list without forcing save
    if staged:
        st.session_state["_reel_staged_files"] = staged

    if st.session_state["_reel_staged_files"]:
        with st.expander("Staging Preview (not saved yet)", expanded=True):
            cols = st.columns(4)
            for i, f in enumerate(st.session_state["_reel_staged_files"]):
                with cols[i % 4]:
                    st.image(f, use_container_width=True)
            st.caption("Press **Commit to Reel** to save these into the slideshow.")

    if commit and st.session_state["_reel_staged_files"]:
        changed = False
        for f in st.session_state["_reel_staged_files"]:
            ext = _safe_ext(f.name)
            if not ext:
                continue
            fname = f"reel_{int(time.time()*1000)}{ext}"
            out = MEDIA_DIR / fname
            out.write_bytes(f.getbuffer())
            reel_items.append(fname)
            changed = True

        if changed:
            # de-dupe, cap to 18
            deduped = []
            seen = set()
            for x in reel_items:
                if x not in seen:
                    deduped.append(x)
                    seen.add(x)
            reel_items = deduped[-18:]
            _save_index(reel_items)

        st.session_state["_reel_staged_files"] = []
        st.success("Reel updated.")
        st.rerun()

# Build slides (data uris)
slides = []
for fname in reel_items:
    p = MEDIA_DIR / fname
    if p.exists() and p.suffix.lower() in (".png", ".jpg", ".jpeg"):
        slides.append(_data_uri_from_file(p))

if not slides:
    slides = [""]  # placeholder

per_slide = 4.5
total = max(1, len(slides)) * per_slide

slides_html = ""
for i, uri in enumerate(slides):
    delay = i * per_slide
    if uri:
        slides_html += f"""
        <div class="df-reel-slide" style="animation-delay:{delay}s">
          <img src="{uri}" alt="student work {i+1}" />
        </div>
        """
    else:
        slides_html += f"""
        <div class="df-reel-slide" style="animation-delay:{delay}s">
          <div class="df-reel-empty">
            <div style="font-weight:900; font-size:1.05rem;">Student Work Reel</div>
            <div style="opacity:.75; margin-top:.35rem;">(Admin can upload PNG/JPG.)</div>
          </div>
        </div>
        """

st.markdown(
    dedent(f"""
    <style>
      .df-reel-frame {{
        position: relative;
        height: 340px;
        border-radius: 22px;
        overflow: hidden;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.22);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 18px 40px rgba(0,0,0,0.10);
      }}
      .df-reel-slide {{
        position: absolute;
        inset: 0;
        display:flex;
        align-items:center;
        justify-content:center;
        padding: 18px;
        opacity: 0;
        animation: dfReelFade {total}s infinite ease-in-out;
        will-change: opacity, transform;
      }}
      .df-reel-slide img {{
        max-height: 100%;
        max-width: 100%;
        border-radius: 18px;
        object-fit: contain;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.28);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 14px 28px rgba(0,0,0,0.12);
        padding: 10px;
      }}
      .df-reel-empty {{
        width: 100%;
        height: 100%;
        border-radius: 18px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        background: rgba(255,255,255,0.10);
        border: 1px dashed rgba(255,255,255,0.28);
      }}
      @keyframes dfReelFade {{
        0%   {{ opacity: 0; transform: scale(0.996); }}
        10%  {{ opacity: 1; transform: scale(1.0); }}
        30%  {{ opacity: 1; transform: scale(1.0); }}
        45%  {{ opacity: 0; transform: scale(1.004); }}
        100% {{ opacity: 0; }}
      }}
    </style>
    <div class="df-reel-frame">{slides_html}</div>
    """).strip(),
    unsafe_allow_html=True
)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# ============================================================
# 3) PROMOTE DEV PAGE (your attached vibe)
# ============================================================
st.subheader("DevPage")
st.caption("A clean entry point for teachers and tools. One link. One hub.")

promo = st.columns([1.3, 1], gap="large")
with promo[0]:
    st.markdown(
        dedent("""
        <div style="
          padding: 18px 18px;
          border-radius: 18px;
          background: rgba(255,255,255,0.10);
          border: 1px solid rgba(255,255,255,0.22);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          box-shadow: 0 18px 40px rgba(0,0,0,0.08);
        ">
          <div style="font-weight:900; font-size:1.2rem;">What DevPage is</div>
          <div style="opacity:.82; margin-top:.5rem; line-height:1.55;">
            • A home for teacher tools (no Google Sites headache)<br/>
            • Fast launches, consistent UI, export-ready assets<br/>
            • Admin gated uploads & templates, student-safe output
          </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )

with promo[1]:
    # Keep your original quick launch buttons but present “DevPage” as the primary path.
    st.markdown(
        dedent("""
        <div style="
          padding: 18px;
          border-radius: 18px;
          background: rgba(255,255,255,0.10);
          border: 1px solid rgba(255,255,255,0.22);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          box-shadow: 0 18px 40px rgba(0,0,0,0.08);
        ">
          <div style="font-weight:900; font-size:1.2rem;">Quick Launch</div>
          <div style="opacity:.82; margin-top:.4rem;">Core tools right now.</div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )
    c = st.columns(3)
    with c[0]:
        if st.button("🔬 Science", use_container_width=True, type="primary"):
            st.switch_page("pages/Ms_Piluso_Science.py")
    with c[1]:
        if st.button("📚 Library", use_container_width=True, type="primary"):
            st.switch_page("pages/Code_Library.py")
    with c[2]:
        if st.button("⚡ ABC", use_container_width=True, type="primary"):
            st.switch_page("pages/ABC_Generator.py")

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# ============================================================
# 4) INSTRUCTIONS (How to use)
# ============================================================
st.subheader("How to Use DevForge")
with st.expander("Open instructions", expanded=False):
    st.markdown(
        """
**Workflow**
1. **Choose a tool** (Science / Library / ABC)  
2. **Use the outputs** (copy/paste code blocks, exports, JPGs)  
3. **Save what matters** (your signature, notes, and admin-managed assets)

**Admin**
- Upload student work in the **Home Reel** without touching the repo  
- Keep the reel updated for demos + stakeholder walkthroughs

**Theme**
- Science mode = your blue/green science palette  
- Neutral mode = light gray across UI with black text (as previously defined)
        """.strip()
    )

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# ============================================================
# 5) USER ENTRY (signature + quick notes)
# ============================================================
st.subheader("User Entry")

col_sig, col_notes = st.columns([1, 1], gap="large")

with col_sig:
    current_sig = st.session_state.get("signature", "")
    new_sig = st.text_input(
        "Developer Signature / Name",
        value=current_sig,
        placeholder="e.g., Ben • Lead Developer • L.E.A.D.",
        help="Used across DevForge exports and sidebar identity.",
        key="home_signature_input",
    )
    if new_sig.strip() != current_sig:
        st.session_state["signature"] = new_sig.strip()
        st.success("Signature updated.", icon="✅")

with col_notes:
    notes = st.session_state.get("notes", "")
    new_note = st.text_input("Quick note", placeholder="One-line thought…", key="home_quick_note")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Append", use_container_width=True):
            if new_note.strip():
                st.session_state["notes"] = (notes + "\n" + new_note.strip()).strip()
                st.success("Note appended.")
                st.rerun()
    with b2:
        if st.button("Clear Notes", use_container_width=True):
            st.session_state["notes"] = ""
            st.success("Notes cleared.")
            st.rerun()

    if st.session_state.get("notes", ""):
        lines = st.session_state["notes"].splitlines()
        st.caption("Recent (last 3 lines)")
        st.code("\n".join(lines[-3:]), language=None)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ============================================================
# 6) PERSISTENT TICKER (only render if not already rendered)
# ============================================================
ticker_text = st.session_state.get("ticker_text", "DEVFORGE • We are L.E.A.D. 🌟")
_render_ticker_once(ticker_text)

# ============================================================
# 7) SHARE LINK + QR (copy/email + QR if dependency exists)
# ============================================================
st.subheader("Share DevForge")

# Try to use Streamlit’s own host URL if available; otherwise user can paste.
default_url = st.session_state.get("devforge_share_url", "")
share_url = st.text_input(
    "Share URL",
    value=default_url,
    placeholder="Paste your hub URL here (e.g., https://your-hub/DevForge)",
    help="Used for Copy / Email and QR code.",
    key="share_url_input",
)
if share_url.strip() and share_url.strip() != default_url:
    st.session_state["devforge_share_url"] = share_url.strip()

c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

with c1:
    # Copy button (Streamlit built-in)
    st.code(share_url.strip() if share_url.strip() else "(add a URL above)", language=None)

with c2:
    if share_url.strip():
        subject = urllib.parse.quote("DevForge link")
        body = urllib.parse.quote(f"Here’s the DevForge link:\n\n{share_url.strip()}\n")
        st.link_button("✉️ Share by Email", f"mailto:?subject={subject}&body={body}", use_container_width=True)
    else:
        st.button("✉️ Share by Email", disabled=True, use_container_width=True)

with c3:
    # Optional QR
    if share_url.strip():
        qr_bytes = _make_qr_png_bytes(share_url.strip())
        if qr_bytes:
            st.image(qr_bytes, caption="QR code", use_container_width=True)
            st.download_button("Download QR (PNG)", qr_bytes, file_name=f"{_slug('devforge')}_qr.png", mime="image/png", use_container_width=True)
        else:
            st.info("QR not available. Install `qrcode[pil]` to enable QR rendering.")
    else:
        st.info("Add a URL to generate QR.")

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
