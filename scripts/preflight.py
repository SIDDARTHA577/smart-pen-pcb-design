"""Deterministic static design validator for Smart Pen Rev E.
Usage: python scripts/preflight.py --workspace . --reports reports
"""
import argparse
import csv
import json
import sys
from pathlib import Path

def run_preflight(workspace_dir, reports_dir):
    ws = Path(workspace_dir)
    rep = Path(reports_dir)
    rep.mkdir(parents=True, exist_ok=True)

    results = {}
    errors = []
    warnings = []

    print("==================================================")
    print("      SMART PEN Rev E PREFLIGHT DESIGN AUDIT      ")
    print("==================================================")

    # 1. JSON parse & document types
    sch_file = ws / 'output/RevE_work/SmartPen_RevE_Schematic.json'
    pcb_file = ws / 'output/RevE_work/SmartPen_RevE_PCB.json'

    if not sch_file.exists():
        errors.append(f"Schematic file missing: {sch_file}")
    else:
        try:
            with open(sch_file, 'r', encoding='utf-8') as f:
                sch_data = json.load(f)
            sch_doc_type = sch_data.get('head', {}).get('docType')
            if str(sch_doc_type) != '1':
                errors.append(f"Schematic docType expected '1', got {sch_doc_type}")
            else:
                results['schematic_json'] = 'PASS'
        except Exception as e:
            errors.append(f"Schematic JSON parse error: {e}")

    if not pcb_file.exists():
        errors.append(f"PCB file missing: {pcb_file}")
    else:
        try:
            with open(pcb_file, 'r', encoding='utf-8') as f:
                pcb_data = json.load(f)
            pcb_doc_type = pcb_data.get('head', {}).get('docType')
            if str(pcb_doc_type) != '3':
                errors.append(f"PCB docType expected '3', got {pcb_doc_type}")
            else:
                results['pcb_json'] = 'PASS'
        except Exception as e:
            errors.append(f"PCB JSON parse error: {e}")

    # 2. Schematic component check & unique references
    sch_comps = {}
    if 'schematic_json' in results:
        for item in sch_data.get('shape', []):
            if isinstance(item, str) and item.startswith('LIB~'):
                subs = item.split('#@$')
                ref = ''
                for sub in subs:
                    if sub.startswith('T~'):
                        t = sub.split('~')
                        if len(t) >= 13 and t[1] == 'P':
                            ref = t[12] if t[11] == 'comment' else t[11]
                if ref:
                    if ref in sch_comps:
                        errors.append(f"Duplicate schematic component reference: {ref}")
                    sch_comps[ref] = item

        if len(sch_comps) == 60:
            results['schematic_components_count'] = 'PASS (60 components)'
        else:
            errors.append(f"Expected 60 schematic components, found {len(sch_comps)}")

    # 3. PCB component check & board outline dimensions
    pcb_comps = {}
    board_dims = None
    if 'pcb_json' in results:
        for item in pcb_data.get('shape', []):
            if isinstance(item, str):
                if item.startswith('LIB~'):
                    subs = item.split('#@$')
                    ref = ''
                    for sub in subs:
                        if sub.startswith('TEXT~P~'):
                            ref = sub.split('~')[10]
                    if ref:
                        if ref in pcb_comps:
                            errors.append(f"Duplicate PCB component reference: {ref}")
                        pcb_comps[ref] = item
                elif item.startswith('TRACK~'):
                    toks = item.split('~')
                    if toks[2] == '10': # Outline
                        coords = [float(c) for c in toks[4].split()]
                        xs = [(coords[i] - 4000.0) * 0.254 for i in range(0, len(coords)-1, 2)]
                        ys = [(coords[i+1] - 3000.0) * 0.254 for i in range(0, len(coords)-1, 2)]
                        board_dims = (max(xs) - min(xs), max(ys) - min(ys))

        if len(pcb_comps) == 60:
            results['pcb_components_count'] = 'PASS (60 components)'
        else:
            errors.append(f"Expected 60 PCB components, found {len(pcb_comps)}")

        if board_dims:
            length, width = board_dims
            if abs(length - 84.0) < 0.1 and abs(width - 9.2) < 0.1:
                results['board_outline_dimensions'] = f'PASS ({length:.1f} x {width:.1f} mm)'
            else:
                errors.append(f"Board dimensions mismatch: {length:.2f} x {width:.2f} mm (expected 84.0 x 9.2 mm)")
        else:
            errors.append("Board outline track on Layer 10 missing")

    # 4. Schematic-vs-PCB parity
    missing_on_pcb = set(sch_comps.keys()) - set(pcb_comps.keys())
    extra_on_pcb = set(pcb_comps.keys()) - set(sch_comps.keys())
    if not missing_on_pcb and not extra_on_pcb:
        results['schematic_pcb_parity'] = 'PASS (100% matched, 0 missing, 0 extra)'
    else:
        errors.append(f"Parity mismatch! Missing on PCB: {missing_on_pcb}, Extra on PCB: {extra_on_pcb}")

    # 5. BOM & Footprint audit verification
    audit_file = ws / 'reports/FOOTPRINT_AUDIT.csv'
    if not audit_file.exists():
        errors.append("reports/FOOTPRINT_AUDIT.csv missing")
    else:
        with open(audit_file, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
        if len(reader) == 60:
            unresolved = [r['Reference'] for r in reader if r['Validation Status'] != 'PASS']
            if not unresolved:
                results['bom_footprint_audit'] = 'PASS (60/60 parts verified)'
            else:
                errors.append(f"Unresolved parts in BOM audit: {unresolved}")
        else:
            errors.append(f"BOM audit has {len(reader)} entries, expected 60")

    # 6. Gerber manufacturing package completeness
    gerber_zip = ws / 'output/RevE_work/SmartPen_RevE_Gerbers.zip'
    if gerber_zip.exists() and gerber_zip.stat().st_size > 1000:
        results['gerber_package'] = f'PASS ({gerber_zip.stat().st_size} bytes)'
    else:
        errors.append("Gerber package missing or empty")

    # 7. Mechanical 3D STL models completeness
    stl_dir = ws / 'output/RevE_work/3D_STL'
    stl_files = list(stl_dir.glob('*.stl')) if stl_dir.exists() else []
    if len(stl_files) >= 10:
        results['mechanical_cad_stls'] = f'PASS ({len(stl_files)} STL components verified)'
    else:
        errors.append(f"Expected at least 10 STL models, found {len(stl_files)}")

    # Print summary
    print(f"\nPreflight Status: {'SUCCESS' if not errors else 'FAILURE'}")
    for k, v in results.items():
        print(f" [PASS] {k:<30}: {v}")
    for w in warnings:
        print(f" [WARN] {w}")
    for e in errors:
        print(f" [FAIL] {e}")

    return len(errors) == 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', default='.', help='Workspace path')
    parser.add_argument('--reports', default='reports', help='Reports directory')
    args = parser.parse_args()

    success = run_preflight(args.workspace, args.reports)
    sys.exit(0 if success else 1)

