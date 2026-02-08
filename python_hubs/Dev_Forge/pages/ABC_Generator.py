"""
ABC Generator - DevForge

Make architecture decisions quickly with interactive framework

A - Architecture (standalone/integrated/hybrid)
B - Build pattern (minimal/standard/full)
C - Code style (functional/OOP/modular)
S - Stylistic choice (theme selection)
I - Indentation check (code linting + safe auto-fix)
"""

import ast
import streamlit as st

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="ABC Generator",
    page_icon="⚡",
    layout="wide",
)

# =====================
# THEME
# =====================

is_science = st.session_state.get("dev_theme", "science") == "science"

SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"

NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"

BG = SCI_BG if is_science else NEUTRAL_BG
CARD = SCI_CARD if is_science else NEUTRAL_CARD
BORDER = SCI_BORDER if is_science else NEUTRAL_BORDER
TEXT = SCI_TEXT if is_science else NEUTRAL_TEXT

st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# =====================
# SESSION STATE
# =====================

if "abc_choices" not in st.session_state:
    st.session_state["abc_choices"] = {"A": None, "B": None, "C": None, "S": None}

if "indent_cleaned" not in st.session_state:
    st.session_state["indent_cleaned"] = ""

# Helper: render a choice card
def render_choice_card(title: str, bullets_html: str, selected: bool) -> None:
    st.markdown(
        f"""
<div class='choice-card {"selected" if selected else ""}'>
<strong>{title}</strong>
<p style='font-size:0.9rem; margin-top:8px; opacity:0.8;'>
{bullets_html}
</p>
</div>
""",
        unsafe_allow_html=True,
    )

# =====================
# HEADER
# =====================

st.title("⚡ ABC Generator")
st.markdown("### Make Architecture Decisions Fast")

