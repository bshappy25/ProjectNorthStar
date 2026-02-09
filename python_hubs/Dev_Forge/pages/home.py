# --- HERO + REEL (1:1 replacement, fixes HTML showing as text) ---
import base64
from pathlib import Path
from textwrap import dedent
import json
import time

MEDIA_DIR = Path("devforge_media/home_reel")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = MEDIA_DIR / "index.json"

def _load_reel_index():
    if INDEX_PATH.exists():
        try:
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def _save_reel_index(items):
    INDEX_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")

def _data_uri_from_file(p: Path) -> str:
    ext = p.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def _safe_ext(name: str) -> str:
    name = (name or "").lower()
    if name.endswith(".png"):
        return ".png"
    if name.endswith(".jpg") or name.endswith(".jpeg"):
        return ".jpg"
    return ""

# Load reel list
reel_items = _load_reel_index()

# Admin-only upload UI (saves to disk; not repo unless committed)
if st.session_state.get("admin_unlocked", False):
    st.markdown("### 🖼️ Home Reel (Admin)")
    up = st.file_uploader(
        "Add images to the Home Reel (PNG/JPG only)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="home_reel_uploader",
        help="Uploads save to devforge_media/home_reel/ (not your repo unless you commit).",
    )
    if up:
        changed = False
        for f in up:
            ext = _safe_ext(f.name)
            if not ext:
                continue
            fname = f"reel_{int(time.time()*1000)}{ext}"
            out = MEDIA_DIR / fname
            out.write_bytes(f.getbuffer())
            reel_items.append(fname)
            changed = True

        if changed:
            # keep most recent first; cap to 18 to keep the hero light
            reel_items = list(dict.fromkeys(reel_items[::-1]))[::-1]
            reel_items = reel_items[-18:]
            _save_reel_index(reel_items)
            st.success("Reel updated.")
            st.rerun()

    if reel_items:
        with st.expander("Manage Reel Images", expanded=False):
            cols = st.columns(3)
            for i, fname in enumerate(list(reel_items)):
                p = MEDIA_DIR / fname
                if not p.exists():
                    continue
                with cols[i % 3]:
                    st.image(str(p), use_container_width=True)
                    if st.button(f"Remove {fname}", key=f"rm_reel_{fname}"):
                        # remove from index + delete file
                        reel_items = [x for x in reel_items if x != fname]
                        try:
                            p.unlink(missing_ok=True)
                        except Exception:
                            pass
                        _save_reel_index(reel_items)
                        st.rerun()

# Build slideshow HTML (inside hero)
slides = []
for fname in reel_items:
    p = MEDIA_DIR / fname
    if p.exists() and p.suffix.lower() in (".png", ".jpg", ".jpeg"):
        slides.append(_data_uri_from_file(p))

# If empty, show a tasteful placeholder panel
if not slides:
    slides = [""]

n = len(slides)
per_slide = 4.5  # seconds per image (subtle)
total = max(1, n) * per_slide

slides_html = ""
for idx, uri in enumerate(slides):
    delay = idx * per_slide
    if uri:
        slides_html += f"""
        <div class="reel-slide" style="animation-delay:{delay}s">
          <img src="{uri}" alt="student work {idx+1}" />
        </div>
        """
    else:
        slides_html += f"""
        <div class="reel-slide" style="animation-delay:{delay}s">
          <div class="reel-empty">
            <div style="font-weight:900; font-size:1.05rem;">Student Work Reel</div>
            <div style="opacity:.75; margin-top:.35rem;">(Admin can upload PNG/JPG to populate.)</div>
          </div>
        </div>
        """

# IMPORTANT: dedent() prevents Markdown code-block rendering
hero_html = dedent(f"""
<div class="devforge-hero">
  <h1 class="devforge-title">🔧 DevForge</h1>

  <p class="kicker">
    Your Personal Streamlit Development Forge
  </p>

  <div class="lead-wrap">
    <span class="badge badge-accent">We are L.E.A.D.</span>
  </div>

  <div class="reel-wrap">
    <div class="reel-frame">
      {slides_html}
    </div>
  </div>
</div>

<style>
/* HERO */
.devforge-hero {{
  text-align:center;
  padding: 5rem 1.5rem 4rem;
  background: linear-gradient(135deg, var(--bg), rgba(20,184,166,0.06));
  border-radius: 0 0 2rem 2rem;
  margin: -1.5rem -2rem 3rem;
  position: relative;
  overflow: hidden;
}}

.devforge-title {{
  font-size: 4.5rem;
  margin: 0;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, var(--accent), var(--accent2, var(--accent)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.05;
}}

.kicker {{
  font-size: 1.6rem;
  margin: 1.25rem 0 1.25rem;
  opacity: 0.92;
  font-weight: 400;
  letter-spacing: 0.02em;
}}

.lead-wrap {{
  animation: pulse 4.5s infinite ease-in-out;
  display: inline-block;
  margin-bottom: 1.75rem;
}}

.reel-wrap {{
  max-width: 980px;
  margin: 0 auto;
  padding: 0 0.25rem;
}}

.reel-frame {{
  position: relative;
  height: 320px;
  border-radius: 22px;
  overflow: hidden;

  /* glassy board container */
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.24);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.10);
}}

.reel-slide {{
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px;
  opacity: 0;
  animation: reelFade {total}s infinite ease-in-out;
}}

.reel-slide img {{
  max-height: 100%;
  max-width: 100%;
  border-radius: 18px;
  object-fit: contain;

  /* each image gets its own glassy board */
  background: rgba(255,255,255,0.14);
  border: 1px solid rgba(255,255,255,0.28);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 14px 28px rgba(0,0,0,0.12);
  padding: 10px;
}}

.reel-empty {{
  width: 100%;
  height: 100%;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.10);
  border: 1px dashed rgba(255,255,255,0.28);
}}

@keyframes reelFade {{
  0%   {{ opacity: 0; transform: scale(0.995); }}
  8%   {{ opacity: 1; transform: scale(1.0); }}
  28%  {{ opacity: 1; transform: scale(1.0); }}
  40%  {{ opacity: 0; transform: scale(1.005); }}
  100% {{ opacity: 0; }}
}}
</style>
""").strip()

st.markdown(hero_html, unsafe_allow_html=True)
