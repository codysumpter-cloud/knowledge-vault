---
name: hermes-reflect-memory-analyst
description: Use when synthesizing approved memory, notes, sessions, and KnowledgeVault context into patterns, top insights, decision support, and next actions.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, reflection, knowledge-vault, insights, productivity]
    related_skills: [obsidian, notion, llm-wiki, hermes-bookmark-research-digest]
  buddy:
    risk_class: read-only
    auto_executable: false
    requires_explicit_approval: true
---
# Hermes Reflect Memory Analyst

## Overview

This skill lets Hermes reflect across approved memory sources without mutating them by default. It finds recurring themes, decisions, constraints, open loops, relationship context, and high-leverage next steps.

The goal is actionable synthesis, not memory hoarding. It should cite source notes where possible and mark confidence levels when context is partial.

## When to Use

- The user asks for reflection, patterns, daily insights, project memory, relationship context, or what they have been circling around lately.
- Hermes needs to connect prior notes, KnowledgeVault entries, meeting notes, bookmarks, and session summaries.
- The user wants a Top 5 insight report or decision brief based on approved memory.
- Do not use to delete memory, export private memory, store secrets, or infer sensitive traits without need.

## Source Adaptation Notes

0xJeff Hermes article: Reflect synthesizes past information, preferences, relationships, patterns, and actionable daily insights.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- approved memory sources
- topic or time window
- current goals
- relevance filters
- privacy constraints

## Outputs

- top insights
- evidence map
- patterns
- risks/blind spots
- next actions
- optional note draft

## Workflow

1. **Define scope** — Clarify or assume a narrow time window/topic and list sources used.
2. **Retrieve** — Read only approved memory/KnowledgeVault/notes. Avoid secret stores and unrelated personal data.
3. **Cluster** — Group by project, decision, relationship, risk, recurring blocker, and opportunity.
4. **Synthesize** — Produce concise insights with evidence, confidence, and recommended next action.
5. **Approval before write** — If saving reflections, produce a draft and ask approval before memory or repo mutation.

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
