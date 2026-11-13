import json, time, sys
sys.path.insert(0, '.')
from scripts.clean_pcb_router import CleanPCBRouter

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

router = CleanPCBRouter(84.0, 9.2, res=0.10)
net_pads = {}
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet: continue
            nid = net_id_map[pnet]
            router.add_pad(cx + p['dx'], cy + p['dy'], p['w'], p['h'], nid)
            if pnet not in net_pads: net_pads[pnet] = []
            net_pads[pnet].append({'ref': ref, 'pin': p['num'], 'x': cx + p['dx'], 'y': cy + p['dy']})

# Sort nets: short local nets first, long bus nets, then power nets
non_gnd_nets = [n for n in sorted_nets if n and n != 'GND']

def net_rank(n):
    if n == '3V3': return 1000
    if n == '3V3_RF': return 900
    if n == 'USB_VBUS': return 800
    plist = net_pads[n]
    xs = [p['x'] for p in plist]
    return max(xs) - min(xs)

sorted_nets_by_rank = sorted(non_gnd_nets, key=net_rank)

print(f"Routing {len(sorted_nets_by_rank)} nets...")
t0 = time.time()
success = 0
failed = 0
paths_by_net = {}

for net in sorted_nets_by_rank:
    plist = sorted(net_pads[net], key=lambda p: p['x'])
    nid = net_id_map[net]
    net_paths = []
    net_ok = True
    for i in range(len(plist) - 1):
        p1 = (plist[i]['x'], plist[i]['y'])
        p2 = (plist[i+1]['x'], plist[i+1]['y'])
        path = router.route_segment(p1, p2, nid)
        if path:
            router.commit_path(path, nid)
            net_paths.append(path)
        else:
            net_ok = False
            print(f"  FAILED segment {i} of {net}: ({p1[0]:.2f}, {p1[1]:.2f}) -> ({p2[0]:.2f}, {p2[1]:.2f})")
            break
    if net_ok:
        success += 1
        paths_by_net[net] = net_paths
    else:
        failed += 1

print(f"\nDone in {time.time()-t0:.2f}s: {success} succeeded, {failed} failed.")

