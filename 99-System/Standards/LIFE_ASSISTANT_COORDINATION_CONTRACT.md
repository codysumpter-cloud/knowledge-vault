---
type: integration
status: draft
owner: Prismtek
source_of_truth: knowledge-vault
last_verified: 2026-08-04
risk_level: high
privacy: public
freshness: slow-changing
agent_load: task-specific
tags:
  - life-assistant
  - automation
  - coordination
  - receipts
  - safety
---

# Life Assistant Coordination Contract

## Purpose

This contract coordinates the five-task Prismtek life-assistant loop without treating chat context as durable shared state.

The five tasks are:

1. Prismtek Command Center
2. Daytime Command Watch
3. Prismtek Engineering Watch
4. Knowledge Vault Daily Log
5. Weekly Life & Strategy Loop

The operating loop is:

> Plan → monitor → handle safe work → escalate consequential decisions → record → review → plan again.

## Source-of-truth boundaries

- GitHub is authoritative for repositories, commits, pull requests, issues, checks, workflows, deployments, and releases.
- Connected mail, calendar, finance, weather, and other providers are authoritative for their own current records.
- The private operational ledger is authoritative for cross-task receipts, dedupe keys, task-created object ownership, pending approvals, and carry-forward state.
- KnowledgeVault stores only public-safe architecture, rules, schemas, engineering receipts, and durable public project memory.
- Chat labels and task instructions provide responsibility separation but do not guarantee memory, context, or state isolation.

## Privacy split

### Private operational ledger

The private ledger may contain minimal operational references needed to coordinate family, email, calendar, finance, home, and personal workflows.

It must never contain:

- passwords, authentication tokens, recovery codes, or session material
- full account or card numbers
- raw medical records
- full email bodies or unnecessary private message content
- copied private-repository content
- unnecessary custody, legal, or precise-location detail

Use provider references and concise summaries instead of copying source content.

### Public KnowledgeVault

The public vault may contain:

- this coordination contract
- public-safe receipt schemas and examples
- public GitHub and CI evidence
- public project decisions and status
- redacted aggregate automation health

Personal, family, finance, communication, home, and private-repository details must not be committed.

## Single-owner responsibility map

| Task | Owns | Must not own |
|---|---|---|
| Prismtek Command Center | Daily prioritization, exactly one One Big Win, morning plan, five-task health, daily focus/checklist plan | Routine mail housekeeping, engineering mutations, durable journal writes |
| Daytime Command Watch | Email, calendar, finance, weather, and same-day personal logistics after the morning brief | GitHub repair, CI reruns, daily journaling, weekly strategy |
| Prismtek Engineering Watch | GitHub and CI diagnosis; explicitly authorized low-risk engineering execution | Personal mail/calendar, family planning, durable life journaling |
| Knowledge Vault Daily Log | Receipt ingestion, reconciliation, append-only history, public-safe Vault updates | Planning, inbox operation, engineering repair, creating new life commitments |
| Weekly Life & Strategy Loop | Thursday weekend mission and Sunday weekly objective/reset | Routine inbox work, routine CI operation, rewriting daily history |

A task may report another task's verified result, but it must not duplicate that task's mutation responsibilities.

## Authority matrix

### Allowed without additional approval

- Read and summarize available sources.
- Create a draft response when the recipient, intent, and source thread are unambiguous.
- Perform explicitly allowlisted, reversible personal housekeeping within the owning task's action limits.
- Record verified facts and append receipts.
- Diagnose GitHub or CI failures without mutating a repository.

### Requires explicit approval

- Send, forward, or post communication as the user.
- Purchase, reserve, pay, transfer, subscribe, cancel, or move money.
- RSVP, invite attendees, alter another person's calendar, or cancel shared events.
- Merge, deploy, publish, release, modify protected branches, or alter production systems.
- Change secrets, authentication, permissions, billing, schemas, or destructive migrations.
- Delete important data or make destructive repository changes.
- Mutate a repository without an active autonomy token.

## Engineering autonomy token

Repository mutation is allowed only when a current receipt or direct user instruction provides all of:

- repository
- branch or pull request
- allowed change classes
- maximum file or line budget
- allowed write actions
- expiration
- whether comments, labels, issues, commits, pushes, and workflow reruns are allowed

The token does not authorize merging, deploying, protected-branch writes, secrets, permissions, migrations, destructive changes, or broad architecture work unless the user separately approves those exact actions.

Engineering must also:

