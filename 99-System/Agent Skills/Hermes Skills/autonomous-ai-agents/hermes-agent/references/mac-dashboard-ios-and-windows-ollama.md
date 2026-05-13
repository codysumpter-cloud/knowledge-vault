# Mac Dashboard iPhone Access + Windows Ollama Guardrail

Use when configuring Hermes on the MacBook for Telegram/dashboard access while a Windows Ollama endpoint is the intended model backend.

## Known-good Windows Ollama source of truth

The user keeps the working Windows Ollama config in Obsidian. In the Knowledge Vault dashboard note, the current values are:

- Windows Ollama base URL: `http://192.168.7.170:11434`
- Ollama Launch provider: `ollama-launch`
- Ollama Launch Hermes model: `gemma4:31b-cloud` (UI may phrase this as `gemma4:31b(cloud)`)
- API key placeholder: `ollama`

Before changing `~/.hermes/config.yaml`, distinguish the backend the user asked for:
- **Windows Ollama** = remote Windows host at `192.168.7.170:11434`; verify `/api/tags` before routing to it.
- **Ollama Launch** = local launch bridge/provider alias; fix via `ollama launch hermes` and the interactive model picker, not by rewriting to the Windows endpoint.

Do **not** replace either with a local tunnel/loopback URL just because `127.0.0.1:11435` is open; that may only be a temporary Mac-side route.

## Verification ladder before switching model URL

1. Read current config:
   ```bash
   hermes config path
   sed -n '1,12p' ~/.hermes/config.yaml
   ```
2. Verify Windows Ollama reachability from the Mac:
   ```bash
   python3 - <<'PY'
import socket
for host, port in [('192.168.7.170', 11434)]:
    s = socket.socket(); s.settimeout(3)
    try:
        s.connect((host, port)); print(f'{host}:{port} OPEN')
    except Exception as e:
        print(f'{host}:{port} CLOSED {type(e).__name__}: {e}')
    finally:
        s.close()
PY
   ```
3. Only if reachable, probe Ollama HTTP endpoints:
   ```bash
   curl -sS --max-time 5 http://192.168.7.170:11434/api/tags
   curl -sS --max-time 5 http://192.168.7.170:11434/v1/models
   ```
4. Only after live success, update Hermes config and restart gateway.

## iPhone access to MacBook Hermes dashboard

For same-Wi-Fi iPhone access, bind the dashboard to all interfaces on the Mac and provide the Mac LAN IP URL.

```bash
# Check if dashboard port is free
lsof -nP -iTCP:9119 -sTCP:LISTEN || true

# Start dashboard for LAN access
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --tui --skip-build --no-open

# Find Mac Wi-Fi IP
ipconfig getifaddr en0 || ipconfig getifaddr en1

# Verify locally
curl -sS http://127.0.0.1:9119/ | head
```

Receipt should include:

- `lsof` showing `*:9119 (LISTEN)`
- `curl` returning Hermes Dashboard HTML
- iPhone URL: `http://<mac-lan-ip>:9119/`

## Password-protected external access from a Mac

Use the VPS pattern conceptually: dashboard on loopback, reverse proxy with Basic Auth in front. Mac differences:

- Intel/Homebrew config path is usually `/usr/local/etc/nginx/`; Apple Silicon/Homebrew is usually `/opt/homebrew/etc/nginx/`. Check `brew --prefix nginx` before writing config.
- Port `80`/`443` and `brew services` usually require interactive admin/sudo on macOS. If the agent lacks sudo, do not claim nginx setup is complete; prepare config/commands for the user to run at home.
- `htpasswd` syntax is `htpasswd -bc FILE USER PASS` or `htpasswd -nb USER PASS`; do not pipe `user:pass` into `htpasswd -b`. Quote passwords containing `$` so the shell does not expand them.
- For same-LAN only, `:9119` is acceptable. For internet exposure, prefer loopback dashboard + nginx/Caddy/Cloudflare Tunnel/Tailscale auth rather than raw `--host 0.0.0.0 --insecure`.

## Pitfalls

- `hermes dashboard --host 0.0.0.0 --insecure` exposes config/API-key management on the LAN. Use only on trusted local Wi-Fi; prefer loopback + reverse proxy/auth for internet exposure.
- If Windows Ollama says `No route to host`, do not rewrite Hermes to that endpoint yet. Report that Windows host/network/firewall must be fixed or keep the currently reachable Mac route.
- `HEAD /` may return `405 Method Not Allowed`; use `GET` (`curl http://127.0.0.1:9119/`) for dashboard verification.
- Never overwrite a whole Obsidian daily note just to save credentials; append or patch a small credential/access section.
