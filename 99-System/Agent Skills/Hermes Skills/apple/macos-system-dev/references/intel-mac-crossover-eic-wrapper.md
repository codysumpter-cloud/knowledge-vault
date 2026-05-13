# Intel macOS CrossOver bottle wrapper for Everything is Crab

Session learning: on the user's Intel Iris MacBook Pro, a standalone Wine/Porting Kit style prefix could install Steam/EIC but Steam CEF rendered black/offscreen and the game did not launch reliably. The working path was to reuse the existing CrossOver `Steam` bottle directly via CrossOver's CLI, without launching the CrossOver GUI.

## Key distinction

Do not call a Windows `.exe` wrapper "native" in the strict sense. The practical target is a macOS `.app`/`.command` launcher that uses the known-working Wine/CrossOver bottle while minimizing user friction.

## Working launch pattern

Use CrossOver's `cxstart` directly:

```bash
CXROOT="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver"
CXSTART="$CXROOT/bin/cxstart"
BOTTLE="Steam"
STEAM_EXE='C:\Program Files (x86)\Steam\steam.exe'

export CX_BOTTLE="$BOTTLE"
export WINEMSYNC=1
export WINEDEBUG=-all
export DXVK_LOG_LEVEL=none

exec "$CXSTART" \
  --bottle "$BOTTLE" \
  --no-update \
  --no-gui \
  --no-wait \
  --workdir 'C:\Program Files (x86)\Steam' \
  "$STEAM_EXE" \
  -silent \
  -nochatui \
  -nofriendsui \
  -vgui \
  -cef-disable-gpu \
  -cef-disable-gpu-compositing \
  -applaunch 3526710 \
  -screen-fullscreen 1 \
  -screen-width 1280 \
  -screen-height 800 \
  -window-mode exclusive \
  -force-d3d11 \
  -force-d3d11-flip-model \
  -nolog
```

For EIC specifically, Steam AppID is `3526710`.

## Verification receipts

Verify the game actually launched through Steam, not just that Steam opened:

```bash
ps aux | egrep -i 'Everything is Crab|steam.exe|UnityCrash|wineserver|winedevice' | egrep -v egrep

tail -40 "$HOME/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam/logs/gameprocess_log.txt"

tail -80 "$HOME/Library/Application Support/CrossOver/Bottles/Steam/drive_c/users/crossover/AppData/LocalLow/Odd Dreams Digital/Everything is Crab/Player.log"
```

Good signs:
- `Everything is Crab.exe -timestamps ...` appears in `ps`
- Steam `gameprocess_log.txt` shows `AppID 3526710 adding PID ...`
- Unity `Player.log` reaches `Main Menu` and ideally `Gameplay`

## Input latency tweaks for Intel Mac

Inside the CrossOver bottle, disable Windows mouse acceleration first:

```bash
CX="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxstart"
B="Steam"
"$CX" --bottle "$B" --no-update --no-gui reg add 'HKCU\\Control Panel\\Mouse' /v MouseSpeed /t REG_SZ /d 0 /f
"$CX" --bottle "$B" --no-update --no-gui reg add 'HKCU\\Control Panel\\Mouse' /v MouseThreshold1 /t REG_SZ /d 0 /f
"$CX" --bottle "$B" --no-update --no-gui reg add 'HKCU\\Control Panel\\Mouse' /v MouseThreshold2 /t REG_SZ /d 0 /f
```

Then choose DirectInput warp behavior by profile, not as a universal fix:

```bash
# Better for Unity relative mouse/aim capture; use for actual aim-latency testing.
"$CX" --bottle "$B" --no-update --no-gui reg add 'HKCU\\Software\\Wine\\DirectInput' /v MouseWarpOverride /t REG_SZ /d force /f

# Fallback if cursor capture/visibility is the main problem rather than aim feel.
"$CX" --bottle "$B" --no-update --no-gui reg add 'HKCU\\Software\\Wine\\DirectInput' /v MouseWarpOverride /t REG_SZ /d disable /f
```

Session finding: `MouseWarpOverride=disable` can make the visible cursor feel more normal, but Unity/Wine relative aiming may need `MouseWarpOverride=force` to reduce delayed/heavy aim. Ask the user to test subjective aim after changing this; tools can verify registry and process flags, not whether mouse feel is solved.

If `reg add` reports success but the expected values are not visible in `user.reg`, inspect the file directly. CrossOver may have active registry state; after stopping wineserver, direct patching of `user.reg` may be needed. Verify with:

```bash
egrep -n 'MouseSpeed|MouseThreshold|DirectInput|MouseWarpOverride' "$HOME/Library/Application Support/CrossOver/Bottles/Steam/user.reg"
```

## Low-latency launcher profile

For this user's Intel Iris / 8GB MacBook Pro, prioritize a small, recoverable set of launcher profiles instead of repeatedly mutating one opaque wrapper:

