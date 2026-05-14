# Prismtek X Autonomous Relationship Mode v1

Status: proposed/guarded autonomous mode  
Created: 2026-05-14

## Purpose

Automate Prismtek X relationship handling as much as safely possible without relying on paid X API credits, while preventing spam patterns, account damage, duplicate replies, and platform-friction escalation.

This mode is designed for autonomous relationship intelligence and limited low-risk engagement. It is not an unbounded posting, DM, follow, or reply bot.

## Context

The user wants high automation and notifications when things happen. X recently returned automation challenge code `226`, so autonomous writes must be limited and must stop on friction.

Core principle:

```txt
Automate detection, memory, classification, receipts, drafting, and low-risk acknowledgements.
Limit autonomous public writes.
Keep high-risk actions approval-gated.
```

## Tools / Skills

Use:

- `x-retweet-relationship-response`
- `x-trend-devrel-intelligence`
- `content-growth-social-ops`
- `signed-in-safari-social-automation`
- No-API X Relationship Adapter
- `prismtek-social`
- local signed-in Safari/browser routes
- manual seed fallback
- KnowledgeVault receipts

Do not rely on paid X API. X API is optional only. If X API returns `CreditsDepleted`, continue with browser/manual routes.

## Autonomous Allowed Actions

### 1. Read / Scan

Hermes may autonomously:

- scan X notifications;
- scan recent Prismtek posts;
- detect retweets/reposts;
- detect replies;
- detect mentions;
- detect quote posts if visible;
- use signed-in Safari/browser routes;
- use screenshot/vision read;
- use manual seed fallback.

### 2. Memory

Hermes may autonomously:

- write relationship receipts;
- write run receipts;
- update `_seen.json`;
- update Cron Jobs Runs/Learnings/Next Plans;
- classify accounts;
- track repeated supporters;
- track suspicious/low-quality accounts;
- track possible collaborators.

### 3. Drafting

Hermes may autonomously:

- draft thank-you replies;
- draft optional DMs;
- draft follow-up posts;
- draft relationship notes;
- draft collaboration suggestions;
- create approval packets.

### 4. Low-Risk Engagement

Hermes may autonomously like legitimate retweets/replies only if all safety checks pass.

Caps:

- max auto-likes/day: 10;
- minimum 20 minutes between auto-likes;
- dedupe by `source_post_id + actor_handle + action_type`;
- never like suspicious/spam accounts;
- stop on any X friction/challenge state.

## Limited Autonomous Replies

Autonomous reply is allowed only when **all** conditions pass:

- X has no active code `226`, code `344`, auth, challenge, or friction state;
- account is classified as real/legitimate;
- account is not suspicious, spam, scam, adult, pump, gambling, or ragebait;
- profile context is visible enough to personalize lightly;
- retweeter/replier is relevant or neutral-positive;
- no previous reply to same actor/source pair;
- no duplicate or near-duplicate reply text;
- reply is short, human, and non-pushy;
- no more than 3 autonomous replies per day;
- at least 30 minutes since previous autonomous reply;
- reply does not contain hard sell, repeated CTA, or generic `DM me` spam;
- exact reply text is stored with SHA256 before publish;
- receipt path is ready;
- direct control route is currently healthy.

## Approved Autonomous Reply Styles

Style A:

```txt
Appreciate the boost @handle — building Prismtek in public so the work stays visible and accountable.
```

Style B:

```txt
Thanks for sharing this @handle. Prismtek is focused on durable agent memory, guarded execution, and receipts.
```

Style C:

```txt
Appreciate it @handle. If local-first agents or workflow automation are your lane too, happy to compare notes.
```

## Avoid

Do not autonomously publish:

- `DM me if you want to work together` as a repeated generic CTA;
- repeated identical replies;
- salesy phrasing;
- fake familiarity;
- claims of partnership;
- hype language;
- aggressive tagging.

## Approval Required

Do not do these without explicit approval:

