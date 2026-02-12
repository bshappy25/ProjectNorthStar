a beautiful and secure Python version of your NorthEmerald hub with the Palm ID admin gate and delete tool features.

# 🌲 NorthEmerald Hub

**Navigate North • Go NE**

A modular Streamlit hub application with secure admin features and aesthetic northern/emerald theming.

---

## 📁 File Structure

```
northemeraid/
├── app.py          # Main hub application
├── myapp1.py       # MyApp One module
├── myapp2.py       # MyApp Two module
└── readme.md       # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit

### Install Dependencies
```bash
pip install streamlit
```

### Run the Application
```bash
streamlit run app.py
```

---

## 🔐 Security Features

### Palm ID Admin Gate
1. **Activate**: Tap the 🖐️ palm icon **3 times** in the top-right corner
2. **Authenticate**: Enter admin code when prompted
3. **Unlock**: Gain access to admin-only delete tools

**Default Admin Code**: `Bshapp`

The code is stored as a SHA-256 hash for security.

---

## ✨ Features

### Home Screen
- Beautiful emerald gradient design
- Two app cards for navigation
- Secure Palm ID access in corner

### MyApp One
- Productivity-focused features
- Interactive demo with text input and slider
- Admin delete capability

### MyApp Two  
- Creative tools and collaboration
- Color picker and multi-select tools
- Admin delete capability

### Admin Tools
- **Delete Tool**: Remove individual app modules (❌ button)
- **Secure Access**: SHA-256 hashed password
- **Reset Option**: Clear Palm ID session

---

## 🎨 Design Aesthetic

- **Color Palette**: Deep teals, emerald greens, northern lights inspired
- **Typography**: Orbitron font for tech-forward look
- **Effects**: Glassmorphism, gradients, smooth animations
- **Icons**: Diamond (◆) branding throughout

---

## 🛠️ Adding New Apps

1. Create new file `myapp3.py`
2. Implement `render(admin_unlocked)` function
3. Import in `app.py`
4. Add navigation button in home section

Example:
```python
# myapp3.py
def render(admin_unlocked=False):
    st.markdown("## ◆ MyApp Three")
    # Your app content here
```

---

## 📝 License

© 2026 NorthEmerald • Go North

---

## 🐛 Troubleshooting

**Import Errors**: Ensure all `.py` files are in the same directory  
**Admin Access**: Remember to tap palm icon 3 times before entering code  
**Delete Not Working**: Must be admin unlocked first

---

**Navigate North with NorthEmerald! 🌲✨**
