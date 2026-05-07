# Sovereign Cloud Current State

Last documented: 2026-05-07
Owner: codysumpter-cloud
Vault: knowledge-vault

## Purpose

The Sovereign Cloud / Cloud-Brain host is the VPS-side foundation for moving Buddy Brain and Omni Buddy agentic functionality off the local Intel MacBook and into cloud infrastructure that can support iOS-facing workflows.

## Hostinger VPS

- Provider: Hostinger VPS
- Public IP: 187.77.223.224
- OS: Ubuntu 24.04.x LTS, previously verified as Ubuntu 24.04.4 LTS during setup
- SSH user used during setup: root
- SSH key state: root SSH key was installed during setup

## Known deployed paths

These paths were established during the setup session:

- /opt/bmo-gateway
- /opt/automindlab-stack -> /opt/bmo-gateway
- /opt/buddy-brain
- /opt/omni-buddy

## Gateway/app service

- Service name: automind-app-factory.service
- Expected health endpoint on direct IP: http://187.77.223.224/api/health
- Expected health payload from setup receipt:

```json
{"status":"ok","service":"automindlab-enterprise-app-factory"}
```

- Expected root app title from setup receipt:

```html
<title>AutoMindLab Enterprise App Factory</title>
```

## Docker state from setup receipt

- Docker installed: Docker 29.4.3
- Docker Compose installed: v5.1.3
- Running container seen during setup:
  - openclaw-postgres-1
  - exposed port: 5432

## Important implementation fix already applied

The Enterprise App Factory initially returned:

```text
The client bundle has not been built yet.
```

Root cause:

The server resolved its package root incorrectly after the TypeScript build and looked for:

```text
/opt/bmo-gateway/services/enterprise-app-factory/dist/dist/client
```

The real client bundle path was:

```text
/opt/bmo-gateway/services/enterprise-app-factory/dist/client
```

Patch applied during setup:

- /opt/bmo-gateway/services/enterprise-app-factory/dist/server/server/app.js
- /opt/bmo-gateway/services/enterprise-app-factory/src/server/app.ts

The packageRoot() behavior was changed to use:

```ts
process.cwd()
```

## Protected boundary

The VPS being healthy by direct IP does not imply any public domain should be moved to it. Domain changes are protected release actions. See [DNS Guardrails](./dns-guardrails.md).
