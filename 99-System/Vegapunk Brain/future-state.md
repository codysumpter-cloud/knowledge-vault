---
type: architecture
status: draft
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
---

# Future State

Vegapunk Brain evolves KnowledgeVault from a wiki/book into a living graph-backed memory substrate.

```txt
User
↓
Buddy
↓
Knowledge Graph
↓
Planner
Builder
Researcher
Operator
Memory Keeper
↓
Knowledge Graph
↓
Future Sessions
```

## What changes

Today, the Buddy ecosystem has useful memory spread across notes, repos, PRs, sessions, and app state.

The future state makes durable memory explicit:

- Repos emit public-safe graph events.
- KnowledgeVault compiles events and notes into graph records.
- The graph builder merges seed, generated, and repo-emitted records.
- The linter keeps records strict.
- Indexes make the graph easy for apps and agents to consume.
- Search returns connected graph neighborhoods.

## Agent roles

| Role | Graph behavior |
|---|---|
| Buddy | Talks to the user, loads graph context, routes work. |
| Planner | Reads decisions/tasks and proposes safe next steps. |
| Builder | Consumes repo/system/task records and emits implementation summaries. |
| Researcher | Adds public-safe concepts and source-linked findings. |
| Operator | Tracks workflows, releases, checks, and handoffs. |
| Memory Keeper | Compiles summaries into graph updates and flags stale records. |

## Source-of-truth rule

- GitHub repos remain source of truth for code, CI, releases, and implementation state.
- KnowledgeVault becomes source of truth for durable project memory, decisions, relationships, and graph-backed context.
- Private memory belongs in private/ignored storage, not the public vault.

## Success path

1. Keep the seed graph small and trusted.
2. Compile public-safe summaries into generated graph files.
3. Lint all graph files.
4. Build one compiled graph.
5. Generate compact indexes.
6. Let Buddy systems consume indexes at runtime.
7. Let Buddy systems emit graph events after work.
8. Promote verified generated records back into curated graph records.

## Definition of done

Vegapunk Brain is working when:

- Graph records are machine-generated.
- Repositories can emit graph updates.
- Relationships are searchable.
- Knowledge survives beyond individual agents.
- Buddy systems load shared context before acting.
- Human-readable docs are views over the graph, not the only memory layer.
