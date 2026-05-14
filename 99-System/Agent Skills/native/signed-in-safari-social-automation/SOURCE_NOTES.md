# Signed-in Safari Social Automation — Source Notes

Date: 2026-05-13  
Status: Created locally in Hermes and mirrored as sanitized KnowledgeVault source notes.

## Local Hermes skill

- Skill: `signed-in-safari-social-automation`
- Local path: `/Users/codysumpter/.hermes/skills/social-media/signed-in-safari-social-automation/SKILL.md`
- Purpose: Use signed-in Safari via Apple Events JavaScript when isolated browser sessions cannot access the user's real login state.

## Confirmed procedure

- Use the real signed-in Safari session through Apple Events JavaScript.
- Do not rely on isolated browser tool sessions for logged-in browser state.
- Avoid paid or rate-limited APIs when the approved Safari DOM path works.
- Use React-safe native setters plus `input` and `change` events for controlled fields.
- Keep receipts secret-free.
- Remove duplicate skill references when ambiguous skill loading occurs.
- Verify the skill loads cleanly by bare name.

## Supported flows

- X profile update flow.
- X native post compose flow.
- YouTube Studio verification flow.
- Secret-free receipt generation.

## Credential storage receipt

Secrets were stored in local Hermes secure env locations with owner-only file permissions. Do not copy raw secrets into KnowledgeVault.

Expected local locations:

- `/Users/codysumpter/.hermes/.env`
- `/Users/codysumpter/.hermes/hermes-agent/.env.x`
- `/Users/codysumpter/.hermes/hermes-agent/.env.google`

Expected file mode:

```txt
-rw-------
```

## Obsidian / KnowledgeVault private inventory

A private credential inventory note was created locally at:

`/Users/codysumpter/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault/00-Private/Credentials/Prismtek Social Automation Credentials.md`

The note should store only:

- where secrets live,
- which key names are expected,
- setup receipts,
- safety rules.

It must not store raw passwords, tokens, API keys, cookies, or login codes.

## Safety rules

- Require explicit user approval before using signed-in Safari automation.
- Never export cookies or sessions.
- Never request passwords or MFA codes in notes.
- Never claim public visibility until verified through a public or logged-out path.
- Treat account-changing actions as external-action risk.
