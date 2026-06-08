#!/usr/bin/env python3
"""Deterministic Wikipedia concept-card extraction for the Knowledge Vault.

Input: article JSON/JSONL from the API or dump ingest scripts.
Output: generated concept-card JSON, Obsidian notes, indexes, graph edges,
redirect aliases, domain maps, category maps, and a run manifest.
"""
from __future__ import annotations

import argparse, json, re, sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Literal

Freshness = Literal["stable", "medium", "volatile"]
RELATIONS = {"depends_on", "contains", "contrasts", "causes", "enables", "related_to", "alias_of", "categorized_as"}
VOLATILE = ("living people", "current events", "politics", "election", "law", "medicine", "health", "market", "finance")
MEDIUM = ("software", "company", "population", "statistics", "biology", "climate", "technology", "recent")
DOMAIN_RULES = {
    "mathematics": ("mathematics", "algebra", "geometry", "calculus", "statistics", "probability"),
    "computing": ("computer", "software", "programming", "internet", "machine learning", "artificial intelligence", "algorithm"),
    "physics": ("physics", "quantum", "relativity", "thermodynamics", "mechanics"),
    "biology": ("biology", "species", "genetics", "evolution", "medicine", "anatomy"),
    "history": ("history", "ancient", "medieval", "war", "empire", "revolution"),
    "geography": ("geography", "countries", "cities", "rivers", "mountains", "regions"),
    "arts": ("art", "music", "film", "literature", "architecture", "design"),
    "society": ("society", "politics", "law", "economics", "religion", "culture", "education"),
    "philosophy": ("philosophy", "ethics", "logic", "metaphysics", "epistemology"),
}
STOP = {"citation needed", "isbn", "doi", "wikipedia", "wikimedia commons", "category", "template", "file", "portal", "special", "talk"}

@dataclass(slots=True)
class SourceArticle:
    title: str
    page_id: int | None = None
    canonical_url: str | None = None
    revision_id: str | int | None = None
    retrieved_at: str | None = None
    extract: str = ""
    wikitext: str = ""
    sections: list[dict[str, Any]] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    redirects: list[dict[str, str]] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    namespace: int = 0
    is_redirect: bool = False
    is_disambiguation: bool = False
    source: str = "English Wikipedia"

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "SourceArticle":
        return cls(
            title=str(data.get("title") or data.get("normalized_title") or "Untitled"),
            page_id=data.get("page_id") or data.get("pageid"),
            canonical_url=data.get("canonical_url") or data.get("url"),
            revision_id=data.get("revision_id") or data.get("revid") or data.get("lastrevid"),
            retrieved_at=data.get("retrieved_at"),
            extract=data.get("extract") or data.get("lead") or "",
            wikitext=data.get("wikitext") or data.get("text") or "",
            sections=list(data.get("sections") or []),
            categories=[clean_title(c) for c in data.get("categories", [])],
            links=[clean_title(l) for l in data.get("links", [])],
            redirects=list(data.get("redirects") or []),
            aliases=[clean_title(a) for a in data.get("aliases", [])],
            namespace=int(data.get("namespace", 0) or 0),
            is_redirect=bool(data.get("is_redirect", False)),
            is_disambiguation=bool(data.get("is_disambiguation", False)),
            source=data.get("source") or "English Wikipedia",
        )

@dataclass(slots=True)
class Relationship:
    source: str
    relation: str
    target: str
    weight: float = 1.0
    evidence: str | None = None

@dataclass(slots=True)
class ConceptCard:
    title: str
    slug: str
    domain: str
    tiny_model: str
    primitives: list[str]
    mechanism: str
    relationships: list[Relationship]
    examples: list[str]
    common_traps: list[str]
    read_next: list[str]
    freshness: Freshness
    should_verify_live: bool
    source_url: str | None
    revision_id: str | int | None
    retrieved_at: str
    categories: list[str]
    aliases: list[str] = field(default_factory=list)
    source: str = "English Wikipedia"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def clean_title(value: Any) -> str:
    if isinstance(value, dict): value = value.get("title") or value.get("*") or ""
    return re.sub(r"\s+", " ", re.sub(r"^Category:", "", str(value or ""), flags=re.I)).strip()

