#!/usr/bin/env python3
"""Build a merged Vegapunk Brain graph from seed and generated JSONL files.

Usage:
    python "99-System/Vegapunk Brain/tools/graph_builder.py" \
      --graph "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
      --graph "99-System/Vegapunk Brain/graph/generated.graph.jsonl" \
      --out "99-System/Vegapunk Brain/graph/compiled.graph.jsonl"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


def load_records(paths: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            raise SystemExit(f"Missing graph input: {path}")
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"Invalid JSON in {path}:{line_no}: {exc}") from exc
    return records


def confidence(record: dict[str, Any]) -> int:
    return CONFIDENCE_RANK.get(record.get("provenance", {}).get("confidence", "low"), 0)


def merge_links(existing: list[dict[str, str]], incoming: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = {(link.get("type"), link.get("target"), link.get("reason")) for link in existing}
    merged = list(existing)
    for link in incoming:
        key = (link.get("type"), link.get("target"), link.get("reason"))
        if key not in seen:
            merged.append(link)
            seen.add(key)
    return merged


def merge_records(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record["id"]
        if record_id not in merged:
            merged[record_id] = record
            continue
        current = merged[record_id]
        winner, loser = (record, current) if confidence(record) > confidence(current) else (current, record)
        winner = dict(winner)
        winner["links"] = merge_links(current.get("links", []), record.get("links", []))
        winner["tags"] = sorted(set(current.get("tags", []) + record.get("tags", [])))
        merged[record_id] = winner
    return merged


def prune_broken_links(records: dict[str, dict[str, Any]]) -> None:
    ids = set(records)
    for record in records.values():
        record["links"] = [link for link in record.get("links", []) if link.get("target") in ids]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build merged Vegapunk Brain graph JSONL.")
    parser.add_argument("--graph", action="append", required=True, help="Input graph JSONL. Repeat for multiple files.")
    parser.add_argument("--out", required=True, help="Output compiled graph JSONL path.")
    parser.add_argument("--keep-broken-links", action="store_true", help="Keep links to records that are not present in loaded graph files.")
    args = parser.parse_args()

    merged = merge_records(load_records([Path(item) for item in args.graph]))
    if not args.keep_broken_links:
        prune_broken_links(merged)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for record_id in sorted(merged):
            handle.write(json.dumps(merged[record_id], sort_keys=True, separators=(",", ":")) + "\n")

    print(f"Built {len(merged)} records into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
