# Content Report 018 — Governed Market Intelligence Loop Skill

Date: 2026-05-14  
Status: Added to GitHub KnowledgeVault Branch / Native Hermes + Buddy Skill Created

## Summary

A new native Hermes/Buddy skill, `governed-market-intelligence-loop`, was created and stored across Hermes, Buddy-Agent, and KnowledgeVault source paths. The skill converts a market cron idea into a model/provider-agnostic, proposal-only, risk-governed intelligence loop.

The skill is money-risk classified and non-auto-executable.

## Files Added

Hermes native skill:

```txt
hermes-agent/skills/money/governed-market-intelligence-loop/SKILL.md
```

Buddy-Agent mirror skill:

```txt
buddy-agent/skills/native/governed-market-intelligence-loop/SKILL.md
```

KnowledgeVault source notes:

```txt
knowledge-vault/99-System/Agent Skills/native/governed-market-intelligence-loop/SOURCE_NOTES.md
```

Hermes activation prompt:

```txt
knowledge-vault/99-System/Agent Skills/native/governed-market-intelligence-loop/Hermes Activation Prompt.md
```

## Core Upgrade

From:

```txt
Signal -> Analyze -> Report -> Execute
```

To:

```txt
Observe -> Validate -> Score -> Propose -> Require Approval -> Log
```

## Skill Boundary

Allowed:

- observe public/account-read-only signals;
- validate sources;
- normalize signals;
- score divergence;
- create proposals;
- write receipts;
- write digests;
- produce educational/process content ideas.

Blocked inside the skill:

- trade placement;
- order modification;
- stop modification;
- exposure changes;
- deposits/withdrawals;
- wallet signing;
- broker/wallet/sportsbook execution actions;
- watchlists framed as direct financial recommendations.

## Provider-Agnostic Architecture

The skill can work with any model/provider if outputs are schema-normalized and policy-governed:

- local Ollama / LM Studio;
- OpenAI-compatible APIs;
- Claude-compatible APIs;
- Gemini-compatible APIs;
- TradingAgents / InvestSkill style multi-agent debate;
- deterministic Python/TypeScript rules.

Deterministic risk policy has veto power over all model agents.

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

Cron is treated as a heartbeat. App-level market calendar checks decide whether a run is valid.

## Risk Posture

- Congressional disclosures are delayed context, not real-time execution triggers.
- Social/X sentiment is a reflexivity/noise layer, not a sole decision source.
- No single X post, analyst quote, or delayed disclosure may trigger a high-confidence pivot.
- High confidence requires at least two independent verified sources and primary-source evidence.
- Stable runs should be logged, not spammed.

## Next Move

Hermes should sync and activate:

```txt
/skill governed-market-intelligence-loop
```

Then use the activation prompt to improve any existing market intelligence cron job into proposal-only, calendar-aware, least-privilege, source-validated form.
