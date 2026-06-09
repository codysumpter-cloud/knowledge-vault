# Note Quality Linter

Status: active
Owner: Prismtek / Buddy ecosystem
Privacy: public
Last verified: 2026-06-09

## Purpose

`note_quality_linter.py` checks markdown notes for basic agent-readiness.

It helps keep KnowledgeVault useful as a retrieval layer by flagging notes that are hard for agents to trust, route, or summarize.

## What it checks

The linter checks for:

- top-level title
- short opening summary
- recommended metadata on important notes
- important project-note sections
- generated-content marker reminders

It is intentionally lightweight and dependency-free.

## Run it

From the vault root:

```bash
python3 "99-System/Automation/note_quality_linter.py"
```

Print JSON output:

```bash
python3 "99-System/Automation/note_quality_linter.py" --json
```

Fail on warnings:

```bash
python3 "99-System/Automation/note_quality_linter.py" --strict
```

Check specific files:

```bash
python3 "99-System/Automation/note_quality_linter.py" README.md AGENTS.md
```

## How to use findings

- Treat errors as fix-now problems.
- Treat warnings as agent-readiness improvements.
- Treat info findings as review reminders.

Do not blindly rewrite human-authored notes. Prefer small, additive fixes.

## Relationship to Vault Doctor

`vault_doctor.py` checks safety and publication hazards.

`note_quality_linter.py` checks knowledge shape and retrieval quality.

Run both before claiming a vault maintenance pass is complete.
