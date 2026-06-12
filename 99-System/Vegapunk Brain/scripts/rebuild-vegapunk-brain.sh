#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"

python "$BRAIN/tools/graph_rebuilder.py" --root "$ROOT"
python "$BRAIN/tools/graph_health.py" \
  --graph "$BRAIN/outbox/graph-records/compiled.graph.jsonl" \
  --out "$BRAIN/outbox/health-report.json"
python "$BRAIN/tools/graph_export.py" \
  --graph "$BRAIN/outbox/graph-records/compiled.graph.jsonl" \
  --out-dir "$BRAIN/outbox/visualizations"
