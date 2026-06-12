#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"

python "$BRAIN/tools/graph_doctor.py"
python "$BRAIN/tools/graph_linter.py" "$BRAIN/graph/seed.graph.jsonl"
python "$BRAIN/tools/event_ingestor.py" \
  --source "$BRAIN/emitters" \
  --inbox "$BRAIN/inbox/events" \
  --reject-dir "$BRAIN/outbox/rejected-events"
python "$BRAIN/tools/event_router.py" \
  --inbox "$BRAIN/inbox/events" \
  --processed "$BRAIN/inbox/processed"
