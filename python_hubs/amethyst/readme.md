Purple aesthetic

# 🔮 AMETHYST HUB - Streamlit Application

**Dream Purple • Go Beyond**

A beautiful, hazy purple-themed Streamlit hub application with integrated creative tools.

---

## 🎨 Features

### Main Hub
- **Amethyst Aesthetic**: Dreamy purple gradient with glassmorphism effects
- **Palm ID Authentication**: Secure admin access with 3-tap unlock
- **Modular Architecture**: Easy to add new apps/tools

### Included Apps
1. **🎨 Mr. Benji's Creative Studio** (Teacher Tools)
   - Image Enhancement Tool
   - Markup & Annotation Tool
   - Photo Collage Maker
   - AI Art Studio (VIP)

2. **🖼️ Universal Gallery**
   - Grid, Slideshow, and List view modes
   - Image metadata display
   - Glossy, modern interface

---

## 📁 File Structure

```
your_project/
│
├── app.py                          # Main hub application
├── teacher_tools.py                # Creative Studio module
├── gallery_view.py                 # Gallery viewer module
│
└── html_tools/                     # Optional: HTML tools directory
    ├── enhance.html                # Image enhancer
    ├── markup.html                 # Markup tool
    ├── collage.html                # Collage maker
    └── ai-art-studio-vip.html      # AI Art VIP tool
```

---

## 🚀 Setup & Installation

### 1. Install Dependencies

```bash
pip install streamlit pillow
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Access the Hub

The app will open in your browser at `http://localhost:8501`

---

## 🔐 Admin Access

**Default Admin Code**: `BENJI2026`

To unlock admin features:
1. Click the 🖐️ palm button **3 times**
2. Enter the admin code
3. Click "🔓 Unlock"

To change the admin code, edit line 20 in `app.py`:
```python
ADMIN_CODE_HASH = hashlib.sha256("YOUR_NEW_CODE".encode()).hexdigest()
```

---

## 🎨 Embedding HTML Tools

To add your HTML creative tools to the Teacher Tools module:

### Option 1: Direct Embedding (Recommended)

1. Place your HTML files in the same directory as `teacher_tools.py`
2. Edit `teacher_tools.py` and uncomment the embedding code:

```python
html_file = Path("enhance.html")
if html_file.exists():
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=1200, scrolling=True)
```

3. Adjust the `height` parameter based on your tool's needs

### Option 2: External Hosting

Host your HTML files on a server and use `components.iframe()`:

```python
components.iframe("https://your-domain.com/enhance.html", height=1200)
```

---

## 🎭 Customization

### Change Color Scheme

Edit the CSS in `app.py` (lines 40-250). Key color variables:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);

/* Accent color */
color: #f093fb;  /* Light purple */

/* Card backgrounds */
background: rgba(255, 255, 255, 0.15);
```

### Add New Apps

1. Create a new Python file (e.g., `my_new_app.py`)
2. Add a `render(admin_unlocked)` function
3. Import it in `app.py`:
   ```python
   import my_new_app
   ```
4. Add navigation button in the home page section
5. Add routing logic:
   ```python
   elif st.session_state.current_page == "my_new_app":
       my_new_app.render(st.session_state.admin_unlocked)
   ```

---

## 🌟 Your HTML Tools

The following HTML tools were created for integration:

### ✨ Enhance Tool
- JPEG/PNG color and sharpness enhancement
- Adjustable saturation, brightness, contrast
- Real-time preview

### 📦 Markup Tool
- Draw annotation boxes on images
- Add labels for AI training
- Customizable colors

### 🎨 Collage Maker
- Combine 2-6 photos
- 10+ layout options
- Customizable borders and styling

### 👑 AI Art Studio (VIP)
- Lock screen with access code
- Multiple art style presets
- Advanced generation controls
- API-ready structure

All tools maintain the same purple aesthetic as the hub!

---

## 🔧 Troubleshooting

### Images not loading in Gallery
- Ensure PIL/Pillow is installed: `pip install pillow`
- Check file formats are supported (PNG, JPG, JPEG, GIF, WEBP)

### HTML tools not showing
- Verify file paths are correct
- Check that `streamlit.components.v1` is imported
- Ensure HTML files are in the same directory

### Admin unlock not working
- Verify you've tapped the palm button 3 times
- Check that the code matches (case-sensitive)
- Try resetting with the 🔄 Reset button

---

## 📝 License

Created for Mr. Benji's classroom 2026

---

## 🎯 Future Enhancements

- [ ] Batch image processing in Gallery
- [ ] ZIP download for multiple images
- [ ] User preferences storage
- [ ] Dark/light theme toggle
- [ ] Mobile-optimized layouts
- [ ] More creative tools

---

**Enjoy your Amethyst Hub! Dream Purple, Go Beyond! 🔮✨**
