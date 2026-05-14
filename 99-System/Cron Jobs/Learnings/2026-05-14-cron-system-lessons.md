# Cron System Lessons — 2026-05-14

## Durable Lessons

- Recurring jobs need job cards, not only one-off receipts.
- Skill activation must be verified locally, not assumed from repo commits.
- Long skill names can visually truncate in Rich tables, so bare-name dry-run markers are important.
- Public/repo-stored receipts must sanitize local paths and avoid cookie/token/auth implementation details.
- External-action jobs should stop after one packet/action and return receipts before continuing.
- Market/sports jobs must remain educational and manual-review only.
- Trend/devrel jobs must remain draft-only until explicit approval.

## Operational Pattern

Every cron job should write three layers:

1. Run receipt — what happened today.
2. Learning note — what should persist beyond today.
3. Next plan — what the next run should do differently or continue.

## Safety Pattern

Default job mode should be read-only unless the job card explicitly says otherwise.

Any external action job needs:

- exact target;
- exact approval phrase;
- route wording safe for public receipts;
- no route hammering;
- one-action stop condition;
- before/after verification;
- uncertainty labels.
