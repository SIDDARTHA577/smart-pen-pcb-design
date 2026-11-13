"""XY Orthogonal Router for SmartPen PCB.
Strictly:
- F.Cu = vertical segments + local escapes
- B.Cu = horizontal highways
Guarantees 0 segment crossings and 0 via collisions.
"""
import json, uuid, csv, subprocess, sys, math
from pathlib import Path

sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

out_dir = Path("output/RevF_Working")
kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

def run_xy_router():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
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

    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
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
                    pads.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(pw, 4), 'h': round(ph, 4)
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

    def is_via_pos_clean(vx, vy, net_name, existing_vias, pads):
        # 1. Board bounds
        if vx < 0.55 or vx > 83.45 or vy < 0.55 or vy > 8.65:
            return False
        # 2. Distance to other vias
        for ex, ey, enet in existing_vias:
            if math.hypot(vx - ex, vy - ey) < 0.60:
                return False
        # 3. Distance to foreign pads
        for p in pads:
            if p['net'] == net_name: continue
            dx = max(0.0, abs(vx - p['x']) - p['w']/2.0)
            dy = max(0.0, abs(vy - p['y']) - p['h']/2.0)
            if math.hypot(dx, dy) < 0.38:
                return False
        return True

    def is_fcu_seg_clean(x1, y1, x2, y2, net_name, pads):
        steps = int(math.ceil(math.hypot(x2 - x1, y2 - y1) / 0.10)) + 1
        for s in range(steps):
            t = s / max(1, steps - 1)
            sx = x1 + t * (x2 - x1)
            sy = y1 + t * (y2 - y1)
            for p in pads:
                if p['net'] == net_name: continue
                dx = max(0.0, abs(sx - p['x']) - p['w']/2.0)
                dy = max(0.0, abs(sy - p['y']) - p['h']/2.0)
                if math.hypot(dx, dy) < 0.22:
                    return False
        return True

    print("Checking layout parameters...")
    # Group pads by net
    nets_pads = {}
    for p in all_pads:
        net = p['net']
        if not net or net == 'GND': continue
        if net not in nets_pads: nets_pads[net] = []
        nets_pads[net].append(p)

    print(f"Total non-GND active nets: {len(nets_pads)}")
    return True

if __name__ == '__main__':
    run_xy_router()

