---
type: integration
status: draft
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - vegapunk-brain
  - buddy-brain
  - integration
---

# Buddy Brain Integration

Buddy Brain is the governance, Council, operator policy, and continuity consumer/producer for Vegapunk Brain.

## Emits graph records

Buddy Brain should emit:

- `decision:*` records for governance rules and approved direction.
- `system:*` records for Council roles, review loops, and safety boundaries.
- `task:*` records for escalations and follow-up work.
- `concept:*` records for reusable operating principles.

## Consumes graph records

Buddy Brain should consume:

- `decision:*` before approving or rejecting plans.
- `repo:*` to understand repo ownership and source-of-truth boundaries.
- `system:*` for Council, Codex Tasks, Agent Browser, Memory Compiler, and Shared Memory Bus context.
- `person:*` only when records are public-safe and relevant to named agent roles.

## Synchronization strategy

1. Load graph decisions and system records before Council review.
2. Attach Council review outputs to public-safe summaries.
3. Emit decision records when policy changes.
4. Let KnowledgeVault compile and validate records before they become durable context.

## Update frequency

- Before plan review: read graph decisions.
- After human-approved policy/governance changes: emit graph update.
- Weekly or release-boundary: refresh Council/system records.

## Safety

Buddy Brain must keep private memory and sensitive operating context outside public KnowledgeVault unless explicitly sanitized.
