# python_hubs/streamlit_app.py
# ============================================================
# ProjectNorthStar — Streamlit Router (STABLE FRONT DOOR)
# - Keep this file name/path forever.
# - Swap versions by changing DEFAULT_APP or using ?app=v1 / ?app=v2
# ============================================================

import streamlit as st

DEFAULT_APP = "v2"  # change to "v3" later when ready


def run_v2():
    # BSChapp v2 package: python_hubs/BSChapp_v2/
    from python_hubs.BSChapp_v2 import main
    main()


def run_v1():
    # v1 legacy module: python_hubs/hub_v1.py (or package)
    from python_hubs.hub_v1 import main
    main()


ROUTES = {
    "v1": ("BSChapp v1", run_v1),
    "v2": ("BSChapp v2", run_v2),
}


def get_route_key() -> str:
    """
    Route selection via query param:
      - default: v2
      - override: https://<app>/?app=v1
    """
    try:
        qp = st.query_params
        key = qp.get("app", DEFAULT_APP)
        if isinstance(key, list):  # some environments may return lists
            key = key[0] if key else DEFAULT_APP
        return key or DEFAULT_APP
    except Exception:
        return DEFAULT_APP


key = get_route_key()
label, fn = ROUTES.get(key, ROUTES[DEFAULT_APP])

# Optional: lightweight banner (can delete if you want it invisible)
# st.caption(f"Router: {label}  •  (?app=v1 or ?app=v2)")

fn()