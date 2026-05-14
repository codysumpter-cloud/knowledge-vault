from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path
from typing import Any


def analyze_wav_to_visemes(path: str | Path, cfg: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Create a lightweight mouth timeline from WAV energy.

    The output is intentionally simple and robust for sprite animation. It does
    not attempt full phoneme recognition; it maps short-window audio energy and
    zero-crossing rate into mouth buckets.
    """

    cfg = cfg or {}
    window_ms = int(cfg.get("window_ms", 45))
    window_ms = max(20, min(120, window_ms))

    rate, samples = _read_mono_16bit(Path(path))
    if not samples:
        return [{"t": 0.0, "mouth": "closed", "energy": 0.0}]

    window = max(1, int(rate * (window_ms / 1000.0)))
    frames: list[dict[str, Any]] = []

    rms_values: list[float] = []
    zcr_values: list[float] = []
    starts: list[int] = []

    for start in range(0, len(samples), window):
        chunk = samples[start : start + window]
        if not chunk:
            continue
        rms = math.sqrt(sum(s * s for s in chunk) / len(chunk))
        zcr = _zero_crossing_rate(chunk)
        rms_values.append(rms)
        zcr_values.append(zcr)
        starts.append(start)

    peak = max(rms_values) if rms_values else 0.0
    if peak <= 0.000001:
        return [{"t": 0.0, "mouth": "closed", "energy": 0.0}]

    last_mouth = "closed"
    for start, rms, zcr in zip(starts, rms_values, zcr_values):
        energy = min(1.0, rms / peak)
        mouth = _mouth_for_energy(energy, zcr)

        if cfg.get("smooth", True):
            if mouth == "closed" and last_mouth in {"wide_open", "open"} and energy > 0.08:
                mouth = "small_open"
            if mouth == "wide_open" and last_mouth == "closed":
                mouth = "open"

        frames.append(
            {
                "t": round(start / float(rate), 3),
                "mouth": mouth,
                "energy": round(energy, 3),
            }
        )
        last_mouth = mouth

    if not frames or frames[-1]["mouth"] != "closed":
        frames.append({"t": round(len(samples) / float(rate), 3), "mouth": "closed", "energy": 0.0})

    return frames


def _mouth_for_energy(energy: float, zcr: float) -> str:
    if energy < 0.06:
        return "closed"
    if energy < 0.18:
        return "small_open"
    if energy > 0.74:
        return "wide_open"
    if zcr < 0.075 and energy > 0.32:
        return "round_o"
    if energy > 0.38:
        return "open"
    return "small_open"


def _zero_crossing_rate(samples: list[float]) -> float:
    if len(samples) < 2:
        return 0.0
    changes = 0
    last = samples[0]
    for sample in samples[1:]:
        if (sample >= 0 > last) or (sample < 0 <= last):
            changes += 1
        last = sample
    return changes / float(len(samples) - 1)


def _read_mono_16bit(path: Path) -> tuple[int, list[float]]:
    with wave.open(str(path), "rb") as wf:
        channels = wf.getnchannels()
        width = wf.getsampwidth()
        rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())

    if width != 2:
        raise ValueError("Only 16-bit PCM WAV is supported")

    pcm = array("h")
    pcm.frombytes(frames)
    if pcm.itemsize != 2:
        pcm.byteswap()

    if channels <= 1:
        return rate, [s / 32768.0 for s in pcm]

    mono: list[float] = []
    for i in range(0, len(pcm), channels):
        chunk = pcm[i : i + channels]
        mono.append(sum(chunk) / (32768.0 * len(chunk)))
    return rate, mono
