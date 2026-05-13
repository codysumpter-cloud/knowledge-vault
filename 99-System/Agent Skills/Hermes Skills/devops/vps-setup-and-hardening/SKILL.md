---
name: vps-setup-and-hardening
description: "Workflow for 'Surgical Scrubbing' and hardening a used or fresh VPS to ensure a zero-trust environment before deployment."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [vps, linux, hardening, security, devops]
---

# VPS Setup & Hardening

Use this skill when inheriting a VPS (e.g., from a friend or a repurposed instance) to ensure no legacy users, keys, or services compromise the new stack.

## The "Surgical Scrub" Workflow

### 1. Identity Audit & Purge
Identify and remove non-system users to ensure you are the only human operator.
- **Audit**: `grep -v "/sbin" /etc/passwd` (Look for unexpected users in `/home`).
- **Purge**: `userdel -r <username>` for any ghost accounts.

### 2. SSH Lockdown
Prevent unauthorized access via legacy SSH keys.
- **Wipe Keys**: `echo "" > /root/.ssh/authorized_keys` (Immediately removes all existing key-based access).
- **Password Update**: Set a strong root password if not already done.
- **Key Rotation**: Immediately generate a new SSH key pair and add your public key to the now-empty `authorized_keys`.

### 3. Network Hardening (UFW)
Establish a default-deny posture.
- **Allow SSH**: `ufw allow 22/tcp` (CRITICAL: do this before enabling).
- **Enable**: `ufw --force enable`.
- **App-Specific Ports**: Open only necessary ports (e.g., 80, 443) as the stack is deployed.

### 4. System Refresh
Ensure the OS is patched and clean.
- **Update**: `apt update && apt upgrade -y`.
- **Clean**: `apt autoremove -y`.

## Technical Patterns

### Non-Interactive Setup
When automating this via a remote agent, use `sshpass` for initial password-based entry until keys are rotated:
```bash
sshpass -p 'password' ssh -o StrictHostKeyChecking=no root@<ip> 'command'
```

### Monorepo Deployment Pitfall
When deploying from monorepos (like the `automindlab-stack`), the `docker-compose.yaml` is often NOT in the root.
- **Discovery**: Use `find . -name "compose.yaml"` to locate the specific deployment slice.
- **Execution**: Always specify the file path: `docker compose -f path/to/compose.yaml up -d`.

## Verification
- Check active ports: `netstat -tulpn` or `ss -tulpn`.
- Verify users: `cut -d: -f1 /etc/passwd`.
- Test firewall: Try accessing a blocked port from an external IP.
