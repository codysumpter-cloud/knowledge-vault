---
type: decision
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-09
risk_level: low
privacy: public
freshness: stable
agent_load: task-specific
tags:
  - decisions
  - knowledge-vault
  - agent-memory
---

# Decisions — knowledge-vault

> Durable decisions that future agents should not rediscover from scratch.

| Date | Decision | Why | Owner |
|---|---|---|---|
| 2026-06-04 | Treat KnowledgeVault as active Prismtek infrastructure. | It is the durable operating memory and navigation layer for Prismtek/Buddy/Hermes work. | Prismtek / Vault Steward |
| 2026-06-09 | Position KnowledgeVault as an agent memory database. | Agents need structured retrieval, provenance, freshness, and quality rules; a loose markdown pile is not enough. | Prismtek |
| 2026-06-09 | Add note standards, schemas, context bundles, and a linter. | The vault needs enforceable shapes and starter bundles so future agents can use it consistently. | Prismtek / agent maintainer |

## 2026-06-04 — Treat KnowledgeVault as active Prismtek infrastructure

**Decision:** KnowledgeVault is active critical infrastructure, not a triage placeholder.

**Context:** Prismtek has multiple repos and agent/runtime directions. Agents need a durable source of memory that survives chat context loss.

**Rationale:** Without a memory layer, agents repeatedly rediscover repo purpose, stale decisions, and safety boundaries.

**Consequences:** Root docs, project status, automation safety, and future agent ingestion should treat the vault as a serious operating system for project memory.

**Reversal conditions:** Revisit only if a better memory layer fully replaces KnowledgeVault and imports its durable context.

## 2026-06-09 — Position KnowledgeVault as an agent memory database

**Decision:** KnowledgeVault should be described and maintained as a public-safe agent memory database, not just an Obsidian note collection.

**Context:** The repo needs to be useful to humans and agents. Agents need predictable metadata, source-of-truth rules, freshness classes, and routing paths.

**Rationale:** Better retrieval beats more raw notes. Clear structure reduces hallucinated capability claims and stale assumptions.

**Consequences:** Root docs now point agents through `AGENT_KNOWLEDGE_INDEX.md`, `AGENT_DATABASE_BLUEPRINT.md`, standards, schemas, and context bundles.

**Reversal conditions:** Revisit if the vault becomes private-only, if Buddy-agent owns all memory directly, or if a dedicated database replaces markdown-backed memory.

## 2026-06-09 — Add note standards, schemas, context bundles, and a linter

**Decision:** Add formal note-format standards, machine-readable schemas, a cold-start context bundle, and a lightweight markdown quality linter.

**Context:** Prior docs explained the goal but did not provide enough operational scaffolding for agents to create or validate useful notes.

**Rationale:** Agents need examples and checks. Humans need a consistent house style. CI or local automation should eventually catch missing titles, metadata, and weak note structure.

**Consequences:** Future notes should prefer the standard metadata contract and record shapes. Maintenance passes should run both `vault_doctor.py` and `note_quality_linter.py`.

**Reversal conditions:** Revisit if a stronger generated schema/lint pipeline replaces the lightweight linter.
