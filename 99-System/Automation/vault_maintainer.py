#!/usr/bin/env python3
"""Vault Steward maintenance script.

Creates/updates Obsidian project-memory folders from GitHub repository metadata.
Safe default: private repos are written under 00-Private and remain ignored by Git.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

OWNER = os.environ.get("VAULT_GITHUB_OWNER", "codysumpter-cloud")
TOKEN = os.environ.get("VAULT_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
TRACK_PRIVATE = os.environ.get("VAULT_TRACK_PRIVATE", "false").lower() == "true"
TODAY = date.today().isoformat()


def vault_root() -> Path:
    here = Path(__file__).resolve()
    # 99-System/Automation/vault_maintainer.py -> vault root
    return here.parents[2]


def request_json(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "KnowledgeVault-Vault-Steward",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_repos() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        if TOKEN:
            url = f"https://api.github.com/user/repos?affiliation=owner&per_page=100&page={page}&sort=full_name"
        else:
            url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&page={page}&sort=full_name"
        batch = request_json(url)
        if not batch:
            break
        repos.extend([r for r in batch if r.get("owner", {}).get("login") == OWNER])
        if len(batch) < 100:
            break
        page += 1
    return sorted(repos, key=lambda r: r["name"].lower())


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def ensure_project(repo: dict[str, Any], root: Path) -> dict[str, str]:
    visibility = "private" if repo.get("private") else "public"
    name = repo["name"]
    full_name = repo["full_name"]
    default_branch = repo.get("default_branch") or "main"
    html_url = repo.get("html_url") or f"https://github.com/{full_name}"
    clone_url = repo.get("clone_url") or f"https://github.com/{full_name}.git"

    if visibility == "private" and not TRACK_PRIVATE:
        folder = root / "00-Private" / "GitHub Projects" / OWNER / name
    else:
        folder = root / "30 - Projects" / "GitHub" / OWNER / name
    folder.mkdir(parents=True, exist_ok=True)

    project = folder / "Project.md"
    if not project.exists():
        write(project, f"""
---
type: github-repo
repo: {full_name}
repo_name: {name}
owner: {OWNER}
visibility: {visibility}
default_branch: {default_branch}
github_url: {html_url}
clone_url: {clone_url}
status: Needs triage
priority: Triage
source_of_truth: vault-project-memory
code_source: github
agent_owner: Vault Steward
last_synced: {TODAY}
tags:
  - github/repo
  - project
  - visibility/{visibility}
---

# {name}

> GitHub is the source of truth for source code; this note is the source of truth for project context, decisions, status, and agent handoffs.

## Links

- GitHub: {html_url}
- Clone: `{clone_url}`
- Default branch: `{default_branch}`
- Visibility: `{visibility}`

## Current status

- Status: Needs triage
- Owner: Prismtek
- Agent owner: Vault Steward
- Last sync: {TODAY}

## Project intent

_To be filled in by Prismtek or an agent after reading the repo README/issues._

## Next actions

- [ ] Triage README and current repo purpose.
- [ ] Capture install/build/test commands.
- [ ] Capture active issues and project risks.
- [ ] Decide whether this repo is active, incubating, archived, or reference-only.

## Human notes

_Add durable project context here._
""")
    for filename, body in {
        "Agent Context.md": "# Agent Context\n\nKeep repo-specific instructions, build commands, risks, and handoff notes here.\n",
        "Decisions.md": "# Decisions\n\n| Date | Decision | Why | Owner |\n|---|---|---|---|\n",
        "Tasks.md": "# Tasks\n\n- [ ] Triage repo purpose, README, and current branch health.\n",
    }.items():
        p = folder / filename
        if not p.exists():
            write(p, body)

    return {
        "name": name,
        "full_name": full_name,
        "owner": OWNER,
        "visibility": visibility,
        "default_branch": default_branch,
        "github_url": html_url,
        "clone_url": clone_url,
        "last_synced": TODAY,
        "vault_path": str(folder.relative_to(root)),
    }


def update_indexes(root: Path, registry: list[dict[str, str]]) -> None:
    public = [r for r in registry if r["visibility"] == "public"]
    private = [r for r in registry if r["visibility"] == "private"]
    public_table = "\n".join(
        f'| [[{OWNER}/{r["name"]}/Project|{r["name"]}]] | `{r["default_branch"]}` | {r["visibility"]} | [GitHub]({r["github_url"]}) |'
        for r in public
    )
    write(root / "30 - Projects" / "GitHub" / "GitHub Projects Index.md", f"""
---
type: github-project-index
owner: {OWNER}
repo_count_public: {len(public)}
repo_count_private_local: {len(private)}
last_synced: {TODAY}
tags:
  - github/index
  - project/index
---

# GitHub Projects Index

Private repo folders are kept under `00-Private/GitHub Projects/{OWNER}/` unless `VAULT_TRACK_PRIVATE=true`.

| Repo | Default branch | Visibility | GitHub |
|---|---|---:|---|
{public_table}
""")
    write(root / "99-System" / "Repositories" / f"{OWNER}.public.repo-registry.json", json.dumps(public, indent=2))
    write(root / "00-Private" / "GitHub Projects" / f"{OWNER}.private.repo-registry.json", json.dumps(private, indent=2))
    write(root / "99-System" / "Agents" / "Vault Steward" / "Logs" / f"{TODAY}.md", f"""
---
type: vault-steward-log
date: {TODAY}
agent: Vault Steward
tags:
  - vault/log
---

# Vault Steward Log — {TODAY}

- Public repos indexed: {len(public)}
- Private repos indexed locally: {len(private)}
- Total repos seen: {len(registry)}
""")


def main() -> int:
    root = vault_root()
    if not TOKEN:
        print("No VAULT_GITHUB_TOKEN/GITHUB_TOKEN set; public GitHub repos only.", file=sys.stderr)
    repos = fetch_repos()
    registry = [ensure_project(repo, root) for repo in repos]
    update_indexes(root, registry)
    print(f"Vault Steward indexed {len(registry)} repos for {OWNER}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
