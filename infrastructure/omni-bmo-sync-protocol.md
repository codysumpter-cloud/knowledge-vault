---
title: Omni-BMO Sync Protocol
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [omni-buddy, transport, synchronization, mesh]
sources: [omni-buddy/docs/TRANSPORT_CONTRACT.md]
confidence: high
---

# Omni-BMO Sync Protocol

The Omni-BMO protocol ensures reliable communication between the operator and the agent across varying network conditions.

## 1. Transport Modes
The system dynamically selects the best path based on health checks:
- **`online`**: High-throughput internet/local network (Preferred).
- **`mesh`**: Peer-to-peer mesh reachable endpoints.
- **`reticulum_fallback`**: Sovereignty path. Low-bandwidth, high-resilience control messages.
- **`auto`**: Automatic selection based on real-time health.

## 2. Resolution Hierarchy
1. **Manual Override:** User-set mode wins.
2. **Online Path:** Preferred if healthy.
3. **Mesh Path:** Preferred if IP is down but mesh is up.
4. **Reticulum:** Last resort for critical control and text.

## 3. Reliability and Diagnostics
- **Failover:** Managed by `transport_failover_timeout_sec`.
- **Verification:** The `/doctor` and `/net-doctor` commands emit actionable diagnostics.
- **Sovereignty:** The use of Reticulum allows the system to function even in completely disconnected (off-grid) environments.

[[buddy-system-architecture]]
[[prismtek-product-map]]
