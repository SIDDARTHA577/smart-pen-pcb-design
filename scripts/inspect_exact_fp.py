from pathlib import Path
import re

def parse_kicad_pcb_footprints(pcb_path):
    text = Path(pcb_path).read_text(encoding='utf-8')
    footprints = {}
    
    # Each footprint starts with (footprint "..."
    # Find all footprint tokens
    pos = 0
    while True:
        pos = text.find('(footprint ', pos)
        if pos == -1:
            break
        # find matching paren
        depth = 0
        i = pos
        while i < len(text):
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    fp_block = text[pos:i+1]
                    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_block)
                    val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', fp_block)
                    lib_m = re.match(r'\(footprint\s+"([^"]+)"', fp_block)
                    if ref_m:
                        footprints[ref_m.group(1)] = {
                            'lib': lib_m.group(1) if lib_m else '',
                            'val': val_m.group(1) if val_m else '',
                            'block': fp_block
                        }
                    pos = i + 1
                    break
            i += 1
        else:
            break
    return footprints

def parse_kicad_sch_symbols(sch_path):
    text = Path(sch_path).read_text(encoding='utf-8')
    symbols = {}
    pos = 0
    while True:
        pos = text.find('(symbol ', pos)
        if pos == -1:
            break
        # find matching paren
        depth = 0
        i = pos
        while i < len(text):
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
                if depth == 0:
                    sym_block = text[pos:i+1]
                    # check if this is an instance with (lib_id ...)
                    if '(lib_id ' in sym_block:
                        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', sym_block)
                        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', sym_block)
                        fp_m = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', sym_block)
                        lib_m = re.search(r'\(lib_id\s+"([^"]+)"', sym_block)
                        if ref_m and not ref_m.group(1).startswith('#'):
                            symbols[ref_m.group(1)] = {
                                'val': val_m.group(1) if val_m else '',
                                'fp': fp_m.group(1) if fp_m else '',
                                'lib': lib_m.group(1) if lib_m else '',
                                'block': sym_block
                            }
                    pos = i + 1
                    break
            i += 1
        else:
            break
    return symbols

pcb_fps = parse_kicad_pcb_footprints('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_pcb')
sch_syms = parse_kicad_sch_symbols('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_sch')

for ref in ['Q1', 'Q2', 'U4', 'R9']:
    print(f"\n=================== {ref} ===================")
    if ref in sch_syms:
        s = sch_syms[ref]
        print(f"SCH: LibID={s['lib']}, Val={s['val']}, Footprint={s['fp']}")
    else:
        print("SCH: NOT FOUND")
        
    if ref in pcb_fps:
        p = pcb_fps[ref]
        print(f"PCB: LibID={p['lib']}, Val={p['val']}")
        # print all pads in PCB
        pads = re.findall(r'\(pad\s+"([^"]+)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([^\)]+)\).*?\(net\s+(\d+)\s+"([^"]+)"\)', p['block'])
        for pad in pads:
            print(f"  Pad {pad[0]} ({pad[1]} {pad[2]}) at ({pad[3]}): Net {pad[4]} = {pad[5]}")
    else:
        print("PCB: NOT FOUND")

