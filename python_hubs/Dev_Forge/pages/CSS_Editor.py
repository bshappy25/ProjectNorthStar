# pages/CSS_Editor.py
"""
CSS Editor Page for DevForge

Allows editing of:
- Streamlit app-wide CSS overrides (stored in session_state)
- Standalone HTML + CSS documents (preview + download)

Stable version – safe for production / GitHub commit
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page header & description
# ─────────────────────────────────────────────────────────────

st.title("🎨 CSS Editor")
st.markdown(
    """
    Customize visual appearance for:
    - **DevForge itself** (Streamlit CSS overrides)
    - **Standalone HTML documents** (exportable lessons, previews, etc.)
    """
)

# ─────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────

tab_streamlit, tab_html = st.tabs(
    [
        "Streamlit CSS Overrides (App-wide)",
        "HTML + CSS Generator",
    ]
)

# ─────────────────────────────────────────────────────────────
# Tab 1: Streamlit CSS Overrides
# ─────────────────────────────────────────────────────────────

with tab_streamlit:
    st.subheader("Streamlit Application CSS")
    st.caption(
        "Changes apply immediately across the app via session state. "
        "They persist only for the current session."
    )

    current_css = st.session_state.get("custom_css", "")

    edited_css = st.text_area(
        label="Custom CSS (overrides)",
        value=current_css,
        height=320,
        placeholder=(
            "/* Example overrides */\n"
            ".stButton > button {\n"
            "    background: var(--accent) !important;\n"
            "    color: white !important;\n"
            "}\n\n"
            ".dev-card {\n"
            "    border-color: var(--accent2) !important;\n"
            "}\n"
        ),
        key="css_editor_streamlit_input",
        help=(
            "Enter valid CSS. It will be appended after base theme styles.\n"
            "Prefer :root variables (--bg, --accent, etc.).\n"
            "Avoid !important unless targeting Streamlit internals."
        ),
    )

    col_apply, col_reset, _ = st.columns([1, 1, 4])

    with col_apply:
        if st.button("Apply Changes", type="primary", use_container_width=True):
            st.session_state["custom_css"] = edited_css.strip()
            st.success("Custom CSS applied.")
            st.rerun()

    with col_reset:
        if st.button("Reset to Default", use_container_width=True):
            st.session_state.pop("custom_css", None)
            st.success("Custom CSS removed.")
            st.rerun()

    st.markdown("---")
    st.caption("Quick preview")

    st.markdown(
        """
        <div class="dev-card" style="padding: 1.5rem; border: 2px dashed #ccc;">
            <h4 style="margin-top:0;">Test Card</h4>
            <p>This block reflects your custom CSS after applying.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Tab 2: HTML + CSS Generator
# ─────────────────────────────────────────────────────────────

with tab_html:
    st.subheader("Standalone HTML Document")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("**HTML Content**")
        html_body = st.text_area(
            label="Body content (HTML)",
            height=220,
            value="<h1>Lesson Title</h1>\n<p>Your lesson text here...</p>",
            key="html_content_input",
        )

    with col_right:
        st.markdown("**CSS for this document**")
        html_css = st.text_area(
            label="Custom CSS",
            height=220,
            value=(
                "body {\n"
                "    font-family: system-ui, sans-serif;\n"
                "    max-width: 800px;\n"
                "    margin: 2rem auto;\n"
                "    padding: 0 1rem;\n"
                "    line-height: 1.6;\n"
                "}\n"
                "h1 { color: #0d6efd; }\n"
            ),
            key="html_css_input",
        )

    if st.button("Generate & Preview", type="primary"):
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Document</title>
    <style>
{html_css.strip()}
    </style>
</head>
<body>
{html_body.strip()}
</body>
</html>
"""

        st.markdown("### Preview")
        st.markdown(full_html, unsafe_allow_html=True)

        st.download_button(
            label="Download HTML file",
            data=full_html,
            file_name="custom-lesson.html",
            mime="text/html",
        )

    st.caption(
        "Tip: You can reuse styles from the left tab for consistent "
        "visual design between the app and exported documents."
    )

# ─────────────────────────────────────────────────────────────
# Bottom spacing
# ─────────────────────────────────────────────────────────────

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)