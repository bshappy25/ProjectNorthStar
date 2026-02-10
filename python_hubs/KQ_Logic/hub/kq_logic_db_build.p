# python_hubs/KQ_Logic/hub/kq_logic_db_build.py
"""
KQ Logic DB (Private) — Extensive, expandable SQLite schema

Goals:
- Safe to run repeatedly (idempotent)
- Versioned migrations table
- "Append later" friendly: add tables + add migration rows
- Explicit indexes + foreign keys
- Clean separation of "facts" (events/entries) from "tags" and "entities"

Run:
  python python_hubs/KQ_Logic/hub/kq_logic_db_build.py

DB output:
  python_hubs/KQ_Logic/hub/kq_logic.db
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime
import json

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "kq_logic.db"


# ---------------------------
# Helpers
# ---------------------------
def utc_now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    # Foreign keys + good defaults
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (name,),
    ).fetchone()
    return row is not None


def apply_migration(conn: sqlite3.Connection, mig_id: str, label: str, sql: str) -> None:
    """
    Records applied migrations in kq_migrations.
    If migration already applied, skip.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kq_migrations(
          mig_id TEXT PRIMARY KEY,
          label TEXT NOT NULL,
          applied_at TEXT NOT NULL
        );
        """
    )
    exists = conn.execute(
        "SELECT mig_id FROM kq_migrations WHERE mig_id=?;",
        (mig_id,),
    ).fetchone()
    if exists:
        return
    conn.executescript(sql)
    conn.execute(
        "INSERT INTO kq_migrations(mig_id,label,applied_at) VALUES(?,?,?);",
        (mig_id, label, utc_now()),
    )


# ---------------------------
# Schema (Migrations)
# ---------------------------

MIGRATIONS: list[dict] = [
    {
        "id": "0001_core_entities",
        "label": "Core entities, tags, linking tables",
        "sql": """
        -- Profiles: allow multiple profiles if you ever want them
        CREATE TABLE IF NOT EXISTS kq_profiles(
          profile_id TEXT PRIMARY KEY,
          display_name TEXT NOT NULL,
          is_active INTEGER NOT NULL DEFAULT 1,
          created_at TEXT NOT NULL,
          notes TEXT DEFAULT ''
        );

        -- Generic "entities" can represent people, places, projects, apps, etc.
        CREATE TABLE IF NOT EXISTS kq_entities(
          entity_id TEXT PRIMARY KEY,
          entity_type TEXT NOT NULL,          -- e.g. person, place, project, app, concept
          label TEXT NOT NULL,
          description TEXT DEFAULT '',
          created_at TEXT NOT NULL,
          is_archived INTEGER NOT NULL DEFAULT 0
        );

        -- Tags (simple)
        CREATE TABLE IF NOT EXISTS kq_tags(
          tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
          tag TEXT NOT NULL UNIQUE
        );

        -- Link entities to tags (many-to-many)
        CREATE TABLE IF NOT EXISTS kq_entity_tags(
          entity_id TEXT NOT NULL,
          tag_id INTEGER NOT NULL,
          PRIMARY KEY(entity_id, tag_id),
          FOREIGN KEY(entity_id) REFERENCES kq_entities(entity_id) ON DELETE CASCADE,
          FOREIGN KEY(tag_id) REFERENCES kq_tags(tag_id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_entities_type ON kq_entities(entity_type);
        CREATE INDEX IF NOT EXISTS idx_entities_label ON kq_entities(label);
        """,
    },
    {
        "id": "0002_energy_and_states",
        "label": "Energy states, mode switches, state snapshots",
        "sql": """
        -- Energy states: fixed vocab but editable
        CREATE TABLE IF NOT EXISTS kq_energy_states(
          energy_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,          -- low, mid, high
          description TEXT DEFAULT ''
        );

        -- Modes: any switches you want (e.g. shield, dev, teacher, finance, etc.)
        CREATE TABLE IF NOT EXISTS kq_modes(
          mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,
          description TEXT DEFAULT ''
        );

        -- Current snapshot (append-only history)
        CREATE TABLE IF NOT EXISTS kq_state_log(
          state_id INTEGER PRIMARY KEY AUTOINCREMENT,
          profile_id TEXT NOT NULL,
          energy_id INTEGER,
          mode_id INTEGER,
          note TEXT DEFAULT '',
          created_at TEXT NOT NULL,
          FOREIGN KEY(profile_id) REFERENCES kq_profiles(profile_id) ON DELETE CASCADE,
          FOREIGN KEY(energy_id) REFERENCES kq_energy_states(energy_id),
          FOREIGN KEY(mode_id) REFERENCES kq_modes(mode_id)
        );

        CREATE INDEX IF NOT EXISTS idx_state_log_profile_time ON kq_state_log(profile_id, created_at);
        """,
    },
    {
        "id": "0003_rings_zones_milestones",
        "label": "Rings, zones, milestones, and scheduling structures",
        "sql": """
        CREATE TABLE IF NOT EXISTS kq_rings(
          ring_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,          -- e.g. day, week, month, season, year
          sort_order INTEGER NOT NULL DEFAULT 0,
          description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS kq_zones(
          zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,          -- zone 1, zone 2, etc
          sort_order INTEGER NOT NULL DEFAULT 0,
          description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS kq_milestones(
          milestone_id INTEGER PRIMARY KEY AUTOINCREMENT,
          profile_id TEXT NOT NULL,
          title TEXT NOT NULL,
          target_date TEXT,                   -- YYYY-MM-DD (optional)
          ring_id INTEGER,
          zone_id INTEGER,
          status TEXT NOT NULL DEFAULT 'planned',  -- planned|active|done|deferred
          notes TEXT DEFAULT '',
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(profile_id) REFERENCES kq_profiles(profile_id) ON DELETE CASCADE,
          FOREIGN KEY(ring_id) REFERENCES kq_rings(ring_id),
          FOREIGN KEY(zone_id) REFERENCES kq_zones(zone_id)
        );

        CREATE INDEX IF NOT EXISTS idx_milestones_profile_date ON kq_milestones(profile_id, target_date);
        CREATE INDEX IF NOT EXISTS idx_milestones_status ON kq_milestones(status);
        """,
    },
    {
        "id": "0004_logs_entries_tasks",
        "label": "Entries, tasks, and event log (core appendable content)",
        "sql": """
        -- General entries: journaling, decisions, reflections (private)
        CREATE TABLE IF NOT EXISTS kq_entries(
          entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
          profile_id TEXT NOT NULL,
          title TEXT DEFAULT '',
          body TEXT NOT NULL,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(profile_id) REFERENCES kq_profiles(profile_id) ON DELETE CASCADE
        );

        -- Tasks: lightweight (not a full PM tool)
        CREATE TABLE IF NOT EXISTS kq_tasks(
          task_id INTEGER PRIMARY KEY AUTOINCREMENT,
          profile_id TEXT NOT NULL,
          title TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'open',   -- open|doing|done|deferred
          priority INTEGER NOT NULL DEFAULT 2,   -- 1 high, 2 normal, 3 low
          due_date TEXT,                          -- YYYY-MM-DD optional
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(profile_id) REFERENCES kq_profiles(profile_id) ON DELETE CASCADE
        );

        -- Event log: generalized audit trail
        CREATE TABLE IF NOT EXISTS kq_events(
          event_id INTEGER PRIMARY KEY AUTOINCREMENT,
          profile_id TEXT NOT NULL,
          event_type TEXT NOT NULL,             -- e.g. "toggle_theme", "create_task"
          payload_json TEXT NOT NULL DEFAULT '{}',
          created_at TEXT NOT NULL,
          FOREIGN KEY(profile_id) REFERENCES kq_profiles(profile_id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_entries_profile_time ON kq_entries(profile_id, created_at);
        CREATE INDEX IF NOT EXISTS idx_tasks_profile_status ON kq_tasks(profile_id, status);
        CREATE INDEX IF NOT EXISTS idx_events_profile_time ON kq_events(profile_id, created_at);
        """,
    },
    {
        "id": "0005_symbol_palette_map",
        "label": "Symbol/color mappings (anchors)",
        "sql": """
        CREATE TABLE IF NOT EXISTS kq_symbols(
          symbol_id INTEGER PRIMARY KEY AUTOINCREMENT,
          key TEXT NOT NULL UNIQUE,             -- e.g. "yin_yang", "donut", "shield"
          emoji TEXT DEFAULT '',
          description TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS kq_palettes(
          palette_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE,
          data_json TEXT NOT NULL               -- store CSS vars or colors as JSON
        );

        -- Link symbols to palettes if desired
        CREATE TABLE IF NOT EXISTS kq_symbol_palette(
          symbol_id INTEGER NOT NULL,
          palette_id INTEGER NOT NULL,
          PRIMARY KEY(symbol_id, palette_id),
          FOREIGN KEY(symbol_id) REFERENCES kq_symbols(symbol_id) ON DELETE CASCADE,
          FOREIGN KEY(palette_id) REFERENCES kq_palettes(palette_id) ON DELETE CASCADE
        );
        """,
    },
]


# ---------------------------
# Seed (minimal, safe defaults)
# ---------------------------
def seed_defaults(conn: sqlite3.Connection) -> None:
    # Profile
    conn.execute(
        """
        INSERT OR IGNORE INTO kq_profiles(profile_id, display_name, is_active, created_at, notes)
        VALUES(?,?,?,?,?);
        """,
        ("kq-01", "KQ (Private)", 1, utc_now(), "Private operating profile"),
    )

    # Energy
    for name, desc in [
        ("low", "Low energy: minimum viable actions only"),
        ("mid", "Mid energy: grounded progress"),
        ("high", "High energy: create, but avoid refactors"),
    ]:
        conn.execute(
            "INSERT OR IGNORE INTO kq_energy_states(name, description) VALUES(?,?);",
            (name, desc),
        )

    # Modes
    for name, desc in [
        ("private", "KQ-only internal mode"),
        ("shield", "Boundaries / protect + filter mode"),
        ("dev", "Build mode (code)"),
        ("teacher", "Teacher-facing mode"),
        ("finance", "Finance clarity mode"),
    ]:
        conn.execute(
            "INSERT OR IGNORE INTO kq_modes(name, description) VALUES(?,?);",
            (name, desc),
        )

    # Rings
    for i, name in enumerate(["day", "week", "month", "season", "year"], start=1):
        conn.execute(
            "INSERT OR IGNORE INTO kq_rings(name, sort_order, description) VALUES(?,?,?);",
            (name, i, ""),
        )

    # Zones (simple scaffold)
    for i, name in enumerate(["zone_1", "zone_2", "zone_3", "zone_4"], start=1):
        conn.execute(
            "INSERT OR IGNORE INTO kq_zones(name, sort_order, description) VALUES(?,?,?);",
            (name, i, ""),
        )

    # Symbols (anchors you already use)
    for key, emoji, desc in [
        ("yin_yang", "☯️", "Balance anchor"),
        ("donut", "🍩", "Playful anchor / token vibe"),
        ("shield", "🛡️", "Boundary / protection"),
        ("sparkles", "✨", "Highlight / emphasis"),
    ]:
        conn.execute(
            "INSERT OR IGNORE INTO kq_symbols(key, emoji, description) VALUES(?,?,?);",
            (key, emoji, desc),
        )

    # Default palette: your DevForge vars (as JSON)
    default_palette = {
        "bg": "#f3f4f6",
        "card": "#ffffff",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "accent2": "#16a34a",
    }
    conn.execute(
        "INSERT OR IGNORE INTO kq_palettes(name, data_json) VALUES(?,?);",
        ("devforge_default", json.dumps(default_palette, ensure_ascii=False)),
    )

    conn.commit()


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = connect(DB_PATH)
    try:
        # Apply migrations in order
        for m in MIGRATIONS:
            apply_migration(conn, m["id"], m["label"], m["sql"])

        seed_defaults(conn)

        # Quick sanity print
        applied = conn.execute("SELECT COUNT(*) AS n FROM kq_migrations;").fetchone()["n"]
        print(f"[OK] DB ready: {DB_PATH}")
        print(f"[OK] Migrations applied: {applied}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()