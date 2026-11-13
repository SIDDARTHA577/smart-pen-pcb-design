"""Diagnose the 12 failed connections."""
import json, math, sys
sys.path.insert(0, '.')
from scripts.fast_clean_pcb_router import FastPCBRouter

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

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

router = FastPCBRouter(84.0, 9.2, res=0.10)
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet: continue
            nid = net_id_map[pnet]
            router.add_pad(cx + p['dx'], cy + p['dy'], p['w'], p['h'], nid)

failed_cases = [
    ("USB_CC2", (73.6, 2.5), (79.2, 3.1)),
    ("USB_DM_PORT", (72.0, 6.9), (78.6, 3.1)),
    ("SD_MOSI", (41.1, 2.4), (58.7, 4.2)),
    ("USB_DP_CORE", (44.1, 7.2), (70.8, 5.8)),
    ("3V3_RF", (40.5, 5.6), (41.1, 7.2))
]

for net, p1, p2 in failed_cases:
    nid = net_id_map[net]
    s_gx, s_gy = router.to_grid(p1[0], p1[1])
    t_gx, t_gy = router.to_grid(p2[0], p2[1])
    
    # Check start neighbors
    s_free = [(dx, dy) for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)] if router.is_free(0, s_gx+dx, s_gy+dy, nid)]
    t_free = [(dx, dy) for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)] if router.is_free(0, t_gx+dx, t_gy+dy, nid)]
    print(f"\nNet {net}:")
    print(f"  Start ({p1[0]}, {p1[1]}) grid ({s_gx}, {s_gy}): free F.Cu neighbors = {s_free}")
    print(f"  Target ({p2[0]}, {p2[1]}) grid ({t_gx}, {t_gy}): free F.Cu neighbors = {t_free}")

