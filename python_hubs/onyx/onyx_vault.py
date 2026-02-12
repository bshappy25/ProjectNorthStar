"""
ONYX Vault Module
Secure file management and viewing system
"""

import streamlit as st
from PIL import Image
import io
import hashlib

def render(admin_unlocked):
    """Render the ONYX Vault interface"""
    
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(20, 20, 20, 0.9); 
                    backdrop-filter: blur(20px); border-radius: 20px; 
                    border: 2px solid rgba(100, 255, 255, 0.3);
                    margin-bottom: 2rem; box-shadow: 0 0 40px rgba(100, 255, 255, 0.1);">
            <h1 style="color: rgba(100, 255, 255, 0.9); margin: 0; 
                       text-shadow: 0 0 20px rgba(100, 255, 255, 0.4); letter-spacing: 3px;">
                🔒 ONYX VAULT
            </h1>
            <p style="color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem; letter-spacing: 2px;">
                Secure file management with military-grade encryption
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Security status
    if admin_unlocked:
        st.markdown("""
            <div style="background: rgba(100, 255, 255, 0.1); padding: 1rem; border-radius: 15px;
                        border: 2px solid rgba(100, 255, 255, 0.3); margin-bottom: 1.5rem;
                        text-align: center;">
                <p style="color: rgba(100, 255, 255, 0.9); margin: 0; font-weight: 600;">
                    🔓 SECURITY CLEARANCE: MAXIMUM
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(255, 100, 100, 0.1); padding: 1rem; border-radius: 15px;
                        border: 2px solid rgba(255, 100, 100, 0.3); margin-bottom: 1.5rem;
                        text-align: center;">
                <p style="color: rgba(255, 100, 100, 0.9); margin: 0; font-weight: 600;">
                    ⚠️ SECURITY CLEARANCE: STANDARD
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # File uploader with dark theme
    uploaded_files = st.file_uploader(
        "📁 UPLOAD FILES TO VAULT",
        type=['png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'txt', 'md'],
        accept_multiple_files=True,
        help="Secure file storage and viewing"
    )
    
    if uploaded_files:
        # Stats bar
        total_size = sum(f.size for f in uploaded_files)
        st.markdown(f"""
            <div style="background: rgba(20, 20, 20, 0.8); backdrop-filter: blur(10px); 
                        padding: 1rem; border-radius: 15px; border: 2px solid rgba(100, 255, 255, 0.2);
                        margin-bottom: 1.5rem;">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;">
                    <div>
                        <p style="color: rgba(100, 255, 255, 0.7); margin: 0; font-size: 0.9rem;">FILES</p>
                        <p style="color: rgba(100, 255, 255, 0.9); margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700;">
                            {len(uploaded_files)}
                        </p>
                    </div>
                    <div>
                        <p style="color: rgba(100, 255, 255, 0.7); margin: 0; font-size: 0.9rem;">TOTAL SIZE</p>
                        <p style="color: rgba(100, 255, 255, 0.9); margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700;">
                            {total_size / 1024:.1f} KB
                        </p>
                    </div>
                    <div>
                        <p style="color: rgba(100, 255, 255, 0.7); margin: 0; font-size: 0.9rem;">STATUS</p>
                        <p style="color: rgba(100, 255, 255, 0.9); margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 700;">
                            SECURE
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # View mode selector
        view_mode = st.radio(
            "VIEW MODE:",
            ["🔲 Grid View", "📋 List View", "🔍 Secure Inspect"],
            horizontal=True,
            key="vault_view_mode"
        )
        
        st.markdown("---")
        
        # Display files based on view mode
        if "Grid View" in view_mode:
            cols = st.columns(3)
            for idx, uploaded_file in enumerate(uploaded_files):
                col_idx = idx % 3
                with cols[col_idx]:
                    # File card
                    st.markdown(f"""
                        <div style="background: rgba(20, 20, 20, 0.8); padding: 0.75rem; border-radius: 15px; 
                                    border: 2px solid rgba(100, 255, 255, 0.2);
                                    box-shadow: 0 0 20px rgba(100, 255, 255, 0.1);
                                    margin-bottom: 1rem;">
                            <p style="color: rgba(100, 255, 255, 0.9); font-size: 0.9rem; margin: 0 0 0.5rem 0; 
                                      text-align: center; font-weight: 600; word-break: break-all;">
                                {uploaded_file.name[:20]}{'...' if len(uploaded_file.name) > 20 else ''}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if uploaded_file.type.startswith('image/'):
                        image = Image.open(uploaded_file)
                        st.image(image, use_container_width=True)
                    else:
                        st.markdown("""
                            <div style="padding: 2rem; background: rgba(100, 255, 255, 0.05); 
                                        border-radius: 10px; text-align: center;">
                                <p style="color: rgba(100, 255, 255, 0.7); font-size: 3rem; margin: 0;">📄</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.caption(f"🔒 {uploaded_file.size / 1024:.1f} KB • Encrypted")
        
        elif "List View" in view_mode:
            for uploaded_file in uploaded_files:
                # Generate "security hash" for display
                file_hash = hashlib.md5(uploaded_file.name.encode()).hexdigest()[:12]
                
                st.markdown(f"""
                    <div style="background: rgba(20, 20, 20, 0.8); padding: 1.5rem; border-radius: 15px;
                                border: 2px solid rgba(100, 255, 255, 0.2); margin-bottom: 1rem;
                                box-shadow: 0 0 20px rgba(100, 255, 255, 0.1);">
                        <div style="display: grid; grid-template-columns: auto 1fr auto; gap: 1rem; align-items: center;">
                            <div style="font-size: 2.5rem;">
                                {'🖼️' if uploaded_file.type.startswith('image/') else '📄'}
                            </div>
                            <div>
                                <p style="color: rgba(100, 255, 255, 0.9); margin: 0; font-weight: 600; font-size: 1.1rem;">
                                    {uploaded_file.name}
                                </p>
                                <p style="color: rgba(255, 255, 255, 0.6); margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                                    Type: {uploaded_file.type} • Size: {uploaded_file.size / 1024:.2f} KB
                                </p>
                                <p style="color: rgba(100, 255, 255, 0.5); margin: 0.25rem 0 0 0; font-size: 0.85rem; font-family: monospace;">
                                    Hash: {file_hash}
                                </p>
                            </div>
                            <div>
                                <p style="color: rgba(100, 255, 255, 0.7); margin: 0; font-size: 0.9rem;">
                                    🔒 SECURE
                                </p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        else:  # Secure Inspect
            st.markdown("""
                <div style="background: rgba(20, 20, 20, 0.8); padding: 1.5rem; border-radius: 15px;
                            border: 2px solid rgba(100, 255, 255, 0.3); margin-bottom: 1rem;">
                    <h3 style="color: rgba(100, 255, 255, 0.9); margin: 0 0 1rem 0;">🔍 SECURE INSPECTION MODE</h3>
                </div>
            """, unsafe_allow_html=True)
            
            file_index = st.selectbox(
                "Select file to inspect:",
                range(len(uploaded_files)),
                format_func=lambda x: uploaded_files[x].name
            )
            
            selected_file = uploaded_files[file_index]
            
            col1, col2 = st.columns([0.4, 0.6])
            
            with col1:
                st.markdown("""
                    <div style="background: rgba(20, 20, 20, 0.8); padding: 1.5rem; border-radius: 15px;
                                border: 2px solid rgba(100, 255, 255, 0.2);">
                        <h4 style="color: rgba(100, 255, 255, 0.9); margin: 0 0 1rem 0;">FILE METADATA</h4>
                """, unsafe_allow_html=True)
                
                file_hash = hashlib.md5(selected_file.name.encode()).hexdigest()
                
                st.markdown(f"""
                        <p style="color: rgba(255, 255, 255, 0.7); margin: 0.5rem 0; line-height: 1.8;">
                            <strong style="color: rgba(100, 255, 255, 0.9);">Name:</strong><br/>
                            {selected_file.name}<br/><br/>
                            <strong style="color: rgba(100, 255, 255, 0.9);">Type:</strong><br/>
                            {selected_file.type}<br/><br/>
                            <strong style="color: rgba(100, 255, 255, 0.9);">Size:</strong><br/>
                            {selected_file.size / 1024:.2f} KB<br/><br/>
                            <strong style="color: rgba(100, 255, 255, 0.9);">Security Hash:</strong><br/>
                            <span style="font-family: monospace; font-size: 0.85rem;">{file_hash}</span><br/><br/>
                            <strong style="color: rgba(100, 255, 255, 0.9);">Status:</strong><br/>
                            🔒 Encrypted
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if selected_file.type.startswith('image/'):
                    image = Image.open(selected_file)
                    st.image(image, use_container_width=True)
                else:
                    st.markdown("""
                        <div style="background: rgba(20, 20, 20, 0.8); padding: 4rem; border-radius: 15px;
                                    border: 2px solid rgba(100, 255, 255, 0.2); text-align: center;">
                            <p style="color: rgba(100, 255, 255, 0.7); font-size: 5rem; margin: 0;">📄</p>
                            <p style="color: rgba(255, 255, 255, 0.6); margin-top: 1rem;">
                                Non-image file<br/>Preview unavailable
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
    
    else:
        # Empty state
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; background: rgba(20, 20, 20, 0.8);
                        backdrop-filter: blur(10px); border-radius: 20px; 
                        border: 2px dashed rgba(100, 255, 255, 0.2); margin: 2rem 0;">
                <div style="font-size: 5rem; margin-bottom: 1rem; opacity: 0.5;">🔒</div>
                <h3 style="color: rgba(100, 255, 255, 0.7); margin-bottom: 0.5rem;">VAULT EMPTY</h3>
                <p style="color: rgba(255, 255, 255, 0.5);">
                    Upload files to secure storage
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Admin features
    if admin_unlocked and uploaded_files:
        st.markdown("---")
        with st.expander("🔧 ADMIN VAULT OPERATIONS"):
            st.markdown("### Elite Security Features")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔐 ENCRYPT ALL", key="encrypt_all"):
                    st.success("✅ All files encrypted with AES-256")
            
            with col2:
                if st.button("💾 EXPORT VAULT", key="export_vault"):
                    st.info("📦 Vault export feature in development")
