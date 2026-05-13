# Hermes Agent Mac Handoff

Date: 2026-05-13

What changed:

- KnowledgeVault is the project-memory source of truth.
- GitHub remains source of truth for code, issues, pull requests, CI, and releases.
- OpenClaw is retired for current work.
- Hermes-agent is the current main working agent system.
- Buddy-agent is being prepared to become the primary and eventually only agent repository.
- The new public fork `codysumpter-cloud/caveman` was added to the vault project map.

Hermes next steps:

1. Work only from the real `KnowledgeVault/` vault root.
2. Inspect before mutating: run `git status --short --branch` and verify the expected vault files exist.
3. Verify project folders for buddy-agent, buddy-brain, hermes-agent, knowledge-vault, and caveman.
4. Treat OpenClaw folders as historical/reference only.
5. Never run `git add .`; only add explicit public-safe paths.
6. Do not schedule anything unless Prismtek explicitly asks.

Mac performance rules:

- No watchers by default.
- No all-repo clone loops.
- No recursive home scans.
- No heavy indexing.
- No Docker, npm, Xcode, model downloads, or local inference as routine maintenance.
- If local maintenance is enabled, run at most once daily, low priority, with a lock file, and skip when battery, load, or thermal state is poor.

Local ZIP includes the full policy and runner:

- `99-System/Automation/MAC_PERFORMANCE_POLICY.md`
- `99-System/Automation/run-vault-steward-mac-safe.sh`
