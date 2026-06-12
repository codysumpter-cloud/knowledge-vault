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
  - shared-memory-bus
  - agent-integration
---

# Shared Memory Bus

The Shared Memory Bus is the repository-agnostic exchange format for systems that want to contribute to or consume the Vegapunk Brain graph.

It keeps the rule intact:

> Agents do not own durable memory. They emit memory events and consume graph context.

## Supported producers

- `buddy-agent`
- `buddy-brain`
- `omni-buddy`
- `prismtek-apps`
- Future Buddy-compatible agents

## Input contract

A producer emits public-safe memory events as JSON or JSONL.

```json
{
  "event_id": "event:buddy-agent:2026-06-12:example",
  "producer": "repo:buddy-agent",
  "kind": "decision",
  "title": "KnowledgeVault is the shared memory source of truth",
  "summary": "Buddy Agent should consume compiled graph context instead of storing canonical project memory locally.",
  "body": "Decision: KnowledgeVault feeds Buddy Agent. Buddy Agent emits graph updates after tasks.",
  "tags": ["memory", "agent-system"],
  "source": "repo:buddy-agent/docs/example.md",
  "confidence": "high",
  "created": "2026-06-12T00:00:00Z",
  "updated": "2026-06-12T00:00:00Z"
}
```

### Input kinds

| Kind | Meaning | Typical graph output |
|---|---|---|
| `decision` | Durable choice or source-of-truth rule. | `decision:*` plus links to affected repos/systems/concepts. |
| `memory` | Durable fact, preference, or project state. | `concept:*`, `system:*`, or relationship update. |
| `task` | Work item, TODO, check, or implementation handoff. | `task:*` linked to repo/system/concept. |
| `skill` | Tool, capability, or reusable agent behavior. | `system:*` or `concept:*` with `implements`/`uses` links. |
| `artifact` | File, build output, generated index, bundle, or document. | `concept:*` or `system:*` linked with `implements`/`feeds`. |
| `conversation_summary` | Public-safe summary of a session. | Multiple generated graph records. |

## Output contract

The bus converts events into one of four graph operations.

### Graph record

A complete schema-compatible record.

```json
{
  "op": "graph_record",
  "record": {
    "id": "decision:knowledge-vault-shared-memory-source-of-truth",
    "type": "decision",
    "name": "KnowledgeVault shared memory source of truth",
    "summary": "KnowledgeVault owns durable shared memory for Buddy systems.",
    "tags": ["decision", "memory"],
    "links": [],
    "provenance": {
      "source": "event:buddy-agent:2026-06-12:example",
      "confidence": "high",
      "created": "2026-06-12T00:00:00Z",
      "updated": "2026-06-12T00:00:00Z"
    },
    "freshness": {"status": "current", "updated": "2026-06-12"}
  }
}
```

### Graph update

A replacement or merge request for an existing record.

```json
{
  "op": "graph_update",
  "target": "repo:buddy-agent",
  "patch": {
    "tags_add": ["graph-consumer"],
    "summary": "Primary Buddy runtime that consumes compiled graph context."
  }
}
```

### Graph relationship

A link to add between existing records.

```json
{
  "op": "graph_relationship",
  "source": "concept:knowledge-vault",
  "type": "feeds",
  "target": "repo:buddy-agent",
  "reason": "Buddy Agent consumes compiled memory and graph context."
}
```

### Graph event

An auditable event that may or may not change the graph immediately.

```json
{
  "op": "graph_event",
  "event_id": "event:prismtek-apps:2026-06-12:graph-context-loaded",
  "producer": "repo:prismtek-apps",
  "summary": "App loaded compiled Buddy graph context for user-facing display.",
  "source": "runtime-log:public-safe-summary"
}
```

## Synchronization pattern

1. Producer emits memory events into a repo-local `graph-events/` or generated artifact path.
2. KnowledgeVault imports public-safe events.
3. `memory_compiler.py` compiles markdown/session material when needed.
4. `graph_builder.py` merges records into `compiled.graph.jsonl`.
5. `graph_linter.py` validates the graph.
6. `concept_indexer.py` generates indexes.
7. Consumers load only the indexes/records they need.

## Conflict handling

- Higher confidence records win summary/name conflicts.
- Tags and links merge.
- Broken links are pruned by default in `graph_builder.py`.
- Stale records remain searchable but should not be treated as current source of truth.
- Runtime repos remain source of truth for code, CI, and release status.

## Safety rules

- The bus must not accept secrets, tokens, private browser/session data, or local-only machine details.
- Public repo events must be public-safe.
- Private memory requires a private companion vault or ignored local path.
- Generated records must always include provenance.
