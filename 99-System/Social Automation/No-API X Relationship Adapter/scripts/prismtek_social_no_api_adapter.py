#!/usr/bin/env python3
"""
Prismtek No-API X Relationship Adapter

Purpose:
  Avoid paid X API dependency for relationship automation by using manual seed,
  local browser/session routes, receipts, dedupe, and approval-gated actions.

This scaffold is safe-by-default:
  - no token/cookie storage;
  - no automatic replies/DMs/follows;
  - no CAPTCHA/MFA/platform-limit bypass;
  - writes receipts and reply drafts only unless explicitly approved.

Install example:
  cp prismtek_social_no_api_adapter.py ~/.hermes/scripts/
  ln -sf ~/.hermes/scripts/prismtek_social_no_api_adapter.py ~/.hermes/bin/prismtek-social-no-api
  chmod +x ~/.hermes/scripts/prismtek_social_no_api_adapter.py
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

DEFAULT_KV_ROOT = Path(os.environ.get("KNOWLEDGEVAULT_PATH", "KnowledgeVault"))
REL_RECEIPTS = Path("50 - Content/x-relationship-receipts")
OUTREACH = Path("50 - Content/outreach-drafts")
CRON_RUNS = Path("99-System/Cron Jobs/Runs")

SAFE_ROUTE_NAMES = {
    "manual_seed_fallback",
    "signed_in_safari_ui",
    "safari_javascript_bookmarklet",
    "screenshot_vision_read",
    "accessibility_click_type",
    "signed_in_web_session_graphql",
    "x_api_optional",
}

@dataclasses.dataclass
class RelationshipEvent:
    source_post_url: str
    actor_handle: str
    event_type: str = "retweet"
    source_post_id: Optional[str] = None
    detected_route: str = "manual_seed_fallback"
    detected_at: str = dataclasses.field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    classification: str = "unknown"
    risk_level: str = "review"
    notes: str = ""

    @property
    def dedupe_key(self) -> str:
        post = self.source_post_id or extract_post_id(self.source_post_url) or stable_slug(self.source_post_url)
        handle = normalize_handle(self.actor_handle)
        return f"{post}:{handle}:{self.event_type}"

    @property
    def receipt_id(self) -> str:
        digest = sha256_text(self.dedupe_key)[:12]
        return f"{timestamp_slug()}-{self.event_type}-{normalize_handle(self.actor_handle)}-{digest}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H%M")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-")[:40] or "unknown"


def normalize_handle(handle: str) -> str:
    handle = handle.strip()
    if handle.startswith("@"):
        handle = handle[1:]
    return re.sub(r"[^A-Za-z0-9_]", "", handle).lower()


def extract_post_id(url: str) -> Optional[str]:
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None


def ensure_dirs(kv_root: Path) -> None:
    for rel in [REL_RECEIPTS, OUTREACH, CRON_RUNS]:
        (kv_root / rel).mkdir(parents=True, exist_ok=True)


def sanitize_route(route: str) -> str:
    if route not in SAFE_ROUTE_NAMES:
        return "unknown_safe_route"
    if route == "signed_in_web_session_graphql":
        return "signed-in local web-session fallback"
    if route == "signed_in_safari_ui":
        return "signed-in Safari UI"
    if route == "manual_seed_fallback":
        return "manual seed fallback"
    if route == "screenshot_vision_read":
        return "screenshot/vision read"
    if route == "x_api_optional":
        return "X API optional"
    return route.replace("_", "-")


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def receipt_path(kv_root: Path, receipt_id: str) -> Path:
    return kv_root / REL_RECEIPTS / f"{receipt_id}.json"


def draft_path(kv_root: Path, receipt_id: str) -> Path:
    return kv_root / OUTREACH / f"{receipt_id}-reply-draft.md"


def classify_actor(handle: str, profile_summary: str = "") -> Dict[str, str]:
    """Simple deterministic classifier. Hermes can replace/enrich this with visible profile context."""
    h = normalize_handle(handle)
    text = f"{h} {profile_summary}".lower()
    suspicious_terms = ["giveaway", "airdrop", "casino", "promo", "onlyfans", "100x", "pump"]
    builder_terms = ["dev", "engineer", "builder", "ai", "agent", "founder", "open source", "tools", "software"]
    if any(t in text for t in suspicious_terms):
        return {"classification": "suspicious_or_low_quality", "risk_level": "high"}
    if any(t in text for t in builder_terms):
        return {"classification": "builder_or_ai_tools", "risk_level": "normal"}
    return {"classification": "unknown_or_low_context", "risk_level": "review"}


def create_relationship_receipt(kv_root: Path, event: RelationshipEvent, profile_summary: str = "") -> Path:
    ensure_dirs(kv_root)
    cls = classify_actor(event.actor_handle, profile_summary)
    event.classification = cls["classification"]
    event.risk_level = cls["risk_level"]
    rid = event.receipt_id
    path = receipt_path(kv_root, rid)
    existing = path.exists()
    payload = {
        "receipt_id": rid,
        "created_at": now_iso(),
        "source_post_url": event.source_post_url,
        "source_post_id": event.source_post_id or extract_post_id(event.source_post_url),
        "actor_handle": normalize_handle(event.actor_handle),
        "event_type": event.event_type,
        "dedupe_key": event.dedupe_key,
        "duplicate_existing_receipt": existing,
        "detected_route": sanitize_route(event.detected_route),
        "classification": event.classification,
        "risk_level": event.risk_level,
        "profile_summary": profile_summary,
        "actions": {
            "external_action_taken": False,
            "like_taken": False,
            "reply_published": False,
            "dm_sent": False,
            "followed": False
        },
        "approval_required_for": ["reply", "dm", "follow", "quote", "repost", "mention_tag"],
        "notes": event.notes,
        "uncertainty": "Manual seed or browser-read events should be verified against visible X UI when possible."
    }
    write_json(path, payload)
    return path


def build_reply_text(handle: str, style: str = "compare_notes") -> str:
    handle = "@" + normalize_handle(handle)
    if style == "short":
        return f"Appreciate the repost {handle} — building this in public so the receipts stay visible."
    if style == "dm_open":
        return (
            f"Appreciate the repost {handle}.\n\n"
            "I’m building Prismtek around durable agent memory, guarded execution, and receipts.\n\n"
            "If you’re exploring agent workflows or want to compare notes, DMs are open."
        )
    return (
        f"Appreciate the repost {handle} — building Prismtek in public so the memory, "
        "execution, and receipt layer stays visible.\n\n"
        "If agent workflows are your lane too, happy to compare notes."
    )


def create_reply_draft(kv_root: Path, receipt_id: str, style: str = "compare_notes") -> Path:
    ensure_dirs(kv_root)
    rpath = receipt_path(kv_root, receipt_id)
    receipt = read_json(rpath)
    if not receipt:
        raise SystemExit(f"No relationship receipt found for receipt_id={receipt_id}")
    handle = receipt.get("actor_handle", "unknown")
    text = build_reply_text(handle, style=style)
    digest = sha256_text(text)
    out = draft_path(kv_root, receipt_id)
    md = f"""# X Retweet Reply Draft

