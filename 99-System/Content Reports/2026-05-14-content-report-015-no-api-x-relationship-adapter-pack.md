# Content Report 015 — No-API X Relationship Adapter Pack

Date: 2026-05-14  
Status: Built / Stored in KnowledgeVault PR Branch

## Summary

A no-API X relationship automation implementation pack was created in KnowledgeVault so Hermes can reduce dependency on paid X API credits. The pack is designed for local Hermes activation and focuses on relationship detection, manual seed fallback, receipts, dedupe, reply drafting, and approval-gated engagement.

The adapter avoids storing raw credentials and treats X API as optional rather than required.

## Root Path

```txt
KnowledgeVault/99-System/Social Automation/No-API X Relationship Adapter/
```

## Files Created

```txt
README.md
route-matrix.json
scripts/prismtek_social_no_api_adapter.py
runbooks/Hermes Activation Runbook.md
runbooks/Local Mac Access Checklist.md
templates/relationship-receipt.template.json
templates/reply-draft.template.md
```

## Core Commands Provided

```bash
prismtek-social-no-api status

prismtek-social-no-api retweet-seed \
  --source-post-url <url> \
  --retweeter-handle <handle> \
  --write-receipt

prismtek-social-no-api relationship-draft \
  --receipt-id <receipt-id> \
  --write-receipt

prismtek-social-no-api notification-scan \
  --write-receipt
```

## Route Matrix

The adapter prioritizes:

1. signed-in Safari UI
2. Safari JavaScript / bookmarklet route
3. screenshot / vision read
4. accessibility click/type
5. signed-in local web-session fallback
6. manual seed fallback
7. X API optional

X API must never be the only route. If the API returns `CreditsDepleted`, Hermes should continue with local browser routes or manual seed fallback.

## Safety Posture

Allowed automatically:

- read/seed relationship events;
- classify candidates;
- dedupe;
- write receipts;
- draft replies;
- draft DMs;
- queue approval packets.

Requires approval:

- replies;
- DMs;
- follows;
- quote posts;
- reposts;
- mentions/tags;
- promotional CTAs.

Blocked:

- CAPTCHA/MFA/account-lock bypass;
- platform-limit bypass;
- aggressive retries;
- raw token/cookie export into KnowledgeVault;
- mass replies;
- mass DMs;
- identical CTA repetition;
- fake personalization;
- harassment/dogpiling.

## Known Limitation

The included Python adapter implements manual seed, receipts, reply drafts, status, and placeholder notification-scan receipt generation. The actual Safari/screenshot/browser-control notification scanning must be wired locally inside Hermes where Mac browser/screen tools are available.

## Next Move

Hermes should copy the adapter into local `.hermes` script/bin paths, verify `status`, seed the known `@legitgaran` retweet event, generate a relationship receipt and reply draft, then update the retweet relationship cron job to prefer local/browser/manual routes before X API.
