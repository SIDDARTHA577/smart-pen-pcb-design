# STEP CAD KERNEL IMPORT EVIDENCE & EXECUTION LOG

**Document ID:** SRG-P4C-FBC-001  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Scope:** Real CAD Kernel Import & Geometry Validation Investigation (Task 1)  
**Status:** **GATE FORMALLY MARKED BLOCKED (RETAINING USABLE STLs & VALID AP214 STEPs)**

---

## 1. INVESTIGATIVE PROTOCOL & MANDATE

Task 1 mandates:
> *"The existing 29 STEP files now have zero reported duplicate entity IDs. However, actual OpenCascade import and geometry validation remain blocked. Identify a permitted solution using: Official FreeCAD installation, or a controlled, reproducible CAD CI environment. Use a real CAD kernel to re-import all parts, verify closed solids, validate topology, compare against source, and store actual CAD application logs. Do not claim success from custom text parsing alone. If CAD execution remains unavailable, mark the STEP gate BLOCKED and retain the usable STL/source files."*

Furthermore, the mission constraints explicitly state:
> *"Do not bypass Windows Defender Application Control or any security restrictions."*

This document provides the exhaustive technical log of all CAD kernel execution attempts on this host system.

---

## 2. HOST SYSTEM CAD TOOL AUDIT & RESULTS

### 2.1 FreeCAD Availability Check
An automated search was executed across system PATH and default installation directories:
```powershell
Get-Command freecad*, FreeCADCmd* -ErrorAction SilentlyContinue
Get-ChildItem -Path "C:\Program Files", "C:\Program Files (x86)", "C:\Users\goran\AppData\Local\Programs" -Filter "*FreeCAD*" -Recurse -Depth 2
```
**Result:** No FreeCAD or FreeCADCmd binaries exist on the host system.

### 2.2 Package Manager Installation Attempt
Attempted to query and install FreeCAD via Windows Package Manager (`winget`):
```powershell
winget search FreeCAD
```
**Result:**
```
Program 'winget.exe' failed to run: The file cannot be accessed by the system.
NativeCommandFailed: ResourceUnavailable
```
On this enterprise-managed Windows installation, UWP App execution aliases and package manager installs are restricted by group security policies.

### 2.3 Python OpenCASCADE / OCP Execution Attempt
Attempted to load the OpenCASCADE Python wrapper (`OCP` / `cadquery` / `build123d`):
```powershell
python -c "import OCP"
```
**Result:**
```
ImportError: DLL load failed while importing OCP: An Application Control policy has blocked this file.
```
**Root Cause:** Windows Defender Application Control (WDAC) or Smart App Control strictly blocks unsigned or non-whitelisted third-party `.pyd` dynamic libraries located in user directories (`AppData\Local\Programs\Python`). In compliance with instructions, no attempt was made to bypass or disable WDAC.

### 2.4 KiCad 10.0 Native OpenCASCADE Wrapper Audit
KiCad 10.0 contains officially Microsoft-signed OpenCASCADE 7.9 libraries (`TKSTEP.dll`, `TKMesh.dll`, etc.) and a bundled Python 3.11 environment.
Setting `$env:PATH` to KiCad's bin directory successfully loads `pcbnew`:
```powershell
$env:PATH = "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin;" + $env:PATH
& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\python.exe" -c "import pcbnew; print(pcbnew.GetBuildVersion())"
# Output: 10.0.7
```
However, invoking the SWIG wrapper `pcbnew.UTILS_STEP_MODEL().LoadSTEP()`:
```python
import pcbnew

sm = pcbnew.UTILS_STEP_MODEL()
sm.LoadSTEP('19_LiPo_Battery_LP380830.step')
```
**Result:** Process exited with return code 1 without error output.  
**Analysis:** KiCad's internal `UTILS_STEP_MODEL` class is tightly coupled to KiCad's wxWidgets `Pgm()` / `EDA_BASE_FRAME` application context. Calling its C++ methods outside a running KiCad GUI application frame throws an unhandled GUI assertion that terminates the process.

---

## 3. FORMAL TASK 1 GATE EVALUATION

Because:
1. FreeCAD is not installed on this host,
2. Third-party OCP binaries are restricted by host WDAC security policies, and
3. KiCad's CLI does not expose an arbitrary solid-modeling STEP validation engine for mechanical housings,

We follow the explicit directive of Task 1:
> *"If CAD execution remains unavailable, mark the STEP gate BLOCKED and retain the usable STL/source files. Do not claim success from custom text parsing alone."*

**Gate Status: BLOCKED.**  
We do not certify native OpenCASCADE import from custom parsing scripts alone.

---

## 4. STATUS OF RETAINED DELIVERABLES

All generated mechanical files in `output/RevG/Mechanical_Phase04C/` are preserved intact and ready for ingestion on a compliant CAD station or CI runner:

| Asset Directory | File Count | Format & Specification | Quality Status |
| :--- | :---: | :--- | :--- |
| `output/RevG/Mechanical_Phase04C/STL/` | 16 | Binary STL, Watertight 2-Manifold Solids | **100% Watertight (`is_watertight = True`)** |
| `output/RevG/Mechanical_Phase04C/STEP/` | 27 | ISO-10303-21 AP214 BRep (`MANIFOLD_SOLID_BREP`) | **0 Duplicate IDs, 0 Broken References** |
| `output/RevG/Mechanical_Phase04C/Assemblies/` | 2 | Master & Exploded Assemblies (STEP AP214) | **0 Duplicate IDs, 0 Broken References** |
| `output/RevG/Mechanical_Phase04C/Drawings/` | 6 | High-Resolution SVG and PNG Orthographic Drawings | **Complete Dimensioned Views** |
| `output/RevG/Mechanical_Phase04C/CAD_Source/` | 1 | Parametric Solid Generation Script | **Reproducible Python Solid Engine** |

---

## 5. RECOMMENDED CI UNBLOCKING PATH FOR PHASE 5

To achieve automated native OpenCASCADE validation during Phase 5:
1. **GitHub Actions CI Runner:** Configure a Linux runner (`ubuntu-latest`) with `python-occ-core` or `freecad`:
   ```yaml
   - name: Validate STEP Geometry via FreeCAD
     run: |
       sudo apt-get install -y freecad-python3
       python3 scripts/validate_step_freecad.py output/RevG/Mechanical_Phase04C/STEP/*.step
   ```
2. **Workstation Whitelisting:** Request workstation administrator clearance to add an application control exception for OpenCASCADE / FreeCAD binaries.
