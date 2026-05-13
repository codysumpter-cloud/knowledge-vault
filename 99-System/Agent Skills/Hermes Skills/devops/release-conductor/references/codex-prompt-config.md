# Codex Prompt Configuration: Prismtek Ecosystem

## Canonical Repository Rename Map
Use current GitHub repo names, not stale names.

Current rename map:
- codysumpter-cloud/bmo-stack is now codysumpter-cloud/buddy-brain
- codysumpter-cloud/omni-bmo is now codysumpter-cloud/omni-buddy

**Resolution Logic:**
- When a PR body says `bmo-stack`, resolve it to `codysumpter-cloud/buddy-brain` unless it explicitly points to `Automind-Lab/bmo-stack`.
- When a PR body says `omni-bmo`, resolve it to `codysumpter-cloud/omni-buddy`.

## Priority Repositories
- codysumpter-cloud/prismtek-apps
- codysumpter-cloud/buddy-brain
- codysumpter-cloud/prismtek-site
- codysumpter-cloud/omni-buddy
- codysumpter-cloud/prismtek-buddy-core
- codysumpter-cloud/agentmemory
- Automind-Lab/automindlab-stack
- Automind-Lab/bmo-stack

## High-Priority current PRs (As of 2026-05-06)

### prismtek-apps
- #118 fix: force CodeQL enabled (Critical: Unblocks release-candidate checks)
- #117 Runtime update
- #116 Add BeMore Buddy Windows shell and Gemma 4 GPT gateway
- #115 Add read-only Buddy Symphony Mission Control panel

### buddy-brain
- #309 Add WorldBox AgentCraft safe tools
- #307 Add Buddy Symphony orchestration contract
- #306 Add optional AgentCraft local observability bridge
- #305 feat(specs): add BMO spec gate v1

### prismtek-site
- #68 feat: add account-scoped Buddy WebUI
- #67 feat(site): add BMO WebUI surface

### omni-buddy
- #6 Add repo health files and lightweight automation
- #5 Integrate context-mode session continuity
- #4 Add Buddy runtime boundary plan
- #3 remove generated skill artifact files
- #2 apply fork evolution skills
- #1 transport contract and remote operator mode docs

### prismtek-buddy-core
- #2 Add Buddy visual contracts and T-Rex style packs
- #1 first commit scaffold

### agentmemory
- #2 add local provider and resilient skill extraction
- #1 enhance ProceduralMemory

### Automind-Lab/automindlab-stack
- #51 Harden Enterprise App Factory spec contract pipeline
- #50 Add OMX + Codex NIM + claw-code Mission Control surface
