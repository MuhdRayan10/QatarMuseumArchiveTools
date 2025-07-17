# FFmpeg + REDCINE‑X PRO / REDline – Windows Installation Guide

> Follow the steps below in an **elevated PowerShell window** to install FFmpeg, REDCINE‑X PRO, and expose both `ffmpeg` and `redline` on your command‑line PATH.

---

## Rough Steps

1. **Open PowerShell as Administrator**
   \*Press **Win ⇒ type “powershell” ⇒ right‑click →* **Run as administrator***.

2. **Locate the directory that contains `windows.ps1`**

   ```powershell
   cd "C:\Path\To\Your\Script"
   ```

3. **Allow local scripts to run**

   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   When prompted, type **A** and press **Enter**.

4. **Execute the installer script**

   ```powershell
   .\windows.ps1
   ```

5. **Open a *new* terminal session and verify**

   ```powershell
   ffmpeg -version
   redline --help
   ```

   Both commands should print their version/usage banners.

---

## What the script does

| Component                   | Action                                                                                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FFmpeg**                  | Downloads the latest *release‑essentials* build from Gyan.dev (unless already present), extracts it to `C:\Tools\ffmpeg`, and adds `…\bin` to the machine‑wide **PATH**.  |
| **REDCINE‑X PRO / REDline** | Downloads the v64.0.25 MSI, installs silently (skipped if already installed), ensures `REDline.exe`’s folder is on **PATH**, and copies/installs `libmmd.dll` if missing. |

---

## Troubleshooting

| Symptom                               | Fix                                                                                                                       |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **`ffmpeg`/`redline` not recognized** | Close all terminals (or reboot) so the new PATH is loaded.                                                                |
| **`libmmd.dll` missing**              | Re‑run `windows.ps1`; the script now copies or installs Intel’s runtime DLL automatically.                                |
| **“Unable to load clip” in REDline**  | Check you passed the *first* segment (usually `_001.R3D`), quote paths with spaces, and ensure the clip isn’t cloud‑only. |

---

## Uninstalling

* **FFmpeg** – delete `C:\Tools\ffmpeg` and remove its PATH entry (*System Properties → Environment Variables*).
* **REDCINE‑X PRO** – uninstall via *Settings → Apps → REDCINE‑X PRO 64‑bit* and delete the PATH entry if you no longer need `REDline.exe`.

---

*Document generated July 17 2025.*
