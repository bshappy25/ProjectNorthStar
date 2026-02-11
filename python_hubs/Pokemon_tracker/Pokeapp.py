import streamlit as st
from pathlib import Path
import base64
import random
import html
from datetime import datetime, date
import re
import io
from PIL import Image

# ═══════════════════════════════════════════════════════════════
# NACLI POKÉAPP V2 - Builder Edition
# Clarity and Steadfastness
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="⛏️ Nacli PokéApp v2",
    page_icon="⛏️",
    layout="wide"
)

# Paths
APP_DIR = Path(__file__).parent
ENTRIES_DIR = APP_DIR / "pokemon_entries"
IMAGES_DIR = APP_DIR / "images"
SCREENSHOTS_DIR = APP_DIR / "screenshots"
MUSIC_DIR = APP_DIR / "music"

for directory in [ENTRIES_DIR, IMAGES_DIR, SCREENSHOTS_DIR, MUSIC_DIR]:
    directory.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def safe_stem(name):
    """Clean name for filesystem"""
    cleaned = re.sub(r'[^\w\s-]', '', name.lower())
    cleaned = re.sub(r'[\s]+', '_', cleaned)
    return cleaned[:50]

def image_to_base64(image_file):
    """Convert uploaded image to base64 string"""
    if image_file is None:
        return None
    
    # Read image
    image = Image.open(image_file)
    
    # Convert to RGB if necessary
    if image.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    
    # Save to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    
    # Encode to base64
    b64_string = base64.b64encode(img_bytes).decode()
    
    return b64_string

def create_hero_image_tag(b64_string, alt_text="Pokemon"):
    """Create hero image HTML tag"""
    if not b64_string:
        return '<div class="hero-placeholder">⛏️</div>'
    return f'<img src="data:image/png;base64,{b64_string}" alt="{alt_text}" class="hero-image">'

def create_gallery_image_tag(b64_string, caption=""):
    """Create gallery image HTML tag"""
    if not b64_string:
        return ""
    
    caption_html = f'<div class="gallery-caption">{caption}</div>' if caption else ''
    return f'''<div class="gallery-item">
    <img src="data:image/png;base64,{b64_string}" alt="{caption}">
    {caption_html}
</div>'''

def list_pokemon_entries():
    """List all Pokemon HTML files"""
    return sorted([f for f in ENTRIES_DIR.glob("*.html")])

def get_pokemon_name_from_path(path):
    """Extract Pokemon name from file path"""
    return path.stem.replace('_', ' ').title()

