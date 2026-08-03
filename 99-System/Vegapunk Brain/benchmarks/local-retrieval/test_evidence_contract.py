import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("evidence_contract.py")
spec = importlib.util.spec_from_file_location("local_retrieval_evidence", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def report(model="none", runtime="python"):
    return {
        "version": 1,
        "adapter": {
            "name": "adapter",
            "runtime": runtime,
            "model": model,
        },
        "metrics": {
            "recall_at_k": 0.9,
            "mrr": 0.8,
            "top_k": 5,
            "warm_embed_ms_per_query": 12.5,
        },
        "details": [{"query": "private-like query", "results": [{"path": "README.md"}]}],
    }


def manifest(measurement_class="contract_baseline", model="none", runtime="python"):
    return {
        "schema": "buddy.local-retrieval-run.v1",
        "measurement_class": measurement_class,
        "target": "ci-contract",
        "model": {
            "model_id": model,
            "model_sha256": None,
            "quantization": "none" if model == "none" else "unknown",
        },
        "runtime": {
            "name": runtime,
            "version": "3.12",
            "adapter_version": "v1",
        },
        "host": {
            "hardware": "github-hosted-runner",
            "operating_system": "ubuntu-24.04",
            "architecture": "x86_64",
        },
        "measurements": {
            "cold_start_ms": None,
            "warm_latency_ms": 12.5,
            "peak_memory_mb": None,
            "energy": {
                "status": "not_measured",
                "observation": "CI contract run; energy was not measured.",
            },
        },
        "claims": {
            "offline_verified": True,
            "fallback_behavior": "contract-only",
            "fallback_verified": False,
            "native_acceleration": "not_measured",
        },
        "evidence_refs": [],
    }


class LocalRetrievalEvidenceTests(unittest.TestCase):
    def test_contract_baseline_is_valid_but_never_routing_qualified(self):
        run = module.RunManifest.from_dict(manifest())
        receipt = module.build_receipt(report(), "a" * 64, run)
        self.assertFalse(receipt["qualified_for_routing"])
        self.assertEqual(receipt["measurement_class"], "contract_baseline")
        self.assertEqual(receipt["raw_queries"], "excluded")
        self.assertEqual(receipt["ranked_paths"], "excluded")
        self.assertNotIn("private-like query", json.dumps(receipt))
        self.assertNotIn("README.md", json.dumps(receipt))

    def test_contract_baseline_cannot_claim_a_real_model_or_hash(self):
        bad_model = manifest(model="embedding-model")
        bad_model["model"]["model_sha256"] = "a" * 64
        with self.assertRaisesRegex(module.EvidenceContractError, "non-model adapter"):
            module.build_receipt(
                report(model="embedding-model"),
                "b" * 64,
                module.RunManifest.from_dict(bad_model),
            )

        bad_hash = manifest()
        bad_hash["model"]["model_sha256"] = "a" * 64
        with self.assertRaisesRegex(module.EvidenceContractError, "must not claim a model hash"):
            module.build_receipt(
                report(),
                "b" * 64,
                module.RunManifest.from_dict(bad_hash),
            )

    def test_hardware_measured_run_requires_complete_evidence(self):
        incomplete = manifest("hardware_measured", model="embedding-model", runtime="litert")
        with self.assertRaisesRegex(module.EvidenceContractError, "hardware_measured run is incomplete"):
            module.build_receipt(
                report(model="embedding-model", runtime="litert"),
                "c" * 64,
                module.RunManifest.from_dict(incomplete),
            )

    def test_complete_hardware_run_is_routing_qualified(self):
        measured = manifest("hardware_measured", model="embedding-model", runtime="litert")
        measured["target"] = "m5-mac"
        measured["model"] = {
            "model_id": "embedding-model",
            "model_sha256": "d" * 64,
            "quantization": "int8",
        }
        measured["runtime"] = {
            "name": "litert",
            "version": "2.0.1",
            "adapter_version": "knowledge-vault-litert-v1",
        }
        measured["host"] = {
            "hardware": "Apple M5",
            "operating_system": "macOS 27.0",
            "architecture": "arm64",
        }
        measured["measurements"] = {
            "cold_start_ms": 210.0,
            "warm_latency_ms": 12.5,
            "peak_memory_mb": 180.0,
            "energy": {
                "status": "observed",
                "observation": "Battery discharge remained stable across the fixed query suite.",
            },
        }
        measured["claims"] = {
            "offline_verified": True,
            "fallback_behavior": "WebGPU unavailable then WASM completed the same suite",
            "fallback_verified": True,
            "native_acceleration": "measured",
        }
        measured["evidence_refs"] = [
            "artifact://benchmark-report",
            "artifact://runtime-log",
        ]
        receipt = module.build_receipt(
            report(model="embedding-model", runtime="litert"),
            "e" * 64,
            module.RunManifest.from_dict(measured),
        )
        self.assertTrue(receipt["qualified_for_routing"])
        self.assertEqual(receipt["model"]["model_sha256"], "d" * 64)
        self.assertEqual(receipt["measurements"]["quality"]["recall_at_k"], 0.9)

    def test_manifest_must_match_report_model_runtime_and_warm_latency(self):
        mismatch = manifest()
        mismatch["runtime"]["name"] = "different-runtime"
        with self.assertRaisesRegex(module.EvidenceContractError, "does not match report"):
            module.build_receipt(
                report(),
                "f" * 64,
                module.RunManifest.from_dict(mismatch),
            )

        latency = manifest()
        latency["measurements"]["warm_latency_ms"] = 99.0
        with self.assertRaisesRegex(module.EvidenceContractError, "warm_latency_ms"):
            module.build_receipt(
                report(),
                "f" * 64,
                module.RunManifest.from_dict(latency),
            )

    def test_cli_receipt_hashes_exact_report_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report_path = root / "report.json"
            manifest_path = root / "manifest.json"
            report_path.write_text(json.dumps(report(), indent=2) + "\n", encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest(), indent=2) + "\n", encoding="utf-8")
            loaded_report, digest = module._load_json(report_path)
            loaded_manifest, _ = module._load_json(manifest_path)
            receipt = module.build_receipt(
                loaded_report,
                digest,
                module.RunManifest.from_dict(loaded_manifest),
            )
            self.assertEqual(receipt["report_sha256"], digest)
            self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
