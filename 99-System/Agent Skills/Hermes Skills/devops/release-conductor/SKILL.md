---
name: release-conductor
description: High-discipline release management for the Prismtek/BMO ecosystem.
---

# Prismtek Release Conductor Protocol

This skill governs the safe promotion of code from PRs to production builds across iOS, macOS, Windows, and AI platforms. The primary directive is **Zero-Risk Promotion**: no merge or release occurs without absolute verification.

## 🛡️ The Hard Rules (Non-Negotiable)
- **The Sovereign Path (Vault-First)**: For all infrastructure, cloud, and server deployments, the sequence MUST be: **GitHub (Source of Truth) $\rightarrow$ Knowledge Vault (Technical Spec) $\rightarrow$ Execution**.
    - Blind execution ("Running it up") without a documented spec in the Knowledge Vault is a failure of the protocol.
    - Every deployment must have a corresponding spec file (e.g., `deployment-spec.md`) before the first command is run.
- **No 'Blind' Merges**: Never merge a PR unless it is:
    - Not a draft.
    - Fully mergeable (no conflicts).
    - Up-to-date with the base branch.
    - Every required check is `SUCCESS` (Draft, queued, cancelled, failed, missing, stale, unknown, conflicted, or skipped-required checks are all BLOCKERS).
- **No Force/Bypass**: Do not force-push, bypass branch protection, delete branches, or rewrite shared history.
- **Receipt-Based Success**: Never claim a build, upload, or release is "done" without providing a durable receipt:\n    - GitHub Workflow URL\n    - Artifact Download Link\n    - Notarization/Signing result\n    - Release Page URL\n- **TestFlight Processing Gate**: For App Store Connect uploads, `Upload succeeded` / `Uploaded package is processing` is an upload receipt only. Do not mark TestFlight tasks complete until the exact platform/version/build is visible in TestFlight/App Store Connect or an Apple-side blocker has been identified. See `references/testflight-receipts-and-signing.md`.\n- **Smallest Safe Fix**: Prefer the smallest possible fix. If a fix is risky, create a PR or comment the blocker rather than attempting a direct fix on the main branch.\n- **Secret Hygiene**: Keep secrets out of logs, commits, and comments.\n- **DNS and Nameserver Changes Are Protected Release Actions**: Do not suggest, save, click through, or otherwise alter DNS providers, authoritative nameservers, Cloudflare zones, Hostinger DNS delegation, or cutovers for working domains unless Cody explicitly asks for that exact DNS action. Runtime/app/API failures must be diagnosed from services, logs, provider config, and health receipts first; DNS is not a default fix path. Example: Do not suggest moving prismtek.dev or automindlab.tech DNS to the VPS unless the user explicitly asks for a cutover. See the Knowledge Vault wiki page `DNS Guardrails` (infrastructure/dns-guardrails.md) for the current policy and verification receipts.\n- **Environment Awareness**: For Intel-based Mac hardware (e.g., MBP 15,2), prioritize memory efficiency. Avoid running heavy background services (HUDs, Directors) during `xcodebuild` to prevent swap-induced slowdowns.

## 🔄 The 4-Phase Execution Loop

### Phase 1: Read-Only Audit
### Phase 1: Read-Only Audit
1. **Dynamic Repository Resolution**: Before auditing or acting, resolve renamed repositories dynamically using `references/codex-prompt-config.md`.
    - Use `gh repo view <owner>/<repo>` to confirm the current canonical name and default branch.
    - Use current canonical names in all commands, comments, merge actions, and final reports.
    - Follow redirects and record the current repo name; do not fail if a redirect occurs.
    - Maintain a "Historical" column in reports for old names.
2. List all accessible repos in the target orgs.
3. List all open PRs.
4. Collect: PR number, title, draft state, base branch, head SHA, mergeability, and full check/workflow status.
5. Produce a **Blocker Table** for user approval before any action.

### Phase 2: Safe Fixes
1. Inspect logs for failing PRs.
2. Apply small, obvious fixes to the PR branch.
3. Run documented checks to verify the fix.
4. Comment on the PR with the change and remaining blockers.

**Surgical PR Resolution (for Conflicts/Mergeability):**
If a PR is `CONFLICTING` or not mergeable due to `main` drift:
- Do not force-push to the original branch.
- Clone to a temporary directory $\rightarrow$ create new branch from `main` $\rightarrow$ checkout target files from the original PR head $\rightarrow$ push $\rightarrow$ create new PR $\rightarrow$ close old PR as superseded.
- **Manifest Collision Handling**: When resolving conflicts in `operator-surface.manifest.json` or similar registration files, perform a **union merge**. Do not pick `ours` or `theirs`; manually combine all new component IDs, document shortcuts, and validation actions to ensure no functionality is lost.


**Triggering Stalled Checks:**
If a check (e.g., `task-readiness`) fails to re-run after a PR body edit:
- Apply a no-op commit using `git commit --allow-empty -m "chore: trigger check"` to force a fresh event payload.

### Phase 3: Controlled Merges
1. **Surgical Audit**: Before merging, verify the PR is `OPEN`, `isDraft: false`, `mergeable: "MERGEABLE"`, and all status checks (CI, Lint, CodeQL) are `SUCCESS`. `QUEUED` or `CANCELLED` are blockers.
- **Contract Check**: For BMO/Stack repos, verify the PR body contains both a `## Problem` and a `## Task contract` block. If missing, append these sections based on the PR goals to satisfy the `check_task_readiness.py` validator.
3. **Merge Strategy**: Use repo-preferred merge strategy.
4. **Post-Merge Health**: Verify the default branch head remains green after the merge. If it turns red, stop immediately and diagnose.

### Phase 4: Release Build Pipeline
1. **iOS (BeMore)**: Prepare build only after `prismtek-apps/main` is green. Verify Gemma 4 bundle checks and archive contents. When upload succeeds, keep the task open until TestFlight/App Store Connect visibility is confirmed; use `references/testflight-receipts-and-signing.md` for receipt and Apple-processing language.
2. **macOS**: Produce signed/notarized artifacts if credentials exist; otherwise, produce unsigned and mark as blocked. If archive fails with Apple certificate maximum/invalid signing identity errors, treat it as a CI signing-asset blocker before upload; inspect local keychain validity and refresh GitHub signing secrets only after macOS Keychain export approval.
3. **Windows**: Prepare build only after the Windows/Gemma 4 gateway PR is green and merged.
4. **ChatGPT/GPT**: Configure OpenAPI Action schema and gateway based on the merged Gemma 4 gateway PR.
5. **WorldBox/AgentCraft**: Use the canonical GitHub PR branch as the source of truth. Never use local zip files or unstable Swift helpers.

## ⚠️ Critical Safety Guards
- **WorldBox**: Do not attempt autonomous clicking. Use safe-tools (`worldboxctl-safe`) for observations and planning only.
- **Modding**: The goal is always the real NML/BepInEx bridge, not pixel-based workarounds.
