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
  - omni-buddy
  - integration
---

# Omni Buddy Integration

Omni Buddy is the local multimodal Buddy presence. It should consume shared graph context while keeping local sensory/session data private by default.

## Emits graph records

Omni Buddy should emit only sanitized/public-safe records:

- `task:*` records for device setup or local workflow follow-up.
- `system:*` records for public-safe capabilities such as voice, vision, local model, or device integration.
- `decision:*` records only when the user approves durable architecture changes.

## Consumes graph records

Omni Buddy should consume:

- `concept:*` records for shared Buddy principles.
- `system:*` records for memory bus and runtime integration contracts.
- `repo:*` records for repo responsibilities.
- `decision:*` records that affect local/offline behavior.

## Synchronization strategy

1. Pull compiled graph context from KnowledgeVault.
2. Cache only the graph records needed for local workflows.
3. Keep local sensor/session details private.
4. Emit sanitized summaries when local work changes public architecture.

## Update frequency

- At startup or sync: read graph indexes.
- After local workflow milestones: emit sanitized summary if public-safe.
- Never continuously stream private local observations to public KnowledgeVault.

## Safety

Omni Buddy must treat audio, camera, local paths, device identity, network state, and private home/work context as private unless explicitly summarized into public-safe form.
