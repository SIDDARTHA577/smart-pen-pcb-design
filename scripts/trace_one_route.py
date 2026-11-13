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
p2 = (79.20, 3.10)
nid = net_id_map['USB_CC2']
print("Running route_connection on USB_CC2...")
sx, sy = router.to_grid(p1[0], p1[1])
tx, ty = router.to_grid(p2[0], p2[1])
print(f"sx={sx}, sy={sy}, tx={tx}, ty={ty}")

# Check where it can go
for step in range(10):
    pass
path = router.route_connection(p1, p2, nid)
print("Path found:", path is not None)
