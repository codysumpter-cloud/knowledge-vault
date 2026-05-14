from __future__ import annotations

import json
import queue
import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EventBus:
    """Small in-process fanout bus for Server-Sent Events clients."""

    history_limit: int = 80
    _subscribers: list[queue.Queue[dict[str, Any]]] = field(default_factory=list)
    _history: list[dict[str, Any]] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def publish(self, event_type: str, **payload: Any) -> dict[str, Any]:
        event = {
            "type": event_type,
            "ts": time.time(),
            **payload,
        }

        with self._lock:
            self._history.append(event)
            if len(self._history) > self.history_limit:
                self._history = self._history[-self.history_limit:]

            dead: list[queue.Queue[dict[str, Any]]] = []
            for subscriber in self._subscribers:
                try:
                    subscriber.put_nowait(event)
                except queue.Full:
                    dead.append(subscriber)

            for subscriber in dead:
                try:
                    self._subscribers.remove(subscriber)
                except ValueError:
                    pass

        return event

    def subscribe(self) -> queue.Queue[dict[str, Any]]:
        q: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=200)
        with self._lock:
            self._subscribers.append(q)
            for event in self._history[-10:]:
                q.put_nowait(event)
        return q

    def unsubscribe(self, q: queue.Queue[dict[str, Any]]) -> None:
        with self._lock:
            try:
                self._subscribers.remove(q)
            except ValueError:
                pass


def encode_sse(event: dict[str, Any]) -> bytes:
    event_type = str(event.get("type", "message"))
    data = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    return f"event: {event_type}\ndata: {data}\n\n".encode("utf-8")
