# KnowledgeVault Cold Start Bundle

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

Use this bundle to orient a new agent or human to KnowledgeVault without relying on previous chat history.

## Load these files first

1. [`README.md`](../../../README.md)
2. [`AGENTS.md`](../../../AGENTS.md)
3. [`SYSTEMMAP.md`](../../../SYSTEMMAP.md)
4. [`AGENT_DATABASE_BLUEPRINT.md`](../../../AGENT_DATABASE_BLUEPRINT.md)
5. [`99-System/Standards/NOTE_FORMAT_STANDARD.md`](../../Standards/NOTE_FORMAT_STANDARD.md)
6. [`RUNBOOK.md`](../../../RUNBOOK.md)
7. [`SECURITY.md`](../../../SECURITY.md)
8. [`BACKLOG.md`](../../../BACKLOG.md)

## Operating summary

KnowledgeVault is Prismtek's public agent memory database and human-readable operating book.

Its job is to preserve durable project memory, decisions, runbooks, handoffs, indexes, and source-guided knowledge. It is not the execution runtime. GitHub remains the source of truth for code, issues, pull requests, CI state, and releases.

## Agent rules

- Do not blindly ingest the entire vault.
- Load this cold-start bundle, then pick task-specific files.
- Verify current repo/PR/CI/runtime claims against the owning source before acting.
- Treat skill notes as references unless their status is wired/tested and verified in the owning runtime repo.
- Keep public/private boundaries strict.
- Preserve human-authored content outside generated markers.

## What to inspect next

| Task | Inspect next |
|---|---|
| Repo purpose/status | `30 - Projects/GitHub/.../Project.md`, then GitHub repo |
| Build/test instructions | `Agent Context.md`, then repo README/workflows |
| Runtime capability claim | skill note + target runtime repo + verification receipt |
| Vault maintenance | `RUNBOOK.md`, `99-System/Automation/README.md`, Vault Steward spec |
| Public safety question | `SECURITY.md`, `.gitignore`, `AGENTS.md` |
| Formatting or knowledge-quality question | `99-System/Standards/NOTE_FORMAT_STANDARD.md` |
| Broad concept learning | relevant source pack README + concept cards + live verification when needed |

## Known limits

- This bundle does not include live GitHub state.
- This bundle does not prove runtime features are wired.
- This bundle does not include private project memory.
- This bundle is intentionally small; load task-specific context after orientation.

## Receipt seed

```json
{
  "bundle": "cold-start",
  "loaded_files": [
    "README.md",
    "AGENTS.md",
    "SYSTEMMAP.md",
    "AGENT_DATABASE_BLUEPRINT.md",
    "99-System/Standards/NOTE_FORMAT_STANDARD.md",
    "RUNBOOK.md",
    "SECURITY.md",
    "BACKLOG.md"
  ],
  "live_sources_checked": [],
  "known_unverified_claims": [
    "Current GitHub state must be checked live.",
    "Runtime capability status must be checked in the owning runtime repo."
  ]
}
```
