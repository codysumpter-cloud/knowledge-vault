---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

- **Obsidian Sync/iCloud Drive pitfall (macOS):** Obsidian's iCloud container is not the normal `~/Library/Mobile Documents/com~apple~CloudDocs/` top-level iCloud folder. Check `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/` for Obsidian-created vaults (for this user, `iCloud Vault/KnowledgeVault`). A previous session failed by moving a vault to `com~apple~CloudDocs`; always search the Obsidian iCloud container before assuming the generic iCloud Drive path.
- **Mobile Plugin Activation:** Community plugins installed via filesystem on Mac may not automatically enable on iOS. User must manually toggle the plugin **ON** in Settings $\rightarrow$ Community Plugins and may need to trust plugins/disable Restricted Mode.
- **Mobile UI Fallback:** Because the mobile app can be slow to hydrate plugins or exhibit "No commands found" in the palette, always provide a `Mobile Command Center.md` note with direct wikilinks to the daily notes and dashboards.
- **Vault package ZIP safety:** When applying a ZIP that contains a top-level vault folder, strip that prefix into the real vault root but skip any path containing `.git` (including nested repo `.git` folders) so the package does not overwrite Git internals. On macOS, shell installers should not assume GNU `date -Is` or `flock`; use BSD-compatible timestamps (`date '+%Y-%m-%dT%H:%M:%S%z'`) and an atomic `mkdir` lock fallback.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

### Interactive stack install + safe commit review

When applying or committing an Obsidian interactive/plugin stack, treat it as a live vault release, not a generic code commit:

1. Verify status first with `git status --short --branch`; do not pull into a dirty vault.
2. Correct plugin IDs before installing. Known pitfall: `style-settings` should be `obsidian-style-settings` in `.obsidian/community-plugins.json`, `.obsidian/plugin-profiles/*.json`, and stack manifests.
3. Do not auto-install archived, exact-ID-missing, or push-protection-risk plugins. Known pitfall: skip `dbfolder` unless the user accepts archived plugin risk; leave `obsidian-projects` skipped if the registry does not expose that exact ID. Also skip tracking bundled `smart-composer` runtime files: GitHub push protection can flag its packaged `main.js` for embedded Google OAuth client credentials. If Smart Composer is desired, mark it skipped in the manifest and install/enable it manually from Obsidian's community store rather than committing the bundled payload. Use Make.md + Metadata Menu + Advanced Canvas + dashboards/Kanban/Tasks as the replacement layer.
4. Stage essential runtime files for every enabled plugin (`manifest.json`, `main.js`, `styles.css`) but do not stage plugin `data.json` unless explicitly reviewed.
5. Before commit, run `git fetch origin main` then `git status --short --branch`; if the vault is behind/diverged, stop and report rather than committing or pushing.
6. For one-file or cleanup commits, verify the **entire** staged set with `git diff --cached --name-only`, not just the paths you just added. `git stash pop`, conflict resolution, or interrupted runs may have left unrelated tracked files staged; do not include them silently.
7. Show the final staged list and scan it for secrets/private files/ZIPs/security paths before asking for commit approval.

Detailed commands: `references/interactive-stack-git-review.md`. Extra release/push-protection and scoped-cleanup notes: `references/obsidian-git-release-safety.md`.

### Active operating-system vaults, not template dumps

When the user asks for an Obsidian "operating system", do not stop at template files or static folders. Build live entry points and commands:

1. Create/update a dashboard note that links to today's note, inbox, activity log, current release receipts, and mobile command center.
2. Create the actual daily note/activity log/inbox files for the current date, not just templates for future dates.
3. If installing a custom plugin, create `.obsidian/plugins/<id>/manifest.json`, `main.js`, `styles.css` as needed, and add command names that are searchable both as slash commands and plain-language aliases.
4. Register/open the vault, then verify the Obsidian process starts. Still report plugin enablement as a user-visible gate if Restricted Mode/community plugin toggles require GUI confirmation.

### Register an Obsidian vault without GUI sign-in

Obsidian vaults are filesystem folders; account sign-in is only required for the app's cloud services. To preconfigure a vault while the user is away:
1. Create or locate the vault folder, ideally under `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/` when the user wants Obsidian+iCloud.
2. Create `.obsidian/` with `app.json`, `core-plugins.json`, `daily-notes.json`, and `templates.json` as needed.
3. Register the vault in `~/Library/Application Support/obsidian/obsidian.json` (lowercase `obsidian`) under `vaults` with `{ "path": "ABSOLUTE_PATH", "ts": <millis>, "open": true }`.
4. Set `OBSIDIAN_VAULT_PATH="ABSOLUTE_PATH"` in `~/.hermes/.env` so future agent sessions use the same folder.
5. Open with `open "obsidian://open?vault=<VaultName>" || open -a Obsidian` for GUI pickup.

For a VPS/remote agent mirror, `rsync` the vault to a server path and set `OBSIDIAN_VAULT_PATH` there too. Exclude private credential notes and workspace files (`00-Private/Credentials/*.md`, `.obsidian/workspace*.json`, `.git/`, `.DS_Store`).

### Mobile custom commands and dashboard fallbacks

When creating an Obsidian "operating system" vault (daily notes, metrics, quick capture, activity logs, `/today` and `/close-day` workflows), treat custom plugins as an enhancement, not the only access path. Mobile devices may show **"No commands found"** until Restricted Mode is disabled, the community plugin is enabled on that device, and the app is restarted. Always create a `Mobile Command Center.md` with direct wikilinks to today's note, inbox, activity log, and live dashboard before claiming the workflow is ready. Prefer command aliases that work with search (`Today - Start day...`) in addition to slash-style names (`/today`). See `references/mobile-command-dashboard.md`.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

If the user provides an `obsidian://open?vault=...&file=...` URL, do not assume the `file=` value is at the vault root. URL-decode the file target, try the direct path first, then search filenames under the vault (for example `*2026-05-11*`) and inspect likely dashboard/daily/activity-log paths. Obsidian may resolve bare note names through its index even when files live in folders like `01-Dashboard/Daily/` or `01-Dashboard/Activity Log/`.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For simple appends such as access credentials, receipts, or daily-log entries, never overwrite an existing daily note with a small replacement block. First read/search the target note, then append a timestamped section or patch under a stable heading. If a credential must be stored, keep the response concise and avoid reprinting secrets unless the user explicitly needs the value.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

## References

- `references/macos-icloud-vault-setup.md` — known-good macOS Obsidian+iCloud vault registration, `.obsidian` setup, Hermes env, VPS mirror, and verification recipe.
- `references/mobile-command-dashboard.md` — operating-system dashboard setup with mobile-safe fallbacks for custom commands like `/today`, including Restricted Mode/plugin pitfalls and verification commands.
- `references/interactive-stack-verification.md` — safe verification/staging workflow for Obsidian interactive-stack packages in Git-tracked vaults, including skipped plugin diagnosis and forbidden staged-path checks.
- `references/interactive-stack-git-review.md` — commit-readiness reference for plugin ID correction, archived/renamed plugin handling, enabled-plugin runtime-file staging, and divergence stop gates.
- `references/obsidian-git-release-safety.md` — scoped cleanup/one-file commit gates, stash-pop conflict handling, and GitHub push-protection remediation for bundled plugin payloads.
