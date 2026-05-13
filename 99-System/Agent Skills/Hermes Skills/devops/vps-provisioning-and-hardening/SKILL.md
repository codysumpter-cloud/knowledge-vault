---
name: vps-provisioning-and-hardening
description: "Provisioning, auditing, and hardening a fresh VPS for BMO/Sovereign Cloud deployments."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [vps, hardening, ubuntu, ssh, devops]
---

# VPS Provisioning and Hardening

This skill governs the 'Surgical Scrub' process for taking over a potentially used VPS and preparing it as a secure, clean host for BMO/Sovereign Cloud infrastructure.

## Workflow: The Surgical Scrub

### 1. Connectivity & Reachability
Before attempting login, verify the network path:
- **Ping**: Check basic ICMP reachability.
- **Port Probe**: Use `nc -zv <ip> 22` to ensure SSH is listening.

### 2. Initial Access (Non-Interactive)
When dealing with a fresh root password and no keys, standard `ssh` is interactive. For agent-driven setup:
- **Tool**: Use `sshpass` to provide the password non-interactively.
- **Command**: `sshpass -p '<password>' ssh -o StrictHostKeyChecking=no root@<ip> '<command>'`
- **Fall-back**: If `sshpass` is missing on the host, install it via `brew install sshpass` (macOS).

### 3. Audit (The Discovery Phase)
Run a baseline probe to identify legacy residents:
- **System**: `uname -a; uptime`
- **Storage**: `df -h` (Check for large unexpected partitions or filled disks).
- **Memory**: `free -m`
- **Processes**: `ps aux` (Look for unexpected long-running services).
- **Ports**: `netstat -tulpn` or `ss -tulpn` (Identify what is listening).
- **Cron**: `crontab -l` and `ls /etc/cron.*` (Check for persistence).

### 4. Cleanse & Harden
- **OS Update**: `apt update && apt upgrade -y`
- **User Management**:
    - Create a dedicated non-root service user for the application stack.
    - Implement SSH Key-based authentication.
    - Disable root password login in `/etc/ssh/sshd_config` (`PermitRootLogin prohibit-password`).
- **Network Security**:
    - Install/Configure `ufw` (Uncomplicated Firewall).
    - Default Deny: `ufw default deny incoming`.
    - Allow SSH: `ufw allow ssh`.
    - Open specific application ports only as needed.

### 5. Environment Provisioning
- Install required runtimes (Docker, Node.js, Python).
- Set up repository clones and environment secrets.

## Pitfalls
- **SSH Lockout**: Always verify key-based access works in a separate terminal session BEFORE disabling password authentication.
- **Kernel Panic**: Be cautious with `apt upgrade` on specialized VPS kernels; check provider docs for custom kernel requirements.
- **Memory Bottlenecks**: On small VPS instances (e.g., 8GB), configure a swap file if the workload involves heavy LLM gateways or builds.

## Verification
- `ssh <user>@<ip>` (Should connect without password).
- `sudo ufw status` (Should show only intended ports open).
- `last` (Should show only expected login sessions).
