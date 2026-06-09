from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .core import (
    DEFAULT_GRAPH_PATH,
    DEFAULT_INDEX_PATH,
    DEFAULT_OBSIDIAN_INDEX_PATH,
    build_bundle_markdown,
    index_vault,
    load_index,
    read_note,
    records_by_paths,
    search_index,
    write_graph,
    write_index,
    write_json,
    write_obsidian_index,
)


def repo_root() -> Path:
    return Path.cwd().resolve()


def ensure_index(args: argparse.Namespace):
    index_path = Path(args.index)
    if index_path.exists() and not getattr(args, "rebuild", False):
        return load_index(index_path)
    index = index_vault(Path(args.root), vault_name=args.vault, include_private=args.include_private)
    write_index(index, index_path)
    return index


def cmd_index(args: argparse.Namespace) -> int:
    index = index_vault(Path(args.root), vault_name=args.vault, include_private=args.include_private)
    write_index(index, Path(args.index))
    if args.graph:
        write_graph(index, Path(args.graph))
    if args.obsidian:
        write_obsidian_index(index, Path(args.obsidian))
    print(json.dumps({
        "ok": True,
        "index": str(args.index),
        "graph": str(args.graph) if args.graph else None,
        "obsidian": str(args.obsidian) if args.obsidian else None,
        "stats": index.stats,
    }, indent=2))
    return 0


def record_to_result(score: int, record) -> dict[str, object]:
    return {
        "score": score,
        "path": record.path,
        "title": record.title,
        "summary": record.summary,
        "type": record.metadata.get("type"),
        "status": record.metadata.get("status"),
        "tags": record.tags,
        "obsidian_uri": record.obsidian_uri,
        "backlinks": record.backlinks,
        "outgoing_paths": record.outgoing_paths,
    }


def cmd_search(args: argparse.Namespace) -> int:
    index = ensure_index(args)
    results = search_index(index, args.query, limit=args.limit, record_type=args.type, status=args.status, tag=args.tag)
    if args.json:
        print(json.dumps([record_to_result(score, record) for score, record in results], indent=2, ensure_ascii=False))
    else:
        for score, record in results:
            print(f"[{score:03d}] {record.title}")
            print(f"      {record.path}")
            if record.summary:
                print(f"      {record.summary}")
            print(f"      {record.obsidian_uri}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    index = ensure_index(args)
    record = None
    if args.path:
        matches = records_by_paths(index, [args.path])
        record = matches[0] if matches else None
    elif args.query:
        results = search_index(index, args.query, limit=1)
        record = results[0][1] if results else None
    if record is None:
        print("No matching note found.", file=sys.stderr)
        return 1
    if args.json:
        payload = record_to_result(1, record)
        if args.body:
            payload["body"] = read_note(Path(args.root), record)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(read_note(Path(args.root), record))
    return 0


def cmd_bundle(args: argparse.Namespace) -> int:
    index = ensure_index(args)
    selected = []
    if args.path:
        selected.extend(records_by_paths(index, args.path))
    if args.query:
        selected.extend(record for _score, record in search_index(index, args.query, limit=args.limit, record_type=args.type, status=args.status, tag=args.tag))
    deduped = []
    seen = set()
    for record in selected:
        if record.path not in seen:
            deduped.append(record)
            seen.add(record.path)
    if not deduped:
        print("No records selected for bundle.", file=sys.stderr)
        return 1
    title = args.title or "KnowledgeVault Context Bundle"
    purpose = args.purpose or "Curated context exported by memory_engine."
    text = build_bundle_markdown(index, Path(args.root), deduped, title=title, purpose=purpose, max_chars_per_note=args.max_chars_per_note)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    receipt = {
        "bundle": str(output),
        "title": title,
        "purpose": purpose,
        "included_files": [record.path for record in deduped],
        "index_generated_at": index.generated_at,
        "live_sources_checked": [],
        "known_unverified_claims": [
            "This bundle is generated from local vault notes.",
            "Current repo, PR, CI, release, and runtime claims should be verified against their owning sources."
        ],
    }
    if args.receipt:
        write_json(Path(args.receipt), receipt)
    print(json.dumps({"ok": True, "output": str(output), "receipt": str(args.receipt) if args.receipt else None, "files": receipt["included_files"]}, indent=2))
    return 0


def cmd_obsidian(args: argparse.Namespace) -> int:
    index = ensure_index(args)
    write_obsidian_index(index, Path(args.output))
    print(json.dumps({"ok": True, "output": str(args.output), "records": len(index.records)}, indent=2))
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    output = Path(args.path)
    if output.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {output}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    note_type = args.type
    title = args.title or output.stem
    content = f"""---
type: {note_type}
status: draft
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: {args.date}
risk_level: {args.risk}
privacy: public
freshness: slow-changing
agent_load: task-specific
tags: []
---

# {title}

> One-sentence summary.

## Purpose

Why this note exists.

## Current state

Confirmed:

- 

Assumptions:

- 

## Source links

- 

## Known unknowns

- 

## Agent instructions

- Load this note when:
- Verify live before:
- Do not assume:

## Next action

- [ ] 
"""
    output.write_text(content, encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(output)}, indent=2))
    return 0


