# Obsidian Git release safety notes

Use this reference when committing or pushing changes from a live, Git-tracked Obsidian vault after rebases, stash restoration, plugin-stack installs, or cleanup passes.

## One-file / scoped cleanup rule

A path-limited `git add path` does **not** guarantee the staged set contains only that path. A previous `stash pop`, conflict resolution, or interrupted run may have left unrelated tracked files already staged.

Before committing a scoped cleanup or one-file fix:

```bash
git fetch origin main
git status --short --branch
AHEAD=$(git rev-list --count origin/main..HEAD)
BEHIND=$(git rev-list --count HEAD..origin/main)
[ "$BEHIND" = 0 ] || exit 41

# After staging the intended path(s), verify the full staged set exactly.
git diff --cached --name-status
git diff --cached --name-only
```

For a one-file change, enforce:

```bash
STAGED=$(git diff --cached --name-only)
[ "$STAGED" = ".obsidian/obsidian-git.json" ] || exit 43
```

For a small allowed set, compare with an explicit allowlist and stop if anything else is staged. Do not rely on `git status` alone.

## Stash pop after push

`git stash pop` can both restore tracked modifications and leave conflicts. If it conflicts, Git may keep the stash entry. After resolving the conflict:

```bash
git diff --name-only --diff-filter=U
# must be empty before claiming resolved

git stash list | sed -n '1,20p'
# report the stash; do not drop it unless explicitly asked
```

If the user requested only a final cleanup, do not silently include stash-restored tracked files in the cleanup commit. Either unstage/restore them from the last commit or stop and report.

## GitHub push protection on bundled Obsidian plugins

Bundled plugin `main.js` files may contain upstream OAuth client IDs/secrets or other strings that GitHub push protection treats as secrets. Known example: Smart Composer's packaged `main.js` triggered Google OAuth Client ID and Client Secret detection.

Safe response:

1. Do not bypass push protection.
2. Rewrite the local commit before it reaches remote.
3. Remove the flagged plugin runtime payload from tracked files.
4. Remove it from active plugin profiles.
5. Mark it skipped in the stack manifest with a reason.
6. Re-run path/content safety scans, then push.

## Report format

Use receipt-style output:

- sync gate: ahead/behind
- staged files: exact list
- commit hash/message
- push range
- final `git status --short --branch`
- stash status if stash was involved
