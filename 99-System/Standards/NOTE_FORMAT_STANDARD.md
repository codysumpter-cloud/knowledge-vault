# KnowledgeVault Note Format Standard

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

This standard makes KnowledgeVault easier for humans to skim and easier for agents to retrieve, trust, and cite.

A note is useful to an agent when it answers four questions quickly:

1. What is this?
2. How trustworthy/current is it?
3. What source should be checked before acting?
4. What is the next useful action?

## Default note shape

Use this structure for durable notes unless a more specific format applies.

```md
---
type: project | decision | runbook | skill | source | dashboard | handoff | index | bundle
status: reference | draft | active | wired | tested | stale | disabled
owner: Prismtek
source_of_truth: github | knowledge-vault | runtime-repo | external-source | mixed
last_verified: YYYY-MM-DD
risk_level: low | medium | high
privacy: public
freshness: stable | slow-changing | volatile | high-stakes
agent_load: cold-start | task-specific | reference-only | never-auto-load
tags: []
---

# Title

> One-sentence summary.

## Purpose

Why this note exists.

## Current state

What is true now. Separate confirmed facts from assumptions.

## Source links

- Source:
- Related repo:
- Related PR/issue:

## Known unknowns

- What must be checked before action?

## Agent instructions

- When to load this note:
- What not to assume:
- What to verify live:

## Next action

- [ ] Smallest useful next step.
```

## Formatting rules

- Start with a short summary before details.
- Use headings that survive search and chunking.
- Prefer short paragraphs and direct language.
- Keep generated sections behind clear generated markers.
- Put volatile/current claims near source links and verification notes.
- Avoid burying commands inside prose.
- Mark assumptions explicitly.
- Keep one durable idea per note when possible.

## Required sections by note type

### Project

Required:

- Purpose
- Current state
- Source links
- Build/test/verification commands when known
- Risks and gotchas
- Next action

### Decision

Required:

- Decision
- Context
- Options considered
- Rationale
- Consequences
- Reversal conditions
- Source links

### Runbook

Required:

- Goal
- Preconditions
- Steps
- Verification
- Rollback
- Risks
- Escalation rules

### Skill

Required:

- What it does
- Runtime target
- Status
- Required tools/configuration
- Input/output contract
- Risk level
- Validation receipt
- When not to use

### Source / concept card

Required:

- Source name
- Source URL
- Retrieved or revised date
- License note when relevant
- Summary
- Key concepts
- Related concepts
- Freshness class
- Caveats

### Handoff

Required:

- Task goal
- Current state
- Files touched
- Commands run
- Verification performed
- Remaining risks
- Next action

## Claim language

Use explicit claim status words.

| Use this | Meaning |
|---|---|
| Confirmed | Verified from a source or command. |
| Inferred | Reasonable conclusion, but not directly stated. |
| Assumption | Useful placeholder that needs verification. |
| Stale | Known to need re-checking before action. |
| Blocked | Cannot proceed without a missing input, permission, or dependency. |

## Agent retrieval hints

Add `agent_load` metadata:

- `cold-start` — safe to load during startup.
- `task-specific` — load only when the task matches.
- `reference-only` — useful background, not operational truth.
- `never-auto-load` — requires explicit human request or extra review.

## Done checklist

Before a note is considered agent-ready:

- [ ] It has a clear title.
- [ ] It has a one-sentence summary.
- [ ] It has status and last-verified metadata.
- [ ] It names the source of truth.
- [ ] It separates facts, assumptions, and unknowns.
- [ ] It has a next action or says no action is needed.
- [ ] It is public-safe.
- [ ] It is short enough to retrieve without dragging unrelated context.
