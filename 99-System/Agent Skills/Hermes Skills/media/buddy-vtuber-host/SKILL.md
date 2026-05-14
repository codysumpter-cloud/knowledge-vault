# Buddy VTuber Host

## Purpose

Build and operate a lightweight Buddy talking-host runtime for YouTube, OBS, and local rendered videos.

This skill captures the refined implementation direction from the AI-Vtuber pattern and AvatarFX-style audio-driven animation research: Buddy should be a reusable host pipeline, not another static sprite sheet.

## Scope

The reference implementation in this folder provides:

- YouTube live-chat input adapter.
- Omni/local response adapter.
- Piper TTS generation path.
- Safe original `bright_toy_robot` voice post-processing profile.
- WAV-to-viseme mouth timeline generation.
- Browser/OBS transparent overlay runtime.
- Local render-friendly event contract.

## Non-goals and guardrails

- Do not clone or impersonate a copyrighted character voice or actor performance.
- Do not claim official Adventure Time, Cartoon Network, or Warner Bros. affiliation.
- Keep the voice profile original: cute, bright, small-device, toy-robot friendly.
- Keep secrets out of config files. Read tokens only from environment variables.
- Treat YouTube chat as untrusted input. Rate-limit, dedupe, and ignore unsafe commands.

## Runtime architecture

```text
YouTube chat / script / mic input
        -> response engine
        -> Piper TTS WAV
        -> optional Buddy voice shaping
        -> WAV amplitude analysis
        -> viseme timeline
        -> browser overlay animation
        -> OBS / rendered video output
```

## Recommended owners

- KnowledgeVault owns this skill, runbook, and reference implementation.
- `omni-buddy` may adopt the Piper/viseme/overlay code.
- `buddy-agent` should eventually own the production runtime integration.

## Quick start

```bash
cd "99-System/Agent Skills/Hermes Skills/media/buddy-vtuber-host/reference-implementation"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m buddy_vtuber_host.host_server --config config.example.json --port 8765
```

Open:

```text
http://127.0.0.1:8765/overlay.html
```

Send a local test phrase:

```bash
curl -X POST http://127.0.0.1:8765/api/say \
  -H 'content-type: application/json' \
  -d '{"text":"Hi friend. I am Buddy, and I am ready to help!"}'
```

## Integration notes

- The server uses Server-Sent Events so the overlay can run in a normal browser source without WebSocket dependencies.
- If Piper is missing, `/api/say` emits text/state events but no audio. This keeps development mode usable.
- If `pytchat` is missing, YouTube chat mode is disabled while local/manual mode still works.
- The overlay is transparent by default for OBS browser sources.
