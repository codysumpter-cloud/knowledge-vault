# macOS restored-machine GitHub recovery notes

Use this when a restored Mac has Apple Git but no Homebrew, no `gh`, no credentials, and needs a GitHub workspace rebuilt quickly.

## Observed baseline

- Apple Git may already exist after restore (`git version 2.39.x`).
- Homebrew may be missing.
- `gh` may be missing.
- `~/.ssh/` may not exist.
- Global `user.name`, `user.email`, and credential helper may be unset.

## Install GitHub CLI without Homebrew

Download the latest macOS zip from `cli/cli` releases, choosing `macOS_amd64.zip` on Intel or `macOS_arm64.zip` on Apple Silicon, then copy `bin/gh` into `~/.local/bin`.

Example deterministic installer:

```bash
mkdir -p "$HOME/.local/bin" "$HOME/.local/opt"
python3 - <<'PY'
import json, urllib.request, platform, os, re, sys, tempfile, zipfile, shutil
arch = platform.machine().lower()
asset_arch = 'amd64' if arch in ('x86_64', 'amd64') else 'arm64'
with urllib.request.urlopen('https://api.github.com/repos/cli/cli/releases/latest', timeout=30) as r:
    rel = json.load(r)
pat = re.compile(rf'gh_.*_macOS_{asset_arch}\.zip$')
asset = next((a for a in rel['assets'] if pat.search(a['name'])), None)
if not asset:
    raise SystemExit(f'no gh macOS zip found for {arch}')
tmp = tempfile.mkdtemp(prefix='gh-install-')
zip_path = os.path.join(tmp, asset['name'])
urllib.request.urlretrieve(asset['browser_download_url'], zip_path)
with zipfile.ZipFile(zip_path) as z:
    z.extractall(tmp)
root = next(os.path.join(tmp,n) for n in os.listdir(tmp) if n.startswith('gh_') and os.path.isdir(os.path.join(tmp,n)))
dst = os.path.expanduser('~/.local/bin/gh')
shutil.copy2(os.path.join(root, 'bin', 'gh'), dst)
os.chmod(dst, 0o755)
print(dst)
PY
~/.local/bin/gh --version
```

Persist PATH for new shells:

```bash
for f in "$HOME/.zshrc" "$HOME/.bash_profile"; do
  touch "$f"
  grep -q 'HOME/.local/bin' "$f" || printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$f"
done
```

## Rebuild credentials and identity

```bash
git config --global user.name "<github-username>"
git config --global user.email "<github-username>@users.noreply.github.com"
git config --global credential.helper store

mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keygen -t ed25519 -C "<github-username>@users.noreply.github.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

On macOS, copy and open settings:

```bash
pbcopy < ~/.ssh/id_ed25519.pub
open https://github.com/settings/keys
```

Verify after the user adds the key:

```bash
ssh -o StrictHostKeyChecking=accept-new -T git@github.com
```

Expected success includes: `Hi <username>! You've successfully authenticated`.

## gh auth caveat in agent PTYs

`gh auth login --web` can hang or fail to advance when driven through some pseudo-terminal/process wrappers. If interactive device login is flaky, use one of these instead:

```bash
# Browser/device flow in the user's real shell
~/.local/bin/gh auth login --hostname github.com --git-protocol https --web --scopes repo,workflow,read:org
~/.local/bin/gh auth setup-git

# Or token-based login
printf '%s' "$GITHUB_TOKEN" | ~/.local/bin/gh auth login --with-token
~/.local/bin/gh auth setup-git
```

## Clone public repos while auth is pending

Public repos can still be restored via the GitHub public API and HTTPS clone. Private repos, fork sources requiring auth, and push access will wait until SSH/gh auth is complete.
