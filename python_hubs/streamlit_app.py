# python_hubs/streamlit_app.py
# ============================================================
# ProjectNorthStar — Streamlit Router (STABLE FRONT DOOR)
# Works even when Streamlit "Main file path" is python_hubs/streamlit_app.py
# ============================================================

import os
import sys
import streamlit as st

# Ensure repo root is on sys.path (prevents python_hubs/python_hubs import bug)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

DEFAULT_APP = "v2"


def run_v2():
    from python_hubs.BSChapp_v2 import main
    main()


def run_v1():
    from python_hubs.hub_v1 import main
    main()


ROUTES = {
    "v1": ("BSChapp v1", run_v1),
    "v2": ("BSChapp v2", run_v2),
}


def get_route_key() -> str:
    try:
        key = st.query_params.get("app", DEFAULT_APP)
        if isinstance(key, list):
            key = key[0] if key else DEFAULT_APP
        return key or DEFAULT_APP
    except Exception:
        return DEFAULT_APP


key = get_route_key()
label, fn = ROUTES.get(key, ROUTES[DEFAULT_APP])
fn()