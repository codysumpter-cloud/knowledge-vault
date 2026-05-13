# Sovereign Cloud Setup Reference for Knowledge Vault

This reference documents the Sovereign Cloud setup performed for the Buddy Brain/Omni Buddy infrastructure migration.

## Overview
Moved agentic functionality from local Intel MacBook to Hostinger VPS to enable iOS-facing workflows and reduce local resource constraints.

## VPS Details
- Provider: Hostinger VPS
- IP: 187.77.223.224
- OS: Ubuntu 24.04.x LTS
- Access: root SSH key installed

## Deployed Components
- /opt/bmo-gateway (Enterprise App Factory)
- /opt/buddy-brain (AgentCraft core)
- /opt/omni-buddy (Omni-buddy orchestration)
- /opt/automindlab-stack → /opt/bmo-gateway (symlink)

## Key Services
- automind-app-factory.service (runs Enterprise App Factory)
- openclaw-postgres-1 (Docker container on port 5432)

## Critical Fix Applied
**Issue**: Enterprise App Factory returned "The client bundle has not been built yet."
**Root Cause**: TypeScript build output structure mismatch:
  - Expected: /dist/client
  - Resolved: /dist/dist/client (incorrect nesting)
**Fix**: Modified packageRoot() in:
  - /opt/bmo-gateway/services/enterprise-app-factory/dist/server/server/app.js
  - /opt/bmo-gateway/services/enterprise-app-factory/src/server/app.ts
  - Changed to use: process.cwd()

## Verification Receipts
- Direct IP health: http://187.77.223.224/api/health → {"status":"ok","service":"automindlab-enterprise-app-factory"}
- Direct IP root: Contains <title>AutoMindLab Enterprise App Factory</title>
- Nginx configured for: 187.77.223.224, automindlab.tech, prismtek.dev (and www variants)

## DNS Guardrails (Critical)
- automindlab.tech: Remains on Hostinger DNS (working setup - do not change)
- prismtek.dev: Remains on Cloudflare Pages (free hosting benefit - do not change)
- **Never suggest DNS cutovers without explicit user authorization**
- Future additive subdomains only (e.g., api.prismtek.dev → VPS) if explicitly requested

## Knowledge Vault Integration
This setup is documented in the knowledge-vault repository:
- infrastructure/sovereign-cloud-current-state.md
- infrastructure/dns-guardrails.md
- infrastructure/deployment-receipts.md
- wiki/Home.md

GitHub Receipt: https://github.com/codysumpter-cloud/knowledge-vault/commit/d2c2f4a322010f5ff10a3fe3fcd6d8a86c02ef14

## Operating Principle
The VPS serves as sovereign cloud infrastructure - healthy by direct IP for testing/staging, but public domains remain unchanged unless explicitly authorized as a release action.
