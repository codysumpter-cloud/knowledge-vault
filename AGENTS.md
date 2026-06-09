# KnowledgeVault Agent Operating Contract

This vault is the project-memory source of truth for Prismtek's work.

## Source of truth rules

- GitHub is the source of truth for code, issues, pull requests, CI state, and releases.
- Obsidian is the source of truth for project memory: decisions, status, context, roadmaps, runbooks, handoffs, and daily agent logs.
- Private repo metadata must not be committed to a public vault.
- Local-only security material and workspace state must stay out of version control.

## Current agent direction

- OpenClaw is retired for current work. Do not use it as an active runtime, default toolchain, or product target.
- Hermes-agent is the current main working agent system.
- Buddy-agent is the intended primary and eventually only agent repository. New durable agent work should converge there.
- Buddy-brain remains continuity and memory context until Buddy-agent fully owns that role.
- KnowledgeVault is the book/memory layer, not the execution runtime.

## Prismtek operating preferences

- Discord relay outputs should be compact: 1500 characters or less, no code fences, no markdown tables, no emoji, minimal line breaks, and relay-safe wording.
- Prefer the smallest working step first, prove it, then continue.
- Inspect the system when unsure instead of guessing.
- Keep self-upgrades frozen until usefulness is proven.
- Preserve recovery branches and backups during risky repository work.

## Startup memory contract

Agents should read these files, in order, before trusting automation claims or editing the vault:

1. `README.md`
2. `AGENTS.md`
3. `SYSTEMMAP.md`
4. `AGENT_DATABASE_BLUEPRINT.md`
5. `RUNBOOK.md`
6. `BACKLOG.md`
7. `SECURITY.md`
8. `01-Dashboard/Today.md`
9. `01-Dashboard/Project Source of Truth.md`
10. `01-Dashboard/Agent Handoff.md`
11. relevant project notes under `30 - Projects/GitHub/codysumpter-cloud/`
12. relevant skill notes under `99-System/Agent Skills/`

## Agent database rules

KnowledgeVault should be treated as an agent memory database, not a loose markdown dump.

Agents should prefer notes that are:

- source-linked
- status-tagged
- last-verified when they make current claims
- scoped to known facts, assumptions, risks, and next actions
- public-safe

Agents should not blindly ingest the whole vault. Load the cold-start path, then retrieve task-specific project notes, skill notes, source packs, or generated bundles.

See `AGENT_DATABASE_BLUEPRINT.md` for the full design standard.

## Agent: Vault Steward

The Vault Steward maintains repo project folders, indexes, registries, dashboards, and daily logs.

Default behavior:

1. Fetch public repos for `codysumpter-cloud`.
2. Ensure every public repo has an Obsidian project folder.
3. Generate or refresh `Project.md`, `Agent Context.md`, `Decisions.md`, and `Tasks.md` when missing.
4. Preserve human-written notes outside generated blocks.
5. Update the GitHub project index and public repo registry.
6. Generate dashboard pages under `01-Dashboard/`.
7. Run `99-System/Automation/vault_doctor.py` before committing automation updates.
8. Commit changes through GitHub Actions when files changed.

Private repo handling is opt-in only. Keep `VAULT_TRACK_PRIVATE=false` unless the vault repository is private.

## Skill claim rules

A skill note in KnowledgeVault is a reference unless proven otherwise in the target runtime repo.

Use explicit status wording:

- `reference` — useful source material only
- `draft` — designed but not implemented
- `ported` — copied/adapted into the target repo
- `wired` — connected to a runtime or app path
- `tested` — validated by command, CI, or runtime behavior
- `disabled` — intentionally unavailable
- `public-alpha-safe` — allowed for guarded public alpha use

## Safety invariants

- Never write private repo names into tracked public files.
- Never print sensitive values into logs.
- Never commit files under `00-Private/**`.
- Never commit files under `99-System/Security/**`.
- Never overwrite human-authored sections unless they are between explicit generated markers.
- Prefer additive updates over destructive rewrites.
