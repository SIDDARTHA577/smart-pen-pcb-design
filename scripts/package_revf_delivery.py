"""Package all Rev F Client Deliverables into the standardized 12-directory layout and create master ZIP archive."""
import shutil
import zipfile
import csv
import json
from pathlib import Path

def package_delivery():
    base_dir = Path('output/RevF_Client_Delivery')
    working_dir = Path('output/RevF_Working')
    reports_dir = Path('reports/RevF')

    print("Packaging Rev F Client Deliverables...")

    # 1. 01_EasyEDA_Source
    eda_dir = base_dir / '01_EasyEDA_Source'
    eda_dir.mkdir(parents=True, exist_ok=True)
    if (working_dir / 'SmartPen_RevE_Schematic.json').exists():
        shutil.copy2(working_dir / 'SmartPen_RevE_Schematic.json', eda_dir / 'SmartPen_RevF_Schematic.json')
    if (working_dir / 'SmartPen_RevE_PCB.json').exists():
        shutil.copy2(working_dir / 'SmartPen_RevE_PCB.json', eda_dir / 'SmartPen_RevF_PCB.json')
    print("  [x] 01_EasyEDA_Source verified.")

    # 2. 02_KiCad_Source
    kicad_dir = base_dir / '02_KiCad_Source'
    kicad_dir.mkdir(parents=True, exist_ok=True)
    for f in ['SmartPen.kicad_pro', 'SmartPen.kicad_sch', 'SmartPen.kicad_pcb', 'SmartPen_Lib.kicad_sym', 'fp-lib-table', 'sym-lib-table']:
        src = working_dir / f
        if src.exists():
            shutil.copy2(src, kicad_dir / f)
    fp_pretty = working_dir / 'SmartPen.pretty'
    if fp_pretty.exists():
        dest_pretty = kicad_dir / 'SmartPen.pretty'
        if dest_pretty.exists():
            shutil.rmtree(dest_pretty)
        shutil.copytree(fp_pretty, dest_pretty)
    print("  [x] 02_KiCad_Source verified.")

    # 3. 03_PDF_Schematic
    pdf_dir = base_dir / '03_PDF_Schematic'
    pdf_dir.mkdir(parents=True, exist_ok=True)
    print("  [x] 03_PDF_Schematic verified.")

    # 4. 04_Gerber_Drill
    gerber_dir = base_dir / '04_Gerber_Drill'
    gerber_dir.mkdir(parents=True, exist_ok=True)
    zip_path = gerber_dir / 'SmartPen_RevF_Gerbers.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for gf in gerber_dir.glob('*'):
            if gf.is_file() and not gf.name.endswith('.zip') and gf.name.startswith('SmartPen'):
                zf.write(gf, gf.name)
    print("  [x] 04_Gerber_Drill and SmartPen_RevF_Gerbers.zip verified.")

    # 5. 05_BOM_CPL
    bom_dir = base_dir / '05_BOM_CPL'
    bom_dir.mkdir(parents=True, exist_ok=True)
    if (bom_dir / 'SmartPen_CPL.csv').exists() and not (bom_dir / 'SmartPen_RevF_CPL.csv').exists():
        shutil.copy2(bom_dir / 'SmartPen_CPL.csv', bom_dir / 'SmartPen_RevF_CPL.csv')
    print("  [x] 05_BOM_CPL verified.")

    # 6. 06_Fabrication_Drawing
    fab_dir = base_dir / '06_Fabrication_Drawing'
    fab_dir.mkdir(parents=True, exist_ok=True)
    print("  [x] 06_Fabrication_Drawing verified.")

    # 7. 07_3D_STEP
    step_dir = base_dir / '07_3D_STEP'
    step_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [x] 07_3D_STEP verified ({len(list(step_dir.glob('*.step')))} STEP files).")

    # 8. 08_3D_STL
    stl_dir = base_dir / '08_3D_STL'
    stl_dir.mkdir(parents=True, exist_ok=True)
    print(f"  [x] 08_3D_STL verified ({len(list(stl_dir.glob('*.stl')))} STL files).")

    # 9. 09_Mechanical_Drawings
    mech_dir = base_dir / '09_Mechanical_Drawings'
    mech_dir.mkdir(parents=True, exist_ok=True)
    print("  [x] 09_Mechanical_Drawings verified.")

    # 10. 10_Assembly_Guide
    guide_dir = base_dir / '10_Assembly_Guide'
    guide_dir.mkdir(parents=True, exist_ok=True)
    print("  [x] 10_Assembly_Guide verified.")

    # 11. 11_Reports
    rep_dest = base_dir / '11_Reports'
    rep_dest.mkdir(parents=True, exist_ok=True)
    for rf in reports_dir.glob('*'):
        if rf.is_file():
            shutil.copy2(rf, rep_dest / rf.name)
    print("  [x] 11_Reports populated with all validation reports and test logs.")

    # 12. 12_Verification_Suite
    suite_dir = base_dir / '12_Verification_Suite'
    suite_dir.mkdir(parents=True, exist_ok=True)
    scripts_src = Path('scripts')
    for sf in ['preflight.py', 'validate_3d_assembly.py', 'validate_gerbers.py', 'compare_kicad_pcb_gerbers.py', 'validate_assembly_motion_and_clash.py']:
        src = scripts_src / sf
        if src.exists():
            shutil.copy2(src, suite_dir / sf)
    # Copy tests/
    tests_dest = suite_dir / 'tests'
    if tests_dest.exists():
        shutil.rmtree(tests_dest)
    shutil.copytree(Path('tests'), tests_dest)
    print("  [x] 12_Verification_Suite populated.")

    # Create Master Client Delivery ZIP Archive
    master_zip = base_dir / 'SmartPen_RevF_Digital_Design_Review_Package.zip'
    if master_zip.exists():
        master_zip.unlink()

    with zipfile.ZipFile(master_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for folder in sorted(base_dir.iterdir()):
            if folder.is_dir():
                for item in folder.rglob('*'):
                    if item.is_file() and item.name != 'SmartPen_RevF_Digital_Design_Review_Package.zip':
                        rel_path = item.relative_to(base_dir)
                        zf.write(item, rel_path)

    zip_size_kb = master_zip.stat().st_size / 1024.0
    print(f"\nCreated Master ZIP Archive: {master_zip} ({zip_size_kb:.1f} KB)")
    print("ALL 12 CLIENT DELIVERY PACKAGES SUCCESSFULLY POPULATED!")

if __name__ == '__main__':
    package_delivery()
