---
type: decision
status: active
owner: Prismtek
source_of_truth: mixed
last_verified: 2026-08-04
risk_level: high
privacy: public
freshness: volatile
agent_load: cold-start
tags:
  - repository-authority
  - consolidation
  - privacy
---

# Canonical repository authority map

> Public-safe routing for Prismtek repository authority after the 2026-08-04 Buddy consolidation. Private repository names, paths, issue numbers, and commit identifiers are intentionally omitted.

## Purpose

This record gives public agents enough context to avoid using retired repository boundaries without publishing private implementation details.

GitHub remains authoritative for live repository visibility, branches, pull requests, checks, workflows, releases, and archive state. Authorized private sources remain authoritative for private implementation paths and migration evidence.

## Public standalone authorities

| Repository | Public role |
| --- | --- |
| `codysumpter-cloud/knowledge-vault` | Public-safe memory, schemas, receipts, evidence standards, and coordination contracts. |
| `codysumpter-cloud/buddy-universal-agent-profile` | Public BUAP policy/compiler project and stable public artifact. |
| `codysumpter-cloud/PocketBuddyPlus` | Active Pocket Buddy+ product-rescue repository. Pocket Buddy+ is the product identity; OpenPets is the donor/upstream foundation. |

## Private implementation authority

The canonical Buddy product/runtime monorepo is private. Its name, paths, pull requests, issues, and commit identifiers must not be copied into this public vault.

It owns the consolidated implementation for Buddy runtime, governance, adapters, embodied-device support, visual/core contracts, and trust-fabric verification. Agents without authorized private access must not guess its structure or claim a private implementation is present, tested, or deployed.

## Consolidation status

Confirmed on 2026-08-04:

- Eight legacy Buddy repository boundaries were retired and archived rather than deleted.
- Five source histories were imported into the private canonical implementation repository.
- Three sources were audited and retained only as historical/reference archives.
- Exact source names, destination paths, source heads, private migration manifests, and private tracker references are intentionally omitted here.

Historical public notes written before consolidation may still use old repository names. Treat them as historical context, not current routing authority.

## Public routing rules

1. Current explicit user direction wins for product intent.
2. Public BUAP manifests own public policy and component-contract declarations.
3. Authorized private repository records own private implementation paths and migration state.
4. KnowledgeVault owns only the redacted public-safe decision history.
5. Pocket Buddy+ remains standalone during product rescue.
6. A copied directory is not proof of a completed migration.
7. A merged migration is not proof that every source archive gate passed.
8. Never infer private repository names or paths from old chat context.
9. Never copy private repository identifiers into public notes, dashboards, registries, receipts, PR bodies, or commit messages.
10. Verify live GitHub and runtime evidence before claiming a feature is implemented, tested, released, or deployed.

## Buddy Brain licensing status

Source-backed as resolved on 2026-08-04:

- The current governing license for the consolidated Buddy Brain subtree is Prismtek Source Available License 1.0.
- The repository owner attested that the affected contributor consented to inclusion of their Apache-2.0-window contributions under the current license.
- The written consent artifact is not attached to this public vault. Attaching a durable written record and adding a CLA or DCO remain recommended non-blocking follow-ups.
- Copies distributed during the prior Apache-2.0 window retain the rights already granted to those copies.

This is a project-status record, not legal advice.

## Known unknowns

- A full content-level scan for private repository identifiers has not been run in this connector session.
- Public Git history may retain identifiers that were previously committed; this task does not rewrite history.
- Repository doctor and note-quality linter execution have not been observed for this draft remediation branch.
- The five-task life-assistant loop remains in monitored rollout until the required seven-day soak test passes.

## Agent instructions

- Load this note when deciding which public source can be cited for Prismtek repository authority.
- Do not use it to infer private repository structure.
- Verify public repository state directly in GitHub.
- Use authorized private sources for private implementation decisions.
- Keep public receipts redacted and public-safe.

## Next action

- [ ] Run `python3 "99-System/Automation/vault_doctor.py"` and `python3 "99-System/Automation/note_quality_linter.py"` on the remediation branch.
- [ ] Run a repository-wide content scan for private repository identifiers before merging.
- [ ] Review the draft remediation PR and merge only after validation is green.
