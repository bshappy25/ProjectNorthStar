# ngss_ms_research_vault_app.py
# ============================================================
# NGSS MS Research Vault (App 2)
# - SQLite-backed standards database browser
# - Search (FTS if available) + tag filters
# - Export selected rows to CSV/JSON
# - Universal Gray signature theme + "tool-only refresh"
# ============================================================

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

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
# 1) DB: condensed schema (from your v1)
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
  source_doc TEXT,
  source_page_start INTEGER,
  source_page_end INTEGER
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

CREATE INDEX IF NOT EXISTS idx_standards_pe ON standards(pe_code);
CREATE INDEX IF NOT EXISTS idx_tags_type_label ON tags(tag_type, label);
CREATE INDEX IF NOT EXISTS idx_join_tag ON standard_tags(tag_id);
CREATE INDEX IF NOT EXISTS idx_join_std ON standard_tags(standard_id);

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

    # FTS
    use_fts = bool(q.strip())
    if use_fts:
        where.append("s.id IN (SELECT rowid FROM standards_fts WHERE standards_fts MATCH ?)")
        params.append(q.strip())

    # Tags: require ALL selected tags
    if tag_ids:
        # join on standard_tags and count distinct matches
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


# -----------------------------
# 2) Tool-only Refresh (for this app)
# -----------------------------
def refresh_view(prefix: str = "vault") -> None:
    """
    Clears only this app's UI keys (filters/search/selection), not the DB.
    """
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
    ticker_text="NGSS MS Research Vault • Universal Gray • Search + Filter + Export",
    show_ticker=True,
)

st.markdown(
    """
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
        <div>
          <div style="font-weight:900; font-size:1.05rem;">NGSS MS Research Vault</div>
          <div class="muted" style="margin-top:4px;">
            App 2: browse NGSS performance expectations with tag filters + keyword search.
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

    db_path = st.text_input("DB path", value="ngss_ms.db", help="SQLite file in your repo (same folder is fine).")

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

if not db_has_data(con):
    st.warning("Database is empty. Step 3 (ingestion) will populate it from your NGSS PDF.")
    st.stop()

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
    st.caption("Tip: try codes like MS-ESS2-4 or terms like 'energy', 'forces', 'cycles'.")

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

    # Results list
    if not rows:
        st.info("No matches. Loosen tags or search term.")
    else:
        # Simple selector list
        options = [(int(r["id"]), f'{r["pe_code"]} — {r["domain_title"] or ""}'.strip(" —")) for r in rows]
        selected = st.selectbox(
            "Select a standard",
            options=options,
            format_func=lambda x: x[1],
            index=0,
        )
        st.session_state["vault_sel_standard_id"] = int(selected[0])

        # Export selection
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
                "source_doc": r["source_doc"],
                "source_page_start": r["source_page_start"],
                "source_page_end": r["source_page_end"],
            }
            for r in rows
        ]

        export_json = json.dumps(export_rows, indent=2, ensure_ascii=False)
        st.download_button("⬇️ Export results (JSON)", data=export_json, file_name="ngss_results.json", mime="application/json")

        # lightweight CSV
        # (manual to avoid pandas dependency assumptions)
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

            st.markdown("#### Performance Expectation")
            st.write(r["pe_statement"] or "—")

            if r["clarification_statement"]:
                st.markdown("#### Clarification Statement")
                st.write(r["clarification_statement"])

            if r["assessment_boundary"]:
                st.markdown("#### Assessment Boundary")
                st.write(r["assessment_boundary"])

            if r["connections"]:
                st.markdown("#### Connections")
                st.write(r["connections"])

            st.markdown("#### Tags")
            tags_rows = get_standard_tags(con, int(r["id"]))
            if not tags_rows:
                st.caption("No tags attached yet (will appear after ingestion).")
            else:
                # Grouped display
                grouped: Dict[str, List[str]] = {}
                for tr in tags_rows:
                    ttype = str(tr["tag_type"])
                    label = str(tr["label"])
                    code = tr["code"]
                    grouped.setdefault(ttype, []).append(f"{label}" + (f" ({code})" if code else ""))

                for ttype, items in grouped.items():
                    st.markdown(f"**{ttype}**")
                    st.write(" • ".join(items))

            # Provenance
            if r["source_doc"] or r["source_page_start"] is not None:
                st.markdown("#### Source")
                st.caption(
                    f'{r["source_doc"] or "unknown"} • pages {r["source_page_start"] or "?"}–{r["source_page_end"] or "?"}'
                )