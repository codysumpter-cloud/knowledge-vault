# Vegapunk Brain Tools

Dependency-free Python tools for the KnowledgeVault shared graph layer.

## Compile memory

```bash
python "99-System/Vegapunk Brain/tools/memory_compiler.py" \
  --source "99-System/Vegapunk Brain/examples/session-to-graph.md" \
  --out "99-System/Vegapunk Brain/graph/generated.graph.jsonl"
```

## Lint graph records

```bash
python "99-System/Vegapunk Brain/tools/graph_linter.py" \
  "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
  "99-System/Vegapunk Brain/graph/generated.graph.jsonl"
```

## Build compiled graph

```bash
python "99-System/Vegapunk Brain/tools/graph_builder.py" \
  --graph "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
  --graph "99-System/Vegapunk Brain/graph/generated.graph.jsonl" \
  --out "99-System/Vegapunk Brain/graph/compiled.graph.jsonl"
```

## Generate indexes

```bash
python "99-System/Vegapunk Brain/tools/concept_indexer.py" \
  --graph "99-System/Vegapunk Brain/graph/compiled.graph.jsonl" \
  --out-dir "99-System/Vegapunk Brain/indexes"
```

Generated indexes:

- `concepts.json`
- `repos.json`
- `systems.json`
- `relationships.json`
- `tags.json`
- `all-records.json`

## Search graph

```bash
python "99-System/Vegapunk Brain/tools/graph_search.py" \
  --graph "99-System/Vegapunk Brain/graph/compiled.graph.jsonl" \
  --query "Knowledge Vault"
```

Useful filters:

```bash
--tag memory
--repo buddy-agent
--relationship feeds
--confidence high
--freshness current
--depth 2
--json
```
