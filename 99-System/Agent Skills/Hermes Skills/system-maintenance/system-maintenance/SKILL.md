---
name: system-maintenance
description: Procedures for system cleanup, log archiving, and temporary file management.
---

# System Maintenance

Use this skill when performing cleanup tasks (deleting logs, tmp files, or caches) to ensure the user's preference for an audit trail is honored.

## Cleanup & Archiving Workflow

When the user asks for "cleanup" or "cleaning up":

1.  **Identify Targets**: Use `find` or `ls` to locate `.log`, `.tmp`, or `.bak` files in relevant directories (`~/.hermes`, `~/Documents`, or current working directory).
2.  **Assess Impact**: Check file sizes and ages.
3.  **Archive First (Crucial)**: Before deleting, create an archive note in the Obsidian KnowledgeVault (e.g., `Archive_Hermes_Logs_YYYY-MM-AST.md`).
    *   Use `read_file` to capture the content of the logs.
    *   Use `write_file` to append the content to the Obsidian archive with a timestamp and file path header.
4.  **Verify Archive**: Use `read_file` or `ls` on the new Obsidian note to confirm the content was successfully written.
5.  **Delete Originals**: Once the archive is verified, use `rm` via `terminal` to delete the original files.
6.  **Report Receipt**: Provide a summary of how many files were archived and how many were deleted.

## Pitfalls
- **Don't Delete Without Archiving**: Never delete logs without the Obsidian step unless explicitly told otherwise.
- **Large Files**: If a log file is extremely large (e.g., >100MB), do not try to read it into the context window; instead, just report its existence and ask if the user wants to "truncate" it via `terminal` instead of archiving.
- **Recursive Depth**: Avoid deep recursive searches (e.g., `**`) on the root or home directory to prevent timeouts; use `-maxdepth` with `find`.
