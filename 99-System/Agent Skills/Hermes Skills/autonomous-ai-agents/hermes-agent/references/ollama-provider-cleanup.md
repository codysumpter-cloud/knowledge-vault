# Ollama Provider Cleanup: Ollama Launch vs Windows Ollama

Use when Hermes starts on an unexpected local custom endpoint such as `provider: custom`, `gemma4:26b`, or `http://127.0.0.1:11435/v1`, while the intended setup is exactly two Ollama providers.

## Intended provider identities

- **Ollama Launch**: local launch bridge, provider key `ollama-launch`, base URL `http://127.0.0.1:11434/v1`, model `gemma4:31b-cloud`.
- **Windows Ollama**: remote Windows host, provider key like `windows-ollama`, display name `windows ollama`, base URL `http://192.168.7.170:11434/v1`, models commonly `gemma4:26b` and `gemma4:latest`.

Do not rewrite Ollama Launch to the Windows endpoint. Do not treat a loopback tunnel such as `127.0.0.1:11435` as authoritative unless the user explicitly says so.

## Repair sequence

1. Inspect active config and provider aliases:
   ```bash
   hermes config path
   sed -n '1,40p' ~/.hermes/config.yaml
   grep -n "custom_providers\|11435\|gemma4:26b\|ollama" ~/.hermes/config.yaml
   ```
2. Verify live endpoints before editing:
   ```bash
   curl -sS --max-time 5 http://127.0.0.1:11434/v1/models
   curl -sS --max-time 5 http://192.168.7.170:11434/api/tags
   curl -sS --max-time 5 http://192.168.7.170:11434/v1/models
   ```
3. Back up `~/.hermes/config.yaml`.
4. Set the active model to Ollama Launch, not generic `custom`:
   ```yaml
   model:
     api_key: ollama
     base_url: ''
     default: gemma4:31b-cloud
     provider: ollama-launch
   ```
5. Keep providers keyed, not duplicated through legacy `custom_providers`:
   ```yaml
   providers:
     ollama-launch:
       api_key: ollama
       base_url: http://127.0.0.1:11434/v1
       default_model: gemma4:31b-cloud
       models: [gemma4:31b-cloud]
       name: Ollama Launch
       type: custom
     windows-ollama:
       api_key: ollama
       base_url: http://192.168.7.170:11434/v1
       default_model: gemma4:26b
       models: [gemma4:26b, gemma4:latest]
       name: windows ollama
       type: custom
   custom_providers: []
   ```
6. Remove stale bad endpoint entries from `~/.hermes/context_length_cache.yaml` if they mention the wrong loopback, e.g. `127.0.0.1:11435`.
7. Verify:
   ```bash
   grep -n "127.0.0.1:11435\|provider: custom\|default: gemma4:26b" ~/.hermes/config.yaml || true
   hermes config check
   hermes chat -Q --provider ollama-launch -m gemma4:31b-cloud -q 'Reply exactly: OK_OLLAMA_LAUNCH'
   hermes gateway restart
   ```

## Pitfalls

- `custom_providers` is a compatibility layer and can duplicate provider-picker entries or override expectations; prefer keyed `providers` entries and set `custom_providers: []` when the providers are already represented.
- The bad pattern is not that Windows has `gemma4:26b`; the bad pattern is making the main model `provider: custom` + `base_url: 127.0.0.1:11435/v1` when the user expects Ollama Launch as default.
- Provide receipts only: active provider/model, bad endpoint absent, live probe token returned, backup path. Do not over-explain provider theory.
