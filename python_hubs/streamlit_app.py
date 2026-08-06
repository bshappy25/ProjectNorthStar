from __future__ import annotations

import io
import json
import re
import zipfile
from copy import deepcopy
from typing import Any

import streamlit as st

APP_TITLE = "NorthStar Game Forge"
APP_VERSION = "0.1.0"
SCENE_TYPES = ["menu", "room", "dialogue", "terminal", "puzzle", "cutscene", "locked", "ending"]
ACTION_TYPES = ["goto", "dialogue", "set_variable", "condition", "end"]
SCREEN_PRESETS = {
    "GBA 240 × 160": (240, 160),
    "Game Boy 160 × 144": (160, 144),
    "Nintendo 3DS top 400 × 240": (400, 240),
    "Nintendo 3DS bottom 320 × 240": (320, 240),
    "Custom": (240, 160),
}

DEFAULT_PROJECT = {
    "schema_version": 1,
    "meta": {
        "title": "Blue Crystal",
        "slug": "blue_crystal",
        "author": "",
        "version": "0.1.0",
        "description": "A menu-driven adventure prototype.",
        "target": "GBA 240 × 160",
        "screen_width": 240,
        "screen_height": 160,
        "start_scene": "title",
    },
    "variables": {
        "stone_state": {"type": "integer", "default": 0, "notes": "0 inactive, 1 beam pending, 2 activated"},
        "terminal_solved": {"type": "boolean", "default": False, "notes": ""},
    },
    "assets": [],
    "scenes": {
        "title": {
            "name": "Title Screen", "type": "menu", "background": "",
            "body": "RECOVER THE BLUE CRYSTAL",
            "choices": [{"label": "START", "action": {"type": "goto", "target": "manias_stone"}}],
            "notes": "",
        },
        "manias_stone": {
            "name": "Manias Stone", "type": "room", "background": "",
            "body": "The stone is silent.",
            "choices": [
                {"label": "INITIATE RESONANCE", "action": {"type": "condition", "variable": "stone_state", "operator": "==", "value": 0, "then": "stone_puzzle", "else": "stone_beam"}},
                {"label": "LEAVE", "action": {"type": "goto", "target": "title"}},
            ],
            "notes": "",
        },
        "stone_puzzle": {
            "name": "Stone Puzzle", "type": "puzzle", "background": "",
            "body": "ALIGN THREE CRYSTALS",
            "choices": [
                {"label": "ALIGN", "action": {"type": "set_variable", "variable": "stone_state", "value": 1, "next": "stone_beam"}},
                {"label": "WITHDRAW", "action": {"type": "goto", "target": "manias_stone"}},
            ],
            "notes": "Replace ALIGN with the final minigame.",
        },
        "stone_beam": {
            "name": "Stone Beam", "type": "cutscene", "background": "",
            "body": "SIGNAL RESTORED.\nBLUE CRYSTAL RECOVERED.",
            "choices": [{"label": "CONTINUE", "action": {"type": "set_variable", "variable": "stone_state", "value": 2, "next": "ending"}}],
            "notes": "",
        },
        "ending": {
            "name": "Ending", "type": "ending", "background": "",
            "body": "DEMO COMPLETE",
            "choices": [{"label": "RETURN TO TITLE", "action": {"type": "goto", "target": "title"}}],
            "notes": "",
        },
    },
}


def norm(value: str, fallback: str = "item") -> str:
    value = re.sub(r"[^a-z0-9_ -]", "", value.strip().lower())
    value = re.sub(r"[\s-]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_") or fallback


def idx(options: list[str], value: str) -> int:
    try:
        return options.index(value)
    except ValueError:
        return 0


def runtime_defaults(project: dict[str, Any]) -> dict[str, Any]:
    return {key: item.get("default") for key, item in project.get("variables", {}).items()}


def init_state() -> None:
    if "project" not in st.session_state:
        st.session_state.project = deepcopy(DEFAULT_PROJECT)
    if "selected_scene" not in st.session_state:
        st.session_state.selected_scene = st.session_state.project["meta"]["start_scene"]
    if "runtime_scene" not in st.session_state:
        st.session_state.runtime_scene = st.session_state.project["meta"]["start_scene"]
    if "runtime_variables" not in st.session_state:
        st.session_state.runtime_variables = runtime_defaults(st.session_state.project)
    if "runtime_log" not in st.session_state:
        st.session_state.runtime_log = []


