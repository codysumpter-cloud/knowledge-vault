# Repo Emitter Contracts

Each Buddy ecosystem repo emits events. Repos never directly edit graph records.

## Required event fields

Every event must include:

```json
{
  "event_id": "evt-source-yyyymmdd-kind-001",
  "event_type": "conversation_summarized",
  "source": "buddy-agent",
  "timestamp": "2026-06-12T00:00:00Z",
  "payload": {
    "name": "Short name",
    "summary": "Public-safe durable summary.",
    "tags": ["public-safe"],
    "confidence": "medium"
  }
}
```

## buddy-agent

Emits:

- `conversation_summarized`
- `task_created`
- `task_completed`
- `memory_created`

Expected payload fields:

- `name`
- `summary`
- `tags`
- `repo`
- `confidence`

Ingestion expectation: Buddy Agent should emit events after meaningful work, task completion, or public-safe session summarization.

## buddy-brain

Emits:

- `decision_made`
- `policy_updated`
- `council_update`

Expected payload fields:

- `name`
- `summary`
- `tags`
- `target`
- `confidence`

Ingestion expectation: Buddy Brain should emit events only after durable governance, policy, or Council-state changes.

## omni-buddy

Emits:

- `device_registered`
- `model_changed`
- `local_memory_created`

Expected payload fields:

- `name`
- `summary`
- `tags`
- `repo`
- `confidence`

Ingestion expectation: Omni Buddy must sanitize local/device/private details before emitting public KnowledgeVault events.

## prismtek-apps

Emits:

- `app_created`
- `feature_added`
- `feature_removed`
- `release_created`

Expected payload fields:

- `name`
- `summary`
- `tags`
- `repo`
- `status`
- `confidence`

Ingestion expectation: Prismtek Apps should emit product/app/release events, not private user data, OAuth tokens, or device identifiers.

## Relationship events

Use `relationship_created` when a repo needs to propose a graph edge:

```json
{
  "event_id": "evt-buddy-brain-20260612-relationship-001",
  "event_type": "relationship_created",
  "source": "buddy-brain",
  "timestamp": "2026-06-12T00:00:00Z",
  "payload": {
    "name": "KnowledgeVault feeds Buddy Agent",
    "summary": "Buddy Agent consumes compiled graph context from KnowledgeVault.",
    "source_record": "concept:knowledge-vault",
    "target": "repo:buddy-agent",
    "relationship_type": "feeds",
    "tags": ["relationship", "memory"],
    "confidence": "high"
  }
}
```

Relationship events are audit records first. Human or maintainer review can later promote them into curated seed graph links.
