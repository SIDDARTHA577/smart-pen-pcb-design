import json, sys
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

p1 = (73.56, 2.46)
sx, sy = router.to_grid(p1[0], p1[1])
nid = net_id_map['USB_CC2']

print(f"R6.1 is at ({p1[0]}, {p1[1]}), grid ({sx}, {sy})")
# Check how far F.Cu can walk from (sx, sy)
visited_f = set()
q = [(sx, sy)]
while q:
    cx, cy = q.pop(0)
    if (cx, cy) in visited_f: continue
    visited_f.add((cx, cy))
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = cx + dx, cy + dy
        if (nx, ny) not in visited_f and router.is_free(0, nx, ny, nid):
            q.append((nx, ny))

print(f"Total reachable cells on F.Cu from R6.1: {len(visited_f)}")
xs = [c[0] for c in visited_f]
ys = [c[1] for c in visited_f]
print(f"X range: {min(xs)}..{max(xs)} ({min(xs)*0.1:.2f}..{max(xs)*0.1:.2f} mm)")
print(f"Y range: {min(ys)}..{max(ys)} ({min(ys)*0.1:.2f}..{max(ys)*0.1:.2f} mm)")

legal_vias_in_reachable = [c for c in visited_f if router.is_via_legal(c[0], c[1], nid)]
print(f"Legal vias inside reachable F.Cu area: {len(legal_vias_in_reachable)}")

