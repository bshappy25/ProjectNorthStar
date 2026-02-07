# python_hubs/streamlit_app.py
# Stable router (v1/v2/v3/v4)

import streamlit as st

DEFAULT_APP = "v2"

def run_v2():
    from BSChapp_v2 import main
    main()

def run_v1():
    from hub_v1 import main
    main()

ROUTES = {
    "v1": run_v1,
    "v2": run_v2,
}

key = st.query_params.get("app", DEFAULT_APP)
if isinstance(key, list):
    key = key[0] if key else DEFAULT_APP

ROUTES.get(key, ROUTES[DEFAULT_APP])()