class MemoryServer(BaseHTTPRequestHandler):
    index = None
    root = Path.cwd()

    def send_json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_text(self, text: str, status: int = 200, content_type: str = "text/plain; charset=utf-8") -> None:
        data = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if parsed.path in {"/", "/health"}:
            self.send_json({"ok": True, "vault": self.index.vault, "generated_at": self.index.generated_at, "stats": self.index.stats})
            return
        if parsed.path == "/search":
            query = params.get("q", [""])[0]
            limit = int(params.get("limit", ["10"])[0])
            results = search_index(self.index, query, limit=limit)
            self.send_json([record_to_result(score, record) for score, record in results])
            return
        if parsed.path == "/record":
            note_path = params.get("path", [""])[0]
            matches = records_by_paths(self.index, [note_path])
            if not matches:
                self.send_json({"error": "record not found"}, status=404)
                return
            record = matches[0]
            self.send_json({**record_to_result(1, record), "body": read_note(self.root, record)})
            return
        if parsed.path == "/bundle":
            query = params.get("q", [""])[0]
            limit = int(params.get("limit", ["8"])[0])
            records = [record for _score, record in search_index(self.index, query, limit=limit)]
            text = build_bundle_markdown(self.index, self.root, records, "Ad hoc Memory Bundle", f"Query: {query}")
            self.send_text(text, content_type="text/markdown; charset=utf-8")
            return
        self.send_json({"error": "not found"}, status=404)

    def log_message(self, fmt: str, *args) -> None:
        return


def cmd_serve(args: argparse.Namespace) -> int:
    index = ensure_index(args)
    MemoryServer.index = index
    MemoryServer.root = Path(args.root)
    server = ThreadingHTTPServer((args.host, args.port), MemoryServer)
    print(f"memory_engine serving {index.vault} at http://{args.host}:{args.port}")
    print("Endpoints: /health, /search?q=term, /record?path=README.md, /bundle?q=agent")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping memory_engine server.")
    finally:
        server.server_close()
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="Vault root. Defaults to current directory.")
    parser.add_argument("--vault", default=None, help="Obsidian vault name. Defaults to root folder name.")
    parser.add_argument("--index", default=str(DEFAULT_INDEX_PATH), help="Memory index JSON path.")
    parser.add_argument("--include-private", action="store_true", help="Include local-only private folder when indexing. Do not use for public exports.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild index before command.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="memory_engine", description="Run KnowledgeVault as a local markdown memory engine.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("index", help="Build JSON graph/index files from markdown notes.")
    add_common(p)
    p.add_argument("--graph", default=str(DEFAULT_GRAPH_PATH), help="Graph JSON output path. Empty string disables.")
    p.add_argument("--obsidian", default=str(DEFAULT_OBSIDIAN_INDEX_PATH), help="Obsidian markdown index path. Empty string disables.")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("search", help="Search indexed notes.")
    add_common(p)
    p.add_argument("query", help="Search query.")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--type", default=None, help="Filter by metadata type.")
    p.add_argument("--status", default=None, help="Filter by metadata status.")
    p.add_argument("--tag", default=None, help="Filter by tag.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("show", help="Show a note by path or top query result.")
    add_common(p)
    p.add_argument("--path", default=None)
    p.add_argument("--query", default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--body", action="store_true", help="Include note body in JSON output.")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("bundle", help="Export a markdown context bundle from paths or search results.")
    add_common(p)
    p.add_argument("--query", default=None)
    p.add_argument("--path", action="append", default=[])
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--type", default=None)
    p.add_argument("--status", default=None)
    p.add_argument("--tag", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--purpose", default=None)
    p.add_argument("--output", default="99-System/Context Bundles/generated.bundle.md")
    p.add_argument("--receipt", default="99-System/Context Bundles/generated.receipt.json")
    p.add_argument("--max-chars-per-note", type=int, default=12000)
    p.set_defaults(func=cmd_bundle)

    p = sub.add_parser("obsidian", help="Generate Obsidian-friendly memory index note.")
    add_common(p)
    p.add_argument("--output", default=str(DEFAULT_OBSIDIAN_INDEX_PATH))
    p.set_defaults(func=cmd_obsidian)

    p = sub.add_parser("new", help="Create a new note from the standard memory template.")
    p.add_argument("path", help="New note path.")
    p.add_argument("--title", default=None)
    p.add_argument("--type", default="project")
    p.add_argument("--date", default="YYYY-MM-DD")
    p.add_argument("--risk", default="medium")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("serve", help="Run a local read-only HTTP API for humans and agents.")
    add_common(p)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "graph") and args.graph == "":
        args.graph = None
    if hasattr(args, "obsidian") and args.obsidian == "":
        args.obsidian = None
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
