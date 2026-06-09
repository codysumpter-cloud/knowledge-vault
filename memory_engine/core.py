from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import quote

DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".obsidian",
    ".trash",
    ".data",
    "00-Private",
    "99-System/Security",
    "99-System/Logs",
    "99-System/Backups",
    "__pycache__",
}

DEFAULT_OUTPUT_DIR = Path("99-System/Memory Engine")
DEFAULT_INDEX_PATH = DEFAULT_OUTPUT_DIR / "memory-index.json"
DEFAULT_GRAPH_PATH = DEFAULT_OUTPUT_DIR / "memory-graph.json"
DEFAULT_OBSIDIAN_INDEX_PATH = DEFAULT_OUTPUT_DIR / "Obsidian Memory Index.md"

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"!?!?\[\[([^\]\n]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_/-]+)")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_/-]{1,}")


@dataclass
class MemoryRecord:
    path: str
    title: str
    summary: str
    metadata: dict[str, object]
    headings: list[str]
    tags: list[str]
    wikilinks: list[str]
    markdown_links: list[str]
    outgoing_paths: list[str]
    backlinks: list[str] = field(default_factory=list)
    word_count: int = 0
    sha256: str = ""
    modified_utc: str = ""
    obsidian_uri: str = ""


@dataclass
class MemoryIndex:
    vault: str
    generated_at: str
    root: str
    records: list[MemoryRecord]
    stats: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "vault": self.vault,
            "generated_at": self.generated_at,
            "root": self.root,
            "stats": self.stats,
            "records": [asdict(record) for record in self.records],
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_excluded(path: Path, root: Path, exclude_dirs: set[str] | None = None) -> bool:
    exclude_dirs = exclude_dirs or DEFAULT_EXCLUDE_DIRS
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    parts = relative.parts
    if any(part in exclude_dirs for part in parts):
        return True
    rel = relative.as_posix()
    return any("/" in item and (rel == item or rel.startswith(item + "/")) for item in exclude_dirs)


def iter_markdown(root: Path, include_private: bool = False) -> Iterable[Path]:
    root = root.resolve()
    excludes = set(DEFAULT_EXCLUDE_DIRS)
    if include_private:
        excludes.discard("00-Private")
    for path in sorted(root.rglob("*.md")):
        if not is_excluded(path, root, excludes):
            yield path


def parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
    return value.strip('"')


