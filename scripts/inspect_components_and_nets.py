import json, csv

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)
with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
    parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

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

print("=== COMPONENTS ALONG X ===")
for ref, (x, y) in sorted(coords.items(), key=lambda item: item[1][0]):
    part_type = parts_audit.get(ref, {}).get('Description', '')
    pad_count = len(fp_defs.get(ref, []))
    print(f"{ref:8s}: X={x:6.2f}, Y={y:6.2f} | {pad_count:2d} pads | {part_type[:30]}")

print("\n=== NETS AND THEIR CONNECTED PADS ===")
net_pads = {}
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pnet = p['net']
            if not pnet: continue
            if pnet not in net_pads: net_pads[pnet] = []
            net_pads[pnet].append({
                'ref': ref, 'pin': p['num'],
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

for net, plist in sorted(net_pads.items()):
    if net == 'GND': continue
    print(f"\nNet {net} ({len(plist)} pads):")
    for p in sorted(plist, key=lambda x: x['x']):
        print(f"  {p['ref']}.{p['pin']} at ({p['x']:.2f}, {p['y']:.2f})")

