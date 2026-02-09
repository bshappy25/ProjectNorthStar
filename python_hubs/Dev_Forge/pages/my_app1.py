```python
# ngss_ms_research_vault_app.py
# ============================================================
# NGSS MS Research Vault (DEMO SANDBOX)
# - SQLite-backed mini database (AUTO-SEEDS 2 standards if empty)
# - Standards: MS-ESS1-1 + MS-LS1-1
# - Includes demo "activity variables" (5E ideas + materials + accom)
# - Search + Export (JSON/CSV)
# - Universal Gray signature theme + tool-only refresh
# ============================================================

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from pathlib import Path
import streamlit as st


# -----------------------------
# 0) Signature Theme Injector (condensed)
# -----------------------------
def apply_signature_theme(
    *,
    ticker_text: str | None = "NGSS MS Research Vault • Universal Gray",
    show_ticker: bool = True,
    palette: dict | None = None,
):
    base = {
        "bg": "#f3f4f6",
        "surface": "#ffffff",
        "surface2": "#f8fafc",
        "border": "#d1d5db",
        "text": "#111827",
        "muted": "#6b7280",
        "accent": "#2563eb",
        "radius": "18px",
        "pad": "14px",
        "font": "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
        "weight": "900",
        "shadow": "0 8px 24px rgba(0,0,0,0.12)",
        "ov_bg": "rgba(255,255,255,0.10)",
        "ov_border": "rgba(120,255,220,0.30)",
        "ov_blur": "12px",
        "ov_text_opacity": "0.22",
        "ov_sheen": "0.14",
        "ov_text_color": "rgba(255,255,255,0.55)",
        "ov_text_shadow": "rgba(0,0,0,0.25)",
        "ticker_bg": "rgba(255,255,255,0.08)",
        "ticker_border": "rgba(120,255,220,0.30)",
        "ticker_blur": "10px",
        "ticker_size": "0.85rem",
    }
    if palette:
        base.update(palette)

    css = f"""
    :root {{
      --bg:{base["bg"]}; --surface:{base["surface"]}; --surface2:{base["surface2"]}; --border:{base["border"]};
      --text:{base["text"]}; --muted:{base["muted"]}; --accent:{base["accent"]};
      --radius:{base["radius"]}; --pad:{base["pad"]}; --font:{base["font"]}; --font_weight:{base["weight"]};
      --shadow:{base["shadow"]};
      --ov_bg:{base["ov_bg"]}; --ov_border:{base["ov_border"]}; --ov_blur:{base["ov_blur"]};
      --ov_text_opacity:{base["ov_text_opacity"]}; --ov_sheen:{base["ov_sheen"]};
      --ov_text_color:{base["ov_text_color"]}; --ov_text_shadow:{base["ov_text_shadow"]};
      --ticker_bg:{base["ticker_bg"]}; --ticker_border:{base["ticker_border"]};
      --ticker_blur:{base["ticker_blur"]}; --ticker_size:{base["ticker_size"]};
    }}
    html, body {{ background:var(--bg); color:var(--text); font-family:var(--font); font-weight:var(--font_weight); }}
    [data-testid="stAppViewContainer"]{{ background:var(--bg); }}
    [data-testid="stHeader"]{{ background:transparent; }}
    .block-container{{ padding-top:1.1rem; padding-bottom:2.6rem; }}

    .card{{ background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:var(--pad); box-shadow:var(--shadow); }}
    .muted{{ color:var(--muted); font-weight:700; }}
    .badge{{ display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px;
            border:1px solid color-mix(in srgb, var(--accent) 35%, var(--border));
            background:color-mix(in srgb, var(--accent) 10%, var(--surface));
            font-weight:900; font-size:.85rem; white-space:nowrap; }}
    .overlay-card{{ background:var(--ov_bg); border:1px solid var(--ov_border); border-radius:var(--radius); padding:16px;
                   backdrop-filter:blur(var(--ov_blur)); -webkit-backdrop-filter:blur(var(--ov_blur));
                   position:relative; overflow:hidden; }}
    .overlay-card:before{{ content:""; position:absolute; inset:0; pointer-events:none; mix-blend-mode:screen;
                          background:linear-gradient(135deg, rgba(255,255,255,var(--ov_sheen)) 0%, rgba(255,255,255,.05) 35%, rgba(255,255,255,0) 62%); }}
    .overlay-text{{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; text-align:center; padding:14px;
                   opacity:var(--ov_text_opacity); color:var(--ov_text_color); letter-spacing:.14em; text-transform:uppercase; font-weight:900;
                   text-shadow:0 2px 10px var(--ov_text_shadow); pointer-events:none; }}

    .ticker{{ position:fixed; left:0; right:0; bottom:0; z-index:9999; text-align:center; padding:8px 20px;
             background:var(--ticker_bg); border-top:1px solid var(--ticker_border); font-size:var(--ticker_size);
             font-weight:900; letter-spacing:.06em; backdrop-filter:blur(var(--ticker_blur)); -webkit-backdrop-filter:blur(var(--ticker_blur)); }}
    .ticker-spacer{{ height:64px; }}
    """.strip()

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    if show_ticker and ticker_text:
        st.markdown(f"<div class='ticker'>{ticker_text}</div><div class='ticker-spacer'></div>", unsafe_allow_html=True)


# -----------------------------
# 1) DB: schema (adds demo_activities)
# -----------------------------
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS standards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pe_code TEXT NOT NULL UNIQUE,
  grade_band TEXT NOT NULL DEFAULT 'MS',
  topic_area TEXT,
  domain_code TEXT,
  domain_title TEXT,
  pe_statement TEXT,
  clarification_statement TEXT,
  assessment_boundary TEXT,
  connections TEXT,
  source_url TEXT
);

CREATE TABLE IF NOT EXISTS tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_type TEXT NOT NULL,
  code TEXT,
  label TEXT NOT NULL,
  UNIQUE(tag_type, label),
  UNIQUE(tag_type, code)
);

CREATE TABLE IF NOT EXISTS standard_tags (
  standard_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  excerpt TEXT,
  PRIMARY KEY (standard_id, tag_id),
  FOREIGN KEY (standard_id) REFERENCES standards(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Demo activities (variables) for sandbox use
CREATE TABLE IF NOT EXISTS demo_activities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  standard_id INTEGER NOT NULL,
  phase TEXT NOT NULL,                 -- Engage/Explore/Explain/Elaborate/Evaluate
  activity_title TEXT NOT NULL,
  activity_text TEXT NOT NULL,
  materials TEXT,
  accommodations TEXT,
  sentence_starters TEXT,
  links TEXT,
  FOREIGN KEY (standard_id) REFERENCES standards(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_standards_pe ON standards(pe_code);
CREATE INDEX IF NOT EXISTS idx_tags_type_label ON tags(tag_type, label);
CREATE INDEX IF NOT EXISTS idx_join_tag ON standard_tags(tag_id);
CREATE INDEX IF NOT EXISTS idx_join_std ON standard_tags(standard_id);
CREATE INDEX IF NOT EXISTS idx_demo_std ON demo_activities(standard_id);
CREATE INDEX IF NOT EXISTS idx_demo_phase ON demo_activities(phase);

-- Optional FTS (if FTS5 exists)
CREATE VIRTUAL TABLE IF NOT EXISTS standards_fts
USING fts5(
  pe_code,
  domain_title,
  pe_statement,
  clarification_statement,
  assessment_boundary,
  connections,
  content='standards',
  content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS standards_ai AFTER INSERT ON standards BEGIN
  INSERT INTO standards_fts(rowid, pe_code, domain_title, pe_statement, clarification_statement, assessment_boundary, connections)
  VALUES (new.id, new.pe_code, new.domain_title, new.pe_statement, new.clarification_statement, new.assessment_boundary, new.connections);
END;

CREATE TRIGGER IF NOT EXISTS standards_au AFTER UPDATE ON standards BEGIN
  UPDATE standards_fts SET
    pe_code=new.pe_code,
    domain_title=new.domain_title,
    pe_statement=new.pe_statement,
    clarification_statement=new.clarification_statement,
    assessment_boundary=new.assessment_boundary,
    connections=new.connections
  WHERE rowid=new.id;
END;

CREATE TRIGGER IF NOT EXISTS standards_ad AFTER DELETE ON standards BEGIN
  DELETE FROM standards_fts WHERE rowid=old.id;
END;
"""


def db_connect(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def db_init(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA_SQL)
    con.commit()


def db_has_data(con: sqlite3.Connection) -> bool:
    cur = con.execute("SELECT COUNT(*) AS n FROM standards;")
    return int(cur.fetchone()["n"]) > 0


def _upsert_tag(con: sqlite3.Connection, tag_type: str, code: str | None, label: str) -> int:
    con.execute(
        "INSERT OR IGNORE INTO tags(tag_type, code, label) VALUES (?,?,?)",
        (tag_type, code, label),
    )
    r = con.execute("SELECT id FROM tags WHERE tag_type=? AND label=?", (tag_type, label)).fetchone()
    return int(r["id"])


def _attach_tag(con: sqlite3.Connection, pe_code: str, tag_id: int, excerpt: str | None = None) -> None:
    sid_row = con.execute("SELECT id FROM standards WHERE pe_code=?", (pe_code,)).fetchone()
    if not sid_row:
        return
    con.execute(
        "INSERT OR IGNORE INTO standard_tags(standard_id, tag_id, excerpt) VALUES (?,?,?)",
        (int(sid_row["id"]), int(tag_id), excerpt),
    )


def _insert_demo_activity(
    con: sqlite3.Connection,
    pe_code: str,
    phase: str,
    title: str,
    text: str,
    materials: str = "",
    accommodations: str = "",
    sentence_starters: str = "",
    links: str = "",
) -> None:
    sid_row = con.execute("SELECT id FROM standards WHERE pe_code=?", (pe_code,)).fetchone()
    if not sid_row:
        return
    con.execute(
        """
        INSERT INTO demo_activities(standard_id, phase, activity_title, activity_text, materials, accommodations, sentence_starters, links)
        VALUES (?,?,?,?,?,?,?,?)
        """,
        (int(sid_row["id"]), phase, title, text, materials, accommodations, sentence_starters, links),
    )


def db_seed_demo_if_empty(con: sqlite3.Connection) -> bool:
    """
    Seeds 2 standards + demo activities (5E) if DB is empty.
    Returns True if seeded.
    """
    if db_has_data(con):
        return False

    # --- Standards (from NGSS pages)
    # MS-LS1-1 PE statement + clarification (no assessment boundary shown on page)
    con.execute(
        """
        INSERT INTO standards(pe_code, grade_band, topic_area, domain_code, domain_title,
                              pe_statement, clarification_statement, assessment_boundary, connections, source_url)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "MS-LS1-1",
            "MS",
            "Life Science",
            "MS-LS1",
            "From Molecules to Organisms: Structures and Processes",
            "Conduct an investigation to provide evidence that living things are made of cells; either one cell or many different numbers and types of cells.",
            "Emphasis is on developing evidence that living things are made of cells, distinguishing between living and non-living things, and understanding that living things may be made of one cell or many and varied cells.",
            None,
            "Connections to engineering/technology and CCSS are available on the NGSS page.",
            "https://www.nextgenscience.org/pe/ms-ls1-1-molecules-organisms-structures-and-processes",
        ),
    )

    # MS-ESS1-1 PE statement + clarification (no assessment boundary shown on page)
    con.execute(
        """
        INSERT INTO standards(pe_code, grade_band, topic_area, domain_code, domain_title,
                              pe_statement, clarification_statement, assessment_boundary, connections, source_url)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "MS-ESS1-1",
            "MS",
            "Earth & Space Science",
            "MS-ESS1",
            "Earth's Place in the Universe",
            "Develop and use a model of the Earth-sun-moon system to describe the cyclic patterns of lunar phases, eclipses of the sun and moon, and seasons.",
            "Examples of models can be physical, graphical, or conceptual.",
            None,
            "Connections to other DCIs and CCSS are available on the NGSS page.",
            "https://www.nextgenscience.org/pe/ms-ess1-1-earths-place-universe",
        ),
    )

    # --- Minimal tags (nice for demo filtering)
    # SEP
    sep_models = _upsert_tag(con, "SEP", "SEP-MODEL", "Developing and Using Models")
    sep_invest = _upsert_tag(con, "SEP", "SEP-INV", "Planning and Carrying Out Investigations")
    # CCC
    ccc_patterns = _upsert_tag(con, "CCC", "CCC-PAT", "Patterns")
    ccc_scale = _upsert_tag(con, "CCC", "CCC-SCALE", "Scale, Proportion, and Quantity")
    # DCI (broad)
    dci_ls1a = _upsert_tag(con, "DCI", "LS1.A", "LS1.A: Structure and Function")
    dci_ess1b = _upsert_tag(con, "DCI", "ESS1.B", "ESS1.B: Earth and the Solar System")

    _attach_tag(con, "MS-LS1-1", sep_invest)
    _attach_tag(con, "MS-LS1-1", ccc_scale)
    _attach_tag(con, "MS-LS1-1", dci_ls1a)

    _attach_tag(con, "MS-ESS1-1", sep_models)
    _attach_tag(con, "MS-ESS1-1", ccc_patterns)
    _attach_tag(con, "MS-ESS1-1", dci_ess1b)

    # --- Demo activities (variables) — lightweight, editable in-app
    # MS-LS1-1
    _insert_demo_activity(
        con,
        "MS-LS1-1",
        "Engage",
        "Living vs Nonliving: Evidence Wall",
        "Show 6 images (e.g., plant, rock, mushroom, flame, bacteria, robot). Students sort: living / nonliving and write ONE piece of evidence for each choice. Class builds an “evidence wall.”",
        materials="Image set (slides/print), sticky notes, marker, optional magnifiers.",
        accommodations="Provide 2-choice cards (living/nonliving). Allow oral responses. Use sentence starters.",
        sentence_starters="I think it is living because ____. / My evidence is ____. / I noticed ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-LS1-1",
        "Explore",
        "Microscope / Model Cell Hunt",
        "Stations: (A) microscope slides (onion, cheek, pond water) OR photos; (B) LEGO/bead ‘cell’ models. Students collect 3 observations per station to support the claim that living things are made of cells.",
        materials="Slides/images, microscopes or photo cards, station sheets.",
        accommodations="Pre-labeled diagrams, paired reading, reduced station count (2).",
        sentence_starters="At station __ I observed ____. / This supports the claim because ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-LS1-1",
        "Explain",
        "CER Mini-Write: Cells are the Unit of Life",
        "Students write a short CER: Claim = living things are made of cells; Evidence = station data; Reasoning = connect evidence to the definition of cell as smallest unit of life.",
        materials="CER template, exemplar, word bank (cell, organism, unicellular, multicellular).",
        accommodations="Fill-in-the-blank CER, speech-to-text, allow bullet points.",
        sentence_starters="Claim: ____. Evidence: ____. Reasoning: ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-LS1-1",
        "Elaborate",
        "Unicellular vs Multicellular Case Cards",
        "Give organism cards (amoeba, yeast, human, oak tree). Students categorize and explain how cell number/type supports the category. Extend: why specialization matters.",
        materials="Case cards, T-chart, optional short readings.",
        accommodations="Color-coded cards, fewer cases, partner talk.",
        sentence_starters="____ is (uni/multi)cellular because ____. / One advantage is ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-LS1-1",
        "Evaluate",
        "Exit Ticket: Evidence Snapshot",
        "Prompt: “Write one piece of evidence that something is made of cells and one question you still have.” Optional: quick 4-question check.",
        materials="Exit ticket slips or Google Form.",
        accommodations="Multiple choice option, allow drawing + label.",
        sentence_starters="My evidence is ____. / I still wonder ____.",
        links="",
    )

    # MS-ESS1-1
    _insert_demo_activity(
        con,
        "MS-ESS1-1",
        "Engage",
        "Moon Mystery: What’s Changing?",
        "Show a 10–15 sec montage of moon photos across a month. Students predict: what changes, what stays the same, and what could cause the pattern.",
        materials="Moon photo set, projector.",
        accommodations="Provide 3-word choices: shape/position/brightness. Allow pointing.",
        sentence_starters="I notice ____. / The pattern might be caused by ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-ESS1-1",
        "Explore",
        "Lamp + Ball Model Lab",
        "Groups model Sun (lamp), Earth (ball), Moon (ping pong). Students generate the sequence of phases and capture 4 ‘data’ sketches (positions) to explain phases and eclipses.",
        materials="Lamp, balls, ping-pong, darkened room, lab sheet.",
        accommodations="Provide labeled diagram frames. Assign roles (holder/recorder).",
        sentence_starters="When the Moon is here, we see ____. / This happens because ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-ESS1-1",
        "Explain",
        "Model-to-Claim: Phases, Eclipses, Seasons",
        "Students use their model data to write 3 claims: (1) phases pattern, (2) eclipse condition, (3) seasons cause (tilt + sunlight intensity), each with a diagram.",
        materials="Claim/diagram template, vocab bank (orbit, rotation, tilt, axis).",
        accommodations="Provide sentence frames and diagram stickers/arrows.",
        sentence_starters="My claim is ____. / My model shows ____. / Therefore ____.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-ESS1-1",
        "Elaborate",
        "Predict the Sky: Calendar Challenge",
        "Given a date and a ‘new moon’ reference, students predict approximate phase and justify using cycle length. Extend: connect to tides or cultural calendars.",
        materials="Calendar, reference phase chart.",
        accommodations="Use phase wheel, allow approximate answers.",
        sentence_starters="I predict ____ because ____. / The cycle repeats about every ____ days.",
        links="",
    )
    _insert_demo_activity(
        con,
        "MS-ESS1-1",
        "Evaluate",
        "Two-Tier Check",
        "Tier 1: choose the correct phase/eclipses diagram. Tier 2: explain why the chosen model matches the phenomenon.",
        materials="2-tier quiz (paper/form).",
        accommodations="Read-aloud, reduced items, picture choices.",
        sentence_starters="I chose __ because in the diagram ____.",
        links="",
    )

    con.commit()
    return True


def list_tags(con: sqlite3.Connection, tag_type: str) -> List[Tuple[int, str]]:
    cur = con.execute(
        "SELECT id, label FROM tags WHERE tag_type=? ORDER BY label COLLATE NOCASE;",
        (tag_type,),
    )
    return [(int(r["id"]), str(r["label"])) for r in cur.fetchall()]


def query_standards(
    con: sqlite3.Connection,
    *,
    q: str,
    tag_ids: List[int],
    limit: int = 50,
) -> List[sqlite3.Row]:
    """
    - If q is provided, prefer FTS MATCH
    - If tag_ids is provided, require standards that have ALL selected tags
    """
    params: List[Any] = []
    where: List[str] = []

    use_fts = bool(q.strip())
    if use_fts:
        where.append("s.id IN (SELECT rowid FROM standards_fts WHERE standards_fts MATCH ?)")
        params.append(q.strip())

    if tag_ids:
        placeholders = ",".join(["?"] * len(tag_ids))
        where.append(
            f"""s.id IN (
                SELECT st.standard_id
                FROM standard_tags st
                WHERE st.tag_id IN ({placeholders})
                GROUP BY st.standard_id
                HAVING COUNT(DISTINCT st.tag_id) = ?
            )"""
        )
        params.extend(tag_ids)
        params.append(len(tag_ids))

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = f"""
    SELECT s.*
    FROM standards s
    {where_sql}
    ORDER BY s.pe_code ASC
    LIMIT ?;
    """
    params.append(int(limit))
    cur = con.execute(sql, params)
    return cur.fetchall()


def get_standard_tags(con: sqlite3.Connection, standard_id: int) -> List[sqlite3.Row]:
    cur = con.execute(
        """
        SELECT t.tag_type, t.code, t.label, st.excerpt
        FROM standard_tags st
        JOIN tags t ON t.id = st.tag_id
        WHERE st.standard_id=?
        ORDER BY t.tag_type, t.label COLLATE NOCASE;
        """,
        (standard_id,),
    )
    return cur.fetchall()


def get_demo_activities(con: sqlite3.Connection, standard_id: int) -> List[sqlite3.Row]:
    cur = con.execute(
        """
        SELECT phase, activity_title, activity_text, materials, accommodations, sentence_starters, links
        FROM demo_activities
        WHERE standard_id=?
        ORDER BY CASE phase
          WHEN 'Engage' THEN 1
          WHEN 'Explore' THEN 2
          WHEN 'Explain' THEN 3
          WHEN 'Elaborate' THEN 4
          WHEN 'Evaluate' THEN 5
          ELSE 99 END, activity_title COLLATE NOCASE;
        """,
        (standard_id,),
    )
    return cur.fetchall()


# -----------------------------
# 2) Tool-only Refresh (for this app)
# -----------------------------
def refresh_view(prefix: str = "vault") -> None:
    wipe = [
        f"{prefix}_q",
        f"{prefix}_limit",
        f"{prefix}_sel_standard_id",
        f"{prefix}_sel_sep",
        f"{prefix}_sel_dci",
        f"{prefix}_sel_ccc",
        f"{prefix}_sel_conn",
        f"{prefix}_sel_ela",
        f"{prefix}_sel_math",
        f"{prefix}_phase_pick",
    ]
    for k in wipe:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state[f"{prefix}_nonce"] = st.session_state.get(f"{prefix}_nonce", 0) + 1


# -----------------------------
# 3) App
# -----------------------------
st.set_page_config(page_title="NGSS MS Research Vault", layout="wide")
apply_signature_theme(
    ticker_text="NGSS MS Research Vault • DEMO (2 Standards) • Search + Filter + Export",
    show_ticker=True,
)

st.markdown(
    """
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
        <div>
          <div style="font-weight:900; font-size:1.05rem;">NGSS MS Research Vault (Sandbox Demo)</div>
          <div class="muted" style="margin-top:4px;">
            Demo DB auto-seeds MS-ESS1-1 + MS-LS1-1 with simple 5E activity variables for a quick Piluso walkthrough.
          </div>
        </div>
        <span class="badge">APP 2</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar controls
with st.sidebar:
    st.title("Vault Controls")

    # Put DB next to this file by default (more reliable than CWD)
    DEFAULT_DB = str(Path(__file__).with_name("ngss_ms_demo.db"))
    db_path = st.text_input("DB path", value=DEFAULT_DB, help="SQLite file path. Default is next to this app file.")

    colA, colB = st.columns([0.6, 0.4])
    with colA:
        if st.button("🔄 Refresh view", help="Reset filters/search (keeps DB)"):
            refresh_view(prefix="vault")
            st.rerun()
    with colB:
        limit = st.number_input("Limit", min_value=10, max_value=500, value=50, step=10, key="vault_limit")

    st.caption("Search uses FTS when available. Tag filters require ALL selected tags (AND).")

# Connect + init
con = db_connect(db_path)
db_init(con)

seeded = db_seed_demo_if_empty(con)
if seeded:
    st.success("Seeded demo database with 2 standards + 5E activity variables.")

# Load tags
seps = list_tags(con, "SEP")
dcis = list_tags(con, "DCI")
cccs = list_tags(con, "CCC")
conns = list_tags(con, "CONNECTION")
elas = list_tags(con, "ELA")
maths = list_tags(con, "MATH")

# Main layout
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("Search + Filter")

    q = st.text_input("Keyword search (FTS)", value=st.session_state.get("vault_q", ""), key="vault_q")
    st.caption("Tip: try MS-ESS1-1 or MS-LS1-1, or search 'cells' / 'moon' / 'seasons'.")

    # Tag filters (multi-select by label)
    sel_sep = st.multiselect("SEPs", options=seps, format_func=lambda x: x[1], key="vault_sel_sep")
    sel_dci = st.multiselect("DCIs", options=dcis, format_func=lambda x: x[1], key="vault_sel_dci")
    sel_ccc = st.multiselect("CCCs", options=cccs, format_func=lambda x: x[1], key="vault_sel_ccc")

    with st.expander("More filters"):
        sel_conn = st.multiselect("Connections", options=conns, format_func=lambda x: x[1], key="vault_sel_conn")
        sel_ela = st.multiselect("ELA", options=elas, format_func=lambda x: x[1], key="vault_sel_ela")
        sel_math = st.multiselect("Math", options=maths, format_func=lambda x: x[1], key="vault_sel_math")

    tag_ids: List[int] = []
    for group in (sel_sep, sel_dci, sel_ccc, sel_conn, sel_ela, sel_math):
        tag_ids.extend([int(t[0]) for t in group])

    rows = query_standards(con, q=q, tag_ids=tag_ids, limit=int(limit))

    st.markdown(
        f"<div class='overlay-card'><div class='overlay-text'>RESEARCH</div>"
        f"<div style='font-weight:900;'>Results</div>"
        f"<div class='muted' style='margin-top:4px;'>{len(rows)} match(es)</div></div>",
        unsafe_allow_html=True,
    )

    if not rows:
        st.info("No matches. Clear tags or search term.")
    else:
        options = [(int(r["id"]), f'{r["pe_code"]} — {r["domain_title"] or ""}'.strip(" —")) for r in rows]
        selected = st.selectbox(
            "Select a standard",
            options=options,
            format_func=lambda x: x[1],
            index=0,
        )
        st.session_state["vault_sel_standard_id"] = int(selected[0])

        # Export selection (rows list)
        export_rows = [
            {
                "pe_code": r["pe_code"],
                "domain_code": r["domain_code"],
                "domain_title": r["domain_title"],
                "topic_area": r["topic_area"],
                "pe_statement": r["pe_statement"],
                "clarification_statement": r["clarification_statement"],
                "assessment_boundary": r["assessment_boundary"],
                "connections": r["connections"],
                "source_url": r["source_url"],
            }
            for r in rows
        ]

        export_json = json.dumps(export_rows, indent=2, ensure_ascii=False)
        st.download_button("⬇️ Export results (JSON)", data=export_json, file_name="ngss_results.json", mime="application/json")

        if export_rows:
            headers = list(export_rows[0].keys())
            csv_lines = [",".join(headers)]
            for rr in export_rows:
                row = []
                for h in headers:
                    val = "" if rr[h] is None else str(rr[h]).replace('"', '""')
                    row.append(f'"{val}"')
                csv_lines.append(",".join(row))
            st.download_button("⬇️ Export results (CSV)", data="\n".join(csv_lines), file_name="ngss_results.csv", mime="text/csv")


with right:
    st.subheader("Details")

    sid = int(st.session_state.get("vault_sel_standard_id", 0))
    if sid <= 0:
        st.info("Select a standard on the left.")
    else:
        r = con.execute("SELECT * FROM standards WHERE id=?", (sid,)).fetchone()
        if not r:
            st.error("Selected item not found.")
        else:
            st.markdown(
                f"""
                <div class="card">
                  <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
                    <div style="font-weight:900; font-size:1.05rem;">{r["pe_code"]}</div>
                    <span class="badge">{(r["domain_code"] or "NGSS")}</span>
                  </div>
                  <div class="muted" style="margin-top:6px;">
                    {(r["domain_title"] or "")} • {(r["topic_area"] or "MS")}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            tabs = st.tabs(["Standard", "5E Demo Variables", "Tags"])

            with tabs[0]:
                st.markdown("#### Performance Expectation")
                st.write(r["pe_statement"] or "—")

                if r["clarification_statement"]:
                    st.markdown("#### Clarification Statement")
                    st.write(r["clarification_statement"])

                if r["assessment_boundary"]:
                    st.markdown("#### Assessment Boundary")
                    st.write(r["assessment_boundary"])
                else:
                    st.caption("Assessment boundary: (not provided in this demo seed)")

                if r["connections"]:
                    st.markdown("#### Connections (demo)")
                    st.write(r["connections"])

                if r["source_url"]:
                    st.markdown("#### Source")
                    st.link_button("Open NGSS page", r["source_url"])

            with tabs[1]:
                st.markdown("#### 5E activity variables (demo)")
                st.caption("Pick a phase → copy/paste ideas into Ms. Piluso Science or a lesson doc.")

                acts = get_demo_activities(con, int(r["id"]))
                if not acts:
                    st.info("No demo activities for this standard.")
                else:
                    phases = ["Engage", "Explore", "Explain", "Elaborate", "Evaluate"]
                    phase_pick = st.radio("Phase", phases, horizontal=True, key="vault_phase_pick")

                    phase_acts = [a for a in acts if str(a["phase"]) == phase_pick]
                    if not phase_acts:
                        st.info("No items for this phase.")
                    else:
                        for a in phase_acts:
                            with st.expander(f"{a['phase']} • {a['activity_title']}", expanded=True):
                                st.write(a["activity_text"])

                                if a["sentence_starters"]:
                                    st.markdown("**Sentence starters**")
                                    st.code(a["sentence_starters"], language=None)

                                colm, cola = st.columns(2)
                                with colm:
                                    st.markdown("**Materials**")
                                    st.write(a["materials"] or "—")
                                with cola:
                                    st.markdown("**Accommodations**")
                                    st.write(a["accommodations"] or "—")

                                # quick copy block
                                copy_block = (
                                    f"{a['phase']} — {a['activity_title']}\n\n"
                                    f"{a['activity_text']}\n\n"
                                    f"Sentence starters: {a['sentence_starters'] or '—'}\n"
                                    f"Materials: {a['materials'] or '—'}\n"
                                    f"Accommodations: {a['accommodations'] or '—'}\n"
                                )
                                st.text_area("Copy block", value=copy_block, height=180)

            with tabs[2]:
                st.markdown("#### Tags")
                tags_rows = get_standard_tags(con, int(r["id"]))
                if not tags_rows:
                    st.caption("No tags attached yet (demo is minimal).")
                else:
                    grouped: Dict[str, List[str]] = {}
                    for tr in tags_rows:
                        ttype = str(tr["tag_type"])
                        label = str(tr["label"])
                        code = tr["code"]
                        grouped.setdefault(ttype, []).append(f"{label}" + (f" ({code})" if code else ""))

                    for ttype, items in grouped.items():
                        st.markdown(f"**{ttype}**")
                        st.write(" • ".join(items))

st.divider()
st.markdown(
    """
**Demo scope (for Piluso walkthrough):**
- Only **2** NGSS standards are seeded.
- Each standard has **5E activity variables** you can copy/paste.
- Later, we’ll swap seeding → real ingestion pipeline + full database build.
"""
)
```
