# VPS Dashboard / Web UI Internet Access

Use when exposing `hermes dashboard` from a VPS while keeping Telegram/gateway separate.

## Safe topology

- Run dashboard on loopback only: `127.0.0.1:8080`
- Expose it through nginx on `:80`/`:443`
- Put nginx Basic Auth in front of it
- Keep the gateway as a separate service/process
- Use `--tui` when the browser workspace/chat tab should be functional

## Systemd units

Gateway:

```ini
[Unit]
Description=Hermes Gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=hermes
Group=hermes
WorkingDirectory=/home/hermes
EnvironmentFile=/home/hermes/.hermes/.env
ExecStart=/home/hermes/.hermes/hermes-agent/venv/bin/hermes gateway run --replace
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Dashboard:

```ini
[Unit]
Description=Hermes Dashboard Web UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=hermes
Group=hermes
WorkingDirectory=/home/hermes
EnvironmentFile=/home/hermes/.hermes/.env
ExecStart=/home/hermes/.hermes/hermes-agent/venv/bin/hermes dashboard --host 127.0.0.1 --port 8080 --tui
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Nginx reverse proxy with Basic Auth

```bash
apt-get install -y nginx apache2-utils
PASS=$(openssl rand -base64 18 | tr -d '=+/' | cut -c1-18)
printf '%s\n' "$PASS" > /root/hermes-dashboard-password.txt
htpasswd -bc /etc/nginx/.htpasswd-hermes cody "$PASS"
chmod 640 /etc/nginx/.htpasswd-hermes
chown root:www-data /etc/nginx/.htpasswd-hermes
```

```nginx
server {
    listen 80 default_server;
    server_name 187.77.223.224 hermes.example.com _;

    auth_basic "Hermes Dashboard";
    auth_basic_user_file /etc/nginx/.htpasswd-hermes;

    location / {
        proxy_pass http://127.0.0.1:8080;
        # Dashboard Host-header protection rejects arbitrary public Host values when bound to loopback.
        proxy_set_header Host 127.0.0.1:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 3600;
        proxy_send_timeout 3600;
    }
}
```

Apply:

```bash
nginx -t && systemctl reload nginx
systemctl enable --now hermes-gateway hermes-dashboard
systemctl restart hermes-gateway hermes-dashboard
```

## Verification receipts

Run from outside the VPS:

```bash
# should require auth
curl -I http://VPS_IP/

# should load dashboard
curl -u cody:$(ssh root@VPS_IP 'cat /root/hermes-dashboard-password.txt') \
  -s http://VPS_IP/ | grep -o '<title>[^<]*'
```

Run on VPS:

```bash
systemctl is-active hermes-gateway hermes-dashboard nginx
ss -tlnp | egrep ':(80|8080)'
su - hermes -c 'cd /home/hermes && .hermes/hermes-agent/venv/bin/hermes status --all'
su - hermes -c 'cd /home/hermes && set -a && source .hermes/.env && set +a && .hermes/hermes-agent/venv/bin/hermes chat -Q -q "Reply exactly OK_DEFAULT"'
```

Expected:

- nginx listens on `0.0.0.0:80`
- dashboard listens only on `127.0.0.1:8080`
- unauthenticated public request returns `401`
- authenticated `/`, `/chat`, `/api/status`, and `/api/model/info` return `200`
- `OK_DEFAULT` proves the workspace uses a working model/provider

## Provider cleanup pitfall

If a provider returns runtime auth errors such as OpenRouter `401 User not found`, do not leave it as the default just because config exists. Disable/rotate the bad key, set a known-good primary provider, restart both gateway and dashboard, then run a live `hermes chat -Q` probe.

## Gateway lifecycle notification pitfall

If Telegram receives repeated `Gateway shutting down/restarting` messages while the VPS agent otherwise works, inspect `journalctl -u hermes-gateway.service` before chasing provider/DNS issues. Planned `--replace` takeovers and systemd restarts can send user-facing lifecycle pings. For user-facing Telegram bots, set `platforms.telegram.gateway_restart_notification: false`; see `references/vps-gateway-troubleshooting.md`.

## DNS release pitfall

Do not touch production domain routing unless explicitly authorized. If the main domain already resolves through Hostinger/Cloudflare, prepare nginx for `hermes.<domain>` and request/add only that A record. Direct IP access can be fully functional before DNS is complete.
