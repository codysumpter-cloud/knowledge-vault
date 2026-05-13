# Dirty KnowledgeVault Handoff Ingestion

Use when the user says a handoff was added to `codysumpter-cloud/knowledge-vault` but the local Obsidian/iCloud KnowledgeVault working tree may be dirty or behind.

## Pattern

1. Resolve the real vault root from `OBSIDIAN_VAULT_PATH` or the known iCloud path.
2. Inspect before mutating:
   ```bash
   git -C "$VAULT" status --short --branch
   git -C "$VAULT" remote -v
   ```
3. If the expected handoff file is absent and the tree is dirty, do **not** pull, merge, reset, or checkout over the working tree.
4. Fetch/read the specific commit or remote object safely:
   ```bash
   git -C "$VAULT" fetch --quiet origin <commit-sha>
   git -C "$VAULT" show <commit-sha>:99-System/Handoffs/<file>.md
   git -C "$VAULT" show --name-only --format='%H %s' --no-renames <commit-sha>
   ```
5. Ingest durable operating-state rules into memory/skills as appropriate, but do not write to the vault unless explicitly asked.

## Mac safety guardrails

- No recursive home scans to find the file; search the known vault root first, then use Git object reads.
- No watchers, daemons, full repo crawlers, npm installs, Docker builds, Xcode builds, or model downloads as routine handoff ingestion.
- Never run `git add .` / `git add ..`; if later committing, add explicit public-safe paths only.

## Receipts

Report only:

- real vault root used
- `git status --short --branch` summary
- target handoff path present/absent locally
- commit/file read successfully
- whether local working tree was left untouched
