---
name: hermes-precall-context-brief
description: Use when preparing concise pre-call context briefs from approved notes, prior conversations, public signals, project status, and open questions.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pre-call, meetings, briefing, context, productivity]
    related_skills: [google-workspace, notion, hermes-reflect-memory-analyst]
  buddy:
    risk_class: read-only
    auto_executable: false
    requires_explicit_approval: true
---
# Hermes Pre-call Context Brief

## Overview

This skill generates a compact briefing before a call or meeting. It combines approved notes, prior conversations, current project status, and public/social signals into a useful brief: who they are, what matters, open loops, likely objections, and smart questions.

It is read-only by default. Calendar/message sending, contact updates, CRM writes, and note persistence require explicit approval.

## When to Use

- The user asks for call prep, founder/investor/customer context, project status before a meeting, or smart questions to ask.
- Hermes has approved meeting notes, transcripts, KnowledgeVault notes, public pages, or read-only calendar context.
- A scheduled task needs to generate a briefing 30-60 minutes before a call.
- Do not use to spy on private accounts, access unauthorized data, or send messages/updates without approval.

## Source Adaptation Notes

0xJeff Hermes article: planned next workflow for pre-call context using social media, transcripts, notes, and latest status before a call.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- meeting title/time/participants
- approved notes/transcripts
- project status
- public links or social signals
- desired tone and agenda

## Outputs

- one-page brief
- participant context
- recent changes
- open loops
- suggested questions
- risks and follow-ups

## Workflow

1. **Scope call** — Identify meeting objective, participants, and available approved sources.
2. **Gather context** — Read calendar/notes/transcripts/public links through read-only adapters.
3. **Compress** — Prioritize the most decision-relevant facts, open loops, and relationship context.
4. **Prepare agenda** — Create suggested talking points, questions, and follow-ups.
5. **Protect privacy** — Exclude private or sensitive data not necessary for the meeting objective.

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
