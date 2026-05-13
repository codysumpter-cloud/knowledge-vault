---
title: MCP Dispatcher
description: Interface with the mcporter dispatcher to execute external MCP tools.
category: infrastructure
---

# MCP Dispatcher

## Goal
Execute tools from the registered MCP servers (Codex, Arcade-FS, Telemetry, PixelLab) without needing to know the exact server name.

## Workflow
1. Call `npx mcporter list` to see available servers.
2. Use `npx mcporter call <server> <tool> <args>` to execute a tool.
3. Verify the output before proceeding.

## Pitfalls
- Servers are stdio-based; a timeout usually means the server process failed to start.
- Always check the server status before calling a complex tool.
