#!/usr/bin/env python3
"""
Prepares the Smart Pen Rev G Final Digital Delivery Package v1.2.
- Preserves v1.0 and v1.1 intact.
- Removes any residual machine-specific *.kicad_prl files.
- Synchronizes mechanical STEP, STL, drawings, CAD sources, BOMs, and CPLs.
- Includes synchronized 19_LiPo_Battery_LP300830_PCM.step.
- Packages SmartPen_RevG_Final_Digital_Delivery_Package_v1.2.zip.
- Validates ZIP archive integrity via zipfile.testzip().
- Computes SHA-256 hashes directly from the uncompressed byte stream inside the ZIP.
- Generates SHA256_FINAL_DELIVERY_MANIFEST.txt and compares v1.1 vs v1.2.
"""

import os
import shutil
import zipfile
import hashlib
from pathlib import Path

def prepare_v1_2():
    base_dir = Path("output/RevG/Final_Client_Delivery")
    if not base_dir.exists():
        raise FileNotFoundError(f"Delivery base directory not found: {base_dir}")

    print("=== Step 1: Removing Machine-Specific *.kicad_prl Files ===")
    prl_files = list(base_dir.rglob("*.kicad_prl"))
    for prl in prl_files:
        print(f"  Removing: {prl.relative_to(base_dir)}")
        prl.unlink()
    print(f"Removed {len(prl_files)} *.kicad_prl files.")

    print("\n=== Step 2: Synchronizing Mechanical CAD Deliverables ===")
    cad_src = Path("output/RevG/Mechanical_Phase04C")
    
    # 1. Sync CAD Python script
    dest_cad_src = base_dir / "05_Mechanical_CAD_Source"
    dest_cad_src.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cad_src / "CAD_Source" / "SmartPen_Parametric_CAD_RevG_Phase4C.py", dest_cad_src)
    print("  Synchronized 05_Mechanical_CAD_Source")

    # 2. Sync 27 component STEP files + 2 assemblies
    dest_step = base_dir / "06_Mechanical_STEP_Assemblies"
    dest_step.mkdir(parents=True, exist_ok=True)
    
    # Remove any obsolete LP380830 files
    for old_file in [
        dest_step / "19_LiPo_Battery_LP380830.step",
        dest_step / "Parts" / "19_LiPo_Battery_LP380830.step"
    ]:
        if old_file.exists():
            old_file.unlink()
            print(f"  Removed obsolete: {old_file.name}")

    for f in (cad_src / "STEP").glob("*.step"):
        shutil.copy2(f, dest_step)
        if (dest_step / "Parts").exists():
            shutil.copy2(f, dest_step / "Parts")
    for f in (cad_src / "Assemblies").glob("*.step"):
        shutil.copy2(f, dest_step)
    print(f"  Synchronized 06_Mechanical_STEP_Assemblies ({len(list(dest_step.glob('*.step')))} files in root)")

    # 3. Sync 16 STLs
    dest_stl = base_dir / "07_Mechanical_Printable_STL"
    dest_stl.mkdir(parents=True, exist_ok=True)
    for f in (cad_src / "STL").glob("*.stl"):
        shutil.copy2(f, dest_stl)
    print(f"  Synchronized 07_Mechanical_Printable_STL ({len(list(dest_stl.glob('*.stl')))} files)")

    # 4. Sync Drawings
    dest_draw = base_dir / "08_Mechanical_Drawings_and_Visuals"
    dest_draw.mkdir(parents=True, exist_ok=True)
    for f in (cad_src / "Drawings").glob("*.*"):
        shutil.copy2(f, dest_draw)
    print(f"  Synchronized 08_Mechanical_Drawings_and_Visuals ({len(list(dest_draw.glob('*.*')))} files)")

    print("\n=== Step 3: Updating Delivery README.md ===")
    readme_path = base_dir / "README.md"
    readme_content = """# Smart Pen Rev G — Final Digital Delivery Package (Release v1.2)

**Product:** Smart Pen Rev G (Production-Optimized Architecture)  
**Release Version:** v1.2  
**Release Date:** November 17, 2026  
**Repository Branch:** `engineering/revg-production`  
**License / Proprietary Notice:** Confidential & Proprietary — Prepared for Client Delivery  

---

## 1. Scope of Digital Delivery Package

This release archive contains the complete digital engineering deliverables for the Smart Pen Rev G:
- **01_KiCad_Design_Source:** Complete native KiCad design trees for all four boards (FourLayer_ECR_R9_50mA Main Board, Front_MPU, MicroSD_Carrier, and Touch_Sensor) with embedded footprint libraries. All machine-specific `*.kicad_prl` files have been excluded.
- **02_Fabrication_Gerber_Drill:** Production Gerber files (RS-274X) and Excellon drill files for all four boards with unified coordinate origins and validated drill tables.
- **03_BOM_and_CPL:** Standardized Bill of Materials with genuine manufacturer names, verified orderable MPNs, IPC package sizes, and automated Pick-and-Place (CPL) centroid files. Includes Consolidated System BOM.
- **04_Drawings_Schematics_Assembly:** Vector schematic and PCBA assembly drawings in PDF and SVG formats.
- **05_Mechanical_CAD_Source:** Complete parametric Python CAD construction scripts (`SmartPen_Parametric_CAD_RevG_Phase4C.py`).
- **06_Mechanical_STEP_Assemblies:** 27 individual AP214 BRep component models (including `19_LiPo_Battery_LP300830_PCM.step`), Master Assembly STEP, and Exploded Assembly STEP.
- **07_Mechanical_Printable_STL:** 16 watertight 2-manifold STL models ready for high-resolution stereolithography (SLA) printing.
- **08_Mechanical_Drawings_and_Visuals:** Technical orthographic drawings, section views, click kinematics charts, and assembly visual references.
- **09_Assembly_Instructions:** Comprehensive step-by-step mechanical and electrical integration manual.
- **10_Engineering_Verification_Reports:** Electrical, RF power profiling, ground plane, thermal, and mechanical collision reports.
- **11_Manufacturing_Notes:** PCBA fabrication tolerances, surface finish (ENIG), copper weight, stackup, and test point specs.
- **12_Prototype_Validation_and_Limitations:** Engineering evaluation guidelines and prototype boundary notes.

---

## 2. Key Architecture & Physical Specifications

- **Enclosure Envelope:** Overall Length: 153.5 mm (within mandatory 150–155 mm span); Barrel Outer Diameter: 15.5 mm (within mandatory 15–16 mm span).
- **Main Board Form Factor:** 84.0 × 9.2 × 1.6 mm (4-Layer JLC04161H-7628 stackup, 1.0 oz copper, ENIG finish).
- **Battery Architecture:** Removable below-rail conformal cradle with positive mechanical clearances.
  - **Selected Commercial Cell:** Model `LP300830-PCM` (50 mAh nominal, 3.7 V LiPo).
  - **Maximum Finished Pack Envelope:** 33.00 mm (L) × 8.20 mm (W) × 3.30 mm (T) with integrated PCM and silicone leads.
  - **Cradle Cavity:** 34.00 mm (L) × 8.40 mm (W) × 3.50 mm (T) (+0.20 mm thickness, +0.20 mm width, +1.00 mm length clearance).
  - **Bore Clearance:** +0.437 mm corner clearance to barrel inner bore; +0.25 mm clearance to moving pushrod tunnel.
- **Charging & Headroom:**
  - $R_9 = 20.0\\text{ k}\\Omega \\implies 50.0\\text{ mA}$ charge current (1.0C rating).
  - MCP73831 thermal dissipation $P_D \\le 82.5\\text{ mW}$, $\\Delta T \\le 19.0^\\circ\\text{C}$.
  - AP2112K-3.3 regulator provides positive voltage margin above ESP32-C3 brownout threshold.
  - Power path P-FET $Q_2$ turns firmly OFF when USB is attached, isolating battery.

---

## 3. Package Checksums & Integrity

All files in this archive have been cryptographically hashed (SHA-256) directly from the uncompressed byte streams inside the archive. Refer to `SHA256_FINAL_DELIVERY_MANIFEST.txt` for the authoritative checksums.
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("  Updated README.md for Release v1.2")

    print("\n=== Step 4: Building Delivery ZIP v1.2 ===")
    zip_dest = Path("output/RevG/SmartPen_RevG_Final_Digital_Delivery_Package_v1.2.zip")
    
    # Collect all files to include (excluding SHA256 manifest which will be computed from the zip)
    all_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            p = Path(root) / f
            if p.name == "SHA256_FINAL_DELIVERY_MANIFEST.txt":
                continue
            all_files.append(p)
    all_files.sort(key=lambda p: str(p.relative_to(base_dir)).replace("\\", "/"))

    print(f"  Packaging {len(all_files)} files into {zip_dest.name}...")
    with zipfile.ZipFile(zip_dest, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in all_files:
            rel = p.relative_to(base_dir)
            arcname = str(rel).replace("\\", "/")
            zf.write(p, arcname=arcname)

    print(f"  Package created: {zip_dest.name} ({zip_dest.stat().st_size:,} bytes)")

    print("\n=== Step 5: Testing ZIP Archive Integrity ===")
    with zipfile.ZipFile(zip_dest, 'r') as zf:
        bad_file = zf.testzip()
        if bad_file is not None:
            raise RuntimeError(f"Corrupted file found in ZIP archive: {bad_file}")
        print("  ZIP Integrity Check: PASSED (zipfile.testzip() returned 0 corrupted files)")

    print("\n=== Step 6: Generating Cryptographic SHA-256 Manifest ===")
    manifest_lines = []
    manifest_lines.append("# SMART PEN REV G — FINAL DIGITAL DELIVERY PACKAGE v1.2 SHA-256 MANIFEST")
    manifest_lines.append("# Archive: SmartPen_RevG_Final_Digital_Delivery_Package_v1.2.zip")
    manifest_lines.append("# Generated directly from uncompressed byte streams inside the delivery archive")
    manifest_lines.append(f"# Date: 2026-11-17T20:30:00+05:30")
    manifest_lines.append(f"# Total Files: {len(all_files)}")
    manifest_lines.append("# " + "=" * 80)
    manifest_lines.append(f"{'SHA-256 Hash':<64}  {'Size (bytes)':<12}  {'Archive Path'}")
    manifest_lines.append("# " + "-" * 80)

    with zipfile.ZipFile(zip_dest, 'r') as zf:
        namelist = sorted(zf.namelist())
        for name in namelist:
            data = zf.read(name)
            sha256 = hashlib.sha256(data).hexdigest()
            size = len(data)
            manifest_lines.append(f"{sha256}  {size:<12}  {name}")

    manifest_content = "\n".join(manifest_lines) + "\n"
    
    # Save manifest both in the delivery folder and outside
    manifest_path = base_dir / "SHA256_FINAL_DELIVERY_MANIFEST.txt"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"  Wrote delivery manifest: {manifest_path} ({len(namelist)} verified files)")

    # Also append the manifest file into the ZIP archive so the ZIP is self-contained
    with zipfile.ZipFile(zip_dest, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(manifest_path, arcname="SHA256_FINAL_DELIVERY_MANIFEST.txt")
    print(f"  Appended self-contained manifest into {zip_dest.name} (Final size: {zip_dest.stat().st_size:,} bytes)")

    # Re-verify testzip
    with zipfile.ZipFile(zip_dest, 'r') as zf:
        assert zf.testzip() is None
        total_in_zip = len(zf.namelist())
        print(f"  Final ZIP total files: {total_in_zip}")

    print("\n=== Step 7: Comparison v1.1 vs v1.2 ===")
    v1_1_path = Path("output/RevG/SmartPen_RevG_Final_Digital_Delivery_Package_v1.1.zip")
    with zipfile.ZipFile(v1_1_path, 'r') as zf1:
        names_v1_1 = set(zf1.namelist())
    with zipfile.ZipFile(zip_dest, 'r') as zf2:
        names_v1_2 = set(zf2.namelist())

    removed = names_v1_1 - names_v1_2
    added = names_v1_2 - names_v1_1

    print(f"  v1.1 Total Files: {len(names_v1_1)}")
    print(f"  v1.2 Total Files: {len(names_v1_2)}")
    print(f"  Removed Files ({len(removed)}):")
    for r in sorted(removed):
        print(f"    - {r}")
    print(f"  Added Files ({len(added)}):")
    for a in sorted(added):
        print(f"    + {a}")

if __name__ == "__main__":
    prepare_v1_2()
