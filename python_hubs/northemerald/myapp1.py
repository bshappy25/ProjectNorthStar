"""
╔══════════════════════════════════════════════════════════════╗
║                    Teacher Tools - Emerald                   ║
║              VIP TV Mode • HTML Teaching Tools               ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import html
import time
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

TOOLS_DIR = Path("teacher_tools")
TOOLS_DIR.mkdir(exist_ok=True)

MAX_TOOLS = 25
ADMIN_CODE = "Bshapp"

# Emerald theme colors
EMERALD_BG = "#0f2027"
EMERALD_CARD = "rgba(62, 139, 95, 0.2)"
EMERALD_BORDER = "rgba(95, 179, 130, 0.3)"
EMERALD_TEXT = "rgba(255, 255, 255, 0.92)"
EMERALD_MUTED = "rgba(255, 255, 255, 0.74)"
EMERALD_ACCENT = "#5fb382"

# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def list_tools():
    """Return tool stems for all .html files in teacher_tools/"""
    return sorted([p.stem for p in TOOLS_DIR.glob("*.html")])

def tool_path(stem: str) -> Path:
    return TOOLS_DIR / f"{stem}.html"

def load_tool(stem: str) -> str:
    p = tool_path(stem)
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    return ""

def save_tool(name: str, html_code: str) -> Path:
    """Save as <name>.html (no edits to content)."""
    p = tool_path(name)
    p.write_text(html_code, encoding="utf-8")
    return p

def safe_stem(name: str) -> str:
    """Keep letters, numbers, underscores, hyphens; convert spaces to underscores."""
    stem = Path(name).stem.strip()
    stem = stem.replace(" ", "_")
    stem = re.sub(r"[^A-Za-z0-9_\-]+", "", stem)
    stem = stem[:60] if stem else "uploaded_tool"
    return stem

def next_available_stem(base: str) -> str:
    """Avoid overwrite: base, base_1, base_2 ..."""
    base = safe_stem(base)
    if not tool_path(base).exists():
        return base
    n = 1
    while True:
        cand = f"{base}_{n}"
        if not tool_path(cand).exists():
            return cand
        n += 1

def delete_tool(stem: str):
    p = tool_path(stem)
    if p.exists():
        p.unlink()
    if st.session_state.get("tt_current_tool") == stem:
        st.session_state["tt_current_tool"] = None

def cap_tools_guard():
    tools = list_tools()
    if len(tools) >= MAX_TOOLS:
        return True, f"Tool cap reached ({MAX_TOOLS}). Delete one to add more."
    return False, ""

def delete_self():
    """Delete this app module (admin only)"""
    from pathlib import Path
    app_path = Path(__file__)
    if app_path.exists():
        app_path.unlink()
        return True
    return False

# ═══════════════════════════════════════════════════════════════
# RENDER FUNCTION (called by app.py)
# ═══════════════════════════════════════════════════════════════

def render(admin_unlocked=False):
    """Main render function for Teacher Tools"""
    
    # Initialize session state for this module
    if "tt_current_tool" not in st.session_state:
        st.session_state.tt_current_tool = None
    if "tt_new_tool_name" not in st.session_state:
        st.session_state.tt_new_tool_name = ""
    if "tt_html_input" not in st.session_state:
        st.session_state.tt_html_input = ""
    if "tt_tool_search" not in st.session_state:
        st.session_state.tt_tool_search = ""
    if "tt_fav_tools" not in st.session_state:
        st.session_state.tt_fav_tools = set()
    if "tt_confirm_delete" not in st.session_state:
        st.session_state.tt_confirm_delete = False
    
    # Emerald styling
    st.markdown(f"""
    <style>
        .teacher-tools-container {{
            background: linear-gradient(135deg, rgba(62, 139, 95, 0.15) 0%, rgba(95, 179, 130, 0.05) 100%);
            border: 1px solid rgba(95, 179, 130, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
        }}
        
        .tt-header {{
            color: #5fb382;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(95, 179, 130, 0.3);
        }}
        
        .tt-badge {{
            display: inline-flex;
            gap: 10px;
            align-items: center;
            padding: 8px 16px;
            border-radius: 14px;
            border: 1px solid rgba(95, 179, 130, 0.3);
            background: rgba(95, 179, 130, 0.15);
            margin-bottom: 20px;
        }}
        
        .tt-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #5fb382;
            box-shadow: 0 0 18px rgba(95, 179, 130, 0.55);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .tv-frame {{
            position: relative;
            width: 100%;
            height: min(86vh, 980px);
            border: 3px solid rgba(95, 179, 130, 0.4);
            border-radius: 20px;
            overflow: hidden;
            background: rgba(0,0,0,0.05);
            box-shadow: 0 0 40px rgba(95, 179, 130, 0.20), inset 0 0 60px rgba(95, 179, 130, 0.06);
        }}
        
        .tv-frame::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
            pointer-events: none;
            z-index: 3;
            animation: scanlines 8s linear infinite;
        }}
        
        @keyframes scanlines {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(4px); }}
        }}
        
        .tv-label {{
            position: absolute;
            top: 10px;
            left: 12px;
            z-index: 6;
            padding: 8px 10px;
            border-radius: 14px;
            border: 1px solid rgba(95, 179, 130, 0.4);
            background: rgba(62, 139, 95, 0.3);
            color: rgba(255, 255, 255, 0.88);
            font-weight: 800;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            font-size: 12px;
            backdrop-filter: blur(10px);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="tt-header">◆ Teacher Tools Hub</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tt-badge">
        <div class="tt-dot"></div>
        <div style="font-weight: 900; letter-spacing: 0.10em; color: rgba(255, 255, 255, 0.9);">
            VIP VIEWING CONSOLE
        </div>
        <div style="opacity: 0.75; font-weight: 800; color: rgba(255, 255, 255, 0.7);">
            Preview • Upload • Manage
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for tool selection
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📺 Your Tools")
        
        st.session_state.tt_tool_search = st.text_input(
            "Search tools",
            placeholder="type to filter...",
            value=st.session_state.get("tt_tool_search", ""),
            key="tt_search_input"
        )
        
        tools_all = list_tools()
        q = st.session_state.tt_tool_search.strip().lower()
        
        favs = st.session_state.get("tt_fav_tools", set())
        tools_filtered = [t for t in tools_all if (q in t.lower())]
        tools_favs = [t for t in tools_filtered if t in favs]
        tools_rest = [t for t in tools_filtered if t not in favs]
        tools = tools_favs + tools_rest
        
        if not tools_all:
            st.info("No tools yet. Add one below!")
        else:
            for t in tools:
                is_active = st.session_state.tt_current_tool == t
                icon = "📺" if is_active else "📄"
                star = "⭐" if t in favs else "☆"
                
                cols = st.columns([0.82, 0.18])
                with cols[0]:
                    if st.button(
                        f"{icon} {t}",
                        key=f"tt_tool_{t}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary"
                    ):
                        st.session_state.tt_current_tool = t
                        st.session_state.tt_confirm_delete = False
                        st.rerun()
                
                with cols[1]:
                    if st.button(star, key=f"tt_fav_{t}", help="favorite"):
                        if t in favs:
                            favs.remove(t)
                        else:
                            favs.add(t)
                        st.session_state.tt_fav_tools = favs
                        st.rerun()
        
        st.caption(f"Limit: **{len(tools_all)}/{MAX_TOOLS}** tools")
    
    # Main tabs
    tabs = st.tabs(["📺 Preview", "➕ Add/Paste", "⬆️ Upload", "🛠️ Manage"])
    
    # TAB: PREVIEW
    with tabs[0]:
        if not st.session_state.tt_current_tool:
            st.markdown("""
            <div class="teacher-tools-container" style="text-align: center; padding: 60px 20px;">
                <h2 style="color: #5fb382; margin-bottom: 15px;">📺 Teacher Tools VIP Mode</h2>
                <p style="color: rgba(255, 255, 255, 0.7); font-size: 16px;">
                    Select a tool from the sidebar to view it in the VIP TV console.
                </p>
                <p style="color: rgba(255, 255, 255, 0.6); margin-top: 10px;">
                    💡 Tip: ⭐ favorite your daily drivers so they stay on top
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            tool_name = st.session_state.tt_current_tool
            tool_html = load_tool(tool_name)
            
            hcol1, hcol2, hcol3 = st.columns([0.64, 0.18, 0.18])
            with hcol1:
                st.markdown(f"### 📺 {tool_name}")
                st.caption("Viewing in VIP TV Mode • Tool content is not modified")
            
            with hcol2:
                if st.button("🔄 Refresh", use_container_width=True, key="tt_refresh"):
                    st.rerun()
            
            with hcol3:
                st.button("📸 Screenshot", use_container_width=True, help="Use device screenshot", key="tt_screenshot")
            
            if admin_unlocked:
                dcolA, dcolB = st.columns([0.85, 0.15])
                with dcolB:
                    if st.button("✖", help="Delete tool", use_container_width=True, key="tt_del_btn"):
                        st.session_state.tt_confirm_delete = True
                
                if st.session_state.get("tt_confirm_delete"):
                    st.warning("⚠️ Delete this tool? This cannot be undone.")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Confirm", type="primary", use_container_width=True, key="tt_confirm_yes"):
                            delete_tool(tool_name)
                            st.session_state.tt_confirm_delete = False
                            st.success(f"🗑️ Deleted: {tool_name}")
                            time.sleep(0.5)
                            st.rerun()
                    with c2:
                        if st.button("Cancel", use_container_width=True, key="tt_confirm_no"):
                            st.session_state.tt_confirm_delete = False
                            st.rerun()
            
            if not tool_html.strip():
                st.error("Tool file is empty or missing.")
            else:
                escaped = html.escape(tool_html, quote=True)
                combined = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
  html, body {{ height: 100%; margin: 0; background: transparent; }}
  .tv-frame {{
    position: relative; width: 100%; height: min(86vh, 980px);
    border: 3px solid rgba(95, 179, 130, 0.4); border-radius: 20px;
    overflow: hidden; background: rgba(0,0,0,0.05);
    box-shadow: 0 0 40px rgba(95, 179, 130, 0.20), inset 0 0 60px rgba(95, 179, 130, 0.06);
  }}
  .tv-frame::before {{
    content: ''; position: absolute; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
    pointer-events: none; z-index: 3; animation: scanlines 8s linear infinite;
  }}
  @keyframes scanlines {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(4px); }} }}
  .tv-label {{
    position: absolute; top: 10px; left: 12px; z-index: 6;
    padding: 8px 10px; border-radius: 14px;
    border: 1px solid rgba(95, 179, 130, 0.4);
    background: rgba(62, 139, 95, 0.3); color: rgba(255, 255, 255, 0.88);
    font-weight: 800; letter-spacing: 0.10em; font-size: 12px;
    backdrop-filter: blur(10px);
  }}
  .screen {{ position: relative; z-index: 5; width: 100%; height: 100%; background: rgba(255,255,255,0.06); }}
  iframe {{ width: 100%; height: 100%; border: 0; background: white; }}
</style>
</head>
<body>
  <div class="tv-frame">
    <div class="tv-label">EMERALD VIP PREVIEW</div>
    <div class="screen">
      <iframe sandbox="allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin" srcdoc="{escaped}"></iframe>
    </div>
  </div>
</body>
</html>
"""
                components.html(combined, height=1020, scrolling=False)
    
    # TAB: ADD/PASTE
    with tabs[1]:
        st.markdown("### ➕ Add New Tool (Paste HTML)")
        st.caption("Copy → Paste → Save. Does not modify existing tools.")
        
        cap_hit, cap_msg = cap_tools_guard()
        if cap_hit:
            st.error(cap_msg)
        else:
            tool_name_raw = st.text_input(
                "Tool Name",
                placeholder="e.g., Evidence Capture v1",
                value=st.session_state.get("tt_new_tool_name", ""),
                key="tt_name_input"
            )
            
            html_code = st.text_area(
                "HTML Code",
                placeholder="Paste your complete HTML code here...",
                height=320,
                value=st.session_state.get("tt_html_input", ""),
                key="tt_html_area"
            )
            
            c1, c2, c3 = st.columns([0.33, 0.33, 0.34])
            with c1:
                if st.button("🗑️ Clear", use_container_width=True, key="tt_clear"):
                    st.session_state.tt_html_input = ""
                    st.rerun()
            with c2:
                if st.button("🧪 Validate", use_container_width=True, key="tt_validate"):
                    s = (html_code or "").lower()
                    if "<html" not in s or "<body" not in s:
                        st.warning("⚠️ Missing <html> or <body>. May still work, but complete files are safer.")
                    else:
                        st.success("✅ Looks like a complete HTML document.")
            with c3:
                if st.button("💾 Save", type="primary", use_container_width=True, key="tt_save"):
                    if not tool_name_raw.strip():
                        st.error("❌ Enter a tool name!")
                    elif not html_code.strip():
                        st.error("❌ Paste HTML code!")
                    else:
                        safe_name = next_available_stem(tool_name_raw.strip())
                        save_tool(safe_name, html_code)
                        st.session_state.tt_current_tool = safe_name
                        st.session_state.tt_html_input = ""
                        st.session_state.tt_new_tool_name = ""
                        st.success(f"✅ Saved: {safe_name}.html")
                        time.sleep(0.5)
                        st.rerun()
    
    # TAB: UPLOAD
    with tabs[2]:
        st.markdown("### ⬆️ Upload HTML Tool")
        st.caption("Upload a .html file directly (requires admin unlock)")
        
        if not admin_unlocked:
            st.info("🔒 Admin access required. Unlock via Palm ID in main hub.")
        else:
            cap_hit, cap_msg = cap_tools_guard()
            if cap_hit:
                st.error(cap_msg)
            else:
                up = st.file_uploader("Upload .html file", type=["html"], key="tt_uploader")
                if up is not None:
                    base = safe_stem(up.name)
                    stem = next_available_stem(base)
                    dest = tool_path(stem)
                    dest.write_bytes(up.getbuffer())
                    st.session_state.tt_current_tool = stem
                    st.success(f"✅ Uploaded: {dest.name}")
                    time.sleep(0.5)
                    st.rerun()
    
    # TAB: MANAGE
    with tabs[3]:
        st.markdown("### 🛠️ Tool Management")
        
        tools = list_tools()
        
        with st.expander("📜 View Source Code", expanded=True):
            if not tools:
                st.info("No tools yet.")
            else:
                pick = st.selectbox("Select tool", ["(choose)"] + tools, key="tt_src_pick")
                if pick != "(choose)":
                    src = load_tool(pick)
                    st.caption("Read-only view of saved HTML")
                    st.download_button(
                        "⬇️ Download Backup",
                        data=src.encode("utf-8"),
                        file_name=f"{pick}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.text_area("HTML Source", value=src, height=300, key="tt_src_view")
        
        if admin_unlocked:
            with st.expander("🧹 Delete Tools", expanded=False):
                if not tools:
                    st.info("No tools to manage.")
                else:
                    pick = st.selectbox("Select tool to delete", ["(choose)"] + tools, key="tt_del_pick")
                    if pick != "(choose)":
                        st.warning("⚠️ This will permanently delete the tool file.")
                        colA, colB = st.columns(2)
                        with colA:
                            if st.button("✖ Delete", type="primary", use_container_width=True, key="tt_del_confirm"):
                                delete_tool(pick)
                                st.success(f"🗑️ Deleted: {pick}")
                                time.sleep(0.5)
                                st.rerun()
                        with colB:
                            st.button("Cancel", use_container_width=True, key="tt_del_cancel")
    
    # Admin delete this module
    if admin_unlocked:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete Teacher Tools module", use_container_width=True, key="tt_self_delete"):
                if delete_self():
                    st.success("🗑️ Teacher Tools module deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()
