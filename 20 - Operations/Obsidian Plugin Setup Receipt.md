---
type: setup-receipt
system: obsidian
status: configured
updated: 2026-05-11T15:24:19
---
# Obsidian Plugin Setup Receipt

## Core plugins enabled
- File explorer, Global search, Quick switcher, Graph, Backlinks, Canvas
- Outgoing links, Tags, Page preview, Daily notes, Templates
- Command palette, Slash commands, Properties, Bookmarks
- Workspaces, Outline, Word count, File recovery

## Community plugins enabled
- BMO Ops Dashboard
- BMO Command Center
- Dataview
- Templater
- Tasks
- QuickAdd
- Calendar
- Periodic Notes
- Advanced Tables
- Omnisearch
- Kanban
- Excalidraw
- Obsidian Git (auto-push disabled)
- Linter
- Meld Encrypt

## Installed but intentionally disabled until secure secret handoff
- Local REST API
- Copilot
- Smart Connections
- Smart Composer

## Secrets posture
- BMO Command Center now adds Settings → BMO Command Center → **BMO Secrets**.
- Entries save to macOS Keychain service `obsidian-bmo`.
- No API key values are stored in notes, `data.json`, or workspace files.
- Secret map note: `00-Private/Credentials/SECRET_INDEX.md`.

## Verification
- BMO plugin JavaScript syntax: passed with `node --check`.
- Obsidian JSON config validation: passed.
- Regex scan for common plaintext API key patterns in `.obsidian/*.json`: zero hits.
