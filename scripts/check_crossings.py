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

# Check the X-intervals of long nets (span > 5 mm)
intervals = []
for net, plist in net_pads.items():
    xs = [p['x'] for p in plist]
    ys = [p['y'] for p in plist]
    if max(xs) - min(xs) >= 4.0:
        intervals.append({
            'net': net,
            'xmin': min(xs), 'xmax': max(xs),
            'ymin': min(ys), 'ymax': max(ys),
            'avg_y': sum(ys)/len(ys)
        })

print(f"Total long nets: {len(intervals)}")
# Sort by average Y
for item in sorted(intervals, key=lambda x: x['avg_y']):
    print(f"Net {item['net']:16s}: X in [{item['xmin']:5.1f}, {item['xmax']:5.1f}] (len {item['xmax']-item['xmin']:5.1f}) | avg Y = {item['avg_y']:.2f}")

