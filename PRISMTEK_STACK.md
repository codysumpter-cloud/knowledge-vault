# Prismtek Buddy Stack

KnowledgeVault is the **durable records and provenance layer** of the Prismtek Buddy Agent Platform. It is not the entire agent platform and it is not the guarded execution runtime.

Its machine-readable ownership and dependencies are declared in [`prismtek.component.json`](prismtek.component.json). The canonical public topology is maintained by BUAP.

## KnowledgeVault owns

- durable project memory and source-of-truth records
- immutable Vegapunk Brain events
- graph compilation and rebuildable indexes
- provenance, freshness, claim status, and public/private boundaries

## KnowledgeVault does not own

- portable agent policy compilation
- guarded execution or sandbox enforcement
- final artifact verification
- device runtime
- product interfaces

## Trust Fabric receiver

Buddy Agent emits sanitized `evidence_evaluated` and `execution_verified` events. The events contain task IDs, policy state, source hashes, and artifact hashes; they must not contain raw prompts, credentials, browser state, or source excerpts.

See [`99-System/Vegapunk Brain/integrations/prismtek-trust-fabric.md`](99-System/Vegapunk%20Brain/integrations/prismtek-trust-fabric.md).