def parse_front_matter(text: str) -> tuple[dict[str, object], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    metadata: dict[str, object] = {}
    lines = match.group(1).splitlines()
    current_key: str | None = None
    current_list: list[str] = []

    def flush_list() -> None:
        nonlocal current_key, current_list
        if current_key is not None and current_list:
            metadata[current_key] = current_list
        current_key = None
        current_list = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_key is not None:
                item = line.split("- ", 1)[1].strip().strip('"')
                current_list.append(item)
            continue
        flush_list()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                current_key = key
                current_list = []
            else:
                metadata[key] = parse_scalar(value)
    flush_list()
    return metadata, text[match.end():]


def extract_title(body: str, path: Path) -> str:
    match = TITLE_RE.search(body)
    if match:
        return match.group(1).strip()
    return path.stem


def extract_summary(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("---"):
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
        if stripped:
            return stripped[:280]
    return ""


def normalize_tags(metadata: dict[str, object], body: str) -> list[str]:
    tags: set[str] = set()
    raw_tags = metadata.get("tags")
    if isinstance(raw_tags, list):
        tags.update(str(item).strip("#") for item in raw_tags if str(item).strip())
    elif isinstance(raw_tags, str):
        tags.update(part.strip().strip("#") for part in raw_tags.split(",") if part.strip())
    tags.update(match.group(1) for match in TAG_RE.finditer(body))
    return sorted(tags)


def extract_wikilinks(body: str) -> list[str]:
    links: set[str] = set()
    for match in WIKILINK_RE.finditer(body):
        target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            links.add(target)
    return sorted(links)


def extract_markdown_links(body: str) -> list[str]:
    links: set[str] = set()
    for _label, target in MARKDOWN_LINK_RE.findall(body):
        if target and not target.startswith(("http://", "https://", "mailto:")):
            links.add(target.split("#", 1)[0])
    return sorted(links)


def slug_note_name(path: Path) -> str:
    return path.stem


def make_obsidian_uri(path: str, vault_name: str) -> str:
    return "obsidian://open?vault=" + quote(vault_name) + "&file=" + quote(path)


def resolve_links(records: list[MemoryRecord], root: Path) -> None:
    by_stem: dict[str, str] = {}
    by_path_no_ext: dict[str, str] = {}
    by_path: dict[str, str] = {}
    for record in records:
        p = Path(record.path)
        by_stem[p.stem.lower()] = record.path
        by_path_no_ext[p.with_suffix("").as_posix().lower()] = record.path
        by_path[p.as_posix().lower()] = record.path

    backlinks: dict[str, set[str]] = {record.path: set() for record in records}
    for record in records:
        outgoing: set[str] = set(record.outgoing_paths)
        for link in record.wikilinks:
            resolved = by_stem.get(Path(link).stem.lower()) or by_path_no_ext.get(link.lower()) or by_path.get(link.lower())
            if resolved:
                outgoing.add(resolved)
        for link in record.markdown_links:
            candidate = (Path(record.path).parent / link).as_posix()
            resolved = by_path.get(candidate.lower()) or by_path.get(link.lower())
            if resolved:
                outgoing.add(resolved)
        record.outgoing_paths = sorted(path for path in outgoing if path != record.path)
        for target in record.outgoing_paths:
            backlinks.setdefault(target, set()).add(record.path)
    for record in records:
        record.backlinks = sorted(backlinks.get(record.path, set()))


def index_vault(root: Path, vault_name: str | None = None, include_private: bool = False) -> MemoryIndex:
    root = root.resolve()
    vault_name = vault_name or root.name
    records: list[MemoryRecord] = []
    for path in iter_markdown(root, include_private=include_private):
        text = path.read_text(encoding="utf-8", errors="replace")
        metadata, body = parse_front_matter(text)
        relative = path.relative_to(root).as_posix()
        headings = [match.group(2).strip() for match in HEADING_RE.finditer(body)]
        wikilinks = extract_wikilinks(body)
        markdown_links = extract_markdown_links(body)
        words = WORD_RE.findall(body)
        stat = path.stat()
        record = MemoryRecord(
            path=relative,
            title=extract_title(body, path),
            summary=extract_summary(body),
            metadata=metadata,
            headings=headings,
            tags=normalize_tags(metadata, body),
            wikilinks=wikilinks,
            markdown_links=markdown_links,
            outgoing_paths=[],
            word_count=len(words),
            sha256=hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
            modified_utc=datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            obsidian_uri=make_obsidian_uri(relative, vault_name),
        )
        records.append(record)
    resolve_links(records, root)
    stats = {
        "records": len(records),
        "words": sum(record.word_count for record in records),
        "links": sum(len(record.outgoing_paths) for record in records),
        "tags": len({tag for record in records for tag in record.tags}),
    }
    return MemoryIndex(vault=vault_name, generated_at=utc_now(), root=str(root), records=records, stats=stats)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_index(index: MemoryIndex, output_path: Path) -> None:
    write_json(output_path, index.to_dict())


def write_graph(index: MemoryIndex, output_path: Path) -> None:
    nodes = [
        {
            "id": record.path,
            "title": record.title,
            "type": record.metadata.get("type"),
            "status": record.metadata.get("status"),
            "tags": record.tags,
        }
        for record in index.records
    ]
    edges = [
        {"source": record.path, "target": target, "type": "links_to"}
        for record in index.records
        for target in record.outgoing_paths
    ]
    write_json(output_path, {"generated_at": index.generated_at, "nodes": nodes, "edges": edges})


def write_obsidian_index(index: MemoryIndex, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Obsidian Memory Index",
        "",
        "> Generated by `python3 -m memory_engine index --obsidian`.",
        "",
        f"Generated: {index.generated_at}",
        "",
        "## Stats",
        "",
        f"- Records: {index.stats['records']}",
        f"- Words: {index.stats['words']}",
        f"- Links: {index.stats['links']}",
        f"- Tags: {index.stats['tags']}",
        "",
        "## Records",
        "",
    ]
    for record in sorted(index.records, key=lambda item: item.path.lower()):
        tags = ", ".join(record.tags[:8]) if record.tags else "no tags"
        note_link = f"[[{Path(record.path).with_suffix('').as_posix()}|{record.title}]]"
        lines.append(f"- {note_link} — `{record.metadata.get('type', 'unknown')}` / `{record.metadata.get('status', 'unknown')}` — {tags}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_index(path: Path) -> MemoryIndex:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = [MemoryRecord(**record) for record in data.get("records", [])]
    return MemoryIndex(
        vault=data.get("vault", "knowledge-vault"),
        generated_at=data.get("generated_at", ""),
        root=data.get("root", ""),
        records=records,
        stats=data.get("stats", {}),
    )


def score_record(record: MemoryRecord, terms: Sequence[str]) -> int:
    haystacks = {
        "title": record.title.lower(),
        "path": record.path.lower(),
        "summary": record.summary.lower(),
        "tags": " ".join(record.tags).lower(),
        "headings": " ".join(record.headings).lower(),
        "metadata": json.dumps(record.metadata, ensure_ascii=False).lower(),
    }
    score = 0
    for term in terms:
        term_l = term.lower()
        if term_l in haystacks["title"]:
            score += 10
        if term_l in haystacks["path"]:
            score += 7
        if term_l in haystacks["tags"]:
            score += 6
        if term_l in haystacks["headings"]:
            score += 4
        if term_l in haystacks["summary"]:
            score += 3
        if term_l in haystacks["metadata"]:
            score += 2
    return score


def search_index(index: MemoryIndex, query: str, limit: int = 10, record_type: str | None = None, status: str | None = None, tag: str | None = None) -> list[tuple[int, MemoryRecord]]:
    terms = [term for term in WORD_RE.findall(query) if term]
    results: list[tuple[int, MemoryRecord]] = []
    for record in index.records:
        if record_type and record.metadata.get("type") != record_type:
            continue
        if status and record.metadata.get("status") != status:
            continue
        if tag and tag not in record.tags:
            continue
        score = score_record(record, terms) if terms else 1
        if score > 0:
            results.append((score, record))
    return sorted(results, key=lambda item: (-item[0], item[1].path.lower()))[:limit]


def read_note(root: Path, record: MemoryRecord) -> str:
    path = root / record.path
    return path.read_text(encoding="utf-8", errors="replace")


def records_by_paths(index: MemoryIndex, paths: Sequence[str]) -> list[MemoryRecord]:
    by_path = {record.path: record for record in index.records}
    result = []
    for path in paths:
        normalized = Path(path).as_posix()
        record = by_path.get(normalized)
        if record:
            result.append(record)
    return result


def build_bundle_markdown(index: MemoryIndex, root: Path, records: Sequence[MemoryRecord], title: str, purpose: str, max_chars_per_note: int = 12000) -> str:
    lines = [
        f"# {title}",
        "",
        f"> {purpose}",
        "",
        f"Generated: {utc_now()}",
        "",
        "## Included files",
        "",
    ]
    for record in records:
        lines.append(f"- `{{}}` — {{}}".format(record.path, record.title))
    lines.extend(["", "## Notes", ""])
    for record in records:
        text = read_note(root, record)
        if len(text) > max_chars_per_note:
            text = text[:max_chars_per_note] + "\n\n<!-- truncated by memory_engine bundle export -->\n"
        lines.extend([
            f"### {record.title}",
            "",
            f"Path: `{record.path}`",
            "",
            "```md",
            text.rstrip(),
            "```",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
