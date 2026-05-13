---
name: vps-hardening
description: "Surgical scrubbing and hardening of a used or fresh VPS to ensure a zero-trust, clean environment."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [vps, security, hardening, ubuntu, devops]
---

# VPS Hardening (Surgical Scrub)

This skill defines the "Surgical Scrub" workflow for taking over an existing VPS. Instead of a full OS reinstall (which can be slow), this process identifies and removes legacy artifacts to create a clean, secure baseline.

## Workflow

### 1. Audit & Purge (The Scrub)
- **User Audit**: Inspect `/etc/passwd` for non-system users. Remove any unauthorized or legacy users.
  - `grep -v "/sbin" /etc/passwd`
  - `killall -u <username>` (Important: kill active processes first).
  - `userdel -r <username>`
- **SSH Lockdown**: Wipe existing authorized keys to prevent legacy access.
  - `echo "" > /root/.ssh/authorized_keys`
- **Service Audit**: List all running services and disable non-essential legacy ones.
  - `systemctl list-units --type=service --state=running`
- **Cron Cleanup**: Clear all system and user crontabs.
  - `crontab -l` / `crontab -r`

### 2. Hardening & Base Setup
- **System Update**: Ensure the kernel and all packages are current.
  - `apt update && apt upgrade -y`
- **Firewall Setup**: Implement a "Deny All" default policy.
  - `apt install -y ufw`
  - `ufw default deny incoming`
  - `ufw allow 22/tcp` (Crucial: do this before enabling!)
  - `ufw --force enable`
- **Identity**: Create a dedicated non-root service user for application stacks.

### 3. Verification
- Verify firewall status: `ufw status`
- Verify user list: `cut -d: -f1 /etc/passwd`
- Verify SSH key emptiness: `ls -l /root/.ssh/authorized_keys`

## Pitfalls

- **SSH Lockout**: Never enable `ufw` without first allowing port 22.
- **Active Users**: `userdel` will fail if the user has running processes. Use `killall -u <user>` before deleting.
- **Kernel Updates**: Major upgrades (like `apt upgrade`) often require a reboot to load the new kernel. Verify with `uname -a` after reboot.
- **Interactive Prompts**: When running `apt upgrade` non-interactively via SSH, set `DEBIAN_FRONTEND=noninteractive` to avoid hanging on config prompts.

## Receipts
Provide a summary of:
1. Users removed.
2. Services disabled.
3. Firewall rules applied.
4. Final OS/Kernel version.
