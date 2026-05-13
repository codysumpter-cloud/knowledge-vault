---
name: bemore-ios-development
description: Unified workflow for developing, building, and maintaining the BeMore iOS ecosystem (Shell and Platform apps).
---

# BeMore iOS Development

This skill governs the development of the native iOS subtrees within the BeMore ecosystem, managing the critical balance between local-first runtime and cloud platform orchestration.

## 🛠️ System Architecture
The iOS product is split into two primary targets to separate concerns:
- **BeMoreAgent Shell (`apps/openclaw-shell-ios`)**: Local-first operator shell. Focuses on MLC runtime, on-device inference, and local files.
- **BeMoreAgent Platform (`apps/bemoreagent-platform-ios`)**: Cloud control plane. Focuses on repo-linked workspaces, provider management, and admin surfaces.

## 🔄 Essential Workflow

### 1. Context Alignment
Before making any change, verify the current product phase via `knowledge-vault/pokemon-champions/BEMORE_PHASED_ROADMAP.md`.
- **Priority Order**: Body $\rightarrow$ Continuity $\rightarrow$ Ecosystem $\rightarrow$ Economy.
- Avoid introducing "Marketplace" or "Economy" features if "Core Embodiment" (Workspace/Runtime) is not yet validated.

### 2. Target Selection
Determine which project the change belongs to:
- **Local Runtime/Buddy Loop/On-device ML** $\rightarrow$ `openclaw-shell-ios`.
- **Cloud Sync/Workspaces/Billing/Admin** $\rightarrow$ `bemoreagent-platform-ios`.
- **Common Schemas/Stats/Buddy DNA** $\rightarrow$ `buddy-brain/config/buddy/` (JSON).

### 3. Build & Verification (Resource-Constrained)
Given the 8GB Intel MacBook bottleneck:
- **Primary Path**: Use **Xcode Cloud/GitHub Actions** for builds and TestFlight distribution. This is the only stable path since local signing certificates (private keys) are rarely persistent or synchronized on this Mac.
- **Local Path**: Use the local machine for surgical verification, UI tests, and `xcodegen` project generation.
- **Stability Rule**: Local `xcodebuild archive` is possible, but `xcodebuild -exportArchive` will fail if the Distribution `.p12` private key is missing from the Keychain. Do not waste time attempting local exports unless a `.p12` is explicitly provided; immediately pivot to the GitHub workflow.
- **Bundled MLC Model Rule**: When shipping Gemma/MLC assets, verify the final archive contains `Products/Applications/BeMoreAgent.app/BundledModels/<model>/mlc-chat-config.json`. If a plain XcodeGen `resources:` folder reference does not land the nested model in the archive, add an explicit post-build `ditto`/copy phase into `$TARGET_BUILD_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/BundledModels` and verify before export.
- **TestFlight Visibility Rule**: Treat `Upload succeeded` / `Uploaded package is processing` as an upload receipt, not final availability. Keep the release task open until Build/Platform/Version is visible in TestFlight/App Store Connect or an Apple-side processing blocker is found.

## ⚠️ Pitfalls & Guardrails
- **No Fake Completion**: Do not claim a la-mode "completed" feature without a receipt (build log, screenshot, or verified IPA).
- **Boundary Integrity**: Ensure the iOS app does not mutate the MacBook `~/.openclaw` runtime directly unless explicitly routed through a gateway.
- **Schema First**: Always update the JSON schemas in `buddy-brain` before implementing the corresponding Swift models in the app to prevent contract drift.

## 📂 References
- [[architecture]] - Detailed mapping of the Shell vs. Platform split.
- [[roadmap]] - Current phase goals and exit criteria.
- [[product-vision]] - The 'Lovable Buddy' thesis.
