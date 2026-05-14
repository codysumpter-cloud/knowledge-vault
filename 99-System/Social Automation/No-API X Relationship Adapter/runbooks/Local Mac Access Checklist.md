# Local Mac Access Checklist — Hermes Social Automation

## Purpose

Hermes can reduce dependency on paid social APIs only if local browser, screen, and keyboard control are reliable. This checklist records the ordinary macOS permissions needed for user-approved local automation.

## Permissions to Review

System Settings → Privacy & Security → Accessibility

Review the active controlling process, commonly one or more of:

- Terminal
- iTerm
- Python
- osascript
- Script Editor
- Safari
- cliclick
- Hermes app/process if visible

System Settings → Privacy & Security → Screen Recording

Review:

- Terminal / iTerm
- Python
- Hermes process
- any screenshot helper used by Hermes

System Settings → Privacy & Security → Automation

Allow the controlling process to control:

- Safari
- System Events

## Verification Checks

Hermes should report:

```txt
System Events UI elements enabled: true/false
Safari JavaScript route: pass/fail
Safari javascript URL route: pass/fail
screenshot capture: pass/fail
cliclick installed: yes/no
focused element typing test: pass/fail
```

## Stop Conditions

If Hermes sees a login challenge, account warning, unexpected page, permission prompt, or route friction, it should stop and report the exact issue instead of repeatedly retrying.

## Success State

Hermes can:

- open X notifications in signed-in Safari;
- take screenshot receipts;
- inspect visible text;
- click approved UI targets;
- type exact approved text;
- stop on unexpected pages;
- write receipts.
