# Prismtek Agent Direction and Memory Import - 2026-05-13

## Current agent direction

- OpenClaw is retired for current work. Do not use OpenClaw as an active runtime, default toolchain, product target, or implementation path.
- Hermes-agent is the current main working agent system.
- Buddy-agent is being prepared to become the primary and eventually only agent repository.
- Buddy-brain remains continuity and memory context until Buddy-agent fully owns that role.
- KnowledgeVault / Obsidian remains the source of truth for project memory, decisions, daily notes, handoffs, and agent context.

## Critical operating preferences

- Discord / PrismBot relay output must be compact: 1,500 characters or less, no code fences, no markdown tables, no emoji, no backticks, minimal line breaks, and relay-safe compressed wording.
- Never expose private credentials or private infrastructure details. Never publicly expose services by default.
- Prefer the smallest working step first. Prove it, then continue.
- Inspect the system if unsure instead of guessing.
- Self-upgrades stay frozen until usefulness is proven.
- Preserve recovery branches, backups, and resumable state during risky repository work.
- Prefer exact commands, exact files, and explicit implementation plans over abstract guidance.

## Startup routine reminder

Agents should read SOUL.md, USER.md, AGENTS.md, memory.md / MEMORY.md, daily notes, SYSTEMMAP.md, RUNBOOK.md, BACKLOG.md, and relevant file listings before trusting automation claims when those files exist.

## Saved and inferred memory import

