# Next Cron Plans — 2026-05-14

## Priority 1 — Confirm Activated Skills on Next Runs

On 2026-05-15, verify the scheduled jobs explicitly report:

```txt
Active skill used: x-trend-devrel-intelligence
Active skill used: market-sports-trend-intelligence
```

## Priority 2 — Update Job Cards After Each Run

Each recurring run should update its job card with:

- latest receipt path;
- new durable lesson;
- next planned action;
- any source/risk/route uncertainty.

## Priority 3 — Build Daily Learning Summaries

Hermes should create daily summaries in:

```txt
99-System/Cron Jobs/Learnings/
```

Each summary should answer:

- What did the jobs learn today?
- Which facts were source-backed?
- Which claims need verification?
- What should become content?
- What should become a new skill?
- What should be ignored?

## Priority 4 — Turn Useful Signals Into Content

Daily scans should produce content candidates, not automatic publishing.

Preferred content flow:

```txt
trend -> brief -> post draft -> queue/hash -> explicit approval -> publish -> receipt
```

## Priority 5 — Keep Risky Domains Manual

Market/sports jobs can produce:

- educational briefs;
- watchlists;
- no-action cases;
- risk notes;
- content drafts;
- manual-review packets.

They must not produce automatic trading/betting actions.

## Priority 6 — Build Monthly Cron Review

At the end of each month, Hermes should create:

```txt
99-System/Cron Jobs/Learnings/YYYY-MM-monthly-cron-review.md
```

Include:

- jobs run;
- outputs produced;
- best trends discovered;
- content published;
- skills improved;
- failures or blocked routes;
- next-month changes.
