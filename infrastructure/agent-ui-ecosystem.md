---
title: Agent UI Ecosystem
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [ui, dashboard, monitoring, control, hermes]
sources: [hermes-hudui, hermes-control-interface, hermes-webui, hermes-workspace]
confidence: high
---

# Agent UI Ecosystem

This page maps the available visual interfaces for the Hermes/BMO stack. The ecosystem is split between **Consciousness Monitoring** (read-heavy) and **Operational Control** (write-heavy).

## 1. Monitoring & Observation (Read-Heavy)
These tools focus on transparency, token analytics, and internal state visualization.

### Hermes HUD (HUDUI)
- **Purpose:** "Consciousness Monitor." A real-time dashboard of the agent's internal state.
- **Key Features:** 17 tabs covering identity, memory, sessions, and cost tracking.
- **Best Use:** High-level monitoring of agent health and token spend.
- **Access:** `http://localhost:3001`

## 2. Operational Control (Write-Heavy)
These tools focus on system administration, file editing, and agent configuration.

### Hermes Control Interface (HCI)
- **Purpose:** "Management Console." The administrative hub for the entire stack.
- **Key Features:**
  - **Multi-Agent Gateway:** Start/Stop/Configure multiple Hermes profiles.
  - **File Explorer:** Secure editor for `~/.hermes` config and memory.
  - **Cron Management:** Schedule and run background jobs.
  - **Terminal:** Browser-based PTY for direct shell access.
- **Best Use:** System administration, profile configuration, and low-level debugging.
- **Access:** `http://localhost:10272`

## 3. Integrated Workspaces (Hybrid)
Future targets for a unified experience.
- **Hermes Workspace:** A native web workspace combining chat, terminal, and memory inspection into one fluid interface.

## Comparison Matrix

| Feature | HUDUI | HCI | Workspace |
| :--- | :---: | :---: | :---: |
| **Real-time State** | ✅ High | ✅ Med | ✅ High |
| **File Editing** | ❌ No | ✅ Yes | ✅ Yes |
| **Profile Mgmt** | ❌ No | ✅ Yes | ✅ Yes |
| **Token Analytics** | ✅ High | ✅ Med | ✅ Med |
| **Terminal Access** | ❌ No | ✅ Yes | ✅ Yes |
| **Cron Control** | ❌ No | ✅ Yes | ✅ Yes |

[[buddy-system-architecture]]
[[prismtek-product-map]]