def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower().replace("&", " and "))
    return re.sub(r"-+", "-", slug).strip("-") or "untitled"

def strip_markup(text: str) -> str:
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>|\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[(?:[^|\]]+\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[https?://[^\s\]]+\s*([^\]]*)\]", r"\1", text)
    return text.replace(chr(39) * 3, "").replace(chr(39) * 2, "")

def dedupe(items: Iterable[str], limit: int | None = None) -> list[str]:
    seen, out = set(), []
    for item in items:
        s, key = clean_title(item), clean_title(item).lower()
        if not s or key in seen or key in STOP: continue
        seen.add(key); out.append(s)
        if limit and len(out) >= limit: break
    return out

def section_titles(article: SourceArticle) -> list[str]:
    titles = [clean_title(s.get("line") or s.get("title")) for s in article.sections]
    if not titles and article.wikitext:
        titles = [m.group(1).strip() for m in re.finditer(r"^==\s*([^=]+?)\s*==\s*$", article.wikitext, flags=re.M)]
    return [t for t in titles if t and t.lower() not in {"references", "external links", "see also", "notes"}][:12]

def extract_links_from_wikitext(text: str) -> list[str]:
    return dedupe(re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]*)?\]\]", text), 500)

def lead_text(article: SourceArticle) -> str:
    if article.extract: return article.extract
    return strip_markup(re.split(r"\n==\s*[^=]+\s*==\n", article.wikitext or "", maxsplit=1)[0])

def first_sentence(text: str, fallback: str) -> str:
    cleaned = re.sub(r"\s+", " ", strip_markup(text)).strip()
    if not cleaned: return fallback
    for part in re.split(r"(?<=[.!?])\s+", cleaned):
        if 40 <= len(part) <= 280: return part
    return cleaned[:260].rstrip() + ("…" if len(cleaned) > 260 else "")

def classify_freshness(article: SourceArticle) -> Freshness:
    hay = " ".join([article.title, *article.categories, *section_titles(article)]).lower()
    if any(t in hay for t in VOLATILE): return "volatile"
    if any(t in hay for t in MEDIUM): return "medium"
    return "stable"

def classify_domain(article: SourceArticle) -> str:
    hay = " ".join([article.title, *article.categories, *article.links[:25], *section_titles(article)]).lower()
    scores = Counter({d: sum(1 for k in keys if k in hay) for d, keys in DOMAIN_RULES.items()})
    return scores.most_common(1)[0][0] if scores and scores.most_common(1)[0][1] else "general"

def build_concept_card(article: SourceArticle) -> ConceptCard:
    freshness, domain = classify_freshness(article), classify_domain(article)
    primitives = dedupe([*section_titles(article)[:5], *(article.links or extract_links_from_wikitext(article.wikitext))[:12], *article.categories[:5]], 8)
    rels: list[Relationship] = []
    rels += [Relationship(article.title, "categorized_as", c, 0.7, "Wikipedia category") for c in dedupe(article.categories, 10)]
    rels += [Relationship(article.title, "contains", s, 0.6, "Article section") for s in dedupe(section_titles(article), 8)]
    rels += [Relationship(article.title, "related_to", l, 0.45, "Article link") for l in dedupe(article.links or extract_links_from_wikitext(article.wikitext), 14)]
    aliases = dedupe(article.aliases + [r.get("from", "") for r in article.redirects], 25)
    rels += [Relationship(a, "alias_of", article.title, 1.0, "Redirect or alias") for a in aliases if a.lower() != article.title.lower()]
    if domain != "general": rels.append(Relationship(article.title, "categorized_as", domain, 0.8, "Domain classifier"))
    sections = section_titles(article)
    mechanism = f"Understand {article.title} by walking through: {', '.join(sections[:6])}." if sections else f"Understand {article.title} through its nearest primitives: {', '.join(primitives[:6])}."
    traps = ["Do not treat this generated card as a full replacement for the source article.", "Do not copy long Wikipedia passages into the vault; regenerate compact original notes instead."]
    if freshness == "volatile": traps.insert(0, "This topic can change quickly; verify live before making current claims.")
    if freshness == "medium": traps.insert(0, "Some facts may drift over time; refresh before public or formal use.")
    read_next = dedupe([r.target for r in rels if r.relation in {"related_to", "contains"}], 8)
    return ConceptCard(article.title, slugify(article.title), domain, first_sentence(lead_text(article), f"{article.title} is a concept best understood through its source context and relationships."), primitives, mechanism, rels[:40], [f"Use {article.title} as a node in the {domain} map.", f"Teach {article.title} from the tiny model outward."], traps, read_next, freshness, freshness in {"medium", "volatile"}, article.canonical_url, article.revision_id, article.retrieved_at or utc_now(), article.categories, aliases, article.source)

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

