---
type: integration
status: wired
owner: Prismtek
source_of_truth: mixed
last_verified: 2026-07-29
risk_level: medium
privacy: public
freshness: volatile
agent_load: task-specific
tags:
  - vegapunk-brain
  - trust-fabric
  - provenance
  - buddy-agent
---

# Prismtek Trust Fabric receiver

## Purpose

Define how Buddy Agent evidence and verification outputs enter Vegapunk Brain without turning retrieval output into trusted memory by default.

## Ownership boundary

- External retrieval providers supply cited source candidates.
- Buddy Agent normalizes evidence, applies admissibility policy, guards execution, and verifies artifacts.
- Buddy Brain aggregates policy outcomes and verified-outcome economics.
- KnowledgeVault stores accepted immutable events and rebuildable graph state.
- BUAP owns portable policy compilation and ecosystem routing.

## Accepted events

### `evidence_evaluated`

Required payload fields:

- `task_id`
- `provider`
- `risk_level`
- `decision`: `allow`, `review`, or `block`
- `query_digest`
- `evidence_hashes`
- `stale_source_ids`
- `conflicting_source_ids`

This event records that evidence was evaluated. It does **not** claim the resulting work was completed or verified.

### `execution_verified`

Required payload fields:

- `task_id`
- `decision`
- `artifact_hash`
- `reviewer`
- `security_gate`

This event may be emitted only after Buddy Agent verifies a real artifact and the security gate passes.

## Privacy invariant

The event payload must not contain:

- raw prompts or full user queries
- credentials, tokens, or secret values
- browser state
- source excerpts or full private documents
- unredacted personal data

Use cryptographic digests and stable source IDs for traceability.

## Ingestion flow

```text
buddy-trust evaluate
      -> evidence_evaluated event
      -> Vegapunk event ingestor
      -> policy/claim graph records

buddy-trust finalize
      -> execution_verified event
      -> Vegapunk event ingestor
      -> artifact/verification relationships
```

## Claim status

- `evidence_evaluated` with `allow` is `source-backed`, not `verified`.
- `review` and `block` remain unresolved until a later event records adjudication.
- Only `execution_verified` with a passing security gate can support a `verified` completion claim.

## Validation

Run the normal Vegapunk Brain validation and rebuild sequence after adding fixtures or changing the event schema.