- DMs;
- follows;
- quote posts;
- reposts;
- paid boosts;
- tagging/mentioning someone in standalone posts;
- replying after any active X automation challenge;
- replying to controversial/risky accounts;
- replying with a work-together CTA;
- publishing more than 3 relationship replies/day;
- deleting posts/replies;
- changing profile settings.

## Stop Conditions

Immediately stop all autonomous writes if any occurs:

- X code `226`;
- X code `344`;
- `CreditsDepleted` on API route plus browser route instability;
- login challenge;
- MFA;
- CAPTCHA;
- suspicious activity screen;
- account lock/warning;
- unexpected composer state;
- duplicate detection failure;
- receipt write failure;
- more than one route failure in a row;
- user says stop.

When stopped:

- continue read-only scans if safe;
- continue drafting;
- continue receipts;
- notify Prismtek;
- recommend manual-assisted path.

## Notification Requirements

Notify Prismtek when:

- a retweet/repost is detected;
- someone relevant replies;
- a potential collaborator is found;
- an autonomous like is taken;
- an autonomous reply is published;
- an action is blocked;
- X returns friction/challenge;
- daily caps are reached;
- a reply/DM/follow needs approval.

Each notification must include:

- actor handle;
- source post;
- event type;
- classification;
- action taken;
- receipt path;
- next suggested action.

## Cron Behavior

Create or update job:

```txt
prismtek-x-relationship-autopilot
```

Recommended schedule:

```txt
every 2 hours during active posting windows
```

Do not run at the same time as:

- X autopublisher;
- YouTube upload jobs;
- market/sports scans;
- heavy browser-control jobs.

Stagger by at least 15 minutes from other browser jobs.

Performance requirements:

- lightweight scan first;
- no heavy screenshots unless needed;
- no more than one browser-control job at once;
- MacBook is a 2018 Intel 8 GB RAM machine, so avoid concurrent heavy jobs;
- future target is VPS for recurring scans and automation.

## KnowledgeVault Paths

Relationship receipts:

```txt
KnowledgeVault/50 - Content/x-relationship-receipts/
```

Outreach drafts:

```txt
KnowledgeVault/50 - Content/outreach-drafts/
```

Cron runs:

```txt
KnowledgeVault/99-System/Cron Jobs/Runs/
```

Learnings:

```txt
KnowledgeVault/99-System/Cron Jobs/Learnings/
```

Next plans:

```txt
KnowledgeVault/99-System/Cron Jobs/Next Plans/
```

## Required Updates

Hermes should update:

- Cron Job Index;
- relationship autopilot job card;
- next plan;
- safety policy note;
- daily cap counters;
- friction state tracker.

## @legitgaran Handling

For `@legitgaran`:

1. Verify whether the reply already exists.
2. If not, check whether autonomous reply conditions pass.
3. Because X recently returned code `226`, do **not** auto-publish if challenge state is still active.
4. If challenge state is clear, publish only if within autonomous reply caps.
5. Otherwise prepare manual-assisted composer and notify Prismtek.

Known queued reply:

```txt
Appreciate the repost @legitgaran — building Prismtek in public so the memory, execution, and receipt layer stays visible.

If agent workflows are your lane too, happy to compare notes.
```

Known SHA256:

```txt
75840ce2f4add685e727f99afddc2ac4c568631a76aceb630dc68b8788390ef8
```

## Recommended Today Mode

Because X recently returned code `226`:

```txt
auto-read: on
auto-receipts: on
auto-drafts: on
auto-likes: paused or 1 test max
auto-replies: paused
auto-DMs: off
```

After X friction clears:

```txt
auto-likes: on, capped
auto-replies: 1/day test
auto-DMs: off
```

After 7 clean days:

```txt
auto-likes: 10/day
auto-replies: 3/day
auto-DMs: approval-gated
```

## Success Criteria

The mode is working if Hermes can:

- detect relationship events without X API credits;
- write receipts and dedupe correctly;
- classify actors correctly;
- draft useful responses;
- notify Prismtek;
- perform low-risk likes only within caps;
- stop autonomous writes on platform friction;
- avoid duplicate/promotional/spammy replies.
