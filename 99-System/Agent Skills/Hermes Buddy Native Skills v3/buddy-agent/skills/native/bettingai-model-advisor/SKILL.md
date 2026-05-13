---
name: bettingai-model-advisor
description: Use when reviewing betting-model pipelines, sports prediction datasets, backtests, expected value math, and model-risk controls without placing bets.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [bettingai, machine-learning, sports-models, backtesting, expected-value, risk]
    related_skills: [sportsbook-betting-advisor, polymarket-trading-advisor, dspy]
  buddy:
    risk_class: money
    auto_executable: false
    requires_explicit_approval: true
---
# BettingAI Model Advisor

## Overview

This skill helps Hermes or Buddy inspect and design sports prediction workflows inspired by BettingAI: data collection, feature processing, model training, validation, prediction surfaces, and performance reporting.

It is for model critique and research. It must not place bets or recommend execution without a legal, manual, and responsible-gaming review by the user.

## When to Use

- The user asks how to build, critique, or improve a sports betting model.
- The user provides model probabilities, odds, backtest results, feature lists, or performance metrics.
- Hermes needs to distinguish apparent edge from leakage, overfitting, stale data, bad calibration, or sample-size errors.
- Do not use to create unattended betting bots, loss-chasing systems, or platform-abuse workflows.

## Source Adaptation Notes

erikbohne/bettingAI repo: data gathering, processing, model training/tuning, prediction, and API modules; adapted as model-review skill, not bet executor.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- sport/league/market
- data sources
- features and labels
- model architecture
- validation split
- odds source
- backtest results

## Outputs

- pipeline review
- data leakage risks
- calibration notes
- EV math
- backtest checklist
- deployment risk plan

## Workflow

1. **Data lineage** — Map raw data source, collection cadence, schema, missingness, and timestamp integrity.
2. **Feature/label audit** — Check for leakage, post-event features, target leakage, class imbalance, and label ambiguity.
3. **Validation design** — Prefer time-based splits, out-of-sample windows, calibration curves, and realistic odds snapshots.
4. **EV layer** — Compare model probabilities to market prices after vig, spread, limits, and slippage.
5. **Deployment plan** — Recommend monitoring, drift detection, no-bet thresholds, and manual approval gates.

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
