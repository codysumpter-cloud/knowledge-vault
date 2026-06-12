#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"

bash "$BRAIN/scripts/validate-vegapunk-brain.sh" "$ROOT"
bash "$BRAIN/scripts/rebuild-vegapunk-brain.sh" "$ROOT"

python "$BRAIN/tools/graph_search.py" \
  --graph "$BRAIN/outbox/graph-records/compiled.graph.jsonl" \
  --query "Knowledge Vault"
