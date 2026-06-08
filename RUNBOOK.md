# KnowledgeVault Runbook

This runbook describes safe, repeatable maintenance for KnowledgeVault.

## Golden rule

KnowledgeVault is public. Treat every tracked file as publishable.

Never commit secrets, private repo names, private project notes, credential inventories, signed-in session details, or local-only operational logs.

## Before changing the vault

1. Read [`README.md`](README.md).
2. Read [`AGENTS.md`](AGENTS.md).
3. Read [`SYSTEMMAP.md`](SYSTEMMAP.md).
4. Read [`SECURITY.md`](SECURITY.md).
5. Check current GitHub issues and PRs if making repo-level changes.
6. Run or mentally apply `vault_doctor.py` before claiming a change is safe.

## Local setup

From the vault root:

```bash
chmod +x "99-System/Automation/run-vault-maintenance.sh"
chmod +x "99-System/Automation/install-local-vault-steward.sh"
"99-System/Automation/install-local-vault-steward.sh"
```

Then configure local environment values in:

```bash
~/.config/knowledge-vault.env
```

Example:

```bash
VAULT_GITHUB_OWNER=codysumpter-cloud
VAULT_GITHUB_TOKEN=replace_with_local_token
VAULT_TRACK_PRIVATE=false
```

Keep `VAULT_TRACK_PRIVATE=false` while this repository is public.

## Run safety checks

```bash
python3 "99-System/Automation/vault_doctor.py"
```

The doctor checks for:

- tracked private paths
- tracked security paths
- `.env` files
- secret-like filenames
- token/key-like content patterns in tracked text files
- workflow attempts to stage forbidden paths
- accidental `git add .` usage in automation scripts

A passing doctor check does not prove perfection. It is a guardrail, not a substitute for review.

## Run vault maintenance

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

The Vault Steward should:

1. Fetch repo metadata.
2. Ensure public repo project folders exist.
3. Keep private repo memory local-only unless explicitly allowed.
4. Refresh indexes and registries.
5. Preserve human-authored content outside generated sections.
6. Write daily maintenance logs.
7. Stage only approved public-safe paths.

## Daily GitHub Actions workflow

The workflow lives at:

```txt
.github/workflows/vault-steward-daily.yml
```

It should:

1. Check out the vault.
2. Run the Vault Steward.
3. Run `vault_doctor.py`.
4. Commit safe generated changes only.

The workflow must not stage:

- `00-Private/**`
- `99-System/Security/**`
- `99-System/Logs/**`
- `99-System/Backups/**`
- `99-System/Prompts/**`
- `99-System/Templates/**`
- credential or signing files

## Adding a project note

When adding or improving a repo project note, use this shape:

```md
# repo-name

> One-line purpose.

## Links

- GitHub:
- Default branch:
- Primary app/runtime, if any:

## Current status

- Status:
- Priority:
- Last verified:

## Project intent

What this repo is for.

## Current known state

What is known from README, issues, PRs, and recent work.

## Agent context

Build/test commands, risks, special setup, and constraints.

## Decisions

Links to decision records or short durable decisions.

## Next actions

- [ ] Concrete next action.
```

## Adding a skill note

Skill notes should say:

- what the skill does
- when to use it
- when not to use it
- required tools/secrets/network access
- risk level
- public-alpha availability
- input/output contract
- validation steps
- source files or upstream references

Avoid claiming a skill is wired into Buddy-agent unless the Buddy-agent repo actually contains and tests that integration.

## Decision record format

Use this concise format:

```md
## YYYY-MM-DD — Decision title

**Decision:** What changed.

**Why:** Rationale.

**Scope:** What this affects.

**Risks:** Known risks or open questions.

**Owner:** Human or agent responsible.
```

## PR checklist

Before opening a PR:

- [ ] Root docs still tell the true current story.
- [ ] No private material was added.
- [ ] `vault_doctor.py` passes.
- [ ] Generated files are clearly generated or safe to review.
- [ ] Human-authored sections were not overwritten accidentally.
- [ ] Any public claims about runtime capability are verified in the relevant runtime repo.

## Emergency cleanup

If a secret or private detail is committed:

1. Stop further pushes.
2. Revoke or rotate the exposed credential immediately.
3. Remove the value from the repo.
4. Treat public Git history as compromised.
5. Use GitHub secret scanning and history rewriting only after rotation.
6. Record a sanitized incident note without repeating the secret.

Do not preserve secret values in the vault for evidence.
