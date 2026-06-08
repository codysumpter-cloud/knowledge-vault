# Security Policy

KnowledgeVault is a public repository. Tracked files must be safe to publish.

## Boundary

- Public notes and public runbooks may be tracked.
- Private notes stay under `00-Private/`.
- Local security material stays under `99-System/Security/`.
- Do not store sensitive values in tracked files.

## Forbidden tracked paths

These paths must remain untracked:

```txt
00-Private/**
99-System/Security/**
99-System/Logs/**
99-System/Backups/**
99-System/Prompts/**
99-System/Templates/**
```

## Safe workflow rules

- Use allowlisted staging only.
- Do not use broad repository-wide staging commands.
- Run the vault doctor before opening a PR.

```bash
python3 "99-System/Automation/vault_doctor.py"
```

## Public claims policy

KnowledgeVault can contain plans, references, source indexes, and skill notes. Those notes do not prove that a feature is implemented in a runtime.

Use explicit status labels:

- `reference`
- `draft`
- `ported`
- `wired`
- `tested`
- `disabled`
- `public-alpha-safe`

Do not claim a Buddy-agent capability exists unless the Buddy-agent repository contains and verifies it.

## If sensitive material appears

1. Remove the material from active files.
2. Rotate or replace anything that may have been exposed.
3. Treat public history as already published.
4. Record only a sanitized incident note.
