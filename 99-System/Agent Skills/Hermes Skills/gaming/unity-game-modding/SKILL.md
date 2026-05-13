---
name: unity-game-modding
description: Framework for reverse-engineering, patching, and modding Unity-based games on macOS/Windows.
---

# Unity Game Modding Framework

This skill provides a structured workflow for analyzing and modifying Unity games, focusing on C# injection and runtime patching.

## 🛠 The Modding Stack

### 1. Execution & Environment
- **CrossOver/Wine (macOS)**: Used to run Windows Unity games. Ensure the bottle is configured for the correct Windows version (usually Win 10).
- **BepInEx**: The industry-standard modding framework for Unity. It handles the loading of custom DLLs into the game process.
- **Harmony**: A powerful library used by BepInEx to "patch" existing game methods at runtime without modifying the original binary on disk.

### 2. Analysis & Reverse Engineering
- **UnityExplorer**: An in-game GUI tool that allows you to browse the Scene hierarchy, inspect GameObjects, and modify component values in real-time. **Essential for mapping class names to game objects.**
- **dnSpy / ILSpy**: Decompilers used to read the `Assembly-CSharp.dll` (the heart of the game's logic).
- **Cpp2IL / Il2CppInspector**: Required for games using the **IL2CPP** backend (where C# is converted to C++). These tools reconstruct the method signatures.

## 🔄 Workflow: From Idea to Mod

### Step 1: Backend Identification
Determine if the game is **Mono** or **IL2CPP**.
- **Mono**: Look for `Managed/Assembly-CSharp.dll`. (Easy to mod).
- **IL2CPP**: Look for `GameAssembly.dll` and `global-metadata.dat`. (Harder to mod).

### Step 2: Logic Mapping
1. Launch the game with **UnityExplorer**.
2. Find the object you want to change (e.g., "PlayerController").
3. Note the exact class name and the methods being called.
4. Open `Assembly-CSharp.dll` in **dnSpy** and find that class/method to understand the logic.

### Step 3: Writing the Patch (Harmony)
Use Harmony to "Prefix" (run before) or "Postfix" (run after) a game method.

**Example Pattern (C#):**
```csharp
[HarmonyPatch(typeof(PlayerController), "Update")]
class PlayerSpeedPatch {
    static void Postfix(ref float ___moveSpeed) {
        ___moveSpeed = 50.0f; // Override speed to be insane
    }
}
```

### Step 4: Deployment
1. Compile the patch into a `.dll`.
2. Drop the `.dll` into `BepInEx/plugins`.
3. Launch game and verify via BepInEx console.

## ⚠️ Pitfalls & Troubleshooting

| Issue | Cause | Solution |
|-----------|------------|----------|
| Game crashes on launch | Incompatible BepInEx version | Match BepInEx version to Unity version (check `version.txt` or logs) |
| Patch not applying | Method signature mismatch | Use Harmony's `Transpiler` for complex changes or verify method name exactly |
| "Access Denied" on DLLs | macOS Permissions/SIP | Move game folder to a non-system directory or use `chmod` |
| IL2CPP method not found | Metadata stripped | Use `Il2CppInspector` to generate a C# dummy project for referencing |
| Steam Unity game crashes/exits when launched directly in Wine | Game expects Steam client/API context | Launch through Wine Steam with `steam.exe -applaunch <appid>`; verify Steam auth logs before blaming renderer or mods. |
| DXVK fails on Intel Iris/MoltenVK | GPU/driver missing Vulkan features such as `geometryShader` | Disable/rename local DXVK DLLs and try WineD3D/OpenGL fallback; do not assume DXVK is always better on Intel Macs. |
| Standalone Wine prefix shows black Steam/game containers but CrossOver works | CrossOver bottle has a working Steam auth/session/runtime stack that plain Wine did not reproduce | Prefer reusing the working CrossOver bottle with `cxstart` from CLI/no GUI before trying to rebuild the bottle from scratch. Verify via Steam `gameprocess_log.txt` and Unity `Player.log`. |

## 📚 References
- `references/everything-is-crab.md`: Specific roadmap and compatibility notes for EIC, including CrossOver-bottle CLI launch receipts, standalone Wine/Steam failures, and Intel Iris renderer pitfalls.