def style() -> None:
    st.markdown("""
    <style>
    :root{--bg:#06171d;--panel:rgba(9,35,45,.86);--border:rgba(119,242,222,.3);--text:#eafffb;--accent:#70f0d0;--muted:#a4c8c6}
    div[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 10% 0%,rgba(31,91,120,.3),transparent 35%),linear-gradient(180deg,#05131a,var(--bg))}
    section[data-testid="stSidebar"]{background:rgba(3,15,20,.9);border-right:1px solid var(--border)}
    .block-container{padding-top:1.1rem;max-width:1500px}
    h1,h2,h3,h4,p,label,span,div{color:var(--text)}
    .card{border:1px solid var(--border);background:var(--panel);border-radius:14px;padding:1rem;margin:.5rem 0 1rem;box-shadow:0 10px 30px rgba(0,0,0,.18)}
    .kicker{color:var(--accent);font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:.78rem}
    .muted{color:var(--muted)}
    .screen{position:relative;margin:0 auto;background:#04131c;border:3px solid #5ba8d8;box-shadow:0 0 0 3px #0b3752,0 0 24px rgba(80,182,255,.25);overflow:hidden;image-rendering:pixelated}
    .screen img{width:100%;height:100%;object-fit:cover;image-rendering:pixelated}
    .copy{position:absolute;inset:0;padding:7%;display:flex;flex-direction:column;justify-content:flex-end;text-shadow:0 2px #000;background:linear-gradient(transparent 35%,rgba(0,12,20,.72))}
    .screen-title{color:#b7fff0;font-weight:900;letter-spacing:.08em;margin-bottom:.35rem}
    .screen-body{white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92rem;line-height:1.25}
    button[kind="primary"]{border-color:var(--accent)!important}
    div[data-testid="stExpander"]{border:1px solid var(--border);background:rgba(255,255,255,.025);border-radius:12px}
    </style>
    """, unsafe_allow_html=True)


def validate(project: dict[str, Any]) -> list[str]:
    errors = []
    scenes = project.get("scenes", {})
    variables = project.get("variables", {})
    start = project.get("meta", {}).get("start_scene", "")
    if start not in scenes:
        errors.append(f"Start scene '{start}' does not exist.")
    for sid, scene in scenes.items():
        for n, choice in enumerate(scene.get("choices", []), 1):
            action = choice.get("action", {})
            kind = action.get("type")
            label = choice.get("label", f"choice {n}")
            if kind == "goto" and action.get("target") not in scenes:
                errors.append(f"{sid} / {label}: missing target '{action.get('target')}'.")
            if kind == "set_variable":
                if action.get("variable") not in variables:
                    errors.append(f"{sid} / {label}: missing variable '{action.get('variable')}'.")
                if action.get("next") and action.get("next") not in scenes:
                    errors.append(f"{sid} / {label}: missing next scene '{action.get('next')}'.")
            if kind == "condition":
                if action.get("variable") not in variables:
                    errors.append(f"{sid} / {label}: missing variable '{action.get('variable')}'.")
                for branch in ("then", "else"):
                    if action.get(branch) not in scenes:
                        errors.append(f"{sid} / {label}: missing {branch} scene '{action.get(branch)}'.")
    return errors


