# X Trend DevRel Intelligence — Source Notes

Date: 2026-05-14  
Status: Added as native Buddy/Hermes skill candidate

## Purpose

Create a safe trend intelligence and developer relationship-building skill for Prismtek. The skill monitors public X/Twitter discourse, AI development stacks, developer conversations, repo launches, tool announcements, and builder communities, then turns the findings into KnowledgeVault digests, post drafts, and approval-gated outreach drafts.

## Core Behavior

The skill should:

- search or inspect approved public sources for AI/developer trends;
- identify useful builders, maintainers, creators, repos, and communities;
- map AI development stacks and toolchains;
- create KnowledgeVault trend digests;
- draft X posts, threads, replies, and outreach messages;
- suggest new Hermes/Buddy skill ideas;
- preserve receipts and source links;
- require explicit approval before any external action.

## Safety Boundary

This is not a spam, scraping, or mass-outreach skill.

Allowed without approval:

- identify public accounts or repos;
- summarize public posts;
- draft replies or DMs;
- suggest people to follow;
- create a relationship map;
- create KnowledgeVault notes.

Requires explicit approval:

- follow;
- like;
- repost;
- reply;
- quote post;
- DM;
- tag or mention a person;
- subscribe;
- join a Discord/Slack/community;
- open a pull request or issue;
- send email;
- publish any post.

Blocked:

- spam or mass outreach;
- fake personalization;
- scraping private or non-public data;
- exporting cookies or sessions;
- bypassing X limits or anti-abuse systems;
- harassment or dogpiling;
- undisclosed paid promotion;
- pretending Prismtek has a relationship that does not exist.

## KnowledgeVault Targets

Default write targets:

```txt
KnowledgeVault/50 - Content/trend-digests/
KnowledgeVault/50 - Content/outreach-drafts/
KnowledgeVault/50 - Content/post-ideas/
KnowledgeVault/99-System/Agent Skills/candidates/
```

Never write raw credentials, cookies, tokens, private DMs, private emails, or unapproved personal data into KnowledgeVault.

## Prismtek Positioning

Use this skill to build relationships around Prismtek's real lane:

- durable memory;
- guarded execution;
- local-first agents;
- AI development stacks;
- developer tools;
- KnowledgeVault/Buddy-Brain/Buddy-Agent;
- receipts and verification;
- practical AI operator workflows.
