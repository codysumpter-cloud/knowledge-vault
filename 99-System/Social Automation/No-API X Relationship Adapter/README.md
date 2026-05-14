# No-API X Relationship Adapter

Status: implementation pack for Hermes local activation  
Created: 2026-05-14

## Purpose

Avoid paid X API dependency for Prismtek relationship automation by using local signed-in browser/session routes, manual seed fallback, receipts, dedupe, and approval-gated public actions.

This adapter is designed for:

- retweet/repost detection;
- reply/mention detection;
- relationship receipts;
- account classification;
- thank-you reply drafts;
- optional capped likes;
- approval-gated replies/DMs/follows/quotes.

It is not designed for spam, mass replies, mass DMs, stealth automation, or bypassing platform protections.

## Route Matrix

Preferred read/action routes:

1. `signed_in_safari_ui`
2. `safari_javascript_bookmarklet`
3. `screenshot_vision_read`
4. `accessibility_click_type`
5. `signed_in_web_session_graphql`
6. `manual_seed_fallback`
7. `x_api_optional`

X API must never be the only route. If X API returns `CreditsDepleted`, the adapter should continue to signed-in browser routes or manual seed fallback.

## Safety Boundary

Allowed automatically:

- read notifications through approved local routes;
- seed known retweet events manually;
- classify relationship candidates;
- dedupe events;
- write receipts;
- draft replies;
- draft DMs;
- queue approval packets.

Optional, if explicitly enabled:

- like one legitimate retweet/reply under strict caps.

Requires approval:

- replies;
- DMs;
- follows;
- quote posts;
- reposts;
- mentions/tags;
- promotional CTAs.

Blocked:

- CAPTCHA/MFA/lock bypass;
- platform-limit bypass;
- aggressive retries;
- raw cookie/token export into KnowledgeVault;
- mass replies;
- mass DMs;
- identical CTA under every retweet;
- outreach to suspicious/spam accounts;
- pretending a relationship exists.

## Core Workflow

```txt
engagement signal
  -> route-specific scan
  -> retweeter/replier identity
  -> dedupe by source_post_id + actor_handle + action_type
  -> classify account
  -> write relationship receipt
  -> draft response
  -> queue action packet
  -> explicit approval
  -> publish/like/reply through local route
  -> receipt
```

## Included Files

```txt
README.md
route-matrix.json
scripts/prismtek_social_no_api_adapter.py
runbooks/Hermes Activation Runbook.md
runbooks/Mac Permissions Checklist.md
runbooks/Retweet Relationship Cron Job.md
templates/relationship-receipt.template.json
templates/reply-draft.template.md
```

## Local Activation Summary

Hermes should copy the Python adapter to a local executable path, for example:

```txt
~/.hermes/scripts/prismtek_social_no_api_adapter.py
~/.hermes/bin/prismtek-social-no-api
```

Then activate commands:

```bash
prismtek-social-no-api retweet-seed \
  --source-post-url <url> \
  --retweeter-handle <handle> \
  --write-receipt

prismtek-social-no-api relationship-draft \
  --receipt-id <receipt-id> \
  --write-receipt
```

## First Use for @legitgaran

Manual seed fallback should be used because X API read/search is unavailable:

```bash
prismtek-social-no-api retweet-seed \
  --source-post-url <Prismtek source post URL> \
  --retweeter-handle legitgaran \
  --write-receipt
```

Then draft a reply:

```bash
prismtek-social-no-api relationship-draft \
  --receipt-id <receipt-id> \
  --write-receipt
```

Suggested reply:

```txt
Appreciate the repost @legitgaran — building Prismtek in public so the memory, execution, and receipt layer stays visible.

If agent workflows are your lane too, happy to compare notes.
```

Do not publish until exact text/hash is approved.
