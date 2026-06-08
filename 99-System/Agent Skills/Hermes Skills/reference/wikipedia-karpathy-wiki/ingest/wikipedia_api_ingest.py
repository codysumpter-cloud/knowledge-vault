#!/usr/bin/env python3
"""Polite MediaWiki API ingestion for the Wikipedia Knowledge Engine."""
from __future__ import annotations
import argparse, hashlib, json, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from concept_extractor import SourceArticle, build_concept_card, quality_gate, write_card, write_json
API_URL = "https://en.wikipedia.org/w/api.php"
DEFAULT_USER_AGENT = "Prismtek-Buddy-Knowledge-Vault/0.2 (https://github.com/codysumpter-cloud/knowledge-vault; contact: cody.sumpter@gmail.com)"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

class MediaWikiClient:
    def __init__(self, api_url: str = API_URL, user_agent: str = DEFAULT_USER_AGENT, sleep_seconds: float = 0.4, max_retries: int = 3) -> None:
        self.api_url, self.user_agent, self.sleep_seconds, self.max_retries = api_url, user_agent, sleep_seconds, max_retries
        self._last_request = 0.0
    def get(self, params: dict[str, Any]) -> dict[str, Any]:
        merged = {"format": "json", "formatversion": "2", "maxlag": "5", **params}
        url = f"{self.api_url}?{urllib.parse.urlencode(merged, doseq=True)}"
        delay = max(0.0, self.sleep_seconds - (time.time() - self._last_request))
        if delay: time.sleep(delay)
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    self._last_request = time.time(); data = json.loads(response.read().decode("utf-8"))
                if "error" in data and data["error"].get("code") == "maxlag":
                    time.sleep(min(float(data["error"].get("lag", 1)) + 1, 10)); continue
                return data
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.max_retries: time.sleep(2 ** attempt); continue
                raise
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                if attempt < self.max_retries: time.sleep(2 ** attempt); continue
                raise
        raise RuntimeError(f"MediaWiki request failed after retries: {last_error}")
    def query_pages(self, titles: list[str], prop: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.get({"action": "query", "titles": "|".join(titles), "redirects": "1", "prop": prop, **(extra or {})})

def cache_key(title: str) -> str: return hashlib.sha256(title.encode("utf-8")).hexdigest()[:16]
def normalized_page_url(title: str) -> str: return "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe="/_()")

def fetch_page(client: MediaWikiClient, title: str) -> dict[str, Any]:
    data = client.query_pages([title], "extracts|revisions|categories|links|info|pageprops", {"exintro": "1", "explaintext": "1", "exsectionformat": "plain", "rvprop": "ids|timestamp|content", "rvslots": "main", "cllimit": "max", "pllimit": "max", "inprop": "url", "ppprop": "disambiguation"})
    pages = data.get("query", {}).get("pages", [])
    if not pages: raise RuntimeError(f"No page returned for {title!r}")
    page = pages[0]; resolved = page.get("title") or title
    sections = client.get({"action": "parse", "page": resolved, "prop": "sections"}).get("parse", {}).get("sections", [])
    revision = (page.get("revisions") or [{}])[0]
    content = revision.get("slots", {}).get("main", {}).get("content") or revision.get("content") or ""
    redirects = data.get("query", {}).get("redirects", [])
    return {"source": "English Wikipedia", "title": resolved, "page_id": page.get("pageid"), "namespace": page.get("ns", 0), "canonical_url": page.get("canonicalurl") or page.get("fullurl") or normalized_page_url(resolved), "revision_id": revision.get("revid"), "revision_timestamp": revision.get("timestamp"), "retrieved_at": utc_now(), "extract": page.get("extract") or "", "wikitext": content, "sections": sections, "categories": [c.get("title", "") for c in page.get("categories", [])], "links": [l.get("title", "") for l in page.get("links", [])], "redirects": redirects, "aliases": [r.get("from") for r in redirects if r.get("from")], "is_redirect": False, "is_disambiguation": "disambiguation" in (page.get("pageprops") or {}), "license_note": "Wikipedia text is generally CC BY-SA licensed; generated notes should be original summaries with source attribution."}

def write_source_article(article: dict[str, Any], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{cache_key(article['title'])}-{article['title'].replace('/', '-').replace(' ', '_')}.json"
    write_json(path, article); return path

def ingest_titles(titles: list[str], source_dir: Path, root: Path, generate: bool, client: MediaWikiClient) -> dict[str, Any]:
    manifest: dict[str, Any] = {"version": 1, "source": "English Wikipedia API", "generated_at": utc_now(), "requested_titles": titles, "articles_written": [], "cards_generated": [], "quality_failures": {}}
    for title in titles:
        article_data = fetch_page(client, title); path = write_source_article(article_data, source_dir); manifest["articles_written"].append(str(path))
        if generate:
            card = build_concept_card(SourceArticle.from_mapping(article_data)); failures = quality_gate(card)
            if failures: manifest["quality_failures"][card.slug] = failures
            manifest["cards_generated"].append({k: str(v) for k, v in write_card(card, root).items()})
    write_json(source_dir / "manifest.json", manifest); return manifest

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fetch Wikipedia articles through the MediaWiki API.")
    p.add_argument("titles", nargs="*"); p.add_argument("--titles-file", type=Path); p.add_argument("--source-dir", type=Path, default=Path(".data/wikipedia/api")); p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); p.add_argument("--generate", action="store_true"); p.add_argument("--user-agent", default=DEFAULT_USER_AGENT); p.add_argument("--sleep", type=float, default=0.4)
    args = p.parse_args(argv or sys.argv[1:]); titles = list(args.titles)
    if args.titles_file: titles.extend(line.strip() for line in args.titles_file.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#"))
    if not titles: raise SystemExit("provide at least one title or --titles-file")
    print(json.dumps(ingest_titles(titles, args.source_dir, args.root, args.generate, MediaWikiClient(user_agent=args.user_agent, sleep_seconds=args.sleep)), indent=2, ensure_ascii=False)); return 0
if __name__ == "__main__": raise SystemExit(main())