- use an isolated worktree or ephemeral clone
- preserve dirty checkouts
- verify the branch head has not changed since diagnosis
- never force-push
- rerun the same failed workflow no more than once for an unchanged commit SHA
- stop when another active lease owns the same repository and branch
- record commands, results, branch, commit SHA, checks, and remaining risk

## Severity model

- `P0`: Safety, security, fraud, or immediate same-day family disruption. Notify immediately.
- `P1`: Action required today or a consequential blocker requiring a decision. Notify promptly.
- `P2`: Important but suitable for the next scheduled briefing.
- `P3`: Informational or historical; record only when useful.

## Confidence model

`high` confidence requires one authoritative source with all required fields or two independent sources that agree.

Treat an item as ambiguous when any required date, time, timezone, location, ownership, sender identity, financial coverage, commit identity, or source evidence is missing or conflicting.

Ambiguous items must not become firm commitments, calendar appointments, financial conclusions, repository mutations, or completion claims.

## Idempotency and ownership

Every proposed or completed mutation must have a stable `dedupe_key`.

Before creating or updating a draft, event, issue, checklist item, receipt, or carry-forward entry:

1. Search the private ledger or provider for the dedupe key.
2. Update the existing task-created object when appropriate.
3. Do not create a duplicate.

Only the task that created a mutable object may later move, remove, or replace it.

Preserve human edits. When a human has edited a task-created object, stop automatic replacement unless the new change is clearly additive, directly supported, and safe.

## Default action limits per run

- Archive no more than 10 obvious promotional messages.
- Never auto-archive direct-human, family, school, legal, medical, security, financial, or account-access mail.
- Create or materially update no more than two private calendar events.
- Never create a firm appointment from incomplete timing.
- Never create duplicate GitHub issues for an existing verified blocker.
- Never rerun the same failed workflow more than once for an unchanged commit SHA.
- Never claim a plan, draft, queued job, attempted fix, or pending check is complete.

## Canonical receipt contract

Each task emits exactly one receipt per run using:

`99-System/Schemas/life-assistant-task-receipt.schema.json`

Receipts are append-only and include:

- unique run ID
- task identity and time window
- source freshness and coverage
- verified facts
- reversible actions and provider object references
- approval requests
- cross-task handoffs
- failures and data gaps
- privacy classification
- overall result

Cross-task handoffs are accepted only when they reference a unique receipt and evidence.

## Handoff rules

A handoff must include:

- destination task
- severity
- stable dedupe key
- concise verified summary
- evidence references
- deadline when applicable
- safe default when no decision arrives

The receiving task acknowledges the handoff in its next receipt. It must not silently reinterpret an ambiguous handoff.

## Reconciliation rules

The Knowledge Vault Daily Log is the only task that reconciles the day's receipts into durable history.

The evening run must:

1. Preserve immutable receipt history.
2. Collapse duplicate carry-forward items by dedupe key.
3. Mark superseded items without deleting prior evidence.
4. Distinguish completed, attempted, blocked, planned, drafted, queued, and merely discussed work.
5. Keep private facts in the private ledger.
6. Emit only public-safe project events to KnowledgeVault or Vegapunk Brain.

## Notification rules

- Notify for `P0` and `P1` findings.
- Include `P2` findings in the next appropriate briefing.
- Suppress `P3` output unless it materially improves the record.
- Suppress unchanged healthy state and unchanged failures.
- Vault reconciliation should normally be silent unless blocked or inconsistent.

## Required seven-day soak test

Do not call the loop fully operational until a seven-day test verifies:

- urgent mail detection and notification
- safe update of a task-created draft after a thread changes
- preservation of a human-edited draft
- exactly one event for a confirmed appointment
- no event for ambiguous timing
- removal only of a task-created private event after cancellation
- no repeated duplicate-transaction alert
- transfers are not misclassified as spending
- no repeated CI rerun for an unchanged SHA
- changed branch head prevents an autonomous push
- attempted work is not recorded as completed
- completed work does not remain in carry-forward
- private facts never enter public repositories
- every source gap appears without repeated spam

## Status wording

Use explicit claims:

- `Verified`: directly confirmed through provider, repository, command, check, or readback evidence.
- `Source-backed`: supported by a cited authoritative source but not independently executed.
- `Locally verified`: validated in an available local environment.
- `Unverified`: plausible but not yet proven.
- `Blocked`: prevented by missing access, evidence, approval, or capability.
- `Assumption`: an explicitly labeled working assumption.

## Next action

After this contract is merged, every task prompt should reference this contract, the private operational ledger, and the canonical receipt schema. The loop remains in a monitored rollout state until the soak test passes.
