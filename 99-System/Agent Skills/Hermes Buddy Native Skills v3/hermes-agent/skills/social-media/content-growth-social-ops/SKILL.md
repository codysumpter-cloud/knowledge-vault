---
name: content-growth-social-ops
description: Use when planning, drafting, repurposing, and promoting content across YouTube, X, and Twitch while keeping posting, DMs, replies, deletions, and account changes approval-gated.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [social-media, youtube, x, twitch, content-growth, approval-gated]
    related_skills: [youtube-content, xurl, moneyprinter-content-factory, hermes-x-insights-analyst]
  buddy:
    risk_class: external-action
    auto_executable: false
    requires_explicit_approval: true
---
# Content Growth Social Ops

## Overview

This skill turns approved source material into a safe cross-platform content engine for YouTube, X, and Twitch. It teaches Hermes or Buddy to select a content angle, create platform-native drafts, prepare metadata, build a promotion calendar, and report what still needs human approval.

It is intentionally not an autoposter. Publishing, account changes, replies, DMs, deletions, paid boosts, and credential handling must stay behind explicit Prismtek approval and the Buddy adapter policy.

## When to Use

- The user asks for a viral content plan, social growth loop, Shorts strategy, X thread, Twitch promo plan, or cross-platform repurposing workflow.
- The user provides a video, transcript, stream topic, product update, repo milestone, launch note, or market insight and wants platform-native content.
- Hermes needs to prepare a posting checklist, metadata, titles, thumbnails, descriptions, clips, or promo copy for human review.
- Don't use for account login, credential collection, unsolicited outreach, automated engagement farming, spam, fake testimonials, or guaranteed virality claims.

## Source Adaptation Notes

Prismtek KnowledgeVault/Buddy bridge request plus Genviral/Hermes YouTube workflow patterns.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- source content or topic
- target audience
- platforms: YouTube/X/Twitch
- brand voice
- constraints and links
- posting window if known

## Outputs

- content angle matrix
- YouTube title/description/tags/chapters/shorts ideas
- X posts or threads
- Twitch stream title/promo schedule
- approval checklist
- risk notes

## Workflow

1. **Intake** — Identify the source asset, audience, objective, conversion goal, and platforms. If missing, make conservative assumptions and label them.
2. **Extract hooks** — Find the strongest novelty, conflict, utility, identity, and proof points. Reject clickbait that the source cannot support.
3. **Platform transform** — Write native drafts: YouTube metadata and Shorts hooks, X posts/threads, and Twitch stream promo with schedule.
4. **Safety pass** — Remove unsupported claims, private info, spam patterns, manipulation, misleading urgency, and platform ToS-risky behavior.
5. **Approval package** — Return previews plus a clear list of actions that require Prismtek approval before any adapter can execute.

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
