# KnowledgeVault Agent Database Blueprint

Status: active design
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

This blueprint defines what “best database for an AI agent” means for KnowledgeVault.

The goal is not to turn the vault into a giant blob of notes. The goal is to make it a dependable memory and retrieval layer that is:

- easy for humans to browse
- safe for a public repository
- strict enough for automation
- structured enough for task-specific retrieval
- honest about freshness, provenance, and capability status
- portable into Buddy-agent, Hermes, and future Prismtek agents

## Design principle

Agents do not need every note. They need the right note, with the right confidence, at the right time.

KnowledgeVault should therefore optimize for **trustworthy retrieval**, not maximum volume.

## Source-of-truth split

| Information type | Source of truth | Vault role |
|---|---|---|
| Code | GitHub repos | Link, summarize, explain context. |
| Issues / PRs | GitHub | Link and summarize active state. |
| CI / releases | GitHub Actions and release tooling | Link and summarize, never invent status. |
| Durable decisions | KnowledgeVault | Preserve rationale and current implications. |
| Project memory | KnowledgeVault | Store summaries, status, risks, and handoffs. |
| Agent skills | Runtime repo once wired/tested | Store references, specs, and status metadata. |
| Broad knowledge | Source packs and external references | Store compact concept cards and provenance. |
| Sensitive/private context | Never public KnowledgeVault | Keep local-only or in a private companion vault. |

## Core record types

Every durable record should fit one of these types.

### 1. Project record

Purpose: explain one repo or product area.

Required files for important repos:

- `Project.md` — intent, current status, links, source-of-truth pointers
- `Agent Context.md` — setup, commands, risks, gotchas, handoff notes
- `Decisions.md` — durable decisions and why they were made
- `Tasks.md` — vault-side todo list and next suggested actions

### 2. Decision record

Purpose: prevent agents from re-litigating old choices.

Required sections:

- Decision
- Context
- Options considered
- Rationale
- Consequences
- Reversal conditions
- Source links

### 3. Runbook record

Purpose: make repeatable work safe and predictable.

Required sections:

- Goal
- Preconditions
- Commands
- Verification
- Rollback
- Known risks
- Escalation rules

### 4. Skill record

Purpose: describe a reusable agent capability without overstating runtime support.

Required metadata:

- skill id
- category
- runtime target
- status
- risk level
- required permissions
- required private configuration
- entrypoint
- verification receipt

Allowed statuses:

- `reference` — useful source material only
- `draft` — designed but not implemented
- `ported` — copied/adapted into the target repo
- `wired` — connected to a runtime or app path
- `tested` — validated by command, CI, or runtime behavior
- `disabled` — intentionally unavailable
- `public-alpha-safe` — allowed for guarded public alpha use

### 5. Source record

Purpose: preserve reusable knowledge without mirroring raw source material.

Required fields:

- source name
- source URL
- source revision or retrieval date
- license note when applicable
- summary type
- freshness class
- high-stakes caveat when needed

### 6. Dashboard record

Purpose: give humans and agents a current operating view.

Dashboards should clearly separate:

- generated sections
- human-authored sections
- stale sections
- unknown sections
- verified source links

### 7. Handoff record

Purpose: allow a future agent to resume work safely.

Required sections:

- Task goal
- Current state
- Files touched
- Commands run
- Verification performed
- Remaining risks
- Next action

## Minimum metadata contract

Use front matter on important durable notes.

```yaml
---
type: project | decision | runbook | skill | source | dashboard | handoff
status: reference | draft | active | wired | tested | stale | disabled
owner: Prismtek
source_of_truth: github | knowledge-vault | runtime-repo | external-source | mixed
last_verified: YYYY-MM-DD
risk_level: low | medium | high
privacy: public
tags: []
---
```

Optional but useful fields:

```yaml
runtime_target: buddy-agent | hermes-agent | prismtek-apps | knowledge-vault | external
freshness: stable | slow-changing | volatile | high-stakes
requires_network: true | false
requires_private_config: true | false
agent_load: cold-start | task-specific | reference-only | never-auto-load
```

## Freshness classes

| Class | Meaning | Agent behavior |
|---|---|---|
| `stable` | Architecture, durable decisions, definitions | Use unless superseded. |
| `slow-changing` | Repo purpose, project direction, runbooks | Check last verified date before acting. |
| `volatile` | PR state, CI state, releases, schedules, current APIs | Verify against live source before claiming. |
| `high-stakes` | Security, legal, medical, financial, account access | Use as context only; verify with authoritative source. |

