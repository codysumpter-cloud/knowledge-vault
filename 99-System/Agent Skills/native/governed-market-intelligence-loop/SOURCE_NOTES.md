# Governed Market Intelligence Loop — Source Notes

Date: 2026-05-14  
Status: Added as native Buddy/Hermes skill candidate

## Purpose

Create a native Hermes/Buddy skill that turns market cron jobs into governed, proposal-first intelligence loops.

The skill is designed to help Hermes improve and run market-monitoring workflows without allowing autonomous trade execution.

## Core Upgrade

From:

```txt
hourly automated divergence hunter
```

To:

```txt
market-calendar-aware, source-validated, proposal-first intelligence loop with hard execution vetoes
```

## Target Pipeline

```txt
Scheduler
  -> Market calendar guard
  -> State loader
  -> Source collectors
  -> Signal normalizer
  -> Evidence validator
  -> Divergence scorer
  -> Deterministic risk policy
  -> Proposal generator
  -> Alert router
  -> Audit log
```

## Core Rule

The job may observe, validate, score, propose, and log.

It must not:

- place trades;
- modify orders;
- resize positions;
- change stops;
- deposit or withdraw;
- sign wallet transactions;
- open broker/wallet pages for execution;
- treat watchlists as direct financial recommendations.

## Why This Exists

The motivating prompt described a market loop that claimed:

- top-of-hour hourly cron;
- insider/social/fundamental divergence hunting;
- active positions/queued orders;
- daily congressional scan;
- hourly market loop;
- InvestSkill + TradingAgents + native synthesis;
- fully automated fills.

The correct architecture is not an autonomous trading loop. It is a governed intelligence loop where risk policy and user approval control all execution.

## Critical Design Choices

### Cron Is a Heartbeat

Cron should wake the system. The application should decide whether the run is valid using market calendars, trading sessions, early closes, and job type.

### Congressional Disclosures Are Delayed Context

A disclosure detected today may describe a trade that happened days or weeks earlier. Track transaction date, filing date, and detected date separately.

### Model Agents Are Advisors, Not Governors

InvestSkill, TradingAgents, OpenAI, Claude, local Ollama, Gemini, Kronos, or any other model/provider may contribute analysis, but all outputs must be schema-normalized and passed through deterministic risk policy.

### Evidence Beats Vibes

No evidence URL or evidence hash means no high-confidence alert.

No single X post, analyst quote, or delayed disclosure should trigger a pivot by itself.

### Stable Runs Should Be Quiet

Use alert tiers. Log stable/noise runs instead of spamming hourly updates.

## Recommended Schedule

```cron
CRON_TZ=America/New_York
15 8 * * 1-5  hermes premarket-scan --proposal-only
25 9 * * 1-5  hermes open-risk-check --require-human-approval
7,22,37,52 9-15 * * 1-5 hermes market-loop --proposal-only
5 16 * * 1-5 hermes close-review --digest
30 17 * * 1-5 hermes slow-signal-scan --proposal-only
15 20 * * 1-5 hermes calibrate-thresholds --no-live-actions
```

## KnowledgeVault Targets

Suggested local paths:

```txt
KnowledgeVault/50 - Content/market-sports-digests/
KnowledgeVault/50 - Content/market-watchlists/
KnowledgeVault/50 - Content/market-risk-proposals/
KnowledgeVault/99-System/Risk Policy/
KnowledgeVault/99-System/Cron Jobs/Runs/
KnowledgeVault/99-System/Cron Jobs/Learnings/
KnowledgeVault/99-System/Cron Jobs/Next Plans/
KnowledgeVault/99-System/Agent Skills/candidates/
```

## Content Angles

This skill can generate Prismtek content about:

- why agents need deterministic risk vetoes;
- why market intelligence should be proposal-first;
- why social sentiment is not a trading signal by itself;
- why delayed disclosures are context, not execution triggers;
- how model-agnostic financial intelligence can be made safer;
- how receipts turn market analysis from vibes into an auditable process.

## Activation Note

Promote/install this skill locally before enabling any money-adjacent market intelligence job.

Verify bare-name load:

```txt
/skill governed-market-intelligence-loop
```

It must remain:

```txt
auto_executable: false
requires_explicit_approval: true
risk_class: money
```
