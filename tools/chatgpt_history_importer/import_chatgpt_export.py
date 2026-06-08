#!/usr/bin/env python3
"""Import ChatGPT export data into public-safe KnowledgeVault digests.

This tool intentionally does not preserve raw transcripts by default. It creates
reviewable summaries and short redacted excerpts so KnowledgeVault can become
useful long-term project memory without becoming a secret dump.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

PROJECT_KEYWORDS: dict[str, list[str]] = {
    "buddy-agent": ["buddy-agent", "buddy agent", "lil buddy", "orchestrator", "worker agent"],
    "prismtek-apps": ["prismtek-apps", "testflight", "swiftui", "xcode", "ios", "macos", "buddy app"],
    "knowledge-vault": ["knowledge-vault", "knowledgevault", "vault", "obsidian", "vault steward"],
    "buddy-brain": ["buddy-brain", "buddy brain", "bemore-stack", "be more stack", "governance"],
    "omni-buddy": ["omni-buddy", "raspberry pi", "voice", "vision", "local multimodal"],
    "hermes-agent": ["hermes-agent", "hermes", "providerrouter", "provider router"],
    "pixel-art-assets": ["pixel art", "sprite", "sprites", "tamagotchi", "buddy appearance"],
    "pokemon-games": ["pokemon", "pokemmo", "elite four", "ev train", "iv", "pokemon-inspired"],
    "trading-research": ["alpaca", "paper trading", "crypto", "trading", "prediction market"],
    "resume-jobs": ["resume", "cover letter", "job", "interview", "application"],
    "react-migration": ["react", "vite", "next.js", "site migration", "frontend"],
    "openai-chatgpt": ["chatgpt", "openai", "export data", "archived chats"],
}

SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{20,}"), "[REDACTED_OPENAI_KEY]"),
    (re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "[REDACTED_GITHUB_PAT]"),
    (re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b"), "[REDACTED_NPM_TOKEN]"),
    (re.compile(r"\bpypi-[A-Za-z0-9_\-]{20,}\b"), "[REDACTED_PYPI_TOKEN]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_ACCESS_KEY]"),
    (re.compile(r"(?is)-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY_BLOCK]"),
    (re.compile(r"(?i)\b(bearer|token|api[_-]?key|password|passwd|secret)\s*[:=]\s*[^\s,;]{6,}"), r"\1=[REDACTED_SECRET]"),
    (re.compile(r"(?i)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b"), "[REDACTED_EMAIL]"),
    (re.compile(r"(?i)(/Users/)[^/\s]+"), r"\1[REDACTED_USER]"),
    (re.compile(r"(?i)(C:\\Users\\)[^\\\s]+"), r"\1[REDACTED_USER]"),
]

DECISION_HINTS = [
    "decision",
    "decided",
    "we will",
    "we should",
    "do not",
    "don't",
    "retired",
    "source of truth",
    "default",
    "must",
    "must not",
    "prefer",
]

TASK_HINTS = [
    "todo",
    "next",
    "fix",
    "build",
    "add",
    "create",
    "implement",
    "merge",
    "ship",
    "open loop",
    "blocker",
]


@dataclass
class Message:
    role: str
    text: str
    created_at: str | None = None


@dataclass
class Conversation:
    id: str
    title: str
    created_at: str | None
    updated_at: str | None
    messages: list[Message]


@dataclass
class ConversationSummary:
    id: str
    title: str
    created_at: str | None
    updated_at: str | None
    projects: list[str]
    message_count: int
    user_message_count: int
    assistant_message_count: int
    excerpt: str
    decision_candidates: list[str]
    task_candidates: list[str]


def redact(text: str) -> str:
    cleaned = text
    for pattern, replacement in SECRET_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    return cleaned


def compact(text: str, limit: int = 500) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower().strip())
    return re.sub(r"-+", "-", value).strip("-") or "untitled"


def iso_from_timestamp(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return value if isinstance(value, str) and value else None


def date_key(value: str | None) -> str:
    return value[:10] if value else "unknown-date"


def load_json_from_input(input_path: Path) -> Any:
    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(input_path) as zf:
            candidates = [name for name in zf.namelist() if name.endswith("conversations.json")]
            if not candidates:
                raise SystemExit("No conversations.json found in export zip.")
            with zf.open(candidates[0]) as f:
                return json.loads(f.read().decode("utf-8"))
    if input_path.is_dir():
        candidate = input_path / "conversations.json"
        if not candidate.exists():
            raise SystemExit(f"No conversations.json found in {input_path}")
        return json.loads(candidate.read_text(encoding="utf-8"))
    return json.loads(input_path.read_text(encoding="utf-8"))


def parse_parts(content: dict[str, Any]) -> str:
    parts = content.get("parts", [])
    text_parts: list[str] = []
    for part in parts:
        if isinstance(part, str):
            text_parts.append(part)
        elif isinstance(part, dict):
            kind = part.get("content_type") or part.get("type") or "object"
            text_parts.append(f"[non-text content: {kind}]")
    return "\n".join(text_parts).strip()


def parse_chatgpt_export(data: Any) -> list[Conversation]:
    if not isinstance(data, list):
        raise SystemExit("Expected conversations.json to contain a list.")

    conversations: list[Conversation] = []
    for index, conv in enumerate(data):
        if not isinstance(conv, dict):
            continue
        mapping = conv.get("mapping") or {}
        messages: list[Message] = []
        for node in mapping.values():
            if not isinstance(node, dict):
                continue
            raw_message = node.get("message")
            if not raw_message:
                continue
            author = raw_message.get("author") or {}
            role = author.get("role") or "unknown"
            content = raw_message.get("content") or {}
            text = parse_parts(content) if isinstance(content, dict) else ""
            text = redact(text)
            if not text:
                continue
            messages.append(Message(role=role, text=text, created_at=iso_from_timestamp(raw_message.get("create_time"))))
        title = redact(str(conv.get("title") or f"Untitled Conversation {index + 1}"))
        conversations.append(
            Conversation(
                id=str(conv.get("id") or f"conversation-{index + 1}"),
                title=title,
                created_at=iso_from_timestamp(conv.get("create_time")),
                updated_at=iso_from_timestamp(conv.get("update_time")),
                messages=messages,
            )
        )
    return conversations


def parse_manual_text(input_path: Path) -> list[Conversation]:
    paths = sorted(p for p in input_path.rglob("*") if p.suffix.lower() in {".txt", ".md"}) if input_path.is_dir() else [input_path]
    conversations: list[Conversation] = []
    for i, path in enumerate(paths, start=1):
        text = redact(path.read_text(encoding="utf-8", errors="replace"))
        modified = dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).isoformat()
        conversations.append(
            Conversation(
                id=f"manual-{i}-{slugify(path.stem)}",
                title=path.stem,
                created_at=modified,
                updated_at=modified,
                messages=[Message(role="manual", text=text, created_at=modified)],
            )
        )
    return conversations


def classify_projects(conversation: Conversation) -> list[str]:
    haystack = (conversation.title + "\n" + "\n".join(m.text for m in conversation.messages)).lower()
    scores: Counter[str] = Counter()
    for project, keywords in PROJECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in haystack:
                scores[project] += 1
    return [project for project, _ in scores.most_common(5)] or ["uncategorized"]


def candidate_lines(conversation: Conversation, hints: Iterable[str], limit: int = 8) -> list[str]:
    hint_list = [h.lower() for h in hints]
    found: list[str] = []
    for message in conversation.messages:
        for raw_line in re.split(r"[\n\r]+", message.text):
            line = compact(raw_line, 220)
            if line and any(hint in line.lower() for hint in hint_list):
                found.append(line)
                break
        if len(found) >= limit:
            break
    return found


def summarize(conversation: Conversation) -> ConversationSummary:
    projects = classify_projects(conversation)
    user_count = sum(1 for m in conversation.messages if m.role == "user")
    assistant_count = sum(1 for m in conversation.messages if m.role == "assistant")
    excerpt_source = next((m.text for m in conversation.messages if m.role in {"user", "manual"} and m.text.strip()), "")
    if not excerpt_source and conversation.messages:
        excerpt_source = conversation.messages[0].text
    return ConversationSummary(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        projects=projects,
        message_count=len(conversation.messages),
        user_message_count=user_count,
        assistant_message_count=assistant_count,
        excerpt=compact(excerpt_source, 700),
        decision_candidates=candidate_lines(conversation, DECISION_HINTS),
        task_candidates=candidate_lines(conversation, TASK_HINTS),
    )


def render_conversation_card(summary: ConversationSummary) -> str:
    lines = [
        f"### {summary.title}",
        "",
        f"- Conversation ID: `{summary.id}`",
        f"- Created: `{summary.created_at or 'unknown'}`",
        f"- Updated: `{summary.updated_at or 'unknown'}`",
        f"- Projects: {', '.join(f'`{p}`' for p in summary.projects)}",
        f"- Messages: {summary.message_count} total, {summary.user_message_count} user, {summary.assistant_message_count} assistant",
        "",
        "**Redacted excerpt**",
        "",
        f"> {summary.excerpt or 'No safe excerpt generated.'}",
        "",
    ]
    if summary.decision_candidates:
        lines.extend(["**Decision candidates**", ""])
        lines.extend(f"- {item}" for item in summary.decision_candidates)
        lines.append("")
    if summary.task_candidates:
        lines.extend(["**Task/open-loop candidates**", ""])
        lines.extend(f"- {item}" for item in summary.task_candidates)
        lines.append("")
    return "\n".join(lines)


def write_markdown_outputs(summaries: list[ConversationSummary], output: Path) -> None:
    by_date = output / "by-date"
    by_project = output / "by-project"
    indexes = output / "indexes"
    by_date.mkdir(parents=True, exist_ok=True)
    by_project.mkdir(parents=True, exist_ok=True)
    indexes.mkdir(parents=True, exist_ok=True)

    grouped_by_date: dict[str, list[ConversationSummary]] = defaultdict(list)
    grouped_by_project: dict[str, list[ConversationSummary]] = defaultdict(list)
    decisions: list[dict[str, Any]] = []

    for summary in summaries:
        grouped_by_date[date_key(summary.created_at)].append(summary)
        for project in summary.projects:
            grouped_by_project[project].append(summary)
        for decision in summary.decision_candidates:
            decisions.append({"conversation_id": summary.id, "title": summary.title, "created_at": summary.created_at, "projects": summary.projects, "candidate": decision})

    for day, day_summaries in sorted(grouped_by_date.items()):
        text = [
            f"# ChatGPT History Digest — {day}",
            "",
            "Status: generated summary; review before committing.",
            "Visibility: public-safe candidate.",
            "",
            "This file contains redacted summaries and short excerpts, not raw transcripts.",
            "",
        ]
        for summary in sorted(day_summaries, key=lambda s: s.updated_at or s.created_at or ""):
            text.append(render_conversation_card(summary))
        (by_date / f"{day}.md").write_text("\n".join(text).strip() + "\n", encoding="utf-8")

    for project, project_summaries in sorted(grouped_by_project.items()):
        text = [
            f"# ChatGPT History Digest — {project}",
            "",
            "Status: generated summary; review before committing.",
            "Visibility: public-safe candidate.",
            "",
            "Use this as project memory intake, not as source-of-truth for current repo status.",
            "",
        ]
        for summary in sorted(project_summaries, key=lambda s: s.updated_at or s.created_at or ""):
            text.append(render_conversation_card(summary))
        (by_project / f"{project}.md").write_text("\n".join(text).strip() + "\n", encoding="utf-8")

    (indexes / "conversations.json").write_text(json.dumps([asdict(s) for s in summaries], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    project_index = {project: {"conversation_count": len(items), "conversation_ids": [item.id for item in items]} for project, items in sorted(grouped_by_project.items())}
    (indexes / "projects.json").write_text(json.dumps(project_index, indent=2) + "\n", encoding="utf-8")
    (indexes / "decisions.json").write_text(json.dumps(decisions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    review = [
        "# Review Checklist",
        "",
        "Generated ChatGPT history summaries are candidates only.",
        "",
        "Before committing generated outputs:",
        "",
        "- [ ] Confirm no raw export zip or raw transcripts are staged.",
        "- [ ] Search generated files for API keys, tokens, cookies, passwords, and `.env` content.",
        "- [ ] Search generated files for private operational details and sensitive local paths.",
        "- [ ] Remove or rewrite anything that should remain private.",
        "- [ ] Confirm repo/PR status claims against GitHub before treating them as current.",
        "- [ ] Commit only public-safe markdown/index outputs.",
        "",
        "Suggested scans:",
        "",
        "```bash",
        "grep -RniE 'sk-|ghp_|github_pat_|AKIA|BEGIN .*PRIVATE KEY|password|api[_-]?key|token|secret|\\.env' 99-System/Memory/ChatGPT-History/generated || true",
        "```",
        "",
    ]
    (output / "REVIEW_CHECKLIST.md").write_text("\n".join(review), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate KnowledgeVault digests from ChatGPT export data.")
    parser.add_argument("--input", required=True, help="Path to export zip, extracted export dir, conversations.json, or manual text path.")
    parser.add_argument("--output", required=True, help="Output directory for generated digests.")
    parser.add_argument("--manual-text", action="store_true", help="Treat input as manual .txt/.md batch files instead of ChatGPT export JSON.")
    parser.add_argument("--max-conversations", type=int, default=None, help="Limit imported conversations for test runs.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not input_path.exists():
        raise SystemExit(f"Input path not found: {input_path}")

    conversations = parse_manual_text(input_path) if args.manual_text else parse_chatgpt_export(load_json_from_input(input_path))
    conversations = [c for c in conversations if c.messages]
    conversations.sort(key=lambda c: c.updated_at or c.created_at or "")
    if args.max_conversations is not None:
        conversations = conversations[: args.max_conversations]

    summaries = [summarize(c) for c in conversations]
    write_markdown_outputs(summaries, output)
    print(f"Generated {len(summaries)} conversation summaries in {output}")
    print("Review generated outputs before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
