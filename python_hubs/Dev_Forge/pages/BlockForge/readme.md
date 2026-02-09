# BlockForge (DEMO) — Sandbox Version

This is a **self-contained demo** of BlockForge designed to run safely inside DevForge’s sandbox page (`pages/my_app2.py`).

## What this demo includes
- Block Library (search + category filter)
- Puzzle-like Sequencing (add / reorder / remove)
- Assembled code preview
- AI Prompt generation (copy/paste into external model)
- Export downloads:
  - `blockforge_demo_output.py`
  - `blockforge_demo_prompt.txt`

## What this demo intentionally does NOT include (yet)
- Repo PATHWAYS injection (coming next)
- Branch packs (A/B/C folders)
- Reading/writing `blocks.json` from disk
- Admin tools for editing blocks

## How to run
1. Paste the demo file into: `python_hubs/Dev_Forge/pages/my_app2.py`
2. Run DevForge normally:
   - `streamlit run DevForge.py`
3. Open **Sandboxes → Sandbox 2**
4. Use BlockForge (Demo) to assemble a sequence and export code/prompt.

## Next step (tomorrow)
We’ll add:
- Repo-aware PATHWAYS header injection
- Optional branch packs loader (A/B/C) from repo folders
- A sidebar toggle to enable/disable branch packs