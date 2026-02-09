# pages/my_app2.py
"""
BlockForge (DEMO) — Self-contained Streamlit Code Block Inserter
Sandbox-ready: no external files, no branches, no pathways.

What it does:
- Block library (search + category filter)
- Puzzle-like sequence builder (add / reorder / remove)
- Assembled code output + download .py
- AI prompt generator + download prompt.txt
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Dict, List

import streamlit as st


# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="BlockForge (Demo)", page_icon="🧱", layout="wide")


# ─────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Block:
    id: str
    title: str
    category: str
    tags: List[str]
    description: str
    code: str


# ─────────────────────────────────────────────────────────────
# Demo library (edit freely)
# ─────────────────────────────────────────────────────────────
def demo_blocks() -> List[Block]:
    return [
        Block(
            id="page_config_wide",
            title="Page Config (Wide)",
            category="App",
            tags=["config", "layout"],
            description="Standard Streamlit page config.",
            code='st.set_page_config(page_title="DevForge Tool", page_icon="🧱", layout="wide")\n',
        ),
        Block(
            id="ss_init_basic",
            title="Session State Init (Basic)",
            category="State",
            tags=["session_state", "init"],
            description="Safe pattern: setdefault for multiple keys.",
            code=textwrap.dedent(
                """\
                for k, v in {
                    "count": 0,
                    "items": [],
                    "selected": None,
                }.items():
                    st.session_state.setdefault(k, v)
                """
            )
            + "\n",
        ),
        Block(
            id="title_caption",
            title="Title + Caption Header",
            category="UI",
            tags=["header"],
            description="Simple header scaffold.",
            code='st.title("🧱 Tool")\nst.caption("Short description of what this tool does.")\n',
        ),
        Block(
            id="two_cols_layout",
            title="Two Column Layout",
            category="UI",
            tags=["columns", "layout"],
            description="Basic two-column split.",
            code=textwrap.dedent(
                """\
                colA, colB = st.columns([1,1], gap="large")
                with colA:
                    st.subheader("Left")
                with colB:
                    st.subheader("Right")
                """
            )
            + "\n",
        ),
        Block(
            id="file_uploader_png",
            title="PNG Uploader",
            category="Input",
            tags=["upload", "png", "image"],
            description="Upload a PNG and preview it.",
            code=textwrap.dedent(
                """\
                file = st.file_uploader("Upload a PNG", type=["png"])
                if file:
                    st.image(file, caption="Uploaded PNG", use_container_width=True)
                """
            )
            + "\n",
        ),
        Block(
            id="download_text",
            title="Download Text File",
            category="Export",
            tags=["download", "export"],
            description="Download a text payload as a file.",
            code=textwrap.dedent(
                """\
                payload = "hello world"
                st.download_button(
                    "⬇️ Download text",
                    data=payload.encode("utf-8"),
                    file_name="output.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                """
            )
            + "\n",
        ),
        Block(
            id="simple_tabs",
            title="Tabs Scaffold",
            category="UI",
            tags=["tabs"],
            description="A basic tabs scaffold.",
            code=textwrap.dedent(
                """\
                tab1, tab2 = st.tabs(["One", "Two"])
                with tab1:
                    st.write("Tab one content")
                with tab2:
                    st.write("Tab two content")
                """
            )
            + "\n",
        ),
        Block(
            id="admin_gate_demo",
            title="Admin Gate (Demo)",
            category="Safety",
            tags=["admin", "gate"],
            description="Simple admin unlock pattern (demo only).",
            code=textwrap.dedent(
                """\
                ADMIN_CODE = "Bshapp"
                st.session_state.setdefault("admin_unlocked", False)

                with st.sidebar:
                    st.subheader("Admin")
                    code = st.text_input("Enter admin code", type="password")
                    if st.button("Unlock"):
                        if code == ADMIN_CODE:
                            st.session_state.admin_unlocked = True
                            st.success("Admin unlocked")
                        else:
                            st.error("Wrong code")

                if st.session_state.admin_unlocked:
                    st.info("Admin-only controls go here.")
                """
            )
            + "\n",
        ),
    ]


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def norm_text(b: Block) -> str:
    return " ".join([b.id, b.title, b.category, " ".join(b.tags), b.description]).lower()


