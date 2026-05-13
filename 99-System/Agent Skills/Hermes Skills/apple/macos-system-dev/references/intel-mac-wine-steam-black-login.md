# Intel macOS Wine/Steam black login window

Context: running Windows Steam games such as Everything is Crab on Intel macOS without CrossOver, using standalone Wine/Porting Kit-style prefixes.

Observed failure pattern:
- Steam launches, but the login/CEF window is black or invisible.
- Window metadata can show impossible/offscreen coordinates such as `805240832,805240832`.
- Logs may include: `Browser requested transparent background, but it is not supported`.
- GPU/CEF flags may reduce symptoms but not fix the Steam login compositor on Intel Iris/Wine.
- This can happen in standalone Wine, not just CrossOver. Verify no CrossOver process is involved before attributing cause.

Useful diagnostic sequence:
1. Confirm the active runtime: check for CrossOver processes and identify the exact Wine binary/prefix being used.
2. Inspect Steam logs and window state before changing wrappers.
3. Check whether the failure is Steam authentication UI only versus the actual game binary/runtime.
4. Try Steam CEF/GPU mitigation flags, but treat them as workaround attempts, not proof of fix.
5. If the graphical login stays black/offscreen, use a terminal/CLI Steam login path in the same prefix so authentication can complete without the broken CEF login window.
6. After authentication succeeds, relaunch the app wrapper and verify by process/log receipts, not by claiming native readiness.

Wrapper pattern used successfully:
- Build a standalone Wine prefix/app wrapper for the game.
- Copy Steam game files/appmanifest into the prefix when possible.
- Add a separate `.command` helper for local Steam CLI login that reads the password silently and does not echo it to logs.
- Keep CrossOver completely out of the process when the goal is a no-CrossOver path.

User-facing receipt standard:
- State whether CrossOver is required or absent.
- State exact app/helper paths.
- State the remaining blocker separately from what is working.
- Avoid saying the game is "native" or "ready" until launched and verified end-to-end on the Mac.
