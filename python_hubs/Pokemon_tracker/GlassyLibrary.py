import streamlit as st
from pathlib import Path
import html
import random

# ═══════════════════════════════════════════════════════════════
# 🪟 GLASSY LIBRARY - Ultra Clean Universal Gray Shell
# View-only app for Nacli-generated Pokemon cards
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="🪟 Glassy Library",
    page_icon="🪟",
    layout="wide"
)

# Paths
APP_DIR = Path(__file__).parent
ENTRIES_DIR = APP_DIR / "pokemon_entries"
ENTRIES_DIR.mkdir(exist_ok=True)

# Admin code
ADMIN_CODE = "Bshapp"

# ═══════════════════════════════════════════════════════════════
# UI TINT SYSTEM
# ═══════════════════════════════════════════════════════════════

TYPE_TINTS = {
    "Universal Gray": ("#0b0f17", "#111827", "#cbd5e1", "rgba(203,213,225,0.10)", "rgba(203,213,225,0.06)"),
    "Water (Blue)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(56,189,248,0.12)", "rgba(56,189,248,0.06)"),
    "Fire (Orange)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(251,146,60,0.12)", "rgba(251,146,60,0.06)"),
    "Fairy/Psychic (Pink)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(251,113,133,0.12)", "rgba(251,113,133,0.06)"),
    "Grass (Green)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(34,197,94,0.12)", "rgba(34,197,94,0.06)"),
    "Electric (Yellow)": ("#0b0f17", "#0f172a", "#cbd5e1", "rgba(245,158,11,0.12)", "rgba(245,158,11,0.06)")
}

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def list_pokemon_entries():
    """List all Pokemon HTML files"""
    return sorted([f for f in ENTRIES_DIR.glob("*.html")])

def get_pokemon_name_from_path(path):
    """Extract Pokemon name from file path"""
    return path.stem.replace('_', ' ').title()

def delete_tool(name):
    """Delete selected HTML tool safely"""
    path = ENTRIES_DIR / f"{name}.html"
    if path.exists():
        path.unlink()
        st.session_state["current_tool"] = None
        st.success(f"🗑️ {name} deleted.")

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════

# Palm ID Gate
if "palm_taps" not in st.session_state:
    st.session_state["palm_taps"] = 0
if "show_admin_box" not in st.session_state:
    st.session_state["show_admin_box"] = False
if "admin_unlocked" not in st.session_state:
    st.session_state["admin_unlocked"] = False

# UI
if "ui_tint" not in st.session_state:
    st.session_state.ui_tint = "Universal Gray"
if "current_tool" not in st.session_state:
    st.session_state["current_tool"] = None
if "preview_height" not in st.session_state:
    st.session_state.preview_height = 800

# ═══════════════════════════════════════════════════════════════
# GLASSY UI THEME
# ═══════════════════════════════════════════════════════════════

bg0, bg1, text, glass, glass2 = TYPE_TINTS[st.session_state.ui_tint]

