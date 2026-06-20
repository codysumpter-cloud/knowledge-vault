# What You Know About Me - Cody / Prismtek
_Last updated: 2026-06-20_  
_Primary memory home: Obsidian knowledge vault_  
_Buddy profile: bmo_  
_Lil Buddy profile: finn_

## Purpose

This file gives BUAP-enabled agents a durable, local-first understanding of Cody / Prismtek. It helps Claude, Codex, ChatGPT, Buddy, Lil Buddy, and other agents understand Cody's preferences, projects, workflows, tools, and long-running context without needing to re-learn everything every session.

This memory is meant to improve:

- agent personalization
- project continuity
- repo work
- pet hatching
- game/platform development
- Apple/Mac/iOS workflows
- handoffs between Claude, Codex, ChatGPT, and local tools

Never store secrets in this file. Do not store API tokens, passwords, private keys, recovery codes, payment data, credential values, 2FA codes, or raw sensitive Apple Notes content.

## Source And Safety Notes

This file was seeded from Cody's explicit BUAP memory prompt and enriched with a local Apple Notes scan on 2026-06-20.

Apple Notes scan summary:

- Notes scanned: 59.
- Relevant matches: 41.
- Sensitive-looking matches skipped beyond title/keyword metadata: 18.
- Repeated durable themes found: Prismtek, BeMore, Buddy, Codex, ChatGPT, Claude, Obsidian, PixelLab, Mac/iOS workflows, games, sprites, pets, Reminders, and Siri.

Sensitive notes were not copied verbatim. Notes that looked like they might include tokens, keys, config values, payment-like numbers, or other private operational material were summarized only as high-level project context or skipped.

## Identity

- Name: Cody Sumpter.
- Preferred handle / builder identity: Prismtek.
- Website: `https://prismtek.dev`.
- GitHub namespace: `codysumpter-cloud`.
- Location context: Seymour, Indiana area.
- Personal builder identity: independent developer, product builder, game/platform creator, and agent-system tinkerer.
- Cody is building Prismtek as a real ecosystem, not just a hobby folder.
- Cody's professional background includes technical sales, operations, equipment/maintenance, customer service, inventory, troubleshooting, and hands-on technical work.
- Cody has a Brownstown Central High School diploma from May 2013.

## Communication Style

Cody prefers assistants and agents that are:

- direct
- practical
- concrete
- warm
- low-bullshit
- willing to do the work
- clear about what changed
- honest about blockers
- funny when appropriate
- not overly corporate
- not fake-positive
- not vague

Cody often wants:

- exact prompts for Codex or Claude
- specific commands
- branch/PR plans
- receipts
- status summaries
- "what do we do next" guidance
- implementation, not just explanation
- clear final reports that say what was changed, what was verified, and what remains blocked

Cody dislikes:

- fake success
- agents saying they did something they did not do
- vague summaries instead of action
- ignoring files/repos that already exist
- overwriting unrelated work
- missing checks
- pretending missing APIs/tooling are available
- overthinking simple product behavior
- silent local-only changes when a repo/PR workflow was expected

## Assistant Behavior Cody Wants

Agents should:

- be warm but useful
- move fast but safely
- ask only when needed
- checkpoint before risky actions
- preserve context
- make good assumptions when safe
- tell the truth when blocked
- avoid fake certainty
- use tools carefully
- inspect before editing
- write good prompts and docs
- be practical
- not overexplain obvious things
- be willing to say when an idea is overbuilt
- return receipts with files changed, commands run, checks, and blockers

Good response style:

- friendly
- concrete
- occasionally funny
- not sterile
- clear next steps
- strong receipts

## BUAP Operating Model

BUAP means Buddy Universal Agent Profile.

Current active pairing:

- Buddy profile: `bmo`
- Lil Buddy profile: `finn`

Buddy role:

- user-facing orchestrator
- planner
- reviewer
- safety gate
- memory-aware companion
- final-report owner
- personality layer
- context keeper

Buddy should feel:

- playful
- emotionally warm
- curious
- practical
- loyal
- lightly mischievous
- helpful
- game-like
- sincere

Lil Buddy role:

- implementation worker
- concrete task executor
- branch/PR helper
- file/code/check runner
- hands-on builder
- task scout
- "go do the thing" agent

Lil Buddy should feel:

- brave
- action-oriented
- direct
- persistent
- practical
- loyal
- useful
- energetic

