#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"

python "$BRAIN/tools/memory_compiler.py" \
  --source "$BRAIN/examples/session-to-graph.md" \
  --out "$BRAIN/graph/generated.graph.jsonl"

python "$BRAIN/tools/graph_linter.py" \
  "$BRAIN/graph/seed.graph.jsonl" \
  "$BRAIN/graph/generated.graph.jsonl"

python "$BRAIN/tools/graph_builder.py" \
  --graph "$BRAIN/graph/seed.graph.jsonl" \
  --graph "$BRAIN/graph/generated.graph.jsonl" \
  --out "$BRAIN/graph/compiled.graph.jsonl"

python "$BRAIN/tools/graph_linter.py" \
  "$BRAIN/graph/compiled.graph.jsonl"

python "$BRAIN/tools/concept_indexer.py" \
  --graph "$BRAIN/graph/compiled.graph.jsonl" \
  --out-dir "$BRAIN/indexes"

python "$BRAIN/tools/graph_search.py" \
  --graph "$BRAIN/graph/compiled.graph.jsonl" \
  --query "Knowledge Vault"
