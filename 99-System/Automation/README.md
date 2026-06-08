---
type: automation-readme
last_updated: 2026-06-04
tags:
  - automation
  - vault
---

# Vault Automation

This folder installs and runs the practical part of the Vault Steward.

## What it does

- Lists GitHub repositories for `codysumpter-cloud`.
- Creates or updates project-memory folders.
- Keeps public repo memory in `30 - Projects/GitHub/codysumpter-cloud/`.
- Keeps local-only repo memory in `00-Private/GitHub Projects/codysumpter-cloud/` unless `VAULT_TRACK_PRIVATE=true`.
- Regenerates indexes and registry files.
- Generates daily dashboard pages under `01-Dashboard/`.
- Runs the Vault Doctor safety check before committing.
- Commits and pushes allowlisted tracked paths when run through the wrapper script.

## Scripts

| Script | Purpose |
|---|---|
| `vault_maintainer.py` | Refresh repo project folders, indexes, registries, and steward logs. |
| `generate_vault_dashboards.py` | Generate `Today`, `Repo Health`, `Open PRs`, and `Agent Handoff` dashboards. |
| `vault_doctor.py` | Fail fast on tracked forbidden paths or unsafe automation staging. |
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

Then edit:

```bash
~/.config/knowledge-vault.env
```

Example:

```bash
VAULT_GITHUB_OWNER=codysumpter-cloud
VAULT_GITHUB_TOKEN=replace_with_local_read_token
VAULT_TRACK_PRIVATE=false
```

Keep `VAULT_TRACK_PRIVATE=false` while `knowledge-vault` is public.

## Manual run

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

The wrapper runs:

```bash
python3 "99-System/Automation/vault_maintainer.py"
python3 "99-System/Automation/generate_vault_dashboards.py"
python3 "99-System/Automation/vault_doctor.py"
```

## GitHub Actions setup

The daily workflow runs the same safe sequence and stages only allowlisted public paths.

Optional repository secret for expanded repo metadata access:

```txt
VAULT_MAINTAINER_TOKEN
```

Keep `VAULT_TRACK_PRIVATE` false unless the vault repo is private.

## Safety rules

- Do not use broad repository-wide staging.
- Do not stage `00-Private/`.
- Do not stage `99-System/Security/`.
- Do not overwrite human-authored notes unless they are inside explicit generated markers.
- Run `vault_doctor.py` before claiming a vault update is safe.
