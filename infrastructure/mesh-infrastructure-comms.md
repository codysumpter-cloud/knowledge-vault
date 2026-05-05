---
title: Mesh & Infrastructure Comms
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [mesh, reticulum, lXMF, sideband, scada, telemetry]
sources: [sideband, json-scada, nemoclaw]
---

# Mesh & Infrastructure Comms

## Overview
Strategic integration of infrastructure-less, peer-to-peer communication and industrial telemetry to enable robust, resilient agent coordination.

## Components

### 1. Reticulum & Sideband (Mesh Networking)
- **Capability:** Peer-to-peer, end-to-end encrypted messaging and telephony over LoRa, Packet Radio, and WiFi.
- **Strategic Value:** Provides a "Black-Out" communication channel. If cloud APIs go down, the Buddy Brain can still coordinate with local "Buddy-Nodes" via Reticulum.
- **Integration Path:** Implement a `sideband --daemon` bridge that allows the Buddy Brain to send and receive LXMF messages as an MCP tool.

### 2. JSON-SCADA (Industrial Telemetry)
- **Capability:** Scalable SCADA/IIoT platform centered on MongoDB.
- **Strategic Value:** High-resolution telemetry for physical hardware.
- **Integration Path:** Use the `mcp-json-scada-db` bridge to allow the agent to query real-time sensor data and trigger physical actuators.

### 3. NemoClaw (Secure Installation)
- **Capability:** NVIDIA plugin for secure OpenClaw installation.
- **Strategic Value:** Ensures that the hardware-acceleration layer for the local ML models is securely and correctly installed.

## Integration State
- [x] JSON-SCADA MCP bridge registered in dispatcher.
- [ ] Reticulum/Sideband daemon configured as a background transport.
- [ ] NemoClaw verified for GPU acceleration.
