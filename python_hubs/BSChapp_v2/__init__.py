# python_hubs/BSChapp_v2/__init__.py
# Export a stable entrypoint for the router.

try:
    # Preferred: your main v2 file is BSChapp_v2.py
    from .BSChapp_v2 import main
except Exception:
    # Fallback: if your main file is named app.py
    from .app import main