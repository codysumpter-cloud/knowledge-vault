# BUAP Tooling Context

_Last updated: 2026-06-20_

## Local-first memory

Primary vault:

```text
/Users/prismtek/Prismtek/knowledge-vault
```

Primary Cody memory file:

```text
/Users/prismtek/Prismtek/knowledge-vault/99-System/BUAP/WHAT_YOU_KNOW_ABOUT_ME.md
```

Hatch context:

```text
/Users/prismtek/Prismtek/knowledge-vault/99-System/BUAP/BUAP_HATCH_CONTEXT.md
```

Profile pairing:

```text
/Users/prismtek/Prismtek/knowledge-vault/99-System/BUAP/BUAP_PROFILE_PAIRING.md
```

## Apple Notes and Reminders

BUAP has a local macOS Apple Notes/Reminders bridge in:

```text
/Users/prismtek/Prismtek/buddy-universal-agent-profile/packages/buap-apple-notes-reminders
```

Use it for read-only listing/summarization unless Cody explicitly authorizes writes. Do not copy sensitive Apple Notes verbatim. Do not store secrets.

## Codex hatch-pet

Skill path:

```text
/Users/prismtek/.codex/skills/hatch-pet/SKILL.md
```

Verified pet output should live under:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/
```

Required files:

```text
pet.json
spritesheet.webp
```

BUAP verifier command:

```bash
cd /Users/prismtek/Prismtek/buddy-universal-agent-profile/packages/buap-hatch-pet
node dist/cli.js verify --name Buddy
```

Do not claim a pet exists unless the verifier confirms the files.

## PixelLab

PixelLab MCP config exists in Cody's Codex config:

```text
/Users/prismtek/.codex/config.toml
```

Never print config contents or token values. Doctor/smoke scripts must not call PixelLab API automatically because it can spend credits.

## LibreSprite

LibreSprite app:

```text
/Applications/LibreSprite.app
```

CLI:

```text
/Applications/LibreSprite.app/Contents/MacOS/libresprite
```

Recommended alias:

```bash
alias libresprite="/Applications/LibreSprite.app/Contents/MacOS/libresprite"
```

PixelLab LibreSprite script:

```text
/Users/prismtek/Library/Application Support/LibreSprite/scripts/PixelLab.js
```

Original Aseprite extension reference:

```text
/Users/prismtek/Library/Application Support/LibreSprite/PixelLab-Aseprite-extension
```

The extension is Lua-based Aseprite code and is reference-only for LibreSprite. LibreSprite runs JavaScript scripts in this setup.

## Safety reminders

- No secrets in memory files.
- No PixelLab API calls from doctor/smoke checks.
- No Apple Notes writes without explicit permission.
- No pet success claims without `pet.json` plus spritesheet/atlas verification.
- No destructive repo operations without confirmation.
