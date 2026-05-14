from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class ChatMessage:
    source: str
    author: str
    text: str
    message_id: str
    timestamp: float


@dataclass
class YouTubeChatAdapter:
    video_id: str
    on_message: Callable[[ChatMessage], None]
    poll_interval_sec: float = 1.0
    max_message_chars: int = 240
    ignore_prefixes: list[str] = field(default_factory=lambda: ["!", "/"])
    blocked_terms: list[str] = field(default_factory=list)

    _thread: threading.Thread | None = None
    _stop: threading.Event = field(default_factory=threading.Event)
    _seen: set[str] = field(default_factory=set)

    def start(self) -> None:
        if not self.video_id:
            print("[youtube-chat] no video_id configured; chat adapter disabled", flush=True)
            return

        if self._thread and self._thread.is_alive():
            return

        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="youtube-chat", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        try:
            import pytchat  # type: ignore
        except Exception as exc:
            print(f"[youtube-chat] pytchat unavailable: {exc}", flush=True)
            return

        print(f"[youtube-chat] connecting to video_id={self.video_id}", flush=True)
        chat = pytchat.create(video_id=self.video_id)

        while not self._stop.is_set() and chat.is_alive():
            try:
                for item in chat.get().sync_items():
                    message_id = str(getattr(item, "id", "")) or (
                        f"{getattr(item, 'author', '')}:"
                        f"{getattr(item, 'datetime', '')}:"
                        f"{getattr(item, 'message', '')}"
                    )
                    if message_id in self._seen:
                        continue
                    self._seen.add(message_id)

                    author = str(getattr(item, "author", "") or "viewer")
                    text = str(getattr(item, "message", "") or "")

                    if not self._is_allowed(text):
                        continue

                    self.on_message(
                        ChatMessage(
                            source="youtube",
                            author=author,
                            text=text[: self.max_message_chars],
                            message_id=message_id,
                            timestamp=time.time(),
                        )
                    )
            except Exception as exc:
                print(f"[youtube-chat] poll error: {exc}", flush=True)

            time.sleep(max(0.25, self.poll_interval_sec))

        print("[youtube-chat] stopped", flush=True)

    def _is_allowed(self, text: str) -> bool:
        clean = " ".join(str(text or "").split())
        if not clean:
            return False

        if any(clean.startswith(prefix) for prefix in self.ignore_prefixes):
            return False

        lowered = clean.lower()
        if any(term.lower() in lowered for term in self.blocked_terms):
            return False

        # Drop obvious repeated-character spam.
        if re.search(r"(.)\1{12,}", clean):
            return False

        return True
