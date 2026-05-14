from __future__ import annotations

import hashlib
import math
import subprocess
import time
import wave
from array import array
from pathlib import Path
from typing import Any

from .buddy_voice_profile import apply_bright_toy_robot_profile


class PiperEngine:
    def __init__(self, config: dict[str, Any], base_dir: str | Path):
        self.config = config
        self.base_dir = Path(base_dir).resolve()
        self.tts_config = config.get("tts", {})
        self.output_dir = self._resolve(self.tts_config.get("output_dir", "generated/audio"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def synthesize(self, text: str) -> Path | None:
        if not self.tts_config.get("enabled", True):
            return None

        text = " ".join(str(text or "").split())
        if not text:
            return None

        filename = self._safe_audio_name(text)
        output_path = self.output_dir / filename

        piper_binary = self._resolve(self.tts_config.get("piper_binary", "piper/piper"))
        voice_model = self._resolve(self.tts_config.get("voice_model", ""))

        if piper_binary.exists() and voice_model.exists():
            self._run_piper(piper_binary, voice_model, output_path, text)
        else:
            print("[tts] Piper binary or voice model missing; generating dev placeholder WAV", flush=True)
            self._write_placeholder_voice(output_path, text)

        if self.tts_config.get("voice_shape_enabled", True):
            if str(self.tts_config.get("voice_profile", "bright_toy_robot")) == "bright_toy_robot":
                apply_bright_toy_robot_profile(output_path, self.tts_config)

        return output_path

    def _run_piper(self, piper_binary: Path, voice_model: Path, output_path: Path, text: str) -> None:
        cmd = [
            str(piper_binary),
            "--model",
            str(voice_model),
            "--output_file",
            str(output_path),
        ]

        proc = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if proc.returncode != 0:
            detail = proc.stderr.decode("utf-8", errors="replace")[:400]
            raise RuntimeError(f"Piper failed with exit code {proc.returncode}: {detail}")

    def _write_placeholder_voice(self, output_path: Path, text: str) -> None:
        # Development fallback: short friendly blips roughly proportional to text length.
        rate = 22050
        duration = min(6.0, max(0.8, len(text) / 42.0))
        total = int(rate * duration)
        samples = array("h")

        for i in range(total):
            t = i / float(rate)
            word_gate = 0.5 + 0.5 * math.sin(2.0 * math.pi * 4.4 * t)
            amp = 0.22 * (0.45 + 0.55 * word_gate)
            freq = 430.0 + 70.0 * math.sin(2.0 * math.pi * 2.2 * t)
            sample = amp * math.sin(2.0 * math.pi * freq * t)
            samples.append(int(sample * 32767.0))

        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(rate)
            wf.writeframes(samples.tobytes())

    def _safe_audio_name(self, text: str) -> str:
        digest = hashlib.sha1(f"{time.time()}:{text}".encode("utf-8")).hexdigest()[:16]
        return f"buddy_{digest}.wav"

    def _resolve(self, value: Any) -> Path:
        path = Path(str(value)).expanduser()
        if path.is_absolute():
            return path
        return self.base_dir / path