def action_editor(action: dict[str, Any], key: str) -> dict[str, Any]:
    scenes = list(st.session_state.project["scenes"])
    variables = list(st.session_state.project["variables"])
    kind = st.selectbox("Action", ACTION_TYPES, index=idx(ACTION_TYPES, action.get("type", "goto")), key=f"{key}_kind")
    out: dict[str, Any] = {"type": kind}
    if kind == "goto":
        out["target"] = st.selectbox("Destination", scenes, index=idx(scenes, action.get("target", scenes[0])))
    elif kind == "dialogue":
        out["text"] = st.text_area("Dialogue", action.get("text", ""), key=f"{key}_text")
        options = [""] + scenes
        out["next"] = st.selectbox("Then go to", options, index=idx(options, action.get("next", "")), key=f"{key}_next")
    elif kind == "set_variable":
        out["variable"] = st.selectbox("Variable", variables, index=idx(variables, action.get("variable", variables[0] if variables else "")), key=f"{key}_var") if variables else ""
        definition = st.session_state.project["variables"].get(out["variable"], {})
        vtype = definition.get("type", "integer")
        current = action.get("value", definition.get("default"))
        if vtype == "boolean":
            out["value"] = st.checkbox("Value", bool(current), key=f"{key}_bool")
        elif vtype == "string":
            out["value"] = st.text_input("Value", str(current or ""), key=f"{key}_str")
        else:
            out["value"] = st.number_input("Value", value=int(current or 0), step=1, key=f"{key}_num")
        options = [""] + scenes
        out["next"] = st.selectbox("Then go to", options, index=idx(options, action.get("next", "")), key=f"{key}_next")
    elif kind == "condition":
        out["variable"] = st.selectbox("Variable", variables, index=idx(variables, action.get("variable", variables[0] if variables else "")), key=f"{key}_var") if variables else ""
        operators = ["==", "!=", ">", ">=", "<", "<="]
        out["operator"] = st.selectbox("Operator", operators, index=idx(operators, action.get("operator", "==")), key=f"{key}_op")
        definition = st.session_state.project["variables"].get(out["variable"], {})
        vtype = definition.get("type", "integer")
        current = action.get("value", definition.get("default"))
        if vtype == "boolean":
            out["value"] = st.checkbox("Compare with", bool(current), key=f"{key}_cmp_bool")
        elif vtype == "string":
            out["value"] = st.text_input("Compare with", str(current or ""), key=f"{key}_cmp_str")
        else:
            out["value"] = st.number_input("Compare with", value=int(current or 0), step=1, key=f"{key}_cmp_num")
        c1, c2 = st.columns(2)
        out["then"] = c1.selectbox("If true", scenes, index=idx(scenes, action.get("then", scenes[0])), key=f"{key}_then")
        out["else"] = c2.selectbox("If false", scenes, index=idx(scenes, action.get("else", scenes[0])), key=f"{key}_else")
    else:
        out["message"] = st.text_input("End message", action.get("message", "THE END"), key=f"{key}_end")
    return out


def project_page() -> None:
    meta = st.session_state.project["meta"]
    st.subheader("Project")
    a, b = st.columns([1.2, 1])
    with a:
        meta["title"] = st.text_input("Game title", meta["title"])
        meta["slug"] = norm(st.text_input("Project ID", meta["slug"]), "game")
        meta["author"] = st.text_input("Author", meta.get("author", ""))
        meta["version"] = st.text_input("Version", meta.get("version", "0.1.0"))
        meta["description"] = st.text_area("Description", meta.get("description", ""), height=120)
    with b:
        names = list(SCREEN_PRESETS)
        target = st.selectbox("Target layout", names, index=idx(names, meta.get("target", names[0])))
        meta["target"] = target
        if target != "Custom":
            meta["screen_width"], meta["screen_height"] = SCREEN_PRESETS[target]
            st.caption(f"Logical screen: {meta['screen_width']} × {meta['screen_height']}")
        else:
            c1, c2 = st.columns(2)
            meta["screen_width"] = c1.number_input("Width", 64, 1920, int(meta.get("screen_width", 240)))
            meta["screen_height"] = c2.number_input("Height", 64, 1080, int(meta.get("screen_height", 160)))
        scenes = list(st.session_state.project["scenes"])
        meta["start_scene"] = st.selectbox("Start scene", scenes, index=idx(scenes, meta.get("start_scene", scenes[0])))
    st.markdown('<div class="card"><div class="kicker">North Star</div><p>Content stays in structured project data. HTML, Python, Butano, and 3DS become separate runtimes.</p></div>', unsafe_allow_html=True)


