---
name: macos-gui-automation
description: "Use when controlling macOS GUI apps, automating clicks/screenshots, or remotely keeping a Mac awake with Amphetamine/caffeinate."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [macOS, GUI, Automation, Vision, cliclick]
    related_skills: [apple-notes, apple-reminders]
---

# macOS GUI Automation

This skill enables the agent to interact with non-CLI macOS applications by creating a feedback loop of screen capture, visual analysis, and simulated input.

## When to use

- Interacting with apps that lack an API or CLI.
- "Playing" a game or performing repetitive GUI tasks.
- Automating workflows in proprietary software.
- Clicking specific buttons or navigating menus visually.

## Prerequisites

- **cliclick**: Required for mouse/keyboard simulation.
  - Install: `brew install cliclick`
- **Accessibility Permissions**: **CRITICAL.** The terminal emulator (e.g., Terminal, iTerm2, or the Hermes environment) MUST be granted accessibility permissions.
  - Path: `System Settings` $\rightarrow$ `Privacy & Security` $\rightarrow$ `Accessibility` $\rightarrow$ Enable the relevant terminal app.
  - Without this, `cliclick` commands will execute but the system will block the actual mouse movement/clicks.

## Core Workflow (The Vision Loop)

To interact with a GUI app, follow this iterative loop:

1. **Focus the App**: Ensure the target app is frontmost.
   ```bash
   osascript -e 'tell application "AppName" to activate'
   # OR if the app name is different from the process name:
   osascript -e 'tell application "System Events" to set frontmost of process "ProcessName" to true'
   ```
2. **Capture the Screen**: Take a screenshot for analysis.
   ```bash
   screencapture -x /path/to/screenshot.png
   ```
3. **Analyze for Coordinates**: Use `vision_analyze` to find the exact [X, Y] pixel coordinates of the target UI element.
   - **Prompt Tip**: "Provide the exact [X, Y] pixel coordinates for [Element Name] relative to the full image size. If the element is not explicitly labeled, look for symbolic icons (e.g., gears for settings, '...' for more/menu, trophies for achievements)."
4. **Execute Action**: Use `cliclick` or `osascript` for input.
   - **Click**: `cliclick c:X,Y`
   - **Move**: `cliclick m:X,Y`
   - **Type**: `cliclick t:text`
   - **Complex Input (AppleScript)**: For more reliable typing or Tab/Enter keys in specific apps:
     ```bash
     osascript -e 'tell application "System Events" to keystroke "text"'
     osascript -e 'tell application "System Events" to key code 48' # Tab
     osascript -e 'tell application "System Events" to key code 36' # Enter
     ```
   - **Wait/Sleep**: Always insert small `sleep` intervals (0.2s - 0.5s) between clicks to allow the UI to react.
5. **Verify State Change**: **CRITICAL.** Immediately take another screenshot and analyze it to confirm the action had the intended effect (e.g., a menu opened, a unit was selected). Do not assume a `cliclick` success means the game state updated.

## Browser CDP Fallback

When Chrome/Chromium is running with `--remote-debugging-port=9222`, prefer Chrome DevTools Protocol for web portals before coordinate-based GUI clicks:

```bash
curl -s http://127.0.0.1:9222/json/list
```

Use the target page's `webSocketDebuggerUrl` and evaluate DOM JavaScript through CDP to read visible text, click buttons, or fill inputs. This is useful when vision/OCR quota is exhausted, when Chrome AppleScript JavaScript is disabled (`View -> Developer -> Allow JavaScript from Apple Events`), or when dynamic portals like Hostinger hPanel/Cloudflare are easier to verify through DOM state.

Keep the same verification rule: after a CDP click/input, re-read DOM text or verify the real external receipt endpoint. Do not assume a CDP command changed server state.

## Remote keep-awake emergency

When the user is away and asks if the Mac is awake / closed / Amphetamine was not enabled, do not wait for GUI automation. Start a CLI power assertion first, then verify it:

```bash
# Start as a tracked background process (not nohup/disown in a foreground command)
/usr/bin/caffeinate -dimsu

# Verify
pgrep -afil 'caffeinate|Amphetamine' || true
pmset -g assertions | sed -n '1,180p'
open -gj -a /Applications/Amphetamine.app 2>/dev/null || true
```

Receipt to look for in `pmset`: `PreventSystemSleep: 1`, `PreventUserIdleSystemSleep: 1`, `PreventUserIdleDisplaySleep: 1`, with owner `caffeinate command-line tool`. Use Amphetamine GUI only as an optional secondary launch; `caffeinate` is the immediate reliable fix.

## Pitfalls & Troubleshooting

- **Background process wrapper refusal**: If the terminal tool rejects `nohup`/`&`/`disown` in a foreground command, rerun the keep-awake command with the terminal tool's `background=true` option, then verify in a separate command.
- **Accessibility Block**: If `cliclick` returns success but nothing happens on screen, the Accessibility permission is missing. Instruct the user to enable it in System Settings.
- **Coordinate Drift**: If the app window moves or resizes, the coordinates from the previous screenshot become invalid. Re-capture and re-analyze.
- **App Sandbox/Quarantine**: Apps downloaded via browser may be blocked by macOS Gatekeeper. Use `xattr -rd com.apple.quarantine /path/to/app` to remove the quarantine flag before launching.
- **Retina Scaling**: Be aware that `screencapture` pixel dimensions may differ from coordinate systems in some legacy apps, though `cliclick` generally aligns with the screen resolution.
- **Focus Loss**: If the agent performs a command that opens a new window or alert, the target app may lose focus. Re-run the `osascript` activate command.
## Quick cliclick Reference

| Action | Command | Notes |
|---|---|---|
| Right Click | `cliclick rc:X,Y` | Moves mouse to X,Y and performs a right click |
| Move | `cliclick m:X,Y` | Moves mouse to X,Y without clicking |
| Type | `cliclick t:text` | Types the specified string |
| Key Press | `cliclick kp:key` | Presses a specific key (e.g., `kp:enter`) |
