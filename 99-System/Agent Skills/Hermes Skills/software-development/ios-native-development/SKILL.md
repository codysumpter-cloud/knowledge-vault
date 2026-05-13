---
name: ios-native-development
description: Workflow for building, signing, and distributing native iOS applications via CLI (xcodegen, xcodebuild, Transporter).
---

# iOS Native Development

This skill governs the lifecycle of building native iOS applications, specifically for projects using `xcodegen` for project management and `xcodebuild` for CI/CD-style archives.

## Trigger Conditions
- Task involves building native iOS apps (`.xcodeproj`, `.xcworkspace`).
- Task requires generating an `.ipa` for TestFlight or App Store distribution.
- Task involves troubleshooting Xcode signing certificates, provisioning profiles, or build failures on restored machines.
- Task requires automating the build-to-distribution pipeline.

## Workflow

### 1. Project Generation
Avoid editing `.xcodeproj` files manually. Use `xcodegen` to maintain project structure via a `project.yml`.
```bash
# Generate the Xcode project from project.yml
xcodegen generate
```

## Bundle Identifier Migration
When changing the `PRODUCT_BUNDLE_IDENTIFIER` for the project:
1. **Project File**: Update all occurrences of `PRODUCT_BUNDLE_IDENTIFIER` in the `.pbxproj` file. Use `grep` to find all occurrences across all targets.
2. **Export Options**: Update the `provisioningProfiles` dictionary in the `.plist` export options file to map the new Bundle ID to its Provisioning Profile UUID.
3. **Portal Sync**: Ensure the new identifier is registered as an **Explicit App ID** in the Apple Developer portal before attempting to archive.

## Build and Archive
## Build and Archive\n\n- **Surgical Build Bumps:** Use `patch` or `sed` to update `CFBundleVersion` in `Info.plist` directly. Avoid manual Xcode UI bumps to save resources on constrained hardware.
- **Bundle ID Governance:** Ensure the `PRODUCT_BUNDLE_IDENTIFIER` in the `.pbxproj` corresponds to the authorized team certificate (e.g., `com.prismtek.buddy`). Generic identifiers will trigger signing failures.
- **Xcode Cloud First:** On resource-constrained hardware (e.g., 8GB RAM), prioritize pushing commits to trigger Xcode Cloud over local archiving.
- **Conflict Resolution:** When rebasing native projects, prefer `checkout --ours` for runtime scripts (e.g., `prepare-bundled-mlc-model.sh`) if the local version contains advanced optimizations.
\n\nUse `xcodebuild archive` to create a `.xcarchive`.

xcodebuild archive \
  -scheme <SchemeName> \
  -configuration Release \
  -archivePath Build/<AppName>.xcarchive \
  -destination 'generic/platform=iOS'
```

### 3. Exporting the IPA
Use a `.plist` export options file to define the distribution method (e.g., `app-store`, `ad-hoc`, `development`).
```bash
xcodebuild -exportArchive \
  -archivePath Build/<AppName>.xcarchive \
  -exportOptionsPlist exportOptions-testflight.plist \
  -exportPath Build/Export
```
### Distribution via Transporter
Push the resulting `.ipa` to App Store Connect.
```bash
# MODERN METHOD: Using App Store Connect API Key (.p8 file)
xcrun altool --upload-app \
  --type ios \
  --file Build/Export/<AppName>.ipa \
  --api-issuer <IssuerID> \
  --api-key <KeyID> \
  --api-key-file /path/to/AuthKey_<KeyID>.p8

