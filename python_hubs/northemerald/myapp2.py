"""
╔══════════════════════════════════════════════════════════════╗
║                    Universal Gallery - Emerald               ║
║           Super Glossy Viewer • Connected to Tools           ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import html
import random
import time

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

GALLERY_DIR = Path("universal_gallery")
GALLERY_DIR.mkdir(exist_ok=True)

# Optional: Connect to teacher_tools directory
TEACHER_TOOLS_DIR = Path("teacher_tools")

ADMIN_CODE = "Bshapp"

# ═══════════════════════════════════════════════════════════════
# UI TINT SYSTEM - Super Glossy Universal Gray + Variants
# ═══════════════════════════════════════════════════════════════

TYPE_TINTS = {
    "Universal Gray": ("#0b0f17", "#111827", "#cbd5e1", "rgba(203,213,225,0.10)", "rgba(203,213,225,0.06)"),
    "Water (Blue)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(56,189,248,0.12)", "rgba(56,189,248,0.06)"),
    "Fire (Orange)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(251,146,60,0.12)", "rgba(251,146,60,0.06)"),
    "Fairy (Pink)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(251,113,133,0.12)", "rgba(251,113,133,0.06)"),
    "Grass (Green)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(34,197,94,0.12)", "rgba(34,197,94,0.06)"),
    "Electric (Yellow)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(245,158,11,0.12)", "rgba(245,158,11,0.06)"),
    "Emerald": ("#0b0f17", "#0f172a", "#5fb382", "rgba(95,179,130,0.12)", "rgba(95,179,130,0.06)")
}

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def list_gallery_entries():
    """List all HTML files in gallery"""
    return sorted([f for f in GALLERY_DIR.glob("*.html")])

def list_teacher_tools():
    """List all HTML files in teacher_tools (if exists)"""
    if TEACHER_TOOLS_DIR.exists():
        return sorted([f for f in TEACHER_TOOLS_DIR.glob("*.html")])
    return []

def get_entry_name(path):
    """Extract name from file path"""
    return path.stem.replace('_', ' ').title()

def delete_entry(path):
    """Delete selected HTML entry"""
    if path.exists():
        path.unlink()
        return True
    return False

def delete_self():
    """Delete this app module (admin only)"""
    app_path = Path(__file__)
    if app_path.exists():
        app_path.unlink()
        return True
    return False

# ═══════════════════════════════════════════════════════════════
# RENDER FUNCTION
# ═══════════════════════════════════════════════════════════════

def render(admin_unlocked=False):
    """Main render function for Universal Gallery"""
    
    # Initialize session state for this module
    if "ug_ui_tint" not in st.session_state:
        st.session_state.ug_ui_tint = "Universal Gray"
    if "ug_current_entry" not in st.session_state:
        st.session_state.ug_current_entry = None
    if "ug_preview_height" not in st.session_state:
        st.session_state.ug_preview_height = 800
    if "ug_source" not in st.session_state:
        st.session_state.ug_source = "gallery"  # "gallery" or "teacher_tools"
    if "ug_confirm_delete" not in st.session_state:
        st.session_state.ug_confirm_delete = False
    
    # Get current tint colors
    bg0, bg1, text, glass, glass2 = TYPE_TINTS[st.session_state.ug_ui_tint]
    
    # Super Glossy Universal Gray Styling
    st.markdown(f"""
    <style>
        :root {{
            --ug-bg0: {bg0};
            --ug-bg1: {bg1};
            --ug-text: {text};
            --ug-glass: {glass};
            --ug-glass2: {glass2};
            --ug-r1: 22px;
            --ug-r2: 16px;
            --ug-shadow: 0 16px 60px rgba(0,0,0,.45);
            --ug-shadow2: 0 10px 30px rgba(0,0,0,.20);
        }}
        
        .ug-container {{
            background:
                radial-gradient(1200px 800px at 20% 10%, var(--ug-glass), transparent 60%),
                radial-gradient(900px 700px at 80% 0%, var(--ug-glass2), transparent 55%),
                radial-gradient(900px 700px at 15% 30%, var(--ug-glass2), transparent 60%),
                linear-gradient(180deg, var(--ug-bg0), var(--ug-bg1));
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
        }}
        
        .ug-glass-card {{
            border-radius: var(--ug-r1);
            background: var(--ug-glass);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,.16);
            box-shadow: var(--ug-shadow);
            padding: 25px;
            margin: 15px 0;
        }}
        
        .ug-header {{
            color: {text};
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }}
        
        .ug-badge {{
            display: inline-flex;
            gap: 12px;
            align-items: center;
            padding: 10px 18px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,.16);
            background: var(--ug-glass);
            backdrop-filter: blur(20px);
            margin-bottom: 20px;
        }}
        
        .ug-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: {text};
            box-shadow: 0 0 18px rgba(203,213,225,0.55);
            animation: ug-pulse 2s infinite;
        }}
        
        @keyframes ug-pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.6; transform: scale(0.95); }}
        }}
        
        .ug-preview-frame {{
            border-radius: 16px;
            border: 2px solid rgba(255,255,255,.16);
            background: var(--ug-glass);
            backdrop-filter: blur(20px);
            box-shadow: var(--ug-shadow);
            overflow: hidden;
        }}
        
        .stButton>button {{
            background: var(--ug-glass) !important;
            backdrop-filter: blur(20px) !important;
            color: {text} !important;
            border: 1px solid rgba(255,255,255,.16) !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton>button:hover {{
            background: rgba(255,255,255,.12) !important;
            border-color: rgba(255,255,255,.24) !important;
            transform: translateY(-2px) !important;
            box-shadow: var(--ug-shadow2) !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🪟 Universal Gallery")
        
        # UI Tint Selector
        st.session_state.ug_ui_tint = st.selectbox(
            "UI Tint",
            list(TYPE_TINTS.keys()),
            index=list(TYPE_TINTS.keys()).index(st.session_state.ug_ui_tint),
            key="ug_tint_select"
        )
        
        st.markdown("---")
        
        # Source selector (Gallery or Teacher Tools)
        st.markdown("### 📂 Source")
        
        sources_available = ["Gallery"]
        if TEACHER_TOOLS_DIR.exists() and list_teacher_tools():
            sources_available.append("Teacher Tools")
        
        if len(sources_available) > 1:
            st.session_state.ug_source = st.radio(
                "View from:",
                sources_available,
                index=sources_available.index(st.session_state.ug_source) if st.session_state.ug_source in sources_available else 0,
                key="ug_source_radio"
            ).lower().replace(" ", "_")
        else:
            st.session_state.ug_source = "gallery"
            st.info("💡 Create tools in Teacher Tools to view them here!")
        
        st.markdown("---")
        
        # Entry Selection
        st.markdown("### 📋 Library")
        
        if st.session_state.ug_source == "teacher_tools":
            all_entries = list_teacher_tools()
            source_label = "Teacher Tools"
        else:
            all_entries = list_gallery_entries()
            source_label = "Gallery"
        
        if all_entries:
            entry_names = [get_entry_name(entry) for entry in all_entries]
            
            # Random button
            if st.button("🎲 Random", use_container_width=True, key="ug_random"):
                st.session_state.ug_current_entry = random.choice(all_entries)
                st.rerun()
            
            # Dropdown
            current_index = 0
            if st.session_state.ug_current_entry and st.session_state.ug_current_entry in all_entries:
                try:
                    current_index = all_entries.index(st.session_state.ug_current_entry)
                except ValueError:
                    current_index = 0
            
            selected_name = st.selectbox(
                f"Select from {source_label}",
                entry_names,
                index=current_index,
                label_visibility="collapsed",
                key="ug_entry_select"
            )
            
            selected_index = entry_names.index(selected_name)
            st.session_state.ug_current_entry = all_entries[selected_index]
            
            st.info(f"**{len(all_entries)}** entries in {source_label}")
        else:
            st.warning(f"No entries in {source_label}.")
        
        st.markdown("---")
        
        # Display Settings
        st.markdown("### ⚙️ Display")
        st.session_state.ug_preview_height = st.slider(
            "Preview Height",
            400, 1200, st.session_state.ug_preview_height, 50,
            key="ug_height_slider"
        )
    
    # Main Content
    st.markdown(f'<div class="ug-header">🪟 Universal Gallery</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="ug-badge">
        <div class="ug-dot"></div>
        <div style="font-weight: 900; letter-spacing: 0.10em; color: {text};">
            SUPER GLOSSY VIEWER
        </div>
        <div style="opacity: 0.75; font-weight: 800; color: {text};">
            Universal Gray • Connected Libraries
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.ug_current_entry and st.session_state.ug_current_entry.exists():
        current_path = st.session_state.ug_current_entry
        entry_name = get_entry_name(current_path)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns([1, 1, 1, 0.5])
        
        with col1:
            html_content = current_path.read_text(encoding="utf-8", errors="replace")
            st.download_button(
                label="💾 Download",
                data=html_content,
                file_name=current_path.name,
                mime="text/html",
                use_container_width=True,
                key="ug_download"
            )
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True, key="ug_refresh"):
                st.rerun()
        
        with col3:
            if st.button("📸 Screenshot", use_container_width=True, help="Use device screenshot", key="ug_screenshot"):
                st.info("💡 Use your device's screenshot tool")
        
        with col4:
            if admin_unlocked:
                if st.button("✖", help="Delete entry", key="ug_delete_btn"):
                    st.session_state.ug_confirm_delete = True
        
        # Delete confirmation
        if st.session_state.get("ug_confirm_delete"):
            st.warning(f"⚠️ Delete {entry_name}? This cannot be undone.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Confirm Delete", type="primary", use_container_width=True, key="ug_confirm_yes"):
                    if delete_entry(current_path):
                        st.session_state.ug_confirm_delete = False
                        st.session_state.ug_current_entry = None
                        st.success(f"🗑️ Deleted: {entry_name}")
                        time.sleep(0.5)
                        st.rerun()
            with c2:
                if st.button("Cancel", use_container_width=True, key="ug_confirm_no"):
                    st.session_state.ug_confirm_delete = False
                    st.rerun()
        
        st.markdown(f"### 🪟 {entry_name}")
        st.caption(f"Source: {st.session_state.ug_source.replace('_', ' ').title()}")
        
        # Preview in glossy frame
        escaped_html = html.escape(html_content)
        
        wrapper_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    background: {bg0};
                }}
                .preview-container {{
                    width: 100%;
                    height: {st.session_state.ug_preview_height}px;
                    border-radius: 16px;
                    overflow: hidden;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                    background: white;
                }}
                iframe {{ 
                    width: 100%; 
                    height: 100%; 
                    border: none;
                }}
            </style>
        </head>
        <body>
            <div class="preview-container">
                <iframe srcdoc="{escaped_html}" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>
            </div>
        </body>
        </html>
        """
        
        st.markdown('<div class="ug-preview-frame">', unsafe_allow_html=True)
        components.html(wrapper_html, height=st.session_state.ug_preview_height + 20, scrolling=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Debug panel
        with st.expander("🔍 View Source Code"):
            st.code(html_content, language="html")
    
    else:
        # Welcome screen
        st.markdown(f"""
        <div class="ug-glass-card">
            <h2 style="color: {text}; margin-bottom: 15px;">Welcome to Universal Gallery</h2>
            <p style="color: {text}; opacity: 0.8; font-size: 16px; line-height: 1.8;">
                This is a <strong>super glossy viewer</strong> for HTML content with a beautiful 
                universal gray interface.
            </p>
            
            <h3 style="color: {text}; margin-top: 25px; margin-bottom: 10px;">✨ Features:</h3>
            <ul style="color: {text}; opacity: 0.8; line-height: 2;">
                <li>🪟 Ultra-clean glassy Apple-like aesthetic</li>
                <li>🎨 7 UI tint variations (Universal Gray, Water, Fire, Fairy, Grass, Electric, Emerald)</li>
                <li>🔗 Connected to Teacher Tools library</li>
                <li>🎲 Random entry picker</li>
                <li>💾 Download entries as HTML</li>
                <li>🗑️ Delete tool (admin only)</li>
                <li>📱 Responsive design with adjustable preview height</li>
            </ul>
            
            <h3 style="color: {text}; margin-top: 25px; margin-bottom: 10px;">🔗 Connection to Teacher Tools:</h3>
            <p style="color: {text}; opacity: 0.8; font-size: 16px; line-height: 1.8;">
                This app can view HTML files from both its own Gallery folder and the Teacher Tools library! 
                Use the <strong>Source</strong> selector in the sidebar to switch between them.
            </p>
            
            <h3 style="color: {text}; margin-top: 25px; margin-bottom: 10px;">📝 How to Use:</h3>
            <ol style="color: {text}; opacity: 0.8; line-height: 2;">
                <li>Add HTML files to <code>universal_gallery/</code> folder</li>
                <li>Or create tools in Teacher Tools app</li>
                <li>Select entries from the sidebar</li>
                <li>Switch UI tints to match your content's mood</li>
                <li>Adjust preview height as needed</li>
            </ol>
            
            <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="color: {text}; opacity: 0.9; margin: 0;">
                    👈 <strong>Select an entry from the sidebar to get started!</strong>
                </p>
                <p style="color: {text}; opacity: 0.7; margin-top: 10px; margin-bottom: 0; font-size: 14px;">
                    💡 Pro tip: Change the UI Tint to match your content's theme!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Admin delete this module
    if admin_unlocked:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete Universal Gallery module", use_container_width=True, key="ug_self_delete"):
                if delete_self():
                    st.success("🗑️ Universal Gallery module deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()
