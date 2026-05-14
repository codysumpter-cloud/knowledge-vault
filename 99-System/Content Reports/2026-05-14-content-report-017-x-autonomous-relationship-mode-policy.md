# Content Report 017 — X Autonomous Relationship Mode Policy

Date: 2026-05-14  
Status: Added to GitHub KnowledgeVault Branch

## Summary

Prismtek X Autonomous Relationship Mode v1 was added to the KnowledgeVault GitHub branch. The policy codifies high automation for relationship intelligence while limiting public writes after X recently returned automation challenge code `226`.

## Files Added

Runbook:

```txt
99-System/Social Automation/No-API X Relationship Adapter/runbooks/Prismtek X Autonomous Relationship Mode V1.md
```

Machine-readable policy:

```txt
99-System/Social Automation/No-API X Relationship Adapter/autonomous-mode-policy.json
```

## Core Principle

```txt
Automate detection, memory, classification, receipts, drafting, and low-risk acknowledgements.
Limit autonomous public writes.
Keep high-risk actions approval-gated.
```

## Default Mode After X Code 226

```txt
auto-read: on
auto-receipts: on
auto-drafts: on
auto-likes: paused or 1 test max
auto-replies: paused
auto-DMs: off
```

## Fully Autonomous Scope

Hermes may autonomously:

- scan notifications;
- scan recent Prismtek posts;
- detect retweets/reposts;
- detect replies;
- detect mentions;
- detect quote posts if visible;
- classify accounts;
- write relationship receipts;
- write run receipts;
- update `_seen.json`;
- draft replies;
- draft DMs;
- draft follow-up posts;
- create approval packets.

## Limited Autonomous Engagement

Auto-likes are allowed only under strict caps and only for legitimate, non-suspicious accounts.

Autonomous replies are allowed only when all safety conditions pass, including no active X challenge/friction state and no duplicate/near-duplicate reply text.

## Approval Required

Approval remains required for:

- DMs;
- follows;
- quote posts;
- reposts;
- paid boosts;
- work-together CTAs;
- replies after active X automation challenge;
- controversial/risky accounts;
- deleting posts/replies;
- profile changes.

## Stop Conditions

Autonomous writes stop on:

- X code `226`;
- X code `344`;
- login challenge;
- MFA;
- CAPTCHA;
- suspicious-activity screen;
- account lock/warning;
- unexpected composer state;
- duplicate detection failure;
- receipt write failure;
- more than one route failure in a row;
- user says stop.

## Cron Guidance

Job target:

```txt
prismtek-x-relationship-autopilot
```

Schedule:

```txt
every 2 hours during active posting windows
```

Stagger by at least 15 minutes from other browser jobs. Do not overlap with X autopublisher, YouTube uploads, market/sports scans, or heavy browser-control jobs.

Future target: VPS for recurring scans and automation.

## Next Move

Hermes should sync this policy from the GitHub KnowledgeVault branch into the local Obsidian KnowledgeVault, then update or create the `prismtek-x-relationship-autopilot` job using the policy.
