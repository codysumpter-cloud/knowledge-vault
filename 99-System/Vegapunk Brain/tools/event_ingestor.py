#!/usr/bin/env python3
"""Validate and accept Vegapunk Brain graph events into inbox/events.

Examples:
    python "99-System/Vegapunk Brain/tools/event_ingestor.py" \
      --source "99-System/Vegapunk Brain/emitters" \
      --inbox "99-System/Vegapunk Brain/inbox/events"
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from event_common import load_json_events, validate_event, write_json


def event_filename(event: dict) -> str:
    return f"{event['timestamp'][:10]}__{event['source']}__{event['event_id']}.json"


def ingest_path(source: Path, inbox: Path, reject_dir: Path | None = None) -> tuple[int, int]:
    accepted = 0
    rejected = 0
    for path in sorted(source.rglob("*.json")) if source.is_dir() else [source]:
        if path.name == "graph-event.schema.json":
            continue
        try:
            events = load_json_events(path)
        except Exception as exc:  # noqa: BLE001 - CLI should report every bad file.
            rejected += 1
            if reject_dir:
                write_json(reject_dir / f"{path.stem}.error.json", {"source_file": str(path), "errors": [str(exc)]})
            continue
        for event in events:
            errors = validate_event(event)
            if errors:
                rejected += 1
                if reject_dir:
                    write_json(reject_dir / f"{path.stem}.{rejected}.error.json", {"source_file": str(path), "event": event, "errors": errors})
                continue
            destination = inbox / event_filename(event)
            if destination.exists():
                existing = json.loads(destination.read_text(encoding="utf-8"))
                if existing != event:
                    raise SystemExit(f"Immutable event conflict for {event['event_id']} at {destination}")
            else:
                write_json(destination, event)
            accepted += 1
    return accepted, rejected


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and accept Vegapunk Brain graph events.")
    parser.add_argument("--source", required=True, help="Event JSON file or directory.")
    parser.add_argument("--inbox", required=True, help="Accepted event inbox directory.")
    parser.add_argument("--reject-dir", help="Optional directory for rejected event reports.")
    parser.add_argument("--copy-source", help="Optional directory to copy raw accepted source files for audit.")
    args = parser.parse_args()

    accepted, rejected = ingest_path(Path(args.source), Path(args.inbox), Path(args.reject_dir) if args.reject_dir else None)
    if args.copy_source and accepted:
        copy_target = Path(args.copy_source)
        copy_target.mkdir(parents=True, exist_ok=True)
        source = Path(args.source)
        if source.is_file():
            shutil.copy2(source, copy_target / source.name)
    print(f"Ingested {accepted} events; rejected {rejected}")
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
