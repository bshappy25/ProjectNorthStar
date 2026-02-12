"""
╔══════════════════════════════════════════════════════════════╗
║                 ONYX HUB - Main Application                  ║
║                  Embrace Dark • Rise Elite                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from pathlib import Path
import hashlib
import time

# Import MyApp modules
try:
    import onyx_tools
    import onyx_vault
    import onyx_elite
except ImportError as e:
    st.error(f"⚠️ Error importing apps: {e}")

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION & SECURITY
# ═══════════════════════════════════════════════════════════════

ADMIN_CODE_HASH = hashlib.sha256("ONYX2026".encode()).hexdigest()

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
# STYLING - ONYX DARK SLEEK AESTHETIC
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;600;700&family=Orbitron:wght@400;600;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Sleek grid overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Glowing accent lines */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(100, 255, 255, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(200, 200, 200, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .main-header {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(20, 20, 20, 0.95);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        border: 2px solid rgba(100, 255, 255, 0.2);
        box-shadow: 0 0 50px rgba(100, 255, 255, 0.1),
                    inset 0 0 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 3rem;
        position: relative;
        z-index: 1;
    }
    
    .onyx-logo {
        font-size: 5rem;
        color: rgba(100, 255, 255, 0.5);
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 30px rgba(100, 255, 255, 0.3));
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { 
            filter: drop-shadow(0 0 30px rgba(100, 255, 255, 0.3));
            transform: scale(1);
        }
        50% { 
            filter: drop-shadow(0 0 50px rgba(100, 255, 255, 0.5));
            transform: scale(1.05);
        }
    }
    
    .onyx-title {
        font-size: 4.5rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: 20px;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 30px rgba(100, 255, 255, 0.3);
        background: linear-gradient(135deg, #ffffff 0%, #64ffff 50%, #c8c8c8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .onyx-subtitle {
        color: rgba(100, 255, 255, 0.7);
        font-size: 1.1rem;
        letter-spacing: 8px;
        text-transform: uppercase;
        font-weight: 300;
        text-shadow: 0 0 10px rgba(100, 255, 255, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        color: rgba(100, 255, 255, 0.9);
        border: 2px solid rgba(100, 255, 255, 0.3);
        border-radius: 20px;
        padding: 0.85rem 2.5rem;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        transition: all 0.4s ease;
        box-shadow: 0 0 20px rgba(100, 255, 255, 0.2),
                    inset 0 0 20px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(100, 255, 255, 0.4),
                    inset 0 0 30px rgba(100, 255, 255, 0.1);
        border-color: rgba(100, 255, 255, 0.6);
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
    }
    
    .app-card {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(100, 255, 255, 0.2);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        box-shadow: 0 0 30px rgba(100, 255, 255, 0.1),
                    inset 0 0 30px rgba(0, 0, 0, 0.5);
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
        background: radial-gradient(circle, rgba(100, 255, 255, 0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .app-card:hover::before {
        opacity: 1;
    }
    
    .app-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 0 60px rgba(100, 255, 255, 0.3),
                    inset 0 0 40px rgba(100, 255, 255, 0.05);
        border-color: rgba(100, 255, 255, 0.5);
    }
    
    .app-card h3 {
        color: rgba(100, 255, 255, 0.9);
        text-shadow: 0 0 15px rgba(100, 255, 255, 0.3);
        position: relative;
        z-index: 1;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    .admin-badge {
        background: linear-gradient(135deg, rgba(100, 255, 255, 0.2) 0%, rgba(100, 255, 255, 0.1) 100%);
        color: rgba(100, 255, 255, 0.9);
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(100, 255, 255, 0.2);
        border: 1px solid rgba(100, 255, 255, 0.3);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    div[data-testid="stTextInput"] input {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(100, 255, 255, 0.3);
        border-radius: 15px;
        color: rgba(100, 255, 255, 0.9);
        font-family: 'Rajdhani', sans-serif;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(100, 255, 255, 0.4);
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(100, 255, 255, 0.6);
        box-shadow: 0 0 30px rgba(100, 255, 255, 0.2);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(100, 255, 255, 0.3) 50%, transparent 100%);
        margin: 2rem 0;
    }
    
    /* Palm button special styling */
    div[data-testid="column"]:last-child button {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(100, 255, 255, 0.3);
        font-size: 2rem;
        width: 100%;
        padding: 0.5rem;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(100, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(100, 255, 255, 0.3);
        color: rgba(100, 255, 255, 0.9);
    }
    
    .stError {
        background: rgba(255, 100, 100, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(255, 100, 100, 0.3);
        color: rgba(255, 100, 100, 0.9);
    }
    
    /* Scan line effect */
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    
    .scan-line {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(100, 255, 255, 0.3), transparent);
        animation: scan 8s linear infinite;
        pointer-events: none;
        z-index: 9999;
    }
</style>
<div class="scan-line"></div>
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
            <div class="onyx-logo">💠</div>
            <div class="onyx-title">ONYX</div>
            <div class="onyx-subtitle">Embrace Dark • Rise Elite</div>
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
    st.markdown('<div class="admin-badge">🖐️ PALM ID: UNLOCKED</div>', unsafe_allow_html=True)

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
    # Dark Tools Card
    st.markdown("""
        <div class="app-card">
            <h3>🛠️ ONYX DARK TOOLS</h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 1rem; margin-top: 0.5rem;">
                Professional dark-mode creative utilities for elite creators
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 LAUNCH DARK TOOLS", key="dark_tools", use_container_width=True):
        st.session_state.current_page = "onyx_tools"
        st.rerun()
    
    # Two column layout for additional apps
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="app-card">
                <h3>🔒 ONYX VAULT</h3>
                <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.95rem;">
                    Secure file management system
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH VAULT", key="vault"):
            st.session_state.current_page = "onyx_vault"
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="app-card">
                <h3>⚫ ELITE ACCESS</h3>
                <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.95rem;">
                    🔒 Maximum security clearance
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("LAUNCH ELITE", key="elite"):
            st.session_state.current_page = "onyx_elite"
            st.rerun()
    
    # Coming Soon Section
    st.markdown("---")
    st.markdown("""
        <div class="app-card" style="text-align: center; background: rgba(20, 20, 20, 0.5); 
                    border: 2px dashed rgba(100, 255, 255, 0.2);">
            <h3 style="color: rgba(100, 255, 255, 0.6);">⚡ NEW ONYX SYSTEMS INCOMING</h3>
            <p style="color: rgba(255, 255, 255, 0.5); font-size: 1rem; margin-top: 0.5rem;">
                Next-generation dark utilities in development
            </p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "onyx_tools":
    onyx_tools.render(st.session_state.admin_unlocked)

elif st.session_state.current_page == "onyx_vault":
    onyx_vault.render(st.session_state.admin_unlocked)

elif st.session_state.current_page == "onyx_elite":
    onyx_elite.render(st.session_state.admin_unlocked)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(100, 255, 255, 0.5); 
                font-size: 0.9rem; letter-spacing: 4px; font-weight: 300; text-transform: uppercase;">
        ONYX SYSTEMS © 2026 • EMBRACE DARK
    </div>
""", unsafe_allow_html=True)
