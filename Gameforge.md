NorthStar Dev Forge for GB Studio

Purpose

NorthStar Dev Forge is not intended to replace GB Studio.

It is a companion toolkit that prepares assets, organizes scene logic, previews transitions, and helps design puzzles before they are implemented inside GB Studio.

GB Studio remains the main game-building environment because it already provides:

scene organization

actor placement

event scripting

dialogue

variables

music and sound integration

ROM and web export

a visual workflow that does not require full custom coding

NorthStar Dev Forge should strengthen the parts that GB Studio handles less efficiently.

Core Principle

The workflow should remain:

Create or import asset
→ Process it in NorthStar Dev Forge
→ Review the result
→ Export a GB Studio-ready file or design document
→ Implement it inside GB Studio

The Forge should never rewrite or replace a GB Studio project directly unless that workflow becomes proven and reliable.

Planned Tools

1. Scene Image Converter

Goal

Convert an imported image into a scene image that can be used in GB Studio.

Inputs

PNG

JPG

JPEG

WEBP

generated artwork

screenshots

scanned sketches

Processing options

resize to exact scene dimensions

crop or letterbox

convert to Game Boy or Game Boy Color palette

reduce color count

preserve strong silhouettes

simplify detail

improve contrast

sharpen important edges

preview tile readability

warn when an image is too detailed

export multiple conversion attempts

Target presets

Game Boy scene:       160 × 144
Game Boy background:  160 × 144
Game Boy Color:       160 × 144
Game Boy sprite:      GB Studio-compatible dimensions
Custom preview:       user-defined

Possible outputs

scene_name_gb.png
scene_name_gbc.png
scene_name_high_contrast.png
scene_name_simplified.png
scene_name_notes.txt

Future AI support

AI may later help identify:

focal objects

important paths

likely interaction areas

overly detailed regions

text readability problems

sprite/background separation issues

2. Sprite Bundle Builder

Goal

Collect one or more character or object images and prepare them for later conversion into GB Studio sprites.

Inputs

full-body character images

front, back, and side views

animation frames

object images

icons

enemy concepts

generated sprite references

Functions

background removal

crop and center

scale normalization

sprite-sheet arrangement

frame naming

direction grouping

idle and walk grouping

preview animation

export individual frames

export contact sheet

generate sprite conversion notes

Suggested bundle structure

character_name/
├── source/
├── processed/
├── front/
├── back/
├── left/
├── right/
├── idle/
├── walk/
├── interaction/
└── sprite_manifest.json

Example manifest

{
  "name": "player",
  "frame_size": [16, 16],
  "directions": ["front", "back", "left", "right"],
  "animations": {
    "idle": 1,
    "walk": 2
  },
  "notes": "Convert final frames inside GB Studio sprite editor."
}

The Forge should prepare and organize the material. Final GB Studio sprite compatibility remains the last check.

3. Logic Maker for AI-Assisted Implementation

Goal

Create clear game logic that can be pasted into an AI system and translated into GB Studio events.

This tool should not pretend to generate perfect GB Studio scripting automatically.

It should produce a structured implementation brief.

Inputs

current scene

interaction trigger

dialogue

menu choices

variables

conditions

destination scenes

win state

lose state

return route

locked route

sound or transition notes

Example output

SCENE: Manias Stone

TRIGGER:
Player interacts with the stone actor.

VARIABLE:
Stone State

STATE VALUES:
0 = inactive
1 = puzzle completed, beam pending
2 = fully activated

LOGIC:
If Stone State = 0:
- Ask: "INITIATE RESONANCE TEST?"
- YES → change scene to Stone Puzzle
- NO → remain in Manias Stone

If Stone State = 1:
- change scene to Stone Beam

If Stone State = 2:
- display: "THE STONE IS ALREADY ACTIVE."

STONE PUZZLE:
- Lose or withdraw → return to Manias Stone
- Win → set Stone State to 1
- Change scene to Stone Beam

STONE BEAM:
- play activation sequence
- set Stone State to 2
- continue to CT2

DO NOT CHANGE:
- Locked Screen routing
- existing terminal route

Export formats

plain text

Markdown

JSON

AI prompt

checklist

scene-by-scene event plan

Future goal

An AI system may eventually read the logic output, inspect a GB Studio project, and suggest exact event placement.

Until then, the output should remain understandable to a human.

4. Puzzle Maker for GB Studio

Goal

Design puzzles that are realistic to implement inside GB Studio.

The Forge should not create puzzle concepts that depend on systems GB Studio cannot reasonably support.

Puzzle categories

menu puzzles

sequence puzzles

switch puzzles

symbol alignment

memory puzzles

