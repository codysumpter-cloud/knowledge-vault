---
type: integration
status: draft
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - vegapunk-brain
  - prismtek-apps
  - integration
---

# Prismtek Apps Integration

Prismtek Apps is the user-facing Buddy experience. It should surface graph-backed context without becoming the canonical memory store.

## Emits graph records

Prismtek Apps should emit:

- `task:*` records for user-facing app follow-up work.
- `system:*` records for app-visible Buddy features.
- `decision:*` records for user-approved product direction.
- `concept:*` records for reusable UX or companion-loop concepts.

## Consumes graph records

Prismtek Apps should consume:

- `repo:*` records for app/repo status displays.
- `system:*` records for Council, Agent Browser, Codex Tasks, and Knowledge Graph UI.
- `task:*` records for task dashboards.
- `decision:*` records for product state and source-of-truth boundaries.

## Synchronization strategy

1. Load compact indexes such as `concepts.json`, `repos.json`, `systems.json`, and `relationships.json`.
2. Display graph-backed state in user-facing dashboards.
3. Emit sanitized app events when user choices or shipped features change durable memory.
4. Do not store canonical memory in app-only local state.

## Update frequency

- On app launch or manual refresh: read compact graph indexes.
- After user-approved product decisions: emit graph event.
- After release/build milestones: emit public-safe summary.

## Safety

The app must not emit private journal content, credentials, OAuth tokens, local device identifiers, or personal data into public KnowledgeVault.
