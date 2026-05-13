---
name: polymarket-trading-advisor
description: Use when analyzing Polymarket or prediction-market questions, prices, liquidity, resolution rules, and thesis quality without trading, custody, or money movement.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [polymarket, prediction-markets, risk, research, manual-only]
    related_skills: [polymarket, sportsbook-betting-advisor, bettingai-model-advisor]
  buddy:
    risk_class: money
    auto_executable: false
    requires_explicit_approval: true
---
# Polymarket Trading Advisor

## Overview

This skill helps Hermes or Buddy analyze prediction-market opportunities without executing trades. It focuses on market wording, resolution rules, implied probability, liquidity, spreads, catalyst timing, adverse selection, and portfolio risk.

The core posture is “research assistant, not broker.” It can produce a thesis memo and manual checklist, but cannot trade, custody assets, bridge funds, or interact with wallets.

## When to Use

- The user asks for a Polymarket thesis, market wording review, implied probability explanation, or entry/exit checklist.
- The user provides a market URL, price, orderbook/liquidity details, news catalyst, or resolution source.
- Hermes needs to compare public evidence against market odds and identify ambiguities.
- Do not use for automated trading, wallet operations, evading geographic restrictions, or guaranteed return claims.

## Source Adaptation Notes

Prismtek request for Polymarket trading advisory with money-action guardrails.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- market title and URL if available
- current YES/NO prices
- resolution criteria
- liquidity/orderbook/spread
- public evidence and timeline
- user risk constraints if provided

## Outputs

- market interpretation
- implied probability
- resolution ambiguity risks
- liquidity/spread notes
- thesis table
- manual trade checklist or no-trade case

## Workflow

1. **Read the rules** — Start with title, description, resolution source, close date, and edge cases. Ambiguous markets default to caution.
2. **Translate price** — Convert price into implied probability and compare against the user thesis.
3. **Evidence audit** — Separate primary-source facts, recent news, social signals, and unsupported speculation.
4. **Market mechanics** — Flag spread, liquidity, slippage, fees, counterparty/adverse-selection, and time-to-resolution risk.
5. **Manual-only output** — Return a thesis and checklist. Do not execute trades or wallet actions.

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
