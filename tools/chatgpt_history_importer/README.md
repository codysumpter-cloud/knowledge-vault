# ChatGPT History Importer

This tool converts a ChatGPT data export into KnowledgeVault-friendly markdown digests.

It exists because KnowledgeVault is public and agent-readable. Raw ChatGPT transcripts should not be committed here. Instead, the importer reads an export locally, redacts obvious sensitive material, groups conversations by project/workstream, and writes reviewable summaries under `99-System/Memory/ChatGPT-History/generated/`.

## What this can ingest

- A ChatGPT export `.zip` downloaded from the official data export flow.
- An extracted ChatGPT export directory.
- A direct `conversations.json` file from an export.
- Manual `.txt` / `.md` batches copied from chats.

## What this cannot do

This tool cannot log into ChatGPT, scrape the ChatGPT sidebar, or directly access archived/unarchived chats from inside a ChatGPT conversation.

Unarchiving chats makes them visible in the user's ChatGPT UI, but it does not expose those conversations to an assistant in another chat. The assistant still needs either:

1. the official export zip / `conversations.json`, or
2. pasted conversation batches supplied by the user.

## Public-safety model

Default mode is conservative:

- no raw transcripts are written by default
- source messages are truncated into excerpts
- obvious secrets are redacted
- generated notes are marked as generated summaries
- results require human review before committing

Do not commit:

- raw export zip files
- full raw transcripts
- secrets, tokens, cookies, passwords, API keys, certificates, or `.env` contents
- private operational details
- local machine paths exposing sensitive workspace state
- account numbers, wallet data, or live trading credentials

## Basic usage

From the root of `knowledge-vault`:

```bash
python3 tools/chatgpt_history_importer/import_chatgpt_export.py \
  --input /path/to/chatgpt-export.zip \
  --output 99-System/Memory/ChatGPT-History/generated \
  --max-conversations 500
```

For an extracted export:

```bash
python3 tools/chatgpt_history_importer/import_chatgpt_export.py \
  --input /path/to/export/conversations.json \
  --output 99-System/Memory/ChatGPT-History/generated
```

For pasted/manual batches, put text files in a local-only folder outside Git and run:

```bash
python3 tools/chatgpt_history_importer/import_chatgpt_export.py \
  --input /path/to/manual-chat-batches \
  --manual-text \
  --output 99-System/Memory/ChatGPT-History/generated
```

## Output layout

```txt
99-System/Memory/ChatGPT-History/generated/
├── by-date/
├── by-project/
├── indexes/
│   ├── conversations.json
│   ├── projects.json
│   └── decisions.json
└── REVIEW_CHECKLIST.md
```

## Review checklist before commit

1. Read `REVIEW_CHECKLIST.md`.
2. Search generated notes for secrets or sensitive values.
3. Delete or rewrite any note that exposes private details.
4. Keep raw export files out of the repository.
5. Commit only the reviewed markdown/index outputs.

## Design intent

The goal is a vault that future agents can digest quickly:

- what was built
- why decisions were made
- which repos matter
- which tasks remain open
- what safety boundaries apply
- where source-of-truth code/PRs live

This importer is intentionally boring and local-first. Reliable little goblin machine, not magic smoke.
