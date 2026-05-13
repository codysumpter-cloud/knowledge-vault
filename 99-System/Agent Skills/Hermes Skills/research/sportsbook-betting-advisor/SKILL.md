---
name: sportsbook-betting-advisor
description: Use when explaining sportsbook odds, bankroll risk, implied probability, expected value, and no-action cases without placing bets or guaranteeing outcomes.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sportsbook, betting, risk, expected-value, finance, manual-only]
    related_skills: [polymarket-trading-advisor, bettingai-model-advisor]
  buddy:
    risk_class: money
    auto_executable: false
    requires_explicit_approval: true
---
# Sportsbook Betting Advisor

## Overview

This skill helps Hermes or Buddy give structured, conservative sportsbook analysis. It can explain odds, translate prices into implied probability, compare the user's thesis to market price, flag weak evidence, and produce a manual decision checklist.

It must never place bets, route money, recommend chasing losses, or claim certainty. The default recommendation may be “no bet” when evidence, bankroll, legal status, or market quality is insufficient.

## When to Use

- The user asks whether a sportsbook line is worth considering, how odds imply probability, or how to size risk responsibly.
- The user asks for a pre-bet checklist, market comparison, model critique, or explanation of EV.
- The user provides odds, stake, bankroll, model probability, injury/news context, or historical stats.
- Do not use to automate betting, evade sportsbook rules, bypass jurisdiction restrictions, or advise minors.

## Source Adaptation Notes

Prismtek request for sportsbook advisory with money-action guardrails.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- sport/event/market
- odds format and price
- user-estimated probability if available
- bankroll and max risk constraints if voluntarily provided
- data/news/model assumptions

## Outputs

- implied probability
- break-even probability
- edge estimate if enough data exists
- risk factors
- no-bet triggers
- manual checklist

## Workflow

1. **Normalize odds** — Convert American/decimal/fractional odds into implied probability and break-even threshold.
2. **Compare thesis** — Compare user/model probability to implied probability. Separate evidence from vibes.
3. **Risk screen** — Check bankroll exposure, correlation, uncertainty, stale lines, injuries, limits, and responsible-gaming red flags.
4. **Decision frame** — Return Bet/Pass/Need more data as an analysis label, never as an instruction to wager.
5. **Manual-only close** — Make clear that any wager must be placed manually by the user only if legal and appropriate.

## Buddy Adapter Boundary

Analysis only. No transactions, orders, wagers, deposits, withdrawals, wallet actions, or money movement.

Skills describe what to do and how to reason. Adapters are the only place where account APIs, browsers, local CLIs, memory stores, repositories, or money-related systems may be touched. Before adapter execution, produce:

- the exact action preview;
- the target account, repo, vault, market, or platform;
- the data that will be sent or changed;
- the risk class;
- a one-line approval request.

## Confirmation Rules

Require explicit Prismtek approval before any of these actions:

- posting, replying, DMing, liking, reposting, deleting, following, or changing social/account settings;
- writing to KnowledgeVault, Obsidian, Notion, Google Workspace, GitHub, or any memory store;
- browser actions inside authenticated sessions;
- wallet, sportsbook, exchange, prediction-market, deposit, withdrawal, or trade actions;
- bulk outreach, affiliate publishing, scraping, or scheduled automation.

## Common Pitfalls

1. **Treating skill instructions as permission.** Loading a skill does not authorize external actions.
2. **Skipping source validation.** Important claims need supporting evidence or must be labeled as assumptions.
3. **Letting automation outrun taste.** High-volume drafts still need editorial review, brand fit, and platform safety checks.
4. **Confusing analysis with execution.** Financial and account actions are separate high-risk adapter events.
5. **Forgetting stale context.** Mark data age when the source, market, odds, or platform state may have changed.

## Verification Checklist

- [ ] SKILL.md frontmatter starts at byte 0 and closes before the body.
- [ ] `name`, `description`, `version`, `author`, `license`, and `metadata.hermes` are present.
- [ ] Description starts with `Use when` and is under 1024 characters.
- [ ] The output separates facts, assumptions, recommendations, and approval-required actions.
- [ ] No high-risk action is executed directly by the skill.
- [ ] Any proposed adapter call includes a clear preview and approval gate.
