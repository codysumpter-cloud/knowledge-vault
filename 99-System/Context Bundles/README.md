# Context Bundles

Status: draft
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

Context bundles are curated vault slices for agents.

They prevent the worst agent-memory failure mode: loading too much unrelated context, then confidently mixing stale notes with current work.

A bundle should be small, public-safe, source-linked, and task-specific.

## Bundle rule

A context bundle is not the source of truth. It is a routing layer.

Agents should use a bundle to decide what to inspect next, then verify current claims against the owning source before acting.

## Bundle types

| Bundle | Purpose |
|---|---|
| `cold-start` | Orient any new agent or human. |
| `vault-steward` | Maintain KnowledgeVault safely. |
| `buddy-agent-maintainer` | Work on Buddy-agent with current project memory. |
| `prismtek-apps-maintainer` | Work on Prismtek app projects with current context. |
| `public-alpha-reviewer` | Review claims, docs, and public readiness. |
| `knowledge-engine` | Work on source-guided concept packs like Wikipedia. |

## Required bundle files

Each bundle should eventually have:

```txt
99-System/Context Bundles/<bundle-id>/
├── manifest.json
├── bundle.md
└── receipt.example.json
```

## Manifest fields

See [`../Schemas/context-bundle.schema.json`](../Schemas/context-bundle.schema.json).

Minimum fields:

- `id`
- `name`
- `purpose`
- `status`
- `generated_at`
- `privacy`
- `included_files`
- `excluded_patterns`
- `freshness_notes`
- `safety_notes`

## Agent loading order

1. Load `README.md`, `AGENTS.md`, `SYSTEMMAP.md`, and `AGENT_DATABASE_BLUEPRINT.md`.
2. Pick the smallest matching bundle.
3. Read the bundle manifest before reading the bundled content.
4. Check freshness notes and safety notes.
5. Verify current repo/PR/CI/runtime claims with the owning source.
6. Produce or update a receipt if taking meaningful action.

## Safety exclusions

Bundles must not include:

- local-only private folders
- security folders
- private repo details while this repo is public
- sensitive local paths
- signed-in session material
- raw large third-party mirrors
- copyrighted binaries or game files
- automation payloads that violate platform or game rules

## Bundle quality checklist

- [ ] The bundle has a single clear task family.
- [ ] Every included file has a reason.
- [ ] The bundle excludes private/local-only paths.
- [ ] Volatile claims are marked for live verification.
- [ ] The bundle is short enough to fit in an agent context window.
- [ ] The manifest can be validated against the schema.
- [ ] The bundle has a receipt example.
