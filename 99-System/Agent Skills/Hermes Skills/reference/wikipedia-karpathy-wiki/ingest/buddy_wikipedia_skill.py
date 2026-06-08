#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from concept_extractor import run as generate_cards
from reading_path_generator import generate as generate_paths
ROOT = Path(__file__).resolve().parents[1]
def wikipedia_generate_concept_cards(inputs: list[str], root: str | None = None, fail_on_quality: bool = False) -> dict[str, Any]:
    resolved = Path(root) if root else ROOT
    return generate_cards([Path(item) for item in inputs], resolved, fail_on_quality=fail_on_quality)
def wikipedia_generate_reading_path(starts: list[str], root: str | None = None, max_steps: int = 8) -> dict[str, Any]:
    resolved = Path(root) if root else ROOT
    return generate_paths(resolved, starts, resolved / "generated" / "reading-paths", max_steps=max_steps)
def wikipedia_lookup_concept(query: str, root: str | None = None) -> dict[str, Any]:
    resolved = Path(root) if root else ROOT
    concepts_path = resolved / "indexes" / "concepts.json"
    redirects_path = resolved / "indexes" / "redirects.json"
    concepts = json.loads(concepts_path.read_text(encoding="utf-8")) if concepts_path.exists() else {"concepts": {}}
    redirects = json.loads(redirects_path.read_text(encoding="utf-8")) if redirects_path.exists() else {"aliases": {}}
    key = query.strip().lower()
    slug = redirects.get("aliases", {}).get(key)
    if not slug:
        for candidate, item in concepts.get("concepts", {}).items():
            if candidate == key or item.get("title", "").lower() == key:
                slug = candidate
                break
    if not slug:
        return {"found": False, "query": query}
    return {"found": True, "query": query, "slug": slug, "concept": concepts.get("concepts", {}).get(slug, {})}
SKILL_EXPORTS = {"wikipedia_generate_concept_cards": wikipedia_generate_concept_cards, "wikipedia_generate_reading_path": wikipedia_generate_reading_path, "wikipedia_lookup_concept": wikipedia_lookup_concept}
