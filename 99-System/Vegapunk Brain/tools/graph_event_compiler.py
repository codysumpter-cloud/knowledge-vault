#!/usr/bin/env python3
"""Convert Shared Memory Bus events into Vegapunk Brain graph records.

Usage:
    python "99-System/Vegapunk Brain/tools/graph_event_compiler.py" \
      --event "99-System/Vegapunk Brain/graph-events/example.event.json" \
      --out "99-System/Vegapunk Brain/graph/events.graph.jsonl"
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

VALID_TYPES = {"decision", "memory", "task", "skill", "artifact", "conversation_summary"}
TYPE_MAP = {
    "decision": "decision",
    "task": "task",
    "skill": "system",
    "artifact": "concept",
    "memory": "concept",
    "conversation_summary": "concept",
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-") or "unnamed"


def load_events(paths: list[Path]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in paths:
        if path.is_dir():
            for child in sorted(path.glob("*.json")):
                events.extend(load_events([child]))
            for child in sorted(path.glob("*.jsonl")):
                events.extend(load_events([child]))
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        if path.suffix == ".jsonl":
            for line in text.splitlines():
                if line.strip():
                    events.append(json.loads(line))
        else:
            payload = json.loads(text)
            if isinstance(payload, list):
                events.extend(payload)
            else:
                events.append(payload)
    return events


def event_to_record(event: dict[str, Any]) -> dict[str, Any]:
    kind = event.get("kind")
    if kind not in VALID_TYPES:
        raise ValueError(f"Unsupported event kind: {kind!r}")
    record_type = TYPE_MAP[kind]
    title = event.get("title") or event.get("summary") or event.get("event_id")
    created = event.get("created") or event.get("updated")
    updated = event.get("updated") or created
    if not created or not updated:
        raise ValueError(f"Event {event.get('event_id', '<unknown>')} needs created and updated timestamps")
    record_id = f"{record_type}:{slugify(str(title))}"
    tags = sorted(set([record_type, "graph-event"] + list(event.get("tags", []))))
    links = []
    producer = event.get("producer")
    if isinstance(producer, str) and ":" in producer:
        links.append({"type": "emitted_by", "target": producer, "reason": "Record was compiled from a Shared Memory Bus event."})
    return {
        "id": record_id,
        "type": record_type,
        "name": str(title)[:120],
        "summary": str(event.get("summary") or event.get("body") or title)[:500],
        "tags": tags,
        "links": links,
        "provenance": {
            "source": str(event.get("event_id") or event.get("source") or "graph-event"),
            "confidence": event.get("confidence", "medium"),
            "created": created,
            "updated": updated,
        },
        "freshness": {"status": "current", "updated": updated[:10]},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile graph events into graph JSONL records.")
    parser.add_argument("--event", nargs="+", required=True, help="Event JSON/JSONL file or directory.")
    parser.add_argument("--out", required=True, help="Output graph JSONL file.")
    args = parser.parse_args()

    records = [event_to_record(event) for event in load_events([Path(item) for item in args.event])]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for record in sorted(records, key=lambda item: item["id"]):
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"Compiled {len(records)} event records into {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