def scenes_page() -> None:
    scenes = st.session_state.project["scenes"]
    st.subheader("Scenes and routing")
    left, right = st.columns([.34, 1])
    with left:
        ids = list(scenes)
        selected = st.selectbox("Scene", ids, index=idx(ids, st.session_state.selected_scene)) if ids else ""
        st.session_state.selected_scene = selected
        st.markdown("##### Add scene")
        name = st.text_input("Display name", key="new_scene_name")
        sid = st.text_input("Scene ID", value=norm(name, "new_scene"), key="new_scene_id")
        if st.button("Add scene", use_container_width=True):
            sid = norm(sid, "new_scene")
            if sid in scenes:
                st.error("That scene ID already exists.")
            else:
                scenes[sid] = {"name": name or sid.title(), "type": "room", "background": "", "body": "", "choices": [], "notes": ""}
                st.session_state.selected_scene = sid
                st.rerun()
        if selected and len(scenes) > 1:
            if st.button("Duplicate selected", use_container_width=True):
                base, n = f"{selected}_copy", 1
                copy_id = base
                while copy_id in scenes:
                    n += 1
                    copy_id = f"{base}_{n}"
                scenes[copy_id] = deepcopy(scenes[selected])
                scenes[copy_id]["name"] += " Copy"
                st.session_state.selected_scene = copy_id
                st.rerun()
            if st.button("Delete selected", use_container_width=True):
                del scenes[selected]
                st.session_state.selected_scene = next(iter(scenes), "")
                st.rerun()
    with right:
        if not selected:
            return
        scene = scenes[selected]
        st.caption(f"Scene ID: `{selected}`")
        c1, c2 = st.columns([2, 1])
        scene["name"] = c1.text_input("Scene name", scene.get("name", ""), key=f"{selected}_name")
        scene["type"] = c2.selectbox("Type", SCENE_TYPES, index=idx(SCENE_TYPES, scene.get("type", "room")), key=f"{selected}_type")
        scene["background"] = st.text_input("Background path", scene.get("background", ""), key=f"{selected}_bg", placeholder="assets/backgrounds/manias_stone.png")
        scene["body"] = st.text_area("Scene text", scene.get("body", ""), height=130, key=f"{selected}_body")
        scene["notes"] = st.text_area("Design notes", scene.get("notes", ""), height=80, key=f"{selected}_notes")
        st.markdown("#### Choices / hotspots")
        choices = scene.setdefault("choices", [])
        delete = None
        for i, choice in enumerate(choices):
            with st.expander(f"{i+1}. {choice.get('label','Choice')}", expanded=i == 0):
                choice["label"] = st.text_input("Label", choice.get("label", ""), key=f"{selected}_{i}_label")
                choice["action"] = action_editor(choice.get("action", {}), f"{selected}_{i}")
                if st.button("Delete choice", key=f"{selected}_{i}_delete"):
                    delete = i
        if delete is not None:
            choices.pop(delete)
            st.rerun()
        if st.button("Add choice / hotspot"):
            choices.append({"label": "NEW OPTION", "action": {"type": "goto", "target": selected}})
            st.rerun()


def variables_page() -> None:
    variables = st.session_state.project["variables"]
    st.subheader("Variables")
    name = st.text_input("New variable name")
    vid = st.text_input("Variable ID", value=norm(name, "new_variable"))
    vtype = st.selectbox("Type", ["integer", "boolean", "string"])
    if st.button("Add variable"):
        vid = norm(vid, "new_variable")
        if vid in variables:
            st.error("That variable already exists.")
        else:
            default: Any = 0 if vtype == "integer" else False if vtype == "boolean" else ""
            variables[vid] = {"type": vtype, "default": default, "notes": ""}
            st.rerun()
    delete = None
    for vid, definition in variables.items():
        with st.expander(vid):
            types = ["integer", "boolean", "string"]
            definition["type"] = st.selectbox("Type", types, index=idx(types, definition.get("type", "integer")), key=f"{vid}_type")
            if definition["type"] == "boolean":
                definition["default"] = st.checkbox("Default", bool(definition.get("default", False)), key=f"{vid}_bool")
            elif definition["type"] == "string":
                definition["default"] = st.text_input("Default", str(definition.get("default", "")), key=f"{vid}_str")
            else:
                definition["default"] = st.number_input("Default", value=int(definition.get("default", 0)), step=1, key=f"{vid}_num")
            definition["notes"] = st.text_input("Notes", definition.get("notes", ""), key=f"{vid}_notes")
            if st.button("Delete variable", key=f"{vid}_delete"):
                delete = vid
    if delete:
        del variables[delete]
        st.rerun()


