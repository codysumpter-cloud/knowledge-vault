---
name: hermes-bookmark-research-digest
description: Use when turning approved bookmarks and linked articles into ranked research digests, summaries, and next actions using read-only browser or API adapters.
version: 1.0.0
author: Prismtek / Buddy-Hermes Skill Bridge
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [bookmarks, research, digest, browser-readonly, x, knowledge-vault]
    related_skills: [hermes-x-insights-analyst, llm-wiki, blogwatcher]
  buddy:
    risk_class: external-action
    auto_executable: false
    requires_explicit_approval: true
---
# Hermes Bookmark Research Digest

## Overview

This skill turns bookmarks into a useful research digest. It fetches approved bookmark metadata, follows approved links through a read-only browser or extractor, summarizes the full material, ranks by Prismtek relevance, and proposes next actions.

Browser use is treated as an external action because browsers can hold credentials and sensitive tabs. Use isolated read-only browser profiles and avoid random browsing.

## When to Use

- The user wants a daily or ad-hoc digest of X bookmarks, saved links, articles, or research tabs.
- The user wants bookmarks ranked by interests, investments, projects, or current priorities.
- Hermes needs to store distilled insights into KnowledgeVault or a wiki after approval.
- Do not use for credentialed browsing, paywall bypass, arbitrary web wandering, or sensitive account automation.

## Source Adaptation Notes

0xJeff Hermes article: X bookmarks ranked, linked URLs opened, articles summarized, and insights stored in a wiki with browser-harness caution.

The source is treated as design inspiration and workflow context. Do not copy upstream runtime code into Hermes or Buddy unless Prismtek explicitly reviews the license, dependency tree, secrets handling, and adapter permissions.

## Inputs

- bookmark export/API data
- approved URL list
- ranking criteria
- KnowledgeVault topic map
- time budget or item limit

## Outputs

- ranked digest
- per-link summary
- key claims and caveats
- next actions
- optional KnowledgeVault note draft

## Workflow

1. **Scope** — Cap the number of bookmarks and define ranking criteria before fetching full pages.
2. **Read-only fetch** — Use API/export first; use browser-readonly only for approved URLs that need rendering.
3. **Summarize** — Capture thesis, evidence, novelty, usefulness, and unresolved questions.
4. **Rank** — Prioritize by current goals, project relevance, decision value, and freshness.
5. **Persist draft** — Prepare KnowledgeVault note content but require approval before writing or syncing.

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
