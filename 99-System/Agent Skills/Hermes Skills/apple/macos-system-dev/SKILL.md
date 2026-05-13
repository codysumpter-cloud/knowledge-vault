---
name: macos-system-dev
description: Troubleshooting macOS system glitches and compiling software from source on macOS (Intel/Apple Silicon).
---

# macOS System & Development Troubleshooting

This skill covers common macOS system maintenance tasks and patterns for compiling open-source software on modern macOS versions.

## System Maintenance

### Installing GUI Apps with CLI Access
Many macOS apps (like VS Code, Obsidian, etc.) provide a CLI binary bundled inside the `.app` package. To install from a DMG and enable CLI access:

1. **Mount DMG**: `hdiutil attach /path/to/image.dmg -nobrowse`
2. **Install App**: `cp -R "/Volumes/MountName/AppName.app" /Applications/`
3. **Unmount**: `hdiutil detach /dev/diskX` (where diskX is the mounted device).
4. **Link CLI**: Locate the binary (usually in `Contents/Resources/app/bin/` or `Contents/MacOS/`) and symlink it to a PATH directory:
   `ln -sf "/Applications/AppName.app/Contents/Resources/app/bin/cli-name" /usr/local/bin/cli-name`

**Example (Visual Studio Code):**
`ln -sf "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" /usr/local/bin/code`

### Refreshing Launchpad

If apps are missing from Launchpad or the layout is corrupted:
`defaults write com.apple.dock ResetLaunchPad -bool true; killall Dock`

### Resolving Corrupted Tooling & Path Conflicts
When a CLI tool (e.g., `npm`, `node`) fails with internal module errors (`MODULE_NOT_FOUND`) `despite appearing to be installed`:

1. **Trace the Binary**: Use `which <tool>` followed by `ls -la <path>` to determine if the binary is a symlink pointing to a non-standard or corrupted local directory (e.g., `~/.local/bin` or `~/.hermes/node`).
   * **Pitfall**: The binary may still return a version number (e.g., `npm -v`) but fail during execution if the underlying library paths are corrupted. Do not trust `version` commands as proof of a healthy installation.
2. **Install Clean Version**: Use Homebrew to install a fresh, system-managed version: `brew install <tool>`.
3. **Force Link**: Use `brew link --overwrite <tool>` to ensure the Homebrew version is active in `/usr/local/bin`.
4. **Repair Local Shims**: If a corrupted local symlink is still overriding the brew version in the PATH, manually overwrite it:
   `ln -sf /usr/local/bin/<tool> /path/to/corrupted/local/bin/<tool>`

## Network & Remote Access

### Infrastructure Discovery
When a user refers to a "VPS", "server", or "Cloud-Brain" without providing an IP address:
1. **Check `known_hosts`**: Examine `~/.ssh/known_hosts`. This often reveals the IP addresses of recently connected servers and their public keys, providing a viable starting point for connectivity tests.
2. **Verify Access**: Attempt a non-interactive probe with `ssh -o BatchMode=yes -o ConnectTimeout=5 <user>@<ip> "hostname; uptime"`.
3. **Identity Troubleshooting**: If permission is denied, if permission is denied, check `~/.ssh/` for available identity files (`id_rsa`, `id_ed25519`, `.pem` files) and try explicitly specifying the key with `-i`.

### GitHub Runner Recovery (Self-Hosted)
If a machine is restored from backup or OS re-installed, self-hosted GitHub runners are lost.
1. **Clean state**: Ensure old runner directories are removed to avoid configuration drift.
2. **Registration**: Requires a short-lived registration token from the repo's `Settings -> Actions -> Runners -> New self-hosted runner`. This can be retrieved programmatically via the GitHub API: `gh api -X POST /repos/{owner}/{repo}/actions/runners/registration-token`.
3. **Installation**: Download the correct OS-specific runner (e.g., `osx-x64` for Intel Macs). Avoid generic `macos` keywords in URLs as they may redirect or return 404s; use `osx` in the asset name.
4. **Service Mode**: Always install as a system service (e.g., via `svc.sh install`) to ensure the runner starts on boot and persists across sessions.
5. **Verification**: Confirm the runner is "Online" in the GitHub UI before triggering CI/CD pipelines.



