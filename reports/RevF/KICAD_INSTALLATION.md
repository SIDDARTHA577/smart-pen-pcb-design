# KiCad Automated Installation & Verification Record

**Tool:** KiCad EDA Suite  
**Method:** Windows Package Manager (`winget`)  
**Package Identifier:** `KiCad.KiCad`  
**Installed Version:** KiCad 10.0.7 (x86_64)  
**Install Date:** November 2026  
**Host Platform:** Windows 10/11 x64  
**Binary Location:** `C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe`  

---

## 1. Installation Command & Output Log

```powershell
winget install --id KiCad.KiCad --exact --source winget --accept-package-agreements --accept-source-agreements --silent
```

### Installation Log Trace:
```
Found KiCad [KiCad.KiCad] Version 10.0.7
This application is licensed to you by its owner.
Microsoft is not responsible for, nor does it grant any licenses to, third-party packages.
Downloading https://github.com/KiCad/kicad-source-mirror/releases/download/10.0.7/kicad-10.0.7-x86_64.exe
Successfully verified installer hash
Starting package install...
Successfully installed
```

---

## 2. Binary Verification & Version Check

```powershell
& "$env:LOCALAPPDATA\Programs\KiCad\10.0\bin\kicad-cli.exe" version
```

### Output:
```
10.0.7
```
**Exit Code:** 0 (SUCCESS)

---

## 3. Available Subcommands

`kicad-cli` version 10.0.7 supports all automated engineering verification interfaces:
- `kicad-cli sch erc`: Native Electrical Rules Check on schematic files (`.kicad_sch`).
- `kicad-cli pcb drc`: Native Design Rules Check on PCB layouts (`.kicad_pcb`).
- `kicad-cli pcb export gerbers`: Automated RS-274X Gerber file generation.
- `kicad-cli pcb export drill`: Automated Excellon drill file generation.
- `kicad-cli pcb export step`: Native 3D STEP solid model generation.
- `kicad-cli sch export pdf`: Production schematic vector PDF export.

---

## 4. Verification Gate Status

- [x] Official KiCad installed via authorized package manager
- [x] `kicad-cli.exe` located and executable
- [x] Verified version returns `10.0.7` with exit code 0
- [x] Environment configured for automated ERC, DRC, and manufacturing exports
