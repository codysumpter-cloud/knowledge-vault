---
type: architecture
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - vegapunk-brain
  - satellites
  - shared-memory
---

# Satellite Model

Vegapunk Brain treats KnowledgeVault as **Punk Records**: the shared durable memory store.

Repos and agents are satellites. They do not own canonical memory. They emit events and consume graph context.

## Current satellites

| Satellite | Vegapunk role | Primary behavior |
|---|---|---|
| Buddy Agent | Executor | Executes tasks, summarizes conversations, emits task/session/memory events. |
| Buddy Brain | Planner | Emits decisions, policies, operator events, and Council updates. |
| KnowledgeVault | Punk Records | Validates events, compiles graph records, rebuilds indexes, and preserves durable memory. |
| Omni Buddy | Device Satellite | Emits sanitized device/local-agent/model events. |
| Prismtek Apps | Product Surface | Emits app, feature, release, and product events. |

## Future satellites

- Researcher: emits source-linked findings and concept updates.
- Builder: emits implementation and artifact events.
- Operator: emits release, CI, workflow, and runbook events.
- Memory Keeper: emits summaries, stale-record reports, and curation proposals.
- Auditor: emits graph health, provenance, and policy review events.

## Communication flow

```txt
User
↓
Buddy Agent / Buddy Brain / Omni Buddy / Prismtek Apps
↓
Event Emitters
↓
Vegapunk Brain Inbox
↓
Event Ingestor
↓
Event Router
↓
Graph Compiler
↓
Knowledge Graph
↓
Indexes + Search + Exports
↓
Future Sessions
```

## Write boundary

Satellites may write events.

Only Vegapunk Brain compiles graph records.

This keeps memory traceable, append-only, and recoverable from event history.

## Read boundary

Satellites should read compact graph indexes or scoped graph search results. They should not ingest the whole graph unless performing maintenance, indexing, or audit work.