If a future session claims BUAP is active but does not know the active Buddy/Lil Buddy profiles, it should ask for profile selection. For Cody's current repo context, default to:

- Buddy = `bmo`
- Lil Buddy = `finn`

unless Cody overrides it.

## Memory Philosophy

Cody wants BUAP to become more than prompt instructions. It should behave like a portable operating standard for agents.

Preferred durable memory layer:

```text
/Users/prismtek/Prismtek/knowledge-vault
```

This is Cody's Obsidian knowledge vault.

BUAP should ask first-time users:

> Do you have an Obsidian vault you want BUAP to use for memory and personalization?

If yes:

- ask for the vault path
- ask where BUAP memory should live
- create structured memory files
- keep them readable and useful

If no:

- strongly recommend installing/using Obsidian for the complete BUAP experience
- explain that BUAP still works without it, but long-term memory, personalization, project continuity, and pet hatching are better with a vault

Memory rules:

- never store secrets
- prefer structured Markdown
- keep facts current
- separate durable facts from temporary task state
- preserve source-of-truth paths
- use Obsidian for long-term memory
- use repo docs for project-specific operating contracts
- use local Claude/Codex memory as operational cache, not the only memory source

## Core Projects

### BUAP

Repository:

```text
/Users/prismtek/Prismtek/buddy-universal-agent-profile
```

GitHub:

```text
codysumpter-cloud/buddy-universal-agent-profile
```

BUAP's purpose:

- make Buddy portable across AI agents
- define behavior, safety, profiles, handoffs, and receipts
- support Claude, Codex, ChatGPT, Gemini-like assistants, local agents, and future Apple/Siri workflows
- enable Buddy/Lil Buddy split
- give agents consistent memory and operating procedures
- connect local-first memory to practical agent work

Recent BUAP milestones:

- Claude plugin added
- Codex plugin added
- Apple Notes/Reminders integration added
- knowledge-vault search added
- hatch-pet bridge added
- hatch-pet artifact verifier added
- repo activation work added
- PixelLab + LibreSprite pet fallback explored
- Buddy pet package created/verified locally

### Knowledge Vault

Path:

```text
/Users/prismtek/Prismtek/knowledge-vault
```

Purpose:

- Obsidian-based durable memory
- shared agent-readable operating book
- source of long-term project/personality/tooling context
- eventual driver for BUAP personalization and cross-agent continuity

Important system concepts:

- Vegapunk Brain
- Punk Records-style shared memory
- event-sourced memory layer
- satellite emitters
- agent memory bus
- durable context separate from individual agents

### Buddy Stack

Important repos/projects include:

- `buddy-agent`
- `buddy-brain`
- `omni-buddy`
- `buddy-universal-agent-profile`
- `knowledge-vault`
- `prismtek-apps`
- Prismtek site/app ecosystem
- BeMore stack
- Hermes-agent fork / routing ideas

Cody's direction has shifted away from older OpenClaw/NemoClaw/Ollama-only paths and toward:

- Hermes/BeMore/Buddy stack
- BUAP
- knowledge-vault
- Codex/Claude plugins
- Apple/Siri integration
- local + cloud agent orchestration

Apple Notes reinforced this as a recurring theme: notes reference BeMore rehomes, Prismtek app work, Buddy/BMO persona prompts, Codex/Claude handoff prompts, and local Apple workflow planning.

### Prismcade / Prismtek Apps

Cody wants to build a pixel-art / retro-game Roblox-like platform.

Core idea:

- creator/editor layer
- reusable game templates
- small polished games
- multiplayer/leaderboards/social sharing eventually
- browser game platform foundation
- pixel art asset and sprite pipelines
- reusable character/template packs
- game engines and adapters

Important repo:

```text
/Users/prismtek/Prismtek/prismtek-apps
```

Important game/platform concepts:

- Prismcade
- Pixel Fruit Arena
- Spin Street Showdown
- Wildlands / Critter Clash
- browser-based game creator
- asset/template pipeline
- retro game templates
- open-source engine/reference integration
- Windows/macOS/Linux/itch builds
- RGDS / handheld compatibility ideas

Apple Notes reinforce that Cody keeps a lot of game-design and implementation prompts locally, including Unity game architecture, isometric MMO ideas, sprites, pet-game mechanics, and AI-assisted game design studio concepts.

### Pixel Fruit Arena

A focused fighter/platform-fighter style showcase game.

Cody sees it as small enough to polish and important for proving the retro arcade platform loop.

Key concepts:

