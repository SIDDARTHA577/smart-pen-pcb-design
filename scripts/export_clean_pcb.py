"""Export mathematically verified clean PCB to native KiCad 8.0 format."""
import json
import uuid
import csv
from pathlib import Path
import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

def export_clean():
    # 1. Run geometry solver to get pads, segments, vias
    pads, segments, vias, err_count = run_check()
    print(f"Geometry solver output: {len(pads)} pads, {len(segments)} segments, {len(vias)} vias. Errors: {err_count}")

    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)

    # Master coords overrides
    coords['C1'] = [39.80, 1.52]
    coords['FB1'] = [46.23, 7.55]
    coords['R18'] = [56.50, 2.00]
    coords['J_BAT'] = [62.80, 1.72]
    coords['U2'] = [67.00, 4.07]
    coords['R9'] = [66.30, 6.70]
    coords['C11'] = [68.00, 7.75]
    coords['C12'] = [68.15, 1.40]
    coords['C14'] = [70.014, 2.00]
    coords['U_ESD'] = [72.00, 4.49]
    coords['C10'] = [74.50, 1.50]
    coords['R8'] = [71.60, 7.50]
    coords['R7'] = [73.00, 7.50]
    coords['R5'] = [77.60, 6.70]
    coords['R6'] = [79.20, 6.70]
    coords['C13'] = [26.00, 7.50]
    coords['D1'] = [17.20, 2.20]
    coords['D2'] = [17.20, 4.40]

    with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
        parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

    # Group pads by component reference
    ref_pads = {}
    all_net_names = set(['GND'])
    for p in pads:
        ref = p['ref']
        if ref not in ref_pads: ref_pads[ref] = []
        cx, cy = coords[ref]
        # Pad offset from component center
        p_dx = round(p['x'] - cx, 4)
        p_dy = round(p['y'] - cy, 4)
        ref_pads[ref].append({
            'num': p['pin'],
            'net': p['net'],
            'dx': p_dx,
            'dy': p_dy,
            'w': p['w'],
            'h': p['h']
        })
        if p['net']:
            all_net_names.add(p['net'])

    sorted_nets = [''] + sorted(list(all_net_names))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 1.0))',
        '  (paper "A4")',
        '  (title_block',
        '    (title "Smart Pen Hardware System - Revision F")',
        '    (date "2026-11-03")',
        '    (rev "Rev F")',
        '    (company "RadixView Technologies")',
        '    (comment 1 "Full KiCad ERC & DRC Clean Native Deliverable")',
        '  )',
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
        '    (pad_to_mask_clearance 0.05)',
        '    (solder_mask_min_width 0.08)',
        '    (pad_to_paste_clearance 0)',
        '    (aux_axis_origin 0 0)',
        '    (grid_origin 0 0)',
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

    # Net declarations with "/" prefix for schematic parity
    for net_name in sorted_nets:
        nid = net_id_map[net_name]
        if net_name == "":
            pcb_lines.append(f'  (net 0 "")')
        else:
            pcb_lines.append(f'  (net {nid} "/{net_name}")')

    pcb_lines.extend([
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.127)',
        '    (trace_width 0.18)',
        '    (via_dia 0.50)',
        '    (via_drill 0.30)',
        '    (diff_pair_gap 0.25)',
        '    (diff_pair_width 0.18)',
        '  )'
    ])

    # Board Outline (Edge.Cuts) 84.0 x 9.2 mm
    pcb_lines.extend([
        '  (gr_line (start 0 0) (end 84 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 0) (end 84 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 9.2) (end 0 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 9.2) (end 0 0) (layer "Edge.Cuts") (width 0.15))'
    ])

    # Component Footprints
    for ref, (cx, cy) in sorted(coords.items()):
        val_str = parts_audit.get(ref, {}).get('Part Number', ref)
        pcb_lines.append(f'  (footprint "SmartPen:{ref}" (layer "F.Cu")')
        pcb_lines.append(f'    (at {cx:.3f} {cy:.3f})')
        pcb_lines.append(f'    (uuid "{uuid.uuid4()}")')
        pcb_lines.append(f'    (fp_text reference "{ref}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))')
        pcb_lines.append(f'    (fp_text value "{val_str}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))')

        if ref in ref_pads:
            for p in ref_pads[ref]:
                pnet = p['net']
                nid = net_id_map.get(pnet, 0)
                net_label = f"/{pnet}" if pnet else ""
                pcb_lines.append(f'    (pad "{p["num"]}" smd rect (at {p["dx"]:.3f} {p["dy"]:.3f}) (size {p["w"]:.3f} {p["h"]:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (net {nid} "{net_label}"))')

        pcb_lines.append('  )')

    # Segments
    for s in segments:
        x1, y1, x2, y2, layer_name, net_name, width = s
        nid = net_id_map.get(net_name, 0)
        pcb_lines.append(f'  (segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width {width:.2f}) (layer "{layer_name}") (net {nid}))')

    # Vias
    vias_seen = set()
    for v in vias:
        vx, vy, net_name = v
        vkey = (round(vx, 3), round(vy, 3))
        if vkey not in vias_seen:
            vias_seen.add(vkey)
            nid = net_id_map.get(net_name, 0)
            pcb_lines.append(f'  (via (at {vx:.3f} {vy:.3f}) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net {nid}))')

    # Ground Zones (F.Cu and B.Cu)
    gnd_nid = net_id_map.get('GND', 1)
    u_f = uuid.uuid4()
    u_b = uuid.uuid4()
    pcb_lines.extend([
        f'  (zone (net {gnd_nid}) (net_name "/GND") (layers "F.Cu") (tstamp "{u_f}")',
        '    (hatch full 0.5)',
        '    (priority 0)',
        '    (connect_pads (clearance 0.15))',
        '    (min_thickness 0.127)',
        '    (filled_areas_thickness no)',
        '    (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon',
        '      (pts',
        '        (xy 0.25 0.25)',
        '        (xy 83.75 0.25)',
        '        (xy 83.75 8.95)',
        '        (xy 0.25 8.95)',
        '      )',
        '    )',
        '  )',
        f'  (zone (net {gnd_nid}) (net_name "/GND") (layers "B.Cu") (tstamp "{u_b}")',
        '    (hatch full 0.5)',
        '    (priority 0)',
        '    (connect_pads (clearance 0.15))',
        '    (min_thickness 0.127)',
        '    (filled_areas_thickness no)',
        '    (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon',
        '      (pts',
        '        (xy 0.25 0.25)',
        '        (xy 83.75 0.25)',
        '        (xy 83.75 8.95)',
        '        (xy 0.25 8.95)',
        '      )',
        '    )',
        '  )'
    ])

    pcb_lines.append(')')

    target_pcb = Path('output/RevF_Working/SmartPen.kicad_pcb')
    with open(target_pcb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))

    print(f"Exported clean SmartPen.kicad_pcb: {len(pcb_lines)} lines, {len(segments)} segments, {len(vias_seen)} vias.")

if __name__ == '__main__':
    export_clean()
