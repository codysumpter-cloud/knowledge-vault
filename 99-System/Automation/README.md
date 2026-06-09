---
type: automation-readme
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-09
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - automation
  - vault
---

# Vault Automation

This folder installs and runs the practical part of the Vault Steward.

## Purpose

Vault automation keeps KnowledgeVault useful as an agent memory database by refreshing public repo memory, dashboards, registries, and quality checks without overwriting human-authored context.

## What it does

- Lists GitHub repositories for `codysumpter-cloud`.
- Creates or updates project-memory folders.
- Keeps public repo memory in `30 - Projects/GitHub/codysumpter-cloud/`.
- Keeps local-only repo memory out of public tracked paths unless the repository model changes.
- Regenerates indexes and registry files.
- Generates daily dashboard pages under `01-Dashboard/`.
- Runs the Vault Doctor safety check before committing.
- Can run the note quality linter to check formatting and agent-readiness.
- Commits and pushes allowlisted tracked paths when run through the wrapper script.

## Scripts

| Script | Purpose |
|---|---|
| `vault_maintainer.py` | Refresh repo project folders, indexes, registries, and steward logs. |
| `generate_vault_dashboards.py` | Generate `Today`, `Repo Health`, `Open PRs`, and `Agent Handoff` dashboards. |
| `vault_doctor.py` | Fail fast on tracked forbidden paths or unsafe automation staging. |
| `note_quality_linter.py` | Flag notes that are hard for agents to retrieve, trust, or maintain. |
| `run-vault-maintenance.sh` | Local wrapper that runs maintainer, dashboards, doctor, and safe commit flow. |
| `run-vault-steward-mac-safe.sh` | Conservative Mac-safe runner with lock, battery, thermal, and load checks. |
| `install-local-vault-steward.sh` | Local install helper. |

## One-time local setup

From the vault root:

```bash
chmod +x "99-System/Automation/run-vault-maintenance.sh"
chmod +x "99-System/Automation/install-local-vault-steward.sh"
"99-System/Automation/install-local-vault-steward.sh"
```

Then edit the local vault environment file documented by the installer.

Keep private repo tracking disabled while `knowledge-vault` is public.

## Manual run

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

The wrapper runs the maintainer, dashboard generator, and doctor.

For a formatting-quality pass, also run:

```bash
python3 "99-System/Automation/note_quality_linter.py"
```

JSON output:

```bash
python3 "99-System/Automation/note_quality_linter.py" --json
```

Strict mode:

```bash
python3 "99-System/Automation/note_quality_linter.py" --strict
```

## GitHub Actions setup

The daily workflow runs the safe maintenance sequence and stages only allowlisted public paths.

Expanded repo metadata access can be configured through repository-level settings if needed.

Keep private tracking disabled unless the vault repository model changes.

## Safety rules

- Do not use broad repository-wide staging.
- Do not stage local-only private folders.
- Do not stage security-only folders.
- Do not overwrite human-authored notes unless they are inside explicit generated markers.
- Run `vault_doctor.py` before claiming a vault update is safe.
- Run `note_quality_linter.py` before claiming a formatting or agent-readiness pass is complete.

## Quality workflow

For a full docs/knowledge maintenance pass:

```bash
python3 "99-System/Automation/vault_doctor.py"
python3 "99-System/Automation/note_quality_linter.py"
```

Then inspect warnings and fix the highest-value notes first:

1. Root docs.
2. Active repo project notes.
3. Skill notes with runtime claims.
4. Context bundle manifests.
5. Generated dashboards and indexes.

## Agent instructions

- Treat linter warnings as guidance, not permission to rewrite everything.
- Prefer small additive fixes.
- Do not replace human-authored sections unless explicitly asked.
- Keep source links close to volatile claims.
- Record meaningful maintenance work in a handoff or receipt when useful.