### Command Line Tools (CLT) on Sequoia
On macOS Sequoia, Homebrew may report a missing or outdated CLT installation even if the full Xcode app is installed. Homebrew often requires the standalone CLT package to be installed separately.

**Standard Fix:**
`sudo xcode-select --install`
(Then follow the GUI prompt to complete installation.)

**Clean Slate Fix (if update fails or is skipped):**
`sudo rm -rf /Library/Developer/CommandLineTools`
`sudo xcode-select --install`

**Conflict Fix (Both Xcode.app and CLT installed):**
If `brew doctor` still complains about versions while you have both the full Xcode app and standalone tools, verify your active directory with `xcode-select -p`. If it points to `/Applications/Xcode.app/...`, Homebrew may ignore the standalone tools. Switch to the standalone tools:
`sudo xcode-select -s /Library/Developer/CommandLineTools`

**Pitfall: The Homebrew CLT Version Loop**
If you have manually installed the latest CLT `.dmg` and `brew doctor` *still* reports an outdated version, verify your current active developer directory with `xcode-select -p`. If it points to `/Applications/Xcode.app/...`, Homebrew may ignore the standalone tools you just installed. Run the **Conflict Fix** above to force Homebrew to recognize the standalone CLT path.

**Manual Fallback:**
If the system installer doesn't provide the specific version Homebrew expects, download the `.dmg` manually from [developer.apple.com/download/all/](https://developer.apple.com/download/all/).

## Low-RAM/Intel Performance Tuning
For Intel Macs with limited RAM (e.g., 8GB) on modern macOS:

### Intel macOS Wine/Steam Game Wrappers
When helping the user run Windows games on Intel macOS via Porting Kit, standalone Wine, or a no-CrossOver wrapper, distinguish three layers before changing anything: the wrapper/runtime, Steam authentication UI, and the actual game process. Intel Iris/Wine issues can masquerade as a game failure when only Steam's CEF login window is broken.

For the known black/invisible Steam login pattern, see `references/intel-mac-wine-steam-black-login.md`. Key indicators include impossible/offscreen Steam window coordinates, CEF transparent-background errors, and persistence after GPU/CEF flags. If the login compositor is the blocker, add a terminal/CLI Steam login helper inside the same prefix rather than repeatedly tuning the wrapper blindly. Always verify CrossOver is absent when the goal is a standalone/no-paid-CrossOver path, and avoid claiming "native" or "ready" until launch is verified end-to-end.

If standalone Wine/Porting Kit fails but the user's CrossOver bottle already launches the game, prefer reusing that proven bottle via CrossOver's CLI (`cxstart --bottle ... --no-gui`) before trying to recreate the bottle. See `references/intel-mac-crossover-eic-wrapper.md` for the EIC/AppID 3526710 pattern, verification receipts, input-latency registry tweaks, and the clean-start guard that prevents duplicate Unity instances on 8GB Intel Macs.


### Managing Photos mediaanalysisd CPU spikes

When an Intel/low-RAM Mac is slow and `ps`/Activity Monitor shows `mediaanalysisd`, `photoanalysisd`, or `photolibraryd` pegging CPU, identify the active Photos libraries before acting:

```bash
ps -axo pid,ppid,%cpu,%mem,etime,command | awk 'NR==1 || /mediaanalysisd|photoanalysisd|photolibraryd/'
lsof -p $(pgrep -x mediaanalysisd | head -1) 2>/dev/null | head -120
```

Typical libraries are `~/Pictures/Photos Library.photoslibrary` and `~/Library/Photos/Libraries/Syndication.photoslibrary`. Do **not** delete Photos databases or media. For an immediate low-risk relief while the user is away, stop or pause only the analysis processes:

