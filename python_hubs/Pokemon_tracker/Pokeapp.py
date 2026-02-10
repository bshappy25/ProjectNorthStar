import streamlit as st
from pathlib import Path
import base64
import random
import json
from datetime import datetime
import html

# Setup
st.set_page_config(
    page_title="Pokémon Viewer",
    page_icon="🔮",
    layout="centered"
)

# Define paths
APP_DIR = Path(__file__).parent
THEMES_DIR = APP_DIR / "themes"
ASSETS_DIR = APP_DIR / "assets"
ENTRIES_DIR = APP_DIR / "pokemon_entries"
MUSIC_DIR = APP_DIR / "music"
SCREENSHOTS_DIR = APP_DIR / "screenshots"

# Ensure directories exist
for directory in [THEMES_DIR, ASSETS_DIR, ENTRIES_DIR, MUSIC_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True)

# Theme configurations
THEMES = {
    "🌊 WATER": "water.css",
    "🌿 GRASS": "grass.css",
    "🔥 FIRE": "fire.css",
    "⚪ NORMAL": "normal.css",
    "✨ PSYCHIC/FAIRY": "psychic_fairy.css"
}

# Type options for filtering
POKEMON_TYPES = [
    "All Types", "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock",
    "Ghost", "Dragon", "Dark", "Steel", "Fairy"
]

# Generation options
GENERATIONS = ["All Generations"] + [f"Gen {i}" for i in range(1, 10)]

def safe_stem(name):
    """Clean a name to make it filesystem-safe"""
    import re
    cleaned = re.sub(r'[^\w\s-]', '', name.lower())
    cleaned = re.sub(r'[\s]+', '_', cleaned)
    return cleaned[:50]

def load_css(theme_file):
    """Load CSS from theme file"""
    theme_path = THEMES_DIR / theme_file
    if theme_path.exists():
        return theme_path.read_text()
    return ""

def get_audio_base64(audio_path):
    """Convert audio file to base64 for embedding"""
    if audio_path.exists():
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def list_pokemon_entries():
    """List all Pokemon HTML files"""
    return sorted([f for f in ENTRIES_DIR.glob("*.html")])

def parse_pokemon_metadata(html_content):
    """Extract metadata from HTML file (stored in HTML comments)"""
    import re
    metadata = {
        "type": "Normal",
        "generation": "Gen 1",
        "evolution_line": []
    }
    
    # Look for metadata in HTML comments
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
    """Filter Pokemon entries based on type and generation"""
    filtered = []
    
    for entry_path in entries:
        content = entry_path.read_text()
        metadata = parse_pokemon_metadata(content)
        
        # Apply filters
        type_match = (type_filter == "All Types" or metadata["type"] == type_filter)
        gen_match = (gen_filter == "All Generations" or metadata["generation"] == gen_filter)
        
        if type_match and gen_match:
            filtered.append((entry_path, metadata))
    
    return filtered

def get_pokemon_name_from_path(path):
    """Extract Pokemon name from file path"""
    return path.stem.replace('_', ' ').title()

def render_pokemon_html(html_content, theme_name):
    """Render the Pokemon HTML content with theme wrapper"""
    
    # Escape the HTML for safe embedding
    escaped_html = html.escape(html_content)
    
    # Build wrapper with iframe
    wrapper = f"""
    <div class="pokemon-viewer-container">
        <iframe 
            srcdoc="{escaped_html}"
            style="width: 100%; min-height: 600px; border: none; border-radius: 8px;"
            sandbox="allow-same-origin"
        ></iframe>
    </div>
    """
    
    return wrapper

