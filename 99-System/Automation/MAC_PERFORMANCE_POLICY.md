# Mac Performance Policy for Vault and Agent Maintenance

Date: 2026-05-13
Owner: Prismtek
Applies to: Hermes agent, Vault Steward, local Obsidian/Git automation, future Buddy-agent maintenance

## Goal

Keep KnowledgeVault and agent memory current without making Prismtek's Mac feel slower.

## Defaults

- No always-on repo crawlers.
- No recursive full-disk scans.
- No cloning all GitHub repositories.
- No model downloads or builds during maintenance.
- No Docker, npm install, Xcode build, indexing, or local LLM inference unless explicitly requested.
- No scheduled work more frequent than daily.
- No work while another maintenance run is active.

## Allowed low-impact work

- Read small markdown files.
- Update project index files.
- Fetch GitHub repository metadata.
- Run `git status`.
- Run explicit, reviewed `git add` commands.
- Commit and push public-safe vault notes.

## Required local safeguards

Use low priority for scheduled jobs:

`nice -n 19`

Use a lock file so jobs do not overlap.

Use quick exits when Mac state is not suitable:

- battery below 35 percent and not charging
- thermal pressure is not nominal
- load average is already high
- another run is active

## Scheduling rule

If scheduled locally, run once daily at a low-friction time. Do not run every few minutes.

Prefer GitHub Actions for public metadata refreshes when possible. Prefer local runs only for vault-local private context that should not leave the Mac.

## Prohibited by default

- `git add .`
- background file watchers over the whole vault
- recursive grep over home directory
- `find /` or wide filesystem scans
- all-repo clone/sync loops
- launching OpenClaw work
- writing private repo metadata into public tracked files

## Report after each run

Use a compact summary:

- what changed
- what was skipped
- whether performance safeguards passed
- whether any manual action is needed
