# Cron Job Index

Last updated: 2026-05-14

## Purpose

Central index of active Hermes/Buddy recurring jobs, scheduled jobs, and automation loops.

## Active Jobs

| Job ID | Name | Schedule | Mode | Primary Skills | Status | Job Card |
|---|---|---:|---|---|---|---|
| `b570a09a0d62` | Prismtek daily trend + devrel scan | Daily 08:00 EDT | Read-only research + KnowledgeVault writes | `x-trend-devrel-intelligence`, `hermes-x-insights-analyst`, `content-growth-social-ops` | Active | `Jobs/b570a09a0d62-prismtek-daily-trend-devrel-scan.md` |
| `c41254da025e` | Prismtek daily market + sports trend intelligence | Daily 08:20 EDT | Read-only educational + manual-review only | `market-sports-trend-intelligence`, `sportsbook-betting-advisor`, `bettingai-model-advisor`, `content-growth-social-ops` | Active | `Jobs/c41254da025e-prismtek-daily-market-sports-trend-intelligence.md` |
| `6995ca3faf0b` | Scheduled X publish packet | One-shot 2026-05-14 09:11 EDT | External action, one packet only | `signed-in-safari-social-automation`, `content-growth-social-ops` | Scheduled / one-shot | `Jobs/6995ca3faf0b-scheduled-x-publish-packet.md` |

## Required Update Cadence

Hermes should update this index whenever:

- a cron job is created;
- a cron job is disabled;
- a schedule changes;
- a job's active skills change;
- a job produces a major receipt;
- a recurring job fails or hits a safety boundary.

## Current Watch Items

- Confirm the 2026-05-15 runs explicitly report the newly activated native skills.
- Confirm the one-shot X publish job stops after exactly one packet.
- Keep market/sports scan educational and manual-review only.
- Keep all social engagement approval-gated.
