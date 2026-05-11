# Sovereign Cloud Deployment Specification

## Target Infrastructure
- **Host**: Hostinger VPS
- **IP Address**: 187.77.223.224
- **Domain**: automindlab.tech (Targeting api.automindlab.tech)
- **Source Org**: AutoMindLab/automindlab-stack

## Agent Identity
- **Bot Name**: Cloud Buddy
- **Bot Username**: @BeMoreBuddy_bot
- **Bot Token**: 8650547852:AAHPcMsoKhKKCCbusWVtZGCL9BbQptSCr10
- **Owner ID**: 7636355145 (Cody Sumpter)
- **Allowed Users**: 7636355145, [TBD: Taylor]

## Stack Components
1. **Hermes Agent**: Full install with systemd/launchd service.
2. **BMO Gateway**: Orchestration layer from automindlab-stack.
3. **Buddy-Brain**: Core compute.
4. **Omni-Buddy**: Orchestration layer.
5. **Postgres**: Database for state and memory.

## Deployment Workflow
1. Restore SSH access via hPanel.
2. Install system dependencies (Python, Node, Docker).
3. Deploy BMO Stack containers.
4. Install and configure Hermes Agent.
5. Route DNS via Cloudflare.
6. Verify multi-user access for Taylor.
