---
title: Canonical repository authority map
status: current
decided: 2026-08-04
supersedes: repository roles recorded before the 2026-08-04 Buddy consolidation
authority: codysumpter-cloud/prismtek-apps#359
---

# Canonical repository authority map

Recorded after the Buddy repository consolidation completed on 2026-08-04.

This is a durable public-safe decision record. GitHub remains authoritative for
live branch, PR, check, workflow, release, and archive state. The generated
inventory in `codysumpter-cloud.public.repo-registry.json` is a sync artifact
and is deliberately not rewritten by this record.

## Standalone and canonical

| Repository | Role |
| --- | --- |
| `codysumpter-cloud/prismtek-apps` | Canonical product and runtime monorepo. Owns product surfaces, Buddy runtime, governance, adapters, visual/core contracts, and verification tooling. |
| `codysumpter-cloud/buddy-universal-agent-profile` | Canonical public BUAP policy and compiler project. Standalone by explicit authority: it is a public portfolio artifact and the project submitted for the OpenAI six-month Pro application. Its public URL, history, issues, releases, and identity stay intact. |
| `codysumpter-cloud/knowledge-vault` | This repository. Canonical public-safe memory, schema, receipt, and evidence boundary. |
| `codysumpter-cloud/PocketBuddyPlus` | Active product repository, temporarily standalone during its product-rescue phase. Pocket Buddy+ is the product; OpenPets is the donor/upstream foundation. `@open-pets/*` names remain as compatibility identifiers only. |

## Consolidated into prismtek-apps and archived

Each was archived, not deleted. Full history was imported with original
authorship preserved, and each carries a `pre-archive-final` tag marking the
exact final state of its default branch.

| Former repository | Canonical location now | Migration record |
| --- | --- | --- |
| `codysumpter-cloud/prismtek-buddy-core` | `packages/buddy-core` | `docs/migrations/prismtek-buddy-core.yaml` |
| `codysumpter-cloud/buddy-agent` | `services/buddy-agent` | `docs/migrations/buddy-agent.yaml` |
| `codysumpter-cloud/buddy-brain` | `tools/buddy-brain` + `packages/buddy-governance` | `docs/migrations/buddy-brain.yaml` |
| `codysumpter-cloud/omni-buddy` | `packages/omni-adapters` + `services/omni-buddy` | `docs/migrations/omni-buddy.yaml` |
| `codysumpter-cloud/buddy` | `tools/trust-fabric` | `docs/migrations/buddy.yaml` |

## Audited and retired without migration

| Former repository | Outcome | Record |
| --- | --- | --- |
| `codysumpter-cloud/BMO-app` | Nothing salvaged. Every candidate was coupled to obsolete Firebase architecture, was a duplicate agent model, or was already represented by the canonical Buddy visual contract. Preserved as a historical reference. | `docs/migrations/BMO-app.yaml` |
| `codysumpter-cloud/be-more-agent` | Reference fork of `brenpoly/be-more-agent`. Prismtek delta was 2 files of fork maintenance; no product code. | `docs/migrations/be-more-agent.yaml` |
| `codysumpter-cloud/buddy-workspace` | Reference fork of `outsourc-e/hermes-workspace`. The 244-line Prismtek branding delta is preserved as a patch in prismtek-apps rather than vendoring the upstream tree. | `docs/migrations/buddy-workspace.yaml` |

## Terminology

Repository names are implementation boundaries, not product identity.

- **Buddy Brain** is a governance, memory-interpretation, economics, and model-policy capability. It is no longer a repository boundary.
- **Omni Buddy** is an embodied voice and vision adapter capability. It is no longer a repository boundary, and it is not a second canonical brain.
- **OpenPets** is the donor/upstream for Pocket Buddy+, not the current product.

## Historical note

Receipts and records written before 2026-08-04 that name the archived
repositories were correct when written and are deliberately left unchanged.
Read them against this map rather than assuming the old repository is still the
source of truth.

prismtek-apps revision at the time of this record: `f47023186c67e649378734ee80a158a022dbb941`
