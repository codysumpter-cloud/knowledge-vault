# Content Report 002 — Signed-in Safari Social Automation Skill

Date: 2026-05-13  
Status: Completed / Sanitized for repo storage

## Summary

A local Hermes skill named `signed-in-safari-social-automation` was created to document the working procedure for using the user's real signed-in Safari session through Apple Events JavaScript when isolated browser automation cannot access logged-in X, YouTube, or Google state.

## Local Hermes Skill Receipt

- Skill: `signed-in-safari-social-automation`
- Local path: `/Users/codysumpter/.hermes/skills/social-media/signed-in-safari-social-automation/SKILL.md`
- Verified load path: bare skill name works after duplicate reference cleanup.

## Capability Captured

- Use real signed-in Safari via Apple Events JavaScript.
- Do not rely on isolated browser sessions for logged-in browser state.
- Avoid paid or rate-limited APIs when approved Safari DOM automation works.
- Use React-safe native setters plus `input` and `change` events.
- Support X profile update flow.
- Support X native post compose flow.
- Support YouTube Studio verification flow.
- Produce secret-free receipts.

## Technical Discovery

Normal isolated browser tooling does not inherit the user's physical Safari login. Safari Apple Events JavaScript automation can operate against the signed-in local Safari session when approved.

System Events keystrokes remain blocked unless Accessibility permissions are enabled, but Safari DOM automation is enough for many logged-in web workflows.

## Credential Storage Receipt

Secrets were stored locally in Hermes-controlled env files with owner-only permissions. Raw secrets are intentionally excluded from this report.

Local files:

- `/Users/codysumpter/.hermes/.env`
- `/Users/codysumpter/.hermes/hermes-agent/.env.x`
- `/Users/codysumpter/.hermes/hermes-agent/.env.google`

Expected mode:

```txt
-rw-------
```

## Private Credential Inventory Note

A private inventory note was created locally in Obsidian/KnowledgeVault:

`/Users/codysumpter/Library/Mobile Documents/iCloud~md~obsidian/Documents/iCloud Vault/KnowledgeVault/00-Private/Credentials/Prismtek Social Automation Credentials.md`

The note stores only:

- where secrets live,
- which key names are expected,
- setup receipts,
- safety rules.

It must not store raw passwords, tokens, API keys, cookies, or login codes.

## Safety Rules

- Require explicit user approval before using signed-in Safari automation.
- Never export cookies or sessions.
- Never request or store passwords, API keys, tokens, or MFA codes in notes.
- Treat profile edits, posting, replies, DMs, or account changes as external-action risk.
- Public visibility must be verified separately from local UI publication.

## Next Move

Use `/skill signed-in-safari-social-automation` when X, YouTube, or Google browser login automation fails but Safari is already signed in and the user explicitly approves local Safari automation.
