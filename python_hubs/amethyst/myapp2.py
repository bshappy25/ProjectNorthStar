"""
Gallery View Module - Universal Image Gallery
Super glossy, modern image viewer with amethyst theme
"""

import streamlit as st
from PIL import Image
import io

def render(admin_unlocked):
    """Render the Gallery View interface"""
    
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.15); 
                    backdrop-filter: blur(20px); border-radius: 20px; border: 2px solid rgba(255, 255, 255, 0.3);
                    margin-bottom: 2rem;">
            <h1 style="color: #ffffff; margin: 0; text-shadow: 0 2px 15px rgba(240, 147, 251, 0.6);">
                🖼️ Universal Gallery
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); margin-top: 0.5rem;">
                Super glossy image viewer with style
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "📸 Upload Images",
        type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
        accept_multiple_files=True,
        help="Upload one or multiple images to view in the gallery"
    )
    
    if uploaded_files:
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); 
                        padding: 1rem; border-radius: 15px; border: 2px solid rgba(255, 255, 255, 0.25);
                        margin-bottom: 1.5rem; text-align: center;">
                <p style="color: #ffffff; margin: 0; font-size: 1.1rem;">
                    ✨ {len(uploaded_files)} image{'s' if len(uploaded_files) != 1 else ''} loaded
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Layout options
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            view_mode = st.radio(
                "View Mode:",
                ["Grid View", "Slideshow", "List View"],
                horizontal=True,
                key="view_mode"
            )
        with col2:
            if view_mode == "Grid View":
                columns = st.slider("Columns", 1, 4, 3, key="grid_columns")
        
        st.markdown("---")
        
        # Display images based on view mode
        if view_mode == "Grid View":
            # Grid layout
            cols = st.columns(columns)
            for idx, uploaded_file in enumerate(uploaded_files):
                col_idx = idx % columns
                with cols[col_idx]:
                    image = Image.open(uploaded_file)
                    
                    # Create a glossy card effect
                    st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                                    padding: 0.75rem; border-radius: 15px; 
                                    border: 2px solid rgba(255, 255, 255, 0.3);
                                    box-shadow: 0 8px 25px rgba(118, 75, 162, 0.2);
                                    margin-bottom: 1rem;">
                            <p style="color: #ffffff; font-size: 0.9rem; margin: 0 0 0.5rem 0; 
                                      text-align: center; font-weight: 600;">
                                {uploaded_file.name}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.image(image, use_container_width=True)
                    
                    # Image info
                    st.caption(f"📐 {image.size[0]} × {image.size[1]} pixels")
        
        elif view_mode == "Slideshow":
            # Slideshow with navigation
            if 'current_slide' not in st.session_state:
                st.session_state.current_slide = 0
            
            # Navigation buttons
            col_prev, col_counter, col_next = st.columns([0.3, 0.4, 0.3])
            
            with col_prev:
                if st.button("⬅️ Previous", use_container_width=True, key="prev_slide"):
                    st.session_state.current_slide = (st.session_state.current_slide - 1) % len(uploaded_files)
            
            with col_counter:
                st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.15);
                                backdrop-filter: blur(10px); border-radius: 10px; 
                                border: 2px solid rgba(255, 255, 255, 0.3);">
                        <p style="color: #ffffff; margin: 0; font-weight: 600;">
                            {st.session_state.current_slide + 1} / {len(uploaded_files)}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_next:
                if st.button("Next ➡️", use_container_width=True, key="next_slide"):
                    st.session_state.current_slide = (st.session_state.current_slide + 1) % len(uploaded_files)
            
            # Display current image
            current_file = uploaded_files[st.session_state.current_slide]
            image = Image.open(current_file)
            
            st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                            padding: 1rem; border-radius: 20px; 
                            border: 2px solid rgba(255, 255, 255, 0.3);
                            box-shadow: 0 10px 35px rgba(118, 75, 162, 0.3);
                            margin: 1.5rem 0; text-align: center;">
                    <h3 style="color: #ffffff; margin: 0 0 1rem 0;">
                        {current_file.name}
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            
            st.image(image, use_container_width=True)
            st.caption(f"📐 {image.size[0]} × {image.size[1]} pixels • 📄 {current_file.type}")
        
        else:  # List View
            for uploaded_file in uploaded_files:
                with st.container():
                    col_img, col_info = st.columns([0.3, 0.7])
                    
                    with col_img:
                        image = Image.open(uploaded_file)
                        st.image(image, use_container_width=True)
                    
                    with col_info:
                        st.markdown(f"""
                            <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
                                        padding: 1rem; border-radius: 15px; height: 100%;
                                        border: 2px solid rgba(255, 255, 255, 0.3);">
                                <h4 style="color: #ffffff; margin: 0 0 0.5rem 0;">
                                    {uploaded_file.name}
                                </h4>
                                <p style="color: rgba(255, 255, 255, 0.8); margin: 0.25rem 0;">
                                    📐 Dimensions: {image.size[0]} × {image.size[1]} pixels
                                </p>
                                <p style="color: rgba(255, 255, 255, 0.8); margin: 0.25rem 0;">
                                    📄 Type: {uploaded_file.type}
                                </p>
                                <p style="color: rgba(255, 255, 255, 0.8); margin: 0.25rem 0;">
                                    💾 Size: {uploaded_file.size / 1024:.2f} KB
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
    
    else:
        # Empty state
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px); border-radius: 20px; 
                        border: 2px dashed rgba(255, 255, 255, 0.3); margin: 2rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                <h3 style="color: #ffffff; margin-bottom: 0.5rem;">No images yet</h3>
                <p style="color: rgba(255, 255, 255, 0.8);">
                    Upload some images to get started with your gallery
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Admin features
    if admin_unlocked and uploaded_files:
        with st.expander("🔧 Admin Tools"):
            st.markdown("### Advanced Gallery Options")
            
            if st.button("💾 Download All as ZIP", key="download_zip"):
                st.info("ZIP download feature coming soon!")
            
            if st.button("🔄 Batch Convert to PNG", key="batch_convert"):
                st.info("Batch conversion feature coming soon!")
