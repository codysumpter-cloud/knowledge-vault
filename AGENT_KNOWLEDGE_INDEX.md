# KnowledgeVault Agent Knowledge Index

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

This index tells an agent where to start, what to load, and what to verify before making claims or changing the vault.

Use it after reading `README.md`, `AGENTS.md`, and `SYSTEMMAP.md`.

## Fast start

| Need | Load |
|---|---|
| Cold-start orientation | `99-System/Context Bundles/cold-start/bundle.md` |
| Vault purpose and public front door | `README.md` |
| Agent operating rules | `AGENTS.md` |
| Navigation map | `SYSTEMMAP.md` |
| Agent database design | `AGENT_DATABASE_BLUEPRINT.md` |
| Note formatting rules | `99-System/Standards/NOTE_FORMAT_STANDARD.md` |
| Copyable record shapes | `99-System/Standards/RECORD_EXAMPLES.md` |
| Context bundle rules | `99-System/Context Bundles/README.md` |
| Metadata schema | `99-System/Schemas/note.schema.json` |
| Bundle schema | `99-System/Schemas/context-bundle.schema.json` |
| Safe maintenance | `RUNBOOK.md` |
| Current roadmap | `BACKLOG.md` |

## Agent load order

1. Read `README.md` for purpose.
2. Read `AGENTS.md` for behavior rules.
3. Read `SYSTEMMAP.md` for navigation.
4. Read this file for task routing.
5. Load the smallest matching context bundle.
6. Load task-specific project, skill, source, or runbook notes.
7. Verify volatile claims against the owning source.
8. Produce a receipt for meaningful actions.

## Task routing

| Task | Primary files | Verify live? |
|---|---|---|
| Explain the vault | `README.md`, `SYSTEMMAP.md`, this index | No, unless claiming current repo status. |
| Improve formatting | `NOTE_FORMAT_STANDARD.md`, `RECORD_EXAMPLES.md` | No. |
| Add project memory | project folder under `30 - Projects/GitHub/`, record examples | Yes, verify repo state. |
| Add or assess a skill | skill note, skill registry, target runtime repo | Yes, verify runtime status. |
| Maintain the vault | `RUNBOOK.md`, automation docs | Yes, verify changed files. |
| Generate a context bundle | context bundle README and schema | Yes, verify included paths. |
| Use Wikipedia/source packs | source pack README and generated concept cards | Yes for current/high-stakes claims. |
| Review publication readiness | `SECURITY.md`, `AGENTS.md`, `vault_doctor.py` | Yes. |

## Trust levels

| Label | Meaning | Agent behavior |
|---|---|---|
| `confirmed` | Verified against source or command. | Can cite with source. |
| `reference` | Useful background. | Do not treat as runtime truth. |
| `draft` | Proposed but not proven. | Do not claim as active. |
| `wired` | Connected to runtime path. | Still check tests before strong claims. |
| `tested` | Validated by command, CI, or runtime behavior. | Prefer for capability claims. |
| `stale` | Needs re-checking. | Verify before use. |

## What makes knowledge useful here

A useful vault note should:

- have a clear title and summary
- say what type of record it is
- say who owns it
- name the source of truth
- include a last verified date for current claims
- separate facts from assumptions
- link to source material
- explain what an agent should verify before acting
- include a next action or say no action is needed

## Current best next improvements

1. Add front matter to the most important existing notes.
2. Run the note quality linter and triage warnings.
3. Upgrade generated repo project notes from scaffolds into useful briefs.
4. Add task-specific bundles for Buddy-agent, Prismtek apps, Vault Steward, and public-alpha review.
5. Add receipts to meaningful agent-maintained updates.
6. Promote skill notes into a maintained registry with verification status.

## Agent reminder

This vault is a memory and retrieval layer. It helps you find the right context; it does not replace live verification for current repo state, CI, releases, or runtime capability claims.
