---
title: Local ML & Model Orchestration
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [ml, local-llm, mlc-llm, mlx, gemma, inference]
sources: [mlc-llm, mlx-swift, gemma, ml-intern]
---

# Local ML & Model Orchestration

## Overview
Strategic integration of local LLM inference to reduce dependency on cloud APIs and enable offline agent operations.

## Components

### 1. MLC LLM (Universal Deployment)
- **Capability:** Compiles and runs LLMs natively on Intel iGPU (via Metal/Vulkan).
- **Strategic Value:** Provides an OpenAI-compatible REST server locally.
- **Integration Path:** Deploy as a background service in `omni-buddy` for low-latency "Fast-Thinking" tasks.

### 2. MLX Swift (Apple Silicon/Metal Optimization)
- **Capability:** High-performance ML primitives for Apple hardware.
- **Strategic Value:** Optimization of local embedding models and small-parameter LLMs.

### 3. ML-Intern (Automated ML Engineering)
- **Capability:** An open-source ML engineer that reads papers and ships models.
- **Strategic Value:** Automating the fine-tuning and optimization of the Buddy Brain's local models.

## Integration State
- [ ] Deploy MLC LLM REST server on Intel Mac (Metal iGPU).
- [ ] Connect `buddy-brain` to local inference endpoint as a fallback provider.
- [ ] Integrate `ml-intern` into the `self-evolution` loop for automated model optimization.
