import json, csv

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

fp_defs = {}
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'):
                ref = sub.split('~')[10]
        if not ref:
            continue
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
                pnet = ptoks[7] if len(ptoks) > 7 else ''
                pnum = ptoks[8] if len(ptoks) > 8 else ''
                pads.append({
                    'num': pnum, 'net': pnet,
                    'dx': round(dx, 4), 'dy': round(dy, 4),
                    'w': round(pw, 4), 'h': round(ph, 4)
                })
        fp_defs[ref] = pads

net_pads = {}
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet: continue
            if pnet not in net_pads: net_pads[pnet] = []
            net_pads[pnet].append({'ref': ref, 'pin': p['num'], 'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4), 'w': p['w'], 'h': p['h']})

print('Total nets:', len(net_pads))
for net, plist in sorted(net_pads.items()):
    xs = [p['x'] for p in plist]
    span = max(xs) - min(xs)
    print(f'{net:16s}: {len(plist):2d} pads, X min={min(xs):6.2f}, max={max(xs):6.2f}, span={span:6.2f} mm')

