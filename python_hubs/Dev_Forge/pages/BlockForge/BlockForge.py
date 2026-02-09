from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

# ─────────────────────────────────────────────────────────────
# PATHWAYS (repo-aware)
# ─────────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent               # .../pages/BlockForge
PAGES_DIR = HERE.parent                              # .../pages
BRANCH_DIR = PAGES_DIR / "BlockForge_Branches"       # .../pages/BlockForge_Branches

DATA_DIR = HERE / "data"
BLOCKS_JSON = DATA_DIR / "blocks.json"
PROMPT_TEMPLATE = DATA_DIR / "prompt_template.txt"


def find_repo_root(start: Path) -> Path:
    """
    Find repo root by walking up until we see a common marker.
    Works on Streamlit Cloud + local.
    """
    markers = [".git", "pyproject.toml", "requirements.txt", "README.md"]
    cur = start.resolve()
    for _ in range(12):
        if any((cur / m).exists() for m in markers):
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # fallback
    return Path.cwd().resolve()


REPO_ROOT = find_repo_root(HERE)

# Handy repo pathways (these are what you want "in the sequence")
PATHWAYS = {
    "REPO_ROOT": REPO_ROOT,
    "PYTHON_HUBS": REPO_ROOT / "python_hubs",
    "DEV_FORGE": REPO_ROOT / "python_hubs" / "Dev_Forge",
    "PAGES_DIR": PAGES_DIR,
    "BLOCKFORGE_DIR": HERE,
    "BRANCH_DIR": BRANCH_DIR,
}

## 2) The app (`python_hubs/Dev_Forge/pages/BlockForge/BlockForge.py`)

