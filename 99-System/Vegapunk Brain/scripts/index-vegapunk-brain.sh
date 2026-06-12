#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"
GRAPH="${2:-$BRAIN/outbox/graph-records/compiled.graph.jsonl}"

python "$BRAIN/tools/concept_indexer.py" \
  --graph "$GRAPH" \
  --out-dir "$BRAIN/outbox/indexes"
