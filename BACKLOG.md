# KnowledgeVault Backlog

This backlog ranks improvements that make KnowledgeVault a better book for humans and a better operating memory/database for agents.

## Priority legend

- **P0:** needed for safe public operation.
- **P1:** high-value usability or agent-readiness improvement.
- **P2:** polish, scale, or future integration.

## P0 — Safety and truthfulness

### 1. Keep public/private boundaries strict

**Status:** In progress.

**Why:** The repo is public. Private repo names, sensitive local paths, and security material must not leak into tracked files.

**Done when:**

- `vault_doctor.py` runs in CI.
- Workflow staging excludes forbidden paths.
- `00-Private/**` and `99-System/Security/**` stay untracked.
- Root docs clearly explain the public safety model.

### 2. Remove stale or false capability claims

**Status:** Needed.

**Why:** The vault can store skills and plans, but a skill existing in the vault does not prove it is wired, tested, or enabled in Buddy-agent.

**Done when:**

- Skill notes use status labels: `reference`, `draft`, `ported`, `wired`, `tested`, `disabled`, `public-alpha-safe`.
- Public docs distinguish knowledge references from runtime capabilities.

### 3. Make KnowledgeVault self-describing

**Status:** In progress.

**Why:** A human or agent should understand the repo from the root without prior chat context.

**Done when:**

- Root `README.md` exists.
- `SYSTEMMAP.md`, `RUNBOOK.md`, `SECURITY.md`, and `BACKLOG.md` exist.
- `AGENT_DATABASE_BLUEPRINT.md` defines the agent-database standard.
- The `knowledge-vault` project note is marked active and explains its purpose.

## P1 — Agent database quality

### 4. Upgrade repo project notes from scaffolds to useful briefs

**Status:** Needed.

**Why:** Generated project folders are useful structure, but placeholders like “Needs triage” do not help agents make decisions.

**Done when:**

Each active repo has:

- purpose
- current state
- build/test commands
- open risks
- active PR/issue summary
- next recommended actions
- source links

### 5. Generate daily repo health dashboards

**Status:** Needed.

**Why:** Agents need an at-a-glance daily operating page.

**Done when:**

Vault Steward generates:

- `01-Dashboard/Today.md`
- `01-Dashboard/Repo Health.md`
- `01-Dashboard/Open PRs.md`
- `01-Dashboard/Agent Handoff.md`

### 6. Add machine-readable skill registry

**Status:** Needed.

**Why:** The skill index is readable, but Buddy-agent needs structured metadata.

**Done when:**

A canonical registry exists with fields like:

```json
{
  "id": "github-pr-workflow",
  "name": "GitHub PR Workflow",
  "category": "github",
  "runtime": "hermes",
  "status": "reference",
  "risk_level": "medium",
  "requires_private_config": false,
  "requires_network": true,
  "allowed_in_public_alpha": true,
  "entrypoint": "99-System/Agent Skills/Hermes Skills/github/github-pr-workflow/SKILL.md"
}
```

### 7. Add note quality linting

**Status:** Needed.

**Why:** The vault should stay digestible as it grows.

**Done when:**

A linter flags notes missing:

- title
- purpose
- status
- last verified date
- next action
- source links where claims depend on external state

### 8. Add retrieval receipts

**Status:** Needed.

**Why:** Agents should be able to explain which vault files, bundles, and live sources influenced meaningful answers or repo actions.

**Done when:**

- Bundle export scripts produce a receipt ID.
- Agent actions can list loaded vault files.
- Stale or unverified claims are surfaced before action.
- Safety checks are recorded without exposing sensitive material.

## P2 — Productization

### 9. Add agent bootstrap packs

**Status:** Needed.

**Why:** Different agents need different context windows.

**Done when:**

The vault includes compact boot packs for:

- Buddy-agent maintainer
- Prismtek-apps maintainer
- Vault Steward
- public-alpha reviewer
- PokeMMO coach
- content/social ops assistant

### 10. Split public/private vaults or make this repo private

**Status:** Future decision.

**Why:** The current public vault is useful, but a true operating memory will eventually need private context.

**Options:**

1. Keep this repo public and create a separate private memory repo.
2. Make this repo private and publish selected docs elsewhere.
3. Keep public/private split inside one repo with strong local-only rules.

**Current recommendation:** keep this repo public, but create a separate private companion vault before storing deeper operational memory.

### 11. Connect Buddy-agent to curated vault exports

**Status:** Future.

**Why:** Buddy should not ingest the entire vault blindly. It should ingest curated, public-safe, task-specific packs.

**Done when:**

- Export scripts produce compact context bundles.
- Buddy-agent can load a bundle by task type.
- Receipts show which bundle was used.

### 12. Add graph/index exports

**Status:** Future.

**Why:** Agents will benefit from structured edges between projects, decisions, skills, runbooks, and source packs.

**Done when:**

- The vault can emit a public-safe graph index.
- Nodes include type, status, freshness, and source-of-truth metadata.
- Edges connect repos to decisions, skills to runtimes, and runbooks to tasks.
