# KnowledgeVault System Map

This map explains how to navigate KnowledgeVault as both a human-readable book and an agent-readable operating memory.

## Mental model

KnowledgeVault has three jobs:

1. **Orient:** explain the Prismtek/Buddy/Hermes ecosystem clearly enough that a new human or agent can get productive quickly.
2. **Remember:** preserve project decisions, repo state, handoffs, runbooks, and reusable skill knowledge.
3. **Protect:** keep public knowledge public-safe while keeping private notes, secrets, and sensitive operational details out of Git.

## Source-of-truth split

| Topic | Source of truth |
|---|---|
| Code | GitHub repositories |
| Issues and PRs | GitHub |
| CI and releases | GitHub Actions / release systems |
| Project memory | KnowledgeVault |
| Durable decisions | KnowledgeVault |
| Agent handoffs | KnowledgeVault |
| Skills and runbooks | KnowledgeVault / Buddy-agent once ported |
| Secrets | Never KnowledgeVault |
| Private notes while public | Local-only `00-Private/**` |

## Top-level reading path

Use this path for a cold start:

1. [`README.md`](README.md) — public front door.
2. [`AGENTS.md`](AGENTS.md) — rules for agents.
3. [`SYSTEMMAP.md`](SYSTEMMAP.md) — this navigation map.
4. [`RUNBOOK.md`](RUNBOOK.md) — how to maintain or safely modify the vault.
5. [`SECURITY.md`](SECURITY.md) — what must not be published.
6. [`BACKLOG.md`](BACKLOG.md) — current improvement plan.
7. [`01-Dashboard/Project Source of Truth.md`](01-Dashboard/Project%20Source%20of%20Truth.md) — main dashboard.
8. [`30 - Projects/GitHub/GitHub Projects Index.md`](30%20-%20Projects/GitHub/GitHub%20Projects%20Index.md) — repo memory index.
9. [`99-System/Agent Skills/Skill Index.md`](99-System/Agent%20Skills/Skill%20Index.md) — skill catalog.

## Folder guide

### `01-Dashboard/`

Human-readable front pages and project dashboards.

Use it to answer:

- What matters right now?
- Which projects exist?
- What should an agent inspect first?
- What is the current operating direction?

### `30 - Projects/GitHub/`

Project-memory folders for GitHub repositories.

Each repo should eventually have:

- `Project.md` — intent, current status, repo links, source-of-truth pointers.
- `Agent Context.md` — build/test commands, risks, gotchas, handoff notes.
- `Decisions.md` — durable decisions and rationale.
- `Tasks.md` — open vault-side tasks.

GitHub is still the source of truth for the code. These notes are the source of truth for context.

### `99-System/Agents/`

Agent specifications, operating loops, and logs.

Start with:

- [`99-System/Agents/Vault Steward/AGENT.md`](99-System/Agents/Vault%20Steward/AGENT.md)

### `99-System/Automation/`

Scripts and wrappers that maintain the vault.

Important files:

- `vault_maintainer.py` — syncs repo memory folders and indexes.
- `vault_doctor.py` — checks for public-safety hazards.
- `run-vault-maintenance.sh` — local maintenance wrapper.
- `README.md` — setup and maintenance notes.

### `99-System/Agent Skills/`

Mirrored Hermes/Buddy skill material.

Use this as a reference library, not as proof that every skill is currently wired into Buddy-agent. Skills need status metadata before public/runtime claims are made.

### `99-System/Repositories/`

Generated registries for public repo metadata.

These files are machine-readable inputs for dashboards and agents.

### `00-Private/`

Local-only private memory.

This folder is intentionally ignored by Git. Do not rely on public GitHub to preserve this folder.

## Agent task routing

| User asks for | Agent should inspect |
|---|---|
| Repo purpose or status | `30 - Projects/GitHub/.../Project.md`, then GitHub repo |
| Build/test instructions | `Agent Context.md`, then repo README/workflows |
| Why a decision was made | `Decisions.md`, then related PRs/issues |
| Current platform direction | `AGENTS.md`, `01-Dashboard/Project Source of Truth.md` |
| Available skills | `99-System/Agent Skills/Skill Index.md` |
| Vault maintenance | `RUNBOOK.md`, `99-System/Automation/README.md` |
| Safety/publication rules | `SECURITY.md`, `.gitignore`, Vault Steward spec |

## Agent writing rules

Agents may add or update:

- Public-safe project summaries
- Source-linked runbooks
- Decision records
- Generated indexes with clear generated markers
- Daily maintenance logs
- Backlog items

Agents must not add or update:

- Secret values
- Private repo names in public paths
- `00-Private/**`
- `99-System/Security/**`
- Certificates, keys, cookies, tokens, `.env` files, or local credential inventories
- Human-authored content outside explicit generated markers unless directly requested

## Book quality standards

A good KnowledgeVault note should be:

- **Skimmable:** headings explain the shape before details.
- **Durable:** useful weeks later without chat context.
- **Grounded:** links to source repos, PRs, issues, or files when possible.
- **Actionable:** tells the next human or agent what to do next.
- **Scoped:** says what is known, unknown, and unsafe to assume.
- **Public-safe:** contains no secrets or private operational details.

## Current architecture direction

- OpenClaw is retired.
- Hermes-agent is current active working agent system.
- Buddy-agent is intended to become the primary runtime.
- KnowledgeVault is the book/memory layer, not the runtime.
- Skills should gradually become structured, portable, status-tagged, and consumable by Buddy-agent.
