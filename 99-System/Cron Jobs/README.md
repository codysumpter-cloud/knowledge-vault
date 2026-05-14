# Cron Jobs

Status: Active operating index for Hermes/Buddy recurring jobs.

## Purpose

This folder gives Hermes, Buddy-Agent, and Prismtek a durable place to look back on recurring jobs, what they have learned, what they produced, what failed, and what should happen next.

Use this folder for:

- recurring job inventory;
- daily scan notes;
- trend and market intelligence summaries;
- content sprint job receipts;
- next-action planning;
- recurring skill improvement ideas;
- failure/uncertainty logs;
- job safety boundaries.

## Folder Map

```txt
99-System/Cron Jobs/
  README.md
  Cron Job Index.md
  Jobs/
  Runs/
  Learnings/
  Next Plans/
  Templates/
```

## Operating Rules

Every recurring or scheduled job should have:

1. a job card in `Jobs/`;
2. run receipts in `Runs/`;
3. durable lessons in `Learnings/`;
4. planned next actions in `Next Plans/`;
5. safety and approval boundaries listed clearly.

## Safety Defaults

Recurring jobs are read-only unless explicitly approved otherwise.

Blocked by default:

- publishing;
- social engagement;
- DMs;
- trades;
- bets;
- broker/sportsbook/wallet access;
- repo mutation;
- credential handling;
- destructive memory changes.

Any external-action job must write receipts and stop on route/auth/platform friction.