# LEGACY METHOD: Using App-Specific Password
xcrun altool --upload-app -f Build/Export/<AppName>.ipa -t ios -u <AppleID> -p <AppSpecificPassword>
```

## Pitfalls & Troubleshooting

### API Key Authentication Failure (altool 401)
**Symptom**: `altool` returns `NOT_AUTHORIZED` or `Authentication credentials are missing or invalid` despite providing the correct Key ID and Issuer ID.
**Root Causes & Fixes**:
1. **Missing Flag**: Ensure you are using `--api-key-file` to explicitly point to the `.p8` file. Passing the path as a positional argument often fails.
2. **Insufficient Role**: The API Key must be created with the **App Manager** or **Admin** role in App Store Connect ($\rightarrow$ Users and Access $\rightarrow$ Integrations). "Developer" role is often insufficient for uploads.
3. **Issuer ID Mismatch**: Verify the Issuer ID exactly matches the one provided in the App Store Connect API page (it is a UUID).
4. **Key File Corruption**: Ensure the `.p8` file contains the full `[REDACTED PRIVATE KEY BLOCK]` block.



### The "Passcode Protected" Block
**Symptom**: `xcodebuild` fails with `The device is passcode protected` or `Failed to prepare the device for development` (Error Code -402653158).
**Root Cause**: The iOS device is locked. Xcode cannot mount the Developer Disk Image or push the binary while the screen is locked.
**Fix**:
- The user MUST unlock the device and be on the home screen.
- If automating via script, implement a retry loop (e.g., cron) to attempt the build periodically until the device is unlocked and becomes available.

### Automated Device Deployment (Watchdog Pattern)
To deploy to a physical device without manual intervention for every single run:
1. Use `xcrun xctrace list devices` and `sed` to isolate the `DEVICE_ID`.
2. Construct the destination flag as `-destination "id=<DEVICE_ID>"`.
3. Wrap the `xcodebuild` command in a bash script and schedule via `crontab` to handle intermittent "Device Offline" or "Passcode Protected" states.

**Symptom**: `xcodebuild` fails with `No signing certificate "iOS Development" found` or `No private key was found`, even when "Automatic Signing" is enabled.
**Root Cause**: The `.xcodeproj` specifies a Team ID, but the private key required to sign the app was not backed up/restored to the local macOS Keychain.
**Fix**:
- **Cannot be fixed via CLI**. The user MUST open the project in the Xcode GUI.
- Navigate to: `Project` $\rightarrow$ `Target` $\rightarrow$ `Signing & Capabilities`.
- Toggle "Automatically manage signing" off and on, or click the "Fix Issue" button provided by Xcode. This forces Xcode to communicate with Apple's servers and generate a new private key in the local Keychain.

### Destination Ambiguity
**Symptom**: `xcodebuild` warns about "multiple matching destinations."
**Fix**: Always specify `-destination 'generic/platform=iOS'` for archives to avoid the tool attempting to build for a specific connected simulator.

### The "No profiles found" Export Failure
**Symptom**: `xcodebuild -exportArchive` fails with `error: exportArchive No profiles for '<TargetName>' were found`, despite `signingStyle: automatic` and `teamID` being set.
**Root Cause**: The CLI tool fails to automatically resolve the provisioning profile. This is common with non-standard bundle identifiers (e.g., `BeMoreAgent` instead of `com.prismtek.bemore`) or when the tool cannot correlate the target name with a local `.mobileprovision` file.
**Fix**:
1. **Confirm Bundle ID**: Verify the `CFBundleIdentifier` in the archived `.app`'s `Info.plist` using `plutil -p` to ensure the target name in the plist matches the app's actual identifier.
2. **Identify the correct UUID**: Find the actual UUID of the profile on disk using `security cms -D -i <profile_path>`.
3. **Explicitly map the UUID**: In the `exportOptions.plist`, map the target name (exactly as it appears in the error) to the **UUID string**, not the profile name.
```xml
<key>provisioningProfiles</key>
<dict>
  <key>BeMoreAgent</key>
  <string>233e413d-cec0-4094-92b6-571ff77ee4d0</string>
