from __future__ import annotations

import streamlit as st

# ============================================================
# DEVFORGE HOME (ROUTED PAGE)
# - No st.set_page_config here
# - No sidebar here
# - Uses global CSS from app.py
# ============================================================

st.title("🔧 DevForge - Developer Hub")
st.markdown("### Your Streamlit Development Assistant")

st.markdown(
    """
<div class='dev-card animate-fade'>
<div class='kicker'>SYSTEM OVERVIEW</div>
<h3>🎯 Quick Start</h3>
<p>DevForge helps you build Streamlit apps faster with:</p>
<ul>
<li><strong>Ms. Piluso Science Page</strong> — NGSS + New Visions curriculum tools + exports</li>
<li><strong>Code Library</strong> — Copy/paste UI components and patterns</li>
<li><strong>ABC Generator</strong> — Make architecture decisions quickly</li>
<li><strong>my_app1 / my_app2</strong> — sandbox pages for experiments</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# FEATURE GRID
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
<div class='dev-card glow-hover'>
<h3>🔬 Science Tools</h3>
<p>NGSS-aligned lesson planning</p>
<p>New Visions integration</p>
<p>5E framework builder + accommodations</p>
<br>
<p><strong>→ Open “Ms. Piluso Science”</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class='dev-card glow-hover'>
<h3>📚 Code Library</h3>
<p>Glassy UI components</p>
<p>Export patterns + UI recipes</p>
<p>Session state patterns</p>
<br>
<p><strong>→ Open “Code Library”</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
<div class='dev-card glow-hover'>
<h3>⚡ ABC Framework</h3>
<p><strong>A</strong> — Architecture</p>
<p><strong>B</strong> — Build pattern</p>
<p><strong>C</strong> — Code style</p>
<p><strong>S</strong> — Style selection</p>
<br>
<p><strong>→ Open “ABC Generator”</strong></p>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# PRIMARY VS TESTER
# ============================================================

st.markdown("## 🧭 Primary Apps vs Tester Apps")

st.markdown(
    """
<div class='dev-card'>
<h3>Primary Apps</h3>
<ul>
  <li><strong>Ms_Piluso_Science</strong> — production lesson builder</li>
  <li><strong>Code_Library</strong> — canonical snippets (copy/paste)</li>
  <li><strong>ABC_Generator</strong> — build decisions + starter structures</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='dev-card'>
<h3>Tester Apps</h3>
<p class='muted'>Use these to experiment without risking your core pages.</p>
<ul>
  <li><strong>my_app1</strong> — small UI blocks / forms</li>
  <li><strong>my_app2</strong> — export experiments, widgets, layouts</li>
</ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# QUICK REFERENCE
# ============================================================

st.markdown("## 🚀 Quick Reference")

with st.expander("📋 Common Tasks", expanded=False):
    st.markdown(
        """
**Create new science lesson**
1) Open **Ms. Piluso Science**
2) Select NGSS standard
3) Fill 5E + Materials + Notes + Accommodations
4) Export / copy preview

**Use sandbox**
1) Open **Sandbox 1** or **Sandbox 2**
2) Paste a UI block or feature idea
3) Once stable, move it into a primary page

**Make architecture decision**
1) Open **ABC Generator**
2) Answer A, B, C, S
3) Use the recommended structure + starter code
"""
    )

with st.expander("🔒 PALM ID Notes", expanded=False):
    st.markdown(
        """
**PALM ID gate**
- Tap 🤚 three times
- Enter admin code
- Unlock reveals:
  - **Pink** theme option
  - Admin tools (reset notes / lock gate)
"""
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ============================================================
# STATE SUMMARY
# ============================================================

st.markdown("## 🧩 Current State")

cA, cB = st.columns([0.55, 0.45])

with cA:
    st.markdown(
        """
<div class='dev-card'>
<h3>System Status</h3>
<p><span class='badge badge-accent'>Theme</span> <strong>{theme}</strong></p>
<p><span class='badge badge-accent2'>Signature</span> <strong>{sig}</strong></p>
<p><span class='badge'>Admin</span> <strong>{admin}</strong></p>
</div>
""".format(
            theme=st.session_state.get("dev_theme", "science"),
            sig=(st.session_state.get("signature") or "Not set"),
            admin=("Unlocked" if st.session_state.get("admin_unlocked") else "Locked"),
        ),
        unsafe_allow_html=True,
    )

with cB:
    st.markdown(
        """
<div class='dev-card'>
<h3>Developer Notes</h3>
<p class='muted'>These are stored in session_state (temporary).</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.text_area(
        "Notes Preview",
        value=st.session_state.get("notes", ""),
        height=155,
        disabled=True,
        label_visibility="collapsed",
    )

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
