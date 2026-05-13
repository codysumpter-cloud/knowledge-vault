---
name: bemore-ios-dev
description: Development, build, and deployment lifecycle for native BeMore iOS apps.
triggers: [ "be-more ios", "testflight", "build number", "bundle id", "xcode cloud" ]
---
# BeMore iOS Development

This skill governs the development, build, and deployment lifecycle of the BeMore native iOS apps (`BeMoreAgentShell` and `BeMoreAgentPlatform`).

## 🎯 Core Objectives
- Maintain the distinction between the **Local-First Shell** (on-device runtime) and the **Platform Control Plane** (cloud/admin).
- Ensure a high-confidence deployment pipeline from local source $\rightarrow$ Xcode Cloud $\rightarrow$ TestFlight.
- Prevent "Build Number Drift" and "Signing Zombie" states.

## 🛠️ Operational Workflow

### 1. Versioning & Build Numbers
- **Surgical Bumps:** Always verify the current `CFBundleVersion` in `Info.plist` before claiming a build number.
- **Tainted Builds:** If a build is failed or skipped, increment to the next integer (e.g., if 52 is tainted, bump directly to 53) rather than attempting to reuse the number.
- **Canonical Source:** The `Info.plist` in the `.xcodeproj` is the source of truth for the build number.

### 2. Signing & Bundle IDs
- **Avoid Generic IDs:** Never use generic bundle identifiers like `BeMoreAgent`. Always use the professional reverse-DNS format (e.g., `com.prismtek.buddy`).
- **Signing Errors:** When encountering `No signing certificate found` or `No Accounts` errors on a local Mac:
    - Prioritize updating the `PRODUCT_BUNDLE_IDENTIFIER` in the `.pbxproj` first.
    - If local signing is blocked by keychain/account issues (common on Intel Macs), pivot immediately to **Xcode Cloud** for delivery.

### 3. Build & Deployment Path (Intel Mac Optimized)
Due to the 8GB RAM constraint on the development machine, follow this path:
1. **Local Edit** $\rightarrow$ **Git Commit** $\rightarrow$ **Push to Main**.
2. **Trigger Xcode Cloud:** Let Apple's infrastructure handle the heavy lifting of archiving and signing.
3. **TestFlight Verification:** Verify the build version in TestFlight before starting the next feature cycle.

## ⚠️ Pitfalls & Lessons
- **The "OpenClaw" Ghost:** Legacy directories (like `openclaw-shell-ios` in `buddy-brain`) may still exist. Always treat the monorepo path `apps/bemore-ios-native/` as the canonical source.
- **Local vs. Cloud Divergence:** Be wary of local build artifacts that aren't committed. Always `git status` before claiming a build is "ready" for the cloud.
- **Surgical Patching:** Use `patch` for `Info.plist` and `.pbxproj` changes to avoid corrupting complex Xcode project files.

## ✅ Verification Checklist
- [ ] `CFBundleVersion` incremented in `Info.plist`.
- [ ] `PRODUCT_BUNDLE_IDENTIFIER` matches the active Apple Developer team account.
- [ ] Changes pushed to the branch triggering Xcode Cloud.
- [ ] Build version in TestFlight matches the targeted build number.
