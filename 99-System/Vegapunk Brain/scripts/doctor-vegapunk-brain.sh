#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
BRAIN="$ROOT/99-System/Vegapunk Brain"

python "$BRAIN/tools/graph_doctor.py"
python "$BRAIN/tools/graph_linter.py" "$BRAIN/graph/seed.graph.jsonl"
