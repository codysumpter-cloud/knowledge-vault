---
type: automation-readme
last_updated: 2026-05-13
tags:
  - automation
  - vault
---

# Vault Automation

This folder installs the practical part of the Vault Steward.

## What it does

- Lists GitHub repositories for `codysumpter-cloud`.
- Creates/updates project-memory folders.
- Keeps public repo memory in `30 - Projects/GitHub/codysumpter-cloud/`.
- Keeps private repo memory in `00-Private/GitHub Projects/codysumpter-cloud/` unless `VAULT_TRACK_PRIVATE=true`.
- Regenerates indexes and registry files.
- Commits and pushes safe tracked paths when run through the wrapper script.

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

Add a GitHub token with repo read access. For private repos, the token needs access to private repositories.

```bash
VAULT_GITHUB_OWNER=codysumpter-cloud
VAULT_GITHUB_TOKEN=ghp_REPLACE_ME
# Keep false while knowledge-vault is public.
VAULT_TRACK_PRIVATE=false
```

## Manual run

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

## GitHub Actions setup

The included workflow runs daily, but full private repo refresh requires a repository secret:

```txt
VAULT_MAINTAINER_TOKEN
```

Keep `VAULT_TRACK_PRIVATE` false unless the vault repo is private.
