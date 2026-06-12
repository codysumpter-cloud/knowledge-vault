---
type: status
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: medium
privacy: public
freshness: volatile
agent_load: task-specific
tags:
  - vegapunk-brain
  - status
  - event-sourced-memory
---

# Vegapunk Brain Status

Vegapunk Brain has moved from a static graph layer toward an event-sourced shared-memory platform.

## Implemented

### Graph substrate

- Minimal graph schema.
- Seed graph JSONL.
- Graph linter.
- Schema/linter support for generated `task`, `decision`, and `person` records.
- Graph builder for merged compiled graph output.
- Graph search for connected neighborhoods.
- Concept indexer for compact JSON indexes:
  - `concepts.json`
  - `repos.json`
  - `systems.json`
  - `decisions.json`
  - `tasks.json`
  - `people.json`
  - `relationships.json`

### Memory compilers

- Memory compiler for markdown/session/decision/repo docs.
- Graph event compiler for Shared Memory Bus event JSON/JSONL.
- Event-sourced graph compiler for emitter events.
- Event-sourced graph rebuilder.

### Event architecture

- Emitter schema.
- Emitter examples for:
  - `buddy-agent`
  - `buddy-brain`
  - `omni-buddy`
  - `prismtek-apps`
- Event inbox and processed directories.
- Event ingestor.
- Event router.
- Repo emitter contracts.

### Platform operations

- Graph health checks.
- Mermaid/JSON/text graph export.
- Tool syntax doctor.
- Shared Memory Bus contract.
- Satellite architecture document.
- Architecture summary.
- End-to-end runner.
- Validation/rebuild/index/doctor scripts.
- CI validation workflow for Punk Records.

## Operator commands

```bash
bash "99-System/Vegapunk Brain/scripts/doctor-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/validate-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/rebuild-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/index-vegapunk-brain.sh"
bash "99-System/Vegapunk Brain/scripts/run-vegapunk-brain.sh"
```

## Generated outputs

Generated outputs are intentionally ignored by git:

- `graph/generated.graph.jsonl`
- `graph/compiled.graph.jsonl`
- `indexes/*.json`
- `inbox/events/*.json`
- `inbox/processed/**/*.json`
- `outbox/**/*.json`
- `outbox/**/*.jsonl`
- `outbox/**/*.mmd`
- `outbox/**/*.txt`

## Current limitations

- The KnowledgeVault side of the event platform exists.
- Native event emitters still need to be added inside `buddy-agent`, `buddy-brain`, `omni-buddy`, and `prismtek-apps`.
- GraphViz DOT export was deferred; Mermaid, JSON, and text tree exports are implemented.
- Runtime validation must be confirmed by local execution or CI run results.

## Next useful build

Add repo-native event emitter helpers to each satellite repo so real task/session/decision/release flows produce event JSON automatically.