1. [saved](2026-02-26) I asked to make content small enough to send to my Discord PrismBot OpenClaw agent.
2. [saved](2026-02-26) I prefer Discord-safe formatting with <=1,500 characters, no code blocks, no markdown tables, no emojis, no backticks, minimal line breaks, and relay-safe compressed prompts.
3. [saved](2026-02-26) I require OpenClaw dashboard work to never expose private credentials, never publicly expose services, always propose the smallest working step first, stop after each step for feedback, and inspect the system if unsure.
4. [saved](2026-03-19) I created a memory/ directory and started a daily memory log at 2026-03-19.md.
5. [saved](2026-03-19) I instructed BMO to follow a startup routine reading SOUL.md, USER.md, AGENTS.md, and daily notes.
6. [saved](2026-03-19) I wanted BMO to prove it by showing SYSTEMMAP.md, RUNBOOK.md, BACKLOG.md, and file listings before I trusted further automation.
7. [saved](2026-03-19) I wanted self-upgrades frozen until usefulness was proven.
8. [saved](2026-03-20) I requested a council of sub-agents modeled after Adventure Time characters.
9. [saved](2026-03-20) I defined Prismo as the most powerful and omniscient coordinating agent in the council.
10. [saved](2026-03-20) I assigned detailed roles to Princess Bubblegum, Finn, Jake, Marceline, Simon, Peppermint Butler, NEPTR, Lady Rainicorn, Lemongrab, and other specialist agents.
11. [saved](2026-03-20) I required implementation deliverables including a ~/bmo-context/council/ directory with markdown files for each agent.
12. [saved](2026-03-20) I required BOOTSTRAP updates for the council system.
13. [saved](2026-03-30) I saved the repo reference https://github.com/codysumpter-cloud/PrismBot because I wanted BMO to match PrismBot behavior.
14. [saved](2026-03-30) I requested an explicit PrismBot-to-BMO parity plan and capability matrix covering YouTube intake, transcription, summarization, analysis, long-video handling, caching, queueing, chunking, and exact files/modules to modify.
15. [saved](2026-03-30) I noted that the gh CLI was available but private repo access required authentication.
16. [saved](2026-03-30) I forbade asking for PATs, SSH keys, or private credentials in chat.
17. [saved](2026-03-30) I initiated or completed a GitHub auth flow and expected the CLI device code and URL to be surfaced for completion.
18. [saved](2026-03-30) I emphasized exact gh commands including gh auth login --web --clipboard, gh auth status, and gh repo view codysumpter-cloud/PrismBot.
19. [saved](2026-03-30) I requested a complete dump of saved memories and inferred details with creation dates.
20. [saved](2026-04-01) I saved recovery details for bmo-stack including HEAD SHA f89c9aee87fe35fa7c688b8bd6525e241085034d.
21. [saved](2026-04-01) I created a stash named pre-update backup 20260331-201453 containing thousands of untracked files.
22. [saved](2026-04-01) I pushed a bmo-stack recovery branch named recovery/agent-automation-mission-control-enhancement-20260331-202149.
23. [saved](2026-04-01) I reset prismtek-site main cleanly to origin/main and created recovery/main-local-work-20260331-202345.
24. [saved](2026-04-01) I preserved extensive local work in recovery branches instead of discarding it.
25. [saved](2026-04-01) I ran diagnostics showing 127.0.0.1:8080 refused connections and openclaw-status.prismtek.dev/status returned Cloudflare 530 error 1033.
26. [saved](2026-04-01) I observed that the openclaw-gateway process existed but was not serving the expected port.
27. [saved](2026-04-01) I later observed the gateway reporting healthy: false with HTTP 502 fallback fixture data.
28. [saved](2026-04-01) I confirmed 127.0.0.1:18789/status returned the OpenClaw Control UI.
29. [saved](2026-04-01) I confirmed my cloudflared config mapped openclaw-status.prismtek.dev to http://127.0.0.1:8080.
30. [saved](2026-04-06) I started building OpenClaw stack-builder assets with a strong focus on the Xcode app.
31. [saved](2026-04-06) I wanted the Xcode app to become the real product with local runtime ownership, memory, onboarding, generated configs, and task execution.
32. [saved](2026-04-06) I requested a roadmap and implementation prompt for turning the SwiftUI shell into the first real OpenClaw Stack Builder app.
33. [saved](2026-04-07) I checked whether the app matched the documentation and reported that BMO stopped responding while the gateway appeared degraded.
34. [saved](2026-04-10) I requested a roadmap, product vision, and Codex implementation prompt for the BeMore product.
35. [saved](2026-04-10) I defined BeMore as a standalone personal agent app with workspace runtime, evolving markdown memory, and a Buddy continuity layer.
36. [saved](2026-04-10) I asked to remake outputs with a Buddy Workshop marketplace specification and a Council Starter Pack.
37. [saved](2026-04-10) I provided the repository https://github.com/codysumpter-cloud/bmo-stack and requested suggested additions.
38. [saved](2026-04-13) I stored a donor audit strategy in persistent memory.
39. [saved](2026-04-13) I defined my updated priority stack as provider failover/routing fix first, then memory compiler work, then MCP/tooling cleanup, then token-efficiency mode.
40. [saved](2026-04-13) I imposed a hard constraint that claw-code could not be directly imported and that hidden gateways, bridges, or runtime sprawl were forbidden.
41. [saved](2026-04-13) I received an audit result showing split-brain routing between run_agent.py and agent/auxiliary_client.py with reactive-only failover behavior.
42. [saved](2026-04-13) I required MCP-schema migration and donor implementation work to pause until provider routing was fixed and validated.
43. [saved](2026-04-13) I required routing fixes to unify provider authority, add cooldown and degraded-provider memory, handle ~46k-token routing, and validate real failover without reconnect loops.
44. [saved](2026-04-21) I owned the repositories codysumpter-cloud/bmo-stack, codysumpter-cloud/prismtek-apps, and codysumpter-cloud/prismtek-site.
45. [saved](2026-04-21) I tracked the prismtek-apps iOS build number as 40 in apps/bemore-ios-native/BeMoreAgentShell/Info.plist.
46. [saved](2026-04-21) I had PRs merged including prismtek-apps PR #65, prismtek-site PR #64, and bmo-stack PR #269.
47. [saved](2026-04-21) I created or tracked Codex handoff issue #64 for post-merge stabilization and iOS build submission.
48. [saved](2026-04-24) I corrected a stale Info.plist from build 32 to canonical build 46 and established that the next build should be 47.
49. [saved](2026-04-24) I opened bmo-stack PR #279 to add fork governor automation.
50. [saved](2026-04-24) I configured the fork governor to scan forks, seed auto-sync workflows, regenerate DONORS.yaml, and open refresh PRs.
51. [saved](2026-04-24) I successfully merged PR #279 and seeded automation workflows into 33 forks.
52. [saved](2026-04-24) I tracked that one fork, codysumpter-cloud/claw-code, was blocked or locked.
53. [saved](2026-04-24) I maintained a canonical donor count of 34.
54. [saved](2026-04-24) I defined a Buddy Manifesto product architecture and a 3-pack roadmap for Creator, Teen, and Field Tech personas.
55. [saved](2026-04-24) I specified canonical objects including BuddyProfile, BuddyMemory, BuddyPack, BuddyReceipt, and BuddyTemplate.
56. [saved](2026-04-24) I outlined a detailed 90-day build sequence, IP checklist, and repo-by-repo licensing plan.
57. [saved](2026-05-09) I requested a complete dump of all saved memories and inferred details formatted in first person with dates.
58. [inferred](2026-02-26) I heavily optimize prompts and workflows for relay systems, bots, and constrained interfaces.
59. [inferred](2026-02-26) I prefer operationally safe automation with strict boundaries around private credentials and infrastructure exposure.
60. [inferred](2026-03-19) I care deeply about inspectability, reproducibility, and proving automation reliability before trusting it.
61. [inferred](2026-03-20) I like using narrative frameworks and fictional character metaphors to organize AI system responsibilities.
62. [inferred](2026-03-20) I think in terms of multi-agent orchestration with specialized roles instead of monolithic assistants.
63. [inferred](2026-03-30) I want BMO to achieve feature parity with PrismBot rather than becoming a separate incompatible system.
64. [inferred](2026-03-30) I prefer exact commands, exact files, and explicit implementation plans instead of abstract guidance.
65. [inferred](2026-03-30) I have strong security boundaries around credentials and authentication handling.
66. [inferred](2026-04-01) I preserve recovery branches and backups aggressively during risky repo operations.
67. [inferred](2026-04-01) I actively self-host infrastructure involving OpenClaw, Cloudflare tunnels, gateways, and local services.
68. [inferred](2026-04-01) I debug systems by tracing networking, ports, health endpoints, reverse proxies, and runtime configs directly.
69. [inferred](2026-04-06) I see the native iOS experience as the primary long-term interface for my AI platform.
70. [inferred](2026-04-06) I want local-first AI runtimes and memory systems instead of purely cloud-hosted assistants.
71. [inferred](2026-04-10) I am building a persistent personal AI platform centered around continuity, memory, and evolving identity.
72. [inferred](2026-04-10) I care about packaging and distributing customizable AI companions or Buddy systems.
73. [inferred](2026-04-13) I strongly dislike architecture sprawl, hidden bridges, and fragmented runtime authority.
74. [inferred](2026-04-13) I prioritize infrastructure correctness and failover reliability before feature expansion.
75. [inferred](2026-04-21) I manage multiple interconnected repositories as part of a broader AI platform ecosystem.
76. [inferred](2026-04-21) I use GitHub PRs and issues as operational coordination mechanisms for both humans and agents.
77. [inferred](2026-04-24) I think in terms of ecosystems, governance automation, and donor/fork management at scale.
78. [inferred](2026-04-24) I am designing BeMore/Buddy as a product family with distinct user archetypes and lifecycle systems.
79. [inferred](2026-04-24) I value maintainable schemas, canonical object models, and structured long-term architecture.
80. [inferred](2026-05-09) I care about transparency in what the assistant stores, remembers, and infers about me.
