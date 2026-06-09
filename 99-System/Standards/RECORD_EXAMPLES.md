# KnowledgeVault Record Examples

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

These examples give humans and agents copyable shapes for useful vault records.

Use them when creating or repairing notes so KnowledgeVault stays consistent, skimmable, and retrieval-friendly.

## Project record

```md
---
type: project
status: active
owner: Prismtek
source_of_truth: mixed
last_verified: YYYY-MM-DD
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags: [project]
---

# repo-name

> One-sentence purpose and current role.

## Purpose

What this repo is for.

## Current state

Confirmed:

- Fact from README/source.

Assumptions:

- Assumption that needs verification.

## Source links

- GitHub:
- README:
- Relevant PRs/issues:

## Verify

```bash
# command here
```

## Risks and gotchas

- Risk:

## Agent instructions

- Load this note when:
- Verify live before:
- Do not assume:

## Next action

- [ ] Smallest useful next step.
```

## Decision record

```md
---
type: decision
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: YYYY-MM-DD
risk_level: medium
privacy: public
freshness: stable
agent_load: task-specific
tags: [decision]
---

# YYYY-MM-DD — Decision title

> Short summary of the decision.

## Decision

What changed or what was chosen.

## Context

Why this decision was needed.

## Options considered

1. Option A — tradeoff.
2. Option B — tradeoff.

## Rationale

Why this option won.

## Consequences

- Positive:
- Negative:
- Follow-up:

## Reversal conditions

What would make this decision worth revisiting.

## Source links

- Related note:
- Related PR/issue:
```

## Runbook record

```md
---
type: runbook
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: YYYY-MM-DD
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags: [runbook]
---

# Runbook title

> What this runbook helps do safely.

## Goal

The outcome this runbook produces.

## Preconditions

- Required files:
- Required live checks:

## Steps

1. Step one.
2. Step two.

## Verification

- [ ] Check result.

## Rollback

How to recover if the run fails.

## Risks

- Risk:

## Escalation rules

When an agent must stop and ask a human.
```

## Skill record

```md
---
type: skill
status: reference
owner: Prismtek
source_of_truth: mixed
last_verified: YYYY-MM-DD
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: reference-only
runtime_target: buddy-agent
requires_network: true
tags: [skill]
---

# Skill name

> What this skill helps an agent do.

## What it does

Short description.

## Runtime status

- Status:
- Evidence:
- Verification receipt:

## When to use

- Good use case.

## When not to use

- Bad use case or unsafe use case.

## Input / output contract

Input:

Output:

## Required tools

- Tool:

## Risks

- Risk:

## Validation

```bash
# validation command or manual check
```

## Source links

- Runtime repo:
- Source doc:
```

## Handoff record

```md
---
type: handoff
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: YYYY-MM-DD
risk_level: medium
privacy: public
freshness: volatile
agent_load: task-specific
tags: [handoff]
---

# Handoff — task name

> Where the next agent should resume.

## Task goal

What the task is trying to accomplish.

## Current state

What is done and what is not done.

## Files touched

- Path:

## Commands run

```bash
# commands
```

## Verification performed

- Check:

## Remaining risks

- Risk:

## Next action

- [ ] Resume here.
```

## Source record

```md
---
type: source
status: active
owner: Prismtek
source_of_truth: external-source
last_verified: YYYY-MM-DD
risk_level: low
privacy: public
freshness: slow-changing
agent_load: reference-only
tags: [source]
---

# Source / concept title

> Short concept summary.

## Source

- Name:
- URL:
- Retrieved:
- Revision/date:
- License note:

## Summary

Compact, original explanation.

## Key concepts

- Concept:

## Related concepts

- Related:

## Caveats

- What this source should not be used for.

## Agent instructions

- Verify live before high-stakes or volatile claims.
```
