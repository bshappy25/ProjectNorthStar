"""
Teacher Tools Module - Mr. Benji's Creative Studio
Embeds HTML tools: Enhance, Markup, Collage, AI Art Studio
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

def render(admin_unlocked):
    """Render the Teacher Tools interface"""
    
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.15); 
                    backdrop-filter: blur(20px); border-radius: 20px; border: 2px solid rgba(255, 255, 255, 0.3);
                    margin-bottom: 2rem;">
            <h1 style="color: #ffffff; margin: 0; text-shadow: 0 2px 15px rgba(240, 147, 251, 0.6);">
                🎨 Mr. Benji's Creative Studio
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); margin-top: 0.5rem;">
                Professional image tools for students and creators
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tool selection
    tool_choice = st.selectbox(
        "Choose a tool:",
        ["✨ Enhance - Image Enhancement", 
         "📦 Markup - Add Boxes & Labels", 
         "🎨 Collage - Photo Collage Maker",
         "👑 AI Art Studio - VIP Only"],
        key="tool_selector"
    )
    
    st.markdown("---")
    
    # Load and display the selected HTML tool
    if "Enhance" in tool_choice:
        st.markdown("### ✨ Image Enhancer")
        st.info("💡 Upload a JPEG and adjust colors, sharpness, brightness, and contrast!")
        
        # You would embed the enhance.html file here
        # For now, placeholder
        st.warning("📄 Enhance tool will be embedded here. Place 'enhance.html' in the same directory.")
        
        # Example of how to embed:
        # html_file = Path("enhance.html")
        # if html_file.exists():
        #     with open(html_file, 'r', encoding='utf-8') as f:
        #         html_content = f.read()
        #     components.html(html_content, height=1200, scrolling=True)
    
    elif "Markup" in tool_choice:
        st.markdown("### 📦 Image Markup Tool")
        st.info("💡 Add boxes and labels to images for AI training and annotations!")
        
        st.warning("📄 Markup tool will be embedded here. Place 'markup.html' in the same directory.")
    
    elif "Collage" in tool_choice:
        st.markdown("### 🎨 Photo Collage Maker")
        st.info("💡 Combine 2-6 photos into beautiful collages with 10+ layout options!")
        
        st.warning("📄 Collage tool will be embedded here. Place 'collage.html' in the same directory.")
    
    elif "AI Art" in tool_choice:
        st.markdown("### 👑 AI Art Studio - VIP")
        
        if admin_unlocked:
            st.success("🔓 VIP Access Granted")
            st.info("💡 Generate AI art with advanced style controls and prompts!")
            
            st.warning("📄 AI Art Studio will be embedded here. Place 'ai-art-studio-vip.html' in the same directory.")
        else:
            st.error("🔒 This tool requires admin access. Use Palm ID to unlock.")
    
    # Instructions for embedding HTML files
    with st.expander("📖 How to Add Your HTML Tools"):
        st.markdown("""
        To embed your HTML tools in this Streamlit app:
        
        1. **Place your HTML files** in the same directory as this `teacher_tools.py` file:
           - `enhance.html`
           - `markup.html`
           - `collage.html`
           - `ai-art-studio-vip.html`
        
        2. **Uncomment the embedding code** in this file (see examples above)
        
        3. **Use `components.html()`** to render them:
        ```python
        html_file = Path("enhance.html")
        if html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=1200, scrolling=True)
        ```
        
        4. **Adjust height** parameter based on your tool's needs
        """)
