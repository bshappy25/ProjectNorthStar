import streamlit as st
from pathlib import Path
import base64
import random
import html
from datetime import datetime
import re

# ═══════════════════════════════════════════════════════════════
# NACLI POKEAPP - Clarity and Steadfastness
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="⛏️ Nacli PokéApp",
    page_icon="⛏️",
    layout="wide"
)

# Paths
APP_DIR = Path(__file__).parent
ENTRIES_DIR = APP_DIR / "pokemon_entries"
IMAGES_DIR = APP_DIR / "images"
MUSIC_DIR = APP_DIR / "music"
SCREENSHOTS_DIR = APP_DIR / "screenshots"

# Ensure directories exist
for directory in [ENTRIES_DIR, IMAGES_DIR, MUSIC_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def safe_stem(name):
    """Clean a name to make it filesystem-safe"""
    cleaned = re.sub(r'[^\w\s-]', '', name.lower())
    cleaned = re.sub(r'[\s]+', '_', cleaned)
    return cleaned[:50]

def next_available_path(stem):
    """Find next available filename to avoid overwriting"""
    base_path = ENTRIES_DIR / f"{stem}.html"
    if not base_path.exists():
        return base_path
    
    counter = 1
    while True:
        new_path = ENTRIES_DIR / f"{stem}_{counter}.html"
        if not new_path.exists():
            return new_path
        counter += 1

def list_pokemon_entries():
    """List all Pokemon HTML files"""
    return sorted([f for f in ENTRIES_DIR.glob("*.html")])

def parse_pokemon_metadata(html_content):
    """Extract metadata from HTML comments"""
    metadata = {
        "type": "Normal",
        "generation": "Gen 1",
        "evolution_line": []
    }
    
    type_match = re.search(r'<!-- TYPE:\s*(\w+)\s*-->', html_content)
    gen_match = re.search(r'<!-- GENERATION:\s*(Gen\s*\d+)\s*-->', html_content)
    evo_match = re.search(r'<!-- EVOLUTION_LINE:\s*(.+?)\s*-->', html_content)
    
    if type_match:
        metadata["type"] = type_match.group(1)
    if gen_match:
        metadata["generation"] = gen_match.group(1)
    if evo_match:
        metadata["evolution_line"] = [e.strip() for e in evo_match.group(1).split(',')]
    
    return metadata

def filter_pokemon(entries, type_filter, gen_filter):
    """Filter Pokemon entries"""
    filtered = []
    for entry_path in entries:
        content = entry_path.read_text()
        metadata = parse_pokemon_metadata(content)
        
        type_match = (type_filter == "All Types" or metadata["type"] == type_filter)
        gen_match = (gen_filter == "All Generations" or metadata["generation"] == gen_filter)
        
        if type_match and gen_match:
            filtered.append((entry_path, metadata))
    
    return filtered

def get_pokemon_name_from_path(path):
    """Extract Pokemon name from file path"""
    return path.stem.replace('_', ' ').title()

def get_audio_base64(audio_path):
    """Convert audio file to base64"""
    if audio_path.exists():
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def save_uploaded_image(uploaded_file):
    """Save uploaded image to images folder"""
    if uploaded_file is not None:
        image_path = IMAGES_DIR / uploaded_file.name
        image_path.write_bytes(uploaded_file.getvalue())
        return uploaded_file.name
    return None

def list_available_images():
    """List all images in the images folder"""
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']
    images = []
    for ext in extensions:
        images.extend(IMAGES_DIR.glob(ext))
    return sorted([img.name for img in images])

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════

if 'current_pokemon' not in st.session_state:
    st.session_state.current_pokemon = None
if 'preview_height' not in st.session_state:
    st.session_state.preview_height = 700
if 'safe_mode' not in st.session_state:
    st.session_state.safe_mode = True
if 'show_html_editor' not in st.session_state:
    st.session_state.show_html_editor = False

# ═══════════════════════════════════════════════════════════════
# NACLI UI THEME
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Nacli Theme: Clarity and Steadfastness */
    :root {
        --nacli-primary: #d4a574;
        --nacli-secondary: #8b6f47;
        --nacli-accent: #f4e4c1;
        --nacli-dark: #5c4a2f;
        --nacli-light: #fef9f0;
    }
    
    /* Main container */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--nacli-dark) !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fef9f0 0%, #f4e4c1 100%);
        border-right: 3px solid var(--nacli-secondary);
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--nacli-dark) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--nacli-primary) 0%, var(--nacli-secondary) 100%);
        color: white;
        border: 2px solid var(--nacli-secondary);
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--nacli-secondary) 0%, var(--nacli-dark) 100%);
        border-color: var(--nacli-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(92, 74, 47, 0.3);
    }
    
    /* Info boxes */
    .element-container div[data-testid="stMarkdownContainer"] p {
        color: var(--nacli-dark);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--nacli-accent);
        border-radius: 8px;
        border: 2px solid var(--nacli-primary);
        color: var(--nacli-dark) !important;
        font-weight: 600;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        border: 2px solid var(--nacli-primary);
        border-radius: 8px;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        border: 2px solid var(--nacli-primary);
        border-radius: 8px;
    }
    
    /* Success/warning/error boxes */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 8px;
        border-left: 4px solid var(--nacli-primary);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("⛏️ Nacli PokéApp")
    st.caption("*Clarity and Steadfastness*")
    
    st.markdown("---")
    
    # Music Player
    st.subheader("🎵 Background Music")
    music_files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.wav"))
    
    if music_files:
        selected_music = st.selectbox(
            "Track",
            ["None"] + [f.name for f in music_files],
            label_visibility="collapsed"
        )
        
        if selected_music != "None":
            music_path = MUSIC_DIR / selected_music
            audio_base64 = get_audio_base64(music_path)
            if audio_base64:
                st.markdown(f"""
                    <audio controls autoplay loop style="width: 100%;">
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                """, unsafe_allow_html=True)
    else:
        st.info("Add .mp3/.wav files to music/ folder")
    
    st.markdown("---")
    
    # Filters
    st.subheader("🔍 Filter Pokémon")
    
    POKEMON_TYPES = [
        "All Types", "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
        "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock",
        "Ghost", "Dragon", "Dark", "Steel", "Fairy"
    ]
    GENERATIONS = ["All Generations"] + [f"Gen {i}" for i in range(1, 10)]
    
    type_filter = st.selectbox("Type", POKEMON_TYPES)
    gen_filter = st.selectbox("Generation", GENERATIONS)
    
    st.markdown("---")
    
    # Pokemon Selection
    st.subheader("📋 Select Pokémon")
    
    all_entries = list_pokemon_entries()
    
    if all_entries:
        filtered_entries = filter_pokemon(all_entries, type_filter, gen_filter)
        
        if filtered_entries:
            pokemon_names = [get_pokemon_name_from_path(entry[0]) for entry in filtered_entries]
            
            # Random button
            if st.button("🎲 Random Pokémon", use_container_width=True):
                random_entry = random.choice(filtered_entries)
                st.session_state.current_pokemon = random_entry[0]
                st.rerun()
            
            # Dropdown
            if st.session_state.current_pokemon:
                current_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
                try:
                    current_index = pokemon_names.index(current_name)
                except ValueError:
                    current_index = 0
            else:
                current_index = 0
            
            selected_pokemon = st.selectbox(
                "Choose",
                pokemon_names,
                index=current_index,
                label_visibility="collapsed"
            )
            
            selected_index = pokemon_names.index(selected_pokemon)
            st.session_state.current_pokemon = filtered_entries[selected_index][0]
            
            st.info(f"**{len(filtered_entries)}** of **{len(all_entries)}** Pokémon")
        else:
            st.warning("No Pokémon match filters")
    else:
        st.warning("No Pokémon entries found")
    
    st.markdown("---")
    
    # Image Upload
    with st.expander("📸 Upload Image"):
        uploaded_image = st.file_uploader(
            "Add to images folder",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            label_visibility="collapsed"
        )
        
        if uploaded_image:
            if st.button("💾 Save Image", use_container_width=True):
                filename = save_uploaded_image(uploaded_image)
                if filename:
                    st.success(f"Saved: {filename}")
                    st.rerun()
        
        st.caption(f"**{len(list_available_images())}** images available")
    
    # Create New Pokemon
    with st.expander("➕ Create New Entry"):
        new_name = st.text_input("Pokémon Name")
        new_type = st.selectbox("Type", POKEMON_TYPES[1:], key="new_type")
        new_gen = st.selectbox("Generation", GENERATIONS[1:], key="new_gen")
        new_evo = st.text_input("Evolution Line", placeholder="Nacli, Naclstack, Garganacl")
        
        if st.button("Create", use_container_width=True):
            if new_name:
                evo_list = [e.strip() for e in new_evo.split(',')] if new_evo else [new_name]
                
                # Create basic HTML
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{new_name}</title>
    <!-- TYPE: {new_type} -->
    <!-- GENERATION: {new_gen} -->
    <!-- EVOLUTION_LINE: {', '.join(evo_list)} -->
    <style>
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #d4a574 0%, #f4e4c1 100%);
            color: #5c4a2f;
        }}
        .pokemon-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 3rem;
            border: 3px solid #8b6f47;
            box-shadow: 0 20px 60px rgba(92, 74, 47, 0.3);
        }}
        h1 {{
            font-size: 3rem;
            text-align: center;
            color: #5c4a2f;
            margin: 1rem 0;
        }}
        .subtitle {{
            text-align: center;
            font-size: 1.5rem;
            color: #8b6f47;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <div class="pokemon-card">
        <h1>{new_name}</h1>
        <div class="subtitle">The {new_type} Type</div>
        <p style="text-align: center; font-size: 5rem;">⛏️</p>
        <div style="margin-top: 2rem;">
            <p><strong>Type:</strong> {new_type}</p>
            <p><strong>Generation:</strong> {new_gen}</p>
            <p><strong>Evolution Line:</strong> {', '.join(evo_list)}</p>
        </div>
    </div>
</body>
</html>"""
                
                filename = safe_stem(new_name)
                file_path = next_available_path(filename)
                file_path.write_text(html_content)
                
                st.success(f"Created: {file_path.name}")
                st.session_state.current_pokemon = file_path
                st.rerun()
            else:
                st.error("Enter a name")
    
    st.markdown("---")
    
    # Display Settings
    st.subheader("⚙️ Display Settings")
    
    st.session_state.preview_height = st.slider(
        "Preview Height",
        400, 1200, st.session_state.preview_height, 50
    )
    
    st.session_state.safe_mode = st.toggle(
        "Safe Mode (no scripts)",
        value=st.session_state.safe_mode
    )
    
    if st.session_state.safe_mode:
        st.caption("✅ Scripts disabled")
    else:
        st.caption("⚠️ Scripts enabled")

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════

# Top action bar
if st.session_state.current_pokemon:
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        if st.button("📝 Edit HTML", use_container_width=True):
            st.session_state.show_html_editor = not st.session_state.show_html_editor
            st.rerun()
    
    with col2:
        if st.button("🖼️ Insert Image", use_container_width=True):
            st.session_state.show_image_inserter = True
            st.rerun()
    
    with col3:
        html_content = st.session_state.current_pokemon.read_text()
        st.download_button(
            label="💾 Download",
            data=html_content,
            file_name=st.session_state.current_pokemon.name,
            mime="text/html",
            use_container_width=True
        )
    
    with col4:
        if st.button("🗑️ Delete", use_container_width=True):
            st.session_state.confirm_delete = True
            st.rerun()
    
    with col5:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

# Display Pokemon or editor
if st.session_state.current_pokemon and st.session_state.current_pokemon.exists():
    pokemon_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
    
    # HTML Editor (if enabled)
    if st.session_state.get('show_html_editor', False):
        st.subheader(f"📝 Editing: {pokemon_name}")
        
        html_content = st.session_state.current_pokemon.read_text()
        
        edited_html = st.text_area(
            "HTML Source",
            value=html_content,
            height=400,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.session_state.current_pokemon.write_text(edited_html)
                st.success("Saved!")
                st.session_state.show_html_editor = False
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_html_editor = False
                st.rerun()
        
        st.markdown("---")
    
    # Image Inserter (if enabled)
    if st.session_state.get('show_image_inserter', False):
        st.subheader("🖼️ Insert Image into HTML")
        
        available_images = list_available_images()
        
        if available_images:
            selected_image = st.selectbox("Choose Image", available_images)
            
            st.code(f'<img src="../images/{selected_image}" alt="{selected_image}" style="max-width: 100%;">', language="html")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📋 Copy Code", use_container_width=True):
                    st.info("Code shown above - copy manually")
            
            with col2:
                if st.button("❌ Close", use_container_width=True):
                    st.session_state.show_image_inserter = False
                    st.rerun()
        else:
            st.warning("No images available. Upload one first!")
            if st.button("❌ Close", use_container_width=True):
                st.session_state.show_image_inserter = False
                st.rerun()
        
        st.markdown("---")
    
    # Delete Confirmation
    if st.session_state.get('confirm_delete', False):
        st.error(f"⚠️ Delete {pokemon_name}?")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("✅ Yes, Delete", use_container_width=True):
                st.session_state.current_pokemon.unlink()
                st.session_state.current_pokemon = None
                st.session_state.confirm_delete = False
                st.success(f"Deleted {pokemon_name}")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.confirm_delete = False
                st.rerun()
        
        st.markdown("---")
    
    # Pokemon Preview (iframe)
    st.title(f"⛏️ {pokemon_name}")
    
    html_content = st.session_state.current_pokemon.read_text()
    escaped_html = html.escape(html_content)
    
    # Determine sandbox permissions
    if st.session_state.safe_mode:
        sandbox = 'allow-same-origin'
    else:
        sandbox = 'allow-scripts allow-forms allow-popups allow-modals allow-downloads allow-same-origin'
    
    # Wrapper HTML with iframe
    wrapper_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; }}
            iframe {{ 
                width: 100%; 
                height: {st.session_state.preview_height}px; 
                border: 3px solid #8b6f47; 
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(92, 74, 47, 0.2);
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
    with st.expander("🔍 Debug: View Raw HTML"):
        st.code(html_content, language="html")

else:
    # Welcome screen
    st.title("⛏️ Nacli PokéApp")
    st.subheader("*Clarity and Steadfastness*")
    
    st.markdown("""
    ### Welcome, Trainer!
    
    This app lets you view, create, and manage Pokémon entries as HTML files.
    
    #### Quick Start:
    1. **Create** a new Pokémon using the sidebar
    2. **Upload images** to use in your entries
    3. **Edit HTML** directly in the app
    4. **Preview** with iframe rendering
    5. **Filter** by type and generation
    
    #### Features:
    - 🎲 Random Pokémon picker
    - 📝 In-app HTML editor
    - 🖼️ Image upload & insertion helper
    - 🎵 Background music support
    - 💾 Export as standalone HTML
    - 🔒 Safe mode (sandboxed preview)
    
    #### The Nacli Way:
    *Like the Rock Salt Pokémon, we value **clarity** in our code and **steadfastness** in our purpose.*
    
    👈 **Get started by creating your first Pokémon in the sidebar!**
    """)
    
    st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/935.png", width=300)
