# python_hubs/KQ_Logic/hub/kq_db.py
# KQ Logic — DB module (read-only)
# Purpose: centralize DB path + safe reads. No writes.

import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "kq_logic.db"  # runtime only (ignored by git)

def conn() -> sqlite3.Connection:
    c = sqlite3.connect(str(DB_PATH))
    c.row_factory = sqlite3.Row
    return c

def table_exists(name: str) -> bool:
    if not DB_PATH.exists():
        return False
    try:
        with conn() as c:
            r = c.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
                (name,),
            ).fetchone()
        return r is not None
    except sqlite3.Error:
        return False

def get_rings() -> list[dict]:
    """
    Read-only.
    Returns [] if DB/table missing.
    """
    if not table_exists("kq_rings"):
        return []
    try:
        with conn() as c:
            rows = c.execute(
                """
                SELECT ring_id, name, sort_order, description
                FROM kq_rings
                ORDER BY sort_order ASC;
                """
            ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error:
        return []