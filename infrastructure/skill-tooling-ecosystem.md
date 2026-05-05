---
title: Skill & Tooling Ecosystem
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [skills, mcp, tooling, superpowers, automation]
sources: [superpowers-zh, arcade-mcp, mcporter]
confidence: high
---

# Skill & Tooling Ecosystem

This page maps the "Force Multipliers" available to the Buddy Brain—the specialized skills and MCP frameworks that turn a general LLM into a professional operator.

## 1. Methodology Layer (Superpowers)
Instead of generic prompts, the system uses **Systematized Workflows**.
- **Core Methodology:** Moving from "Chatting" $\rightarrow$ "Executing Plans."
- **Key Skills:** 
  - `writing-plans` $\rightarrow$ `executing-plans` $\rightarrow$ `verification-before-completion`.
  - `systematic-debugging` (Locate $\rightarrow$ Analyze $\rightarrow$ Hypothesize $\rightarrow$ Fix).
  - `subagent-driven-development` (Parallel task execution with multi-agent review).
- **Sovereignty:** These skills ensure the agent doesn't "hallucinate progress" but provides evidence-based completion.

## 2. Tooling Layer (MCP Frameworks)
The "arms" of the agent. We use a multi-framework approach to build and call tools.

### Arcade MCP (The Builder)
- **Purpose:** Rapid development of production-grade MCP servers.
- **Capability:** Provides a structured way to define tools with `requires_auth` and `requires_secrets` without exposing credentials to the LLM.
- **Strategic Use:** We will use Arcade to build the **Everything is Crab Bridge**, ensuring that API keys for game telemetry are handled securely.

### MCPorter (The Dispatcher)
- **Purpose:** A high-performance runtime and CLI for calling MCP tools across different platforms.
- **Key Capabilities:**
  - **Zero-Config Discovery:** Automatically merges configs from Cursor, Claude, and local files.
  - **Typed Clients:** `emit-ts` generates TypeScript interfaces for MCP tools, allowing for strongly-typed automation.
  - **CLI Generation:** Can turn any MCP server into a standalone CLI tool.
- **Strategic Use:** MCPorter allows the Buddy Brain to call tools across different "harnesses" without re-configuring the transport every time.

## 3. Integration Strategy
The goal is a **Seamless Toolchain**:
`Superpowers (The Method)` $\rightarrow$ `MCPorter (The Dispatcher)` $\rightarrow$ `Arcade MCP (The Tool)` $\rightarrow$ `Game/System (The Target)`.

[[buddy-system-architecture]]
[[prismtek-product-map]]
