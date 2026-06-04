# PokeMMO Mod Install Runbook

This runbook tells Buddy/Hermes how to help Prismtek install PokeMMO mods without becoming a bot, scraper, or unlicensed mod mirror.

## Installation flow

1. Pick a candidate from `POKEMMO_MODPACK_INDEX.md` or the official Client Customization forum.
2. Open the original source thread.
3. Verify category, author, screenshots, update date, install instructions, and safety notes.
4. Download locally only after user approval.
5. Store the file in the local cache.
6. Import it through PokeMMO's Mod Management UI.
7. Enable one mod at a time.
8. Restart the client if required.
9. Record a receipt.

## Suggested local cache

```bash
mkdir -p ~/Games/PokeMMO/modpacks/prismtek-buddy/downloads
mkdir -p ~/Games/PokeMMO/modpacks/prismtek-buddy/enabled
mkdir -p ~/Games/PokeMMO/modpacks/prismtek-buddy/disabled
mkdir -p ~/Games/PokeMMO/modpacks/prismtek-buddy/receipts
```

## Receipt format

```json
{
  "mod_id": "example_mod_id",
  "name": "Example Mod",
  "source_url": "https://forums.pokemmo.com/...",
  "author": "Unknown until verified",
  "retrieved_at": "YYYY-MM-DD",
  "local_file": "~/Games/PokeMMO/modpacks/prismtek-buddy/downloads/example.mod",
  "enabled": true,
  "safety_review": {
    "visual_or_audio_only": true,
    "requires_executable": false,
    "automation_claims": false,
    "memory_or_packet_access": false
  }
}
```

## In-client install steps

Use the PokeMMO client's normal mod/theme management path:

1. Open PokeMMO.
2. Open Mod Management / Client Management from the client UI.
3. Import the downloaded mod file.
4. Enable it.
5. Restart if prompted.
6. Verify the game still launches and menus are readable.

Do not use third-party installers that claim to patch the client.

## Update workflow

1. Check the original thread for updates.
2. Compare local receipt date to thread update date.
3. Download the new file only from the author's current link.
4. Move the old file to `disabled/`.
5. Import the new file.
6. Record a new receipt.

## Uninstall workflow

1. Disable the mod in PokeMMO Mod Management.
2. Restart the client.
3. Move the local cached file from `enabled/` to `disabled/`.
4. Record the reason in a receipt.

## Safety gates

Stop immediately if the candidate requires:

- executable helper
- account login
- private token/cookie
- memory access
- packet access
- automated input
- route/catch/battle/farm automation
- GTL automation
- ROM download
- patched client binary

## Buddy response pattern

When Prismtek asks for mod help, answer like this:

```text
Verdict: This is safe to try / skip this / needs verification.

Why:
- <short safety or quality reason>

Do this:
1. Download from the original thread.
2. Save it to the local cache.
3. Import through Mod Management.
4. Enable and restart.

Watch out:
- <only if important>
```

## Future automation boundary

A future Buddy local tool may organize downloads and receipts, but it must not automate gameplay or modify the PokeMMO client binary. It may open source pages or local folders for the user, but all downloads/imports should remain explicit user-approved actions unless a mod has a clear redistributable license and a trusted direct URL.
