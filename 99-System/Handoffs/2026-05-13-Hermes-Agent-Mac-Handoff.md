# Hermes Agent Mac Handoff — KnowledgeVault Update

Date: 2026-05-13
Owner: Prismtek
Audience: Hermes agent running on Prismtek's Mac

## What changed

- KnowledgeVault is the project-memory source of truth.
- GitHub remains source of truth for code, issues, pull requests, CI, and releases.
- OpenClaw is retired for current work.
- Hermes-agent is the current main working agent system.
- Buddy-agent is being prepared to become the primary and eventually only agent repository.
- The new public fork `codysumpter-cloud/caveman` was added to the vault project map.

## What ChatGPT/BMO completed

1. Hardened the Obsidian vault Git sync posture.
2. Added project-memory folders for GitHub repos under `30 - Projects/GitHub/codysumpter-cloud/`.
3. Kept private repo/project memory under local-only `00-Private/` so it does not leak into a public vault.
4. Installed a Vault Steward operating model inside the vault.
5. Added current agent direction memory:
   - OpenClaw is retired for current work.
   - Hermes-agent is the current main working agent system.
   - Buddy-agent is being prepared to become the primary and eventually only agent repository.
   - KnowledgeVault / Obsidian is the project-memory source of truth.
6. Added the newly forked public repo `codysumpter-cloud/caveman` to the vault project map.
7. Updated the live `knowledge-vault` GitHub repo where connector permissions allowed it.
8. Added live `buddy-agent` root `AGENTS.md` and `memory.md` with current direction.
9. Could not directly update protected `buddy-brain` master because branch protection requires PR flow.

## Hermes next steps

1. Work only from the real `KnowledgeVault/` vault root.
2. Inspect before mutating: run `git status --short --branch` and verify the expected vault files exist.
3. Verify project folders for buddy-agent, buddy-brain, hermes-agent, knowledge-vault, and caveman.
4. Treat OpenClaw folders as historical/reference only.
5. Never run `git add .`; only add explicit public-safe paths.
6. Do not schedule anything unless Prismtek explicitly asks.

## Local inspection checklist

Run only lightweight checks first:

- Confirm current path is the vault root.
- Run `git status --short --branch`.
- List these files if present:
  - `AGENTS.md`
  - `memory.md`
  - `memory/2026-05-13.md`
  - `99-System/Memory/CURRENT_AGENT_DIRECTION.md`
  - `99-System/Handoffs/2026-05-13-Hermes-Agent-Mac-Handoff.md`
  - `30 - Projects/GitHub/codysumpter-cloud/caveman/Project.md`

Stop and report if the vault root is wrong, Git is dirty in unexpected ways, or private files appear staged.

## Project map verification

Verify these project folders exist:

- `30 - Projects/GitHub/codysumpter-cloud/buddy-agent/`
- `30 - Projects/GitHub/codysumpter-cloud/buddy-brain/`
- `30 - Projects/GitHub/codysumpter-cloud/hermes-agent/`
- `30 - Projects/GitHub/codysumpter-cloud/knowledge-vault/`
- `30 - Projects/GitHub/codysumpter-cloud/caveman/`

For OpenClaw-related folders, treat them as historical/reference only. Do not schedule or launch OpenClaw work.

## Sync safety

Before pushing anything, confirm `.gitignore` protects:

- `00-Private/**`
- `99-System/Security/**`
- certificate/signing files
- private key material
- local workspace state
- Hermes archive logs
- accidental nested vaults

Never run `git add .` in this vault.

Use explicit adds only. A safe add set is:

`git add AGENTS.md memory.md memory/2026-05-13.md "99-System" "30 - Projects/GitHub"`

Then inspect:

`git status --short`

Only commit if the staged files are public-safe. Never stage or push ZIPs, `00-Private/**`, `99-System/Security/**`, certificates, signing requests, or secrets.

## Mac performance rules

This is a hard operating rule.

Do not run background watchers, repo crawlers, full-text indexers, all-repo clones, model downloads, npm installs, Docker builds, or recursive scans unless Prismtek explicitly asks.

Default maintenance cadence:

- at most once daily
- run in low-priority mode
- exit quickly if another run is active
- fetch metadata only, not full repository contents
- do not clone every GitHub repo
- do not run during game/dev sessions if CPU, memory, thermal pressure, or battery are constrained

Use `99-System/Automation/run-vault-steward-mac-safe.sh` for local maintenance.

## Buddy-agent migration posture

Hermes should keep doing current agent work only until Buddy-agent is ready.

New durable agent architecture, memory contracts, and agent runtime decisions should be written toward Buddy-agent first, with KnowledgeVault as the memory/index source of truth.

Buddy-brain should remain continuity context, not the final destination.

## Report format back to Prismtek

Use Discord-safe compact formatting when relaying through PrismBot or constrained bot surfaces:

- 1500 characters or less
- no code fences
- no markdown tables
- no emoji
- no backticks
- minimal line breaks
- compressed prompts

Report these fields:

- Vault root confirmed: yes/no
- Git dirty state: clean/dirty and why
- Caveman folder present: yes/no
- Current direction files present: yes/no
- Any private files staged: yes/no
- Maintenance scheduled: no unless Prismtek explicitly asked
- Next smallest safe step

## Stop conditions

Stop before any destructive or expensive action.

Stop if:

- the vault path is ambiguous
- private files are staged
- a command would clone many repos
- a command would start a watcher or daemon
- a command would run more often than daily
- CPU or memory pressure is elevated
- battery is low or thermal pressure is not nominal
- GitHub auth fails
- branch protection requires a PR
