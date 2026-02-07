import streamlit as st

# -------------------------
# CONFIG
# -------------------------
DEFAULT_APP = "v2"

def run_v2():
    from BSChapp_v2 import main
    main()

def run_v1():
    from hub_v1 import main
    main()

ROUTES = {
    "v1": ("BSChapp v1", run_v1),
    "v2": ("BSChapp v2", run_v2),
}

# -------------------------
# ROUTING
# -------------------------
query = st.query_params
requested = query.get("app", DEFAULT_APP)

label, fn = ROUTES.get(requested, ROUTES[DEFAULT_APP])
fn()