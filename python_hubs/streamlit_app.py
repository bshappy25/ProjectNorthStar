# python_hubs/streamlit_app.py
# ============================================================
# ProjectNorthStar — Streamlit Router (STABLE FRONT DOOR)
# Fixes python_hubs/python_hubs import issues on Streamlit Cloud
# ============================================================

import os
import sys
import streamlit as st

THIS_DIR = os.path.abspath(os.path.dirname(__file__))               # .../projectnorthstar/python_hubs
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))          # .../projectnorthstar

# Remove python_hubs directory from sys.path if present (prevents python_hubs/python_hubs)
sys.path = [p for p in sys.path if os.path.abspath(p) != THIS_DIR]

# Ensure repo root is first on sys.path
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
_, fn = ROUTES.get(key, ROUTES[DEFAULT_APP])
fn()