st.markdown(f"""
<style>
    :root {{
        --bg0: {bg0};
        --bg1: {bg1};
        --text: {text};
        --glass: {glass};
        --glass2: {glass2};
        
        --r1: 22px;
        --r2: 16px;
        --shadow: 0 16px 60px rgba(0,0,0,.45);
        --shadow2: 0 10px 30px rgba(0,0,0,.20);
    }}
    
    /* Page background */
    .stApp {{
        background:
            radial-gradient(1200px 800px at 20% 10%, {glass}, transparent 60%),
            radial-gradient(900px 700px at 80% 0%, var(--tint), transparent 55%),
            radial-gradient(900px 700px at 15% 30%, var(--tint2), transparent 60%),
            linear-gradient(180deg, var(--bg0), var(--bg1));
        color: var(--text);
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,.08);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,.12);
    }}
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {{
        color: var(--text) !important;
    }}
    
    /* Universal glass card utility */
    .kq-glass {{
        border-radius: var(--r1);
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,.16);
        box-shadow: var(--shadow);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: var(--glass);
        backdrop-filter: blur(20px);
        color: var(--text);
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background: rgba(255,255,255,.12);
        border-color: rgba(255,255,255,.24);
        transform: translateY(-2px);
        box-shadow: var(--shadow2);
    }}
    
    /* Select boxes */
    .stSelectbox > div > div {{
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 12px;
        color: var(--text);
    }}
    
    /* Text inputs */
    .stTextInput > div > div > input {{
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 12px;
        color: var(--text);
    }}
    
    /* Info/success/warning */
    .stSuccess, .stWarning, .stError, .stInfo {{
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,.16);
    }}
    
    /* Slider */
    .stSlider > div > div {{
        background: var(--glass);
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,.16);
        color: var(--text) !important;
    }}
    
    /* Main content */
    .main h1, .main h2, .main h3 {{
        color: var(--text) !important;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    # PALM ID (Admin Gate)
    left, right = st.columns([0.88, 0.12], vertical_alignment="center")
    
    with left:
        st.title("🪟 BSChapp")
    
    with right:
        if st.button("🖐️", help="Palm ID (tap 3x)"):
            st.session_state["palm_taps"] += 1
            if st.session_state["palm_taps"] >= 3:
                st.session_state["show_admin_box"] = True
    
    # Gate UI (only appears after 3 taps)
    if st.session_state["show_admin_box"] and not st.session_state["admin_unlocked"]:
        st.markdown("**✋ Palm ID:** enter admin code")
        code_try = st.text_input("Admin Code", type="password", placeholder="Enter code...")
        
        colA, colB = st.columns([0.6, 0.4])
        with colA:
            if st.button("Unlock"):
                if code_try == ADMIN_CODE:
                    st.session_state["admin_unlocked"] = True
                    st.success("Admin override unlocked.")
                    st.rerun()
                else:
                    st.error("Incorrect code.")
        with colB:
            if st.button("Reset"):
                st.session_state["palm_taps"] = 0
                st.session_state["show_admin_box"] = False
                st.rerun()
    
    # Optional tiny badge if unlocked
    if st.session_state["admin_unlocked"]:
        st.caption("🔓 Palm ID: unlocked")
    
    st.markdown("---")
    
    # UI Tint Selector
    st.session_state.ui_tint = st.selectbox(
        "UI Tint",
        list(TYPE_TINTS.keys()),
        index=list(TYPE_TINTS.keys()).index(st.session_state.ui_tint)
    )
    
    st.markdown("---")
    
    # Pokemon Selection
    st.subheader("📋 Library")
    
    all_entries = list_pokemon_entries()
    
    if all_entries:
        pokemon_names = [get_pokemon_name_from_path(entry) for entry in all_entries]
        
        # Random button
        if st.button("🎲 Random", use_container_width=True):
            st.session_state["current_tool"] = random.choice(all_entries).name
            st.rerun()
        
        # Dropdown
        if st.session_state["current_tool"]:
            try:
                # Find current index
                current_path = ENTRIES_DIR / st.session_state["current_tool"]
                if current_path.exists():
                    current_name = get_pokemon_name_from_path(current_path)
                    current_index = pokemon_names.index(current_name)
                else:
                    current_index = 0
            except (ValueError, FileNotFoundError):
                current_index = 0
        else:
            current_index = 0
        
        selected_pokemon = st.selectbox(
            "Select Card",
            pokemon_names,
            index=current_index,
            label_visibility="collapsed"
        )
        
        # Update current tool
        selected_index = pokemon_names.index(selected_pokemon)
        st.session_state["current_tool"] = all_entries[selected_index].name
        
        st.info(f"**{len(all_entries)}** cards")
    else:
        st.warning("No cards found. Use Nacli app to create entries.")
    
    st.markdown("---")
    
    # Display Settings
    st.subheader("⚙️ Display")
    
    st.session_state.preview_height = st.slider(
        "Preview Height",
        400, 1200, st.session_state.preview_height, 50
    )

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════

if st.session_state["current_tool"] and (ENTRIES_DIR / st.session_state["current_tool"]).exists():
    current_path = ENTRIES_DIR / st.session_state["current_tool"]
    pokemon_name = get_pokemon_name_from_path(current_path)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        html_content = current_path.read_text()
        st.download_button(
            label="💾 Download",
            data=html_content,
            file_name=current_path.name,
            mime="text/html",
            use_container_width=True
        )
    
    with col2:
        # EASY X (Delete Tool) - Admin only
        if st.session_state.get("admin_unlocked") and st.session_state.get("current_tool"):
            colA, colB = st.columns([0.85, 0.15])
            with colB:
                if st.button("✖", help="Delete tool"):
                    delete_tool(current_path.stem)
                    st.rerun()
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.title(f"🪟 {pokemon_name}")
    
    # Preview in iframe
    html_content = current_path.read_text()
    escaped_html = html.escape(html_content)
    
    # Always allow scripts for tabs to work
    sandbox = 'allow-scripts allow-same-origin'
    
    wrapper_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                margin: 0; 
                padding: 0; 
                background: transparent;
            }}
            iframe {{ 
                width: 100%; 
                height: {st.session_state.preview_height}px; 
                border: none;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            }}
        </style>
    </head>
    <body>
        <iframe srcdoc="{escaped_html}" sandbox="{sandbox}"></iframe>
    </body>
    </html>
    """
    
    st.components.v1.html(wrapper_html, height=st.session_state.preview_height + 20, scrolling=False)
    
    # Debug panel
    with st.expander("🔍 Debug: Raw HTML"):
        st.code(html_content, language="html")

else:
    # Welcome screen
    st.title("🪟 Glassy Library")
    st.subheader("Universal Gray Glass UI Shell")
    
    st.markdown("""
    ### Welcome to the Library
    
    This is a **view-only** app for displaying Pokémon cards created in the **Nacli Builder**.
    
    #### Features:
    - 🪟 Ultra-clean glassy Apple-like aesthetic
    - 🎨 5 UI tint variations
    - 🎲 Random card picker
    - 🔒 Admin gate (Palm ID)
    - 💾 Download cards
    - 🗑️ Delete tool (admin only)
    
    #### How to Use:
    1. Create cards using the **Nacli PokéApp** (Builder mode)
    2. Generated HTML files appear in `pokemon_entries/`
    3. Open this **Glassy Library** to view them
    4. Switch UI tints for different moods
    5. Tap 🖐️ 3 times to unlock admin tools
    
    #### Admin Code:
    `Bshapp`
    
    ---
    
    👈 **Select a card from the sidebar to get started!**
    
    **Note:** If you don't see any cards, use the Nacli Builder app to create your first entry.
    """)
    
    st.info("**Pro tip:** Change the UI Tint in the sidebar to match your Pokemon's type!")
