import json, sys
sys.path.insert(0, '.')

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]
coords['C10'] = [73.90, 1.50]
coords['R6'] = [74.04, 2.46]
coords['U_ESD'] = [71.80, 4.49]
coords['R7'] = [72.50, 6.85]
coords['R8'] = [72.48, 7.70]
coords['R5'] = [70.20, 7.70]

with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

fp_defs = {}
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
        if not ref: continue
        orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
        pads_sub = []
        for sub in subs:
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                dx = (float(ptoks[2]) - orig_x) * 0.254
                dy = (float(ptoks[3]) - orig_y) * 0.254
                pads_sub.append({
                    'num': ptoks[8], 'net': ptoks[7],
                    'dx': round(dx, 4), 'dy': round(dy, 4),
                    'w': round(float(ptoks[4]) * 0.254, 4),
                    'h': round(float(ptoks[5]) * 0.254, 4)
                })
        fp_defs[ref] = pads_sub

for p in fp_defs['R9']:
    p['dx'], p['dy'] = p['dy'], p['dx']
    p['w'], p['h'] = p['h'], p['w']

pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pads.append({
                'ref': ref, 'pin': p['num'], 'net': p['net'],
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

# Check vertical corridors on F.Cu for Y in [0.6, 7.0]
# Width of trace = 0.18, clearance = 0.13 -> clearance zone = 0.18/2 + 0.13 = 0.22 mm
print("Scanning for clear vertical corridors between X = 68.0 and 74.0 for Y in [0.6, 7.0]...")
for test_x_int in range(680, 740, 5):
    tx = test_x_int / 10.0
    blocked = []
    for p in pads:
        # Check if pad overlaps with vertical line at tx with width 0.18 + clearance 0.13
        if abs(p['x'] - tx) < (p['w']/2.0 + 0.22):
            if not (p['y'] + p['h']/2.0 < 0.6 or p['y'] - p['h']/2.0 > 7.0):
                blocked.append(f"{p['ref']}.{p['pin']} at ({p['x']:.2f},{p['y']:.2f})")
    if not blocked:
        print(f"  CLEAN CORRIDOR found at X = {tx:.2f}!")
    else:
        # print first blocker
        pass

