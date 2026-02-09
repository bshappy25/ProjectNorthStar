# pages/my_app2.py
# BlockForge Sandbox – UI + Puzzle Component Inserter
# 1:1 replacement version – ready to commit and run

import streamlit as st

st.set_page_config(page_title="BlockForge Sandbox", layout="wide")

# ─────────────────────────────────────────────────────────────
# Preloaded blocks (fake / example blocks for testing)
# Expand or replace these with your real patterns later
# ─────────────────────────────────────────────────────────────

BLOCKS = {
    "Safe Session Init": {
        "category": "Session State",
        "code": """def ss_init(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default

# Example usage:
ss_init("counter", 0)
ss_init("theme", "science")""",
        "short_desc": "Safe initialization pattern used in every app"
    },

    "Theme-aware Card": {
        "category": "UI Components",
        "code": """st.markdown(
    f'''
    <div class="dev-card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    ''',
    unsafe_allow_html=True
)""",
        "short_desc": "Standard glassmorphic card with dynamic title/content"
    },

    "Download Button – CSV": {
        "category": "Export",
        "code": """import io
import pandas as pd

csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download CSV",
    data=csv_buffer.getvalue(),
    file_name="data.csv",
    mime="text/csv"
)""",
        "short_desc": "Common CSV export pattern"
    },

    "Wide Dataframe + Conditional Format": {
        "category": "Data Display",
        "code": """st.dataframe(
    df.style.format(precision=2)
             .highlight_max(color='#d4f4dd')
             .highlight_min(color='#f8d7da'),
    use_container_width=True
)""",
        "short_desc": "Styled wide dataframe"
    },

    "File Uploader + Preview": {
        "category": "Input",
        "code": """uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "png", "jpg"])
if uploaded_file:
    st.image(uploaded_file)  # or pd.read_csv(uploaded_file) etc.
    st.success("File uploaded successfully")""",
        "short_desc": "Basic uploader with immediate preview"
    },

    "Metric Delta Row": {
        "category": "UI Components",
        "code": """cols = st.columns(3)
with cols[0]:
    st.metric("Users", 1245, delta=89)
with cols[1]:
    st.metric("Conversion", "18.2%", delta=-1.4, delta_color="inverse")
with cols[2]:
    st.metric("Revenue", "$42.3k", delta=3200)""",
        "short_desc": "Three-column KPI dashboard row"
    }
}

# ─────────────────────────────────────────────────────────────
# Sidebar – Filters
# ─────────────────────────────────────────────────────────────

st.sidebar.title("BlockForge")

category = st.sidebar.selectbox(
    "Category",
    options=["All"] + sorted(set(b["category"] for b in BLOCKS.values()))
)

search_term = st.sidebar.text_input("Search blocks", "")

# ─────────────────────────────────────────────────────────────
# Main layout – three columns
# ─────────────────────────────────────────────────────────────

left, center, right = st.columns([1.2, 2.8, 1.3])

# ─────────────────────────────────────────────────────────────
# Left column – Block browser
# ─────────────────────────────────────────────────────────────

with left:
    st.subheader("Blocks")

    filtered = [
        title for title, data in BLOCKS.items()
        if (category == "All" or data["category"] == category)
        and (not search_term or search_term.lower() in title.lower() or search_term.lower() in data["short_desc"].lower())
    ]

    if not filtered:
        st.info("No blocks match current filters.")
    else:
        for title in filtered:
            data = BLOCKS[title]
            with st.expander(title):
                st.caption(data["short_desc"])
                st.code(data["code"], language="python")

                if st.button("Add to Sequence", key=f"add_{title}", use_container_width=True):
                    if "puzzle_sequence" not in st.session_state:
                        st.session_state.puzzle_sequence = []
                    st.session_state.puzzle_sequence.append(title)
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# Center column – Puzzle / Sequence builder
# ─────────────────────────────────────────────────────────────

with center:
    st.subheader("Current Sequence")

    if "puzzle_sequence" not in st.session_state:
        st.session_state.puzzle_sequence = []

    sequence = st.session_state.puzzle_sequence

    if not sequence:
        st.info("Add blocks from the left panel to build your sequence.")
    else:
        for i, title in enumerate(sequence):
            data = BLOCKS[title]

            c1, c2, c3, c4 = st.columns([5, 1, 1, 1])

            with c1:
                st.markdown(f"**{i+1}. {title}**")
                st.caption(data["short_desc"])
                st.code(data["code"], language="python")

            with c2:
                if st.button("↑", key=f"up_{i}", disabled=i == 0):
                    sequence[i-1], sequence[i] = sequence[i], sequence[i-1]
                    st.rerun()

            with c3:
                if st.button("↓", key=f"down_{i}", disabled=i == len(sequence)-1):
                    sequence[i+1], sequence[i] = sequence[i], sequence[i+1]
                    st.rerun()

            with c4:
                if st.button("×", key=f"remove_{i}"):
                    del sequence[i]
                    st.rerun()

            st.markdown("↓")

        c_clear, c_copy = st.columns(2)
        with c_clear:
            if st.button("Clear Sequence", type="secondary", use_container_width=True):
                st.session_state.puzzle_sequence = []
                st.rerun()

        with c_copy:
            if st.button("Copy Full Sequence", type="primary", use_container_width=True):
                full_code = "\n\n".join(BLOCKS[t]["code"] for t in sequence)
                st.session_state["clipboard_buffer"] = full_code
                st.success("Sequence copied to buffer below")

# ─────────────────────────────────────────────────────────────
# Right column – Prompt + Clipboard
# ─────────────────────────────────────────────────────────────

with right:
    st.subheader("Next Step Prompt")

    if st.button("Generate Continuation Prompt", use_container_width=True):
        if sequence:
            last_title = sequence[-1]
            last_code = BLOCKS[last_title]["code"]

            prompt_text = f"""You are extending my Streamlit app in the DevForge ecosystem.

My conventions:
- Use ss_init(key, default) for session state
- Theme variables: --bg, --card, --accent, --accent2, etc.
- Glassmorphic cards: backdrop-filter blur(10px), border-radius 14px
- Prefer wide layout when useful
- Primary buttons often have type="primary" + custom styling

Latest block added:
```python
{last_code}