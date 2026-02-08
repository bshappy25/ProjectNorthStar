# “””
ABC Generator - DevForge

Make architecture decisions quickly with interactive framework

A - Architecture (standalone/integrated/hybrid)
B - Build pattern (minimal/standard/full)
C - Code style (functional/OOP/modular)
S - Stylistic choice (theme selection)
I - Indentation check (code linting)
“””

import streamlit as st

# =====================

# PAGE CONFIG

# =====================

st.set_page_config(
page_title=“ABC Generator”,
page_icon=“⚡”,
layout=“wide”
)

# =====================

# THEME

# =====================

is_science = st.session_state.get(“dev_theme”, “science”) == “science”

SCI_BG = “#061B15”
SCI_CARD = “rgba(255,255,255,0.08)”
SCI_BORDER = “rgba(120,255,220,0.3)”
SCI_TEXT = “rgba(255,255,255,0.92)”

NEUTRAL_BG = “#f2f2f2”
NEUTRAL_CARD = “rgba(230, 230, 230, 0.7)”
NEUTRAL_BORDER = “rgba(207, 207, 207, 0.5)”
NEUTRAL_TEXT = “#000000”

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

st.markdown(f”””

<style>
:root {{
  --bg: {BG};
  --card: {CARD};
  --border: {BORDER};
  --text: {TEXT};
}}

div[data-testid="stAppViewContainer"] {{
  background-color: var(--bg) !important;
}}

h1, h2, h3, h4, h5, h6, p, span, label, div {{
  color: var(--text) !important;
}}

.choice-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin: 10px 0;
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
}}

.choice-card:hover {{
  border-color: rgba(20,184,166,0.6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(20,184,166,0.2);
}}

.choice-card.selected {{
  border: 2px solid rgba(20,184,166,0.8);
  background: rgba(20,184,166,0.1);
}}

.badge {{
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(20,184,166,0.2);
  color: rgba(20,184,166,1) !important;
  font-weight: 900;
  font-size: 0.75rem;
  margin-right: 8px;
}}
</style>

“””, unsafe_allow_html=True)

# =====================

# SESSION STATE

# =====================

if “abc_choices” not in st.session_state:
st.session_state[“abc_choices”] = {
“A”: None,
“B”: None,
“C”: None,
“S”: None
}

# =====================

# HEADER

# =====================

