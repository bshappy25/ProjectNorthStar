# 🪟 Glassy Library

**Universal Gray Glass UI Shell** - Ultra-clean viewer for Nacli-generated Pokemon cards

---

## 🎯 Purpose

This is a **VIEW-ONLY** app - a beautiful display shell for Pokemon cards created in the **Nacli Builder** app.

### Two-App System:
1. **Nacli PokéApp** (`Pokeapp.py`) → Builder mode for creating cards
2. **Glassy Library** (`GlassyLibrary.py`) → Clean viewer for displaying cards

---

## ✨ Features

### 🪟 Ultra-Clean Aesthetic
- Apple-like glassy design
- Universal gray base with tint variations
- Backdrop blur effects
- Smooth animations
- Minimal UI, maximum clarity

### 🎨 UI Tint System
Choose from 5 color variations:
- **Universal Gray** (default)
- **Water (Blue)**
- **Fire (Orange)**
- **Fairy/Psychic (Pink)**
- **Grass (Green)**
- **Electric (Yellow)**

### 🔒 Palm ID Admin Gate
- Tap 🖐️ button **3 times** to reveal admin panel
- Enter code: `Bshapp`
- Unlock admin tools (delete, etc.)
- Reset to lock again

### 🗑️ Admin Tools (NON-NEGOTIABLE)
Once unlocked:
- **✖ Delete button** appears on cards
- Safely remove entries
- Confirmation built-in

---

## 🚀 Quick Start

```bash
# Same directory as Nacli Builder
cd python_hubs/Pokemon_tracker

# Run the Glassy Library
streamlit run GlassyLibrary.py
```

**Note:** Make sure you have Pokemon cards in `pokemon_entries/` folder (created by Nacli Builder)

---

## 📖 How to Use

### Step 1: Create Cards (Nacli Builder)
```bash
streamlit run Pokeapp.py
```
- Switch to Builder mode
- Fill in Pokemon details
- Upload images
- Generate HTML cards

### Step 2: View Cards (Glassy Library)
```bash
streamlit run GlassyLibrary.py
```
- Cards automatically appear in library
- Select from dropdown or use random button
- Change UI tint to match Pokemon type
- Preview with full tab functionality

---

## 🎨 UI Tint Guide

Match the tint to your Pokemon's vibe:

| Tint | Best For | Color |
|------|----------|-------|
| Universal Gray | Default, all types | Slate gray |
| Water (Blue) | Water, Ice types | Cool blue |
| Fire (Orange) | Fire types | Warm orange |
| Fairy/Psychic (Pink) | Fairy, Psychic types | Soft pink |
| Grass (Green) | Grass types | Natural green |
| Electric (Yellow) | Electric types | Electric yellow |

---

## 🔒 Admin Features

### Unlocking Admin Mode
1. Click 🖐️ button in top-right of sidebar
2. Click **3 times** (tap counter)
3. Admin panel appears
4. Enter code: `Bshapp`
5. Click "Unlock"

### Admin Tools Available
- ✖ **Delete button** (appears next to Download)
- Removes HTML files safely
- No confirmation dialog (be careful!)

### Locking Again
- Click "Reset" button in admin panel
- Palm taps reset to 0
- Admin box disappears

---

## 📐 Display Settings

### Preview Height Slider
- Adjust iframe height: **400px - 1200px**
- Default: 800px
- Changes apply immediately

### Download Cards
- Every card has a Download button
- Saves as standalone HTML file
- Fully self-contained (images embedded)

---

## 🎯 Design Philosophy

### Glassiness
- `backdrop-filter: blur(20px)`
- Semi-transparent backgrounds
- Layered depth
- Soft shadows

### Universal Gray
- Works with any Pokemon type
- Professional appearance
- Apple-inspired
- Focus on content, not UI

### Minimalism
- No clutter
- Clean spacing
- Smooth transitions
- Purposeful interactions

---

## 🔧 Technical Details

### File Structure
```
pokemon_entries/
├─ snivy_shiny_20260211.html
├─ pikachu_20260211.html
└─ garganacl_20260211.html
```

All HTML files in this folder appear in the library automatically.

### Iframe Rendering
- Scripts enabled (tabs work)
- Sandboxed for security
- Rounded corners
- Shadow effects

### Session State
- `palm_taps`: Admin gate counter
- `admin_unlocked`: Admin status
- `ui_tint`: Selected color scheme
- `current_tool`: Active card
- `preview_height`: Iframe height

---

## 📦 Batch Loading (Future)

From the README spec:
> "On GitHub I can load a batch of premade cards"

### How This Will Work:
1. Download pre-made HTML cards from GitHub
2. Place them in `pokemon_entries/` folder
3. Refresh Glassy Library
4. Cards appear automatically!

### Gallery Mode (Planned)
- Grid view of all cards
- Thumbnail previews
- Quick navigation

### User Gallery Mode (Planned)
- Personal collections
- Favorites system
- Custom organization

---

## 🎨 CSS Variables

The tint system uses these CSS variables:
```css
--bg0: Background start
--bg1: Background end
--text: Text color
--glass: Primary glass effect
--glass2: Secondary glass effect
--r1: Border radius large (22px)
--r2: Border radius small (16px)
--shadow: Large shadow
--shadow2: Small shadow
```

---

## 🆚 Nacli vs Glassy Library

| Feature | Nacli Builder | Glassy Library |
|---------|---------------|----------------|
| Purpose | Create cards | View cards |
| Mode | Builder + Library | View only |
| Aesthetic | Earth tones | Gray glass |
| Editing | Full HTML editor | Read-only |
| Images | Base64 converter | Display only |
| Admin | None | Palm ID gate |

---

## 🚧 Future Enhancements

- [ ] Gallery grid view
- [ ] User collections
- [ ] Favorites system
- [ ] Search/filter
- [ ] Card comparison
- [ ] Export to PDF
- [ ] Batch operations

---

## 💡 Tips

### Best Practices
- Keep UI tint on "Universal Gray" for consistency
- Use admin tools sparingly
- Download important cards as backup
- Preview at different heights to test responsive design

### Troubleshooting
- **No cards showing?** → Create some in Nacli Builder first
- **Tabs not working?** → Check if HTML has JavaScript
- **Admin won't unlock?** → Make sure you're typing `Bshapp` exactly

---

**Simple. Clean. Glassy. 🥤**

🪟 **Enjoy your Pokemon library!**