def assets_page() -> None:
    assets = st.session_state.project["assets"]
    st.subheader("Asset manifest")
    st.caption("Repository paths remain the source of truth. Upload here only to preview.")
    uploaded = st.file_uploader("Preview image", type=["png", "jpg", "jpeg", "webp"])
    if uploaded:
        st.image(uploaded, caption=uploaded.name)
    with st.form("asset_form", clear_on_submit=True):
        aid = st.text_input("Asset ID")
        path = st.text_input("Repository path", placeholder="assets/backgrounds/manias_stone.png")
        kind = st.selectbox("Asset type", ["background", "sprite", "ui", "sound", "music", "font", "other"])
        notes = st.text_input("Notes")
        if st.form_submit_button("Add to manifest"):
            assets.append({"id": norm(aid or path.rsplit("/",1)[-1], "asset"), "path": path, "type": kind, "notes": notes})
            st.rerun()
    remove = None
    for i, asset in enumerate(assets):
        cols = st.columns([1, 2, 1, .4])
        cols[0].code(asset.get("id", ""))
        cols[1].write(asset.get("path", ""))
        cols[2].write(asset.get("type", ""))
        if cols[3].button("×", key=f"asset_{i}"):
            remove = i
    if remove is not None:
        assets.pop(remove)
        st.rerun()


def execute(action: dict[str, Any]) -> None:
    scenes = st.session_state.project["scenes"]
    kind = action.get("type")
    def go(target: str) -> None:
        if target in scenes:
            st.session_state.runtime_scene = target
            st.session_state.runtime_log.append(f"goto:{target}")
    if kind == "goto":
        go(action.get("target", ""))
    elif kind == "dialogue":
        st.session_state.runtime_log.append(f"dialogue:{action.get('text','')}")
        go(action.get("next", ""))
    elif kind == "set_variable":
        st.session_state.runtime_variables[action.get("variable", "")] = action.get("value")
        st.session_state.runtime_log.append(f"set:{action.get('variable')}={action.get('value')!r}")
        go(action.get("next", ""))
    elif kind == "condition":
        current = st.session_state.runtime_variables.get(action.get("variable"))
        expected = action.get("value")
        op = action.get("operator", "==")
        result = {"==": current == expected, "!=": current != expected}.get(op, False)
        if op in (">", ">=", "<", "<="):
            try:
                result = {">": current > expected, ">=": current >= expected, "<": current < expected, "<=": current <= expected}[op]
            except TypeError:
                result = False
        st.session_state.runtime_log.append(f"condition:{current!r} {op} {expected!r} -> {result}")
        go(action.get("then" if result else "else", ""))


def preview_page() -> None:
    project = st.session_state.project
    scenes = project["scenes"]
    meta = project["meta"]
    st.subheader("Playable logic preview")
    left, right = st.columns([.35, 1])
    with left:
        if st.button("Restart preview", use_container_width=True):
            st.session_state.runtime_scene = meta["start_scene"]
            st.session_state.runtime_variables = runtime_defaults(project)
            st.session_state.runtime_log = []
            st.rerun()
        jump = st.selectbox("Jump to scene", list(scenes), index=idx(list(scenes), st.session_state.runtime_scene))
        if st.button("Jump", use_container_width=True):
            st.session_state.runtime_scene = jump
            st.rerun()
        st.markdown("##### Runtime variables")
        st.json(st.session_state.runtime_variables)
        with st.expander("Runtime log"):
            st.code("\n".join(st.session_state.runtime_log[-30:]) or "No actions yet.")
    with right:
        sid = st.session_state.runtime_scene
        if sid not in scenes:
            sid = next(iter(scenes))
            st.session_state.runtime_scene = sid
        scene = scenes[sid]
        width, height = int(meta["screen_width"]), int(meta["screen_height"])
        dw = min(720, max(360, width * 2))
        dh = int(dw * height / width)
        bg = scene.get("background", "")
        img = f'<img src="{bg}" alt="" onerror="this.style.display=\'none\'">' if bg else ""
        st.markdown(f'<div class="screen" style="width:{dw}px;height:{dh}px">{img}<div class="copy"><div class="screen-title">{scene.get("name",sid)}</div><div class="screen-body">{scene.get("body","")}</div></div></div>', unsafe_allow_html=True)
        st.caption(f"`{sid}` · {scene.get('type','room')}")
        for i, choice in enumerate(scene.get("choices", [])):
            if st.button(choice.get("label", f"Choice {i+1}"), key=f"run_{sid}_{i}", use_container_width=True):
                execute(choice.get("action", {}))
                st.rerun()


