#!/usr/bin/env python3
"""Search Vegapunk Brain graph records and return connected neighborhoods.

Usage:
    python "99-System/Vegapunk Brain/tools/graph_search.py" \
      --graph "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
      --query "Knowledge Vault"

Filters:
    --tag memory
    --repo buddy-agent
    --relationship feeds
    --confidence high
    --freshness current
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any


def load_graph(paths: list[Path]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                records[record["id"]] = record
    return records


def normalize(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def matches(record: dict[str, Any], args: argparse.Namespace) -> bool:
    blob = " ".join([
        record.get("id", ""),
        record.get("name", ""),
        record.get("summary", ""),
        " ".join(record.get("tags", [])),
    ]).lower()
    if args.query and normalize(args.query) not in normalize(blob):
        return False
    if args.tag and args.tag not in record.get("tags", []):
        return False
    if args.repo:
        repo_id = f"repo:{normalize(args.repo).removeprefix('repo:')}"
        if record.get("id") != repo_id and all(link.get("target") != repo_id for link in record.get("links", [])):
            return False
    if args.relationship and all(link.get("type") != args.relationship for link in record.get("links", [])):
        return False
    if args.confidence and record.get("provenance", {}).get("confidence") != args.confidence:
        return False
    if args.freshness and record.get("freshness", {}).get("status") != args.freshness:
        return False
    return True


def reverse_edges(records: dict[str, dict[str, Any]]) -> dict[str, list[tuple[str, dict[str, str]]]]:
    reverse: dict[str, list[tuple[str, dict[str, str]]]] = {record_id: [] for record_id in records}
    for source_id, record in records.items():
        for link in record.get("links", []):
            target = link.get("target")
            if target in reverse:
                reverse[target].append((source_id, link))
    return reverse


def neighborhood(records: dict[str, dict[str, Any]], seeds: list[str], depth: int) -> dict[str, dict[str, Any]]:
    reverse = reverse_edges(records)
    found: dict[str, dict[str, Any]] = {}
    queue: deque[tuple[str, int]] = deque((seed, 0) for seed in seeds)
    while queue:
        record_id, distance = queue.popleft()
        if record_id in found or record_id not in records:
            continue
        found[record_id] = records[record_id]
        if distance >= depth:
            continue
        for link in records[record_id].get("links", []):
            queue.append((link["target"], distance + 1))
        for source_id, _link in reverse.get(record_id, []):
            queue.append((source_id, distance + 1))
    return found


def print_tree(records: dict[str, dict[str, Any]], seeds: list[str], depth_records: dict[str, dict[str, Any]]) -> None:
    for seed in seeds:
        if seed not in depth_records:
            continue
        root = depth_records[seed]
        print(root["name"])
        connected = []
        for link in root.get("links", []):
            if link["target"] in depth_records:
                connected.append((link["type"], link["target"]))
        for source_id, source in depth_records.items():
            if source_id == seed:
                continue
            for link in source.get("links", []):
                if link.get("target") == seed:
                    connected.append((link["type"], source_id))
        seen = set()
        for rel, target in connected:
            if target in seen or target not in records:
                continue
            seen.add(target)
            print(f"├── {records[target]['name']} ({rel})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Vegapunk Brain graph neighborhoods.")
    parser.add_argument("--graph", nargs="+", required=True, help="Graph JSONL file(s).")
    parser.add_argument("--query", help="Search by id, name, summary, or tag text.")
    parser.add_argument("--tag", help="Filter by exact tag.")
    parser.add_argument("--relationship", help="Filter by outgoing relationship type.")
    parser.add_argument("--repo", help="Filter records connected to a repo slug/id.")
    parser.add_argument("--confidence", choices=["low", "medium", "high"], help="Filter by provenance confidence.")
    parser.add_argument("--freshness", choices=["current", "stale", "unknown"], help="Filter by freshness status.")
    parser.add_argument("--depth", type=int, default=1, help="Neighborhood depth. Default: 1.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of tree text.")
    args = parser.parse_args()

    records = load_graph([Path(item) for item in args.graph])
    seeds = [record_id for record_id, record in records.items() if matches(record, args)]
    results = neighborhood(records, seeds, args.depth)

    if args.json:
        print(json.dumps([results[key] for key in sorted(results)], indent=2, sort_keys=True))
    else:
        if not seeds:
            print("No matching graph records.")
        else:
            print_tree(records, seeds, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