st.markdown(
    """
<div style='background:var(--card); border:1px solid var(--border); border-radius:16px; padding:20px; backdrop-filter:blur(10px);'>
<p><strong>How it works:</strong> Answer A, B, C, S questions → Get recommended structure + starter code</p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# =====================
# A - ARCHITECTURE
# =====================

st.markdown("## 🏗️ A - Architecture")
st.caption("How should this app relate to your ecosystem?")

arch_col1, arch_col2, arch_col3 = st.columns(3)

with arch_col1:
    if st.button("📦 Standalone", use_container_width=True, key="arch_standalone"):
        st.session_state["abc_choices"]["A"] = "standalone"
        st.rerun()
    selected = st.session_state["abc_choices"]["A"] == "standalone"
    render_choice_card(
        "Standalone App",
        "• Independent operation<br>• Own data/state<br>• Simple deployment<br>• Like Teacher Tools Hub",
        selected,
    )

with arch_col2:
    if st.button("🔗 Integrated", use_container_width=True, key="arch_integrated"):
        st.session_state["abc_choices"]["A"] = "integrated"
        st.rerun()
    selected = st.session_state["abc_choices"]["A"] == "integrated"
    render_choice_card(
        "Integrated Pages",
        "• Part of existing app<br>• Shared session state<br>• Unified navigation<br>• Like BSChapp pages",
        selected,
    )

with arch_col3:
    if st.button("⚡ Hybrid", use_container_width=True, key="arch_hybrid"):
        st.session_state["abc_choices"]["A"] = "hybrid"
        st.rerun()
    selected = st.session_state["abc_choices"]["A"] == "hybrid"
    render_choice_card(
        "Hybrid Router",
        "• URL-based routing<br>• Shared resources<br>• Modular design<br>• Maximum flexibility",
        selected,
    )

st.divider()

# =====================
# B - BUILD PATTERN
# =====================

st.markdown("## 🔨 B - Build Pattern")
st.caption("How complex should the initial build be?")

build_col1, build_col2, build_col3 = st.columns(3)

with build_col1:
    if st.button("⚡ Minimal", use_container_width=True, key="build_minimal"):
        st.session_state["abc_choices"]["B"] = "minimal"
        st.rerun()
    selected = st.session_state["abc_choices"]["B"] == "minimal"
    render_choice_card(
        "Minimal MVP",
        "• Single workflow<br>• Core features only<br>• Fast to build (1-2hr)<br>• Easy iteration",
        selected,
    )

with build_col2:
    if st.button("📦 Standard", use_container_width=True, key="build_standard"):
        st.session_state["abc_choices"]["B"] = "standard"
        st.rerun()
    selected = st.session_state["abc_choices"]["B"] == "standard"
    render_choice_card(
        "Standard Build",
        "• Multiple features<br>• Form validation<br>• Session management<br>• 3-5hr build time",
        selected,
    )

with build_col3:
    if st.button("🚀 Full", use_container_width=True, key="build_full"):
        st.session_state["abc_choices"]["B"] = "full"
        st.rerun()
    selected = st.session_state["abc_choices"]["B"] == "full"
    render_choice_card(
        "Full Featured",
        "• Complete system<br>• Database integration<br>• Advanced features<br>• Multi-day project",
        selected,
    )

st.divider()

# =====================
# C - CODE STYLE
# =====================

st.markdown("## 💻 C - Code Style")
st.caption("What coding approach fits best?")

code_col1, code_col2, code_col3 = st.columns(3)

with code_col1:
    if st.button("📝 Functional", use_container_width=True, key="code_functional"):
        st.session_state["abc_choices"]["C"] = "functional"
        st.rerun()
    selected = st.session_state["abc_choices"]["C"] == "functional"
    render_choice_card(
        "Functional Style",
        "• Helper functions<br>• Linear flow<br>• Easy to read<br>• Quick prototyping",
        selected,
    )

with code_col2:
    if st.button("🏛️ OOP", use_container_width=True, key="code_oop"):
        st.session_state["abc_choices"]["C"] = "oop"
        st.rerun()
    selected = st.session_state["abc_choices"]["C"] == "oop"
    render_choice_card(
        "Object-Oriented",
        "• Classes & methods<br>• Encapsulation<br>• Reusable components<br>• Scalable structure",
        selected,
    )

with code_col3:
    if st.button("🧩 Modular", use_container_width=True, key="code_modular"):
        st.session_state["abc_choices"]["C"] = "modular"
        st.rerun()
    selected = st.session_state["abc_choices"]["C"] == "modular"
    render_choice_card(
        "Modular Design",
        "• Separate files/modules<br>• Import system<br>• Clean separation<br>• Team-friendly",
        selected,
    )

st.divider()

# =====================
# S - STYLISTIC
# =====================

st.markdown("## 🎨 S - Stylistic Choice")
st.caption("What visual theme?")

style_col1, style_col2, style_col3 = st.columns(3)

with style_col1:
    if st.button("🔬 Science Glassy", use_container_width=True, key="style_science"):
        st.session_state["abc_choices"]["S"] = "science"
        st.rerun()
    selected = st.session_state["abc_choices"]["S"] == "science"
    render_choice_card(
        "Science Mode",
        "• Blue-green theme<br>• Glassy texture<br>• Dark background<br>• BSChapp v2 style",
        selected,
    )

with style_col2:
    if st.button("📝 Neutral Glassy", use_container_width=True, key="style_neutral"):
        st.session_state["abc_choices"]["S"] = "neutral"
        st.rerun()
    selected = st.session_state["abc_choices"]["S"] == "neutral"
    render_choice_card(
        "Neutral Mode",
        "• Gray theme<br>• Glassy texture<br>• Light background<br>• Professional look",
        selected,
    )

with style_col3:
    if st.button("🎯 Custom", use_container_width=True, key="style_custom"):
        st.session_state["abc_choices"]["S"] = "custom"
        st.rerun()
    selected = st.session_state["abc_choices"]["S"] == "custom"
    render_choice_card(
        "Custom Theme",
        "• Your color palette<br>• Unique identity<br>• Brand-specific<br>• Full control",
        selected,
    )

st.divider()

# =====================
# RESULTS & CODE GEN
# =====================

choices = st.session_state["abc_choices"]

if all(choices.values()):
    st.markdown("## ✅ Your Configuration")

    st.markdown(
        f"""
<div style='background:var(--card); border:2px solid rgba(20,184,166,0.6); border-radius:16px; padding:20px; backdrop-filter:blur(10px);'>
<p><span class='badge'>A</span> <strong>Architecture:</strong> {choices['A'].title()}</p>
<p><span class='badge'>B</span> <strong>Build:</strong> {choices['B'].title()}</p>
<p><span class='badge'>C</span> <strong>Code:</strong> {choices['C'].upper() if choices['C'] == 'oop' else choices['C'].title()}</p>
<p><span class='badge'>S</span> <strong>Style:</strong> {choices['S'].title()}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### 🎯 Recommended Approach")

    arch = choices["A"]
    build = choices["B"]
    code = choices["C"]
    style = choices["S"]

    if arch == "standalone":
        structure = """my_app/
├── my_app.py          # Main file
├── pages/             # Optional multipage
│   └── page1.py
└── data/              # Local storage

Run: streamlit run my_app.py
"""
    elif arch == "integrated":
        structure = """existing_app/
├── main.py
├── pages/
│   ├── existing_page.py
│   └── new_feature.py  # Add your page here
└── shared/
    └── utils.py

Add page to pages/ folder
"""
    else:
        structure = """python_hubs/
├── router.py          # Main router
├── app_v1/
│   └── app.py
└── app_v2/            # Your new app
    └── app.py

Access via: ?app=v2
"""

    st.code(structure, language="text")
    st.markdown("### 📝 Starter Code")

    with st.expander("🔧 Main File Template", expanded=True):
        if style == "science":
            theme_code = """
# SCIENCE THEME
SCI_BG = "#061B15"
SCI_CARD = "rgba(255,255,255,0.08)"
SCI_BORDER = "rgba(120,255,220,0.3)"
SCI_TEXT = "rgba(255,255,255,0.92)"
""".strip()
        elif style == "neutral":
            theme_code = """
# NEUTRAL THEME
NEUTRAL_BG = "#f2f2f2"
NEUTRAL_CARD = "rgba(230, 230, 230, 0.7)"
NEUTRAL_BORDER = "rgba(207, 207, 207, 0.5)"
NEUTRAL_TEXT = "#000000"
""".strip()
        else:
            theme_code = """
# CUSTOM THEME
# Add your palette variables here
""".strip()

        starter_code = f'''"""
My App - Project North Star
"""

import streamlit as st

st.set_page_config(
    page_title="My App",
    page_icon="🌟",
    layout="wide"
)

if "data" not in st.session_state:
    st.session_state["data"] = {{}}

{theme_code}

st.markdown(
    """
<style>
/* Add your theme CSS here */
</style>
""",
    unsafe_allow_html=True
)

st.title("🌟 My App")
st.markdown("### Built with DevForge ABC Framework")

# Your code here…
'''
        st.code(starter_code, language="python")

    st.markdown("### 🚀 Next Steps")
    st.markdown(
        f"""
1. **Copy starter code** above
2. **Create file structure** as recommended
3. **Add your features** based on **{build}** build pattern
4. **Test and iterate** quickly
5. **Deploy** when ready
"""
    )
else:
    st.info("👆 Select options for A, B, C, and S above to generate your recommended structure")

st.divider()

# =====================
# I - INDENTATION CHECK (REAL PARSE + SAFE AUTO-FIX)
# =====================

st.markdown("## 🔍 I - Indentation Checker")
st.caption("Paste code to check formatting (real Python parse + safe auto-fix options)")

code_input = st.text_area(
    "Paste Python Code",
    height=260,
    placeholder="def my_function():\n    return True\n",
)

opt_col1, opt_col2, opt_col3 = st.columns([1, 1, 1])

with opt_col1:
    run_check = st.button("✅ Check Code", type="primary", use_container_width=True)

with opt_col2:
    run_fix = st.button("🧼 Auto-fix (safe)", use_container_width=True)

with opt_col3:
    show_cleaned = st.checkbox("Show cleaned version", value=True)

def safe_autofix(text: str) -> str:
    # Safe-only fixes:
    # 1) Tabs -> 4 spaces
    # 2) Strip trailing whitespace
    # 3) Normalize line endings, ensure final newline
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    fixed_lines = []
    for line in lines:
        line = line.replace("\t", "    ")
        line = line.rstrip()
        fixed_lines.append(line)
    fixed = "\n".join(fixed_lines).rstrip() + "\n"
    return fixed

def parse_report(code_text: str):
    # Returns (ok: bool, message: str)
    try:
        ast.parse(code_text)
        return True, "✅ Parsed successfully — no Python indentation/syntax errors found."
    except IndentationError as e:
        line = getattr(e, "lineno", None)
        col = getattr(e, "offset", None)
        return False, f"❌ IndentationError: {e.msg} (line {line}, column {col})"
    except SyntaxError as e:
        line = getattr(e, "lineno", None)
        col = getattr(e, "offset", None)
        return False, f"❌ SyntaxError: {e.msg} (line {line}, column {col})"

if run_check:
    if not code_input.strip():
        st.error("Paste code to check.")
    else:
        warnings = []
        tab_lines = [i for i, line in enumerate(code_input.split("\n"), 1) if "\t" in line]
        if tab_lines:
            warnings.append(
                f"Contains TAB characters on lines: {', '.join(map(str, tab_lines))} (use spaces)"
            )

        cleaned = safe_autofix(code_input)
        ok, msg = parse_report(cleaned)

        if ok:
            st.success(msg)
        else:
            st.error(msg)

        if warnings:
            st.warning("⚠️ Whitespace warnings:")
            for w in warnings:
                st.write(f"- {w}")

        if show_cleaned:
            st.markdown("### 🧼 Cleaned code (tabs→spaces, trailing whitespace removed)")
            st.code(cleaned, language="python")

            st.download_button(
                "⬇️ Download cleaned code (.py)",
                data=cleaned.encode("utf-8"),
                file_name="cleaned_code.py",
                mime="text/x-python",
                use_container_width=True,
            )

if run_fix:
    if not code_input.strip():
        st.error("Paste code to fix.")
    else:
        cleaned = safe_autofix(code_input)
        st.session_state["indent_cleaned"] = cleaned

        ok, msg = parse_report(cleaned)
        if ok:
            st.success("🧼 Auto-fix applied. " + msg)
        else:
            st.warning("🧼 Auto-fix applied, but parsing still fails:")
            st.write(msg)

        if show_cleaned:
            st.markdown("### 🧼 Auto-fixed output (copy/paste this)")
            st.code(cleaned, language="python")

        st.download_button(
            "⬇️ Download auto-fixed code (.py)",
            data=cleaned.encode("utf-8"),
            file_name="autofixed_code.py",
            mime="text/x-python",
            use_container_width=True,
        )

st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)