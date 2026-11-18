#!/usr/bin/env python3
"""
Prepares the Smart Pen Rev G Final Digital Delivery Package v1.3.
- Preserves v1.0 (7,311,129 bytes), v1.1 (8,604,846 bytes), and v1.2 (7,969,398 bytes) intact.
- Removes any residual machine-specific *.kicad_prl files.
- Synchronizes mechanical STEP (27 parts + 2 assemblies), STL (16 watertight meshes), drawings, CAD sources, BOMs, and CPLs.
- Includes updated technical documentation with 100 mW charger dissipation, D4 power-path / D3 flyback diode designators, and explicit hardware limitations.
- Packages SmartPen_RevG_Final_Digital_Delivery_Package_v1.3.zip.
- Validates ZIP archive integrity via zipfile.testzip().
- Computes SHA-256 hashes directly from the uncompressed byte stream inside the ZIP.
- Generates self-contained SHA256_FINAL_DELIVERY_MANIFEST.txt and embeds it into the archive.
"""

import os
import sys
import shutil
import zipfile
import hashlib
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent

def prepare_v1_3():
    base_dir = repo_root / "output" / "RevG" / "Final_Client_Delivery"
    if not base_dir.exists():
        raise FileNotFoundError(f"Delivery base directory not found: {base_dir}")

    print("=== Step 1: Removing Machine-Specific *.kicad_prl Files ===")
    prl_files = list(base_dir.rglob("*.kicad_prl"))
    for prl in prl_files:
        print(f"  Removing: {prl.relative_to(base_dir)}")
        prl.unlink()
    print(f"Removed {len(prl_files)} *.kicad_prl files.")

    print("\n=== Step 2: Synchronizing Mechanical CAD Deliverables from Verified Mechanical_Phase04C ===")
    cad_src = repo_root / "output" / "RevG" / "Mechanical_Phase04C"
    
    # 1. Sync CAD Python script
    dest_cad_src = base_dir / "05_Mechanical_CAD_Source"
    dest_cad_src.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cad_src / "CAD_Source" / "SmartPen_Parametric_CAD_RevG_Phase4C.py", dest_cad_src)
    print("  Synchronized 05_Mechanical_CAD_Source")

    # 2. Sync 27 component STEP files + 2 assemblies
    dest_step = base_dir / "06_Mechanical_STEP_Assemblies"
    dest_step.mkdir(parents=True, exist_ok=True)
    
    # Remove any obsolete LP380830 files if present
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

    print("\n=== Step 3: Building Delivery ZIP v1.3 ===")
    zip_dest = repo_root / "output" / "RevG" / "SmartPen_RevG_Final_Digital_Delivery_Package_v1.3.zip"
    
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

    print("\n=== Step 4: Testing ZIP Archive Integrity ===")
    with zipfile.ZipFile(zip_dest, 'r') as zf:
        bad_file = zf.testzip()
        if bad_file is not None:
            raise RuntimeError(f"Corrupted file found in ZIP archive: {bad_file}")
        print("  ZIP Integrity Check: PASSED (zipfile.testzip() returned 0 corrupted files)")

    print("\n=== Step 5: Generating Cryptographic SHA-256 Manifest ===")
    manifest_lines = []
    manifest_lines.append("# SMART PEN REV G — FINAL DIGITAL DELIVERY PACKAGE v1.3 SHA-256 MANIFEST")
    manifest_lines.append("# Archive: SmartPen_RevG_Final_Digital_Delivery_Package_v1.3.zip")
    manifest_lines.append("# Generated directly from uncompressed byte streams inside the delivery archive")
    manifest_lines.append("# Date: 2026-11-18T07:45:00+05:30")
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
    
    # Save manifest in delivery folder
    manifest_path = base_dir / "SHA256_FINAL_DELIVERY_MANIFEST.txt"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"  Wrote delivery manifest: {manifest_path} ({len(namelist)} verified files)")

    # Append self-contained manifest into the ZIP archive
    with zipfile.ZipFile(zip_dest, 'a', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(manifest_path, arcname="SHA256_FINAL_DELIVERY_MANIFEST.txt")
    print(f"  Appended self-contained manifest into {zip_dest.name} (Final size: {zip_dest.stat().st_size:,} bytes)")

    # Re-verify testzip
    with zipfile.ZipFile(zip_dest, 'r') as zf:
        assert zf.testzip() is None
        total_in_zip = len(zf.namelist())
        print(f"  Final ZIP total files: {total_in_zip}")

    print("\n=== Step 6: Independent Verification of All Archive Entries ===")
    with zipfile.ZipFile(zip_dest, 'r') as zf:
        namelist = zf.namelist()
        manifest_data = zf.read("SHA256_FINAL_DELIVERY_MANIFEST.txt").decode('utf-8')
        m_hashes = {}
        for line in manifest_data.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "SHA-256 Hash" in line:
                continue
            parts = line.split(maxsplit=2)
            if len(parts) == 3:
                h, sz, path = parts
                m_hashes[path] = (h, int(sz))

        verified = 0
        for name in namelist:
            if name == "SHA256_FINAL_DELIVERY_MANIFEST.txt":
                continue
            if name not in m_hashes:
                raise ValueError(f"File {name} not found in manifest!")
            data = zf.read(name)
            computed_h = hashlib.sha256(data).hexdigest()
            expected_h, expected_sz = m_hashes[name]
            if computed_h != expected_h:
                raise ValueError(f"Hash mismatch on {name}")
            if len(data) != expected_sz:
                raise ValueError(f"Size mismatch on {name}")
            verified += 1
        print(f"  Successfully verified {verified} files against embedded SHA-256 manifest (0 errors)!")

if __name__ == "__main__":
    prepare_v1_3()
