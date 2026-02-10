# python_hubs/KQ_Logic/hub/app.py
# KQ Logic — READ-ONLY DB HOOK (RINGS)
# Purpose: prove DB access works without writing anything

import streamlit as st
import sqlite3
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="KQ Logic (Private)",
    page_icon="☯️",
    layout="wide",
)

# -----------------------------
# DB PATH (read-only)
# -----------------------------
HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "kq_logic.db"  # runtime-created later, ignored by git

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def get_rings() -> list[dict]:
    """
    READ-ONLY access.
    Assumes table exists later.
    Safe: returns [] if DB or table not present.
    """
    if not DB_PATH.exists():
        return []

    try:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT ring_id, name, sort_order, description
                FROM kq_rings
                ORDER BY sort_order ASC;
                """
            ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error:
        return []

# -----------------------------
# UI
# -----------------------------
st.title("☯️ KQ Logic")
st.caption("Private • Read-only DB test • Rings")

rings = get_rings()

if not rings:
    st.warning(
        "No Rings found.\n\n"
        "This is expected until the database is created at runtime.\n"
        "Read-only hook is working if this message renders cleanly."
    )
else:
    st.success("Rings loaded from local database.")
    st.dataframe(
        rings,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.markdown(
    """
**Status**
- DB file: runtime-only (ignored by git)
- Mode: read-only
- Writes: disabled
- Purpose: confirm safe access path
"""
)