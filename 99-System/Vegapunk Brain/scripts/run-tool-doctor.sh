#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
python "$ROOT/99-System/Vegapunk Brain/tools/graph_doctor.py"
