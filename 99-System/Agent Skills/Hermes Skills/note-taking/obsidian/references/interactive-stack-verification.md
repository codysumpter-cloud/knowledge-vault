# Obsidian Interactive Stack Verification + Safe Commit

Use this reference when applying or verifying an Obsidian plugin/dashboard package in a Git-tracked vault, especially on a constrained Mac.

## Guardrails

- Do not pull into a dirty vault.
- Do not run `git add .`.
- Do not stage ZIP packages, `.git` paths, logs, backups, security folders, credentials, secrets, tokens, private notes, `.env`, or key files unless explicitly requested.
- Avoid watchers, daemons, crawlers, npm installs, Docker, Xcode, model downloads, and indexing jobs.

## Verification commands

From the vault root:

```bash
git status --short --branch

grep -i "style-settings\|obsidian-projects\|dbfolder\|skipped\|failed" \
  "99-System/Logs/obsidian-plugin-install.log" \
  "99-System/Logs/obsidian-interactive-stack-install.log"
```

For skipped plugins, distinguish:

1. exact Community Plugin registry ID missing,
2. renamed/plugin-ID mismatch,
3. unavailable GitHub release or archived repo,
4. replaced by another installed plugin,
5. better installed manually from Obsidian Community Plugins.

A useful registry probe is:

```bash
python3 - <<'PY'
import json, urllib.request
wanted = {'style-settings', 'obsidian-projects', 'dbfolder'}
url='https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json'
data=json.load(urllib.request.urlopen(url, timeout=20))
for pid in sorted(wanted):
    exact=[p for p in data if p.get('id') == pid]
    fuzzy=[p for p in data if pid.replace('obsidian-','') in (p.get('id','')+' '+p.get('name','')).lower()]
    print('\nID', pid)
    print('exact', exact[:3])
    print('fuzzy', fuzzy[:10])
PY
```

Known examples from this package class:

- `style-settings` is usually `obsidian-style-settings` in the registry (`obsidian-community/obsidian-style-settings`).
- `dbfolder` may refer to `RafaelGB/obsidian-db-folder`, which has been archived; prefer manual/BRAT only with explicit approval.
- `obsidian-projects` is not a stable exact registry ID; verify intended replacement or manual install path.

## Safe staging pattern

Use explicit paths only, then immediately inspect status:

```bash
git add \
  .obsidian/community-plugins.json \
  .obsidian/core-plugins.json \
  .obsidian/plugin-profiles \
  .obsidian/plugins/advanced-canvas \
  .obsidian/plugins/juggl \
  "01-Dashboard" \
  "30 - Projects/GitHub" \
  "99-System/Agents" \
  "99-System/Automation" \
  "99-System/Handoffs" \
  "99-System/Memory" \
  "99-System/Obsidian" \
  "99-System/Repositories"

git status --short --branch
```

Before asking for review, run a staged forbidden-path check:

```bash
git diff --cached --name-only | grep -Ei '(^|/)\.git(/|$)|\.zip$|(^|/)(99-System/Security|.*(credential|secret|token|private|\.env|key).*)' || true
```

Report staged count and top-level buckets:

```bash
git diff --cached --name-only | wc -l | tr -d ' '
git diff --cached --name-only | awk -F/ '{print $1}' | sort | uniq -c
```

Stop before committing unless the user explicitly approves the staged file list.