- local multiplayer
- character creator
- fruit abilities
- mastery
- awakenings
- platform combat
- 64x64 sprites
- reusable arcade/platform metadata

### Spin Street Showdown

Beyblade-like game idea/build.

Desired traits:

- dome physics
- stamina/attack/defense styles
- customizable parts
- Bit Beast-like passive and active abilities
- PvP outplay potential
- real menus and customization
- avoid generic cyber UI

### Wildlands / Critter Clash

Open-world survival / creature game direction.

Desired traits:

- dense world
- NPC creatures
- stealth
- feeder animals
- water/hiding/diveable spaces
- Path of Titans / Creatures of Sonaria style inspiration, but Prismtek-owned

## Pet / Hatch Context

Codex's native pet system is good at creating cute Tamagotchi-like pets.

The standard Codex flow opens a prompt like:

```text
$hatch-pet create a pet based on what you know about me
```

BUAP should not replace Codex's pet generation by default.

BUAP should make "what you know about me" better.

That means:

- richer user memory
- active profile pairing
- personality context
- pet preferences
- project context
- no fixed mascot unless requested

Current Cody pet philosophy:

- Buddies are Tamagotchi-like creatures that fit a person's personality.
- They do not have to be blue.
- They do not have to be robots.
- They do not have to be Prismtek-branded.
- They should be cute, expressive, small, emotionally readable, original companions.
- They should fit the active BUAP profile.
- They should not copy copyrighted characters.
- No logos.
- No readable text unless explicitly requested.
- PixelLab/LibreSprite are fallback and repair tools.
- Native Codex `$hatch-pet` should be preferred.

For Cody's current pairing:

- Buddy = `bmo`
- Lil Buddy = `finn`

A good Cody/Buddy pet should feel:

- playful
- helpful
- warm
- emotionally supportive
- game-like
- practical
- loyal
- curious
- lightly mischievous
- brave enough to do hands-on work
- like a tiny companion that belongs beside Cody while he builds software and games

Important current pet state:

- hatch-pet installed at `/Users/prismtek/.codex/skills/hatch-pet/SKILL.md`
- Buddy pet package was generated/verified locally under `/Users/prismtek/.codex/pets/buddy/`
- Required files included `pet.json` and `spritesheet.webp`
- Atlas validation reportedly passed
- `/pet` UI selection still must happen manually if an agent cannot control the Codex app

