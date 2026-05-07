# Deployment Receipts

Last documented: 2026-05-07

This page stores receipt-based setup facts from the Sovereign Cloud setup session. Treat these as last-known receipts unless re-verified in a later session.

## GitHub / repository receipts

- Canonical GitHub account: codysumpter-cloud
- Core repo rename:
  - bmo-stack -> buddy-brain
  - omni-bmo -> omni-buddy
- Current cloud-side clones recorded during setup:
  - /opt/buddy-brain
  - /opt/omni-buddy

## VPS receipts from setup

- VPS IP: 187.77.223.224
- OS: Ubuntu 24.04.x LTS
- SSH: root SSH key installed
- Gateway path: /opt/bmo-gateway
- App stack alias: /opt/automindlab-stack -> /opt/bmo-gateway
- Service: automind-app-factory.service active during setup

## Health endpoint receipt from setup

Direct IP health endpoint:

```text
http://187.77.223.224/api/health
```

Expected payload:

```json
{"status":"ok","service":"automindlab-enterprise-app-factory"}
```

## Root app receipt from setup

Direct IP root endpoint:

```text
http://187.77.223.224/
```

Expected title/script evidence captured during setup:

```html
<title>AutoMindLab Enterprise App Factory</title>
<script type="module" crossorigin src="/assets/index-yDJR9X_Y.js">
```

## Nginx receipt from setup

Nginx was prepared to recognize these hostnames during setup:

- 187.77.223.224
- automindlab.tech
- www.automindlab.tech
- prismtek.dev
- www.prismtek.dev

Important: this Nginx config does not authorize DNS changes. DNS remains protected. See [DNS Guardrails](./dns-guardrails.md).

## App bundle fix receipt

Issue observed:

```text
The client bundle has not been built yet.
```

Root cause:

```text
dist/dist/client was being resolved instead of dist/client
```

Files patched during setup:

- /opt/bmo-gateway/services/enterprise-app-factory/dist/server/server/app.js
- /opt/bmo-gateway/services/enterprise-app-factory/src/server/app.ts

Behavior changed:

```text
packageRoot() uses process.cwd()
```

## Release conductor note

No public DNS cutover should be inferred from these receipts. Working domains remain where they are unless explicitly changed by the user.
