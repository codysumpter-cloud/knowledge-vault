#!/usr/bin/env python3
"""Rebuild Vegapunk Brain graph state from seed graph plus event history."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild Vegapunk Brain graph from events.")
    parser.add_argument("--root", default=".", help="Repository root. Default: current directory.")
    args = parser.parse_args()

    root = Path(args.root)
    brain = root / "99-System" / "Vegapunk Brain"
    tools = brain / "tools"
    seed = brain / "graph" / "seed.graph.jsonl"
    processed = brain / "inbox" / "processed"
    event_records = brain / "outbox" / "graph-records" / "events.graph.jsonl"
    compiled = brain / "outbox" / "graph-records" / "compiled.graph.jsonl"
    index_out = brain / "outbox" / "indexes"

    for generated in [event_records, compiled]:
        if generated.exists():
            generated.unlink()
    if index_out.exists():
        for child in index_out.glob("*.json"):
            child.unlink()

    event_sources = [str(processed)]
    if not any(processed.rglob("*.json")):
        event_sources = [str(brain / "emitters")]

    run([sys.executable, str(tools / "graph_compiler.py"), "--events", *event_sources, "--out", str(event_records)])
    run([sys.executable, str(tools / "graph_linter.py"), str(seed), str(event_records)])
    run([sys.executable, str(tools / "graph_builder.py"), "--graph", str(seed), "--graph", str(event_records), "--out", str(compiled)])
    run([sys.executable, str(tools / "graph_linter.py"), str(compiled)])
    run([sys.executable, str(tools / "concept_indexer.py"), "--graph", str(compiled), "--out-dir", str(index_out)])
    print(f"Rebuilt Vegapunk Brain graph into {compiled}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
