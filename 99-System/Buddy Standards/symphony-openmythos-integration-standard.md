---
type: standard
status: active
owner: Prismtek / Buddy ecosystem
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: stable
agent_load: cold-start
tags:
  - buddy
  - symphony
  - agents-sdk
  - openmythos
  - world-model
---

# Symphony / Agents SDK / OpenMythos Integration Standard

> Compatibility standard for orchestration, tool contracts, structured outputs, guardrails, shared memory, persona state, and narrative/world-model events.

## Purpose

This document aligns Buddy ecosystem behavior with compatible public concepts from orchestrated agent systems, tool/agent integration patterns, and multi-agent narrative/world-model systems. It does not copy proprietary code and does not claim drop-in compatibility with any external implementation.

## Symphony-style orchestration concepts

Buddy ecosystem systems should support these orchestration concepts:

- **Orchestrator:** Buddy owns intent, planning, delegation, review, and final response.
- **Worker agents:** Lil' Buddy agents execute scoped tasks and return structured results.
- **Handoffs:** Work moves through explicit task envelopes rather than hidden side effects.
- **Guardrails:** Safety and policy checks happen before and after worker execution.
- **Review loop:** Buddy verifies worker output before using it.
- **Receipts:** Meaningful actions should leave enough evidence to audit what happened.

## Agents SDK-style integration concepts

Runtime code should favor these integration patterns:

- **Tool contracts:** Tools declare name, risk class, input schema, output schema, and approval requirements.
- **Structured outputs:** Tasks and results use stable JSON-like envelopes.
- **Agent boundaries:** Buddy and Lil' Buddy roles are explicit and testable.
- **Local-first demos:** Examples should run without paid APIs or secrets.
- **Provider isolation:** Network providers are optional adapters, not required for the standard.
- **Guardrail hooks:** Runtime paths expose review and escalation points before actions.

## OpenMythos-style world-model concepts

Buddy also needs durable shared context for persona, memory, story, and state:

- **Myth/world memory:** Long-lived facts, decisions, relationships, and environment assumptions live in KnowledgeVault or approved runtime memory.
- **Agent personas:** Buddy and Lil' Buddy have stable role contracts. Persona is not permission to bypass policy.
- **Narrative events:** Meaningful interactions can be recorded as events with actor, intent, action, outcome, and review status.
- **Durable shared context:** Multi-agent work should reuse a source-linked context bundle instead of relying only on chat history.
- **Collaboration rules:** Agents coordinate through envelopes, not hidden authority changes.
- **Continuity checks:** Current claims must be verified against the owning source before they are promoted to durable memory.

## Standard event shape

Narrative/world events should use this shape when persisted:

```json
{
  "schema_version": "buddy.world_event.v1",
  "event_id": "event-001",
  "timestamp": "2026-06-12T00:00:00Z",
  "actor": "Buddy",
  "participants": ["Lil' Buddy"],
  "user_intent": "What the human or device event asked for",
  "world_context_refs": ["knowledge-vault/path/to/context.md"],
  "action": "planned | delegated | reviewed | responded | persisted",
  "outcome": "short reviewed outcome",
  "safety_class": "low | medium | high | blocked",
  "review_status": "approved | approved_with_notes | revise | escalate | block"
}
```

## Repository ownership

| Concern | Primary owner | Notes |
|---|---|---|
| Durable standards and memory | `knowledge-vault` | Public-safe source of durable context |
| Governance, policy, council routing | `buddy-brain` | Default contracts and escalation rules |
| Runtime envelopes, CLI, local demo | `buddy-agent` | Executable scaffolds and adapters |
| Local embodied events and device routing | `omni-buddy` | Voice, vision, sensor, and device action contracts |

## Non-goals

This standard does not:

- vendor external orchestration frameworks
- require paid APIs
- require cloud execution
- replace existing repo architectures
- grant Lil' Buddy independent authority
- turn narrative state into a safety bypass

## Agent instructions

- Use these concepts as design constraints when adding Buddy-compatible runtime code or docs.
- Keep role boundaries explicit in schemas and docs.
- Persist only public-safe durable memory in KnowledgeVault.
- Treat personas and narrative state as context, not authorization.
