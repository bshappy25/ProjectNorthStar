# python_hubs/streamlit_app.py
# ============================================================
# ProjectNorthStar — Streamlit Router (STABLE / FROZEN)
# Default: BSChapp v2
# Optional: ?app=v1 or ?app=portal
# ============================================================

import os
import importlib.util
import streamlit as st

DEFAULT_APP = "v2"
THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def load_module(name: str, path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Module not found: {path}")

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec for: {path}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def run_v2():
    v2_path = os.path.join(THIS_DIR, "BSChapp_v2", "BSChapp_v2.py")
    mod = load_module("bschapp_v2", v2_path)

    # Explicit entrypoint (preferred)
    if hasattr(mod, "main") and callable(mod.main):
        mod.main()
        return
    # else: acceptable if module runs at import-time


def run_portal():
    portal_path = os.path.join(THIS_DIR, "BSChapp_v2", "pages", "AI_Storyboard_Portal.py")
    mod = load_module("ai_storyboard_portal", portal_path)

    if hasattr(mod, "main") and callable(mod.main):
        mod.main()


def run_v1():
    v1_path = os.path.join(THIS_DIR, "hub_v1.py")
    mod = load_module("bschapp_v1", v1_path)

    if hasattr(mod, "main") and callable(mod.main):
        mod.main()


ROUTES = {
    "v2": run_v2,
    "v1": run_v1,
    "portal": run_portal,
}

key = st.query_params.get("app", DEFAULT_APP)
if isinstance(key, list):
    key = key[0] if key else DEFAULT_APP

ROUTES.get(key, ROUTES[DEFAULT_APP])()