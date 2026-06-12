#!/usr/bin/env python3
"""Generate Vegapunk Brain graph indexes.

Usage:
    python "99-System/Vegapunk Brain/tools/concept_indexer.py" \
      --graph "99-System/Vegapunk Brain/graph/seed.graph.jsonl" \
      --out-dir "99-System/Vegapunk Brain/indexes"
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

INDEX_NAMES = {
    "concept": "concepts.json",
    "repo": "repos.json",
    "system": "systems.json",
}


def load_graph(paths: list[Path]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                record_id = record["id"]
                if record_id in records:
                    raise SystemExit(f"Duplicate graph id {record_id} in {path}:{line_no}")
                records[record_id] = record
    return records


def compact(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "type": record["type"],
        "name": record["name"],
        "summary": record["summary"],
        "tags": record.get("tags", []),
        "freshness": record.get("freshness", {}),
        "confidence": record.get("provenance", {}).get("confidence", "unknown"),
        "link_count": len(record.get("links", [])),
    }


def build_relationships(records: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    relationships: list[dict[str, str]] = []
    for source_id, record in sorted(records.items()):
        for link in record.get("links", []):
            relationships.append({
                "source": source_id,
                "type": link["type"],
                "target": link["target"],
                "reason": link["reason"],
            })
    return relationships


def build_tag_index(records: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = defaultdict(list)
    for record_id, record in sorted(records.items()):
        for tag in record.get("tags", []):
            tags[tag].append(record_id)
    return dict(sorted(tags.items()))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Vegapunk Brain graph indexes.")
    parser.add_argument("--graph", nargs="+", required=True, help="Graph JSONL file(s).")
    parser.add_argument("--out-dir", required=True, help="Directory for generated JSON indexes.")
    args = parser.parse_args()

    records = load_graph([Path(item) for item in args.graph])
    out_dir = Path(args.out_dir)

    for record_type, filename in INDEX_NAMES.items():
        items = [compact(record) for record in records.values() if record.get("type") == record_type]
        write_json(out_dir / filename, sorted(items, key=lambda item: item["id"]))

    write_json(out_dir / "relationships.json", build_relationships(records))
    write_json(out_dir / "tags.json", build_tag_index(records))
    write_json(
        out_dir / "all-records.json",
        sorted(
            [compact(record) for record in records.values()],
            key=lambda item: item["id"],
        ),
    )

    print(f"Indexed {len(records)} records into {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
