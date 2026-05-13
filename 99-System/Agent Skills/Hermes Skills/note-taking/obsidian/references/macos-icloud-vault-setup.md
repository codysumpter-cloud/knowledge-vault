# macOS iCloud Obsidian Vault Setup Reference

Use this when the user asks to set up Obsidian remotely or says the vault is in iCloud.

## Known-good pattern

- Obsidian iCloud container: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`
- Generic iCloud Drive container: `~/Library/Mobile Documents/com~apple~CloudDocs/`
- Prefer the Obsidian container when the user says “iCloud Vault” or uses Obsidian Sync/iCloud.

## Minimal setup commands

```bash
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault"
mkdir -p "$VAULT/.obsidian" "$VAULT/00-Inbox" "$VAULT/00-Private/Credentials" "$VAULT/06-Templates"
python3 - <<'PY'
from pathlib import Path
import json, time, os
vault = Path(os.path.expanduser('~/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault'))
(vault/'.obsidian/app.json').write_text(json.dumps({
  'alwaysUpdateLinks': True,
  'newFileLocation': 'folder',
  'newFileFolderPath': '00-Inbox',
  'attachmentFolderPath': '07-Attachments',
  'showLineNumber': True
}, indent=2))
(vault/'.obsidian/core-plugins.json').write_text(json.dumps([
  'file-explorer','global-search','switcher','graph','backlink','outgoing-link',
  'tag-pane','page-preview','daily-notes','templates','bookmarks','outline','properties'
], indent=2))
app = Path(os.path.expanduser('~/Library/Application Support/obsidian'))
app.mkdir(parents=True, exist_ok=True)
obs = app/'obsidian.json'
data = json.loads(obs.read_text()) if obs.exists() else {}
data.setdefault('vaults', {})['knowledgevault'] = {'path': str(vault), 'ts': int(time.time()*1000), 'open': True}
obs.write_text(json.dumps(data, indent=2))
PY
```

## Agent env

Add to local Hermes env:

```bash
OBSIDIAN_VAULT_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault"
```

For VPS mirrors:

```bash
ssh root@HOST 'mkdir -p /opt/knowledge-vault/KnowledgeVault'
rsync -az --delete \
  --exclude '.git/' \
  --exclude '.obsidian/workspace*.json' \
  --exclude '00-Private/Credentials/*.md' \
  --exclude '.DS_Store' \
  "$VAULT/" root@HOST:/opt/knowledge-vault/KnowledgeVault/
ssh root@HOST 'printf "%s\n" "OBSIDIAN_VAULT_PATH=/opt/knowledge-vault/KnowledgeVault" >> /root/.hermes/.env'
```

## Verification

- Local: vault directory exists, `Home.md` exists, `.obsidian/core-plugins.json` exists, Obsidian `obsidian.json` contains the absolute path.
- Git: credential notes show as ignored, e.g. `!! 00-Private/Credentials/Alpaca.md`.
- VPS: `test -f /opt/knowledge-vault/KnowledgeVault/Home.md` and `grep OBSIDIAN_VAULT_PATH /root/.hermes/.env`.
