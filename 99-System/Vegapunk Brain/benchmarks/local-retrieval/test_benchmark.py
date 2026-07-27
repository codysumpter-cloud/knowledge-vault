import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("benchmark.py")
spec = importlib.util.spec_from_file_location("local_retrieval_benchmark", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class LocalRetrievalBenchmarkTests(unittest.TestCase):
    def test_hash_embedding_is_deterministic_and_normalized(self):
        first = module.hash_embedding("Buddy agent receipts", 64)
        second = module.hash_embedding("Buddy agent receipts", 64)
        self.assertEqual(first, second)
        self.assertLess(abs(sum(value * value for value in first) - 1.0), 1e-9)

    def test_public_safe_corpus_excludes_private_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Public\nBuddy runtime", encoding="utf-8")
            private = root / "00-Private"
            private.mkdir()
            (private / "secret.md").write_text("# Secret\nnope", encoding="utf-8")
            chunks = module.build_corpus(root, ["README.md", "00-Private"])
            self.assertEqual(len(chunks), 1)
            self.assertEqual(chunks[0].path, "README.md")

    def test_evaluate_returns_quality_and_runtime_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Buddy Agent\nGuarded execution and receipts", encoding="utf-8"
            )
            chunks = module.build_corpus(root, ["README.md"])
            report = module.evaluate(
                module.HashEmbeddingAdapter(64),
                chunks,
                [module.QueryCase("guarded execution receipts", ("README.md",))],
                1,
            )
            self.assertEqual(report["metrics"]["recall_at_k"], 1.0)
            self.assertTrue(report["targets"]["offline_required"])
            self.assertTrue(report["targets"]["model_download_under_150_mb"])

    def test_baseline_comparison_uses_five_percentage_point_floor(self):
        candidate = {"adapter": {"name": "candidate"}, "metrics": {"recall_at_k": 0.85}}
        baseline = {"adapter": {"name": "cloud"}, "metrics": {"recall_at_k": 0.9}}
        result = module.compare_to_baseline(candidate, baseline)
        self.assertTrue(result["within_5_percent_of_baseline"])


if __name__ == "__main__":
    unittest.main()
