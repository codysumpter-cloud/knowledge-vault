# Source Map

## Primary modding sources

### Official WorldBox Wiki: Modding
URL: https://the-official-worldbox-wiki.fandom.com/wiki/Modding

Key facts:

- Desktop mods are supported for macOS, Windows, and Linux.
- Mobile modding is not supported by the wiki guidance.
- Mod loaders include NML / NeoModLoader and BepInEx.
- NCMS is considered outdated and users are recommended to move to NML.
- NML supports loading both NML and NCMS mods.

Agent takeaway:

> Prefer NML first. Keep BepInEx as an alternative. Treat NCMS as legacy/research-only.

### Official WorldBox Wiki: Modding Code Examples
URL: https://the-official-worldbox-wiki.fandom.com/wiki/Modding_Code_Examples

Key facts:

- WorldBox mods can create/clone custom UI windows.
- Mods can load sprites and attach sprites to custom windows.
- Examples reference Unity objects/components and game classes such as `Actor` and `MapBox`.
- Example code moves actors with `cancelEverything()` and `moveTo(MapBox.instance.GetTile(...))`.

Agent takeaway:

> A bridge mod is plausible because mod code can interact with Unity UI and in-game actors/tiles, but exact current class names must be mapped against the user's installed WorldBox version.

### NCMS docs
URL: https://denq04.github.io/ncms/

Key facts:

- NCMS docs state NCMS will no longer be updated.
- They point users to NML as the better alternative.
- NCMS included method patching and supported uncompiled C# code.

Agent takeaway:

> Do not start new work on NCMS unless explicitly needed for compatibility research.

### GameBanana WorldBox hub / tutorial
URLs:
- https://gamebanana.com/games/11196
- https://gamebanana.com/tuts/16266

Key facts:

- GameBanana is a relevant community source for WorldBox mods/tutorials.
- Some pages require JavaScript and may not be fully readable from a text scraper.

Agent takeaway:

> Use GameBanana as discovery/community evidence, not as the only source of truth.

### lkolbly/worldbox GitHub repo
URL: https://github.com/lkolbly/worldbox

Key facts:

- This is a separate entity-centric C++/JavaScript game engine, not the official WorldBox god-sim API.
- Its README describes a goal of networked entity status/control, but says the project does not really have that yet.

Agent takeaway:

> Do not rely on this repo as an official WorldBox API. It is useful only as conceptual inspiration for entity-centric simulation/API design.

## Achievement source

### Official WorldBox Wiki: Achievements
URL: https://the-official-worldbox-wiki.fandom.com/wiki/Achievements

Key facts:

- PC has 96 achievements; mobile has 86.
- The wiki marks some methods as cheats.
- Many achievements are triggered by inspecting menus, units, religions, languages, cultures, traits, and subspecies.
- Some achievements explicitly require no trait editor / unscarred units.

Agent takeaway:

> Use fresh unedited units for strict achievements. Separate fun custom units from achievement-valid units.
