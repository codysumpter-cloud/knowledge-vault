# Restored Mac GitHub auth and deleting a fork

This reference captures a restored-machine recovery flow where git worked, Homebrew was absent, GitHub CLI was absent, SSH auth was set up, and a broken fork needed deletion.

## Install gh without Homebrew

If `brew` is missing but Python/curl are present, download the latest `cli/cli` macOS zip from GitHub Releases and place `gh` in `~/.local/bin`.

```bash
mkdir -p "$HOME/.local/bin"
python3 - <<'PY'
import json, urllib.request, platform, os, re, sys, tempfile, zipfile, shutil
arch = platform.machine().lower()
asset_arch = 'amd64' if arch in ('x86_64', 'amd64') else 'arm64'
with urllib.request.urlopen('https://api.github.com/repos/cli/cli/releases/latest', timeout=30) as r:
    rel = json.load(r)
pat = re.compile(rf'gh_.*_macOS_{asset_arch}\.zip$')
asset = next((a for a in rel['assets'] if pat.search(a['name'])), None)
if not asset:
    raise SystemExit(f'No gh macOS {asset_arch} asset found')
tmp = tempfile.mkdtemp(prefix='gh-install-')
zip_path = os.path.join(tmp, asset['name'])
urllib.request.urlretrieve(asset['browser_download_url'], zip_path)
with zipfile.ZipFile(zip_path) as z:
    z.extractall(tmp)
root = next(os.path.join(tmp, n) for n in os.listdir(tmp) if n.startswith('gh_') and os.path.isdir(os.path.join(tmp, n)))
dst = os.path.expanduser('~/.local/bin/gh')
shutil.copy2(os.path.join(root, 'bin', 'gh'), dst)
os.chmod(dst, 0o755)
print(dst)
PY
```

Persist PATH:

```bash
for f in "$HOME/.zshrc" "$HOME/.bash_profile"; do
  touch "$f"
  grep -q 'HOME/.local/bin' "$f" || printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$f"
done
```

## SSH first: enough for git clone/fetch/push

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "USERNAME@users.noreply.github.com" -f ~/.ssh/id_ed25519 -N ""
pbcopy < ~/.ssh/id_ed25519.pub
open https://github.com/settings/keys
```

After the user adds the key:

```bash
ssh -T git@github.com
# Expected: Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.

git config --global url."git@github.com:".insteadOf "https://github.com/"
```

## gh OAuth/device flow pitfalls

SSH auth does not authorize GitHub API actions such as deleting a repo. For deletion, `gh` must be logged in with `delete_repo` scope or a PAT must have `delete_repo`.

Device-code auth can behave differently depending on terminal/PTY handling. If non-PTY attempts hang or print no code, run with a PTY and interact with prompts:

```bash
~/.local/bin/gh auth login --hostname github.com --git-protocol ssh --web --scopes repo,workflow,read:org,delete_repo
```

If `gh` asks to upload an SSH key that the user already added manually, choose `Skip`. Then copy the displayed one-time code and open:

```bash
open https://github.com/login/device
```

Wait for the user to approve before continuing.

## Delete the fork/repo

```bash
gh auth status
gh repo delete USERNAME/claw-code --yes
gh repo view USERNAME/claw-code || echo 'deleted or inaccessible'
```

Curl fallback with a token:

```bash
curl -sS -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/USERNAME/claw-code \
  -D /tmp/github-delete-headers.txt
# Success is HTTP 204.
grep -i '^HTTP/' /tmp/github-delete-headers.txt
```

## Disabled fork symptom

A repo can appear in the public API but fail to clone:

```text
ERROR: Repository 'USERNAME/claw-code' is disabled.
Please ask the owner to check their account.
fatal: Could not read from remote repository.
```

This is not an SSH-key or local git problem if `ssh -T git@github.com` succeeds. Treat it as a GitHub-side disabled repo/fork: delete it if the user asks, re-enable it in GitHub settings/support, or skip it.