Receipt ID: `{receipt_id}`  
Created: {now_iso()}  
Status: queued / approval required

## Source

- Source post: {receipt.get('source_post_url')}
- Retweeter: @{handle}
- Classification: {receipt.get('classification')}
- Risk level: {receipt.get('risk_level')}

## Exact Reply Text

```txt
{text}
```

## SHA256

```txt
{digest}
```

## Approval Phrase

```txt
GO X REPLY RETWEET {receipt_id}
```

## Safety

- Do not publish without exact hash approval.
- Do not DM automatically.
- Do not follow automatically.
- Do not repeat identical CTA replies.
"""
    out.write_text(md)
    receipt.setdefault("drafts", {})["reply_draft_path"] = str(out)
    receipt["drafts"]["reply_text_sha256"] = digest
    receipt["drafts"]["approval_phrase"] = f"GO X REPLY RETWEET {receipt_id}"
    write_json(rpath, receipt)
    return out


def cmd_retweet_seed(args: argparse.Namespace) -> int:
    kv = Path(args.kv_root)
    event = RelationshipEvent(
        source_post_url=args.source_post_url,
        actor_handle=args.retweeter_handle,
        event_type=args.event_type,
        source_post_id=args.source_post_id or extract_post_id(args.source_post_url),
        detected_route="manual_seed_fallback",
        notes=args.notes or "Manual seed fallback used because automated X read route was unavailable or insufficient."
    )
    path = create_relationship_receipt(kv, event, profile_summary=args.profile_summary or "")
    print(json.dumps({
        "ok": True,
        "action": "retweet_seed",
        "receipt_id": path.stem,
        "receipt_path": str(path),
        "dedupe_key": event.dedupe_key,
        "route": "manual seed fallback"
    }, indent=2))
    return 0


def cmd_relationship_draft(args: argparse.Namespace) -> int:
    kv = Path(args.kv_root)
    path = create_reply_draft(kv, args.receipt_id, style=args.style)
    text = path.read_text()
    digest_match = re.search(r"## SHA256\n\n```txt\n([a-f0-9]+)\n```", text)
    print(json.dumps({
        "ok": True,
        "action": "relationship_draft",
        "draft_path": str(path),
        "receipt_id": args.receipt_id,
        "sha256": digest_match.group(1) if digest_match else None,
        "approval_phrase": f"GO X REPLY RETWEET {args.receipt_id}"
    }, indent=2))
    return 0


def cmd_notification_scan(args: argparse.Namespace) -> int:
    # Placeholder for Hermes local browser implementation.
    # This command intentionally does not use X API. Hermes should wire this to Safari/screenshot/vision locally.
    kv = Path(args.kv_root)
    ensure_dirs(kv)
    rid = f"{timestamp_slug()}-notification-scan-placeholder"
    path = kv / CRON_RUNS / f"{rid}.json"
    payload = {
        "receipt_id": rid,
        "created_at": now_iso(),
        "status": "placeholder_no_external_action",
        "route_matrix": [
            "signed-in Safari UI",
            "screenshot/vision read",
            "manual seed fallback",
            "X API optional"
        ],
        "new_relationship_events": [],
        "notes": "Hermes should implement local Safari/screenshot notification scanning in its Mac runtime. No X API used here."
    }
    write_json(path, payload)
    print(json.dumps({"ok": True, "receipt_path": str(path), "new_relationship_events": []}, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    payload = {
        "ok": True,
        "adapter": "Prismtek No-API X Relationship Adapter",
        "safe_by_default": True,
        "x_api_required": False,
        "commands": ["retweet-seed", "relationship-draft", "notification-scan", "status"],
        "blocked": ["auto-reply", "auto-DM", "MFA bypass", "CAPTCHA bypass", "platform-limit bypass"],
    }
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Prismtek No-API X Relationship Adapter")
    p.add_argument("--kv-root", default=str(DEFAULT_KV_ROOT), help="KnowledgeVault root path")
    sub = p.add_subparsers(dest="cmd", required=True)

    seed = sub.add_parser("retweet-seed", help="Manually seed a retweet/repost relationship event")
    seed.add_argument("--source-post-url", required=True)
    seed.add_argument("--retweeter-handle", required=True)
    seed.add_argument("--source-post-id")
    seed.add_argument("--event-type", default="retweet", choices=["retweet", "quote", "reply", "mention"])
    seed.add_argument("--profile-summary")
    seed.add_argument("--notes")
    seed.add_argument("--write-receipt", action="store_true")
    seed.set_defaults(func=cmd_retweet_seed)

    draft = sub.add_parser("relationship-draft", help="Create a thank-you reply draft from a relationship receipt")
    draft.add_argument("--receipt-id", required=True)
    draft.add_argument("--style", choices=["compare_notes", "short", "dm_open"], default="compare_notes")
    draft.add_argument("--write-receipt", action="store_true")
    draft.set_defaults(func=cmd_relationship_draft)

    scan = sub.add_parser("notification-scan", help="Placeholder local notification scan receipt without X API")
    scan.add_argument("--write-receipt", action="store_true")
    scan.set_defaults(func=cmd_notification_scan)

    status = sub.add_parser("status", help="Show adapter status")
    status.set_defaults(func=cmd_status)
    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
