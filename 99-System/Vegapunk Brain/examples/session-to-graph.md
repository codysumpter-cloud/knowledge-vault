---
type: example
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: low
privacy: public
freshness: stable
agent_load: reference-only
tags:
  - vegapunk-brain
  - memory-compiler
  - example
---

# Session To Graph Example

This file is a public-safe sample input for `memory_compiler.py`.

## Session summary

Prismtek decided that KnowledgeVault should become the shared memory source of truth for Buddy systems.

Knowledge Vault feeds buddy-agent, buddy-brain, omni-buddy, and prismtek-apps.

Buddy Agent consumes Knowledge Vault graph context before executing Codex Tasks.

Buddy Brain coordinates the Council and uses Knowledge Vault as durable public-safe memory.

Prismtek Apps surfaces Council state, Agent Browser workflows, and compiled Buddy graph context.

Omni Buddy consumes Knowledge Vault graph context instead of maintaining isolated memory.

## Decisions

Decision: KnowledgeVault is the shared memory source of truth for Buddy systems.

Decision: The wiki is a view, but the knowledge graph is the machine-readable substrate.

Do not let individual agents own canonical durable memory.

## Tasks

Build the Memory Compiler for markdown notes, session summaries, decision logs, PR summaries, and repo documentation.

Create graph_builder.py to merge seed and generated graph records.

Create concept_indexer.py to generate concepts.json, repos.json, systems.json, and relationships.json.

Create graph_search.py to return connected graph neighborhoods.

## Expected graph themes

- Knowledge Vault
- Buddy Agent
- Buddy Brain
- Omni Buddy
- Prismtek Apps
- Council
- Codex Tasks
- Agent Browser
- Knowledge Graph
- Shared Memory Bus
- Memory Compiler
- Future Sessions
