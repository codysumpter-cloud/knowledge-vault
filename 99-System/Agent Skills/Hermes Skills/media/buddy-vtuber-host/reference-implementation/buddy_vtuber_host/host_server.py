from __future__ import annotations

import argparse
import json
import mimetypes
import queue
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .adapters.response_engine import ResponseEngine
from .adapters.youtube_chat import ChatMessage, YouTubeChatAdapter
from .config import load_config
from .event_bus import EventBus, encode_sse
from .tts.piper_engine import PiperEngine
from .tts.viseme_from_audio import analyze_wav_to_visemes


class BuddyRuntime:
    def __init__(self, config: dict[str, Any], base_dir: str | Path):
        self.config = config
        self.base_dir = Path(base_dir).resolve()
        self.bus = EventBus()
        self.response_engine = ResponseEngine(config)
        self.tts = PiperEngine(config, self.base_dir)
        self.jobs: queue.Queue[dict[str, Any]] = queue.Queue()
        self.worker = threading.Thread(target=self._worker_loop, name="buddy-worker", daemon=True)
        self.worker.start()
        self.last_youtube_reply = 0.0
        self.youtube_adapter: YouTubeChatAdapter | None = None

    def start_youtube_if_enabled(self, override_video_id: str | None = None) -> None:
        yt = self.config.get("youtube", {})
        video_id = override_video_id or str(yt.get("video_id", "")).strip()
        enabled = bool(yt.get("enabled", False) or override_video_id)

        if not enabled or not video_id:
            return

        self.youtube_adapter = YouTubeChatAdapter(
            video_id=video_id,
            on_message=self._handle_youtube_message,
            poll_interval_sec=float(yt.get("poll_interval_sec", 1.0)),
            max_message_chars=int(yt.get("max_message_chars", 240)),
            ignore_prefixes=list(yt.get("ignore_prefixes", ["!", "/"])),
            blocked_terms=list(yt.get("blocked_terms", [])),
        )
        self.youtube_adapter.start()

    def enqueue_say(self, text: str, author: str | None = None, source: str = "manual") -> None:
        self.jobs.put({"kind": "say", "text": text, "author": author, "source": source})

    def enqueue_respond(self, text: str, author: str | None = None, source: str = "manual") -> None:
        self.jobs.put({"kind": "respond", "text": text, "author": author, "source": source})

    def _handle_youtube_message(self, msg: ChatMessage) -> None:
        yt = self.config.get("youtube", {})
        cooldown = float(yt.get("min_seconds_between_replies", 7.5))
        now = time.time()
        if now - self.last_youtube_reply < cooldown:
            return
        self.last_youtube_reply = now

        self.bus.publish(
            "chat",
            source=msg.source,
            author=msg.author,
            text=msg.text,
            message_id=msg.message_id,
        )
        self.enqueue_respond(msg.text, author=msg.author, source="youtube")

    def _worker_loop(self) -> None:
        self.bus.publish("state", state="idle")
        while True:
            job = self.jobs.get()
            try:
                kind = job.get("kind")
                text = str(job.get("text", ""))
                author = job.get("author")
                source = str(job.get("source", "manual"))

                if kind == "respond":
                    self.bus.publish("state", state="thinking", source=source)
                    text = self.response_engine.respond(text, author=author)
                elif kind != "say":
                    continue

                self._speak(text, source=source)
            except Exception as exc:
                self.bus.publish("error", message=str(exc))
                self.bus.publish("state", state="idle")
                print(f"[runtime] job failed: {exc}", flush=True)
            finally:
                self.jobs.task_done()

    def _speak(self, text: str, source: str = "manual") -> None:
        self.bus.publish("state", state="speaking", source=source)
        audio_path = self.tts.synthesize(text)

        audio_url = None
        visemes: list[dict[str, Any]] = [{"t": 0.0, "mouth": "smile", "energy": 0.1}]
        if audio_path and audio_path.exists():
            visemes = analyze_wav_to_visemes(audio_path, self.config.get("visemes", {}))
            try:
                rel = audio_path.resolve().relative_to(self.base_dir)
                audio_url = "/" + rel.as_posix()
            except ValueError:
                audio_url = f"/audio/{audio_path.name}"

        self.bus.publish(
            "speech",
            text=text,
            audio_url=audio_url,
            visemes=visemes,
            source=source,
        )
        self.bus.publish("state", state="idle", source=source)


