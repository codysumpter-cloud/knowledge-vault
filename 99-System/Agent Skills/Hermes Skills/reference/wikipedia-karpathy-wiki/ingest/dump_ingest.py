#!/usr/bin/env python3
"""Stream Wikimedia dump XML into compact source JSONL records."""
from __future__ import annotations

import argparse
import bz2
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from concept_extractor import SourceArticle, build_concept_card, extract_links_from_wikitext, quality_gate, write_card, write_json

NS = "{http://www.mediawiki.org/xml/export-0.10/}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def open_dump(path: Path):
    if path.suffix == ".bz2":
        return bz2.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("rt", encoding="utf-8", errors="replace")


def first_text(parent: ET.Element, name: str) -> str:
    child = parent.find(f"{NS}{name}")
    return child.text if child is not None and child.text is not None else ""


def revision_text(page: ET.Element) -> tuple[str | None, str | None, str]:
    revision = page.find(f"{NS}revision")
    if revision is None:
        return None, None, ""
    text_node = revision.find(f"{NS}text")
    return first_text(revision, "id") or None, first_text(revision, "timestamp") or None, text_node.text if text_node is not None and text_node.text is not None else ""


def is_redirect(page: ET.Element, text: str) -> bool:
    return page.find(f"{NS}redirect") is not None or bool(re.match(r"\s*#redirect\b", text, flags=re.I))


def is_disambiguation(title: str, text: str) -> bool:
    return "{{disambiguation" in text.lower() or title.lower().endswith("(disambiguation)")


def extract_categories(text: str) -> list[str]:
    return [category.strip() for category in re.findall(r"\[\[Category:([^\]|]+)", text, flags=re.I)]


def iter_dump_articles(path: Path, limit: int | None = None, include_redirects: bool = False) -> Iterable[dict[str, Any]]:
    count = 0
    retrieved_at = utc_now()
    with open_dump(path) as handle:
        for _, elem in ET.iterparse(handle, events=("end",)):
            if not elem.tag.endswith("page"):
                continue
            title = first_text(elem, "title")
            namespace = int(first_text(elem, "ns") or "0")
            page_id = first_text(elem, "id")
            revision_id, revision_timestamp, text = revision_text(elem)
            redirect = is_redirect(elem, text)
            if namespace != 0 or (redirect and not include_redirects):
                elem.clear()
                continue
            yield {
                "source": "English Wikipedia dump",
                "title": title,
                "page_id": int(page_id) if page_id.isdigit() else None,
                "namespace": namespace,
                "canonical_url": "https://en.wikipedia.org/wiki/" + title.replace(" ", "_"),
                "revision_id": revision_id,
                "revision_timestamp": revision_timestamp,
                "retrieved_at": retrieved_at,
                "extract": "",
                "wikitext": text,
                "sections": [{"line": match.group(1).strip()} for match in re.finditer(r"^==\s*([^=]+?)\s*==\s*$", text, flags=re.M)][:40],
                "categories": extract_categories(text),
                "links": extract_links_from_wikitext(text)[:500],
                "redirects": [],
                "aliases": [],
                "is_redirect": redirect,
                "is_disambiguation": is_disambiguation(title, text),
                "license_note": "Wikipedia dump source; preserve attribution posture for reused source facts or text.",
            }
            count += 1
            elem.clear()
            if limit and count >= limit:
                break


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def generate_from_jsonl(jsonl_path: Path, root: Path, max_generate: int | None = None) -> dict[str, Any]:
    manifest: dict[str, Any] = {"version": 1, "generated_at": utc_now(), "source_jsonl": str(jsonl_path), "cards_generated": 0, "quality_failures": {}}
    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            article = SourceArticle.from_mapping(json.loads(line))
            if article.is_redirect or article.is_disambiguation:
                continue
            card = build_concept_card(article)
            failures = quality_gate(card)
            if failures:
                manifest["quality_failures"][card.slug] = failures
            write_card(card, root)
            manifest["cards_generated"] += 1
            if max_generate and manifest["cards_generated"] >= max_generate:
                break
    write_json(root / "generated" / "dump_ingest_manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream a Wikimedia dump into JSONL source records and optional generated notes.")
    parser.add_argument("dump", type=Path)
    parser.add_argument("--out", type=Path, default=Path(".data/wikipedia/dump/articles.jsonl"))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--include-redirects", action="store_true")
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--max-generate", type=int)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    count = write_jsonl(args.out, iter_dump_articles(args.dump, args.limit, args.include_redirects))
    manifest: dict[str, Any] = {"version": 1, "generated_at": utc_now(), "source": str(args.dump), "articles_written": count, "jsonl": str(args.out)}
    if args.generate:
        manifest["generation"] = generate_from_jsonl(args.out, args.root, args.max_generate)
    write_json(args.out.parent / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
