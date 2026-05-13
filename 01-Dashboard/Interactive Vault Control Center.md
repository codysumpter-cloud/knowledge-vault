# Interactive Vault Control Center

Updated: 2026-05-13

This is the cockpit for the interactive KnowledgeVault setup.

## Start here

- [[99-System/Obsidian/INTERACTIVE_PLUGIN_STACK|Interactive Plugin Stack]]
- [[99-System/Handoffs/2026-05-13-Hermes-Obsidian-Interactive-Stack|Hermes Interactive Stack Handoff]]
- [[30 - Projects/GitHub/GitHub Projects Index|GitHub Projects Index]]
- [[99-System/Agents/Vault Steward/AGENT|Vault Steward]]
- [[99-System/Agents/Hermes/AGENT|Hermes Agent]]

## Current direction

- OpenClaw is retired for current work.
- Hermes-agent is current.
- Buddy-agent is becoming the primary agent repository.
- KnowledgeVault is the project-memory source of truth.

## Visual systems

- Graph view: enabled as a core plugin.
- Canvas: enabled as a core plugin.
- Advanced Canvas: install target for flowcharts, presentations, portals, and canvas metadata.
- Juggl: install target for interactive graph workspaces.
- Excalidraw: already present for sketches and visual thinking.

## Daily rhythm

1. Capture new project state.
2. Link it to the relevant repo project folder.
3. Turn decisions into durable notes.
4. Let Hermes maintain indexes only when the Mac-safe policy allows it.

## Mac safety

Hermes must not run watchers, recursive home scans, local inference, Docker, npm installs, Xcode builds, or indexing jobs as routine vault maintenance.
