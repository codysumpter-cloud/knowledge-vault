---
name: worldbox-control
description: "Reliable control and automation of WorldBox - God Simulator using the worldbox-agent-bridge toolset."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [WorldBox, Automation, God-Sim, Vision-Lock, Surgical-Mode]
    related_skills: [hermes-agent]
---

# WorldBox Control

Controlling WorldBox via synthetic input is brittle due to UI overlays, coordinate drift (camera move/zoom), and macOS security restrictions. This skill implements a "Surgical" approach to ensure reliability and prevent accidental triggers (like the "Quit Game" prompt).

## The "Surgical" Operational Loop

NEVER batch actions or perform "blind" clicks. Every single interaction must follow this strict loop:
1. **Ready**: Run `worldboxctl ready <label>` to focus the game and take a baseline shot.
2. **Inspect**: Use vision to find the EXACT current pixels of the tool and target in that specific frame.
3. **Act**: Execute ONE action using `worldboxctl click` or `zones click` with `--slow --hold 250`.
4. **Verify**: Run `worldboxctl ready <label>` again and verify the result visually.
5. **Emit**: Log the action to the AgentCraft HUD (`worldboxctl emit`).

## Modal & Focus Safety
WorldBox menus (Quit, Settings, Unit Info) block all map interactions.
- **Hard Stop**: If a modal/quit/settings prompt appears, run `worldboxctl modal-stop "reason"` and STOP immediately. Ask the user to clear it manually.
- **Safe Clear**: Use `worldboxctl safe-clear --esc 1 --label close-info-panel` ONLY when a normal info panel (e.g., Unit Profile) is open.
- **Strict Ban**: NEVER use `clear-ui 5` or spam the Escape key; this is a legacy approach that often triggers the Quit prompt.

## The "Divine Strategist" Pivot
If `worldboxinput probe` confirms that synthetic input is ignored by WorldBox (a common macOS issue), or if Vision AI identifies a coordinate mismatch between "Scan" and "Act" frames, STOP all autonomous clicking. Pivot to **Divine Strategist Mode**:
- Provide the user with precise coordinates and step-by-step instructions.
- User performs the action manually.
- Agent verifies the result via screenshot.
- This is the only viable path until a real Mod Bridge (NML/BepInEx) is active.

## Xcode & SDK Requirements
For any build-related tasks (iOS, macOS, Windows), a full installation of the **Xcode Application** is required.
- **Path Verification**: The active developer directory must be set to `/Applications/Xcode.app/Contents/Developer`.
- **Common Failure**: If `xcodebuild` reports that the active directory is `/Library/Developer/CommandLineTools`, the agent must fix this via `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`.
- **Installation Check**: If the command fails, verify the app is moved from `~/Downloads` to `/Applications`.

## Installation Pitfalls
When installing the `worldbox-agent-bridge` zips, be aware that they often extract into a nested directory (e.g., `~/bridge/bridge/apps`). Always verify the path to `package.json` before running `npm link`.

## Vanilla Achievement Recipes
Achievements must be step-verified.

### The Princess
1. Spawn **Frog**.
2. Verify frog exists.
3. Apply **Bless**.
4. Verify transformation.

### Ant World
1. Spawn **10 Blue Ants**, **10 Black Ants**, **10 Green Ants**, **10 Red Ants** in separate, distant corners of the map to prevent early combat.
2. Verify all 40 ants are present before concluding.

### Ninja Turtle
1. Spawn **Turtle**.
2. Apply **Madness**.
3. Spawn **Grasshoppers** in small batches.
4. Verify turtle is fighting/leveling.

### Super Mushroom
1. Spawn creature.
2. Apply **MUSH Spores**.
3. Kill creature to convert to Mush.
4. Use **Powerup** on Mush.
5. Verify.
