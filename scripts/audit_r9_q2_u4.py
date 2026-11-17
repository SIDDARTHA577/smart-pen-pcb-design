import os
import re
from pathlib import Path

def parse_sexpr_blocks(text, keyword):
    blocks = []
    idx = 0
    target = f'({keyword}'
    while True:
        pos = text.find(target, idx)
        if pos == -1:
            break
        # find matching closing parenthesis
        depth = 0
        i = pos
        while i < len(text):
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    blocks.append(text[pos:i+1])
                    idx = i + 1
                    break
            i += 1
        else:
            break
    return blocks

def audit():
    var_dir = Path('output/RevG/variants/FourLayer_ECR_R9_50mA')
    pcb_path = var_dir / 'SmartPen.kicad_pcb'
    sch_path = var_dir / 'SmartPen.kicad_sch'
    sym_path = var_dir / 'SmartPen_Lib.kicad_sym'
    fp_dir = var_dir / 'SmartPen.pretty'

    pcb_text = pcb_path.read_text(encoding='utf-8')
    sch_text = sch_path.read_text(encoding='utf-8')
    sym_text = sym_path.read_text(encoding='utf-8')

    sch_symbols = parse_sexpr_blocks(sch_text, 'symbol')
    pcb_footprints = parse_sexpr_blocks(pcb_text, 'footprint')

    print(f"Total SCH top-level/nested symbols: {len(sch_symbols)}")
    print(f"Total PCB footprints: {len(pcb_footprints)}")

    # Map references
    sch_by_ref = {}
    for block in sch_symbols:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        fp_m = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', block)
        lib_m = re.search(r'\(lib_id\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            if not ref.startswith('#'):
                sch_by_ref[ref] = {
                    'val': val_m.group(1),
                    'fp': fp_m.group(1) if fp_m else '',
                    'lib_id': lib_m.group(1) if lib_m else '',
                    'raw': block
                }

    pcb_by_ref = {}
    for block in pcb_footprints:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        # lib_id in footprint
        m_lib = re.match(r'\(footprint\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            pcb_by_ref[ref] = {
                'val': val_m.group(1),
                'fp_lib_id': m_lib.group(1) if m_lib else '',
                'raw': block
            }

    print("\n--- R9 AUDIT ---")
    if 'R9' in sch_by_ref:
        print("SCH R9:", sch_by_ref['R9']['val'], "FP:", sch_by_ref['R9']['fp'], "LIB:", sch_by_ref['R9']['lib_id'])
    if 'R9' in pcb_by_ref:
        print("PCB R9:", pcb_by_ref['R9']['val'], "FP LIB ID:", pcb_by_ref['R9']['fp_lib_id'])
    # check footprint file in SmartPen.pretty
    r9_fp_file = fp_dir / 'R9.kicad_mod'
    if r9_fp_file.exists():
        print(f"SmartPen.pretty/R9.kicad_mod exists:\n{r9_fp_file.read_text(encoding='utf-8')[:400]}")
    else:
        print("SmartPen.pretty/R9.kicad_mod DOES NOT EXIST")

    # check symbol in sym_lib
    r9_sym = re.search(r'\(symbol\s+"R9".*?\n  \)', sym_text, re.DOTALL)
    if r9_sym:
        print("sym_lib R9:\n", r9_sym.group(0)[:300])
    else:
        print("No (symbol \"R9\" ...) in sym_lib")

    print("\n--- Q1 & Q2 AUDIT ---")
    for q in ['Q1', 'Q2']:
        if q in sch_by_ref:
            print(f"SCH {q}: Value={sch_by_ref[q]['val']}, Footprint={sch_by_ref[q]['fp']}, Lib={sch_by_ref[q]['lib_id']}")
        if q in pcb_by_ref:
            print(f"PCB {q}: Value={pcb_by_ref[q]['val']}, Footprint LibID={pcb_by_ref[q]['fp_lib_id']}")
            pads = re.findall(r'\(pad\s+"([^"]+)"\s+[^\(]+\(at\s+([^\)]+)\).*?\(net\s+\d+\s+"([^"]+)"\)', pcb_by_ref[q]['raw'])
            for p in pads:
                print(f"  Pad {p[0]} at ({p[1]}): Net {p[2]}")

    print("\n--- U4 & J_PWR AUDIT ---")
    for u in ['U4', 'J_PWR', 'J_BAT']:
        if u in sch_by_ref:
            print(f"SCH {u}: Value={sch_by_ref[u]['val']}, Footprint={sch_by_ref[u]['fp']}, Lib={sch_by_ref[u]['lib_id']}")
        else:
            print(f"SCH {u}: NOT IN SCH")
        if u in pcb_by_ref:
            print(f"PCB {u}: Value={pcb_by_ref[u]['val']}, Footprint LibID={pcb_by_ref[u]['fp_lib_id']}")
            pads = re.findall(r'\(pad\s+"([^"]+)"\s+[^\(]+\(at\s+([^\)]+)\).*?\(net\s+\d+\s+"([^"]+)"\)', pcb_by_ref[u]['raw'])
            for p in pads:
                print(f"  Pad {p[0]} at ({p[1]}): Net {p[2]}")
        else:
            print(f"PCB {u}: NOT ON PCB")

    # Check all footprints in SmartPen.pretty to see what files exist
    pretty_files = sorted([f.name for f in fp_dir.glob('*.kicad_mod')])
    print(f"\nFiles in SmartPen.pretty ({len(pretty_files)} files):")
    print(", ".join(pretty_files))

if __name__ == '__main__':
    audit()
