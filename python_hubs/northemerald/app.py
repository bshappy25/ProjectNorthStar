"""
╔══════════════════════════════════════════════════════════════╗
║              NORTHEMERAID HUB - Python Edition               ║
║                    Navigate North • Go NE                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from pathlib import Path
import hashlib
import time

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION & SECURITY
# ═══════════════════════════════════════════════════════════════

ADMIN_CODE_HASH = hashlib.sha256("Bshapp".encode()).hexdigest()
APPS_DIR = Path("ne_apps")
APPS_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

if "palm_taps" not in st.session_state:
    st.session_state.palm_taps = 0
if "show_admin_box" not in st.session_state:
    st.session_state.show_admin_box = False
if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "current_app" not in st.session_state:
    st.session_state.current_app = None

# ═══════════════════════════════════════════════════════════════
# STYLING - EMERALD NORTHERN AESTHETIC
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        font-family: 'Orbitron', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, rgba(30, 60, 41, 0.8) 0%, rgba(45, 95, 63, 0.6) 100%);
        border-radius: 20px;
        border: 1px solid rgba(95, 179, 130, 0.3);
        box-shadow: 0 8px 32px rgba(95, 179, 130, 0.2);
        margin-bottom: 2rem;
    }
    
    .ne-logo {
        font-size: 4rem;
        color: #5fb382;
        text-shadow: 0 0 20px rgba(95, 179, 130, 0.5);
        margin-bottom: 0.5rem;
    }
    
    .ne-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #5fb382;
        letter-spacing: 4px;
        text-shadow: 0 2px 10px rgba(95, 179, 130, 0.3);
        margin-bottom: 0.5rem;
    }
    
    .ne-subtitle {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3d8b5f 0%, #5fb382 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(95, 179, 130, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(95, 179, 130, 0.5);
    }
    
    .app-card {
        background: linear-gradient(135deg, rgba(62, 139, 95, 0.2) 0%, rgba(95, 179, 130, 0.1) 100%);
        border: 1px solid rgba(95, 179, 130, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(95, 179, 130, 0.2);
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #5fb382 0%, #3d8b5f 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 10px;
        font-size: 0.75rem;
        display: inline-block;
        margin-top: 1rem;
    }
    
    .success-box {
        background: rgba(95, 179, 130, 0.2);
        border-left: 4px solid #5fb382;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(220, 53, 69, 0.2);
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(95, 179, 130, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Orbitron', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ADMIN FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def verify_admin_code(code):
    """Securely verify admin code using hash comparison"""
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    return code_hash == ADMIN_CODE_HASH

def delete_app_safely(app_name):
    """Delete app HTML file safely"""
    app_path = APPS_DIR / f"{app_name}.html"
    if app_path.exists():
        app_path.unlink()
        st.session_state.current_app = None
        return True
    return False

# ═══════════════════════════════════════════════════════════════
# HEADER WITH PALM ID
# ═══════════════════════════════════════════════════════════════

col_title, col_palm = st.columns([0.88, 0.12], vertical_alignment="center")

with col_title:
    st.markdown("""
        <div class="main-header">
            <div class="ne-logo">◆</div>
            <div class="ne-title">NORTHEMERAID</div>
            <div class="ne-subtitle">Navigate North</div>
        </div>
    """, unsafe_allow_html=True)

with col_palm:
    if st.button("🖐️", help="Palm ID (tap 3x)"):
        st.session_state.palm_taps += 1
        if st.session_state.palm_taps >= 3:
            st.session_state.show_admin_box = True

# ═══════════════════════════════════════════════════════════════
# ADMIN GATE (Palm ID Authentication)
# ═══════════════════════════════════════════════════════════════

if st.session_state.show_admin_box and not st.session_state.admin_unlocked:
    st.markdown("### 🖐️ **Palm ID:** enter admin code")
    
    code_input = st.text_input("Admin Code", type="password", placeholder="Enter code...", key="admin_code")
    
    col_unlock, col_reset = st.columns([0.6, 0.4])
    
    with col_unlock:
        if st.button("🔓 Unlock"):
            if verify_admin_code(code_input):
                st.session_state.admin_unlocked = True
                st.success("✅ Admin override unlocked.")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Incorrect code.")
    
    with col_reset:
        if st.button("🔄 Reset"):
            st.session_state.palm_taps = 0
            st.session_state.show_admin_box = False
            st.rerun()

# Admin status badge
if st.session_state.admin_unlocked:
    st.markdown('<div class="admin-badge">🖐️ Palm ID: unlocked</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# NAVIGATION
# ═══════════════════════════════════════════════════════════════

st.markdown("---")

if st.session_state.current_page != "home":
    if st.button("← Back to Hub"):
        st.session_state.current_page = "home"
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════════

if st.session_state.current_page == "home":
    st.markdown("""
        <div class="app-card">
            <h2 style="color: #5fb382; margin-bottom: 0.5rem;">🌟 Welcome to NE Hub</h2>
            <p style="color: rgba(255, 255, 255, 0.7);">
                Your gateway to northern excellence. Explore curated applications designed for peak performance.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="app-card">
                <h3 style="color: #5fb382;">◆ MyApp One</h3>
                <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">Discover features</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch MyApp One", key="app1"):
            st.session_state.current_page = "app1"
            st.session_state.current_app = "app1"
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="app-card">
                <h3 style="color: #5fb382;">◆ MyApp Two</h3>
                <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">Explore tools</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch MyApp Two", key="app2"):
            st.session_state.current_page = "app2"
            st.session_state.current_app = "app2"
            st.rerun()

