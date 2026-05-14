# Home Windows AI Workstation

Status: User-provided hardware profile  
Created: 2026-05-14

## Purpose

This is Prismtek's home Windows workstation profile for local AI, agent runtime testing, NVIDIA AI tooling, content production, local model experiments, and future Omni-Buddy / Buddy-Agent local execution work.

## User-Provided Hardware

- CPU: Intel Core Ultra 9 285K / "Intel 285K"
- Memory: 48 GB DDR5, 8000 MHz
- Motherboard: ASUS B860-I motherboard
- GPU: ASUS Prime RTX 5070 Ti OC graphics card, user wrote `5070t OC`
- Account access: build.nvidia.com account exists
- OS target: Windows PC

## Notes / Clarifications Needed

- Confirm exact GPU model string in Windows/NVIDIA Control Panel or GPU-Z. User wrote `5070t OC`; likely means ASUS Prime RTX 5070 Ti OC.
- Confirm GPU VRAM amount.
- Confirm Windows version.
- Confirm NVIDIA driver version.
- Confirm whether WSL2 is enabled.
- Confirm whether Docker Desktop, CUDA toolkit, Ollama, LM Studio, or NVIDIA app are installed.

## Strategic Value

This machine should be treated as a local AI operator workstation for:

- local LLM experiments;
- Ollama/LM Studio model serving;
- NVIDIA build.nvidia.com workflows;
- local agent runtime testing;
- Buddy-Agent Windows adapter testing;
- Omni-Buddy local-first experiments;
- content production and video rendering;
- YouTube Factory production packets;
- local browser/social automation testing with strict approval gates;
- hardware/content angle around AI PCs and local-first agents.

## Safety Boundaries

Do not store:

- NVIDIA account credentials;
- Windows login credentials;
- cookies;
- auth tokens;
- remote-access secrets;
- wallet keys;
- brokerage/sportsbook credentials.

Agent access to this machine should remain approval-gated for:

- installing software;
- changing drivers;
- changing BIOS/UEFI settings;
- overclocking/undervolting;
- opening broker/sportsbook/wallet pages;
- publishing content;
- deleting files;
- modifying repositories.

## Recommended Setup Targets

### Local AI Runtime

- NVIDIA driver current and stable.
- NVIDIA app installed.
- Ollama or LM Studio installed for local LLM serving.
- Python 3.11+ installed.
- Git installed.
- Windows Terminal installed.
- WSL2 enabled for Linux-compatible agent tooling if needed.
- Optional: Docker Desktop with NVIDIA GPU support after confirming stable drivers.

### Prismtek Stack Targets

- Clone/sync public repos:
  - `buddy-brain`
  - `omni-buddy`
  - `prismtek-apps`
  - `knowledge-vault`
  - `hermes-agent`
- Keep `buddy-agent` private until public alpha hardening is complete.
- Add this workstation as a known local execution target in Buddy-Agent docs once safe.

### Content Targets

- Use this hardware profile for AI PC / local-first agent content.
- Good topic angle:
  - AI PCs matter because agents need local context, local tools, local approvals, and local receipts.

## Next Plans

1. Ask Hermes to run a Windows workstation inventory script manually or approval-gated.
2. Record exact CPU/GPU/VRAM/driver/Windows/WSL/CUDA state.
3. Create a local AI setup checklist.
4. Create a Buddy-Agent Windows adapter checklist.
5. Create content drafts around NVIDIA AI PC / local-first Prismtek stack.
6. Use build.nvidia.com only through approved user-controlled login/session routes. Do not store credentials.
