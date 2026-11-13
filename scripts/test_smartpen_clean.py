"""Test script for modular zero-error routing of SmartPen PCB."""
import json, sys, math
from pathlib import Path

sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

out_dir = Path("output/RevF_Working")

def build_pcb():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

    # 1. Extract pads
    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
            if not ref: continue
            orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
            pads = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pads.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(float(ptoks[4]) * 0.254, 4),
                        'h': round(float(ptoks[5]) * 0.254, 4)
                    })
            fp_defs[ref] = pads

    all_pads = []
    for ref, (cx, cy) in coords.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                all_pads.append({
                    'ref': ref, 'pin': p['num'], 'net': p['net'],
                    'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                    'w': p['w'], 'h': p['h']
                })

    segments = []
    vias = set()

    def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
        if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
            segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, net_name, width))

    def add_via(vx, vy, net_name):
        vias.add((round(vx, 3), round(vy, 3), net_name))

    print(f"Loaded {len(all_pads)} pads across {len(coords)} components.")
    return all_pads, segments, vias, add_seg, add_via

if __name__ == '__main__':
    all_pads, segments, vias, add_seg, add_via = build_pcb()
    errors = check_pcb_geometry(all_pads, segments, list(vias))
    print(f"Baseline pads check: {len(errors)} errors.")

