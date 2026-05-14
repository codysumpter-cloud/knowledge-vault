# Market and Sports Trend Intelligence — Source Notes

Date: 2026-05-14  
Status: Added as native Buddy/Hermes skill candidate

## Purpose

Create a safe market, stock, macro, sports, betting, and content-intelligence skill for Prismtek. The skill watches public discourse from X, YouTube, official sources, and approved data feeds, then turns what it learns into KnowledgeVault briefs, watchlists, manual-review packets, and content ideas.

## Core Behavior

The skill should:

- monitor public stock-market, AI-stock, sector, macro, crypto, sports, betting, and prediction-market discourse;
- watch X and YouTube for timely narratives and creator/influencer framing;
- compare public chatter against official sources where possible;
- build educational watchlists and risk briefs;
- create manual-review decision packets for possible stock or sports-betting ideas;
- draft X posts, YouTube Shorts, and long-form content from trends;
- suggest new Hermes/Buddy skills and KnowledgeVault notes;
- preserve receipts and source links.

## Safety Boundary

This is a research, education, and content-intelligence skill. It is not an execution skill.

Allowed without approval:

- read public sources;
- summarize public market/sports discourse;
- create watchlists;
- explain odds, volatility, implied probability, and risk concepts;
- draft content;
- draft manual-review decision packets;
- create KnowledgeVault notes.

Requires explicit approval:

- publishing X/YouTube content;
- tagging/mentioning accounts;
- replying, quoting, reposting, liking, following, or DMing;
- joining external communities;
- opening brokerage/sportsbook/wallet pages;
- preparing any broker/sportsbook/wallet action for manual review.

Blocked:

- placing stock, options, crypto, prediction-market, or sportsbook orders;
- depositing, withdrawing, transferring, or signing transactions;
- bypassing jurisdiction, broker, sportsbook, exchange, or platform controls;
- pretending to be a licensed financial advisor;
- promising returns;
- encouraging loss chasing;
- using private account data without approval;
- hammering rate-limited or blocked routes.

## KnowledgeVault Targets

Default write targets:

```txt
KnowledgeVault/50 - Content/market-sports-digests/
KnowledgeVault/50 - Content/market-watchlists/
KnowledgeVault/50 - Content/sports-risk-briefs/
KnowledgeVault/50 - Content/post-ideas/
KnowledgeVault/50 - Content/youtube-production/
KnowledgeVault/99-System/Agent Skills/candidates/
```

Never write raw credentials, brokerage tokens, sportsbook credentials, wallet keys, private DMs, or non-public personal data into KnowledgeVault.

## Prismtek Content Angle

Use this skill to create content around:

- what markets teach about attention and narratives;
- how public sentiment differs from source-backed information;
- why agents need risk boundaries around money and betting;
- how KnowledgeVault turns noisy trend streams into durable learning;
- why watchlists and decision packets are safer than automated money actions;
- how Prismtek uses receipts, uncertainty labels, and manual approval for risky domains.

## Recommended Daily Output

```txt
Market/Sports Trend Digest
- Time window:
- Sources checked:
- Top stock/sector narratives:
- Top sports/betting narratives:
- Official facts:
- Chatter/sentiment:
- Watchlist candidates:
- Risk/no-action notes:
- Content opportunities:
- Skill ideas:
- Next monitoring tasks:
```
