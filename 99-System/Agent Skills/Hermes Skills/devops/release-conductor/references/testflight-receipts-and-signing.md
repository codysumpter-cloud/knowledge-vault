# TestFlight receipts and signing blockers

Use this reference when auditing BeMore/Prismtek App Store Connect uploads from GitHub Actions.

## Do not equate upload success with tester availability

`xcodebuild -exportArchive` may finish with:

```text
Uploaded package is processing.
Upload succeeded.
Uploaded <AppName>
** EXPORT SUCCEEDED **
```

This is a valid upload receipt, but it is not proof the build is visible/usable in TestFlight. Treat it as **processing** until App Store Connect/TestFlight shows the build or the App Store Connect API confirms a non-invalid processing state for the exact platform/version/build.

Report as:

- Upload: succeeded
- Apple processing/TestFlight visibility: pending user/API confirmation
- Completion gate: open until build appears or an Apple-side blocker is identified

## Receipts to capture

- GitHub run URL and run id
- Job names and pass/fail status
- Commit SHA/message that triggered the run
- App platform, version, and build number
- Archive verification result, especially bundled model/resource checks
- Upload log lines showing `Upload succeeded` and `Uploaded package is processing`
- Any annotations (for example provisioning profile name drift)

## iOS bundled MLC model pitfall

XcodeGen resource folder references may not reliably place a large nested model directory into the archive in the expected path. If archive verification fails for a bundled MLC model such as:

```text
Products/Applications/<App>.app/BundledModels/<model>/mlc-chat-config.json
```

then add an explicit post-build copy script to copy `BundledModels` into `$TARGET_BUILD_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/BundledModels`, and verify the archive path before export/upload.

## macOS signing asset blocker pattern

If a macOS TestFlight workflow fails during archive with:

```text
Choose a certificate to revoke. Your account has reached the maximum number of certificates.
Signing certificate is invalid. Signing certificate "Apple Development: ..." is not valid for code signing.
```

then the upload pipeline is blocked before export. Audit local keychain with:

```bash
security find-identity -v -p codesigning
security find-certificate -a -p -c "Apple Development" login.keychain-db | openssl x509 -noout -subject -issuer -dates
```

If local keychain has a valid identity, refreshing GitHub secrets may require interactive macOS Keychain/SecurityAgent approval to export the private key. If Apple still reports maximum certificates after refreshing, revoke stale certs in Apple Developer or provide a valid distribution signing asset.
