"""Test bare PCB generation and DRC baseline."""
import json
import uuid
from pathlib import Path

def generate_bare_pcb():
    with open('output/RevF_Working/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
        pcb_json = json.load(f)

    nets = set(['GND'])
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    if len(ptoks) > 7 and ptoks[7]:
                        nets.add(ptoks[7])
    sorted_nets = [''] + sorted(list(nets))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 1.0))',
        '  (paper "A4")',
        '  (layers',
        '    (0 "F.Cu" signal)',
        '    (31 "B.Cu" signal)',
        '    (36 "B.SilkS" user "B.Silkscreen")',
        '    (37 "F.SilkS" user "F.Silkscreen")',
        '    (38 "B.Mask" user)',
        '    (39 "F.Mask" user)',
        '    (44 "Edge.Cuts" user)',
        '    (48 "F.Fab" user)',
        '    (49 "B.Fab" user)',
        '  )',
        '  (setup',
        '    (pad_to_mask_clearance 0.03)',
        '    (solder_mask_min_width 0.05)',
        '    (pad_to_paste_clearance 0)',
        '    (pcbplotparams (layerselection 0x00010fc_ffffffff))',
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

    # Footprints
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]

            lib_toks = subs[0].split('~')
            x_mm = (float(lib_toks[1]) - 4000.0) * 0.254
            y_mm = (float(lib_toks[2]) - 3000.0) * 0.254

            pcb_lines.append(f'  (footprint "SmartPen:{ref}" (layer "F.Cu")')
            pcb_lines.append(f'    (at {x_mm:.3f} {y_mm:.3f})')
            pcb_lines.append(f'    (uuid "{uuid.uuid4()}")')
            pcb_lines.append(f'    (fp_text reference "{ref}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))')

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

    pcb_lines.append(')')
    with open('output/RevF_Working/test_bare.kicad_pcb', 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))

if __name__ == '__main__':
    generate_bare_pcb()
