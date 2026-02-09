# pages/home.py
"""
DevForge Home Page - Enhanced landing with real functionality
Preserves wow-factor styling while adding practical tools
"""

import streamlit as st

# Hero Section – single call, fully enabled for HTML rendering
st.markdown(
    """
    <div style="
        text-align: center;
        padding: 5rem 1.5rem 4rem;
        background: linear-gradient(135deg, var(--bg), rgba(20,184,166,0.06));
        border-radius: 0 0 2rem 2rem;
        margin: -1.5rem -2rem 3rem;
        position: relative;
        overflow: hidden;
    ">
        <h1 style="
            font-size: 4.5rem;
            margin: 0;
            letter-spacing: -0.03em;
            background: linear-gradient(90deg, var(--accent), var(--accent2));
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
# Quick Launch Section – Core functionality
# ─────────────────────────────────────────────────────────────

st.subheader("Quick Launch Core Tools")

cols = st.columns(3)

with cols[0]:
    if st.button("🔬 Ms. Piluso Science", use_container_width=True, type="primary"):
        st.switch_page("pages/Ms_Piluso_Science.py")

with cols[1]:
    if st.button("📚 Code Library", use_container_width=True, type="primary"):
        st.switch_page("pages/Code_Library.py")

with cols[2]:
    if st.button("⚡ ABC Generator", use_container_width=True, type="primary"):
        st.switch_page("pages/ABC_Generator.py")

st.markdown("<div class='hr' style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Developer Identity & Notes (persistent across pages)
# ─────────────────────────────────────────────────────────────

st.subheader("Developer Identity")

col_sig, col_clear = st.columns([4, 1])

with col_sig:
    current_sig = st.session_state.get("signature", "")
    new_sig = st.text_input(
        "Your Developer Signature / Name",
        value=current_sig,
        placeholder="e.g., Ben • Lead Developer • L.E.A.D.",
        help="This appears in the sidebar and can be used in exports.",
        key="home_signature_input"
    )
    if new_sig != current_sig:
        st.session_state["signature"] = new_sig.strip()
        st.success("Signature updated.", icon="✅")

with col_clear:
    if st.button("Clear", help="Reset signature", use_container_width=True):
        st.session_state["signature"] = ""
        st.rerun()

# ─────────────────────────────────────────────────────────────
# Quick Notes Management
# ─────────────────────────────────────────────────────────────

st.subheader("Quick Notes")

notes = st.session_state.get("notes", "")
if notes:
    lines = notes.splitlines()
    preview_lines = lines[-3:] if len(lines) > 3 else lines
    st.markdown("**Recent entries (last 3 lines):**")
    st.code("\n".join(preview_lines), language=None)
else:
    st.info("No notes yet. Use the sidebar scratch pad or add below.")

new_note = st.text_input("Add quick note", placeholder="One-line thought…", key="home_quick_note")
if st.button("Append to Notes", use_container_width=True):
    if new_note.strip():
        st.session_state["notes"] = (notes + "\n" + new_note.strip()).strip()
        st.success("Note appended.")
        st.rerun()

if notes and st.button("Clear All Notes", type="secondary"):
    st.session_state["notes"] = ""
    st.success("Notes cleared.")
    st.rerun()

st.markdown("<div class='hr' style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Theme Quick Controls (alternative to sidebar radio)
# ─────────────────────────────────────────────────────────────

st.subheader("Theme Quick Switch")

theme_cols = st.columns(3)

with theme_cols[0]:
    if st.button("Science (default)", use_container_width=True):
        st.session_state["dev_theme"] = "science"
        st.rerun()

with theme_cols[1]:
    if st.button("Neutral", use_container_width=True):
        st.session_state["dev_theme"] = "neutral"
        st.rerun()

with theme_cols[2]:
    if st.session_state.get("admin_unlocked", False):
        if st.button("Pink (admin)", use_container_width=True):
            st.session_state["dev_theme"] = "pink"
            st.rerun()
    else:
        st.button("Pink (locked)", disabled=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Status Summary Dashboard
# ─────────────────────────────────────────────────────────────

st.subheader("Current Status")

status_cols = st.columns(4)

with status_cols[0]:
    st.metric("Theme", st.session_state["dev_theme"].title())

with status_cols[1]:
    st.metric("Admin", "Unlocked" if st.session_state.get("admin_unlocked", False) else "Locked")

with status_cols[2]:
    sig = st.session_state.get("signature", "Not set")
    st.metric("Developer", sig if sig else "—")

with status_cols[3]:
    notes_count = len(st.session_state.get("notes", "").splitlines())
    st.metric("Notes Lines", notes_count)

st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)