---
type: status
status: active
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-06-12
risk_level: low
privacy: public
freshness: volatile
agent_load: task-specific
tags:
  - vegapunk-brain
  - status
---

# Vegapunk Brain Status

## Implemented

- Minimal graph schema.
- Seed graph JSONL.
- Graph linter.
- Schema/linter support for generated `task`, `decision`, and `person` records.
- Memory compiler for markdown/session/decision/repo docs.
- Graph event compiler for Shared Memory Bus event JSON/JSONL.
- Graph builder for merged compiled graph output.
- Concept indexer for compact JSON indexes.
- Graph search for connected neighborhoods.
- Tool syntax doctor.
- Shared Memory Bus contract.
- Integration contracts for:
  - `buddy-agent`
  - `buddy-brain`
  - `omni-buddy`
  - `prismtek-apps`
- Session-to-graph example.
- End-to-end local runner.

## Local validation command

```bash
bash "99-System/Vegapunk Brain/scripts/run-vegapunk-brain.sh"
```

## Generated outputs

Generated outputs are intentionally ignored by git:

- `graph/generated.graph.jsonl`
- `graph/compiled.graph.jsonl`
- `indexes/*.json`

## Next useful build

Add CI that runs:

```bash
python "99-System/Vegapunk Brain/tools/graph_doctor.py"
python "99-System/Vegapunk Brain/tools/graph_linter.py" "99-System/Vegapunk Brain/graph/seed.graph.jsonl"
```

Then add repo-specific graph-event emitters in `buddy-agent`, `buddy-brain`, `omni-buddy`, and `prismtek-apps`.
