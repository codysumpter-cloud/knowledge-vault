# Hermes Handoff — Finish Obsidian Interactive Stack

Date: 2026-05-13

Hermes, this is the missing setup task.

You already read the earlier handoff, but you did not finish applying the Obsidian interactive/plugin stack.

## Current state

- Real vault root reported by Hermes:
  `/Users/codysumpter/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault`
- The vault working tree was dirty.
- Hermes correctly did not pull into a dirty working tree.
- Hermes read the GitHub handoff commit only.
- The full plugin/dashboard setup still needs to be applied locally.

## What this ZIP adds

- Full interactive plugin manifest:
  `99-System/Obsidian/obsidian-interactive-stack.manifest.json`
- Plugin profiles:
  `.obsidian/plugin-profiles/interactive-safe.community-plugins.json`
  `.obsidian/plugin-profiles/desktop-full.community-plugins.json`
  `.obsidian/plugin-profiles/mobile-safe.community-plugins.json`
- Mac-safe installer:
  `99-System/Automation/install-obsidian-interactive-stack-mac-safe.sh`
- Python installer:
  `99-System/Automation/install_obsidian_plugins_from_manifest.py`
- Setup docs:
  `99-System/Obsidian/INTERACTIVE_PLUGIN_STACK.md`
  `99-System/Obsidian/Interactive Vault Control Center.md`

## Required operating direction

- OpenClaw is retired for current work.
- Hermes-agent is current.
- Buddy-agent is being prepared to become the primary and eventually only agent repository.
- KnowledgeVault / Obsidian is the project-memory source of truth.
- GitHub remains source of truth for code, issues, pull requests, CI, and releases.

## Mac performance constraints

Do not degrade Prismtek's Mac.

Do not run:

- watchers
- daemons
- recursive home scans
- all-repo crawls
- Docker builds
- npm installs
- Xcode builds
- local model downloads
- local inference jobs
- embedding/indexing jobs unless Prismtek explicitly asks

Installer must run once, low priority, and stop.

## Safe local procedure

From the real vault root:

1. Inspect only.

```bash
cd "/Users/codysumpter/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault"
git status --short --branch
```

2. Back up current Obsidian config before changing it.

```bash
mkdir -p "99-System/Backups/obsidian-config-2026-05-13"
cp -R .obsidian "99-System/Backups/obsidian-config-2026-05-13/.obsidian.backup"
```

3. Copy the updated ZIP contents into the vault root without deleting local-only files.

4. Install missing visual/community plugins using the Mac-safe installer only.

```bash
chmod +x "99-System/Automation/install-obsidian-interactive-stack-mac-safe.sh"
"99-System/Automation/install-obsidian-interactive-stack-mac-safe.sh"
```

5. Open Obsidian desktop and verify:

- Graph opens.
- Canvas opens.
- Advanced Canvas appears if installed.
- Juggl appears if installed.
- Project dashboard opens.
- Dataview/Tasks/Kanban/Excalidraw still work.

6. Do not run `git add .`.

If committing, only stage public-safe paths explicitly.

## Success criteria

Hermes may claim setup complete only after:

- plugin profile files exist
- missing plugins are installed or logged as unavailable
- Obsidian opens without obvious plugin startup errors
- iPhone-safe caveat remains documented
- Mac was not slowed down by long-running jobs
