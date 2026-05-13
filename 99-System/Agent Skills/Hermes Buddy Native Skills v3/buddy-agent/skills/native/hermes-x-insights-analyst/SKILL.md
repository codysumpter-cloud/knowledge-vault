---
name: hermes-x-insights-analyst
description: Use when summarizing approved X accounts or timelines into read-only insight reports while blocking posts, replies, reposts, likes, DMs, and cookie-based write tooling.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [x, twitter, read-only, insights, daily-brief, social-media]
    related_skills: [xurl, hermes-bookmark-research-digest, content-growth-social-ops]
  buddy:
    risk_class: read-only
    auto_executable: false
    requires_explicit_approval: true
---
# Hermes X Insights Analyst

## Overview

This skill creates read-only X insight reports from approved accounts, lists, searches, or exported data. It ranks signal, summarizes what changed, identifies why it matters, and proposes follow-up research.

It explicitly blocks write-capable X actions. If the available adapter cannot guarantee read-only permissions, the skill must stop and request a safer adapter.

## When to Use

- The user wants a daily X macro/tech/AI/creator/social signal digest.
- The user provides handles, search terms, lists, bookmarks, exports, or approved API results.
- Hermes needs to turn noisy social posts into ranked insights and next actions.
- Do not use to post, like, reply, DM, scrape private content, reuse cookies, or run write-capable X CLIs.

## Source Adaptation Notes

0xJeff Hermes article: daily X insight reports and cautionary lesson that write-capable X tooling accidentally posted content.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- approved account list or search terms
- time window
- topics of interest
- read-only API/export data
- ranking preferences

## Outputs

- ranked insights
- evidence snippets
- why-it-matters notes
- follow-up questions
- source links where available

## Workflow

1. **Permission check** — Confirm data came from a read-only adapter, export, or user-provided text. Stop if write-capable access is required.
2. **Collect signals** — Group posts by account, theme, recency, engagement, novelty, and relevance.
3. **Score signal** — Rank by user relevance, factual density, novelty, and actionability. Penalize hype and thin takes.
4. **Synthesize** — Produce concise insights with context and uncertainty labels.
5. **Next actions** — Suggest reading, content ideas, market questions, or watchlist changes without posting anything.

## Buddy Adapter Boundary

Read-only adapters only. Any write action belongs in a separate explicit approval flow.

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
