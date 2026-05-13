---
name: github-access-management
description: Establish secure access for AI agents and VPS nodes to GitHub repos, managing identity conflicts and GitHub First requirements.
trigger: remote agent access configuration or SSH permission errors (Permission denied, Key already in use).
---

# GitHub Access & Identity Management

This skill governs the process of establishing secure, autonomous access for AI agents and remote VPS nodes to GitHub repositories, especially when dealing with identity conflicts.

## Implementation Workflow

### 1. Identity Audit
Determine if the request is from a specific GitHub user (e.g., `TNwkrk`) or a generic machine/VPS (e.g., `hermes@srv1425557`).

### 2. Access Vector Selection (Hierarchical)

#### A. Repository Deploy Keys (Surgical)
Use for repo-specific access not tied to a global user identity.
- **Command:** `gh repo deploy-key add <key_file> --repo <owner/repo> --allow-write --title "<Title>"`
- **Constraint:** A key can only be a deploy key for one repo unless it's a user-level key.

#### B. Collaborator Invites (User-Level)
Use when operating under a known GitHub User identity.
- **Command:** `gh api /repos/<owner>/<repo>/collaborators/<username> -X PUT -f permission=push`
- **Constraint:** Target user must "Accept" via browser/email.

#### C. HTTPS via PAT (The Nuclear Bypass)
Use when SSH identity conflicts (`key is already in use`) block deploy keys and users cannot accept invites.
- **Mechanism:** Fine-Grained PAT with `contents:write` permissions.
- **Config:** Set remote to `https://<token>@github.com/<owner>/<repo>.git`.
- **Pros:** Bypasses SSH identity checks and "Invite" bottlenecks.

## Pitfalls & Lessons

### The "Key Already in Use" Trap
**Symptom:** `HTTP 422: Validation Failed ... key is already in use`.
**Root Cause:** GitHub prohibits a key from being both a **User Account Key** (global) and a **Deploy Key** (repo-specific).
**Solution:** If a key is tied to a user, you cannot use it as a deploy key for another account. Either:
1. Remove key from the original user account.
2. Invite that user as a collaborator.
3. Switch to HTTPS via PAT.

### Personal Account Constraints
Personal accounts do not support "Teams" (`/orgs` API calls will 404). Use individual collaborator invites or deploy keys.

## Verification
- Run `git fetch` or `git ls-remote` from the remote node.
- Confirm the protocol (SSH vs HTTPS) matches the implemented solution.
