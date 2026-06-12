---
type: architecture
status: draft
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: cold-start
tags:
  - vegapunk-brain
  - knowledge-graph
  - shared-memory
  - buddy
  - agents
---

# Vegapunk Brain

Vegapunk Brain is the KnowledgeVault upgrade path from **human-readable wiki** to **living shared knowledge graph**.

The rule is simple:

> Agents do not own memory. Agents consume and contribute to shared memory.

KnowledgeVault remains the public-safe durable source of truth. Buddy-agent, Buddy Brain, Omni Buddy, the app, council members, and future agents become specialized satellites that read from and write back to this shared substrate.

## Why this exists

The current Prismtek ecosystem already has most of the pieces:

- `knowledge-vault` stores durable project memory and source-of-truth notes.
- `buddy-brain` stores continuity, council posture, governance, and operator memory.
- `buddy-agent` is becoming the execution/runtime agent.
- `omni-buddy` targets local multimodal presence.
- Prismtek apps expose the user-facing Buddy loop.

The missing piece is not another agent. It is the **shared graph** that lets every agent understand the same world model.

## Core architecture

```txt
KnowledgeVault
  |
  |-- Book view          human-readable markdown
  |-- Records            decisions, projects, handoffs, runbooks
  |-- Semantic graph      concepts, entities, claims, relationships
  |-- Memory compiler     extracts graph records from notes and sessions
  |-- Shared memory bus   agent read/write contract
  |
  +--> Buddy Agent        runtime executor
  +--> Buddy Brain        council + governance
  +--> Omni Buddy         local embodied Buddy
  +--> Buddy App          user-facing companion
  +--> Future Agents      specialized satellites
```

## Design principles

1. **Separate knowledge from agents.**
   - KnowledgeVault owns durable public-safe knowledge.
   - Agents have caches, working memory, and local context, but not the canonical memory.

2. **Make the graph real.**
   - Markdown remains a view.
   - JSONL graph records are the machine substrate.
   - Indexes and bundles are generated from records, not hand-maintained forever.

3. **Every claim needs provenance.**
   - A graph edge should know where it came from.
   - Source can be a vault note, repo file, PR, issue, user decision, or generated artifact.

4. **Use small public-safe records.**
   - No secrets.
   - No private browser/session material.
   - No high-risk automation payloads.

5. **Agents contribute through contracts.**
   - Agents propose graph updates.
   - The compiler validates them.
   - Unsafe, stale, or ungrounded writes are rejected or marked draft.

## First implementation slice

This folder introduces the minimum viable living brain:

| File | Purpose |
|---|---|
| `README.md` | Architecture and operating model. |
| `schema/graph-record.schema.json` | JSON Schema for graph records. |
| `graph/seed.graph.jsonl` | Seed graph for the Prismtek/Buddy ecosystem. |
| `memory-compiler.md` | Compiler contract and extraction rules. |
| `satellites.md` | Specialized agent roles and write permissions. |
| `shared-memory-bus.md` | Read/write protocol for agents. |
| `examples/session-to-graph.md` | Example of turning a chat/session into graph records. |

## Graph record model

The graph uses JSONL so it can be appended, diffed, linted, indexed, and consumed by simple tools.

Each line is one record:

```json
{"id":"concept:knowledge-vault","kind":"concept","name":"KnowledgeVault","status":"active"}
```

Supported initial record kinds:

- `concept`
- `entity`
- `project`
- `agent`
- `capability`
- `claim`
- `relationship`
- `decision`
- `task`

## Relationship examples

```json
{"id":"rel:buddy-agent-consumes-knowledge-vault","kind":"relationship","from":"project:buddy-agent","to":"project:knowledge-vault","predicate":"consumes"}
{"id":"rel:knowledge-vault-source-of-truth-memory","kind":"relationship","from":"project:knowledge-vault","to":"concept:durable-project-memory","predicate":"source_of_truth_for"}
{"id":"rel:council-specializes-agent-review","kind":"relationship","from":"agent:council","to":"capability:review","predicate":"specializes_in"}
```

## Agent usage

Before an agent claims project state, it should:

1. Load the relevant context bundle.
2. Search the graph for matching concepts/entities/projects.
3. Check provenance and freshness.
4. Prefer runtime repo state for code/CI/release claims.
5. Propose graph updates after meaningful changes.

## Non-goals for this first slice

- This does not replace GitHub as code source of truth.
- This does not store private secrets or private operational context.
- This does not claim a runtime integration is complete.
- This does not add autonomous write access to agents yet.

## Next build steps

1. Add a Python graph linter for JSONL records.
2. Add a compiler that extracts records from markdown front matter and `## Current state` sections.
3. Generate `indexes/concepts.json`, `indexes/relationships.json`, and `indexes/projects.json`.
4. Export a `buddy-agent` context bundle from graph records.
5. Add agent proposal files under a quarantined `proposals/` folder before direct writes are allowed.