def load_json(path: Path, default: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def card_mapping(card: ConceptCard) -> dict[str, Any]:
    data = asdict(card); data["relationships"] = [asdict(r) for r in card.relationships]; return data

def render_obsidian_note(card: ConceptCard) -> str:
    primitive_lines = "\n".join(f"- **{p}**" for p in card.primitives) or "- No primitives extracted yet."
    rel_lines = "\n".join(f"  - from: {json.dumps(r.source, ensure_ascii=False)}\n    relation: {r.relation}\n    to: {json.dumps(r.target, ensure_ascii=False)}\n    weight: {r.weight}\n    evidence: {json.dumps(r.evidence or '', ensure_ascii=False)}" for r in card.relationships) or "  []"
    return f"""---
title: {json.dumps(card.title, ensure_ascii=False)}
status: generated concept card
source_url: {json.dumps(card.source_url or 'unknown', ensure_ascii=False)}
revision_id: {json.dumps(str(card.revision_id or 'unknown'), ensure_ascii=False)}
retrieved_at: {json.dumps(card.retrieved_at, ensure_ascii=False)}
freshness: {card.freshness}
should_verify_live: {str(card.should_verify_live).lower()}
domain: {card.domain}
---

# {card.title}

Status: generated concept card  
Source: {card.source_url or 'unknown'}  
Revision: {card.revision_id or 'unknown'}  
Retrieved: {card.retrieved_at}  
Freshness: {card.freshness}  
Domain: {card.domain}

## Tiny model

{card.tiny_model}

## Build from primitives

{primitive_lines}

## Mechanism

{card.mechanism}

## Relationships

```yaml
relationships:
{rel_lines}
```

## Examples

{chr(10).join(f'- {x}' for x in card.examples)}

## Common traps

{chr(10).join(f'- {x}' for x in card.common_traps)}

## Read next

{chr(10).join(f'{i}. [[{x}]]' for i, x in enumerate(card.read_next, 1)) or '1. Refresh source links and categories.'}

## Source posture

This is an original compressed note derived from Wikipedia metadata and/or article text. Verify live before using for volatile or high-stakes claims.
"""

def update_indexes(card: ConceptCard, indexes: Path) -> None:
    concepts = load_json(indexes / "concepts.json", {"version": 1, "generated_at": None, "concepts": {}})
    concepts.setdefault("concepts", {})[card.slug] = {"title": card.title, "domain": card.domain, "freshness": card.freshness, "source_url": card.source_url, "revision_id": card.revision_id, "retrieved_at": card.retrieved_at, "path": f"generated/concepts/{card.domain}/{card.slug}.md", "aliases": card.aliases, "read_next": card.read_next}
    concepts["generated_at"] = utc_now(); write_json(indexes / "concepts.json", concepts)
    domains = load_json(indexes / "domains.json", {"version": 1, "generated_at": None, "domains": {}})
    bucket = domains.setdefault("domains", {}).setdefault(card.domain, {"concept_count": 0, "concepts": []})
    if card.slug not in bucket["concepts"]: bucket["concepts"].append(card.slug)
    bucket["concept_count"] = len(bucket["concepts"]); domains["generated_at"] = utc_now(); write_json(indexes / "domains.json", domains)
    redirects = load_json(indexes / "redirects.json", {"version": 1, "generated_at": None, "aliases": {}})
    for alias in card.aliases: redirects.setdefault("aliases", {})[alias.lower()] = card.slug
    redirects["generated_at"] = utc_now(); write_json(indexes / "redirects.json", redirects)
    cats = load_json(indexes / "categories.json", {"version": 1, "generated_at": None, "categories": {}})
    for c in card.categories:
        bucket = cats.setdefault("categories", {}).setdefault(c, {"concepts": []})
        if card.slug not in bucket["concepts"]: bucket["concepts"].append(card.slug)
    cats["generated_at"] = utc_now(); write_json(indexes / "categories.json", cats)
    graph = load_json(indexes / "knowledge_graph.json", {"version": 1, "generated_at": None, "nodes": {}, "edges": []})
    graph.setdefault("nodes", {})[card.slug] = {"title": card.title, "domain": card.domain, "freshness": card.freshness}
    seen = {(e.get("source"), e.get("relation"), e.get("target")) for e in graph.setdefault("edges", [])}
    for r in card.relationships:
        key = (r.source, r.relation, r.target)
        if key not in seen: graph["edges"].append(asdict(r)); seen.add(key)
    graph["generated_at"] = utc_now(); write_json(indexes / "knowledge_graph.json", graph)

def write_card(card: ConceptCard, root: Path) -> dict[str, Path]:
    card_json = root / "generated" / "cards" / card.domain / f"{card.slug}.json"
    note_path = root / "generated" / "concepts" / card.domain / f"{card.slug}.md"
    write_json(card_json, card_mapping(card)); note_path.parent.mkdir(parents=True, exist_ok=True); note_path.write_text(render_obsidian_note(card), encoding="utf-8")
    update_indexes(card, root / "indexes")
    return {"card_json": card_json, "note": note_path}

def quality_gate(card: ConceptCard) -> list[str]:
    failures = []
    if not card.source_url: failures.append("missing_source_url")
    if not card.retrieved_at: failures.append("missing_retrieval_date")
    if not card.relationships: failures.append("missing_relationships")
    if card.freshness == "volatile" and not card.should_verify_live: failures.append("volatile_without_live_verification_flag")
    return failures

def load_articles(path: Path):
    if path.suffix == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip(): yield SourceArticle.from_mapping(json.loads(line))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in (data if isinstance(data, list) else data.get("articles", [data]) if isinstance(data, dict) else []): yield SourceArticle.from_mapping(item)

def iter_inputs(inputs: list[Path]):
    for item in inputs:
        if item.is_dir(): yield from sorted(item.rglob("*.json")); yield from sorted(item.rglob("*.jsonl"))
        else: yield item

def run(inputs: list[Path], root: Path, fail_on_quality: bool = False) -> dict[str, Any]:
    cards, failures, categories = 0, {}, {}
    for path in iter_inputs(inputs):
        for article in load_articles(path):
            if article.namespace != 0 or article.is_redirect or article.is_disambiguation: continue
            card = build_concept_card(article); q = quality_gate(card)
            if q: failures[card.slug] = q
            write_card(card, root); cards += 1
            for c in card.categories: categories.setdefault(c, {"parents": [], "children": [], "concepts": []})["concepts"].append(card.slug)
    write_json(root / "indexes" / "category_hierarchy.json", {"version": 1, "generated_at": utc_now(), "categories": categories})
    manifest = {"version": 1, "generated_at": utc_now(), "cards_generated": cards, "quality_failures": failures}
    write_json(root / "generated" / "manifest.json", manifest)
    if fail_on_quality and failures: raise SystemExit(f"quality gate failed: {failures}")
    return manifest

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate Wikipedia Karpathy concept cards from JSON/JSONL.")
    p.add_argument("inputs", nargs="+", type=Path); p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); p.add_argument("--fail-on-quality", action="store_true")
    a = p.parse_args(argv or sys.argv[1:]); print(json.dumps(run(a.inputs, a.root, a.fail_on_quality), indent=2, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
