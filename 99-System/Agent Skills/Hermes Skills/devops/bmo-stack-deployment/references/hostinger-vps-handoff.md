# Hostinger VPS handoff reference

Use this when continuing a Sovereign Cloud / Hostinger deployment after a terminal restart or Telegram-agent handoff.

## Confirmed VPS facts from session
- Hostinger VPS: `187.77.223.224`
- Hostname: `srv1425557.hstgr.cloud`
- OS: Ubuntu 24.04 LTS / 24.04.4 observed
- SSH user: `root`
- Canonical paths observed:
  - `/opt/bmo-gateway`
  - `/opt/automindlab-stack -> /opt/bmo-gateway`
  - `/opt/buddy-brain`
  - `/opt/omni-buddy`

## Recovery sequence
1. Check liveness:
   ```bash
   ping -c 3 187.77.223.224
   nc -zv 187.77.223.224 22
   ```
2. If password SSH fails but hPanel is open, reset root password in hPanel (`Root password -> Change`) and retry:
   ```bash
   sshpass -p '<password>' ssh -o StrictHostKeyChecking=no root@187.77.223.224 'hostnamectl; id'
   ```
3. Install the local SSH key after first password login:
   ```bash
   PUB=$(tr -d '\n' < ~/.ssh/id_ed25519.pub)
   sshpass -p '<password>' ssh root@187.77.223.224 "mkdir -p /root/.ssh; chmod 700 /root/.ssh; grep -qxF '$PUB' /root/.ssh/authorized_keys 2>/dev/null || printf '%s\n' '$PUB' >> /root/.ssh/authorized_keys; chmod 600 /root/.ssh/authorized_keys"
   ssh -o BatchMode=yes root@187.77.223.224 'echo SSH_KEY_OK'
   ```
4. Inspect stack:
   ```bash
   ssh root@187.77.223.224 'docker --version; docker compose version; docker ps; systemctl list-units --type=service --state=running | grep -Ei "automind|bmo|factory|openclaw" || true'
   ```

## Enterprise App Factory app-root fix
Symptom: `/api/health` works, but `/` says the client bundle has not been built, while `dist/client/index.html` exists.

Cause: `packageRoot()` resolves from built server directory and searches `dist/dist/client`.

Fix both source and built output if doing an emergency server patch:
```bash
ssh root@187.77.223.224 "python3 -c \"from pathlib import Path
files=['/opt/bmo-gateway/services/enterprise-app-factory/dist/server/server/app.js','/opt/bmo-gateway/services/enterprise-app-factory/src/server/app.ts']
for f in files:
 p=Path(f); s=p.read_text(); old=s
 s=s.replace('return path.resolve(import.meta.dirname, \\\"../..\\\");','return process.cwd();')
 p.write_text(s); print(f, s!=old)\""
ssh root@187.77.223.224 'systemctl restart automind-app-factory.service; systemctl is-active automind-app-factory.service'
```

Verify:
```bash
python3 - <<'PY'
import urllib.request
for u in ['http://187.77.223.224/api/health','http://187.77.223.224/']:
    r=urllib.request.urlopen(u, timeout=10)
    print(u, r.status, r.read(300).decode('utf-8','replace'))
PY
```

## DNS cutover receipts
VPS-local Host header checks are necessary but not sufficient:
```bash
ssh root@187.77.223.224 "python3 - <<'PY'
import http.client
for host in ['187.77.223.224','automindlab.tech','prismtek.dev']:
 c=http.client.HTTPConnection('127.0.0.1',80,timeout=5)
 c.request('GET','/api/health',headers={'Host':host})
 r=c.getresponse(); print(host, r.status, r.read(200).decode())
PY"
```

Public receipts must also be checked after Cloudflare changes:
```bash
python3 - <<'PY'
import urllib.request
for u in ['https://prismtek.dev/api/health','https://automindlab.tech/api/health']:
    try:
        r=urllib.request.urlopen(u, timeout=12)
        print(u, r.status, r.read(300).decode('utf-8','replace'))
    except Exception as e:
        print(u, type(e).__name__, e)
PY
```
