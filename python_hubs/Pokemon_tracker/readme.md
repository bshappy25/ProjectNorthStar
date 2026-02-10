# 🔮 Pokémon Viewer App

A Streamlit-based Pokémon viewing and tracking application with HTML-based storage, theme switching, filtering, randomization, and music support.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation & Setup](#installation--setup)
- [How to Use](#how-to-use)
- [Pokémon Entry System](#pokémon-entry-system)
- [Theme System](#theme-system)
- [Music System](#music-system)
- [Screenshot System](#screenshot-system)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This app provides a beautiful, interactive way to view and organize your Pokémon collection. Each Pokémon (or evolution line) is stored as a separate HTML file with embedded metadata for filtering and sorting.

### Key Philosophy
- **One File Per Evolution Line**: Bulbasaur, Ivysaur, and Venusaur share one HTML file
- **HTML-Based Storage**: Each entry is a self-contained HTML document
- **Theme Flexibility**: 5 distinct visual themes based on Pokémon type energies
- **Filter & Randomize**: Sort by type and generation, or get a random Pokémon

---

## ✨ Features

### Core Features
✅ **HTML File Storage** - Each Pokémon/evolution line stored as `.html` file  
✅ **Metadata System** - Type and generation stored in HTML comments  
✅ **Filtering** - Filter by Pokémon type (18 types) and generation (Gen 1-9)  
✅ **Randomization** - Random Pokémon picker respects active filters  
✅ **5 Theme Variants** - Water, Grass, Fire, Normal, Psychic/Fairy themes  
✅ **Background Music** - MP3/WAV support with in-app player  
✅ **Screenshot Markers** - Track when you viewed each Pokémon  
✅ **HTML Export** - Download any entry as standalone HTML  
✅ **In-App Creation** - Create new Pokémon entries directly in the sidebar  

### Planned Features
⏳ **PNG Screenshot Export** (requires Selenium/Playwright)  
⏳ **Animated Image Support** (GIF, WebP, sprite layers)  
⏳ **Pokémon Stats Integration**  
⏳ **Battle Move Lists**  

---

## 📁 Directory Structure

```
Pokemon_tracker/
│
├─ Pokeapp.py                 # Main Streamlit application
│
├─ pokemon_entries/           # HTML files for each Pokémon
│   ├─ garganacl.html         # Example: Rock-type, Gen 9
│   ├─ bulbasaur.html         # Example: Grass-type, Gen 1 (full evolution line)
│   ├─ pikachu.html           # Example: Electric-type, Gen 1
│   └─ {your_pokemon}.html    # Add more here!
│
├─ themes/                    # CSS theme files
│   ├─ water.css              # 🌊 Calm, reflective theme
│   ├─ grass.css              # 🌿 Grounded, natural theme
│   ├─ fire.css               # 🔥 Intense, powerful theme
│   ├─ normal.css             # ⚪ Clean, utilitarian theme (default)
│   └─ psychic_fairy.css      # ✨ Mystical, ethereal theme
│
├─ music/                     # Background music files
│   ├─ README.md              # Music folder instructions
│   └─ {your_music}.mp3       # Add .mp3 or .wav files here
│
├─ screenshots/               # Screenshot markers (future: PNG exports)
│   ├─ README.md              # Screenshots folder instructions
│   └─ {pokemon}_{time}.txt   # Screenshot markers
│
├─ assets/                    # Shared assets (images, etc.)
│   └─ README.txt             # Assets folder instructions
│
└─ README.md                  # This file
```

---

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install streamlit
```

### 2. Navigate to the App

```bash
cd python_hubs/Pokemon_tracker
```

### 3. Run the App

```bash
streamlit run Pokeapp.py
```

### 4. Open in Browser

The app will automatically open at `http://localhost:8501`

---

## 🎮 How to Use

### Basic Workflow

1. **Launch the app** using `streamlit run Pokeapp.py`
2. **Select a theme** from the sidebar (default: Normal)
3. **Choose filters** (Type and/or Generation)
4. **Pick a Pokémon** from the dropdown OR click "🎲 Random Pokémon"
5. **View the entry** in the main area
6. **Take actions**: Screenshot, Download HTML, or Refresh

### Sidebar Controls

#### 🎵 Background Music
- Select from available music tracks
- Control playback with audio player
- Music loops automatically

#### 🔍 Filters
- **Type Filter**: All Types, Normal, Fire, Water, etc. (18 types)
- **Generation Filter**: All Generations, Gen 1-9

#### 🎨 Theme
- Choose from 5 energy-based themes
- Theme applies immediately to the current view

#### 📋 Select Pokémon
- **🎲 Random Pokémon**: Picks random entry from filtered results
- **Dropdown**: Manual selection from filtered list
- **Info Display**: Shows "X of Y Pokémon" matching filters

#### ➕ Add New Pokémon
- Enter Pokémon name
- Select type and generation
- Input evolution line (comma-separated)
- Click "Create Sample Entry" to generate HTML file

### Action Buttons

#### 📸 Screenshot
- Creates a marker file in `screenshots/` folder
- Records: Pokémon name, timestamp, active theme
- (PNG export planned for future)

#### 💾 Download HTML
- Download the current Pokémon entry as standalone HTML
- File can be opened in any browser
- Useful for sharing or backup

#### 🔄 Refresh
- Reload the current view
- Useful after editing files manually

---

## 📝 Pokémon Entry System

### HTML File Structure

Each Pokémon entry is a self-contained HTML file with embedded metadata.

#### Required Metadata (in HTML comments)

```html
<!-- TYPE: Electric -->
<!-- GENERATION: Gen 1 -->
<!-- EVOLUTION_LINE: Pichu, Pikachu, Raichu -->
```

#### Metadata Fields

| Field | Format | Example |
|-------|--------|---------|
| `TYPE` | Single word | `Fire`, `Water`, `Grass` |
| `GENERATION` | `Gen X` where X is 1-9 | `Gen 1`, `Gen 9` |
| `EVOLUTION_LINE` | Comma-separated names | `Bulbasaur, Ivysaur, Venusaur` |

### Creating New Entries

#### Option 1: Use the Sidebar Tool (Easiest)
1. Click "➕ Add New Pokémon" in sidebar
2. Fill in the form
3. Click "Create Sample Entry"
4. Edit the generated HTML file for customization

#### Option 2: Manually Create HTML File

1. Create a new file in `pokemon_entries/` folder
2. Name it: `{pokemon_name}.html` (use lowercase, underscores for spaces)
3. Include required metadata in HTML comments
4. Design your HTML content however you want!

#### Example Minimal Template

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Charizard</title>
    <!-- TYPE: Fire -->
    <!-- GENERATION: Gen 1 -->
    <!-- EVOLUTION_LINE: Charmander, Charmeleon, Charizard -->
    <style>
        body { 
            background: linear-gradient(135deg, #dc2626, #f97316);
            color: white;
            font-family: sans-serif;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <h1>Charizard</h1>
    <p>The Flame Pokémon</p>
    <!-- Add your custom content here -->
</body>
</html>
```

### Evolution Lines

**Important Rule**: Different Pokémon of the same evolutionary branch are contained in ONE file.

✅ **Correct**: 
- `bulbasaur.html` contains Bulbasaur, Ivysaur, AND Venusaur
- `pikachu.html` contains Pichu, Pikachu, AND Raichu

❌ **Incorrect**:
- `bulbasaur.html`, `ivysaur.html`, `venusaur.html` as separate files

**Why?** This keeps related Pokémon together and makes the app cleaner.

---

## 🎨 Theme System

### Available Themes

#### 🌊 WATER
- **Vibe**: Calm, reflective, crystalline
- **Colors**: Slate → Aqua gradient with cyan accents
- **Use Case**: Observation mode, studying stats
- **Layout**: Centered with glass card effect
- **Typography**: Sans-serif with letter spacing

#### 🌿 GRASS
- **Vibe**: Stable, grounded, growth
- **Colors**: Moss green → Sage with stone accents
- **Use Case**: Daily logs, long-form entries
- **Layout**: Split (image left, text right on desktop)
- **Typography**: Serif for subtitles, sans for data

#### 🔥 FIRE
- **Vibe**: Power, intensity, declaration
- **Colors**: Charcoal → Ember red with molten orange
- **Use Case**: Highlights, shinies, legendary Pokémon
- **Layout**: Large centered with overlay text
- **Typography**: Heavy sans-serif, all caps titles

#### ⚪ NORMAL
- **Vibe**: Clean, neutral, utilitarian
- **Colors**: Light gray / off-white
- **Use Case**: Baseline testing, debugging, fast loading
- **Layout**: Simple card (DEFAULT FALLBACK)
- **Typography**: System default

#### ✨ PSYCHIC/FAIRY
- **Vibe**: Mythic clarity, higher meaning
- **Colors**: Lavender → Pale pink with gold accents
- **Use Case**: Narrative entries, symbolic days
- **Layout**: Centered with soft halo effect
- **Typography**: Elegant serif for titles

### Customizing Themes

Edit any CSS file in the `themes/` folder:

```css
/* themes/fire.css */
body {
    background: linear-gradient(135deg, #1c1917 0%, #dc2626 100%);
}

.pokemon-name {
    color: #fafaf9;
    font-size: 3.5rem;
    text-shadow: 0 0 20px rgba(234, 88, 12, 0.8);
}
```

Changes take effect on next refresh (🔄 button).

---

## 🎵 Music System

### Adding Music

1. **Get music files** (.mp3 or .wav format)
2. **Place them** in the `music/` folder
3. **Refresh the app**
4. **Select track** from sidebar dropdown

### Music Player Features

- ▶️ Play/Pause controls
- 🔁 Auto-loop enabled
- 🔊 Volume control
- 📁 Multiple track support

### Recommended Music Types

- **Pokémon OST**: Route themes, town themes, battle music
- **Ambient**: Nature sounds, lo-fi beats
- **Type-based**: Match music to current Pokémon type

### Copyright Notice

⚠️ Only use music you have rights to:
- Original compositions
- Royalty-free music
- Licensed music
- Creative Commons

See `music/README.md` for royalty-free music sources.

---

## 📸 Screenshot System

### Current Functionality: Markers

The app currently creates **screenshot markers** (text files) that record:
- Pokémon name
- Timestamp
- Active theme

Location: `screenshots/{pokemon_name}_{timestamp}.txt`

### Future: PNG Screenshots

To enable PNG export, install:

```bash
# Option 1: Selenium (recommended)
pip install selenium webdriver-manager pillow

# Option 2: Playwright
pip install playwright
playwright install
```

Future PNG files will be saved as:
```
screenshots/{pokemon_name}_{theme}_{timestamp}.png
```

---

## 🔧 Advanced Usage

### Filtering Logic

Filters are **additive** (AND logic):
- Type: Fire + Generation: Gen 1 = Only Gen 1 Fire types
- Type: All + Generation: Gen 9 = All Gen 9 Pokémon
- Type: Water + Generation: All = All Water types

### Random Pokémon Behavior

The 🎲 Random button:
1. Applies current filters first
2. Selects randomly from filtered results
3. Updates immediately

**Example**: With "Type: Electric" + "Gen 1" filters, random will only pick from Gen 1 Electric types.

### HTML Safe Rendering

Pokémon HTML is rendered in a **sandboxed iframe** with `allow-same-origin` only. This means:
- ✅ HTML/CSS works
- ❌ JavaScript won't execute (security)
- ❌ Forms won't submit
- ❌ External links are restricted

To change this, edit the `render_pokemon_html()` function in `Pokeapp.py`.

### Debugging Tips

#### View Source
Use the "🔍 Debug: View Source" expander to:
- See the raw HTML of current Pokémon
- Check metadata is formatted correctly
- Debug CSS issues

#### File Naming
- Use lowercase for filenames
- Replace spaces with underscores
- Keep names under 50 characters
- Example: `mega_charizard_x.html`

---

## 🐛 Troubleshooting

### Common Issues

#### "No Pokémon entries found"
- **Cause**: No `.html` files in `pokemon_entries/` folder
- **Fix**: Use "➕ Add New Pokémon" or manually add HTML files

#### "No Pokémon match your filters"
- **Cause**: Filters exclude all entries
- **Fix**: Change Type or Generation to "All"

#### Music not playing
- **Cause**: No music files or wrong format
- **Fix**: Add `.mp3` or `.wav` files to `music/` folder

#### Theme not changing
- **Cause**: CSS file missing or incorrectly named
- **Fix**: Check `themes/` folder for corresponding `.css` file

#### Pokémon not appearing in list
- **Cause**: Missing or incorrect metadata
- **Fix**: Check HTML comments have correct format:
  ```html
  <!-- TYPE: Fire -->
  <!-- GENERATION: Gen 1 -->
  <!-- EVOLUTION_LINE: Charmander, Charmeleon, Charizard -->
  ```

---

## 📚 Quick Reference

### Supported Types
Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy

### Supported Generations
Gen 1 (Kanto), Gen 2 (Johto), Gen 3 (Hoenn), Gen 4 (Sinnoh), Gen 5 (Unova), Gen 6 (Kalos), Gen 7 (Alola), Gen 8 (Galar), Gen 9 (Paldea)

### File Formats
- Pokémon Entries: `.html`
- Music: `.mp3`, `.wav`
- Themes: `.css`
- Screenshots: `.txt` (markers), `.png` (future)

---

## 🎯 Next Steps

1. **Add more Pokémon**: Create HTML files for your favorites
2. **Customize themes**: Edit CSS to match your style
3. **Add music**: Drop in your favorite Pokémon soundtracks
4. **Share entries**: Export HTML files to share with friends

---

## 📄 License & Credits

Created for tracking and viewing Pokémon collections.

**Pokémon** is a trademark of Nintendo/Game Freak/Creatures Inc.

This is a fan-made tool for personal use.

---

**Happy Pokémon viewing! 🔮⚡🌟**
