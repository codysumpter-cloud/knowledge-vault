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
  - memory-compiler
  - knowledge-graph
---

# Memory Compiler

The Vegapunk Brain Memory Compiler turns public-safe notes, summaries, decisions, PR summaries, and repo docs into schema-compatible graph JSONL records.

It is the first active layer between the human-readable KnowledgeVault book view and the machine-readable shared graph.

## Contract

```txt
markdown/session/decision/repo docs
  ↓
memory_compiler.py
  ↓
generated.graph.jsonl
  ↓
graph_linter.py
  ↓
graph_builder.py
  ↓
compiled.graph.jsonl
  ↓
concept_indexer.py + graph_search.py
```

## Inputs

The compiler accepts:

- Markdown notes
- Session summaries
- Decision logs
- PR summaries
- Repo documentation
- Directories containing `.md` files

## Outputs

The compiler emits one JSON object per line using the Vegapunk Brain graph schema.

Supported generated record types:

- `concept`
- `repo`
- `system`
- `task`
- `decision`
- `person`

Every generated record includes:

- `id`
- `type`
- `name`
- `summary`
- `tags`
- `links`
- `provenance.source`
- `provenance.confidence`
- `provenance.created`
- `provenance.updated`
- `freshness.status`
- `freshness.updated`

## Entity extraction

The compiler detects entities through deterministic rules:

| Entity | Detection source |
|---|---|
| Repos | Known repo names such as `buddy-agent`, `buddy-brain`, `omni-buddy`, `prismtek-apps`, `knowledge-vault`. |
| Systems | Known systems such as `Council`, `Codex Tasks`, `Agent Browser`, `Knowledge Graph`, `Shared Memory Bus`, `Memory Compiler`. |
| Concepts | Known phrases and markdown headings/bullets. |
| Tasks | Lines beginning with task-like verbs or containing `must` / `should`. |
| Decisions | Lines beginning with decision-like language or containing source-of-truth / do-not rules. |
| People | Known human/agent names such as Prismtek, Buddy, Hermes, BMO, Finn, Jake, Marceline, Prismo, NEPTR, Simon. |

This is intentionally simple and inspectable. It should be upgraded later with richer extraction, but only after the deterministic graph path is stable.

## Relationship inference

The compiler can create links when source text contains relationship hints:

- `feeds`
- `consumes`
- `depends_on`
- `owns`
- `implements`
- `supersedes`
- `related_to`
- `uses`
- `integrates_with`
- `syncs_with`

The graph builder merges duplicate records and combines links/tags.

## Commands

Compile a single source:

```bash
python "99-System/Vegapunk Brain/tools/memory_compiler.py" \
  --source "99-System/Vegapunk Brain/examples/session-to-graph.md" \
  --out "99-System/Vegapunk Brain/graph/generated.graph.jsonl"
```

Lint seed and generated graph together:

```bash
python "99-System/Vegapunk Brain/tools/graph_linter.py" \
  "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
  "99-System/Vegapunk Brain/graph/generated.graph.jsonl"
```

Build the compiled graph:

```bash
python "99-System/Vegapunk Brain/tools/graph_builder.py" \
  --graph "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
  --graph "99-System/Vegapunk Brain/graph/generated.graph.jsonl" \
  --out "99-System/Vegapunk Brain/graph/compiled.graph.jsonl"
```

Generate indexes:

```bash
python "99-System/Vegapunk Brain/tools/concept_indexer.py" \
  --graph "99-System/Vegapunk Brain/graph/compiled.graph.jsonl" \
  --out-dir "99-System/Vegapunk Brain/indexes"
```

Search the graph:

```bash
python "99-System/Vegapunk Brain/tools/graph_search.py" \
  --graph "99-System/Vegapunk Brain/graph/compiled.graph.jsonl" \
  --query "Knowledge Vault"
```

## Safety

The compiler is public-safe by default because it only emits summaries and structured entity references from supplied public-safe files. Do not point it at private notes, credentials, local secrets, browser sessions, or proprietary data while this repository remains public.
