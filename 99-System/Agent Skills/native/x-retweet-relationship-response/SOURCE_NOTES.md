# X Retweet Relationship Response — Source Notes

Date: 2026-05-14  
Status: Added as native Buddy/Hermes skill candidate

## Purpose

Create a safe relationship-building response skill for Prismtek when X posts receive reposts/retweets. The skill should help thank real supporters, identify aligned builders, draft thoughtful replies, and create KnowledgeVault relationship notes.

## Core Behavior

When Prismtek receives a retweet/repost, the skill should:

1. Detect the repost event.
2. Identify the retweeter.
3. Inspect only public context.
4. Classify the account.
5. Deduplicate against prior receipts.
6. Choose the lowest-risk useful response.
7. Write a KnowledgeVault relationship receipt.
8. Draft a reply or outreach message when appropriate.
9. Require explicit approval before public replies, DMs, follows, quote posts, or mentions.

## Recommended Response Ladder

### Level 0 — Receipt Only

Use for unknown, low-context, suspicious, or spammy accounts.

### Level 1 — Like Only

Use for legitimate retweets with no strong relationship signal. This may be automated only if explicitly enabled and rate-limited.

### Level 2 — Thank-You Reply Draft

Use for relevant builder/creator/community accounts. Queue for approval.

### Level 3 — Relationship Outreach Draft

Use for strong potential collaborators. Create a relationship note, public reply draft, and optional DM draft. Approval required.

## Safety Boundary

This is not a spam bot.

Allowed automatically after user enables:

- read retweet events;
- classify retweeters;
- create KnowledgeVault notes;
- create reply/DM drafts;
- optionally like once per retweeter/post pair if configured and healthy.

Requires explicit approval by default:

- reply;
- quote post;
- mention/tag;
- DM;
- follow;
- repost;
- publish a promotional CTA.

Blocked:

- mass replies;
- mass likes;
- mass DMs;
- identical generic replies under every repost;
- fake personalization;
- duplicate replies to the same retweeter/post pair;
- aggressive retries after platform friction;
- outreach to suspicious/spam accounts;
- claiming relationships that do not exist.

## Recommended Safety Caps

- Max auto-likes per day: 10
- Max queued reply drafts per day: 10
- Max approved published replies per day: 3
- Max DMs per day: 0 by default
- Minimum delay between engagement actions: 20 minutes
- Stop immediately on auth, friction, suspicious-activity, or platform-limit errors

## KnowledgeVault Targets

```txt
KnowledgeVault/50 - Content/x-relationship-receipts/
KnowledgeVault/50 - Content/outreach-drafts/
KnowledgeVault/50 - Content/post-ideas/
KnowledgeVault/99-System/Cron Jobs/Runs/
KnowledgeVault/99-System/Cron Jobs/Learnings/
KnowledgeVault/99-System/Cron Jobs/Next Plans/
```

## Preferred Copy Style

Human, short, and specific.

Good:

```txt
Appreciate the repost — building this in public so the receipts stay visible.
```

```txt
Thanks for sharing this. Prismtek is focused on the memory + execution layer for useful agents.
```

```txt
Appreciate you boosting this. If local-first agents / durable memory are your lane too, I’d be glad to compare notes.
```

Avoid repeating this generically under every retweet:

```txt
Thanks for the repost! DM me if you want to work together!
```

## Activation Note

Promote/install this skill locally before enabling any retweet response cron job. Verify bare-name load:

```txt
/skill x-retweet-relationship-response
```