def make_handler(runtime: BuddyRuntime):
    base_dir = runtime.base_dir
    web_dir = Path(__file__).resolve().parent / "web"

    class Handler(BaseHTTPRequestHandler):
        server_version = "BuddyVTuberHost/0.1"

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            path = parsed.path

            if path == "/events":
                self._handle_events()
                return

            if path == "/health":
                self._send_json({"ok": True, "name": runtime.config.get("host", {}).get("name", "Buddy")})
                return

            if path in {"/", "/overlay.html"}:
                self._send_file(web_dir / "overlay.html", "text/html; charset=utf-8")
                return

            if path in {"/overlay.js", "/overlay.css"}:
                content_type = "application/javascript; charset=utf-8" if path.endswith(".js") else "text/css; charset=utf-8"
                self._send_file(web_dir / path.strip("/"), content_type)
                return

            if path.startswith("/generated/audio/"):
                self._send_file(base_dir / path.strip("/"))
                return

            if path.startswith("/audio/"):
                audio_dir = Path(runtime.tts.output_dir)
                self._send_file(audio_dir / Path(path).name)
                return

            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path not in {"/api/say", "/api/respond"}:
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
                return

            try:
                payload = self._read_json()
                text = str(payload.get("text", "")).strip()
                author = payload.get("author")
                if not text:
                    self._send_json({"ok": False, "error": "Missing text"}, status=400)
                    return

                if parsed.path == "/api/respond":
                    runtime.enqueue_respond(text, author=author, source="api")
                else:
                    runtime.enqueue_say(text, author=author, source="api")

                self._send_json({"ok": True, "queued": True})
            except Exception as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=500)

        def _handle_events(self) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            subscriber = runtime.bus.subscribe()
            try:
                self.wfile.write(encode_sse({"type": "hello", "ts": time.time()}))
                self.wfile.flush()
                while True:
                    try:
                        event = subscriber.get(timeout=15)
                        self.wfile.write(encode_sse(event))
                    except queue.Empty:
                        self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                runtime.bus.unsubscribe(subscriber)

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("content-length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            if not raw:
                return {}
            return json.loads(raw.decode("utf-8"))

        def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_file(self, path: Path, content_type: str | None = None) -> None:
            if not path.exists() or not path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return

            body = path.read_bytes()
            guessed = content_type or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", guessed)
            self.send_header("Content-Length", str(len(body)))
            if path.suffix.lower() == ".wav":
                self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt: str, *args: Any) -> None:
            print(f"[http] {self.address_string()} - {fmt % args}", flush=True)

    return Handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Buddy VTuber Host reference server")
    parser.add_argument("--config", default="config.example.json", help="Path to config JSON")
    parser.add_argument("--bind", default=None, help="Override bind address")
    parser.add_argument("--port", type=int, default=None, help="Override port")
    parser.add_argument("--youtube", default=None, help="Enable YouTube chat adapter with this video ID")
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    base_dir = config_path.parent

    bind = args.bind or str(config.get("host", {}).get("bind", "127.0.0.1"))
    port = int(args.port or config.get("host", {}).get("port", 8765))

    runtime = BuddyRuntime(config=config, base_dir=base_dir)
    runtime.start_youtube_if_enabled(override_video_id=args.youtube)

    handler = make_handler(runtime)
    httpd = ThreadingHTTPServer((bind, port), handler)

    print(f"[buddy-host] serving overlay at http://{bind}:{port}/overlay.html", flush=True)
    print("[buddy-host] POST /api/say or /api/respond to make Buddy talk", flush=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[buddy-host] shutting down", flush=True)
    finally:
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
