# python_hubs/streamlit_app.py
# ============================================================
# ProjectNorthStar — Streamlit Router (STABLE FRONT DOOR)
# - Works with Streamlit main file path = python_hubs/streamlit_app.py
# - Routes by query param:
#     default -> v2
#     ?app=v1 -> v1
#     ?app=v2 -> v2
# - Loads modules by file path (no package/import drama)
# ============================================================

import os
import importlib.util
import streamlit as st

DEFAULT_APP = "v2"

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def run_v2():
    # v2 file path
    v2_path = os.path.join(THIS_DIR, "BSChapp_v2.py")
    mod = load_module("bschapp_v2", v2_path)
    mod.main()


def run_v1():
    # if your v1 lives elsewhere, update this path
    v1_path = os.path.join(THIS_DIR, "hub_v1.py")
    mod = load_module("bschapp_v1", v1_path)
    mod.main()


ROUTES = {"v1": run_v1, "v2": run_v2}

key = st.query_params.get("app", DEFAULT_APP)
if isinstance(key, list):
    key = key[0] if key else DEFAULT_APP

ROUTES.get(key, ROUTES[DEFAULT_APP])()