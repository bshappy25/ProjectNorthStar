# Ariel: A People’s Princess - Streamlit App

A beautiful interactive web app celebrating the winter princess artwork.

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip

### Installation

1. **Install Streamlit**

```bash
pip install streamlit
```

1. **Setup Files**
   Place these files in the same directory:

- `streamlit_app.py` (main app)
- `ariel_princess_app.html` (HTML template)
- `princess_image.png` (your princess image - rename your uploaded image to this)

1. **Run the App**

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 File Structure

```
your-project-folder/
│
├── streamlit_app.py           # Main Streamlit application
├── ariel_princess_app.html    # HTML template with styling
├── princess_image.png         # The princess artwork
└── README.md                  # This file
```

## 🎨 Features

- **Responsive Design**: Looks great on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects and scroll animations
- **Beautiful Layout**: Gradient backgrounds and elegant typography
- **Symbolic Breakdown**: Explains the meaning behind each element in the artwork
- **Quality Cards**: Highlights Ariel’s amazing qualities
- **Smooth Animations**: Parallax scrolling and fade-in effects

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
1. Go to [share.streamlit.io](https://share.streamlit.io)
1. Connect your GitHub repository
1. Select your repository and file (`streamlit_app.py`)
1. Click Deploy!

### Deploy to Other Platforms

- **Heroku**: Use the Streamlit buildpack
- **AWS/GCP/Azure**: Deploy as a standard Python web app
- **Docker**: Create a container with Streamlit

## 🛠️ Customization

### Change Colors

Edit the gradient colors in `ariel_princess_app.html`:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modify Content

Edit the HTML sections to change text, add new qualities, or modify symbols.

### Adjust Height

In `streamlit_app.py`, modify the height parameter:

```python
components.html(html_content, height=3000, scrolling=True)
```

## 💡 Tips

- The image is embedded as base64, so the app is fully self-contained
- No external dependencies or API calls needed
- Works offline once loaded
- Fast loading times

## 📝 Notes

- Make sure your image file is named `princess_image.png` or update the filename in `streamlit_app.py`
- The HTML file uses embedded styling, so no external CSS files needed
- All animations are pure CSS/JavaScript - no frameworks required

## 🎉 Enjoy!

Your beautiful Ariel princess app is ready to share with the world!

-----

Created with ✨ and 💝