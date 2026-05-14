from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "host": {
        "name": "Buddy",
        "bind": "127.0.0.1",
        "port": 8765,
        "public_base_url": "http://127.0.0.1:8765",
    },
    "engine": {
        "mode": "template",
        "max_response_chars": 420,
        "system_prompt": (
            "You are Buddy, a compact, friendly talking host. Keep replies short, "
            "curious, helpful, and warm. Do not claim to be a copyrighted character "
            "or an official character voice."
        ),
    },
    "omni": {
        "base_url": "http://127.0.0.1:8799/api/omni",
        "token_env": "PRISMBOT_API_TOKEN",
        "model": "omni-core:phase2",
        "timeout_sec": 60,
    },
    "tts": {
        "enabled": True,
        "piper_binary": "piper/piper",
        "voice_model": "piper/en_GB-semaine-medium.onnx",
        "output_dir": "generated/audio",
        "voice_profile": "bright_toy_robot",
        "voice_shape_enabled": True,
        "speed": 1.11,
        "pitch_shift_steps": 2.0,
        "gain_db": 1.5,
        "bitcrush_bits": 12,
        "vibrato_hz": 5.2,
        "vibrato_depth": 0.006,
    },
    "visemes": {
        "window_ms": 45,
        "smooth": True,
    },
    "youtube": {
        "enabled": False,
        "video_id": "",
        "poll_interval_sec": 1.0,
        "min_seconds_between_replies": 7.5,
        "max_message_chars": 240,
        "ignore_prefixes": ["!", "/"],
        "blocked_terms": [],
    },
    "overlay": {
        "scale": 1.0,
        "anchor": "bottom-right",
    },
}


def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    if not path:
        return copy.deepcopy(DEFAULT_CONFIG)

    cfg_path = Path(path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)

    if not isinstance(loaded, dict):
        raise ValueError("Config root must be a JSON object")

    return _deep_merge(DEFAULT_CONFIG, loaded)


def resolve_path(value: str | Path, base_dir: str | Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return Path(base_dir).resolve() / path
