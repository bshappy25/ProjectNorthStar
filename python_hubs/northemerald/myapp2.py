"""
╔══════════════════════════════════════════════════════════════╗
║                        MyApp Two Module                      ║
║              Creative Tools & Collaboration                  ║
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
    """Main render function for MyApp Two"""
    
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
    
    # Interactive demo section
    st.markdown("---")
    st.markdown("### 🎨 Creative Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        color_pick = st.color_picker("Choose theme color:", "#5fb382")
        st.markdown(f'<div style="background: {color_pick}; padding: 20px; border-radius: 10px; text-align: center; color: white;">Your Color</div>', unsafe_allow_html=True)
    
    with col2:
        options = st.multiselect(
            "Select tools:",
            ["Design", "Code", "Write", "Analyze"],
            default=["Design"]
        )
        if options:
            st.success(f"🛠️ Active tools: {', '.join(options)}")
    
    # Admin delete tool
    if admin_unlocked:
        st.markdown("---")
        col_delete_a, col_delete_b = st.columns([0.85, 0.15])
        with col_delete_b:
            if st.button("❌", help="Delete tool", key="delete_app2"):
                if delete_self():
                    st.success("🗑️ myapp2 deleted.")
                    time.sleep(1)
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    st.error("❌ Could not delete app.")