```python
# python_hubs/Dev_Forge/pages/BlockForge/BlockForge.py
# BlockForge — Streamlit Code Block Inserter (Core App)
# Minimal deps. JSON-backed block library. Puzzle-like sequencing. Prompt builder.

from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

# ─────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
COMP_DIR = HERE / "components"

BLOCKS_JSON = DATA_DIR / "blocks.json"
PROMPT_TEMPLATE = DATA_DIR / "prompt_template.txt"

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="BlockForge", page_icon="🧱", layout="wide")

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
# Utilities (bulletproof file I/O)
# ─────────────────────────────────────────────────────────────

def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def _safe_write_text(path: Path, content: str) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False

def load_blocks() -> Tuple[List[Block], Optional[str]]:
    """Return blocks + optional error string."""
    if not BLOCKS_JSON.exists():
        return [], f"Missing blocks file: {BLOCKS_JSON.as_posix()}"

    try:
        raw = json.loads(_safe_read_text(BLOCKS_JSON) or "{}")
        blocks_raw = raw.get("blocks", [])
        blocks: List[Block] = []
        for b in blocks_raw:
            blocks.append(
                Block(
                    id=str(b.get("id", "")).strip(),
                    title=str(b.get("title", "")).strip(),
                    category=str(b.get("category", "Uncategorized")).strip(),
                    tags=list(b.get("tags", [])) if isinstance(b.get("tags", []), list) else [],
                    description=str(b.get("description", "")).strip(),
                    code=str(b.get("code", "")).rstrip() + ("\n" if str(b.get("code", "")).rstrip() else ""),
                )
            )
        # Filter out any broken entries
        blocks = [b for b in blocks if b.id and b.title and b.code]
        return blocks, None
    except Exception as e:
        return [], f"Failed to load blocks.json: {e}"

def load_prompt_template() -> str:
    tpl = _safe_read_text(PROMPT_TEMPLATE)
    if tpl.strip():
        return tpl
    # Fallback template if file missing
    return (
        "You are continuing a Streamlit app.\n\n"
        "Task:\n{TASK}\n\n"
        "Current code:\n```python\n{CODE}\n```\n\n"
        "Notes:\n{NOTES}\n"
    )

def fuzzy_match(hay: str, needle: str) -> bool:
    # Keep it simple + fast: case-insensitive contains on title/tags/category/desc
    n = needle.strip().lower()
    if not n:
        return True
    return n in hay.lower()

def normalize_block_text(b: Block) -> str:
    return " ".join([
        b.id, b.title, b.category, " ".join(b.tags), b.description
    ])

def assemble_code(blocks_by_id: Dict[str, Block], sequence: List[str]) -> str:
    chunks: List[str] = []
    for bid in sequence:
        b = blocks_by_id.get(bid)
        if not b:
            continue
        # Add a small header comment per block to help readability
        chunks.append(f"# ── Block: {b.title} ({b.id})")
        chunks.append(b.code.rstrip())
        chunks.append("")  # blank line
    return "\n".join(chunks).rstrip() + "\n" if chunks else ""

def build_prompt(template: str, task: str, code: str, notes: str) -> str:
    return template.format(
        TASK=task.strip() or "Continue the app by adding the next logical feature.",
        CODE=code.rstrip(),
        NOTES=notes.strip() or "Keep changes minimal. Preserve existing patterns."
    )

# ─────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────

for k, v in {
    "bf_sequence": [],          # list of block ids
    "bf_search": "",
    "bf_category": "All",
    "bf_selected_block": None,  # block id
    "bf_task": "Add the next feature safely, keeping the app simple and production-safe.",
    "bf_notes": "Use DevForge conventions: session_state.setdefault, minimal dependencies, clean UI.",
    "bf_custom_code": "",       # optional code edit buffer
    "bf_edit_mode": False,
}.items():
    st.session_state.setdefault(k, v)

# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────

st.title("🧱 BlockForge")
st.caption("Assemble pre-vetted Streamlit code blocks into a sequence, then copy/export or generate an AI continuation prompt.")

# ─────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────

blocks, err = load_blocks()
template = load_prompt_template()
blocks_by_id: Dict[str, Block] = {b.id: b for b in blocks}
categories = sorted({b.category for b in blocks})

if err:
    st.error(err)
    st.info("Create the file at the path above. A starter `blocks.json` is included in the instructions.")
    st.stop()

if not blocks:
    st.warning("No valid blocks found in blocks.json.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# Sidebar controls
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.subheader("🔎 Library Filters")
    st.text_input("Search", key="bf_search", placeholder="session_state, export, tabs...")

    cat_options = ["All"] + categories
    st.selectbox("Category", options=cat_options, key="bf_category")

    st.divider()
    st.subheader("🧩 Sequence Actions")

    colA, colB = st.columns(2)
    with colA:
        if st.button("Clear", use_container_width=True):
            st.session_state.bf_sequence = []
            st.session_state.bf_selected_block = None
            st.session_state.bf_edit_mode = False
            st.session_state.bf_custom_code = ""
            st.rerun()
    with colB:
        if st.button("Reload blocks.json", use_container_width=True):
            st.rerun()

    st.divider()
    st.subheader("🧠 Prompt Builder")
    st.text_area("Task", key="bf_task", height=90)
    st.text_area("Notes", key="bf_notes", height=90)

# ─────────────────────────────────────────────────────────────
# Main layout
# ─────────────────────────────────────────────────────────────

col_left, col_mid, col_right = st.columns([1.15, 1.1, 1.25], gap="large")

# ─────────────────────────────────────────────────────────────
# Left: Block Library
# ─────────────────────────────────────────────────────────────

with col_left:
    st.subheader("📚 Block Library")

    search = st.session_state.bf_search.strip()
    category = st.session_state.bf_category

    filtered: List[Block] = []
    for b in blocks:
        if category != "All" and b.category != category:
            continue
        if not fuzzy_match(normalize_block_text(b), search):
            continue
        filtered.append(b)

    st.caption(f"{len(filtered)} blocks shown")

    # list blocks with add/select
    for b in filtered:
        with st.container(border=True):
            top = st.columns([0.78, 0.22])
            with top[0]:
                st.markdown(f"**{b.title}**")
                st.caption(f"{b.category} • `{b.id}` • {', '.join(b.tags) if b.tags else 'no tags'}")
            with top[1]:
                if st.button("➕ Add", key=f"add_{b.id}", use_container_width=True):
                    st.session_state.bf_sequence.append(b.id)
                    st.session_state.bf_selected_block = b.id
                    st.session_state.bf_edit_mode = False
                    st.session_state.bf_custom_code = ""
                    st.rerun()

            if b.description:
                st.write(b.description)

            # quick preview expander
            with st.expander("Preview code", expanded=False):
                st.code(b.code, language="python")

# ─────────────────────────────────────────────────────────────
# Middle: Sequence (Puzzle)
# ─────────────────────────────────────────────────────────────

with col_mid:
    st.subheader("🧩 Sequence")

    seq: List[str] = st.session_state.bf_sequence

    if not seq:
        st.info("Add blocks from the library to build your sequence.")
    else:
        for i, bid in enumerate(seq):
            b = blocks_by_id.get(bid)
            if not b:
                continue

            with st.container(border=True):
                hdr = st.columns([0.70, 0.30])
                with hdr[0]:
                    is_sel = (st.session_state.bf_selected_block == bid)
                    st.markdown(f"**{i+1}. {b.title}**" + (" ✅" if is_sel else ""))
                    st.caption(f"`{b.id}` • {b.category}")

                with hdr[1]:
                    u, d, x = st.columns(3)
                    with u:
                        if st.button("↑", key=f"up_{i}", use_container_width=True, disabled=(i == 0)):
                            seq[i-1], seq[i] = seq[i], seq[i-1]
                            st.session_state.bf_sequence = seq
                            st.rerun()
                    with d:
                        if st.button("↓", key=f"down_{i}", use_container_width=True, disabled=(i == len(seq)-1)):
                            seq[i+1], seq[i] = seq[i], seq[i+1]
                            st.session_state.bf_sequence = seq
                            st.rerun()
                    with x:
                        if st.button("✖", key=f"del_{i}", use_container_width=True):
                            seq.pop(i)
                            st.session_state.bf_sequence = seq
                            if st.session_state.bf_selected_block == bid:
                                st.session_state.bf_selected_block = (seq[i-1] if seq else None)
                            st.session_state.bf_edit_mode = False
                            st.session_state.bf_custom_code = ""
                            st.rerun()

                # select / edit toggle
                selA, selB = st.columns([0.5, 0.5])
                with selA:
                    if st.button("Select", key=f"sel_{i}", use_container_width=True):
                        st.session_state.bf_selected_block = bid
                        st.session_state.bf_edit_mode = False
                        st.session_state.bf_custom_code = ""
                        st.rerun()
                with selB:
                    if st.button("Edit before export", key=f"edit_{i}", use_container_width=True):
                        st.session_state.bf_selected_block = bid
                        st.session_state.bf_edit_mode = True
                        st.session_state.bf_custom_code = b.code
                        st.rerun()

    st.divider()

    # Inline editor for selected block (session-only edit; does NOT overwrite JSON)
    if st.session_state.bf_selected_block and st.session_state.bf_edit_mode:
        sel = blocks_by_id.get(st.session_state.bf_selected_block)
        if sel:
            st.markdown(f"### ✏️ Edit (session-only): **{sel.title}**")
            st.caption("This edit only affects the assembled output for this session. Your blocks.json stays unchanged.")
            st.text_area("Code override", key="bf_custom_code", height=240)
            if st.button("Apply edit (session)", type="primary", use_container_width=True):
                # store a special mapping in session_state
                st.session_state.setdefault("bf_overrides", {})
                st.session_state.bf_overrides[sel.id] = st.session_state.bf_custom_code.rstrip() + "\n"
                st.success("Applied to session output.")
    elif st.session_state.bf_selected_block:
        sel = blocks_by_id.get(st.session_state.bf_selected_block)
        if sel:
            st.markdown(f"### 🎯 Selected: **{sel.title}**")
            st.code(sel.code, language="python")

# ─────────────────────────────────────────────────────────────
# Right: Output (Assembled code + Prompt)
# ─────────────────────────────────────────────────────────────

with col_right:
    st.subheader("📦 Output")

    # Apply overrides if present
    overrides = st.session_state.get("bf_overrides", {})
    effective_blocks_by_id = dict(blocks_by_id)
    if overrides:
        # Create shallow copies with overridden code
        for bid, new_code in overrides.items():
            b = effective_blocks_by_id.get(bid)
            if b:
                effective_blocks_by_id[bid] = Block(
                    id=b.id,
                    title=b.title,
                    category=b.category,
                    tags=b.tags,
                    description=b.description,
                    code=new_code,
                )

    assembled = assemble_code(effective_blocks_by_id, st.session_state.bf_sequence)
    st.caption(f"Assembled lines: {len(assembled.splitlines()) if assembled.strip() else 0}")

    tabs = st.tabs(["Assembled Code", "AI Prompt", "Export"])
    with tabs[0]:
        st.code(assembled if assembled.strip() else "# (empty)\n", language="python")
        st.download_button(
            "⬇️ Download .py",
            data=assembled.encode("utf-8"),
            file_name="blockforge_output.py",
            mime="text/x-python",
            use_container_width=True,
            disabled=not assembled.strip(),
        )

    with tabs[1]:
        prompt = build_prompt(
            template=template,
            task=st.session_state.bf_task,
            code=assembled,
            notes=st.session_state.bf_notes,
        )
        st.text_area("Prompt (copy/paste to your model)", value=prompt, height=360)
        st.download_button(
            "⬇️ Download prompt.txt",
            data=prompt.encode("utf-8"),
            file_name="blockforge_prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with tabs[2]:
        st.markdown("**Quick exports**")
        md = f"# BlockForge Sequence\n\n## Blocks\n" + "\n".join([f"- `{bid}`" for bid in st.session_state.bf_sequence]) + "\n\n## Code\n```python\n" + assembled.rstrip() + "\n```\n"
        st.download_button(
            "⬇️ Download README.md",
            data=md.encode("utf-8"),
            file_name="blockforge_sequence.md",
            mime="text/markdown",
            use_container_width=True,
            disabled=not st.session_state.bf_sequence,
        )

        # Optional: export current sequence as a preset json (not writing to blocks.json)
        preset = {
            "name": "MyPreset",
            "sequence": st.session_state.bf_sequence,
            "overrides": overrides,
        }
        st.download_button(
            "⬇️ Download preset.json",
            data=json.dumps(preset, indent=2).encode("utf-8"),
            file_name="blockforge_preset.json",
            mime="application/json",
            use_container_width=True,
            disabled=not st.session_state.bf_sequence,
        )

# ─────────────────────────────────────────────────────────────
# Footer sanity
# ─────────────────────────────────────────────────────────────

st.divider()
st.caption("BlockForge v0.1 • JSON-backed blocks • Session-only edits • Simple by design")