def html_runtime(project: dict[str, Any]) -> str:
    data = json.dumps(project, ensure_ascii=False)
    title = project["meta"].get("title", "NorthStar Game")
    width, height = project["meta"].get("screen_width", 240), project["meta"].get("screen_height", 160)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#031219;color:#eafffb;font-family:monospace}}#app{{width:min(96vw,900px)}}#screen{{position:relative;width:100%;aspect-ratio:{width}/{height};overflow:hidden;border:4px solid #65b4df;background:#061b25;image-rendering:pixelated}}#bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;image-rendering:pixelated}}#copy{{position:absolute;inset:0;padding:7%;display:flex;flex-direction:column;justify-content:flex-end;text-shadow:0 2px #000;background:linear-gradient(transparent 35%,rgba(0,10,18,.8))}}#title{{color:#aaffea;font-weight:900;letter-spacing:.09em}}#body{{white-space:pre-wrap;margin-top:.5rem}}#choices{{display:grid;gap:.6rem;margin-top:1rem}}button{{padding:.8rem;color:#eafffb;background:#0b3040;border:1px solid #66e4c9;font:inherit;cursor:pointer}}#vars{{opacity:.7;font-size:.8rem;margin-top:1rem}}</style></head><body><div id="app"><div id="screen"><img id="bg" alt=""><div id="copy"><div id="title"></div><div id="body"></div></div></div><div id="choices"></div><div id="vars"></div></div><script>const project={data};const state={{scene:project.meta.start_scene,variables:Object.fromEntries(Object.entries(project.variables||{{}}).map(([k,v])=>[k,v.default]))}};const $=s=>document.querySelector(s);function go(t){{if(project.scenes[t]){{state.scene=t;render()}}}}function cmp(a,o,b){{return o==='=='?a===b:o==='!='?a!==b:o==='>'?a>b:o==='>='?a>=b:o==='<'?a<b:o==='<='?a<=b:false}}function run(a){{if(a.type==='goto')go(a.target);else if(a.type==='set_variable'){{state.variables[a.variable]=a.value;a.next?go(a.next):render()}}else if(a.type==='condition')go(cmp(state.variables[a.variable],a.operator||'==',a.value)?a.then:a.else);else if(a.type==='dialogue'){{if(a.text)alert(a.text);if(a.next)go(a.next)}}else if(a.type==='end')alert(a.message||'THE END')}}function render(){{const s=project.scenes[state.scene];$('#title').textContent=s.name||state.scene;$('#body').textContent=s.body||'';const bg=$('#bg');if(s.background){{bg.src=s.background;bg.style.display='block'}}else{{bg.style.display='none'}}const c=$('#choices');c.innerHTML='';(s.choices||[]).forEach(ch=>{{const b=document.createElement('button');b.textContent=ch.label;b.onclick=()=>run(ch.action||{{}});c.appendChild(b)}});$('#vars').textContent=JSON.stringify(state.variables)}}render();</script></body></html>'''


def cpp_header(project: dict[str, Any]) -> str:
    scenes = project["scenes"]
    enum_lines = "\n".join(f"        {norm(sid)}," for sid in scenes)
    records = []
    for sid, scene in scenes.items():
        name = json.dumps(scene.get("name", sid))
        body = json.dumps(scene.get("body", ""))
        records.append(f"        scene_record{{scene_id::{norm(sid)}, {name}, {body}}},")
    return f'''#ifndef NORTHSTAR_SCENES_H\n#define NORTHSTAR_SCENES_H\n\n#include <array>\n#include <string_view>\n\nnamespace northstar\n{{\n    enum class scene_id\n    {{\n{enum_lines}\n    }};\n\n    struct scene_record\n    {{\n        scene_id id;\n        std::string_view name;\n        std::string_view body;\n    }};\n\n    constexpr std::array<scene_record, {len(scenes)}> scenes = {{\n{chr(10).join(records)}\n    }};\n}}\n\n#endif\n'''


