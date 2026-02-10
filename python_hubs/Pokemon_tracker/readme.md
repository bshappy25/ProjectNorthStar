# ⛏️ Nacli PokéApp

**Clarity and Steadfastness**

A Streamlit-based Pokémon viewer with iframe rendering, in-app HTML editing, image management, and Nacli-inspired UI.

---

## 🎯 Philosophy

Inspired by the Nacli evolution line (Rock Salt Pokémon), this app embodies:
- **Clarity**: Clean code, clear purpose, transparent workflow
- **Steadfastness**: Reliable file storage, solid structure, persistent data

---

## ✨ Key Features

### Core Functionality
✅ **iframe Preview** - Safely render HTML entries with sandboxing  
✅ **In-App HTML Editor** - Edit entries without leaving the app  
✅ **Image Upload & Management** - Upload images and get insertion code  
✅ **Type & Generation Filtering** - Sort your Pokémon collection  
✅ **Random Picker** - Get random Pokémon from filtered results  
✅ **Background Music** - MP3/WAV support with auto-loop  
✅ **Safe Mode Toggle** - Enable/disable JavaScript in previews  
✅ **Download & Delete** - Full file management  

### What Makes This Different

**Compared to the old version:**
- ✅ **Actual iframe rendering** (like your teacher_tools app)
- ✅ **Direct HTML editing** in the app interface
- ✅ **Image upload helper** with code generation
- ✅ **Nacli-themed UI** (warm earth tones, salt crystal aesthetics)
- ✅ **Better UX** with action buttons and confirmations
- ✅ **Preview height slider** for custom viewing
- ✅ **Proper sandbox controls** for security

---

## 📁 Directory Structure

```
Pokemon_tracker/
│
├─ Pokeapp.py              # Main Streamlit app
│
├─ pokemon_entries/        # HTML files for each Pokémon
│   └─ nacli.html          # Sample: Nacli evolution line
│
├─ images/                 # Uploaded images for use in HTML
│   └─ (your images here)
│
├─ music/                  # Background music files
│   └─ (your .mp3/.wav files)
│
├─ screenshots/            # Future: screenshot exports
│
└─ README.md               # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install streamlit
```

### 2. Run the App

```bash
cd python_hubs/Pokemon_tracker
streamlit run Pokeapp.py
```

### 3. First Steps

1. Click **"➕ Create New Entry"** in sidebar
2. Enter a Pokémon name (e.g., "Pikachu")
3. Select type and generation
4. Click **"Create"**
5. View your Pokémon in the iframe!

---

## 🎮 How to Use

### Creating Pokémon Entries

#### Method 1: Use the Sidebar Tool (Easiest)
1. Expand **"➕ Create New Entry"**
2. Fill in:
   - Pokémon Name
   - Type
   - Generation
   - Evolution Line (comma-separated)
3. Click **"Create"**
4. A basic HTML file is generated automatically
5. Edit it using the **"📝 Edit HTML"** button

#### Method 2: Manual HTML Creation
1. Create a file in `pokemon_entries/`
2. Name it: `{pokemon_name}.html`
3. Include metadata in HTML comments:
   ```html
   <!-- TYPE: Fire -->
   <!-- GENERATION: Gen 1 -->
   <!-- EVOLUTION_LINE: Charmander, Charmeleon, Charizard -->
   ```
4. Design your HTML however you want!

---

### Editing HTML In-App

1. **Select** a Pokémon from the sidebar
2. Click **"📝 Edit HTML"** at the top
3. **Edit** the HTML in the text area
4. Click **"💾 Save Changes"** or **"❌ Cancel"**

The preview updates immediately on save!

---

### Adding Images

#### Upload Images
1. Click **"📸 Upload Image"** in sidebar
2. Choose an image file (PNG, JPG, GIF, WebP)
3. Click **"💾 Save Image"**
4. Image is saved to `images/` folder

#### Insert Images into HTML
1. Click **"🖼️ Insert Image"** at the top
2. Select an image from the dropdown
3. Copy the generated `<img>` code
4. Click **"📝 Edit HTML"**
5. Paste the code where you want the image
6. Save!

**Generated Code Example:**
```html
<img src="../images/pikachu.png" alt="pikachu.png" style="max-width: 100%;">
```

---

### Filtering & Randomization

#### Filter Pokémon
- **Type Filter**: Choose from 18 Pokémon types
- **Generation Filter**: Gen 1 through Gen 9
- Filters are **additive** (AND logic)

#### Random Pokémon
1. Set your filters (or leave as "All")
2. Click **"🎲 Random Pokémon"**
3. A random entry from filtered results appears

---

### Display Settings

#### Preview Height
- Adjust the slider: **400px - 1200px**
- Changes apply immediately to the iframe

#### Safe Mode
- **ON** (default): Scripts disabled, forms blocked
  - Sandbox: `allow-same-origin` only
  - Safe for untrusted HTML
- **OFF**: Scripts enabled, interactive features work
  - Sandbox: Full permissions
  - Use for advanced HTML entries

---

### File Management

#### Download HTML
1. Select a Pokémon
2. Click **"💾 Download"**
3. Save the standalone HTML file
4. Can be opened in any browser

#### Delete Entry
1. Select a Pokémon
2. Click **"🗑️ Delete"**
3. Confirm deletion
4. File is permanently removed

---

## 🎨 Nacli UI Theme

The app uses warm earth tones inspired by rock salt and minerals:

### Color Palette
- **Primary**: `#d4a574` (Sandy brown)
- **Secondary**: `#8b6f47` (Earth brown)
- **Accent**: `#f4e4c1` (Salt crystal)
- **Dark**: `#5c4a2f` (Deep earth)
- **Light**: `#fef9f0` (White salt)

