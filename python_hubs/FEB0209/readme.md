Got it — keep this simple, clean, and copy-paste ready. Here’s a production-ready README you can drop straight into your repo for Birthday Viewer.


---

🎂 Birthday Viewer

Birthday Viewer is a lightweight Streamlit app for creating, previewing, and sharing custom birthday HTML cards.
It supports reusable designs, visual customization, and a growing demo system for showcasing features safely.

Built for speed, creativity, and reuse.


---

✨ Current Features

🎉 Upload or paste full HTML birthday cards

👀 Live preview inside Streamlit

🔐 Admin demo mode for safe showcasing

🧩 Token-based demo entries (non-destructive)

🖼️ Image-friendly layouts (optimized for sharing)



---

🧪 Demo Mode

Birthday Viewer includes a Demo/Admin Mode that allows showcasing the app without affecting real user content.

Demo Tokens (Admin Mode)

Currently supported demo tokens:

DEMO-001

DEMO-002

DEMO-003


➡️ TODO:
Add three more demo tokens:

DEMO-004

DEMO-005

DEMO-006


These tokens:

Load pre-seeded birthday cards

Cannot be deleted by non-admin users

Are used for presentations and walkthroughs



---

🛠️ To-Do Roadmap (Next Milestone)

🎨 Palette Creator

Add a palette-based CSS editor that allows users to:

Select from preset color palettes

Apply colors to background, text, accents

Preview changes live

Reset to default with an Abort / Reset button


Status: ⏳ Planned


---

🧱 Block Creator

Add a Block Creator for modular birthday layouts:

Header block (title, subtitle, emoji)

Image block (single image)

Message block (text / poem)

Footer block (signature / date)


Blocks should:

Be reorderable

Generate valid HTML

Export as a single .html file


Status: ⏳ Planned


---

🖼️ Image Hosting (Imgur)

Solidify external image hosting using Imgur:

Upload images → receive hosted URL

Store URLs instead of raw images

Improve load speed & sharing reliability


Benefits:

No repo bloat

Easier sharing

Consistent rendering across devices


Status: ⏳ Planned


---

📁 Suggested File Structure

birthday_viewer/
│
├── Birthday_Viewer.py        # Main Streamlit app
├── README.md                # This file
│
├── data/
│   ├── demos/               # Demo HTML cards
│   ├── user_cards/          # User-generated HTML
│
├── assets/
│   ├── palettes.json        # Preset color palettes (future)
│
├── utils/
│   ├── imgur_uploader.py    # Imgur integration (future)
│   ├── blocks.py            # Block creator logic (future)


---

🚀 Demo Status

✅ Core app works

✅ HTML preview stable

✅ Demo tokens functional

🧪 Live demo coming next

🧱 Block system pending

🎨 Palette editor pending



---

🧠 Philosophy

Birthday Viewer is designed to:

Reduce friction

Encourage creativity

Avoid lock-in

Let users make once, reuse forever


HTML is the source of truth.


---

If you want, next time we can:

Write the Imgur uploader module

Design the palette JSON schema

Or sketch the Block Creator UI in under 30 lines


For now — you did enough.
Go rest.