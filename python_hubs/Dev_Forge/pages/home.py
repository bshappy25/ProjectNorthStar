# pages/home.py
"""
DevForge Home Page - Enhanced landing with visual impact
Stable version suitable for direct GitHub commit
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Hero Section - Immersive entry point
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 5rem 1.5rem 4rem;
        background: linear-gradient(135deg, 
            var(--bg), 
            rgba(20,184,166,0.06)
        );
        border-radius: 0 0 2rem 2rem;
        margin: -1.5rem -2rem 3rem;
        position: relative;
        overflow: hidden;
    ">
        <h1 style="
            font-size: 4.5rem;
            margin: 0;
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, 
                var(--accent), 
                var(--accent2)
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.05;
        ">
            🔧 DevForge
        </h1>
        
        <p style="
            font-size: 1.6rem;
            margin: 1.25rem 0 2.5rem;
            opacity: 0.92;
            font-weight: 400;
            letter-spacing: 0.02em;
        " class="kicker">
            Your Personal Streamlit Development Forge
        </p>
        
        <div style="
            animation: pulse 4.5s infinite ease-in-out;
            display: inline-block;
        ">
            <span style="
                font-size: 1.25rem;
                padding: 0.75rem 2rem;
                border-radius: 3rem;
            " class="badge badge-accent">
                We are L.E.A.D.
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# Feature Showcase - Staggered animated cards
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0 4rem;
    }
    .feature-card {
        animation: fadeInUp 1.1s ease-out forwards;
        opacity: 0;
    }
    .feature-card:nth-child(1) { animation-delay: 0.2s; }
    .feature-card:nth-child(2) { animation-delay: 0.45s; }
    .feature-card:nth-child(3) { animation-delay: 0.7s; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

# Card 1
st.markdown(
    """
    <div class="dev-card feature-card glow-hover">
        <h3>🔬 Science Tools</h3>
        <p>NGSS-aligned lesson planning<br>New Visions integration<br>5E framework + accommodations</p>
        <div style="margin-top: 1.25rem;">
            <span class="badge badge-accent">Production Ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Card 2
st.markdown(
    """
    <div class="dev-card feature-card glow-hover">
        <h3>📚 Code Library</h3>
        <p>Glassy UI components<br>Export patterns (PDF/Image)<br>Session state & layout utilities</p>
        <div style="margin-top: 1.25rem;">
            <span class="badge badge-accent">Reusable Patterns</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Card 3
st.markdown(
    """
    <div class="dev-card feature-card glow-hover">
        <h3>⚡ ABC Generator</h3>
        <p>Architecture decisions<br>Build pattern selection<br>Code style + visual direction</p>
        <div style="margin-top: 1.25rem;">
            <span class="badge badge-accent">Decision Accelerator</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Call to Action - Prominent & pulsing
# ─────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="dev-card" style="
        text-align: center;
        background: linear-gradient(135deg, 
            rgba(20,184,166,0.15), 
            rgba(47,91,234,0.12)
        );
        animation: pulse 6s infinite ease-in-out;
        padding: 3rem 1.5rem;
        margin: 3rem 0 4rem;
    ">
        <h3 style="font-size: 2.8rem; margin-bottom: 1.25rem;">
            Ready to Forge?
        </h3>
        <p style="font-size: 1.25rem; margin: 0 0 2rem; max-width: 640px; margin-left: auto; margin-right: auto;">
            Launch tools from the sidebar.<br>
            Prototype safely in sandboxes.<br>
            Scale confidently to production.
        </p>
        <div style="margin-top: 1.5rem;">
            <span class="badge badge-accent">NGSS Tools</span>
            <span class="badge badge-accent2">UI Components</span>
            <span class="badge badge-accent">Architecture Support</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# Quick Reference & Status (collapsed by default)
# ─────────────────────────────────────────────────────────────

with st.expander("📋 Common Workflows", expanded=False):
    st.markdown("""
    **Create new science lesson**  
    → Open **Ms. Piluso Science** → select standard → build 5E → export SCI-BLOCK

    **Reuse UI patterns**  
    → Open **Code Library** → copy component → paste into your app

    **Make architecture decision**  
    → Open **ABC Generator** → answer A/B/C/S → use recommended starter

    **Experiment safely**  
    → Use **Sandbox 1** or **Sandbox 2** → move stable pieces to core apps
    """)

with st.expander("🧩 Current Session State", expanded=False):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f"""
            <div class="dev-card">
                <h4>Active Configuration</h4>
                <p><strong>Theme:</strong> {st.session_state.get('dev_theme', 'science').title()}</p>
                <p><strong>Admin:</strong> {'Unlocked' if st.session_state.get('admin_unlocked', False) else 'Locked'}</p>
                <p><strong>Developer:</strong> {st.session_state.get('signature', 'Not set')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="dev-card">
                <h4>Quick Notes Preview</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.text_area(
            "Notes (read-only preview)",
            value=st.session_state.get("notes", ""),
            height=140,
            disabled=True,
            label_visibility="collapsed"
        )

# Bottom spacing to prevent overlap with fixed ticker
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)