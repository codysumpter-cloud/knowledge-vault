from __future__ import annotations

import unittest

from drift_benchmark import generate_corpus, run_benchmark


class RetrievalDriftBenchmarkTests(unittest.TestCase):
    def test_generates_requested_scale(self) -> None:
        records, entities = generate_corpus(10_240, 128)
        self.assertEqual(len(records), 10_240)
        self.assertEqual(len(entities), 128)
        self.assertTrue(all(record.content_hash for record in records))

    def test_provenance_rerank_suppresses_stale_near_misses(self) -> None:
        report = run_benchmark(10_240, 128)
        baseline = report["baseline_similarity_only"]
        provenance = report["provenance_graph_rerank"]
        self.assertGreaterEqual(baseline["false_current_rate"], 0.90)
        self.assertEqual(provenance["current_top1_rate"], 1.0)
        self.assertEqual(provenance["stale_top1_rate"], 0.0)
        self.assertEqual(provenance["near_miss_top1_rate"], 0.0)
        self.assertEqual(provenance["conflict_detection_recall"], 1.0)
        self.assertEqual(provenance["lineage_coverage"], 1.0)


if __name__ == "__main__":
    unittest.main()
