# Interactive Obsidian Plugin Stack

Date: 2026-05-13

This vault is now prepared for the full interactive Obsidian setup Prismtek asked for.

## Current answer

Hermes only read the handoff. He did not finish installing or activating the full Obsidian interactive stack.

This vault update adds:

- a full visual/dashboard/plugin manifest
- desktop-full, interactive-safe, and mobile-safe plugin profiles
- a Mac-safe plugin installer
- graph/canvas/dashboard setup notes
- an explicit Hermes setup checklist

## Source-of-truth split

- GitHub remains source of truth for code, issues, pull requests, CI, and releases.
- KnowledgeVault / Obsidian remains source of truth for project memory, decisions, daily notes, handoffs, dashboards, and agent context.
- OpenClaw is retired for current work.
- Hermes-agent is current.
- Buddy-agent is being prepared to become the primary and eventually only agent repository.

## Plugin profiles

### interactive-safe

Default profile. Enables graph/canvas/dashboard/project plugins while avoiding known desktop-only agent/API plugins.

File:

`KnowledgeVault/.obsidian/plugin-profiles/interactive-safe.community-plugins.json`

### desktop-full

Desktop-only profile. Enables everything, including agentic and AI plugins already present in the vault.

File:

`KnowledgeVault/.obsidian/plugin-profiles/desktop-full.community-plugins.json`

Use only after Hermes has confirmed the Mac is on power and not under load.

### mobile-safe

iPhone/iPad fallback profile. Avoids Git, local API, desktop agent, and heavy AI/indexing plugins.

File:

`KnowledgeVault/.obsidian/plugin-profiles/mobile-safe.community-plugins.json`

## Installed or already present

Already present plugin folders include:

- `bmo-command-center`
- `bmo-ops-dashboard`
- `calendar`
- `copilot`
- `dataview`
- `meld-encrypt`
- `obsidian-excalidraw-plugin`
- `obsidian-git`
- `obsidian-kanban`
- `obsidian-linter`
- `obsidian-local-rest-api`
- `obsidian-tasks-plugin`
- `omnisearch`
- `periodic-notes`
- `quickadd`
- `smart-composer`
- `smart-connections`
- `table-editor-obsidian`
- `templater-obsidian`

## New install targets

The installer should fetch these from the Obsidian community registry or explicit GitHub releases:

- `advanced-canvas` — Advanced Canvas: flowcharts, presentations, canvas metadata, collapsible groups.
- `juggl` — Advanced interactive graph workspace; mobile-capable per plugin docs but may be slower on large vaults.
- `breadcrumbs` — Hierarchy and typed relationship layer; integrates with Juggl.
- `style-settings` — Theme/plugin visual settings.
- `metadata-menu` — Project metadata/property editing layer.
- `homepage` — Open to the dashboard/control center.
- `cmdr` — Ribbon/command customization for iPhone and desktop workflows.
- `obsidian-icon-folder` — Folder/file icons for project cockpit navigation.
- `buttons` — Clickable note commands for dashboards and workflows.
- `obsidian-charts` — Chart rendering inside notes.
- `obsidian-tracker` — Habit/status trend views from daily notes.
- `obsidian-projects` — Project database/views.
- `dbfolder` — Database-style folders/views.
- `waypoint` — Folder indexes/MOCs.
- `excalibrain` — Graph-style semantic concept maps for Excalidraw/Obsidian.
- `make-md` — Enhanced spaces, navigation, and file experience.
- `obsidian42-brat` — Manual beta plugin install path for plugins not in the community registry.
- `claudxian` — Desktop-only Codex/Claude-style agent inside Obsidian. Do not enable on iPhone.

## Important mobile note

iPhone should be treated as a cockpit, not the engine room.

Use iPhone for:

- viewing dashboards
- editing notes
- quick capture
- graph/canvas browsing where responsive
- tasks and project review

Do not run on iPhone:

- agent loops
- repo maintenance
- local APIs
- heavy AI indexing
- Git automation
- model downloads
