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

all_pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            all_pads.append({
                'ref': ref, 'pin': p['num'], 'net': pnet,
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

def is_segment_clear_on_fcu(x1, y1, x2, y2, my_net):
    # Check if line segment (x1, y1) to (x2, y2) with width 0.20 mm is >= 0.15 mm from foreign pads
    tr_r = 0.10 + 0.15 # 0.25 mm
    for pad in all_pads:
        if pad['net'] == my_net: continue
        px, py, pw, ph = pad['x'], pad['y'], pad['w'], pad['h']
        # Distance from segment to rectangle
        # Sample 20 points along segment
        for step in range(21):
            t = step / 20.0
            sx = x1 + t * (x2 - x1)
            sy = y1 + t * (y2 - y1)
            dx = max(0.0, abs(sx - px) - pw/2.0)
            dy = max(0.0, abs(sy - py) - ph/2.0)
            if math.hypot(dx, dy) < tr_r:
                return False
    return True

net_pads = {}
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet or pnet == 'GND': continue
            if pnet not in net_pads: net_pads[pnet] = []
            net_pads[pnet].append({'ref': ref, 'pin': p['num'], 'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4)})

clear_fcu_direct = 0
total_conns = 0
for net, plist in net_pads.items():
    plist_sorted = sorted(plist, key=lambda p: p['x'])
    for i in range(len(plist_sorted) - 1):
        total_conns += 1
        p1 = plist_sorted[i]
        p2 = plist_sorted[i+1]
        dist = math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y'])
        # Check direct or L-shape
        direct = is_segment_clear_on_fcu(p1['x'], p1['y'], p2['x'], p2['y'], net)
        l1 = is_segment_clear_on_fcu(p1['x'], p1['y'], p2['x'], p1['y'], net) and is_segment_clear_on_fcu(p2['x'], p1['y'], p2['x'], p2['y'], net)
        l2 = is_segment_clear_on_fcu(p1['x'], p1['y'], p1['x'], p2['y'], net) and is_segment_clear_on_fcu(p1['x'], p2['y'], p2['x'], p2['y'], net)
        if direct or l1 or l2:
            clear_fcu_direct += 1
            print(f"CLEAN F.Cu: {net:16s} ({dist:.2f} mm): {p1['ref']}.{p1['pin']} -> {p2['ref']}.{p2['pin']}")

print(f"\nResult: {clear_fcu_direct} / {total_conns} connections can be routed DIRECTLY on F.Cu without any vias!")

