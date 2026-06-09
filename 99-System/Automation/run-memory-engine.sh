#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "[memory-engine] building index, graph, and Obsidian note"
python3 -m memory_engine index

echo "[memory-engine] smoke search"
python3 -m memory_engine search "agent" --limit 5 --json >/tmp/knowledge-vault-memory-engine-search.json

echo "[memory-engine] done"
echo "  index:   99-System/Memory Engine/memory-index.json"
echo "  graph:   99-System/Memory Engine/memory-graph.json"
echo "  obsidian: 99-System/Memory Engine/Obsidian Memory Index.md"
echo "  search smoke: /tmp/knowledge-vault-memory-engine-search.json"