terminal codes

tile stepping

object placement

variable-based locks

dialogue-choice puzzles

point-and-click scenes

simple match or alignment games

Puzzle builder fields

Puzzle name
Scene name
Instructions
Player objective
Available controls
Number of attempts
Win condition
Lose condition
Reset behavior
Variables used
Scenes used
Required actors
Required backgrounds
Required UI images
Sound cues
Transition after win
Return route after loss

Puzzle output

The tool should produce:

puzzle design summary

variable list

scene list

actor list

event sequence

win route

loss route

reset logic

testing checklist

AI-ready implementation prompt

Design rule

Every puzzle should answer:

Can this be built in GB Studio without custom engine work?

Possible result labels:

GREEN  = straightforward in GB Studio
YELLOW = possible but event-heavy
RED    = requires custom scripting or redesign

5. Scene Transition Viewer

Goal

Preview how one scene leads into another before rebuilding the route in GB Studio.

Functions

arrange scenes in order

display scene thumbnails

preview fades

preview cuts

preview dialogue before transition

preview locked-screen detours

preview puzzle win and loss routes

review variable-dependent branches

show scene duration

show transition notes

export a storyboard or route map

Example route

Year Terminal
→ Artifact
→ Manias Stone
→ Initiate prompt
→ Stone Puzzle
→ Stone Beam
→ CT2

Branch view

Manias Stone
├── NO
│   └── remain at Manias Stone
└── YES
    └── Stone Puzzle
        ├── LOSE
        │   └── Manias Stone
        └── WIN
            └── Stone Beam
                └── CT2

Viewer modes

linear storyboard

branching map

slideshow preview

transition timing preview

variable-state preview

Export options

PNG route map

PDF storyboard

Markdown route summary

JSON transition data

AI implementation prompt

Recommended App Structure

The Forge can remain lightweight and modular.

ProjectNorthStar/
└── python_hubs/
    └── game_forge/
        ├── app.py
        ├── pages/
        │   ├── scene_converter.py
        │   ├── sprite_bundle.py
        │   ├── logic_maker.py
        │   ├── puzzle_maker.py
        │   └── transition_viewer.py
        ├── core/
        │   ├── image_tools.py
        │   ├── palette_tools.py
        │   ├── project_schema.py
        │   ├── validation.py
        │   └── exporters.py
        ├── presets/
        │   ├── gb.json
        │   ├── gbc.json
        │   └── gb_studio.json
        └── projects/

Streamlit is acceptable for this companion toolkit because these tools mainly involve:

forms

previews

image processing

file downloads

scene ordering

structured text generation

simple transition visualization

It does not need to become a full visual game engine.

Project Data Model

Each Forge project should use a neutral project file.

{
  "project_name": "Blue Crystal",
  "target": "GB Studio",
  "screen_size": [160, 144],
  "scenes": [],
  "sprites": [],
  "variables": [],
  "puzzles": [],
  "transitions": [],
  "notes": []
}

This file should describe the project without modifying the GB Studio source project.

Relationship to GB Studio

NorthStar Dev Forge handles

image conversion

visual preparation

sprite organization

logic documentation

puzzle planning

route visualization

AI-ready prompts

export checklists

GB Studio handles

actual scene creation

actor placement

event scripting

variables

collision

gameplay

dialogue execution

music and sound

build and export

ROM testing

Non-Goals

NorthStar Dev Forge is not currently intended to:

replace GB Studio

compile a Game Boy ROM

edit .gbsproj files directly

generate perfect GB Studio event scripts

become a full tile-map editor

become a full animation editor

replace Butano

convert the entire game into custom C++

silently alter existing routes

These may be revisited later only if tooling and AI become reliable enough.

Development Order

Phase 1

Scene Image Converter

Logic Maker

Scene Transition Viewer

These provide immediate value and have low risk.

Phase 2

Sprite Bundle Builder

Puzzle Maker

These require more validation and project structure.

Phase 3

optional GB Studio project inspection

AI-assisted event suggestions

route validation against uploaded project files

asset compatibility checks

automated documentation generation

First Practical Milestone

The first working Forge release should allow a user to:

Upload a scene image
→ convert it to 160 × 144
→ reduce it to a GB-compatible palette
→ preview and download it

Create a route
→ define scenes, choices, variables, and destinations
→ preview the sequence
→ export an AI-ready implementation plan

Design a puzzle
→ define win and lose states
→ receive a GB Studio feasibility rating
→ export the event checklist

That is enough to make the Forge useful without pretending it is a complete game editor.

Guiding Rule

GB Studio builds the game. NorthStar Dev Forge prepares, explains, previews, and organizes the work around it.
