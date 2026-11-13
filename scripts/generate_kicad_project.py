"""Generate native KiCad v7/v8 project files from Smart Pen Rev E design:
- output/kicad/SmartPen.kicad_pro
- output/kicad/SmartPen.kicad_sch
- output/kicad/SmartPen.kicad_pcb
"""
import json
import uuid
from pathlib import Path

def generate_kicad():
    kicad_dir = Path('output/kicad')
    kicad_dir.mkdir(parents=True, exist_ok=True)

    # 1. Project file (SmartPen.kicad_pro)
    pro_content = {
        "meta": {
            "filename": "SmartPen.kicad_pro",
            "version": 1
        },
        "project": {
            "title": "Smart Pen Rev E",
            "company": "RadixView Technologies",
            "rev": "Rev E"
        },
        "schematic": {
            "drawing": {
                "dashed_lines_dash_length_ratio": 12.0,
                "dashed_lines_gap_length_ratio": 3.0,
                "default_line_thickness": 0.1524,
                "default_text_size": 1.27,
                "pin_symbol_size": 0.0
            }
        },
        "pcbnew": {
            "last_paths": {
                "gencad": "",
                "idf": "",
                "netlist": "",
                "plot": "",
                "pos": "",
                "step": "",
                "vrml": ""
            }
        }
    }
    with open(kicad_dir / 'SmartPen.kicad_pro', 'w', encoding='utf-8') as f:
        json.dump(pro_content, f, indent=2)

    # Load schematic JSON and footprint audit
    with open('output/RevE_work/SmartPen_RevE_Schematic.json', 'r', encoding='utf-8') as f:
        sch = json.load(f)
    with open('output/RevE_work/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
        pcb = json.load(f)

    # 2. Schematic file (SmartPen.kicad_sch)
    sch_lines = [
        '(kicad_sch (version 20230121) (generator "eeschema") (generator_version "7.0")',
        f'  (uuid "{uuid.uuid4()}")',
        '  (paper "A3")',
        '  (title_block',
        '    (title "Smart Pen Hardware System")',
        '    (date "2026-11-02")',
        '    (rev "Rev E")',
        '    (company "RadixView Technologies")',
        '    (comment 1 "ESP32-C3 Main Controller with Detachable Tip IMU")',
        '  )'
    ]

    # Add symbols and pins
    sym_idx = 1
    for item in sch['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            val = ''
            pkg = ''
            pins = []
            for sub in subs:
                if sub.startswith('T~'):
                    t = sub.split('~')
                    if len(t) >= 13:
                        if t[1] == 'P': ref = t[12] if t[11] == 'comment' else t[11]
                        elif t[1] == 'N': val = t[12] if t[11] == 'comment' else t[11]
                elif sub.startswith('P~'):
                    psec = sub.split('^^')
                    pname = psec[3].split('~')[4] if len(psec) > 3 and len(psec[3].split('~')) >= 5 else ''
                    pnum = psec[4].split('~')[4] if len(psec) > 4 and len(psec[4].split('~')) >= 5 else ''
                    pins.append((pnum, pname))

            lib_toks = subs[0].split('~')
            props_str = lib_toks[3] if len(lib_toks) > 3 else ''
            for tok in props_str.split('`'):
                if tok.startswith('QFN') or tok.startswith('R0') or tok.startswith('C0') or tok.startswith('SOT') or tok.startswith('CONN'):
                    pkg = tok

            sch_lines.append(f'  (symbol (lib_id "Device:{ref}") (at {20 + (sym_idx%10)*25:.2f} {20 + (sym_idx//10)*30:.2f} 0) (unit 1)')
            sch_lines.append(f'    (in_bom yes) (on_board yes) (dnp no)')
            sch_lines.append(f'    (uuid "{uuid.uuid4()}")')
            sch_lines.append(f'    (property "Reference" "{ref}" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))')
            sch_lines.append(f'    (property "Value" "{val}" (at 0 2.54 0) (effects (font (size 1.27 1.27))))')
            sch_lines.append(f'    (property "Footprint" "{pkg}" (at 0 5.08 0) (effects (font (size 1.27 1.27)) hide))')
            for pnum, pname in pins[:4]:
                sch_lines.append(f'    (pin passive line (at 0 0 0) (length 2.54) (name "{pname}") (number "{pnum}"))')
            sch_lines.append('  )')
            sym_idx += 1

    sch_lines.append(')')
    with open(kicad_dir / 'SmartPen.kicad_sch', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sch_lines))

    # 3. PCB file (SmartPen.kicad_pcb)
    # Collect all nets from PCB
    all_nets = set()
    for item in pcb['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            for sub in subs:
                if sub.startswith('PAD~'):
                    pad_toks = sub.split('~')
                    if len(pad_toks) > 7 and pad_toks[7]:
                        all_nets.add(pad_toks[7])
        elif isinstance(item, str) and item.startswith('TRACK~'):
            toks = item.split('~')
            if len(toks) > 3 and toks[3]:
                all_nets.add(toks[3])

    sorted_nets = [''] + sorted(list(all_nets))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "7.0")',
        '  (general',
        '    (thickness 1.0)',
        '  )',
        '  (paper "A4")',
        '  (title_block',
        '    (title "Smart Pen Rev E PCB")',
        '    (date "2026-11-02")',
        '    (rev "Rev E")',
        '    (company "RadixView Technologies")',
        '  )',
        '  (layers',
        '    (0 "F.Cu" signal)',
        '    (31 "B.Cu" signal)',
        '    (36 "B.SilkS" user "B.Silkscreen")',
        '    (37 "F.SilkS" user "F.Silkscreen")',
        '    (38 "B.Mask" user)',
        '    (39 "F.Mask" user)',
        '    (44 "Edge.Cuts" user)',
        '  )',
        '  (setup',
        '    (pad_to_mask_clearance 0.05)',
        '    (pcbplotparams',
        '      (layerselection 0x00010fc_ffffffff)',
        '      (plotframeref no)',
        '      (viasonmask no)',
        '      (mode 1)',
        '      (usegerberextensions yes)',
        '      (usegerberattributes yes)',
        '      (usegerberadvancedattributes yes)',
        '      (creategerberjobfile yes)',
        '      (outputdirectory "gerber/")',
        '    )',
        '  )'
    ]

    for net_name, nid in net_id_map.items():
        pcb_lines.append(f'  (net {nid} "{net_name}")')

    # Board Outline (Edge.Cuts) 84.0 x 9.2 mm
    pcb_lines.extend([
        '  (gr_line (start 0 0) (end 84 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 0) (end 84 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 9.2) (end 0 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 9.2) (end 0 0) (layer "Edge.Cuts") (width 0.15))'
    ])

    # Footprints and pads
    for item in pcb['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]

            lib_toks = subs[0].split('~')
            # Extract x, y in mm
            x_mm = (float(lib_toks[1]) - 4000.0) * 0.254
            y_mm = (float(lib_toks[2]) - 3000.0) * 0.254

            pcb_lines.append(f'  (footprint "SmartPen:{ref}" (layer "F.Cu")')
            pcb_lines.append(f'    (at {x_mm:.3f} {y_mm:.3f})')
            pcb_lines.append(f'    (uuid "{uuid.uuid4()}")')
            pcb_lines.append(f'    (fp_text reference "{ref}" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))')

            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    px_mm = (float(ptoks[2]) - float(lib_toks[1])) * 0.254
                    py_mm = (float(ptoks[3]) - float(lib_toks[2])) * 0.254
                    pw_mm = float(ptoks[4]) * 0.254
                    ph_mm = float(ptoks[5]) * 0.254
                    pnet = ptoks[7]
                    pnum = ptoks[8]
                    nid = net_id_map.get(pnet, 0)
                    pcb_lines.append(f'    (pad "{pnum}" smd rect (at {px_mm:.3f} {py_mm:.3f}) (size {pw_mm:.3f} {ph_mm:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (net {nid} "{pnet}"))')

            pcb_lines.append('  )')

    # Vias
    for item in pcb['shape']:
        if isinstance(item, str) and item.startswith('VIA~'):
            vtoks = item.split('~')
            vx_mm = (float(vtoks[1]) - 4000.0) * 0.254
            vy_mm = (float(vtoks[2]) - 3000.0) * 0.254
            vnet = vtoks[5]
            nid = net_id_map.get(vnet, 0)
            pcb_lines.append(f'  (via (at {vx_mm:.3f} {vy_mm:.3f}) (size 0.6) (drill 0.3) (layers "F.Cu" "B.Cu") (net {nid}))')

    # Traces
    for item in pcb['shape']:
        if isinstance(item, str) and item.startswith('TRACK~'):
            ttoks = item.split('~')
            layer_id = ttoks[2]
            layer_name = "F.Cu" if layer_id == '1' else ("B.Cu" if layer_id == '2' else None)
            tnet = ttoks[3]
            nid = net_id_map.get(tnet, 0)
            if layer_name and tnet:
                coords = [float(c) for c in ttoks[4].split()]
                for i in range(0, len(coords) - 2, 2):
                    x1 = (coords[i] - 4000.0) * 0.254
                    y1 = (coords[i+1] - 3000.0) * 0.254
                    x2 = (coords[i+2] - 4000.0) * 0.254
                    y2 = (coords[i+3] - 3000.0) * 0.254
                    pcb_lines.append(f'  (segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width 0.25) (layer "{layer_name}") (net {nid}))')

    # Ground Zones (F.Cu and B.Cu)
    gnd_nid = net_id_map.get('GND', 1)
    for zlayer in ["F.Cu", "B.Cu"]:
        pcb_lines.extend([
            f'  (zone (net {gnd_nid}) (net_name "GND") (layer "{zlayer}") (tstamp "{uuid.uuid4()}") (hatch edge 0.5)',
            '    (connect_pads (clearance 0.254))',
            '    (min_thickness 0.254)',
            '    (filled_polygon',
            '      (pts',
            '        (xy 0.2 0.2)',
            '        (xy 83.8 0.2)',
            '        (xy 83.8 9.0)',
            '        (xy 0.2 9.0)',
            '        (xy 0.2 0.2)',
            '      )',
            '    )',
            '  )'
        ])

    pcb_lines.append(')')
    with open(kicad_dir / 'SmartPen.kicad_pcb', 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))

    print(f"Generated KiCad project files in {kicad_dir}:")
    print(" - SmartPen.kicad_pro")
    print(" - SmartPen.kicad_sch")
    print(" - SmartPen.kicad_pcb")

if __name__ == '__main__':
    generate_kicad()

