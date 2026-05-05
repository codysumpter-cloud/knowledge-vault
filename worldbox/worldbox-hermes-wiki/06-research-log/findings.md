# Research Findings

## 2026-05-05

- Official WorldBox modding path is community mod loaders, not an official gameplay CLI/API.
- NML/NeoModLoader is the preferred new-loader direction; NCMS is legacy.
- BepInEx remains a viable alternative and is listed alongside NML in community documentation.
- Mod code examples show Unity UI access and actor movement through game classes, so a bridge mod is plausible.
- lkolbly/worldbox is not official WorldBox god-sim tooling; it is a separate game engine project.
- GameBanana is a community mod distribution/discovery hub; use it as secondary evidence.
- The safe implementation path remains:

```text
no-mod helper -> read-only bridge -> proposal loop -> allowlisted writes -> dangerous writes with approval
```
