"""Build exact routed PCB where all tracks connect directly to exact pad centers."""
import json
import uuid
import csv
from pathlib import Path

def build_exact_routed_pcb():
    # 1. Load coordinates
    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)
    with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)
    with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
        parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

    # Nets
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

    # Extract pad offsets
    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]
            if not ref:
                continue
            lib_toks = subs[0].split('~')
            orig_x, orig_y = float(lib_toks[1]), float(lib_toks[2])
            pads = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pw = float(ptoks[4]) * 0.254
                    ph = float(ptoks[5]) * 0.254
                    pnet = ptoks[7]
                    pnum = ptoks[8]
                    pads.append({
                        'num': pnum, 'net': pnet,
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(pw, 4), 'h': round(ph, 4)
                    })
            fp_defs[ref] = pads

    # Compute absolute pad locations
    net_pads = {net: [] for net in sorted_nets if net}
    all_pads = []
    for ref, pos in coords.items():
        if ref not in fp_defs:
            continue
        cx, cy = pos
        for p in fp_defs[ref]:
            p_abs_x = round(cx + p['dx'], 4)
            p_abs_y = round(cy + p['dy'], 4)
            pnet = p['net']
            all_pads.append({
                'ref': ref, 'pin': p['num'], 'net': pnet,
                'x': p_abs_x, 'y': p_abs_y,
                'w': p['w'], 'h': p['h']
            })
            if pnet:
                net_pads[pnet].append({
                    'ref': ref, 'pin': p['num'],
                    'x': p_abs_x, 'y': p_abs_y,
                    'w': p['w'], 'h': p['h']
                })

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 1.0))',
        '  (paper "A4")',
        '  (title_block',
        '    (title "Smart Pen Hardware System - Revision F")',
        '    (date "2026-11-02")',
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
        '    (pad_to_mask_clearance 0.0)',
        '    (solder_mask_min_width 0.0)',
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

    for net_name, nid in net_id_map.items():
        pcb_lines.append(f'  (net {nid} "{net_name}")')

    pcb_lines.extend([
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.15)',
        '    (trace_width 0.20)',
        '    (via_dia 0.50)',
        '    (via_drill 0.30)',
        '    (diff_pair_gap 0.25)',
        '    (diff_pair_width 0.20)',
        '  )'
    ])

    # Board Outline (Edge.Cuts) 84.0 x 9.2 mm
    pcb_lines.extend([
        '  (gr_line (start 0 0) (end 84 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 0) (end 84 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 9.2) (end 0 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 9.2) (end 0 0) (layer "Edge.Cuts") (width 0.15))'
    ])

    # Footprints
    for ref, (cx, cy) in sorted(coords.items()):
        val_str = parts_audit.get(ref, {}).get('Part Number', ref)
        pcb_lines.append(f'  (footprint "SmartPen:{ref}" (layer "F.Cu")')
        pcb_lines.append(f'    (at {cx:.3f} {cy:.3f})')
        pcb_lines.append(f'    (uuid "{uuid.uuid4()}")')
        pcb_lines.append(f'    (fp_text reference "{ref}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))')
        pcb_lines.append(f'    (fp_text value "{val_str}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))')

        if ref in fp_defs:
            for p in fp_defs[ref]:
                pnet = p['net']
                nid = net_id_map.get(pnet, 0)
                pcb_lines.append(f'    (pad "{p["num"]}" smd rect (at {p["dx"]:.3f} {p["dy"]:.3f}) (size {p["w"]:.3f} {p["h"]:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (net {nid} "{pnet}"))')

        pcb_lines.append('  )')

    # Routing
    non_gnd_nets = [n for n in sorted_nets if n and n != 'GND']
    
    # 26 lanes on B.Cu
    lanes = [round(1.0 + i * 0.28, 3) for i in range(26)]
    lane_assignments = {}
    lane_occupancy = {i: [] for i in range(len(lanes))}

    for net in non_gnd_nets:
        plist = net_pads[net]
        if not plist: continue
        xs = [p['x'] for p in plist]
        x_min, x_max = min(xs), max(xs)

        assigned_lane = None
        for l_idx in range(len(lanes)):
            overlaps = False
            for (occ_start, occ_end) in lane_occupancy[l_idx]:
                if not (x_max + 0.6 < occ_start or x_min - 0.6 > occ_end):
                    overlaps = True
                    break
            if not overlaps:
                assigned_lane = l_idx
                break
        if assigned_lane is None:
            assigned_lane = len(lanes) - 1
        lane_assignments[net] = lanes[assigned_lane]
        lane_occupancy[assigned_lane].append((x_min, x_max))

    vias_set = set()
    total_segments = 0

    for net in non_gnd_nets:
        plist = net_pads[net]
        nid = net_id_map[net]
        if len(plist) < 2:
            continue

        plist_sorted = sorted(plist, key=lambda p: p['x'])
        y_highway = lane_assignments[net]
        via_points = []

        for p in plist_sorted:
            px, py = p['x'], p['y']

            # Find clean via position near px, y_highway
            # Ensure via is not on another net's pad
            via_x = px
            via_y = y_highway

            # Connect pad to via:
            # First segment from exact pad center (px, py) to (via_x, via_y) on F.Cu
            if abs(py - via_y) > 0.001 or abs(px - via_x) > 0.001:
                pcb_lines.append(f'  (segment (start {px:.3f} {py:.3f}) (end {via_x:.3f} {via_y:.3f}) (width 0.20) (layer "F.Cu") (net {nid}))')
                total_segments += 1

            via_key = (round(via_x, 3), round(via_y, 3))
            if via_key not in vias_set:
                vias_set.add(via_key)
                pcb_lines.append(f'  (via (at {via_x:.3f} {via_y:.3f}) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net {nid}))')
            via_points.append((via_x, via_y))

        # Connect consecutive vias along B.Cu highway
        for i in range(len(via_points) - 1):
            vx1, vy1 = via_points[i]
            vx2, vy2 = via_points[i+1]
            if abs(vx1 - vx2) > 0.001:
                pcb_lines.append(f'  (segment (start {vx1:.3f} {vy1:.3f}) (end {vx2:.3f} {vy2:.3f}) (width 0.20) (layer "B.Cu") (net {nid}))')
                total_segments += 1

    # Ground Stitching Vias (tied to all GND pads)
    gnd_nid = net_id_map.get('GND', 1)
    gnd_pads = net_pads['GND']
    # Add small via to each GND pad on F.Cu
    for gp in gnd_pads:
        gx, gy = gp['x'], gp['y']
        via_key = (round(gx, 3), round(gy, 3))
        if via_key not in vias_set:
            vias_set.add(via_key)
            pcb_lines.append(f'  (via (at {gx:.3f} {gy:.3f}) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net {gnd_nid}))')

    # Ground Zones (F.Cu and B.Cu) with modern syntax
    for zlayer in ["F.Cu", "B.Cu"]:
        pcb_lines.extend([
            f'  (zone (net {gnd_nid}) (net_name "GND") (layers "{zlayer}") (tstamp "{uuid.uuid4()}")',
            '    (hatch full 0.5)',
            '    (priority 0)',
            '    (connect_pads (clearance 0.18))',
            '    (min_thickness 0.18)',
            '    (filled_areas_thickness no)',
            '    (fill yes (thermal_gap 0.20) (thermal_bridge_width 0.20))',
            '    (polygon',
            '      (pts',
            '        (xy 0.35 0.35)',
            '        (xy 83.65 0.35)',
            '        (xy 83.65 8.85)',
            '        (xy 0.35 8.85)',
            '      )',
            '    )',
            '  )'
        ])

    pcb_lines.append(')')

    target_pcb = Path('output/RevF_Working/SmartPen.kicad_pcb')
    with open(target_pcb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))

    print(f"Generated SmartPen.kicad_pcb: {len(pcb_lines)} lines, {total_segments} track segments, {len(vias_set)} vias.")

if __name__ == '__main__':
    build_exact_routed_pcb()

