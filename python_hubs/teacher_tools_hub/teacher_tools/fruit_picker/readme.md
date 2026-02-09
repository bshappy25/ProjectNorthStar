# Citrus Picker — Dual Tray Zenith (Offline)

**Citrus Picker** is an offline, single-file HTML arcade prototype designed to measure **accuracy, allocation discipline, and decision commitment** under increasing cognitive load.

Although presented as a casual fruit-sorting game, the system is intentionally structured to harvest **reaction-agnostic performance signals** for difficulty tuning, accessibility testing, and future AI-assisted analysis.

---

## Core Gameplay

Players manage **two simultaneous objectives**:

### 1) Match Tray (Exact Match)
- 4 slots, each requiring a **specific fruit**
- All four must be correct to complete the tray
- Precision matters; proximity assists are disabled

### 2) Drop Tray (Capacity)
- Holds **10 fruits of any type**
- Larger target with forgiving placement
- Designed to test throughput and prioritization

Players must balance **precision (match tray)** against **throughput (drop tray)**.

---

## Accuracy-First Scoring Model (0–100)

Final score is derived from three components:

- **A — Successful tray drops**  
  (both match and drop trays)
- **B — Unallocated fruit**  
  (all remaining fruit becomes *dead fruit* unless Zenith is achieved)
- **C — Placement accuracy**  
  (correct vs incorrect interactions)

Accuracy is the dominant signal; speed alone cannot produce a high score.

**Zenith condition:**  
> Score ≥ **85/100** within a session

---

## Pepper Mechanic 🌶️

Peppers introduce controlled urgency:

- Spawn probabilistically
- Must be **double-tapped** to destroy
- If ignored, expire after a short fuse and become **dead fruit**
- Destroying peppers grants bonus points (no penalty for tray drop)

Peppers are intended to compete for attention, not overwhelm core objectives.

---

## Difficulty Model

Difficulty adjusts:
- Spawn rate
- Maximum on-screen fruit
- Session time limit
- Pepper frequency

Difficulty is designed to increase **allocation pressure**, not reflex demand.

---

## Session Structure (Development Mode)

- Sessions are **forced in batches of 5**
- A session ends by:
  - Zenith achievement
  - Time limit
  - Manual abort
- Aggregate stats are generated after the 5th session

---

## Export Format

After 5 sessions, the game produces a **copy-pasteable text export** containing:

- Aggregate performance
- Per-difficulty breakdown
- Full per-session logs
- All metrics required for external analysis

Example use cases:
- Pasting into ChatGPT or Claude for tuning recommendations
- Comparing difficulty curves
- Evaluating accessibility impact

No network connection or identifiers are required.

---

## Design Philosophy

- **Accuracy over speed**
- **Commitment over reaction**
- **Offline first**
- **Explainable metrics**
- **No real-time AI control**

This project treats AI as an *analysis layer*, not a gameplay dependency.

---

## Status

Prototype validated through multiple development sessions.  
Tuning ongoing; mechanics intentionally transparent.