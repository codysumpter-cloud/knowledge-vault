#!/usr/bin/env python3
"""Validate BUAP Agent Life events and adapt them to canonical Vegapunk events."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from event_common import load_json_events, slugify, write_jsonl

LIFE_SCHEMA = "prismtek-agent-life-event-v1"
ALLOWED_AUTHORITIES = {"human", "host", "verifier"}
REQUIRED_FIELDS = {
    "schema",
    "event_id",
    "agent_id",
    "occurred_at",
    "kind",
    "subject",
    "reward",
    "confidence",
    "authority",
    "evidence",
    "changes",
    "before_sha256",
    "after_sha256",
    "profile_sha256",
    "claim_boundary",
}


def _timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("occurred_at must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError("occurred_at must include a timezone")
    return parsed.astimezone(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _confidence_label(value: float) -> str:
    if value >= 0.8:
        return "high"
    if value >= 0.5:
        return "medium"
    return "low"


def validate_agent_life_event(event: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(event, dict):
        return ["event must be a JSON object"]
    missing = sorted(REQUIRED_FIELDS - set(event))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if event.get("schema") != LIFE_SCHEMA:
        errors.append("schema must be prismtek-agent-life-event-v1")
    for field in ("event_id", "agent_id", "kind", "before_sha256", "after_sha256", "profile_sha256"):
        if not isinstance(event.get(field), str) or not event.get(field, "").strip():
            errors.append(f"{field} must be a non-empty string")
    try:
        reward = float(event.get("reward"))
        if reward < -1 or reward > 1:
            errors.append("reward must be in -1..1")
    except (TypeError, ValueError):
        errors.append("reward must be numeric")
    try:
        confidence = float(event.get("confidence"))
        if confidence < 0 or confidence > 1:
            errors.append("confidence must be in 0..1")
    except (TypeError, ValueError):
        errors.append("confidence must be numeric")
    try:
        _timestamp(str(event.get("occurred_at", "")))
    except ValueError as exc:
        errors.append(str(exc))
    subject = event.get("subject")
    if not isinstance(subject, dict) or not str(subject.get("type", "")).strip() or not str(subject.get("id", "")).strip():
        errors.append("subject requires type and id")
    authority = event.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority must be an object")
    else:
        if authority.get("kind") not in ALLOWED_AUTHORITIES:
            errors.append("authority.kind is not allowed")
        if not str(authority.get("actor_id", "")).strip():
            errors.append("authority.actor_id is required")
        if str(authority.get("actor_id", "")) == str(event.get("agent_id", "")):
            errors.append("an agent may not reinforce itself")
    evidence = event.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must contain at least one provenance reference")
    elif len(evidence) > 16:
        errors.append("evidence may contain at most 16 references")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict) or not str(item.get("type", "")).strip() or not str(item.get("ref", "")).strip():
                errors.append(f"evidence[{index}] requires type and ref")
    return errors


def canonical_event(raw: dict[str, Any]) -> dict[str, Any]:
    errors = validate_agent_life_event(raw)
    if errors:
        raise ValueError(f"Invalid agent life event {raw.get('event_id')}: {errors}")

    subject = raw["subject"]
    subject_type = slugify(str(subject["type"]))
    subject_id = slugify(str(subject["id"]))
    agent_id = slugify(str(raw["agent_id"]))
    reward = float(raw["reward"])
    confidence = float(raw["confidence"])
    evidence_refs = [str(item["ref"]) for item in raw["evidence"]]
    change_groups = sorted(key for key, value in raw.get("changes", {}).items() if value)
    direction = "preferred" if reward > 0 else "avoided" if reward < 0 else "observed"
    summary = (
        f"Agent {raw['agent_id']} {direction} {subject['type']}:{subject['id']} after "
        f"{raw['kind']} (reward {reward:.2f}, confidence {confidence:.2f})."
    )
    if change_groups:
        summary += f" Changed: {', '.join(change_groups)}."

    return {
        "event_id": f"evt-agent-life-{slugify(str(raw['event_id']))}",
        "event_type": "agent_life_updated",
        "source": "knowledge-vault",
        "timestamp": _timestamp(str(raw["occurred_at"])),
        "payload": {
            "id": f"concept:agent-life-{agent_id}-{subject_type}-{subject_id}",
            "name": f"{raw['agent_id']} preference for {subject['type']}:{subject['id']}",
            "summary": summary,
            "agent_id": str(raw["agent_id"]),
            "target": f"agent:{agent_id}",
            "subject_target": f"{subject_type}:{subject_id}",
            "subject": subject,
            "reward": reward,
            "confidence": _confidence_label(confidence),
            "confidence_score": confidence,
            "authority": raw["authority"],
            "evidence_refs": evidence_refs,
            "changes": raw["changes"],
            "before_sha256": str(raw["before_sha256"]),
            "after_sha256": str(raw["after_sha256"]),
            "profile_sha256": str(raw["profile_sha256"]),
            "claim_boundary": str(raw["claim_boundary"]),
            "tags": ["agent-life", "functional-affect", str(raw["kind"]), subject_type],
        },
    }


def load_life_events(paths: list[Path]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in paths:
        events.extend(load_json_events(path))
    return sorted(events, key=lambda event: (str(event.get("occurred_at", "")), str(event.get("event_id", ""))))


def main() -> int:
    parser = argparse.ArgumentParser(description="Adapt BUAP Agent Life events to canonical Vegapunk events.")
    parser.add_argument("--events", nargs="+", required=True, help="Agent Life JSON/JSONL files or directories.")
    parser.add_argument("--out", required=True, help="Output canonical event JSONL path.")
    args = parser.parse_args()
    canonical = [canonical_event(event) for event in load_life_events([Path(item) for item in args.events])]
    write_jsonl(Path(args.out), canonical)
    print(f"Adapted {len(canonical)} agent life events into {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
