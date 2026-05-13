#!/usr/bin/env python3
"""
Install Obsidian interactive-stack plugins from the Obsidian community registry
or explicit GitHub releases.

Safety defaults:
- downloads release assets only
- no npm install
- no builds
- no watchers
- no indexing
- no daemon
- one-shot
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

VAULT_ROOT = Path.cwd()
MANIFEST = VAULT_ROOT / "99-System" / "Obsidian" / "obsidian-interactive-stack.manifest.json"
PLUGIN_ROOT = VAULT_ROOT / ".obsidian" / "plugins"
LOG_DIR = VAULT_ROOT / "99-System" / "Logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG = LOG_DIR / "obsidian-plugin-install.log"

REGISTRY_URL = "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json"
GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"
ASSETS = ["manifest.json", "main.js", "styles.css"]

def log(msg: str) -> None:
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={
        "User-Agent": "knowledgevault-obsidian-plugin-installer",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))

def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "knowledgevault-obsidian-plugin-installer"})
    with urllib.request.urlopen(req, timeout=60) as res:
        dest.write_bytes(res.read())

def repo_from_registry(plugin_id: str, registry: list[dict[str, Any]]) -> str | None:
    for item in registry:
        if item.get("id") == plugin_id:
            repo = item.get("repo")
            if repo:
                return repo.replace("https://github.com/", "").strip("/")
    return None

def install_from_repo(plugin_id: str, repo: str) -> bool:
    target = PLUGIN_ROOT / plugin_id
    target.mkdir(parents=True, exist_ok=True)

    release = get_json(GITHUB_API.format(repo=repo))
    assets = {a["name"]: a["browser_download_url"] for a in release.get("assets", [])}

    downloaded = 0
    for name in ASSETS:
        if name in assets:
            download(assets[name], target / name)
            downloaded += 1

    # Some releases may publish a zip only. Avoid unzip complexity here; log and let Hermes install manually.
    if downloaded < 2:
        log(f"SKIP {plugin_id}: latest release for {repo} did not expose manifest/main assets directly")
        return False

    log(f"OK {plugin_id}: installed from {repo}")
    return True

def main() -> int:
    if not MANIFEST.exists():
        print(f"Missing manifest: {MANIFEST}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    targets = manifest.get("install_targets", [])

    try:
        registry = get_json(REGISTRY_URL)
    except Exception as exc:
        log(f"ERROR registry fetch failed: {exc}")
        return 1

    PLUGIN_ROOT.mkdir(parents=True, exist_ok=True)
    installed = []
    skipped = []
    failed = []

    for item in targets:
        plugin_id = item["id"]
        target = PLUGIN_ROOT / plugin_id
        if (target / "manifest.json").exists() and (target / "main.js").exists():
            log(f"PRESENT {plugin_id}")
            installed.append(plugin_id)
            continue

        repo = item.get("repo") or repo_from_registry(plugin_id, registry)
        if not repo:
            log(f"SKIP {plugin_id}: not found in registry and no explicit repo provided")
            skipped.append(plugin_id)
            continue

        try:
            ok = install_from_repo(plugin_id, repo)
            if ok:
                installed.append(plugin_id)
            else:
                skipped.append(plugin_id)
        except urllib.error.HTTPError as exc:
            log(f"FAIL {plugin_id}: HTTP {exc.code} from {repo}")
            failed.append(plugin_id)
        except Exception as exc:
            log(f"FAIL {plugin_id}: {exc}")
            failed.append(plugin_id)

        time.sleep(0.75)

    log(f"DONE installed_or_present={len(installed)} skipped={len(skipped)} failed={len(failed)}")
    if skipped:
        log("SKIPPED " + ", ".join(skipped))
    if failed:
        log("FAILED " + ", ".join(failed))
    return 0 if not failed else 2

if __name__ == "__main__":
    raise SystemExit(main())
