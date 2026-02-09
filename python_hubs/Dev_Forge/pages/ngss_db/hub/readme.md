README — NGSS MS Research Vault (Sandbox Demo)
What this app is

NGSS MS Research Vault is a sandbox demonstration app for exploring how NGSS standards can live inside a database and feed instructional planning tools.

This version is intentionally limited and safe:

Only 2 standards are included by default

MS-LS1-1 (Cells & Living Things)

MS-ESS1-1 (Earth–Sun–Moon System)

Includes example 5E activity variables (Engage → Evaluate)

Designed for walkthroughs with educators (e.g., Piluso)

Not the final production database

What’s inside the database (demo scope)
Tables used

standards
Core NGSS performance expectation metadata

tags / standard_tags
Lightweight tagging (SEP, DCI, CCC) for filtering

demo_activities
Sandbox-only instructional ideas tied to each standard:

Phase (Engage, Explore, Explain, Elaborate, Evaluate)

Activity description

Materials

Accommodations

Sentence starters

⚠️ These activities are examples, not official NGSS content.

How the demo database is created

On first run:

The app checks whether ngss_ms_demo.db exists and has data

If empty, it automatically seeds:

MS-LS1-1

MS-ESS1-1

Minimal tags

One activity per 5E phase

After that, the database persists between sessions.

How to add MORE standards (sandbox only)

You have two safe options, depending on your comfort level.

Option A — Add via Python (recommended for now)

Open

ngss_ms_research_vault_app.py


Find the function:

def db_seed_demo_if_empty(con):


Copy one of the existing INSERT INTO standards(...) blocks.

Paste it below, and update:

pe_code (e.g., "MS-ESS2-4")

domain_title

pe_statement

source_url

(Optional) Add demo activities using:

_insert_demo_activity(
    con,
    "MS-ESS2-4",
    "Engage",
    "Title",
    "Activity description...",
    materials="...",
    accommodations="...",
    sentence_starters="..."
)


Delete the existing .db file once to re-seed:

ngss_ms_demo.db


Reload the app.

Option B — Add directly to the SQLite database (advanced)

If you’re comfortable with SQLite:

INSERT INTO standards
(pe_code, grade_band, topic_area, domain_code, domain_title, pe_statement, source_url)
VALUES
('MS-ESS2-4', 'MS', 'Earth Science', 'MS-ESS2',
 'Earth’s Systems',
 'Develop a model to describe the cycling of water through Earth’s systems...',
 'https://www.nextgenscience.org/...');


Then add matching rows to demo_activities.

⚠️ This method skips validation—recommended only if you know SQLite.
