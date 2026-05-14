# Mac Hermes + Windows NVIDIA Inference Node

Status: Proposed optimized local AI architecture  
Created: 2026-05-14

## Purpose

Optimize Prismtek's current local AI setup by separating control/orchestration from heavy inference and rendering.

Current user-provided setup:

- Hermes Agent lives on a 2018 Intel MacBook Pro with 8 GB RAM.
- Home Windows PC has Intel 285K, 48 GB DDR5 8000 MHz RAM, ASUS B860-I motherboard, ASUS Prime RTX 5070 Ti OC-class GPU, Ollama, `gemma4:latest`, and `gemma4:26b`.
- The Mac Hermes Agent can access the Windows Ollama server.
- User has a build.nvidia.com account.

## Recommended Architecture

```txt
2018 Intel MacBook Pro
Hermes operator / approval / KnowledgeVault / Obsidian control plane
        |
        | LAN / Tailscale / local HTTP, read-only by default
        v
Windows NVIDIA AI Workstation
Ollama / LM Studio / NVIDIA tooling / rendering / local inference
        |
        v
Model workers: gemma4:latest, gemma4:26b, future RTX/NVIDIA optimized models
```

## Role Split

### MacBook Pro — Control Plane

Keep on the Mac:

- Hermes orchestration;
- KnowledgeVault/Obsidian edits;
- approvals;
- receipts;
- cron job memory;
- content queues;
- light research;
- social publishing coordination.

Avoid on the Mac:

- heavy local model inference;
- video rendering;
- large embedding builds;
- large RAG indexing;
- long-running compute jobs.

### Windows NVIDIA PC — Workload Plane

Use the Windows PC for:

- Ollama model serving;
- local LLM experiments;
- embeddings/RAG indexing;
- YouTube Factory rendering;
- NVIDIA build.nvidia.com experiments;
- TensorRT/TensorRT for RTX investigation;
- model benchmarking;
- Buddy-Agent Windows adapter testing;
- Omni-Buddy local-first experiments.

## Immediate Optimization Plan

1. Verify exact Windows hardware:
   - GPU model;
   - VRAM;
   - NVIDIA driver version;
   - Windows version;
   - CUDA availability;
   - Ollama version;
   - whether WSL2/Docker Desktop are installed.
2. Benchmark current Ollama models from the Mac:
   - time to first token;
   - tokens/sec;
   - VRAM usage;
   - RAM usage;
   - CPU usage;
   - latency over LAN.
3. Add a `windows-inference-node` target to Hermes config.
4. Keep default model routing conservative:
   - Mac handles orchestration;
   - Windows handles heavy model calls;
   - fallback to cloud/ChatGPT only for tasks requiring higher reliability.
5. Test NVIDIA build.nvidia.com as a research/prototyping surface, not a secret-bearing automation target.
6. Evaluate whether LM Studio/Open WebUI adds useful UX over raw Ollama.
7. Evaluate NVIDIA TensorRT for RTX only after the current Ollama path is benchmarked.

## Suggested Routing Policy

```txt
Task type -> route

short planning / safety / approvals -> Mac Hermes local/cloud
content drafts -> Mac Hermes or Windows Ollama
long scripts -> Windows Ollama gemma4:26b
RAG over KnowledgeVault -> Windows inference node once indexed
video production planning -> Windows inference node
rendering / transcription / media -> Windows GPU node
repo mutation / approvals -> Mac Hermes control plane only
publishing -> approval-gated local social adapter only
```

## Security Boundaries

- Do not expose Ollama openly to the internet.
- Bind local model services to LAN/Tailscale only.
- Use firewall allowlists where possible.
- Do not store build.nvidia.com credentials in KnowledgeVault.
- Do not allow the Windows node to publish content, place trades/bets, or mutate repos without Mac-side approval.
- Write receipts on the Mac/KnowledgeVault side.
- Treat the Windows node as a worker, not the authority.

## NVIDIA Research Targets

Use build.nvidia.com to research:

- NVIDIA NIM APIs and model endpoints;
- AI Blueprints;
- NemoClaw / safe agent execution concepts;
- TensorRT for RTX;
- local RTX inference examples;
- AI PC workflows relevant to Prismtek content.

## Content Angles

- My AI operator lives on an old MacBook, but thinks through a Windows NVIDIA node.
- Local-first agents need a control plane and a workload plane.
- AI PCs matter when the agent has local memory, tools, approvals, and receipts.
- The GPU is not the operator; it is the worker.
- The safest architecture is not fully autonomous, it is delegated execution with receipts.

## Next Questions

- Exact GPU VRAM?
- Is Ollama bound to `127.0.0.1`, LAN IP, or Tailscale?
- Is Mac-to-Windows access encrypted or only LAN?
- Is the Windows PC always on?
- Is Open WebUI installed?
- Is LM Studio installed?
- Is Docker Desktop installed?
- Is WSL2 installed?
- Does Hermes have a named config entry for the Windows inference endpoint?
