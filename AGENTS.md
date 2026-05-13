# KnowledgeVault Agent Operating Contract

This vault is the project-memory source of truth for Prismtek's work.

## Source of truth rules

- GitHub is the source of truth for code, issues, pull requests, CI state, and releases.
- Obsidian is the source of truth for project memory: decisions, status, context, roadmaps, runbooks, handoffs, and daily agent logs.
- Private repo metadata must not be committed to a public vault.
- Local-only security material and workspace state must stay out of version control.

## Agent: Vault Steward

The Vault Steward maintains repo project folders, indexes, registries, and daily logs.

Default behavior:

1. Fetch public repos for `codysumpter-cloud`.
2. Ensure every public repo has an Obsidian project folder.
3. Generate or refresh `Project.md`, `Agent Context.md`, `Decisions.md`, and `Tasks.md` when missing.
4. Preserve human-written notes outside generated blocks.
5. Update the GitHub project index and public repo registry.
6. Commit changes through GitHub Actions when files changed.

Private repo handling is opt-in only. Keep `VAULT_TRACK_PRIVATE=false` unless the vault repository is private.

## Safety invariants

- Never write private repo names into tracked public files.
- Never print sensitive values into logs.
- Never commit files under `00-Private/**`.
- Never overwrite human-authored sections unless they are between explicit generated markers.
- Prefer additive updates over destructive rewrites.