def assemble(blocks_by_id: Dict[str, Block], seq: List[str]) -> str:
    if not seq:
        return ""
    out: List[str] = []
    for bid in seq:
        b = blocks_by_id.get(bid)
        if not b:
            continue
        out.append(f"# ── Block: {b.title} ({b.id})")
        out.append(b.code.rstrip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def build_prompt(task: str, code: str, notes: str) -> str:
    return textwrap.dedent(
        f"""\
        You are continuing a Streamlit app inside a curated tool ecosystem.

        Constraints:
        - Keep it production-safe and simple.
        - Prefer st.session_state.setdefault for state init.
        - Avoid external dependencies unless truly necessary.
        - Preserve existing structure and styling.

        Task:
        {task.strip() or "Continue the app with the next logical feature."}

        Current assembled code:
        ```python
        {code.rstrip()}
        ```

        Notes:
        {notes.strip() or "Keep changes minimal. Do not refactor unless required."}
        """
    )


# ─────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────
for k, v in {
    "bf_search": "",
    "bf_category": "All",
    "bf_seq": [],
    "bf_task": "Add the next feature safely, keeping the app simple and consistent.",
    "bf_notes": "Use setdefault patterns. Keep UI clean. Avoid new dependencies.",
}.items():
    st.session_state.setdefault(k, v)


# ─────────────────────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────────────────────
st.title("🧱 BlockForge (Demo)")
st.caption("Self-contained sandbox version. Library → Sequence → Output → Prompt/Export.")

blocks = demo_blocks()
blocks_by_id = {b.id: b for b in blocks}
categories = sorted({b.category for b in blocks})
seq: List[str] = st.session_state.bf_seq

with st.sidebar:
    st.subheader("🔎 Library Filters")
    st.text_input("Search", key="bf_search", placeholder="tabs, export, session_state...")
    st.selectbox("Category", options=["All"] + categories, key="bf_category")

    st.divider()
    st.subheader("🧩 Sequence")
    if st.button("🧹 Clear sequence", use_container_width=True):
        st.session_state.bf_seq = []
        st.rerun()

    st.divider()
    st.subheader("🧠 Prompt Builder")
    st.text_area("Task", key="bf_task", height=90)
    st.text_area("Notes", key="bf_notes", height=90)

colL, colM, colR = st.columns([1.15, 1.05, 1.35], gap="large")

# LEFT: library
with colL:
    st.subheader("📚 Block Library")
    search = st.session_state.bf_search.strip().lower()
    cat = st.session_state.bf_category

    filtered: List[Block] = []
    for b in blocks:
        if cat != "All" and b.category != cat:
            continue
        if search and search not in norm_text(b):
            continue
        filtered.append(b)

    st.caption(f"{len(filtered)} blocks shown")
    for b in filtered:
        with st.container(border=True):
            top = st.columns([0.78, 0.22])
            with top[0]:
                st.markdown(f"**{b.title}**")
                st.caption(f"{b.category} • `{b.id}`")
            with top[1]:
                if st.button("➕ Add", key=f"add_{b.id}", use_container_width=True):
                    st.session_state.bf_seq.append(b.id)
                    st.rerun()

            if b.description:
                st.write(b.description)

            with st.expander("Preview code", expanded=False):
                st.code(b.code, language="python")

# MIDDLE: sequence
with colM:
    st.subheader("🧩 Sequence")
    if not seq:
        st.info("Add blocks from the library.")
    else:
        for i, bid in enumerate(seq):
            b = blocks_by_id.get(bid)
            if not b:
                continue
            with st.container(border=True):
                hdr = st.columns([0.68, 0.32])
                with hdr[0]:
                    st.markdown(f"**{i+1}. {b.title}**")
                    st.caption(f"`{b.id}`")
                with hdr[1]:
                    u, d, x = st.columns(3)
                    with u:
                        if st.button("↑", key=f"up_{i}", use_container_width=True, disabled=(i == 0)):
                            seq[i-1], seq[i] = seq[i], seq[i-1]
                            st.session_state.bf_seq = seq
                            st.rerun()
                    with d:
                        if st.button("↓", key=f"down_{i}", use_container_width=True, disabled=(i == len(seq)-1)):
                            seq[i+1], seq[i] = seq[i], seq[i+1]
                            st.session_state.bf_seq = seq
                            st.rerun()
                    with x:
                        if st.button("✖", key=f"del_{i}", use_container_width=True):
                            seq.pop(i)
                            st.session_state.bf_seq = seq
                            st.rerun()

# RIGHT: output
with colR:
    st.subheader("📦 Output")
    code_out = assemble(blocks_by_id, seq)

    tabs = st.tabs(["Assembled Code", "AI Prompt", "Export"])
    with tabs[0]:
        st.code(code_out if code_out.strip() else "# (empty)\n", language="python")

    with tabs[1]:
        prompt = build_prompt(st.session_state.bf_task, code_out, st.session_state.bf_notes)
        st.text_area("Prompt", value=prompt, height=360)

    with tabs[2]:
        st.download_button(
            "⬇️ Download .py",
            data=(code_out or "").encode("utf-8"),
            file_name="blockforge_demo_output.py",
            mime="text/x-python",
            use_container_width=True,
            disabled=not code_out.strip(),
        )
        prompt2 = build_prompt(st.session_state.bf_task, code_out, st.session_state.bf_notes)
        st.download_button(
            "⬇️ Download prompt.txt",
            data=(prompt2 or "").encode("utf-8"),
            file_name="blockforge_demo_prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.divider()
st.caption("DEMO: No pathways / no branch packs / no file IO. We’ll add repo pathways tomorrow night.")