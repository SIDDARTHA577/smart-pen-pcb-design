import json, math

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

net_pads = {}
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet or pnet == 'GND': continue
            if pnet not in net_pads: net_pads[pnet] = []
            net_pads[pnet].append({'ref': ref, 'pin': p['num'], 'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4)})

print("=== CONNECTION DISTANCES ===")
short_conns = []
long_conns = []
for net, plist in sorted(net_pads.items()):
    plist_sorted = sorted(plist, key=lambda p: p['x'])
    for i in range(len(plist_sorted) - 1):
        p1 = plist_sorted[i]
        p2 = plist_sorted[i+1]
        dist = math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y'])
        dx = abs(p2['x'] - p1['x'])
        conn = (dist, net, p1, p2)
        if dist < 4.0:
            short_conns.append(conn)
        else:
            long_conns.append(conn)

print(f"Short connections (< 4 mm): {len(short_conns)}")
for dist, net, p1, p2 in sorted(short_conns):
    print(f"  {dist:5.2f} mm | {net:16s}: {p1['ref']}.{p1['pin']} -> {p2['ref']}.{p2['pin']}")

print(f"\nLong connections (>= 4 mm): {len(long_conns)}")
for dist, net, p1, p2 in sorted(long_conns):
    print(f"  {dist:5.2f} mm | {net:16s}: {p1['ref']}.{p1['pin']} -> {p2['ref']}.{p2['pin']}")