## Retrieval model

Agents should not ingest the entire vault blindly. They should load context in layers.

### Layer 1 — cold start

Smallest orientation path:

1. `README.md`
2. `AGENTS.md`
3. `SYSTEMMAP.md`
4. `AGENT_DATABASE_BLUEPRINT.md`
5. `RUNBOOK.md`
6. `SECURITY.md`
7. `01-Dashboard/Project Source of Truth.md`

### Layer 2 — task routing

Pick the relevant domain:

| Task | Load |
|---|---|
| Repo work | repo project folder + GitHub repo state |
| Runtime feature claim | skill registry + target runtime repo |
| Vault maintenance | runbook + automation docs + Vault Steward spec |
| Safety decision | security policy + AGENTS.md |
| Broad knowledge | source pack README + generated concept cards |
| Project planning | project dashboard + decisions + tasks |

### Layer 3 — focused bundle

Future export scripts should produce curated bundles such as:

- `buddy-agent-maintainer.bundle.md`
- `prismtek-apps-maintainer.bundle.md`
- `vault-steward.bundle.md`
- `public-alpha-reviewer.bundle.md`
- `pokemmo-coach.bundle.md`
- `wikipedia-concept-learning.bundle.md`

Each bundle should include:

- purpose
- included files
- excluded files
- generated timestamp
- last verified dates
- risk warnings
- source links
- receipt ID

## Retrieval receipts

When an agent uses the vault for a meaningful answer or repo action, it should be able to produce a receipt.

Receipt shape:

```json
{
  "vault": "knowledge-vault",
  "task": "short task name",
  "loaded_files": [
    "README.md",
    "AGENTS.md"
  ],
  "generated_bundle": null,
  "live_sources_checked": [
    "GitHub repo or PR URL"
  ],
  "stale_or_unverified_claims": [],
  "safety_checks": [
    "public-only staging checked",
    "sensitive material check passed"
  ]
}
```

Receipts make agent behavior easier to audit and easier to correct.

## Quality gates

A note is agent-ready only if it passes these checks.

### Required

- Has a clear title.
- Has a purpose section or equivalent opening summary.
- Has status metadata.
- Has a last verified date when it makes external/current claims.
- Links to source material when making repo, runtime, or external claims.
- Has a next action or says no action is needed.
- Does not contain sensitive private configuration, private repo details, or sensitive local paths.

### Strongly preferred

- Separates known facts from assumptions.
- Names stale or risky areas.
- Uses generated markers around automation-owned sections.
- Avoids claiming runtime capability from reference-only skill docs.
- Stays short enough for retrieval.

## Automation roadmap

### P0 — Safety and correctness

- Keep `vault_doctor.py` in CI.
- Keep forbidden paths untracked.
- Keep private repo tracking disabled while public.
- Block broad staging patterns.
- Flag credential-like filenames without printing their contents.

### P1 — Agent-readiness

- Add front matter to key docs.
- Add note quality linting.
- Add canonical schemas for project, decision, runbook, skill, source, dashboard, and handoff records.
- Upgrade generated repo scaffolds into useful briefs.
- Promote skill registry from seed to maintained index.
- Add generated retrieval bundles.

### P2 — Productization

- Add vector/index export targets for Buddy-agent.
- Add bundle receipts.
- Add stale-claim reports.
- Add graph edges between repos, skills, decisions, and runbooks.
- Split public and private memory into separate repos or a clearly enforced companion vault.

## Public safety rules

This repository is public. That is a product choice and a constraint.

Tracked public files must never include private credentials, sensitive operational details, private repository details, signed-in session material, local credential inventories, or machine-specific paths that expose private workspace state.

Private memory should live in:

1. a private companion vault, or
2. local-only ignored folders, or
3. a future encrypted/private storage layer.

## Definition of done

KnowledgeVault becomes a strong agent database when:

- a new agent can cold-start from the root docs without chat history
- important notes have metadata and freshness labels
- project records explain real current state, not placeholders
- skills have explicit runtime status and verification receipts
- generated dashboards show current operating state
- agents can export/load task-specific bundles
- public safety checks run before automation commits
- every major answer/action can cite which vault files and live sources informed it

## Operating mantra

Make the vault small enough to retrieve, structured enough to trust, and honest enough to correct.