### Design Elements
- Gradient backgrounds (earth → salt)
- Rounded corners (8px-20px)
- Border accents (2-3px)
- Hover effects (translateY, shadows)
- Button gradients (brown → gold)

---

## 📝 HTML Entry Structure

### Required Metadata

Every HTML file needs these comments at the top:

```html
<!-- TYPE: Fire -->
<!-- GENERATION: Gen 4 -->
<!-- EVOLUTION_LINE: Chimchar, Monferno, Infernape -->
```

### Metadata Fields

| Field | Format | Example |
|-------|--------|---------|
| `TYPE` | Single word | `Water`, `Electric`, `Dragon` |
| `GENERATION` | `Gen X` (1-9) | `Gen 3`, `Gen 7` |
| `EVOLUTION_LINE` | Comma-separated | `Squirtle, Wartortle, Blastoise` |

### Evolution Line Rules

**One file per evolution branch:**
- ✅ `bulbasaur.html` contains: Bulbasaur, Ivysaur, Venusaur
- ✅ `eevee.html` contains: Eevee, all Eeveelutions
- ❌ Don't create separate files for each stage

---

## 🎵 Background Music

### Adding Music

1. Get `.mp3` or `.wav` files
2. Place them in the `music/` folder
3. Refresh the app
4. Select from dropdown in sidebar

### Music Player
- Auto-loop enabled
- Volume controls
- Play/pause
- Works while browsing entries

### Recommended Sources
- Pokémon OST (route themes, town themes)
- Royalty-free music (YouTube Audio Library)
- Lo-fi beats
- Nature sounds

---

## 🔧 Advanced Usage

### Custom Styling

Each HTML entry can have its own CSS:

```html
<style>
    body {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-family: 'Inter', sans-serif;
        padding: 2rem;
    }
    
    .pokemon-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
    }
</style>
```

### Using JavaScript (Safe Mode OFF)

With Safe Mode disabled, you can add interactivity:

```html
<script>
    function evolve() {
        alert("Your Pokémon is evolving!");
    }
</script>

<button onclick="evolve()">Evolve!</button>
```

**⚠️ Warning:** Only disable Safe Mode for HTML you trust!

### Responsive Design

Make entries mobile-friendly:

```html
<style>
    @media (max-width: 768px) {
        .pokemon-card {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
    }
</style>
```

---

## 🐛 Troubleshooting

### "No Pokémon entries found"
- **Cause**: Empty `pokemon_entries/` folder
- **Fix**: Create an entry using sidebar tool

### Image not showing in HTML
- **Cause**: Wrong file path
- **Fix**: Use `../images/{filename}` as the path
- **Example**: `<img src="../images/pikachu.png">`

### Music not playing
- **Cause**: No music files or wrong format
- **Fix**: Add `.mp3` or `.wav` to `music/` folder

### Preview looks broken
- **Cause**: HTML syntax error
- **Fix**: Use "🔍 Debug" expander to check raw HTML

### Can't delete Pokémon
- **Cause**: File permissions
- **Fix**: Check file isn't open in another app

---

## 📚 Example: Nacli Line

The app includes a **flagship example**: `nacli.html`

Features demonstrated:
- Evolution grid (3 stages)
- Custom gradients (earth tones)
- Stats section
- Story/lore section
- Responsive cards
- Hover effects
- Typography hierarchy

**View it to see best practices!**

---

## 🎯 Best Practices

### File Naming
- Use lowercase: `pikachu.html` not `Pikachu.html`
- Replace spaces with underscores: `mega_charizard_x.html`
- Keep under 50 characters
- Be descriptive: `bulbasaur_line.html`

### HTML Structure
1. Start with metadata comments
2. Include `<style>` for custom CSS
3. Use semantic HTML (`<header>`, `<section>`, etc.)
4. Make it responsive
5. Add alt text to images

### Image Management
- Use web-friendly formats (PNG, JPG, WebP)
- Optimize file sizes (< 2MB recommended)
- Use descriptive filenames: `charizard_flying.png`
- Include alt text for accessibility

### Evolution Lines
- Put all stages in ONE file
- Use grid/flex layouts to show progression
- Include evolution methods (level, stone, trade)
- Show visual differences between stages

---

## 🚀 Future Features

Planned enhancements:
- ⏳ PNG screenshot export (Selenium/Playwright)
- ⏳ Batch image upload
- ⏳ Template library (pre-made HTML templates)
- ⏳ Stats calculator integration
- ⏳ Move list database
- ⏳ Type matchup calculator
- ⏳ Shiny variant toggle

---

## 🙏 Credits

**Inspired by:**
- Your `teacher_tools` app (iframe pattern, Palm ID gate)
- Nacli evolution line (Gen 9 Pokémon)
- Rock salt aesthetics (earth tones, mineral textures)

**Pokémon** is a trademark of Nintendo/Game Freak/Creatures Inc.

This is a fan-made tool for personal collection management.

---

## 📖 Quick Reference

### Supported Types
Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy

### Supported Generations
Gen 1 (Kanto), Gen 2 (Johto), Gen 3 (Hoenn), Gen 4 (Sinnoh), Gen 5 (Unova), Gen 6 (Kalos), Gen 7 (Alola), Gen 8 (Galar), Gen 9 (Paldea)

### File Formats
- **Pokémon Entries**: `.html`
- **Music**: `.mp3`, `.wav`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`

### Keyboard Shortcuts
- None yet (future feature)

---

**"Under pressure, we do not break—we crystallize into something greater."**  
*— The Nacli Philosophy*

⛏️ **Happy Pokémon collecting!** ⛏️
