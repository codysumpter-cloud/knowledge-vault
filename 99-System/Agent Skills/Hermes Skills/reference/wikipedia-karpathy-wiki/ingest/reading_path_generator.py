#!/usr/bin/env python3
"""Generate reading paths from local Wikipedia Knowledge Engine indexes."""
from __future__ import annotations

import argparse
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def resolve_slug(query: str, concepts: dict[str, Any], aliases: dict[str, str]) -> str | None:
    key = query.strip().lower()
    if key in concepts:
        return key
    if key in aliases:
        return aliases[key]
    for slug, item in concepts.items():
        if item.get("title", "").lower() == key:
            return slug
    return None


def build_path(start_slug: str, concepts: dict[str, Any], max_steps: int) -> list[dict[str, Any]]:
    queue = deque([start_slug])
    seen = {start_slug}
    output: list[dict[str, Any]] = []
    title_to_slug = {item.get("title", "").lower(): slug for slug, item in concepts.items()}
    while queue and len(output) < max_steps:
        slug = queue.popleft()
        item = concepts.get(slug, {})
        output.append({
            "step": len(output) + 1,
            "slug": slug,
            "title": item.get("title", slug),
            "domain": item.get("domain", "general"),
            "freshness": item.get("freshness", "unknown"),
            "path": item.get("path"),
        })
        for title in item.get("read_next", []):
            next_slug = title_to_slug.get(str(title).lower())
            if next_slug and next_slug not in seen:
                seen.add(next_slug)
                queue.append(next_slug)
    return output


def render_markdown(title: str, steps: list[dict[str, Any]]) -> str:
    lines = [f"# Reading path: {title}", "", f"Generated: {utc_now()}", "", "## Steps", ""]
    for step in steps:
        lines.append(f"{step['step']}. **{step['title']}** — `{step['domain']}` / `{step['freshness']}`")
        lines.append(f"   - Note: `{step.get('path') or 'not generated'}`")
    lines += ["", "## Use", "", "Read in order. Refresh volatile or medium-freshness topics before relying on current claims.", ""]
    return "\n".join(lines)


def generate(root: Path, starts: list[str], out_dir: Path, max_steps: int = 8) -> dict[str, Any]:
    concepts = load_json(root / "indexes" / "concepts.json", {"concepts": {}}).get("concepts", {})
    aliases = load_json(root / "indexes" / "redirects.json", {"aliases": {}}).get("aliases", {})
    manifest = {"version": 1, "generated_at": utc_now(), "paths": []}
    for start in starts:
        slug = resolve_slug(start, concepts, aliases)
        if not slug:
            manifest["paths"].append({"query": start, "error": "start_not_found"})
            continue
        steps = build_path(slug, concepts, max_steps)
        out = {"query": start, "start_slug": slug, "generated_at": utc_now(), "steps": steps}
        json_path = out_dir / f"{slug}.json"
        md_path = out_dir / f"{slug}.md"
        write_json(json_path, out)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(concepts.get(slug, {}).get("title", start), steps), encoding="utf-8")
        manifest["paths"].append({"query": start, "json": str(json_path), "markdown": str(md_path), "steps": len(steps)})
    write_json(out_dir / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate reading paths from Wikipedia Knowledge Engine indexes.")
    parser.add_argument("starts", nargs="+")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--max-steps", type=int, default=8)
    args = parser.parse_args()
    out_dir = args.out_dir or args.root / "generated" / "reading-paths"
    print(json.dumps(generate(args.root, args.starts, out_dir, args.max_steps), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
