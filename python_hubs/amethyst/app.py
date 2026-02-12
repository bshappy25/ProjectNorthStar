"""
╔══════════════════════════════════════════════════════════════╗
║              AMETHYST HUB - Main Application                 ║
║                    Dream Purple • Go Beyond                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from pathlib import Path
import hashlib
import time

# Import MyApp modules
try:
    import teacher_tools
    import gallery_view
    import myapp3
except ImportError as e:
    st.error(f"⚠️ Error importing apps: {e}")

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION & SECURITY
# ═══════════════════════════════════════════════════════════════

ADMIN_CODE_HASH = hashlib.sha256("BENJI2026".encode()).hexdigest()

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

# ═══════════════════════════════════════════════════════════════
# STYLING - AMETHYST HAZY PURPLE AESTHETIC
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;600;700&family=Quicksand:wght@400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Add dreamy particle effect overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(240, 147, 251, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .main-header {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 40px rgba(118, 75, 162, 0.2);
        margin-bottom: 3rem;
        position: relative;
        z-index: 1;
    }
    
    .amethyst-logo {
        font-size: 5rem;
        color: rgba(240, 147, 251, 0.6);
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 20px rgba(240, 147, 251, 0.4));
    }
    
    .amethyst-title {
        font-size: 4rem;
        font-weight: 400;
        font-family: 'Comfortaa', cursive;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: 18px;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 20px rgba(255, 255, 255, 0.2);
    }
    
    .amethyst-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        font-weight: 300;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 0.85rem 2.5rem;
        font-weight: 600;
        font-family: 'Quicksand', sans-serif;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.4),
                    inset 0 0 15px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(118, 75, 162, 0.6),
                    inset 0 0 25px rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
    }
    
    .app-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.25);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(118, 75, 162, 0.2),
                    inset 0 0 20px rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .app-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .app-card:hover::before {
        opacity: 1;
    }
    
    .app-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(118, 75, 162, 0.4),
                    inset 0 0 30px rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .app-card h3 {
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(240, 147, 251, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #f093fb 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-weight: 600;
    }
    
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        font-family: 'Quicksand', sans-serif;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(240, 147, 251, 0.6);
        box-shadow: 0 0 20px rgba(240, 147, 251, 0.3);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Palm button special styling */
    div[data-testid="column"]:last-child button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        font-size: 2rem;
        width: 100%;
        padding: 0.5rem;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Welcome card special effects */
    .welcome-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(240, 147, 251, 0.15) 100%);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 255, 255, 0.35);
        border-radius: 25px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 35px rgba(118, 75, 162, 0.3),
                    inset 0 0 30px rgba(255, 255, 255, 0.1);
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

# ═══════════════════════════════════════════════════════════════
# HEADER WITH PALM ID
# ═══════════════════════════════════════════════════════════════

col_title, col_palm = st.columns([0.88, 0.12], vertical_alignment="center")

with col_title:
    st.markdown("""
        <div class="main-header">
            <div class="amethyst-logo">◈</div>
            <div class="amethyst-title">AMETHYST</div>
            <div class="amethyst-subtitle">Dream Purple • Go Beyond</div>
        </div>
    """, unsafe_allow_html=True)

with col_palm:
    if st.button("🖐️", help="Palm ID (tap 3x)", key="palm_button"):
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
        if st.button("🔓 Unlock", key="unlock_button"):
            if verify_admin_code(code_input):
                st.session_state.admin_unlocked = True
                st.success("✅ Admin override unlocked.")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Incorrect code.")
    
    with col_reset:
        if st.button("🔄 Reset", key="reset_button"):
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
    if st.button("← Back to Hub", key="back_button"):
        st.session_state.current_page = "home"
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# ROUTING TO APPS
# ═══════════════════════════════════════════════════════════════

if st.session_state.current_page == "home":
    # Teacher Tools Card
    st.markdown("""
        <div class="app-card">
            <h3>🎨 Mr. Benji's Creative Studio</h3>
            <p style="color: rgba(255, 255, 255, 0.8); font-size: 1rem; margin-top: 0.5rem;">
                Image enhancement, markup tools, collage maker, and VIP AI art studio
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Launch Creative Studio", key="creative_tools", use_container_width=True):
        st.session_state.current_page = "teacher_tools"
        st.rerun()
    
    # Two column layout for additional apps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="app-card">
                <h3>🖼️ Universal Gallery</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.95rem;">
                    Super glossy image viewer
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Gallery", key="gallery"):
            st.session_state.current_page = "gallery_view"
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="app-card">
                <h3>👑 SUPER VIP ULTRA</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.95rem;">
                    🔒 Elite platinum experience
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch SUPER VIP", key="super_vip"):
            st.session_state.current_page = "myapp3"
            st.rerun()
    
    # Coming Soon Section
    st.markdown("---")
    st.markdown("""
        <div class="app-card" style="text-align: center; background: rgba(255, 255, 255, 0.08); 
                    border: 2px dashed rgba(255, 255, 255, 0.2);">
            <h3 style="color: rgba(255, 255, 255, 0.7);">✨ New Apps Coming Soon</h3>
            <p style="color: rgba(255, 255, 255, 0.6); font-size: 1rem; margin-top: 0.5rem;">
                Stay tuned for more amazing tools and experiences
            </p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "teacher_tools":
    teacher_tools.render(st.session_state.admin_unlocked)

elif st.session_state.current_page == "gallery_view":
    gallery_view.render(st.session_state.admin_unlocked)

elif st.session_state.current_page == "myapp3":
    myapp3.render(st.session_state.admin_unlocked)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(255, 255, 255, 0.7); 
                font-size: 0.9rem; letter-spacing: 3px; font-weight: 300;">
        AMETHYST HUB © 2026 • DREAM PURPLE
    </div>
""", unsafe_allow_html=True)
