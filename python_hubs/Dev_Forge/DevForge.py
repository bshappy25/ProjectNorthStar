from __future__ import annotations

import streamlit as st

# ============================================================
# DEV FORGE LAUNCHER
# Routes to existing apps in priority order
# ============================================================

st.set_page_config(
    page_title="DevForge - Developer Hub",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "palm_taps" not in st.session_state:
    st.session_state["palm_taps"] = 0
if "show_admin_box" not in st.session_state:
    st.session_state["show_admin_box"] = False
if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = False

ADMIN_CODE = "Bshapp"

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #050818 100%);
    }
    .dev-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .dev-card h3 {
        color: #00d4aa;
        margin-top: 0;
    }
    .glow-hover {
        transition: all 0.3s ease;
    }
    .glow-hover:hover {
        border-color: #00d4aa;
        box-shadow: 0 0 20px rgba(0,212,170,0.3);
        transform: translateY(-2px);
    }
    .kicker {
        color: #ff6b9d;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .hr {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4aa, transparent);
        margin: 2rem 0;
    }
    [data-testid="stSidebar"] {
        background: rgba(10,14,39,0.95);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #00d4aa, #0099ff);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# PALM ID (Admin Gate)
# ============================================================

left, right = st.columns([0.88, 0.12], vertical_alignment="center")

with left:
    st.title("🔧 DevForge")

with right:
    if st.button("🤚", help="Palm ID (tap 3x)"):
        st.session_state["palm_taps"] += 1
        if st.session_state["palm_taps"] >= 3:
            st.session_state["show_admin_box"] = True

# Gate UI
if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
    st.markdown("**✨Palm ID:** enter admin code")
    code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...")
    
    colA, colB = st.columns([0.6, 0.4])
    with colA:
        if st.button("Unlock"):
            if code_try == ADMIN_CODE:
                st.session_state["admin_unlocked"] = True
                st.success("Admin override unlocked.")
                st.rerun()
            else:
                st.error("Incorrect code.")
    with colB:
        if st.button("Reset"):
            st.session_state["palm_taps"] = 0
            st.session_state["show_admin_box"] = False
            st.rerun()

if st.session_state["admin_unlocked"]:
    st.caption("🤚 Palm ID: unlocked")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## 🧭 Navigation")
    
    page = st.radio(
        "Select Page:",
        [
            "🏠 Home",
            "🔬 Ms. Piluso Science",
            "🧪 Nacli App",
            "📚 Code Library",
            "⚡ ABC Generator",
            "🎨 My App 1",
            "🎪 My App 2",
            "🧰 Teacher Tools",
        ],
        label_visibility="collapsed"
    )
    
    # Admin-gated options
    if st.session_state["admin_unlocked"]:
        st.markdown("---")
        st.markdown("### 🔒 Admin Only")
        admin_page = st.radio(
            "Admin Pages:",
            [
                "None",
                "💅 CSS Editor",
                "🔬 NGSS Research Vault",
            ],
            label_visibility="collapsed"
        )
        
        if admin_page != "None":
            page = admin_page

# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🏠 Home":
    exec(open("python_hubs/Dev_Forge/home.py").read())
    
elif page == "🔬 Ms. Piluso Science":
    exec(open("python_hubs/Dev_Forge/Ms_Piluso_Science.py").read())
    
elif page == "🧪 Nacli App":
    exec(open("python_hubs/Dev_Forge/Nacli_app.py").read())
    
elif page == "📚 Code Library":
    exec(open("python_hubs/Dev_Forge/Code_Library.py").read())
    
elif page == "⚡ ABC Generator":
    exec(open("python_hubs/Dev_Forge/ABC_Generator.py").read())
    
elif page == "🎨 My App 1":
    exec(open("python_hubs/Dev_Forge/my_app1.py").read())
    
elif page == "🎪 My App 2":
    exec(open("python_hubs/Dev_Forge/my_app2.py").read())
    
elif page == "🧰 Teacher Tools":
    exec(open("python_hubs/Dev_Forge/Teacher_Tools.py").read())
    
elif page == "💅 CSS Editor":
    exec(open("python_hubs/Dev_Forge/CSS_Editor.py").read())
    
elif page == "🔬 NGSS Research Vault":
    exec(open("python_hubs/Dev_Forge/ngss_ms_research_vault_app.py").read())
