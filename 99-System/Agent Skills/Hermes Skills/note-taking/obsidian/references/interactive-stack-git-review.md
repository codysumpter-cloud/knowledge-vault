# Obsidian interactive stack Git review

Use this reference when applying or committing an Obsidian plugin/dashboard stack into a live vault.

## Guardrails

- Do not pull into a dirty vault. Use `git fetch origin main` only when checking remote state.
- Never use `git add .` in an Obsidian vault.
- Do not stage ZIP packages, `.git` paths, plugin `data.json`, private/security folders, workspace state, logs, or backups unless explicitly reviewed.
- If `git status --short --branch` shows `behind` or `diverged` after fetch, stop and report before committing or pushing.

## Plugin registry mismatches

- `style-settings` is the wrong enabled-plugin ID; the Community Plugin ID is `obsidian-style-settings` (`obsidian-community/obsidian-style-settings`). Replace it in `.obsidian/community-plugins.json`, `.obsidian/plugin-profiles/*.json`, and stack manifests before rerunning the installer.
- `dbfolder` maps to a historical archived DB Folder plugin. Do not auto-install it unless the user explicitly accepts archived plugin risk. Prefer Make.md + Metadata Menu as the replacement layer.
- If `obsidian-projects` is not exposed by the registry under that exact ID, leave it skipped; prefer Make.md, Metadata Menu, Advanced Canvas, dashboards, Kanban, and Tasks as the replacement layer.

## Runtime-file staging recipe

Stage essential runtime files for every enabled plugin, but not plugin settings/data files:

```bash
python3 - <<'PY' > /tmp/obsidian-enabled-plugin-runtime-files.txt
import json
from pathlib import Path

enabled = json.loads(Path('.obsidian/community-plugins.json').read_text())
for plugin in enabled:
    plugin_dir = Path('.obsidian/plugins') / plugin
    for filename in ('manifest.json', 'main.js', 'styles.css'):
        path = plugin_dir / filename
        if path.exists():
            print(path)
PY

xargs git add -- < /tmp/obsidian-enabled-plugin-runtime-files.txt
```

## Final review commands

```bash
git log --oneline origin/main..HEAD
git fetch origin main
git status --short --branch
# Stop if behind/diverged.

git diff --cached --name-status
git diff --cached --name-only | grep -Ei 'secret|token|credential|private|\.env|\.key|\.pem|\.p12|\.cer|certSigningRequest|99-System/Security|00-Private|\.zip' || true
```
