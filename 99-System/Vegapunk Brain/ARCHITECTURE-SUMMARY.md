---
type: architecture
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: cold-start
tags:
  - vegapunk-brain
  - event-sourced-memory
  - architecture-summary
---

# Vegapunk Brain Architecture Summary

Vegapunk Brain is now designed as an event-sourced shared-memory platform for the Buddy ecosystem.

## System flow

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
Indexes / Search / Health / Exports
↓
Future Sessions
```

## Core rule

Repositories emit immutable events.

Vegapunk Brain compiles graph records.

This prevents each satellite from inventing or mutating canonical memory independently.

## Durable layers

| Layer | Path | Purpose |
|---|---|---|
| Event schema | `emitters/graph-event.schema.json` | Defines append-only event contract. |
| Emitter examples | `emitters/*.event.example.json` | Shows each repo's event shape. |
| Inbox | `inbox/events/` | Accepted event staging area. |
| Processed events | `inbox/processed/` | Routed immutable event history. |
| Compiler | `tools/graph_compiler.py` | Converts events into graph records. |
| Rebuilder | `tools/graph_rebuilder.py` | Rebuilds graph from seed + event history. |
| Outbox graph | `outbox/graph-records/` | Generated compiled graph records. |
| Outbox indexes | `outbox/indexes/` | Generated searchable indexes. |
| Health | `tools/graph_health.py` | Finds broken graph state. |
| Export | `tools/graph_export.py` | Emits Mermaid, JSON, and text tree artifacts. |

## Recovery model

The graph can be rebuilt from:

1. `graph/seed.graph.jsonl`
2. `inbox/processed/**`
3. emitter examples when no processed events exist

Generated outputs are ignored and reproducible.

## Satellite mapping

| Repo/System | Satellite role |
|---|---|
| `buddy-agent` | Executor |
| `buddy-brain` | Planner |
| `knowledge-vault` | Punk Records |
| `omni-buddy` | Device Satellite |
| `prismtek-apps` | Product Surface |

## Validation model

CI validates:

- Python tool syntax
- Seed graph linting
- Event ingestion
- Event routing
- Event-sourced graph rebuild
- Graph linting
- Index generation
- Graph health
- Graph search

## Current limitation

The repo now contains the platform-side intake/compile/rebuild system. The satellite repositories still need their own native event emitters wired into their task/session/release flows.