```bash
killall mediaanalysisd photoanalysisd photolibraryd 2>/dev/null || true
# If launchd immediately respawns and CPU remains high, pause until reboot/resume:
for p in $(pgrep -x mediaanalysisd photoanalysisd photolibraryd 2>/dev/null); do kill -STOP "$p" 2>/dev/null || true; done
ps -axo pid,state,%cpu,%mem,etime,command | awk 'NR==1 || /mediaanalysisd|photoanalysisd|photolibraryd/'
```

Receipt: state `T` means paused; CPU should settle to `0.0`. This is temporary and reboot/login activity may resume Apple Photos analysis.

### 2. Visual Overhead Reduction
Reduce GPU load and VRAM usage:
`System Settings -> Accessibility -> Display -> Enable "Reduce transparency" and "Reduce motion"`

### 4. Power & Sleep Management
To maintain active SSH/Agent connections when the MacBook lid is closed:
- **Tool-based**: Use **Amphetamine** (App Store) to keep the system awake.
- **CLI-based**: Disable sleep via `pmset`:
  `sudo pmset -a sleep 0 disablesleep 1`
- **Pitfall: Thermal Hazards in Bags**. NEVER leave Amphetamine active while the MacBook is closed inside a backpack or confined space. Without airflow, the CPU will heat up, potentially damaging the battery or causing hardware failure. Ensure the device is in a ventilated area or disable sleep-prevention before transporting.


## Compiling Software from Source

### 1. Dependency Management
Use Homebrew for system libraries. Always verify installed versions before building.
`brew install <dependencies>`

### 2. Source Acquisition
Avoid `.tar.gz` or `.zip` release archives if the project uses git submodules, as these are often missing from the archive.
**Preferred method:**
`git clone --recursive <repository_url>`

### 3. CMake Build Configuration (Modern macOS)

When dealing with legacy projects on modern CMake (4.x+) and Xcode versions:

#### A. Handle CMake Version Compatibility
Modern CMake has removed compatibility for very old versions ( < 3.5). If you see "Compatibility with CMake < 3.5 has been removed", add:
`-DCMAKE_POLICY_VERSION_MINIMUM=3.5`

#### B. Resolve `std::filesystem` Errors
Errors stating `'copy_file' is unavailable: introduced in macOS 10.15` or similar filesystem errors occur when the deployment target is set too low.
**Fix:** Set the deployment target to 10.15 or higher (e.g., 11.0).
`-DCMAKE_OSX_DEPLOYMENT_TARGET=11.0`

#### C. Architecture Specification
For Intel Macs, explicitly set the architecture to avoid ambiguity:
`-DCMAKE_OSX_ARCHITECTURES=x86_64`

### Example Build Sequence
```bash
mkdir build && cd build
cmake \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_OSX_ARCHITECTURES=x86_64 \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=11.0 \
  -G Ninja \
  ..
ninja <target>
```

## Pitfalls & Troubleshooting

| Error/Symptom | Root Cause | Solution |
|-----------|------------|----------|
| `dyld: Symbol not found: _ACCESS_DESCRIPTION_free` | Node.js / dylib mismatch (common on Sequoia) | Downgrade to a stable LTS version (e.g., `brew install node@22`). If the binary is required by other tools, use `brew uninstall --ignore-dependencies node` first. Ensure symlinks are correct: `mkdir -p /usr/local/opt/node/bin && ln -sf /usr/local/bin/node /usr/local/opt/node/bin/node`. |
| Missing submodules in `src/` | Tarball download missing git submodules | Use `git clone --recursive` |
| `std::filesystem` unavailable | Deployment target < 10.15 | `-DCMAKE_OSX_DEPLOYMENT_TARGET=11.0` |
| CMake minimum version error | Modern CMake removed legacy support | `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` |
| Architecture mismatch | Defaulting to ARM on Intel or vice versa | `-DCMAKE_OSX_ARCHITECTURES=x86_64` |