st.title(“⚡ ABC Generator”)
st.markdown(”### Make Architecture Decisions Fast”)

st.markdown(”””

<div style='background:var(--card); border:1px solid var(--border); border-radius:16px; padding:20px; backdrop-filter:blur(10px);'>
<p><strong>How it works:</strong> Answer A, B, C, S questions → Get recommended structure + starter code</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =====================

# A - ARCHITECTURE

# =====================

st.markdown(”## 🏗️ A - Architecture”)
st.caption(“How should this app relate to your ecosystem?”)

arch_col1, arch_col2, arch_col3 = st.columns(3)

with arch_col1:
if st.button(“📦 Standalone”, use_container_width=True, key=“arch_standalone”):
st.session_state[“abc_choices”][“A”] = “standalone”
st.rerun()

```
selected = st.session_state["abc_choices"]["A"] == "standalone"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Standalone App</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Independent operation<br>
• Own data/state<br>
• Simple deployment<br>
• Like Teacher Tools Hub
</p>
</div>
""", unsafe_allow_html=True)
```

with arch_col2:
if st.button(“🔗 Integrated”, use_container_width=True, key=“arch_integrated”):
st.session_state[“abc_choices”][“A”] = “integrated”
st.rerun()

```
selected = st.session_state["abc_choices"]["A"] == "integrated"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Integrated Pages</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Part of existing app<br>
• Shared session state<br>
• Unified navigation<br>
• Like BSChapp pages
</p>
</div>
""", unsafe_allow_html=True)
```

with arch_col3:
if st.button(“⚡ Hybrid”, use_container_width=True, key=“arch_hybrid”):
st.session_state[“abc_choices”][“A”] = “hybrid”
st.rerun()

```
selected = st.session_state["abc_choices"]["A"] == "hybrid"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Hybrid Router</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• URL-based routing<br>
• Shared resources<br>
• Modular design<br>
• Maximum flexibility
</p>
</div>
""", unsafe_allow_html=True)
```

st.divider()

# =====================

# B - BUILD PATTERN

# =====================

st.markdown(”## 🔨 B - Build Pattern”)
st.caption(“How complex should the initial build be?”)

build_col1, build_col2, build_col3 = st.columns(3)

with build_col1:
if st.button(“⚡ Minimal”, use_container_width=True, key=“build_minimal”):
st.session_state[“abc_choices”][“B”] = “minimal”
st.rerun()

```
selected = st.session_state["abc_choices"]["B"] == "minimal"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Minimal MVP</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Single workflow<br>
• Core features only<br>
• Fast to build (1-2hr)<br>
• Easy iteration
</p>
</div>
""", unsafe_allow_html=True)
```

with build_col2:
if st.button(“📦 Standard”, use_container_width=True, key=“build_standard”):
st.session_state[“abc_choices”][“B”] = “standard”
st.rerun()

```
selected = st.session_state["abc_choices"]["B"] == "standard"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Standard Build</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Multiple features<br>
• Form validation<br>
• Session management<br>
• 3-5hr build time
</p>
</div>
""", unsafe_allow_html=True)
```

with build_col3:
if st.button(“🚀 Full”, use_container_width=True, key=“build_full”):
st.session_state[“abc_choices”][“B”] = “full”
st.rerun()

```
selected = st.session_state["abc_choices"]["B"] == "full"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Full Featured</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Complete system<br>
• Database integration<br>
• Advanced features<br>
• Multi-day project
</p>
</div>
""", unsafe_allow_html=True)
```

st.divider()

# =====================

# C - CODE STYLE

# =====================

st.markdown(”## 💻 C - Code Style”)
st.caption(“What coding approach fits best?”)

code_col1, code_col2, code_col3 = st.columns(3)

with code_col1:
if st.button(“📝 Functional”, use_container_width=True, key=“code_functional”):
st.session_state[“abc_choices”][“C”] = “functional”
st.rerun()

```
selected = st.session_state["abc_choices"]["C"] == "functional"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Functional Style</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Helper functions<br>
• Linear flow<br>
• Easy to read<br>
• Quick prototyping
</p>
</div>
""", unsafe_allow_html=True)
```

with code_col2:
if st.button(“🏛️ OOP”, use_container_width=True, key=“code_oop”):
st.session_state[“abc_choices”][“C”] = “oop”
st.rerun()

```
selected = st.session_state["abc_choices"]["C"] == "oop"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Object-Oriented</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Classes & methods<br>
• Encapsulation<br>
• Reusable components<br>
• Scalable structure
</p>
</div>
""", unsafe_allow_html=True)
```

with code_col3:
if st.button(“🧩 Modular”, use_container_width=True, key=“code_modular”):
st.session_state[“abc_choices”][“C”] = “modular”
st.rerun()

```
selected = st.session_state["abc_choices"]["C"] == "modular"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Modular Design</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Separate files/modules<br>
• Import system<br>
• Clean separation<br>
• Team-friendly
</p>
</div>
""", unsafe_allow_html=True)
```

st.divider()

# =====================

# S - STYLISTIC

# =====================

st.markdown(”## 🎨 S - Stylistic Choice”)
st.caption(“What visual theme?”)

style_col1, style_col2, style_col3 = st.columns(3)

with style_col1:
if st.button(“🔬 Science Glassy”, use_container_width=True, key=“style_science”):
st.session_state[“abc_choices”][“S”] = “science”
st.rerun()

```
selected = st.session_state["abc_choices"]["S"] == "science"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Science Mode</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Blue-green theme<br>
• Glassy texture<br>
• Dark background<br>
• BSChapp v2 style
</p>
</div>
""", unsafe_allow_html=True)
```

with style_col2:
if st.button(“📝 Neutral Glassy”, use_container_width=True, key=“style_neutral”):
st.session_state[“abc_choices”][“S”] = “neutral”
st.rerun()

```
selected = st.session_state["abc_choices"]["S"] == "neutral"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Neutral Mode</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Gray theme<br>
• Glassy texture<br>
• Light background<br>
• Professional look
</p>
</div>
""", unsafe_allow_html=True)
```

with style_col3:
if st.button(“🎯 Custom”, use_container_width=True, key=“style_custom”):
st.session_state[“abc_choices”][“S”] = “custom”
st.rerun()

```
selected = st.session_state["abc_choices"]["S"] == "custom"
st.markdown(f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>Custom Theme</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
• Your color palette<br>
• Unique identity<br>
• Brand-specific<br>
• Full control
</p>
</div>
""", unsafe_allow_html=True)
```

st.divider()

# =====================

# RESULTS & CODE GEN

# =====================

choices = st.session_state[“abc_choices”]

if all(choices.values()):
st.markdown(”## ✅ Your Configuration”)

```
st.markdown(f"""
<div style='background:var(--card); border:2px solid rgba(20,184,166,0.6); border-radius:16px; padding:20px; backdrop-filter:blur(10px);'>
<p><span class='badge'>A</span> <strong>Architecture:</strong> {choices['A'].title()}</p>
<p><span class='badge'>B</span> <strong>Build:</strong> {choices['B'].title()}</p>
<p><span class='badge'>C</span> <strong>Code:</strong> {choices['C'].upper() if choices['C'] == 'oop' else choices['C'].title()}</p>
<p><span class='badge'>S</span> <strong>Style:</strong> {choices['S'].title()}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Generate recommendation
st.markdown("### 🎯 Recommended Approach")

arch = choices["A"]
build = choices["B"]
code = choices["C"]
style = choices["S"]

# File structure recommendation
if arch == "standalone":
    structure = """
```

```
my_app/
├── my_app.py          # Main file
├── pages/             # Optional multipage
│   └── page1.py
└── data/              # Local storage
```

Run: `streamlit run my_app.py`
“””
elif arch == “integrated”:
structure = “””

```
existing_app/
├── main.py
├── pages/
│   ├── existing_page.py
│   └── new_feature.py  # Add your page here
└── shared/
    └── utils.py
```

Add page to `pages/` folder
“””
else:  # hybrid
structure = “””

```
python_hubs/
├── router.py          # Main router
├── app_v1/
│   └── app.py
└── app_v2/            # Your new app
    └── app.py
```

Access via: `?app=v2`
“””

```
st.code(structure, language="text")

# Starter code
st.markdown("### 📝 Starter Code")

with st.expander("🔧 Main File Template", expanded=True):
    
    theme_code = ""
    if style == "science":
        theme_code = '''
```

# SCIENCE THEME

SCI_BG = “#061B15”
SCI_CARD = “rgba(255,255,255,0.08)”
SCI_BORDER = “rgba(120,255,220,0.3)”
SCI_TEXT = “rgba(255,255,255,0.92)”
‘’’
elif style == “neutral”:
theme_code = ‘’’

# NEUTRAL THEME

NEUTRAL_BG = “#f2f2f2”
NEUTRAL_CARD = “rgba(230, 230, 230, 0.7)”
NEUTRAL_BORDER = “rgba(207, 207, 207, 0.5)”
NEUTRAL_TEXT = “#000000”
‘’’

```
    starter_code = f'''
```

“””
My App - Project North Star
“””

import streamlit as st

# PAGE CONFIG

st.set_page_config(
page_title=“My App”,
page_icon=“🌟”,
layout=“wide”
)

# SESSION STATE

if “data” not in st.session_state:
st.session_state[“data”] = {{}}

{theme_code}

# GLASSY UI

st.markdown(”””

<style>
/* Add your theme CSS here */
</style>

“””, unsafe_allow_html=True)

# MAIN APP

st.title(“🌟 My App”)
st.markdown(”### Built with DevForge ABC Framework”)

# Your code here…

‘’’

```
    st.code(starter_code, language="python")

# Next steps
st.markdown("### 🚀 Next Steps")
st.markdown(f"""
1. **Copy starter code** above
2. **Create file structure** as recommended
3. **Add your features** based on {build} build pattern
4. **Test and iterate** quickly
5. **Deploy** when ready
""")
```

else:
st.info(“👆 Select options for A, B, C, and S above to generate your recommended structure”)

st.divider()

# =====================

# I - INDENTATION CHECK

# =====================

st.markdown(”## 🔍 I - Indentation Checker”)
st.caption(“Paste code to check formatting (basic linting)”)

code_input = st.text_area(
“Paste Python Code”,
height=200,
placeholder=“def my_function():\n    return True”
)

if st.button(“✅ Check Code”, type=“primary”):
if code_input.strip():
lines = code_input.split(”\n”)
issues = []

```
    for i, line in enumerate(lines, 1):
        # Check for tabs
        if "\t" in line:
            issues.append(f"Line {i}: Contains tabs (use spaces)")
        
        # Check inconsistent indentation
        if line and not line[0] in (' ', '#', '\n'):
            if any(c.isspace() for c in line[:4]):
                issues.append(f"Line {i}: Inconsistent indentation")
    
    if issues:
        st.warning(f"Found {len(issues)} potential issues:")
        for issue in issues:
            st.write(f"⚠️ {issue}")
    else:
        st.success("✅ No obvious indentation issues found!")
        st.caption("Note: This is basic checking. Use a proper linter for production code.")
else:
    st.error("Paste code to check")
```

st.markdown(”<div style='height:60px'></div>”, unsafe_allow_html=True)