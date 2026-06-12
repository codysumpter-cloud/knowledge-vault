#!/usr/bin/env python3
"""Route accepted Vegapunk Brain events from inbox/events to inbox/processed.

The router is append-safe: if a processed copy already exists, it must match the
incoming event exactly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from event_common import load_json_events, validate_event, write_json


def route_events(inbox: Path, processed: Path, remove: bool = False) -> int:
    count = 0
    processed.mkdir(parents=True, exist_ok=True)
    for path in sorted(inbox.glob("*.json")):
        events = load_json_events(path)
        for event in events:
            errors = validate_event(event)
            if errors:
                raise SystemExit(f"Invalid accepted event in {path}: {errors}")
            event_type = event["event_type"]
            target_dir = processed / event_type
            target = target_dir / path.name
            if target.exists():
                existing = json.loads(target.read_text(encoding="utf-8"))
                if existing != event:
                    raise SystemExit(f"Immutable processed event conflict: {target}")
            else:
                write_json(target, event)
            count += 1
        if remove:
            path.unlink()
    print(f"Routed {count} events into {processed}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Route Vegapunk Brain inbox events by type.")
    parser.add_argument("--inbox", required=True, help="Accepted event inbox directory.")
    parser.add_argument("--processed", required=True, help="Processed event directory.")
    parser.add_argument("--remove", action="store_true", help="Remove inbox copy after routing.")
    args = parser.parse_args()
    route_events(Path(args.inbox), Path(args.processed), args.remove)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
