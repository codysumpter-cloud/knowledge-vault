# Everything is Crab (EIC) Modding Reference

## Hardware Environment
- **Machine:** Intel MacBook Pro (8GB RAM)
- **OS:** macOS Sequoia
- **Execution:** CrossOver / Porting Kit (Windows 10 Bottle)
- **Critical Constraint:** 8GB RAM is a major bottleneck. Avoid running high-memory apps (Chrome, Agent HUDs) during game execution.

## Modding Roadmap
1. **Baseline:** Establish a stable boot via CrossOver.
2. **Mapping:** Use `UnityExplorer` to map game objects to classes in `Assembly-CSharp.dll`.
3. **Patching:** Use `BepInEx` + `Harmony` for runtime injection.
4. **Optimization:** Focus on lowering resolution (720p) and managing RAM to avoid swap stutter.

## Dev Relations (The "Professional Ally" Strategy)
- **Key Contact:** Chazz (Community Manager).
- **Relationship Status:** Respected community member.
- **Boundaries:**
  - No unofficial native ports.
  - No public source code leaks.
  - Modding is "on the table" but not officially supported yet.
- **Communication Style:** Respectful, supportive, business-aware. Position requests as "offering resources" (e.g., Mac test-runner) rather than "asking for permissions."

## Project Infrastructure
- **Repo:** `codysumpter-cloud/prismteksmods`
- **Knowledge Base:** `~/eic-wiki` (Karpathy LLM Wiki pattern)

## macOS Intel Wine/Porting Notes

### Decision rule: prefer proven bottle reuse over recreating CrossOver
If CrossOver launches the game but has input/color problems, first try to reuse the known-good CrossOver bottle from CLI before building a separate Wine prefix. A Windows `.exe` is not truly native on macOS without source-level porting; the practical target is a macOS launcher wrapper around a working Wine/CrossOver runtime.

### CrossOver bottle without opening the CrossOver UI
A working pattern for EIC on the user's Intel Mac is to launch the CrossOver Steam bottle directly with `cxstart`:

```bash
CXSTART="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxstart"
"$CXSTART" \
  --bottle Steam \
  --no-update \
  --no-gui \
  --no-wait \
  --workdir 'C:\Program Files (x86)\Steam' \
  'C:\Program Files (x86)\Steam\steam.exe' \
  -silent \
  -nochatui \
  -nofriendsui \
  -applaunch 3526710 \
  -screen-fullscreen 0 \
  -screen-width 1280 \
  -screen-height 720 \
  -force-d3d11 \
  -nolog
```

Useful wrapper paths created in the successful session:
- `/Users/codysumpter/Games/EverythingIsCrabNative/launch-eic-crossover-bottle.sh`
- `/Users/codysumpter/Games/EverythingIsCrabNative/Everything-is-Crab-CrossOver-Bottle.command`
- `/Users/codysumpter/Applications/Everything is Crab Native.app`

Verification receipts from the working launch:
- `ps` showed `C:\Program Files (x86)\Steam\steamapps\common\Everything is Crab\Everything is Crab.exe -timestamps` under CrossOver's Wine runtime.
- Steam `gameprocess_log.txt` showed AppID `3526710` adding the EIC process and `UnityCrashHandler64.exe`.
- Unity `Player.log` reached `Main Menu`, `NewRunButton`, difficulty `StartButton`, and `Gameplay.unity`.

### Standalone Wine wrapper pattern: experimental only
A standalone Wine/Porting-style wrapper can be built outside CrossOver, but for this EIC session it was not the winning path:
- Separate prefix: `~/Games/EverythingIsCrabNative/prefix`.
- Gcenx Wine 11.8 app bundle layout: `Wine Devel.app/Contents/Resources/wine/bin/wine`.
- Game files copied from CrossOver Steam bottle.
- Quarantine removed with `xattr -dr com.apple.quarantine <paths>`.

Observed failure mode: Steam/CEF and Wine virtual desktops rendered black/offscreen containers. The Steam login window created at bogus coordinates such as `805240832,805240832`; disabling CEF GPU/Vulkan did not make the standalone Steam UI reliable. Do not keep iterating on plain Wine if the CrossOver bottle already works.

### Steam requirement
Everything is Crab currently behaves like a Steam-bound Unity game. Directly launching `Everything is Crab.exe` can crash or exit because Steam is not attached. Prefer launching through Steam:

`steam.exe -applaunch 3526710 -screen-fullscreen 0 -screen-width 1280 -screen-height 720 -force-d3d11 -nolog`

Useful files from a known Steam install:
- `steamapps/appmanifest_3526710.acf`
- `steamapps/common/Everything is Crab/`
- Steam auth/client state (`config`, `userdata`, `package`, `public`, `appcache`) may need to be copied into the standalone prefix, but future sessions must verify login state via Steam logs.

### Intel Iris 655 renderer pitfall
On the user's Intel Iris Plus Graphics 655, DXVK 2.7.1 under MoltenVK failed with:

`Device does not support required feature 'geometryShader'`
`DXVK: No adapters found`
`Failed to initialize DXVK`

For this Mac, do not assume DXVK is the best path. Default to WineD3D/OpenGL fallback with local DXVK DLLs disabled/renamed and use the 1280x720 virtual desktop. Keep DXVK files as an optional experiment only after verifying geometryShader support.

### Verification receipts
Do not claim the game is fully working until verified beyond Steam login/auth. Check:
- `pgrep -fl CrossOver` is empty while the standalone launcher is running.
- `ps ax` shows `Wine Devel.app`/standalone Wine paths, not CrossOver paths.
- Steam login log: `drive_c/Program Files (x86)/Steam/logs/steamui_login.txt` must progress past `WaitingForCredentials`; repeated `Received logon failure response` means the remaining blocker is Steam authentication, not CrossOver dependency.