def create_sample_pokemon_html(name, pokemon_type, generation, evolution_line):
    """Create a sample Pokemon HTML entry"""
    evo_line_str = ", ".join(evolution_line) if evolution_line else name
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{name}</title>
    <!-- TYPE: {pokemon_type} -->
    <!-- GENERATION: {generation} -->
    <!-- EVOLUTION_LINE: {evo_line_str} -->
    <style>
        body {{
            font-family: 'Inter', system-ui, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .pokemon-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
        }}
        h1 {{
            font-size: 3rem;
            margin: 1rem 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            font-size: 1.5rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }}
        .image-placeholder {{
            width: 300px;
            height: 300px;
            margin: 2rem auto;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin: 2rem 0;
            text-align: left;
        }}
        .info-item {{
            background: rgba(255,255,255,0.15);
            padding: 1rem;
            border-radius: 8px;
        }}
        .evolution-line {{
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="pokemon-card">
        <h1>{name}</h1>
        <div class="subtitle">The {pokemon_type} Type Guardian</div>
        
        <div class="image-placeholder">
            🔮
        </div>
        
        <div class="info-grid">
            <div class="info-item">
                <strong>Type:</strong> {pokemon_type}
            </div>
            <div class="info-item">
                <strong>Generation:</strong> {generation}
            </div>
            <div class="info-item">
                <strong>Trainer ID:</strong> KQ-{random.randint(100, 999)}
            </div>
            <div class="info-item">
                <strong>Date Captured:</strong> {datetime.now().strftime('%Y-%m-%d')}
            </div>
        </div>
        
        <div class="evolution-line">
            <strong>Evolution Line:</strong><br>
            {evo_line_str}
        </div>
    </div>
</body>
</html>"""

def save_screenshot(html_content, pokemon_name):
    """Save the current view as a marker file (actual screenshot would need Selenium/Playwright)"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_stem(pokemon_name)}_{timestamp}.txt"
    screenshot_path = SCREENSHOTS_DIR / filename
    
    # Save a marker file with metadata
    marker_content = f"""Screenshot Marker
Pokemon: {pokemon_name}
Timestamp: {datetime.now().isoformat()}
Theme: {st.session_state.get('current_theme', 'NORMAL')}

Note: To enable actual PNG screenshots, install selenium or playwright.
For now, this marks that a screenshot was requested.
"""
    screenshot_path.write_text(marker_content)
    return screenshot_path

# Initialize session state
if 'current_pokemon' not in st.session_state:
    st.session_state.current_pokemon = None
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "⚪ NORMAL"
if 'autoplay_music' not in st.session_state:
    st.session_state.autoplay_music = True

# ============= SIDEBAR =============
st.sidebar.title("🔮 Pokémon Viewer")

# Music player
st.sidebar.markdown("### 🎵 Background Music")
music_files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.wav"))

if music_files:
    selected_music = st.sidebar.selectbox(
        "Select Track",
        ["None"] + [f.name for f in music_files]
    )
    
    if selected_music != "None":
        music_path = MUSIC_DIR / selected_music
        audio_base64 = get_audio_base64(music_path)
        if audio_base64:
            autoplay = "autoplay" if st.session_state.autoplay_music else ""
            st.sidebar.markdown(f"""
                <audio controls {autoplay} loop style="width: 100%;">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
else:
    st.sidebar.info("No music files found. Add .mp3 or .wav files to the music/ folder.")

st.sidebar.markdown("---")

# Filters
st.sidebar.markdown("### 🔍 Filters")
type_filter = st.sidebar.selectbox("Type", POKEMON_TYPES)
gen_filter = st.sidebar.selectbox("Generation", GENERATIONS)

# Theme selector
st.sidebar.markdown("### 🎨 Theme")
selected_theme = st.sidebar.selectbox(
    "Energy Type",
    list(THEMES.keys()),
    index=list(THEMES.keys()).index(st.session_state.current_theme)
)
st.session_state.current_theme = selected_theme

st.sidebar.markdown("---")

# Pokemon selection
st.sidebar.markdown("### 📋 Select Pokémon")

all_entries = list_pokemon_entries()

if all_entries:
    filtered_entries = filter_pokemon(all_entries, type_filter, gen_filter)
    
    if filtered_entries:
        pokemon_names = [get_pokemon_name_from_path(entry[0]) for entry in filtered_entries]
        
        # Random button
        if st.sidebar.button("🎲 Random Pokémon", use_container_width=True):
            random_entry = random.choice(filtered_entries)
            st.session_state.current_pokemon = random_entry[0]
        
        # Dropdown selection
        if st.session_state.current_pokemon:
            current_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
            try:
                current_index = pokemon_names.index(current_name)
            except ValueError:
                current_index = 0
        else:
            current_index = 0
        
        selected_pokemon = st.sidebar.selectbox(
            "Choose from list",
            pokemon_names,
            index=current_index
        )
        
        # Update current pokemon
        selected_index = pokemon_names.index(selected_pokemon)
        st.session_state.current_pokemon = filtered_entries[selected_index][0]
        
        st.sidebar.info(f"**Showing:** {len(filtered_entries)} of {len(all_entries)} Pokémon")
    else:
        st.sidebar.warning("No Pokémon match your filters")
        st.session_state.current_pokemon = None
else:
    st.sidebar.warning("No Pokémon entries found")

st.sidebar.markdown("---")

# Add new Pokemon
with st.sidebar.expander("➕ Add New Pokémon"):
    new_name = st.text_input("Pokémon Name", placeholder="e.g., Garganacl")
    new_type = st.selectbox("Type", POKEMON_TYPES[1:], key="new_type")  # Skip "All Types"
    new_gen = st.selectbox("Generation", GENERATIONS[1:], key="new_gen")  # Skip "All Generations"
    new_evo_line = st.text_input("Evolution Line (comma separated)", placeholder="e.g., Bulbasaur, Ivysaur, Venusaur")
    
    if st.button("Create Sample Entry", use_container_width=True):
        if new_name:
            evo_list = [e.strip() for e in new_evo_line.split(',')] if new_evo_line else [new_name]
            sample_html = create_sample_pokemon_html(new_name, new_type, new_gen, evo_list)
            
            filename = f"{safe_stem(new_name)}.html"
            entry_path = ENTRIES_DIR / filename
            entry_path.write_text(sample_html)
            
            st.success(f"Created {filename}")
            st.rerun()
        else:
            st.error("Please enter a Pokémon name")

# ============= MAIN CONTENT =============

# Load and apply theme CSS
theme_css = load_css(THEMES[selected_theme])
if theme_css:
    st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

# Action buttons
if st.session_state.current_pokemon:
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📸 Screenshot", use_container_width=True):
            pokemon_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
            screenshot_path = save_screenshot("", pokemon_name)
            st.success(f"Screenshot marker saved!")
    
    with col2:
        # Download HTML button
        if st.session_state.current_pokemon:
            html_content = st.session_state.current_pokemon.read_text()
            st.download_button(
                label="💾 Download HTML",
                data=html_content,
                file_name=st.session_state.current_pokemon.name,
                mime="text/html",
                use_container_width=True
            )
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

# Display Pokemon
if st.session_state.current_pokemon and st.session_state.current_pokemon.exists():
    html_content = st.session_state.current_pokemon.read_text()
    pokemon_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
    
    st.title(f"⚡ {pokemon_name}")
    
    # Display the HTML in an iframe
    wrapped_html = render_pokemon_html(html_content, selected_theme)
    st.markdown(wrapped_html, unsafe_allow_html=True)
    
    # Debug section
    with st.expander("🔍 Debug: View Source"):
        st.code(html_content, language="html")

else:
    st.info("👈 Select or create a Pokémon to view")
    
    # Show helpful getting started info
    st.markdown("""
    ### Getting Started
    
    1. **Add Your First Pokémon**: Use the sidebar to create a sample entry
    2. **Add Music**: Place .mp3 or .wav files in the `music/` folder
    3. **Customize Themes**: Edit CSS files in the `themes/` folder
    4. **Create Custom Entries**: Add .html files to `pokemon_entries/` folder
    
    ### Features
    - 🎲 Randomize Pokémon selection
    - 🔍 Filter by Type and Generation
    - 🎨 5 unique theme variants
    - 🎵 Background music support
    - 📸 Screenshot markers
    - 💾 Export as HTML
    """)
