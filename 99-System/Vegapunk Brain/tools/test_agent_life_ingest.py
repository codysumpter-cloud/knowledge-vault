#!/usr/bin/env python3

from __future__ import annotations

import unittest

from agent_life_ingest import canonical_event, validate_agent_life_event
from graph_compiler import record_from_event


def sample_event(**overrides):
    event = {
        "schema": "prismtek-agent-life-event-v1",
        "event_id": "ci-run-123",
        "agent_id": "buddy-cody",
        "occurred_at": "2026-07-30T12:00:00.250Z",
        "kind": "task_succeeded",
        "subject": {"type": "tool", "id": "github-actions"},
        "reward": 0.8,
        "confidence": 0.95,
        "authority": {"kind": "verifier", "actor_id": "ci"},
        "evidence": [{"type": "receipt", "ref": "run-123"}],
        "changes": {
            "preferences": {"tool:github-actions": {"before": 0.0, "after": 0.16}},
            "traits": {"thoroughness": {"before": 0.6, "after": 0.61}},
        },
        "before_sha256": "before-hash",
        "after_sha256": "after-hash",
        "profile_sha256": "profile-hash",
        "claim_boundary": "Functional affect changed; consciousness is not established.",
    }
    event.update(overrides)
    return event


class AgentLifeIngestTests(unittest.TestCase):
    def test_valid_event_adapts_to_canonical_bus(self):
        raw = sample_event()
        self.assertEqual(validate_agent_life_event(raw), [])
        adapted = canonical_event(raw)
        self.assertEqual(adapted["event_type"], "agent_life_updated")
        self.assertEqual(adapted["timestamp"], "2026-07-30T12:00:00Z")
        self.assertEqual(adapted["payload"]["target"], "agent:buddy-cody")
        self.assertEqual(adapted["payload"]["subject_target"], "tool:github-actions")
        self.assertEqual(adapted["payload"]["evidence_refs"], ["run-123"])

    def test_graph_record_links_agent_and_subject(self):
        record = record_from_event(canonical_event(sample_event()))
        targets = {link["target"] for link in record["links"]}
        self.assertIn("agent:buddy-cody", targets)
        self.assertIn("tool:github-actions", targets)
        self.assertIn("agent-life", record["tags"])
        self.assertEqual(record["provenance"]["confidence"], "high")

    def test_rejects_self_reinforcement(self):
        errors = validate_agent_life_event(sample_event(
            authority={"kind": "host", "actor_id": "buddy-cody"},
        ))
        self.assertIn("an agent may not reinforce itself", errors)

    def test_rejects_unprovenanced_or_unbounded_events(self):
        errors = validate_agent_life_event(sample_event(evidence=[], reward=2.0, confidence=-1.0))
        self.assertIn("evidence must contain at least one provenance reference", errors)
        self.assertIn("reward must be in -1..1", errors)
        self.assertIn("confidence must be in 0..1", errors)


if __name__ == "__main__":
    unittest.main()
