# VPS Agent Access Map

Updated: 2026-05-11 14:22

## VPS
- Host: `187.77.223.224`
- Hermes secrets location for Alpaca paper trading: `~/.hermes/secrets/alpaca.json`
- API endpoint: `https://paper-api.alpaca.markets/v2`
- Key material: `[REDACTED]`

## Local vault
- iCloud Obsidian vault: `/Users/codysumpter/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault`
- Local fallback created earlier: `/Users/codysumpter/knowledge-vault/Alpaca_Keys.md` — contains redacted credential pointer content only; do not expand secrets in notes.

## Durable sync requirement
VPS cannot depend on Mac iCloud availability. Preferred pattern:
1. Keep operational docs in this vault.
2. Mirror non-secret vault docs to `/opt/knowledge-vault/KnowledgeVault` on VPS via git/rsync.
3. Keep secrets only in `.hermes/secrets` or platform keychains.
