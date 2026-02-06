"""
BSChapp — Phase 1 Generator Stub
Teacher-first. No AI. No analytics. No admin logic.

Purpose:
- Copy base HTML templates
- Lightly populate safe fields (date, title, standards)
- Output ready-to-print files
"""

import os
from datetime import date

# ===== CONFIG =====
TEMPLATES = {
    "exit_ticket": "materials/exit_tickets/exit_ticket_v1.html",
    "worksheet": "materials/worksheets/worksheet_v1.html",
    "lesson_plan": "materials/lesson_plans/lesson_plan_v1.html",
    "pbis_reflective": "materials/pbis/pbis_reflective_note_v1.html",
    "photo_evidence": "materials/evidence/photo_evidence_v1.html"
}

OUTPUT_DIR = "generated_artifacts"

SAFE_PLACEHOLDERS = {
    "{{DATE}}": date.today().isoformat(),
}

# ===== UTILS =====
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_output(content, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

def populate_safe_fields(content, title="", standards=""):
    content = content.replace("__________________________", title or "__________________________", 1)
    content = content.replace("__________________________", standards or "__________________________", 1)
    return content

# ===== MAIN =====
def generate_all(title="", standards=""):
    today = date.today().isoformat()
    ensure_dir(OUTPUT_DIR)

    for name, template_path in TEMPLATES.items():
        html = load_template(template_path)
        html = populate_safe_fields(html, title=title, standards=standards)

        out_name = f"{name}_{today}.html"
        out_path = os.path.join(OUTPUT_DIR, out_name)

        save_output(html, out_path)
        print(f"Generated: {out_path}")

if __name__ == "__main__":
    print("BSChapp Generator (Phase 1)")
    title = input("Enter lesson/topic title (optional): ").strip()
    standards = input("Enter standard tags (optional): ").strip()

    generate_all(title=title, standards=standards)
    print("Done. Files are ready to print.")