def export_zip(project: dict[str, Any]) -> bytes:
    buf = io.BytesIO()
    errors = validate(project)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project, indent=2, ensure_ascii=False))
        z.writestr("web/index.html", html_runtime(project))
        z.writestr("butano/include/northstar_scenes.h", cpp_header(project))
        z.writestr("validation.txt", "No routing errors found.\n" if not errors else "\n".join(errors))
        z.writestr("README.md", f"# {project['meta'].get('title','NorthStar Game')}\n\nGenerated by {APP_TITLE} {APP_VERSION}.\n")
    return buf.getvalue()


def export_page() -> None:
    project = st.session_state.project
    errors = validate(project)
    st.subheader("Validate and export")
    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("Routing is internally consistent.")
    c1, c2 = st.columns(2)
    c1.download_button("Download project JSON", json.dumps(project, indent=2, ensure_ascii=False).encode(), f"{project['meta']['slug']}.northstar.json", "application/json", use_container_width=True)
    c1.download_button("Download HTML preview", html_runtime(project).encode(), "index.html", "text/html", use_container_width=True)
    c2.download_button("Download complete export ZIP", export_zip(project), f"{project['meta']['slug']}_export.zip", "application/zip", use_container_width=True)
    c2.download_button("Download Butano scene header", cpp_header(project).encode(), "northstar_scenes.h", "text/plain", use_container_width=True)
    uploaded = st.file_uploader("Import project JSON", type=["json"])
    if uploaded:
        try:
            loaded = json.loads(uploaded.getvalue().decode())
            if "meta" not in loaded or "scenes" not in loaded:
                raise ValueError("Not a NorthStar game project.")
            if st.button("Replace current project"):
                st.session_state.project = loaded
                st.session_state.selected_scene = loaded["meta"].get("start_scene", next(iter(loaded["scenes"]), ""))
                st.session_state.runtime_scene = st.session_state.selected_scene
                st.session_state.runtime_variables = runtime_defaults(loaded)
                st.session_state.runtime_log = []
                st.rerun()
        except Exception as exc:
            st.error(str(exc))


def help_page() -> None:
    st.subheader("Workflow")
    st.markdown("""
1. **Project** — choose screen size and start scene.
2. **Variables** — define progression such as `stone_state`.
3. **Scenes** — enter dialogue, choices, and routes.
4. **Assets** — maintain a clean path manifest.
5. **Preview** — test logic without compiling.
6. **Export** — save JSON, HTML, and a starter Butano header.

This first version deliberately focuses on menu-driven game logic. A later version can add a tile-map canvas, hotspot coordinates, sprite animation, font preview, and full Butano project generation.
""")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🎮", layout="wide", initial_sidebar_state="expanded")
    init_state()
    style()
    st.markdown(f'<div class="card"><div class="kicker">ProjectNorthStar</div><h1 style="margin:.25rem 0">{APP_TITLE}</h1><div class="muted">Scene editor · dialogue input · routing · variables · preview · export</div></div>', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## Game Forge")
        page = st.radio("Workspace", ["Project", "Scenes", "Variables", "Assets", "Preview", "Export", "Help"], label_visibility="collapsed")
        st.divider()
        st.caption(st.session_state.project["meta"].get("title", "Untitled"))
        st.code(st.session_state.project["meta"].get("slug", "game"))
        if st.button("Reset starter project", use_container_width=True):
            st.session_state.project = deepcopy(DEFAULT_PROJECT)
            st.session_state.selected_scene = "title"
            st.session_state.runtime_scene = "title"
            st.session_state.runtime_variables = runtime_defaults(st.session_state.project)
            st.session_state.runtime_log = []
            st.rerun()
        st.caption(f"v{APP_VERSION}")
    {"Project": project_page, "Scenes": scenes_page, "Variables": variables_page, "Assets": assets_page, "Preview": preview_page, "Export": export_page, "Help": help_page}[page]()


if __name__ == "__main__":
    main()
