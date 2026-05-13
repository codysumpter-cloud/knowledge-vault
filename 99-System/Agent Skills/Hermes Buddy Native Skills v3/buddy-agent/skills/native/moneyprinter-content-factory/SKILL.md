---
name: moneyprinter-content-factory
description: Use when adapting MoneyPrinter-style modular content automation into safe draft-first workflows for Shorts, X posts, affiliate content, and outreach review.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [content-factory, youtube-shorts, x, affiliate, outreach, approval-gated]
    related_skills: [content-growth-social-ops, youtube-content, xurl]
  buddy:
    risk_class: external-action
    auto_executable: false
    requires_explicit_approval: true
---
# MoneyPrinter Content Factory

## Overview

This skill converts the useful architecture pattern from MoneyPrinter-style systems into a native Hermes/Buddy workflow: modular content planning, reusable scripts/adapters, schedulable drafts, and human approval gates.

Use it as an idea-to-campaign factory. It should generate content packages and operator checklists, not autonomously run monetization scripts, scrape leads, or spam people.

## When to Use

- The user wants an automated-feeling content pipeline while keeping account actions approval-gated.
- The user wants to produce YouTube Shorts concepts, X promo drafts, affiliate content, or outreach copy from a product/topic.
- Hermes needs to turn one source asset into many drafts with metadata and a review queue.
- Do not use to scrape businesses for unsolicited email, post automatically, generate deceptive affiliate claims, or bypass platform restrictions.

## Source Adaptation Notes

FujiwaraChoki/MoneyPrinterV2 repo: modular automation for Twitter bot, YouTube Shorts, affiliate marketing, and cold outreach; adapted without copying AGPL runtime code.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- campaign objective
- offer/product/topic
- approved claims and proof
- platforms
- affiliate/compliance constraints
- asset folder or source notes

## Outputs

- campaign brief
- content batches
- metadata drafts
- outreach drafts marked review-only
- asset checklist
- schedule proposal

## Workflow

1. **Campaign brief** — Define audience, offer, proof, CTA, allowed claims, banned claims, and approval owner.
2. **Content modules** — Create reusable modules: hook bank, proof snippets, CTA variants, visual beats, objection handlers.
3. **Draft batch** — Generate Shorts scripts, X posts, affiliate copy, and optional outreach copy as drafts only.
4. **Compliance screen** — Check claims, disclosure, spam risk, privacy, platform rules, and user approval requirements.
5. **Adapter handoff** — Return structured JSON/YAML for Buddy adapters to preview; do not execute account actions inside the skill.

## Buddy Adapter Boundary

Draft and preview only. Any external account action requires explicit Prismtek approval and a Buddy adapter that enforces allowlists.

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
