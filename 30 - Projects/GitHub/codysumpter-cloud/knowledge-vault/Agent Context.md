---
type: project
status: active
owner: Prismtek
source_of_truth: mixed
last_verified: 2026-06-09
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - github/repo
  - project-context
  - knowledge-vault
  - agent-memory
---

# Agent Context — knowledge-vault

> Use this file when an agent is asked to update, repair, or improve KnowledgeVault itself.

## Purpose

This note gives agents a practical working context for `codysumpter-cloud/knowledge-vault`.

The vault is the public memory/database layer for Prismtek. It is not the runtime. GitHub owns code and live repo state; KnowledgeVault owns durable project memory, routing, decisions, standards, context bundles, and handoffs.

## Working agreement

- Treat this folder as the durable context packet for this repo.
- Keep source code in GitHub; keep decisions, status, and operating memory here.
- Prefer small, reviewable changes.
- Log important decisions in `Decisions.md`.
- Preserve human-authored content outside explicit generated markers.
- Keep public/private boundaries strict.

## Startup path

Before making repo changes, read:

1. `README.md`
2. `AGENTS.md`
3. `SYSTEMMAP.md`
4. `AGENT_KNOWLEDGE_INDEX.md`
5. `AGENT_DATABASE_BLUEPRINT.md`
6. `99-System/Context Bundles/cold-start/bundle.md`
7. `99-System/Standards/NOTE_FORMAT_STANDARD.md`
8. `RUNBOOK.md`
9. `SECURITY.md`
10. `BACKLOG.md`

## Verify

Run or account for these checks before claiming a vault maintenance pass is complete:

```bash
python3 "99-System/Automation/vault_doctor.py"
python3 "99-System/Automation/note_quality_linter.py"
```

For local maintenance:

```bash
"99-System/Automation/run-vault-maintenance.sh"
```

## Important paths

| Path | Use |
|---|---|
| `README.md` | Public front door. |
| `AGENTS.md` | Agent operating contract. |
| `AGENT_KNOWLEDGE_INDEX.md` | Agent task routing. |
| `AGENT_DATABASE_BLUEPRINT.md` | Database/retrieval standard. |
| `SYSTEMMAP.md` | Human and agent navigation. |
| `RUNBOOK.md` | Safe operations. |
| `BACKLOG.md` | Improvement roadmap. |
| `SECURITY.md` | Publication boundaries. |
| `99-System/Standards/` | Formatting and record-shape rules. |
| `99-System/Schemas/` | Machine-readable schemas. |
| `99-System/Context Bundles/` | Curated context bundles. |
| `99-System/Automation/` | Vault Steward and quality scripts. |
| `30 - Projects/GitHub/` | Repo project memory. |

## Known risks

- Root docs may drift if new standards are added but not linked.
- Skill notes can be mistaken for working runtime features unless status is explicit.
- Generated repo scaffolds can look authoritative even when they are placeholders.
- Current GitHub state must be checked live before claims about PRs, CI, branches, or releases.
- Context bundles can become stale unless their manifests are reviewed.

## Agent instructions

When improving this repo:

1. Start from the cold-start bundle.
2. Pick the smallest useful set of files.
3. Add standards/schemas/bundles before broad rewriting.
4. Upgrade placeholders into useful briefs when you touch them.
5. Use source links and last-verified dates near current claims.
6. Avoid claiming runtime capability unless verified in the owning runtime repo.
7. Add a receipt or handoff for meaningful changes.

## Handoff notes

### 2026-06-09 — Agent usability pass

Added the first formal agent usability layer:

- note format standard
- record examples
- metadata schema
- context bundle schema
- cold-start context bundle
- note quality linter
- agent knowledge index
- root docs wired to these resources

Next best step: add more task-specific bundles and run the note quality linter locally to prioritize note cleanup.