</dict>
```
4. **Force Updates**: Use the `-allowProvisioningUpdates` flag with `xcodebuild` to force a refresh of the local profile cache from the Apple Developer portal.

### Xcode Project State Loss
**Symptom**: Xcode GUI prompts to "Perform Changes" to project settings but warns of uncommitted work.
**Fix**: Since `.xcodeproj` files are often ignored by Git (especially in `xcodegen` projects), standard Git commits may not save them. Perform a manual file-system backup of `project.pbxproj` before allowing Xcode to perform automated updates:
```bash
cp path/to/project.pbxproj path/to/project.pbxproj.bak
```

### Distribution via Xcode Cloud (Preferred)
When local hardware (e.g., 8GB RAM Macs) becomes a bottleneck for build times or signing certificates are missing from the local keychain, delegate the CI/CD pipeline to **Xcode Cloud**.
- **Trigger**: Push to a tracked branch (e.g., `fix/symphony-readiness`).
- **Benefit**: Bypasses local CPU/RAM limits and "Restored Mac" signing traps.
- **Verification**: Monitor via App Store Connect / TestFlight "Processing" status.

### Local On-Device Verification
For rapid iterative testing before a full Cloud build:
- Plug in the physical device.
- Use `xcodebuild` to deploy the current scheme directly to the device.
- Verify LLM connectivity by checking that the app is pointing to the correct Sovereign Cloud IP gateway.

### Bundle ID Migration & Naming
When rebranding or correcting a Bundle Identifier (e.g., moving to `com.prismtek.buddy`):
1. **Naming Convention**: Always use **Explicit** IDs in the format `com.[company].[product]`. Avoid `dev.` prefixes as they can clash with some Apple service expectations. **Wildcards are insufficient for TestFlight.**
2. **Surgical Patching**: Update the identifier in:
   - `project.pbxproj` (all targets)
   - `exportOptions.plist`
3. **Capabilities Set (Sovereign Cloud)**: When registering the ID, ensure the following are enabled for full agentic power:
   - **Push Notifications** (Real-time alerts)
   - **iCloud** (Cross-device state)
   - **Associated Domains** (Universal Links to Sovereign Cloud)
   - **Background Modes** (Remote notifications, Background fetch, Background processing)
4. **Sovereign Deployment Workflow**: Transition from local Mac builds to a hybrid "Power/Edge" model:
   - **Power (VPS)**: Host the "Brain" (Postgres, Compute) on a VPS.
   - **Edge (Cloudflare)**: Route professional domains (e.g., `prismtek.dev`) to the VPS gateway.
   - **CI/CD**: Use Xcode Cloud to bypass local resource constraints (RAM/CPU).
   - `project.pbxproj`: Search and replace all instances of `PRODUCT_BUNDLE_IDENTIFIER`.
   - `exportOptions.plist`: Update the key in the `provisioningProfiles` dictionary to match the new Bundle ID.
3. **Portal Synchronization**:
   - Create a new **Explicit App ID** in the Developer Portal.
   - Generate a new **Provisioning Profile** for the new ID.
   - **Critical**: Create a **new App record** in App Store Connect; you cannot change the bundle ID of an existing app record.

### Essential Capabilities for Agentic Apps
To maximize the power of an AI-driven iOS/macOS app, enable the following in the App ID configuration:
- **Push Notifications**: For asynchronous agent alerts and status updates.
- **Associated Domains**: To enable Universal Links (e.g., `prismtek.dev` $\rightarrow$ App).
- **iCloud**: For cross-device state synchronization.
- **App Groups**: For communication between the main app and any extensions/bridges.
- **Background Modes**:
  - `Remote notifications` (for silent updates).
  - `Background fetch` (for periodic state sync).
  - `Background processing` (for heavy agentic tasks).


## Verification
- Verify the `.xcarchive` exists at the specified path.
- Verify the `.ipa` is produced in the export directory.
- Check App Store Connect / TestFlight to ensure the build is "Processing."

## Linked Resources
- `references/signing-pitfalls.md`: Detailed guide on certificate and keychain recovery.
- `templates/export-options.plist`: Standard boilerplate for TestFlight exports.
