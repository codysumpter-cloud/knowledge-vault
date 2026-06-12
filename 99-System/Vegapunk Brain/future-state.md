---
type: architecture
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: reference-only
tags:
  - vegapunk-brain
  - future-state
  - shared-memory
  - event-sourcing
---

# Future State

Vegapunk Brain evolves KnowledgeVault from a wiki/book into an event-sourced shared-memory platform.

```txt
User
↓
Buddy Agent
Buddy Brain
Omni Buddy
Prismtek Apps
↓
Event Emitters
↓
Vegapunk Brain Inbox
↓
Event Compiler
↓
Knowledge Graph
↓
Indexes
↓
Search
↓
Future Sessions
```

## What changes

Today, the Buddy ecosystem has useful memory spread across notes, repos, PRs, sessions, and app state.

The future state makes durable memory explicit and recoverable:

- Repos emit public-safe immutable events.
- KnowledgeVault validates and routes those events.
- Vegapunk Brain compiles events into graph records.
- The graph rebuilder can recreate graph state from seed + event history.
- The linter keeps graph records strict.
- Health checks detect broken relationships, stale records, missing provenance, and duplicate concepts.
- Indexes make the graph easy for apps and agents to consume.
- Search returns connected graph neighborhoods.
- Exports produce Mermaid, JSON, and text tree artifacts.

## Agent roles

| Role | Graph behavior |
|---|---|
| Buddy | Talks to the user, loads graph context, routes work. |
| Executor | Executes tasks and emits task/session/memory events. |
| Planner | Reads decisions/tasks and emits approved decision/policy events. |
| Builder | Consumes repo/system/task records and emits implementation summaries. |
| Researcher | Adds public-safe concepts and source-linked findings. |
| Operator | Tracks workflows, releases, checks, and handoffs. |
| Memory Keeper | Compiles summaries into graph updates and flags stale records. |
| Auditor | Runs graph health, provenance, and policy checks. |

## Satellite model

| System | Satellite role |
|---|---|
| Buddy Agent | Executor |
| Buddy Brain | Planner |
| KnowledgeVault | Punk Records |
| Omni Buddy | Device Satellite |
| Prismtek Apps | Product Surface |

## Source-of-truth rule

- GitHub repos remain source of truth for code, CI, releases, and implementation state.
- KnowledgeVault becomes source of truth for durable project memory, decisions, relationships, and graph-backed context.
- Repos emit events; they do not directly mutate graph records.
- Private memory belongs in private/ignored storage, not the public vault.

## Success path

1. Keep the seed graph small and trusted.
2. Let each repo emit public-safe graph events.
3. Ingest events into the Vegapunk Brain inbox.
4. Route accepted events into processed immutable history.
5. Compile events into graph records.
6. Rebuild the compiled graph from seed + event history.
7. Lint and health-check the graph.
8. Generate compact indexes.
9. Let Buddy systems consume indexes at runtime.
10. Promote verified generated records back into curated graph records when needed.

## Definition of done

Vegapunk Brain is working when:

- Graph records are machine-generated.
- Repositories can emit graph events.
- The graph can be rebuilt from event history.
- Relationships are searchable.
- Health checks protect graph integrity.
- Knowledge survives beyond individual agents.
- Buddy systems load shared context before acting.
- Human-readable docs are views over the graph, not the only memory layer.
