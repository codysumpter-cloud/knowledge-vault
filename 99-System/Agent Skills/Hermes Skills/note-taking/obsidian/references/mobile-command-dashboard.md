# Obsidian Mobile Command Dashboard Pitfalls

Context: Setting up an Obsidian vault as an operating-system style dashboard with custom commands, daily notes, quick capture, activity logs, and agent workflows.

## Key Lessons

- Obsidian vault setup is filesystem-first, but custom command behavior depends on the app loading community plugins.
- On Obsidian mobile, a user typing `/today` and seeing **"No commands found"** usually means one of:
  - the custom community plugin has not synced to mobile yet,
  - Restricted Mode is still enabled,
  - the plugin is not enabled on that device,
  - the user is in a generic search/new-tab UI rather than Obsidian's command palette.
- Do not claim slash commands are usable until verified or until a fallback note exists.

## Robust Setup Pattern

1. Create the operating-system notes first so the vault works without plugins:
   - `Home.md`
   - `01-Dashboard/Live Command Center.md`
   - `01-Dashboard/Mobile Command Center.md`
   - `01-Dashboard/Daily/YYYY-MM-DD.md`
   - `01-Dashboard/Activity Log/YYYY-MM-DD.md`
   - `00-Inbox/Inbox.md`
   - `04-Runbooks/Agent Workflows/...`
2. Add plugin commands as enhancement, not the only access path.
3. Use mobile-friendly command names in addition to slash names:
   - `Today - Start day and build focus note`
   - `/today - Start day and build focus note`
   - `Close Day - metrics and reflection`
   - `/close-day - metrics and reflection`
4. Create a `Mobile Command Center.md` note with direct wikilinks to today's note, inbox, activity log, and dashboard.
5. Tell the user to search `Today` first, not only `/today`.

## Mobile Activation Instructions

If commands do not appear on mobile:
1. Open Obsidian Settings.
2. Go to Community plugins.
3. Turn off Restricted Mode / trust plugins.
4. Enable the custom dashboard plugin.
5. Restart Obsidian mobile.
6. Open the Command Palette and search `Today`.

## Verification

Run local checks before declaring success:

```bash
node --check '.obsidian/plugins/<plugin-id>/main.js'
python3 - <<'PY'
from pathlib import Path
import json
v=Path('/path/to/vault')
print({
 'mobile_launchpad': (v/'01-Dashboard/Mobile Command Center.md').exists(),
 'today_note': any((v/'01-Dashboard/Daily').glob('*.md')),
 'plugin_enabled': '<plugin-id>' in json.loads((v/'.obsidian/community-plugins.json').read_text()),
})
PY
```

For VPS mirrors, sync the vault but exclude private credentials and workspace state:

```bash
rsync -az --delete \
  --exclude '.git/' \
  --exclude '.obsidian/workspace*.json' \
  --exclude '00-Private/Credentials/*.md' \
  --exclude '.DS_Store' \
  "$VAULT/" root@HOST:/opt/knowledge-vault/KnowledgeVault/
```
