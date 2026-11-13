"""Export all client deliverables for MicroSD Carrier subsystem.
Gerbers, Drills, PDF schematic, 3D STEP, CPL/POS, and BOM.
"""
import subprocess
import os
import shutil
import zipfile
from pathlib import Path

KICAD_CLI = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/KiCad/10.0/bin/kicad-cli.exe'

def export_carrier_deliverables():
    carrier_dir = Path('output/RevF_Working/MicroSD_Carrier')
    pcb_path = carrier_dir / 'MicroSD_Carrier.kicad_pcb'
    sch_path = carrier_dir / 'MicroSD_Carrier.kicad_sch'

    delivery_dir = Path('output/RevF_Client_Delivery')
    gerber_dir = carrier_dir / 'gerber'
    gerber_dir.mkdir(parents=True, exist_ok=True)

    print("1. Exporting Gerbers...")
    subprocess.run([
        str(KICAD_CLI), 'pcb', 'export', 'gerbers',
        '--output', str(gerber_dir) + '/',
        str(pcb_path)
    ], check=True)

    print("2. Exporting Drills...")
    subprocess.run([
        str(KICAD_CLI), 'pcb', 'export', 'drill',
        '--output', str(gerber_dir) + '/',
        '--format', 'excellon',
        '--excellon-zeros-format', 'decimal',
        str(pcb_path)
    ], check=True)

    # Zip Gerbers
    zip_dest = delivery_dir / '04_Gerber_Drill/MicroSD_Carrier_Gerbers.zip'
    zip_dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in gerber_dir.glob('*'):
            if f.is_file():
                zf.write(f, f.name)
    print(f"  [x] Created {zip_dest} ({zip_dest.stat().st_size} bytes)")

    # 3. PDF Schematic
    pdf_dest = delivery_dir / '03_PDF_Schematic/MicroSD_Carrier_Schematic.pdf'
    pdf_dest.parent.mkdir(parents=True, exist_ok=True)
    print("3. Exporting PDF Schematic...")
    subprocess.run([
        str(KICAD_CLI), 'sch', 'export', 'pdf',
        '-o', str(pdf_dest),
        str(sch_path)
    ], check=True)
    print(f"  [x] Created {pdf_dest} ({pdf_dest.stat().st_size} bytes)")

    # 4. 3D STEP
    step_dest = delivery_dir / '07_3D_STEP/MicroSD_Carrier.step'
    step_dest.parent.mkdir(parents=True, exist_ok=True)
    print("4. Exporting 3D STEP...")
    subprocess.run([
        str(KICAD_CLI), 'pcb', 'export', 'step',
        '--no-dnp',
        '-o', str(step_dest),
        str(pcb_path)
    ], check=True)
    print(f"  [x] Created {step_dest} ({step_dest.stat().st_size} bytes)")

    # 5. CPL / POS
    pos_dest = delivery_dir / '05_BOM_CPL/MicroSD_Carrier_CPL.csv'
    pos_dest.parent.mkdir(parents=True, exist_ok=True)
    print("5. Exporting CPL / POS...")
    subprocess.run([
        str(KICAD_CLI), 'pcb', 'export', 'pos',
        '--format', 'csv',
        '--units', 'mm',
        '-o', str(pos_dest),
        str(pcb_path)
    ], check=True)
    print(f"  [x] Created {pos_dest} ({pos_dest.stat().st_size} bytes)")

    # 6. Copy BOM
    bom_src = carrier_dir / 'MicroSD_Carrier_BOM.csv'
    bom_dest = delivery_dir / '05_BOM_CPL/MicroSD_Carrier_BOM.csv'
    shutil.copy2(bom_src, bom_dest)
    print(f"  [x] Copied BOM to {bom_dest}")

    # 7. Copy KiCad Source into Client Delivery
    src_dest_dir = delivery_dir / '02_KiCad_Source/MicroSD_Carrier'
    if src_dest_dir.exists():
        shutil.rmtree(src_dest_dir)
    shutil.copytree(carrier_dir, src_dest_dir, ignore=shutil.ignore_patterns('gerber', '*.rpt'))
    print(f"  [x] Synced KiCad source to {src_dest_dir}")

if __name__ == '__main__':
    export_carrier_deliverables()
