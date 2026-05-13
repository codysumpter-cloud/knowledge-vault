---
name: bmo-stack-deployment
description: End-to-end deployment and build pipeline for the BMO (BeMore) AI Operating System, spanning Hostinger VPS (Power), Cloudflare Pages (Edge), and native iOS (Body).
---

# BMO Stack Deployment

This skill governs the deployment of the distributed BMO architecture.

## References
- `references/hostinger-vps-handoff.md`: Hostinger VPS recovery, SSH key install, Enterprise App Factory root-path fix, and DNS receipt checks from a real Sovereign Cloud handoff.
- `references/bread-makers-vps-discovery.md`: Discovery of the bread-makers project on Hostinger VPS, including structure, configuration files, and relevance to BMO stack testing.

## Architecture Overview
- **Sovereign Cloud (Cloud-Brain)**: A hybrid model where heavy LLM orchestration and runtime are offloaded to a Hostinger VPS (Power), routing via Cloudflare Edge (Edge), while the local Mac serves as the bridge for GUI-heavy tasks and developer orchestration.
- **Power (VPS)**: Hostinger VPS running PostgreSQL and the Gateway/Runtime.
- **Edge (Cloudflare)**: Pages/Workers acting as the public API and frontend proxy.
- **Body (iOS)**: Native SwiftUI app (`prismtek-apps`) targeting iOS 26.

## Deployment Workflow

### 1. VPS "Zero-Trust" Scrub
... (keep existing) ...

### 2. Power Layer (Docker - "The Brain Drop")
1. **Install Docker**: Use the official Docker apt repository for Ubuntu.
2. **The Brain Drop**: Clone the brain repositories (`buddy-brain`, `omni-buddy`) directly into `/opt/` to ensure a canonical, system-wide runtime location.
3. **Container Launch**: Execute `docker-compose up -d` within the respective directories to initialize the stack.
3. **Monorepo Pathing**: In the `automindlab-stack` repo, `docker-compose.yaml` files are often located in `deployments/<profile>/compose.yaml` rather than the root.
4. **Postgres Requirements**: Postgres containers WILL crash loop if `POSTGRES_PASSWORD` is not explicitly set in the `.env` file.

### 3. Runtime Posture & Maintenance
1. **Systemd User Services**: Deploy background processes (e.g., `hermes-gateway`) using `systemctl --user`. Ensure `XDG_RUNTIME_DIR` is explicitly set in service files or shell environment (e.g., `/run/user/1001`) to avoid socket failures.
2. **Repository Parity**: When running multiple instances (MacBook + VPS), maintain a "Surgical Delta" workflow:
    - Patch code on MacBook $\rightarrow$ Push to GitHub $\rightarrow$ Pull on VPS.
    - Avoid "hot-patching" directly on the VPS unless it's a critical runtime fix, in which case it MUST be back-ported to the source repo immediately.
3. **Git Sync Automation**: To ensure VPS runtime remains current without manual intervention, install a hourly `crontab` for the service user:
    - `0 * * * * cd /opt/<repo> && git pull origin main > /dev/null 2>&1`
4. **Credential Synchronization**: Use a secure source of truth (e.g., Apple Notes) to manage API keys. Deploy to VPS via a `.env` file local to the runtime root, and verify connectivity via a "Canary" response (e.g., a simple prompt returning a specific token like `OK31`).

## Pitfalls & Fixes
...
- **Telegram Connection Failures**: If the gateway reports `No bot token configured` despite existence in `.env`, verify the service is running under the correct user context and that the `.env` path is absolute or correctly resolved relative to the `WorkingDirectory`.
- **Gemini/Gemma 4 Quota (429)**: Google's free-tier has aggressive rate limits. To prevent "429 amplification", set `api_max_retries: 1` and tune the compression threshold in `config.yaml` to reduce token volume.
- **Symmetry Drift**: Never assume the VPS is up to date because the MacBook is. Run a `git pull` check across all `/opt/` directories during any "Recovery" or "Sustain" phase.


### 4. Body Build (iOS 26)
1. **Identity Pivot (Bundle ID Update)**: If transitioning from experimental to professional IDs:
    - Patch `project.pbxproj` in all targets to the new Bundle ID (e.g., `com.prismtek.buddy`).
    - Update `exportOptions-testflight.plist` to match the new identity for successful App Store Connect uploads.
2. **Archive & Export**: ... (keep existing) ...

## Pitfalls & Fixes
- **Hostinger hPanel Root Password Reset**: If `sshpass` returns `Permission denied` but hPanel is open, use the browser/CDP or hPanel UI to click `Root password -> Change`, set the supplied password, confirm, then immediately verify `ssh root@IP`. After password access works, install the local public SSH key into `/root/.ssh/authorized_keys` and verify `ssh -o BatchMode=yes root@IP "echo SSH_KEY_OK"`.
- **Hostinger/Chrome CDP Control**: When Chrome is running with `--remote-debugging-port=9222`, query `http://127.0.0.1:9222/json/list` to find hPanel tabs and evaluate DOM JavaScript through CDP. This bypasses AppleScript's `Allow JavaScript from Apple Events` requirement and avoids vision-coordinate fragility.
- **Enterprise App Factory Built Client Missing**: If the VPS serves `The client bundle has not been built yet` despite `dist/client/index.html` existing, check `services/enterprise-app-factory/src/server/app.ts` and built `dist/server/server/app.js`: `packageRoot()` may resolve relative to `import.meta.dirname` after TypeScript output, causing lookup under `dist/dist/client`. Patch to `return process.cwd();`, restart `automind-app-factory.service`, then verify `/` serves the app HTML and `/api/health` returns JSON.
- **DNS Receipt Discipline**: Do not claim Cloudflare cutover from VPS-local Host header tests alone. Verify both layers: (1) VPS Nginx accepts `Host: prismtek.dev` locally, and (2) public `https://prismtek.dev/api/health` resolves to the intended VPS response after DNS/proxy changes.
- **App ID Registration**: When using the professional bundle ID `com.prismtek.buddy`, ensure the App ID is registered in the Apple Developer Portal with the following "Full Power" capabilities, or TestFlight builds will fail to initialize core agent features:
    - [ ] Push Notifications (Essential for Agent alerts)
    - [ ] Associated Domains (For Universal Links to `prismtek.dev`)
    - [ ] iCloud (For cross-device state sync)
    - [ ] Background Modes (Remote notifications, Background fetch, Background processing)
    - [ ] App Groups (For communication between the App and the Agent-Bridge)
- **`memo` Install**: ... (keep existing) ...
- **Hardware Heat**: ... (keep existing) ...
- **SSH Pass**: ... (keep existing) ...
