---
name: worldbox-completionist
description: "Guide and automate the 100% completion of WorldBox - God Simulator on macOS."
version: 1.1.0
author: Hermes Agent
license: MIT
---

# WorldBox Completionist

A comprehensive approach to unlocking all vanilla traits, achievements, species, equipment, and collection items in WorldBox.

## Core Philosophy
Act as a **Divine Strategist** and **Unlock Checklist**. Prioritize efficiency and targeted unlocks over random chaos.

## Technical Constraints (macOS)
- **Input Issues:** Standard synthetic clicks (e.g., `cliclick`) are frequently ignored by the game engine (OpenGL/Metal) or blocked by macOS Accessibility permissions.
- **Synthetic Click Syntax:** If using `cliclick` for "slow clicks" to bypass input filters, use `dd:x,y` for button down and `du:x,y` for button up, with `w:ms` for wait (e.g., `cliclick -w 150 m:500,500 dd:500,500 w:250 du:500,500`).
- **Dynamic Coordinates:** Fixed coordinates are invalidated by camera movement and zoom. Always use a **Vision-Lock Loop**.
- **UI Overlays:** Unit profiles, religion windows, and the Main Menu/Quit prompt block map clicks. Ensure all panels are closed. If the "Quit Game" menu is open, it must be closed via the 'NO' button or 'X' before map interaction is possible.

## Operational Workflow

### The Vision-Lock Loop (For Map Interaction)
Whenever an action is required on the map:
1. **Snapshot:** `screencapture` the current view.
2. **Targeting:** Use `vision_analyze` to find the exact current pixel coordinates.
3. **Execution:** Use `cliclick` (or provide coordinates to the user).
4. **Verification:** Snapshot again to confirm the result.
5. **Spread-Clicking:** If a single click fails, use a 3x3 grid of clicks (+/- 5px) around the target.

### The Bridge Workflow (Using `worldboxctl`)
If the `worldbox-agent-bridge` is installed, follow the **Reliability Wrapper** sequence to prevent UI interference and coordinate drift:
1. `worldboxctl focus` $\rightarrow$ Ensure the game is the active window.
2. `worldboxctl clear-ui 5` $\rightarrow$ Wipe away overlapping info panels.
3. `worldboxctl shot` $\rightarrow$ Capture a clean snapshot for vision analysis.
4. **Inspect** $\rightarrow$ Find target coordinates.
5. **Execute** $\rightarrow$ Use `worldboxctl click` or `zones click`.
6. **Verify** $\rightarrow$ Screenshot and report.
7. **Step-Verification:** For complex achievements (e.g., Princess), do NOT batch. Verify each sub-step (e.g., tool selected $\rightarrow$ entity spawned $\rightarrow$ effect applied) before proceeding.

## Completionist Strategies

### 1. Safe Achievement Farming
- **The Arena:** Build small mountain-walled enclosures to isolate fights.
- **Unit Purity:** Use fresh, unedited units for strict achievements. Edited units (e.g., 'Enhanced Penguins') may disqualify certain unlocks.
- **Support:** Use Blood Rain to heal target units during long fights.

### 2. Known Vanilla Farms
- **The Princess:** Spawn Frog $\rightarrow$ Bless.
- **Ninja Turtle:** Spawn Turtle $\rightarrow$ Apply Madness $\rightarrow$ Spawn Grasshoppers around it.
- **Super Mushroom:** Spawn Creature $\rightarrow$ Apply MUSH Spores $\rightarrow$ Powerup the resulting mushroom.
- **Slayers:** Create an arena $\rightarrow$ Spawn King/Mage $\rightarrow$ Spawn Warrior $\rightarrow$ Confirm kill.

## User Preferences
- **Anti-Chaos:** Do not randomly wipe civilizations.
- **Preservation:** Use the Cloner or Smooth Jazz to preserve populations before destructive tests.
- **Order of Operations:**
    1. Passive collection sweep (viewing/hovering).
    2. Safe achievement farming.
    3. Targeted species/subspecies discovery.
    4. New world creation for remaining gaps.
