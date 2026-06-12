# Vegapunk Brain Emitters

Repos do not write graph records directly.

They emit append-only events. Vegapunk Brain ingests those events, validates them, routes them, compiles them into graph records, rebuilds indexes, and reports graph health.

```txt
Buddy repos
  ↓
Event emitters
  ↓
inbox/events
  ↓
event_ingestor.py
  ↓
event_router.py
  ↓
graph_compiler.py
  ↓
compiled graph + indexes
```

## Event rules

All events must be:

- Append-only
- Immutable after emission
- Timestamped with UTC `YYYY-MM-DDTHH:MM:SSZ`
- Traceable through `event_id`, `source`, and payload fields
- Public-safe before entering KnowledgeVault

## Required fields

```json
{
  "event_id": "evt-example-001",
  "event_type": "decision_made",
  "source": "buddy-brain",
  "timestamp": "2026-06-12T00:00:00Z",
  "payload": {}
}
```

## Supported event types

Core:

- `concept_created`
- `concept_updated`
- `task_created`
- `task_completed`
- `decision_made`
- `feature_added`
- `feature_removed`
- `repo_created`
- `repo_updated`
- `memory_created`
- `memory_updated`
- `relationship_created`
- `relationship_removed`
- `conversation_summarized`

Buddy Brain extensions:

- `policy_updated`
- `council_update`

Omni Buddy extensions:

- `device_registered`
- `model_changed`
- `local_memory_created`

Prismtek Apps extensions:

- `app_created`
- `release_created`

## Payload conventions

Common fields:

| Field | Meaning |
|---|---|
| `id` | Optional graph id target or proposed id. |
| `name` | Human-readable name. |
| `summary` | Public-safe summary. |
| `tags` | Array of tags. |
| `target` | Relationship target graph id. |
| `source_record` | Relationship source graph id. |
| `relationship_type` | Graph link type such as `feeds`, `uses`, `implements`, `related_to`. |
| `repo` | Repo slug when applicable. |
| `status` | Task/release/feature status when applicable. |
| `confidence` | `low`, `medium`, or `high`; defaults to `medium`. |

## Ingestion expectation

1. Repos write event JSON/JSONL artifacts.
2. KnowledgeVault copies/imports events into `inbox/events/`.
3. `event_ingestor.py` validates and accepts events.
4. `event_router.py` moves accepted events into `inbox/processed/`.
5. `graph_compiler.py` compiles processed events into graph records.
6. `graph_rebuilder.py` rebuilds graph state from seed + event history.
7. `graph_health.py` fails on broken relationships and invalid graph state.

## Source contracts

- `buddy-agent`: conversations, tasks, task completions, memories.
- `buddy-brain`: decisions, policies, council updates.
- `omni-buddy`: device/local-agent state, model changes, sanitized local memories.
- `prismtek-apps`: apps, features, removals, releases.
