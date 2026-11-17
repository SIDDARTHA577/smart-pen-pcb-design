#!/usr/bin/env python3
"""
Verify 100% Schematic-to-PCB Parity and BOM synchronization for FourLayer_ECR_R9_50mA.
"""
import re
import csv
from pathlib import Path

def check_parity():
    sch_path = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_sch')
    pcb_path = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_pcb')
    bom_path = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen_BOM.csv')

    sch_text = sch_path.read_text(encoding='utf-8')
    pcb_text = pcb_path.read_text(encoding='utf-8')

    # Parse schematic instances
    sch_items = {}
    # Find all (symbol (lib_id ...) ... (property "Reference" "REF") ... (property "Value" "VAL")
    sym_blocks = re.findall(r'\(symbol\s+\(lib_id\s+"[^"]+"\).*?\n  \)', sch_text, re.DOTALL)
    for block in sym_blocks:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        fp_m = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            val = val_m.group(1)
            fp = fp_m.group(1) if fp_m else ''
            # skip power symbols if any
            if not ref.startswith('#'):
                sch_items[ref] = {'val': val, 'fp': fp}

    # Parse PCB footprints
    pcb_items = {}
    fp_blocks = re.findall(r'\(footprint\s+"[^"]+".*?\n\t\)', pcb_text, re.DOTALL)
    for block in fp_blocks:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            val = val_m.group(1)
            pcb_items[ref] = {'val': val}

    print(f"Total Schematic Components: {len(sch_items)}")
    print(f"Total PCB Footprints:       {len(pcb_items)}")

    mismatches = []
    for ref, s_info in sorted(sch_items.items()):
        if ref not in pcb_items:
            mismatches.append(f"Component {ref} in SCH but missing on PCB")
        elif pcb_items[ref]['val'] != s_info['val']:
            mismatches.append(f"Value mismatch for {ref}: SCH={s_info['val']} vs PCB={pcb_items[ref]['val']}")

    for ref in sorted(pcb_items.keys()):
        if ref not in sch_items:
            mismatches.append(f"Footprint {ref} on PCB but missing in SCH")

    if mismatches:
        print(f"Found {len(mismatches)} parity mismatches:")
        for m in mismatches:
            print("  *", m)
        return False
    else:
        print("PERFECT 100% SCHEMATIC-TO-PCB PARITY CONFIRMED!")
        print(f"  R9 in Schematic: {sch_items['R9']['val']}")
        print(f"  R9 on PCB:       {pcb_items['R9']['val']}")

    # Generate synchronized BOM
    with open(bom_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Reference', 'Value', 'Footprint', 'Qty'])
        # group by (val, fp)
        grouped = {}
        for ref, info in sorted(sch_items.items()):
            key = (info['val'], info['fp'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(ref)
        
        for (val, fp), refs in sorted(grouped.items()):
            writer.writerow([','.join(refs), val, fp, len(refs)])
    
    print(f"Generated synchronized BOM at: {bom_path}")
    return True

if __name__ == '__main__':
    ok = check_parity()
    exit(0 if ok else 1)
