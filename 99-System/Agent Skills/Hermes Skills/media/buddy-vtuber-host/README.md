# Buddy VTuber Host Reference Implementation

This folder contains a small, shippable Buddy talking-host runtime that can be used as a YouTube/OBS overlay or as the base for an offline video renderer.

It is intentionally lightweight:

- Python stdlib HTTP server.
- Server-Sent Events for browser overlay updates.
- Piper-compatible TTS command path.
- WAV amplitude analysis for mouth/viseme timing.
- Optional YouTube live-chat polling via `pytchat`.
- Safe original voice profile: `bright_toy_robot`.

## Important voice guardrail

The voice profile is designed to feel cute, bright, retro, and toy-like. It must not be presented as a direct clone of any copyrighted character or performer.

## Folder map

```text
reference-implementation/
├── buddy_vtuber_host/
│   ├── adapters/
│   │   ├── response_engine.py
│   │   └── youtube_chat.py
│   ├── tts/
│   │   ├── buddy_voice_profile.py
│   │   ├── piper_engine.py
│   │   └── viseme_from_audio.py
│   ├── web/
│   │   ├── overlay.css
│   │   ├── overlay.html
│   │   └── overlay.js
│   ├── config.py
│   ├── event_bus.py
│   └── host_server.py
├── config.example.json
└── requirements.txt
```

## Local dev quick start

```bash
cd "99-System/Agent Skills/Hermes Skills/media/buddy-vtuber-host/reference-implementation"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m buddy_vtuber_host.host_server --config config.example.json --port 8765
```

Open the overlay:

```text
http://127.0.0.1:8765/overlay.html
```

Send a phrase:

```bash
curl -X POST http://127.0.0.1:8765/api/say \
  -H 'content-type: application/json' \
  -d '{"text":"Hi friend. I am Buddy, and I am ready to help!"}'
```

## OBS usage

1. Add a Browser Source.
2. URL: `http://127.0.0.1:8765/overlay.html`.
3. Set width/height to your canvas size, for example `1920x1080`.
4. Enable transparent background if OBS offers the option.
5. Route the generated audio output normally through the system or capture it as desktop audio.

## YouTube chat mode

Set `youtube.video_id` in `config.example.json`, or launch with:

```bash
python -m buddy_vtuber_host.host_server --config config.example.json --youtube VIDEO_ID
```

The adapter ignores duplicate messages and simple spam bursts. For production, add account allowlists, blocklists, and stronger moderation before letting chat fully steer the host.

## Piper setup

Point config to your Piper binary and voice model:

```json
{
  "tts": {
    "piper_binary": "../../../../../../omni-buddy/piper/piper",
    "voice_model": "../../../../../../omni-buddy/piper/en_GB-semaine-medium.onnx"
  }
}
```

For standalone use, install Piper separately and update those paths.

## Runtime event contract

The overlay receives SSE events:

```json
{"type":"state","state":"thinking"}
{"type":"speech","text":"Hi friend!","audio_url":"/audio/abc.wav","visemes":[...]}
{"type":"state","state":"idle"}
```

Each viseme item is:

```json
{"t":0.12,"mouth":"small_open","energy":0.42}
```

`mouth` is one of:

- `closed`
- `small_open`
- `open`
- `wide_open`
- `round_o`
- `smile`

## Next production step

Move the reference implementation into `omni-buddy` or `buddy-agent`, then replace the placeholder CSS Buddy with real transparent PNG sprite states from the Buddy art package.
