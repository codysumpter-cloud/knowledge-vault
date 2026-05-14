from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path
from typing import Any


def apply_bright_toy_robot_profile(path: str | Path, cfg: dict[str, Any]) -> None:
    """Post-process a Piper WAV into an original bright toy-robot profile.

    This is intentionally a generic synthetic voice profile. Do not present it
    as a clone of any character or actor voice.
    """

    wav_path = Path(path)
    if not wav_path.exists():
        return

    rate, samples = _read_mono_16bit(wav_path)
    if not samples:
        return

    samples = _remove_dc(samples)
    samples = _normalize(samples, target=0.82)

    speed = _clamp(float(cfg.get("speed", 1.11)), 0.85, 1.35)
    if abs(speed - 1.0) > 0.01:
        samples = _resample(samples, max(32, int(len(samples) / speed)))

    semis = _clamp(float(cfg.get("pitch_shift_steps", 2.0)), -4.0, 5.0)
    pitch_factor = 2 ** (semis / 12.0)
    if abs(pitch_factor - 1.0) > 0.01:
        lifted = _resample(samples, max(32, int(len(samples) / pitch_factor)))
        samples = _resample(lifted, len(samples))

    vibrato_hz = float(cfg.get("vibrato_hz", 5.2))
    vibrato_depth = max(0.0, float(cfg.get("vibrato_depth", 0.006)))
    if vibrato_depth:
        samples = [
            sample * (1.0 + vibrato_depth * math.sin(2.0 * math.pi * vibrato_hz * i / rate))
            for i, sample in enumerate(samples)
        ]

    bits = int(_clamp(int(cfg.get("bitcrush_bits", 12)), 8, 16))
    if bits < 16:
        levels = float(2 ** (bits - 1))
        samples = [round(sample * levels) / levels for sample in samples]

    gain_db = float(cfg.get("gain_db", 1.5))
    gain = 10 ** (gain_db / 20.0)
    samples = [sample * gain for sample in samples]

    fade = min(len(samples) // 8, int(rate * 0.012))
    if fade > 2:
        for i in range(fade):
            amount = i / float(fade)
            samples[i] *= amount
            samples[-i - 1] *= amount

    samples = _normalize(samples, target=0.95, only_if_hot=True)
    _write_mono_16bit(wav_path, rate, samples)


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


def _write_mono_16bit(path: Path, rate: int, samples: list[float]) -> None:
    pcm = array("h", [int(max(-0.98, min(0.98, s)) * 32767.0) for s in samples])
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(pcm.tobytes())


def _resample(samples: list[float], target_len: int) -> list[float]:
    if target_len <= 0 or not samples:
        return []
    if target_len == len(samples):
        return list(samples)
    if target_len == 1:
        return [samples[0]]

    result: list[float] = []
    scale = (len(samples) - 1) / float(target_len - 1)
    for i in range(target_len):
        pos = i * scale
        left = int(pos)
        right = min(left + 1, len(samples) - 1)
        frac = pos - left
        result.append(samples[left] * (1.0 - frac) + samples[right] * frac)
    return result


def _remove_dc(samples: list[float]) -> list[float]:
    mean = sum(samples) / float(len(samples))
    return [s - mean for s in samples]


def _normalize(samples: list[float], target: float, only_if_hot: bool = False) -> list[float]:
    peak = max(abs(s) for s in samples) if samples else 0.0
    if peak <= 0.000001:
        return samples
    if only_if_hot and peak <= target:
        return samples
    scale = target / peak
    return [s * scale for s in samples]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
