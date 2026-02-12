# ⚫ ONYX HUB - Streamlit Application

**Embrace Dark • Rise Elite**

The ultimate dark-themed Streamlit hub with military-grade aesthetics and maximum security clearance features.

---

## 🎨 Features

### Main Hub
- **ONYX Aesthetic**: Sleek black with cyan accents (#64ffff)
- **Cyberpunk Design**: Grid overlays, scan lines, glowing effects
- **Palm ID Security**: Elite-level authentication system
- **Modular Architecture**: Encrypted, secure, professional

### Included Apps
1. **🛠️ ONYX Dark Tools**
   - Dark Enhance (low-light optimization)
   - Dark Markup (stealth annotations)
   - Dark Collage (shadow compositions)
   - AI Dark Studio (neural art - Elite access)

2. **🔒 ONYX Vault**
   - Secure file storage
   - Military-grade encryption display
   - Multiple view modes (Grid, List, Inspect)
   - File metadata and hashing

3. **⚫ ONYX Elite** (Admin Only)
   - Command Center dashboard
   - Black Ops mission control
   - Classified intel system
   - Maximum clearance operations

---

## 🎨 Color Scheme

```css
/* Primary Colors */
Background: #0a0a0a → #1a1a1a (deep black gradient)
Accent: #64ffff (cyan)
Secondary: #c8c8c8 (silver)

/* Effects */
Glow: rgba(100, 255, 255, 0.3)
Borders: rgba(100, 255, 255, 0.2)
Cards: rgba(20, 20, 20, 0.9)
```

---

## 🚀 Setup & Installation

### 1. Install Dependencies

```bash
pip install streamlit pillow
```

### 2. Run the Application

```bash
streamlit run onyx_app.py
```

### 3. Access the Hub

Opens at `http://localhost:8501`

---

## 🔐 Admin Access

**Default Admin Code**: `ONYX2026`

### Unlock Process:
1. Tap 🖐️ palm button **3 times**
2. Enter admin code: `ONYX2026`
3. Click "🔓 Unlock"

### Change Admin Code:
Edit line 20 in `onyx_app.py`:
```python
ADMIN_CODE_HASH = hashlib.sha256("YOUR_CODE".encode()).hexdigest()
```

---

## 📁 File Structure

```
onyx_project/
│
├── onyx_app.py           # Main ONYX hub
├── onyx_tools.py         # Dark creative tools
├── onyx_vault.py         # Secure file vault
└── onyx_elite.py         # Elite access module
```

---

## 🎯 Features by Module

### 🛠️ ONYX Dark Tools
- Low-light image enhancement
- High-contrast markup system
- Shadow-optimized collages
- AI neural art (cyberpunk themes)
- Dark mode color grading

### 🔒 ONYX Vault
- Secure file upload/viewing
- Encryption status display
- File hashing (MD5)
- Grid/List/Inspect view modes
- Metadata analysis

### ⚫ ONYX Elite
- Command center dashboard
- Black ops mission interface
- Session/operation tracking
- Classified intel system
- Stealth metrics

---

## 🎨 Design Philosophy

**ONYX represents:**
- **Professionalism**: Clean, corporate, elite
- **Security**: Military-grade aesthetics
- **Mystery**: Dark, sleek, sophisticated
- **Power**: Maximum clearance, black ops

**Visual Language:**
- Scan line animations
- Grid overlays
- Glowing cyan accents
- Deep black backgrounds
- Minimalist interface

---

## 🔧 Customization

### Change Accent Color

Replace all instances of `#64ffff` (cyan) with your color:

```css
/* Accent color examples */
#64ffff → Cyan (current)
#00ff00 → Matrix green
#ff0080 → Hot pink
#ffaa00 → Amber
```

### Adjust Security Theme

Edit `onyx_elite.py` for different lock screens:
- Change denied color from red to your choice
- Modify clearance badges
- Adjust threat levels

---

## 💡 Integration Notes

### Adding Dark HTML Tools

Place dark-themed versions of your tools:
- Use `#0a0a0a` background
- Cyan accents `#64ffff`
- High contrast text
- Minimal UI chrome

### File Encryption

ONYX Vault displays encryption status:
- Real encryption can be added via `cryptography` library
- Current system shows visual indicators only

---

## 🎭 ONYX vs AMETHYST

| Feature | ONYX | AMETHYST |
|---------|------|----------|
| Theme | Dark/Black | Purple/Hazy |
| Vibe | Professional/Elite | Creative/Dreamy |
| Colors | Cyan/Silver | Purple/Pink |
| Font | Orbitron/Rajdhani | Comfortaa/Quicksand |
| Use Case | Business/Security | Education/Art |

---

## 🚀 Future Enhancements

- [ ] Real file encryption
- [ ] Dark theme HTML tool integration
- [ ] Advanced mission simulator
- [ ] Network monitoring dashboard
- [ ] Threat intelligence feed
- [ ] Encrypted messaging system

---

## 📝 Notes

- **Scan line**: Animated effect for cyberpunk feel
- **Grid overlay**: Subtle background pattern
- **Pulse animations**: For elite status indicators
- **Monospace fonts**: For technical/classified data

---

**ONYX SYSTEMS © 2026 • EMBRACE DARK**

⚫ Maximum Security • Elite Operations • Classified Access 💠
