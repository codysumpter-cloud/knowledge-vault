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
  - buddy-agent
  - integration
---

# Buddy Agent Integration

Buddy Agent is the primary runtime/execution consumer of the Vegapunk Brain graph.

## Emits graph records

Buddy Agent should emit:

- `task:*` records for coding tasks, checks, and implementation handoffs.
- `decision:*` records when a human-approved implementation choice changes system direction.
- `system:*` records for new runtime capabilities.
- `concept:*` records for reusable agent concepts discovered during work.

## Consumes graph records

Buddy Agent should consume:

- `repo:*` records for repo orientation.
- `system:*` records for tools, Council, Codex Tasks, Agent Browser, and Memory Compiler context.
- `decision:*` records before changing architecture.
- `task:*` records when resuming work.

## Synchronization strategy

1. Load `compiled.graph.jsonl` or generated indexes at task start.
2. Search by repo/task/system tags.
3. Execute the task.
4. Emit public-safe session summaries or graph events.
5. KnowledgeVault compiles and validates updates.

## Update frequency

- At task start: read graph context.
- After meaningful task completion: emit graph event or summary.
- Before architecture changes: check decision records.

## Safety

Buddy Agent must not emit secrets, private local paths, signed-in browser state, or unreviewed private repo details into public KnowledgeVault.