def get_audio_base64(audio_path):
    """Convert audio to base64"""
    if audio_path.exists():
        with open(audio_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ═══════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════

def generate_pokemon_html(data):
    """Generate complete Pokemon HTML entry"""
    
    # Determine shiny styling
    shiny_class = "shiny" if data['is_shiny'] else ""
    shiny_bookend = "✨ " if data['is_shiny'] else ""
    shiny_bookend_end = " ✨" if data['is_shiny'] else ""
    
    # Hero image
    hero_html = create_hero_image_tag(data.get('hero_image_b64'), data['name'])
    
    # Gallery images
    gallery_html = ""
    for item in data.get('gallery_items', []):
        if item['b64']:
            gallery_html += create_gallery_image_tag(item['b64'], item['caption'])
    
    if not gallery_html:
        gallery_html = '<p style="text-align: center; opacity: 0.6;">No images in gallery</p>'
    
    # Moves HTML
    moves_html = ""
    for move in data.get('moves', []):
        if move:
            moves_html += f'<div class="move-item">{move}</div>\n'
    
    if not moves_html:
        moves_html = '<p style="opacity: 0.6;">No moves listed</p>'
    
    # Traits HTML
    traits_html = ""
    for trait in data.get('traits', []):
        if trait['name']:
            traits_html += f'''<div class="trait-box">
    <div class="trait-label">{trait['label']}</div>
    <div class="trait-name">{trait['name']}</div>
    <div class="trait-desc">{trait['description']}</div>
</div>\n'''
    
    if not traits_html:
        traits_html = '<p style="opacity: 0.6;">No traits listed</p>'
    
    # Stats
    stats = data.get('stats', {})
    
    # Build HTML
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{data['name']}</title>
    <!-- TYPE: {data['type']} -->
    <!-- GENERATION: {data['generation']} -->
    <!-- EVOLUTION_LINE: {data['evolution_line']} -->
    <!-- VARIANT: {data['variant']} -->
    <!-- SELF_CONTAINED: true -->
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: white;
            min-height: 100vh;
            padding: 2rem;
        }}
        
        body.shiny {{
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
            animation: shimmer 3s ease-in-out infinite;
        }}
        
        @keyframes shimmer {{
            0%, 100% {{ filter: brightness(1) saturate(1); }}
            50% {{ filter: brightness(1.2) saturate(1.3); }}
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
        }}
        
        body.shiny .header h1 {{
            animation: sparkle 2s ease-in-out infinite;
        }}
        
        @keyframes sparkle {{
            0%, 100% {{ text-shadow: 0 0 20px #fbbf24, 3px 3px 6px rgba(0, 0, 0, 0.5); }}
            50% {{ text-shadow: 0 0 40px #f59e0b, 0 0 60px #fbbf24, 3px 3px 6px rgba(0, 0, 0, 0.5); }}
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.8;
            margin-bottom: 1rem;
        }}
        
        .tabs {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }}
        
        .tab-button {{
            background: none;
            border: none;
            color: white;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
        }}
        
        .tab-button:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}
        
        .tab-button.active {{
            border-bottom-color: #fbbf24;
            background: rgba(255, 255, 255, 0.05);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Tab A: Card View */
        .card-view {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 3rem;
            border: 3px solid rgba(251, 191, 36, 0.3);
        }}
        
        body.shiny .card-view {{
            border-color: rgba(251, 191, 36, 0.6);
            box-shadow: 0 0 40px rgba(251, 191, 36, 0.3);
        }}
        
        .hero-image {{
            max-width: 400px;
            width: 100%;
            height: auto;
            display: block;
            margin: 2rem auto;
            border-radius: 16px;
        }}
        
        .hero-placeholder {{
            width: 400px;
            height: 400px;
            margin: 2rem auto;
            background: rgba(251, 191, 36, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10rem;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .info-item {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #fbbf24;
        }}
        
        .info-item strong {{
            color: #fef3c7;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        /* Tab B: Stats & Moves */
        .stats-section {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 3rem;
            border: 3px solid rgba(251, 191, 36, 0.3);
            margin-bottom: 2rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-box {{
            background: rgba(251, 191, 36, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 2px solid rgba(251, 191, 36, 0.3);
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 0.5rem;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: #fbbf24;
        }}
        
        .moves-section {{
            margin-top: 2rem;
        }}
        
        .moves-section h3 {{
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .move-item {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #fbbf24;
        }}
        
        .traits-section {{
            margin-top: 2rem;
        }}
        
        .traits-section h3 {{
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .trait-box {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border: 2px solid rgba(251, 191, 36, 0.3);
        }}
        
        .trait-label {{
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #fbbf24;
            margin-bottom: 0.5rem;
        }}
        
        .trait-name {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .trait-desc {{
            opacity: 0.9;
            line-height: 1.6;
        }}
        
        /* Tab C: Gallery */
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }}
        
        .gallery-item {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 1rem;
            border: 2px solid rgba(251, 191, 36, 0.3);
            transition: transform 0.3s ease;
        }}
        
        .gallery-item:hover {{
            transform: translateY(-5px);
            border-color: #fbbf24;
        }}
        
        .gallery-item img {{
            width: 100%;
            height: auto;
            border-radius: 12px;
            margin-bottom: 0.5rem;
        }}
        
        .gallery-caption {{
            text-align: center;
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        /* Fallback for no-script */
        .no-script-warning {{
            background: rgba(251, 191, 36, 0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border-left: 4px solid #fbbf24;
        }}
    </style>
</head>
<body class="{shiny_class}">
    <div class="container">
        <div class="header">
            <h1>{shiny_bookend}{data['name']}{shiny_bookend_end}</h1>
            <div class="subtitle">
                {data['type']} Type • {data['generation']} • {data['variant']}
            </div>
        </div>
        
        <noscript>
            <div class="no-script-warning">
                ⚠️ Tabs require JavaScript. Content is displayed below in order: Card → Stats → Gallery
            </div>
        </noscript>
        
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('card')">⛏️ Card</button>
            <button class="tab-button" onclick="showTab('stats')">📊 Stats</button>
            <button class="tab-button" onclick="showTab('gallery')">🖼️ Gallery</button>
        </div>
        
        <!-- Tab A: Card View -->
        <div id="tab-card" class="tab-content active">
            <div class="card-view">
                {hero_html}
                
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Type:</strong> {data['type']}
                    </div>
                    <div class="info-item">
                        <strong>Generation:</strong> {data['generation']}
                    </div>
                    <div class="info-item">
                        <strong>Evolution Line:</strong><br>{data['evolution_line']}
                    </div>
                    <div class="info-item">
                        <strong>OT:</strong> {data.get('ot', 'N/A')}
                    </div>
                    <div class="info-item">
                        <strong>ID No.:</strong> {data.get('id_no', 'N/A')}
                    </div>
                    <div class="info-item">
                        <strong>First Met:</strong><br>{data.get('first_met_location', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>First Met Date:</strong><br>{data.get('first_met_date', 'Unknown')}
                    </div>
                    <div class="info-item">
                        <strong>Nature:</strong> {data.get('nature', 'N/A')}
                    </div>
                    <div class="info-item">
                        <strong>Ability:</strong> {data.get('ability', 'N/A')}
                    </div>
                    <div class="info-item">
                        <strong>Characteristic:</strong><br>{data.get('characteristic', 'N/A')}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tab B: Stats & Moves -->
        <div id="tab-stats" class="tab-content">
            <div class="stats-section">
                <h2>Base Stats</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">HP</div>
                        <div class="stat-value">{stats.get('hp', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Attack</div>
                        <div class="stat-value">{stats.get('attack', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Defense</div>
                        <div class="stat-value">{stats.get('defense', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Sp. Atk</div>
                        <div class="stat-value">{stats.get('sp_atk', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Sp. Def</div>
                        <div class="stat-value">{stats.get('sp_def', 0)}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Speed</div>
                        <div class="stat-value">{stats.get('speed', 0)}</div>
                    </div>
                </div>
                
                <div class="moves-section">
                    <h3>Moves</h3>
                    {moves_html}
                </div>
                
                <div class="traits-section">
                    <h3>Traits</h3>
                    {traits_html}
                </div>
            </div>
        </div>
        
        <!-- Tab C: Gallery -->
        <div id="tab-gallery" class="tab-content">
            <div class="gallery-grid">
                {gallery_html}
            </div>
        </div>
    </div>
    
    <script>
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById('tab-' + tabName).classList.add('active');
            
            // Activate button
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''
    
    return html_content

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════

if 'mode' not in st.session_state:
    st.session_state.mode = "Library"
if 'current_pokemon' not in st.session_state:
    st.session_state.current_pokemon = None
if 'preview_height' not in st.session_state:
    st.session_state.preview_height = 700
if 'safe_mode' not in st.session_state:
    st.session_state.safe_mode = False

# Builder state
if 'hero_image_b64' not in st.session_state:
    st.session_state.hero_image_b64 = None
if 'gallery_items' not in st.session_state:
    st.session_state.gallery_items = [{'b64': None, 'caption': ''} for _ in range(6)]

# ═══════════════════════════════════════════════════════════════
# NACLI UI THEME
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>
    :root {
        --nacli-primary: #d4a574;
        --nacli-secondary: #8b6f47;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fef9f0 0%, #f4e4c1 100%);
        border-right: 3px solid var(--nacli-secondary);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--nacli-primary) 0%, var(--nacli-secondary) 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.title("⛏️ Nacli PokéApp v2")
    st.caption("*Clarity and Steadfastness*")
    
    st.markdown("---")
    
    # Mode Toggle
    st.session_state.mode = st.radio(
        "**Mode**",
        ["Library", "Builder"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if st.session_state.mode == "Library":
        # Music
        st.subheader("🎵 Music")
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
        
        st.markdown("---")
        
        # Pokemon selection
        all_entries = list_pokemon_entries()
        
        if all_entries:
            pokemon_names = [get_pokemon_name_from_path(entry) for entry in all_entries]
            
            if st.button("🎲 Random", use_container_width=True):
                st.session_state.current_pokemon = random.choice(all_entries)
                st.rerun()
            
            if st.session_state.current_pokemon:
                current_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
                try:
                    current_index = pokemon_names.index(current_name)
                except ValueError:
                    current_index = 0
            else:
                current_index = 0
            
            selected_pokemon = st.selectbox(
                "Select",
                pokemon_names,
                index=current_index,
                label_visibility="collapsed"
            )
            
            selected_index = pokemon_names.index(selected_pokemon)
            st.session_state.current_pokemon = all_entries[selected_index]
            
            st.info(f"**{len(all_entries)}** entries")
        else:
            st.warning("No entries yet")
        
        st.markdown("---")
        
        # Display settings
        st.subheader("⚙️ Display")
        st.session_state.preview_height = st.slider(
            "Height",
            400, 1200, st.session_state.preview_height, 50
        )
        
        st.session_state.safe_mode = st.toggle(
            "Safe Mode",
            value=st.session_state.safe_mode
        )

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════

if st.session_state.mode == "Library":
    # LIBRARY MODE
    
    if st.session_state.current_pokemon and st.session_state.current_pokemon.exists():
        pokemon_name = get_pokemon_name_from_path(st.session_state.current_pokemon)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            html_content = st.session_state.current_pokemon.read_text()
            st.download_button(
                label="💾 Download",
                data=html_content,
                file_name=st.session_state.current_pokemon.name,
                mime="text/html",
                use_container_width=True
            )
        
        with col2:
            if st.button("🗑️ Delete", use_container_width=True):
                st.session_state.current_pokemon.unlink()
                st.session_state.current_pokemon = None
                st.success(f"Deleted {pokemon_name}")
                st.rerun()
        
        with col3:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        
        st.title(f"⛏️ {pokemon_name}")
        
        # Preview in iframe
        html_content = st.session_state.current_pokemon.read_text()
        escaped_html = html.escape(html_content)
        
        if st.session_state.safe_mode:
            sandbox = 'allow-same-origin'
        else:
            sandbox = 'allow-scripts allow-same-origin'
        
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
                }}
            </style>
        </head>
        <body>
            <iframe srcdoc="{escaped_html}" sandbox="{sandbox}"></iframe>
        </body>
        </html>
        """
        
        st.components.v1.html(wrapper_html, height=st.session_state.preview_height + 20, scrolling=False)
        
        with st.expander("🔍 Debug: Raw HTML"):
            st.code(html_content, language="html")
    
    else:
        st.title("⛏️ Nacli PokéApp v2")
        st.subheader("Library Mode")
        
        st.info("👈 No Pokémon selected. Switch to **Builder** mode to create your first entry!")

else:
    # BUILDER MODE
    st.title("🔨 Builder Mode")
    st.caption("Generate self-contained Pokemon entries with embedded images")
    
    with st.form("pokemon_builder"):
        st.subheader("Core Identity")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            pokemon_name = st.text_input("Pokémon Name *", placeholder="Snivy")
        with col2:
            is_shiny = st.checkbox("✨ Shiny")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pokemon_type = st.selectbox("Type *", [
                "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
                "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock",
                "Ghost", "Dragon", "Dark", "Steel", "Fairy"
            ])
        with col2:
            generation = st.selectbox("Generation *", [f"Gen {i}" for i in range(1, 10)])
        with col3:
            variant = st.text_input("Variant", value="Sparkle" if is_shiny else "Normal")
        
        evolution_line = st.text_input("Evolution Line", placeholder="Snivy, Servine, Serperior")
        
        st.markdown("---")
        st.subheader("Trainer / Provenance")
        
        col1, col2 = st.columns(2)
        with col1:
            ot = st.text_input("OT (Original Trainer)")
            id_no = st.text_input("ID No.")
            first_met_location = st.text_input("First Met Location", placeholder="Galar region")
        with col2:
            first_met_date = st.date_input("First Met Date", value=date.today())
            nature = st.text_input("Nature", placeholder="Adamant")
            ability = st.text_input("Ability")
        
        characteristic = st.text_input("Characteristic")
        
        st.markdown("---")
        st.subheader("Stats")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            hp = st.number_input("HP", min_value=0, value=45)
        with col2:
            attack = st.number_input("Attack", min_value=0, value=45)
        with col3:
            defense = st.number_input("Defense", min_value=0, value=55)
        with col4:
            sp_atk = st.number_input("Sp. Atk", min_value=0, value=45)
        with col5:
            sp_def = st.number_input("Sp. Def", min_value=0, value=55)
        with col6:
            speed = st.number_input("Speed", min_value=0, value=63)
        
        st.markdown("---")
        st.subheader("Moves")
        
        move1 = st.text_input("Move 1", placeholder="Leaf Tornado")
        move2 = st.text_input("Move 2", placeholder="Leaf Blade")
        move3 = st.text_input("Move 3", placeholder="Coil")
        
        st.markdown("---")
        st.subheader("Traits")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            trait_a_label = st.text_input("Trait A Label", value="Trait A")
            trait_a_name = st.text_input("Trait A Name", placeholder="Overgrow")
            trait_a_desc = st.text_area("Trait A Description", placeholder="Powers up Grass moves in a pinch")
        with col2:
            trait_b_label = st.text_input("Trait B Label", value="Trait B")
            trait_b_name = st.text_input("Trait B Name")
            trait_b_desc = st.text_area("Trait B Description")
        with col3:
            trait_c_label = st.text_input("Trait C Label", value="Trait C")
            trait_c_name = st.text_input("Trait C Name")
            trait_c_desc = st.text_area("Trait C Description")
        
        submit = st.form_submit_button("🔨 Generate Entry", use_container_width=True)
    
    # Base64 Image Converter
    st.markdown("---")
    st.subheader("📦 Base64 Image Converter")
    st.caption("Upload images to embed directly into the HTML (self-contained)")
    
    converter_tab1, converter_tab2 = st.tabs(["Hero Image", "Gallery Images"])
    
    with converter_tab1:
        st.write("**Hero Image** (appears on Card tab)")
        
        hero_upload = st.file_uploader(
            "Upload Hero Image",
            type=['png', 'jpg', 'jpeg', 'webp'],
            key="hero_upload"
        )
        
        if hero_upload:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(hero_upload, caption="Preview", use_container_width=True)
            
            with col2:
                if st.button("Use as Hero Image", use_container_width=True):
                    st.session_state.hero_image_b64 = image_to_base64(hero_upload)
                    st.success("✅ Hero image set!")
                    st.rerun()
                
                if st.session_state.hero_image_b64:
                    st.success("Hero image loaded ✓")
                    if st.button("Clear Hero Image"):
                        st.session_state.hero_image_b64 = None
                        st.rerun()
    
    with converter_tab2:
        st.write("**Gallery Images** (appear on Gallery tab)")
        
        for i in range(6):
            with st.expander(f"Gallery Slot {i+1}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    gallery_upload = st.file_uploader(
                        f"Image {i+1}",
                        type=['png', 'jpg', 'jpeg', 'webp'],
                        key=f"gallery_{i}",
                        label_visibility="collapsed"
                    )
                    
                    caption = st.text_input(
                        f"Caption {i+1}",
                        key=f"caption_{i}",
                        placeholder="Optional caption"
                    )
                
                with col2:
                    if gallery_upload:
                        st.image(gallery_upload, use_container_width=True)
                        if st.button(f"Add to Slot {i+1}", key=f"add_gallery_{i}"):
                            st.session_state.gallery_items[i] = {
                                'b64': image_to_base64(gallery_upload),
                                'caption': caption
                            }
                            st.success(f"Added to slot {i+1}!")
                            st.rerun()
                    
                    if st.session_state.gallery_items[i]['b64']:
                        st.success(f"✓ Image loaded")
                        if st.button(f"Clear Slot {i+1}", key=f"clear_{i}"):
                            st.session_state.gallery_items[i] = {'b64': None, 'caption': ''}
                            st.rerun()
    
    # Generate HTML
    if submit:
        if not pokemon_name:
            st.error("⚠️ Pokemon Name is required!")
        else:
            # Prepare data
            data = {
                'name': pokemon_name,
                'is_shiny': is_shiny,
                'type': pokemon_type,
                'generation': generation,
                'variant': variant,
                'evolution_line': evolution_line,
                'ot': ot,
                'id_no': id_no,
                'first_met_location': first_met_location,
                'first_met_date': first_met_date.strftime('%Y-%m-%d'),
                'nature': nature,
                'ability': ability,
                'characteristic': characteristic,
                'stats': {
                    'hp': hp,
                    'attack': attack,
                    'defense': defense,
                    'sp_atk': sp_atk,
                    'sp_def': sp_def,
                    'speed': speed
                },
                'moves': [move1, move2, move3],
                'traits': [
                    {'label': trait_a_label, 'name': trait_a_name, 'description': trait_a_desc},
                    {'label': trait_b_label, 'name': trait_b_name, 'description': trait_b_desc},
                    {'label': trait_c_label, 'name': trait_c_name, 'description': trait_c_desc}
                ],
                'hero_image_b64': st.session_state.hero_image_b64,
                'gallery_items': st.session_state.gallery_items
            }
            
            # Generate HTML
            html_output = generate_pokemon_html(data)
            
            # Save to file
            filename_stem = safe_stem(pokemon_name)
            if is_shiny:
                filename = f"{filename_stem}_shiny_{datetime.now().strftime('%Y%m%d')}.html"
            else:
                filename = f"{filename_stem}_{datetime.now().strftime('%Y%m%d')}.html"
            
            file_path = ENTRIES_DIR / filename
            file_path.write_text(html_output)
            
            st.success(f"✅ Entry created: {filename}")
            
            # Auto-load into preview
            st.session_state.current_pokemon = file_path
            st.session_state.mode = "Library"
            
            # Reset builder state
            st.session_state.hero_image_b64 = None
            st.session_state.gallery_items = [{'b64': None, 'caption': ''} for _ in range(6)]
            
            st.rerun()
