from __future__ import annotations

import json
import os
import textwrap
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class ResponseEngine:
    config: dict[str, Any]

    def respond(self, text: str, author: str | None = None) -> str:
        text = self._sanitize_user_text(text)
        mode = str(self.config.get("engine", {}).get("mode", "template")).lower()

        if mode == "omni":
            try:
                response = self._respond_omni(text, author=author)
                if response:
                    return self._trim_response(response)
            except Exception as exc:
                print(f"[response-engine] Omni failed, falling back to template: {exc}", flush=True)

        return self._respond_template(text, author=author)

    def _respond_template(self, text: str, author: str | None = None) -> str:
        lower = text.lower()
        who = f"{author}, " if author else ""

        if "hello" in lower or "hi" in lower or "hey" in lower:
            return f"Hi {who}friend! I am Buddy, and I am ready to help."

        if "explain" in lower or "what is" in lower or "how do" in lower:
            return self._trim_response(
                f"{who}tiny summary: {textwrap.shorten(text, width=90, placeholder='...')} "
                "sounds like a good explainer topic. I would break it into one clear idea, one example, and one takeaway."
            )

        if "youtube" in lower or "video" in lower:
            return f"{who}I can host this video with a clean overlay, generated voice, and mouth animation synced to my audio."

        return self._trim_response(
            f"{who}good question. I would keep it simple: {textwrap.shorten(text, width=120, placeholder='...')} "
            "needs a clear answer, then a small next step."
        )

    def _respond_omni(self, text: str, author: str | None = None) -> str:
        omni = self.config.get("omni", {})
        engine = self.config.get("engine", {})

        base_url = str(omni.get("base_url", "")).rstrip("/")
        if not base_url:
            raise ValueError("omni.base_url is empty")

        token_env = str(omni.get("token_env", "PRISMBOT_API_TOKEN"))
        token = os.getenv(token_env, "")
        timeout = float(omni.get("timeout_sec", 60))
        model = str(omni.get("model", "omni-core:phase2"))
        system_prompt = str(engine.get("system_prompt", ""))

        user_content = text if not author else f"{author} says: {text}"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "stream": False,
        }

        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = urllib.request.Request(base_url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Omni HTTP {exc.code}: {detail[:240]}") from exc

        return self._extract_text(data)

    def _extract_text(self, data: Any) -> str:
        if isinstance(data, str):
            return data

        if not isinstance(data, dict):
            return ""

        for key in ("text", "message", "response", "content"):
            value = data.get(key)
            if isinstance(value, str):
                return value

        result = data.get("result")
        if isinstance(result, dict):
            text = self._extract_text(result)
            if text:
                return text

        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                msg = first.get("message")
                if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                    return msg["content"]
                if isinstance(first.get("text"), str):
                    return first["text"]

        return ""

    def _sanitize_user_text(self, text: str) -> str:
        cleaned = " ".join(str(text or "").split())
        return cleaned[:1000]

    def _trim_response(self, text: str) -> str:
        max_chars = int(self.config.get("engine", {}).get("max_response_chars", 420))
        text = " ".join(str(text or "").split())
        if len(text) <= max_chars:
            return text
        return text[: max(0, max_chars - 1)].rstrip() + "…"
