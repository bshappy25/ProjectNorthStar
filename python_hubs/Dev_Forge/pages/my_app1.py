# python_hubs/Dev_Forge/pages/my_app1.py
# ============================================================
# DevForge — Sandbox (App 1)
# Purpose:
# - Always-loads page so DevForge never crashes
# - Paste / drag-drop code into a sandbox panel
# - Validate syntax BEFORE anything runs
# - Save snippets locally so they persist between sessions
# ============================================================

from __future__ import annotations

import ast
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import streamlit as st


# -----------------------------
# Paths (kept inside repo)
# -----------------------------
SANDBOX_DIR = Path("python_hubs/Dev_Forge/devforge_media/sandbox_app1")
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
SNIPPETS_JSON = SANDBOX_DIR / "snippets.json"


# -----------------------------
# Minimal theme (does NOT override hub hard)
# -----------------------------
def soft_universal_gray_css(ticker_text: str = "DevForge • Sandbox (App 1)") -> None:
    css = """
    :root{
      --bg:#f3f4f6; --surface:#ffffff; --surface2:#f8fafc; --border:#d1d5db;
      --text:#111827; --muted:#6b7280; --accent:#2563eb;
      --radius:18px; --shadow:0 8px 24px rgba(0,0,0,0.10);
    }
    .df-card{
      background:var(--surface);
      border:1px solid var(--border);
      border-radius:var(--radius);
      padding:14px;
      box-shadow:var(--shadow);
    }
    .df-muted{ color:var(--muted); font-weight:600; }
    .df-badge{
      display:inline-flex; align-items:center; gap:8px;
      padding:6px 10px; border-radius:999px;
      border:1px solid rgba(37,99,235,0.35);
      background:rgba(37,99,235,0.08);
      font-weight:900; font-size:.85rem; white-space:nowrap;
    }
    .df-ticker{
      position:fixed; left:0; right:0; bottom:0; z-index:9999;
      text-align:center; padding:8px 20px;
      background:rgba(255,255,255,0.85);
      border-top:1px solid var(--border);
      font-size:.85rem; font-weight:900; letter-spacing:.06em;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }
    .df-ticker-spacer{ height:64px; }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='df-ticker'>{ticker_text}</div><div class='df-ticker-spacer'></div>",
        unsafe_allow_html=True,
    )


# -----------------------------
# Persistence helpers
# -----------------------------
def load_snippets() -> Dict[str, Dict[str, Any]]:
    if not SNIPPETS_JSON.exists():
        return {}
    try:
        return json.loads(SNIPPETS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_snippets(data: Dict[str, Dict[str, Any]]) -> None:
    SNIPPETS_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def safe_name(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "untitled"
    keep = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_", " "):
            keep.append(ch)
    out = "".join(keep).strip().replace(" ", "_")
    return out[:40] if out else "untitled"


# -----------------------------
# Syntax check (prevents hub crashes)
# -----------------------------
def syntax_check(code: str) -> Optional[str]:
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        # return a friendly message with line/col
        return f"{e.msg} (line {e.lineno}, col {e.offset})"


# -----------------------------
# Page
# -----------------------------
st.set_page_config(page_title="Sandbox (App 1)", layout="wide")
soft_universal_gray_css()

st.title("🧪 Sandbox (App 1)")
st.caption("Paste code here first. Validate it. Save it. Only run if you intentionally enable execution.")

# Session defaults
st.session_state.setdefault("sb_code", "")
st.session_state.setdefault("sb_name", "")
st.session_state.setdefault("sb_selected", "")

snips = load_snippets()

# Layout
left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown(
        """
        <div class="df-card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
            <div>
              <div style="font-weight:900; font-size:1.05rem;">Paste Zone</div>
              <div class="df-muted" style="margin-top:4px;">
                This page is designed to <b>never crash DevForge</b>. Use Validate before saving.
              </div>
            </div>
            <span class="df-badge">APP 1</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state["sb_name"] = st.text_input(
        "Snippet name",
        value=st.session_state["sb_name"],
        placeholder="e.g., NGSS demo seed v1",
    )

    st.session_state["sb_code"] = st.text_area(
        "Paste Python code here",
        value=st.session_state["sb_code"],
        height=420,
        placeholder="Paste code blocks here…",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Validate", use_container_width=True):
            err = syntax_check(st.session_state["sb_code"])
            if err:
                st.error(f"Syntax error: {err}")
            else:
                st.success("Syntax OK. Safe to save.")

    with c2:
        if st.button("💾 Save snippet", use_container_width=True):
            name = safe_name(st.session_state["sb_name"])
            code = st.session_state["sb_code"]
            if not code.strip():
                st.warning("Nothing to save.")
            else:
                err = syntax_check(code)
                if err:
                    st.error(f"Not saved. Fix syntax first: {err}")
                else:
                    snips[name] = {
                        "name": name,
                        "saved_at": int(time.time()),
                        "code": code,
                    }
                    save_snippets(snips)
                    st.session_state["sb_selected"] = name
                    st.success(f"Saved: {name}")

    with c3:
        if st.button("🧼 Clear", use_container_width=True):
            st.session_state["sb_code"] = ""
            st.session_state["sb_name"] = ""
            st.rerun()

    st.divider()

    # Optional execution (OFF by default)
    with st.expander("⚠️ Optional: Run inside sandbox (advanced)", expanded=False):
        st.caption("This is intentionally OFF by default. Running arbitrary code can break the page.")
        allow_run = st.toggle("Enable execution", value=False, key="sb_allow_run")
        if allow_run:
            if st.button("▶️ Run code now", type="primary", use_container_width=True):
                err = syntax_check(st.session_state["sb_code"])
                if err:
                    st.error(f"Cannot run. Syntax error: {err}")
                else:
                    # very basic sandbox: local dict; no imports blocked (you control the code)
                    scope: Dict[str, Any] = {"st": st}
                    try:
                        exec(st.session_state["sb_code"], scope, scope)
                        st.success("Executed.")
                    except Exception as e:
                        st.error(f"Runtime error: {e}")

with right:
    st.markdown(
        """
        <div class="df-card">
          <div style="font-weight:900; font-size:1.05rem;">Saved Snippets</div>
          <div class="df-muted" style="margin-top:4px;">Stored in devforge_media/sandbox_app1/snippets.json</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not snips:
        st.info("No saved snippets yet.")
    else:
        names = sorted(snips.keys())
        pick = st.selectbox("Load snippet", options=[""] + names, index=0)
        if pick:
            st.session_state["sb_selected"] = pick
            st.session_state["sb_name"] = pick
            st.session_state["sb_code"] = snips[pick]["code"]
            st.success(f"Loaded: {pick}")

        if st.session_state.get("sb_selected"):
            sel = st.session_state["sb_selected"]
            st.code(snips[sel]["code"], language="python")
            st.download_button(
                "⬇️ Download .py",
                snips[sel]["code"],
                file_name=f"{sel}.py",
                mime="text/plain",
                use_container_width=True,
            )

            if st.button("🗑️ Delete selected", use_container_width=True):
                if sel in snips:
                    del snips[sel]
                    save_snippets(snips)
                    st.session_state["sb_selected"] = ""
                    st.success("Deleted.")
                    st.rerun()