# ═══════════════════════════════════════════════════════════════
# MYAPP ONE PAGE
# ═══════════════════════════════════════════════════════════════

elif st.session_state.current_page == "app1":
    st.markdown("## ◆ MyApp One")
    
    st.markdown("""
        <div class="app-card">
            <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                Experience the power of streamlined productivity. MyApp One brings you cutting-edge 
                features designed for the modern user.
            </p>
            <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8; margin-top: 1rem;">
                Built with precision and care, this application embodies the NorthEmerald philosophy 
                of excellence and simplicity.
            </p>
            
            <h4 style="color: #5fb382; margin-top: 2rem; margin-bottom: 1rem;">Key Features:</h4>
            <ul style="color: rgba(255, 255, 255, 0.7); line-height: 2;">
                <li>✨ Intuitive user interface with emerald aesthetics</li>
                <li>⚡ Lightning-fast performance optimization</li>
                <li>🔗 Seamless integration with NE ecosystem</li>
                <li>🎨 Advanced customization options</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Admin delete tool
    if st.session_state.admin_unlocked and st.session_state.current_app:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete tool"):
                if delete_app_safely(st.session_state.current_app):
                    st.success(f"🗑️ {st.session_state.current_app} deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()

# ═══════════════════════════════════════════════════════════════
# MYAPP TWO PAGE
# ═══════════════════════════════════════════════════════════════

elif st.session_state.current_page == "app2":
    st.markdown("## ◆ MyApp Two")
    
    st.markdown("""
        <div class="app-card">
            <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                Unlock new possibilities with MyApp Two. Your companion for enhanced workflow 
                and creative exploration.
            </p>
            <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8; margin-top: 1rem;">
                Crafted with attention to detail, this tool represents the pinnacle of 
                NorthEmerald innovation.
            </p>
            
            <h4 style="color: #5fb382; margin-top: 2rem; margin-bottom: 1rem;">Key Features:</h4>
            <ul style="color: rgba(255, 255, 255, 0.7); line-height: 2;">
                <li>🎭 Elegant design with northern-inspired themes</li>
                <li>🤝 Powerful collaboration features</li>
                <li>🤖 Smart automation capabilities</li>
                <li>☁️ Cloud-synced for seamless access</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Admin delete tool
    if st.session_state.admin_unlocked and st.session_state.current_app:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete tool"):
                if delete_app_safely(st.session_state.current_app):
                    st.success(f"🗑️ {st.session_state.current_app} deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(255, 255, 255, 0.4); 
                font-size: 0.85rem; letter-spacing: 2px;">
        NORTHEMERAID © 2026 • GO NORTH
    </div>
""", unsafe_allow_html=True)