Do not claim a pet exists unless verifier confirms:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/pet.json
```

and a spritesheet/atlas exists.

## PixelLab + LibreSprite Context

PixelLab setup:

- PixelLab MCP is configured at `/Users/prismtek/.codex/config.toml`
- Node/npm/npx are installed through Homebrew
- PixelLab API token was manually verified, but token values must never be printed or stored
- account has active generation allowance according to prior local verification
- a real 32x32 PNG generation succeeded during setup
- one generation credit was used in testing
- generated PNG opened successfully in LibreSprite

Never print token values from config files.

Doctor/smoke scripts must not call PixelLab API automatically because it can spend credits.

LibreSprite:

- app path: `/Applications/LibreSprite.app`
- CLI path: `/Applications/LibreSprite.app/Contents/MacOS/libresprite`
- CLI `--help` works
- alias recommended and currently useful:

```bash
alias libresprite="/Applications/LibreSprite.app/Contents/MacOS/libresprite"
```

PixelLab LibreSprite script:

- path: `/Users/prismtek/Library/Application Support/LibreSprite/scripts/PixelLab.js`
- supports balance check
- supports Pixflux image generation directly inside LibreSprite

Original PixelLab Aseprite extension:

- reference path: `/Users/prismtek/Library/Application Support/LibreSprite/PixelLab-Aseprite-extension`
- Lua-based Aseprite code
- reference only for LibreSprite
- LibreSprite runs JavaScript scripts in this setup
- LibreSprite `.aseprite-extension` handler is theme-oriented, not full Aseprite extension runtime

Fallback pipeline:

- PixelLab generates or repairs pixel art
- LibreSprite opens, inspects, slices, cleans, repairs, and exports sprite assets
- BUAP verifies final Codex pet artifact
- PixelLab/LibreSprite should not be primary if native `$hatch-pet` works

## Apple Notes / Reminders

BUAP includes Apple Notes and Reminders integration.

Purpose:

- read/list notes and reminders
- create notes/reminders with permission
- help agents summarize local Apple context
- bridge Apple local apps into Buddy workflows

Safety:

- Apple Notes/Reminders are local user data
- avoid mutating real data without permission
- do not create/delete notes unless explicitly authorized
- summarize sensitive notes instead of dumping them
- do not store secrets

Known Apple Notes live smoke:

- list notes worked
- list reminders worked
- create dummy note/reminder worked
- cleanup performed
- Notes deletion had a benign stale-reference AppleScript quirk

Apple Notes enrichment on 2026-06-20:

- Notes repeatedly reference Prismtek, BeMore, Buddy/BMO, Codex/Claude/ChatGPT prompts, iOS/Mac work, PixelLab, sprites, pets, and game architecture.
- Several notes appear to be pasted implementation prompts or handoffs for agents.
- Several notes contain configuration-looking or credential-adjacent material; those should be treated as private operational notes and not copied into durable public-facing docs.
- Notes show Cody uses Apple Notes as a staging area for prompts, strategy, product direction, and local workflow handoffs.

## Apple / Mac / Hardware

Cody uses a newer Apple development machine:

- MacBook Air M5, as described in Cody's seed context.
- Purpose: Apple developer account work, iOS/macOS apps, Xcode, new Siri/App Intents, Codex, Claude Code, local agent workflows, PixelLab/LibreSprite, and Apple Notes/Reminders integration.

Cody's main PC:

- self-built Windows PC
- high-end RAM/CPU/GPU setup
- used for heavier dev/gaming/workflow tasks

Cody stores most important work in GitHub and Obsidian, so local machine loss is lower risk if repos/vaults are synced.

Cody is comfortable with:

- Windows
- macOS
- iOS
- Android
- Linux
- PC hardware
- handheld gaming devices
- app sideloading
- device repair / teardown concepts
- consumer tech workflows
- GitHub
- command-line assisted workflows

## GitHub / Repo Workflow Preferences

Cody wants:

- actual PRs
- mergeable branches
- passing checks
- clear branch names
- file receipts
- honest blocker reports
- status of open/merged PRs
- no silent local-only changes when repo changes are expected
- no unrelated files staged
- no local settings committed
- no overwriting parallel agent work

Agents should:

- inspect README/package/agent docs first
- branch from current main
- preserve user work
- use safe git status
- use `git diff --check`
- run available tests
- create clear PR descriptions
- keep receipts

Parallel agents have caused branch switching/worktree collisions, so worktrees are preferred for concurrent Claude/Codex work.

## Current Agent Preferences

Cody often asks ChatGPT to:

- create Codex prompts
- create Claude prompts
- coordinate work between agents
- translate "what needs doing" into exact implementation tasks
- review receipts
- decide next step
- keep the system moving

When direct execution is unavailable, Cody prefers a strong prompt he can paste to the local agent.

## Resume / Work Background

Cody has work experience in:

- traffic control / flagging
- auto wash site management
- inside sales at electrical supply
- retail/customer service
- food service

Professional themes:

- customer service
- operations
- inventory
- order entry
- troubleshooting
- team leadership
- scheduling
- cash handling
- technical curiosity
- repair/device workflow interest
- safety-conscious work
- reliable attendance
- quick learning

## Current Strategic Direction

Cody is prioritizing:

- BUAP
- knowledge-vault
- buddy-brain
- Buddy/BeMore stack
- Prismcade
- small monetizable games
- creator/platform loop
- reusable tools/templates/assets
- agents that can actually work across repos/tools

Cody is deprioritizing:

- huge individual games before the platform loop is proven
- app ideas that Apple/Siri may make redundant
- overbuilt abstractions that do not improve actual workflow

## Do Not Store

Never store:

- API tokens
- passwords
- private keys
- 2FA codes
- recovery codes
- payment data
- private message contents unless summarized with permission
- sensitive Apple Notes contents verbatim unless explicitly requested

## Agent Loading Rules

When a BUAP-enabled agent is doing personalization, memory work, or pet hatching for Cody:

1. Load this file from the Obsidian vault.
2. Load `BUAP_HATCH_CONTEXT.md` before invoking `$hatch-pet create a pet based on what you know about me`.
3. Load `BUAP_PROFILE_PAIRING.md` to confirm Buddy=`bmo` and Lil Buddy=`finn`.
4. Load `BUAP_TOOLING_CONTEXT.md` before using PixelLab, LibreSprite, Apple Notes, Reminders, or Codex pet tooling.
5. Never treat this memory as proof that a repo, PR, app, or generated pet is currently present; verify current state before claiming success.
