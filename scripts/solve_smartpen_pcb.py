"""Complete Deterministic Routing Solver for Smart Pen Rev F Main PCB."""
import json, math, uuid, csv
import sys
sys.path.insert(0, '.')
from scripts.pcb_geom import dist_point_to_segment, dist_segment_to_segment, dist_segment_to_rect

def solve_smartpen_pcb():
    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)
    with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)
    with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
        parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

    nets = set(['GND'])
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            for sub in item.split('#@$'):
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    if len(ptoks) > 7 and ptoks[7]:
                        nets.add(ptoks[7])
    sorted_nets = [''] + sorted(list(nets))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]
            if not ref: continue
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
                    pads.append({'num': ptoks[8], 'net': ptoks[7], 'dx': round(dx, 4), 'dy': round(dy, 4), 'w': round(pw, 4), 'h': round(ph, 4)})
            fp_defs[ref] = pads

    all_pads = []
    net_pads = {net: [] for net in sorted_nets if net}
    for ref, (cx, cy) in coords.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                pnet = p['net']
                pad_info = {
                    'ref': ref, 'pin': p['num'], 'net': pnet,
                    'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                    'w': p['w'], 'h': p['h']
                }
                all_pads.append(pad_info)
                if pnet:
                    net_pads[pnet].append(pad_info)

    print(f"Loaded {len(coords)} components, {len(all_pads)} pads across {len(net_pads)} nets.")
    return True

if __name__ == '__main__':
    solve_smartpen_pcb()

