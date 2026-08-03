#!/usr/bin/env python3
"""Validate local-retrieval reports into truthful, routing-safe evidence receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, cast

MeasurementClass = Literal["contract_baseline", "hardware_measured"]
AccelerationEvidence = Literal["measured", "not_measured", "unsupported"]
EnergyStatus = Literal["measured", "observed", "not_measured"]
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_UNKNOWN = {"", "unknown", "not_measured", "none"}


class EvidenceContractError(ValueError):
    """A run manifest or benchmark report makes an unsupported evidence claim."""


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise EvidenceContractError(f"{field} is required")
    if "\x00" in text:
        raise EvidenceContractError(f"{field} contains a NUL byte")
    return text


def _optional_number(value: Any, field: str) -> float | None:
    if value is None:
        return None
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise EvidenceContractError(f"{field} must be a finite non-negative number")
    return number


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise EvidenceContractError(f"{path}: JSON root must be an object")
    return cast(dict[str, Any], payload), _sha256_bytes(raw)


@dataclass(frozen=True)
class ModelEvidence:
    model_id: str
    model_sha256: str | None
    quantization: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ModelEvidence:
        model_hash = payload.get("model_sha256")
        normalized_hash = None if model_hash is None else _required_text(model_hash, "model.model_sha256")
        if normalized_hash is not None and not _SHA256.fullmatch(normalized_hash):
            raise EvidenceContractError("model.model_sha256 must be a SHA-256 hex digest")
        return cls(
            model_id=_required_text(payload.get("model_id"), "model.model_id"),
            model_sha256=normalized_hash,
            quantization=_required_text(payload.get("quantization"), "model.quantization"),
        )


@dataclass(frozen=True)
class RuntimeEvidence:
    name: str
    version: str
    adapter_version: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> RuntimeEvidence:
        return cls(
            name=_required_text(payload.get("name"), "runtime.name"),
            version=_required_text(payload.get("version"), "runtime.version"),
            adapter_version=_required_text(
                payload.get("adapter_version"), "runtime.adapter_version"
            ),
        )


@dataclass(frozen=True)
class HostEvidence:
    hardware: str
    operating_system: str
    architecture: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> HostEvidence:
        return cls(
            hardware=_required_text(payload.get("hardware"), "host.hardware"),
            operating_system=_required_text(
                payload.get("operating_system"), "host.operating_system"
            ),
            architecture=_required_text(payload.get("architecture"), "host.architecture"),
        )


@dataclass(frozen=True)
class EnergyEvidence:
    status: EnergyStatus
    observation: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> EnergyEvidence:
        status = str(payload.get("status", "not_measured"))
        if status not in {"measured", "observed", "not_measured"}:
            raise EvidenceContractError(f"unsupported energy status: {status}")
        observation = _required_text(payload.get("observation"), "measurements.energy.observation")
        return cls(status=cast(EnergyStatus, status), observation=observation)


@dataclass(frozen=True)
class MeasurementEvidence:
    cold_start_ms: float | None
    warm_latency_ms: float | None
    peak_memory_mb: float | None
    energy: EnergyEvidence

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> MeasurementEvidence:
        energy = payload.get("energy", {})
        if not isinstance(energy, dict):
            raise EvidenceContractError("measurements.energy must be an object")
        return cls(
            cold_start_ms=_optional_number(
                payload.get("cold_start_ms"), "measurements.cold_start_ms"
            ),
            warm_latency_ms=_optional_number(
                payload.get("warm_latency_ms"), "measurements.warm_latency_ms"
            ),
            peak_memory_mb=_optional_number(
                payload.get("peak_memory_mb"), "measurements.peak_memory_mb"
            ),
            energy=EnergyEvidence.from_dict(cast(dict[str, Any], energy)),
        )


@dataclass(frozen=True)
class ClaimEvidence:
    offline_verified: bool
    fallback_behavior: str
    fallback_verified: bool
    native_acceleration: AccelerationEvidence

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ClaimEvidence:
        acceleration = str(payload.get("native_acceleration", "not_measured"))
        if acceleration not in {"measured", "not_measured", "unsupported"}:
            raise EvidenceContractError(f"unsupported native_acceleration value: {acceleration}")
        return cls(
            offline_verified=bool(payload.get("offline_verified", False)),
            fallback_behavior=_required_text(
                payload.get("fallback_behavior"), "claims.fallback_behavior"
            ),
            fallback_verified=bool(payload.get("fallback_verified", False)),
            native_acceleration=cast(AccelerationEvidence, acceleration),
        )


@dataclass(frozen=True)
class RunManifest:
    schema: str
    measurement_class: MeasurementClass
    target: str
    model: ModelEvidence
    runtime: RuntimeEvidence
    host: HostEvidence
    measurements: MeasurementEvidence
    claims: ClaimEvidence
    evidence_refs: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> RunManifest:
        schema = str(payload.get("schema", "buddy.local-retrieval-run.v1"))
        if schema != "buddy.local-retrieval-run.v1":
            raise EvidenceContractError(f"unsupported manifest schema: {schema}")
        measurement_class = str(payload.get("measurement_class", ""))
        if measurement_class not in {"contract_baseline", "hardware_measured"}:
            raise EvidenceContractError(
                "measurement_class must be contract_baseline or hardware_measured"
            )
        nested: dict[str, dict[str, Any]] = {}
        for field in ("model", "runtime", "host", "measurements", "claims"):
            value = payload.get(field)
            if not isinstance(value, dict):
                raise EvidenceContractError(f"{field} must be an object")
            nested[field] = cast(dict[str, Any], value)
        refs_raw = payload.get("evidence_refs", [])
        if not isinstance(refs_raw, list):
            raise EvidenceContractError("evidence_refs must be an array")
        refs = tuple(_required_text(item, "evidence_refs[]") for item in refs_raw)
        if len(set(refs)) != len(refs):
            raise EvidenceContractError("evidence_refs must be unique")
        return cls(
            schema=schema,
            measurement_class=cast(MeasurementClass, measurement_class),
            target=_required_text(payload.get("target"), "target"),
            model=ModelEvidence.from_dict(nested["model"]),
            runtime=RuntimeEvidence.from_dict(nested["runtime"]),
            host=HostEvidence.from_dict(nested["host"]),
            measurements=MeasurementEvidence.from_dict(nested["measurements"]),
            claims=ClaimEvidence.from_dict(nested["claims"]),
            evidence_refs=refs,
        )


def _report_value(report: dict[str, Any], section: str, field: str) -> Any:
    value = report.get(section)
    if not isinstance(value, dict) or field not in value:
        raise EvidenceContractError(f"benchmark report missing {section}.{field}")
    return value[field]


def _is_unknown(value: str) -> bool:
    return value.strip().lower() in _UNKNOWN


def validate_run(report: dict[str, Any], manifest: RunManifest) -> tuple[bool, tuple[str, ...]]:
    adapter_model = str(_report_value(report, "adapter", "model"))
    adapter_runtime = str(_report_value(report, "adapter", "runtime"))
    warm_reported = float(_report_value(report, "metrics", "warm_embed_ms_per_query"))
    recall = float(_report_value(report, "metrics", "recall_at_k"))
    mrr = float(_report_value(report, "metrics", "mrr"))
    if not 0 <= recall <= 1 or not 0 <= mrr <= 1:
        raise EvidenceContractError("benchmark quality metrics must be between 0 and 1")
    if manifest.model.model_id != adapter_model:
        raise EvidenceContractError(
            f"manifest model {manifest.model.model_id!r} does not match report {adapter_model!r}"
        )
    if manifest.runtime.name != adapter_runtime:
        raise EvidenceContractError(
            f"manifest runtime {manifest.runtime.name!r} does not match report {adapter_runtime!r}"
        )
    if manifest.measurements.warm_latency_ms is not None and not math.isclose(
        manifest.measurements.warm_latency_ms,
        warm_reported,
        rel_tol=0.02,
        abs_tol=0.05,
    ):
        raise EvidenceContractError(
            "measurements.warm_latency_ms does not match benchmark report"
        )

    missing: list[str] = []
    if manifest.measurement_class == "contract_baseline":
        if adapter_model != "none":
            raise EvidenceContractError("contract_baseline must use a non-model adapter")
        if manifest.model.model_sha256 is not None:
            raise EvidenceContractError("contract_baseline must not claim a model hash")
        return False, ()

    if adapter_model == "none":
        raise EvidenceContractError("hardware_measured runs require a real model")
    if manifest.model.model_sha256 is None:
        missing.append("model.model_sha256")
    if _is_unknown(manifest.model.quantization):
        missing.append("model.quantization")
    for field, value in (
        ("runtime.version", manifest.runtime.version),
        ("runtime.adapter_version", manifest.runtime.adapter_version),
        ("host.hardware", manifest.host.hardware),
        ("host.operating_system", manifest.host.operating_system),
        ("host.architecture", manifest.host.architecture),
    ):
        if _is_unknown(value):
            missing.append(field)
    for field, value in (
        ("measurements.cold_start_ms", manifest.measurements.cold_start_ms),
        ("measurements.warm_latency_ms", manifest.measurements.warm_latency_ms),
        ("measurements.peak_memory_mb", manifest.measurements.peak_memory_mb),
    ):
        if value is None:
            missing.append(field)
    if manifest.measurements.energy.status == "not_measured":
        missing.append("measurements.energy")
    if not manifest.claims.offline_verified:
        missing.append("claims.offline_verified")
    if not manifest.claims.fallback_verified:
        missing.append("claims.fallback_verified")
    if manifest.claims.native_acceleration == "not_measured":
        missing.append("claims.native_acceleration")
    if not manifest.evidence_refs:
        missing.append("evidence_refs")
    if missing:
        raise EvidenceContractError(
            "hardware_measured run is incomplete: " + ", ".join(missing)
        )
    return True, ()


def build_receipt(
    report: dict[str, Any],
    report_sha256: str,
    manifest: RunManifest,
) -> dict[str, Any]:
    qualified, warnings = validate_run(report, manifest)
    return {
        "schema": "buddy.local-retrieval-evidence.v1",
        "measurement_class": manifest.measurement_class,
        "qualified_for_routing": qualified,
        "target": manifest.target,
        "report_sha256": report_sha256,
        "model": asdict(manifest.model),
        "runtime": asdict(manifest.runtime),
        "host": asdict(manifest.host),
        "measurements": {
            **asdict(manifest.measurements),
            "quality": {
                "recall_at_k": _report_value(report, "metrics", "recall_at_k"),
                "mrr": _report_value(report, "metrics", "mrr"),
                "top_k": _report_value(report, "metrics", "top_k"),
            },
        },
        "claims": asdict(manifest.claims),
        "evidence_refs": list(manifest.evidence_refs),
        "warnings": list(warnings),
        "raw_queries": "excluded",
        "ranked_paths": "excluded",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a local-retrieval report and run manifest."
    )
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-routing-qualified", action="store_true")
    args = parser.parse_args()
    report, report_hash = _load_json(args.report)
    manifest_payload, _manifest_hash = _load_json(args.manifest)
    receipt = build_receipt(report, report_hash, RunManifest.from_dict(manifest_payload))
    if args.require_routing_qualified and not receipt["qualified_for_routing"]:
        raise SystemExit("evidence is valid but not qualified for routing")
    rendered = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
