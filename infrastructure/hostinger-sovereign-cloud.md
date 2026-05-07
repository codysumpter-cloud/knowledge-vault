# Hostinger Sovereign Cloud Setup

## Overview
This document describes the Hostinger VPS setup for the AutoMindLab/BMO stack and the Cloud Buddy Telegram Hermes gateway.

## VPS Details
- Provider: Hostinger
- IP: 187.77.223.224
- OS: Ubuntu 24.04
- RAM: 7.8 GiB
- vCPU: 2
- Storage: 251 GB SSD

## Services Running
- Docker
- Nginx
- `automind-diagnostic.service`
- `automind-app-factory.service`
- `ollama.service`
- `hermes-gateway.service` (user service under hermes user)

## Hermes Agent Configuration
- Hermes home: `/home/hermes/.hermes`
- Model: local Ollama `gemma4:e2b`
- Provider: custom
- Base URL: `http://127.0.0.1:11434/v1/`
- Max tokens: 2048
- Context length: 64000
- Auxiliary models (vision, compression, session_search, title_generation) also point to the same local endpoint.

## Installed Models
- Ollama model: `gemma4:e2b` (approx 7.2 GB)

## AutoMindLab Services
- Enterprise app factory: accessible at `/api/health`
- Diagnostic consultation: accessible at `/diagnostic/api/health`
- Gateway health: `/healthz` returns "automindlab gateway ok"

## Telegram Bot
- Bot username: `@BeMoreBuddy_bot`
- Owner Telegram ID: 7636355145
- Bot token stored in `/home/hermes/.hermes/.env` as `TELEGRAM_BOT_TOKEN`

## DNS Policy
- `prismtek.dev` remains on Cloudflare DNS.
- `automindlab.tech` is intended to remain on Hostinger DNS (per user direction).
- DNS changes require explicit user approval.

## Verification (as of 2026-05-07)
- All services active.
- Hermes gateway responds to local model without API errors (429/401).
- Direct bot API send successful.

## Maintenance
- Local repositories (`/opt/buddy-brain`, `/opt/omni-buddy`) should be kept up to date via periodic `git pull`.
- Hermes gateway can be restarted via `systemctl --user restart hermes-gateway.service`.
- Ollama service can be restarted via `systemctl restart ollama`.

## References
- Buddy-brain repo: `https://github.com/codysumpter-cloud/buddy-brain`
- Omni-buddy repo: `https://github.com/codysumpter-cloud/omni-buddy`
- Knowledge vault: this repository