- Aim fallback profile: `-screen-fullscreen 1 -screen-width 1152 -screen-height 720 -window-mode exclusive -force-d3d11 -force-d3d11-flip-model -nolog`
- In-world performance/default profile after aim is confirmed: same exclusive/fullscreen/D3D11 flags but reduce to `1024x640` to cut pixel load on Intel Iris.
- Smoother FPS profile: preserve the input-good path but reduce to `960x600` (`EIC_PROFILE=smooth`/`butter`). This was launched and verified with `-force-d3d11 -force-d3d11-flip-model`, `MouseWarpOverride=force`, and `VideoMemorySize=1536`. Keep as the next candidate default if the user confirms it feels smooth.
- Emergency max-FPS profile: same input-good path at `800x500` (`EIC_PROFILE=potato`/`maxfps`) for quick A/B testing if 960x600 is still too slow.
- If in-world FPS is still abnormally low while macOS CPU/thermal/memory look fine, check Unity `Player.log` for `Graphics Memory: 8192 MB`, `VRAM: 8192 MB`, and `GpuFence::Create(): Failed to create ID3D11Fence`. On this Intel Iris Mac, macOS reports only 1536 MB dynamic VRAM; cap Wine with `HKCU\Software\Wine\Direct3D VideoMemorySize=1536`. User testing confirmed removing `-force-d3d11-flip-model` makes input delay worse, so keep flip-model in the default/input-good profile and investigate FPS via VRAM cap, resolution, Steam helper trimming, or alternate renderer profiles instead.
- XeSS / Windows Intel drivers: Wine/CrossOver cannot use Windows kernel display drivers on macOS; the path remains Unity D3D11 → Wine/CrossOver translation → macOS Metal/Intel driver. EIC install was checked for `*xess*`, `*fsr*`, `*dlss*`, and `*nvngx*` files and none were present, so do not promise XeSS/FSR/DLSS unless the game is modded or a renderer hook is built.
- Cursor fallback: same core launcher but with `MouseWarpOverride=disable` if capture/visibility is worse than aim delay.
- Renderer experiment: keep D3DMetal/DXVK/quality experiments as separate `.command` launchers; do not overwrite the known-good aim launcher until the user confirms improvement.

Use `caffeinate` while the game is running to avoid macOS sleep/display throttling during tests, and after launch attempt to trim Steam helper pressure (`steamwebhelper`) if it is consuming RAM/CPU. On this machine, memory pressure can feel like input latency.

## Steam overlay/toast stuck under Wine

If the lower-right Steam toast (`Access Steam features...`) sticks around, verify `gameoverlayui64.exe` is running. Killing it clears the toast for the active game. If Steam respawns it repeatedly, disable the overlay binaries in the CrossOver bottle by renaming them with a reversible backup suffix:

```bash
STEAMDIR="$HOME/Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam"
mv "$STEAMDIR/gameoverlayui64.exe" "$STEAMDIR/gameoverlayui64.exe.prismtek-disabled"
mv "$STEAMDIR/gameoverlayui.exe" "$STEAMDIR/gameoverlayui.exe.prismtek-disabled"
pkill -f 'gameoverlayui64.exe.*3526710' 2>/dev/null || true
pkill -f 'gameoverlayui.exe.*3526710' 2>/dev/null || true
```

Keep a restore command/script that moves the `.prismtek-disabled` files back to their original names. This is safer than deleting them and avoids claiming Steam overlay is permanently disabled if Steam later updates/restores the files.

## Prevent duplicate Unity instances and self-killing commands

On an 8GB Intel Mac, duplicate EIC/Unity players can stack after repeated launch tests and destroy perceived input latency. Add clean-start logic before launch:

```bash
pkill -f 'Everything is Crab.exe' 2>/dev/null || true
pkill -f 'UnityCrashHandler64.exe.*Everything is Crab' 2>/dev/null || true
sleep 1
```

When trimming Steam helpers or overlays from within a heredoc/agent shell, avoid broad `pkill -f 'steamwebhelper.exe --type=renderer'` patterns because the search string can match the shell command itself and terminate the active tool call. Prefer bracketed grep patterns (`[s]teamwebhelper`) for inspection and a PID-based helper for killing actual Wine child processes:

```bash
kill_matching() {
  /bin/ps -Ao pid=,command= |
    /usr/bin/awk -v pat="$1" -v self="$$" 'tolower($0) ~ tolower(pat) && $1 != self {print $1}' |
    while read -r pid; do [ -n "$pid" ] && kill "$pid" 2>/dev/null || true; done
}
kill_matching 'steamwebhelper.exe --type=renderer'
kill_matching 'steamwebhelper.exe --type=utility'
kill_matching 'gameoverlayui64.exe.*3526710'
```

## Color fidelity caution

Slight color shifts can come from the active D3D11/D3DMetal/DXVK path, macOS display color management, True Tone/Night Shift/HDR-like display behavior, or Steam/CEF overlays. Do not switch renderers in the working launcher blindly. Create separate profiles for experiments (e.g. low-latency vs quality/borderless) so the known-good launch path remains recoverable.

## Pitfalls

- Standalone Wine may fail only at Steam CEF/login while CrossOver's bottle works. Reuse the working bottle when the user says CrossOver game launch works but UX is bad.
- CrossOver GUI being paid/annoying is distinct from using the installed CrossOver runtime/CLI. `cxstart --no-gui` can launch through the bottle without opening the CrossOver UI.
- Do not keep trying random CEF/GPU flags against a black standalone prefix after the working CrossOver bottle has proved itself.
- Avoid claiming input/color are fixed without a user subjective test; verify only launch/process/log receipts from tools.
