"""
╔══════════════════════════════════════════════════════════════╗
║                        MyApp One Module                      ║
║              Productivity & Feature Discovery                ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import time

def delete_self():
    """Delete this app module (admin only)"""
    from pathlib import Path
    app_path = Path(__file__)
    if app_path.exists():
        app_path.unlink()
        return True
    return False

def render(admin_unlocked=False):
    """Main render function for MyApp One"""
    
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
    
    # Interactive demo section
    st.markdown("---")
    st.markdown("### 🚀 Quick Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        user_input = st.text_input("Enter something:", placeholder="Type here...")
        if user_input:
            st.success(f"✅ You entered: {user_input}")
    
    with col2:
        slider_val = st.slider("Adjust setting:", 0, 100, 50)
        st.info(f"📊 Current value: {slider_val}")
    
    # Admin delete tool
    if admin_unlocked:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete tool", key="delete_app1"):
                if delete_self():
                    st.success("🗑️ myapp1 deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    st.error("❌ Could not delete app.")
